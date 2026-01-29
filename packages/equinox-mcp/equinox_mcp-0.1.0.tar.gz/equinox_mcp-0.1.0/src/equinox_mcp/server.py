"""MCP Server for Equinox documentation."""

import asyncio
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    GetPromptResult,
    PromptMessage,
    PromptArgument,
)

from equinox_mcp.docs_source import DocsSource
from equinox_mcp.tools.list_sections import list_sections
from equinox_mcp.tools.get_documentation import get_documentation
from equinox_mcp.tools.equinox_checker import equinox_checker
from equinox_mcp.prompts.equinox_task import EQUINOX_TASK_PROMPT

logger = logging.getLogger(__name__)

# Initialize server
server = Server("equinox-mcp")

# Initialize docs source (handles local/GitHub resolution)
docs_source = DocsSource()


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list-sections",
            description=(
                "List all available Equinox documentation sections. "
                "Returns section titles, paths, and use cases to help identify relevant docs."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get-documentation",
            description=(
                "Retrieve full documentation for requested sections. "
                "Accepts section name(s) or path(s) like 'attention', 'api/nn/attention', or ['module', 'pattern']."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                        ],
                        "description": "Section name(s) or path(s) to retrieve",
                    }
                },
                "required": ["section"],
            },
        ),
        Tool(
            name="equinox-checker",
            description=(
                "Analyze Equinox module code and suggest fixes. "
                "Checks PyTree compliance, __init__ signature, __call__ signature, and common mistakes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Equinox module code to check",
                    }
                },
                "required": ["code"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "list-sections":
            result = await list_sections(docs_source)
        elif name == "get-documentation":
            section = arguments.get("section", "")
            result = await get_documentation(docs_source, section)
        elif name == "equinox-checker":
            code = arguments.get("code", "")
            result = await equinox_checker(code)
        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=f"Error: {e}")]


@server.list_prompts()
async def handle_list_prompts():
    """List available prompts."""
    return [
        {
            "name": "equinox-task",
            "description": "Guide for working with Equinox - patterns, tools, and best practices",
            "arguments": [],
        }
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
    """Get prompt content."""
    if name == "equinox-task":
        return GetPromptResult(
            description="Equinox development guide",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=EQUINOX_TASK_PROMPT),
                )
            ],
        )
    raise ValueError(f"Unknown prompt: {name}")


def main():
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Equinox MCP server...")
    logger.info(f"Docs source: {docs_source.source_type}")

    asyncio.run(run_server())


async def run_server():
    """Run the stdio server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    main()
