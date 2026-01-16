# Quick Start Guide

Get the Bedrock Translation Service MCP running in 5 minutes!

## Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- AWS credentials configured

## Quick Install (Recommended)

### 1. Install UV

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install the Package

```bash
cd bedrock-translation-service-mcp
uv pip install -e .
```

### 3. Configure AWS Credentials

**Quick method (environment variables):**

**Windows:**
```powershell
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"
```

**macOS/Linux:**
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### 4. Add to Kiro

Edit `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "bedrock-translation": {
      "command": "uvx",
      "args": ["--from", "translation-power-mcp", "translation-power-mcp"],
      "env": {
        "AWS_REGION": "us-east-1",
        "MODEL_ID": "amazon.nova-pro-v1:0"
      },
      "disabled": false
    }
  }
}
```

### 5. Restart Kiro

Restart Kiro or reconnect the MCP server.

### 6. Test It!

In Kiro, try:
```
translate "hello" to Spanish
```

Should return: "hola"

## Alternative: Without UV

### 1. Install Dependencies

```bash
cd bedrock-translation-service-mcp
pip install -r requirements.txt
```

### 2. Configure Kiro with Full Path

Edit `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "bedrock-translation": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/full/path/to/bedrock-translation-service-mcp",
      "env": {
        "AWS_REGION": "us-east-1"
      },
      "disabled": false
    }
  }
}
```

Replace `/full/path/to/` with your actual path.

## Troubleshooting

**Server won't start?**
```bash
# Test manually
cd bedrock-translation-service-mcp
python -m src.server
```

**AWS errors?**
```bash
# Verify credentials
aws bedrock list-foundation-models --region us-east-1
```

**Need help?** See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

## What's Next?

- Try translating files
- Generate sample code in Java/Python/Node.js
- Customize configuration options
- Read the full [README.md](README.md)

## Common Commands

**Translate text:**
```
translate "hello world" to French
```

**Translate file:**
```
translate the file at /path/to/doc.txt to German
```

**Get sample code:**
```
provide me sample code for translation service in Java
```

## Configuration Options

Add these to the `env` section in your `mcp.json`:

```json
{
  "AWS_REGION": "us-east-1",
  "MODEL_ID": "amazon.nova-pro-v1:0",
  "LOG_LEVEL": "INFO",
  "TEMPERATURE": "0.3",
  "MAX_TOKENS": "2000"
}
```

That's it! You're ready to translate! 🚀
