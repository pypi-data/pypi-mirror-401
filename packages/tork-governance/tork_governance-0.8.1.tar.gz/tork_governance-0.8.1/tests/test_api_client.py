"""
Tests for the Tork Admin API client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import httpx

from tork.api_client import (
    TorkAPIClient,
    ConfigCache,
    HITLConfig,
    Tool,
    Policy,
    PIIRule,
    Approval,
    ApprovalStatus,
    create_api_client,
)


class TestConfigCache:
    """Tests for the ConfigCache class."""

    def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = ConfigCache(ttl_seconds=60)
        cache.set("key1", {"data": "value1"})

        result = cache.get("key1")
        assert result == {"data": "value1"}

    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        cache = ConfigCache(ttl_seconds=60)
        result = cache.get("nonexistent")
        assert result is None

    def test_expired_entry(self):
        """Test that expired entries return None."""
        cache = ConfigCache(ttl_seconds=1)
        cache.set("key1", "value1")

        # Manually expire the entry
        cache._cache["key1"] = ("value1", datetime.utcnow() - timedelta(seconds=10))

        result = cache.get("key1")
        assert result is None

    def test_clear(self):
        """Test clearing the cache."""
        cache = ConfigCache(ttl_seconds=60)
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestTorkAPIClient:
    """Tests for the TorkAPIClient class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        with patch.object(TorkAPIClient, "client", new_callable=lambda: MagicMock()):
            client = TorkAPIClient(api_key="test-api-key")
            yield client
            client.close()

    def test_init(self):
        """Test client initialization."""
        client = TorkAPIClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            cache_ttl_seconds=120,
        )

        assert client.api_key == "test-key"
        assert client.base_url == "https://custom.api.com"
        assert client._cache.ttl_seconds == 120
        client.close()

    def test_fetch_hitl_config_success(self):
        """Test successful HITL config fetch."""
        client = TorkAPIClient(api_key="test-key")

        mock_response = Mock()
        mock_response.json.return_value = {
            "enabled": True,
            "approval_timeout_minutes": 45,
            "max_approvals_per_minute": 10,
            "cooldown_minutes": 20,
        }
        mock_response.raise_for_status = Mock()

        with patch.object(client, "_request", return_value=mock_response.json()):
            config = client.fetch_hitl_config()

            assert isinstance(config, HITLConfig)
            assert config.enabled is True
            assert config.approval_timeout_minutes == 45
            assert config.max_approvals_per_minute == 10
            assert config.cooldown_minutes == 20

        client.close()

    def test_fetch_hitl_config_uses_cache(self):
        """Test that HITL config is cached."""
        client = TorkAPIClient(api_key="test-key", cache_ttl_seconds=60)

        # Manually set cache
        cached_config = HITLConfig(enabled=False, approval_timeout_minutes=99)
        client._cache.set("hitl_config", cached_config)

        # Should return cached value without making API call
        with patch.object(client, "_request") as mock_request:
            config = client.fetch_hitl_config()

            assert config.enabled is False
            assert config.approval_timeout_minutes == 99
            mock_request.assert_not_called()

        client.close()

    def test_fetch_hitl_config_fallback_on_error(self):
        """Test fallback to defaults when API fails."""
        client = TorkAPIClient(api_key="test-key")

        with patch.object(client, "_request", side_effect=Exception("API Error")):
            config = client.fetch_hitl_config()

            # Should return default config
            assert isinstance(config, HITLConfig)
            assert config.enabled is True

        client.close()

    def test_fetch_tools_success(self):
        """Test successful tools fetch."""
        client = TorkAPIClient(api_key="test-key")

        mock_data = [
            {
                "id": "tool-1",
                "name": "file_read",
                "max_calls_per_minute": 30,
                "blocked_flags": ["--force"],
                "requires_hitl": True,
            },
            {
                "id": "tool-2",
                "name": "file_write",
                "max_calls_per_minute": 10,
                "allowed_agents": ["agent-1"],
            },
        ]

        with patch.object(client, "_request", return_value=mock_data):
            tools = client.fetch_tools()

            assert len(tools) == 2
            assert tools[0].name == "file_read"
            assert tools[0].max_calls_per_minute == 30
            assert tools[0].blocked_flags == ["--force"]
            assert tools[0].requires_hitl is True
            assert tools[1].name == "file_write"
            assert tools[1].allowed_agents == ["agent-1"]

        client.close()

    def test_get_tool(self):
        """Test getting a specific tool by name."""
        client = TorkAPIClient(api_key="test-key")

        mock_data = [
            {"id": "1", "name": "tool_a"},
            {"id": "2", "name": "tool_b"},
        ]

        with patch.object(client, "_request", return_value=mock_data):
            tool = client.get_tool("tool_b")
            assert tool is not None
            assert tool.name == "tool_b"

            missing = client.get_tool("nonexistent")
            assert missing is None

        client.close()

    def test_fetch_policies_success(self):
        """Test successful policies fetch."""
        client = TorkAPIClient(api_key="test-key")

        mock_data = [
            {
                "id": "policy-1",
                "name": "security-policy",
                "yaml_content": "policies:\n  - name: test",
                "is_active": True,
                "priority": 10,
            },
            {
                "id": "policy-2",
                "name": "inactive-policy",
                "is_active": False,
                "priority": 5,
            },
            {
                "id": "policy-3",
                "name": "low-priority",
                "is_active": True,
                "priority": 1,
            },
        ]

        with patch.object(client, "_request", return_value=mock_data):
            policies = client.fetch_policies()

            # Should only return active policies, sorted by priority
            assert len(policies) == 2
            assert policies[0].name == "security-policy"  # priority 10
            assert policies[1].name == "low-priority"  # priority 1

        client.close()

    def test_fetch_pii_rules_success(self):
        """Test successful PII rules fetch."""
        client = TorkAPIClient(api_key="test-key")

        mock_data = [
            {"pii_type": "email", "enabled": True, "action": "redact"},
            {"pii_type": "phone", "enabled": True, "action": "block"},
            {"pii_type": "ssn", "enabled": False, "action": "redact"},
        ]

        with patch.object(client, "_request", return_value=mock_data):
            rules = client.fetch_pii_rules()

            # Should only return enabled rules
            assert len(rules) == 2
            assert rules[0].pii_type == "email"
            assert rules[0].action == "redact"
            assert rules[1].pii_type == "phone"
            assert rules[1].action == "block"

        client.close()

    def test_fetch_pii_rules_fallback(self):
        """Test fallback to default PII rules on error."""
        client = TorkAPIClient(api_key="test-key")

        with patch.object(client, "_request", side_effect=Exception("API Error")):
            rules = client.fetch_pii_rules()

            # Should return default rules
            assert len(rules) == 5
            pii_types = [r.pii_type for r in rules]
            assert "email" in pii_types
            assert "phone" in pii_types
            assert "ssn" in pii_types

        client.close()

    def test_submit_approval(self):
        """Test submitting an approval request."""
        client = TorkAPIClient(api_key="test-key")

        mock_response = {
            "approval_id": "approval-123",
            "status": "pending",
            "expires_at": "2025-01-15T12:00:00Z",
        }

        with patch.object(client, "_request", return_value=mock_response):
            approval = client.submit_approval(
                agent_id="agent-1",
                tool_name="file_write",
                target="production",
                parameters={"path": "/etc/config"},
                amount=1000.0,
            )

            assert approval.approval_id == "approval-123"
            assert approval.status == "pending"
            assert approval.agent_id == "agent-1"
            assert approval.tool_name == "file_write"
            assert approval.target == "production"

        client.close()

    def test_check_approval_found(self):
        """Test checking an existing approval."""
        client = TorkAPIClient(api_key="test-key")

        mock_response = {
            "found": True,
            "status": "approved",
            "is_expired": False,
            "agent_id": "agent-1",
            "tool_name": "file_write",
            "target": "production",
        }

        with patch.object(client, "_request", return_value=mock_response):
            status = client.check_approval("approval-123")

            assert status.found is True
            assert status.status == "approved"
            assert status.is_expired is False
            assert status.agent_id == "agent-1"

        client.close()

    def test_check_approval_not_found(self):
        """Test checking a non-existent approval."""
        client = TorkAPIClient(api_key="test-key")

        mock_error = httpx.HTTPStatusError(
            "Not Found",
            request=Mock(),
            response=Mock(status_code=404),
        )

        with patch.object(client, "_request", side_effect=mock_error):
            status = client.check_approval("nonexistent")

            assert status.found is False
            assert status.status == "not_found"

        client.close()

    def test_log_audit(self):
        """Test logging an audit event."""
        client = TorkAPIClient(api_key="test-key")

        with patch.object(client, "_request") as mock_request:
            # Should not raise even on success
            client.log_audit(
                action="tool_call",
                agent_id="agent-1",
                tool_name="file_read",
                result="allowed",
                governance_score=85.5,
            )

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/api/audit-logs"

        client.close()

    def test_log_audit_handles_error(self):
        """Test that audit logging doesn't raise on error."""
        client = TorkAPIClient(api_key="test-key")

        with patch.object(client, "_request", side_effect=Exception("API Error")):
            # Should not raise
            client.log_audit(action="test")

        client.close()

    def test_refresh_cache(self):
        """Test refreshing the cache."""
        client = TorkAPIClient(api_key="test-key")

        # Set some cached values
        client._cache.set("hitl_config", HITLConfig())
        client._cache.set("tools", [])

        client.refresh_cache()

        assert client._cache.get("hitl_config") is None
        assert client._cache.get("tools") is None

        client.close()

    def test_prefetch_config(self):
        """Test prefetching all config."""
        client = TorkAPIClient(api_key="test-key")

        with patch.object(client, "fetch_hitl_config") as mock_hitl, \
             patch.object(client, "fetch_tools") as mock_tools, \
             patch.object(client, "fetch_policies") as mock_policies, \
             patch.object(client, "fetch_pii_rules") as mock_pii:

            client.prefetch_config()

            mock_hitl.assert_called_once()
            mock_tools.assert_called_once()
            mock_policies.assert_called_once()
            mock_pii.assert_called_once()

        client.close()

    def test_context_manager(self):
        """Test using client as context manager."""
        with TorkAPIClient(api_key="test-key") as client:
            assert client.api_key == "test-key"

        # Client should be closed after exiting context
        assert client._client is None


