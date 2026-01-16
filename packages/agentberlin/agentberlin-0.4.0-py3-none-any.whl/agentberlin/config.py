"""Configuration for the Agent Berlin SDK."""

from dataclasses import dataclass

DEFAULT_BASE_URL = "https://backend.agentberlin.ai/sdk"
DEFAULT_TIMEOUT = 30


@dataclass
class Config:
    """SDK configuration.

    Attributes:
        base_url: Base URL for the Agent Berlin API.
        timeout: Request timeout in seconds.
    """

    base_url: str = DEFAULT_BASE_URL
    timeout: int = DEFAULT_TIMEOUT
