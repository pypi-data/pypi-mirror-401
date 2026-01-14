"""Category models."""

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    """Category model."""

    id: int
    name: str
    slug: str
    description: str | None = None
    agent_count: int = 0

    model_config = ConfigDict(from_attributes=True)
