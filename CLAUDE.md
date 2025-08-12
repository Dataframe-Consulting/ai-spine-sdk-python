# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is the Python SDK for AI Spine - an AI agent orchestration system. Currently in pre-development phase with comprehensive requirements documentation but no implementation yet.

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

## Architecture

### Target Package Structure
```
ai_spine/
├── client.py      # Main SpineClient class - primary SDK interface
├── api.py         # HTTP client implementation with requests.Session
├── models.py      # Data models for Flow, Agent, Execution, etc.
├── exceptions.py  # Custom exception hierarchy
├── utils.py       # Helper functions
└── constants.py   # API endpoints and configuration
```

### Key Design Patterns
1. **Session-based HTTP Client**: Use `requests.Session()` with connection pooling and retry logic
2. **Polling for Async Operations**: No webhooks available - implement polling with configurable intervals for execution monitoring
3. **Type Safety**: All public methods must have type hints, use `mypy` in strict mode
4. **Error Handling**: Custom exception hierarchy mapping HTTP status codes to specific exceptions

### API Integration
- **Base URL**: `https://ai-spine-api-production.up.railway.app`
- **Authentication**: Currently disabled (`API_KEY_REQUIRED=false` in production)
- **Key Endpoints**:
  - `POST /flows/execute` - Execute AI flows
  - `GET /executions/{id}` - Monitor execution status
  - `GET/POST/DELETE /agents` - Agent management
  - `GET /health`, `/metrics`, `/status` - System monitoring

### Implementation Requirements
- Python 3.7+ compatibility required
- Use Google-style docstrings for all public methods
- Maintain 80%+ test coverage
- Follow the detailed specifications in `PYTHON_SDK_REQUIREMENTS.md`
- Package name for PyPI: `ai-spine-sdk`

## Current Status
**Pre-development phase**: No source code exists yet. Begin by creating the `ai_spine/` package structure and implementing the core `SpineClient` class in `client.py` according to the requirements specification.