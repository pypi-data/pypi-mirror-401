"""Job related models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class JobStatus(str, Enum):
    """Job 상태."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    """Step 상태."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Scenario(BaseModel):
    """시나리오 정보."""

    scenario_id: int
    name: str
    entry_url: str
    description: str | None = None

    model_config = {"extra": "allow"}


class Step(BaseModel):
    """Step 정보."""

    step_id: int
    step_order: int
    goal: str = ""  # prompt_text에서 채워질 수 있음
    expected_result: str | None = None

    model_config = {"extra": "allow"}

    @model_validator(mode="before")
    @classmethod
    def map_prompt_text_to_goal(cls, data: Any) -> Any:
        """prompt_text를 goal로 매핑."""
        # prompt_text가 있고 goal이 없으면 매핑
        if isinstance(data, dict) and "prompt_text" in data and not data.get("goal"):
            data["goal"] = data["prompt_text"]
        return data


class Job(BaseModel):
    """Job 정보.

    Gateway로부터 job_assign 메시지와 함께 수신됩니다.
    """

    job_id: int
    scenario: Scenario
    steps: list[Step] = Field(default_factory=list)
    status: JobStatus = JobStatus.PENDING
    current_step_index: int = 0
    # Runner에서 전달하는 환경변수 (스크립트에서 사용)
    environment_variables: dict[str, str] = Field(default_factory=dict)
    # 브라우저 설정 (쿠키, localStorage, 헤더, test_access_key 등)
    config: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}

    @property
    def current_step(self) -> Step | None:
        """현재 Step 반환."""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    @property
    def is_last_step(self) -> bool:
        """마지막 Step 여부."""
        return self.current_step_index >= len(self.steps) - 1

    def advance_step(self) -> bool:
        """다음 Step으로 이동.

        Returns:
            이동 성공 여부 (마지막 Step이면 False)
        """
        if self.is_last_step:
            return False
        self.current_step_index += 1
        return True


class DomData(BaseModel):
    """추출된 DOM 데이터."""

    url: str
    title: str
    html: str
    timestamp: str
    viewport: dict[str, int] | None = None

    model_config = {"extra": "allow"}


class ScriptResult(BaseModel):
    """스크립트 실행 결과."""

    success: bool
    error: str | None = None
    screenshot_base64: str | None = None
    duration_ms: int | None = None

    model_config = {"extra": "allow"}
