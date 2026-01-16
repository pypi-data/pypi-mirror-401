"""
Unit tests for AWS Bedrock client.

Tests successful model invocation, streaming, credential validation, and rate limiting.
Requirements: 8.1, 8.4, 8.5
"""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from botocore.exceptions import ClientError, NoCredentialsError

from bedrock_client import (
    BedrockClient,
    BedrockAuthenticationError,
    BedrockRateLimitError,
    BedrockServiceError
)


class TestBedrockClientInitialization:
    """Test suite for BedrockClient initialization."""
    
    def test_successful_initialization_with_credentials(self):
        """Test successful client initialization with explicit credentials."""
        credentials = {
            'aws_access_key_id': 'AKIAIOSFODNN7EXAMPLE',
            'aws_secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        }
        
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient(region='us-west-2', credentials=credentials)
            
            assert client.region == 'us-west-2'
            assert client.max_retries == 3
            assert client.timeout == 30
            mock_sts.get_caller_identity.assert_called_once()
    
    def test_successful_initialization_without_credentials(self):
        """Test successful client initialization using default credential chain."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            
            assert client.region == 'us-east-1'  # default region
            mock_sts.get_caller_identity.assert_called_once()
    
    def test_initialization_with_custom_retry_and_timeout(self):
        """Test client initialization with custom retry and timeout settings."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient(max_retries=5, timeout=60)
            
            assert client.max_retries == 5
            assert client.timeout == 60
    
    def test_initialization_fails_with_no_credentials(self):
        """Test that initialization fails when no credentials are available."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            mock_sts.get_caller_identity.side_effect = NoCredentialsError()
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            with pytest.raises(BedrockAuthenticationError) as exc_info:
                BedrockClient()
            
            assert "credentials" in str(exc_info.value).lower()
    
    def test_initialization_fails_with_invalid_credentials(self):
        """Test that initialization fails with invalid credentials."""
        credentials = {
            'aws_access_key_id': 'INVALID',
            'aws_secret_access_key': 'INVALID'
        }
        
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            error_response = {
                'Error': {
                    'Code': 'InvalidClientTokenId',
                    'Message': 'The security token included in the request is invalid'
                }
            }
            mock_sts.get_caller_identity.side_effect = ClientError(
                error_response, 'GetCallerIdentity'
            )
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            with pytest.raises(BedrockAuthenticationError):
                BedrockClient(credentials=credentials)


class TestBedrockClientInvokeModel:
    """Test suite for synchronous model invocation."""
    
    def test_successful_model_invocation(self):
        """Test successful synchronous model invocation with mocked AWS."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # Mock successful response
            mock_response = {
                'body': BytesIO(json.dumps({
                    'completion': 'Translated text here',
                    'stop_reason': 'end_turn'
                }).encode())
            }
            mock_bedrock.invoke_model.return_value = mock_response
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            result = client.invoke_model(
                model_id='amazon.nova-pro-v1:0',
                prompt='Translate this text',
                parameters={'temperature': 0.3, 'max_tokens': 1000}
            )
            
            assert 'completion' in result
            assert result['completion'] == 'Translated text here'
            mock_bedrock.invoke_model.assert_called_once()
    
    def test_model_invocation_with_authentication_error(self):
        """Test that authentication errors are properly raised."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # Mock authentication error
            error_response = {
                'Error': {
                    'Code': 'UnauthorizedException',
                    'Message': 'User is not authorized'
                }
            }
            mock_bedrock.invoke_model.side_effect = ClientError(
                error_response, 'InvokeModel'
            )
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            
            with pytest.raises(BedrockAuthenticationError):
                client.invoke_model('amazon.nova-pro-v1:0', 'Test prompt')
    
    def test_model_invocation_with_rate_limiting(self):
        """Test rate limiting handling with retries."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # Mock rate limit error
            error_response = {
                'Error': {
                    'Code': 'ThrottlingException',
                    'Message': 'Rate exceeded'
                }
            }
            mock_bedrock.invoke_model.side_effect = ClientError(
                error_response, 'InvokeModel'
            )
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient(max_retries=2)
            
            with patch('bedrock_client.time.sleep'):  # Mock sleep to speed up test
                with pytest.raises(BedrockRateLimitError) as exc_info:
                    client.invoke_model('amazon.nova-pro-v1:0', 'Test prompt')
                
                assert "rate limit" in str(exc_info.value).lower()
                # Should have tried 3 times (initial + 2 retries)
                assert mock_bedrock.invoke_model.call_count == 3
    
    def test_model_invocation_with_transient_error_then_success(self):
        """Test that transient errors are retried and eventually succeed."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # First call fails, second succeeds
            error_response = {
                'Error': {
                    'Code': 'ServiceUnavailable',
                    'Message': 'Service temporarily unavailable'
                }
            }
            success_response = {
                'body': BytesIO(json.dumps({
                    'completion': 'Success after retry'
                }).encode())
            }
            mock_bedrock.invoke_model.side_effect = [
                ClientError(error_response, 'InvokeModel'),
                success_response
            ]
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient(max_retries=2)
            
            with patch('bedrock_client.time.sleep'):  # Mock sleep to speed up test
                result = client.invoke_model('amazon.nova-pro-v1:0', 'Test prompt')
                
                assert result['completion'] == 'Success after retry'
                assert mock_bedrock.invoke_model.call_count == 2


class TestBedrockClientInvokeModelStream:
    """Test suite for streaming model invocation."""
    
    def test_successful_streaming_invocation(self):
        """Test successful streaming invocation with mocked AWS."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # Mock streaming response
            chunk1 = {'chunk': {'bytes': json.dumps({'completion': 'Hello '}).encode()}}
            chunk2 = {'chunk': {'bytes': json.dumps({'completion': 'world'}).encode()}}
            chunk3 = {'chunk': {'bytes': json.dumps({'completion': '!', 'stop_reason': 'end_turn'}).encode()}}
            
            mock_stream = [chunk1, chunk2, chunk3]
            mock_response = {'body': mock_stream}
            mock_bedrock.invoke_model_with_response_stream.return_value = mock_response
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            chunks = list(client.invoke_model_stream(
                model_id='amazon.nova-pro-v1:0',
                prompt='Test prompt'
            ))
            
            assert len(chunks) == 3
            assert chunks[0]['completion'] == 'Hello '
            assert chunks[1]['completion'] == 'world'
            assert chunks[2]['completion'] == '!'
    
    def test_streaming_with_rate_limiting(self):
        """Test that streaming handles rate limiting with retries."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_bedrock = Mock()
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            # Mock rate limit error
            error_response = {
                'Error': {
                    'Code': 'TooManyRequestsException',
                    'Message': 'Too many requests'
                }
            }
            mock_bedrock.invoke_model_with_response_stream.side_effect = ClientError(
                error_response, 'InvokeModelWithResponseStream'
            )
            
            def client_factory(service_name, **kwargs):
                if service_name == 'bedrock-runtime':
                    return mock_bedrock
                elif service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient(max_retries=2)
            
            with patch('bedrock_client.time.sleep'):  # Mock sleep to speed up test
                with pytest.raises(BedrockRateLimitError):
                    list(client.invoke_model_stream('amazon.nova-pro-v1:0', 'Test'))
                
                # Should have tried 3 times (initial + 2 retries)
                assert mock_bedrock.invoke_model_with_response_stream.call_count == 3


class TestBedrockClientHelperMethods:
    """Test suite for helper methods."""
    
    def test_prepare_request_body_with_all_parameters(self):
        """Test request body preparation with all parameters."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            
            parameters = {
                'temperature': 0.7,
                'max_tokens': 2000,
                'top_p': 0.9,
                'top_k': 50,
                'stop_sequences': ['END']
            }
            
            body = client._prepare_request_body('Test prompt', parameters)
            
            assert body['prompt'] == 'Test prompt'
            assert body['temperature'] == 0.7
            assert body['max_tokens'] == 2000
            assert body['top_p'] == 0.9
            assert body['top_k'] == 50
            assert body['stop_sequences'] == ['END']
    
    def test_prepare_request_body_without_parameters(self):
        """Test request body preparation without optional parameters."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            body = client._prepare_request_body('Test prompt', None)
            
            assert body['prompt'] == 'Test prompt'
            assert 'temperature' not in body
            assert 'max_tokens' not in body
    
    def test_calculate_backoff(self):
        """Test exponential backoff calculation."""
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            mock_sts.get_caller_identity.return_value = {'Account': '123456789012'}
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            client = BedrockClient()
            
            assert client._calculate_backoff(0) == 1.0  # 2^0 = 1
            assert client._calculate_backoff(1) == 2.0  # 2^1 = 2
            assert client._calculate_backoff(2) == 4.0  # 2^2 = 4
            assert client._calculate_backoff(3) == 8.0  # 2^3 = 8
