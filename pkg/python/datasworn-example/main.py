from importlib.resources import files
from typing import Any

from datasworn.core.models import (
    Expansion,
    OracleTableText,
    Ruleset,
)
from pydantic import BaseModel
from rich import print
from rich.console import Console
from rich.traceback import install

console = Console(force_terminal=True, color_system="truecolor")

install(show_locals=True)
datasworn_tree = {}

DATASWORN_JSON_SOURCES = {
    "classic": ("datasworn", Ruleset),
    "delve": ("datasworn", Expansion),
    "starforged": ("datasworn", Ruleset),
    "sundered_isles": ("datasworn", Expansion),
    "ancient_wonders": ("datasworn_community_content", Expansion),
    "fe_runners": ("datasworn_community_content", Expansion),
    "starsmith": ("datasworn_community_content", Expansion),
}


def _load_sources():
    for name in DATASWORN_JSON_SOURCES:
        scope, type_ = DATASWORN_JSON_SOURCES[name]
        json_source = files(f"{scope}.{name}").joinpath(f"json/{name}.json").read_text()
        datasworn_tree[name] = type_.model_validate_json(json_source)
        # datasworn_tree[name] = pydantic_core.from_json(json_source)


def _walk_model(
    name: str,
    obj: Any,
    level: int = 0,
    max_level: int | None = None,
    max_string: int = 80,
    max_items: int | None = 10,
):
    if max_level is not None and level > max_level:
        print(f"{' ':{level}}[dim white]...[/]")
        return
    match obj:
        case BaseModel():
            _id = getattr(obj, "id", None)
            print(
                f"{' ':{level}}[bright_yellow]{name}[/] <{obj.__class__.__name__}> {f'[cyan] <-- {_id}[/]' if _id else ''}"
            )
            for k, v in obj:
                _walk_model(k, v, level + 2)
        case dict():
            if len(obj) == 0:
                print(f"{' ':{level}}[dim yellow]{name} {{}}[/]")
                return
            _id = obj.get("_id", None)
            print(
                f"{' ':{level}}[bright_yellow]{name}[/] {{}} {f'<-- [blue]{_id}[/]' if _id else ''}"
            )
            for k, v in obj.items():
                _walk_model(k, v, level + 2)
        case list():
            if len(obj) == 0:
                print(f"{' ':{level}}[dim yellow]{name} [][/]")
                return
            print(f"{' ':{level}}[bright_yellow]{name}[/] []")
            for i, v in enumerate(obj):
                if max_items is not None and i >= max_items:
                    print(f"{' ':{level + 2}}[dim white]...[/]")
                    break
                _walk_model(f"[{i}]", v, level + 2)
        case str():
            print(
                f"{' ':{level}}[yellow]{name}[/]="
                f"{f'{obj[:max_string]!r}...' if len(obj) > max_string else f'{obj!r}'}"
            )
        case _:
            if obj:
                print(f"{' ':{level}}[yellow]{name}[/]={obj!r}")
            else:
                print(f"{' ':{level}}[dim yellow]{name}[/]=[dim]{obj!r}[/]")


def _get_example_oracle():
    role = datasworn_tree["starforged"].oracles["character"].contents["role"]
    oracle = OracleTableText(
        **role.model_dump() | {"oracle_type": role.oracle_type.name}
    )
    print(oracle)


if __name__ == "__main__":
    _load_sources()

    for key in datasworn_tree:
        console.rule(f"[bold green] Datasworn Package: {key} [/]")
        # _walk_model(key, datasworn_tree[key], max_level=5)
        console.print(datasworn_tree[key])