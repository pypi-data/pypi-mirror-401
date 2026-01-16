---
name: Translation Power
description: Advanced text translation using AWS Bedrock Nova Pro LLM with MCP integration
version: 1.0.0
author: Kiro
keywords: [translation, aws, bedrock, nova-pro, mcp, multilingual]
---

# Translation Power

A Kiro Power that provides advanced text translation capabilities through AWS Bedrock Nova Pro LLM via a custom MCP (Model Context Protocol) server.

## Overview

The Translation Power enables seamless text translation within your Kiro workflows. It leverages AWS Bedrock's Nova Pro language model to deliver high-quality translations with support for multiple input formats, streaming responses, and multi-language code generation.

### Key Capabilities

- **Text Translation**: Translate plain text or file contents using AWS Bedrock Nova Pro
- **Flexible Input**: Support for both direct text input and file path references
- **Streaming Responses**: Receive translation results incrementally for better user experience
- **Sample Code Generation**: Get integration examples in Java, Python, and Node.js
- **MCP Integration**: Fully integrated with Kiro's Model Context Protocol infrastructure

## Installation

### Prerequisites

Before installing the Translation Power, ensure you have:

1. **Python 3.9 or higher** installed on your system
2. **AWS Account** with access to Amazon Bedrock
3. **AWS Credentials** configured with appropriate permissions
4. **Kiro IDE** installed and running

### AWS Setup Requirements

#### 1. Enable Amazon Bedrock Access

1. Log in to your AWS Console
2. Navigate to Amazon Bedrock service
3. Request access to the Nova Pro model (if not already enabled)
4. Wait for approval (typically instant for most regions)

#### 2. Configure IAM Permissions

Your AWS credentials must have the following permissions:

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

#### 3. Set Up AWS Credentials

Choose one of the following methods:

**Option A: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Option B: AWS Credentials File**
Create or edit `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```

And `~/.aws/config`:
```ini
[default]
region = us-east-1
```

**Option C: IAM Role** (for EC2 instances)
Attach an IAM role with Bedrock permissions to your EC2 instance.

### Install the Power

1. **Install Python Dependencies**:
   ```bash
   cd translation-power
   pip install -r requirements.txt
   ```

2. **Configure the MCP Server**:
   - Copy `mcp-config.json` to your Kiro MCP configuration directory
   - Update the configuration with your AWS region and preferences
   - See [Configuration Options](#configuration-options) below

3. **Install via Kiro**:
   - Open Kiro IDE
   - Navigate to the Powers panel
   - Click "Install Power"
   - Select the translation-power directory
   - Kiro will register the MCP server automatically

4. **Verify Installation**:
   - Check that the MCP server appears in Kiro's MCP Server list
   - The server should show as "Running" or "Connected"

## Usage

### Tool 1: translate

Translate text from one language to another using AWS Bedrock Nova Pro.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input` | string | Yes | - | The text to translate or a file path |
| `is_file` | boolean | No | false | Whether the input is a file path |
| `source_lang` | string | No | auto | Source language code (e.g., 'en', 'es', 'fr') |
| `target_lang` | string | Yes | - | Target language code |
| `stream` | boolean | No | false | Enable streaming response |

#### Examples

**Example 1: Translate Plain Text**
```json
{
  "input": "Hello, how are you?",
  "target_lang": "es"
}
```

Response:
```json
{
  "translated_text": "Hola, ¿cómo estás?",
  "source_language": "en",
  "target_language": "es",
  "model_used": "amazon.nova-pro-v1:0",
  "timestamp": "2026-01-13T10:30:00Z"
}
```

**Example 2: Translate from File**
```json
{
  "input": "/path/to/document.txt",
  "is_file": true,
  "source_lang": "en",
  "target_lang": "fr"
}
```

**Example 3: Streaming Translation**
```json
{
  "input": "This is a long document that will be translated incrementally...",
  "target_lang": "de",
  "stream": true
}
```

Response (streamed chunks):
```json
{"chunk": "Dies ist ein langes", "is_complete": false}
{"chunk": " Dokument, das schrittweise", "is_complete": false}
{"chunk": " übersetzt wird...", "is_complete": true}
```

#### Supported Languages

The Translation Power supports all languages available through AWS Bedrock Nova Pro, including but not limited to:

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Russian (ru)
- And many more...

Use standard ISO 639-1 language codes or set `source_lang` to "auto" for automatic detection.

### Tool 2: get_sample_code

Generate sample code demonstrating how to integrate the translation service into your application.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `language` | string | Yes | - | Programming language: 'java', 'python', or 'nodejs' |
| `include_comments` | boolean | No | true | Include explanatory comments in the code |

#### Examples

**Example 1: Python Sample Code**
```json
{
  "language": "python"
}
```

Response:
```json
{
  "code": "# Python sample code here...",
  "language": "python",
  "description": "Python example for integrating the Translation Power MCP server"
}
```

**Example 2: Java Sample Code**
```json
{
  "language": "java",
  "include_comments": true
}
```

#### Supported Languages

- `java` - Java 11+ with AWS SDK
- `python` - Python 3.9+ with boto3
- `nodejs` - Node.js 16+ with AWS SDK v3

## Configuration Options

The Translation Power can be configured through the `mcp-config.json` file or environment variables.

### MCP Configuration File

Location: `.kiro/settings/mcp.json` (or workspace-specific location)

```json
{
  "mcpServers": {
    "translation-power": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/translation-power",
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
        "MODEL_ID": "amazon.nova-pro-v1:0",
        "LOG_LEVEL": "INFO",
        "MAX_RETRIES": "3",
        "TIMEOUT": "30",
        "MAX_INPUT_LENGTH": "10000",
        "TEMPERATURE": "0.3",
        "MAX_TOKENS": "2000"
      }
    }
  }
}
```

### Configuration Parameters

#### Server Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `AWS_REGION` | string | us-east-1 | AWS region for Bedrock API calls |
| `MODEL_ID` | string | amazon.nova-pro-v1:0 | Bedrock model identifier |
| `LOG_LEVEL` | string | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_RETRIES` | integer | 3 | Maximum retry attempts for failed API calls |
| `TIMEOUT` | integer | 30 | Request timeout in seconds |

