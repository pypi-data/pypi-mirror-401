# Nova Agent 구현 스펙

## 개요

Nova Agent는 QA Nova 플랫폼의 Local Agent CLI 도구입니다. 사용자의 로컬 머신에서 Playwright 브라우저를 실행하고, Gateway를 통해 Runner와 통신하여 테스트를 수행합니다.

**패키지명**: `nova-agent`
**설치**: `pip install nova-agent`
**CLI 명령어**: `nova-agent`

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Nova Agent CLI                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │     CLI      │    │   WebSocket  │    │   Browser Manager    │  │
│  │   (Typer)    │───▶│    Client    │───▶│    (Playwright)      │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│         │                   │                       │               │
│         │                   │                       │               │
│         ▼                   ▼                       ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │    Config    │    │  Job/Step    │    │    DOM Extractor     │  │
│  │   Manager    │    │   Executor   │    │                      │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ WebSocket (JWT Auth)
                              ▼
                    ┌──────────────────┐
                    │     Gateway      │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │     Runner       │
                    │   (AI Engine)    │
                    └──────────────────┘
```

---

## 프로젝트 구조

```
nova-agent/
├── pyproject.toml              # 패키지 설정 (Poetry)
├── README.md                   # 사용자 가이드
├── IMPLEMENTATION_SPEC.md      # 이 문서
├── src/
│   └── nova_agent/
│       ├── __init__.py
│       ├── __main__.py         # python -m nova_agent 진입점
│       ├── cli.py              # CLI 명령어 (Typer)
│       ├── config.py           # 설정 관리
│       ├── constants.py        # 상수 정의
│       │
│       ├── websocket/          # WebSocket 통신
│       │   ├── __init__.py
│       │   ├── client.py       # Gateway WebSocket 클라이언트
│       │   ├── handlers.py     # 메시지 핸들러
│       │   └── heartbeat.py    # Heartbeat 관리
│       │
│       ├── browser/            # Playwright 브라우저 관리
│       │   ├── __init__.py
│       │   ├── manager.py      # BrowserManager
│       │   ├── dom_extractor.py # DOM 추출
│       │   └── screenshot.py   # 스크린샷 캡처
│       │
│       ├── executor/           # Job/Step 실행
│       │   ├── __init__.py
│       │   ├── job_executor.py # Job 실행 관리
│       │   └── script_runner.py # Playwright 스크립트 실행
│       │
│       ├── models/             # 데이터 모델
│       │   ├── __init__.py
│       │   ├── messages.py     # WebSocket 메시지 모델
│       │   ├── job.py          # Job/Step 모델
│       │   └── dom.py          # DOM 모델
│       │
│       └── utils/              # 유틸리티
│           ├── __init__.py
│           ├── logging.py      # 로깅 설정
│           └── system_info.py  # 시스템 정보 수집
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_cli.py
    ├── test_websocket.py
    └── test_browser.py
```

---

## CLI 명령어

### 1. `nova-agent login`

브라우저를 열어 Agent 등록 페이지로 이동하고, 발급된 JWT 토큰을 입력받아 저장합니다.

```bash
$ nova-agent login

🌐 Opening browser for agent registration...
   URL: https://app.qanova.io/agent/register

After registering your agent in the browser, paste the token below.

Enter Agent Token: eyJhbGciOiJIUzI1NiIs...

✅ Token saved successfully!
   Location: ~/.nova-agent/token

Run 'nova-agent start' to connect to the server.
```

**구현 흐름**:
1. 브라우저 열기: `webbrowser.open(f"{FRONTEND_URL}/agent/register")`
2. 프롬프트 표시: "Enter Agent Token: "
3. 토큰 입력 받기
4. JWT 형식 검증 (3개의 `.`으로 구분된 문자열)
5. `~/.nova-agent/token` 파일에 저장
6. 성공 메시지 출력

### 2. `nova-agent start`

Gateway에 WebSocket으로 연결하고 Job 대기 상태로 진입합니다.

```bash
$ nova-agent start

🔌 Connecting to Gateway...
   URL: wss://gateway.qanova.io/ws/agent

✅ Connected to server
✅ Agent registered: agent-abc123 (Project: My Project)
✅ Playwright ready (chromium)
🔄 Waiting for jobs...

