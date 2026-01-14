# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-01-13

### Added
- CodeQL security scanning workflow
- Snyk vulnerability scanning
- Dependabot for automated dependency updates
- Codecov integration for coverage reporting
- Comprehensive README with 14 badges
- Detailed API documentation and examples

### Changed
- Updated all GitHub Actions to latest versions (checkout v6, setup-python v6, etc.)
- Improved README with installation, configuration, and development sections

## [0.1.0] - 2026-01-13

### Added
- Initial release
- `MarketplaceClient` for synchronous operations
- `AsyncMarketplaceClient` for asynchronous operations
- Agent operations: list, get, install, publish, update, delete, star, unstar
- User operations: get, me, get_agents, get_starred
- Review operations: list, create, update, delete, mark_helpful
- Category operations: list, get
- Search operations: search with filters
- Analytics operations: get_agent_analytics, get_trending
- Configuration management with file and environment variable support
- Pydantic models for type-safe data handling
- Custom exceptions for error handling
- Comprehensive test suite with 100% coverage
- GitHub Actions CI/CD workflows
- Full documentation and examples
