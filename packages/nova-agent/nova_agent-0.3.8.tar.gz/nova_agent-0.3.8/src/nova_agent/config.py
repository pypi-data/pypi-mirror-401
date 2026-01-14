"""Nova Agent configuration management."""

from __future__ import annotations

from pathlib import Path

import structlog

from nova_agent.constants import CONFIG_DIR, TOKEN_FILE

logger = structlog.get_logger(__name__)


class ConfigManager:
    """Agent 설정 및 토큰 관리.

    토큰은 ~/.nova-agent/token 에 저장됩니다.
    """

    def __init__(self) -> None:
        """Initialize ConfigManager."""
        self._config_dir = CONFIG_DIR
        self._token_file = TOKEN_FILE

    def ensure_config_dir(self) -> None:
        """설정 디렉토리 생성."""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("config_dir_ensured", path=str(self._config_dir))

    def save_token(self, token: str) -> None:
        """토큰 저장.

        Args:
            token: JWT 토큰
        """
        self.ensure_config_dir()
        self._token_file.write_text(token.strip())
        # 파일 권한 설정 (owner만 read/write)
        self._token_file.chmod(0o600)
        logger.info("token_saved", path=str(self._token_file))

    def load_token(self) -> str | None:
        """토큰 로드.

        Returns:
            저장된 토큰 또는 None
        """
        if not self._token_file.exists():
            logger.debug("token_not_found", path=str(self._token_file))
            return None

        token = self._token_file.read_text().strip()
        if not token:
            logger.debug("token_empty", path=str(self._token_file))
            return None

        logger.debug("token_loaded", path=str(self._token_file))
        return token

    def delete_token(self) -> bool:
        """토큰 삭제.

        Returns:
            삭제 성공 여부
        """
        if not self._token_file.exists():
            logger.debug("token_not_found_for_delete", path=str(self._token_file))
            return False

        self._token_file.unlink()
        logger.info("token_deleted", path=str(self._token_file))
        return True

    def has_token(self) -> bool:
        """토큰 존재 여부 확인.

        Returns:
            토큰 존재 여부
        """
        return self._token_file.exists() and bool(self._token_file.read_text().strip())

    @property
    def config_dir(self) -> Path:
        """설정 디렉토리 경로."""
        return self._config_dir

    @property
    def token_file(self) -> Path:
        """토큰 파일 경로."""
        return self._token_file


# Singleton instance
_config_manager: ConfigManager | None = None


def get_config_manager() -> ConfigManager:
    """ConfigManager 싱글톤 인스턴스 반환."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
