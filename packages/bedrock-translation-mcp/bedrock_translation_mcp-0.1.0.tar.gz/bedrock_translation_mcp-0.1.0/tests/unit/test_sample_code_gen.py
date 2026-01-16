"""
Unit tests for sample code generator.

Tests Java, Python, and Node.js code generation, unsupported language errors,
and code syntax validation.
Requirements: 3.1, 3.2, 3.3, 3.5
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from sample_code_gen import SampleCodeGenerator
from models import TranslationError, SampleCodeResult


class TestSampleCodeGenerator:
    """Test suite for SampleCodeGenerator class."""
    
    def test_java_code_generation(self):
        """
        Test Java code generation.
        Requirements: 3.1
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('java')
        
        # Verify result structure
        assert isinstance(result, SampleCodeResult)
        assert result.language == 'java'
        assert result.code is not None
        assert len(result.code) > 0
        assert result.description is not None
        
        # Verify Java-specific content
        assert 'class' in result.code
        assert 'public' in result.code
        
        # Verify comments exist
        assert '//' in result.code or '/*' in result.code
        
        # Verify key integration points are mentioned
        code_lower = result.code.lower()
        assert 'translate' in code_lower
        assert 'mcp' in code_lower or 'server' in code_lower
    
    def test_python_code_generation(self):
        """
        Test Python code generation.
        Requirements: 3.2
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('python')
        
        # Verify result structure
        assert isinstance(result, SampleCodeResult)
        assert result.language == 'python'
        assert result.code is not None
        assert len(result.code) > 0
        assert result.description is not None
        
        # Verify Python-specific content
        assert 'def ' in result.code or 'class ' in result.code
        assert 'import' in result.code
        
        # Verify comments exist
        assert '#' in result.code or '"""' in result.code or "'''" in result.code
        
        # Verify key integration points are mentioned
        code_lower = result.code.lower()
        assert 'translate' in code_lower
        assert 'mcp' in code_lower or 'server' in code_lower
    
    def test_nodejs_code_generation(self):
        """
        Test Node.js code generation.
        Requirements: 3.3
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('nodejs')
        
        # Verify result structure
        assert isinstance(result, SampleCodeResult)
        assert result.language == 'nodejs'
        assert result.code is not None
        assert len(result.code) > 0
        assert result.description is not None
        
        # Verify Node.js-specific content
        assert 'function' in result.code or 'class' in result.code or '=>' in result.code
        assert 'const' in result.code or 'require' in result.code or 'import' in result.code
        
        # Verify comments exist
        assert '//' in result.code or '/*' in result.code
        
        # Verify key integration points are mentioned
        code_lower = result.code.lower()
        assert 'translate' in code_lower
        assert 'mcp' in code_lower or 'server' in code_lower
    
    def test_case_insensitive_language_names(self):
        """Test that language names are case-insensitive."""
        generator = SampleCodeGenerator()
        
        # Test various case combinations
        result_lower = generator.generate_sample('java')
        result_upper = generator.generate_sample('JAVA')
        result_mixed = generator.generate_sample('Java')
        
        # All should return the same language
        assert result_lower.language == 'java'
        assert result_upper.language == 'java'
        assert result_mixed.language == 'java'
        
        # Code should be identical
        assert result_lower.code == result_upper.code
        assert result_lower.code == result_mixed.code
    
    def test_unsupported_language_error(self):
        """
        Test that unsupported languages raise appropriate errors.
        Requirements: 3.5
        """
        generator = SampleCodeGenerator()
        
        # Test various unsupported languages
        unsupported_languages = ['ruby', 'go', 'rust', 'c++', 'csharp', 'php']
        
        for language in unsupported_languages:
            with pytest.raises(TranslationError) as exc_info:
                generator.generate_sample(language)
            
            error = exc_info.value
            assert error.error_type == "validation"
            assert "unsupported" in error.message.lower() or language in error.message.lower()
    
    def test_get_supported_languages(self):
        """Test that get_supported_languages returns the correct list."""
        generator = SampleCodeGenerator()
        supported = generator.get_supported_languages()
        
        # Verify it's a list
        assert isinstance(supported, list)
        
        # Verify expected languages are present
        assert 'java' in supported
        assert 'python' in supported
        assert 'nodejs' in supported
        
        # Verify it's a copy (modifying it shouldn't affect the generator)
        original_length = len(supported)
        supported.append('fake_language')
        new_supported = generator.get_supported_languages()
        assert len(new_supported) == original_length
    
    def test_java_code_syntax_validity(self):
        """
        Verify Java code contains valid syntax elements.
        Requirements: 3.1
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('java')
        
        # Check for basic Java syntax elements
        assert 'class' in result.code
        assert '{' in result.code and '}' in result.code
        assert '(' in result.code and ')' in result.code
        
        # Check for method declarations
        assert 'public' in result.code or 'private' in result.code
        
        # Check for proper imports (if any)
        if 'import' in result.code:
            assert 'import ' in result.code
    
    def test_python_code_syntax_validity(self):
        """
        Verify Python code contains valid syntax elements.
        Requirements: 3.2
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('python')
        
        # Check for basic Python syntax elements
        assert 'def ' in result.code or 'class ' in result.code
        assert ':' in result.code
        
        # Check for proper imports
        assert 'import ' in result.code or 'from ' in result.code
        
        # Verify indentation exists (Python requires it)
        lines = result.code.split('\n')
        indented_lines = [line for line in lines if line.startswith('    ') or line.startswith('\t')]
        assert len(indented_lines) > 0, "Python code should have indented lines"
    
    def test_nodejs_code_syntax_validity(self):
        """
        Verify Node.js code contains valid syntax elements.
        Requirements: 3.3
        """
        generator = SampleCodeGenerator()
        result = generator.generate_sample('nodejs')
        
        # Check for basic JavaScript/Node.js syntax elements
        assert 'function' in result.code or 'class' in result.code or '=>' in result.code
        assert '{' in result.code and '}' in result.code
        assert '(' in result.code and ')' in result.code
        
        # Check for variable declarations
        assert 'const' in result.code or 'let' in result.code or 'var' in result.code
        
        # Check for require or import
        assert 'require(' in result.code or 'import ' in result.code
    
    def test_custom_templates_directory(self, tmp_path):
        """Test that generator can use a custom templates directory."""
        # Create a custom template
        custom_template = tmp_path / "java_sample.txt"
        custom_template.write_text("// Custom Java template\nclass CustomTest {}")
        
        # Create generator with custom directory
        generator = SampleCodeGenerator(templates_dir=str(tmp_path))
        result = generator.generate_sample('java')
        
        # Verify custom template was used
        assert "Custom Java template" in result.code
        assert "CustomTest" in result.code
    
    def test_missing_template_error(self, tmp_path):
        """Test that missing template files raise appropriate errors."""
        # Create generator with empty directory
        generator = SampleCodeGenerator(templates_dir=str(tmp_path))
        
        # Attempt to generate code should fail
        with pytest.raises(TranslationError) as exc_info:
            generator.generate_sample('java')
        
        error = exc_info.value
        assert error.error_type == "file"
        assert "template" in error.message.lower() or "not found" in error.message.lower()
