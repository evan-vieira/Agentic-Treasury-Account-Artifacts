# Agentic Treasury Account — Phase A research artifact

This directory contains the **synthetic, simulated Phase A** artifact for the Crypto Valley paper. The original D01 files and the post-hoc D02 additions are preserved byte for byte from their source packages. D03 is a separate experiment archived in [`../phase-b/`](../phase-b/). The [reviewer guide](../REVIEWER_GUIDE.md) records the manuscript/evidence-control versions used for this export.

## Evidence map

| Record | Scope | Inputs and code | Raw output | Report |
| --- | --- | --- | --- | --- |
| **D01, principal** | 47 case labels × 10 deterministic replays = 470 runs | `dataset/`, `scenarios/`, `policies/`, `authority/`, `resolved/`, `src/` | `results/runs.jsonl`, `results/case_summary.csv`, `results/summary.json` | `REPORT.md` |
| **D02, post-hoc** | T15b plus A1/A2 paired variants; 5 variants × 10 = 50 runs | Same frozen D01 inputs and engine; `supplementary/run_supplementary.py`, `results-supplementary/protocol.json` | `results-supplementary/runs.jsonl`, `results-supplementary/summary.json` | `SUPPLEMENTARY_REPORT.md` |

The D02 counts are separate from D01. Replays are repeated evaluations of synthetic cases, not independent financial observations. D01 T14 and T15 remain in the original record, including their exact-label mismatches. D02 T15b does not replace T15.

## Reproduce

Use Python 3.12 and PyYAML 6.0.3 (the recorded D01 environment). D02 was originally executed under Python 3.13.5. For an isolated verification, copy the repository to a temporary folder because the runners write into `results/` and `results-supplementary/`.

```bash
python -m pip install -r requirements.txt
python scripts/verify_frozen.py
python -m unittest discover -s tests -v
python src/run.py
python supplementary/run_supplementary.py
```

Run `python scripts/verify_frozen.py` **before** replay, and compare the new summaries with the archived summaries. The script checks source manifest hashes and the archived record counts; it intentionally fails after a replay overwrites an archived file with different timestamps. `RUN_SPRINT3D.md` describes the D01 harness; `supplementary/README.md` describes the D02 runner.

## Provenance

Original D01/D02 files retain their archived bytes and manifest hashes. The source-delivery ZIPs and private Git history are not distributed here; all extracted files required by the verification scripts are included. Consult the root `SOURCE_PROVENANCE.json` for the export mapping.

## Limits

Financial entities, balances, obligations, rails, receipts, and settlements are synthetic or simulated. Phase A used fixed Proposed Actions and no LLM inference. It does not establish production security, real settlement finality, economic superiority, regulatory sufficiency, or agent performance. This review artifact is an independent export; independent external reproduction remains unestablished. Historical Phase A fields such as `phase_B: NOT_RUN_OPTIONAL` describe the original D01 run, not the current repository inventory.

See the root [reproduction guide](../REPRODUCIBILITY.md) and this directory’s [evidence map](EVIDENCE_MAP.md).
