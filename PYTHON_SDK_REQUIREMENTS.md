# Python SDK Requirements for AI Spine

## 🎯 Project Overview

Create a Python SDK for AI Spine that mirrors the functionality of the JavaScript SDK, providing a pythonic interface for AI agent orchestration.

**Goal**: Enable Python developers to integrate AI Spine into their applications with minimal friction, following Python best practices and conventions.

## 📋 Functional Requirements

### Core Features (Must Have)

1. **Client initialization**
   - Support optional API key (currently disabled in backend)
   - Default to production URL: `https://ai-spine-api-production.up.railway.app`
   - Allow custom base URL override
   - Session management with connection pooling

2. **Flow execution**
   - `execute_flow(flow_id: str, input_data: dict) -> dict`
   - `get_execution(execution_id: str) -> dict`
   - `wait_for_execution(execution_id: str, timeout: int = 300, interval: int = 2) -> dict`
   - `cancel_execution(execution_id: str) -> dict`

3. **Flow management**
   - `list_flows() -> List[dict]`
   - `get_flow(flow_id: str) -> dict`

4. **Agent management**
   - `list_agents() -> List[dict]`
   - `create_agent(agent_config: dict) -> dict`
   - `delete_agent(agent_id: str) -> bool`
   - Note: No update/PUT endpoint exists

5. **System operations**
   - `health_check() -> dict`
   - `get_metrics() -> dict`
   - `get_status() -> dict`

6. **Error handling**
   - Custom exception hierarchy
   - Automatic retry with exponential backoff
   - Timeout handling
   - Rate limit handling

### Features NOT to Implement

- ❌ **Webhooks** - Backend doesn't support them
- ❌ **Agent update (PUT)** - Endpoint doesn't exist
- ❌ **WebSocket connections** - Not supported
- ❌ **File uploads** - Not part of current API

## 🏗️ Technical Requirements

### Project Structure

```
ai-spine-sdk-python/
├── README.md                    # User documentation
├── CONTRIBUTING.md              # Development guidelines
├── LICENSE                      # MIT License
├── setup.py                     # Package configuration
├── setup.cfg                    # Additional config
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── .gitignore
├── .github/
│   └── workflows/
│       ├── test.yml            # CI testing
│       └── publish.yml         # PyPI publishing
├── ai_spine/
│   ├── __init__.py            # Package exports
│   ├── __version__.py         # Version management
│   ├── client.py              # Main SDK class
│   ├── api.py                 # HTTP client implementation
│   ├── exceptions.py          # Custom exceptions
│   ├── models.py              # Data models/types
│   ├── utils.py               # Helper functions
│   └── constants.py           # Configuration constants
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest configuration
│   ├── test_client.py         # Client tests
│   ├── test_api.py            # API tests
│   ├── test_models.py         # Model tests
│   ├── test_utils.py          # Utility tests
│   └── fixtures/              # Test data
│       └── responses.json
└── examples/
    ├── basic_usage.py          # Simple example
    ├── error_handling.py       # Error handling patterns
    ├── async_execution.py      # Async patterns
    └── batch_processing.py     # Batch operations

```

### Dependencies

**Runtime dependencies** (requirements.txt):
```
requests>=2.28.0,<3.0.0        # HTTP client
typing-extensions>=4.0.0       # Type hints for older Python
python-dateutil>=2.8.0         # Date handling
```

**Development dependencies** (requirements-dev.txt):
```
pytest>=7.0.0                  # Testing framework
pytest-cov>=4.0.0              # Coverage reporting
pytest-mock>=3.0.0             # Mocking support
responses>=0.22.0              # Mock HTTP responses
black>=22.0.0                  # Code formatting
flake8>=6.0.0                  # Linting
mypy>=1.0.0                    # Type checking
sphinx>=5.0.0                  # Documentation
build>=0.10.0                  # Build backend
twine>=4.0.0                   # PyPI upload
```

### Python Version Support

- **Minimum**: Python 3.7 (for compatibility)
- **Recommended**: Python 3.8+
- **Test matrix**: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

### Code Quality Standards

