"""包级别导出。

- `app`：FastMCP 应用实例
- `main`：启动 MCP Server 的入口函数

这样配置之后，可以在 pyproject.toml 中通过：

[project.scripts]
mysql_mcp_server = "mysql_mcp_server:main"

让 `uvx mysql_mcp_server` 或 `python -m mysql_mcp_server.server` 作为统一入口。
"""

from .server import app, main

__all__ = ["app", "main"]
