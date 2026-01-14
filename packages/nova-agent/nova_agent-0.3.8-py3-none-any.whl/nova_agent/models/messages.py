"""WebSocket message models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

# ============================================================
# Base Message
# ============================================================

class BaseMessage(BaseModel):
    """기본 메시지 모델."""

    type: str

    model_config = {"extra": "allow"}


# ============================================================
# Agent → Gateway Messages
# ============================================================

class AgentConnectMessage(BaseModel):
    """Agent 연결 요청 메시지."""

    type: Literal["agent_connect"] = "agent_connect"
    token: str


class HeartbeatMessage(BaseModel):
    """Heartbeat 메시지."""

    type: Literal["heartbeat"] = "heartbeat"
    agent_id: str
    timestamp: str


class JobAcceptedMessage(BaseModel):
    """Job 수락 메시지."""

    type: Literal["job_accepted"] = "job_accepted"
    job_id: int
    agent_id: str


class JobAssignFailedMessage(BaseModel):
    """Job 할당 실패 메시지."""

    type: Literal["job_assign_failed"] = "job_assign_failed"
    job_id: int
    agent_id: str
    reason: str


class StepStartedMessage(BaseModel):
    """Step 시작 메시지."""

    type: Literal["step_started"] = "step_started"
    job_id: int
    step_id: int
    agent_id: str


class DomExtractedMessage(BaseModel):
    """DOM 추출 완료 메시지."""

    type: Literal["dom_extracted"] = "dom_extracted"
    job_id: int
    step_id: int
    agent_id: str
    dom: dict[str, Any]  # url, title, html, timestamp


class ScriptResultMessage(BaseModel):
    """스크립트 실행 결과 메시지."""

    type: Literal["script_result"] = "script_result"
    job_id: int
    step_id: int
    agent_id: str
    status: str  # "success" | "failed"
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    screenshot: dict[str, Any] | None = None


class StepCompletedMessage(BaseModel):
    """Step 완료 메시지."""

    type: Literal["step_completed"] = "step_completed"
    job_id: int
    step_id: int
    agent_id: str
    success: bool
    error: str | None = None


class GoalAchievedMessage(BaseModel):
    """목표 달성 메시지 (Runner의 check_goal에 대한 응답)."""

    type: Literal["goal_achieved"] = "goal_achieved"
    job_id: int
    step_id: int
    agent_id: str
    achieved: bool
    reason: str | None = None


class JobCompletedMessage(BaseModel):
    """Job 완료 메시지."""

    type: Literal["job_completed"] = "job_completed"
    job_id: int
    agent_id: str
    success: bool
    total_steps: int
    completed_steps: int  # Gateway/Runner와 호환을 위해 passed_steps → completed_steps로 변경
    failed_steps: int
    error: str | None = None


class ErrorMessage(BaseModel):
    """에러 메시지."""

    type: Literal["error"] = "error"
    job_id: int | None = None
    step_id: int | None = None
    agent_id: str
    error: str
    error_type: str | None = None


# ============================================================
# Gateway → Agent Messages
# ============================================================

class RegisteredMessage(BaseModel):
    """연결 등록 완료 메시지."""

    type: Literal["registered"] = "registered"
    agent_id: str
    project_id: int | None = None


class JobAssignMessage(BaseModel):
    """Job 할당 메시지."""

    type: Literal["job_assign"] = "job_assign"
    job_id: int
    scenario: dict[str, Any]
    steps: list[dict[str, Any]] = Field(default_factory=list)
    # Runner에서 전달하는 환경변수 (스크립트에서 사용)
    environment_variables: dict[str, str] = Field(default_factory=dict)
    # 브라우저 설정 (쿠키, localStorage, 헤더, test_access_key 등)
    config: dict[str, Any] = Field(default_factory=dict)


class ExtractDomMessage(BaseModel):
    """DOM 추출 요청 메시지."""

    type: Literal["extract_dom"] = "extract_dom"
    job_id: int
    step_id: int


class ExecuteScriptMessage(BaseModel):
    """스크립트 실행 요청 메시지."""

    type: Literal["execute_script"] = "execute_script"
    job_id: int
    step_id: int
    script: str
    action_id: int | None = None


class NextStepMessage(BaseModel):
    """다음 Step 진행 메시지."""

    type: Literal["next_step"] = "next_step"
    job_id: int
    step_id: int  # 다음 step_id


class JobCancelMessage(BaseModel):
    """Job 취소 메시지."""

    type: Literal["job_cancel"] = "job_cancel"
    job_id: int
    reason: str | None = None


class CheckGoalMessage(BaseModel):
    """목표 달성 확인 요청 메시지."""

    type: Literal["check_goal"] = "check_goal"
    job_id: int
    step_id: int
    achieved: bool
    reason: str | None = None


# ============================================================
# Message Type Mapping
# ============================================================

AGENT_TO_GATEWAY_MESSAGES = {
    "agent_connect": AgentConnectMessage,
    "heartbeat": HeartbeatMessage,
    "job_accepted": JobAcceptedMessage,
    "job_assign_failed": JobAssignFailedMessage,
    "step_started": StepStartedMessage,
    "dom_extracted": DomExtractedMessage,
    "script_result": ScriptResultMessage,
    "step_completed": StepCompletedMessage,
    "goal_achieved": GoalAchievedMessage,
    "job_completed": JobCompletedMessage,
    "error": ErrorMessage,
}

GATEWAY_TO_AGENT_MESSAGES = {
    "registered": RegisteredMessage,
    "job_assign": JobAssignMessage,
    "extract_dom": ExtractDomMessage,
    "execute_script": ExecuteScriptMessage,
    "next_step": NextStepMessage,
    "job_cancel": JobCancelMessage,
    "check_goal": CheckGoalMessage,
}


def parse_message(data: dict[str, Any]) -> BaseMessage:
    """메시지 파싱.

    Args:
        data: 메시지 딕셔너리

    Returns:
        파싱된 메시지 객체

    Raises:
        ValueError: 알 수 없는 메시지 타입
    """
    msg_type = data.get("type")
    if not msg_type:
        raise ValueError("Message type is required")

    # Gateway → Agent 메시지 먼저 확인
    if msg_type in GATEWAY_TO_AGENT_MESSAGES:
        return GATEWAY_TO_AGENT_MESSAGES[msg_type](**data)  # type: ignore[no-any-return]

    # Agent → Gateway 메시지 확인
    if msg_type in AGENT_TO_GATEWAY_MESSAGES:
        return AGENT_TO_GATEWAY_MESSAGES[msg_type](**data)  # type: ignore[no-any-return]

    # 알 수 없는 타입은 기본 메시지로 반환
    return BaseMessage(**data)
