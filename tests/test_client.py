"""Tests for AI Spine client."""

import pytest
import responses
import json
import warnings
from ai_spine import AISpine, Client, ValidationError, AuthenticationError, APIError, InsufficientCreditsError, RateLimitError, ExecutionError


class TestClientInitialization:
    """Test client initialization."""

    def test_api_key_required(self):
        """Test that API key is required."""
        with pytest.raises(ValueError, match="API key is required"):
            client = AISpine(api_key="")

        with pytest.raises(ValueError, match="API key is required"):
            client = AISpine(api_key=None)

    def test_api_key_warning(self):
        """Test warning for invalid API key format."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            client = AISpine(api_key="invalid_key_format")
            assert len(w) == 1
            assert "API key should start with 'sk_'" in str(w[0].message)

    def test_valid_api_key(self):
        """Test client with valid API key."""
        client = AISpine(api_key="sk_test_key")
        assert client.api_key == "sk_test_key"
        assert client.base_url == "https://ai-spine-api.up.railway.app"
        assert client.timeout == 30
        assert client.debug is False

    def test_custom_initialization(self):
        """Test client with custom settings."""
        client = AISpine(
            api_key="sk_test_key",
            base_url="https://custom.ai-spine.com/",  # Test trailing slash removal
            timeout=60,
            max_retries=5,
            debug=True
        )
        assert client.api_key == "sk_test_key"
        assert client.base_url == "https://custom.ai-spine.com"  # Trailing slash removed
        assert client.timeout == 60
        assert client.debug is True

    def test_client_alias(self):
        """Test Client alias works."""
        client = Client(api_key="sk_test_key")
        assert client.api_key == "sk_test_key"
        assert isinstance(client, AISpine)

    def test_context_manager(self):
        """Test client as context manager."""
        with AISpine(api_key="sk_test_key") as client:
            assert client.session is not None
            # Check Authorization header is set
            assert "Authorization" in client.session.headers
            assert client.session.headers["Authorization"] == "Bearer sk_test_key"


class TestFlowExecution:
    """Test flow execution methods."""

    @responses.activate
    def test_execute_flow_success(self, client, base_url):
        """Test successful flow execution."""
        responses.add(
            responses.POST,
            f"{base_url}/flows/execute",
            json={"execution_id": "exec-123", "status": "pending"},
            status=200
        )

        result = client.execute_flow("test-flow", {"input": "data"})
        assert result["execution_id"] == "exec-123"
        assert result["status"] == "pending"

    @responses.activate
    def test_execute_flow_with_metadata(self, client, base_url):
        """Test flow execution with metadata."""
        responses.add(
            responses.POST,
            f"{base_url}/flows/execute",
            json={"execution_id": "exec-123", "status": "pending"},
            status=200
        )

        result = client.execute_flow(
            "test-flow",
            {"input": "data"},
            metadata={"user": "test"}
        )
        assert result["execution_id"] == "exec-123"

    def test_execute_flow_invalid_flow_id(self, client):
        """Test flow execution with invalid flow ID."""
        with pytest.raises(ValidationError):
            client.execute_flow("", {"input": "data"})

    def test_execute_flow_invalid_input_data(self, client):
        """Test flow execution with invalid input data."""
        with pytest.raises(ValidationError):
            client.execute_flow("test-flow", None)

    @responses.activate
    def test_get_execution_success(self, client, base_url, sample_execution):
        """Test getting execution status."""
        responses.add(
            responses.GET,
            f"{base_url}/executions/exec-456",
            json=sample_execution,
            status=200
        )

        result = client.get_execution("exec-456")
        assert result["execution_id"] == "exec-456"
        assert result["status"] == "pending"

    @responses.activate
    def test_wait_for_execution_success(self, client, base_url):
        """Test waiting for execution completion."""
        # First call returns running
        responses.add(
            responses.GET,
            f"{base_url}/executions/exec-123",
            json={"execution_id": "exec-123", "status": "running"},
            status=200
        )
        # Second call returns completed
        responses.add(
            responses.GET,
            f"{base_url}/executions/exec-123",
            json={
                "execution_id": "exec-123",
                "status": "completed",
                "output_data": {"result": "success"}
            },
            status=200
        )

        result = client.wait_for_execution("exec-123", timeout=5, interval=0.1)
        assert result["status"] == "completed"
        assert result["output_data"]["result"] == "success"

    @responses.activate
    def test_wait_for_execution_failure(self, client, base_url):
        """Test waiting for failed execution."""
        responses.add(
            responses.GET,
            f"{base_url}/executions/exec-123",
            json={
                "execution_id": "exec-123",
                "status": "failed",
                "error_message": "Processing failed"
            },
            status=200
        )

        with pytest.raises(ExecutionError) as exc_info:
            client.wait_for_execution("exec-123", timeout=5, interval=0.1)
        assert "Processing failed" in str(exc_info.value)


class TestFlowManagement:
    """Test flow management methods."""

    @responses.activate
    def test_list_flows_array_response(self, client, base_url, sample_flow):
        """Test listing flows with array response."""
        responses.add(
            responses.GET,
            f"{base_url}/flows",
            json=[sample_flow],
            status=200
        )

        flows = client.list_flows()
        assert len(flows) == 1
        assert flows[0]["flow_id"] == "test-flow-123"

    @responses.activate
    def test_list_flows_object_response(self, client, base_url, sample_flow):
        """Test listing flows with object response."""
        responses.add(
            responses.GET,
            f"{base_url}/flows",
            json={"flows": [sample_flow]},
            status=200
        )

        flows = client.list_flows()
        assert len(flows) == 1
        assert flows[0]["flow_id"] == "test-flow-123"

    @responses.activate
    def test_get_flow_success(self, client, base_url, sample_flow):
        """Test getting flow details."""
        responses.add(
            responses.GET,
            f"{base_url}/flows/test-flow-123",
            json=sample_flow,
            status=200
        )

        flow = client.get_flow("test-flow-123")
        assert flow["flow_id"] == "test-flow-123"
        assert flow["name"] == "Test Flow"


class TestAgentManagement:
    """Test agent management methods."""

    @responses.activate
    def test_list_agents(self, client, base_url, sample_agent):
        """Test listing agents."""
        responses.add(
            responses.GET,
            f"{base_url}/agents",
            json=[sample_agent],
            status=200
        )

        agents = client.list_agents()
        assert len(agents) == 1
        assert agents[0]["agent_id"] == "agent-789"

    @responses.activate
    def test_create_agent(self, client, base_url, sample_agent):
        """Test creating an agent."""
        responses.add(
            responses.POST,
            f"{base_url}/agents",
            json=sample_agent,
            status=201
        )

        agent_config = {
            "name": "Test Agent",
            "type": "processor",
            "configuration": {"model": "gpt-4"}
        }

        agent = client.create_agent(agent_config)
        assert agent["agent_id"] == "agent-789"

    @responses.activate
    def test_delete_agent_success(self, client, base_url):
        """Test deleting an agent."""
        responses.add(
            responses.DELETE,
            f"{base_url}/agents/agent-789",
            status=204
        )

        result = client.delete_agent("agent-789")
        assert result is True

    @responses.activate
    def test_delete_agent_not_found(self, client, base_url):
        """Test deleting non-existent agent."""
        responses.add(
            responses.DELETE,
            f"{base_url}/agents/agent-999",
            json={"message": "Agent not found"},
            status=404
        )

        result = client.delete_agent("agent-999")
        assert result is False


class TestSystemOperations:
    """Test system operation methods."""

    @responses.activate
    def test_health_check(self, client, base_url):
        """Test health check."""
        responses.add(
            responses.GET,
            f"{base_url}/health",
            json={"status": "healthy", "version": "1.0.0"},
            status=200
        )

        health = client.health_check()
        assert health["status"] == "healthy"

    @responses.activate
    def test_get_metrics(self, client, base_url):
        """Test getting metrics."""
        responses.add(
            responses.GET,
            f"{base_url}/metrics",
            json={"executions_total": 100, "flows_total": 10},
            status=200
        )

        metrics = client.get_metrics()
        assert metrics["executions_total"] == 100

    @responses.activate
    def test_get_status(self, client, base_url):
        """Test getting status."""
        responses.add(
            responses.GET,
            f"{base_url}/status",
            json={"status": "operational", "uptime": 3600},
            status=200
        )

        status = client.get_status()
        assert status["status"] == "operational"


class TestUserAndCredits:
    """Test user and credits management."""

    @responses.activate
    def test_get_current_user(self, client, base_url):
        """Test getting current user info."""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/users/me",
            json={
                "id": "user-123",
                "email": "test@example.com",
                "credits": 1000,
                "plan": "pro"
            },
            status=200
        )

        user = client.get_current_user()
        assert user["id"] == "user-123"
        assert user["email"] == "test@example.com"
        assert user["credits"] == 1000
        assert user["plan"] == "pro"

    @responses.activate
    def test_check_credits(self, client, base_url):
        """Test checking credits."""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/users/me",
            json={
                "id": "user-123",
                "email": "test@example.com",
                "credits": 500,
                "plan": "basic"
            },
            status=200
        )

        credits = client.check_credits()
        assert credits == 500

    @responses.activate
    def test_check_credits_zero(self, client, base_url):
        """Test checking credits when user has none."""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/users/me",
            json={
                "id": "user-123",
                "email": "test@example.com",
                "plan": "basic"
                # No credits field
            },
            status=200
        )

        credits = client.check_credits()
        assert credits == 0


class TestAPIKeyManagement:
    """Test API key management methods."""

    @responses.activate
    def test_check_user_api_key_exists(self, client, base_url):
        """Test checking user API key when it exists."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/user/keys/my-key",
            json={
                "has_api_key": True,
                "api_key": "sk_user_test_key",
                "credits": 1000,
                "rate_limit": 100,
                "created_at": "2024-01-01T00:00:00Z",
                "last_used_at": "2024-01-02T00:00:00Z"
            },
            status=200
        )

        result = client.check_user_api_key(user_id)
        assert result["has_api_key"] is True
        assert result["api_key"] == "sk_user_test_key"
        assert result["credits"] == 1000
        assert result["rate_limit"] == 100
        assert result["created_at"] == "2024-01-01T00:00:00Z"
        assert result["last_used_at"] == "2024-01-02T00:00:00Z"

    @responses.activate
    def test_check_user_api_key_not_exists(self, client, base_url):
        """Test checking user API key when it doesn't exist."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/user/keys/my-key",
            json={
                "has_api_key": False,
                "api_key": None,
                "credits": 0,
                "rate_limit": 0,
                "created_at": None,
                "last_used_at": None
            },
            status=200
        )

        result = client.check_user_api_key(user_id)
        assert result["has_api_key"] is False
        assert result["api_key"] is None

    def test_check_user_api_key_invalid_user_id(self, client):
        """Test checking API key with invalid user ID."""
        with pytest.raises(ValidationError, match="User ID is required"):
            client.check_user_api_key("")

        with pytest.raises(ValidationError, match="User ID is required"):
            client.check_user_api_key(None)

    @responses.activate
    def test_generate_user_api_key_create(self, client, base_url):
        """Test generating API key for first time."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/user/keys/generate",
            json={
                "message": "API key created successfully",
                "api_key": "sk_new_user_key",
                "action": "created"
            },
            status=200
        )

        result = client.generate_user_api_key(user_id)
        assert result["message"] == "API key created successfully"
        assert result["api_key"] == "sk_new_user_key"
        assert result["action"] == "created"

    @responses.activate
    def test_generate_user_api_key_regenerate(self, client, base_url):
        """Test regenerating existing API key."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/user/keys/generate",
            json={
                "message": "API key regenerated successfully",
                "api_key": "sk_regenerated_key",
                "action": "regenerated"
            },
            status=200
        )

        result = client.generate_user_api_key(user_id)
        assert result["message"] == "API key regenerated successfully"
        assert result["api_key"] == "sk_regenerated_key"
        assert result["action"] == "regenerated"

    def test_generate_user_api_key_invalid_user_id(self, client):
        """Test generating API key with invalid user ID."""
        with pytest.raises(ValidationError, match="User ID is required"):
            client.generate_user_api_key("")

        with pytest.raises(ValidationError, match="User ID is required"):
            client.generate_user_api_key(None)

    @responses.activate
    def test_revoke_user_api_key_success(self, client, base_url):
        """Test revoking user API key."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        responses.add(
            responses.DELETE,
            f"{base_url}/api/v1/user/keys/revoke",
            json={
                "message": "API key revoked successfully",
                "status": "revoked"
            },
            status=200
        )

        result = client.revoke_user_api_key(user_id)
        assert result["message"] == "API key revoked successfully"
        assert result["status"] == "revoked"

    def test_revoke_user_api_key_invalid_user_id(self, client):
        """Test revoking API key with invalid user ID."""
        with pytest.raises(ValidationError, match="User ID is required"):
            client.revoke_user_api_key("")

        with pytest.raises(ValidationError, match="User ID is required"):
            client.revoke_user_api_key(None)


