"""
Power installation verification tests.

Tests that verify the Translation Power can be properly installed in Kiro,
including MCP server registration and tool accessibility.

Requirements: 4.4
"""

import pytest
import json
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from server import MCPServer
from models import ServerConfig


class TestPowerPackageStructure:
    """Verify the power package has the correct structure."""
    
    def test_power_md_exists(self):
        """Test that POWER.md documentation exists."""
        power_root = Path(__file__).parent.parent.parent
        power_md = power_root / 'POWER.md'
        
        assert power_md.exists(), "POWER.md file is missing"
        assert power_md.is_file(), "POWER.md is not a file"
        
        # Verify it has content
        content = power_md.read_text(encoding='utf-8')
        assert len(content) > 0, "POWER.md is empty"
        assert 'Translation Power' in content, "POWER.md doesn't contain expected title"
    
    def test_package_json_exists(self):
        """Test that package.json metadata exists."""
        power_root = Path(__file__).parent.parent.parent
        package_json = power_root / 'package.json'
        
        assert package_json.exists(), "package.json file is missing"
        assert package_json.is_file(), "package.json is not a file"
        
        # Verify it's valid JSON
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify required fields
        assert 'name' in data, "package.json missing 'name' field"
        assert 'version' in data, "package.json missing 'version' field"
        assert 'description' in data, "package.json missing 'description' field"
    
    def test_mcp_config_exists(self):
        """Test that MCP configuration template exists."""
        power_root = Path(__file__).parent.parent.parent
        mcp_config = power_root / 'mcp-config.json'
        
        assert mcp_config.exists(), "mcp-config.json file is missing"
        assert mcp_config.is_file(), "mcp-config.json is not a file"
        
        # Verify it's valid JSON
        with open(mcp_config, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify structure
        assert 'mcpServers' in data, "mcp-config.json missing 'mcpServers' field"
        assert 'translation-power' in data['mcpServers'], "mcp-config.json missing 'translation-power' server"
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        power_root = Path(__file__).parent.parent.parent
        requirements = power_root / 'requirements.txt'
        
        assert requirements.exists(), "requirements.txt file is missing"
        assert requirements.is_file(), "requirements.txt is not a file"
        
        # Verify it has content
        content = requirements.read_text(encoding='utf-8')
        assert len(content) > 0, "requirements.txt is empty"
        
        # Verify key dependencies
        assert 'boto3' in content, "requirements.txt missing boto3 dependency"
        assert 'pytest' in content, "requirements.txt missing pytest dependency"
    
    def test_src_directory_structure(self):
        """Test that src directory has all required modules."""
        power_root = Path(__file__).parent.parent.parent
        src_dir = power_root / 'src'
        
        assert src_dir.exists(), "src directory is missing"
        assert src_dir.is_dir(), "src is not a directory"
        
        # Check for required modules
        required_modules = [
            'server.py',
            'translation_engine.py',
            'bedrock_client.py',
            'sample_code_gen.py',
            'input_handler.py',
            'models.py',
            'config.py'
        ]
        
        for module in required_modules:
            module_path = src_dir / module
            assert module_path.exists(), f"Required module {module} is missing"
            assert module_path.is_file(), f"{module} is not a file"
    
    def test_templates_directory_structure(self):
        """Test that templates directory has all required templates."""
        power_root = Path(__file__).parent.parent.parent
        templates_dir = power_root / 'templates'
        
        assert templates_dir.exists(), "templates directory is missing"
        assert templates_dir.is_dir(), "templates is not a directory"
        
        # Check for required templates
        required_templates = [
            'java_sample.txt',
            'python_sample.txt',
            'nodejs_sample.txt'
        ]
        
        for template in required_templates:
            template_path = templates_dir / template
            assert template_path.exists(), f"Required template {template} is missing"
            assert template_path.is_file(), f"{template} is not a file"
            
            # Verify template has content
            content = template_path.read_text(encoding='utf-8')
            assert len(content) > 0, f"Template {template} is empty"
    
    def test_tests_directory_structure(self):
        """Test that tests directory has proper structure."""
        power_root = Path(__file__).parent.parent.parent
        tests_dir = power_root / 'tests'
        
        assert tests_dir.exists(), "tests directory is missing"
        assert tests_dir.is_dir(), "tests is not a directory"
        
        # Check for test subdirectories
        assert (tests_dir / 'unit').exists(), "tests/unit directory is missing"
        assert (tests_dir / 'property').exists(), "tests/property directory is missing"
        assert (tests_dir / 'integration').exists(), "tests/integration directory is missing"


class TestMCPServerRegistration:
    """Test MCP server registration and tool availability."""
    
    def test_server_can_be_initialized(self):
        """Test that MCP server can be initialized with configuration."""
        config = ServerConfig(
            host="localhost",
            port=8080,
            log_level="INFO",
            aws_region="us-east-1"
        )
        
        server = MCPServer(config)
        
        assert server is not None
        assert server.config == config
        assert server.is_running is False
    
    def test_server_registers_required_tools(self):
        """Test that server registers all required tools on startup."""
        from unittest.mock import patch
        
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock AWS components to avoid actual AWS calls
        with patch('server.BedrockClient'), \
             patch('server.TranslationEngine'), \
             patch('server.InputHandler'), \
             patch('server.SampleCodeGenerator'):
            
            server.start()
            
            try:
                # Verify server is running
                assert server.is_running is True
                
                # Verify required tools are registered
                assert 'translate' in server.tools, "translate tool not registered"
                assert 'get_sample_code' in server.tools, "get_sample_code tool not registered"
                
                # Verify tool structure
                translate_tool = server.tools['translate']
                assert 'handler' in translate_tool, "translate tool missing handler"
                assert 'schema' in translate_tool, "translate tool missing schema"
                
                sample_code_tool = server.tools['get_sample_code']
                assert 'handler' in sample_code_tool, "get_sample_code tool missing handler"
                assert 'schema' in sample_code_tool, "get_sample_code tool missing schema"
                
            finally:
                server.stop()
    
    def test_tool_schemas_are_valid(self):
        """Test that tool schemas are properly formatted."""
        from unittest.mock import patch
        
        config = ServerConfig()
        server = MCPServer(config)
        
        with patch('server.BedrockClient'), \
             patch('server.TranslationEngine'), \
             patch('server.InputHandler'), \
             patch('server.SampleCodeGenerator'):
            
            server.start()
            
            try:
                # Check translate tool schema
                translate_schema = server.tools['translate']['schema']
                assert 'type' in translate_schema
                assert translate_schema['type'] == 'object'
                assert 'properties' in translate_schema
                assert 'required' in translate_schema
                
                # Verify required parameters
                assert 'input' in translate_schema['properties']
                assert 'target_lang' in translate_schema['properties']
                assert 'input' in translate_schema['required']
                assert 'target_lang' in translate_schema['required']
                
                # Check get_sample_code tool schema
                sample_code_schema = server.tools['get_sample_code']['schema']
                assert 'type' in sample_code_schema
                assert sample_code_schema['type'] == 'object'
                assert 'properties' in sample_code_schema
                assert 'required' in sample_code_schema
                
                # Verify required parameters
                assert 'language' in sample_code_schema['properties']
                assert 'language' in sample_code_schema['required']
                
            finally:
                server.stop()
    
    def test_tools_are_accessible_through_invoke(self):
        """Test that registered tools can be invoked through the server."""
        from unittest.mock import patch, Mock
        
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock AWS components
        mock_bedrock = Mock()
        mock_bedrock.invoke_model.return_value = {'completion': 'Test translation'}
        
        with patch('server.BedrockClient', return_value=mock_bedrock), \
             patch('server.TranslationEngine'), \
             patch('server.InputHandler'), \
             patch('server.SampleCodeGenerator'):
            
            server.start()
            
            try:
                # Test that translate tool is accessible
                result = server.invoke_tool('translate', {
                    'input': 'test',
                    'target_lang': 'es'
                })
                
                # Should return a result (not an error about unknown tool)
                assert result is not None
                assert isinstance(result, dict)
                
                # Test that get_sample_code tool is accessible
                result = server.invoke_tool('get_sample_code', {
                    'language': 'python'
                })
                
                # Should return a result
                assert result is not None
                assert isinstance(result, dict)
                
            finally:
                server.stop()
    
    def test_unknown_tool_returns_error(self):
        """Test that invoking an unknown tool returns an appropriate error."""
        from unittest.mock import patch
        
        config = ServerConfig()
        server = MCPServer(config)
        
        with patch('server.BedrockClient'), \
             patch('server.TranslationEngine'), \
             patch('server.InputHandler'), \
             patch('server.SampleCodeGenerator'):
            
            server.start()
            
            try:
                # Try to invoke a non-existent tool
                result = server.invoke_tool('nonexistent_tool', {})
                
                # Should return an error
                assert 'error' in result
                assert result['error']['code'] == 'protocol'
                assert 'Unknown tool' in result['error']['message']
                
            finally:
                server.stop()


class TestDependencyValidation:
    """Test dependency validation during installation."""
    
    def test_boto3_is_available(self):
        """Test that boto3 dependency is available."""
        try:
            import boto3
            assert True
        except ImportError:
            pytest.fail("boto3 is not installed - required dependency missing")
    
    def test_pytest_is_available(self):
        """Test that pytest dependency is available."""
        try:
            import pytest
            assert True
        except ImportError:
            pytest.fail("pytest is not installed - required dependency missing")
    
    def test_hypothesis_is_available(self):
        """Test that hypothesis dependency is available."""
        try:
            import hypothesis
            assert True
        except ImportError:
            pytest.fail("hypothesis is not installed - required dependency missing")
    
    def test_server_validates_dependencies_on_start(self):
        """Test that server validates dependencies during startup."""
        from unittest.mock import patch
        
        config = ServerConfig()
        server = MCPServer(config)
        
        # Mock AWS components
        with patch('server.BedrockClient'), \
             patch('server.TranslationEngine'), \
             patch('server.InputHandler'), \
             patch('server.SampleCodeGenerator'):
            
            # Should not raise an error if dependencies are available
            try:
                server.start()
                assert server.is_running is True
            finally:
                server.stop()


class TestConfigurationLoading:
    """Test configuration loading from various sources."""
    
    def test_default_configuration_is_valid(self):
        """Test that default configuration is valid."""
        config = ServerConfig()
        
        assert config.host is not None
        assert config.port is not None
        assert config.log_level is not None
        assert config.aws_region is not None
        assert config.model_id is not None
    
    def test_custom_configuration_is_applied(self):
        """Test that custom configuration values are applied."""
        config = ServerConfig(
            host="0.0.0.0",
            port=9090,
            log_level="DEBUG",
            aws_region="eu-west-1",
            model_id="custom-model"
        )
        
        assert config.host == "0.0.0.0"
        assert config.port == 9090
        assert config.log_level == "DEBUG"
        assert config.aws_region == "eu-west-1"
        assert config.model_id == "custom-model"
    
    def test_mcp_config_template_is_valid(self):
        """Test that the MCP configuration template is valid and complete."""
        power_root = Path(__file__).parent.parent.parent
        mcp_config = power_root / 'mcp-config.json'
        
        with open(mcp_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verify server configuration
        server_config = config['mcpServers']['translation-power']
        
        assert 'command' in server_config, "MCP config missing 'command'"
        assert 'args' in server_config, "MCP config missing 'args'"
        assert 'env' in server_config, "MCP config missing 'env'"
        
        # Verify environment variables
        env = server_config['env']
        assert 'AWS_REGION' in env, "MCP config missing AWS_REGION"
        assert 'MODEL_ID' in env, "MCP config missing MODEL_ID"


class TestDocumentation:
    """Test that documentation is complete and accurate."""
    
    def test_power_md_has_installation_instructions(self):
        """Test that POWER.md includes installation instructions."""
        power_root = Path(__file__).parent.parent.parent
        power_md = power_root / 'POWER.md'
        
        content = power_md.read_text(encoding='utf-8')
        
        # Check for key sections
        assert '## Installation' in content, "POWER.md missing Installation section"
        assert 'Prerequisites' in content, "POWER.md missing Prerequisites"
        assert 'AWS' in content, "POWER.md missing AWS setup information"
    
    def test_power_md_has_usage_examples(self):
        """Test that POWER.md includes usage examples."""
        power_root = Path(__file__).parent.parent.parent
        power_md = power_root / 'POWER.md'
        
        content = power_md.read_text(encoding='utf-8')
        
        # Check for usage documentation
        assert '## Usage' in content, "POWER.md missing Usage section"
        assert 'translate' in content, "POWER.md missing translate tool documentation"
        assert 'get_sample_code' in content, "POWER.md missing get_sample_code tool documentation"
        assert 'Example' in content, "POWER.md missing examples"
    
    def test_power_md_has_configuration_options(self):
        """Test that POWER.md documents configuration options."""
        power_root = Path(__file__).parent.parent.parent
        power_md = power_root / 'POWER.md'
        
        content = power_md.read_text(encoding='utf-8')
        
        # Check for configuration documentation
        assert 'Configuration' in content, "POWER.md missing Configuration section"
        assert 'AWS_REGION' in content, "POWER.md missing AWS_REGION documentation"
        assert 'MODEL_ID' in content, "POWER.md missing MODEL_ID documentation"
    
    def test_power_md_has_error_handling_guide(self):
        """Test that POWER.md includes error handling information."""
        power_root = Path(__file__).parent.parent.parent
        power_md = power_root / 'POWER.md'
        
        content = power_md.read_text(encoding='utf-8')
        
        # Check for error handling documentation
        assert 'Error' in content, "POWER.md missing error handling information"
        assert 'Troubleshooting' in content, "POWER.md missing troubleshooting section"
