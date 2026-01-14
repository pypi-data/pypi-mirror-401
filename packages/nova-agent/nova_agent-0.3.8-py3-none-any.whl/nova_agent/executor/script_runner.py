"""Script runner for executing Playwright scripts."""

from __future__ import annotations

import asyncio
import datetime as datetime_module
import re
import time as time_module
from typing import Any

import structlog
from playwright.async_api import Page

from nova_agent.settings import get_settings

logger = structlog.get_logger(__name__)


# =============================================================================
# Canvas Helper Functions (Cloud 모드와 동일)
# =============================================================================


async def click_canvas(
    page: Page,
    selector: str,
    x_percent: float,
    y_percent: float,
) -> None:
    """
    Canvas 요소 내 상대 좌표(%)를 클릭.

    Args:
        page: Playwright Page 객체
        selector: Canvas 셀렉터 (예: '#game-canvas', 'canvas.chart')
        x_percent: 가로 위치 (0.0 ~ 1.0, 0=왼쪽, 1=오른쪽)
        y_percent: 세로 위치 (0.0 ~ 1.0, 0=위, 1=아래)

    Examples:
        # 캔버스 중앙 클릭
        await click_canvas(page, '#game', 0.5, 0.5)

        # 캔버스 우측 하단 클릭
        await click_canvas(page, '#game', 0.9, 0.9)
    """
    canvas = page.locator(selector)
    box = await canvas.bounding_box()

    if not box:
        raise ValueError(f"캔버스 요소를 찾을 수 없거나 크기가 없습니다: {selector}")

    # % 좌표를 절대 픽셀 좌표로 변환
    target_x = box["x"] + (box["width"] * x_percent)
    target_y = box["y"] + (box["height"] * y_percent)

    await page.mouse.click(target_x, target_y)


async def drag_canvas(
    page: Page,
    selector: str,
    start_x_percent: float,
    start_y_percent: float,
    end_x_percent: float,
    end_y_percent: float,
) -> None:
    """
    Canvas 요소 내에서 드래그 수행.

    Args:
        page: Playwright Page 객체
        selector: Canvas 셀렉터
        start_x_percent: 시작점 가로 위치 (0.0 ~ 1.0)
        start_y_percent: 시작점 세로 위치 (0.0 ~ 1.0)
        end_x_percent: 끝점 가로 위치 (0.0 ~ 1.0)
        end_y_percent: 끝점 세로 위치 (0.0 ~ 1.0)

    Examples:
        # 왼쪽 중앙에서 오른쪽 중앙으로 드래그
        await drag_canvas(page, '#chart', 0.1, 0.5, 0.9, 0.5)
    """
    canvas = page.locator(selector)
    box = await canvas.bounding_box()

    if not box:
        raise ValueError(f"캔버스 요소를 찾을 수 없거나 크기가 없습니다: {selector}")

    start_x = box["x"] + (box["width"] * start_x_percent)
    start_y = box["y"] + (box["height"] * start_y_percent)
    end_x = box["x"] + (box["width"] * end_x_percent)
    end_y = box["y"] + (box["height"] * end_y_percent)

    await page.mouse.move(start_x, start_y)
    await page.mouse.down()
    await page.mouse.move(end_x, end_y)
    await page.mouse.up()


async def hover_canvas(
    page: Page,
    selector: str,
    x_percent: float,
    y_percent: float,
) -> None:
    """
    Canvas 요소 내 상대 좌표(%)에 마우스 호버.

    Args:
        page: Playwright Page 객체
        selector: Canvas 셀렉터
        x_percent: 가로 위치 (0.0 ~ 1.0)
        y_percent: 세로 위치 (0.0 ~ 1.0)

    Examples:
        # 차트의 특정 데이터 포인트에 호버하여 툴팁 표시
        await hover_canvas(page, '#chart', 0.3, 0.6)
    """
    canvas = page.locator(selector)
    box = await canvas.bounding_box()

    if not box:
        raise ValueError(f"캔버스 요소를 찾을 수 없거나 크기가 없습니다: {selector}")

    target_x = box["x"] + (box["width"] * x_percent)
    target_y = box["y"] + (box["height"] * y_percent)

    await page.mouse.move(target_x, target_y)

