"""
AWS Bedrock client for Translation Power.

This module provides a client for interacting with AWS Bedrock Runtime API,
supporting both synchronous and streaming model invocations with error handling
and retry logic.

Requirements: 1.3, 1.6, 8.1, 8.4
"""

import time
import json
from typing import Optional, Dict, Any, Iterator
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from botocore.config import Config


class BedrockClientError(Exception):
    """Base exception for Bedrock client errors."""
    pass


class BedrockAuthenticationError(BedrockClientError):
    """Exception raised for authentication/authorization errors."""
    pass


class BedrockRateLimitError(BedrockClientError):
    """Exception raised when rate limits are exceeded."""
    pass


class BedrockServiceError(BedrockClientError):
    """Exception raised for AWS service errors."""
    pass


class BedrockClient:
    """
    Client for AWS Bedrock Runtime API.
    
    Handles model invocations with retry logic, error handling, and support
    for both synchronous and streaming responses.
    """
    
    def __init__(
        self,
        region: Optional[str] = None,
        credentials: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the Bedrock client.
        
        Args:
            region: AWS region for Bedrock API (defaults to AWS_REGION env var or us-east-1)
            credentials: Optional dict with 'aws_access_key_id', 'aws_secret_access_key',
                        and optionally 'aws_session_token'. If not provided, uses default
                        AWS credential chain.
            max_retries: Maximum number of retry attempts for transient errors
            timeout: Request timeout in seconds
        
        Raises:
            BedrockAuthenticationError: If credentials are invalid or missing
        """
        self.region = region or "us-east-1"
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Configure boto3 client with retry settings
        import certifi
        config = Config(
            region_name=self.region,
            retries={'max_attempts': 0},  # We handle retries manually
            connect_timeout=timeout,
            read_timeout=timeout,
            signature_version='v4'
        )
        
        # Set SSL certificate path
        import os
        os.environ['AWS_CA_BUNDLE'] = certifi.where()
        
        try:
            # Initialize the Bedrock Runtime client
            if credentials:
                self.client = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region,
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token'),
                    config=config
                )
            else:
                self.client = boto3.client(
                    'bedrock-runtime',
                    region_name=self.region,
                    config=config
                )
            
            # Validate credentials by attempting to get caller identity
            # This is a lightweight call to verify credentials work
            sts = boto3.client('sts', region_name=self.region)
            sts.get_caller_identity()
            
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise BedrockAuthenticationError(
                f"AWS credentials not found or incomplete: {str(e)}"
            ) from e
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch', 'AccessDenied', 'UnauthorizedException']:
                raise BedrockAuthenticationError(
                    f"AWS authentication failed: {str(e)}"
                ) from e
            raise BedrockServiceError(f"Failed to initialize Bedrock client: {str(e)}") from e
    
    def invoke_model(
        self,
        model_id: str,
        prompt: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synchronously invoke a Bedrock model.
        
        Args:
            model_id: The Bedrock model identifier (e.g., 'amazon.nova-pro-v1:0')
            prompt: The prompt text to send to the model
            parameters: Optional model parameters (temperature, max_tokens, etc.)
        
        Returns:
            Dictionary containing the model response
        
        Raises:
            BedrockAuthenticationError: If authentication fails
            BedrockRateLimitError: If rate limits are exceeded
            BedrockServiceError: For other AWS service errors
        """
        # Prepare the request body
        body = self._prepare_request_body(prompt, parameters)
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType='application/json',
                    accept='application/json'
                )
                
                # Parse and return the response
                response_body = json.loads(response['body'].read())
                return response_body
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                error_message = e.response.get('Error', {}).get('Message', str(e))
                
                # Handle authentication errors (don't retry)
                if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch', 'AccessDenied', 'UnauthorizedException']:
                    raise BedrockAuthenticationError(
                        f"Authentication failed: {error_message}"
                    ) from e
                
                # Handle rate limiting (retry with backoff)
                if error_code in ['ThrottlingException', 'TooManyRequestsException']:
                    last_exception = BedrockRateLimitError(
                        f"Rate limit exceeded: {error_message}"
                    )
                    if attempt < self.max_retries:
                        wait_time = self._calculate_backoff(attempt)
                        time.sleep(wait_time)
                        continue
                    raise last_exception from e
                
                # Handle transient errors (retry with backoff)
                if error_code in ['ServiceUnavailable', 'InternalServerError', 'RequestTimeout']:
                    last_exception = BedrockServiceError(
                        f"AWS service error: {error_message}"
                    )
                    if attempt < self.max_retries:
                        wait_time = self._calculate_backoff(attempt)
                        time.sleep(wait_time)
                        continue
                    raise last_exception from e
                
                # Other errors (don't retry)
                raise BedrockServiceError(
                    f"Bedrock API error ({error_code}): {error_message}"
                ) from e
            
            except Exception as e:
                # Unexpected errors
                raise BedrockServiceError(
                    f"Unexpected error invoking model: {str(e)}"
                ) from e
        
        # Should not reach here, but just in case
        if last_exception:
            raise last_exception
        raise BedrockServiceError("Max retries exceeded")
    
    def invoke_model_stream(
        self,
        model_id: str,
        prompt: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Invoke a Bedrock model with streaming response.
        
        Args:
            model_id: The Bedrock model identifier
            prompt: The prompt text to send to the model
            parameters: Optional model parameters
        
        Yields:
            Dictionary chunks from the streaming response
        
        Raises:
            BedrockAuthenticationError: If authentication fails
            BedrockRateLimitError: If rate limits are exceeded
            BedrockServiceError: For other AWS service errors
        """
        # Prepare the request body
        body = self._prepare_request_body(prompt, parameters)
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.invoke_model_with_response_stream(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType='application/json',
                    accept='application/json'
                )
                
                # Stream the response chunks
                stream = response.get('body')
                if stream:
                    for event in stream:
                        chunk = event.get('chunk')
                        if chunk:
                            chunk_data = json.loads(chunk.get('bytes').decode())
                            yield chunk_data
                
                # Successfully completed streaming
                return
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                error_message = e.response.get('Error', {}).get('Message', str(e))
                
                # Handle authentication errors (don't retry)
                if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch', 'AccessDenied', 'UnauthorizedException']:
                    raise BedrockAuthenticationError(
                        f"Authentication failed: {error_message}"
                    ) from e
                
                # Handle rate limiting (retry with backoff)
                if error_code in ['ThrottlingException', 'TooManyRequestsException']:
                    last_exception = BedrockRateLimitError(
                        f"Rate limit exceeded: {error_message}"
                    )
                    if attempt < self.max_retries:
                        wait_time = self._calculate_backoff(attempt)
                        time.sleep(wait_time)
                        continue
                    raise last_exception from e
                
                # Handle transient errors (retry with backoff)
                if error_code in ['ServiceUnavailable', 'InternalServerError', 'RequestTimeout']:
                    last_exception = BedrockServiceError(
                        f"AWS service error: {error_message}"
                    )
                    if attempt < self.max_retries:
                        wait_time = self._calculate_backoff(attempt)
                        time.sleep(wait_time)
                        continue
                    raise last_exception from e
                
                # Other errors (don't retry)
                raise BedrockServiceError(
                    f"Bedrock API error ({error_code}): {error_message}"
                ) from e
            
            except Exception as e:
                # Unexpected errors
                raise BedrockServiceError(
                    f"Unexpected error invoking model: {str(e)}"
                ) from e
        
        # Should not reach here, but just in case
        if last_exception:
            raise last_exception
        raise BedrockServiceError("Max retries exceeded")
    
    def _prepare_request_body(
        self,
        prompt: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare the request body for Bedrock API (Nova Pro format).
        
        Args:
            prompt: The prompt text
            parameters: Optional model parameters
        
        Returns:
            Dictionary with the request body structure for Nova Pro
        """
        # Nova Pro uses the messages format
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {}
        }
        
        if parameters:
            # Add parameters to inferenceConfig
            if 'temperature' in parameters:
                body['inferenceConfig']['temperature'] = parameters['temperature']
            if 'max_tokens' in parameters:
                body['inferenceConfig']['maxTokens'] = parameters['max_tokens']
            if 'top_p' in parameters:
                body['inferenceConfig']['topP'] = parameters['top_p']
            if 'stop_sequences' in parameters:
                body['inferenceConfig']['stopSequences'] = parameters['stop_sequences']
        
        return body
    
    def _calculate_backoff(self, attempt: int) -> float:
        """
        Calculate exponential backoff wait time.
        
        Args:
            attempt: The current attempt number (0-indexed)
        
        Returns:
            Wait time in seconds
        """
        # Exponential backoff: 1s, 2s, 4s, 8s, etc.
        base_wait = 1.0
        return base_wait * (2 ** attempt)
