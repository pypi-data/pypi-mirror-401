from pathlib import Path

async def pwd() -> str:
    """返回当前工作目录"""
    return str(Path.cwd())

TOOLS = [pwd]
