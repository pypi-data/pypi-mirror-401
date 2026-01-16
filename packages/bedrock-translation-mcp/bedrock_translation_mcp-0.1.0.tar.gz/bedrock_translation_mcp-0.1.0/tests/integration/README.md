# Integration Tests

This directory contains comprehensive integration tests for the Translation Power.

## Test Coverage

### End-to-End Tests (`test_end_to_end.py`)

Tests complete translation flows from MCP request to response:

1. **Complete Translation Flow** (4 tests)
   - Plain text translation end-to-end
   - File-based translation end-to-end
   - Streaming translation end-to-end
   - Auto language detection

2. **Sample Code Generation Flow** (3 tests)
   - Java sample code generation
   - Python sample code generation
   - Node.js sample code generation

3. **Error Handling Flow** (4 tests)
   - Invalid input error handling
   - File not found error handling
   - AWS error handling
   - Unsupported language error handling

4. **Multiple File Formats** (3 tests)
   - .txt file translation
   - .md file translation
   - .json file translation

5. **Server Lifecycle Integration** (2 tests)
   - Multiple requests on same server
   - Server restart functionality

6. **Configuration Integration** (2 tests)
   - Custom region configuration
   - Custom model configuration

**Total: 18 tests**

### Power Installation Tests (`test_power_installation.py`)

Tests power package structure and installation requirements:

1. **Power Package Structure** (7 tests)
   - POWER.md exists and has content
   - package.json exists and is valid
   - mcp-config.json exists and is valid
   - requirements.txt exists and has dependencies
   - src directory has all required modules
   - templates directory has all required templates
   - tests directory has proper structure

2. **MCP Server Registration** (5 tests)
   - Server can be initialized
   - Server registers required tools
   - Tool schemas are valid
   - Tools are accessible through invoke
   - Unknown tool returns error

3. **Dependency Validation** (4 tests)
   - boto3 is available
   - pytest is available
   - hypothesis is available
   - Server validates dependencies on start

4. **Configuration Loading** (3 tests)
   - Default configuration is valid
   - Custom configuration is applied
   - MCP config template is valid

5. **Documentation** (4 tests)
   - POWER.md has installation instructions
   - POWER.md has usage examples
   - POWER.md has configuration options
   - POWER.md has error handling guide

**Total: 23 tests**

## Running the Tests

### Run All Integration Tests
```bash
pytest tests/integration/ -v
```

### Run Specific Test File
```bash
pytest tests/integration/test_end_to_end.py -v
pytest tests/integration/test_power_installation.py -v
```

### Run with Coverage
```bash
pytest tests/integration/ --cov=src --cov-report=html
```

### Run Specific Test Class
```bash
pytest tests/integration/test_end_to_end.py::TestCompleteTranslationFlow -v
pytest tests/integration/test_power_installation.py::TestMCPServerRegistration -v
```

## Test Requirements

All integration tests use mocked AWS Bedrock calls to avoid:
- Actual AWS API costs
- Network dependencies
- AWS credential requirements during testing

The tests verify:
- Complete request/response flows
- Error handling across all layers
- MCP protocol compliance
- Configuration application
- Package structure and dependencies
- Documentation completeness

## Test Results

All 41 integration tests pass successfully:
- ✅ 18 end-to-end tests
- ✅ 23 power installation tests

## Requirements Validated

These integration tests validate the following requirements:

- **1.1**: Plain text translation input
- **1.2**: File-based translation input
- **1.3**: AWS Bedrock Nova Pro translation
- **1.4**: Translation result response
- **1.5**: Invalid input error handling
- **1.7**: File not found error handling
- **2.1**: Streaming response support
- **2.2**: Streaming data chunks
- **2.3**: Streaming completion signal
- **3.1**: Java sample code generation
- **3.2**: Python sample code generation
- **3.3**: Node.js sample code generation
- **3.4**: Sample code comments
- **3.5**: Unsupported language error
- **4.4**: MCP server registration
- **6.1**: Error validation and messages
- **6.5**: AWS service error handling
- **7.1**: Configuration application
- **7.5**: AWS region configuration
- **8.5**: AWS rate limit handling

## Notes

- Tests use Python's `unittest.mock` for mocking AWS services
- Temporary files are created and cleaned up automatically
- All tests are isolated and can run in any order
- Tests verify both success and error scenarios
