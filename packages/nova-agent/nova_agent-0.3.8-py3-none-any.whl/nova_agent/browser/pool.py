"""Browser pool for managing multiple browser instances."""

from __future__ import annotations

import asyncio
from typing import Any

import structlog

from nova_agent.browser.manager import BrowserManager

logger = structlog.get_logger(__name__)


class BrowserPool:
    """Browser pool for concurrent job execution.

    Manages a pool of browser slots that can be acquired for job execution.
    Browsers are created on-demand when a job is assigned and closed
    immediately when the job completes.

    Key behaviors:
    - Lazy initialization: No browsers started at pool creation
    - On-demand creation: Browser started when acquire() is called
    - Immediate cleanup: Browser closed when release() is called
    - Queuing: Jobs wait when pool is full (via semaphore)
    """

    def __init__(
        self,
        max_size: int = 1,
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
    ) -> None:
        """Initialize browser pool.

        Args:
            max_size: Maximum number of concurrent browsers
            headless: Run browsers in headless mode
            viewport_width: Browser viewport width
            viewport_height: Browser viewport height
        """
        self._max_size = max_size
        self._headless = headless
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height

        self._active_count = 0
        self._active_browsers: dict[int, BrowserManager] = {}  # job_id -> BrowserManager
        self._lock = asyncio.Lock()
        self._available = asyncio.Semaphore(max_size)

    @property
    def max_size(self) -> int:
        """Maximum pool size."""
        return self._max_size

    @property
    def active_count(self) -> int:
        """Number of active browsers."""
        return self._active_count

    @property
    def available_count(self) -> int:
        """Number of available slots."""
        return self._max_size - self._active_count

    async def acquire(
        self,
        job_id: int,
        config: dict[str, Any] | None = None,
    ) -> BrowserManager:
        """Acquire a browser for a job.

        Creates a new browser instance for the job. If pool is full,
        waits until a slot becomes available.

        Args:
            job_id: The job ID requesting the browser
            config: 브라우저 설정 (쿠키, localStorage, 헤더, test_access_key 등)

        Returns:
            BrowserManager instance dedicated to this job

        Raises:
            Exception: Browser start 실패 시 (semaphore는 자동 release됨)
        """
        logger.debug(
            "acquiring_browser",
            job_id=job_id,
            active=self._active_count,
            max=self._max_size,
            has_config=config is not None,
        )

        # Wait for an available slot (blocks if pool is full)
        await self._available.acquire()

        try:
            async with self._lock:
                # Create new browser manager for this job (with config)
                browser_manager = BrowserManager(
                    headless=self._headless,
                    viewport_width=self._viewport_width,
                    viewport_height=self._viewport_height,
                    config=config,
                )

                # Start the browser
                await browser_manager.start()

                # Track the browser
                self._active_browsers[job_id] = browser_manager
                self._active_count += 1

                logger.info(
                    "browser_acquired",
                    job_id=job_id,
                    active=self._active_count,
                    max=self._max_size,
                )

                return browser_manager

        except Exception as e:
            # Browser start 실패 시 semaphore 반환하여 pool capacity 유지
            self._available.release()
            logger.error(
                "browser_acquire_failed",
                job_id=job_id,
                error=str(e),
                active=self._active_count,
                max=self._max_size,
            )
            raise

    async def release(self, job_id: int) -> None:
        """Release a browser after job completion.

        Immediately closes the browser and frees the slot.

        Args:
            job_id: The job ID releasing the browser
        """
        async with self._lock:
            browser_manager = self._active_browsers.pop(job_id, None)

            if browser_manager:
                # browser.stop() 실패해도 semaphore는 반드시 release
                try:
                    await browser_manager.stop()
                except Exception as e:
                    logger.error(
                        "browser_stop_failed_during_release",
                        job_id=job_id,
                        error=str(e),
                    )

                self._active_count -= 1

                logger.info(
                    "browser_released",
                    job_id=job_id,
                    active=self._active_count,
                    max=self._max_size,
                )

                # Signal that a slot is available
                self._available.release()
            else:
                logger.warning(
                    "browser_not_found_for_release",
                    job_id=job_id,
                )

    def get_browser(self, job_id: int) -> BrowserManager | None:
        """Get browser manager for a specific job.

        Args:
            job_id: The job ID

        Returns:
            BrowserManager if found, None otherwise
        """
        return self._active_browsers.get(job_id)

    async def shutdown(self) -> None:
        """Shutdown all active browsers."""
        async with self._lock:
            for job_id, browser_manager in list(self._active_browsers.items()):
                try:
                    await browser_manager.stop()
                    logger.debug("browser_stopped", job_id=job_id)
                except Exception as e:
                    logger.error(
                        "browser_stop_failed",
                        job_id=job_id,
                        error=str(e),
                    )

            self._active_browsers.clear()
            self._active_count = 0

            logger.info("browser_pool_shutdown")
