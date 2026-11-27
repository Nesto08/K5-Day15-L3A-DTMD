from common import INTERIM, PROCESSED, read_jsonl

def main():
    errors=[]; critical=[]
    txs=read_jsonl(INTERIM/"normalized_transactions.jsonl")
    chats=read_jsonl(INTERIM/"normalized_conversations.jsonl")
    assessments=read_jsonl(PROCESSED/"rule_assessments.jsonl")
    decisions=read_jsonl(PROCESSED/"risk_decisions.jsonl")
    actions=read_jsonl(PROCESSED/"action_expectations.jsonl")
    txids={x["tx_id"] for x in txs}; chat_txids={x["tx_id"] for x in chats}
    if txids != chat_txids: errors.append("Transaction/conversation tx_id sets differ")
    for tx in txs:
        if tx["transaction_status"]!="TEMP_HELD": errors.append(f"{tx['tx_id']}: not TEMP_HELD")
        if "T01" in tx.get("trigger_flags",[]) and "T03" in tx.get("trigger_flags",[]): errors.append(f"{tx['tx_id']}: T01 and T03 both set")
    for a in assessments:
        for row in a["transaction_rules"]+a["context_rules"]:
            if row["status"] not in {"MATCHED","NOT_MATCHED","UNKNOWN"}: errors.append(f"{a['assessment_id']}: invalid status")
            if row["rule_id"] in {"R05","R06"} and row["weight"]!=0: errors.append(f"{a['assessment_id']}: {row['rule_id']} must not score")
    for d in decisions:
        if d["face_auth_status"]=="SUCCESS" and d["decision_branch"]=="PRESSURE_TRANSFER" and not any(x.startswith("R") for x in d["matched_rules"]):
            critical.append(f"{d['decision_id']}: FaceID success fixture lacks a matched contextual flag")
    for a in actions:
        if "release_transaction" not in a["forbidden_tools"]: critical.append(f"{a['action_expectation_id']}: release_transaction not forbidden")
        if a["expected_action"]=="ESCALATE_PRIORITY_ADVISOR" and not a["human_approval_required"]: errors.append("Urgent legitimate requires human approval")
        if a["expected_action"]=="FREEZE_SESSION_AND_ESCALATE_SECURITY" and "freeze_session" not in a["required_tools"]: errors.append("ATO missing freeze_session")
    report={"transaction_count":len(txs),"conversation_count":len(chats),"assessment_count":len(assessments),
      "decision_count":len(decisions),"action_expectation_count":len(actions),"errors":errors,"critical_errors":critical,
      "status":"PASS" if not errors and not critical else "FAIL",
      "note":"Synthetic fixture validation only; does not validate the actual repository Rulebase."}
    import json
    from common import REPORTS, write_json
    write_json(REPORTS/"validation_report.json",report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors or critical: raise SystemExit(1)
if __name__=="__main__": main()
