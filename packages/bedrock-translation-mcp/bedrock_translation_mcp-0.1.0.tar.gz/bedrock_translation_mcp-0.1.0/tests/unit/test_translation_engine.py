"""
Unit tests for Translation Engine.

Tests prompt formatting, response parsing, streaming, and error handling.
Requirements: 8.2, 8.3, 2.1
"""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest

from translation_engine import TranslationEngine, TranslationEngineError
from bedrock_client import BedrockClient, BedrockClientError, BedrockServiceError
from models import TranslationConfig, TranslationResult, TranslationChunk


class TestPromptFormatting:
    """Test suite for prompt formatting."""
    
    def test_format_prompt_with_explicit_languages(self):
        """Test prompt formatting with explicit source and target languages."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        text = "Hello, world!"
        prompt = engine.format_prompt(text, "en", "es")
        
        assert text in prompt
        assert "en" in prompt.lower() or "english" in prompt.lower()
        assert "es" in prompt.lower() or "spanish" in prompt.lower()
        assert "translate" in prompt.lower()
    
    def test_format_prompt_with_auto_detection(self):
        """Test prompt formatting with automatic language detection."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        text = "Bonjour le monde!"
        prompt = engine.format_prompt(text, "auto", "en")
        
        assert text in prompt
        assert "detect" in prompt.lower() or "auto" in prompt.lower()
        assert "en" in prompt.lower() or "english" in prompt.lower()
    
    def test_format_prompt_with_various_texts(self):
        """Test prompt formatting with various text inputs."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        test_cases = [
            "Simple text",
            "Text with numbers: 123, 456",
            "Text with special chars: @#$%",
            "Multi-line\ntext\nwith\nbreaks",
            "Text with unicode: 你好世界 🌍"
        ]
        
        for text in test_cases:
            prompt = engine.format_prompt(text, "auto", "en")
            assert text in prompt
            assert "translate" in prompt.lower()


class TestResponseParsing:
    """Test suite for response parsing."""
    
    def test_parse_response_completion_format(self):
        """Test parsing response with 'completion' field."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'completion': 'Translated text here'}
        result = engine.parse_response(response)
        
        assert result == 'Translated text here'
    
    def test_parse_response_output_text_format(self):
        """Test parsing response with 'output' as text."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'output': 'Translated text here'}
        result = engine.parse_response(response)
        
        assert result == 'Translated text here'
    
    def test_parse_response_output_dict_format(self):
        """Test parsing response with 'output' as dictionary."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'output': {'text': 'Translated text here'}}
        result = engine.parse_response(response)
        
        assert result == 'Translated text here'
    
    def test_parse_response_text_format(self):
        """Test parsing response with 'text' field."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'text': 'Translated text here'}
        result = engine.parse_response(response)
        
        assert result == 'Translated text here'
    
    def test_parse_response_results_format(self):
        """Test parsing response with 'results' array."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'results': [{'outputText': 'Translated text here'}]}
        result = engine.parse_response(response)
        
        assert result == 'Translated text here'
    
    def test_parse_response_strips_whitespace(self):
        """Test that response parsing strips leading/trailing whitespace."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'completion': '  \n  Translated text  \n  '}
        result = engine.parse_response(response)
        
        assert result == 'Translated text'
    
    def test_parse_response_invalid_format_raises_error(self):
        """Test that invalid response format raises TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'unknown_field': 'some value'}
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.parse_response(response)
        
        assert 'parse' in str(exc_info.value).lower() or 'response' in str(exc_info.value).lower()
    
    def test_parse_response_empty_text_raises_error(self):
        """Test that empty extracted text raises TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        response = {'completion': '   '}
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.parse_response(response)
        
        assert 'empty' in str(exc_info.value).lower()


class TestSynchronousTranslation:
    """Test suite for synchronous translation."""
    
    def test_successful_translation(self):
        """Test successful synchronous translation."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        # Mock AWS response
        mock_bedrock.invoke_model.return_value = {
            'completion': 'Hola, mundo!'
        }
        
        result = engine.translate("Hello, world!", source_lang="en", target_lang="es")
        
        assert isinstance(result, TranslationResult)
        assert result.translated_text == 'Hola, mundo!'
        assert result.source_language == 'en'
        assert result.target_language == 'es'
        assert result.model_used
        assert result.timestamp
        
        # Verify AWS was called
        mock_bedrock.invoke_model.assert_called_once()
    
    def test_translation_with_default_languages(self):
        """Test translation using default language settings."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig(
            default_source_lang='auto',
            default_target_lang='en'
        )
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model.return_value = {
            'completion': 'Hello, world!'
        }
        
        result = engine.translate("Bonjour le monde!")
        
        assert result.source_language == 'auto'
        assert result.target_language == 'en'
    
    def test_translation_with_custom_parameters(self):
        """Test translation with custom temperature and max_tokens."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig(
            temperature=0.5,
            max_tokens=1000
        )
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model.return_value = {
            'completion': 'Translated text'
        }
        
        engine.translate("Test text", target_lang="es")
        
        # Verify parameters were passed
        call_args = mock_bedrock.invoke_model.call_args
        params = call_args[1]['parameters']
        assert params['temperature'] == 0.5
        assert params['max_tokens'] == 1000
    
    def test_translation_empty_input_raises_error(self):
        """Test that empty input raises TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("", target_lang="es")
        
        assert 'empty' in str(exc_info.value).lower()
        mock_bedrock.invoke_model.assert_not_called()
    
    def test_translation_whitespace_input_raises_error(self):
        """Test that whitespace-only input raises TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("   \n\t  ", target_lang="es")
        
        assert 'empty' in str(exc_info.value).lower()
        mock_bedrock.invoke_model.assert_not_called()
    
    def test_translation_exceeds_max_length_raises_error(self):
        """Test that input exceeding max_input_length raises error."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig(max_input_length=100)
        engine = TranslationEngine(mock_bedrock, config)
        
        long_text = "a" * 101
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate(long_text, target_lang="es")
        
        assert 'maximum length' in str(exc_info.value).lower() or 'exceeds' in str(exc_info.value).lower()
        mock_bedrock.invoke_model.assert_not_called()
    
    def test_translation_bedrock_error_raises_translation_error(self):
        """Test that BedrockClientError is wrapped in TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model.side_effect = BedrockServiceError("AWS error")
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("Test text", target_lang="es")
        
        assert 'translation failed' in str(exc_info.value).lower()


