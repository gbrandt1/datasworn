
# Datasworn and Datasworn Community Content Python Projects

This directory contains two Python projects for Datasworn and Datasworn Community Content organized using [`uv` workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/).

## Installation

to install the datasworn core package (with the Pydantic models)
directly from GitHub, run for example

```
uv add "git+https://github.com/gbrandt1/datasworn.git&subdirectory=pkg/python/datasworn/src/datasworn/core"
```

to add the rule packages, run eg.

```
uv add "git+https://github.com/gbrandt1/datasworn.git#subdirectory=pkg/python/datasworn/src/datasworn/starforged"
```

## Building

/!\ Building does not work out-of-the-box yet and the generated models require some manual fixes /!\

Please install [`uv`](https://docs.astral.sh/uv/) to work with this repository.

The `build.py` script in the root directory of the repository is used to

- copy the datasworn output JSON files.
- generate the Pydantic models for the `core` package from the JSON schema provided by Datasworn.

To run the build script:

```bash
./build.py
```

The build script is self-contained (apart from requiring `uv`) using [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata).

## Testing

Tests are provided to validate the JSON files can be correctly parsed into Pydantic models.
To run the tests from the root directory of `datasworn` or `datasworn-community-content`:

```bash
uv run pytest --cov
```

The tests should demonstrate 100% coverage.

## Datasworn Project

Pydantic Models:

- `datasworn-core` core functionality (only Pydantic models for now).

JSON-only packages:

| Package | Rulebook
|---|---
| `datasworn-classic` | Ironsworn
| `datasworn-delve` | Ironsworn: Delve
| `datasworn-starforged` | Ironsworn: Starforged
| `datasworn-sundered-isles` | Sundered Isles

For convenience the top-level `datasworn` package can be installed which depends on all the above packages.

## Datasworn Community Content Python Project

JSON-only packages:

| Package | Rulebook
|---|---
| `datasworn-community-content-ancient-wonders` | Ancient Wonders
| `datasworn-community-content-fe-runners` | FE runners
| `datasworn-community-content-starsmith` | Starsmith
  
## Licensing

These Datasworn Python projects in `pkg/python` by -southpole- use the MIT license.

Datasworn package content (the typings and JSON schema) and internal tooling (by rsek and tbsvttr) use the MIT license.

Textual and image content (in other words, the actual content from the rulebooks as described in JSON, Markdown, and other files) is CC-BY-4.0 or CC-BY-NC-4.0.

Additionally, the JSON files embed licensing information in the source property that appears on many objects throughout Datasworn.
