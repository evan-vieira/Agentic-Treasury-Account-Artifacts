# ATA Supplementary Governance Tests v1.0

Status: EXECUTED

These are post-hoc supplementary robustness tests. They are reported separately from the original Sprint 3D case set and must not be added retroactively to the original 470-run denominator.

## Original harness integrity

- Sprint 3C manifest files matching: 26/26
- Frozen case set hash match: True
- Frozen expectation hash match: True
- Original harness files modified by supplementary run: No

## Supplementary results

| Case | Variant | Observed governance | Instruction | Execution | Interpretation |
|---|---|---|---|---|---|
| T15b | Full governance + adapter binding | ALLOW | Issued | EXECUTION_VALIDATION_FAIL (PROVIDER_RAIL_MISMATCH) | Adapter/provider validation reached after governance |
| A1 | Full governance | DENY | No | Not attempted | Authority Envelope blocked counterparty outside delegation |
| A1 | Policy-only ablation | ALLOW | Issued | Not attempted | Removing Authority Envelope enforcement removed that control |
| A2 | Full governance | DENY | No | Not attempted | Treasury Policy blocked projected liquidity breach |
| A2 | Authority-only ablation | ALLOW | Issued | SUCCESS / RECONCILED | Removing Treasury Policy enforcement allowed the action |

Each variant was replayed 10 times. All five variants matched their specified supplementary expectations and were deterministic across replays. Total supplementary runs: 50.

## Interpretation boundary

These tests strengthen evidence that Authority Envelope and Treasury Policy perform distinct control functions in the implemented artifact, and that execution-stage validation can reject a provider/rail mismatch even after governance has issued an AuthorizedInstruction. They do not establish production security, universal necessity of this architecture, legal sufficiency, or external reproducibility.

## Relationship to original T15

Original T15 remains unchanged: expected EXECUTION_VALIDATION_FAIL, observed DENY before adapter execution. T15b is a separately versioned supplementary test designed to isolate the downstream validation path that T15 did not reach.
