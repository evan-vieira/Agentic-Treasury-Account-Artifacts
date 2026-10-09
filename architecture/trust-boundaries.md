# Trust boundaries — Reference Architecture v1.2

Current document: [Reference Architecture v1.2](../REVIEWER_GUIDE.md), an editorial revision of the v1.1 design. TB1–TB5 and their controls are unchanged.

| Boundary | Crossing | Required design control | Phase A evidence limit |
| --- | --- | --- | --- |
| TB1 | External data → ATA | Normalize and check provenance, completeness and freshness. | Synthetic fixture freshness checks only. |
| TB2 | Financial intelligence → agent layer | Provide scoped treasury state and constraints. | No six-agent inference evaluated. |
| TB3 | Agent layer → Control Plane | Parse a `ProposedAction` as non-executable intent; independently evaluate principal, authority, policy and context. | Fixed proposals entered the implemented deterministic Control Plane. |
| TB4 | Control Plane → execution adapter | Permit only an `AuthorizedInstruction`; validate issuance, expiry, idempotency, provider and rail at execution time. | Simulated adapters, including D02/T15b provider validation. |
| TB5 | Execution rail → settlement evidence | Treat submission as incomplete until the outcome is checked and reconciled. | Synthetic receipts and injected reconciliation faults; no independent finality. |

The Treasury Governance & Controls Agent can explain or flag a control concern, but does not enforce authorization. An optional orchestrator has no independent financial authority. This is a proposed architecture; the listed boundary behavior is only experimentally supported where the Phase A artifact and reports explicitly exercise it.
