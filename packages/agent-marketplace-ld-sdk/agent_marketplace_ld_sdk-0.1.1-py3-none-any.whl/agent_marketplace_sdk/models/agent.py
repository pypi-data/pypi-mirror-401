"""Agent models."""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from agent_marketplace_sdk.models.user import User


class AgentSummary(BaseModel):
    """Agent summary model for list responses."""

    id: int
    name: str
    slug: str
    description: str
    author: User
    current_version: str
    downloads: int
    stars: int
    rating: float
    category: str
    is_public: bool
    is_validated: bool

    model_config = ConfigDict(from_attributes=True)


class Agent(BaseModel):
    """Full agent model."""

    id: int
    name: str
    slug: str
    description: str
    author: User
    current_version: str
    downloads: int
    stars: int
    rating: float
    category: str
    is_public: bool
    is_validated: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentVersion(BaseModel):
    """Agent version model."""

    id: int
    agent_id: int
    version: str
    changelog: str | None = None
    size_bytes: int
    tested: bool
    security_scan_passed: bool
    quality_score: float | None = None
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentCreate(BaseModel):
    """Agent creation schema."""

    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    category: str
    version: str = "1.0.0"

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate semantic version."""
        if not re.match(r"^\d+\.\d+\.\d+$", v):
            raise ValueError("Version must be semantic (e.g., 1.0.0)")
        return v
