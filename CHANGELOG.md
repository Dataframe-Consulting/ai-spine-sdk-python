# Changelog

## [Unreleased]

## [2.3.0] - 2025-01-14
### Added
- New API key management methods for user administration (no authentication required):
  - `check_user_api_key()` - Check if a user has an API key and get its details
  - `generate_user_api_key()` - Generate or regenerate API key for a user
  - `revoke_user_api_key()` - Revoke (delete) a user's API key
- Support for unauthenticated API requests via `auth_required` parameter in `_request()` method
- New example script `api_key_management.py` demonstrating API key operations
- Comprehensive test coverage for all new API key management methods

### Changed
- Enhanced authentication system to support manual API key generation
- API key management endpoints do not require Bearer token authentication
- Updated base URL to `https://ai-spine-api.up.railway.app` in examples
- Updated documentation to clarify authentication requirements

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