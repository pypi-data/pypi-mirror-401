"""
Governed Tool wrapper for LangChain.

Provides a wrapper that applies governance controls to any LangChain tool.
"""

from typing import Any, Optional, Dict, Callable
import structlog

from tork.core.engine import GovernanceEngine
from tork.core.models import EvaluationRequest, PolicyDecision
from tork.adapters.langchain.exceptions import GovernanceViolation

logger = structlog.get_logger(__name__)


class TorkGovernedTool:
    """
    Wrapper that applies governance controls to a LangChain tool.

    Evaluates tool inputs before execution and outputs after,
    enforcing DENY decisions and applying REDACT modifications.

    Can be initialized with either a GovernanceEngine instance or
    an API key for cloud-based governance.
    """

    def __init__(
        self,
        tool: Any,
        engine: Optional[GovernanceEngine] = None,
        api_key: Optional[str] = None,
        agent_id: str = "governed-tool",
    ) -> None:
        """
        Initialize the governed tool wrapper.

        Args:
            tool: The LangChain tool to wrap.
            engine: Optional GovernanceEngine instance. If not provided,
                   api_key must be specified.
            api_key: Optional Tork API key for cloud governance.
            agent_id: Agent ID for governance requests.

        Raises:
            ValueError: If neither engine nor api_key is provided.
        """
        if engine is None and api_key is None:
            raise ValueError("Either engine or api_key must be provided")

        self.tool = tool
        self.agent_id = agent_id
        self._receipts: list[Any] = []

        if engine:
            self.engine = engine
        else:
            self.engine = GovernanceEngine(api_key=api_key)

        # Copy tool attributes for compatibility
        self.name = getattr(tool, 'name', 'unknown_tool')
        self.description = getattr(tool, 'description', '')

        logger.info(
            "TorkGovernedTool initialized",
            agent_id=agent_id,
            tool_name=self.name,
            using_api=api_key is not None,
        )

    @property
    def receipts(self) -> list[Any]:
        """Return list of generated receipts."""
        return self._receipts

    def _evaluate(
        self,
        action: str,
        payload: Dict[str, Any],
    ) -> Any:
        """
        Evaluate payload against governance policies.

        Args:
            action: The action type.
            payload: Data to evaluate.

        Returns:
            EvaluationResult from the engine.

        Raises:
            GovernanceViolation: If policy decision is DENY.
        """
        request = EvaluationRequest(
            agent_id=self.agent_id,
            action=action,
            payload=payload,
        )

        result = self.engine.evaluate(request)

        if result.decision == PolicyDecision.DENY:
            logger.warning(
                "Governance violation in tool",
                action=action,
                tool_name=self.name,
                violations=result.violations,
            )
            raise GovernanceViolation(
                message=result.reason,
                decision=result.decision,
                violations=result.violations,
            )

        return result

    def run(self, tool_input: str, **kwargs: Any) -> Any:
        """
        Run the tool with governance controls.

        Args:
            tool_input: Input string for the tool.
            **kwargs: Additional keyword arguments.

        Returns:
            The tool output, possibly modified by redaction policies.

        Raises:
            GovernanceViolation: If input or output is denied.
        """
        # Evaluate input
        input_payload = {
            "tool_name": self.name,
            "tool_input": tool_input,
        }
        input_result = self._evaluate("tool_run_input", input_payload)

        # Apply input redactions if any
        if input_result.decision == PolicyDecision.REDACT and input_result.modified_payload:
            tool_input = input_result.modified_payload.get("tool_input", tool_input)

        logger.debug("Running wrapped tool", tool_name=self.name)

        # Execute the actual tool
        output = self.tool.run(tool_input, **kwargs)

        # Evaluate output
        output_payload = {
            "tool_name": self.name,
            "tool_output": output,
        }
        output_result = self._evaluate("tool_run_output", output_payload)

        # Apply output redactions if any
        if output_result.decision == PolicyDecision.REDACT and output_result.modified_payload:
            return output_result.modified_payload.get("tool_output", output)

        return output

    async def arun(self, tool_input: str, **kwargs: Any) -> Any:
        """
        Run the tool asynchronously with governance controls.

        Args:
            tool_input: Input string for the tool.
            **kwargs: Additional keyword arguments.

        Returns:
            The tool output, possibly modified by redaction policies.
        """
        # Evaluate input
        input_payload = {
            "tool_name": self.name,
            "tool_input": tool_input,
        }
        input_result = self._evaluate("tool_run_input", input_payload)

        if input_result.decision == PolicyDecision.REDACT and input_result.modified_payload:
            tool_input = input_result.modified_payload.get("tool_input", tool_input)

        # Execute the actual tool
        if hasattr(self.tool, 'arun'):
            output = await self.tool.arun(tool_input, **kwargs)
        else:
            output = self.tool.run(tool_input, **kwargs)

        # Evaluate output
        output_payload = {
            "tool_name": self.name,
            "tool_output": output,
        }
        output_result = self._evaluate("tool_run_output", output_payload)

        if output_result.decision == PolicyDecision.REDACT and output_result.modified_payload:
            return output_result.modified_payload.get("tool_output", output)

        return output

    def __call__(self, tool_input: str, **kwargs: Any) -> Any:
        """Allow calling the governed tool directly."""
        return self.run(tool_input, **kwargs)


def create_governed_tool(
    tool: Any,
    engine: Optional[GovernanceEngine] = None,
    api_key: Optional[str] = None,
    agent_id: str = "governed-tool",
) -> TorkGovernedTool:
    """
    Create a governed tool wrapper.

    Convenience function for creating a TorkGovernedTool instance.

    Args:
        tool: The LangChain tool to wrap.
        engine: Optional GovernanceEngine for policy evaluation.
        api_key: Optional Tork API key for cloud governance.
        agent_id: Agent ID for governance requests.

    Returns:
        TorkGovernedTool instance wrapping the provided tool.
    """
    return TorkGovernedTool(
        tool=tool,
        engine=engine,
        api_key=api_key,
        agent_id=agent_id,
    )
