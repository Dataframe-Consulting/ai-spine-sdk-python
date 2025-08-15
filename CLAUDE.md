# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is the Python SDK for AI Spine - an AI agent orchestration system. The SDK provides a Python interface for interacting with the AI Spine API, including flow execution, agent management, and system monitoring.

## Development Commands
Once the project is set up with dependencies, use these commands:

```bash
# Testing
pytest                          # Run all tests
pytest --cov=ai_spine          # Run tests with coverage report
pytest tests/test_client.py -v # Run specific test file

# Code Quality
black ai_spine tests           # Format code
flake8 ai_spine tests         # Lint code
mypy ai_spine                 # Type checking

# Building
python -m build               # Build distribution packages
pip install -e .              # Install package in development mode
```

## Deployment and Versioning

### 🚀 Automatic Deployment
**IMPORTANT**: The main branch has automatic deployment to PyPI configured via GitHub Actions. When you update the version in `ai_spine/__version__.py` and push to main, the package will be automatically published to PyPI.

### 📦 Version Management
When completing a feature or fix, you MUST:
1. Ask the user what version number to use (if not already specified)
2. Follow semantic versioning (A.B.C):
   - **A (Major)**: Breaking changes, incompatible API changes
   - **B (Minor)**: New features, backwards compatible
   - **C (Patch)**: Bug fixes, minor improvements

Examples:
- `2.2.0` → `3.0.0`: Breaking change (e.g., required parameters, removed methods)
- `2.2.0` → `2.3.0`: New feature (e.g., new methods, new optional parameters)
- `2.2.0` → `2.2.1`: Bug fix or documentation update

### 📝 Release Process
**CRITICAL**: Before deploying a new version, you MUST:

1. **Update CHANGELOG.md** (MUST be written in English):
   - Move changes from `[Unreleased]` section to a new version section
   - Add the version number and current date
   - Format: `## [X.Y.Z] - YYYY-MM-DD`
   - List all changes under appropriate categories (Added, Changed, Fixed, etc.)
   - Use clear, concise English for all descriptions

2. **Update version**:
   - Edit `ai_spine/__version__.py` with the new version number

3. **Commit and deploy**:
   ```bash
   git add CHANGELOG.md ai_spine/__version__.py
   git commit -m "chore: release vX.Y.Z"
   git push origin main
   ```

4. **GitHub Actions will automatically**:
   - Run tests
   - Build package
   - Publish to PyPI
   - Create GitHub release with notes from CHANGELOG.md

## Architecture

### Current Package Structure
```
ai_spine/
├── client.py      # Main AISpine class - primary SDK interface
├── models.py      # Data models for Flow, Agent, Execution, etc.
├── exceptions.py  # Custom exception hierarchy including InsufficientCreditsError
├── utils.py       # Helper functions
├── constants.py   # API endpoints and configuration
└── __version__.py # Version information (triggers auto-deploy on change)
```

### Key Design Patterns
1. **Session-based HTTP Client**: Uses `requests.Session()` with connection pooling and retry logic
2. **Polling for Async Operations**: Implements polling with configurable intervals for execution monitoring
3. **Type Safety**: All public methods have type hints, use `mypy` in strict mode
4. **Error Handling**: Custom exception hierarchy mapping HTTP status codes to specific exceptions

### API Integration
- **Base URL**: `https://ai-spine-api.up.railway.app`
- **Authentication**: API key required (must start with `sk_` prefix)
- **Key Endpoints**:
  - `POST /flows/execute` - Execute AI flows
  - `GET /executions/{id}` - Monitor execution status
  - `GET/POST/DELETE /agents` - Agent management
  - `GET /api/v1/users/me` - Get current user and credits
  - `GET /health`, `/metrics`, `/status` - System monitoring

### Implementation Requirements
- Python 3.7+ compatibility required
- Use Google-style docstrings for all public methods
- Maintain 80%+ test coverage
- Package name for PyPI: `ai-spine-sdk`

## Current Status
**Version 2.2.0**: Production-ready SDK with full API coverage, credit management, and comprehensive error handling. Automatic deployment configured via GitHub Actions.