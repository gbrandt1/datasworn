<<<<<<< HEAD

to install the datasworn core package (with the Pydantic models)
directly from GitHub, run for example

```
uv add "git+https://github.com/gbrandt1/datasworn.git@sp-devel#egg=datasworn-core&subdirectory=pkg/python/datasworn/src/datasworn/core"
```

to add the rule packages, run

```
uv add "git+https://github.com/gbrandt1/datasworn.git@sp-devel#subdirectory=pkg/python/datasworn/src/datasworn/starforged"
```
=======
# Datasworn Official Python Packages

Official Datasworn content packages for Python/Pydantic.

## Packages

- `datasworn-core` - Pydantic models for all Datasworn types
- `datasworn-classic` - Ironsworn Classic ruleset
- `datasworn-delve` - Ironsworn: Delve expansion
- `datasworn-starforged` - Ironsworn: Starforged ruleset
- `datasworn-sundered-isles` - Sundered Isles expansion

## Installation

```bash
uv add datasworn-core datasworn-starforged
```

## Usage

See the main [Python README](../README.md) for usage examples.
>>>>>>> upstream/main
