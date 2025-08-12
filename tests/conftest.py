"""Pytest configuration and fixtures."""

import pytest
import responses
from ai_spine import AISpine


@pytest.fixture
def base_url():
    """Base URL for testing."""
    return "https://test-api.ai-spine.com"


@pytest.fixture
def client(base_url):
    """Create AI Spine client for testing."""
    return AISpine(base_url=base_url)


@pytest.fixture
def mock_responses():
    """Enable responses mocking."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def sample_flow():
    """Sample flow data."""
    return {
        "flow_id": "test-flow-123",
        "name": "Test Flow",
        "description": "A test flow",
        "nodes": [
            {"id": "node1", "type": "input"},
            {"id": "node2", "type": "process"},
            {"id": "node3", "type": "output"}
        ],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_execution():
    """Sample execution data."""
    return {
        "execution_id": "exec-456",
        "flow_id": "test-flow-123",
        "status": "pending",
        "input_data": {"test": "data"},
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_agent():
    """Sample agent data."""
    return {
        "agent_id": "agent-789",
        "name": "Test Agent",
        "type": "processor",
        "configuration": {
            "model": "gpt-4",
            "temperature": 0.7
        },
        "created_at": "2024-01-01T00:00:00Z"
    }