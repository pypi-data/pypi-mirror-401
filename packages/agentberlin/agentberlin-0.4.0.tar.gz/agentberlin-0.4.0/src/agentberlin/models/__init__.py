"""Pydantic models for Agent Berlin API responses."""

from .analytics import (
    AnalyticsResponse,
    ChannelBreakdown,
    CompetitorSummary,
    DailyTraffic,
    DataRange,
    TopicSummary,
    TrafficData,
    VisibilityData,
    VisibilityPoint,
)
from .brand import BrandProfileResponse, BrandProfileUpdateResponse
from .search import (
    KeywordResult,
    KeywordSearchResponse,
    PageDetailResponse,
    PageLink,
    PageLinksDetail,
    PageResult,
    PageSearchResponse,
    PageTopicInfo,
)
from .serp import SERPResponse, SERPResult

__all__ = [
    # Analytics
    "AnalyticsResponse",
    "VisibilityData",
    "VisibilityPoint",
    "TrafficData",
    "ChannelBreakdown",
    "DailyTraffic",
    "TopicSummary",
    "CompetitorSummary",
    "DataRange",
    # Search
    "PageSearchResponse",
    "PageResult",
    "KeywordSearchResponse",
    "KeywordResult",
    "PageDetailResponse",
    "PageLinksDetail",
    "PageLink",
    "PageTopicInfo",
    # Brand
    "BrandProfileResponse",
    "BrandProfileUpdateResponse",
    # SERP
    "SERPResponse",
    "SERPResult",
]
