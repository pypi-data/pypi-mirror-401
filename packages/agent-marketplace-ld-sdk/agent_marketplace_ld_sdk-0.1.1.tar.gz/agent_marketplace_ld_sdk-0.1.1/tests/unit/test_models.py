"""Tests for Pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError as PydanticValidationError

from agent_marketplace_sdk.models import (
    Agent,
    AgentAnalytics,
    AgentCreate,
    AgentVersion,
    Category,
    DownloadStats,
    Review,
    ReviewCreate,
    TrendingAgent,
    User,
    UserProfile,
)


class TestUserModels:
    """Tests for User models."""

    def test_user_model(self):
        """Test User model."""
        user = User(id=1, username="testuser")
        assert user.id == 1
        assert user.username == "testuser"
        assert user.avatar_url is None

    def test_user_model_with_avatar(self):
        """Test User model with avatar."""
        user = User(
            id=1,
            username="testuser",
            avatar_url="https://example.com/avatar.png",
        )
        assert user.avatar_url == "https://example.com/avatar.png"

    def test_user_profile_model(self):
        """Test UserProfile model."""
        profile = UserProfile(
            id=1,
            username="testuser",
            email="test@example.com",
            reputation=100,
            created_at=datetime(2025, 1, 1),
        )
        assert profile.email == "test@example.com"
        assert profile.reputation == 100


class TestAgentModels:
    """Tests for Agent models."""

    def test_agent_model(self):
        """Test Agent model."""
        agent = Agent(
            id=1,
            name="Test Agent",
            slug="test-agent",
            description="A test agent",
            author=User(id=1, username="testuser"),
            current_version="1.0.0",
            downloads=100,
            stars=50,
            rating=4.5,
            category="testing",
            is_public=True,
            is_validated=True,
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 15),
        )
        assert agent.name == "Test Agent"
        assert agent.rating == 4.5

    def test_agent_version_model(self):
        """Test AgentVersion model."""
        version = AgentVersion(
            id=1,
            agent_id=1,
            version="1.0.0",
            size_bytes=1024,
            tested=True,
            security_scan_passed=True,
            published_at=datetime(2025, 1, 1),
        )
        assert version.version == "1.0.0"
        assert version.changelog is None

    def test_agent_create_model(self):
        """Test AgentCreate model."""
        agent = AgentCreate(
            name="Test Agent",
            description="A test agent for testing purposes.",
            category="testing",
            version="1.0.0",
        )
        assert agent.name == "Test Agent"

    def test_agent_create_invalid_version(self):
        """Test AgentCreate with invalid version."""
        with pytest.raises(PydanticValidationError):
            AgentCreate(
                name="Test Agent",
                description="A test agent for testing purposes.",
                category="testing",
                version="invalid",
            )

    def test_agent_create_name_too_short(self):
        """Test AgentCreate with name too short."""
        with pytest.raises(PydanticValidationError):
            AgentCreate(
                name="AB",
                description="A test agent for testing purposes.",
                category="testing",
            )

    def test_agent_create_description_too_short(self):
        """Test AgentCreate with description too short."""
        with pytest.raises(PydanticValidationError):
            AgentCreate(
                name="Test Agent",
                description="Short",
                category="testing",
            )


class TestReviewModels:
    """Tests for Review models."""

    def test_review_model(self):
        """Test Review model."""
        review = Review(
            id=1,
            agent_id=1,
            agent_slug="test-agent",
            user=User(id=1, username="testuser"),
            rating=5,
            comment="Great agent!",
            helpful_count=10,
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 1),
        )
        assert review.rating == 5
        assert review.comment == "Great agent!"

    def test_review_create_model(self):
        """Test ReviewCreate model."""
        review = ReviewCreate(rating=5, comment="Great agent!")
        assert review.rating == 5

    def test_review_create_invalid_rating(self):
        """Test ReviewCreate with invalid rating."""
        with pytest.raises(PydanticValidationError):
            ReviewCreate(rating=6)

    def test_review_create_invalid_rating_low(self):
        """Test ReviewCreate with rating too low."""
        with pytest.raises(PydanticValidationError):
            ReviewCreate(rating=0)


class TestCategoryModel:
    """Tests for Category model."""

    def test_category_model(self):
        """Test Category model."""
        category = Category(
            id=1,
            name="Testing",
            slug="testing",
            description="Testing category",
            agent_count=10,
        )
        assert category.name == "Testing"

    def test_category_model_minimal(self):
        """Test Category model with minimal data."""
        category = Category(id=1, name="Testing", slug="testing")
        assert category.description is None
        assert category.agent_count == 0


class TestAnalyticsModels:
    """Tests for Analytics models."""

    def test_download_stats_model(self):
        """Test DownloadStats model."""
        stats = DownloadStats(
            date=datetime(2025, 1, 1),
            downloads=100,
        )
        assert stats.downloads == 100

    def test_agent_analytics_model(self):
        """Test AgentAnalytics model."""
        analytics = AgentAnalytics(
            agent_id=1,
            agent_slug="test-agent",
            total_downloads=1000,
            total_stars=50,
            average_rating=4.5,
            review_count=25,
            daily_downloads=[
                DownloadStats(date=datetime(2025, 1, 1), downloads=100),
            ],
        )
        assert analytics.total_downloads == 1000

    def test_trending_agent_model(self):
        """Test TrendingAgent model."""
        trending = TrendingAgent(
            id=1,
            name="Test Agent",
            slug="test-agent",
            description="A test agent",
            downloads_this_week=500,
            stars_this_week=25,
            trend_score=95.5,
        )
        assert trending.trend_score == 95.5
