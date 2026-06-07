from mcp.server.fastmcp import FastMCP
from tools.rag_tool import rag_search

mcp = FastMCP("AI MCP Server")


@mcp.tool()
def search_docs(query: str):
    return rag_search(query)


@mcp.tool()
def add(a: int, b: int):
    return a + b


if __name__ == "__main__":
    mcp.run()
