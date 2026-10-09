# ATA — Simulation Harness & Experimental Run v1.0

Executed research artifact, 23 September 2026. See REPORT.md for findings and ASSUMPTIONS.md for implementation choices. The original README.md is retained unchanged as part of the Sprint 3C input package.

## Reproduce

Use Python 3.12 and PyYAML 6.0.3. From the extracted directory:

```bash
python -m pip install -r requirements.txt
python src/run.py
python -m unittest discover -s tests -v
```

`resolved/cases.json` and `resolved/expectations.json` are the frozen explicit case definitions and separate oracles. `src/prepare_cases.py` documents how they were derived; it is not necessary to regenerate them for replay. The evaluator in `src/engine.py` never imports or reads expected-results files. Only the experiment runner compares the observed outcome with the separate oracle.

No API key, LLM, blockchain endpoint or banking connection is required. All execution is simulated. This is a local repository-ready package; it has not been published to GitHub.

## Contents

- src/engine.py — profile-specific policy evaluator, authority checks, approvals, instruction gate, simulated adapters, reconciliation and hash-linked audit events.
- src/prepare_cases.py — reproducible resolution of narrative fixtures into explicit cases.
- src/run.py — experiment runner and metric aggregation.
- tests/test_controls.py — 13 additional verification tests with independent accounting and control assertions.
- resolved/ — frozen input cases, expected outcomes and hashes.
- results/summary.json — aggregate metrics, denominators and discrepancies.
- results/case_summary.csv — one row per distinct case.
- results/runs.jsonl — all 470 runs, including full policy-input snapshots, reason codes, instructions, receipts and audit records.
- results/verification.txt — test-suite output.
- results/input_integrity.json — integrity comparison for all 26 original inputs.
- metadata/sprint3c-manifest.json — original manifest.
- metadata/delivery-manifest.json — hashes of the delivered source, fixtures and results (excluding itself).

## Interpretation

The 33 preregistered case labels are not 33 independent discoveries: several negative tests repeat scenario variants. The ten repetitions per case do not expand scenario coverage. Eight additional safeguards and six approved lifecycle cases are separate cohorts.

The engine supports the supplied policy profiles rather than every possible schema or treasury action. Phase B (agent-generated proposals) is optional and was not executed. No formal claim of complete schema validation, production security, legal compliance, economic superiority or optimal routing follows from these experiments.

No license for public redistribution of the user's research is inferred. Repository publication and licensing remain outside this deliverable.
