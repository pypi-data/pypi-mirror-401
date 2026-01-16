"""
Unit tests for MCP Server functionality.

Tests server startup/shutdown, tool registration, dependency validation,
and tool handlers with various inputs.

Requirements: 4.4, 5.1, 5.2, 6.3, 6.4
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from server import MCPServer, handle_translate, handle_get_sample_code, MCPServerError
from models import ServerConfig, TranslationConfig, TranslationResult, SampleCodeResult, TranslationError


class TestMCPServerLifecycle:
    """Test server startup and shutdown."""
    
    def test_server_initialization(self):
        """Test that server initializes with configuration."""
        config = ServerConfig(
            host="localhost",
            port=8080,
            log_level="INFO"
        )
        
        server = MCPServer(config)
        
        assert server.config == config
        assert server.is_running is False
        assert len(server.tools) == 0
    
    @patch('server.BedrockClient')
    @patch('server.TranslationEngine')
    @patch('server.InputHandler')
    @patch('server.SampleCodeGenerator')
    def test_server_start_initializes_components(
        self,
        mock_sample_gen,
        mock_input_handler,
        mock_translation_engine,
        mock_bedrock_client
    ):
        """Test that server start initializes all components."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Start the server
        server.start()
        
        # Verify server is running
        assert server.is_running is True
        
        # Verify components were initialized
        assert server.bedrock_client is not None
        assert server.translation_engine is not None
        assert server.input_handler is not None
        assert server.sample_code_generator is not None
        
        # Verify tools were registered
        assert 'translate' in server.tools
        assert 'get_sample_code' in server.tools
    
    @patch('server.BedrockClient')
    @patch('server.TranslationEngine')
    @patch('server.InputHandler')
    @patch('server.SampleCodeGenerator')
    def test_server_stop_cleans_up(
        self,
        mock_sample_gen,
        mock_input_handler,
        mock_translation_engine,
        mock_bedrock_client
    ):
        """Test that server stop cleans up resources."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Start then stop the server
        server.start()
        server.stop()
        
        # Verify server is not running
        assert server.is_running is False
        
        # Verify components were cleaned up
        assert server.bedrock_client is None
        assert server.translation_engine is None
        assert server.input_handler is None
        assert server.sample_code_generator is None
        
        # Verify tools were cleared
        assert len(server.tools) == 0


class TestToolRegistration:
    """Test tool registration mechanism."""
    
    def test_register_tool_adds_tool(self):
        """Test that register_tool adds a tool to the server."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Create a mock handler
        handler = Mock()
        schema = {"type": "object"}
        
        # Register the tool
        server.register_tool("test_tool", handler, schema)
        
        # Verify tool was registered
        assert "test_tool" in server.tools
        assert server.tools["test_tool"]["handler"] == handler
        assert server.tools["test_tool"]["schema"] == schema
    
    def test_register_duplicate_tool_raises_error(self):
        """Test that registering a duplicate tool raises an error."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Register a tool
        handler = Mock()
        schema = {"type": "object"}
        server.register_tool("test_tool", handler, schema)
        
        # Try to register the same tool again
        with pytest.raises(MCPServerError, match="already registered"):
            server.register_tool("test_tool", handler, schema)


class TestDependencyValidation:
    """Test dependency validation at startup."""
    
    def test_validate_dependencies_runs_without_error(self):
        """Test that dependency validation runs without error when dependencies are available."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Should not raise an error since boto3 is installed
        try:
            server._validate_dependencies()
        except MCPServerError:
            pytest.fail("Dependency validation should not raise error when boto3 is available")


