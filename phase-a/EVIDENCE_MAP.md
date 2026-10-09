# Manuscript-to-artifact map

| Paper claim | Source file | Interpretation |
| --- | --- | --- |
| 27/27 governance decisions | `results/summary.json`; `results/case_summary.csv` | Original Control Plane decision cases only |
| 31/33 exact original labels; 32/33 with T14 semantic equivalence | `results/summary.json`; `REPORT.md` | T15 remains an exact and semantic mismatch |
| 47/47 deterministic case labels, 470 runs | `results/summary.json`; `results/runs.jsonl` | Replays, not independent observations |
| 90/100 simulated settlements reconciled; 10/10 injected mismatches became exceptions | `results/summary.json`; `results/runs.jsonl` | Synthetic receipts and fault injection |
| 26/26 original frozen inputs matched | `results/input_integrity.json`; `metadata/sprint3c-manifest.json` | Hash integrity of supplied fixture files |
| D02 five variants, 50 separate runs | `results-supplementary/summary.json`; `results-supplementary/runs.jsonl` | Post-hoc supplementary evidence; never add to D01 denominator |
| T15b adapter validation after authorization | `results-supplementary/summary.json`; `SUPPLEMENTARY_REPORT.md` | Downstream provider/rail mismatch in the tested fixture |
| A1/A2 authority/policy ablations | `results-supplementary/summary.json`; `results-supplementary/protocol.json` | Distinct tested control roles, not universal causal necessity |

Manuscript citations to D01 and D02 should identify these separate records. Use the current [Claim–Evidence Matrix v2.1 and Evaluation and Results v1.10](../REVIEWER_GUIDE.md) for claim boundaries. Counts are replay-aggregated, not independent attempts. Original summary keys using `preregistered` are historical field names; current prose uses **pre-specified**. D01 T09 is the duplicate-instruction case; D03 is mapped separately in [`../phase-b/EVIDENCE_MAP.md`](../phase-b/EVIDENCE_MAP.md).