[2024-01-08 12:00:00] Job 1001 received
[2024-01-08 12:00:01] Step 1/3: 로그인 페이지로 이동
[2024-01-08 12:00:05] Step 2/3: 이메일 입력
[2024-01-08 12:00:10] Step 3/3: 비밀번호 입력 후 로그인
[2024-01-08 12:00:15] Job 1001 completed ✓
```

**구현 흐름**:
1. 토큰 파일 확인 (`~/.nova-agent/token`)
2. 토큰 없으면 에러: "Run 'nova-agent login' first"
3. Gateway WebSocket 연결 (JWT를 쿼리 파라미터로 전달)
4. `registered` 메시지 수신 대기
5. Playwright 브라우저 초기화
6. Heartbeat 루프 시작 (30초 주기)
7. 메시지 수신 루프 시작
8. Job 수신 시 처리

### 3. `nova-agent status`

현재 Agent 상태를 확인합니다.

```bash
$ nova-agent status

Agent Status
────────────────────────────
Token:     ✅ Configured
Location:  ~/.nova-agent/token
Agent ID:  agent-abc123 (from token)
Gateway:   wss://gateway.qanova.io/ws/agent
```

### 4. `nova-agent logout`

저장된 토큰을 삭제합니다.

```bash
$ nova-agent logout

🗑️  Token removed successfully.
```

---

## 설정 파일

### 토큰 저장 위치

```
~/.nova-agent/token
```

단순 텍스트 파일로 JWT 토큰만 저장합니다.

### 환경 변수 (선택)

```bash
# Gateway URL 오버라이드 (개발용)
NOVA_GATEWAY_URL=ws://localhost:8080

# Frontend URL 오버라이드 (개발용)
NOVA_FRONTEND_URL=http://localhost:3000

# 로그 레벨
NOVA_LOG_LEVEL=DEBUG

