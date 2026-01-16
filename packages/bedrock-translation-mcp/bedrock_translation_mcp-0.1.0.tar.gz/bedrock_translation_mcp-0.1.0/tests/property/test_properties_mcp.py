"""
Property-based tests for MCP server functionality.

Tests MCP protocol compliance, input parameter validation, and error handling
using property-based testing with Hypothesis.

Feature: translation-power
"""

import pytest
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from server import MCPServer, handle_translate, handle_get_sample_code
from models import ServerConfig, TranslationConfig, TranslationResult, SampleCodeResult, TranslationError


# Strategies for generating test data
@st.composite
def invalid_translate_params(draw):
    """Generate invalid parameter combinations for translate tool."""
    choice = draw(st.integers(min_value=0, max_value=5))
    
    if choice == 0:
        # Missing 'input' parameter
        return {
            'target_lang': draw(st.text(min_size=1, max_size=10))
        }
    elif choice == 1:
        # Missing 'target_lang' parameter
        return {
            'input': draw(st.text(min_size=1, max_size=100))
        }
    elif choice == 2:
        # Invalid type for 'input' (not a string)
        return {
            'input': draw(st.integers()),
            'target_lang': draw(st.text(min_size=1, max_size=10))
        }
    elif choice == 3:
        # Invalid type for 'is_file' (not a boolean)
        return {
            'input': draw(st.text(min_size=1, max_size=100)),
            'target_lang': draw(st.text(min_size=1, max_size=10)),
            'is_file': draw(st.text(min_size=1, max_size=10))
        }
    elif choice == 4:
        # Invalid type for 'target_lang' (not a string)
        return {
            'input': draw(st.text(min_size=1, max_size=100)),
            'target_lang': draw(st.integers())
        }
    else:
        # Both required parameters missing
        return {}


@st.composite
def invalid_sample_code_params(draw):
    """Generate invalid parameter combinations for get_sample_code tool."""
    choice = draw(st.integers(min_value=0, max_value=2))
    
    if choice == 0:
        # Missing 'language' parameter
        return {}
    elif choice == 1:
        # Invalid type for 'language' (not a string)
        return {
            'language': draw(st.integers())
        }
    else:
        # Invalid type for 'include_comments' (not a boolean)
        return {
            'language': draw(st.text(min_size=1, max_size=10)),
            'include_comments': draw(st.text(min_size=1, max_size=10))
        }


