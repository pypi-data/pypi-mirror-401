"""Core MCP tools for Summary Stack search and discovery.

These tools are designed to be imported and registered by connector-specific
MCP servers (e.g., Obsidian, Notion). They provide search, listing, and
discovery capabilities across the user's Summary Stacks via the API.
"""

import logging

from .api_client import SummaryStackCoreAPIClient, SummaryStackCoreAPIError
from .config import load_config


logger = logging.getLogger(__name__)


async def search_stacks(query: str, limit: int = 10) -> str:
    """Semantic search across your Summary Stacks.

    Finds stacks that are semantically related to your query using
    vector similarity search. Returns the most relevant stacks with
    matching content snippets.

    Args:
        query: Search query (what you're looking for)
        limit: Maximum number of results to return (default: 10)

    Returns:
        Formatted search results with titles, summaries, and similarity scores
    """
    config = load_config()
    client = SummaryStackCoreAPIClient(config.api_url, config.api_key)

    try:
        response = await client.search_stacks(query=query, limit=limit)

        if not response.results:
            return f"No stacks found matching '{query}'"

        lines = [f"Found {response.total_results} stack(s) matching '{query}':\n"]

        for i, result in enumerate(response.results, 1):
            similarity_pct = int(result.similarity * 100)
            lines.append(f"{i}. **{result.title}** ({similarity_pct}% match)")
            lines.append(f"   ID: {result.summary_stack_id}")

            if result.summary:
                summary_preview = result.summary[:150] + "..." if len(result.summary) > 150 else result.summary
                lines.append(f"   {summary_preview}")

            if result.matching_chunks:
                lines.append(f"   Matching content: \"{result.matching_chunks[0][:100]}...\"")

            lines.append("")

        return "\n".join(lines)

    except SummaryStackCoreAPIError as e:
        logger.error(f"Search failed: {e}")
        return f"Search failed: {e}"


async def get_stack(stack_id: str) -> str:
    """Get full details of a specific Summary Stack.

    Retrieves the complete summary stack including title, executive summary,
    key insights, and source information.

    Args:
        stack_id: The UUID of the summary stack to retrieve

    Returns:
        Formatted stack details with all available information
    """
    config = load_config()
    client = SummaryStackCoreAPIClient(config.api_url, config.api_key)

    try:
        stack = await client.get_stack(stack_id)

        lines = [
            f"# {stack.title or 'Untitled'}",
            f"**ID:** {stack.summary_stack_id}",
            "",
        ]

        if stack.source_metadata:
            meta = stack.source_metadata
            if meta.source_domain:
                lines.append(f"**Source:** {meta.source_domain}")
            if meta.uri:
                lines.append(f"**URL:** {meta.uri}")
            lines.append("")

        if stack.executive_summary:
            lines.append("## Summary")
            lines.append(stack.executive_summary.summary or "")
            lines.append("")

            if stack.executive_summary.bullets:
                lines.append("## Key Insights")
                for bullet in stack.executive_summary.bullets:
                    text = bullet.text if hasattr(bullet, "text") else str(bullet)
                    lines.append(f"- {text}")
                lines.append("")

        return "\n".join(lines)

    except SummaryStackCoreAPIError as e:
        logger.error(f"Get stack failed: {e}")
        return f"Failed to get stack: {e}"


async def list_stacks(limit: int = 20, offset: int = 0) -> str:
    """List your most recent Summary Stacks.

    Returns a paginated list of your stacks ordered by creation date
    (newest first). Use offset for pagination through large collections.

    Args:
        limit: Maximum number of stacks to return (default: 20)
        offset: Number of stacks to skip for pagination (default: 0)

    Returns:
        Formatted list of stacks with titles and summaries
    """
    config = load_config()
    client = SummaryStackCoreAPIClient(config.api_url, config.api_key)

    try:
        response = await client.list_stacks(limit=limit, offset=offset)

        if not response.items:
            return "No Summary Stacks found"

        lines = [f"Found {response.total} stack(s) (showing {len(response.items)}):\n"]

        for i, item in enumerate(response.items, offset + 1):
            lines.append(f"{i}. **{item.title}**")
            lines.append(f"   ID: {item.summary_stack_id}")

            if item.source_domain:
                lines.append(f"   Source: {item.source_domain}")

            if item.summary:
                lines.append(f"   {item.summary}")

            lines.append("")

        if response.total > offset + len(response.items):
            remaining = response.total - (offset + len(response.items))
            lines.append(f"... and {remaining} more. Use offset={offset + limit} to see next page.")

        return "\n".join(lines)

    except SummaryStackCoreAPIError as e:
        logger.error(f"List stacks failed: {e}")
        return f"Failed to list stacks: {e}"


async def get_related_stacks(stack_id: str, limit: int = 5) -> str:
    """Find Summary Stacks related to a specific stack.

    Uses semantic similarity to discover stacks with related content.
    Useful for exploring connections between your knowledge.

    Args:
        stack_id: The UUID of the source stack
        limit: Maximum number of related stacks to return (default: 5)

    Returns:
        Formatted list of related stacks with similarity scores
    """
    config = load_config()
    client = SummaryStackCoreAPIClient(config.api_url, config.api_key)

    try:
        response = await client.get_related_stacks(stack_id=stack_id, limit=limit)

        if not response.related:
            return f"No related stacks found for {stack_id}"

        lines = [f"Found {len(response.related)} related stack(s):\n"]

        for i, item in enumerate(response.related, 1):
            similarity_pct = int(item.similarity_score * 100)
            lines.append(f"{i}. **{item.title}** ({similarity_pct}% similar)")
            lines.append(f"   ID: {item.summary_stack_id}")

            if item.summary:
                summary_preview = item.summary[:150] + "..." if len(item.summary) > 150 else item.summary
                lines.append(f"   {summary_preview}")

            lines.append("")

        return "\n".join(lines)

    except SummaryStackCoreAPIError as e:
        logger.error(f"Get related stacks failed: {e}")
        return f"Failed to get related stacks: {e}"
