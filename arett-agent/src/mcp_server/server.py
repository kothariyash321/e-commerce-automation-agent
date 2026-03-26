import asyncio
import json

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from src.tools import execute_tool
from src.tools.registry import TOOL_REGISTRY

server = Server('arett-agent')


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=t['name'], description=t['description'], inputSchema=t['input_schema'])
        for t in TOOL_REGISTRY
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = execute_tool(name, arguments or {})
    return [types.TextContent(type='text', text=json.dumps(result, default=str))]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(
            read,
            write,
            InitializationOptions(server_name='arett-agent', server_version='1.0.0'),
        )


if __name__ == '__main__':
    asyncio.run(main())