class TestCreateApiClient:
    """Tests for the create_api_client helper function."""

    def test_create_with_defaults(self):
        """Test creating client with default values."""
        client = create_api_client(api_key="test-key")

        assert client.api_key == "test-key"
        assert client.base_url == "https://tork.network"
        assert client._cache.ttl_seconds == 60

        client.close()

    def test_create_with_custom_values(self):
        """Test creating client with custom values."""
        client = create_api_client(
            api_key="custom-key",
            base_url="https://custom.api.com",
            cache_ttl_seconds=300,
        )

        assert client.api_key == "custom-key"
        assert client.base_url == "https://custom.api.com"
        assert client._cache.ttl_seconds == 300

        client.close()


class TestDataClasses:
    """Tests for the data classes."""

    def test_hitl_config_defaults(self):
        """Test HITLConfig default values."""
        config = HITLConfig()

        assert config.enabled is True
        assert config.approval_timeout_minutes == 30
        assert config.max_approvals_per_minute == 5
        assert config.cooldown_minutes == 15

    def test_tool_defaults(self):
        """Test Tool default values."""
        tool = Tool(id="1", name="test_tool")

        assert tool.max_calls_per_minute == 60
        assert tool.blocked_flags == []
        assert tool.requires_hitl is False
        assert tool.is_blocked is False

    def test_pii_rule_defaults(self):
        """Test PIIRule default values."""
        rule = PIIRule(pii_type="email")

        assert rule.enabled is True
        assert rule.action == "redact"
        assert rule.custom_pattern is None

    def test_approval_status_defaults(self):
        """Test ApprovalStatus defaults."""
        status = ApprovalStatus(
            found=True,
            approval_id="test-123",
            status="pending",
        )

        assert status.is_expired is False
        assert status.agent_id is None
