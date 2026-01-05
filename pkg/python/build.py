#!/usr/bin/env -S uv run --script
# /// script
# name = "python-datasworn"
# version = "0.1.0"
# description = "Datasworn Python packages"
# readme = "README.md"
# requires-python = ">=3.14"
# dependencies = [
#     "datamodel-code-generator[debug,http]==0.52.1",
#     "rich>=14.2.0",
# ]
# ///

import argparse
import enum
import json
import logging
import re
import shutil
from ctypes import Union
from email.policy import strict
from encodings.punycode import T
from pathlib import Path
from typing import Any

import tomllib
from datamodel_code_generator import (
    DataModelType,
    Formatter,
    InputFileType,
    PythonVersion,
    YamlValue,
    # UnionMode,
    generate,
)
from datamodel_code_generator.config import JSONSchemaParserConfig
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.model.pydantic_v2 import UnionMode
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from rich import print
from rich.logging import RichHandler
from rich.syntax import Syntax

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


def snake(name: str):
    return re.sub(r"[-]+", "_", name).lower()


def read(script: str) -> dict[str, Any]:
    """Read script metadata https://peps.python.org/pep-0723/"""
    name = "script"
    matches = list(
        filter(lambda m: m.group("type") == name, re.finditer(REGEX, script))
    )
    content = "".join(
        line[2:] if line.startswith("# ") else line[1:]
        for line in matches[0].group("content").splitlines(keepends=True)
    )
    return tomllib.loads(content)


def copy_json(args):
    print(args)
    log.info("Datasworn Python package builder")
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


def fix_schema(path: Path):
    def _parse_allof(node) -> list[Any]:
        result = []
        for i, subnode in enumerate(node):
            then = subnode.get("then")
            if then:
                result.append(then)
            else:
                result.append(subnode)
        return result

    def _parse(node) -> Any:
        match node:
            case list():
                result = []
                for i, subnode in enumerate(node):
                    result.append(_parse(subnode))
            case {"allOf": subnode}:
                result = {"oneOf": _parse_allof(subnode)}
                log.info(f"Converted allOf to oneOf with {len(subnode)} subnodes")
            case dict():
                result = {}
                for key, subnode in node.items():
                    result[key] = _parse(subnode)
                result.pop("pattern", None)
                result.pop("description", None)
                result.pop("examples", None)
                result.pop("minimum", None)
                result.pop("multipleOf", None)
                result.pop("$schema", None)
            case _:
                result = node
        return result

    with path.open("r", encoding="utf-8") as f:
        schema = json.loads(f.read())
        output = Path(path.parent / "datasworn-fix.schema.json")
        output.write_text(json.dumps(_parse(schema)))
        return output


def build_core_package(args):
    log.info("Generating Pydantic models...")

    json_schema = ROOT_OUTPUT / "datasworn.schema.json"
    # json_schema = Path(Path(__file__).parent / "datasworn-fix.schema.json")
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
    print(data_model_types)

    parser_config = JSONSchemaParserConfig(
        # --- JSON Schema Parser Options--------------------------------------------------
        data_model_type=data_model_types.data_model,
        data_model_root_type=data_model_types.root_model,
        data_model_field_type=data_model_types.field_model,
        data_type_manager_type=data_model_types.data_type_manager,
        dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
        # result = generate(
        # --- Base Options --------------------------------------------------------------
        # json_schema,
        # input_file_type=InputFileType.JsonSchema,
        # --- Model Customization --------------------------------------------------------
        collapse_reuse_models=True,
        # collapse_root_models=True,
        # collapse_root_models_name_strategy="parent",
        keep_model_order=True,
        # naming_strategy="parent-prefixed",
        # output_model_type=DataModelType.PydanticV2BaseModel,
        reuse_model=True,
        # skip_root_model=True,
        # strict_nullable=True,
        target_pydantic_version="2.11",
        target_python_version=PythonVersion.PY_312,
        # union_mode=UnionMode.smart,
        # union_mode=UnionMode.left_to_right,
        # use_default=True,
        # use_default_factory_for_optional_nested_models=True,
        use_generic_base_class=True,
        use_one_literal_as_default=True,
        use_subclass_enum=True,
        # # --- Field Customization --------------------------------------------------------
        # aliases - rename from file
        capitalise_enum_members=True,
        # default_values - override from JSON file
        extra_fields="allow",
        field_constraints=True,
        # field_include_all_keys=True, # makes file huge by including everything
        # field_type_collision_strategy="rename-type",
        # remove_special_field_name_prefix=True,
        set_default_enum_member=True,
        snake_case_field=True,
        special_field_name_prefix="",
        use_attribute_docstrings=True,
        # use_enum_values_in_discriminator=True,
        use_field_description=True,
        # use_field_description_example=True,
        # use_inline_field_description=True,
        use_schema_description=True,
        use_title_as_name=True,
        # --- Typing Customization --------------------------------------------------------
        # allof_class_hierarchy="always",
        allof_merge_mode="none",
        enum_field_as_literal="all",
        # enum_field_as_literal_map --- override from JSON file
        # ignore_enum_constraints=True,
        # output_datetime_class
        # strict_types=True,
        # type_overrides={
        # "DelveSite.denizens": "list[Denizens]",
        # "DelveSiteTheme.features": "list[Feature]",
        # "DelveSiteTheme.dangers": "list[Danger]",
        # "DelveSiteDomain.features": "list[Feature]",
        # "DelveSiteDomain.dangers": "list[Danger]",
        # },
        use_generic_container_types=True,
        # use_root_model_type_alias=True, # does not respect constraints
        use_specialized_enum=True,
        use_standard_collections=True,
        use_tuple_for_fixed_items=True,
        # use_type_alias=True,
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

    schema = fix_schema(json_schema)
    log.info(f"Fixed schema written to {schema}")
    parser = JsonSchemaParser(
        schema,
        config=parser_config,
        # data_model_types=data_model_types,
    )

    result = parser.parse()

    # remaining problems to fix up manually:
    #  - DelveSite.denizens = Denizens # should be list[Denizens]
    #  - DelveSiteTheme.features = Features # should be list[Features]
    #  - DelveSiteTheme.dangers = Dangers # should be list[Dangers]
    #  - DelveSiteDomain.features = Features # should be list[Features]
    #  - DelveSiteDomain.dangers = Dangers # should be list[Dangers]

    log.info(
        f"Pydantic models generated: {result.count('\n')} lines, {result.count('\nclass ')} classes."
    )

    if args.dry_run:
        # print(Syntax(result, "python"))
        print("would write to", output)
    else:
        with open(output, "w") as f:
            log.info(f"Writing {output}")
            f.write(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Datasworn Python package builder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--log-level", default="info", help="Logging level")
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level.upper(),
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )

    with open(__file__) as f:
        script = read(f.read())
        print(script)

    # copy_json(args)
    build_core_package(args)
