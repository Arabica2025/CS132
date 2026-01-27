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
5. `uv sync`: install all packages in my virtual environment
    - `pyproject.toml`: package receipt (list)
    - `uv.lock`: package receipt for the machine