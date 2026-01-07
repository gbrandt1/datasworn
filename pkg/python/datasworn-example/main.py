from importlib.resources import files
from typing import Any

from datasworn.core import datasworn_tree, index
from datasworn.core.models import Expansion, OracleTableText, Ruleset
from pydantic import BaseModel, RootModel
from rich import print
from rich.console import Console
from rich.traceback import install

# from pkg.python import build

console = Console(force_terminal=True, color_system="truecolor")

install(show_locals=True)


def _walk_model(
    name: str,
    obj: Any,
    level: int = 0,
    # *,
    # max_level: int | None = None,
    # max_string: int | None = None,
    # max_items: int | None = None,
    # show_none: bool | None = False,
    # id_callback: Callable[[str, object], None] | None = None,
):
    def _indent():
        return " " * level * 4

    if _walk_model._max_level is not None and level > _walk_model._max_level:
        # print(f"{_indent()}[dim white]{name} ...[/]")
        return

    match obj:
        # case RootModel():
        #     print(
        #         f"{_indent()}[blue]{name}[/] <{obj.__class__.__name__}>"
        #         # f"{repr(obj.root)[: _walk_model._max_string]}"
        #         f"{'...' if _walk_model._max_string and len(repr(obj.root)) > _walk_model._max_string else ''}"
        #     )
        #     _walk_model("root", obj.root, level + 1)
        case BaseModel():
            _id = getattr(obj, "id", None)
            # if isinstance(_id, RootModel) and isinstance(_id.root, RootModel):
            #     index[_id.root.root] = obj
            # if isinstance(_id, RootModel) and isinstance(_id.root, str):
            #     index[_id.root] = obj
            index[_id] = obj

            print(
                f"{_indent()}[bright_yellow]{name}[/] <{obj.__class__.__name__}> {f'[cyan] <-- {_id}[/]' if _id else ''}"
            )
            for k, v in obj:
                _walk_model(k, v, level + 1)
        case dict():
            if len(obj) == 0:
                print(f"{_indent()}[dim yellow]{name} {{}}[/]")
                return
            print(f"{_indent()}[bright_yellow]{name} {{}}[/]")
            for k, v in obj.items():
                _walk_model(k, v, level + 1)
        case list():
            if len(obj) == 0:
                print(f"{_indent()}[dim yellow]{name} [][/]")
                return
            print(f"{_indent()}[bright_yellow]{name} [][/]")
            for i, v in enumerate(obj):
                if _walk_model._max_items is not None and i >= _walk_model._max_items:
                    print(f"{_indent()}[dim white]...[/]")
                    break
                _walk_model(f"[{i}]", v, level + 1)
        case str():
            if (
                _walk_model._max_string is not None
                and len(obj) > _walk_model._max_string
            ):
                print(
                    f"{_indent()}[yellow]{name}[/]="
                    f"{obj[: _walk_model._max_string]!r}..."
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


def walk_datasworn_tree(key, node):
    _walk_model._max_level = None
    _walk_model._max_string = 120
    _walk_model._max_items = None
    _walk_model._show_none = False
    _walk_model(key, node)
    # console.print(datasworn_tree[key])

    for _id, obj in index.items():
        print(f"[magenta]Indexed ID:[/] {_id!r} -> {obj.__class__!r}")
    print(f"Indexed {len(index)} IDs.")


if __name__ == "__main__":
    # from typing import get_type_hints

    # inspect(AnyId, all=True)
    # if MoveId in
    # get_type_hints(AnyId)["root"]

    # _load_sources()

    # _build_index(datasworn_tree)

    # trigger lazy loading
    for k, v in datasworn_tree["classic"]:
        print(k)

    walk_datasworn_tree("classic", datasworn_tree["classic"])

    # for i in index:
    #     if ".row" in i:
    #         continue
    #     print(f"{i!r} -> {index[i].__class__.__name__}")
    #     # print(f"{index[i].__class__.__name__}")
    #     # print(index[i])

    # print(f"Found {len(index)} IDs.")

    # # for key in datasworn_tree:
    # #     console.rule(f"[bold green] Datasworn Package: {key} [/]")
    # #     print(datasworn_tree[key])

    # print(datasworn_tree["classic"])
