#!/usr/bin/env -S uv run --script
# /// script
# name = "python-datasworn"
# version = "0.1.0"
# description = "Datasworn Python packages"
# readme = "README.md"
# requires-python = ">=3.14"
# dependencies = [
#     "datamodel-code-generator[debug,http]==0.52.2",
#     "rich>=14.2.0",
#     "typer>=0.21.1",
# ]
# ///

import json
import logging
import re
import shutil
import string
from pathlib import Path
from typing import Any

import tomllib
from datamodel_code_generator import (
    InputFileType,
    PythonVersion,
    TargetPydanticVersion,
    generate,
)
from datamodel_code_generator.config import JSONSchemaParserConfig
from datamodel_code_generator.enums import DataModelType
from datamodel_code_generator.format import Formatter
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from rich import print
from rich.logging import RichHandler
from typer import Typer

REGEX = r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"

FORMAT = "%(message)s"
log = logging.getLogger(__name__)

PKG_ROOT = Path(__file__).parent  # / "pkg" / "python"
ROOT_OUTPUT = Path(__file__).parent.parent.parent / "datasworn"
VERSION = "0.1.0"

PKG_SCOPE_OFFICIAL = "datasworn"
PKG_SCOPE_COMMUNITY = "datasworn-community-content"

PKG_CONFIG = {
    "classic": {"scope": PKG_SCOPE_OFFICIAL},
    "delve": {"scope": PKG_SCOPE_OFFICIAL},
    "starforged": {"scope": PKG_SCOPE_OFFICIAL},
    "sundered_isles": {"scope": PKG_SCOPE_OFFICIAL},
    "ancient_wonders": {"scope": PKG_SCOPE_COMMUNITY},
    "fe_runners": {"scope": PKG_SCOPE_COMMUNITY},
    "starsmith": {"scope": PKG_SCOPE_COMMUNITY},
}

app = Typer()


def snake(name: str):
    return re.sub(r"[-]+", "_", name).lower()


def read(script: str) -> dict[str, Any]:
    """
    Read script metadata https://peps.python.org/pep-0723/
    """

    name = "script"
    matches = list(
        filter(lambda m: m.group("type") == name, re.finditer(REGEX, script))
    )
    content = "".join(
        line[2:] if line.startswith("# ") else line[1:]
        for line in matches[0].group("content").splitlines(keepends=True)
    )
    return tomllib.loads(content)


def copy_json(dry_run: bool, force: bool, log_level: str) -> None:
    """
    Copy Datasworn Output JSON Files to Python Package
    """

    log.info(__doc__)
    log.info(f"PKG_ROOT: {PKG_ROOT}\nROOT_OUTPUT: {ROOT_OUTPUT}\n")

    for pkg in PKG_CONFIG:
        log.info(f"Copying {pkg} JSON...")
        pkg_config = PKG_CONFIG[pkg]
        scope = pkg_config["scope"]
        sscope = snake(scope)
        pkg_root = PKG_ROOT / scope / "src" / scope / pkg / "src" / sscope / pkg
        pkg_json_dest = pkg_root / "json"
        json_src = ROOT_OUTPUT / pkg / f"{pkg}.json"

        if json_src.is_file():
            log.info(f"Source ok: {json_src}")
        else:
            log.error(f"Source missing: {json_src}")
            continue

        if not pkg_json_dest.is_dir():
            if not args.dry_run:
                pkg_json_dest.mkdir(exist_ok=True, parents=True)
            else:
                log.info(f"Would create\n{pkg_json_dest}")

            if args.force:
                for f in pkg_json_dest.iterdir():
                    if not args.dry_run:
                        f.unlink()
                    else:
                        log.info(f"Would delete\n{f}")

        if not args.dry_run:
            shutil.copy(json_src, pkg_json_dest)
        else:
            log.info(f"Copy to\n{pkg_json_dest}")

        # log.info("Building package...")
        # build_content_package(pkg_config)


