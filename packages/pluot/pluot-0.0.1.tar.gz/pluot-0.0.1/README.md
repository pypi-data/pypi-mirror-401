# pluot

## Publishing

To publish this package to PyPI:

1.  Install build tools and twine:
    ```bash
    pip install build twine
    ```

2.  Build the distribution packages:
    ```bash
    python3 -m build
    ```

3.  Upload to PyPI:
    ```bash
    python3 -m twine upload dist/*
    ```
