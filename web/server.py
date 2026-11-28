"""Backend tích hợp — Task 1 & Task 5.

Expose session_manager.py (Task 2) qua HTTP API đơn giản để
frontend (vi_an_toan_mvp_v2.html) gọi vào Agent thật, hỗ trợ
hội thoại nhiều lượt, và hiển thị bằng chứng dùng AI thật
(tên model, số lần gọi model, token usage, hành động Agent).

Chạy:
    cd project/
    python3 web/server.py
Mặc định phục vụ ở http://127.0.0.1:5000

Muốn chạy với model thật: tạo file .env ở project/ (cùng cấp
với codebase/ và data/) theo mẫu .env.example, rồi chạy lại.
Không cần sửa file này để đổi provider — ai.py tự đọc .env.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, request, jsonify, send_from_directory  # noqa: E402
from web.session_manager import manager  # noqa: E402
from codebase import ai  # noqa: E402

app = Flask(__name__, static_folder=None)


@app.after_request
def add_cors_headers(response):
    # Cho phép frontend tĩnh (file:// hoặc server khác) gọi vào.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/api/health", methods=["GET"])
def health():
    """Cho frontend biết backend đang chạy provider nào.

    Đây là một phần của Task 5: minh bạch ngay từ đầu cho
    người dùng/giám khảo biết hệ thống đang nói chuyện với
    model thật hay model giả lập cục bộ.
    """

    return jsonify(
        {
            "ok": True,
            "model_provider": ai.MODEL_PROVIDER,
            "model_name": ai.MODEL_NAME or None,
            "is_real_model": ai.MODEL_PROVIDER != "fake",
        }
    )


@app.route("/api/session/start", methods=["POST"])
def start_session():
    """Task 1 & 2: tạo session mới cho một cuộc hội thoại.

    Body JSON tuỳ chọn: {"tx_id": "...", "authenticated_user_id": "..."}
    Mặc định dùng TX-0001 / USER-0001 nếu không truyền.
    """

    body = request.get_json(silent=True) or {}

    session_id = manager.start_session(
        tx_id=body.get("tx_id", "TX-0001"),
        authenticated_user_id=body.get(
            "authenticated_user_id", "USER-0001"
        ),
    )

    return jsonify({"ok": True, "session_id": session_id})


@app.route("/api/session/<session_id>/reset", methods=["POST"])
def reset_session(session_id):
    """Task 2: bắt đầu lại tình huống trong cùng session_id."""

    body = request.get_json(silent=True) or {}

    ok = manager.reset_session(
        session_id,
        tx_id=body.get("tx_id", "TX-0001"),
        authenticated_user_id=body.get(
            "authenticated_user_id", "USER-0001"
        ),
    )

    if not ok:
        return jsonify({"ok": False, "error": "SESSION_NOT_FOUND"}), 404

    return jsonify({"ok": True})


@app.route("/api/session/<session_id>/message", methods=["POST"])
def send_message(session_id):
    """Task 1: gửi một lượt chat, nhận lại phản hồi Agent + bằng chứng AI.

    Body JSON bắt buộc: {"text": "..."}
    """

    body = request.get_json(silent=True) or {}
    text = body.get("text", "")

    if not text.strip():
        return jsonify({"ok": False, "error": "EMPTY_MESSAGE"}), 400

    try:
        result = manager.send_message(session_id, text)
    except KeyError:
        return jsonify({"ok": False, "error": "SESSION_NOT_FOUND"}), 404

    return jsonify(
        {
            "ok": True,
            "output": result["output"],
            "classification": result["classification"],
            "action": result["action"],
            "tier": result.get("tier"),
            "priority": result.get("priority"),
            "tools_used": result.get("tools_used", []),
            # Task 5 — bằng chứng dùng AI thật cho lượt này
            # và cộng dồn cho cả session.
            "evidence": {
                "turn": result["turn_trace"]["summary"],
                "session_total": result["session_trace"]["summary"],
            },
        }
    )


@app.route("/api/session/<session_id>/history", methods=["GET"])
def get_history(session_id):
    """Task 2: lấy lại lịch sử hội thoại để hiển thị khi quay lại."""

    try:
        history = manager.get_history(session_id)
    except KeyError:
        return jsonify({"ok": False, "error": "SESSION_NOT_FOUND"}), 404

    return jsonify({"ok": True, "history": history})


@app.route("/api/session/<session_id>/evidence", methods=["GET"])
def get_evidence(session_id):
    """Task 5: bằng chứng AI thật cộng dồn của cả session, dùng
    để hiển thị ở panel "bằng chứng" trên giao diện tư vấn viên."""

    try:
        summary = manager.get_trace_summary(session_id)
    except KeyError:
        return jsonify({"ok": False, "error": "SESSION_NOT_FOUND"}), 404

    return jsonify(
        {
            "ok": True,
            "model_provider": ai.MODEL_PROVIDER,
            "is_real_model": ai.MODEL_PROVIDER != "fake",
            "summary": summary,
        }
    )


@app.route("/")
def index():
    html_path = PROJECT_ROOT / "web" / "vi_an_toan_mvp_v2.html"
    return send_from_directory(html_path.parent, html_path.name)


if __name__ == "__main__":
    print(f"MODEL_PROVIDER hiện tại: {ai.MODEL_PROVIDER}")
    if ai.MODEL_PROVIDER == "fake":
        print(
            "⚠ Đang chạy với model GIẢ LẬP (fake). "
            "Tạo file .env ở thư mục project/ để dùng model thật."
        )
    app.run(host="127.0.0.1", port=5000, debug=False)
