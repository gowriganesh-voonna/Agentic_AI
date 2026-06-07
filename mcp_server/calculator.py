import httpx

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Calculator")


@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
    
