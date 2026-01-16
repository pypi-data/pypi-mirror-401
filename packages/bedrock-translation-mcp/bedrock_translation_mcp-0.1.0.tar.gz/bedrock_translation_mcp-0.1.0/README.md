# Translation Power

A Kiro Power that provides text translation capabilities through AWS Bedrock Nova Pro LLM via a custom MCP server.

## Features

- Text translation using AWS Bedrock Nova Pro
- Support for plain text and file-based inputs
- Streaming response support
- Sample code generation in Java, Python, and Node.js
- MCP protocol integration for Kiro

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials in `mcp-config.json` or via environment variables

3. Install the power in Kiro through the Power management interface

## Configuration

See `mcp-config.json` for configuration options including:
- AWS region and credentials
- Model selection
- Translation parameters
- Server settings

## Documentation

See `POWER.md` for detailed usage instructions and API documentation.

## Development

Run tests:
```bash
pytest tests/
```

Run property-based tests:
```bash
pytest tests/ -v
```

## Requirements

- Python >= 3.9
- AWS account with Bedrock access
- Valid AWS credentials
