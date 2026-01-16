# Bedrock Translation Service MCP - Installation Guide

This guide will walk you through installing and configuring the Bedrock Translation Service MCP server.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.9 or higher** installed
   - Check version: `python --version`
   - Download from: https://www.python.org/downloads/

2. **AWS Account** with Amazon Bedrock access
   - Sign up at: https://aws.amazon.com/

3. **AWS Credentials** with Bedrock permissions
   - IAM permission required: `bedrock:InvokeModel`

4. **Nova Pro Model** enabled in your AWS account
   - Enable in AWS Bedrock console

## Installation Steps

### Step 1: Install Python Dependencies

Navigate to the MCP server directory and install dependencies:

```bash
cd bedrock-translation-service-mcp
pip install -r requirements.txt
```

**Alternative using virtual environment (recommended):**

```bash
cd bedrock-translation-service-mcp

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure AWS Credentials

Choose one of the following methods to configure your AWS credentials:

#### Option A: Environment Variables (Temporary)

**Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_DEFAULT_REGION="us-east-1"
```

**Windows (Command Prompt):**
```cmd
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1
```

**macOS/Linux:**
```bash
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Option B: AWS Credentials File (Recommended)

Create or edit the AWS credentials file:

**Location:**
- Windows: `C:\Users\YourUsername\.aws\credentials`
- macOS/Linux: `~/.aws/credentials`

**Content:**
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

**AWS Config File** (optional):

**Location:**
- Windows: `C:\Users\YourUsername\.aws\config`
- macOS/Linux: `~/.aws/config`

**Content:**
```ini
[default]
region = us-east-1
```

#### Option C: AWS CLI Configuration

If you have AWS CLI installed:

```bash
aws configure
```

Follow the prompts to enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name (e.g., us-east-1)
- Default output format (e.g., json)

### Step 3: Verify AWS Configuration

Test your AWS credentials and Bedrock access:

```bash
aws bedrock list-foundation-models --region us-east-1
```

If successful, you should see a list of available models including Nova Pro.

### Step 4: Test the MCP Server

Run the MCP server directly to verify it works:

```bash
cd bedrock-translation-service-mcp
python -m src.server
```

The server should start without errors. Press `Ctrl+C` to stop it.

### Step 5: Install UV Package Manager (Recommended)

For the easiest setup, install `uv` - a fast Python package manager:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Alternative (using pip):**
```bash
pip install uv
```

Verify installation:
```bash
uv --version
```

### Step 6: Publish the Package Locally (for uvx usage)

To use the MCP server with `uvx`, you need to build and install it:

```bash
cd bedrock-translation-service-mcp

# Build the package
uv build