# 브라우저 Headless 모드
NOVA_HEADLESS=true
```

---

## WebSocket 메시지 프로토콜

### Agent → Gateway

#### 1. heartbeat (30초 주기)
```json
{
  "type": "heartbeat",
  "agent_id": "agt_1a2b3c4d5e6f",
  "timestamp": "2024-01-08T12:00:00Z",
  "status": "idle",
  "running_jobs": [],
  "system_info": {
    "cpu_usage": 25.5,
    "memory_usage_mb": 512
  }
}
```

#### 2. job_accepted
```json
{
  "type": "job_accepted",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "browser_session_id": "session_xyz789",
  "timestamp": "2024-01-08T12:00:01Z"
}
```

#### 3. step_started
```json
{
  "type": "step_started",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 1,
  "timestamp": "2024-01-08T12:00:02Z"
}
```

#### 4. dom_extracted
```json
{
  "type": "dom_extracted",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "dom": {
    "url": "https://example.com/login",
    "title": "로그인 - Example",
    "body_text": "Email\nPassword\nLogin\nForgot password?",
    "interactive_elements": [
      {
        "tag": "input",
        "type": "email",
        "id": "email",
        "name": "email",
        "placeholder": "이메일을 입력하세요",
        "selector": "#email",
        "aria_label": "Email address",
        "bounding_box": {"x": 100, "y": 200, "width": 300, "height": 40}
      }
    ],
    "metadata": {
      "viewport_width": 1280,
      "viewport_height": 720,
      "device_pixel_ratio": 1
    }
  },
  "screenshot": {
    "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/png",
    "width": 1280,
    "height": 720
  },
  "goal": "이메일 입력란에 test@example.com 입력",
  "timestamp": "2024-01-08T12:00:03Z"
}
```

#### 5. script_result
```json
{
  "type": "script_result",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "status": "success",
  "result": {
    "executed": true,
    "duration_ms": 234
  },
  "screenshot": {
    "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
    "mime_type": "image/png"
  },
  "timestamp": "2024-01-08T12:00:06Z"
}
```

#### 6. step_completed
```json
{
  "type": "step_completed",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "duration_ms": 5234,
  "retry_count": 0,
  "timestamp": "2024-01-08T12:00:08Z"
}
```

#### 7. step_failed
```json
{
  "type": "step_failed",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "error": {
    "message": "Element not found: #email",
    "type": "ElementNotFoundError",
    "stack": "..."
  },
  "retry_count": 2,
  "timestamp": "2024-01-08T12:00:08Z"
}
```

#### 8. job_completed
```json
{
  "type": "job_completed",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "total_steps": 5,
  "completed_steps": 5,
  "failed_steps": 0,
  "duration_ms": 45678,
  "timestamp": "2024-01-08T12:00:45Z"
}
```

#### 9. job_failed
```json
{
  "type": "job_failed",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "reason": "step_failed",
  "failed_step_id": 3,
  "error": {
    "message": "Browser crashed",
    "type": "BrowserError"
  },
  "completed_steps": 2,
  "total_steps": 5,
  "duration_ms": 15678,
  "timestamp": "2024-01-08T12:00:15Z"
}
```

### Gateway → Agent

#### 1. registered (연결 성공)
```json
{
  "type": "registered",
  "agent_id": "agt_1a2b3c4d5e6f",
  "project_id": 1
}
```

#### 2. heartbeat_ack
```json
{
  "type": "heartbeat_ack",
  "timestamp": "2024-01-08T12:00:00Z"
}
```

#### 3. job_assign
```json
{
  "type": "job_assign",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "scenario": {
    "scenario_id": 123,
    "name": "로그인 테스트",
    "base_url": "https://example.com",
    "viewport": {
      "width": 1280,
      "height": 720
    },
    "browser": "chromium",
    "headless": false
  },
  "steps": [
    {
      "step_id": 1,
      "order": 1,
      "action_type": "NAVIGATE",
      "goal": "로그인 페이지로 이동",
      "config": {"url": "/login"}
    },
    {
      "step_id": 2,
      "order": 2,
      "action_type": "AI_ASSIST",
      "goal": "이메일 입력란에 test@example.com 입력"
    }
  ],
  "environment_variables": {
    "TEST_USER_EMAIL": "test@example.com"
  },
  "config": {
    "timeout": 30000,
    "retry_on_failure": true,
    "max_retries": 2
  }
}
```

#### 4. execute_script
```json
{
  "type": "execute_script",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "script": "await page.fill('#email', 'test@example.com');",
  "explanation": "이메일 입력란에 값을 입력합니다.",
  "timestamp": "2024-01-08T12:00:05Z"
}
```

#### 5. goal_achieved
```json
{
  "type": "goal_achieved",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "verification": {
    "method": "visual_inspection",
    "confidence": 0.95,
    "details": "목표가 달성되었습니다."
  },
  "timestamp": "2024-01-08T12:00:07Z"
}
```

#### 6. step_abandoned
```json
{
  "type": "step_abandoned",
  "job_id": 1001,
  "agent_id": "agt_1a2b3c4d5e6f",
  "step_id": 2,
  "reason": "max_retries_exceeded",
  "details": "3번 시도 후에도 목표를 달성하지 못했습니다.",
  "timestamp": "2024-01-08T12:00:07Z"
}
```

#### 7. error
```json
{
  "type": "error",
  "code": "ROUTING_ERROR",
  "message": "Runner not connected",
  "job_id": 1001,
  "timestamp": "2024-01-08T12:00:00Z"
}
```

---

## 핵심 컴포넌트 상세

### 1. CLI (`cli.py`)

```python
# 구현할 함수들
def login() -> None:
    """브라우저 열고 토큰 입력받아 저장"""

def start() -> None:
    """Gateway 연결 및 Job 대기"""

def status() -> None:
    """현재 상태 출력"""

def logout() -> None:
    """토큰 삭제"""
```

**사용 라이브러리**: `typer`, `rich` (터미널 UI)

### 2. Config Manager (`config.py`)

```python
class Config:
    """설정 관리"""

    # 경로
    CONFIG_DIR = Path.home() / ".nova-agent"
    TOKEN_FILE = CONFIG_DIR / "token"

    # URL (환경변수로 오버라이드 가능)
    GATEWAY_URL = "wss://gateway.qanova.io/ws/agent"
    FRONTEND_URL = "https://app.qanova.io"

    # 브라우저 설정
    DEFAULT_BROWSER = "chromium"
    DEFAULT_HEADLESS = False
    DEFAULT_VIEWPORT = {"width": 1280, "height": 720}

    # Heartbeat
    HEARTBEAT_INTERVAL = 30  # seconds

    def load_token(self) -> str | None:
        """저장된 토큰 로드"""

    def save_token(self, token: str) -> None:
        """토큰 저장"""

    def delete_token(self) -> None:
        """토큰 삭제"""

    def get_agent_id_from_token(self) -> str | None:
        """JWT에서 agent_id 추출"""
