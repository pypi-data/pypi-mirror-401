from .dashscope_tools import TOOLS as dashscope_tools
from .pwd import TOOLS as pwd_tools

TOOLS = [dashscope_tools, pwd_tools]
ALL_TOOLS = [func for tool in TOOLS for func in tool]
