# Summary Stack MCP Core

Shared MCP tools for Summary Stack connectors. Provides core RAG/search functionality that connector-specific MCP servers can import and register.

## Tools Provided

- `search_stacks` - Semantic search across summary stacks
- `get_stack` - Get a specific stack by ID
- `list_stacks` - List recent stacks
- `get_related_stacks` - Find related stacks

## Usage

```python
from summary_stack_mcp_core import search_stacks, get_stack, list_stacks, get_related_stacks

# Register with FastMCP
mcp.tool()(search_stacks)
mcp.tool()(get_stack)
mcp.tool()(list_stacks)
mcp.tool()(get_related_stacks)
```

## Configuration

Set environment variables:
- `SUMMARY_STACK_API_URL` - API base URL
- `SUMMARY_STACK_API_KEY` - API key for authentication
