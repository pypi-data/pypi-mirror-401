"""
Property-based tests for AWS Bedrock client.

Tests AWS authentication handling and error handling properties.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from bedrock_client import (
    BedrockClient,
    BedrockAuthenticationError,
    BedrockRateLimitError,
    BedrockServiceError
)


# Feature: translation-power, Property 5: AWS Authentication Handling
# Validates: Requirements 1.6
@settings(max_examples=20)
@given(
    region=st.sampled_from(['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']),
    has_credentials=st.booleans()
)
def test_property_aws_authentication_handling(region, has_credentials):
    """
    Property 5: AWS Authentication Handling
    
    For any translation request, when invoking AWS Bedrock, the Translation_Engine
    should properly use AWS credentials for authentication and authorization.
    
    This test verifies that:
    1. Valid credentials are properly passed to boto3
    2. Missing credentials raise BedrockAuthenticationError
    3. Invalid credentials raise BedrockAuthenticationError
    4. The client attempts to validate credentials during initialization
    """
    if has_credentials:
        # Test with valid credentials (mocked)
        credentials = {
            'aws_access_key_id': 'AKIAIOSFODNN7EXAMPLE',
            'aws_secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            'aws_session_token': 'FwoGZXIvYXdzEBYaDExample'
        }
        
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            # Mock both bedrock-runtime and sts clients
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
            
            # Should successfully create client with credentials
            client = BedrockClient(region=region, credentials=credentials)
            
            # Verify credentials were passed to boto3
            assert mock_boto_client.call_count >= 2  # bedrock-runtime and sts
            bedrock_call = [call for call in mock_boto_client.call_args_list 
                          if call[0][0] == 'bedrock-runtime'][0]
            assert bedrock_call[1]['aws_access_key_id'] == credentials['aws_access_key_id']
            assert bedrock_call[1]['aws_secret_access_key'] == credentials['aws_secret_access_key']
            assert bedrock_call[1]['region_name'] == region
            
            # Verify STS was called to validate credentials
            mock_sts.get_caller_identity.assert_called_once()
    else:
        # Test with missing credentials
        with patch('bedrock_client.boto3.client') as mock_boto_client:
            mock_sts = Mock()
            mock_sts.get_caller_identity.side_effect = NoCredentialsError()
            
            def client_factory(service_name, **kwargs):
                if service_name == 'sts':
                    return mock_sts
                return Mock()
            
            mock_boto_client.side_effect = client_factory
            
            # Should raise BedrockAuthenticationError for missing credentials
            with pytest.raises(BedrockAuthenticationError) as exc_info:
                BedrockClient(region=region)
            
            assert "credentials" in str(exc_info.value).lower()


@settings(max_examples=20)
@given(
    error_code=st.sampled_from([
        'InvalidClientTokenId',
        'SignatureDoesNotMatch', 
        'AccessDenied',
        'UnauthorizedException'
    ])
)
def test_property_invalid_credentials_raise_auth_error(error_code):
    """
    Property: Invalid credentials should always raise BedrockAuthenticationError.
    
    For any authentication-related error code from AWS, the client should
    raise BedrockAuthenticationError (not a generic error).
    """
    with patch('bedrock_client.boto3.client') as mock_boto_client:
        mock_sts = Mock()
        
        # Simulate AWS authentication error
        error_response = {
            'Error': {
                'Code': error_code,
                'Message': f'Authentication failed with {error_code}'
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
        
        # Should raise BedrockAuthenticationError
        with pytest.raises(BedrockAuthenticationError):
            BedrockClient(region='us-east-1')



# Feature: translation-power, Property 14: AWS Service Error Handling
# Validates: Requirements 6.5, 8.5
@settings(max_examples=20, deadline=None)
@given(
    error_code=st.sampled_from([
        'ThrottlingException',
        'TooManyRequestsException',
        'ServiceUnavailable',
        'InternalServerError',
        'RequestTimeout',
        'ValidationException',
        'ResourceNotFoundException'
    ]),
    model_id=st.text(min_size=1, max_size=50),
    prompt=st.text(min_size=1, max_size=100)
)
def test_property_aws_service_error_handling(error_code, model_id, prompt):
    """
    Property 14: AWS Service Error Handling
    
    For any AWS Bedrock API failure (including rate limits and throttling),
    the Translation_Engine should return an appropriate error message indicating
    the AWS service issue and handle it gracefully.
    
    This test verifies that:
    1. Rate limit errors raise BedrockRateLimitError
    2. Transient errors are retried with exponential backoff
    3. Non-retryable errors raise BedrockServiceError immediately
    4. Error messages are descriptive and include the error code
    """
    with patch('bedrock_client.boto3.client') as mock_boto_client:
        # Mock successful initialization
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
        
        # Create client
        client = BedrockClient(region='us-east-1', max_retries=2)
        
        # Simulate AWS error during invoke_model
        error_response = {
            'Error': {
                'Code': error_code,
                'Message': f'AWS error: {error_code}'
            }
        }
        mock_bedrock.invoke_model.side_effect = ClientError(
            error_response, 'InvokeModel'
        )
        
        # Test error handling based on error type
        if error_code in ['ThrottlingException', 'TooManyRequestsException']:
            # Rate limit errors should raise BedrockRateLimitError after retries
            with pytest.raises(BedrockRateLimitError) as exc_info:
                client.invoke_model(model_id, prompt)
            
            assert "rate limit" in str(exc_info.value).lower()
            # Should have retried (initial + 2 retries = 3 calls)
            assert mock_bedrock.invoke_model.call_count == 3
            
        elif error_code in ['ServiceUnavailable', 'InternalServerError', 'RequestTimeout']:
            # Transient errors should be retried and raise BedrockServiceError
            with pytest.raises(BedrockServiceError) as exc_info:
                client.invoke_model(model_id, prompt)
            
            assert "service error" in str(exc_info.value).lower() or "aws" in str(exc_info.value).lower()
            # Should have retried (initial + 2 retries = 3 calls)
            assert mock_bedrock.invoke_model.call_count == 3
            
        else:
            # Non-retryable errors should raise BedrockServiceError immediately
            with pytest.raises(BedrockServiceError) as exc_info:
                client.invoke_model(model_id, prompt)
            
            assert error_code in str(exc_info.value) or "bedrock" in str(exc_info.value).lower()
            # Should NOT retry (only 1 call)
            assert mock_bedrock.invoke_model.call_count == 1


@settings(max_examples=20, deadline=None)
@given(
    num_retries=st.integers(min_value=0, max_value=5),
    fail_count=st.integers(min_value=1, max_value=10)
)
def test_property_retry_logic_with_exponential_backoff(num_retries, fail_count):
    """
    Property: Retry logic should use exponential backoff for transient errors.
    
    For any transient error, the client should retry with exponentially
    increasing wait times (1s, 2s, 4s, etc.) up to max_retries.
    """
    with patch('bedrock_client.boto3.client') as mock_boto_client:
        # Mock successful initialization
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
        
        # Create client with specified max_retries
        client = BedrockClient(region='us-east-1', max_retries=num_retries)
        
        # Simulate transient error
        error_response = {
            'Error': {
                'Code': 'ServiceUnavailable',
                'Message': 'Service temporarily unavailable'
            }
        }
        mock_bedrock.invoke_model.side_effect = ClientError(
            error_response, 'InvokeModel'
        )
        
        # Mock time.sleep to track backoff
        with patch('bedrock_client.time.sleep') as mock_sleep:
            with pytest.raises(BedrockServiceError):
                client.invoke_model('test-model', 'test prompt')
            
            # Should attempt initial call + retries (up to max_retries)
            expected_attempts = num_retries + 1  # initial + retries
            assert mock_bedrock.invoke_model.call_count == expected_attempts
            
            # Should have called sleep for each retry (not for initial attempt)
            expected_sleeps = num_retries
            assert mock_sleep.call_count == expected_sleeps
            
            # Verify exponential backoff pattern
            if expected_sleeps > 0:
                sleep_times = [call[0][0] for call in mock_sleep.call_args_list]
                for i, sleep_time in enumerate(sleep_times):
                    expected_time = 1.0 * (2 ** i)  # 1s, 2s, 4s, 8s, etc.
                    assert sleep_time == expected_time


@settings(max_examples=20, deadline=None)
@given(
    error_code=st.sampled_from([
        'ThrottlingException',
        'TooManyRequestsException'
    ]),
    model_id=st.text(min_size=1, max_size=50),
    prompt=st.text(min_size=1, max_size=100)
)
def test_property_streaming_error_handling(error_code, model_id, prompt):
    """
    Property: Streaming invocations should handle errors the same way as synchronous calls.
    
    For any error during streaming, the client should apply the same error
    handling and retry logic as synchronous invocations.
    """
    with patch('bedrock_client.boto3.client') as mock_boto_client:
        # Mock successful initialization
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
        
        # Create client
        client = BedrockClient(region='us-east-1', max_retries=2)
        
        # Simulate AWS error during streaming
        error_response = {
            'Error': {
                'Code': error_code,
                'Message': f'AWS error: {error_code}'
            }
        }
        mock_bedrock.invoke_model_with_response_stream.side_effect = ClientError(
            error_response, 'InvokeModelWithResponseStream'
        )
        
        # Should raise BedrockRateLimitError after retries
        with pytest.raises(BedrockRateLimitError):
            list(client.invoke_model_stream(model_id, prompt))
        
        # Should have retried (initial + 2 retries = 3 calls)
        assert mock_bedrock.invoke_model_with_response_stream.call_count == 3
