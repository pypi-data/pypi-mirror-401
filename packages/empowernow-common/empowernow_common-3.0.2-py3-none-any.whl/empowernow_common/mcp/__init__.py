"""MCP Tool ID and Server Registry Module.

This module provides tool ID parsing and server registry functionality
for the Model Context Protocol (MCP) integration.

Features:
    - Tool ID parsing per Neo4j schema v2.3
    - Server configuration and registry
    - Loopback server detection for routing

Tool ID Format:
    tool:{mcp_server_id}:{tool_key}

    Examples:
        tool:jira:create-issue
        tool:mcp-server:travel:flight-search
        tool:crud-service-loopback:entra.users.create

Usage:
    from empowernow_common.mcp import (
        ToolId,
        parse_tool_id,
        is_loopback_server,
    )

    # Parse a tool ID
    tool = parse_tool_id("tool:jira:create-issue")
    if tool:
        print(f"Server: {tool.server_id}")
        print(f"Tool: {tool.tool_key}")

    # Check if loopback
    if is_loopback_server(tool.server_id):
        # Route internally
        pass

Security Note:
    is_loopback_server() is a ROUTING HINT only.
    It does NOT authenticate or authorize requests.
    All loopback calls must be cryptographically signed.
"""

from .tool_id import (
    ToolId,
    parse_tool_id,
    is_valid_tool_id,
    create_tool_id,
    clear_tool_id_cache,
    TOOL_ID_PATTERN,
    SERVER_ID_PATTERN,
    TOOL_KEY_PATTERN,
)

from .servers import (
    # Constants
    DEFAULT_LOOPBACK_SERVERS,
    # Classes
    ServerConfig,
    ServerRegistry,
    # Functions
    is_loopback_server,
    register_server,
    get_server,
    list_loopback_servers,
    reset_registry,
)


__all__ = [
    # Tool ID
    "ToolId",
    "parse_tool_id",
    "is_valid_tool_id",
    "create_tool_id",
    "clear_tool_id_cache",
    "TOOL_ID_PATTERN",
    "SERVER_ID_PATTERN",
    "TOOL_KEY_PATTERN",
    # Server Registry
    "DEFAULT_LOOPBACK_SERVERS",
    "ServerConfig",
    "ServerRegistry",
    "is_loopback_server",
    "register_server",
    "get_server",
    "list_loopback_servers",
    "reset_registry",
]
