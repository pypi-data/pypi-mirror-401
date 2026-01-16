"""
Sample Code Generator for Translation Power.

This module provides functionality to generate sample code in multiple programming
languages (Java, Python, Node.js) demonstrating how to integrate with the
Translation Power MCP server.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from .models import SampleCodeRequest, SampleCodeResult, TranslationError
except ImportError:
    from models import SampleCodeRequest, SampleCodeResult, TranslationError


class SampleCodeGenerator:
    """
    Generator for sample code in multiple programming languages.
    
    Supports Java, Python, and Node.js code generation with explanatory comments
    showing how to integrate with the Translation Power MCP server.
    """
    
    # Supported programming languages
    SUPPORTED_LANGUAGES = ['java', 'python', 'nodejs']
    
    # Language descriptions
    LANGUAGE_DESCRIPTIONS = {
        'java': 'Java sample code for Translation Power MCP server integration using HttpClient and JSON',
        'python': 'Python sample code for Translation Power MCP server integration using requests library',
        'nodejs': 'Node.js sample code for Translation Power MCP server integration using axios'
    }
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the sample code generator.
        
        Args:
            templates_dir: Optional path to templates directory. If not provided,
                          uses the default templates directory relative to this file.
        """
        if templates_dir is None:
            # Default to templates directory in the package
            current_dir = Path(__file__).parent.parent
            self.templates_dir = current_dir / 'templates'
        else:
            self.templates_dir = Path(templates_dir)
    
    def get_supported_languages(self) -> list[str]:
        """
        Get list of supported programming languages.
        
        Returns:
            List of supported language identifiers
        """
        return self.SUPPORTED_LANGUAGES.copy()
    
    def generate_sample(self, language: str, include_comments: bool = True) -> SampleCodeResult:
        """
        Generate sample code for the specified language.
        
        Args:
            language: Programming language identifier ('java', 'python', or 'nodejs')
            include_comments: Whether to include comments (currently always included in templates)
            
        Returns:
            SampleCodeResult containing the generated code, language, and description
            
        Raises:
            TranslationError: If the language is not supported or template cannot be loaded
        """
        # Normalize language name to lowercase
        language = language.lower()
        
        # Validate language is supported
        if language not in self.SUPPORTED_LANGUAGES:
            raise TranslationError(
                error_type="validation",
                message=f"Unsupported language: {language}. Supported languages are: {', '.join(self.SUPPORTED_LANGUAGES)}",
                details={"requested_language": language, "supported_languages": self.SUPPORTED_LANGUAGES}
            )
        
        # Load the template file
        template_file = self.templates_dir / f"{language}_sample.txt"
        
        try:
            code = self._load_template(template_file)
        except FileNotFoundError:
            raise TranslationError(
                error_type="file",
                message=f"Template file not found for language: {language}",
                details={"template_path": str(template_file)}
            )
        except Exception as e:
            raise TranslationError(
                error_type="file",
                message=f"Failed to load template for language: {language}",
                details={"error": str(e), "template_path": str(template_file)}
            )
        
        # Get description for the language
        description = self.LANGUAGE_DESCRIPTIONS.get(
            language,
            f"Sample code for {language}"
        )
        
        # Return the result
        return SampleCodeResult(
            code=code,
            language=language,
            description=description
        )
    
    def _load_template(self, template_path: Path) -> str:
        """
        Load template content from file.
        
        Args:
            template_path: Path to the template file
            
        Returns:
            Template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            IOError: If template file cannot be read
        """
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
