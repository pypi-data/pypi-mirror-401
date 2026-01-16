"""
MCP Server implementation for Translation Power.

This module implements the Model Context Protocol (MCP) server that exposes
translation and sample code generation tools to Kiro clients.

Requirements: 4.4, 6.3, 6.4
"""

import logging
import sys
from typing import Dict, Callable, Any, Optional
from datetime import datetime

try:
    from .models import ServerConfig, TranslationError
    from .config import ConfigLoader
    from .bedrock_client import BedrockClient
    from .translation_engine import TranslationEngine
    from .input_handler import InputHandler
    from .sample_code_gen import SampleCodeGenerator
except ImportError:
    from models import ServerConfig, TranslationError
    from config import ConfigLoader
    from bedrock_client import BedrockClient
    from translation_engine import TranslationEngine
    from input_handler import InputHandler
    from sample_code_gen import SampleCodeGenerator


# Type alias for tool handlers
ToolHandler = Callable[[Dict[str, Any]], Dict[str, Any]]


class MCPServerError(Exception):
    """Base exception for MCP server errors."""
    pass


class MCPServer:
    """
    MCP Server for Translation Power.
    
    Manages tool registration, request handling, and server lifecycle.
    Validates dependencies at startup and provides MCP-compliant responses.
    """
    
    def __init__(self, config: ServerConfig):
        """
        Initialize the MCP server with configuration.
        
        Args:
            config: ServerConfig instance with server settings
        """
        self.config = config
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.logger = self._setup_logging()
        self.is_running = False
        
        # Initialize components (will be set up in start())
        self.bedrock_client: Optional[BedrockClient] = None
        self.translation_engine: Optional[TranslationEngine] = None
        self.input_handler: Optional[InputHandler] = None
        self.sample_code_generator: Optional[SampleCodeGenerator] = None
    
    def _setup_logging(self) -> logging.Logger:
        """
        Set up logging for the MCP server.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger('translation_power.mcp_server')
        logger.setLevel(getattr(logging, self.config.log_level.upper(), logging.INFO))
        
        # Create console handler if not already configured
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(getattr(logging, self.config.log_level.upper(), logging.INFO))
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def register_tool(
        self,
        name: str,
        handler: ToolHandler,
        schema: Dict[str, Any]
    ) -> None:
        """
        Register a tool with its handler and input schema.
        
        Args:
            name: Tool name (e.g., 'translate', 'get_sample_code')
            handler: Function that handles tool invocations
            schema: JSON schema describing tool parameters
        
        Raises:
            MCPServerError: If tool name is already registered
        """
        if name in self.tools:
            raise MCPServerError(f"Tool '{name}' is already registered")
        
        self.tools[name] = {
            'handler': handler,
            'schema': schema
        }
        
        self.logger.info(f"Registered tool: {name}")
    
    def start(self) -> None:
        """
        Start the MCP server.
        
        Validates dependencies, initializes components, and registers tools.
        
        Raises:
            MCPServerError: If dependencies are missing or initialization fails
        """
        self.logger.info("Starting Translation Power MCP Server...")
        
        try:
            # Validate dependencies
            self._validate_dependencies()
            
            # Initialize components
            self._initialize_components()
            
            # Register tools
            self._register_tools()
            
            self.is_running = True
            self.logger.info(
                f"MCP Server started successfully on {self.config.host}:{self.config.port}"
            )
            self.logger.info(f"Registered tools: {', '.join(self.tools.keys())}")
        
        except Exception as e:
            self.logger.error(f"Failed to start MCP server: {str(e)}")
            raise MCPServerError(f"Server startup failed: {str(e)}") from e
    
    def stop(self) -> None:
        """
        Gracefully stop the MCP server.
        
        Cleans up resources and shuts down components.
        """
        self.logger.info("Stopping Translation Power MCP Server...")
        
        try:
            # Clean up components
            self.bedrock_client = None
            self.translation_engine = None
            self.input_handler = None
            self.sample_code_generator = None
            
            # Clear registered tools
            self.tools.clear()
            
            self.is_running = False
            self.logger.info("MCP Server stopped successfully")
        
        except Exception as e:
            self.logger.error(f"Error during server shutdown: {str(e)}")
            raise MCPServerError(f"Server shutdown failed: {str(e)}") from e
    
    def _validate_dependencies(self) -> None:
        """
        Validate that all required dependencies are available.
        
        Checks for:
        - AWS credentials (via environment or config)
        - Required Python packages
        - Template files for sample code generation
        
        Raises:
            MCPServerError: If required dependencies are missing
        """
        self.logger.info("Validating dependencies...")
        
        # Check for boto3 (AWS SDK)
        try:
            import boto3
        except ImportError:
            raise MCPServerError(
                "Missing required dependency: boto3. "
                "Install with: pip install boto3"
            )
        
        # Check for AWS credentials
        try:
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if credentials is None:
                self.logger.warning(
                    "AWS credentials not found. Translation functionality may not work. "
                    "Configure credentials using AWS CLI or environment variables."
                )
        except Exception as e:
            self.logger.warning(f"Could not validate AWS credentials: {str(e)}")
        
        # Check for template files
        from pathlib import Path
        templates_dir = Path(__file__).parent.parent / 'templates'
        
        required_templates = ['java_sample.txt', 'python_sample.txt', 'nodejs_sample.txt']
        missing_templates = []
        
        for template in required_templates:
            template_path = templates_dir / template
            if not template_path.exists():
                missing_templates.append(template)
        
        if missing_templates:
            self.logger.warning(
                f"Missing template files: {', '.join(missing_templates)}. "
                "Sample code generation may not work for some languages."
            )
        
        self.logger.info("Dependency validation complete")
    
    def _initialize_components(self) -> None:
        """
        Initialize server components.
        
        Creates instances of:
        - BedrockClient
        - TranslationEngine
        - InputHandler
        - SampleCodeGenerator
        
        Raises:
            MCPServerError: If component initialization fails
        """
        self.logger.info("Initializing components...")
        
        try:
            # Load translation config
            try:
                from .config import ConfigLoader
            except ImportError:
                from config import ConfigLoader
                
            config_loader = ConfigLoader()
            translation_config = config_loader.load_translation_config()
            
            # Initialize Bedrock client
            self.bedrock_client = BedrockClient(
                region=self.config.aws_region
            )
            self.logger.info(f"Initialized Bedrock client for region: {self.config.aws_region}")
            
            # Initialize translation engine
            self.translation_engine = TranslationEngine(
                bedrock_client=self.bedrock_client,
                config=translation_config
            )
            self.logger.info("Initialized translation engine")
            
            # Initialize input handler
            self.input_handler = InputHandler(
                max_input_length=translation_config.max_input_length
            )
            self.logger.info("Initialized input handler")
            
            # Initialize sample code generator
            self.sample_code_generator = SampleCodeGenerator()
            self.logger.info("Initialized sample code generator")
            
            self.logger.info("All components initialized successfully")
        
        except Exception as e:
            raise MCPServerError(f"Component initialization failed: {str(e)}") from e
    
    def _register_tools(self) -> None:
        """
        Register all available tools with the server.
        
        Registers:
        - translate: Text translation tool
        - get_sample_code: Sample code generation tool
        """
        # Register translate tool
        translate_schema = {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Text to translate or file path"
                },
                "is_file": {
                    "type": "boolean",
                    "description": "Whether input is a file path",
                    "default": False
                },
                "source_lang": {
                    "type": "string",
                    "description": "Source language code (e.g., 'en', 'es', 'fr'). Use 'auto' for auto-detection.",
                    "default": "auto"
                },
                "target_lang": {
                    "type": "string",
                    "description": "Target language code (e.g., 'en', 'es', 'fr')",
                    "default": "en"
                },
                "stream": {
                    "type": "boolean",
                    "description": "Whether to stream the response",
                    "default": False
                }
            },
            "required": ["input", "target_lang"]
        }
        
        self.register_tool(
            name="translate",
            handler=lambda params: handle_translate(params, self),
            schema=translate_schema
        )
        
        # Register get_sample_code tool
        sample_code_schema = {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "description": "Programming language for sample code",
                    "enum": ["java", "python", "nodejs"]
                },
                "include_comments": {
                    "type": "boolean",
                    "description": "Whether to include explanatory comments",
                    "default": True
                }
            },
            "required": ["language"]
        }
        
        self.register_tool(
            name="get_sample_code",
            handler=lambda params: handle_get_sample_code(params, self),
            schema=sample_code_schema
        )
    
    def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a registered tool with parameters.
        
        Args:
            tool_name: Name of the tool to invoke
            parameters: Tool parameters
        
        Returns:
            MCP-compliant response dictionary
        
        Raises:
            MCPServerError: If tool is not found or invocation fails
        """
        if not self.is_running:
            return self._format_error_response(
                "protocol",
                "Server is not running"
            )
        
        if tool_name not in self.tools:
            return self._format_error_response(
                "protocol",
                f"Unknown tool: {tool_name}. Available tools: {', '.join(self.tools.keys())}"
            )
        
        tool = self.tools[tool_name]
        handler = tool['handler']
        
        try:
            # Invoke the tool handler
            result = handler(parameters)
            return result
        
        except Exception as e:
            self.logger.error(f"Tool invocation failed for '{tool_name}': {str(e)}")
            return self._format_error_response(
                "execution",
                f"Tool execution failed: {str(e)}"
            )
    
    def _format_error_response(
        self,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Format an error response in MCP-compliant format.
        
        Args:
            error_type: Type of error
            message: Error message
            details: Optional additional details
        
        Returns:
            MCP-compliant error response
        """
        return {
            "error": {
                "code": error_type,
                "message": message,
                "data": {
                    "error_type": error_type,
                    "details": details or {},
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        }


# Tool handler functions
def handle_translate(params: Dict[str, Any], server: MCPServer) -> Dict[str, Any]:
    """
    Handle translation requests.
    
    Processes translation requests by:
    1. Validating input parameters
    2. Processing input (plain text or file)
    3. Invoking translation engine
    4. Formatting response in MCP-compliant format
    
    Args:
        params: Dictionary containing:
            - input (str, required): Text to translate or file path
            - is_file (bool, optional): Whether input is a file path (default: False)
            - source_lang (str, optional): Source language code (default: 'auto')
            - target_lang (str, required): Target language code
            - stream (bool, optional): Whether to stream response (default: False)
        server: MCPServer instance
    
    Returns:
        MCP-compliant response dictionary with translation result or error
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 5.1, 5.3, 6.1, 6.2
    """
    try:
        # Validate required parameters
        if 'input' not in params:
            server.logger.error("Missing required parameter: input")
            return server._format_error_response(
                "validation",
                "Missing required parameter: 'input'",
                {"missing_parameter": "input"}
            )
        
        if 'target_lang' not in params:
            server.logger.error("Missing required parameter: target_lang")
            return server._format_error_response(
                "validation",
                "Missing required parameter: 'target_lang'",
                {"missing_parameter": "target_lang"}
            )
        
        # Extract parameters
        input_data = params['input']
        is_file = params.get('is_file', False)
        source_lang = params.get('source_lang', 'auto')
        target_lang = params['target_lang']
        stream = params.get('stream', False)
        
        # Validate parameter types
        if not isinstance(input_data, str):
            server.logger.error(f"Invalid type for 'input': expected str, got {type(input_data).__name__}")
            return server._format_error_response(
                "validation",
                f"Invalid type for 'input': expected string, got {type(input_data).__name__}",
                {"parameter": "input", "expected_type": "string", "actual_type": type(input_data).__name__}
            )
        
        if not isinstance(is_file, bool):
            server.logger.error(f"Invalid type for 'is_file': expected bool, got {type(is_file).__name__}")
            return server._format_error_response(
                "validation",
                f"Invalid type for 'is_file': expected boolean, got {type(is_file).__name__}",
                {"parameter": "is_file", "expected_type": "boolean", "actual_type": type(is_file).__name__}
            )
        
        if not isinstance(target_lang, str):
            server.logger.error(f"Invalid type for 'target_lang': expected str, got {type(target_lang).__name__}")
            return server._format_error_response(
                "validation",
                f"Invalid type for 'target_lang': expected string, got {type(target_lang).__name__}",
                {"parameter": "target_lang", "expected_type": "string", "actual_type": type(target_lang).__name__}
            )
        
        # Log the translation request
        server.logger.info(
            f"Translation request: is_file={is_file}, source={source_lang}, "
            f"target={target_lang}, stream={stream}"
        )
        
        # Process input (read file or use plain text)
        try:
            text_content = server.input_handler.process_input(input_data, is_file=is_file)
            server.logger.debug(f"Processed input: {len(text_content)} characters")
        except FileNotFoundError as e:
            server.logger.error(f"File not found: {str(e)}")
            return server._format_error_response(
                "file",
                f"File not found: {str(e)}",
                {"file_path": input_data}
            )
        except PermissionError as e:
            server.logger.error(f"Permission denied: {str(e)}")
            return server._format_error_response(
                "file",
                f"Permission denied reading file: {str(e)}",
                {"file_path": input_data}
            )
        except ValueError as e:
            server.logger.error(f"Invalid input: {str(e)}")
            return server._format_error_response(
                "validation",
                str(e),
                {"input_validation_error": str(e)}
            )
        except UnicodeDecodeError as e:
            server.logger.error(f"Encoding error: {str(e)}")
            return server._format_error_response(
                "file",
                f"Unable to decode file: {str(e)}",
                {"file_path": input_data, "encoding_error": str(e)}
            )
        except Exception as e:
            server.logger.error(f"Input processing error: {str(e)}")
            return server._format_error_response(
                "file",
                f"Error processing input: {str(e)}",
                {"error": str(e)}
            )
        
        # Perform translation
        try:
            result = server.translation_engine.translate(
                text=text_content,
                source_lang=source_lang,
                target_lang=target_lang,
                stream=stream
            )
            
            # Handle streaming vs synchronous response
            if stream:
                # For streaming, we need to handle the iterator
                # In a real MCP implementation, this would stream chunks
                # For now, we'll collect all chunks and return them
                chunks = []
                for chunk in result:
                    if chunk.chunk:
                        chunks.append(chunk.chunk)
                    if chunk.is_complete:
                        break
                
                translated_text = ''.join(chunks)
                
                server.logger.info(f"Streaming translation completed: {len(translated_text)} characters")
                
                return {
                    "translated_text": translated_text,
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "model_used": server.config.model_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "streamed": True
                }
            else:
                # Synchronous response
                server.logger.info(
                    f"Translation completed: {len(result.translated_text)} characters"
                )
                
                return {
                    "translated_text": result.translated_text,
                    "source_language": result.source_language,
                    "target_language": result.target_language,
                    "model_used": result.model_used,
                    "timestamp": result.timestamp
                }
        
        except TranslationError as e:
            server.logger.error(f"Translation error: {str(e)}")
            return server._format_error_response(
                e.error_type,
                str(e),
                e.details
            )
        except Exception as e:
            server.logger.error(f"Translation failed: {str(e)}")
            return server._format_error_response(
                "aws",
                f"Translation failed: {str(e)}",
                {"error": str(e)}
            )
    
    except Exception as e:
        # Catch-all for unexpected errors
        server.logger.error(f"Unexpected error in translate handler: {str(e)}")
        return server._format_error_response(
            "execution",
            f"Unexpected error: {str(e)}",
            {"error": str(e)}
        )


def handle_get_sample_code(params: Dict[str, Any], server: MCPServer) -> Dict[str, Any]:
    """
    Handle sample code generation requests.
    
    Processes sample code requests by:
    1. Validating input parameters
    2. Invoking sample code generator
    3. Formatting response in MCP-compliant format
    
    Args:
        params: Dictionary containing:
            - language (str, required): Programming language ('java', 'python', 'nodejs')
            - include_comments (bool, optional): Whether to include comments (default: True)
        server: MCPServer instance
    
    Returns:
        MCP-compliant response dictionary with sample code or error
    
    Requirements: 3.1, 3.2, 3.3, 5.2, 5.3
    """
    try:
        # Validate required parameters
        if 'language' not in params:
            server.logger.error("Missing required parameter: language")
            return server._format_error_response(
                "validation",
                "Missing required parameter: 'language'",
                {"missing_parameter": "language"}
            )
        
        # Extract parameters
        language = params['language']
        include_comments = params.get('include_comments', True)
        
        # Validate parameter types
        if not isinstance(language, str):
            server.logger.error(f"Invalid type for 'language': expected str, got {type(language).__name__}")
            return server._format_error_response(
                "validation",
                f"Invalid type for 'language': expected string, got {type(language).__name__}",
                {"parameter": "language", "expected_type": "string", "actual_type": type(language).__name__}
            )
        
        if not isinstance(include_comments, bool):
            server.logger.error(f"Invalid type for 'include_comments': expected bool, got {type(include_comments).__name__}")
            return server._format_error_response(
                "validation",
                f"Invalid type for 'include_comments': expected boolean, got {type(include_comments).__name__}",
                {"parameter": "include_comments", "expected_type": "boolean", "actual_type": type(include_comments).__name__}
            )
        
        # Log the request
        server.logger.info(f"Sample code request: language={language}, include_comments={include_comments}")
        
        # Generate sample code
        try:
            result = server.sample_code_generator.generate_sample(
                language=language,
                include_comments=include_comments
            )
            
            server.logger.info(f"Sample code generated for {language}: {len(result.code)} characters")
            
            return {
                "code": result.code,
                "language": result.language,
                "description": result.description
            }
        
        except TranslationError as e:
            server.logger.error(f"Sample code generation error: {str(e)}")
            return server._format_error_response(
                e.error_type,
                str(e),
                e.details
            )
        except Exception as e:
            server.logger.error(f"Sample code generation failed: {str(e)}")
            return server._format_error_response(
                "execution",
                f"Sample code generation failed: {str(e)}",
                {"error": str(e)}
            )
    
    except Exception as e:
        # Catch-all for unexpected errors
        server.logger.error(f"Unexpected error in get_sample_code handler: {str(e)}")
        return server._format_error_response(
            "execution",
            f"Unexpected error: {str(e)}",
            {"error": str(e)}
        )



# MCP Server Entry Point
async def main():
    """Main entry point for the MCP server."""
    import asyncio
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    
    # Load configuration
    config_loader = ConfigLoader()
    server_config = config_loader.load_server_config()
    
    # Create MCP server instance
    mcp_server = Server("translation-power")
    
    # Create our custom server
    translation_server = MCPServer(server_config)
    
    # Register tools with MCP
    from mcp.types import Tool
    
    @mcp_server.list_tools()
    async def list_tools():
        """List available tools."""
        return [
            Tool(
                name="translate",
                description="Translate text from one language to another using AWS Bedrock Nova Pro",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "Text to translate or file path"
                        },
                        "target_lang": {
                            "type": "string",
                            "description": "Target language code (e.g., 'es', 'fr', 'de')"
                        },
                        "source_lang": {
                            "type": "string",
                            "description": "Source language code or 'auto' for auto-detection",
                            "default": "auto"
                        },
                        "is_file": {
                            "type": "boolean",
                            "description": "Whether input is a file path",
                            "default": False
                        },
                        "stream": {
                            "type": "boolean",
                            "description": "Whether to stream the response",
                            "default": False
                        }
                    },
                    "required": ["input", "target_lang"]
                }
            ),
            Tool(
                name="get_sample_code",
                description="Generate sample code for integrating with the Translation Power",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "Programming language",
                            "enum": ["java", "python", "nodejs"]
                        },
                        "include_comments": {
                            "type": "boolean",
                            "description": "Include explanatory comments",
                            "default": True
                        }
                    },
                    "required": ["language"]
                }
            )
        ]
    
    @mcp_server.call_tool()
    async def call_tool(name: str, arguments: dict):
        """Handle tool calls."""
        # Start the translation server if not already running
        if not translation_server.is_running:
            translation_server.start()
        
        # Invoke the tool
        result = translation_server.invoke_tool(name, arguments)
        
        # Check if there's an error
        if "error" in result:
            error = result["error"]
            raise Exception(f"{error.get('code', 'error')}: {error.get('message', 'Unknown error')}")
        
        # Return successful result
        return [{"type": "text", "text": str(result)}]
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


def run():
    """Entry point for the installed script."""
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    run()
