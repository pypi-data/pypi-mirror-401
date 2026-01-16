"""Brand resource for Agent Berlin SDK."""

from typing import Literal, Optional

from .._http import HTTPClient
from ..models.brand import BrandProfileResponse, BrandProfileUpdateResponse


class BrandResource:
    """Resource for brand profile operations.

    Example:
        # Get brand profile
        profile = client.brand.get_profile(project_domain="example.com")
        print(f"Domain Authority: {profile.domain_authority}")
        print(f"Competitors: {profile.competitors}")

        # Update brand profile
        client.brand.update_profile(
            project_domain="example.com",
            field="competitors",
            value="competitor.com",
            mode="add"
        )
    """

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get_profile(self, project_domain: str) -> BrandProfileResponse:
        """Get the brand profile configuration for a project.

        Args:
            project_domain: The domain of the project (e.g., 'example.com').

        Returns:
            BrandProfileResponse with brand configuration.
        """
        data = self._http.post(
            "/brand/profile",
            json={"project_domain": project_domain},
        )
        return BrandProfileResponse.model_validate(data)

    def update_profile(
        self,
        project_domain: str,
        field: Literal[
            "name",
            "context",
            "competitors",
            "industries",
            "business_models",
            "company_size",
            "target_segments",
            "geographies",
            "personas",
        ],
        value: str,
        *,
        mode: Literal["add", "set"] = "add",
    ) -> BrandProfileUpdateResponse:
        """Update a specific field in the brand profile.

        For array fields (competitors, industries, etc.), you can either
        add new values to existing ones or set (replace) all values.

        Args:
            project_domain: The domain of the project (e.g., 'example.com').
            field: The field to update.
            value: The new value. For array fields, provide comma-separated values.
            mode: For array fields: 'add' adds to existing, 'set' replaces all.

        Returns:
            BrandProfileUpdateResponse with update confirmation.

        Note:
            Valid company_size values: solo, early_startup, startup, smb, mid_market, enterprise
        """
        payload: dict[str, object] = {
            "project_domain": project_domain,
            "field": field,
            "value": value,
            "mode": mode,
        }

        data = self._http.post("/brand/profile/update", json=payload)
        return BrandProfileUpdateResponse.model_validate(data)
