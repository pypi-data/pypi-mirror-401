"""Mock API responses for testing."""

# Sample user data
SAMPLE_USER = {
    "id": 1,
    "username": "testuser",
    "avatar_url": "https://example.com/avatar.png",
}

SAMPLE_USER_PROFILE = {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "avatar_url": "https://example.com/avatar.png",
    "bio": "A test user",
    "reputation": 100,
    "created_at": "2025-01-01T00:00:00Z",
}

# Sample agent data
SAMPLE_AGENT = {
    "id": 1,
    "name": "Advanced PM",
    "slug": "advanced-pm",
    "description": "Enhanced project management agent with advanced capabilities.",
    "author": SAMPLE_USER,
    "current_version": "1.2.0",
    "downloads": 1000,
    "stars": 50,
    "rating": 4.5,
    "category": "pm",
    "is_public": True,
    "is_validated": True,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-15T00:00:00Z",
}

SAMPLE_AGENT_2 = {
    "id": 2,
    "name": "Code Reviewer",
    "slug": "code-reviewer",
    "description": "Automated code review agent.",
    "author": SAMPLE_USER,
    "current_version": "2.0.0",
    "downloads": 500,
    "stars": 25,
    "rating": 4.2,
    "category": "testing",
    "is_public": True,
    "is_validated": True,
    "created_at": "2025-01-05T00:00:00Z",
    "updated_at": "2025-01-20T00:00:00Z",
}

# Sample agent version data
SAMPLE_AGENT_VERSION = {
    "id": 1,
    "agent_id": 1,
    "version": "1.2.0",
    "changelog": "Bug fixes and performance improvements",
    "size_bytes": 102400,
    "tested": True,
    "security_scan_passed": True,
    "quality_score": 0.95,
    "published_at": "2025-01-15T00:00:00Z",
}

# Sample review data
SAMPLE_REVIEW = {
    "id": 1,
    "agent_id": 1,
    "agent_slug": "advanced-pm",
    "user": SAMPLE_USER,
    "rating": 5,
    "comment": "Excellent agent! Very helpful.",
    "helpful_count": 10,
    "created_at": "2025-01-10T00:00:00Z",
    "updated_at": "2025-01-10T00:00:00Z",
}

# Sample category data
SAMPLE_CATEGORY = {
    "id": 1,
    "name": "Project Management",
    "slug": "pm",
    "description": "Agents for project management tasks",
    "agent_count": 15,
}

SAMPLE_CATEGORY_2 = {
    "id": 2,
    "name": "Testing",
    "slug": "testing",
    "description": "Agents for testing and quality assurance",
    "agent_count": 10,
}

# Sample analytics data
SAMPLE_DOWNLOAD_STATS = [
    {"date": "2025-01-10T00:00:00Z", "downloads": 100},
    {"date": "2025-01-11T00:00:00Z", "downloads": 150},
    {"date": "2025-01-12T00:00:00Z", "downloads": 200},
]

SAMPLE_AGENT_ANALYTICS = {
    "agent_id": 1,
    "agent_slug": "advanced-pm",
    "total_downloads": 1000,
    "total_stars": 50,
    "average_rating": 4.5,
    "review_count": 25,
    "daily_downloads": SAMPLE_DOWNLOAD_STATS,
}

SAMPLE_TRENDING_AGENT = {
    "id": 1,
    "name": "Advanced PM",
    "slug": "advanced-pm",
    "description": "Enhanced project management agent.",
    "downloads_this_week": 500,
    "stars_this_week": 25,
    "trend_score": 95.5,
}

# List responses
AGENTS_LIST_RESPONSE = {
    "items": [SAMPLE_AGENT, SAMPLE_AGENT_2],
    "total": 2,
}

CATEGORIES_LIST_RESPONSE = {
    "items": [SAMPLE_CATEGORY, SAMPLE_CATEGORY_2],
    "total": 2,
}

REVIEWS_LIST_RESPONSE = {
    "items": [SAMPLE_REVIEW],
    "total": 1,
}

VERSIONS_LIST_RESPONSE = {
    "items": [SAMPLE_AGENT_VERSION],
    "total": 1,
}

TRENDING_LIST_RESPONSE = {
    "items": [SAMPLE_TRENDING_AGENT],
    "total": 1,
}

SEARCH_RESPONSE = {
    "items": [SAMPLE_AGENT],
    "total": 1,
}
