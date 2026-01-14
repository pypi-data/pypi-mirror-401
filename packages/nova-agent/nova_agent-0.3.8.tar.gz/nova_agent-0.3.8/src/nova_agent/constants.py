"""Nova Agent constants.

환경별로 변경되는 설정은 settings.py를 사용하세요.
이 파일은 변경되지 않는 상수만 포함합니다.
"""

from pathlib import Path

# Config paths (기본값, settings에서 오버라이드 가능)
CONFIG_DIR = Path.home() / ".nova-agent"
TOKEN_FILE = CONFIG_DIR / "token"

# WebSocket protocol constants
WS_PING_INTERVAL = 20
WS_PING_TIMEOUT = 10

# Browser timeouts (ms)
NAVIGATION_TIMEOUT = 30000
ACTION_TIMEOUT = 7000  # 액션(클릭, 입력 등) 타임아웃

# Message types - Agent → Gateway
MSG_AGENT_CONNECT = "agent_connect"
MSG_REGISTER = "register"
MSG_HEARTBEAT = "heartbeat"
MSG_JOB_ACCEPTED = "job_accepted"
MSG_JOB_ASSIGN_FAILED = "job_assign_failed"
MSG_STEP_STARTED = "step_started"
MSG_DOM_EXTRACTED = "dom_extracted"
MSG_SCRIPT_RESULT = "script_result"
MSG_STEP_COMPLETED = "step_completed"
MSG_GOAL_ACHIEVED = "goal_achieved"
MSG_JOB_COMPLETED = "job_completed"
MSG_ERROR = "error"

# Message types - Gateway → Agent
MSG_REGISTERED = "registered"
MSG_REGISTER_ACK = "register_ack"
MSG_HEARTBEAT_ACK = "heartbeat_ack"
MSG_JOB_ASSIGN = "job_assign"
MSG_EXTRACT_DOM = "extract_dom"
MSG_EXECUTE_SCRIPT = "execute_script"
MSG_NEXT_STEP = "next_step"
MSG_JOB_CANCEL = "job_cancel"
MSG_CHECK_GOAL = "check_goal"
MSG_GOAL_ACHIEVED_FROM_RUNNER = "goal_achieved"  # Runner가 보내는 goal_achieved (check_goal과 동일 처리)
