"""Nova Agent settings - Environment configuration."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _load_env() -> None:
    """환경 변수 파일 로드.

    NOVA_ENV 환경 변수에 따라 다른 .env 파일을 로드합니다:
    - dev: .env (개발용)
    - 기본(prod): .env.prod
    """
    env = os.getenv("NOVA_ENV", "prod").lower()
    env_file = PROJECT_ROOT / ".env" if env == "dev" else PROJECT_ROOT / ".env.prod"

    if env_file.exists():
        load_dotenv(env_file, override=True)


# 환경 변수 로드
_load_env()


class Settings(BaseSettings):
    """Nova Agent 설정.

    환경 변수 또는 .env 파일에서 설정을 로드합니다.
    NOVA_ 접두사를 가진 환경 변수를 자동으로 매핑합니다.
    """

    # URLs
    gateway_url: str = Field(
        default="wss://agent-gw.qanova.kr/ws/agent",
        description="Gateway WebSocket URL",
    )
    frontend_url: str = Field(
        default="https://qanova.kr",
        description="Frontend URL for agent registration",
    )
    agent_register_path: str = Field(
        default="/agent/register",
        description="Agent registration path",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Log level (DEBUG, INFO, WARNING, ERROR)",
    )

    # Browser
    headless: bool = Field(
        default=True,
        description="Run browser in headless mode",
    )
    viewport_width: int = Field(
        default=1920,
        description="Browser viewport width",
    )
    viewport_height: int = Field(
        default=1080,
        description="Browser viewport height",
    )

    # Browser Pool
    pool_size: int = Field(
        default=1,
        description="Maximum number of concurrent browser instances",
        ge=1,
        le=10,
    )

    # Heartbeat
    heartbeat_interval: int = Field(
        default=30,
        description="Heartbeat interval in seconds",
    )

    # Connection
    connection_timeout: int = Field(
        default=10,
        description="Connection timeout in seconds",
    )
    reconnect_delay: int = Field(
        default=5,
        description="Reconnect delay in seconds",
    )
    max_reconnect_attempts: int = Field(
        default=0,
        description="Maximum reconnection attempts (0 = unlimited)",
    )

    # Job
    job_timeout: int = Field(
        default=300,
        description="Job idle timeout in seconds (default: 5 minutes)",
    )

    # Script execution
    script_timeout: int = Field(
        default=30,
        description="Script execution timeout in seconds (default: 30 seconds)",
    )
    action_timeout: int = Field(
        default=10,
        description="Single action timeout in seconds (default: 10 seconds)",
    )

    # Config paths
    config_dir: Path = Field(
        default=Path.home() / ".nova-agent",
        description="Configuration directory",
    )

    model_config = {
        "env_prefix": "NOVA_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def token_file(self) -> Path:
        """토큰 파일 경로."""
        return self.config_dir / "token"

    @property
    def register_url(self) -> str:
        """Agent 등록 전체 URL."""
        return f"{self.frontend_url.rstrip('/')}{self.agent_register_path}"


# 런타임 상태: verbose 모드 (--verbose 옵션으로 설정)
_verbose_mode: bool = False


def set_verbose(enabled: bool) -> None:
    """Verbose 모드 설정."""
    global _verbose_mode
    _verbose_mode = enabled


def is_verbose() -> bool:
    """Verbose 모드 여부 반환."""
    return _verbose_mode


@lru_cache
def get_settings() -> Settings:
    """Settings 싱글톤 인스턴스 반환.

    Returns:
        Settings 인스턴스
    """
    return Settings()
