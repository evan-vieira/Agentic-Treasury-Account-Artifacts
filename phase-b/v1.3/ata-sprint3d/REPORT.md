# Sprint 3D — Experimental Report v1.0

Status: executed, with documented expectation discrepancies. Date: 23 September 2026.

## Purpose and scope

The experiment evaluates a deterministic implementation of the ATA control plane against the approved synthetic treasury fixtures. It covers intragroup liquidity movement, bank FX and stablecoin conversion, tokenized fund subscription and cross-border settlement. It tests financial authority and operational controls, not AI planning quality, economic optimization or real financial infrastructure.

## Cohorts and results

| Measure | Observed result |
|---|---:|
| Original input files matching supplied hashes | 26/26 |
| Scenario cases | 18 |
| Preregistered negative cases | 15 |
| Additional approved lifecycle cases | 6 |
| Additional safeguard cases | 8 |
| Distinct case labels | 47 |
| Replays per case | 10 |
| Total replay runs | 470 |
| Exact outcome matches, original 33 labels | 31/33 (93.94%) |
| Matches accepting T14 fail-closed equivalence | 32/33 (96.97%) |
| Exact matches for the 27 original governance-decision cases | 27/27 |
| Cases with identical behavior hashes across ten replays | 47/47 |
| Runs with structurally complete audit events | 470/470 |
| Unauthorized simulated adapter submissions observed | 0 |
| Duplicate attempts rejected | 10/10 |
| Settlements reconciled, all cohorts including injected faults | 90/100 |
| Injected settlement discrepancies detected as EXCEPTION | 10/10 |
| Additional verification tests passed | 13/13 |

The remaining 90 settlements had no injected mismatch and all reconciled. The aggregate reconciliation rate is deliberately 90%, not 100%, because the denominator includes ten T13 fault-injection runs. Audit completeness here means presence of required fields, not external attestation of evidence quality.

The replay observations are finite, deterministic fixture results. They are not estimates of failure probability. Cases overlap and repetitions do not count as independent financial observations.

## Findings by scenario

- S01: the BRL 80,000 instruction was authorized and simulated; reserve cash became BRL 2,370,000 and operating cash BRL 3,360,000. A BRL 350,000 proposal required approval. Source-reserve breach was denied; stale balance data requested additional information.
- S02: both USD and USDC routes required approval before execution. After valid approval, the bank route debited BRL 2,434,860 and the stablecoin route BRL 2,433,989.25 under fixed synthetic quote/fee assumptions. These arithmetic differences are not evidence of comparative real-world cost. Unsupported assets and authority-limit violations were denied.
- S03: the USD 75,000 subscription was allowed; cash became USD 1,175,000 and the receipt recorded 75,000 synthetic fund units. Projected minimum cash after investment was USD 750,000. A USD 150,000 proposal required approval; USD 250,000 breached the forecast liquidity floor and was denied.
- S04: both USD bank wire and USDC payment required independent approval. After approval, bank cash became USD 1,000,000 or wallet balance became 50,000 USDC, respectively. Missing jurisdiction, unapproved beneficiary and self-approval were blocked at the appropriate governance state.

## Discrepancy register

**T14 — Mandatory policy conflict.** Expected label: FAIL_CLOSED_OR_ESCALATE. Observed governance decision: DENY, with MANDATORY_POLICY_CONFLICT_FAIL_CLOSED. This implements the frozen default. It counts as a semantic match, not an exact label match.

**T15 — Invented provider.** Expected lifecycle outcome: EXECUTION_VALIDATION_FAIL. Observed: DENY, with COUNTERPARTY_NOT_APPROVED and COUNTERPARTY_OUTSIDE_AUTHORITY. The provider is rejected before any executable instruction exists. The original oracle is retained unchanged. This case does not establish that the adapter's provider check was reached. Its test expectation should be reviewed explicitly in a subsequent version; no silent correction was made.

## Verification and reproducibility

The evaluator does not read expected outcomes. Assertions independently check known monetary balances, threshold boundaries, policy/envelope intersection, approval binding, expiry, revocation between authorization and execution, raw/tampered instruction rejection, duplicate rejection, audit snapshot immutability and settlement mismatch detection.

All original fixture checksums matched. A delivery manifest binds the implementation, resolved cases and result files. Full run-level evidence is in results/runs.jsonl. The same deterministic action/context output is hashed across each ten-run group. Wall-clock execution metadata is excluded from behavior hashes.

## Limits and remaining work

- The primary evaluation is Phase A only. No actual AI-agent inference, live rail call, smart-contract interaction or independent provider settlement occurred.
- Controls are implemented for the supplied policy profiles; this is not a general-purpose or security-certified authorization platform. Authentication, signing, distributed consistency, concurrency, rollback and crash recovery are not evaluated.
- Synthetic settlement receipts are generated from expected postings with explicit fault injection. Passing reconciliation cannot validate external settlement truth.
- The methodological literature gap concerning synthetic treasury data remains OPEN. This code package does not close a bibliographic gap.
- SHA-256 chains and registries support local integrity checks, not tamper-proof storage or production authentication.
- The paper must report the experiment as artifact-level verification. It cannot infer real-world superiority, regulatory sufficiency, product-market fit, optimal treasury strategy or human-versus-agent performance.
- GitHub publication has not occurred. The package is structured for later repository ingestion.

## Proposed next manuscript step

Consolidate the Evaluation/Results section and update the Claim–Evidence Matrix with these bounded findings. Keep the T15 discrepancy visible and T14 mapping explicit. Resolve the synthetic-data methodology citation gap before manuscript finalization. Phase B remains optional under the approved protocol.
