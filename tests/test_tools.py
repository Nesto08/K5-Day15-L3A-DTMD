
import unittest
from pathlib import Path
from unittest.mock import patch

from codebase import tools


FIXTURE_DIR = (
    Path(__file__).resolve().parent / "fixtures"
)


class TestTools(unittest.TestCase):

    def setUp(self):
        self.patcher = patch.object(
            tools, "DATA_DIR", FIXTURE_DIR
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_get_held_transaction(self):
        result = tools.get_held_transaction("TX001")

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["transaction"]["status"],
            "TEMP_HELD",
        )

    def test_transaction_not_found(self):
        result = tools.get_held_transaction("INVALID")

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["error"],
            "TRANSACTION_NOT_FOUND",
        )

    def test_transaction_flags_preserved(self):
        result = tools.get_held_transaction("TX002")

        flags = result["transaction"]["transaction_flags"]

        self.assertTrue(flags["T04"])

    def test_request_verification(self):
        result = tools.request_verification(
            "USER001",
            "Ban chuyen tien cho muc dich gi?",
        )

        self.assertTrue(result["ok"])

    def test_reject_multiple_questions(self):
        result = tools.request_verification(
            "USER001",
            "Chuyen cho ai? Muc dich gi?",
        )

        self.assertFalse(result["ok"])

    def test_reject_empty_question(self):
        result = tools.request_verification(
            "USER001", ""
        )

        self.assertFalse(result["ok"])

    def test_hold_transaction(self):
        result = tools.hold_transaction("TX001")

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "TEMP_HELD")
        self.assertFalse(result["funds_released"])
        self.assertFalse(result["state_changed"])

    def test_hold_invalid_transaction(self):
        result = tools.hold_transaction("INVALID")

        self.assertFalse(result["ok"])

    def test_handoff_to_agent(self):
        summary = {
            "transaction_id": "TX001",
            "hold_reason": "T02/T03",
            "classification": "legitimate_urgent",
            "context_flags": {},
            "recommended_action": "Human review",
        }

        result = tools.handoff_to_agent(
            "CHAT001",
            summary,
            "HIGH",
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(result["status"], "DRAFT")
        self.assertFalse(
            result["sent_to_real_advisor"]
        )

    def test_invalid_handoff_priority(self):
        result = tools.handoff_to_agent(
            "CHAT001", {}, "INVALID"
        )

        self.assertFalse(result["ok"])

    def test_incomplete_handoff(self):
        result = tools.handoff_to_agent(
            "CHAT001", {}, "HIGH"
        )

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["error"],
            "INCOMPLETE_HANDOFF",
        )

    def test_lock_wallet_is_draft_only(self):
        result = tools.lock_wallet("USER001")

        self.assertTrue(result["ok"])
        self.assertFalse(result["wallet_locked"])
        self.assertEqual(
            result["status"],
            "PENDING_HUMAN_APPROVAL",
        )

    def test_retrieval(self):
        result = tools.search_scam_cases(["R03"])

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["case_id"],
            "MOCK-R03",
        )

    def test_retrieval_no_match(self):
        result = tools.search_scam_cases(["R99"])

        self.assertEqual(result, [])

    def test_retrieval_empty_query(self):
        result = tools.search_scam_cases([])

        self.assertEqual(result, [])

    def test_synthetic_source_label(self):
        result = tools.search_scam_cases(["R06"])

        self.assertTrue(result[0]["is_synthetic"])
        self.assertIsNone(result[0]["source"])

    def test_tool_allowlist(self):
        expected = {
            "get_held_transaction",
            "request_verification",
            "hold_transaction",
            "handoff_to_agent",
            "lock_wallet",
        }

        self.assertEqual(
            set(tools.TOOLS.keys()),
            expected,
        )

    def test_no_release_transaction(self):
        self.assertNotIn(
            "release_transaction",
            tools.TOOLS,
        )


if __name__ == "__main__":
    unittest.main()