# Install locally
uv pip install -e .
```

Or install directly from the directory:
```bash
pip install -e bedrock-translation-service-mcp
```

### Step 7: Configure for Kiro

Add the MCP server configuration to your Kiro settings.

**Edit:** `~/.kiro/settings/mcp.json` (or `C:\Users\YourUsername\.kiro\settings\mcp.json` on Windows)

#### Option A: Using uvx (Recommended - No Path Required!)

```json
{
  "mcpServers": {
    "bedrock-translation-service": {
      "command": "uvx",
      "args": [
        "--from",
        "translation-power-mcp",
        "translation-power-mcp"
      ],
      "env": {
        "AWS_REGION": "us-east-1",
        "MODEL_ID": "amazon.nova-pro-v1:0",
        "LOG_LEVEL": "INFO",
        "MAX_RETRIES": "3",
        "TIMEOUT": "30",
        "MAX_INPUT_LENGTH": "10000",
        "TEMPERATURE": "0.3",
        "MAX_TOKENS": "2000"
      },
      "disabled": false,
      "timeout": 60000
    }
  }
}
```

**Benefits:**
- ✅ Works on any machine without hardcoded paths
- ✅ Automatically manages Python environment
- ✅ Easy to share and distribute

#### Option B: Using Python directly (Alternative)

```json
{
  "mcpServers": {
    "bedrock-translation-service": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\full\\path\\to\\bedrock-translation-service-mcp",
      "env": {
        "AWS_REGION": "us-east-1",
        "MODEL_ID": "amazon.nova-pro-v1:0",
        "LOG_LEVEL": "INFO",
        "MAX_RETRIES": "3",
        "TIMEOUT": "30",
        "MAX_INPUT_LENGTH": "10000",
        "TEMPERATURE": "0.3",
        "MAX_TOKENS": "2000"
      },
      "disabled": false,
      "timeout": 60000
    }
  }
}
```

**Important:** Replace `C:\\full\\path\\to\\bedrock-translation-service-mcp` with the actual absolute path.

**To find the absolute path:**

**Windows (PowerShell):**
```powershell
cd bedrock-translation-service-mcp
(Get-Location).Path
```

**macOS/Linux:**
```bash
cd bedrock-translation-service-mcp
pwd
```

#### Option C: Using installed package

If you installed the package globally:

```json
{
  "mcpServers": {
    "bedrock-translation-service": {
      "command": "translation-power-mcp",
      "args": [],
      "env": {
        "AWS_REGION": "us-east-1",
        "MODEL_ID": "amazon.nova-pro-v1:0",
        "LOG_LEVEL": "INFO",
        "MAX_RETRIES": "3",
        "TIMEOUT": "30",
        "MAX_INPUT_LENGTH": "10000",
        "TEMPERATURE": "0.3",
        "MAX_TOKENS": "2000"
      },
      "disabled": false,
      "timeout": 60000
    }
  }
}
```

### Step 8: Restart or Reconnect Kiro

After adding the configuration:

1. **Option A:** Restart Kiro completely
2. **Option B:** Open the MCP Server view in Kiro and click "Reconnect" on the bedrock-translation-service server

## Configuration Options

You can customize the MCP server behavior through environment variables in the `mcp.json` configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_REGION` | us-east-1 | AWS region for Bedrock service |
| `MODEL_ID` | amazon.nova-pro-v1:0 | Bedrock model identifier |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_RETRIES` | 3 | Maximum API retry attempts |
| `TIMEOUT` | 30 | Request timeout in seconds |
| `MAX_INPUT_LENGTH` | 10000 | Maximum input characters |
| `TEMPERATURE` | 0.3 | Model temperature (0.0-1.0, lower = more deterministic) |
| `MAX_TOKENS` | 2000 | Maximum response tokens |

## Troubleshooting

### Issue: "Python not found"

**Solution:** Install Python 3.9+ from https://www.python.org/downloads/

Verify installation:
```bash
python --version
```

### Issue: "Module not found" errors

**Solution:** Install dependencies:
```bash
cd bedrock-translation-service-mcp
pip install -r requirements.txt
```

### Issue: "AWS credentials not found"

**Solution:** Configure AWS credentials using one of the methods in Step 2.

Verify credentials:
```bash
aws configure list
```

### Issue: "Access denied" or "UnauthorizedException"

**Solution:** Ensure your IAM user/role has the required permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/amazon.nova-pro-v1:0"
    }
  ]
}
```

### Issue: "Model not found" or "ValidationException"

**Solution:** 
1. Verify Nova Pro model is enabled in your AWS account
2. Check the AWS region supports Nova Pro
3. Visit AWS Bedrock console and request model access if needed

### Issue: MCP server won't start in Kiro

**Solution:**
1. Check the `cwd` path in `mcp.json` is correct and absolute
2. Verify Python is in your system PATH
3. Check Kiro MCP server logs for detailed error messages
4. Try running the server manually first: `python -m src.server`

### Issue: "Connection timeout" errors

**Solution:**
1. Check your internet connection
2. Verify AWS Bedrock service is available in your region
3. Increase the `timeout` value in `mcp.json`
4. Check if you're behind a proxy or firewall

## Verification

To verify the installation is complete:

1. **Test AWS connection:**
   ```bash
   aws bedrock list-foundation-models --region us-east-1
   ```

2. **Test MCP server:**
   ```bash
   cd bedrock-translation-service-mcp
   python -m src.server
   ```

3. **Test in Kiro:**
   - Ask Kiro: "translate 'hello' to Spanish"
   - Should return: "hola"

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [POWER.md](../translation-power-kiro/POWER.md) for Kiro Power documentation
- Review AWS Bedrock pricing: https://aws.amazon.com/bedrock/pricing/

## Support

For issues or questions:
- Check AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/
- Review MCP protocol documentation: https://modelcontextprotocol.io/
- Check Kiro documentation for MCP server configuration

## Security Notes

- **Never commit AWS credentials** to version control
- Use IAM roles with minimal required permissions
- Rotate credentials regularly
- Consider using AWS IAM Identity Center for better security
- Monitor AWS CloudTrail logs for API usage

## License

MIT License - See LICENSE file for details