1. **Type hints** - All public methods must have type hints
2. **Docstrings** - Google-style docstrings for all public APIs
3. **Code coverage** - Minimum 80% test coverage
4. **Linting** - Pass flake8 with max-line-length=100
5. **Formatting** - Use black with default settings
6. **Type checking** - Pass mypy in strict mode

## 💻 Implementation Guidelines

### 1. Client Class Design

```python
from typing import Optional, Dict, Any, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class AISpine:
    """AI Spine SDK client for Python.
    
    Args:
        api_key: Optional API key for authentication
        base_url: API base URL (defaults to production)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retry attempts (default: 3)
        debug: Enable debug logging (default: False)
    
    Example:
        >>> client = AISpine()
        >>> result = client.execute_flow('credit_analysis', {'amount': 50000})
        >>> execution = client.wait_for_execution(result['execution_id'])
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        debug: bool = False
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://ai-spine-api-production.up.railway.app"
        self.timeout = timeout
        self.debug = debug
        
        # Configure session with retry strategy
        self.session = self._create_session(max_retries)
        
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create HTTP session with retry logic."""
        session = requests.Session()
        
        # Add retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'ai-spine-sdk-python/{__version__}'
        })
        
        if self.api_key:
            session.headers['Authorization'] = f'Bearer {self.api_key}'
            
        return session
```

### 2. Error Handling

```python
# exceptions.py
class AISpineError(Exception):
    """Base exception for AI Spine SDK."""
    pass

class AuthenticationError(AISpineError):
    """Raised when authentication fails."""
    pass

class ValidationError(AISpineError):
    """Raised when input validation fails."""
    pass

class ExecutionError(AISpineError):
    """Raised when flow execution fails."""
    pass

class TimeoutError(AISpineError):
    """Raised when operation times out."""
    pass

class RateLimitError(AISpineError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after
```

### 3. Model Classes (Optional but Recommended)

```python
# models.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime

@dataclass
class Flow:
    """Represents an AI Spine flow."""
    flow_id: str
    name: str
    description: str
    nodes: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Execution:
    """Represents a flow execution."""
    execution_id: str
    flow_id: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

### 4. Async Support (Optional Enhancement)

```python
# async_client.py
import asyncio
import aiohttp
from typing import Optional, Dict, Any

class AsyncAISpine:
    """Async version of AI Spine SDK client."""
    
    async def execute_flow(self, flow_id: str, input_data: Dict[str, Any]) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/flows/execute",
                json={"flow_id": flow_id, "input_data": input_data}
            ) as response:
                return await response.json()
    
    async def wait_for_execution(
        self, 
        execution_id: str,
        timeout: int = 300,
        interval: int = 2
    ) -> Dict:
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < timeout:
            result = await self.get_execution(execution_id)
            if result['status'] in ['completed', 'failed']:
                return result
            await asyncio.sleep(interval)
        raise TimeoutError(f"Execution {execution_id} timed out")
```

## 🧪 Testing Requirements

### Test Coverage Areas

1. **Unit tests** (tests/test_*.py)
   - Client initialization with various configs
   - All public methods
   - Error handling scenarios
   - Retry logic
   - Input validation

2. **Integration tests** (tests/integration/)
   - Real API calls (with test API key)
   - End-to-end flow execution
   - Error scenarios

3. **Mock tests** (using responses library)
   ```python
   import responses
   
   @responses.activate
   def test_execute_flow():
       responses.add(
           responses.POST,
           'https://ai-spine-api-production.up.railway.app/flows/execute',
           json={'execution_id': 'exec-123', 'status': 'pending'},
           status=200
       )
       
       client = AISpine()
       result = client.execute_flow('test-flow', {'data': 'test'})
       assert result['execution_id'] == 'exec-123'
   ```

### Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_spine --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v

# Type checking
mypy ai_spine

# Linting
flake8 ai_spine tests

# Format check
black --check ai_spine tests
```

## 📦 Distribution & Publishing

### setup.py Configuration

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("ai_spine/__version__.py", "r") as f:
    exec(f.read())