#### Translation Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `MAX_INPUT_LENGTH` | integer | 10000 | Maximum input text length in characters |
| `TEMPERATURE` | float | 0.3 | Model temperature (0.0-1.0, lower = more deterministic) |
| `MAX_TOKENS` | integer | 2000 | Maximum tokens in model response |
| `DEFAULT_SOURCE_LANG` | string | auto | Default source language if not specified |
| `DEFAULT_TARGET_LANG` | string | en | Default target language if not specified |

### Environment Variables

All configuration options can be set via environment variables:

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Model Configuration
export MODEL_ID=amazon.nova-pro-v1:0
export TEMPERATURE=0.3
export MAX_TOKENS=2000

# Server Configuration
export LOG_LEVEL=INFO
export MAX_RETRIES=3
export TIMEOUT=30
```

## Error Handling

The Translation Power provides detailed error messages for common issues:

### Common Errors

**Authentication Error**
```json
{
  "error": {
    "code": "authentication_error",
    "message": "AWS credentials are invalid or missing",
    "data": {
      "error_type": "aws",
      "details": "Please configure AWS credentials"
    }
  }
}
```

**File Not Found**
```json
{
  "error": {
    "code": "file_error",
    "message": "File not found: /path/to/file.txt",
    "data": {
      "error_type": "file",
      "details": "Ensure the file path is correct and accessible"
    }
  }
}
```

**Invalid Input**
```json
{
  "error": {
    "code": "validation_error",
    "message": "Input text is empty or invalid",
    "data": {
      "error_type": "validation",
      "details": "Provide non-empty text or valid file path"
    }
  }
}
```

**Rate Limit Exceeded**
```json
{
  "error": {
    "code": "rate_limit_error",
    "message": "AWS Bedrock rate limit exceeded",
    "data": {
      "error_type": "aws",
      "details": "Request will be retried automatically"
    }
  }
}
```

**Unsupported Language**
```json
{
  "error": {
    "code": "unsupported_language",
    "message": "Language 'xyz' is not supported",
    "data": {
      "error_type": "validation",
      "details": "Supported languages: java, python, nodejs"
    }
  }
}
```

## Troubleshooting

### Server Won't Start

1. **Check Python version**: Ensure Python 3.9+ is installed
   ```bash
   python --version
   ```

2. **Verify dependencies**: Reinstall requirements
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check AWS credentials**: Test credentials manually
   ```bash
   aws bedrock list-foundation-models --region us-east-1
   ```

4. **Review logs**: Check Kiro's MCP server logs for detailed error messages

### Translation Fails

1. **Verify Bedrock access**: Ensure Nova Pro model is enabled in your AWS account
2. **Check IAM permissions**: Verify your credentials have `bedrock:InvokeModel` permission
3. **Test connectivity**: Ensure network access to AWS Bedrock endpoints
4. **Review input**: Ensure input text is within size limits (default: 10,000 characters)

### Slow Performance

1. **Enable streaming**: Use `stream: true` for large translations
2. **Adjust timeout**: Increase `TIMEOUT` configuration for large documents
3. **Check region**: Use an AWS region closer to your location
4. **Monitor rate limits**: AWS Bedrock has rate limits that may affect performance

### File Reading Issues

1. **Check file permissions**: Ensure the MCP server has read access to the file
2. **Verify file encoding**: Use UTF-8 encoding for text files
3. **Use absolute paths**: Provide full file paths to avoid ambiguity
4. **Check file size**: Ensure files are within the maximum input length limit

## Best Practices

### Performance Optimization

1. **Use streaming for large texts**: Enable streaming for documents over 1000 characters
2. **Batch similar translations**: Group translations to the same target language
3. **Cache results**: Store frequently translated content to avoid redundant API calls
4. **Set appropriate timeouts**: Balance between reliability and responsiveness

### Cost Management

1. **Monitor API usage**: Track Bedrock API calls through AWS CloudWatch
2. **Use appropriate temperature**: Lower temperature (0.1-0.3) for consistent translations
3. **Limit max tokens**: Set reasonable `MAX_TOKENS` to control response size
4. **Implement rate limiting**: Add application-level rate limiting if needed

### Security

1. **Protect credentials**: Never commit AWS credentials to version control
2. **Use IAM roles**: Prefer IAM roles over access keys when possible
3. **Rotate credentials**: Regularly rotate AWS access keys
4. **Limit permissions**: Grant only necessary Bedrock permissions
5. **Encrypt sensitive data**: Use encryption for sensitive translation content

### Integration Tips

1. **Handle errors gracefully**: Implement retry logic for transient failures
2. **Validate inputs**: Check input length and format before sending to the API
3. **Log appropriately**: Use structured logging for debugging and monitoring
4. **Test thoroughly**: Use the provided sample code as a starting point
5. **Monitor performance**: Track translation latency and success rates

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_translation.py

# Run property-based tests only
pytest tests/ -k property

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Project Structure

```
translation-power/
├── POWER.md                    # This documentation
├── README.md                   # Quick start guide
├── package.json                # Power metadata
├── mcp-config.json            # MCP server configuration template
├── requirements.txt           # Python dependencies
├── src/
│   ├── server.py              # MCP server implementation
│   ├── translation_engine.py # Translation logic
│   ├── bedrock_client.py     # AWS Bedrock integration
│   ├── sample_code_gen.py    # Sample code generator
│   ├── input_handler.py      # Input processing
│   ├── models.py             # Data models
│   └── config.py             # Configuration management
├── templates/
│   ├── java_sample.txt       # Java code template
│   ├── python_sample.txt     # Python code template
│   └── nodejs_sample.txt     # Node.js code template
└── tests/
    ├── unit/                  # Unit tests
    ├── property/              # Property-based tests
    └── integration/           # Integration tests
```

## Support and Resources

### Documentation

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Nova Pro Model Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-nova.html)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Kiro Powers Documentation](https://kiro.ai/docs/powers)

### Getting Help

- **Issues**: Report bugs or request features through your organization's issue tracker
- **AWS Support**: Contact AWS Support for Bedrock-specific issues
- **Community**: Join the Kiro community for tips and best practices

## License

See the main Kiro license for terms and conditions.

## Changelog

### Version 1.0.0 (2026-01-13)

- Initial release
- AWS Bedrock Nova Pro integration
- Text and file-based translation
- Streaming response support
- Sample code generation for Java, Python, and Node.js
- MCP protocol integration
- Comprehensive error handling
- Property-based testing suite
