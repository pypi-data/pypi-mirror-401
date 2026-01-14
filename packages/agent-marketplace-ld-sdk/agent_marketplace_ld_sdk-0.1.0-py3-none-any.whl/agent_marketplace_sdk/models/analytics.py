"""Analytics models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DownloadStats(BaseModel):
    """Download statistics model."""

    date: datetime
    downloads: int

    model_config = ConfigDict(from_attributes=True)


class AgentAnalytics(BaseModel):
    """Agent analytics model."""

    agent_id: int
    agent_slug: str
    total_downloads: int
    total_stars: int
    average_rating: float
    review_count: int
    daily_downloads: list[DownloadStats]

    model_config = ConfigDict(from_attributes=True)


class TrendingAgent(BaseModel):
    """Trending agent model."""

    id: int
    name: str
    slug: str
    description: str
    downloads_this_week: int
    stars_this_week: int
    trend_score: float

    model_config = ConfigDict(from_attributes=True)
