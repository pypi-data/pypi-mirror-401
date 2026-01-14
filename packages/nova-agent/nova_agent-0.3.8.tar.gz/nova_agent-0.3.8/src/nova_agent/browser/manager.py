"""Browser manager using Playwright."""

from __future__ import annotations

import asyncio
import contextlib
from typing import Any

import structlog
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    Request,
    Route,
    async_playwright,
)

from nova_agent.constants import ACTION_TIMEOUT, NAVIGATION_TIMEOUT
from nova_agent.settings import get_settings
from nova_agent.utils.domain_matcher import matches_any_domain_pattern

logger = structlog.get_logger(__name__)


class BrowserManager:
    """Playwright 브라우저 관리자.

    Chromium 브라우저를 관리하고 페이지를 제공합니다.

    Responsibilities:
        1. 브라우저 시작/종료
        2. 컨텍스트 및 페이지 관리
        3. 네비게이션
        4. 쿠키, localStorage, 헤더 설정
    """

    def __init__(
        self,
        headless: bool | None = None,
        viewport_width: int | None = None,
        viewport_height: int | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        """Initialize browser manager.

        Args:
            headless: 헤드리스 모드 여부
            viewport_width: 뷰포트 너비
            viewport_height: 뷰포트 높이
            config: 브라우저 설정 (쿠키, localStorage, 헤더, test_access_key 등)
        """
        settings = get_settings()
        self._headless = headless if headless is not None else settings.headless
        self._config = config or {}

        # config에서 viewport 설정이 있으면 우선 사용
        viewport_config = self._config.get("viewport", {})
        self._viewport_width = viewport_config.get("width") or viewport_width or settings.viewport_width
        self._viewport_height = viewport_config.get("height") or viewport_height or settings.viewport_height

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None  # 초기 페이지 (backward compatibility)
        self._active_page: Page | None = None  # 현재 활성 페이지 (탭/팝업 전환 지원)

    @property
    def page(self) -> Page | None:
        """현재 활성 페이지 (탭/팝업 전환 지원)."""
        return self._active_page or self._page

    @property
    def context(self) -> BrowserContext | None:
        """브라우저 컨텍스트."""
        return self._context

    @property
    def is_running(self) -> bool:
        """브라우저 실행 여부."""
        return self._browser is not None

    async def start(self) -> None:
        """브라우저 시작.

        Chromium 브라우저를 시작하고 새 페이지를 생성합니다.
        config에 따라 쿠키, localStorage, 헤더를 설정합니다.
        """
        if self._browser:
            logger.warning("browser_already_running")
            return

        logger.info(
            "starting_browser",
            headless=self._headless,
            has_config=bool(self._config),
        )

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self._headless,
        )

        # Context 옵션 설정
        context_options: dict[str, Any] = {
            "viewport": {
                "width": self._viewport_width,
                "height": self._viewport_height,
            },
        }

        # 일반 HTTP 헤더 설정 (test_access_key 제외, CORS 우회를 위해 route에서 처리)
        headers = self._config.get("headers", {})
        if headers:
            context_options["extra_http_headers"] = headers
            logger.info("headers_configured", count=len(headers))

        self._context = await self._browser.new_context(**context_options)

        # 쿠키 설정
        await self._setup_cookies()

        # 페이지 생성
        self._page = await self._context.new_page()
        self._page.set_default_timeout(ACTION_TIMEOUT)
        self._active_page = self._page  # 초기 활성 페이지 설정

        # localStorage 설정 (페이지 생성 후)
        await self._setup_local_storage()

        # test_access_key 헤더 설정 (page.route로 인터셉트)
        await self._setup_test_access_key_header()

        logger.info(
            "browser_started",
            viewport=f"{self._viewport_width}x{self._viewport_height}",
        )

    async def _setup_cookies(self) -> None:
        """쿠키 설정.

        Runner에서 전달받은 쿠키와 storage_state의 쿠키를 브라우저 컨텍스트에 추가합니다.
        storage_state 쿠키가 먼저 적용되고, 그 위에 scenario config 쿠키가 추가됩니다.
        """
        if not self._context:
            return

        # storage_state에서 쿠키 추출 (auth_state에서 온 쿠키)
        storage_state = self._config.get("storage_state")
        storage_state_cookies = []
        if storage_state and isinstance(storage_state, dict):
            storage_state_cookies = storage_state.get("cookies", [])

        # scenario config에서 쿠키 추출
        config_cookies = self._config.get("cookies", [])

        # 모든 쿠키가 없으면 종료
        if not storage_state_cookies and not config_cookies:
            return

        try:
            playwright_cookies = []

            # 1. storage_state 쿠키 추가 (이미 Playwright 형식)
            if storage_state_cookies:
                playwright_cookies.extend(storage_state_cookies)
                logger.info("storage_state_cookies_added", count=len(storage_state_cookies))

            # 2. scenario config 쿠키 변환 및 추가
            for cookie in config_cookies:
                pc = {
                    "name": cookie.get("name"),
                    "value": cookie.get("value"),
                    "domain": cookie.get("domain"),
                    "path": cookie.get("path", "/"),
                }
                # Optional fields
                if cookie.get("expires"):
                    pc["expires"] = cookie["expires"]
                if cookie.get("httpOnly") is not None:
                    pc["httpOnly"] = cookie["httpOnly"]
                if cookie.get("secure") is not None:
                    pc["secure"] = cookie["secure"]
                if cookie.get("sameSite"):
                    pc["sameSite"] = cookie["sameSite"]

                playwright_cookies.append(pc)

            if playwright_cookies:
                await self._context.add_cookies(playwright_cookies)
                logger.info("cookies_configured", total=len(playwright_cookies))
        except Exception as e:
            logger.warning("cookies_setup_failed", error=str(e))

    async def _setup_local_storage(self) -> None:
        """localStorage 설정.

        Runner에서 전달받은 localStorage와 storage_state의 localStorage를 페이지에 추가합니다.
        storage_state의 localStorage가 먼저 적용되고, 그 위에 scenario config localStorage가 추가됩니다.
        """
        if not self._page:
            return

        # storage_state에서 localStorage 추출
        storage_state = self._config.get("storage_state")
        storage_state_local_storage: list[dict[str, str]] = []
        if storage_state and isinstance(storage_state, dict):
            # storage_state.origins 형식: [{"origin": "https://...", "localStorage": [{"name": "key", "value": "val"}]}]
            for origin in storage_state.get("origins", []):
                for item in origin.get("localStorage", []):
                    storage_state_local_storage.append({
                        "key": item.get("name", ""),
                        "value": item.get("value", ""),
                    })

        # scenario config에서 localStorage 추출
        config_local_storage = self._config.get("local_storage", [])

        # 모든 localStorage가 없으면 종료
        all_items = storage_state_local_storage + config_local_storage
        if not all_items:
            return

        try:
            count = 0
            for item in all_items:
                key = item.get("key")
                value = item.get("value")
                if key and value is not None:
                    await self._page.evaluate(
                        """([key, value]) => {
                            localStorage.setItem(key, value);
                        }""",
                        [key, value],
                    )
                    count += 1

            logger.info(
                "local_storage_configured",
                total=count,
                from_storage_state=len(storage_state_local_storage),
                from_config=len(config_local_storage),
            )
        except Exception as e:
            logger.warning("local_storage_setup_failed", error=str(e))

    async def _setup_test_access_key_header(self) -> None:
        """test_access_key 헤더 설정.

        Runner에서 복호화하여 전달한 test_access_key를 특정 도메인에만 헤더로 추가합니다.
        CORS를 우회하기 위해 page.route()를 사용합니다.
        """
        test_access_key = self._config.get("test_access_key")
        test_access_key_domains = self._config.get("test_access_key_domains")

        if not test_access_key or not test_access_key_domains or not self._page:
            return

        try:
            key_to_add = test_access_key
            domains_to_match = test_access_key_domains

            async def add_test_access_key_header(route: Route, request: Request) -> None:
                """요청을 인터셉트하여 도메인이 매칭되면 헤더 추가."""
                if matches_any_domain_pattern(request.url, domains_to_match):
                    new_headers = {
                        **request.headers,
                        "X-QANOVA-TEST-KEY": key_to_add,
                    }
                    await route.continue_(headers=new_headers)
                else:
                    await route.continue_()

            await self._page.route("**/*", add_test_access_key_header)
            logger.info(
                "test_access_key_header_configured",
                domain_patterns=domains_to_match,
            )
        except Exception as e:
            logger.warning("test_access_key_setup_failed", error=str(e))

    async def stop(self) -> None:
        """브라우저 종료."""
        self._active_page = None  # 활성 페이지 참조 해제

        if self._page:
            await self._page.close()
            self._page = None

        if self._context:
            await self._context.close()
            self._context = None

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        logger.info("browser_stopped")

    async def navigate(self, url: str) -> None:
        """URL로 이동.

        Args:
            url: 이동할 URL

        Raises:
            RuntimeError: 브라우저가 실행 중이 아닐 때
        """
        if not self._page:
            raise RuntimeError("Browser not started")

        logger.debug("navigating", url=url)
        await self._page.goto(url, wait_until="load", timeout=NAVIGATION_TIMEOUT)
        logger.info("navigated", url=url, title=await self._page.title())

    async def get_current_url(self) -> str:
        """현재 URL 반환."""
        if not self._page:
            raise RuntimeError("Browser not started")
        return self._page.url

    async def get_title(self) -> str:
        """현재 페이지 타이틀 반환."""
        if not self._page:
            raise RuntimeError("Browser not started")
        return await self._page.title()

    async def screenshot(self, full_page: bool = False) -> bytes:
        """스크린샷 촬영.

        Args:
            full_page: 전체 페이지 스크린샷 여부

        Returns:
            스크린샷 PNG 바이트
        """
        if not self._page:
            raise RuntimeError("Browser not started")

        return await self._page.screenshot(full_page=full_page)

    async def new_page(self) -> Page:
        """새 페이지 생성.

        Returns:
            새로 생성된 페이지
        """
        if not self._context:
            raise RuntimeError("Browser not started")

        page = await self._context.new_page()
        page.set_default_timeout(ACTION_TIMEOUT)
        return page

    async def close_page(self, page: Page) -> None:
        """페이지 닫기.

        Args:
            page: 닫을 페이지
        """
        if page and not page.is_closed():
            await page.close()

    # ========================================================================
    # 탭/팝업 관리 메서드 (Cloud 모드와 동일한 동작)
    # ========================================================================

    def get_all_pages(self) -> list[Page]:
        """모든 열린 페이지 반환.

        Returns:
            열린 페이지 리스트
        """
        if not self._context:
            return []
        return [p for p in self._context.pages if not p.is_closed()]

    def switch_to_page(self, page: Page) -> None:
        """활성 페이지 전환.

        Args:
            page: 전환할 페이지
        """
        if page and not page.is_closed():
            self._active_page = page
            logger.info(
                "switched_to_page",
                url=page.url,
                page_count=len(self.get_all_pages()),
            )

    async def detect_and_switch_to_new_page(
        self,
        pages_before: set[Page],
        timeout: float = 3.0,
        poll_interval: float = 0.1,
    ) -> Page | None:
        """새로 열린 탭/팝업 감지 및 자동 전환.

        스크립트 실행 후 호출하여 새 탭이 열렸는지 확인하고,
        열렸다면 해당 탭으로 자동 전환합니다.

        Args:
            pages_before: 스크립트 실행 전 페이지 집합
            timeout: 새 탭 감지 최대 대기 시간 (초)
            poll_interval: 폴링 간격 (초)

        Returns:
            새로 열린 페이지 (없으면 None)
        """
        if not self._context:
            return None

        async def _detect_new_pages() -> set[Page]:
            max_attempts = int(timeout / poll_interval)
            for _ in range(max_attempts):
                await asyncio.sleep(poll_interval)
                pages_after = set(self._context.pages) if self._context else set()
                newly_opened = pages_after - pages_before
                # 닫히지 않은 새 페이지만 필터링
                newly_opened = {p for p in newly_opened if not p.is_closed()}
                if newly_opened:
                    return newly_opened
            return set()

        try:
            newly_opened = await asyncio.wait_for(
                _detect_new_pages(),
                timeout=timeout + 1.0,  # 여유 시간 추가
            )

            if newly_opened:
                # 가장 최근에 열린 페이지로 전환
                new_page = list(newly_opened)[-1]

                # 새 탭이 로드될 때까지 대기 (실패해도 계속 진행)
                with contextlib.suppress(Exception):
                    await new_page.wait_for_load_state("domcontentloaded", timeout=5000)

                self.switch_to_page(new_page)
                logger.info(
                    "new_tab_detected_and_switched",
                    new_url=new_page.url,
                    new_pages_count=len(newly_opened),
                )
                return new_page

        except TimeoutError:
            pass

        return None

    async def handle_page_closed(self) -> bool:
        """현재 페이지가 닫혔는지 확인하고 다른 페이지로 전환.

        Returns:
            True if switched to another page, False if no pages available
        """
        active = self._active_page or self._page
        if active and active.is_closed():
            pages = self.get_all_pages()
            if pages:
                # 가장 최근 페이지로 전환
                fallback_page = pages[-1]
                self.switch_to_page(fallback_page)
                logger.info(
                    "page_closed_switched_to_fallback",
                    fallback_url=fallback_page.url,
                    remaining_pages=len(pages),
                )
                return True
            else:
                logger.warning("all_pages_closed")
                self._active_page = None
                return False
        return True  # 페이지가 닫히지 않았으면 True
