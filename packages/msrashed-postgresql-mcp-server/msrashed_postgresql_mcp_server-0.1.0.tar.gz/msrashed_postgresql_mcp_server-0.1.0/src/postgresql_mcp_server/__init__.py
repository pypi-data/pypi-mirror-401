"""
PostgreSQL MCP Server.

A read-only MCP server for PostgreSQL database platform.
All operations are safe and cannot modify database data.
"""

from postgresql_mcp_server.cli import cli, main
from postgresql_mcp_server.server import create_server

__version__ = "0.1.0"
__all__ = ["create_server", "main", "cli"]
