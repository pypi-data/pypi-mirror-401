"""WebSocket client and handler tests."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from nova_agent.models.messages import (
    ExecuteScriptMessage,
    JobAssignMessage,
    parse_message,
)
from nova_agent.websocket.client import AgentWebSocketClient
from nova_agent.websocket.handlers import MessageHandler
from nova_agent.websocket.heartbeat import HeartbeatManager


class TestAgentWebSocketClient:
    """AgentWebSocketClient 테스트."""

    @pytest.fixture
    def ws_client(self, mock_browser_pool: MagicMock) -> AgentWebSocketClient:
        """테스트용 WebSocket 클라이언트."""
        from nova_agent.executor.job_manager import JobManager

        job_manager = JobManager(browser_pool=mock_browser_pool)

        client = AgentWebSocketClient(
            gateway_url="wss://test.gateway.com/ws",
            token="test_token",
            job_manager=job_manager,
        )
        return client

    def test_client_initialization(self, ws_client: AgentWebSocketClient) -> None:
        """클라이언트 초기화 테스트."""
        assert ws_client._gateway_url == "wss://test.gateway.com/ws"
        assert ws_client._token == "test_token"
        assert ws_client._connected is False
        assert ws_client._agent_id is None

    def test_is_connected_property(self, ws_client: AgentWebSocketClient) -> None:
        """is_connected 프로퍼티 테스트."""
        assert ws_client.is_connected is False

        ws_client._connected = True
        ws_client._ws = MagicMock()
        assert ws_client.is_connected is True

    @pytest.mark.asyncio
    async def test_send_message(self, ws_client: AgentWebSocketClient) -> None:
        """메시지 전송 테스트."""
        mock_ws = MagicMock()
        mock_ws.send = AsyncMock()
        ws_client._ws = mock_ws

        await ws_client.send_message({"type": "test", "data": "hello"})

        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_message_without_connection(
        self, ws_client: AgentWebSocketClient
    ) -> None:
        """연결 없이 메시지 전송 시 에러."""
        with pytest.raises(ConnectionError):
            await ws_client.send_message({"type": "test"})

    @pytest.mark.asyncio
    async def test_close(self, ws_client: AgentWebSocketClient) -> None:
        """연결 종료 테스트."""
        mock_ws = MagicMock()
        mock_ws.close = AsyncMock()
        ws_client._ws = mock_ws
        ws_client._running = True
        ws_client._connected = True

        await ws_client.close()

        assert ws_client._running is False
        assert ws_client._connected is False
        mock_ws.close.assert_called_once()


class TestMessageHandler:
    """MessageHandler 테스트."""

    @pytest.fixture
    def handler(
        self, mock_ws_client: MagicMock, job_manager: MagicMock
    ) -> MessageHandler:
        """테스트용 메시지 핸들러."""
        return MessageHandler(
            client=mock_ws_client,
            job_manager=job_manager,
        )

    @pytest.mark.asyncio
    async def test_handle_job_assign(
        self, handler: MessageHandler, job_assign_message: dict
    ) -> None:
        """job_assign 처리 테스트."""
        handler._job_manager.accept_job = AsyncMock()

        await handler.handle_message(job_assign_message)

        handler._job_manager.accept_job.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_execute_script(
        self, handler: MessageHandler, execute_script_message: dict
    ) -> None:
        """execute_script 처리 테스트."""
        handler._job_manager.execute_script = AsyncMock()

        await handler.handle_message(execute_script_message)

        handler._job_manager.execute_script.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_unknown_message_type(self, handler: MessageHandler) -> None:
        """알 수 없는 메시지 타입."""
        unknown_message = {"type": "unknown_type", "data": "test"}

        # 에러 없이 처리되어야 함
        await handler.handle_message(unknown_message)

    @pytest.mark.asyncio
    async def test_handle_message_without_type(self, handler: MessageHandler) -> None:
        """type 없는 메시지."""
        invalid_message = {"data": "test"}

        # 에러 없이 처리되어야 함 (경고 로그만)
        await handler.handle_message(invalid_message)


class TestHeartbeatManager:
    """HeartbeatManager 테스트."""

    @pytest.fixture
    def heartbeat_manager(self, mock_ws_client: MagicMock) -> HeartbeatManager:
        """테스트용 Heartbeat 매니저."""
        return HeartbeatManager(client=mock_ws_client, interval=0.1)  # 빠른 테스트용

    @pytest.mark.asyncio
    async def test_heartbeat_start_stop(
        self, heartbeat_manager: HeartbeatManager
    ) -> None:
        """Heartbeat 시작/중지 테스트."""
        assert heartbeat_manager._running is False

        await heartbeat_manager.start()
        assert heartbeat_manager._running is True
        assert heartbeat_manager._task is not None

        await heartbeat_manager.stop()
        assert heartbeat_manager._running is False

    @pytest.mark.asyncio
    async def test_heartbeat_sends_message(
        self, heartbeat_manager: HeartbeatManager, mock_ws_client: MagicMock
    ) -> None:
        """Heartbeat 메시지 전송 확인."""
        await heartbeat_manager.start()

        # 짧은 대기 후 heartbeat 전송 확인
        await asyncio.sleep(0.15)

        await heartbeat_manager.stop()

        # send_message가 호출되었는지 확인
        assert mock_ws_client.send_message.called

    @pytest.mark.asyncio
    async def test_heartbeat_skipped_without_agent_id(
        self, mock_ws_client: MagicMock
    ) -> None:
        """agent_id 없을 때 heartbeat 스킵."""
        mock_ws_client.agent_id = None
        heartbeat_manager = HeartbeatManager(client=mock_ws_client, interval=0.1)

        await heartbeat_manager.start()
        await asyncio.sleep(0.15)
        await heartbeat_manager.stop()

        # send_message가 호출되지 않아야 함
        mock_ws_client.send_message.assert_not_called()


class TestMessageParsing:
    """메시지 파싱 테스트."""

    def test_parse_job_assign(self, job_assign_message: dict) -> None:
        """job_assign 메시지 파싱."""
        message = parse_message(job_assign_message)

        assert isinstance(message, JobAssignMessage)
        assert message.job_id == 1001
        assert message.scenario["name"] == "테스트 시나리오"

    def test_parse_execute_script(self, execute_script_message: dict) -> None:
        """execute_script 메시지 파싱."""
        message = parse_message(execute_script_message)

        assert isinstance(message, ExecuteScriptMessage)
        assert message.job_id == 1001
        assert message.step_id == 1
        assert "page.fill" in message.script

    def test_parse_unknown_type(self) -> None:
        """알 수 없는 타입 파싱."""
        unknown = {"type": "unknown", "data": "test"}
        message = parse_message(unknown)

        assert message.type == "unknown"

    def test_parse_without_type_raises(self) -> None:
        """type 없으면 에러."""
        with pytest.raises(ValueError, match="Message type is required"):
            parse_message({"data": "test"})