```

### 3. WebSocket Client (`websocket/client.py`)

```python
class GatewayClient:
    """Gateway WebSocket 클라이언트"""

    def __init__(self, gateway_url: str, token: str):
        self.gateway_url = gateway_url
        self.token = token
        self._ws: WebSocket | None = None
        self._connected = False
        self._agent_id: str | None = None
        self._project_id: int | None = None

    async def connect(self) -> None:
        """Gateway에 연결"""
        # ws://gateway/ws/agent?token=JWT

    async def disconnect(self) -> None:
        """연결 종료"""

    async def send_message(self, message: dict) -> None:
        """메시지 전송"""

    async def receive_message(self) -> dict:
        """메시지 수신"""

    # 편의 메서드
    async def send_heartbeat(self) -> None:
    async def send_job_accepted(self, job_id: int) -> None:
    async def send_step_started(self, job_id: int, step_id: int) -> None:
    async def send_dom_extracted(self, job_id: int, step_id: int, dom: dict, screenshot: dict) -> None:
    async def send_script_result(self, job_id: int, step_id: int, success: bool, ...) -> None:
    async def send_step_completed(self, job_id: int, step_id: int, duration_ms: int) -> None:
    async def send_step_failed(self, job_id: int, step_id: int, error: dict) -> None:
    async def send_job_completed(self, job_id: int, stats: dict) -> None:
    async def send_job_failed(self, job_id: int, error: dict) -> None:
```

### 4. Message Handlers (`websocket/handlers.py`)

```python
class MessageHandler:
    """수신 메시지 핸들러"""

    def __init__(self, job_executor: JobExecutor):
        self.job_executor = job_executor
        self._handlers = {
            "registered": self._handle_registered,
            "heartbeat_ack": self._handle_heartbeat_ack,
            "job_assign": self._handle_job_assign,
            "execute_script": self._handle_execute_script,
            "goal_achieved": self._handle_goal_achieved,
            "step_abandoned": self._handle_step_abandoned,
            "error": self._handle_error,
        }

    async def handle(self, message: dict) -> None:
        """메시지 타입에 따라 핸들러 호출"""
        msg_type = message.get("type")
        handler = self._handlers.get(msg_type)
        if handler:
            await handler(message)

    async def _handle_registered(self, msg: dict) -> None:
        """연결 완료 처리"""

    async def _handle_job_assign(self, msg: dict) -> None:
        """Job 할당 처리 → JobExecutor에게 전달"""

    async def _handle_execute_script(self, msg: dict) -> None:
        """스크립트 실행 명령 처리"""

    async def _handle_goal_achieved(self, msg: dict) -> None:
        """Goal 달성 알림 처리 → Step 완료"""

    async def _handle_step_abandoned(self, msg: dict) -> None:
        """Step 포기 알림 처리 → Step 실패"""
```

### 5. Heartbeat Manager (`websocket/heartbeat.py`)

```python
class HeartbeatManager:
    """Heartbeat 관리"""

    INTERVAL = 30  # seconds

    def __init__(self, client: GatewayClient):
        self.client = client
        self._task: asyncio.Task | None = None
        self._running = False

    async def start(self) -> None:
        """Heartbeat 루프 시작"""
        self._running = True
        self._task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self) -> None:
        """Heartbeat 루프 중지"""
        self._running = False
        if self._task:
            self._task.cancel()

    async def _heartbeat_loop(self) -> None:
        """30초마다 Heartbeat 전송"""
        while self._running:
            await self.client.send_heartbeat()
            await asyncio.sleep(self.INTERVAL)
```

### 6. Browser Manager (`browser/manager.py`)

```python
class BrowserManager:
    """Playwright 브라우저 관리"""

    def __init__(self, browser_type: str = "chromium", headless: bool = False):
        self.browser_type = browser_type
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def initialize(self) -> None:
        """Playwright 초기화 및 브라우저 시작"""

    async def close(self) -> None:
        """브라우저 종료"""

    async def new_page(self, viewport: dict | None = None) -> Page:
        """새 페이지 생성"""

    async def navigate(self, url: str) -> None:
        """URL로 이동"""

    async def execute_script(self, script: str) -> dict:
        """Playwright 스크립트 실행"""
        # eval()로 스크립트 실행
        # 결과 및 에러 반환

    async def take_screenshot(self) -> bytes:
        """스크린샷 캡처"""

    @property
    def page(self) -> Page:
        """현재 페이지 반환"""
