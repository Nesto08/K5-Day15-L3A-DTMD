
"""Integration tests for Track E3 Data Adapter."""

import unittest

from codebase.data_adapter import (
    load_transactions,
    load_scam_cases,
    normalize_transaction,
)
from codebase import tools


class TestDataAdapter(unittest.TestCase):

    def test_load_transactions(self):
        records = load_transactions()

        self.assertEqual(len(records), 25)

    def test_transaction_schema(self):
        records = load_transactions()
        record = records[0]

        required_fields = {
            "tx_id",
            "user_id",
            "amount",
            "status",
            "transaction_flags",
        }

        self.assertTrue(
            required_fields.issubset(record.keys())
        )

    def test_real_pipeline_lookup(self):
        result = tools.get_held_transaction("TX-0001")

        self.assertTrue(result["ok"])

        transaction = result["transaction"]

        self.assertEqual(
            transaction["user_id"],
            "USER-0001",
        )

        self.assertEqual(
            transaction["amount"],
            12000000,
        )

        self.assertEqual(
            transaction["status"],
            "TEMP_HELD",
        )

    def test_trigger_flags(self):
        result = tools.get_held_transaction("TX-0001")

        self.assertTrue(result["ok"])

        flags = result["transaction"]["transaction_flags"]

        self.assertEqual(flags["T02"], "MATCHED")
        self.assertEqual(flags["T03"], "MATCHED")

    def test_unknown_flags(self):
        record = normalize_transaction({
            "tx_id": "TEST-TX",
            "user_id": "TEST-USER",
            "trigger_flags": [],
        })

        self.assertEqual(
            record["transaction_flags"]["T04"],
            "UNKNOWN",
        )

    def test_face_auth(self):
        result = tools.get_held_transaction("TX-0001")

        self.assertTrue(result["ok"])

        self.assertTrue(
            result["transaction"]["face_id_verified"]
        )

    def test_no_scenario_label_leakage(self):
        records = load_transactions()

        for record in records:
            self.assertNotIn(
                "scenario_family_id",
                record,
            )

            self.assertNotIn(
                "fixture_branch_hint",
                record,
            )

    def test_load_scam_cases(self):
        records = load_scam_cases()

        self.assertEqual(len(records), 7)

    def test_synthetic_label(self):
        records = load_scam_cases()

        for record in records:
            self.assertTrue(record["is_synthetic"])
            self.assertIsNone(record["source"])

    def test_retrieval_from_pipeline(self):
        records = tools.search_scam_cases(["R03"])

        self.assertGreater(len(records), 0)

        for record in records:
            self.assertIn("R03", record["rule_ids"])

    def test_hold_pipeline_transaction(self):
        result = tools.hold_transaction("TX-0001")

        self.assertTrue(result["ok"])
        self.assertFalse(result["funds_released"])
        self.assertFalse(result["state_changed"])

    def test_invalid_transaction(self):
        result = tools.get_held_transaction("INVALID")

        self.assertFalse(result["ok"])

        self.assertEqual(
            result["error"],
            "TRANSACTION_NOT_FOUND",
        )


if __name__ == "__main__":
    unittest.main()
