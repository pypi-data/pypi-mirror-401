"""WebSocket message handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import structlog

from nova_agent.constants import (
    MSG_CHECK_GOAL,
    MSG_EXECUTE_SCRIPT,
    MSG_EXTRACT_DOM,
    MSG_GOAL_ACHIEVED_FROM_RUNNER,
    MSG_HEARTBEAT_ACK,
    MSG_JOB_ASSIGN,
    MSG_JOB_CANCEL,
    MSG_NEXT_STEP,
    MSG_REGISTER_ACK,
)
from nova_agent.models.messages import (
    CheckGoalMessage,
    ExecuteScriptMessage,
    ExtractDomMessage,
    JobAssignMessage,
    JobCancelMessage,
    NextStepMessage,
)
from nova_agent.settings import is_verbose

if TYPE_CHECKING:
    from nova_agent.executor.job_manager import JobManager
    from nova_agent.websocket.client import AgentWebSocketClient

logger = structlog.get_logger(__name__)


class MessageHandler:
    """WebSocket 메시지 핸들러.

    Gateway로부터 수신한 메시지를 처리합니다.
    메시지의 job_id를 사용하여 올바른 job session으로 라우팅합니다.

    Responsibilities:
        1. 메시지 타입별 핸들러 라우팅
        2. JobManager에 작업 위임
        3. 응답 메시지 전송
    """

    def __init__(
        self,
        client: AgentWebSocketClient,
        job_manager: JobManager,
    ) -> None:
        """Initialize message handler.

        Args:
            client: WebSocket 클라이언트
            job_manager: Job 관리자
        """
        self._client = client
        self._job_manager = job_manager

        # 메시지 타입별 핸들러 매핑
        self._handlers: dict[str, Any] = {
            MSG_JOB_ASSIGN: self._handle_job_assign,
            MSG_EXTRACT_DOM: self._handle_extract_dom,
            MSG_EXECUTE_SCRIPT: self._handle_execute_script,
            MSG_NEXT_STEP: self._handle_next_step,
            MSG_JOB_CANCEL: self._handle_job_cancel,
            MSG_CHECK_GOAL: self._handle_check_goal,
            MSG_GOAL_ACHIEVED_FROM_RUNNER: self._handle_goal_achieved,  # Runner가 보내는 goal_achieved
            MSG_HEARTBEAT_ACK: self._handle_heartbeat_ack,
            MSG_REGISTER_ACK: self._handle_register_ack,
        }

    async def handle_message(self, data: dict[str, Any]) -> None:
        """메시지 처리.

        Args:
            data: 수신한 메시지 데이터
        """
        msg_type = data.get("type")
        if not msg_type:
            logger.warning("message_without_type", data=data)
            return

        handler = self._handlers.get(msg_type)
        if not handler:
            logger.debug("unhandled_message_type", type=msg_type)
            return

        try:
            await handler(data)
        except Exception as e:
            logger.error(
                "message_handler_error",
                type=msg_type,
                error=str(e),
                exc_info=is_verbose(),
            )
            # 에러 메시지 전송
            await self._send_error(
                job_id=data.get("job_id"),
                step_id=data.get("step_id"),
                error=str(e),
            )

    async def _handle_job_assign(self, data: dict[str, Any]) -> None:
        """job_assign 처리.

        Job을 수락하고 첫 번째 Step을 시작합니다.
        """
        message = JobAssignMessage(**data)
        logger.info(
            "job_assign_received",
            job_id=message.job_id,
            scenario_name=message.scenario.get("name"),
        )

        # Job 수락 여부 결정 (현재는 항상 수락)
        # TODO: 리소스 체크 등 조건 추가 가능

        await self._job_manager.accept_job(message)

    async def _handle_extract_dom(self, data: dict[str, Any]) -> None:
        """extract_dom 처리.

        현재 페이지의 DOM을 추출하여 전송합니다.
        """
        message = ExtractDomMessage(**data)
        logger.debug(
            "extract_dom_received",
            job_id=message.job_id,
            step_id=message.step_id,
        )

        await self._job_manager.extract_dom(message)

    async def _handle_execute_script(self, data: dict[str, Any]) -> None:
        """execute_script 처리.

        Playwright 스크립트를 실행합니다.
        """
        message = ExecuteScriptMessage(**data)
        logger.debug(
            "execute_script_received",
            job_id=message.job_id,
            step_id=message.step_id,
        )

        await self._job_manager.execute_script(message)

    async def _handle_next_step(self, data: dict[str, Any]) -> None:
        """next_step 처리.

        다음 Step으로 이동합니다.
        """
        message = NextStepMessage(**data)
        logger.debug(
            "next_step_received",
            job_id=message.job_id,
            step_id=message.step_id,
        )

        await self._job_manager.start_next_step(message)

    async def _handle_job_cancel(self, data: dict[str, Any]) -> None:
        """job_cancel 처리.

        진행 중인 Job을 취소합니다.
        """
        message = JobCancelMessage(**data)
        logger.info(
            "job_cancel_received",
            job_id=message.job_id,
            reason=message.reason,
        )

        await self._job_manager.cancel_job(message)

    async def _handle_check_goal(self, data: dict[str, Any]) -> None:
        """check_goal 처리.

        Runner의 목표 달성 판단 결과를 수신하고 응답합니다.
        """
        message = CheckGoalMessage(**data)
        logger.debug(
            "check_goal_received",
            job_id=message.job_id,
            step_id=message.step_id,
            achieved=message.achieved,
        )

        await self._job_manager.handle_goal_check_result(message)

    async def _handle_goal_achieved(self, data: dict[str, Any]) -> None:
        """goal_achieved 처리.

        Runner가 goal 달성을 알리면 Step을 완료 처리합니다.
        Runner는 verification 객체를 보내지만, Agent는 achieved=True로 처리합니다.
        """
        # goal_achieved 메시지를 check_goal 형식으로 변환
        converted_data = {
            "type": "check_goal",
            "job_id": data.get("job_id"),
            "step_id": data.get("step_id"),
            "achieved": True,  # goal_achieved는 항상 달성 의미
            "reason": data.get("verification", {}).get("details"),
        }
        message = CheckGoalMessage(**converted_data)
        logger.debug(
            "goal_achieved_received",
            job_id=message.job_id,
            step_id=message.step_id,
        )

        await self._job_manager.handle_goal_check_result(message)

    async def _handle_heartbeat_ack(self, data: dict[str, Any]) -> None:
        """heartbeat_ack 처리.

        Heartbeat 응답 확인. 별도 처리 없음.
        """
        # No-op: heartbeat_ack는 단순 확인 메시지

    async def _handle_register_ack(self, data: dict[str, Any]) -> None:
        """register_ack 처리.

        시스템 정보 등록 확인. 별도 처리 없음.
        """
        success = data.get("success", False)
        if success:
            logger.debug("register_ack_received", success=success)
        else:
            logger.warning("register_ack_failed", data=data)

    async def _send_error(
        self,
        job_id: int | None,
        step_id: int | None,
        error: str,
    ) -> None:
        """에러 메시지 전송."""
        if not self._client.agent_id:
            return

        message = {
            "type": "error",
            "job_id": job_id,
            "step_id": step_id,
            "agent_id": self._client.agent_id,
            "error": error,
        }
        await self._client.send_message(message)
