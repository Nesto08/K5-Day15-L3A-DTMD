from common import RAW, INTERIM, read_jsonl, write_jsonl

def main():
    txs=read_jsonl(RAW/"transactions_raw.jsonl")
    chats=read_jsonl(RAW/"conversations_raw.jsonl")
    # Synthetic identifiers are already pseudonymous. This stage normalizes whitespace and stable IDs.
    for tx in txs:
        tx["amount_vnd"]=int(tx["amount_vnd"])
        tx["trigger_flags"]=sorted(set(tx.get("trigger_flags",[])))
    for chat in chats:
        chat["messages"]=sorted(chat["messages"],key=lambda x:x["sequence"])
        for m in chat["messages"]:
            m["message_text"]=" ".join(m["message_text"].split())
    write_jsonl(INTERIM/"normalized_transactions.jsonl",txs)
    write_jsonl(INTERIM/"normalized_conversations.jsonl",chats)
    for name in ["ledger_transactions_raw","intelligence_sources_raw","scam_cases_raw","benchmark_cases_raw"]:
        write_jsonl(INTERIM/f"normalized_{name.replace('_raw','')}.jsonl",read_jsonl(RAW/f"{name}.jsonl"))
    print("Normalized raw datasets.")
if __name__=="__main__": main()
