"""
Translation Engine for Translation Power.

This module provides the core translation functionality using AWS Bedrock Nova Pro LLM.
It handles prompt formatting, response parsing, and supports both synchronous and
streaming translation modes.

Requirements: 1.3, 1.4, 2.1, 8.2, 8.3
"""

from typing import Optional, Iterator, Union

try:
    from .bedrock_client import BedrockClient, BedrockClientError
    from .models import TranslationConfig, TranslationResult, TranslationChunk
except ImportError:
    from bedrock_client import BedrockClient, BedrockClientError
    from models import TranslationConfig, TranslationResult, TranslationChunk


class TranslationEngineError(Exception):
    """Base exception for translation engine errors."""
    pass


class TranslationEngine:
    """
    Translation engine that uses AWS Bedrock Nova Pro for text translation.
    
    Supports both synchronous and streaming translation modes with configurable
    parameters for temperature, max tokens, and language detection.
    """
    
    def __init__(self, bedrock_client: BedrockClient, config: TranslationConfig):
        """
        Initialize the translation engine.
        
        Args:
            bedrock_client: Configured BedrockClient instance
            config: TranslationConfig with engine settings
        """
        self.bedrock_client = bedrock_client
        self.config = config
    
    def translate(
        self,
        text: str,
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None,
        stream: bool = False
    ) -> Union[TranslationResult, Iterator[TranslationChunk]]:
        """
        Translate text from source language to target language.
        
        Args:
            text: The text to translate
            source_lang: Source language code (e.g., 'en', 'es', 'fr').
                        If None or 'auto', language will be auto-detected.
            target_lang: Target language code. If None, uses config default.
            stream: If True, returns an iterator of TranslationChunk objects.
                   If False, returns a complete TranslationResult.
        
        Returns:
            TranslationResult for synchronous mode, or
            Iterator[TranslationChunk] for streaming mode
        
        Raises:
            TranslationEngineError: If translation fails
            BedrockClientError: If AWS Bedrock API call fails
        """
        # Validate input
        if not text or not text.strip():
            raise TranslationEngineError("Input text cannot be empty")
        
        if len(text) > self.config.max_input_length:
            raise TranslationEngineError(
                f"Input text exceeds maximum length of {self.config.max_input_length} characters"
            )
        
        # Use defaults if not provided
        source_lang = source_lang or self.config.default_source_lang
        target_lang = target_lang or self.config.default_target_lang
        
        # Format the prompt
        prompt = self.format_prompt(text, source_lang, target_lang)
        
        # Prepare model parameters
        parameters = {
            'temperature': self.config.temperature,
            'max_tokens': self.config.max_tokens
        }
        
        # Get model ID from bedrock_client's region-based config or use default
        model_id = "amazon.nova-pro-v1:0"
        
        try:
            if stream:
                # Return streaming iterator
                return self._translate_stream(model_id, prompt, parameters, source_lang, target_lang)
            else:
                # Synchronous translation
                response = self.bedrock_client.invoke_model(
                    model_id=model_id,
                    prompt=prompt,
                    parameters=parameters
                )
                
                # Parse the response
                translated_text = self.parse_response(response)
                
                # Return result
                return TranslationResult(
                    translated_text=translated_text,
                    source_language=source_lang,
                    target_language=target_lang,
                    model_used=model_id
                )
        
        except BedrockClientError as e:
            raise TranslationEngineError(f"Translation failed: {str(e)}") from e
        except Exception as e:
            raise TranslationEngineError(f"Unexpected error during translation: {str(e)}") from e
    
    def format_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Format the translation prompt for Nova Pro.
        
        Creates a clear, structured prompt that instructs the model to translate
        the given text from source to target language.
        
        Args:
            text: The text to translate
            source_lang: Source language code or 'auto' for auto-detection
            target_lang: Target language code
        
        Returns:
            Formatted prompt string
        """
        # Build language instruction
        if source_lang == "auto":
            lang_instruction = f"Translate the following text to {target_lang}. Detect the source language automatically."
        else:
            lang_instruction = f"Translate the following text from {source_lang} to {target_lang}."
        
        # Format the complete prompt
        prompt = f"""{lang_instruction}

Text to translate:
{text}