class TestErrorHandling:
    """Test error handling."""

    @responses.activate
    def test_authentication_error(self, client, base_url):
        """Test authentication error handling."""
        responses.add(
            responses.GET,
            f"{base_url}/flows",
            json={"message": "Invalid API key"},
            status=401
        )

        with pytest.raises(AuthenticationError) as exc_info:
            client.list_flows()
        assert "Invalid API key" in str(exc_info.value)
        assert "https://ai-spine.com/dashboard" in str(exc_info.value)

    @responses.activate
    def test_validation_error(self, client, base_url):
        """Test validation error from API."""
        responses.add(
            responses.POST,
            f"{base_url}/flows/execute",
            json={"message": "Invalid input data"},
            status=400
        )

        with pytest.raises(ValidationError) as exc_info:
            client.execute_flow("test-flow", {"invalid": "data"})
        assert "Invalid input data" in str(exc_info.value)

    @responses.activate
    def test_insufficient_credits_error(self, client, base_url):
        """Test insufficient credits error handling."""
        responses.add(
            responses.POST,
            f"{base_url}/flows/execute",
            json={
                "message": "No credits remaining",
                "error_code": "INSUFFICIENT_CREDITS",
                "credits_needed": 10,
                "credits_available": 0
            },
            status=403
        )

        with pytest.raises(InsufficientCreditsError) as exc_info:
            client.execute_flow("test-flow", {"data": "test"})
        assert "No credits remaining" in str(exc_info.value)
        assert "https://ai-spine.com/billing" in str(exc_info.value)
        assert exc_info.value.credits_needed == 10
        assert exc_info.value.credits_available == 0

    @responses.activate
    def test_rate_limit_error(self, client, base_url):
        """Test rate limit error handling."""
        responses.add(
            responses.GET,
            f"{base_url}/flows",
            json={"message": "Rate limit exceeded"},
            headers={"Retry-After": "60"},
            status=429
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.list_flows()
        assert "Rate limit exceeded" in str(exc_info.value)
        assert exc_info.value.retry_after == 60

    @responses.activate
    def test_server_error(self, client, base_url):
        """Test server error handling."""
        responses.add(
            responses.GET,
            f"{base_url}/flows",
            json={"message": "Internal server error"},
            status=500
        )

        with pytest.raises(APIError) as exc_info:
            client.list_flows()
        assert exc_info.value.status_code == 500
