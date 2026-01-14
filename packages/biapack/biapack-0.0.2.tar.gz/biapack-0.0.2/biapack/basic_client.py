from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

class BasicClient:

    def __init__(self, url: str = "http://0.0.0.0:8000/mcp"):
        sufix = "/mcp"
        self.url = url if url.endswith(sufix) else f"{url}{sufix}"

    async def list_tools(self) -> dict:
        """Lista as ferramentas disponíveis no MCP"""
        async with streamablehttp_client(self.url, timeout=120, terminate_on_close=False) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tool_result = await session.list_tools()
        return tool_result
    
    async def call_tool(self, tool_name: str, params: dict = None, headers: dict = None) -> dict:
        """Executa a ferramenta disponível no MCP"""
        async with streamablehttp_client(self.url, headers, timeout=120, terminate_on_close=False) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, params)
        return result
    