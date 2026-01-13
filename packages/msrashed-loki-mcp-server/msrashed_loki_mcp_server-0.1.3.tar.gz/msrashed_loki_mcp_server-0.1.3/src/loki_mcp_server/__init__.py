"""
Loki MCP Server.

A read-only MCP server for Grafana Loki log aggregation platform.
All operations are safe and cannot modify Loki configuration.
"""

from loki_mcp_server.cli import cli, main
from loki_mcp_server.server import create_server

__version__ = "0.1.0"
__all__ = ["create_server", "main", "cli"]
