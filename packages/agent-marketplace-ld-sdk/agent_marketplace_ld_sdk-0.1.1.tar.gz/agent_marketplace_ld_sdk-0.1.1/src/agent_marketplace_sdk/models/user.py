"""User models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """User model."""

    id: int
    username: str
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    """Full user profile model."""

    id: int
    username: str
    email: str
    avatar_url: str | None = None
    bio: str | None = None
    reputation: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
