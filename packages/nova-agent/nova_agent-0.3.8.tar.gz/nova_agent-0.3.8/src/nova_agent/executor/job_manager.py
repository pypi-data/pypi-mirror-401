"""Job manager for concurrent job execution."""

from __future__ import annotations

import asyncio
import base64
from typing import TYPE_CHECKING, Any

import structlog

from nova_agent.browser.dom_extractor import DomExtractor
from nova_agent.browser.pool import BrowserPool
from nova_agent.executor.job_session import JobSession
from nova_agent.executor.script_runner import ScriptRunner
from nova_agent.models.job import Job, Scenario, Step
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
    from nova_agent.websocket.client import AgentWebSocketClient

logger = structlog.get_logger(__name__)


class JobManager:
    """Manages concurrent job execution.

    Replaces the single-job JobExecutor with a manager that can
    handle multiple concurrent jobs, each with its own browser.

    Responsibilities:
        1. Accept jobs and acquire browsers from pool
        2. Route messages to correct job sessions
        3. Manage job lifecycle (start, execute, complete)
        4. Handle job timeouts
    """

    def __init__(self, browser_pool: BrowserPool) -> None:
        """Initialize job manager.

        Args:
            browser_pool: Browser pool for acquiring browsers
        """
        self._browser_pool = browser_pool
        self._client: AgentWebSocketClient | None = None
        self._sessions: dict[int, JobSession] = {}  # job_id -> JobSession
        self._lock = asyncio.Lock()

    def set_client(self, client: AgentWebSocketClient) -> None:
        """Set WebSocket client reference.

        Args:
            client: WebSocket client
        """
        self._client = client

    @property
    def active_job_count(self) -> int:
        """Number of active jobs."""
        return len(self._sessions)

    def get_session(self, job_id: int) -> JobSession | None:
        """Get session for a job.

        Args:
            job_id: The job ID

        Returns:
            JobSession if found
        """
        return self._sessions.get(job_id)

    async def accept_job(self, message: JobAssignMessage) -> None:
        """Accept a new job assignment.

        Acquires a browser from the pool (queuing if full)
        and creates a new job session.

        Args:
            message: Job assignment message
        """
        if not self._client:
            logger.error("client_not_set")
            return

        job_id = message.job_id

        # Check if job already exists
        if job_id in self._sessions:
            logger.warning(
                "job_already_exists",
                job_id=job_id,
            )
            await self._send_job_assign_failed(
                job_id,
                reason="JOB_ALREADY_EXISTS",
            )
            return

        # Check if pool has available slots (즉시 거부, Runner가 재시도 관리)
        if self._browser_pool.available_count <= 0:
            logger.warning(
                "pool_full_rejecting_job",
                job_id=job_id,
                active=self._browser_pool.active_count,
                max=self._browser_pool.max_size,
            )
            await self._send_job_assign_failed(
                job_id,
                reason="POOL_FULL",
            )
            return

        # config와 environment_variables 추출
        config = message.config
        environment_variables = message.environment_variables

        logger.info(
            "accepting_job",
            job_id=job_id,
            scenario_name=message.scenario.get("name"),
            active_jobs=self.active_job_count,
            pool_available=self._browser_pool.available_count,
            has_config=bool(config),
            env_var_count=len(environment_variables),
            cookie_count=len(config.get("cookies", [])) if config else 0,
            has_test_access_key=bool(config.get("test_access_key")) if config else False,
        )

        try:
            # Acquire browser with config (쿠키, localStorage, 헤더, test_access_key 설정)
            browser_manager = await self._browser_pool.acquire(job_id, config=config)

            # Create job (config와 environment_variables 포함)
            scenario = Scenario(**message.scenario)
            steps = [Step(**s) for s in message.steps]
            job = Job(
                job_id=job_id,
                scenario=scenario,
                steps=steps,
                config=config,
                environment_variables=environment_variables,
            )

            # Create session
            session = JobSession(
                job_id=job_id,
                job=job,
                browser_manager=browser_manager,
            )

            async with self._lock:
                self._sessions[job_id] = session

            logger.info(
                "job_accepted",
                job_id=job_id,
                scenario_name=scenario.name,
                steps_count=len(steps),
            )

            # Send job_accepted
            await self._send_job_accepted(job_id)

            # Navigate to entry URL
            try:
                await browser_manager.navigate(scenario.entry_url)
            except Exception as e:
                logger.error(
                    "navigation_failed",
                    job_id=job_id,
                    url=scenario.entry_url,
                    error=str(e),
                )
                await self._send_error(job_id, None, f"Navigation failed: {e}")
                # Navigation 실패 시 브라우저 정리
                await self._cleanup_session(job_id)
                return

            # Start first step
            await self._start_step(session)

        except Exception as e:
            logger.error(
                "job_accept_failed",
                job_id=job_id,
                error=str(e),
                exc_info=is_verbose(),
            )

            # Clean up if browser was acquired
            await self._browser_pool.release(job_id)

            # Remove session if created
            async with self._lock:
                self._sessions.pop(job_id, None)

            await self._send_error(job_id, None, f"Job accept failed: {e}")

    async def extract_dom(self, message: ExtractDomMessage) -> None:
        """Extract DOM for a job.

        현재 활성 페이지 (탭/팝업 전환 후 페이지)에서 DOM을 추출합니다.

        Args:
            message: Extract DOM message
        """
        session = self.get_session(message.job_id)
        if not session:
            logger.error("session_not_found", job_id=message.job_id)
            return

        session.update_activity()

        try:
            browser_manager = session.browser_manager

            # 페이지 닫힘 확인 및 복구
            if not await browser_manager.handle_page_closed():
                raise RuntimeError("All browser pages closed")

            page = browser_manager.page  # 현재 활성 페이지 사용
            if not page:
                raise RuntimeError("Browser page not available")

            extractor = DomExtractor(page)
            dom_data = await extractor.extract()

            # 스크린샷 촬영 (Runner가 기대하는 형식)
            screenshot_b64: str | None = None
            try:
                screenshot = await browser_manager.screenshot()
                screenshot_b64 = base64.b64encode(screenshot).decode()
            except Exception as e:
                logger.warning("dom_screenshot_failed", error=str(e))

            await self._send_dom_extracted(
                message.job_id,
                message.step_id,
                dom_data,
                screenshot_base64=screenshot_b64,
            )

        except Exception as e:
            logger.error(
                "dom_extraction_failed",
                job_id=message.job_id,
                step_id=message.step_id,
                error=str(e),
            )
            await self._send_error(
                message.job_id,
                message.step_id,
                f"DOM extraction failed: {e}",
            )

    async def execute_script(self, message: ExecuteScriptMessage) -> None:
        """Execute script for a job.

        스크립트 실행 후 새 탭/팝업이 열렸는지 감지하고 자동 전환합니다.

        Args:
            message: Execute script message
        """
        session = self.get_session(message.job_id)
        if not session:
            logger.error("session_not_found", job_id=message.job_id)
            return

        session.update_activity()

        try:
            browser_manager = session.browser_manager

            # 페이지 닫힘 확인 및 복구
            if not await browser_manager.handle_page_closed():
                raise RuntimeError("All browser pages closed")

            page = browser_manager.page
            if not page:
                raise RuntimeError("Browser page not available")

            # 스크립트 실행 전 페이지 목록 저장 (새 탭 감지용)
            context = browser_manager.context
            pages_before = set(context.pages) if context else set()

            runner = ScriptRunner(page)
            result = await runner.run(message.script)

            # 스크립트 실행 후 새 탭/팝업 감지 및 전환
            if result["success"]:
                new_page = await browser_manager.detect_and_switch_to_new_page(
                    pages_before,
                    timeout=3.0,
                    poll_interval=0.1,
                )
                if new_page:
                    logger.info(
                        "script_opened_new_tab",
                        job_id=message.job_id,
                        step_id=message.step_id,
                        new_url=new_page.url,
                    )

            # 페이지 닫힘 재확인 (스크립트가 현재 탭을 닫았을 수 있음)
            await browser_manager.handle_page_closed()

            # Take screenshot (현재 활성 페이지에서)
            screenshot_b64 = None
            try:
                screenshot = await browser_manager.screenshot()
                screenshot_b64 = base64.b64encode(screenshot).decode()
            except Exception as e:
                logger.warning("screenshot_failed", error=str(e))

            await self._send_script_result(
                message.job_id,
                message.step_id,
                success=result["success"],
                error=result.get("error"),
                screenshot_base64=screenshot_b64,
            )

        except Exception as e:
            logger.error(
                "script_execution_failed",
                job_id=message.job_id,
                step_id=message.step_id,
                error=str(e),
            )
            await self._send_error(
                message.job_id,
                message.step_id,
                f"Script execution failed: {e}",
            )

    async def start_next_step(self, message: NextStepMessage) -> None:
        """Start next step for a job.

        Args:
            message: Next step message
        """
        session = self.get_session(message.job_id)
        if not session:
            logger.error("session_not_found", job_id=message.job_id)
            return

        session.update_activity()

        if not session.advance_step():
            logger.warning("no_more_steps", job_id=message.job_id)
            return

        await self._start_step(session)

    async def handle_goal_check_result(self, message: CheckGoalMessage) -> None:
        """Handle goal check result.

        Args:
            message: Check goal message
        """
        session = self.get_session(message.job_id)
        if not session:
            logger.error("session_not_found", job_id=message.job_id)
            return

        session.update_activity()

        await self._send_goal_achieved(
            message.job_id,
            message.step_id,
            achieved=message.achieved,
            reason=message.reason,
        )

        if message.achieved:
            await self._complete_step(session, message.step_id, success=True)

    async def cancel_job(self, message: JobCancelMessage) -> None:
        """Cancel a job.

        Args:
            message: Job cancel message
        """
        session = self.get_session(message.job_id)
        if not session:
            logger.warning("no_job_to_cancel", job_id=message.job_id)
            # 이미 없는 Job도 cancelled 응답 전송 (Gateway/Runner 상태 동기화)
            await self._send_job_cancelled(message.job_id, message.reason)
            return

        logger.info(
            "job_cancelled",
            job_id=message.job_id,
            reason=message.reason,
        )

        await self._cleanup_session(message.job_id)
        await self._send_job_cancelled(message.job_id, message.reason)

    async def check_timeouts(self, timeout_seconds: int) -> list[int]:
        """Check for timed out jobs.

        Args:
            timeout_seconds: Timeout threshold

        Returns:
            List of timed out job IDs
        """
        timed_out = []

        for job_id, session in list(self._sessions.items()):
            if session.is_timed_out(timeout_seconds):
                logger.warning(
                    "job_timed_out",
                    job_id=job_id,
                    idle_seconds=int(session.last_activity),
                )
                timed_out.append(job_id)

        # Clean up timed out sessions
        for job_id in timed_out:
            await self._cleanup_session(job_id)

        return timed_out

    async def reset(self) -> list[int]:
        """Reset all job state and cleanup browsers (called on reconnect).

        Gateway가 재시작되었거나 연결이 끊긴 경우 이전 Job들은 유효하지 않으므로
        모든 세션과 브라우저를 정리합니다.

        Returns:
            List of job IDs that were reset (for notification after reconnect)
        """
        job_ids = list(self._sessions.keys())
        if job_ids:
            logger.info(
                "resetting_jobs_on_reconnect",
                job_count=len(job_ids),
                job_ids=job_ids,
            )
            for job_id in job_ids:
                await self._cleanup_session(job_id)
        else:
            logger.debug("no_jobs_to_reset")

        return job_ids

    async def shutdown(self) -> None:
        """Shutdown manager and release all resources."""
        for job_id in list(self._sessions.keys()):
            await self._cleanup_session(job_id)

        await self._browser_pool.shutdown()

    # ============================================================
    # Internal Methods
    # ============================================================

    async def _start_step(self, session: JobSession) -> None:
        """Start current step for a session."""
        step = session.current_step
        if not step:
            logger.error("no_current_step", job_id=session.job_id)
            return

        logger.info(
            "step_starting",
            job_id=session.job_id,
            step_id=step.step_id,
            goal=step.goal,
        )

        await self._send_step_started(session.job_id, step.step_id)

    async def _complete_step(
        self,
        session: JobSession,
        step_id: int,
        success: bool,
        error: str | None = None,
    ) -> None:
        """Complete current step."""
        await self._send_step_completed(
            session.job_id,
            step_id,
            success,
            error,
        )

        if session.is_last_step and success:
            await self._complete_job(session, success=True)

    async def _complete_job(
        self,
        session: JobSession,
        success: bool,
        error: str | None = None,
    ) -> None:
        """Complete a job."""
        job = session.job
        passed_steps = job.current_step_index + 1 if success else job.current_step_index
        failed_steps = 0 if success else 1

        await self._send_job_completed(
            job.job_id,
            success=success,
            total_steps=len(job.steps),
            passed_steps=passed_steps,
            failed_steps=failed_steps,
            error=error,
        )

        # Clean up session
        await self._cleanup_session(job.job_id)

    async def _cleanup_session(self, job_id: int) -> None:
        """Clean up a job session."""
        async with self._lock:
            session = self._sessions.pop(job_id, None)

        if session:
            await self._browser_pool.release(job_id)
            logger.debug("session_cleaned_up", job_id=job_id)

    # ============================================================
    # Message Sending Methods
    # ============================================================

    @property
    def _ensure_client(self) -> AgentWebSocketClient:
        """Get client or raise error."""
        if self._client is None:
            raise RuntimeError("WebSocket client is not set")
        return self._client

    async def _send_job_accepted(self, job_id: int) -> None:
        """job_accepted 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "job_accepted",
                "job_id": job_id,
                "agent_id": client.agent_id,
            }
        )

    async def _send_job_assign_failed(self, job_id: int, reason: str) -> None:
        """job_assign_failed 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "job_assign_failed",
                "job_id": job_id,
                "agent_id": client.agent_id,
                "reason": reason,
            }
        )

    async def _send_step_started(self, job_id: int, step_id: int) -> None:
        """step_started 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "step_started",
                "job_id": job_id,
                "step_id": step_id,
                "agent_id": client.agent_id,
            }
        )

    async def _send_dom_extracted(
        self,
        job_id: int,
        step_id: int,
        dom: dict[str, Any],
        screenshot_base64: str | None = None,
    ) -> None:
        """dom_extracted 메시지 전송 (스크린샷 포함)."""
        client = self._ensure_client
        msg: dict[str, Any] = {
            "type": "dom_extracted",
            "job_id": job_id,
            "step_id": step_id,
            "agent_id": client.agent_id,
            "dom": dom,
        }
        # 스크린샷이 있으면 Runner 형식에 맞게 추가
        if screenshot_base64:
            msg["screenshot"] = {
                "base64": screenshot_base64,
                "mime_type": "image/png",
            }
        await client.send_message(msg)

    async def _send_script_result(
        self,
        job_id: int,
        step_id: int,
        success: bool,
        error: str | None = None,
        screenshot_base64: str | None = None,
    ) -> None:
        """script_result 메시지 전송 (Runner가 기대하는 메시지 타입)."""
        client = self._ensure_client
        msg: dict[str, Any] = {
            "type": "script_result",
            "job_id": job_id,
            "step_id": step_id,
            "agent_id": client.agent_id,
            "status": "success" if success else "error",
            "error": error,
        }
        # 스크린샷이 있으면 Runner 형식에 맞게 추가
        if screenshot_base64:
            msg["screenshot"] = {
                "base64": screenshot_base64,
                "mime_type": "image/png",
            }
        await client.send_message(msg)

    async def _send_step_completed(
        self,
        job_id: int,
        step_id: int,
        success: bool,
        error: str | None = None,
    ) -> None:
        """step_completed 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "step_completed",
                "job_id": job_id,
                "step_id": step_id,
                "agent_id": client.agent_id,
                "success": success,
                "error": error,
            }
        )

    async def _send_goal_achieved(
        self,
        job_id: int,
        step_id: int,
        achieved: bool,
        reason: str | None = None,
    ) -> None:
        """goal_achieved 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "goal_achieved",
                "job_id": job_id,
                "step_id": step_id,
                "agent_id": client.agent_id,
                "achieved": achieved,
                "reason": reason,
            }
        )

    async def _send_job_completed(
        self,
        job_id: int,
        success: bool,
        total_steps: int,
        passed_steps: int,
        failed_steps: int,
        error: str | None = None,
    ) -> None:
        """job_completed 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "job_completed",
                "job_id": job_id,
                "agent_id": client.agent_id,
                "success": success,
                "total_steps": total_steps,
                "passed_steps": passed_steps,
                "failed_steps": failed_steps,
                "error": error,
            }
        )

    async def _send_error(
        self,
        job_id: int | None,
        step_id: int | None,
        error: str,
    ) -> None:
        """error 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "error",
                "job_id": job_id,
                "step_id": step_id,
                "agent_id": client.agent_id,
                "error": error,
            }
        )

    async def _send_job_cancelled(
        self,
        job_id: int,
        reason: str | None = None,
    ) -> None:
        """job_cancelled 메시지 전송."""
        client = self._ensure_client
        await client.send_message(
            {
                "type": "job_cancelled",
                "job_id": job_id,
                "agent_id": client.agent_id,
                "reason": reason,
            }
        )

    async def notify_jobs_reset(self, job_ids: list[int]) -> None:
        """Notify Runner about jobs that were reset due to reconnect.

        Called after successful reconnection to inform Runner about
        jobs that were terminated due to connection loss.

        Args:
            job_ids: List of job IDs that were reset
        """
        if not job_ids:
            return

        if not self._client:
            logger.warning("cannot_notify_reset_jobs_no_client")
            return

        for job_id in job_ids:
            try:
                await self._client.send_message(
                    {
                        "type": "job_failed",
                        "job_id": job_id,
                        "agent_id": self._client.agent_id,
                        "reason": "agent_reconnected",
                        "error": "Job terminated due to Agent reconnection",
                    }
                )
                logger.info(
                    "reset_job_notification_sent",
                    job_id=job_id,
                )
            except Exception as e:
                logger.error(
                    "failed_to_notify_reset_job",
                    job_id=job_id,
                    error=str(e),
                )