Translation:"""
        
        return prompt
    
    def parse_response(self, response: dict) -> str:
        """
        Extract translated text from Bedrock response.
        
        Handles various response formats from AWS Bedrock Nova Pro and extracts
        the translated text content.
        
        Args:
            response: Dictionary containing the Bedrock API response
        
        Returns:
            Extracted translated text
        
        Raises:
            TranslationEngineError: If response format is invalid or text cannot be extracted
        """
        try:
            # Nova Pro response format uses 'output' with 'message' structure
            if 'output' in response:
                output = response['output']
                if isinstance(output, dict) and 'message' in output:
                    # Nova Pro format: output.message.content[0].text
                    message = output['message']
                    if isinstance(message, dict) and 'content' in message:
                        content = message['content']
                        if isinstance(content, list) and len(content) > 0:
                            if isinstance(content[0], dict) and 'text' in content[0]:
                                translated_text = content[0]['text']
                            else:
                                translated_text = str(content[0])
                        else:
                            translated_text = str(content)
                    else:
                        translated_text = str(message)
                elif isinstance(output, dict) and 'text' in output:
                    translated_text = output['text']
                elif isinstance(output, str):
                    translated_text = output
                else:
                    translated_text = str(output)
            elif 'completion' in response:
                translated_text = response['completion']
            elif 'text' in response:
                translated_text = response['text']
            elif 'results' in response:
                # Handle results array format
                results = response['results']
                if results and len(results) > 0:
                    if isinstance(results[0], dict) and 'outputText' in results[0]:
                        translated_text = results[0]['outputText']
                    else:
                        translated_text = str(results[0])
                else:
                    raise TranslationEngineError("Empty results in response")
            else:
                # Fallback: try to find any text-like field
                raise TranslationEngineError(
                    f"Unable to parse response format. Available keys: {list(response.keys())}"
                )
            
            # Clean up the translated text
            translated_text = translated_text.strip()
            
            if not translated_text:
                raise TranslationEngineError("Extracted text is empty")
            
            return translated_text
        
        except KeyError as e:
            raise TranslationEngineError(f"Missing expected field in response: {str(e)}") from e
        except Exception as e:
            raise TranslationEngineError(f"Error parsing response: {str(e)}") from e
    
    def _translate_stream(
        self,
        model_id: str,
        prompt: str,
        parameters: dict,
        source_lang: str,
        target_lang: str
    ) -> Iterator[TranslationChunk]:
        """
        Perform streaming translation.
        
        Args:
            model_id: Bedrock model identifier
            prompt: Formatted translation prompt
            parameters: Model parameters
            source_lang: Source language code
            target_lang: Target language code
        
        Yields:
            TranslationChunk objects containing incremental translation results
        
        Raises:
            TranslationEngineError: If streaming fails
        """
        try:
            # Invoke streaming API
            stream = self.bedrock_client.invoke_model_stream(
                model_id=model_id,
                prompt=prompt,
                parameters=parameters
            )
            
            # Process stream chunks
            for chunk_data in stream:
                # Extract text from chunk
                chunk_text = self._parse_stream_chunk(chunk_data)
                
                if chunk_text:
                    yield TranslationChunk(
                        chunk=chunk_text,
                        is_complete=False
                    )
            
            # Signal completion
            yield TranslationChunk(
                chunk="",
                is_complete=True
            )
        
        except BedrockClientError as e:
            # Send error chunk
            yield TranslationChunk(
                chunk=f"Error: {str(e)}",
                is_complete=True
            )
            raise TranslationEngineError(f"Streaming translation failed: {str(e)}") from e
        except Exception as e:
            # Send error chunk
            yield TranslationChunk(
                chunk=f"Error: {str(e)}",
                is_complete=True
            )
            raise TranslationEngineError(f"Unexpected error during streaming: {str(e)}") from e
    
    def _parse_stream_chunk(self, chunk_data: dict) -> str:
        """
        Parse a single streaming chunk from Bedrock.
        
        Args:
            chunk_data: Dictionary containing chunk data
        
        Returns:
            Extracted text from the chunk, or empty string if no text
        """
        try:
            # Handle various chunk formats
            if 'completion' in chunk_data:
                return chunk_data['completion']
            elif 'delta' in chunk_data:
                delta = chunk_data['delta']
                if isinstance(delta, dict) and 'text' in delta:
                    return delta['text']
                elif isinstance(delta, str):
                    return delta
            elif 'text' in chunk_data:
                return chunk_data['text']
            elif 'outputText' in chunk_data:
                return chunk_data['outputText']
            
            # No text in this chunk
            return ""
        
        except Exception:
            # If we can't parse the chunk, return empty string
            return ""
