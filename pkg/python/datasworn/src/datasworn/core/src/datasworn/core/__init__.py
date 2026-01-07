import logging
from collections.abc import Mapping
from importlib.resources import files
from typing import Any

from pydantic import BaseModel, RootModel

from .models import Expansion, Ruleset

log = logging.getLogger(__name__)

DATASWORN_JSON_SOURCES: dict[str, tuple[str, type[Expansion] | type[Ruleset]]] = {
    "classic": ("datasworn", Ruleset),
    "delve": ("datasworn", Expansion),
    "starforged": ("datasworn", Ruleset),
    "sundered_isles": ("datasworn", Expansion),
    "ancient_wonders": ("datasworn_community_content", Expansion),
    "fe_runners": ("datasworn_community_content", Expansion),
    "starsmith": ("datasworn_community_content", Expansion),
}

index = {}


class DataswornTree(Mapping[str, Any]):
    def __init__(self, *args: Any, **kwargs: Any):
        self._json_sources = dict(*args, **kwargs)
        self._sources: dict[str, Any] = {}

    def __getitem__(self, name: str):
        if name not in self._json_sources:
            log.error(f"Source must be one of {list(self._json_sources.keys())}")
            raise KeyError(name)
        if name not in self._sources:
            self._load_source(name, *self._json_sources.__getitem__(name))
        return self._sources.__getitem__(name)

    def __iter__(self):
        return iter(self._json_sources)

    def __len__(self):
        return len(self._json_sources)

    def _load_source(
        self, name: str, scope: str, type_: type[Expansion] | type[Ruleset]
    ) -> None:
        # scope, type_ = DATASWORN_JSON_SOURCES[name]
        json_source = files(f"{scope}.{name}").joinpath(f"json/{name}.json").read_text()
        self._sources[name] = type_.model_validate_json(json_source)
        num = self._build_index(self._sources[name])
        log.debug(f"Loaded {name}")

    def _build_index(self, obj: Any) -> int:
        num = 0
        match obj:
            case RootModel():
                self._build_index(obj.root)
            case BaseModel():
                _id = getattr(obj, "id", None)
                # if isinstance(_id, RootModel) and isinstance(_id.root, RootModel):
                #     index[_id.root.root] = obj
                #     num += 1
                # if isinstance(_id, RootModel) and isinstance(_id.root, str):
                #     index[_id.root] = obj
                if _id:
                    index[_id] = obj
                    num += 1
                for _, v in obj:
                    self._build_index(v)
            case dict():
                for v in obj.values():
                    self._build_index(v)
            case list():
                for v in obj:
                    self._build_index(v)
            case _:
                pass
            # datasworn_tree[name] = pydantic_core.from_json(json_source)
        return num


datasworn_tree = DataswornTree(DATASWORN_JSON_SOURCES)
