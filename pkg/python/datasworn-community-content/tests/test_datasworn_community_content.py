import importlib
import json
from pathlib import Path

from datasworn.core.models import Expansion, Ruleset
from rich import print

NAMESPACE = "datasworn_community_content"

RULES_PACKAGES = [
    "ancient_wonders",
    "fe_runners",
    "starsmith",
]


def load_rules_package(package_name: str) -> Ruleset | Expansion:
    package = importlib.import_module(f"{NAMESPACE}.{package_name}")
    json_file = Path(package.__file__).parent / "json" / f"{package_name}.json"
    with json_file.open() as f:
        rules = f.read()
        # rules_json = json.loads(rules)
        # if rules_json["type"] == "expansion":
        return Expansion.model_validate_json(rules)
        # else:
        # return Ruleset.model_validate_json(rules)


def test_datasworn():
    print()
    for rules_package in RULES_PACKAGES:
        rules_package = load_rules_package(rules_package)

        _id = rules_package.field_id
        print(f"{_id}: {type(rules_package)} {rules_package.type}")
