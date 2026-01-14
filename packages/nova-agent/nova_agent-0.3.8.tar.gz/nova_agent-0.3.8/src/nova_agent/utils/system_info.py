"""System information utilities."""

from __future__ import annotations

import os
import platform
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


def get_system_info() -> dict[str, Any]:
    """시스템 정보 수집.

    Heartbeat 메시지에 포함할 시스템 정보를 수집합니다.

    Returns:
        시스템 정보 딕셔너리:
        - cpu_usage: CPU 사용률 (%)
        - memory_usage_mb: 메모리 사용량 (MB)
        - platform: 플랫폼 정보
        - python_version: Python 버전
    """
    info: dict[str, Any] = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "machine": platform.machine(),
    }

    # CPU 사용률 (psutil 없이 간단하게)
    try:
        load_avg = os.getloadavg()
        info["load_average"] = {
            "1min": round(load_avg[0], 2),
            "5min": round(load_avg[1], 2),
            "15min": round(load_avg[2], 2),
        }
    except (OSError, AttributeError):
        # Windows에서는 getloadavg 지원 안함
        info["load_average"] = None

    # 메모리 정보 (간단 버전)
    try:
        info["memory"] = _get_memory_info()
    except Exception:
        info["memory"] = None

    return info


def _get_memory_info() -> dict[str, Any] | None:
    """메모리 정보 수집.

    /proc/meminfo (Linux) 또는 vm_stat (macOS) 사용.

    Returns:
        메모리 정보 또는 None
    """
    system = platform.system()

    if system == "Linux":
        return _get_linux_memory_info()
    elif system == "Darwin":
        return _get_macos_memory_info()

    return None


def _get_linux_memory_info() -> dict[str, Any] | None:
    """Linux 메모리 정보."""
    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()

        meminfo = {}
        for line in lines:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().split()[0]
                meminfo[key] = int(value)

        total_kb = meminfo.get("MemTotal", 0)
        available_kb = meminfo.get("MemAvailable", 0)
        used_kb = total_kb - available_kb

        return {
            "total_mb": round(total_kb / 1024, 2),
            "used_mb": round(used_kb / 1024, 2),
            "available_mb": round(available_kb / 1024, 2),
            "usage_percent": round((used_kb / total_kb) * 100, 2) if total_kb > 0 else 0,
        }
    except Exception as e:
        logger.debug("failed_to_get_linux_memory", error=str(e))
        return None


def _get_macos_memory_info() -> dict[str, Any] | None:
    """macOS 메모리 정보."""
    import subprocess

    try:
        # sysctl로 전체 메모리 가져오기
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        total_bytes = int(result.stdout.strip())
        total_mb = total_bytes / (1024 * 1024)

        # vm_stat으로 사용량 계산
        result = subprocess.run(
            ["vm_stat"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        # 페이지 크기 (보통 4096)
        page_size = 4096

        stats = {}
        for line in result.stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":")
                key = key.strip()
                value = value.strip().rstrip(".")
                if value.isdigit():
                    stats[key] = int(value)

        # 사용 중인 페이지 계산
        wired = stats.get("Pages wired down", 0)
        active = stats.get("Pages active", 0)
        compressed = stats.get("Pages occupied by compressor", 0)

        used_pages = wired + active + compressed
        used_mb = (used_pages * page_size) / (1024 * 1024)
        available_mb = total_mb - used_mb

        return {
            "total_mb": round(total_mb, 2),
            "used_mb": round(used_mb, 2),
            "available_mb": round(available_mb, 2),
            "usage_percent": round((used_mb / total_mb) * 100, 2) if total_mb > 0 else 0,
        }
    except Exception as e:
        logger.debug("failed_to_get_macos_memory", error=str(e))
        return None


def get_cpu_usage_percent() -> float | None:
    """CPU 사용률 반환.

    Returns:
        CPU 사용률 (%) 또는 None
    """
    try:
        load_avg = os.getloadavg()
        cpu_count = os.cpu_count() or 1
        # 1분 평균 로드를 CPU 사용률로 변환
        return round((load_avg[0] / cpu_count) * 100, 2)
    except (OSError, AttributeError):
        return None


def get_memory_usage_mb() -> float | None:
    """메모리 사용량 (MB) 반환.

    Returns:
        메모리 사용량 (MB) 또는 None
    """
    memory = _get_memory_info()
    if memory:
        return memory.get("used_mb")
    return None
