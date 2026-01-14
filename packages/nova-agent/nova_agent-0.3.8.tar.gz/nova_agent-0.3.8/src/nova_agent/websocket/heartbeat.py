"""Heartbeat manager for WebSocket connection."""

from __future__ import annotations

import asyncio
import contextlib
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import structlog

from nova_agent.constants import MSG_HEARTBEAT
from nova_agent.settings import get_settings
from nova_agent.utils.system_info import get_cpu_usage_percent, get_memory_usage_mb

if TYPE_CHECKING:
    from nova_agent.websocket.client import AgentWebSocketClient

logger = structlog.get_logger(__name__)


class HeartbeatManager:
    """Heartbeat 관리자.

    주기적으로 heartbeat 메시지를 전송하여 연결을 유지합니다.
    Gateway는 60초 이상 heartbeat가 없으면 연결을 종료합니다.
    """

    def __init__(
        self,
        client: AgentWebSocketClient,
        interval: float | None = None,
    ) -> None:
        """Initialize heartbeat manager.

        Args:
            client: WebSocket 클라이언트
            interval: Heartbeat 간격 (초)
        """
        self._client = client
        self._interval = interval or get_settings().heartbeat_interval
        self._task: asyncio.Task[None] | None = None
        self._running = False

    async def start(self) -> None:
        """Heartbeat 시작."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._heartbeat_loop())
        logger.debug("heartbeat_started", interval=self._interval)

    async def stop(self) -> None:
        """Heartbeat 중지."""
        self._running = False

        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

        logger.debug("heartbeat_stopped")

    async def _heartbeat_loop(self) -> None:
        """Heartbeat 루프."""
        while self._running:
            try:
                await asyncio.sleep(self._interval)

                if not self._running:
                    break

                await self._send_heartbeat()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("heartbeat_error", error=str(e))
                # 에러가 발생해도 계속 시도

    async def _send_heartbeat(self) -> None:
        """Heartbeat 메시지 전송."""
        if not self._client.agent_id:
            logger.warning("heartbeat_skipped_no_agent_id")
            return

        # 시스템 정보 수집
        system_info = {
            "cpu_usage": get_cpu_usage_percent(),
            "memory_usage_mb": get_memory_usage_mb(),
        }

        message = {
            "type": MSG_HEARTBEAT,
            "agent_id": self._client.agent_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "idle" if self._client._job_manager.active_job_count == 0 else "running",
            "system_info": system_info,
        }

        try:
            await self._client.send_message(message)
            logger.debug("heartbeat_sent", system_info=system_info)
        except Exception as e:
            logger.error("heartbeat_send_failed", error=str(e))
            raise