def fix_schema(path: Path, dry_run: bool) -> Path:
    """
    Apply some fixes to Datasworn JSON schema.
    """

    def _parse_allof(node: list[Any], parents: str = "") -> dict[str, Any]:
        """
        Convert allOf with if/then discriminators to oneOf with discriminator mapping.

        Example:
              "discriminator": {
            "propertyName": "field_type",
            "mapping": {
              "clock": "#/definitions/ClockField",
              "counter": "#/definitions/CounterField",
              "checkbox": "#/definitions/AssetCheckboxField",
              "text": "#/definitions/TextField"
            }
          },
          "oneOf": [
            {
              "$ref": "#/definitions/ClockField"
            },
            {
              "$ref": "#/definitions/CounterField"
            },
            {
              "$ref": "#/definitions/AssetCheckboxField"
            },
            {
              "$ref": "#/definitions/TextField"
            }
          ]
        """

        property = ""
        mapping = {}
        oneOf: list[Any] = []
        for subnode in node:
            if subnode.get("if", None):
                if not property:
                    property = list(subnode["if"]["properties"].keys())[0]
                    log.debug(
                        f"{parents!r}: Found discriminator on property '{property}'"
                    )
                value = subnode["if"]["properties"][property]["const"]
                try:
                    ref = subnode["then"]["$ref"]
                except KeyError as exc:
                    log.exception(exc)
                    log.warning(f"{parents!r}: Skip 'allOf'")
                    return {"allOf": node}
                mapping[value] = ref
                oneOf.append(subnode["then"])
                log.debug(f"{parents!r}: Mapping '{value}' --> '{ref}'")
            else:
                log.warning(f"{parents!r}: Skip 'allOf'")
                return {"allOf": node}
        log.info(f"{parents!r}: Converted allOf to oneOf with {len(node)} subnodes")
        return {
            "discriminator": {"propertyName": property, "mapping": mapping},
            "oneOf": oneOf,
        }

    def _parse(node: Any, parents: str = "") -> Any:
        log.debug(f"Parsing {parents}")
        # result: list[Any] | dict[string, Any]

        match node:
            case list():
                result: list[Any] = []
                for i, subnode in enumerate(node):
                    result.append(_parse(subnode, parents=f"{parents}[{i}]"))

            case {"allOf": subnode}:
                node_ = node.copy()
                if parents in (
                    ".definitions.DelveSite.properties.denizens",
                    ".definitions.DelveSiteDomain.properties.features",
                    ".definitions.DelveSiteDomain.properties.dangers",
                    ".definitions.DelveSiteTheme.properties.features",
                    ".definitions.DelveSiteTheme.properties.dangers",
                ):
                    result = {"oneOf": subnode}
                    log.info(f"{parents!r}: Converted 'allOf' to 'oneOf'")
                else:
                    node_.pop("allOf")
                    result = node_ | _parse_allof(subnode, parents=parents)

            case {"type": "string"}:
                node_ = node.copy()
                if format_ := node_.pop("format", None):
                    log.info(f"{parents!r}: Removed format {format_!r}")
                # if pattern_ := node_.pop("pattern", None):
                # log.info(f"{parents!r}: Removed pattern {pattern_!r}")
                result = node_

            case dict():
                result: dict[str, Any] = {}
                for key, subnode in node.items():
                    result[key] = _parse(subnode, parents=f"{parents}.{key}")
                # result.pop("pattern", None)
                # result.pop("description", None)
                result.pop("examples", None)
                result.pop("minimum", None)
                result.pop("multipleOf", None)
                result.pop("$schema", None)

            case _:
                result = node
        return result

    with path.open("r", encoding="utf-8") as f:
        schema = json.loads(f.read())
        output = Path(__file__).parent / "datasworn-fix.schema.json"
        if not dry_run:
            output.write_text(json.dumps(_parse(schema), indent=2), encoding="utf-8")
            log.info(f"Fixed schema written to {output}")
        else:
            log.info(f"Would write fixed schema to {output}")
        return output


