# How to Publish to PyPI

This project is configured to be built and published to PyPI.

## Prerequisites

1. **Create a PyPI Account**: If you haven't already, sign up at [pypi.org](https://pypi.org/).
2. **Create an API Token**: Go to Account Settings -> API Tokens and create a new token. Save it (it starts with `pypi-`).
3. **Install Build and Publish Tools**:
   ```bash
   pip install build twine
   ```

## Steps to Publish

1. **Build the Package**:
   Run the following command in the project root (`d:\code\python\currency_mcp`):
   ```bash
   python -m build
   ```
   This will create a `dist/` directory containing `.tar.gz` and `.whl` files.

2. **Check the Package (Optional)**:
   You can check if the description maps correctly:
   ```bash
   twine check dist/*
   ```

3. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```
   - When prompted for **username**, enter `__token__`.
   - When prompted for **password**, paste your PyPI API token (`pypi-...`).

## Testing with uv

Once published, you (and others) can run it immediately without manual installation:

```bash
uvx mcp-server-currency-history
```

Or install it globally:

```bash
uv tool install mcp-server-currency-history
```