# 위험한 패턴 목록 (정규식)
# Runner가 생성한 스크립트만 실행되어야 하지만, 추가 안전장치로 검증
# NOTE: 패턴은 단독 호출만 차단 (메서드 체인의 .open() 등은 허용)
DANGEROUS_PATTERNS = [
    r"\bimport\s+os\b",
    r"\bimport\s+sys\b",
    r"\bimport\s+subprocess\b",
    r"\bimport\s+shutil\b",
    r"\bfrom\s+os\b",
    r"\bfrom\s+sys\b",
    r"\bfrom\s+subprocess\b",
    r"\bfrom\s+shutil\b",
    r"\b__import__\s*\(",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bcompile\s*\(",
    r"(?<![.\w])open\s*\(",  # 단독 open() 호출만 차단, .open()은 허용
    r"(?<![.\w])os\.",  # 단독 os. 만 차단
    r"(?<![.\w])sys\.",  # 단독 sys. 만 차단
    r"\bsubprocess\.",
    r"\bshutil\.",
    r"\b__builtins__\b",
    r"\b__globals__\b",
    r"\b__code__\b",
    r"\bgetattr\s*\(",
    r"\bsetattr\s*\(",
    r"\bdelattr\s*\(",
]

# 컴파일된 패턴
DANGEROUS_PATTERN_RE = re.compile("|".join(DANGEROUS_PATTERNS), re.IGNORECASE)


class ScriptValidationError(Exception):
    """스크립트 검증 실패 예외."""

    pass


class ScriptRunner:
    """Playwright 스크립트 실행기.

    Runner가 생성한 Playwright 스크립트를 실행합니다.

    Responsibilities:
        1. 스크립트 파싱 및 검증
        2. 스크립트 실행
        3. 실행 결과 반환
    """

    def __init__(self, page: Page) -> None:
        """Initialize script runner.

        Args:
            page: Playwright 페이지
        """
        self._page = page

    async def run(self, script: str, timeout: int | None = None) -> dict[str, Any]:
        """스크립트 실행.

        Args:
            script: 실행할 Playwright 스크립트
            timeout: 타임아웃 (초). None이면 설정값 사용

        Returns:
            실행 결과:
            - success: 성공 여부
            - error: 에러 메시지 (실패 시)
            - duration_ms: 실행 시간 (밀리초)
            - timed_out: 타임아웃 여부
        """
        settings = get_settings()
        execution_timeout = timeout if timeout is not None else settings.script_timeout

        logger.debug(
            "running_script",
            script_length=len(script),
            timeout_seconds=execution_timeout,
        )
        start_time = time_module.time()

        try:
            # 스크립트 실행 (타임아웃 적용)
            # 스크립트는 page를 사용하는 Python 코드
            # exec()를 사용하여 실행하되, 안전한 환경에서 실행
            await asyncio.wait_for(
                self._execute_script(script),
                timeout=execution_timeout,
            )

            duration_ms = int((time_module.time() - start_time) * 1000)
            logger.info("script_executed_successfully", duration_ms=duration_ms)

            return {
                "success": True,
                "duration_ms": duration_ms,
            }

        except TimeoutError:
            duration_ms = int((time_module.time() - start_time) * 1000)
            error_msg = f"Script execution timed out after {execution_timeout} seconds"
            logger.error(
                "script_execution_timeout",
                timeout_seconds=execution_timeout,
                duration_ms=duration_ms,
            )

            return {
                "success": False,
                "error": error_msg,
                "duration_ms": duration_ms,
                "timed_out": True,
            }

        except Exception as e:
            duration_ms = int((time_module.time() - start_time) * 1000)
            logger.error(
                "script_execution_failed",
                error=str(e),
                duration_ms=duration_ms,
            )

            return {
                "success": False,
                "error": str(e),
                "duration_ms": duration_ms,
            }

    def _validate_script(self, script: str) -> None:
        """스크립트 보안 검증.

        위험한 패턴이 포함되어 있는지 검사합니다.
        Runner가 생성한 스크립트만 실행되어야 하지만,
        추가 안전장치로 검증합니다.

        Args:
            script: 검증할 스크립트

        Raises:
            ScriptValidationError: 위험한 패턴 발견 시
        """
        match = DANGEROUS_PATTERN_RE.search(script)
        if match:
            dangerous_code = match.group()
            logger.warning(
                "dangerous_script_pattern_detected",
                pattern=dangerous_code,
                script_preview=script[:200] if len(script) > 200 else script,
            )
            raise ScriptValidationError(
                f"Script contains potentially dangerous code: '{dangerous_code}'"
            )

    async def _execute_script(self, script: str) -> None:
        """스크립트 실행 (내부).

        Args:
            script: 실행할 스크립트

        Raises:
            ScriptValidationError: 위험한 스크립트 감지 시
            Exception: 실행 실패 시
        """
        # 보안 검증
        self._validate_script(script)

        # 스크립트 실행 컨텍스트 설정 (Cloud 모드와 동일)
        # page 객체 + Canvas 헬퍼 + 시간 유틸리티 제공
        # NOTE: 완전한 샌드박스가 아님 - 추가 보안이 필요한 경우 RestrictedPython 사용 권장
        page = self._page
        local_vars: dict[str, Any] = {
            "page": page,
            # Canvas helper functions
            "click_canvas": lambda sel, x, y: click_canvas(page, sel, x, y),
            "drag_canvas": lambda sel, sx, sy, ex, ey: drag_canvas(page, sel, sx, sy, ex, ey),
            "hover_canvas": lambda sel, x, y: hover_canvas(page, sel, x, y),
            # Time utilities (LLM이 timestamp 입력에 사용)
            "time": time_module,
            "datetime": datetime_module,
            # 편의 함수
            "timestamp_ms": lambda: str(int(time_module.time() * 1000)),
            "timestamp_s": lambda: str(int(time_module.time())),
            "now_iso": lambda: datetime_module.datetime.now().isoformat(),
        }

        # async 스크립트 실행을 위한 래퍼
        # 스크립트가 await를 포함할 수 있으므로 async 함수로 래핑
        wrapped_script = f"""
async def __run_script__():
{self._indent_script(script)}

__result__ = __run_script__()
"""

        # 스크립트 컴파일 및 실행
        exec(wrapped_script, local_vars)

        # 비동기 함수 실행
        coro = local_vars.get("__result__")
        if coro:
            await coro

    def _indent_script(self, script: str) -> str:
        """스크립트 들여쓰기.

        Args:
            script: 원본 스크립트

        Returns:
            4칸 들여쓰기된 스크립트
        """
        lines = script.split("\n")
        indented = ["    " + line for line in lines]
        return "\n".join(indented)

    async def run_action(
        self,
        action: str,
        selector: str | None = None,
        value: str | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """단일 액션 실행.

        스크립트 대신 간단한 액션을 직접 실행합니다.

        Args:
            action: 액션 타입 (click, fill, select, etc.)
            selector: CSS 선택자
            value: 입력값 (fill, select 등)
            timeout: 타임아웃 (초). None이면 설정값 사용

        Returns:
            실행 결과
        """
        settings = get_settings()
        execution_timeout = timeout if timeout is not None else settings.action_timeout

        logger.debug(
            "running_action",
            action=action,
            selector=selector,
            value=value,
            timeout_seconds=execution_timeout,
        )
        start_time = time_module.time()

        try:
            await asyncio.wait_for(
                self._execute_action(action, selector, value),
                timeout=execution_timeout,
            )

            duration_ms = int((time_module.time() - start_time) * 1000)
            logger.info(
                "action_executed_successfully",
                action=action,
                duration_ms=duration_ms,
            )

            return {
                "success": True,
                "duration_ms": duration_ms,
            }

        except TimeoutError:
            duration_ms = int((time_module.time() - start_time) * 1000)
            error_msg = f"Action '{action}' timed out after {execution_timeout} seconds"
            logger.error(
                "action_execution_timeout",
                action=action,
                timeout_seconds=execution_timeout,
                duration_ms=duration_ms,
            )

            return {
                "success": False,
                "error": error_msg,
                "duration_ms": duration_ms,
                "timed_out": True,
            }

        except Exception as e:
            duration_ms = int((time_module.time() - start_time) * 1000)
            logger.error(
                "action_execution_failed",
                action=action,
                error=str(e),
                duration_ms=duration_ms,
            )

            return {
                "success": False,
                "error": str(e),
                "duration_ms": duration_ms,
            }

    async def _execute_action(
        self,
        action: str,
        selector: str | None = None,
        value: str | None = None,
    ) -> None:
        """액션 실행 (내부).

        Args:
            action: 액션 타입
            selector: CSS 선택자
            value: 입력값

        Raises:
            ValueError: 알 수 없는 액션
            Exception: 실행 실패 시
        """
        if action == "click" and selector:
            await self._page.click(selector)
        elif action == "fill" and selector and value is not None:
            await self._page.fill(selector, value)
        elif action == "select" and selector and value is not None:
            await self._page.select_option(selector, value)
        elif action == "check" and selector:
            await self._page.check(selector)
        elif action == "uncheck" and selector:
            await self._page.uncheck(selector)
        elif action == "hover" and selector:
            await self._page.hover(selector)
        elif action == "press" and value:
            await self._page.keyboard.press(value)
        elif action == "type" and value:
            await self._page.keyboard.type(value)
        elif action == "wait":
            wait_ms = int(value) if value else 1000
            await self._page.wait_for_timeout(wait_ms)
        elif action == "goto" and value:
            await self._page.goto(value)
        else:
            raise ValueError(f"Unknown action: {action}")
