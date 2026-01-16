"""
Property-based tests for Translation Engine.

Tests translation round-trip, successful responses, and streaming behavior.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings, assume

from translation_engine import TranslationEngine, TranslationEngineError
from bedrock_client import BedrockClient, BedrockClientError
from models import TranslationConfig, TranslationResult, TranslationChunk


# Feature: translation-power, Property 2: Translation Round-Trip Through AWS
# Validates: Requirements 1.3, 8.2, 8.3
@settings(max_examples=20, deadline=None)
@given(
    text=st.text(min_size=1, max_size=500),
    source_lang=st.sampled_from(['en', 'es', 'fr', 'de', 'auto']),
    target_lang=st.sampled_from(['en', 'es', 'fr', 'de', 'ja', 'zh']),
    temperature=st.floats(min_value=0.0, max_value=1.0),
    max_tokens=st.integers(min_value=100, max_value=4000)
)
def test_property_translation_round_trip_through_aws(
    text, source_lang, target_lang, temperature, max_tokens
):
    """
    Property 2: Translation Round-Trip Through AWS
    
    For any valid text input, when the Translation_Engine processes it,
    the engine should format an appropriate prompt for Nova Pro, invoke
    AWS Bedrock, and extract translated text from the response.
    
    This test verifies that:
    1. The engine formats a proper prompt with language instructions
    2. The engine invokes AWS Bedrock with correct parameters
    3. The engine parses the response and extracts translated text
    4. The complete round-trip succeeds for any valid input
    """
    # Skip if text is only whitespace
    assume(text.strip())
    
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig(
        temperature=temperature,
        max_tokens=max_tokens,
        max_input_length=10000
    )
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Mock AWS response with translated text
    mock_response = {
        'completion': f'Translated: {text[:50]}...'
    }
    mock_bedrock_client.invoke_model.return_value = mock_response
    
    # Perform translation
    result = engine.translate(text, source_lang, target_lang, stream=False)
    
    # Verify the round-trip completed successfully
    assert isinstance(result, TranslationResult)
    assert result.translated_text
    assert result.source_language == source_lang
    assert result.target_language == target_lang
    assert result.model_used
    
    # Verify AWS Bedrock was invoked
    assert mock_bedrock_client.invoke_model.called
    call_args = mock_bedrock_client.invoke_model.call_args
    
    # Verify model ID was provided
    assert call_args[1]['model_id']
    
    # Verify prompt was formatted (should contain the text and language info)
    prompt = call_args[1]['prompt']
    assert text in prompt
    assert target_lang in prompt.lower() or target_lang in prompt
    
    # Verify parameters were passed
    params = call_args[1]['parameters']
    assert params['temperature'] == temperature
    assert params['max_tokens'] == max_tokens


# Feature: translation-power, Property 3: Successful Translation Response
# Validates: Requirements 1.4
@settings(max_examples=20, deadline=None)
@given(
    text=st.text(min_size=1, max_size=500),
    target_lang=st.sampled_from(['en', 'es', 'fr', 'de', 'ja', 'zh']),
    response_format=st.sampled_from([
        'completion',
        'output_text',
        'output_dict',
        'text',
        'results'
    ])
)
def test_property_successful_translation_response(text, target_lang, response_format):
    """
    Property 3: Successful Translation Response
    
    For any valid translation request, when translation completes successfully,
    the Client should receive the translated text in the response.
    
    This test verifies that:
    1. The engine returns a TranslationResult for successful translations
    2. The result contains the translated text
    3. The result includes metadata (source/target languages, model, timestamp)
    4. Various AWS response formats are handled correctly
    """
    # Skip if text is only whitespace
    assume(text.strip())
    
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Create mock response in different formats
    translated_text = f"Translated: {text[:50]}"
    
    if response_format == 'completion':
        mock_response = {'completion': translated_text}
    elif response_format == 'output_text':
        mock_response = {'output': translated_text}
    elif response_format == 'output_dict':
        mock_response = {'output': {'text': translated_text}}
    elif response_format == 'text':
        mock_response = {'text': translated_text}
    elif response_format == 'results':
        mock_response = {'results': [{'outputText': translated_text}]}
    
    mock_bedrock_client.invoke_model.return_value = mock_response
    
    # Perform translation
    result = engine.translate(text, target_lang=target_lang, stream=False)
    
    # Verify successful response
    assert isinstance(result, TranslationResult)
    # parse_response strips whitespace, so we need to compare with stripped version
    assert result.translated_text == translated_text.strip()
    assert result.target_language == target_lang
    assert result.source_language  # Should have a source language
    assert result.model_used  # Should have model ID
    assert result.timestamp  # Should have timestamp


# Feature: translation-power, Property 6: Streaming Response Behavior
# Validates: Requirements 2.1, 2.2, 2.3
@settings(max_examples=20, deadline=None)
@given(
    text=st.text(min_size=1, max_size=500),
    target_lang=st.sampled_from(['en', 'es', 'fr', 'de']),
    num_chunks=st.integers(min_value=1, max_value=10)
)
def test_property_streaming_response_behavior(text, target_lang, num_chunks):
    """
    Property 6: Streaming Response Behavior
    
    For any translation request with streaming enabled, the MCP_Server should
    send response chunks incrementally as they become available and signal
    completion when the stream ends.
    
    This test verifies that:
    1. Streaming returns an iterator of TranslationChunk objects
    2. Chunks are yielded incrementally
    3. The final chunk signals completion (is_complete=True)
    4. All chunks contain text or completion signal
    """
    # Skip if text is only whitespace
    assume(text.strip())
    
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Create mock streaming response
    def mock_stream():
        for i in range(num_chunks):
            chunk_data = {
                'completion': f'Chunk {i}: {text[:20]}...'
            }
            yield chunk_data
    
    mock_bedrock_client.invoke_model_stream.return_value = mock_stream()
    
    # Perform streaming translation
    result_stream = engine.translate(text, target_lang=target_lang, stream=True)
    
    # Collect all chunks
    chunks = list(result_stream)
    
    # Verify streaming behavior
    assert len(chunks) > 0
    
    # All chunks should be TranslationChunk objects
    for chunk in chunks:
        assert isinstance(chunk, TranslationChunk)
    
    # The last chunk should signal completion
    assert chunks[-1].is_complete == True
    
    # All non-final chunks should have is_complete=False
    for chunk in chunks[:-1]:
        assert chunk.is_complete == False
    
    # At least some chunks should have text content
    text_chunks = [c for c in chunks if c.chunk]
    assert len(text_chunks) > 0


# Feature: translation-power, Property 7: Streaming Error Handling
# Validates: Requirements 2.4
@settings(max_examples=20, deadline=None)
@given(
    text=st.text(min_size=1, max_size=500),
    target_lang=st.sampled_from(['en', 'es', 'fr', 'de']),
    error_type=st.sampled_from([
        'bedrock_error',
        'unexpected_error'
    ])
)
def test_property_streaming_error_handling(text, target_lang, error_type):
    """
    Property 7: Streaming Error Handling
    
    For any error that occurs during streaming, the MCP_Server should send
    an error notification and terminate the stream gracefully without leaving
    the client in an undefined state.
    
    This test verifies that:
    1. Errors during streaming are caught
    2. An error chunk is yielded with error information
    3. The stream terminates with is_complete=True
    4. TranslationEngineError is raised after yielding error chunk
    """
    # Skip if text is only whitespace
    assume(text.strip())
    
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Simulate error during streaming
    if error_type == 'bedrock_error':
        mock_bedrock_client.invoke_model_stream.side_effect = BedrockClientError(
            "AWS Bedrock error during streaming"
        )
    else:
        mock_bedrock_client.invoke_model_stream.side_effect = Exception(
            "Unexpected error during streaming"
        )
    
    # Perform streaming translation
    result_stream = engine.translate(text, target_lang=target_lang, stream=True)
    
    # Collect chunks and expect error
    chunks = []
    with pytest.raises(TranslationEngineError):
        for chunk in result_stream:
            chunks.append(chunk)
    
    # Verify error handling
    assert len(chunks) > 0
    
    # Should have received at least one chunk
    last_chunk = chunks[-1]
    assert isinstance(last_chunk, TranslationChunk)
    
    # The last chunk should signal completion
    assert last_chunk.is_complete == True
    
    # The last chunk should contain error information
    assert 'error' in last_chunk.chunk.lower()


@settings(max_examples=20, deadline=None)
@given(
    text=st.text(min_size=1, max_size=500),
    source_lang=st.sampled_from(['en', 'es', 'fr', 'de', 'auto']),
    target_lang=st.sampled_from(['en', 'es', 'fr', 'de', 'ja'])
)
def test_property_prompt_formatting_consistency(text, source_lang, target_lang):
    """
    Property: Prompt formatting should be consistent and include all necessary information.
    
    For any text and language pair, the formatted prompt should:
    1. Include the source text
    2. Include language instructions
    3. Be properly structured for Nova Pro
    4. Handle auto-detection when source_lang is 'auto'
    """
    # Skip if text is only whitespace
    assume(text.strip())
    
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Format prompt
    prompt = engine.format_prompt(text, source_lang, target_lang)
    
    # Verify prompt structure
    assert text in prompt
    assert target_lang in prompt.lower() or target_lang in prompt
    
    if source_lang == 'auto':
        assert 'detect' in prompt.lower() or 'auto' in prompt.lower()
    else:
        assert source_lang in prompt.lower() or source_lang in prompt
    
    # Prompt should have clear structure
    assert 'translate' in prompt.lower()


@settings(max_examples=20, deadline=None)
@given(
    response_data=st.dictionaries(
        keys=st.sampled_from(['completion', 'output', 'text', 'results', 'other']),
        values=st.one_of(
            st.text(min_size=1, max_size=100),
            st.dictionaries(
                keys=st.sampled_from(['text', 'outputText']),
                values=st.text(min_size=1, max_size=100)
            ),
            st.lists(
                st.dictionaries(
                    keys=st.sampled_from(['outputText']),
                    values=st.text(min_size=1, max_size=100)
                ),
                min_size=1,
                max_size=3
            )
        ),
        min_size=1,
        max_size=3
    )
)
def test_property_response_parsing_robustness(response_data):
    """
    Property: Response parsing should handle various AWS response formats.
    
    For any response structure from AWS Bedrock, the engine should either:
    1. Successfully extract the translated text, or
    2. Raise a clear TranslationEngineError
    
    The parser should never crash with unexpected errors.
    """
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Try to parse the response
    try:
        result = engine.parse_response(response_data)
        # If successful, should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
    except TranslationEngineError as e:
        # If it fails, should raise TranslationEngineError with clear message
        assert str(e)
        assert 'parse' in str(e).lower() or 'response' in str(e).lower()
    except Exception as e:
        # Should not raise unexpected exceptions
        pytest.fail(f"Unexpected exception type: {type(e).__name__}: {str(e)}")


@settings(max_examples=20, deadline=None)
@given(
    text=st.one_of(
        st.just(''),
        st.just('   '),
        st.just('\n\n'),
        st.just('\t\t')
    ),
    target_lang=st.sampled_from(['en', 'es', 'fr'])
)
def test_property_empty_input_validation(text, target_lang):
    """
    Property: Empty or whitespace-only input should be rejected.
    
    For any empty or whitespace-only text, the engine should raise
    TranslationEngineError before attempting to call AWS Bedrock.
    """
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Should raise TranslationEngineError for empty input
    with pytest.raises(TranslationEngineError) as exc_info:
        engine.translate(text, target_lang=target_lang)
    
    assert 'empty' in str(exc_info.value).lower()
    
    # Should NOT have called AWS Bedrock
    assert not mock_bedrock_client.invoke_model.called


@settings(max_examples=20, deadline=None)
@given(
    text_length=st.integers(min_value=10001, max_value=20000),
    target_lang=st.sampled_from(['en', 'es', 'fr'])
)
def test_property_max_length_validation(text_length, target_lang):
    """
    Property: Input exceeding max_input_length should be rejected.
    
    For any text exceeding the configured max_input_length, the engine
    should raise TranslationEngineError before attempting to call AWS Bedrock.
    """
    # Create mock Bedrock client
    mock_bedrock_client = Mock(spec=BedrockClient)
    
    # Create translation config with default max_input_length=10000
    config = TranslationConfig()
    
    # Create translation engine
    engine = TranslationEngine(mock_bedrock_client, config)
    
    # Create text that exceeds max length
    text = 'a' * text_length
    
    # Should raise TranslationEngineError for oversized input
    with pytest.raises(TranslationEngineError) as exc_info:
        engine.translate(text, target_lang=target_lang)
    
    assert 'maximum length' in str(exc_info.value).lower() or 'exceeds' in str(exc_info.value).lower()
    
    # Should NOT have called AWS Bedrock
    assert not mock_bedrock_client.invoke_model.called
