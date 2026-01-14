"""Logging configuration."""

from __future__ import annotations

import logging
import sys

import structlog


def setup_logging(verbose: bool = False) -> None:
    """로깅 설정.

    structlog를 사용하여 구조화된 로깅을 설정합니다.

    Args:
        verbose: 상세 로그 출력 여부
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # 표준 logging 설정
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        stream=sys.stderr,
    )

    # structlog 설정
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def setup_json_logging(verbose: bool = False) -> None:
    """JSON 로깅 설정.

    프로덕션 환경에서 사용할 JSON 형식 로깅을 설정합니다.

    Args:
        verbose: 상세 로그 출력 여부
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # 표준 logging 설정
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        stream=sys.stderr,
    )

    # structlog JSON 설정
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
