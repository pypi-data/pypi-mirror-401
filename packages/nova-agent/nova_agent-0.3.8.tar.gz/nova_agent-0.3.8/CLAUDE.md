# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install for development
pip install -e ".[dev]"
playwright install chromium

# Run tests with coverage
pytest

# Run single test file
pytest tests/test_example.py

# Run single test
pytest tests/test_example.py::test_function_name

# Lint
ruff check src/

# Type check (strict mode enabled)
mypy src/

# Format code
ruff format src/
```

## Environment Configuration

설정은 `.env` 파일로 관리됩니다. `NOVA_ENV` 환경 변수로 환경을 선택합니다.

```bash
# 개발 환경 (기본)
cp .env.example .env

# 운영 환경
NOVA_ENV=prod nova-agent start
```

주요 환경 변수:
- `NOVA_GATEWAY_URL`: Gateway WebSocket URL
- `NOVA_FRONTEND_URL`: Agent 등록 페이지 URL
- `NOVA_HEADLESS`: 브라우저 헤드리스 모드 (true/false)
- `NOVA_LOG_LEVEL`: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)

## CLI Commands

```bash
nova-agent login                    # Register agent, get token
nova-agent start                    # Start agent (uses .env settings)
nova-agent start --no-headless      # Start with visible browser
nova-agent start --verbose          # Debug logging
nova-agent status                   # Check status
nova-agent logout                   # Remove token
```

## Architecture

Nova Agent is an async Python CLI that connects to a Gateway server via WebSocket to receive and execute browser automation jobs using Playwright.

```
Agent CLI → WebSocket Client → Gateway ← Runner (AI Engine)
                 ↓
           Message Handler
                 ↓
            Job Executor
                 ↓
          Browser Manager (Playwright/Chromium)
```

### Core Components

- **`cli.py`**: Typer CLI entry point with login/start/status/logout commands
- **`websocket/client.py`**: `AgentWebSocketClient` - WebSocket connection with reconnection logic
- **`websocket/handlers.py`**: Routes incoming messages to appropriate handlers
- **`websocket/heartbeat.py`**: `HeartbeatManager` - sends heartbeat every 30 seconds
- **`browser/manager.py`**: `BrowserManager` - Playwright chromium browser lifecycle
- **`browser/dom_extractor.py`**: `DomExtractor` - extracts DOM and interactive elements
- **`executor/job_executor.py`**: `JobExecutor` - orchestrates job lifecycle
- **`executor/script_runner.py`**: `ScriptRunner` - executes Playwright scripts
- **`models/messages.py`**: Pydantic models for WebSocket messages
- **`models/job.py`**: Job, Scenario, Step models with status enums
- **`config.py`**: Singleton `ConfigManager`, token stored at `~/.nova-agent/token`
- **`settings.py`**: Pydantic Settings for environment configuration (loads from `.env`)

### Key Patterns

- All I/O is async (asyncio) - use `async/await` throughout
- Message types are Pydantic models with strict validation
- mypy strict mode is enforced - all functions need type hints
- structlog for structured logging
- Reconnection with exponential backoff for WebSocket

## Message Protocol

Agent communicates with Gateway using typed JSON messages. See `models/messages.py` for all message types. Key flows:

1. **Connection**: `agent_connect` → `agent_connected`
2. **Job lifecycle**: `job_assign` → `job_accepted` → steps → `job_completed`
3. **Step execution**: `extract_dom` → `dom_extracted` → `execute_script` → `script_executed`
