
"""Deterministic contextual rulebase for Track E3."""

from enum import Enum
from typing import Optional


class RuleStatus(str, Enum):
    MATCHED = "MATCHED"
    NOT_MATCHED = "NOT_MATCHED"
    UNKNOWN = "UNKNOWN"


RULEBASE_VERSION = "E3-context-v1.0"

TRANSACTION_RULES = {
    "T01": "TRUSTED_RECIPIENT",
    "T02": "HIGH_AMOUNT_ANOMALY",
    "T03": "NEW_RECIPIENT",
    "T04": "BLACKLIST_HIT",
}

# Each condition contains a fact name
# and its required Boolean value.
CONTEXT_RULES = {
    "R01": (
        ("COERCIVE_PRESSURE", True),
        ("DOCUMENTED_LEGITIMATE_DEADLINE", False),
    ),
    "R02": (
        ("VERIFICATION_BLOCKED", True),
        ("ORDINARY_PRIVACY_REQUEST", False),
    ),
    "R03": (
        ("SPECIFIC_IMPERSONATION_INDICATOR", True),
        ("TRANSFER_REQUEST", True),
        ("SELF_IDENTIFICATION_ONLY", False),
    ),
    "R04": (
        ("PAY_TO_PROVE_OR_UNLOCK", True),
        ("VERIFIABLE_LEGITIMATE_FEE", False),
    ),
    "R05": (
        ("SUSPICIOUS_REQUEST", True),
        ("INDEPENDENT_VERIFICATION_COMPLETED", False),
    ),
    "R06": (
        ("OTHER_PARTY_REQUESTS_SECRET", True),
    ),
    "R07": (
        ("UNREALISTIC_RISK_FREE_RETURN", True),
        ("TRANSFER_REQUEST", True),
        ("TRANSPARENT_RISK_DISCLOSURE", False),
    ),
    "R16": (
        ("OTHER_PARTY_REQUESTS_REMOTE_ACCESS", True),
    ),
    "R20": (
        ("PHISHING_OR_SPOOFED_PORTAL_INDICATOR", True),
    ),
}

SCAM_RULES = {"R01", "R02", "R03", "R04", "R07"}
SAFETY_RULES = {"R06", "R16", "R20"}
VERIFICATION_RULES = {"R05"}


def normalize_transaction_flags(flags: dict) -> dict:
    """Read existing transaction flags without recalculating risk."""
    result = {}

    for rule_id in TRANSACTION_RULES:
        value = flags.get(rule_id)

        if value is True or value == "MATCHED":
            result[rule_id] = RuleStatus.MATCHED.value
        elif value is False or value == "NOT_MATCHED":
            result[rule_id] = RuleStatus.NOT_MATCHED.value
        else:
            result[rule_id] = RuleStatus.UNKNOWN.value

    return result


def evaluate_rule(
    conditions: tuple,
    facts: dict[str, Optional[bool]],
) -> str:
    """Evaluate an AND rule using three-valued logic."""

    has_unknown = False

    for fact_name, expected_value in conditions:
        actual_value = facts.get(fact_name)

        if not isinstance(actual_value, bool):
            has_unknown = True
            continue

        if actual_value != expected_value:
            return RuleStatus.NOT_MATCHED.value

    if has_unknown:
        return RuleStatus.UNKNOWN.value

    return RuleStatus.MATCHED.value


def evaluate_context(
    facts: dict,
    previous_flags: Optional[dict] = None,
) -> dict:
    """Evaluate contextual rules and preserve matched risk flags."""

    safe_facts = dict(facts)
    previous_flags = previous_flags or {}

    # Self-declared verification is not independent evidence.
    if safe_facts.get("VERIFICATION_SOURCE") == "SELF_DECLARED":
        safe_facts["INDEPENDENT_VERIFICATION_COMPLETED"] = None

    results = {}

    for rule_id, conditions in CONTEXT_RULES.items():
        status = evaluate_rule(conditions, safe_facts)

        # Monotonic protection within the same case.
        if previous_flags.get(rule_id) == RuleStatus.MATCHED.value:
            status = RuleStatus.MATCHED.value

        results[rule_id] = status

    return results


def analyze(
    transaction_flags: dict,
    facts: dict,
    previous_flags: Optional[dict] = None,
) -> dict:
    """Build structured risk evidence for the Agent."""

    tx_results = normalize_transaction_flags(transaction_flags)
    context_results = evaluate_context(facts, previous_flags)

    matched = sorted(
        rule_id
        for rule_id, status in context_results.items()
        if status == RuleStatus.MATCHED.value
    )

    unknown = sorted(
        rule_id
        for rule_id, status in context_results.items()
        if status == RuleStatus.UNKNOWN.value
    )

    scam_flags = sorted(set(matched) & SCAM_RULES)
    safety_flags = sorted(set(matched) & SAFETY_RULES)
    verification_flags = sorted(set(matched) & VERIFICATION_RULES)

    return {
        "version": RULEBASE_VERSION,
        "transaction_flags": tx_results,
        "context_flags": context_results,
        "matched_rules": matched,
        "unknown_rules": unknown,
        "scam_flags": scam_flags,
        "safety_flags": safety_flags,
        "verification_flags": verification_flags,
        "blacklist_hit": (
            tx_results["T04"] == RuleStatus.MATCHED.value
        ),
        "has_scam_signal": bool(scam_flags),
        "has_ato_signal": (
            bool(safety_flags)
            or facts.get("USER_DENIES_TRANSACTION") is True
        ),
    }
