
# Datasworn and Datasworn Community Content Python Projects

This directory contains two Python projects for Datasworn and Datasworn Community Content
organized using [`uv` workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/).

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

! Building does not work out-of-the-box yet and the generated models require some manual fixes !

The build script in the root directory of the repositoryis used to

- copy the JSON files
- generate the Pydantic models for the `core` package from the JSON schema provided by Datasworn.

To run the build script:

```bash
uv run build.py
```

The build script is self-contained using [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata).

## Testing

Tests are provided to validate the JSON files can be correctly parsed into Pydantic models.
To run the tests from the root directory of `datasworn` or `datasworn-community-content`:

```bash
uv run pytest --cov
```

The tests should demonstrate 100% coverage.

## Datasworn Project

Pydantic Models:

- core

JSON-only packages:

- Ironsworn Classic
- Ironsworn Delve
- Starforged
- Sundered Isles

## Datasworn Community Content Python Project

JSON-only packages:

- Ancient Wonders
- FE runners
- Starsmith
  
## Licensing

Python projects use the MIT license.

Datasworn package content (the typings and JSON schema) and internal tooling use the MIT license.

Textual and image content (in other words, the actual content from the rulebooks as described in JSON, Markdown, and other files) is CC-BY-4.0 or CC-BY-NC-4.0.

Additionally, the JSON files embed licensing information in the source property that appears on many objects throughout Datasworn.
