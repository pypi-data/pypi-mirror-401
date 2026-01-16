import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from tork.adapters.autogen.middleware import TorkAutoGenMiddleware
from tork.adapters.autogen.governed import GovernedAutoGenAgent, GovernedGroupChat, TorkGovernedAssistant
from tork.adapters.autogen.exceptions import MessageBlockedError, ResponseBlockedError
from tork.core.engine import GovernanceEngine
from tork.core.models import EvaluationResult, PolicyDecision

class MockAgent:
    def __init__(self, name="TestAgent"):
        self.name = name
    def receive(self, message, sender, request_reply=None):
        return "received"
    def generate_reply(self, messages=None, sender=None, **kwargs):
        return "I am an AI assistant."

def test_middleware_init():
    mw = TorkAutoGenMiddleware(agent_id="test-autogen")
    assert mw.agent_id == "test-autogen"
    assert isinstance(mw.engine, GovernanceEngine)

def test_wrap_agent():
    mw = TorkAutoGenMiddleware()
    agent = MockAgent()
    governed = mw.wrap_agent(agent)
    assert isinstance(governed, GovernedAutoGenAgent)
    assert governed.name == "TestAgent"

def test_process_message_allowed():
    mw = TorkAutoGenMiddleware()
    msg = "Hello"
    res = mw.process_message(msg)
    assert res == "Hello"

def test_process_message_blocked():
    engine = GovernanceEngine()
    mock_res = EvaluationResult(
        decision=PolicyDecision.DENY,
        reason="Blocked",
        violations=["Blocked content"],
        original_payload={"content": "bad"},
        modified_payload=None,
        pii_found=[],
        timestamp=datetime.now(timezone.utc)
    )
    engine.evaluate = MagicMock(return_value=mock_res)
    mw = TorkAutoGenMiddleware(engine=engine)
    with pytest.raises(MessageBlockedError):
        mw.process_message("bad")

def test_process_response_allowed():
    mw = TorkAutoGenMiddleware()
    res = mw.process_response("Clean response")
    assert res == "Clean response"

def test_governed_agent_receive():
    mw = TorkAutoGenMiddleware()
    agent = MockAgent()
    governed = GovernedAutoGenAgent(agent, mw)
    res = governed.receive("Hello", sender="User")
    assert res == "received"

def test_governed_agent_generate_reply():
    mw = TorkAutoGenMiddleware()
    agent = MockAgent()
    governed = GovernedAutoGenAgent(agent, mw)
    res = governed.generate_reply(messages=[{"content": "hi"}])
    assert res == "I am an AI assistant."

def test_governed_group_chat():
    mw = TorkAutoGenMiddleware()
    agents = [MockAgent("A1"), MockAgent("A2")]
    group = GovernedGroupChat(agents, mw)
    assert len(group.agents) == 2
    assert isinstance(group.agents[0], GovernedAutoGenAgent)

def test_pii_redaction_in_message():
    mw = TorkAutoGenMiddleware()
    # PII in message should be handled by default engine if configured
    # Here we just verify the flow doesn't crash
    msg = "My email is test@example.com"
    res = mw.process_message(msg)
    assert isinstance(res, str)

def test_compliance_receipt_on_response():
    mw = TorkAutoGenMiddleware()
    # Use a real or mock engine that allows
    res = mw.process_response("Response text")
    # Receipt generation happens inside process_response
    assert res == "Response text"


class TestTorkGovernedAssistant:
    """Tests for TorkGovernedAssistant class."""

    def test_initialization_with_engine(self):
        """Test initialization with GovernanceEngine."""
        assistant = MockAgent("TestAssistant")
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(
            assistant=assistant,
            engine=engine,
            agent_id="assistant-agent",
        )

        assert governed._assistant == assistant
        assert governed.engine == engine
        assert governed.agent_id == "assistant-agent"
        assert governed.name == "TestAssistant"

    def test_initialization_requires_engine_or_api_key(self):
        """Test that either engine or api_key is required."""
        assistant = MockAgent()

        with pytest.raises(ValueError, match="Either engine or api_key must be provided"):
            TorkGovernedAssistant(assistant=assistant)

    def test_intercept_message_allowed(self):
        """Test intercepting message with ALLOW decision."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)
        result = governed.intercept_message("Hello, how are you?")

        assert result == "Hello, how are you?"

    def test_intercept_message_blocked(self):
        """Test intercepting message with DENY decision."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        mock_res = EvaluationResult(
            decision=PolicyDecision.DENY,
            reason="Message blocked",
            violations=["Blocked content"],
            original_payload={"content": "blocked"},
            modified_payload=None,
            pii_found=[],
            timestamp=datetime.now(timezone.utc)
        )
        engine.evaluate = MagicMock(return_value=mock_res)

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)

        with pytest.raises(MessageBlockedError):
            governed.intercept_message("blocked content")

    def test_validate_tool_call_allowed(self):
        """Test validating tool call with ALLOW decision."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)
        args = governed.validate_tool_call("search", {"query": "test"})

        assert args == {"query": "test"}

    def test_validate_tool_call_blocked(self):
        """Test validating tool call with DENY decision."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        mock_res = EvaluationResult(
            decision=PolicyDecision.DENY,
            reason="Tool call blocked",
            violations=["Blocked tool"],
            original_payload={},
            modified_payload=None,
            pii_found=[],
            timestamp=datetime.now(timezone.utc)
        )
        engine.evaluate = MagicMock(return_value=mock_res)

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)

        with pytest.raises(MessageBlockedError):
            governed.validate_tool_call("dangerous_tool", {})

    def test_receive_with_governance(self):
        """Test receiving message with governance checks."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)
        result = governed.receive("Hello", sender=MockAgent("Sender"))

        assert result == "received"

    def test_generate_reply_with_governance(self):
        """Test generating reply with governance checks."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)
        result = governed.generate_reply(messages=[{"content": "hi"}])

        assert result == "I am an AI assistant."

    def test_generate_reply_blocked(self):
        """Test generating reply with DENY on output."""
        assistant = MockAgent()
        engine = GovernanceEngine()

        # First call allows (for input), second denies (for output)
        allow_res = EvaluationResult(
            decision=PolicyDecision.ALLOW,
            reason="Allowed",
            violations=[],
            original_payload={},
            modified_payload=None,
            pii_found=[],
            timestamp=datetime.now(timezone.utc)
        )
        deny_res = EvaluationResult(
            decision=PolicyDecision.DENY,
            reason="Reply blocked",
            violations=["Blocked output"],
            original_payload={},
            modified_payload=None,
            pii_found=[],
            timestamp=datetime.now(timezone.utc)
        )
        engine.evaluate = MagicMock(side_effect=[allow_res, deny_res])

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)

        with pytest.raises(ResponseBlockedError):
            governed.generate_reply(messages=[{"content": "hi"}])

    def test_getattr_proxy(self):
        """Test that attributes are proxied to wrapped assistant."""
        assistant = MockAgent()
        assistant.custom_attr = "custom_value"
        engine = GovernanceEngine()

        governed = TorkGovernedAssistant(assistant=assistant, engine=engine)

        assert governed.custom_attr == "custom_value"
