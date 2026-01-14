"""CLI command tests."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from nova_agent.cli import app
from nova_agent.config import ConfigManager

runner = CliRunner()


class TestLoginCommand:
    """login 명령어 테스트."""

    def test_login_opens_browser(self, config_manager: ConfigManager) -> None:
        """login 명령이 브라우저를 여는지 확인."""
        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.webbrowser.open") as mock_open:
                with patch("nova_agent.cli.Prompt.ask", return_value="test_token"):
                    result = runner.invoke(app, ["login"])

                    mock_open.assert_called_once()
                    assert "agent/register" in mock_open.call_args[0][0]

    def test_login_saves_token(self, config_manager: ConfigManager) -> None:
        """입력받은 토큰이 올바르게 저장되는지 확인."""
        test_token = "eyJhbGciOiJIUzI1NiJ9.test.token"

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.webbrowser.open"):
                with patch("nova_agent.cli.Prompt.ask", return_value=test_token):
                    result = runner.invoke(app, ["login"])

                    # 토큰이 저장되었는지 확인
                    saved_token = config_manager.load_token()
                    assert saved_token == test_token

    def test_login_empty_token_fails(self, config_manager: ConfigManager) -> None:
        """빈 토큰 입력 시 실패."""
        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.webbrowser.open"):
                with patch("nova_agent.cli.Prompt.ask", return_value=""):
                    result = runner.invoke(app, ["login"])

                    assert result.exit_code == 1
                    assert "토큰이 입력되지 않았습니다" in result.output

    def test_login_with_existing_token_prompts(
        self, config_manager: ConfigManager, sample_token: str
    ) -> None:
        """이미 토큰이 있으면 확인 프롬프트."""
        config_manager.save_token(sample_token)

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.typer.confirm", return_value=False):
                result = runner.invoke(app, ["login"])

                assert "취소되었습니다" in result.output


class TestStartCommand:
    """start 명령어 테스트."""

    def test_start_requires_token(self, config_manager: ConfigManager) -> None:
        """토큰 없이 start 시 에러 발생 확인."""
        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            result = runner.invoke(app, ["start"])

            assert result.exit_code == 1
            assert "등록된 토큰이 없습니다" in result.output

    def test_start_with_token(
        self, config_manager: ConfigManager, sample_token: str
    ) -> None:
        """토큰이 있으면 에이전트 시작 시도."""
        config_manager.save_token(sample_token)

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.asyncio.run") as mock_run:
                # KeyboardInterrupt로 즉시 종료 시뮬레이션
                mock_run.side_effect = KeyboardInterrupt()

                result = runner.invoke(app, ["start"])

                # asyncio.run이 호출되었는지 확인
                mock_run.assert_called_once()
                assert "종료되었습니다" in result.output


class TestStatusCommand:
    """status 명령어 테스트."""

    def test_status_with_token(
        self, config_manager: ConfigManager, sample_token: str
    ) -> None:
        """토큰이 있을 때 상태 표시."""
        config_manager.save_token(sample_token)

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            result = runner.invoke(app, ["status"])

            assert "Agent 등록됨" in result.output

    def test_status_without_token(self, config_manager: ConfigManager) -> None:
        """토큰이 없을 때 상태 표시."""
        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            result = runner.invoke(app, ["status"])

            assert "Agent 미등록" in result.output


class TestLogoutCommand:
    """logout 명령어 테스트."""

    def test_logout_removes_token(
        self, config_manager: ConfigManager, sample_token: str
    ) -> None:
        """토큰 삭제 확인."""
        config_manager.save_token(sample_token)

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.typer.confirm", return_value=True):
                result = runner.invoke(app, ["logout"])

                assert "토큰이 삭제되었습니다" in result.output
                assert not config_manager.has_token()

    def test_logout_without_token(self, config_manager: ConfigManager) -> None:
        """토큰이 없을 때 logout."""
        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            result = runner.invoke(app, ["logout"])

            assert "등록된 토큰이 없습니다" in result.output

    def test_logout_cancelled(
        self, config_manager: ConfigManager, sample_token: str
    ) -> None:
        """로그아웃 취소."""
        config_manager.save_token(sample_token)

        with patch("nova_agent.cli.get_config_manager", return_value=config_manager):
            with patch("nova_agent.cli.typer.confirm", return_value=False):
                result = runner.invoke(app, ["logout"])

                assert "취소되었습니다" in result.output
                assert config_manager.has_token()


class TestVersionOption:
    """--version 옵션 테스트."""

    def test_version_output(self) -> None:
        """버전 출력 확인."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "Nova Agent" in result.output
