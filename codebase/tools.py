
"""Công cụ của bài toán — NHÓM VIẾT. Điền ở guide bước 2.2 (thiết kế) và 3.2 (code).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Số công cụ, kiểu công cụ do thiết kế của nhóm quyết định — có bài chỉ cần một công cụ tra cứu.
Công cụ có tác động ra ngoài: KHÔNG tự làm. Trả về bản nháp chờ người duyệt (guide bước 2.2, "chỗ người duyệt").
Dữ liệu công cụ đọc (bài mẫu, thông báo mẫu, lịch…): để trong data/ và mô tả ở data/DATA_CARD.md.
"""

from pathlib import Path
from uuid import uuid4

if __package__:
    from .tracing import tool, TOOLS
    from .data_adapter import (
        load_transactions,
        load_scam_cases,
    )
else:
    from tracing import tool, TOOLS
    from data_adapter import (
        load_transactions,
        load_scam_cases,
    )


# ============================================================
# TRACK E3 — NHÓM DTMD
# Giao dịch nghi lừa đảo bị tạm chặn
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


# ============================================================
# HÀM HỖ TRỢ TRA CỨU DỮ LIỆU
# ============================================================

def _find_held_transaction(tx_id: str) -> dict:
    """Tra cứu nội bộ, không đăng ký thành công cụ.

    Dữ liệu được đọc thông qua Data Adapter,
    hỗ trợ JSONL của pipeline và JSON fixture kiểm thử.
    """

    records = load_transactions(DATA_DIR)

    for record in records:
        if record.get("tx_id") != tx_id:
            continue

        if record.get("status") != "TEMP_HELD":
            return {
                "ok": False,
                "error": "TRANSACTION_NOT_HELD",
            }

        return {
            "ok": True,
            "sandbox": True,
            "transaction": {
                "tx_id": record["tx_id"],
                "user_id": record["user_id"],
                "amount": record.get("amount"),
                "currency": record.get("currency", "VND"),
                "recipient": record.get("recipient"),
                "status": record["status"],
                "face_id_verified": record.get(
                    "face_id_verified"
                ),
                "memo": record.get("memo", ""),
                "transaction_flags": record.get(
                    "transaction_flags", {}
                ),
            },
        }

    return {
        "ok": False,
        "error": "TRANSACTION_NOT_FOUND",
    }


# ============================================================
# TOOL 01 — TRA CỨU GIAO DỊCH TẠM CHẶN
# ============================================================

@tool
def get_held_transaction(tx_id: str) -> dict:
    """Tra cứu thông tin giao dịch đang bị tạm chặn.

    Input: mã giao dịch tx_id (str).
    Output: hồ sơ giao dịch, trạng thái và cờ T01–T04 (dict).
    Tác động ra ngoài: không; chỉ đọc dữ liệu sandbox.
    """

    return _find_held_transaction(tx_id)


# ============================================================
# TOOL 02 — YÊU CẦU XÁC MINH NGỮ CẢNH
# Mức tự động hóa 1
# ============================================================

@tool
def request_verification(
    user_id: str,
    question: str,
) -> dict:
    """Chuẩn bị một câu hỏi xác minh ngữ cảnh giao dịch.

    Input: mã người dùng (str), câu hỏi xác minh (str).
    Output: câu hỏi đã chuẩn bị để hiển thị trong chat (dict).
    Tác động ra ngoài: không; không gửi OTP hay thông báo thật.
    """

    question = question.strip()

    # Chỉ chấp nhận một câu hỏi.
    if not question or question.count("?") != 1:
        return {
            "ok": False,
            "error": "INVALID_QUESTION",
        }

    if not question.endswith("?"):
        return {
            "ok": False,
            "error": "INVALID_QUESTION",
        }

    return {
        "ok": True,
        "sandbox": True,
        "user_id": user_id,
        "question": question,
        "status": "QUESTION_PREPARED",
    }


# ============================================================
# TOOL 03 — DUY TRÌ TRẠNG THÁI TẠM CHẶN
# Mức tự động hóa 2
# ============================================================

