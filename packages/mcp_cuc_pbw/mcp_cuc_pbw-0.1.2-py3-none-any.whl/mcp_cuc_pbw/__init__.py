"""
MCP (Model Context Protocol) Server Implementation

This package provides a simple MCP Server implementation with a tool to get the current time.
"""

from .mcp_server import (
    MCPRequestHandler,
    run_server,
    main
)

__version__ = "0.1.2"
__all__ = [
    "MCPRequestHandler",
    "run_server",
    "main"
]
