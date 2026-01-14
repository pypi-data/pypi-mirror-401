"""Review models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from agent_marketplace_sdk.models.user import User


class Review(BaseModel):
    """Review model."""

    id: int
    agent_id: int
    agent_slug: str
    user: User
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
    helpful_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    """Review creation schema."""

    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=1000)
