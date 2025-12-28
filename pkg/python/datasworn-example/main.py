from importlib.resources import files

from datasworn.core.models import Expansion, Ruleset
from rich import print

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

for name in DATASWORN_JSON_SOURCES:
    scope, type_ = DATASWORN_JSON_SOURCES[name]
    json_source = files(f"{scope}.{name}").joinpath(f"json/{name}.json").read_text()
    datasworn_tree[name] = type_.model_validate_json(json_source)

for k, v in datasworn_tree.items():
    print(f"{k}: '{v.title.root}' {v.type}")
