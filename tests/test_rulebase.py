
import unittest

from codebase.rulebase import (
    analyze,
    evaluate_context,
    normalize_transaction_flags,
)


class TestRulebase(unittest.TestCase):

    def test_transaction_flags(self):
        result = normalize_transaction_flags({
            "T02": True,
            "T03": True,
            "T04": False,
        })

        self.assertEqual(result["T01"], "UNKNOWN")
        self.assertEqual(result["T02"], "MATCHED")
        self.assertEqual(result["T03"], "MATCHED")
        self.assertEqual(result["T04"], "NOT_MATCHED")

    def test_r01_coercive_pressure(self):
        result = evaluate_context({
            "COERCIVE_PRESSURE": True,
            "DOCUMENTED_LEGITIMATE_DEADLINE": False,
        })

        self.assertEqual(result["R01"], "MATCHED")

    def test_r01_legitimate_deadline(self):
        result = evaluate_context({
            "COERCIVE_PRESSURE": True,
            "DOCUMENTED_LEGITIMATE_DEADLINE": True,
        })

        self.assertEqual(result["R01"], "NOT_MATCHED")

    def test_r01_missing_evidence(self):
        result = evaluate_context({
            "COERCIVE_PRESSURE": True,
        })

        self.assertEqual(result["R01"], "UNKNOWN")

    def test_r02_block_verification(self):
        result = evaluate_context({
            "VERIFICATION_BLOCKED": True,
            "ORDINARY_PRIVACY_REQUEST": False,
        })

        self.assertEqual(result["R02"], "MATCHED")

    def test_r03_impersonation(self):
        result = evaluate_context({
            "SPECIFIC_IMPERSONATION_INDICATOR": True,
            "TRANSFER_REQUEST": True,
            "SELF_IDENTIFICATION_ONLY": False,
        })

        self.assertEqual(result["R03"], "MATCHED")

    def test_r04_unlock_payment(self):
        result = evaluate_context({
            "PAY_TO_PROVE_OR_UNLOCK": True,
            "VERIFIABLE_LEGITIMATE_FEE": False,
        })

        self.assertEqual(result["R04"], "MATCHED")

    def test_r05_self_declared_verification(self):
        result = evaluate_context({
            "SUSPICIOUS_REQUEST": True,
            "INDEPENDENT_VERIFICATION_COMPLETED": True,
            "VERIFICATION_SOURCE": "SELF_DECLARED",
        })

        self.assertEqual(result["R05"], "UNKNOWN")

    def test_r06_secret_request(self):
        result = evaluate_context({
            "OTHER_PARTY_REQUESTS_SECRET": True,
        })

        self.assertEqual(result["R06"], "MATCHED")

    def test_r07_unrealistic_return(self):
        result = evaluate_context({
            "UNREALISTIC_RISK_FREE_RETURN": True,
            "TRANSFER_REQUEST": True,
            "TRANSPARENT_RISK_DISCLOSURE": False,
        })

        self.assertEqual(result["R07"], "MATCHED")

    def test_r16_remote_access(self):
        result = evaluate_context({
            "OTHER_PARTY_REQUESTS_REMOTE_ACCESS": True,
        })

        self.assertEqual(result["R16"], "MATCHED")

    def test_r20_phishing(self):
        result = evaluate_context({
            "PHISHING_OR_SPOOFED_PORTAL_INDICATOR": True,
        })

        self.assertEqual(result["R20"], "MATCHED")

    def test_monotonic_protection(self):
        result = evaluate_context(
            {
                "OTHER_PARTY_REQUESTS_SECRET": False,
            },
            previous_flags={"R06": "MATCHED"},
        )

        self.assertEqual(result["R06"], "MATCHED")

    def test_blacklist_hit(self):
        result = analyze(
            transaction_flags={"T04": True},
            facts={},
        )

        self.assertTrue(result["blacklist_hit"])

    def test_user_denies_transaction(self):
        result = analyze(
            transaction_flags={"T02": True},
            facts={"USER_DENIES_TRANSACTION": True},
        )

        self.assertTrue(result["has_ato_signal"])

    def test_ato_detection(self):
        result = analyze(
            transaction_flags={"T02": True},
            facts={"OTHER_PARTY_REQUESTS_SECRET": True},
        )

        self.assertTrue(result["has_ato_signal"])
        self.assertIn("R06", result["safety_flags"])

    def test_missing_information(self):
        result = analyze({}, {})

        self.assertFalse(result["has_scam_signal"])
        self.assertFalse(result["has_ato_signal"])
        self.assertEqual(len(result["unknown_rules"]), 9)


if __name__ == "__main__":
    unittest.main()
