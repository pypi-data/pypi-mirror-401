"""Pytest configuration and fixtures."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from playwright.async_api import Page

from nova_agent.browser.manager import BrowserManager
from nova_agent.browser.pool import BrowserPool
from nova_agent.config import ConfigManager
from nova_agent.executor.job_manager import JobManager
from nova_agent.models.job import Job, Scenario, Step
from nova_agent.websocket.client import AgentWebSocketClient


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """임시 설정 디렉토리."""
    config_dir = tmp_path / ".nova-agent"
    config_dir.mkdir(parents=True, exist_ok=True)
    yield config_dir


@pytest.fixture
def config_manager(temp_config_dir: Path) -> ConfigManager:
    """테스트용 ConfigManager."""
    manager = ConfigManager()
    manager._config_dir = temp_config_dir
    manager._token_file = temp_config_dir / "token"
    return manager


@pytest.fixture
def sample_token() -> str:
    """샘플 JWT 토큰."""
    # 테스트용 가짜 JWT (실제 서명 없음)
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZ2VudF9pZCI6ImFndF90ZXN0MTIzIiwicHJvamVjdF9pZCI6MX0.fake_signature"


@pytest.fixture
def sample_scenario() -> Scenario:
    """샘플 시나리오."""
    return Scenario(
        scenario_id=1,
        name="테스트 시나리오",
        entry_url="https://example.com",
        description="테스트용 시나리오입니다.",
    )


@pytest.fixture
def sample_steps() -> list[Step]:
    """샘플 Step 목록."""
    return [
        Step(
            step_id=1,
            step_order=1,
            goal="로그인 페이지로 이동",
            expected_result="로그인 폼이 표시됨",
        ),
        Step(
            step_id=2,
            step_order=2,
            goal="이메일 입력",
            expected_result="이메일이 입력됨",
        ),
        Step(
            step_id=3,
            step_order=3,
            goal="비밀번호 입력 후 로그인",
            expected_result="로그인 성공",
        ),
    ]


@pytest.fixture
def sample_job(sample_scenario: Scenario, sample_steps: list[Step]) -> Job:
    """샘플 Job."""
    return Job(
        job_id=1001,
        scenario=sample_scenario,
        steps=sample_steps,
    )


@pytest.fixture
def mock_page() -> MagicMock:
    """Mock Playwright Page."""
    page = MagicMock(spec=Page)
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Example Page")
    page.content = AsyncMock(return_value="<html><body>Test</body></html>")
    page.viewport_size = {"width": 1920, "height": 1080}
    page.goto = AsyncMock()
    page.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
    page.fill = AsyncMock()
    page.click = AsyncMock()
    page.query_selector = AsyncMock(return_value=None)
    page.query_selector_all = AsyncMock(return_value=[])
    page.set_default_timeout = MagicMock()
    page.close = AsyncMock()
    page.is_closed = MagicMock(return_value=False)
    return page


@pytest.fixture
def mock_browser_manager(mock_page: MagicMock) -> MagicMock:
    """Mock BrowserManager."""
    manager = MagicMock(spec=BrowserManager)
    manager.page = mock_page
    manager.is_running = True
    manager.start = AsyncMock()
    manager.stop = AsyncMock()
    manager.navigate = AsyncMock()
    manager.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
    manager.get_current_url = AsyncMock(return_value="https://example.com")
    manager.get_title = AsyncMock(return_value="Example Page")
    return manager


@pytest.fixture
def mock_browser_pool(mock_browser_manager: MagicMock) -> MagicMock:
    """Mock BrowserPool."""
    pool = MagicMock(spec=BrowserPool)
    pool.max_size = 1
    pool.active_count = 0
    pool.available_count = 1
    pool.acquire = AsyncMock(return_value=mock_browser_manager)
    pool.release = AsyncMock()
    pool.get_browser = MagicMock(return_value=mock_browser_manager)
    pool.shutdown = AsyncMock()
    return pool


@pytest.fixture
def mock_ws_client() -> MagicMock:
    """Mock WebSocket Client."""
    client = MagicMock(spec=AgentWebSocketClient)
    client.agent_id = "agt_test123"
    client.is_connected = True
    client.send_message = AsyncMock()
    client.close = AsyncMock()
    client._job_manager = MagicMock()
    client._job_manager.active_job_count = 0
    return client


@pytest.fixture
def job_manager(mock_browser_pool: MagicMock, mock_ws_client: MagicMock) -> JobManager:
    """테스트용 JobManager."""
    manager = JobManager(browser_pool=mock_browser_pool)
    manager.set_client(mock_ws_client)
    return manager


@pytest.fixture
def job_assign_message(sample_scenario: Scenario, sample_steps: list[Step]) -> dict:
    """샘플 job_assign 메시지."""
    return {
        "type": "job_assign",
        "job_id": 1001,
        "scenario": {
            "scenario_id": sample_scenario.scenario_id,
            "name": sample_scenario.name,
            "entry_url": sample_scenario.entry_url,
            "description": sample_scenario.description,
        },
        "steps": [
            {
                "step_id": s.step_id,
                "step_order": s.step_order,
                "goal": s.goal,
                "expected_result": s.expected_result,
            }
            for s in sample_steps
        ],
    }


@pytest.fixture
def execute_script_message() -> dict:
    """샘플 execute_script 메시지."""
    return {
        "type": "execute_script",
        "job_id": 1001,
        "step_id": 1,
        "script": "await page.fill('#email', 'test@example.com')",
    }
