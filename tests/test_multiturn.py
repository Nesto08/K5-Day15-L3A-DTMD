"""Integration tests for multiturn sessions."""

import json
import unittest

from unittest.mock import patch

from codebase import agent


def mock_unclear():
    return {
        "text": json.dumps({
            "classification": "unclear",
            "facts": {},
        }),
        "model": "fake",
        "tokens_in": 0,
        "tokens_out": 0,
    }


class TestMultiturn(unittest.TestCase):

    def setUp(self):
        self.session = agent.create_session()

    @patch.object(agent, "call_model")
    def test_pressure_confirmed(self, model):

        model.return_value = mock_unclear()

        first = agent.run_agent(
            "Tại sao giao dịch bị chặn?",
            self.session,
        )

        self.assertEqual(
            first["action"],
            "EXPLAIN_AND_ASK_ONE_QUESTION",
        )

        second = agent.run_agent(
            "Có.",
            self.session,
        )

        self.assertEqual(
            second["classification"],
            "suspected_scam",
        )

        self.assertEqual(
            second["action"],
            "KEEP_HOLD_AND_WARN",
        )

        self.assertEqual(
            self.session["question_count"],
            1,
        )

    @patch.object(agent, "call_model")
    def test_negative_reply(self, model):

        model.return_value = mock_unclear()

        agent.run_agent(
            "Tại sao bị chặn?",
            self.session,
        )

        result = agent.run_agent(
            "Không.",
            self.session,
        )

        self.assertEqual(
            result["action"],
            "KEEP_HOLD_AND_ESCALATE",
        )

        self.assertEqual(
            self.session["question_count"],
            1,
        )

    @patch.object(agent, "call_model")
    def test_yes_without_previous_question(self, model):

        model.return_value = mock_unclear()

        result = agent.run_agent(
            "Có.",
            self.session,
        )

        self.assertEqual(
            result["classification"],
            "unclear",
        )

    def test_reset_session(self):

        self.session["question_count"] = 1

        self.session["pending_question"] = (
            "COERCIVE_PRESSURE"
        )

        new_session = agent.create_session()

        self.assertEqual(
            new_session["question_count"],
            0,
        )

        self.assertIsNone(
            new_session["pending_question"]
        )

    @patch.object(agent, "call_model")
    def test_independent_benchmark_cases(self, model):

        model.return_value = mock_unclear()

        first = agent.answer("Tại sao bị chặn?")
        second = agent.answer("Tại sao bị chặn?")

        self.assertEqual(
            first["action"],
            "EXPLAIN_AND_ASK_ONE_QUESTION",
        )

        self.assertEqual(
            second["action"],
            "EXPLAIN_AND_ASK_ONE_QUESTION",
        )


if __name__ == "__main__":
    unittest.main()