class TestTranslateTool:
    """Test translate tool handler with various inputs."""
    
    def test_translate_with_plain_text(self):
        """Test translation with plain text input."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.input_handler = Mock()
        server.input_handler.process_input.return_value = "Hello world"
        
        server.translation_engine = Mock()
        mock_result = TranslationResult(
            translated_text="Hola mundo",
            source_language="en",
            target_language="es",
            model_used="test-model"
        )
        server.translation_engine.translate.return_value = mock_result
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'input': 'Hello world',
            'target_lang': 'es'
        }
        result = handle_translate(params, server)
        
        # Verify result
        assert 'error' not in result
        assert result['translated_text'] == "Hola mundo"
        assert result['source_language'] == "en"
        assert result['target_language'] == "es"
        
        # Verify components were called correctly
        server.input_handler.process_input.assert_called_once_with('Hello world', is_file=False)
        server.translation_engine.translate.assert_called_once()
    
    def test_translate_with_file_path(self):
        """Test translation with file path input."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.input_handler = Mock()
        server.input_handler.process_input.return_value = "File content"
        
        server.translation_engine = Mock()
        mock_result = TranslationResult(
            translated_text="Contenido del archivo",
            source_language="en",
            target_language="es",
            model_used="test-model"
        )
        server.translation_engine.translate.return_value = mock_result
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'input': '/path/to/file.txt',
            'is_file': True,
            'target_lang': 'es'
        }
        result = handle_translate(params, server)
        
        # Verify result
        assert 'error' not in result
        assert result['translated_text'] == "Contenido del archivo"
        
        # Verify file was read
        server.input_handler.process_input.assert_called_once_with('/path/to/file.txt', is_file=True)
    
    def test_translate_with_missing_input_returns_error(self):
        """Test that missing input parameter returns validation error."""
        config = ServerConfig()
        server = MCPServer(config)
        server.logger = Mock()
        
        # Call with missing input
        params = {
            'target_lang': 'es'
        }
        result = handle_translate(params, server)
        
        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'validation'
        assert 'input' in result['error']['message']
    
    def test_translate_with_file_not_found_returns_error(self):
        """Test that file not found returns appropriate error."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.input_handler = Mock()
        server.input_handler.process_input.side_effect = FileNotFoundError("File not found")
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'input': '/nonexistent/file.txt',
            'is_file': True,
            'target_lang': 'es'
        }
        result = handle_translate(params, server)
        
        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'file'
        assert 'not found' in result['error']['message'].lower()


class TestGetSampleCodeTool:
    """Test get_sample_code tool handler with various languages."""
    
    def test_get_sample_code_for_java(self):
        """Test sample code generation for Java."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="public class Test {}",
            language="java",
            description="Java sample"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'language': 'java'
        }
        result = handle_get_sample_code(params, server)
        
        # Verify result
        assert 'error' not in result
        assert result['code'] == "public class Test {}"
        assert result['language'] == "java"
        assert result['description'] == "Java sample"
        
        # Verify generator was called
        server.sample_code_generator.generate_sample.assert_called_once_with(
            language='java',
            include_comments=True
        )
    
    def test_get_sample_code_for_python(self):
        """Test sample code generation for Python."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="def test(): pass",
            language="python",
            description="Python sample"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'language': 'python'
        }
        result = handle_get_sample_code(params, server)
        
        # Verify result
        assert 'error' not in result
        assert result['language'] == "python"
    
    def test_get_sample_code_for_nodejs(self):
        """Test sample code generation for Node.js."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="const test = () => {};",
            language="nodejs",
            description="Node.js sample"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'language': 'nodejs'
        }
        result = handle_get_sample_code(params, server)
        
        # Verify result
        assert 'error' not in result
        assert result['language'] == "nodejs"
    
    def test_get_sample_code_with_unsupported_language_returns_error(self):
        """Test that unsupported language returns validation error."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.sample_code_generator = Mock()
        server.sample_code_generator.generate_sample.side_effect = TranslationError(
            error_type="validation",
            message="Unsupported language: ruby",
            details={"requested_language": "ruby"}
        )
        
        server.logger = Mock()
        
        # Call the handler
        params = {
            'language': 'ruby'
        }
        result = handle_get_sample_code(params, server)
        
        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'validation'
        assert 'Unsupported' in result['error']['message']
    
    def test_get_sample_code_with_missing_language_returns_error(self):
        """Test that missing language parameter returns validation error."""
        config = ServerConfig()
        server = MCPServer(config)
        server.logger = Mock()
        
        # Call with missing language
        params = {}
        result = handle_get_sample_code(params, server)
        
        # Verify error response
        assert 'error' in result
        assert result['error']['code'] == 'validation'
        assert 'language' in result['error']['message']


class TestMCPResponseFormat:
    """Test MCP response format compliance."""
    
    def test_success_response_format(self):
        """Test that success responses follow MCP format."""
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="test",
            language="python",
            description="test"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        server.logger = Mock()
        
        # Call the handler
        params = {'language': 'python'}
        result = handle_get_sample_code(params, server)
        
        # Verify response is a dictionary
        assert isinstance(result, dict)
        
        # Verify no error field in success response
        assert 'error' not in result
        
        # Verify expected fields are present
        assert 'code' in result
        assert 'language' in result
        assert 'description' in result
    
    def test_error_response_format(self):
        """Test that error responses follow MCP format."""
        config = ServerConfig()
        server = MCPServer(config)
        server.logger = Mock()
        
        # Call with invalid parameters
        params = {}
        result = handle_get_sample_code(params, server)
        
        # Verify response is a dictionary
        assert isinstance(result, dict)
        
        # Verify error structure
        assert 'error' in result
        assert isinstance(result['error'], dict)
        
        # Verify error fields
        assert 'code' in result['error']
        assert 'message' in result['error']
        assert 'data' in result['error']
        
        # Verify data structure
        assert isinstance(result['error']['data'], dict)
        assert 'error_type' in result['error']['data']
        assert 'details' in result['error']['data']
        assert 'timestamp' in result['error']['data']
