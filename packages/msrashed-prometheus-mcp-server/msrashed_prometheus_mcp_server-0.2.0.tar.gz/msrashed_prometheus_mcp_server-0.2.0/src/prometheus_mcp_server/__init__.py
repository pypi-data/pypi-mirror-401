"""
Prometheus MCP Server.

A read-only MCP server for Prometheus monitoring platform.
All operations are safe and cannot modify Prometheus configuration.
"""

from prometheus_mcp_server.cli import cli, main
from prometheus_mcp_server.server import create_server

__version__ = "0.1.0"
__all__ = ["create_server", "main", "cli"]
