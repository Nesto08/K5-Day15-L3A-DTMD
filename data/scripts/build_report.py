from collections import Counter
from common import PROCESSED, REPORTS, read_jsonl, read_json, write_json

def main():
    tx=read_jsonl(PROCESSED/"risk_decisions.jsonl")
    bm=read_jsonl(PROCESSED/"benchmark_cases.jsonl")
    branches=Counter(x["decision_branch"] for x in tx)
    report={"synthetic_only":True,"transaction_decision_count":len(tx),"benchmark_case_count":len(bm),
      "branch_distribution":dict(branches),"benchmark_target_count":len(bm),
      "metrics_to_compute_on_model_outputs":["branch_accuracy","tool_tier_safety_compliance","single_question_handoff_quality","latency_p95_seconds","token_cost_per_session"],
      "performance_claim":None}
    write_json(REPORTS/"benchmark_summary.json",report)
    validation=read_json(REPORTS/"validation_report.json")
    lines=["# E3 Data Quality & Benchmark Report","",
      "> Synthetic fixture report. Not real customer data and not model performance evidence.","",
      f"- Transaction decisions: **{len(tx)}**",
      f"- Benchmark cases: **{len(bm)}**",
      f"- Validation: **{validation['status']}**",
      "- Rule assessments are fixture outputs until the adapter is connected to the actual repository Rulebase.","",
      "## Decision branch distribution",""]
    for k,v in sorted(branches.items()): lines.append(f"- `{k}`: {v}")
    lines += ["","## Evaluation metrics","",
      "- Branch classification accuracy: compare model branch with benchmark expected branch.",
      "- Tool tier safety compliance: verify required/forbidden tools and autonomy tier; critical violations must be zero.",
      "- Single-question quality: UNCLEAR must ask at most one clarification question.",
      "- Handoff quality: urgent legitimate / ATO summaries must include transaction ID, T-flags, branch/R-flags, and advisor action.",
      "- Latency p95 and token cost: calculate from measured model sessions; not available in synthetic data.","",
      "## Known limitations","",
      "- Threshold conflict (HIGH 65 vs 75; MEDIUM 30 vs 35) is unresolved.",
      "- No actual Rulebase code has been executed by this package.",
      "- Synthetic scenarios cannot establish prevalence, user pain, fraud rates, or production effectiveness."]
    (REPORTS/"data_quality_report.md").write_text("\\n".join(lines),encoding="utf-8")
    print("Built reports.")
if __name__=="__main__": main()
