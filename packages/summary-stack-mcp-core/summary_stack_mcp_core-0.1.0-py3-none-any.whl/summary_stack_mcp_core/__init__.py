"""Summary Stack MCP Core - shared search and discovery tools.

This package provides core MCP tools that can be imported and registered
by connector-specific MCP servers (e.g., Obsidian, Notion).

Usage:
    from summary_stack_mcp_core import (
        search_stacks,
        get_stack,
        list_stacks,
        get_related_stacks,
    )

    # Register with FastMCP
    mcp = FastMCP("my-connector")
    mcp.tool()(search_stacks)
    mcp.tool()(get_stack)
    mcp.tool()(list_stacks)
    mcp.tool()(get_related_stacks)

Environment Variables:
    SUMMARY_STACK_API_URL: Base URL of the Summary Stack API
    SUMMARY_STACK_API_KEY: API key for authentication
"""

from .api_client import SummaryStackCoreAPIClient, SummaryStackCoreAPIError
from .config import CoreConfig, load_config
from .tools import get_related_stacks, get_stack, list_stacks, search_stacks

__all__ = [
    # Tools (primary exports)
    "search_stacks",
    "get_stack",
    "list_stacks",
    "get_related_stacks",
    # Config
    "CoreConfig",
    "load_config",
    # Client (for advanced usage)
    "SummaryStackCoreAPIClient",
    "SummaryStackCoreAPIError",
]
