from typing import Any, Optional, List, Dict, TYPE_CHECKING
import structlog

if TYPE_CHECKING:
    from tork.adapters.autogen.middleware import TorkAutoGenMiddleware

from tork.core.engine import GovernanceEngine
from tork.core.models import EvaluationRequest, PolicyDecision
from tork.adapters.autogen.exceptions import MessageBlockedError, ResponseBlockedError

logger = structlog.get_logger(__name__)


class TorkGovernedAssistant:
    """
    Wrapper that applies governance controls to an AutoGen AssistantAgent.

    Can be initialized with either a GovernanceEngine instance or
    an API key for cloud-based governance.
    """

    def __init__(
        self,
        assistant: Any,
        engine: Optional[GovernanceEngine] = None,
        api_key: Optional[str] = None,
        agent_id: str = "governed-assistant",
    ) -> None:
        """
        Initialize the governed assistant wrapper.

        Args:
            assistant: The AutoGen AssistantAgent to wrap.
            engine: Optional GovernanceEngine instance.
            api_key: Optional Tork API key for cloud governance.
            agent_id: Agent ID for governance requests.
        """
        if engine is None and api_key is None:
            raise ValueError("Either engine or api_key must be provided")

        self._assistant = assistant
        self.agent_id = agent_id

        if engine:
            self.engine = engine
        else:
            self.engine = GovernanceEngine(api_key=api_key)

        # Copy assistant attributes for compatibility
        self.name = getattr(assistant, 'name', 'assistant')

        logger.info(
            "TorkGovernedAssistant initialized",
            agent_id=agent_id,
            assistant_name=self.name,
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
        return result

    def intercept_message(self, message: Any, sender: Optional[str] = None) -> Any:
        """
        Intercept and validate incoming messages.

        Args:
            message: The incoming message.
            sender: Optional sender identifier.

        Returns:
            The message, possibly modified by governance policies.

        Raises:
            MessageBlockedError: If message is denied by policy.
        """
        content = message if isinstance(message, str) else str(message.get("content", message))

        payload = {"content": content, "sender": sender}
        result = self._evaluate("message_intercept", payload)

        if result.decision == PolicyDecision.DENY:
            raise MessageBlockedError(f"Message blocked by policy: {result.violations}")

        if result.decision == PolicyDecision.REDACT and result.modified_payload:
            modified_content = result.modified_payload.get("content", content)
            if isinstance(message, dict) and "content" in message:
                message["content"] = modified_content
                return message
            return modified_content

        return message

    def validate_tool_call(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate a tool call before execution.

        Args:
            tool_name: Name of the tool being called.
            tool_args: Arguments to the tool.

        Returns:
            The tool arguments, possibly modified by governance policies.

        Raises:
            MessageBlockedError: If tool call is denied by policy.
        """
        payload = {
            "tool_name": tool_name,
            "tool_args": tool_args,
        }
        result = self._evaluate("tool_call_validate", payload)

        if result.decision == PolicyDecision.DENY:
            raise MessageBlockedError(
                f"Tool call '{tool_name}' blocked by policy: {result.violations}"
            )

        if result.decision == PolicyDecision.REDACT and result.modified_payload:
            return result.modified_payload.get("tool_args", tool_args)

        return tool_args

    def receive(
        self,
        message: Any,
        sender: Any,
        request_reply: Optional[bool] = None,
    ) -> Any:
        """Receive message with governance checks."""
        governed_message = self.intercept_message(
            message, sender=getattr(sender, "name", str(sender))
        )
        return self._assistant.receive(governed_message, sender, request_reply)

    def generate_reply(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        sender: Optional[Any] = None,
        **kwargs,
    ) -> Any:
        """Generate reply with governance checks on output."""
        # Process input messages
        if messages:
            messages = [self.intercept_message(m) for m in messages]

        # Generate reply via original assistant
        reply = self._assistant.generate_reply(messages=messages, sender=sender, **kwargs)

        # Validate output
        if reply:
            content = reply if isinstance(reply, str) else str(reply.get("content", reply))
            payload = {"content": content, "assistant_name": self.name}
            result = self._evaluate("reply_generate", payload)

            if result.decision == PolicyDecision.DENY:
                raise ResponseBlockedError(f"Reply blocked by policy: {result.violations}")

            if result.decision == PolicyDecision.REDACT and result.modified_payload:
                modified_content = result.modified_payload.get("content", content)
                if isinstance(reply, dict) and "content" in reply:
                    reply["content"] = modified_content
                else:
                    reply = modified_content

        return reply

    def __getattr__(self, name: str):
        """Proxy all other attributes to wrapped assistant."""
        return getattr(self._assistant, name)


class GovernedAutoGenAgent:
    """An AutoGen agent wrapped with Tork governance."""
    
    def __init__(self, agent: Any, middleware: "TorkAutoGenMiddleware"):
        self._agent = agent
        self._middleware = middleware
    
    def receive(self, message: Any, sender: Any, request_reply: Optional[bool] = None):
        """Receive message with governance checks."""
        governed_message = self._middleware.process_message(message, sender=getattr(sender, "name", str(sender)))
        return self._agent.receive(governed_message, sender, request_reply)
    
    def generate_reply(self, messages: Optional[List[Dict[str, Any]]] = None, sender: Optional[Any] = None, **kwargs):
        """Generate reply with governance."""
        # Process input messages
        if messages:
            messages = [self._middleware.process_message(m) for m in messages]
        
        # Generate reply via original agent
        reply = self._agent.generate_reply(messages=messages, sender=sender, **kwargs)
        
        # Process output through governance
        return self._middleware.process_response(reply, agent_name=getattr(self._agent, "name", "agent"))
    
    def __getattr__(self, name: str):
        """Proxy all other attributes to wrapped agent."""
        return getattr(self._agent, name)

class GovernedGroupChat:
    """An AutoGen GroupChat with governance on all agent communications."""
    
    def __init__(self, agents: List[Any], middleware: "TorkAutoGenMiddleware", **kwargs):
        self._middleware = middleware
        self._agents = [middleware.wrap_agent(a) for a in agents]
        self._kwargs = kwargs
    
    @property
    def agents(self):
        return self._agents

    def __getattr__(self, name: str):
        # We don't have a real GroupChat object to wrap in this mock, so we just proxy to self
        return getattr(self, name)
