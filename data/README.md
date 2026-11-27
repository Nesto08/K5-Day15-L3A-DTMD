# E3 Data Pipeline v2 — Transaction Scam Hold & Support Orchestration

**Purpose:** reproducible synthetic data pipeline aligned to DTMD Track E3 rulebase specification supplied by the project team.

> All records shipped in this package are synthetic. They are not customer evidence, real scam reports, real transaction records, or proof of model performance.

## Scope
- Raw synthetic transaction, ledger, intelligence-source, conversation, scam-case and benchmark data.
- Normalization and PII-safe synthetic identifiers.
- Rule-result fixture generation using the supplied rule IDs and statuses.
- Risk-branch / autonomy / expected-action labels for evaluation.
- Validation of critical safety invariants.
- Group split by `scenario_family_id` to avoid scenario-family leakage.
- Benchmark metrics report scaffold.

## Important fidelity notes
1. T01–T04 and R01–R07 semantics and weights follow the DTMD specification provided in the project conversation.
2. R08/R10/R16/R20/R21/R22 are represented as extension flags. The full executable predicates for these rules must be imported from the actual repository; this package does **not** reimplement or claim equivalence to `transaction_predicates.py`, `context_rules.py`, or `catalog.py`.
3. The source specification contains conflicting risk thresholds: HIGH is described as >=75 and >=65; MEDIUM as >=35 and >=30. `config/rulebase_config.json` records this conflict explicitly. This package preserves raw score and uses the provisional label in generated fixtures only; confirm thresholds against code before production evaluation.
4. The supplied branch mapping is represented as benchmark expectations, not as a replacement for deterministic backend policy.
5. `lock_wallet`, `freeze_session`, `hold_transaction`, and `release_transaction` are represented as action names only. No real transaction or wallet operation is executed.
6. `R05` is verification-only and `R06` is a safety/ATO flag; neither contributes a numeric B1 weight.
7. The benchmark uses synthetic expected labels. It is a pipeline smoke-test, not an independent accuracy estimate.

## Requirements
- Python 3.10+
- Standard library only

## Run (from this directory)

```bash
python scripts/run_pipeline.py --seed 42 --benchmark-count 25
```

Or run stages individually:

```bash
python scripts/generate_synthetic.py --seed 42 --benchmark-count 25
python scripts/normalize_data.py
python scripts/build_rule_assessments.py
python scripts/build_decisions.py
python scripts/validate_data.py
python scripts/split_data.py --seed 42
python scripts/build_report.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Main outputs
- `data/raw/transactions_raw.jsonl`
- `data/raw/ledger_transactions_raw.jsonl`
- `data/raw/intelligence_sources_raw.jsonl`
- `data/raw/conversations_raw.jsonl`
- `data/raw/scam_cases_raw.jsonl`
- `data/raw/benchmark_cases_raw.jsonl`
- `data/interim/normalized_*.jsonl`
- `data/processed/rule_assessments.jsonl`
- `data/processed/risk_decisions.jsonl`
- `data/processed/action_expectations.jsonl`
- `data/processed/benchmark_cases.jsonl`
- `data/processed/splits/{train,validation,test}.jsonl`
- `reports/data_quality_report.md`
- `reports/benchmark_summary.json`

## Data lineage
`scenario_family_id` is the grouping key. Keep all paraphrases and variants from one family in a single split. Never randomly split individual messages from the same scenario family.

## Safety invariants
- A `SELF_DECLARED` claim never clears a `MATCHED` rule.
- Face authentication success does not clear scam/ATO indicators.
- `PRESSURE_TRANSFER` must never authorize `release_transaction`.
- `LEGITIMATE_URGENT` requires priority human handoff; AI does not release funds.
- `ACCOUNT_TAKEOVER` requires security escalation and the configured session-protection action.
- `UNCLEAR` asks at most one clarification question and does not prematurely assert a scam/ATO conclusion.
- A tool proposal is not proof of execution. Store proposal, policy authorization, execution result, and state transition separately.

## Integration contract for TV1
The adapter in `scripts/rulebase_adapter.py` is intentionally an integration seam. Replace its fixture implementation with imports from:
- `src/agents/rulebase/transaction_predicates.py`
- `src/agents/rulebase/catalog.py`
- `src/agents/rulebase/context_rules.py`
- `src/transactions/service.py`

Do not copy or fork the rule logic into this data package.
