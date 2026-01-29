"""
LGEDV MCP Server - Modular Architecture
Main server file với cấu trúc module đã được tối ưu
"""
import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from pydantic import FileUrl
import os
import sys
import json
# Import modules từ package structure mới
from javis.modules.config import RESOURCE_FILES, CUSTOM_RULE_URL, setup_logging
from javis.handlers.tool_handlers import ToolHandler
from javis.handlers.prompt_handlers import PromptHandler
from javis.handlers.resource_handler import get_all_resources
from javis.modules.persistent_storage import PersistentTracker, reset_all_analysis



# Setup logging
logger = setup_logging()

@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)

def main(port: int, transport: str):
    """Main entry point for the MCP server"""
    try:
        
        logger.info("Server started and ready to receive requests")
        logger.info(f"Starting server with transport: {transport}, port: {port}")
        
        # Check environment variable for reset
        reset_cache = os.getenv('reset_cache', 'false').lower() == 'true'
        
        if reset_cache:
            logger.info("🗑️  Resetting all analysis cache...")
            reset_all_analysis()
            logger.info("✅ Analysis cache reset completed")

        # Initialize server and handlers
        app = Server("javis_agent_server")
        tool_handler = ToolHandler()
        prompt_handler = PromptHandler()
        
        logger.debug("App server object created")

        # Register tool handler
        @app.call_tool()
        async def fetch_tool(name: str, arguments: dict) -> list[
            types.TextContent | types.ImageContent | types.AudioContent | types.EmbeddedResource
        ]:
            """Route tool calls to appropriate handler"""
            return await tool_handler.handle_tool_call(name, arguments)

        # Register tool list handler
        @app.list_tools()
        async def list_tools() -> list[types.Tool]:
            """List all available tools"""
            logger.info("list_tools called")
            tools = [                
                types.Tool(
                    name="fetch_custom_rule",
                    description="Fetches the Custom rule markdown from remote server.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to fetch Custom rule (optional, default is preset)",
                            }
                        },
                    },
                ),
                types.Tool(
                    name="get_src_context",
                    description="Get the content of all files in the current given directory as a single response for context.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dir": {
                                "type": "string",
                                "description": "Directory to search for code files.",
                            }
                        },
                        "required": []
                    },                    
                ),                
                types.Tool(
                    name="analyze_requirement",
                    description="analyze requirement from .md files in specified directory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dir": {
                                "type": "string",
                                "description": "path to directory containing .md files",
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_interface",
                    description="Quét tất cả thư mục interface, trích xuất API từ .h, .hpp, .cpp",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dir": {
                                "type": "string",
                                "description": "Thư mục chứa các file interface để quét API",
                            }
                        },
                        "required": []
                    }
                ),
                # RAG Tools
                types.Tool(
                    name="rag_index_codebase",
                    description="Index codebase for RAG. Creates vector embeddings. Supports 2 backends (FAISS/LEANN) and 2 modes (retrieval_only/full_rag).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dir": {
                                "type": "string",
                                "description": "Directory to index (optional, defaults to src_dir)",
                            },
                            "index_name": {
                                "type": "string",
                                "description": "Name for the index (optional, defaults to 'default')",
                            },
                            "backend": {
                                "type": "string",
                                "description": "Vector store backend: 'faiss' (traditional) or 'leann' (97% less storage, default from RAG_BACKEND env)",
                                "enum": ["faiss", "leann"]
                            },
                            "mode": {
                                "type": "string",
                                "description": "RAG mode: 'retrieval_only' (Copilot generates, default) or 'full_rag' (OpenAI generates)",
                                "enum": ["retrieval_only", "full_rag"]
                            }
                        },
                        "required": []
                    }
                ),
                types.Tool(
                    name="rag_query_code",
                    description="Search codebase and return relevant code context. Copilot Chat will analyze the context and generate answer.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Question about the codebase",
                            },
                            "index_name": {
                                "type": "string",
                                "description": "Index to query (optional, defaults to 'default')",
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of code snippets to retrieve (optional, defaults to 30)",
                            },
                            "backend": {
                                "type": "string",
                                "description": "Vector store backend to use: 'faiss' or 'leann' (optional, auto-detect from index)",
                                "enum": ["faiss", "leann"]
                            }
                        },
                        "required": ["question"]
                    }
                ),
                types.Tool(
                    name="rag_list_indexes",
                    description="List all available RAG indexes",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                
            ]
            
            return tools

        # Register prompt list handler
        @app.list_prompts()
        async def list_prompts() -> list[types.Prompt]:
            """List all available prompts"""
            logger.info("list_prompts called")
            prompts = [
                
                types.Prompt(
                    name="get_code_context",
                    description="Load content for all source files in the current directory."
                ),
                types.Prompt(
                    name="check_single_requirement",
                    description="Verify whether current code implements a single user-provided requirement.",
                    arguments=[
                        types.PromptArgument(
                            name="requirement_text",
                            description="Free-form requirement to verify (e.g., 'The system shall encrypt data at rest.')",
                            required=True,
                        ),
                    ],
                ),
                types.Prompt(
                        name="check_design",                        
                        description="System design verification",
                        arguments=[
                            types.PromptArgument(
                                name="feature",
                                description="Feature name to focus analysis on (e.g., 'callback waiting')",
                                required=False,
                            ),
                        ],
                ),
            ]
                
            return prompts
        
        # Register prompt handler
        @app.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> types.GetPromptResult:
            """Route prompt calls to appropriate handler"""
            return await prompt_handler.handle_prompt(name, arguments)

        # Register resource list handler
        @app.list_resources()
        async def list_resources() -> list[types.Resource]:
            """List all available resources"""
            logger.info("list_resources called")
            return get_all_resources()

        logger.info("All handlers registered. Entering main event loop...")
        
        # Start server based on transport type
        if transport == "sse":
            _run_sse_server(app, port)
        else:
            _run_stdio_server(app)
            
        logger.info("Server stopped")
        return 0
        
    except Exception as e:
        logger.exception(f"Fatal error in main: {e}")
        print(f"Fatal error in main: {e}", file=sys.stderr)
        raise

def _run_sse_server(app: Server, port: int):
    """Run SSE server (if needed)"""
    try:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        
        sse = SseServerTransport("/messages/")
        
        async def handle_sse(request):
            logger.info("Handling SSE connection")
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await app.run(streams[0], streams[1], app.create_initialization_options())
            return Response()
            
        # Note: Full SSE implementation would need Starlette app setup
        logger.warning("SSE transport not fully implemented in this refactored version")
        
    except ImportError as e:
        logger.error(f"SSE dependencies not available: {e}")
        raise

def _run_stdio_server(app: Server):
    """Run stdio server"""
    async def arun():
        logger.info("Running stdio server")
        try:
            import mcp.server.stdio
            async with mcp.server.stdio.stdio_server() as streams:
                await app.run(streams[0], streams[1], app.create_initialization_options())
            logger.info("stdio server run completed")
        except Exception as e:
            logger.exception(f"Exception in stdio server: {e}")
    
    anyio.run(arun)

if __name__ == "__main__":
    main()