class TestStreamingTranslation:
    """Test suite for streaming translation."""
    
    def test_successful_streaming_translation(self):
        """Test successful streaming translation."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        # Mock streaming response
        def mock_stream():
            yield {'completion': 'Chunk 1 '}
            yield {'completion': 'Chunk 2 '}
            yield {'completion': 'Chunk 3'}
        
        mock_bedrock.invoke_model_stream.return_value = mock_stream()
        
        result_stream = engine.translate("Test text", target_lang="es", stream=True)
        chunks = list(result_stream)
        
        # Should have text chunks + completion chunk
        assert len(chunks) > 0
        assert all(isinstance(chunk, TranslationChunk) for chunk in chunks)
        
        # Last chunk should signal completion
        assert chunks[-1].is_complete == True
        
        # Earlier chunks should have is_complete=False
        for chunk in chunks[:-1]:
            assert chunk.is_complete == False
    
    def test_streaming_with_various_chunk_formats(self):
        """Test streaming with various AWS chunk formats."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        # Mock streaming response with different formats
        def mock_stream():
            yield {'completion': 'Format 1'}
            yield {'delta': {'text': 'Format 2'}}
            yield {'text': 'Format 3'}
            yield {'outputText': 'Format 4'}
        
        mock_bedrock.invoke_model_stream.return_value = mock_stream()
        
        result_stream = engine.translate("Test", target_lang="es", stream=True)
        chunks = list(result_stream)
        
        # Should successfully parse all formats
        text_chunks = [c for c in chunks if c.chunk and not c.is_complete]
        assert len(text_chunks) == 4
    
    def test_streaming_with_empty_chunks(self):
        """Test streaming handles chunks with no text gracefully."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        # Mock streaming response with some empty chunks
        def mock_stream():
            yield {'completion': 'Text 1'}
            yield {'unknown_field': 'value'}  # No text
            yield {'completion': 'Text 2'}
        
        mock_bedrock.invoke_model_stream.return_value = mock_stream()
        
        result_stream = engine.translate("Test", target_lang="es", stream=True)
        chunks = list(result_stream)
        
        # Should handle empty chunks without error
        assert len(chunks) > 0
        assert chunks[-1].is_complete == True
    
    def test_streaming_bedrock_error_yields_error_chunk(self):
        """Test that streaming errors yield error chunk before raising."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model_stream.side_effect = BedrockServiceError("AWS error")
        
        result_stream = engine.translate("Test", target_lang="es", stream=True)
        
        chunks = []
        with pytest.raises(TranslationEngineError):
            for chunk in result_stream:
                chunks.append(chunk)
        
        # Should have yielded at least one error chunk
        assert len(chunks) > 0
        assert chunks[-1].is_complete == True
        assert 'error' in chunks[-1].chunk.lower()
    
    def test_streaming_unexpected_error_yields_error_chunk(self):
        """Test that unexpected streaming errors yield error chunk."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model_stream.side_effect = Exception("Unexpected error")
        
        result_stream = engine.translate("Test", target_lang="es", stream=True)
        
        chunks = []
        with pytest.raises(TranslationEngineError):
            for chunk in result_stream:
                chunks.append(chunk)
        
        # Should have yielded error chunk
        assert len(chunks) > 0
        assert chunks[-1].is_complete == True
        assert 'error' in chunks[-1].chunk.lower()


class TestErrorHandling:
    """Test suite for error handling during translation."""
    
    def test_bedrock_authentication_error_wrapped(self):
        """Test that Bedrock authentication errors are wrapped properly."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        from bedrock_client import BedrockAuthenticationError
        mock_bedrock.invoke_model.side_effect = BedrockAuthenticationError("Auth failed")
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("Test", target_lang="es")
        
        assert 'translation failed' in str(exc_info.value).lower()
    
    def test_bedrock_rate_limit_error_wrapped(self):
        """Test that Bedrock rate limit errors are wrapped properly."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        from bedrock_client import BedrockRateLimitError
        mock_bedrock.invoke_model.side_effect = BedrockRateLimitError("Rate limited")
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("Test", target_lang="es")
        
        assert 'translation failed' in str(exc_info.value).lower()
    
    def test_unexpected_error_wrapped(self):
        """Test that unexpected errors are wrapped in TranslationEngineError."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        mock_bedrock.invoke_model.side_effect = RuntimeError("Unexpected error")
        
        with pytest.raises(TranslationEngineError) as exc_info:
            engine.translate("Test", target_lang="es")
        
        assert 'unexpected error' in str(exc_info.value).lower()


