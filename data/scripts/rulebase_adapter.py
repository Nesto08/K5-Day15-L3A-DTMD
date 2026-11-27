"""Integration seam.

Replace fixture_rules() with calls to the actual DTMD repository Rulebase.
This fixture adapter only creates synthetic expected rule-result rows for pipeline
smoke tests; it is NOT an implementation of the authoritative predicates.
"""
from common import INTERIM, PROCESSED, read_jsonl, write_jsonl, read_json

STATUS={"MATCHED","NOT_MATCHED","UNKNOWN"}
def fixture_rules(tx, chat):
    # Fixture status comes from scenario labels and raw trigger metadata only.
    # It must not be used to claim that the Python predicates have been executed.
    family=tx["scenario_family_id"]
    branch=("PRESSURE_TRANSFER" if family.startswith("APP-SCAM") else
            "LEGITIMATE_URGENT" if family.startswith("URGENT") else
            "ACCOUNT_TAKEOVER" if family.startswith("ATO") else "UNCLEAR")
    trows=[]
    tflags=set(tx.get("trigger_flags",[]))
    for rid in ["T01","T02","T03","T04"]:
        status="MATCHED" if rid in tflags else ("UNKNOWN" if rid=="T02" and not tx.get("ledger_history_ref") else "NOT_MATCHED")
        weight={"T01":-15,"T02":25,"T03":15,"T04":65}[rid] if status=="MATCHED" else 0
        trows.append({"rule_id":rid,"status":status,"weight":weight,"evidence_refs":[tx["tx_id"]] if status=="MATCHED" else []})
    crows=[]
    matched=set()
    for msg in chat["messages"]:
        text=msg["message_text"].lower()
        if "ngay" in text or "ngay lập tức" in text or "phong tỏa" in text: matched.add("R01")
        if "bí mật" in text or "không báo ngân hàng" in text: matched.add("R02")
        if "cán bộ điều tra" in text or "công an" in text: matched.add("R03")
        if "phí mở khóa" in text or "làm nhiệm vụ" in text: matched.add("R04")
        if "otp" in text or "mật khẩu" in text or "mã khôi phục" in text: matched.add("R06")
        if "lợi nhuận" in text or "hoa hồng" in text: matched.add("R07")
        if "tài khoản thứ ba" in text: matched.add("R10")
        if "chuyển lại" in text or "chuyển lại nhiều lần" in text: matched.add("R22")
        if ".apk" in text or "điều khiển màn hình" in text or "chia sẻ màn hình" in text: matched.add("R16")
        if "đường link lạ" in text or "link giả" in text: matched.add("R20")
    weights={"R01":20,"R02":15,"R03":25,"R04":20,"R07":20}
    for rid in ["R01","R02","R03","R04","R05","R06","R07","R08","R10","R16","R20","R21","R22"]:
        status="MATCHED" if rid in matched else "UNKNOWN" if rid=="R05" else "NOT_MATCHED"
        crows.append({"rule_id":rid,"status":status,"weight":weights.get(rid,0) if status=="MATCHED" else 0,
                      "evidence_refs":[m["message_id"] for m in chat["messages"]] if status=="MATCHED" else [],
                      "implementation_status":"FIXTURE_NOT_AUTHORITATIVE"})
    return branch,trows,crows

def main():
    txs=read_jsonl(INTERIM/"normalized_transactions.jsonl")
    chats={x["tx_id"]:x for x in read_jsonl(INTERIM/"normalized_conversations.jsonl")}
    cfg=read_json(PROCESSED.parent.parent/"config"/"rulebase_config.json")
    out=[]
    for i,tx in enumerate(txs,1):
        branch,tr,cr=fixture_rules(tx,chats[tx["tx_id"]])
        score=sum(x["weight"] for x in tr+cr)
        score=max(0,min(100,score))
        out.append({"assessment_id":f"ASM-{i:04d}","tx_id":tx["tx_id"],"scenario_family_id":tx["scenario_family_id"],
          "rulebase_versions":{"transaction":cfg["transaction_rule_version"],"context":cfg["context_rule_version"]},
          "transaction_rules":tr,"context_rules":cr,"total_rule_score":score,
          "risk_level":"UNRESOLVED","fixture_branch_hint":branch,
          "assessment_origin":"SYNTHETIC_FIXTURE_NOT_ACTUAL_RULEBASE_EXECUTION"})
    write_jsonl(PROCESSED/"rule_assessments.jsonl",out)
    print("Wrote fixture rule assessments. Replace adapter before production evaluation.")
if __name__=="__main__": main()
