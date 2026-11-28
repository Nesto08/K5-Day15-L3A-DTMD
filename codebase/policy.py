
"""Policy Engine — Track E3, nhóm DTMD.

Tầng quyết định xác định bằng Python, không gọi LLM.
LLM chỉ đề xuất phân loại; Policy Engine quyết định
hành động được phép dựa trên bằng chứng và quyền hạn.
"""

POLICY_VERSION = "E3-policy-v1.0"

VALID_CLASSIFICATIONS = {
    "suspected_scam",
    "legitimate_urgent",
    "account_takeover",
    "unclear",
}

SAFE_QUESTION = (
    "Có ai đang yêu cầu hoặc gây áp lực "
    "buộc bạn thực hiện giao dịch này không?"
)
UNAUTHORIZED_TRANSACTION_QUESTION = (
    "Bạn có thấy giao dịch nào trong lịch sử ví mà bạn không thực hiện không?"
)


def _decision(
    classification: str,
    action: str,
    tier: int,
    tools: list,
    reason: str,
    priority=None,
    question=None,
) -> dict:
    """Tạo kết quả quyết định có cấu trúc."""

    return {
        "policy_version": POLICY_VERSION,
        "classification": classification,
        "action": action,
        "tier": tier,
        "allowed_tools": tools,
        "reason": reason,
        "priority": priority,
        "question": question,
        "release_allowed": False,
        "requires_human_approval": tier == 3,
    }


def authorize_transaction(
    transaction: dict,
    authenticated_user_id: str,
) -> bool:
    """Kiểm tra quyền sở hữu giao dịch.

    authenticated_user_id phải đến từ session
    đáng tin cậy, không lấy từ lời tự khai trong chat.
    """

    if not authenticated_user_id:
        return False

    if not isinstance(transaction, dict):
        return False

    return (
        transaction.get("user_id")
        == authenticated_user_id
    )


def decide(
    classification: str,
    evidence: dict,
    *,
    authorized: bool = False,
    question_count: int = 0,
    legitimate_evidence_verified: bool = False,
    model_failed: bool = False,
    asks_about_unauthorized_transaction: bool = False,
) -> dict:
    """Quyết định hành động an toàn cho Agent.

    Input:
        classification: phân loại do LLM đề xuất.
        evidence: kết quả analyze() của Rulebase.
        authorized: quyền truy cập đã được kiểm tra.
        question_count: số câu hỏi trong cùng hồ sơ.
        legitimate_evidence_verified: chứng từ hợp lệ
            đã được xác nhận từ nguồn đáng tin cậy.
        model_failed: model lỗi hoặc không trả kết quả.

    Output:
        Quyết định, mức tự động hóa, công cụ được phép.

    Tác động ra ngoài:
        Không. Hàm chỉ quyết định, không thực thi tool.
    """

    # ------------------------------------------------
    # 0. Kiểm tra quyền hạn
    # ------------------------------------------------

    if authorized is not True:
        return _decision(
            classification="unclear",
            action="DENY_UNAUTHORIZED",
            tier=0,
            tools=[],
            reason="Không có quyền truy cập giao dịch.",
        )

    # ------------------------------------------------
    # 1. Account Takeover — ưu tiên cao nhất
    # ------------------------------------------------

    if (
        evidence.get("has_ato_signal") is True
        or classification == "account_takeover"
    ):
        return _decision(
            classification="account_takeover",
            action="DRAFT_LOCK_AND_ESCALATE_SECURITY",
            tier=3,
            tools=[
                "lock_wallet",
                "handoff_to_agent",
            ],
            reason="Phát hiện dấu hiệu chiếm tài khoản.",
            priority="SECURITY",
        )

    # ------------------------------------------------
    # 2. APP Scam / Blacklist
    # ------------------------------------------------

    if (
        evidence.get("blacklist_hit") is True
        or evidence.get("has_scam_signal") is True
        or classification == "suspected_scam"
    ):
        return _decision(
            classification="suspected_scam",
            action="KEEP_HOLD_AND_WARN",
            tier=2,
            tools=["hold_transaction"],
            reason="Có dấu hiệu giao dịch không an toàn.",
        )

    # ------------------------------------------------
    # 3. Model lỗi hoặc classification không hợp lệ
    # ------------------------------------------------

    if (
        model_failed
        or classification not in VALID_CLASSIFICATIONS
    ):
        return _decision(
            classification="unclear",
            action="KEEP_HOLD_AND_ESCALATE",
            tier=3,
            tools=[
                "hold_transaction",
                "handoff_to_agent",
            ],
            reason="Không đủ căn cứ để tự động quyết định.",
            priority="NORMAL",
        )

    # ------------------------------------------------
    # 4. Giao dịch gấp thật
    # ------------------------------------------------

    if classification == "legitimate_urgent":

        transaction_flags = evidence.get(
            "transaction_flags", {}
        )

        if (
            legitimate_evidence_verified is True
            and transaction_flags.get("T04")
            == "NOT_MATCHED"
        ):
            return _decision(
                classification="legitimate_urgent",
                action="ESCALATE_PRIORITY_ADVISOR",
                tier=3,
                tools=["handoff_to_agent"],
                reason=(
                    "Có căn cứ về nhu cầu thanh toán "
                    "khẩn cấp; cần tư vấn viên duyệt."
                ),
                priority="HIGH",
            )

        # Chưa xác minh được chứng từ:
        # không mở tiền nhưng cũng không bỏ lơ.
        return _decision(
            classification="unclear",
            action="KEEP_HOLD_AND_ESCALATE",
            tier=3,
            tools=[
                "hold_transaction",
                "handoff_to_agent",
            ],
            reason=(
                "Người dùng báo cần thanh toán gấp "
                "nhưng chưa đủ căn cứ xác minh."
            ),
            priority="HIGH",
        )

    # ------------------------------------------------
    # 5. Chưa rõ — chỉ hỏi một câu
    # ------------------------------------------------

    if question_count == 0:
        decision = _decision(
            classification="unclear",
            action="EXPLAIN_AND_ASK_ONE_QUESTION",
            tier=1,
            tools=["request_verification"],
            reason="Cần thêm thông tin về ngữ cảnh.",
            question=(
                UNAUTHORIZED_TRANSACTION_QUESTION
                if asks_about_unauthorized_transaction else SAFE_QUESTION
            ),
        )
        if asks_about_unauthorized_transaction:
            decision["question_fact"] = "USER_DENIES_TRANSACTION"
        return decision

    # ------------------------------------------------
    # 6. Vẫn chưa rõ sau khi đã hỏi
    # ------------------------------------------------

    return _decision(
        classification="unclear",
        action="KEEP_HOLD_AND_ESCALATE",
        tier=3,
        tools=[
            "hold_transaction",
            "handoff_to_agent",
        ],
        reason=(
            "Đã hỏi xác minh nhưng vẫn chưa đủ thông tin."
        ),
        priority="NORMAL",
    )


def is_tool_allowed(
    tool_name: str,
    decision: dict,
) -> bool:
    """Kiểm tra công cụ trước khi thực thi."""

    safe_tools = {
        "request_verification",
        "hold_transaction",
        "handoff_to_agent",
        "lock_wallet",
    }

    return (
        tool_name in safe_tools
        and tool_name in decision.get(
            "allowed_tools", []
        )
    )
