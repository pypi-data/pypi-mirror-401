"""Pydantic models for SERP API responses."""

from typing import List

from pydantic import BaseModel, Field


class SERPResult(BaseModel):
    """Single search result."""

    title: str
    url: str
    snippet: str


class SERPResponse(BaseModel):
    """Response for SERP fetch."""

    query: str
    results: List[SERPResult] = Field(default_factory=list)
    total: int
