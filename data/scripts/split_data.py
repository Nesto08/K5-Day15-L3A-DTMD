import argparse, random
from collections import defaultdict
from common import PROCESSED, read_jsonl, write_jsonl

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int,default=42); args=ap.parse_args()
    rows=read_jsonl(PROCESSED/"benchmark_cases.jsonl")
    groups=defaultdict(list)
    for row in rows: groups[row["scenario_family_id"]].append(row)
    keys=list(groups); random.Random(args.seed).shuffle(keys)
    # group-level split, approximate 70/15/15; small family count means exact percentages are not guaranteed.
    n=len(keys); n_train=max(1,round(n*.70)); n_val=max(1,round(n*.15))
    train=set(keys[:n_train]); val=set(keys[n_train:n_train+n_val]); test=set(keys[n_train+n_val:])
    if not test and n>2: test={keys[-1]}; train.discard(keys[-1])
    for name,chosen in [("train",train),("validation",val),("test",test)]:
        write_jsonl(PROCESSED/"splits"/f"{name}.jsonl",[r for r in rows if r["scenario_family_id"] in chosen])
    sets=[train,val,test]
    assert not (sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
    print(f"Split {len(rows)} benchmark rows across {n} scenario families.")
if __name__=="__main__": main()