class TestStreamChunkParsing:
    """Test suite for stream chunk parsing."""
    
    def test_parse_stream_chunk_completion_format(self):
        """Test parsing chunk with 'completion' field."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'completion': 'Chunk text'}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == 'Chunk text'
    
    def test_parse_stream_chunk_delta_text_format(self):
        """Test parsing chunk with 'delta' containing 'text'."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'delta': {'text': 'Chunk text'}}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == 'Chunk text'
    
    def test_parse_stream_chunk_delta_string_format(self):
        """Test parsing chunk with 'delta' as string."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'delta': 'Chunk text'}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == 'Chunk text'
    
    def test_parse_stream_chunk_text_format(self):
        """Test parsing chunk with 'text' field."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'text': 'Chunk text'}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == 'Chunk text'
    
    def test_parse_stream_chunk_output_text_format(self):
        """Test parsing chunk with 'outputText' field."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'outputText': 'Chunk text'}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == 'Chunk text'
    
    def test_parse_stream_chunk_unknown_format_returns_empty(self):
        """Test that unknown chunk format returns empty string."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        chunk_data = {'unknown_field': 'value'}
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == ''
    
    def test_parse_stream_chunk_error_returns_empty(self):
        """Test that parsing errors return empty string."""
        mock_bedrock = Mock(spec=BedrockClient)
        config = TranslationConfig()
        engine = TranslationEngine(mock_bedrock, config)
        
        # Invalid chunk data that might cause errors
        chunk_data = None
        result = engine._parse_stream_chunk(chunk_data)
        
        assert result == ''
