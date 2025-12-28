
to install the datasworn core package (with the Pydantic models)
directly from GitHub, run for example

```
uv add "git+https://github.com/gbrandt1/datasworn.git@sp-devel#egg=datasworn-core&subdirectory=pkg/python/datasworn/src/datasworn/core"
```

to add the rule packages, run

```
uv add "git+https://github.com/gbrandt1/datasworn.git@sp-devel#subdirectory=pkg/python/datasworn/src/datasworn/starforged"
```
