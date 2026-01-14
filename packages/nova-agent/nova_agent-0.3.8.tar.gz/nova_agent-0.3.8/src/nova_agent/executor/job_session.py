"""Job session - encapsulates a single job execution context."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nova_agent.browser.manager import BrowserManager
    from nova_agent.models.job import Job, Step


@dataclass
class JobSession:
    """Encapsulates a single job's execution context.

    Each job gets its own session with:
    - Dedicated browser manager
    - Job state (current step, etc.)
    - Last activity timestamp for timeout tracking
    """

    job_id: int
    job: Job
    browser_manager: BrowserManager
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)

    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = time.time()

    def is_timed_out(self, timeout_seconds: int) -> bool:
        """Check if session has timed out.

        Args:
            timeout_seconds: Timeout threshold in seconds

        Returns:
            True if timed out
        """
        return (time.time() - self.last_activity) > timeout_seconds

    @property
    def current_step(self) -> Step | None:
        """Get current step."""
        return self.job.current_step

    def advance_step(self) -> bool:
        """Advance to next step.

        Returns:
            True if successfully advanced, False if no more steps
        """
        return self.job.advance_step()

    @property
    def is_last_step(self) -> bool:
        """Check if on last step."""
        return self.job.is_last_step
