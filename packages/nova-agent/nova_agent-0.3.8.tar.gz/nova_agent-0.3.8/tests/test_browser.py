"""Browser manager and DOM extractor tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from nova_agent.browser.dom_extractor import DomExtractor
from nova_agent.browser.manager import BrowserManager
from nova_agent.executor.script_runner import ScriptRunner


class TestBrowserManager:
    """BrowserManager 테스트."""

    def test_initialization(self) -> None:
        """초기화 테스트."""
        manager = BrowserManager(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
        )

        assert manager._headless is True
        assert manager._viewport_width == 1280
        assert manager._viewport_height == 720
        assert manager._browser is None
        assert manager.is_running is False

    def test_page_property_before_start(self) -> None:
        """시작 전 page 프로퍼티."""
        manager = BrowserManager()
        assert manager.page is None

    @pytest.mark.asyncio
    async def test_navigate_without_browser(self) -> None:
        """브라우저 없이 navigate 시 에러."""
        manager = BrowserManager()

        with pytest.raises(RuntimeError, match="Browser not started"):
            await manager.navigate("https://example.com")

    @pytest.mark.asyncio
    async def test_screenshot_without_browser(self) -> None:
        """브라우저 없이 screenshot 시 에러."""
        manager = BrowserManager()

        with pytest.raises(RuntimeError, match="Browser not started"):
            await manager.screenshot()

    @pytest.mark.asyncio
    async def test_get_current_url_without_browser(self) -> None:
        """브라우저 없이 get_current_url 시 에러."""
        manager = BrowserManager()

        with pytest.raises(RuntimeError, match="Browser not started"):
            await manager.get_current_url()


class TestDomExtractor:
    """DomExtractor 테스트."""

    @pytest.fixture
    def extractor(self, mock_page: MagicMock) -> DomExtractor:
        """테스트용 DOM 추출기."""
        return DomExtractor(mock_page)

    @pytest.mark.asyncio
    async def test_extract_basic(self, extractor: DomExtractor) -> None:
        """기본 DOM 추출."""
        dom = await extractor.extract()

        assert dom["url"] == "https://example.com"
        assert dom["title"] == "Example Page"
        assert "<html>" in dom["html"]
        assert "timestamp" in dom
        assert dom["viewport"] == {"width": 1920, "height": 1080}

    @pytest.mark.asyncio
    async def test_extract_element_not_found(
        self, extractor: DomExtractor, mock_page: MagicMock
    ) -> None:
        """요소를 찾지 못했을 때."""
        mock_page.query_selector = AsyncMock(return_value=None)

        result = await extractor.extract_element("#nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_extract_element_found(
        self, extractor: DomExtractor, mock_page: MagicMock
    ) -> None:
        """요소를 찾았을 때."""
        mock_element = MagicMock()
        mock_element.evaluate = AsyncMock(return_value="<button>Click</button>")
        mock_element.inner_text = AsyncMock(return_value="Click")
        mock_element.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 200, "width": 80, "height": 30}
        )

        mock_page.query_selector = AsyncMock(return_value=mock_element)

        result = await extractor.extract_element("button")

        assert result is not None
        assert result["selector"] == "button"
        assert result["inner_text"] == "Click"
        assert result["bounding_box"]["x"] == 100

    @pytest.mark.asyncio
    async def test_extract_interactive_elements(
        self, extractor: DomExtractor, mock_page: MagicMock
    ) -> None:
        """상호작용 요소 추출."""
        # 빈 목록 반환 설정
        mock_page.query_selector_all = AsyncMock(return_value=[])

        elements = await extractor.extract_interactive_elements()

        assert isinstance(elements, list)
        # query_selector_all이 각 선택자에 대해 호출되었는지 확인
        assert mock_page.query_selector_all.called


class TestScriptRunner:
    """ScriptRunner 테스트."""

    @pytest.fixture
    def runner(self, mock_page: MagicMock) -> ScriptRunner:
        """테스트용 스크립트 러너."""
        return ScriptRunner(mock_page)

    @pytest.mark.asyncio
    async def test_run_simple_script(
        self, runner: ScriptRunner, mock_page: MagicMock
    ) -> None:
        """간단한 스크립트 실행."""
        mock_page.fill = AsyncMock()

        result = await runner.run("await page.fill('#email', 'test@example.com')")

        assert result["success"] is True
        assert "duration_ms" in result

    @pytest.mark.asyncio
    async def test_run_script_error(
        self, runner: ScriptRunner, mock_page: MagicMock
    ) -> None:
        """스크립트 실행 에러."""
        mock_page.fill = AsyncMock(side_effect=Exception("Element not found"))

        result = await runner.run("await page.fill('#nonexistent', 'test')")

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.asyncio
    async def test_run_action_click(
        self, runner: ScriptRunner, mock_page: MagicMock
    ) -> None:
        """클릭 액션."""
        mock_page.click = AsyncMock()

        result = await runner.run_action("click", selector="#button")

        assert result["success"] is True
        mock_page.click.assert_called_once_with("#button")

    @pytest.mark.asyncio
    async def test_run_action_fill(
        self, runner: ScriptRunner, mock_page: MagicMock
    ) -> None:
        """입력 액션."""
        mock_page.fill = AsyncMock()

        result = await runner.run_action("fill", selector="#input", value="hello")

        assert result["success"] is True
        mock_page.fill.assert_called_once_with("#input", "hello")

    @pytest.mark.asyncio
    async def test_run_action_unknown(self, runner: ScriptRunner) -> None:
        """알 수 없는 액션."""
        result = await runner.run_action("unknown_action")

        assert result["success"] is False
        assert "Unknown action" in result["error"]


class TestJobManagerIntegration:
    """JobManager 통합 테스트."""

    @pytest.mark.asyncio
    async def test_accept_job(
        self,
        mock_browser_pool: MagicMock,
        mock_browser_manager: MagicMock,
        mock_ws_client: MagicMock,
        job_assign_message: dict,
    ) -> None:
        """Job 수락."""
        from nova_agent.executor.job_manager import JobManager
        from nova_agent.models.messages import JobAssignMessage

        # 실제 JobManager 인스턴스 사용
        manager = JobManager(browser_pool=mock_browser_pool)
        manager.set_client(mock_ws_client)

        message = JobAssignMessage(**job_assign_message)
        await manager.accept_job(message)

        # job_accepted 메시지 전송 확인 (첫 번째 호출)
        assert mock_ws_client.send_message.called
        # 여러 메시지가 전송됨 (job_accepted, step_started)
        calls = mock_ws_client.send_message.call_args_list
        first_message = calls[0][0][0]
        assert first_message["type"] == "job_accepted"
        assert first_message["job_id"] == 1001

    @pytest.mark.asyncio
    async def test_accept_job_already_exists(
        self,
        mock_browser_pool: MagicMock,
        mock_browser_manager: MagicMock,
        mock_ws_client: MagicMock,
        job_assign_message: dict,
    ) -> None:
        """이미 동일한 Job ID가 존재할 때."""
        from nova_agent.executor.job_manager import JobManager
        from nova_agent.executor.job_session import JobSession
        from nova_agent.models.job import Job, Scenario
        from nova_agent.models.messages import JobAssignMessage

        manager = JobManager(browser_pool=mock_browser_pool)
        manager.set_client(mock_ws_client)

        # 이미 존재하는 Job 세션 설정
        existing_job = Job(
            job_id=1001,  # 동일한 job_id
            scenario=Scenario(
                scenario_id=1,
                name="Running",
                entry_url="https://example.com",
            ),
            steps=[],
        )
        manager._sessions[1001] = JobSession(
            job_id=1001,
            job=existing_job,
            browser_manager=mock_browser_manager,
        )

        message = JobAssignMessage(**job_assign_message)
        await manager.accept_job(message)

        # job_assign_failed 메시지 전송 확인
        sent_message = mock_ws_client.send_message.call_args[0][0]
        assert sent_message["type"] == "job_assign_failed"
