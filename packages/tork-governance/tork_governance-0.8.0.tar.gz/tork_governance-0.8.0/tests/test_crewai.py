import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from tork.adapters.crewai.middleware import TorkCrewAIMiddleware
from tork.adapters.crewai.governed import GovernedAgent, GovernedCrew, TorkGovernedTask
from tork.adapters.crewai.exceptions import GovernanceBlockedError, PIIDetectedError
from tork.core.engine import GovernanceEngine
from tork.core.models import EvaluationResult, PolicyDecision

class MockTask:
    def __init__(self, description):
        self.description = description

class MockAgent:
    def __init__(self, name="Test Agent"):
        self.name = name
        self.agents = [] # for crew compatibility
    def execute_task(self, task, context=None):
        return f"Result for {task.description}"

class MockCrew:
    def __init__(self, agents):
        self.agents = agents
    def kickoff(self, inputs=None):
        return "Crew result"

def test_middleware_init():
    mw = TorkCrewAIMiddleware(agent_id="test-agent")
    assert mw.agent_id == "test-agent"
    assert isinstance(mw.engine, GovernanceEngine)

def test_wrap_agent():
    mw = TorkCrewAIMiddleware()
    agent = MockAgent()
    governed = mw.wrap_agent(agent)
    assert isinstance(governed, GovernedAgent)
    assert governed.name == "Test Agent"

def test_wrap_crew():
    mw = TorkCrewAIMiddleware()
    agent = MockAgent()
    crew = MockCrew(agents=[agent])
    governed_crew = mw.wrap_crew(crew)
    assert isinstance(governed_crew, GovernedCrew)
    assert isinstance(governed_crew.agents[0], GovernedAgent)

def test_before_task_allowed():
    mw = TorkCrewAIMiddleware()
    task = MockTask("Clean task")
    agent = MockAgent()
    payload = mw.before_task(task, agent)
    assert payload["task_description"] == "Clean task"

def test_before_task_blocked():
    engine = GovernanceEngine()
    mock_res = EvaluationResult(
        decision=PolicyDecision.DENY,
        reason="Blocked",
        violations=["Test violation"],
        original_payload={"task_description": "Bad task"},
        modified_payload=None,
        pii_found=[],
        timestamp=datetime.now(timezone.utc)
    )
    engine.evaluate = MagicMock(return_value=mock_res)
    
    mw = TorkCrewAIMiddleware(engine=engine)
    task = MockTask("Bad task")
    agent = MockAgent()
    
    with pytest.raises(GovernanceBlockedError):
        mw.before_task(task, agent)

def test_after_task_allowed():
    mw = TorkCrewAIMiddleware()
    task = MockTask("task")
    agent = MockAgent()
    res = mw.after_task(task, "Clean result", agent)
    assert res["result"] == "Clean result"
    assert "receipt" in res

def test_governed_agent_execution():
    mw = TorkCrewAIMiddleware()
    agent = MockAgent()
    governed = GovernedAgent(agent, mw)
    task = MockTask("task description")
    
    result = governed.execute_task(task)
    assert result == "Result for task description"

def test_governed_agent_getattr():
    agent = MockAgent()
    governed = GovernedAgent(agent, None)
    assert governed.name == "Test Agent"

def test_governed_crew_kickoff():
    mw = TorkCrewAIMiddleware()
    agent = MockAgent()
    crew = MockCrew(agents=[agent])
    governed_crew = GovernedCrew(crew, mw)
    
    res = governed_crew.kickoff()
    assert res == "Crew result"

def test_pii_redaction_before_task():
    mw = TorkCrewAIMiddleware()
    task = MockTask("My email is test@example.com")
    agent = MockAgent()
    payload = mw.before_task(task, agent)
    assert "task_description" in payload

def test_receipt_generation_after_task():
    mw = TorkCrewAIMiddleware()
    res = mw.after_task(MockTask("t"), "result", MockAgent())
    assert "receipt" in res
    assert res["receipt"]["agent_id"] == "crewai-agent"


class TestTorkGovernedTask:
    """Tests for TorkGovernedTask class."""

    def test_initialization_with_engine(self):
        """Test initialization with GovernanceEngine."""
        task = MockTask("Test task description")
        task.expected_output = "Expected output"
        engine = GovernanceEngine()

        governed = TorkGovernedTask(
            task=task,
            engine=engine,
            agent_id="task-agent",
        )

        assert governed._task == task
        assert governed.engine == engine
        assert governed.agent_id == "task-agent"
        assert governed.description == "Test task description"

    def test_initialization_requires_engine_or_api_key(self):
        """Test that either engine or api_key is required."""
        task = MockTask("task")

        with pytest.raises(ValueError, match="Either engine or api_key must be provided"):
            TorkGovernedTask(task=task)

    def test_validate_before_execution(self):
        """Test validating task before execution."""
        task = MockTask("Clean task")
        task.expected_output = "Clean output"
        engine = GovernanceEngine()

        governed = TorkGovernedTask(task=task, engine=engine)
        payload = governed.validate_before_execution()

        assert payload["task_description"] == "Clean task"
        assert payload["expected_output"] == "Clean output"

    def test_validate_after_execution(self):
        """Test validating task output after execution."""
        task = MockTask("task")
        engine = GovernanceEngine()

        governed = TorkGovernedTask(task=task, engine=engine)
        result = governed.validate_after_execution("Task completed successfully")

        assert result == "Task completed successfully"

    def test_validate_before_execution_denied(self):
        """Test validation denial before execution."""
        task = MockTask("Blocked task")
        engine = GovernanceEngine()

        mock_res = EvaluationResult(
            decision=PolicyDecision.DENY,
            reason="Blocked by policy",
            violations=["Task blocked"],
            original_payload={"task_description": "Blocked task"},
            modified_payload=None,
            pii_found=[],
            timestamp=datetime.now(timezone.utc)
        )
        engine.evaluate = MagicMock(return_value=mock_res)

        governed = TorkGovernedTask(task=task, engine=engine)

        with pytest.raises(GovernanceBlockedError):
            governed.validate_before_execution()

    def test_getattr_proxy(self):
        """Test that attributes are proxied to wrapped task."""
        task = MockTask("task")
        task.custom_attr = "custom_value"
        engine = GovernanceEngine()

        governed = TorkGovernedTask(task=task, engine=engine)

        assert governed.custom_attr == "custom_value"