```

### 7. DOM Extractor (`browser/dom_extractor.py`)

```python
class DOMExtractor:
    """DOM 추출"""

    def __init__(self, page: Page):
        self.page = page

    async def extract(self) -> dict:
        """현재 페이지 DOM 추출"""
        return {
            "url": self.page.url,
            "title": await self.page.title(),
            "body_text": await self._extract_body_text(),
            "interactive_elements": await self._extract_interactive_elements(),
            "metadata": await self._extract_metadata(),
        }

    async def _extract_body_text(self) -> str:
        """페이지 텍스트 추출"""
        # innerText에서 불필요한 공백 제거

    async def _extract_interactive_elements(self) -> list[dict]:
        """상호작용 가능한 요소 추출"""
        # input, button, a, select, textarea 등
        # 각 요소의 속성 + bounding_box

    async def _extract_metadata(self) -> dict:
        """브라우저 메타데이터"""
        return {
            "viewport_width": ...,
            "viewport_height": ...,
            "device_pixel_ratio": ...,
        }
```

### 8. Job Executor (`executor/job_executor.py`)

```python
class JobExecutor:
    """Job 실행 관리"""

    def __init__(
        self,
        gateway_client: GatewayClient,
        browser_manager: BrowserManager,
    ):
        self.client = gateway_client
        self.browser = browser_manager
        self._current_job: Job | None = None
        self._current_step: Step | None = None

    async def execute_job(self, job: Job) -> None:
        """Job 실행"""
        self._current_job = job

        # 1. job_accepted 전송
        await self.client.send_job_accepted(job.job_id)

        # 2. 브라우저 설정
        await self.browser.new_page(viewport=job.scenario.viewport)

        # 3. 첫 번째 Step 시작
        await self._start_step(job.steps[0])

    async def _start_step(self, step: Step) -> None:
        """Step 시작"""
        self._current_step = step

        # 1. step_started 전송
        await self.client.send_step_started(
            job_id=self._current_job.job_id,
            step_id=step.step_id,
        )

        # 2. NAVIGATE 액션이면 먼저 이동
        if step.action_type == "NAVIGATE":
            await self.browser.navigate(step.config["url"])

        # 3. DOM 추출 및 전송
        await self._extract_and_send_dom()

    async def _extract_and_send_dom(self) -> None:
        """DOM 추출하여 Runner에게 전송"""
        extractor = DOMExtractor(self.browser.page)
        dom = await extractor.extract()
        screenshot = await self.browser.take_screenshot()

        await self.client.send_dom_extracted(
            job_id=self._current_job.job_id,
            step_id=self._current_step.step_id,
            dom=dom,
            screenshot={
                "base64": base64.b64encode(screenshot).decode(),
                "mime_type": "image/png",
            },
        )

    async def execute_script(self, script: str) -> None:
        """Runner로부터 받은 스크립트 실행"""
        try:
            result = await self.browser.execute_script(script)

            # 스크린샷 캡처
            screenshot = await self.browser.take_screenshot()

            # script_result 전송
            await self.client.send_script_result(
                job_id=self._current_job.job_id,
                step_id=self._current_step.step_id,
                success=True,
                result=result,
                screenshot={
                    "base64": base64.b64encode(screenshot).decode(),
                    "mime_type": "image/png",
                },
            )

            # 새 DOM 추출하여 전송 (Runner가 goal 달성 여부 확인용)
            await self._extract_and_send_dom()

        except Exception as e:
            # 에러 시 script_result 전송
            await self.client.send_script_result(
                job_id=self._current_job.job_id,
                step_id=self._current_step.step_id,
                success=False,
                error={
                    "message": str(e),
                    "type": type(e).__name__,
                },
            )

    async def complete_step(self, duration_ms: int) -> None:
        """Step 완료 처리"""
        # step_completed 전송
        await self.client.send_step_completed(
            job_id=self._current_job.job_id,
            step_id=self._current_step.step_id,
            duration_ms=duration_ms,
        )

        # 다음 Step으로 이동
        await self._move_to_next_step()

    async def fail_step(self, error: dict) -> None:
        """Step 실패 처리"""
        # step_failed 전송
        await self.client.send_step_failed(
            job_id=self._current_job.job_id,
            step_id=self._current_step.step_id,
            error=error,
        )

        # Job 실패
        await self._fail_job(error)

    async def _move_to_next_step(self) -> None:
        """다음 Step으로 이동"""
        current_index = self._get_current_step_index()

        if current_index + 1 < len(self._current_job.steps):
            # 다음 Step 시작
            next_step = self._current_job.steps[current_index + 1]
            await self._start_step(next_step)
        else:
            # 모든 Step 완료 → Job 완료
            await self._complete_job()

    async def _complete_job(self) -> None:
        """Job 완료"""
        await self.client.send_job_completed(
            job_id=self._current_job.job_id,
            stats={
                "total_steps": len(self._current_job.steps),
                "completed_steps": len(self._current_job.steps),
                "failed_steps": 0,
            },
        )
        self._current_job = None
        self._current_step = None

    async def _fail_job(self, error: dict) -> None:
        """Job 실패"""
        await self.client.send_job_failed(
            job_id=self._current_job.job_id,
            error=error,
            stats={
                "completed_steps": self._get_current_step_index(),
                "total_steps": len(self._current_job.steps),
            },
        )
        self._current_job = None
        self._current_step = None
