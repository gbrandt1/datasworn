from encodings.punycode import T
from importlib.resources import files
from tkinter import N
from typing import Any

from datasworn.core.models import (
    Expansion,
    OracleTableText,
    Ruleset,
)
from pydantic import BaseModel, RootModel
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
    # *,
    # max_level: int | None = None,
    # max_string: int | None = None,
    # max_items: int | None = None,
    # show_none: bool | None = False,
):
    def _indent():
        return " " * level * 4

    if _walk_model._max_level is not None and level > _walk_model._max_level:
        # print(f"{_indent()}[dim white]{name} ...[/]")
        return

    match obj:
        case RootModel():
            print(
                f"{_indent()}[orange1]{name}[/] <{obj.__class__.__name__}> "
                f"{repr(obj.root)[: _walk_model._max_string]}"
                f"{'...' if _walk_model._max_string and len(repr(obj.root)) > _walk_model._max_string else ''}"
            )
        case BaseModel():
            _id = getattr(obj, "id", None)
            print(
                f"{_indent()}[bright_yellow]{name}[/] <{obj.__class__.__name__}> {f'[cyan] <-- {_id}[/]' if _id else ''}"
            )
            for k, v in obj:
                _walk_model(k, v, level + 1)
        case dict():
            if len(obj) == 0:
                print(f"{_indent()}[dim yellow]{name} {{}}[/]")
                return
            _id = obj.get("_id", None)
            print(
                f"{_indent()}[bright_yellow]{name}[/] {{}} {f'<-- [blue]{_id}[/]' if _id else ''}"
            )
            for k, v in obj.items():
                _walk_model(k, v, level + 1)
        case list():
            if len(obj) == 0:
                print(f"{_indent()}[dim yellow]{name} [][/]")
                return
            print(f"{_indent()}[bright_yellow]{name}[/] []")
            for i, v in enumerate(obj):
                if _walk_model._max_items is not None and i >= _walk_model._max_items:
                    print(f"{_indent()}[dim white]...[/]")
                    break
                _walk_model(f"[{i}]", v, level + 1)
        case str():
            if _walk_model._max_string:
                print(
                    f"{_indent()}[yellow]{name}[/]="
                    f"{f'{obj[: _walk_model._max_string]!r}...' if len(obj) > _walk_model._max_string else f'{obj!r}'}"
                )
            else:
                print(f"{_indent()}[yellow]{name}[/]={obj!r}")
        case _:
            if obj:
                print(f"{' ':{level}}[yellow]{name}[/]={obj!r}")
            elif _walk_model._show_none:
                print(f"{' ':{level}}[dim yellow]{name}[/]=[dim]{obj!r}[/]")
            else:
                # print(f"{_indent()}[red]{name} not handeled.[/]")
                pass


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
        _walk_model._max_level = None
        _walk_model._max_string = None
        _walk_model._max_items = None
        _walk_model._show_none = True
        _walk_model(
            key,
            datasworn_tree[key],
        )
        # console.print(datasworn_tree[key])
