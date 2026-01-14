"""Nova Agent models."""

from nova_agent.models.dom import (
    BoundingBox,
    DomExtractionResult,
    InteractiveElement,
    PageMetadata,
    Screenshot,
)
from nova_agent.models.job import DomData, Job, JobStatus, Scenario, ScriptResult, Step, StepStatus
from nova_agent.models.messages import (
    AgentConnectMessage,
    DomExtractedMessage,
    ExecuteScriptMessage,
    ExtractDomMessage,
    GoalAchievedMessage,
    HeartbeatMessage,
    JobAcceptedMessage,
    JobAssignMessage,
    JobCompletedMessage,
    RegisteredMessage,
    ScriptResultMessage,
    StepCompletedMessage,
    StepStartedMessage,
)

__all__ = [
    # Messages
    "AgentConnectMessage",
    "RegisteredMessage",
    "HeartbeatMessage",
    "JobAssignMessage",
    "JobAcceptedMessage",
    "ExtractDomMessage",
    "DomExtractedMessage",
    "ExecuteScriptMessage",
    "ScriptResultMessage",
    "StepStartedMessage",
    "StepCompletedMessage",
    "GoalAchievedMessage",
    "JobCompletedMessage",
    # Job
    "Job",
    "Step",
    "Scenario",
    "JobStatus",
    "StepStatus",
    "DomData",
    "ScriptResult",
    # DOM
    "BoundingBox",
    "InteractiveElement",
    "PageMetadata",
    "Screenshot",
    "DomExtractionResult",
]
