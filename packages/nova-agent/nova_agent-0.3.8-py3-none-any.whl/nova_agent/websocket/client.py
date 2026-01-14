"""WebSocket client for Agent-Gateway communication."""

from __future__ import annotations

import asyncio
import contextlib
import platform
from typing import TYPE_CHECKING, Any

import orjson
import structlog
import websockets

from nova_agent import __version__
from websockets import ClientConnection
from websockets.exceptions import InvalidStatus

from nova_agent.constants import (
    MSG_REGISTER,
    MSG_REGISTERED,
    WS_PING_INTERVAL,
    WS_PING_TIMEOUT,
)
from nova_agent.settings import get_settings, is_verbose
from nova_agent.websocket.handlers import MessageHandler
from nova_agent.websocket.heartbeat import HeartbeatManager

if TYPE_CHECKING:
    from nova_agent.executor.job_manager import JobManager

logger = structlog.get_logger(__name__)


class AuthenticationError(Exception):
    """인증 실패 예외 (401, 403 등)."""

    pass


class AgentWebSocketClient:
    """Agent WebSocket 클라이언트.

    Gateway와의 WebSocket 연결을 관리하고 메시지를 송수신합니다.

    Responsibilities:
        1. WebSocket 연결 관리 (연결/재연결)
        2. 메시지 송수신
        3. Heartbeat 관리
        4. 메시지 핸들러에 위임
    """

    def __init__(
        self,
        gateway_url: str,
        token: str,
        job_manager: JobManager,
    ) -> None:
        """Initialize WebSocket client.

        Args:
            gateway_url: Gateway WebSocket URL
            token: JWT 인증 토큰
            job_manager: Job 관리자
        """
        self._gateway_url = gateway_url
        self._token = token
        self._job_manager = job_manager
        self._settings = get_settings()

        self._ws: ClientConnection | None = None
        self._agent_id: str | None = None
        self._connected = False
        self._running = False

        self._heartbeat: HeartbeatManager | None = None
        self._handler: MessageHandler | None = None
        self._job_timeout_task: asyncio.Task[None] | None = None

        self._reconnect_attempts = 0

    @property
    def agent_id(self) -> str | None:
        """Agent ID."""
        return self._agent_id

    @property
    def is_connected(self) -> bool:
        """연결 상태."""
        return self._connected and self._ws is not None

    async def connect_and_run(self) -> None:
        """Gateway에 연결하고 메인 루프 실행.

        재연결 로직을 포함합니다.
        """
        self._running = True
        pending_reset_jobs: list[int] = []

        while self._running:
            try:
                await self._connect()

                # 재연결 성공 후 reset된 Job들에 대해 Runner에 알림
                if pending_reset_jobs:
                    logger.info(
                        "notifying_reset_jobs_after_reconnect",
                        job_ids=pending_reset_jobs,
                    )
                    await self._job_manager.notify_jobs_reset(pending_reset_jobs)
                    pending_reset_jobs = []

                await self._run_message_loop()
            except AuthenticationError:
                # 인증 실패는 재연결해도 의미 없음 - 즉시 종료
                self._running = False
                return
            except websockets.ConnectionClosed as e:
                logger.warning(
                    "websocket_connection_closed",
                    code=e.code,
                    reason=e.reason,
                )
            except Exception as e:
                logger.error("websocket_error", error=str(e), exc_info=is_verbose())

            # 재연결 시도
            if self._running:
                pending_reset_jobs = await self._handle_reconnect()

    async def _connect(self) -> None:
        """Gateway에 연결.

        Raises:
            ConnectionError: 연결 실패 시
        """
        # 토큰을 쿼리 파라미터로 추가
        separator = "&" if "?" in self._gateway_url else "?"
        connect_url = f"{self._gateway_url}{separator}token={self._token}"

        logger.info("connecting_to_gateway", url=self._gateway_url)

        try:
            self._ws = await asyncio.wait_for(
                websockets.connect(
                    connect_url,
                    ping_interval=WS_PING_INTERVAL,
                    ping_timeout=WS_PING_TIMEOUT,
                ),
                timeout=self._settings.connection_timeout,
            )
            logger.debug("websocket_connected")

            # registered 대기 (서버가 연결 성공 시 전송)
            await self._wait_for_registered()

            self._connected = True
            self._reconnect_attempts = 0

            # Heartbeat 시작
            self._heartbeat = HeartbeatManager(self)
            await self._heartbeat.start()

            # 메시지 핸들러 초기화
            self._handler = MessageHandler(
                client=self,
                job_manager=self._job_manager,
            )

            # Job 타임아웃 모니터 시작
            self._job_timeout_task = asyncio.create_task(self._run_job_timeout_monitor())

            logger.info(
                "agent_connected_to_gateway",
                agent_id=self._agent_id,
            )

        except TimeoutError as e:
            logger.error("connection_timeout", url=self._gateway_url)
            raise ConnectionError(f"Connection timeout: {self._gateway_url}") from e
        except InvalidStatus as e:
            status_code = e.response.status_code
            if status_code in (401, 403):
                logger.error(
                    "authentication_failed",
                    status_code=status_code,
                    message="Token is invalid or expired. Please run 'nova-agent login' to re-authenticate.",
                )
                raise AuthenticationError(
                    "Token is invalid or expired. Please run 'nova-agent login' to re-authenticate."
                ) from e
            logger.error("connection_failed", error=str(e))
            raise ConnectionError(f"Connection failed: {e}") from e
        except Exception as e:
            logger.error("connection_failed", error=str(e))
            raise ConnectionError(f"Connection failed: {e}") from e

    async def _send_register_info(self) -> None:
        """Send system information to Gateway after registration."""
        register_msg = {
            "type": MSG_REGISTER,
            "os": platform.system().lower(),  # "darwin", "linux", "windows"
            "arch": platform.machine(),  # "arm64", "x86_64"
            "agent_version": __version__,
            "python_version": platform.python_version(),
            "browsers": ["chromium"],
        }
        await self.send_message(register_msg)
        logger.info(
            "register_info_sent",
            os=register_msg["os"],
            arch=register_msg["arch"],
            agent_version=register_msg["agent_version"],
        )

    async def _wait_for_registered(self) -> None:
        """registered 응답 대기.

        Raises:
            ConnectionError: 인증 실패 시
        """
        if not self._ws:
            raise ConnectionError("WebSocket not connected")

        try:
            raw = await asyncio.wait_for(
                self._ws.recv(),
                timeout=self._settings.connection_timeout,
            )
            data = orjson.loads(raw)
            logger.debug("received_message", type=data.get("type"))

            if data.get("type") == MSG_REGISTERED:
                self._agent_id = data.get("agent_id")
                logger.info(
                    "agent_registered",
                    agent_id=self._agent_id,
                    project_id=data.get("project_id"),
                )

                # Send system info to Gateway
                await self._send_register_info()
            elif data.get("type") == "error":
                error = data.get("message", data.get("error", "Unknown error"))
                logger.error("authentication_failed", error=error)
                raise ConnectionError(f"Authentication failed: {error}")
            else:
                logger.error("unexpected_response", type=data.get("type"))
                raise ConnectionError(f"Unexpected response: {data.get('type')}")

        except TimeoutError as e:
            logger.error("auth_response_timeout")
            raise ConnectionError("Authentication response timeout") from e

    async def _run_message_loop(self) -> None:
        """메시지 수신 루프."""
        if not self._ws or not self._handler:
            return

        logger.info("message_loop_started")

        async for raw in self._ws:
            if not self._running:
                break

            try:
                data = orjson.loads(raw)
                logger.debug("message_received", type=data.get("type"))
                await self._handler.handle_message(data)
            except orjson.JSONDecodeError as e:
                logger.error("json_decode_error", error=str(e))
            except Exception as e:
                logger.error("message_handling_error", error=str(e), exc_info=is_verbose())

    async def _handle_reconnect(self) -> list[int]:
        """재연결 처리.

        Returns:
            List of job IDs that were reset (to notify Runner after reconnect)
        """
        self._connected = False

        if self._heartbeat:
            await self._heartbeat.stop()
            self._heartbeat = None

        # Job 타임아웃 모니터 중지
        if self._job_timeout_task:
            self._job_timeout_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._job_timeout_task
            self._job_timeout_task = None

        # 재연결 시 이전 Job 상태 및 브라우저 정리
        # Gateway가 재시작되었거나 연결이 끊겼다면 이전 Job 컨텍스트는 유효하지 않음
        reset_job_ids = await self._job_manager.reset()

        self._reconnect_attempts += 1

        # 0 = 무한 재시도
        max_attempts = self._settings.max_reconnect_attempts
        if max_attempts > 0 and self._reconnect_attempts > max_attempts:
            logger.error(
                "max_reconnect_attempts_exceeded",
                attempts=self._reconnect_attempts,
            )
            self._running = False
            return []

        # 최대 60초까지만 증가
        delay = min(self._settings.reconnect_delay * self._reconnect_attempts, 60)
        logger.info(
            "reconnecting",
            attempt=self._reconnect_attempts,
            delay=delay,
            reset_jobs=reset_job_ids,
        )
        await asyncio.sleep(delay)

        return reset_job_ids

    async def _run_job_timeout_monitor(self) -> None:
        """Job 타임아웃 모니터링.

        주기적으로 Job의 유휴 시간을 체크하여 타임아웃된 Job을 정리합니다.
        """
        check_interval = 30  # 30초마다 체크

        logger.debug(
            "job_timeout_monitor_started",
            timeout_seconds=self._settings.job_timeout,
            check_interval=check_interval,
        )

        try:
            while self._running and self._connected:
                await asyncio.sleep(check_interval)

                timed_out = await self._job_manager.check_timeouts(self._settings.job_timeout)
                if timed_out:
                    logger.info(
                        "jobs_timed_out",
                        job_ids=timed_out,
                        timeout_seconds=self._settings.job_timeout,
                    )
        except asyncio.CancelledError:
            logger.debug("job_timeout_monitor_cancelled")
            raise

    async def send_message(self, message: dict[str, Any]) -> None:
        """메시지 전송.

        Args:
            message: 전송할 메시지

        Raises:
            ConnectionError: 연결되지 않은 경우
        """
        if not self._ws:
            raise ConnectionError("WebSocket not connected")

        raw = orjson.dumps(message).decode()
        await self._ws.send(raw)
        logger.debug("message_sent", type=message.get("type"))

    async def close(self) -> None:
        """연결 종료."""
        self._running = False
        self._connected = False

        if self._heartbeat:
            await self._heartbeat.stop()

        # Job 타임아웃 모니터 중지
        if self._job_timeout_task:
            self._job_timeout_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._job_timeout_task
            self._job_timeout_task = None

        if self._ws:
            await self._ws.close()
            self._ws = None

        logger.info("websocket_closed")
