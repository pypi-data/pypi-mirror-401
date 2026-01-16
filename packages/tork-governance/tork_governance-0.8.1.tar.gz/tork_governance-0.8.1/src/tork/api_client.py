"""
Tork Admin API Client

Client for fetching governance configuration from the Tork Admin API.
Enables dynamic configuration management instead of static YAML files.
"""

from typing import Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import httpx
import structlog

logger = structlog.get_logger(__name__)

# Default Admin API URL
DEFAULT_API_URL = "https://tork.network"


@dataclass
class HITLConfig:
    """Human-in-the-Loop configuration."""
    enabled: bool = True
    approval_timeout_minutes: int = 30
    escalation_timeout_minutes: int = 15
    max_approvals_per_minute: int = 5
    cooldown_minutes: int = 15
    velocity_window_minutes: int = 10
    velocity_threshold_count: int = 10
    velocity_threshold_amount: float = 10000.0
    require_reason_for_approval: bool = False
    require_reason_for_rejection: bool = True
    auto_expire_pending: bool = True


@dataclass
class Tool:
    """Tool registration from Admin API."""
    id: str
    name: str
    description: Optional[str] = None
    max_calls_per_minute: int = 60
    blocked_flags: list[str] = field(default_factory=list)
    allowed_agents: list[str] = field(default_factory=list)
    allowed_targets: list[str] = field(default_factory=list)
    requires_hitl: bool = False
    is_blocked: bool = False


@dataclass
class Policy:
    """Governance policy from Admin API."""
    id: str
    name: str
    description: Optional[str] = None
    yaml_content: str = ""
    is_active: bool = True
    priority: int = 0


@dataclass
class PIIRule:
    """PII detection rule from Admin API."""
    pii_type: str
    enabled: bool = True
    action: str = "redact"  # redact, block, warn, log
    custom_pattern: Optional[str] = None


@dataclass
class Approval:
    """Approval request/response."""
    approval_id: str
    agent_id: str
    tool_name: str
    target: str
    parameters: dict[str, Any]
    status: str = "pending"  # pending, approved, rejected, expired
    requested_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_reason: Optional[str] = None


@dataclass
class ApprovalStatus:
    """Approval status check result."""
    found: bool
    approval_id: str
    status: str
    is_expired: bool = False
    agent_id: Optional[str] = None
    tool_name: Optional[str] = None
    target: Optional[str] = None


@dataclass
class GovernanceCheckResult:
    """Result of a real-time governance check."""
    allowed: bool
    reason: str
    checks_performed: list[str]
    requires_hitl: bool = False
    policy_matched: Optional[str] = None
    warnings: list[str] = field(default_factory=list)


@dataclass
class Webhook:
    """Webhook configuration."""
    id: str
    name: str
    url: str
    event_types: list[str] = field(default_factory=list)
    is_active: bool = True
    created_at: Optional[str] = None


