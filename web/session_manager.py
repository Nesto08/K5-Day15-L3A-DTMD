"""Session Manager — Task 2.

Quản lý nhiều phiên hội thoại độc lập cho ứng dụng web demo.
Mỗi session:
    - giữ state hội thoại riêng (qua agent.create_session()),
    - giữ lịch sử hội thoại riêng để hiển thị lại trên UI,
    - giữ trace riêng (model_calls, tool_calls, tokens...) cho Task 5,
    - có thể "bắt đầu lại tình huống" (reset) mà không ảnh hưởng
      session khác.

Không sửa codebase/agent.py hay codebase/tracing.py.
Lớp này chỉ gọi đúng contract public: create_session(), run_agent().
"""

import sys
import threading
import time
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from codebase import agent, tracing  # noqa: E402


class SessionManager:
    """Giữ một dict session_id -> SessionState trong bộ nhớ tiến trình.

    Dùng threading.Lock vì tracing.py dùng một biến toàn cục
    (_case) cho mọi lời gọi model/tool trong tiến trình — nếu
    hai session chạy run_agent() đồng thời, trace sẽ lẫn vào
    nhau. Lock đảm bảo tại một thời điểm chỉ một session được
    "begin...end" trace.
    """

    def __init__(self):
        self._sessions = {}
        self._lock = threading.Lock()

    def start_session(
        self,
        tx_id="TX-0001",
        authenticated_user_id="USER-0001",
        chat_id=None,
    ):
        """Tạo một session hội thoại mới, độc lập.

        Input: tx_id, authenticated_user_id (phải đến từ backend
            đã xác thực trong hệ thống thật — ở demo này do
            người gọi hàm cung cấp), chat_id tuỳ chọn.
        Output: session_id (str) để dùng cho các lệnh gọi sau.
        Tác động ra ngoài: không; chỉ lưu state trong bộ nhớ.
        """

        session_id = uuid.uuid4().hex[:12]
        chat_id = chat_id or f"CHAT-{session_id}"

        with self._lock:
            self._sessions[session_id] = {
                "session_id": session_id,
                "agent_session": agent.create_session(
                    tx_id=tx_id,
                    authenticated_user_id=authenticated_user_id,
                    chat_id=chat_id,
                ),
                "history": [],       # [{role, text, ts}]
                "trace_events": [],  # toàn bộ event từ mọi lượt
                "trace_summary": {
                    "model_calls": 0,
                    "tool_calls": 0,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "models": [],
                    "errors": [],
                },
                "created_at": time.time(),
            }

        return session_id

    def reset_session(
        self,
        session_id,
        tx_id="TX-0001",
        authenticated_user_id="USER-0001",
    ):
        """Bắt đầu lại tình huống trong cùng một session_id.

        Input: session_id hiện có, tx_id/user_id mới (có thể
            giữ nguyên để thử lại đúng tình huống, hoặc đổi
            sang tx_id khác để thử tình huống khác).
        Output: True nếu reset thành công, False nếu không
            tìm thấy session_id.
        Tác động ra ngoài: không; chỉ xoá context/lịch sử cũ
            của riêng session này trong bộ nhớ.
        """

        with self._lock:
            if session_id not in self._sessions:
                return False

            chat_id = self._sessions[session_id][
                "agent_session"
            ]["chat_id"]

            self._sessions[session_id].update(
                agent_session=agent.create_session(
                    tx_id=tx_id,
                    authenticated_user_id=authenticated_user_id,
                    chat_id=chat_id,
                ),
                history=[],
                trace_events=[],
                trace_summary={
                    "model_calls": 0,
                    "tool_calls": 0,
                    "tokens_in": 0,
                    "tokens_out": 0,
                    "models": [],
                    "errors": [],
                },
            )

        return True

    def send_message(self, session_id, text):
        """Gửi một lượt chat vào session, trả kết quả Agent.

        Input: session_id, text (nội dung người dùng gõ).
        Output: dict gồm kết quả run_agent() (output,
            classification, action, tier, ...) cộng thêm
            "turn_trace" (trace riêng của lượt này) và
            "session_trace" (tổng trace cộng dồn cả session).
        Tác động ra ngoài: không trực tiếp; agent.run_agent()
            có thể gọi các tool mô phỏng (không có tác động
            tài chính thật — xem tools.py).

        Nhiều session có thể gọi hàm này đồng thời; self._lock
        đảm bảo mỗi lượt begin()/end() trace không bị lẫn với
        lượt của session khác đang chạy song song.
        """

        with self._lock:
            if session_id not in self._sessions:
                raise KeyError(f"Unknown session_id: {session_id}")

            state = self._sessions[session_id]
            case_id = f"{session_id}-turn-{len(state['history']) // 2 + 1}"

            tracing.begin(case_id)

            try:
                result = agent.run_agent(
                    text, state["agent_session"]
                )
            finally:
                turn_summary, turn_events = tracing.end()

            now = time.time()
            state["history"].append(
                {"role": "user", "text": text, "ts": now}
            )
            state["history"].append(
                {
                    "role": "agent",
                    "text": result.get("output", ""),
                    "ts": now,
                    "classification": result.get("classification"),
                    "action": result.get("action"),
                }
            )

            state["trace_events"].extend(turn_events)

            summary = state["trace_summary"]
            summary["model_calls"] += turn_summary["model_calls"]
            summary["tool_calls"] += turn_summary["tool_calls"]
            summary["tokens_in"] += turn_summary["tokens_in"]
            summary["tokens_out"] += turn_summary["tokens_out"]
            summary["models"] = sorted(
                set(summary["models"]) | set(turn_summary["models"])
            )
            summary["errors"].extend(turn_summary["errors"])

            return {
                **result,
                "session_id": session_id,
                "turn_trace": {
                    "summary": turn_summary,
                    "events": turn_events,
                },
                "session_trace": {
                    "summary": dict(summary),
                    "events": list(state["trace_events"]),
                },
            }

    def get_history(self, session_id):
        """Trả lịch sử hội thoại (list) của một session."""

        with self._lock:
            if session_id not in self._sessions:
                raise KeyError(f"Unknown session_id: {session_id}")
            return list(self._sessions[session_id]["history"])

    def get_trace_summary(self, session_id):
        """Trả tổng trace cộng dồn (dict) của một session."""

        with self._lock:
            if session_id not in self._sessions:
                raise KeyError(f"Unknown session_id: {session_id}")
            return dict(self._sessions[session_id]["trace_summary"])

    def end_session(self, session_id):
        """Xoá hẳn một session khỏi bộ nhớ (đóng hội thoại)."""

        with self._lock:
            self._sessions.pop(session_id, None)


# Một instance dùng chung cho toàn bộ tiến trình web server.
manager = SessionManager()