class TestInputParameterValidation:
    """
    Property 10: Input Parameter Validation
    
    For any tool invocation with invalid parameters, the MCP_Server should
    validate and reject the parameters before processing begins.
    
    Validates: Requirements 5.3
    """
    
    @settings(max_examples=100)
    @given(params=invalid_translate_params())
    def test_translate_rejects_invalid_parameters(self, params):
        """
        Feature: translation-power, Property 10: Input Parameter Validation
        
        Test that translate tool rejects invalid parameters with appropriate error messages.
        """
        # Create a mock server with minimal setup
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components to avoid actual initialization
        server.input_handler = Mock()
        server.translation_engine = Mock()
        server.logger = Mock()
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify that an error response was returned
        assert 'error' in result, "Expected error response for invalid parameters"
        assert 'code' in result['error'], "Error response should have error code"
        assert 'message' in result['error'], "Error response should have error message"
        
        # Verify error type is validation
        assert result['error']['code'] == 'validation', \
            f"Expected validation error, got {result['error']['code']}"
        
        # Verify error message is descriptive
        assert len(result['error']['message']) > 0, "Error message should not be empty"
        
        # Verify that processing did not occur (input_handler and translation_engine not called)
        server.input_handler.process_input.assert_not_called()
        server.translation_engine.translate.assert_not_called()
    
    @settings(max_examples=100)
    @given(params=invalid_sample_code_params())
    def test_get_sample_code_rejects_invalid_parameters(self, params):
        """
        Feature: translation-power, Property 10: Input Parameter Validation
        
        Test that get_sample_code tool rejects invalid parameters with appropriate error messages.
        """
        # Create a mock server with minimal setup
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.sample_code_generator = Mock()
        server.logger = Mock()
        
        # Call the handler
        result = handle_get_sample_code(params, server)
        
        # Verify that an error response was returned
        assert 'error' in result, "Expected error response for invalid parameters"
        assert 'code' in result['error'], "Error response should have error code"
        assert 'message' in result['error'], "Error response should have error message"
        
        # Verify error type is validation
        assert result['error']['code'] == 'validation', \
            f"Expected validation error, got {result['error']['code']}"
        
        # Verify error message is descriptive
        assert len(result['error']['message']) > 0, "Error message should not be empty"
        
        # Verify that processing did not occur
        server.sample_code_generator.generate_sample.assert_not_called()
    
    @settings(max_examples=100)
    @given(
        input_text=st.text(min_size=1, max_size=100),
        target_lang=st.text(min_size=1, max_size=10)
    )
    def test_translate_accepts_valid_parameters(self, input_text, target_lang):
        """
        Feature: translation-power, Property 10: Input Parameter Validation
        
        Test that translate tool accepts valid parameters and proceeds to processing.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.input_handler = Mock()
        server.input_handler.process_input.return_value = input_text
        
        server.translation_engine = Mock()
        mock_result = TranslationResult(
            translated_text="translated",
            source_language="auto",
            target_language=target_lang,
            model_used="test-model"
        )
        server.translation_engine.translate.return_value = mock_result
        
        server.logger = Mock()
        
        # Valid parameters
        params = {
            'input': input_text,
            'target_lang': target_lang
        }
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify no error response
        assert 'error' not in result, "Should not return error for valid parameters"
        
        # Verify processing occurred
        server.input_handler.process_input.assert_called_once()
        server.translation_engine.translate.assert_called_once()
    
    @settings(max_examples=100)
    @given(language=st.sampled_from(['java', 'python', 'nodejs']))
    def test_get_sample_code_accepts_valid_parameters(self, language):
        """
        Feature: translation-power, Property 10: Input Parameter Validation
        
        Test that get_sample_code tool accepts valid parameters and proceeds to processing.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="sample code",
            language=language,
            description="test description"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        
        server.logger = Mock()
        
        # Valid parameters
        params = {
            'language': language
        }
        
        # Call the handler
        result = handle_get_sample_code(params, server)
        
        # Verify no error response
        assert 'error' not in result, "Should not return error for valid parameters"
        
        # Verify processing occurred
        server.sample_code_generator.generate_sample.assert_called_once()


