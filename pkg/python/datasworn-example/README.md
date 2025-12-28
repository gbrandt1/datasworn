# Datasworn Python Example Project

This example shows how to use the Datasworn Python projects.

For development purposes it installs the datasworn packages locally (editable install) instead from GitHub, so you need to clone the repository to run the example.

To install the datasworn core package (with the Pydantic models) directly from GitHub instead, remove the packages and add them back like this for example

```
uv add "git+https://github.com/gbrandt1/datasworn.git&subdirectory=pkg/python/datasworn/src/datasworn/core"
```

to add the rule packages, run eg.

```
uv add "git+https://github.com/gbrandt1/datasworn.git#subdirectory=pkg/python/datasworn/src/datasworn/starforged"
```

This Python package URL syntax works also with `pip` etc.
