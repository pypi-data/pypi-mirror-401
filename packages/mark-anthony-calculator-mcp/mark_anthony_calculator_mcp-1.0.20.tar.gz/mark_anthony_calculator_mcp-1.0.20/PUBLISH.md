# Publishing to PyPI

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **API Token**: Create an API token at https://pypi.org/manage/account/token/
   - Scope: "Entire account" or "Project: calculator-mcp"
   - Copy the token (starts with `pypi-`)

## Publishing Steps

### 1. Install build tools (already done)
```bash
python3 -m pip install --upgrade build twine
```

### 2. Build the package (already done)
```bash
python3 -m build
```

This creates:
- `dist/calculator_mcp-1.0.19.tar.gz` (source distribution)
- `dist/calculator_mcp-1.0.19-py3-none-any.whl` (wheel)

### 3. Check the package
```bash
python3 -m twine check dist/*
```

### 4. Upload to PyPI

**Option A: Using API Token (Recommended)**
```bash
python3 -m twine upload dist/*
# Username: __token__
# Password: pypi-your-api-token-here
```

**Option B: Using .pypirc file**
Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-your-api-token-here
```

Then upload:
```bash
python3 -m twine upload dist/*
```

**Option C: Test on TestPyPI first**
```bash
# Upload to TestPyPI
python3 -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ calculator-mcp
```

## After Publishing

Once published, users can install and use:

```bash
# Install via pip
pip install calculator-mcp

# Run directly
calculator-mcp

# Or use with uvx (no installation needed!)
uvx calculator-mcp
```

## MCP Client Configuration

After publishing, users can configure their MCP clients:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "uvx",
      "args": ["calculator-mcp"]
    }
  }
}
```

## Updating the Package

1. Update version in `pyproject.toml`
2. Rebuild: `python3 -m build`
3. Upload: `python3 -m twine upload dist/*`

## Troubleshooting

- **403 Forbidden**: Check your API token permissions
- **400 Bad Request**: Package name might be taken, try a different name
- **Version already exists**: Increment version number in `pyproject.toml`