class TestMCPProtocolCompliance:
    """
    Property 12: MCP Protocol Compliance
    
    For any tool execution (successful or failed), the MCP_Server should return
    results in MCP-compliant format matching the protocol schema for success
    or error responses.
    
    Validates: Requirements 5.5, 5.6
    """
    
    @settings(max_examples=100)
    @given(
        input_text=st.text(min_size=1, max_size=100),
        target_lang=st.text(min_size=1, max_size=10)
    )
    def test_successful_translate_returns_mcp_compliant_response(self, input_text, target_lang):
        """
        Feature: translation-power, Property 12: MCP Protocol Compliance
        
        Test that successful translation returns MCP-compliant response format.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.input_handler = Mock()
        server.input_handler.process_input.return_value = input_text
        
        server.translation_engine = Mock()
        mock_result = TranslationResult(
            translated_text="translated text",
            source_language="auto",
            target_language=target_lang,
            model_used="test-model"
        )
        server.translation_engine.translate.return_value = mock_result
        
        server.logger = Mock()
        
        # Valid parameters
        params = {
            'input': input_text,
            'target_lang': target_lang
        }
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify MCP-compliant success response format
        assert isinstance(result, dict), "Response should be a dictionary"
        assert 'error' not in result, "Success response should not contain 'error' field"
        
        # Verify required fields for translation response
        assert 'translated_text' in result, "Response should contain 'translated_text'"
        assert 'source_language' in result, "Response should contain 'source_language'"
        assert 'target_language' in result, "Response should contain 'target_language'"
        assert 'model_used' in result, "Response should contain 'model_used'"
        assert 'timestamp' in result, "Response should contain 'timestamp'"
        
        # Verify field types
        assert isinstance(result['translated_text'], str), "translated_text should be string"
        assert isinstance(result['source_language'], str), "source_language should be string"
        assert isinstance(result['target_language'], str), "target_language should be string"
        assert isinstance(result['model_used'], str), "model_used should be string"
        assert isinstance(result['timestamp'], str), "timestamp should be string"
    
    @settings(max_examples=100)
    @given(params=invalid_translate_params())
    def test_failed_translate_returns_mcp_compliant_error(self, params):
        """
        Feature: translation-power, Property 12: MCP Protocol Compliance
        
        Test that failed translation returns MCP-compliant error response format.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.input_handler = Mock()
        server.translation_engine = Mock()
        server.logger = Mock()
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify MCP-compliant error response format
        assert isinstance(result, dict), "Response should be a dictionary"
        assert 'error' in result, "Error response should contain 'error' field"
        
        # Verify error structure
        error = result['error']
        assert isinstance(error, dict), "Error should be a dictionary"
        assert 'code' in error, "Error should contain 'code' field"
        assert 'message' in error, "Error should contain 'message' field"
        assert 'data' in error, "Error should contain 'data' field"
        
        # Verify field types
        assert isinstance(error['code'], str), "Error code should be string"
        assert isinstance(error['message'], str), "Error message should be string"
        assert isinstance(error['data'], dict), "Error data should be dictionary"
        
        # Verify data structure
        assert 'error_type' in error['data'], "Error data should contain 'error_type'"
        assert 'details' in error['data'], "Error data should contain 'details'"
        assert 'timestamp' in error['data'], "Error data should contain 'timestamp'"
    
    @settings(max_examples=100)
    @given(language=st.sampled_from(['java', 'python', 'nodejs']))
    def test_successful_sample_code_returns_mcp_compliant_response(self, language):
        """
        Feature: translation-power, Property 12: MCP Protocol Compliance
        
        Test that successful sample code generation returns MCP-compliant response format.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.sample_code_generator = Mock()
        mock_result = SampleCodeResult(
            code="sample code",
            language=language,
            description="test description"
        )
        server.sample_code_generator.generate_sample.return_value = mock_result
        
        server.logger = Mock()
        
        # Valid parameters
        params = {
            'language': language
        }
        
        # Call the handler
        result = handle_get_sample_code(params, server)
        
        # Verify MCP-compliant success response format
        assert isinstance(result, dict), "Response should be a dictionary"
        assert 'error' not in result, "Success response should not contain 'error' field"
        
        # Verify required fields for sample code response
        assert 'code' in result, "Response should contain 'code'"
        assert 'language' in result, "Response should contain 'language'"
        assert 'description' in result, "Response should contain 'description'"
        
        # Verify field types
        assert isinstance(result['code'], str), "code should be string"
        assert isinstance(result['language'], str), "language should be string"
        assert isinstance(result['description'], str), "description should be string"
    
    @settings(max_examples=100)
    @given(params=invalid_sample_code_params())
    def test_failed_sample_code_returns_mcp_compliant_error(self, params):
        """
        Feature: translation-power, Property 12: MCP Protocol Compliance
        
        Test that failed sample code generation returns MCP-compliant error response format.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.sample_code_generator = Mock()
        server.logger = Mock()
        
        # Call the handler
        result = handle_get_sample_code(params, server)
        
        # Verify MCP-compliant error response format
        assert isinstance(result, dict), "Response should be a dictionary"
        assert 'error' in result, "Error response should contain 'error' field"
        
        # Verify error structure
        error = result['error']
        assert isinstance(error, dict), "Error should be a dictionary"
        assert 'code' in error, "Error should contain 'code' field"
        assert 'message' in error, "Error should contain 'message' field"
        assert 'data' in error, "Error should contain 'data' field"
        
        # Verify field types
        assert isinstance(error['code'], str), "Error code should be string"
        assert isinstance(error['message'], str), "Error message should be string"
        assert isinstance(error['data'], dict), "Error data should be dictionary"
        
        # Verify data structure
        assert 'error_type' in error['data'], "Error data should contain 'error_type'"
        assert 'details' in error['data'], "Error data should contain 'details'"
        assert 'timestamp' in error['data'], "Error data should contain 'timestamp'"