```

### 9. Script Runner (`executor/script_runner.py`)

```python
class ScriptRunner:
    """Playwright 스크립트 실행"""

    def __init__(self, page: Page):
        self.page = page

    async def run(self, script: str) -> dict:
        """스크립트 실행

        Args:
            script: Playwright 스크립트 (예: "await page.fill('#email', 'test@example.com')")

        Returns:
            실행 결과 (success, duration_ms, error 등)
        """
        start_time = time.time()

        try:
            # 스크립트에서 'page'를 현재 page 객체로 대체
            # eval()로 실행
            exec_globals = {"page": self.page, "asyncio": asyncio}

            # async 스크립트 실행
            if script.strip().startswith("await"):
                # "await page.xxx()" 형태
                code = f"async def __script__():\n    {script}\nresult = asyncio.get_event_loop().run_until_complete(__script__())"
            else:
                code = script

            exec(code, exec_globals)

            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "success": True,
                "duration_ms": duration_ms,
            }

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "duration_ms": duration_ms,
                "error": {
                    "message": str(e),
                    "type": type(e).__name__,
                },
            }
```

---

## 실행 흐름 상세

### 1. Agent 시작 (`nova-agent start`)

```
1. 토큰 로드 (~/.nova-agent/token)
2. Gateway WebSocket 연결
   URL: wss://gateway.qanova.io/ws/agent?token=JWT
3. 'registered' 메시지 수신
   → agent_id, project_id 저장
4. Playwright 초기화
   → chromium 브라우저 시작
5. Heartbeat 루프 시작
   → 30초마다 heartbeat 전송
6. 메시지 수신 루프 시작
   → job_assign 대기
```

### 2. Job 실행 흐름

```
1. 'job_assign' 수신
   → Job, Scenario, Steps 정보 파싱

2. JobExecutor.execute_job() 호출

3. 'job_accepted' 전송

4. 첫 번째 Step 시작
   a. 'step_started' 전송
   b. NAVIGATE 타입이면 페이지 이동
   c. DOM 추출
   d. 'dom_extracted' 전송 (DOM + 스크린샷 + goal)

5. 'execute_script' 수신 대기

6. 스크립트 실행
   a. Playwright 스크립트 실행
   b. 'script_result' 전송
   c. 새 DOM 추출하여 'dom_extracted' 전송

7. 'goal_achieved' 또는 'execute_script' 수신
   - goal_achieved: Step 완료 → 'step_completed' 전송 → 다음 Step
   - execute_script: 6번으로 돌아가 반복
   - step_abandoned: Step 실패 → 'step_failed' 전송 → Job 실패

8. 모든 Step 완료 시
   'job_completed' 전송