@tool
def hold_transaction(tx_id: str) -> dict:
    """Xác nhận duy trì trạng thái tạm chặn hiện tại.

    Input: mã giao dịch tx_id (str).
    Output: trạng thái TEMP_HELD và kết quả xử lý (dict).
    Tác động ra ngoài: không; không thay đổi dữ liệu hoặc dòng tiền.
    """

    result = _find_held_transaction(tx_id)

    if not result["ok"]:
        return result

    return {
        "ok": True,
        "sandbox": True,
        "tx_id": tx_id,
        "status": "TEMP_HELD",
        "action": "KEEP_HOLD",
        "state_changed": False,
        "funds_released": False,
    }


# ============================================================
# TOOL 04 — CHUYỂN TƯ VẤN VIÊN
# Mức tự động hóa 3 — Human-in-the-Loop
# ============================================================

@tool
def handoff_to_agent(
    chat_id: str,
    summary: dict,
    priority: str,
) -> dict:
    """Tạo bản nháp hồ sơ bàn giao cho tư vấn viên.

    Input: mã phiên chat (str), hồ sơ tóm tắt (dict),
           mức ưu tiên NORMAL/HIGH/SECURITY (str).
    Output: mã ticket mô phỏng và hồ sơ bàn giao (dict).
    Tác động ra ngoài: không; chỉ tạo bản nháp chờ người duyệt.
    """

    allowed_priorities = {
        "NORMAL",
        "HIGH",
        "SECURITY",
    }

    if priority not in allowed_priorities:
        return {
            "ok": False,
            "error": "INVALID_PRIORITY",
        }

    if not isinstance(summary, dict):
        return {
            "ok": False,
            "error": "INVALID_SUMMARY",
        }

    required_fields = {
        "transaction_id",
        "hold_reason",
        "classification",
        "context_flags",
        "recommended_action",
    }

    missing = required_fields - summary.keys()

    if missing:
        return {
            "ok": False,
            "error": "INCOMPLETE_HANDOFF",
            "missing_fields": sorted(missing),
        }

    return {
        "ok": True,
        "sandbox": True,
        "ticket_id": f"TICKET-{uuid4().hex[:8]}",
        "chat_id": chat_id,
        "priority": priority,
        "status": "DRAFT",
        "summary": summary,
        "sent_to_real_advisor": False,
    }


# ============================================================
# TOOL 05 — ĐÓNG BĂNG PHIÊN / BẢO VỆ VÍ
# Mức tự động hóa 3 — Human-in-the-Loop
# ============================================================

@tool
def freeze_session(user_id: str) -> dict:
    """Tạo bản nháp yêu cầu đóng băng phiên/bảo vệ ví khi nghi ngờ ATO.

    Input: mã người dùng (str).
    Output: mã yêu cầu và trạng thái chờ phê duyệt (dict).
    Tác động ra ngoài: không; không khóa ví thật, không tự đóng băng.
    """

    return {
        "ok": True,
        "sandbox": True,
        "request_id": f"FREEZE-{uuid4().hex[:8]}",
        "user_id": user_id,
        "status": "PENDING_HUMAN_APPROVAL",
        "session_frozen": False,
    }


# ============================================================
# RETRIEVAL — TRA CỨU CA LỪA ĐẢO TƯƠNG ĐỒNG
# Hàm nội bộ, không đăng ký vào danh sách TOOLS
# ============================================================

def search_scam_cases(
    rule_ids: list[str],
    limit: int = 3,
) -> list:
    """Tra cứu ca lừa đảo tương đồng theo mã luật.

    Input: danh sách mã luật R01–R07, R16, R20 (list),
           số kết quả tối đa (int).
    Output: danh sách ca tương đồng và nguồn dữ liệu (list).
    Tác động ra ngoài: không; chỉ đọc dữ liệu qua Data Adapter.
    """

    if not rule_ids or limit <= 0:
        return []

    records = load_scam_cases(DATA_DIR)

    requested_rules = set(rule_ids)

    matches = []

    for record in records:
        overlap = requested_rules.intersection(
            record.get("rule_ids", [])
        )

        if overlap:
            matches.append(
                (len(overlap), record)
            )

    # Ưu tiên ca có nhiều mã luật trùng khớp hơn.
    matches.sort(
        key=lambda item: (
            -item[0],
            item[1].get("case_id", ""),
        )
    )

    return [
        record
        for _, record in matches[:limit]
    ]