class TestErrorLogging:
    """
    Property 13: Error Logging and User Messages
    
    For any error encountered by the Translation_Engine, the MCP_Server should
    both log the error details and return a user-friendly error message to the client.
    
    Validates: Requirements 6.2
    """
    
    @settings(max_examples=100)
    @given(
        input_text=st.text(min_size=1, max_size=100),
        target_lang=st.text(min_size=1, max_size=10),
        error_message=st.text(min_size=1, max_size=100)
    )
    def test_translation_errors_are_logged_and_returned(self, input_text, target_lang, error_message):
        """
        Feature: translation-power, Property 13: Error Logging and User Messages
        
        Test that translation errors are both logged and returned to the client.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.input_handler = Mock()
        server.input_handler.process_input.return_value = input_text
        
        server.translation_engine = Mock()
        # Simulate a translation error
        server.translation_engine.translate.side_effect = TranslationError(
            error_type="aws",
            message=error_message,
            details={"test": "error"}
        )
        
        server.logger = Mock()
        
        # Valid parameters
        params = {
            'input': input_text,
            'target_lang': target_lang
        }
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify error was logged
        server.logger.error.assert_called()
        
        # Get the logged message
        logged_calls = server.logger.error.call_args_list
        assert len(logged_calls) > 0, "Error should be logged"
        
        # Verify logged message contains error information
        logged_message = str(logged_calls[0])
        assert len(logged_message) > 0, "Logged message should not be empty"
        
        # Verify error response was returned to client
        assert 'error' in result, "Error response should be returned to client"
        assert 'message' in result['error'], "Error response should contain message"
        
        # Verify user-friendly error message
        user_message = result['error']['message']
        assert isinstance(user_message, str), "Error message should be string"
        assert len(user_message) > 0, "Error message should not be empty"
    
    @settings(max_examples=100)
    @given(
        language=st.text(min_size=1, max_size=20).filter(lambda x: x.lower() not in ['java', 'python', 'nodejs']),
        error_message=st.text(min_size=1, max_size=100)
    )
    def test_sample_code_errors_are_logged_and_returned(self, language, error_message):
        """
        Feature: translation-power, Property 13: Error Logging and User Messages
        
        Test that sample code generation errors are both logged and returned to the client.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.sample_code_generator = Mock()
        # Simulate a sample code generation error
        server.sample_code_generator.generate_sample.side_effect = TranslationError(
            error_type="validation",
            message=error_message,
            details={"test": "error"}
        )
        
        server.logger = Mock()
        
        # Parameters with unsupported language
        params = {
            'language': language
        }
        
        # Call the handler
        result = handle_get_sample_code(params, server)
        
        # Verify error was logged
        server.logger.error.assert_called()
        
        # Get the logged message
        logged_calls = server.logger.error.call_args_list
        assert len(logged_calls) > 0, "Error should be logged"
        
        # Verify logged message contains error information
        logged_message = str(logged_calls[0])
        assert len(logged_message) > 0, "Logged message should not be empty"
        
        # Verify error response was returned to client
        assert 'error' in result, "Error response should be returned to client"
        assert 'message' in result['error'], "Error response should contain message"
        
        # Verify user-friendly error message
        user_message = result['error']['message']
        assert isinstance(user_message, str), "Error message should be string"
        assert len(user_message) > 0, "Error message should not be empty"
    
    @settings(max_examples=100)
    @given(params=invalid_translate_params())
    def test_validation_errors_are_logged(self, params):
        """
        Feature: translation-power, Property 13: Error Logging and User Messages
        
        Test that validation errors are logged.
        """
        # Create a mock server
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock the components
        server.input_handler = Mock()
        server.translation_engine = Mock()
        server.logger = Mock()
        
        # Call the handler
        result = handle_translate(params, server)
        
        # Verify error was logged
        server.logger.error.assert_called()
        
        # Verify error response was returned
        assert 'error' in result, "Error response should be returned"