def build_core_package(
    jsonschema: Path,
    dry_run: bool = True,
    force: bool = False,
):
    log.info("Generating Pydantic models...")

    output = (
        PKG_ROOT
        / "datasworn"
        / "src"
        / "datasworn"
        / "core"
        / "src"
        / "datasworn"
        / "core"
        / "models.py"
    )

    data_model_types = get_data_model_types(
        DataModelType.PydanticV2BaseModel,
        PythonVersion.PY_312,
    )
    log.debug(data_model_types)

    # parser_config = Config(  # JSONSchemaParserConfig(
    # --- JSON Schema Parser Options--------------------------------------------------
    # data_model_type=data_model_types.data_model,
    # data_model_root_type=data_model_types.root_model,
    # data_model_field_type=data_model_types.field_model,
    # data_type_manager_type=data_model_types.data_type_manager,
    # dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
    result = generate(
        # --- Base Options --------------------------------------------------------------
        jsonschema,
        input_file_type=InputFileType.JsonSchema,
        # --- Model Customization --------------------------------------------------------
        extra_fields="allow",
        # allow_population_by_field_name=True,
        collapse_reuse_models=True,
        # collapse_root_models=True,
        # collapse_root_models_name_strategy="parent",
        keep_model_order=True,
        # model_extra_keys=True, (not present for JSON Schema?)
        # naming_strategy="parent-prefixed", # leads to super long names...
        output_model_type=DataModelType.PydanticV2BaseModel,
        reuse_model=True,
        # skip_root_model=True,
        strict_nullable=True,
        # strip_default_none=True,
        target_pydantic_version=TargetPydanticVersion.V2_11,
        target_python_version=PythonVersion.PY_312,
        # union_mode=UnionMode.smart,
        # union_mode=UnionMode.left_to_right,
        # use_default=True,  # -- not present for JSON Schema?
        use_default_kwarg=True,
        use_frozen_field=True,
        # use_default_factory_for_optional_nested_models=True,
        use_generic_base_class=True,
        use_one_literal_as_default=True,
        # use_subclass_enum=True, # using only string enums
        # # --- Field Customization --------------------------------------------------------
        # aliases - rename from file
        capitalise_enum_members=True,
        # default_values - override from JSON file
        field_constraints=True,
        field_extra_keys=set("rollable"),
        # field_include_all_keys=True, (makes file huge by including everything)
        # field_type_collision_strategy="rename-type",
        remove_special_field_name_prefix=True,
        set_default_enum_member=True,
        snake_case_field=True,
        # special_field_name_prefix="",
        use_attribute_docstrings=True,
        # use_enum_values_in_discriminator=True,
        # use_field_description=True,
        # use_field_description_example=True,
        # use_inline_field_description=True,
        use_schema_description=True,
        use_title_as_name=True,
        # --- Typing Customization --------------------------------------------------------
        # allof_class_hierarchy="never",
        allof_merge_mode="none",
        enum_field_as_literal="all",
        # enum_field_as_literal_map (override from JSON file)
        # ignore_enum_constraints=True,
        # output_datetime_class
        # strict_types=True,
        use_annotated=True,
        use_generic_container_types=True,
        use_root_model_type_alias=True,  #  (does not exist for JSONSchemaParserConfig?)
        # use_specialized_enum=True,
        use_standard_collections=True,
        use_standard_primitive_types=True,
        use_tuple_for_fixed_items=True,
        use_type_alias=True,
        use_union_operator=True,
        use_unique_items_as_set=True,
        # --- Template Customization ------------------------------------------------------
        # disable_appending_item_suffix=True,
        # enable_command_header=True,
        # enable_version_header=True,
        formatters=[Formatter.RUFF_FORMAT, Formatter.RUFF_CHECK],
        treat_dot_as_module=False,
        # validators={
        #     "DelveSite": {
        #         "validators": [
        #             {
        #                 "field": "denizens",
        #                 "function": "pydantic.SkipValidation",
        #                 "mode": "plain",
        #             }
        #         ]
        #     }
        # },
        wrap_string_literal=True,
        # --- General Options -----------------------------------------------------------
        # module_split_mode="recursive",
        # debug=True,
    )
    # log.debug(JSONSchemaParserConfig)

    # parser = JsonSchemaParser(
    #     jsonschema,
    #     config=parser_config,
    #     # data_model_types=data_model_types,
    # )

    # result = parser.parse()

    # remaining problems to fix up manually:
    #  - DelveSite.denizens = Denizens # should be list[Denizens]
    #  - DelveSiteTheme.features = Features # should be list[Features]
    #  - DelveSiteTheme.dangers = Dangers # should be list[Dangers]
    #  - DelveSiteDomain.features = Features # should be list[Features]
    #  - DelveSiteDomain.dangers = Dangers # should be list[Dangers]

    log.info(
        f"Pydantic models generated: {result.count('\n')} lines, {result.count('\nclass ')} classes."
    )

    if dry_run:
        # print(Syntax(result, "python"))
        print("would write to", output)
    else:
        with open(output, "w") as f:
            log.info(f"Writing {output}")
            f.write(result)


@app.command()
def main(
    dry_run: bool = False,
    force: bool = False,
    log_level: str = "info",
):
    """Datasworn Python package builder

    This script builds the core Python package using `datamodel-codegen` in two steps:

    1. Generate modified JSON schema to produce correct Pydantic models.
    2. Use `datamodel-codegen` to generate Pydantic models.
    """
    log.info("Dry Run: %s" % dry_run)
    log.info("Force: %s" % force)

    logging.basicConfig(
        level=log_level.upper(), format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    if log_level != "info":
        log.info(f"Log level set to {log_level.upper()}")

    with open(__file__) as f:
        script = read(f.read())
        log.info("Script metadata:")
        print(script)

    # copy_json(args)
    json_schema = ROOT_OUTPUT / "datasworn.schema.json"
    fixed_json_schema = fix_schema(json_schema, dry_run=dry_run)

    build_core_package(fixed_json_schema, dry_run=dry_run, force=force)


if __name__ == "__main__":
    app()
