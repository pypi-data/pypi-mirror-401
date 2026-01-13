"""Configuration for Summary Stack MCP Core."""

import os

from pydantic import BaseModel, Field


class CoreConfig(BaseModel):
    """Core configuration for Summary Stack MCP tools.

    Loaded from environment variables:
        SUMMARY_STACK_API_URL: API base URL (required)
        SUMMARY_STACK_API_KEY: API key for authentication (required)
    """

    api_url: str = Field(description="Summary Stack API base URL")
    api_key: str = Field(description="API key for authentication")


def load_config() -> CoreConfig:
    """Load configuration from environment variables.

    Returns:
        CoreConfig with API settings

    Raises:
        ValueError: If required environment variables are not set
    """
    api_url = os.environ.get("SUMMARY_STACK_API_URL")
    api_key = os.environ.get("SUMMARY_STACK_API_KEY")

    if not api_url:
        raise ValueError("SUMMARY_STACK_API_URL environment variable is required")

    if not api_key:
        raise ValueError("SUMMARY_STACK_API_KEY environment variable is required")

    return CoreConfig(
        api_url=api_url,
        api_key=api_key,
    )
