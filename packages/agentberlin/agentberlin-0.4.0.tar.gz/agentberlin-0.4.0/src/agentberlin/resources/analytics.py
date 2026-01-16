"""Analytics resource for Agent Berlin SDK."""

from .._http import HTTPClient
from ..models.analytics import AnalyticsResponse


class AnalyticsResource:
    """Resource for analytics operations.

    Example:
        analytics = client.analytics.get(project_domain="example.com")
        print(f"Visibility: {analytics.visibility.current_percentage}%")
        print(f"LLM Sessions: {analytics.traffic.llm_sessions}")
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get(self, project_domain: str) -> AnalyticsResponse:
        """Get analytics data for a project.

        Fetch analytics dashboard data including visibility, traffic,
        topics, and competitors.

        Args:
            project_domain: The domain of the project (e.g., 'example.com').

        Returns:
            AnalyticsResponse with comprehensive analytics data.

        Raises:
            AgentBerlinValidationError: If project_domain is empty.
            AgentBerlinNotFoundError: If the domain doesn't exist.
            AgentBerlinAPIError: If the API returns an error.
        """
        data = self._http.post(
            "/analytics",
            json={"project_domain": project_domain},
        )
        return AnalyticsResponse.model_validate(data)
