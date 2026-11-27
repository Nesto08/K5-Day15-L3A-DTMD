
"""Guardrails — Track E3, nhóm DTMD.

Kiểm soát đầu vào và đầu ra của Agent.
Không gọi LLM, không thực thi hành động tài chính.
"""

import re
import unicodedata


GUARDRAIL_VERSION = "E3-guardrails-v1.0"
MAX_INPUT_LENGTH = 4000

INJECTION_PATTERNS = (
    r"ignore\s+(all\s+)?(previous|prior|system)\s+instructions",
    r"disregard\s+(all\s+)?(previous|system)\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"you\s+are\s+now\s+(an?\s+)?(admin|developer)",
    r"bỏ qua.{0,40}(chỉ dẫn|hướng dẫn|quy tắc|chính sách)",
    r"tiết lộ.{0,30}(system prompt|prompt hệ thống)",
    r"hãy đóng vai.{0,30}(admin|quản trị viên)",
)

BYPASS_PATTERNS = (
    r"bypass.{0,30}(security|verification|hold)",
    r"release_transaction",
    r"(vượt qua|vô hiệu hóa|lách).{0,40}(bảo mật|xác minh|chặn)",
    r"(mở chặn|nhả tiền).{0,40}(không cần|bỏ qua).{0,30}(xác minh|kiểm tra)",
)

PROBING_PATTERNS = (
    r"(dưới|bao nhiêu).{0,40}(không bị|khỏi bị).{0,20}(chặn|hỏi|kiểm tra)",
    r"(chia nhỏ|chia nhiều).{0,40}(né|tránh|qua mặt).{0,20}(chặn|kiểm tra)",
    r"(ngưỡng|hạn mức).{0,40}(né|tránh|không bị).{0,20}(chặn|kiểm tra)",
    r"how much.{0,40}(avoid|bypass).{0,20}(detection|hold)",
)

SENSITIVE_PATTERNS = (
    (
        r"\b(?:otp|pin|mật khẩu|password)"
        r"\s*(?:là|is|:|=)\s*\S+",
        "[REDACTED_SECRET]",
    ),
    (
        r"\b(?:\d[ -]?){12,19}\b",
        "[REDACTED_NUMBER]",
    ),
    (
        r"\b0\d{9}\b",
        "[REDACTED_PHONE]",
    ),
    (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[REDACTED_EMAIL]",
    ),
)

UNSAFE_OUTPUT_PATTERNS = (
    r"(đã|vừa).{0,15}(mở chặn|nhả tiền|giải phóng tiền)",
    r"(đã|vừa).{0,15}(hoàn tiền|khóa ví|khóa tài khoản)",
    r"(chắc chắn|cam kết|đảm bảo).{0,30}(hoàn tiền|an toàn tuyệt đối)",
    r"(hãy|vui lòng|cần).{0,25}(cung cấp|gửi|nhập).{0,20}(otp|pin|mật khẩu)",
    r"(transaction|funds)\s+(has been\s+)?released",
    r"wallet\s+(has been\s+)?locked",
)

SAFE_FALLBACK = (
    "Hiện chưa đủ căn cứ để xác nhận giao dịch an toàn. "
    "Không cung cấp OTP, PIN hoặc mật khẩu cho bất kỳ ai. "
    "Vui lòng liên hệ bộ phận hỗ trợ chính thức của ví "
    "để được kiểm tra."
)


def normalize_text(text: str) -> str:
    """Chuẩn hóa Unicode và loại ký tự ẩn."""

    text = unicodedata.normalize("NFKC", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Cf"
    )

    return " ".join(text.split())


def _matches(text: str, patterns: tuple) -> bool:
    """Kiểm tra văn bản có khớp mẫu regex không."""

    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def redact_sensitive(text: str) -> str:
    """Che dữ liệu nhạy cảm trước khi gửi model."""

    result = text

    for pattern, replacement in SENSITIVE_PATTERNS:
        result = re.sub(
            pattern,
            replacement,
            result,
            flags=re.IGNORECASE,
        )

    return result


def inspect_input(text: str) -> dict:
    """Kiểm tra đầu vào trước khi gọi LLM.

    Input: nội dung chat (str).
    Output: nội dung đã xử lý, cờ rủi ro và quyết định.
    Tác động ra ngoài: không.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "allowed": False,
            "sanitized_text": "",
            "flags": ["EMPTY_INPUT"],
            "action": "ASK_VALID_INPUT",
        }

    if len(text) > MAX_INPUT_LENGTH:
        return {
            "allowed": False,
            "sanitized_text": "",
            "flags": ["INPUT_TOO_LONG"],
            "action": "ASK_SHORTER_INPUT",
        }

    normalized = normalize_text(text)

    if not normalized:
        return {
            "allowed": False,
            "sanitized_text": "",
            "flags": ["EMPTY_INPUT"],
            "action": "ASK_VALID_INPUT",
        }

    sanitized = redact_sensitive(normalized)
    flags = []

    if normalized != sanitized:
        flags.append("SENSITIVE_DATA_REDACTED")

    if _matches(normalized, INJECTION_PATTERNS):
        flags.append("PROMPT_INJECTION")

    if _matches(normalized, BYPASS_PATTERNS):
        flags.append("SECURITY_BYPASS_REQUEST")

    if _matches(normalized, PROBING_PATTERNS):
        flags.append("THRESHOLD_PROBING")

    blocked_flags = {
        "PROMPT_INJECTION",
        "SECURITY_BYPASS_REQUEST",
        "THRESHOLD_PROBING",
    }

    blocked = bool(set(flags) & blocked_flags)

    return {
        "version": GUARDRAIL_VERSION,
        "allowed": not blocked,
        "sanitized_text": sanitized,
        "flags": flags,
        "action": (
            "REFUSE_UNSAFE_REQUEST"
            if blocked
            else "CONTINUE"
        ),
    }


def inspect_output(text: str) -> dict:
    """Kiểm tra phản hồi trước khi hiển thị cho người dùng.

    Input: phản hồi dự kiến của Agent (str).
    Output: phản hồi an toàn và cờ kiểm tra (dict).
    Tác động ra ngoài: không.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "allowed": False,
            "output": SAFE_FALLBACK,
            "flags": ["INVALID_OUTPUT"],
        }

    normalized = normalize_text(text)
    sanitized = redact_sensitive(normalized)

    flags = []

    if normalized != sanitized:
        flags.append("SENSITIVE_DATA_REDACTED")

    if _matches(normalized, UNSAFE_OUTPUT_PATTERNS):
        flags.append("UNSAFE_OUTPUT")

        return {
            "allowed": False,
            "output": SAFE_FALLBACK,
            "flags": flags,
        }

    return {
        "allowed": True,
        "output": sanitized,
        "flags": flags,
    }
