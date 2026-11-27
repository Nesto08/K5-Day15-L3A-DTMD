import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from common import INTERIM, PROCESSED, read_jsonl

class E3InvariantTests(unittest.TestCase):
    def test_no_release_in_any_branch(self):
        for row in read_jsonl(PROCESSED/"action_expectations.jsonl"):
            self.assertIn("release_transaction",row["forbidden_tools"])
    def test_r05_r06_non_scoring(self):
        for row in read_jsonl(PROCESSED/"rule_assessments.jsonl"):
            for r in row["context_rules"]:
                if r["rule_id"] in ("R05","R06"):
                    self.assertEqual(r["weight"],0)
    def test_group_split_no_leakage(self):
        splits=[]
        for name in ("train","validation","test"):
            rows=read_jsonl(PROCESSED/"splits"/f"{name}.jsonl")
            splits.append({x["scenario_family_id"] for x in rows})
        self.assertFalse(splits[0]&splits[1])
        self.assertFalse(splits[0]&splits[2])
        self.assertFalse(splits[1]&splits[2])
if __name__=="__main__": unittest.main()
