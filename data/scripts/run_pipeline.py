import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(script,args=None):
    cmd=[sys.executable,str(ROOT/"scripts"/script)]+(args or [])
    subprocess.run(cmd,cwd=ROOT,check=True)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int,default=42); ap.add_argument("--benchmark-count",type=int,default=25); a=ap.parse_args()
    run("generate_synthetic.py",["--seed",str(a.seed),"--benchmark-count",str(a.benchmark_count)])
    for s in ["normalize_data.py","build_rule_assessments.py","build_decisions.py","validate_data.py"]:
        run(s)
    run("split_data.py",["--seed",str(a.seed)])
    run("build_report.py")
if __name__=="__main__": main()
