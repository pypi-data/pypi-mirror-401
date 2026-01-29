#!/usr/bin/env python3
"""
MCP Server Entry Point for Manim MCP
Provides stdio transport for MCP protocol
"""

import asyncio
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any
import subprocess
import os

app = Server("manim-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="list_files",
            description="List files and directories in the container filesystem",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to list",
                        "default": "/manim"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to list files recursively",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path where the file should be written"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["filepath", "content"]
            }
        ),
        Tool(
            name="run_manim",
            description="Run Manim to generate an animation",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the Python file with Manim scenes"
                    },
                    "scene_name": {
                        "type": "string",
                        "description": "Name of the scene class to render"
                    },
                    "quality": {
                        "type": "string",
                        "description": "Quality setting (low_quality, medium_quality, high_quality, production_quality)",
                        "default": "medium_quality"
                    }
                },
                "required": ["filepath", "scene_name"]
            }
        ),
        Tool(
            name="download_file",
            description="Get information about a file for download",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file"
                    }
                },
                "required": ["filepath"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if name == "list_files":
        directory = arguments.get("directory", "/manim")
        recursive = arguments.get("recursive", False)
        try:
            if recursive:
                cmd = ["find", directory, "-type", "f", "-o", "-type", "d"]
            else:
                cmd = ["ls", "-la", directory]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "write_file":
        filepath = arguments["filepath"]
        content = arguments["content"]
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            return [TextContent(type="text", text=f"File written successfully: {filepath}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "run_manim":
        filepath = arguments["filepath"]
        scene_name = arguments["scene_name"]
        quality = arguments.get("quality", "medium_quality")
        try:
            quality_map = {
                "low_quality": "-ql",
                "medium_quality": "-qm",
                "high_quality": "-qh",
                "production_quality": "-qk"
            }
            quality_flag = quality_map.get(quality, "-qm")
            cmd = ["python3", "-m", "manim", quality_flag, filepath, scene_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return [TextContent(type="text", text=f"Animation rendered successfully:\n{result.stdout}")]
            else:
                return [TextContent(type="text", text=f"Error rendering animation:\n{result.stderr}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "download_file":
        filepath = arguments["filepath"]
        try:
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                return [TextContent(type="text", text=f"File found: {filepath}\nSize: {size} bytes")]
            else:
                return [TextContent(type="text", text=f"File not found: {filepath}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def _main_async():
    """Async main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

def main():
    """Synchronous entry point for console scripts"""
    asyncio.run(_main_async())

if __name__ == "__main__":
    main()