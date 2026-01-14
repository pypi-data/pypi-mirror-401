from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)

# Add an addition tool 
#注释、类型修饰符一定要写
#@mcp.tool()声明了这是一个工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
#@mcp.resource()注册可共享的资源 / 数据对象,如:配置存储、资源连接、数据共享 
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

def main() -> None:
    mcp.run(transport='stdio')
