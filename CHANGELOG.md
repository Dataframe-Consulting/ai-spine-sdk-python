# Changelog

## [Unreleased]

## [2.2.2] - 2025-01-13
### Added
- Dynamic changelog extraction for GitHub releases
- CHANGELOG.md for tracking version history

### Changed
- Simplified CHANGELOG format (removed boilerplate)
- GitHub Actions workflow now uses CHANGELOG.md for release notes

## [2.2.1] - 2025-01-13
### Added
- GitHub Actions CI/CD workflow for automatic PyPI deployment
- Automatic release creation on version changes

### Fixed
- Python 3.8 compatibility issues (now requires Python 3.9+)
- Workflow permissions for creating GitHub releases

## [2.2.0] - 2025-01-13
### Breaking Changes
- API key is now required (no default value)
- API key must start with 'sk_' prefix
- Minimum Python version changed from 3.7 to 3.9

### Added
- `get_current_user()` method to get user info and credits
- `check_credits()` method to check remaining credits
- `InsufficientCreditsError` exception for credit management
- Better error handling for 401, 403, and 429 status codes
- Support for custom base_url with trailing slash handling

### Changed
- Updated exception messages with helpful URLs
- Improved retry logic configuration

## [2.0.0] - 2025-01-12
### Added
- Initial release of the AI Spine Python SDK
- Core client implementation with session management
- Flow execution and monitoring
- Agent management capabilities
- Comprehensive error handling
- Type hints and documentation