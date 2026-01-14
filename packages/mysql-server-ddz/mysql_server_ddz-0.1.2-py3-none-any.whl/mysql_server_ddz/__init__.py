
from mcp.server.fastmcp import FastMCP


mcp=FastMCP("ddzDemo")

@mcp.tool()
def add(a:int,b:int)->int:
    """
    Add tow numbers
    """
    return a+b

def main() -> None:
    mcp.run(transport="stdio")
