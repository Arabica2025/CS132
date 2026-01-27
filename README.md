# CS 132 Repository

## Environment setup

I used `uv` to manage packages

### Initialization

```Python
uv init
```

Python Version: `3.13`

Packages:
```Bash
numpy
scipy
matplotlib
networkx
scikit-learn
```

`uv` commands

1. `uv init`: initialize Python projects in current workspace
2. `uv run yourfile.py`: run your python file
3. `uv add package-name`: install the package
4. `uv remove package-name`: remove the package
5. `uv sync`: install all packages in my virtual environment (if you run any python file using `uv run`, it will automatically execute `uv sync`)
    - `pyproject.toml`: package receipt (list)
    - `uv.lock`: package receipt for the machine
6. `uv add` vs `uv pip install`
    - `uv add`: record packages in `uv.lock`
    - `uv pip install`: don't record
    - usage:
        - want to test a package but don't want to add to `uv.lock` yet (temporary debugging or testing the package before merging into main or etc.) -> use `uv pip install`