from mcp.server.fastmcp import FastMCP
from .tools import ALL_TOOLS

mcp = FastMCP("Demo")

# 自动注册所有工具
for func in ALL_TOOLS:
    mcp.add_tool(func)

def main():
    print("MCP 服务器已启动")
    mcp.run("stdio")

if __name__ == "__main__":
    main()