9. Job 대기 상태로 복귀
```

### 3. Step 실행 루프 상세

```
┌─────────────────────────────────────────────────────┐
│                    Step 시작                         │
│  → step_started 전송                                 │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│              DOM 추출 및 전송                        │
│  → dom_extracted 전송 (DOM + screenshot + goal)     │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│            Runner 명령 대기                          │
│  (execute_script / goal_achieved / step_abandoned)  │
└────────────────────────┬────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ execute_    │  │ goal_       │  │ step_       │
│ script      │  │ achieved    │  │ abandoned   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 스크립트    │  │ Step 완료   │  │ Step 실패   │
│ 실행        │  │ 처리        │  │ 처리        │
│             │  │             │  │             │
│ → script_   │  │ → step_     │  │ → step_     │
│   result    │  │   completed │  │   failed    │
│ → dom_      │  │             │  │ → job_      │
│   extracted │  │ 다음 Step   │  │   failed    │
└──────┬──────┘  └─────────────┘  └─────────────┘
       │
       └──────────▶ Runner 명령 대기 (반복)
```

---

## 에러 처리

### 연결 에러

```python
class ConnectionError(Exception):
    """Gateway 연결 실패"""
    pass

class AuthenticationError(Exception):
    """JWT 인증 실패"""
    pass
```

**처리**:
- 재연결 시도 (5초 간격, 최대 10회)
- 실패 시 에러 메시지 출력 후 종료

### 스크립트 실행 에러

```python
class ScriptExecutionError(Exception):
    """Playwright 스크립트 실행 실패"""
    pass
```

**처리**:
- `script_result` 메시지에 에러 정보 포함하여 전송
- Runner가 재시도 또는 step_abandoned 결정

### 브라우저 크래시

```python
class BrowserCrashError(Exception):
    """브라우저 크래시"""
    pass
```

**처리**:
- `step_failed` 전송
- `job_failed` 전송
- 브라우저 재시작
- Job 대기 상태로 복귀

---

## 의존성

```toml
[tool.poetry.dependencies]
python = "^3.11"
typer = "^0.9.0"              # CLI 프레임워크
rich = "^13.7.0"              # 터미널 UI
websockets = "^12.0"          # WebSocket 클라이언트
playwright = "^1.40.0"        # 브라우저 자동화
pydantic = "^2.5.0"           # 데이터 검증
orjson = "^3.9.0"             # JSON 파싱 (빠름)
structlog = "^24.1.0"         # 구조화된 로깅

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.23.0"
pytest-cov = "^4.1.0"
ruff = "^0.1.0"
mypy = "^1.8.0"
```

---

## 테스트 시나리오

### 1. CLI 테스트

```python
def test_login_opens_browser():
    """login 명령이 브라우저를 여는지 확인"""

def test_login_saves_token():
    """입력받은 토큰이 올바르게 저장되는지 확인"""

def test_start_requires_token():
    """토큰 없이 start 시 에러 발생 확인"""
```

### 2. WebSocket 테스트

```python
async def test_connect_with_valid_token():
    """유효한 토큰으로 연결 성공"""

async def test_connect_with_invalid_token():
    """무효한 토큰으로 연결 실패"""

async def test_heartbeat_sent_periodically():
    """Heartbeat가 30초마다 전송되는지 확인"""

async def test_reconnect_on_disconnect():
    """연결 끊김 시 재연결 시도"""
```

### 3. Job 실행 테스트

```python
async def test_job_accepted_sent():
    """job_assign 수신 시 job_accepted 전송"""

async def test_dom_extracted_sent():
    """Step 시작 시 dom_extracted 전송"""

async def test_script_execution_success():
    """스크립트 실행 성공 시 script_result(success) 전송"""

async def test_step_completed_on_goal_achieved():
    """goal_achieved 수신 시 step_completed 전송"""

async def test_job_completed_after_all_steps():
    """모든 Step 완료 시 job_completed 전송"""
```

---

## 배포

### PyPI 배포

```bash
# 빌드
poetry build

# PyPI 업로드
poetry publish
```

### 사용자 설치

```bash
pip install nova-agent
```

또는

```bash
pipx install nova-agent
```

---

## 향후 확장

### Phase 2

1. **다중 브라우저 지원**: Firefox, WebKit
2. **병렬 Job 실행**: 동시에 여러 Job 처리
3. **브라우저 프로필**: 쿠키/세션 유지
4. **녹화 모드**: 사용자 행동 녹화
5. **로컬 AI**: 간단한 요소 인식 AI

### Phase 3

1. **데스크톱 앱**: Electron 기반 GUI
2. **자동 업데이트**: 버전 자동 업데이트
3. **플러그인 시스템**: 사용자 정의 스크립트
