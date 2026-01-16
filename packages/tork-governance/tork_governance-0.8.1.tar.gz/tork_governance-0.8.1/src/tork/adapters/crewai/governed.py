from typing import Any, Optional, Dict, TYPE_CHECKING
import structlog

if TYPE_CHECKING:
    from tork.adapters.crewai.middleware import TorkCrewAIMiddleware

from tork.core.engine import GovernanceEngine
from tork.core.models import EvaluationRequest, PolicyDecision
from tork.adapters.crewai.exceptions import GovernanceBlockedError

logger = structlog.get_logger(__name__)


class TorkGovernedTask:
    """
    Wrapper that applies governance controls to a CrewAI task.

    Evaluates task description and expected output against policies,
    and validates results after execution.
    """

    def __init__(
        self,
        task: Any,
        engine: Optional[GovernanceEngine] = None,
        api_key: Optional[str] = None,
        agent_id: str = "governed-task",
    ) -> None:
        """
        Initialize the governed task wrapper.

        Args:
            task: The CrewAI Task to wrap.
            engine: Optional GovernanceEngine instance.
            api_key: Optional Tork API key for cloud governance.
            agent_id: Agent ID for governance requests.
        """
        if engine is None and api_key is None:
            raise ValueError("Either engine or api_key must be provided")

        self._task = task
        self.agent_id = agent_id

        if engine:
            self.engine = engine
        else:
            self.engine = GovernanceEngine(api_key=api_key)

        # Copy task attributes for compatibility
        self.description = getattr(task, 'description', '')
        self.expected_output = getattr(task, 'expected_output', '')

        logger.info(
            "TorkGovernedTask initialized",
            agent_id=agent_id,
            using_api=api_key is not None,
        )

    def _evaluate(self, action: str, payload: Dict[str, Any]) -> Any:
        """Evaluate payload against governance policies."""
        request = EvaluationRequest(
            agent_id=self.agent_id,
            action=action,
            payload=payload,
        )
        result = self.engine.evaluate(request)

        if result.decision == PolicyDecision.DENY:
            logger.warning(
                "Governance violation in task",
                action=action,
                violations=result.violations,
            )
            raise GovernanceBlockedError(
                f"Task blocked by policy: {result.violations}"
            )

        return result

    def validate_before_execution(self) -> Dict[str, Any]:
        """Validate task before execution."""
        payload = {
            "task_description": self.description,
            "expected_output": self.expected_output,
        }
        result = self._evaluate("task_before_execution", payload)

        if result.modified_payload:
            return result.modified_payload
        return payload

    def validate_after_execution(self, output: str) -> str:
        """Validate task output after execution."""
        payload = {
            "task_output": output,
            "task_description": self.description,
        }
        result = self._evaluate("task_after_execution", payload)

        if result.decision == PolicyDecision.REDACT and result.modified_payload:
            return result.modified_payload.get("task_output", output)
        return output

    def __getattr__(self, name: str):
        """Proxy all other attributes to wrapped task."""
        return getattr(self._task, name)


class GovernedAgent:
    """A CrewAI agent wrapped with Tork governance."""
    
    def __init__(self, agent: Any, middleware: "TorkCrewAIMiddleware"):
        self._agent = agent
        self._middleware = middleware
    
    def execute_task(self, task: Any, context: Any = None):
        """Execute task with governance checks."""
        # Pre-execution governance
        self._middleware.before_task(task, self._agent)
        
        # Execute original agent task
        result = self._agent.execute_task(task, context=context)
        
        # Post-execution governance
        governed_result = self._middleware.after_task(task, result, self._agent)
        
        return governed_result["result"]
    
    def __getattr__(self, name: str):
        """Proxy all other attributes to wrapped agent."""
        return getattr(self._agent, name)

class GovernedCrew:
    """A CrewAI crew with all agents governed."""
    
    def __init__(self, crew: Any, middleware: "TorkCrewAIMiddleware"):
        self._crew = crew
        self._middleware = middleware
        self._governed_agents = [
            GovernedAgent(agent, middleware) for agent in getattr(crew, "agents", [])
        ]
        # In actual CrewAI we might need to monkeypatch the crew's agents list
        if hasattr(self._crew, "agents"):
            self._crew.agents = self._governed_agents
    
    def kickoff(self, inputs: Optional[Dict[str, Any]] = None):
        """Run the crew with governance on all tasks."""
        results = self._crew.kickoff(inputs=inputs)
        return results

    def __getattr__(self, name: str):
        return getattr(self._crew, name)