class ConfigCache:
    """Simple TTL cache for API configuration."""

    def __init__(self, ttl_seconds: int = 60):
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
        value, expires_at = self._cache[key]
        if datetime.utcnow() > expires_at:
            del self._cache[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with TTL."""
        expires_at = datetime.utcnow() + timedelta(seconds=self.ttl_seconds)
        self._cache[key] = (value, expires_at)

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()


class TorkAPIClient:
    """
    Client for the Tork Admin API.

    Fetches governance configuration dynamically from the Admin API.
    Includes caching to reduce API calls and improve performance.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_API_URL,
        cache_ttl_seconds: int = 60,
        timeout_seconds: float = 10.0,
    ):
        """
        Initialize the API client.

        Args:
            api_key: Tork API key for authentication.
            base_url: Base URL of the Admin API.
            cache_ttl_seconds: TTL for cached configuration (default: 60s).
            timeout_seconds: HTTP request timeout.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_seconds
        self._cache = ConfigCache(ttl_seconds=cache_ttl_seconds)
        self._client: Optional[httpx.Client] = None

        logger.info(
            "TorkAPIClient initialized",
            base_url=self.base_url,
            cache_ttl=cache_ttl_seconds,
        )

    @property
    def client(self) -> httpx.Client:
        """Lazy initialization of HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "tork-python-sdk/0.8.1",
                },
                timeout=self.timeout,
            )
        return self._client

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> "TorkAPIClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make an API request."""
        try:
            response = self.client.request(
                method=method,
                url=path,
                json=json,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "API request failed",
                method=method,
                path=path,
                status_code=e.response.status_code,
                error=str(e),
            )
            raise
        except httpx.RequestError as e:
            logger.error(
                "API request error",
                method=method,
                path=path,
                error=str(e),
            )
            raise

    # =========================================================================
    # HITL Configuration
    # =========================================================================

    def fetch_hitl_config(self) -> HITLConfig:
        """
        Fetch HITL configuration from the Admin API.

        Returns:
            HITLConfig object with current settings.
        """
        cache_key = "hitl_config"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            data = self._request("GET", "/api/hitl/config")
            config = HITLConfig(
                enabled=data.get("enabled", True),
                approval_timeout_minutes=data.get("approval_timeout_minutes", 30),
                escalation_timeout_minutes=data.get("escalation_timeout_minutes", 15),
                max_approvals_per_minute=data.get("max_approvals_per_minute", 5),
                cooldown_minutes=data.get("cooldown_minutes", 15),
                velocity_window_minutes=data.get("velocity_window_minutes", 10),
                velocity_threshold_count=data.get("velocity_threshold_count", 10),
                velocity_threshold_amount=data.get("velocity_threshold_amount", 10000.0),
                require_reason_for_approval=data.get("require_reason_for_approval", False),
                require_reason_for_rejection=data.get("require_reason_for_rejection", True),
                auto_expire_pending=data.get("auto_expire_pending", True),
            )
            self._cache.set(cache_key, config)
            logger.debug("Fetched HITL config from API", config=config)
            return config
        except Exception as e:
            logger.warning("Failed to fetch HITL config, using defaults", error=str(e))
            return HITLConfig()

    # =========================================================================
    # Tools
    # =========================================================================

    def fetch_tools(self) -> list[Tool]:
        """
        Fetch registered tools from the Admin API.

        Returns:
            List of Tool objects.
        """
        cache_key = "tools"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            data = self._request("GET", "/api/tools")
            tools = [
                Tool(
                    id=t["id"],
                    name=t["name"],
                    description=t.get("description"),
                    max_calls_per_minute=t.get("max_calls_per_minute", 60),
                    blocked_flags=t.get("blocked_flags", []),
                    allowed_agents=t.get("allowed_agents", []),
                    allowed_targets=t.get("allowed_targets", []),
                    requires_hitl=t.get("requires_hitl", False),
                    is_blocked=t.get("is_blocked", False),
                )
                for t in data
            ]
            self._cache.set(cache_key, tools)
            logger.debug("Fetched tools from API", count=len(tools))
            return tools
        except Exception as e:
            logger.warning("Failed to fetch tools, returning empty list", error=str(e))
            return []

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a specific tool by name."""
        tools = self.fetch_tools()
        for tool in tools:
            if tool.name == tool_name:
                return tool
        return None

    # =========================================================================
    # Policies
    # =========================================================================

    def fetch_policies(self) -> list[Policy]:
        """
        Fetch governance policies from the Admin API.

        Returns:
            List of active Policy objects, sorted by priority.
        """
        cache_key = "policies"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            data = self._request("GET", "/api/policies")
            policies = [
                Policy(
                    id=p["id"],
                    name=p["name"],
                    description=p.get("description"),
                    yaml_content=p.get("yaml_content", ""),
                    is_active=p.get("is_active", True),
                    priority=p.get("priority", 0),
                )
                for p in data
                if p.get("is_active", True)
            ]
            # Sort by priority (higher first)
            policies.sort(key=lambda p: p.priority, reverse=True)
            self._cache.set(cache_key, policies)
            logger.debug("Fetched policies from API", count=len(policies))
            return policies
        except Exception as e:
            logger.warning("Failed to fetch policies, returning empty list", error=str(e))
            return []

    # =========================================================================
    # PII Rules
    # =========================================================================

    def fetch_pii_rules(self) -> list[PIIRule]:
        """
        Fetch PII detection rules from the Admin API.

        Returns:
            List of enabled PIIRule objects.
        """
        cache_key = "pii_rules"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            data = self._request("GET", "/api/pii-rules")
            rules = [
                PIIRule(
                    pii_type=r["pii_type"],
                    enabled=r.get("enabled", True),
                    action=r.get("action", "redact"),
                    custom_pattern=r.get("custom_pattern"),
                )
                for r in data
                if r.get("enabled", True)
            ]
            self._cache.set(cache_key, rules)
            logger.debug("Fetched PII rules from API", count=len(rules))
            return rules
        except Exception as e:
            logger.warning("Failed to fetch PII rules, returning defaults", error=str(e))
            # Return default PII rules
            return [
                PIIRule(pii_type="email"),
                PIIRule(pii_type="phone"),
                PIIRule(pii_type="ssn"),
                PIIRule(pii_type="credit_card"),
                PIIRule(pii_type="api_key"),
            ]

    # =========================================================================
    # Approvals
    # =========================================================================

    def submit_approval(
        self,
        agent_id: str,
        tool_name: str,
        target: str,
        parameters: dict[str, Any],
        amount: Optional[float] = None,
    ) -> Approval:
        """
        Submit an action for human approval.

        Args:
            agent_id: ID of the agent requesting approval.
            tool_name: Name of the tool requiring approval.
            target: Target resource or environment.
            parameters: Parameters for the action.
            amount: Optional monetary amount for velocity tracking.

        Returns:
            Approval object with approval_id and status.
        """
        payload = {
            "agent_id": agent_id,
            "tool_name": tool_name,
            "target": target,
            "parameters": parameters,
        }
        if amount is not None:
            payload["amount"] = amount

        data = self._request("POST", "/api/approvals", json=payload)

        approval = Approval(
            approval_id=data["approval_id"],
            agent_id=agent_id,
            tool_name=tool_name,
            target=target,
            parameters=parameters,
            status=data.get("status", "pending"),
            requested_at=datetime.utcnow(),
            expires_at=datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
            if data.get("expires_at") else None,
        )

        logger.info(
            "Approval submitted",
            approval_id=approval.approval_id,
            tool_name=tool_name,
            agent_id=agent_id,
        )

        return approval

    def check_approval(self, approval_id: str) -> ApprovalStatus:
        """
        Check the status of an approval request.

        Args:
            approval_id: ID of the approval to check.

        Returns:
            ApprovalStatus with current status information.
        """
        try:
            data = self._request("GET", f"/api/approvals/{approval_id}")
            return ApprovalStatus(
                found=data.get("found", True),
                approval_id=approval_id,
                status=data.get("status", "pending"),
                is_expired=data.get("is_expired", False),
                agent_id=data.get("agent_id"),
                tool_name=data.get("tool_name"),
                target=data.get("target"),
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return ApprovalStatus(
                    found=False,
                    approval_id=approval_id,
                    status="not_found",
                )
            raise

    # =========================================================================
    # Audit Logging
    # =========================================================================

    def log_audit(
        self,
        action: str,
        agent_id: Optional[str] = None,
        tool_name: Optional[str] = None,
        target: Optional[str] = None,
        result: Optional[str] = None,
        governance_score: Optional[float] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Log an audit event to the Admin API.

        Args:
            action: Type of action (e.g., "tool_call", "policy_check").
            agent_id: ID of the agent involved.
            tool_name: Name of the tool involved.
            target: Target resource or environment.
            result: Result of the action (e.g., "allowed", "blocked").
            governance_score: Governance score for the action.
            details: Additional details as JSON.
        """
        payload = {
            "action": action,
            "agent_id": agent_id,
            "tool_name": tool_name,
            "target": target,
            "result": result,
            "governance_score": governance_score,
            "details": details,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            self._request("POST", "/api/audit-logs", json=payload)
            logger.debug("Audit log submitted", action=action, result=result)
        except Exception as e:
            # Don't fail on audit log errors
            logger.warning("Failed to submit audit log", error=str(e))

    # =========================================================================
    # Governance Check
    # =========================================================================

    def check_governance(
        self,
        agent_id: str,
        tool_name: str,
        target: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None,
    ) -> GovernanceCheckResult:
        """
        Perform a real-time governance check for a tool call.

        Validates the tool call against all configured governance policies
        including tool registry, agent authorization, target restrictions,
        blocked flags, HITL requirements, and policy rules.

        Args:
            agent_id: ID of the agent making the request.
            tool_name: Name of the tool to be called.
            target: Optional target resource or environment.
            parameters: Optional parameters for the tool call.

        Returns:
            GovernanceCheckResult with allowed status and details.
        """
        payload: dict[str, Any] = {
            "agent_id": agent_id,
            "tool_name": tool_name,
        }
        if target:
            payload["target"] = target
        if parameters:
            payload["parameters"] = parameters

        try:
            data = self._request("POST", "/api/v1/governance/check", json=payload)

            return GovernanceCheckResult(
                allowed=data.get("allowed", False),
                reason=data.get("reason", ""),
                checks_performed=data.get("checks_performed", []),
                requires_hitl=data.get("requires_hitl", False),
                policy_matched=data.get("policy_matched"),
                warnings=data.get("warnings", []),
            )
        except Exception as e:
            logger.error("Governance check failed", error=str(e))
            # Fail closed - deny on error
            return GovernanceCheckResult(
                allowed=False,
                reason=f"Governance check failed: {str(e)}",
                checks_performed=["error"],
            )

    # =========================================================================
    # Webhooks
    # =========================================================================

    def list_webhooks(self) -> list[Webhook]:
        """
        List all webhooks configured for the organization.

        Returns:
            List of Webhook objects.
        """
        try:
            data = self._request("GET", "/api/v1/webhooks")
            return [
                Webhook(
                    id=w["id"],
                    name=w["name"],
                    url=w["url"],
                    event_types=w.get("event_types", []),
                    is_active=w.get("is_active", True),
                    created_at=w.get("created_at"),
                )
                for w in data
            ]
        except Exception as e:
            logger.warning("Failed to list webhooks", error=str(e))
            return []

    def create_webhook(
        self,
        name: str,
        url: str,
        event_types: Optional[list[str]] = None,
    ) -> Webhook:
        """
        Create a new webhook for HITL notifications.

        Args:
            name: Display name for the webhook.
            url: Target URL to receive webhook events.
            event_types: List of event types to subscribe to.
                        Default: ["approval_requested", "approval_approved", "approval_rejected"]

        Returns:
            Created Webhook object with secret.
        """
        payload: dict[str, Any] = {
            "name": name,
            "url": url,
        }
        if event_types:
            payload["event_types"] = event_types

        data = self._request("POST", "/api/v1/webhooks", json=payload)

        logger.info("Webhook created", name=name, id=data.get("id"))

        return Webhook(
            id=data["id"],
            name=name,
            url=url,
            event_types=event_types or ["approval_requested", "approval_approved", "approval_rejected"],
            is_active=True,
            created_at=data.get("created_at"),
        )

    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook by ID.

        Args:
            webhook_id: The ID of the webhook to delete.

        Returns:
            True if successfully deleted, False otherwise.
        """
        try:
            self._request("DELETE", f"/api/v1/webhooks/{webhook_id}")
            logger.info("Webhook deleted", webhook_id=webhook_id)
            return True
        except Exception as e:
            logger.warning("Failed to delete webhook", webhook_id=webhook_id, error=str(e))
            return False

    # =========================================================================
    # Cache Management
    # =========================================================================

    def refresh_cache(self) -> None:
        """Force refresh all cached configuration."""
        self._cache.clear()
        logger.info("Configuration cache cleared")

    def prefetch_config(self) -> None:
        """
        Prefetch all configuration to populate cache.

        Call this on startup to avoid cold cache misses.
        """
        try:
            self.fetch_hitl_config()
            self.fetch_tools()
            self.fetch_policies()
            self.fetch_pii_rules()
            logger.info("Configuration prefetched successfully")
        except Exception as e:
            logger.warning("Failed to prefetch configuration", error=str(e))


# Convenience function to create client
def create_api_client(
    api_key: str,
    base_url: str = DEFAULT_API_URL,
    cache_ttl_seconds: int = 60,
) -> TorkAPIClient:
    """
    Create a Tork Admin API client.

    Args:
        api_key: Tork API key for authentication.
        base_url: Base URL of the Admin API.
        cache_ttl_seconds: TTL for cached configuration.

    Returns:
        Configured TorkAPIClient instance.
    """
    return TorkAPIClient(
        api_key=api_key,
        base_url=base_url,
        cache_ttl_seconds=cache_ttl_seconds,
    )
