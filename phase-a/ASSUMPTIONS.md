# Implementation decisions — Sprint 3D v1.0

The 26 original Sprint 3C package files are preserved byte-for-byte and checked against the supplied SHA-256 manifest on every run. The approved scientific baseline is Research Charter v1.3, Reference Architecture v1.1, Policy Schema & Authority Model v1.0 and Sprint 3C v1.0. No claims or approved policy thresholds were changed.

## Explicit normalization and experiment resolution

- The flattened YAML actions are converted to a common action representation. `principal_id` is supplied from the corresponding Authority Envelope; `treasury_state_ref` uses ASTERIA-STG-v1.0. FX buy_asset becomes asset, and amount_usd_equivalent becomes amount; denomination remains visible as currency.
- S02 funding account is ACC-BR-OPER-01. Destinations are ACC-BR-USD-01 for USD and WAL-BR-USDC-01 for USDC. These routing fields were absent from the scenario YAML and are implementation choices, not newly discovered data.
- S04 source is ACC-US-OPER-01 for USD and WAL-US-USDC-01 for USDC. Jurisdiction is SG for S04 and BR for S02, from supplied counterparty records. A missing-jurisdiction mutation removes the resolved field; the evaluator does not fill it back in.
- S01-C is resolved as BRL 700,000, causing the reserve balance to fall to BRL 1,750,000, below the BRL 1,800,000 floor, while remaining below the authority maximum. The original narrative did not specify an amount.
- Stale data is 301 seconds old. T12 changes USD 450,000 to USD 400,000 after approval, so both amounts remain within the hard limit but require approval. T13 perturbs the observed source balance by +USD 1. T14 introduces an additional mandatory asset prohibition. T15 changes counterparty to INVENTED-PROVIDER.
- Six valid-approval lifecycle cases supplement the 18 scenario cases and 15 negative tests. Eight further safeguards were introduced during Sprint 3D and are reported separately, not retrospectively described as preregistered.
- Approvers are simulated trusted identities held in an in-process registry. Approval objects bind the complete normalized action hash, denomination, maximum amount and expiry. Instructions are compared with a local issued-instruction registry and rechecked at execution. These are research controls, not cryptographic signatures or production identity systems.
- Decimal arithmetic is used. FX fee = amount × quote × fee_bps/10,000, charged in BRL; total debit is rounded to cents. USDC accounting uses the supplied 1:1 synthetic assumption. No real FX or market data is retrieved.
- A subscription converts USD cash to synthetic fund units at the supplied unit value of 1. No yield accrual is simulated. Cross-border outflows are recorded in an external destination ledger for the receipt.
- Each case resets state. The engine is designed for these single-action scenario profiles and lifecycle fault injections, not general treasury portfolio management, concurrent executions, distributed idempotency or real settlement finality.
- Settlement receipts are synthetic outputs produced by an adapter stub. Reconciliation compares requested postings with observed receipt state. This checks plumbing and mismatch detection, not independent bank/on-chain verification.
- Clock time is fixed to the dataset timestamp except the explicit expiry test. Run wall-clock times are recorded separately in summary.json. Ten identical replays verify deterministic repeatability, not statistical reliability.

## Decision versus lifecycle outcomes

The control plane has exactly four outcomes: ALLOW, DENY, REQUIRE_APPROVAL, REQUIRE_ADDITIONAL_INFORMATION. Execution rejection, approval invalidation, unavailable rails and reconciliation exceptions are lifecycle outcomes, not additional governance decisions.

T14: the preregistered label FAIL_CLOSED_OR_ESCALATE corresponds to the implemented DENY default, a semantic match but not an exact-string match.

T15: the preregistered EXECUTION_VALIDATION_FAIL is not observed. The action is denied earlier because its provider is not approved and is outside authority. This is retained as an exact and semantic expectation discrepancy. It must not be concealed by weakening the governance layer or silently editing the original expected results. A future explicitly versioned test may isolate the adapter's provider-validation control.
