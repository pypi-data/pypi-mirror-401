# Publishing to PyPI

This guide shows you how to publish `bedrock-translation-mcp` to PyPI so anyone can use it with `uvx`.

## Prerequisites

1. **PyPI Account**: Create one at https://pypi.org/account/register/
2. **API Token**: Generate at https://pypi.org/manage/account/token/

## Step 1: Install Build Tools

```bash
pip install build twine
```

## Step 2: Build the Package

```bash
cd bedrock-translation-service-mcp
python -m build
```

This creates:
- `dist/bedrock-translation-mcp-0.1.0.tar.gz`
- `dist/bedrock_translation_mcp-0.1.0-py3-none-any.whl`

## Step 3: Test on TestPyPI (Optional but Recommended)

### Create TestPyPI Account
Sign up at https://test.pypi.org/account/register/

### Upload to TestPyPI
```bash
python -m twine upload --repository testpypi dist/*
```

Enter your TestPyPI credentials when prompted.

### Test Installation
```bash
uvx --from bedrock-translation-mcp --index-url https://test.pypi.org/simple/ bedrock-translation-mcp
```

## Step 4: Publish to PyPI

```bash
python -m twine upload dist/*
```

Enter your PyPI credentials:
- Username: `__token__`
- Password: Your API token (starts with `pypi-`)

## Step 5: Verify Publication

Check your package at: `https://pypi.org/project/bedrock-translation-mcp/`

## Step 6: Test Installation

```bash
uvx --from bedrock-translation-mcp bedrock-translation-mcp
```

## Update mcp.json

After publishing, update your `mcp.json`:

```json
{
  "mcpServers": {
    "translation-server": {
      "command": "uvx",
      "args": [
        "--from",
        "bedrock-translation-mcp",
        "bedrock-translation-mcp"
      ],
      "env": {
        "AWS_REGION": "us-east-1",
        "MODEL_ID": "amazon.nova-pro-v1:0"
      },
      "disabled": false
    }
  }
}
```

Now it works on ANY machine without absolute paths!

## Updating the Package

When you make changes:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.1"
   ```

2. Rebuild and republish:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Alternative: Private Package Index

If you don't want to publish publicly, you can:

1. **Use a private PyPI server** (like devpi or Artifactory)
2. **Publish to GitHub and install from there**:
   ```bash
   uvx --from git+https://github.com/yourusername/bedrock-translation-mcp bedrock-translation-mcp
   ```

## Security Notes

- **Never commit your PyPI token** to version control
- Store token in `~/.pypirc`:
  ```ini
  [pypi]
  username = __token__
  password = pypi-your-token-here
  ```
- Use scoped tokens for better security

## Troubleshooting

### "Package name already exists"
Choose a different name in `pyproject.toml`

### "Invalid credentials"
- Username must be `__token__`
- Password is your API token (not your PyPI password)

### "File already exists"
You can't re-upload the same version. Increment the version number.

## Quick Commands Reference

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Test with uvx
uvx --from bedrock-translation-mcp bedrock-translation-mcp
```

That's it! Once published, anyone can use your MCP server with just `uvx`!