setup(
    name="ai-spine-sdk",
    version=__version__,
    author="AI Spine Team",
    author_email="support@dataframeai.com",
    description="Python SDK for AI Spine - The Stripe for AI Agent Orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dataframe-Consulting/ai-spine-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/Dataframe-Consulting/ai-spine-sdk-python/issues",
        "Documentation": "https://dataframeai.com/docs",
        "Source Code": "https://github.com/Dataframe-Consulting/ai-spine-sdk-python",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0,<3.0.0",
        "typing-extensions>=4.0.0;python_version<'3.8'",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.0.0",
            "responses>=0.22.0",
            "black>=22.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "async": [
            "aiohttp>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-spine=ai_spine.cli:main",  # Optional CLI
        ],
    },
)
```

### Publishing Process

```bash
# 1. Ensure version is updated
# Edit ai_spine/__version__.py
__version__ = "2.1.0"

# 2. Run tests
pytest

# 3. Build distribution
python -m build

# 4. Check distribution
twine check dist/*

# 5. Upload to TestPyPI (optional)
twine upload --repository testpypi dist/*

# 6. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ ai-spine-sdk

# 7. Upload to PyPI
twine upload dist/*

# 8. Verify installation
pip install ai-spine-sdk
```

## 📝 Documentation Requirements

### README.md Structure

1. **Project description** - Clear value proposition
2. **Installation** - pip install instructions
3. **Quick start** - Working example in <10 lines
4. **API reference** - All public methods documented
5. **Examples** - Common use cases
6. **Error handling** - How to handle exceptions
7. **Contributing** - How to contribute
8. **License** - MIT

### Docstring Example

```python
def execute_flow(
    self, 
    flow_id: str, 
    input_data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Execute an AI Spine flow.
    
    Args:
        flow_id: Unique identifier of the flow to execute
        input_data: Input data for the flow execution
        metadata: Optional metadata to attach to the execution
    
    Returns:
        Dictionary containing:
            - execution_id (str): Unique execution identifier
            - status (str): Initial status ('pending')
            - created_at (str): ISO timestamp of creation
    
    Raises:
        ValidationError: If flow_id or input_data is invalid
        AuthenticationError: If API key is invalid
        ExecutionError: If flow execution fails
        requests.RequestException: If network request fails
    
    Example:
        >>> client = AISpine()
        >>> result = client.execute_flow(
        ...     'sentiment-analysis',
        ...     {'text': 'This product is amazing!'}
        ... )
        >>> print(result['execution_id'])
        'exec-123abc'
    """
```

## 🚀 Development Timeline

### Phase 1: Core Implementation (Days 1-2)
- [ ] Project setup and structure
- [ ] Basic client implementation
- [ ] Core API methods
- [ ] Error handling
- [ ] Basic tests

### Phase 2: Enhancement (Day 3)
- [ ] Retry logic and resilience
- [ ] Type hints and models
- [ ] Comprehensive tests
- [ ] Documentation

### Phase 3: Polish (Day 4)
- [ ] Examples and tutorials
- [ ] CI/CD setup
- [ ] Performance optimization
- [ ] Security review

### Phase 4: Release (Day 5)
- [ ] Final testing
- [ ] Documentation review
- [ ] PyPI publication
- [ ] Announcement

## ⚠️ Important Considerations

1. **No authentication required** - API currently has `API_KEY_REQUIRED=false`
2. **No webhooks** - Use polling only
3. **No agent updates** - Only create and delete
4. **Production URL** - Default to Railway, not localhost
5. **HTTP/HTTPS only** - No WebSocket or other protocols

## 🎯 Success Criteria

- [ ] All core endpoints implemented
- [ ] 80%+ test coverage
- [ ] Type hints on all public methods
- [ ] Passes mypy strict mode
- [ ] Comprehensive documentation
- [ ] Published to PyPI
- [ ] Works with Python 3.7+
- [ ] <5 second import time
- [ ] <10MB package size

## 📚 References

- [JavaScript SDK](https://github.com/Dataframe-Consulting/ai-spine-sdk-js)
- [API Documentation](https://ai-spine-api-production.up.railway.app/docs)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)
- [PyPI Publishing Tutorial](https://realpython.com/pypi-publish-python-package/)

---

**Note**: This SDK should maintain feature parity with the JavaScript SDK while following Python conventions and best practices. When in doubt, prioritize pythonic patterns over direct translation.