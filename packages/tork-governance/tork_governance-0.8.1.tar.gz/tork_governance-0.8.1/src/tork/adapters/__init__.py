"""
Adapters module for Tork Governance SDK.

Provides integration adapters for various AI agent frameworks
and external systems.
"""

from tork.adapters.base import BaseAdapter
from tork.adapters.langchain import (
    GovernanceViolation,
    TorkCallbackHandler,
    GovernedChain,
    create_governed_chain,
    TorkGovernedTool,
    create_governed_tool,
)

from tork.adapters.crewai import (
    TorkCrewAIMiddleware,
    GovernedAgent,
    GovernedCrew,
    TorkGovernedTask,
    GovernanceBlockedError,
    PIIDetectedError,
)
from tork.adapters.autogen import (
    TorkAutoGenMiddleware,
    GovernedAutoGenAgent,
    GovernedGroupChat,
    TorkGovernedAssistant,
    AutoGenGovernanceError,
    MessageBlockedError,
    ResponseBlockedError,
)
from tork.adapters.openai_agents import (
    TorkOpenAIAgentsMiddleware,
    GovernedOpenAIAgent,
    GovernedRunner,
    OpenAIAgentGovernanceError,
    InputBlockedError,
    OutputBlockedError,
    ToolCallBlockedError,
)

__all__ = [
    # Base
    "BaseAdapter",
    # LangChain
    "GovernanceViolation",
    "TorkCallbackHandler",
    "GovernedChain",
    "create_governed_chain",
    "TorkGovernedTool",
    "create_governed_tool",
    # CrewAI
    "TorkCrewAIMiddleware",
    "GovernedAgent",
    "GovernedCrew",
    "TorkGovernedTask",
    "GovernanceBlockedError",
    "PIIDetectedError",
    # AutoGen
    "TorkAutoGenMiddleware",
    "GovernedAutoGenAgent",
    "GovernedGroupChat",
    "TorkGovernedAssistant",
    "AutoGenGovernanceError",
    "MessageBlockedError",
    "ResponseBlockedError",
    # OpenAI Agents
    "TorkOpenAIAgentsMiddleware",
    "GovernedOpenAIAgent",
    "GovernedRunner",
    "OpenAIAgentGovernanceError",
    "InputBlockedError",
    "OutputBlockedError",
    "ToolCallBlockedError",
]
