
import unittest

from codebase.policy import (
    authorize_transaction,
    decide,
    is_tool_allowed,
)

from codebase.rulebase import analyze


class TestPolicy(unittest.TestCase):

    def setUp(self):
        self.evidence = analyze(
            {
                "T02": True,
                "T03": True,
                "T04": False,
            },
            {},
        )

    def test_authorized_owner(self):
        self.assertTrue(
            authorize_transaction(
                {"user_id": "USER001"},
                "USER001",
            )
        )

    def test_unauthorized_owner(self):
        self.assertFalse(
            authorize_transaction(
                {"user_id": "USER001"},
                "USER002",
            )
        )

    def test_missing_identity(self):
        self.assertFalse(
            authorize_transaction(
                {"user_id": None},
                None,
            )
        )

    def test_deny_unauthorized(self):
        result = decide(
            "legitimate_urgent",
            self.evidence,
            authorized=False,
        )

        self.assertEqual(
            result["action"],
            "DENY_UNAUTHORIZED",
        )
        self.assertEqual(result["allowed_tools"], [])

    def test_suspected_scam(self):
        result = decide(
            "suspected_scam",
            self.evidence,
            authorized=True,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_WARN",
        )
        self.assertEqual(result["tier"], 2)

    def test_blacklist_overrides_llm(self):
        evidence = analyze({"T04": True}, {})

        result = decide(
            "legitimate_urgent",
            evidence,
            authorized=True,
            legitimate_evidence_verified=True,
        )

        self.assertEqual(
            result["classification"],
            "suspected_scam",
        )

    def test_scam_rule_overrides_llm(self):
        evidence = analyze(
            {"T02": True},
            {
                "COERCIVE_PRESSURE": True,
                "DOCUMENTED_LEGITIMATE_DEADLINE": False,
            },
        )

        result = decide(
            "legitimate_urgent",
            evidence,
            authorized=True,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_WARN",
        )

    def test_ato(self):
        result = decide(
            "account_takeover",
            self.evidence,
            authorized=True,
        )

        self.assertEqual(
            result["action"],
            "DRAFT_LOCK_AND_ESCALATE_SECURITY",
        )
        self.assertEqual(result["priority"], "SECURITY")
        self.assertIn(
            "lock_wallet",
            result["allowed_tools"],
        )

    def test_ato_overrides_scam(self):
        evidence = analyze(
            {"T04": True},
            {"OTHER_PARTY_REQUESTS_SECRET": True},
        )

        result = decide(
            "suspected_scam",
            evidence,
            authorized=True,
        )

        self.assertEqual(
            result["classification"],
            "account_takeover",
        )

    def test_legitimate_urgent(self):
        result = decide(
            "legitimate_urgent",
            self.evidence,
            authorized=True,
            legitimate_evidence_verified=True,
        )

        self.assertEqual(
            result["action"],
            "ESCALATE_PRIORITY_ADVISOR",
        )
        self.assertEqual(result["priority"], "HIGH")
        self.assertTrue(
            result["requires_human_approval"]
        )

    def test_unverified_urgent(self):
        result = decide(
            "legitimate_urgent",
            self.evidence,
            authorized=True,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_ESCALATE",
        )
        self.assertEqual(result["priority"], "HIGH")

    def test_unknown_blacklist_status(self):
        evidence = analyze({}, {})

        result = decide(
            "legitimate_urgent",
            evidence,
            authorized=True,
            legitimate_evidence_verified=True,
        )

        self.assertNotEqual(
            result["action"],
            "ESCALATE_PRIORITY_ADVISOR",
        )

    def test_unclear_first_question(self):
        result = decide(
            "unclear",
            self.evidence,
            authorized=True,
            question_count=0,
        )

        self.assertEqual(
            result["action"],
            "EXPLAIN_AND_ASK_ONE_QUESTION",
        )
        self.assertEqual(
            result["question"].count("?"), 1
        )

    def test_unclear_after_question(self):
        result = decide(
            "unclear",
            self.evidence,
            authorized=True,
            question_count=1,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_ESCALATE",
        )
        self.assertNotIn(
            "request_verification",
            result["allowed_tools"],
        )

    def test_model_failure(self):
        result = decide(
            "unclear",
            self.evidence,
            authorized=True,
            model_failed=True,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_ESCALATE",
        )

    def test_invalid_classification(self):
        result = decide(
            "release_transaction",
            self.evidence,
            authorized=True,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_ESCALATE",
        )

    def test_release_never_allowed(self):
        for label in (
            "suspected_scam",
            "legitimate_urgent",
            "account_takeover",
            "unclear",
        ):
            result = decide(
                label,
                self.evidence,
                authorized=True,
                legitimate_evidence_verified=True,
            )

            self.assertFalse(result["release_allowed"])
            self.assertFalse(
                is_tool_allowed(
                    "release_transaction", result
                )
            )

    def test_allowed_tool(self):
        result = decide(
            "suspected_scam",
            self.evidence,
            authorized=True,
        )

        self.assertTrue(
            is_tool_allowed(
                "hold_transaction", result
            )
        )

    def test_disallowed_tool(self):
        result = decide(
            "unclear",
            self.evidence,
            authorized=True,
        )

        self.assertFalse(
            is_tool_allowed(
                "lock_wallet", result
            )
        )

    def test_fake_allowlist_cannot_release(self):
        self.assertFalse(
            is_tool_allowed(
                "release_transaction",
                {
                    "allowed_tools": [
                        "release_transaction"
                    ]
                },
            )
        )


if __name__ == "__main__":
    unittest.main()
