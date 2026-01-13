"""HTTP client for Summary Stack API."""

import logging
from typing import Any

import httpx

from summary_stack_shared import (
    RelatedStacksResponse,
    StackListResponse,
    StackSearchResponse,
    SummaryStackData,
)


logger = logging.getLogger(__name__)


class SummaryStackCoreAPIError(Exception):
    """Error from Summary Stack API."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class SummaryStackCoreAPIClient:
    """HTTP client for Summary Stack search and discovery endpoints."""

    def __init__(self, api_url: str, api_key: str):
        """Initialize the API client.

        Args:
            api_url: Base URL of the Summary Stack API
            api_key: API key for authentication
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        """Get default request headers."""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    async def list_stacks(self, limit: int = 20, offset: int = 0) -> StackListResponse:
        """List user's most recent summary stacks.

        Args:
            limit: Maximum results to return
            offset: Pagination offset

        Returns:
            Paginated list of stack summaries

        Raises:
            SummaryStackCoreAPIError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/stacks",
                params={"limit": limit, "offset": offset},
                headers=self._headers(),
                timeout=30.0,
            )

            self._raise_for_status(response)
            return StackListResponse.model_validate(response.json())

    async def search_stacks(self, query: str, limit: int = 10) -> StackSearchResponse:
        """Semantic search across user's summary stacks.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            Search results with similarity scores

        Raises:
            SummaryStackCoreAPIError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/api/v1/stacks/search",
                json={"query": query, "limit": limit},
                headers=self._headers(),
                timeout=60.0,  # Longer timeout for vector search
            )

            self._raise_for_status(response)
            return StackSearchResponse.model_validate(response.json())

    async def get_stack(self, stack_id: str) -> SummaryStackData:
        """Get full details of a specific summary stack.

        Args:
            stack_id: Summary stack UUID

        Returns:
            Full summary stack data

        Raises:
            SummaryStackCoreAPIError: If API request fails or stack not found
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/stacks/{stack_id}",
                headers=self._headers(),
                timeout=30.0,
            )

            self._raise_for_status(response)

            # The API returns SummaryStackCardResponse, but we need the full data
            # For now, return what we get from the API
            data = response.json()
            return self._card_to_stack_data(data, stack_id)

    async def get_related_stacks(
        self,
        stack_id: str,
        limit: int = 5,
    ) -> RelatedStacksResponse:
        """Find stacks related to a specific stack.

        Args:
            stack_id: Source stack UUID
            limit: Maximum related stacks to return

        Returns:
            Related stacks with similarity scores

        Raises:
            SummaryStackCoreAPIError: If API request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/stacks/{stack_id}/related",
                params={"limit": limit},
                headers=self._headers(),
                timeout=30.0,
            )

            self._raise_for_status(response)
            return RelatedStacksResponse.model_validate(response.json())

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise exception for error responses.

        Args:
            response: HTTP response

        Raises:
            SummaryStackCoreAPIError: If response indicates an error
        """
        if response.is_success:
            return

        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text

        raise SummaryStackCoreAPIError(
            message=f"API error: {detail}",
            status_code=response.status_code,
        )

    def _card_to_stack_data(self, card_data: dict[str, Any], stack_id: str) -> SummaryStackData:
        """Convert card response to SummaryStackData.

        The get_stack endpoint returns a card format. This converts it
        to SummaryStackData for consistent return type.

        Args:
            card_data: Card response from API
            stack_id: Stack ID

        Returns:
            SummaryStackData with available fields
        """
        from summary_stack_shared import ExecutiveSummary, SourceMetadata

        # Build executive summary from card data
        # Card only has key_insights as strings, so provide defaults for required fields
        bullets = card_data.get("key_insights", [])
        executive_summary = ExecutiveSummary(
            summary=card_data.get("summary", ""),
            bullets=[{"text": b, "source_phrase": "", "theme": ""} for b in bullets] if bullets else [],
        )

        # Build source metadata
        # Card response may have None for source_type, but SourceMetadata requires it
        from summary_stack_shared import SourceType
        source_metadata = SourceMetadata(
            uri=card_data.get("source_url") or "",
            source_type=card_data.get("source_type") or SourceType.URL,
            source_domain=card_data.get("source_domain"),
        )

        return SummaryStackData(
            summary_stack_id=stack_id,
            title=card_data.get("title"),
            executive_summary=executive_summary,
            source_metadata=source_metadata,
            passages=[],
        )
