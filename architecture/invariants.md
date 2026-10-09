# Architectural invariants — approved source register

**Source of I1–I10:** *Crypto Valley Paper - Agentic Treasury Account Reference Architecture v1.0*, Sprint 3A, section 24, pp. 20–21. **Source of I11–I14:** *Crypto Valley Paper — Agentic Treasury Account Reference Architecture v1.1*, section 27. The v1.1 source states that the ten original invariants remain frozen and adds four governance invariants. The current [Reference Architecture v1.2](../REVIEWER_GUIDE.md) is an editorial revision that retains these invariants. The version references below identify their origins. The statements below preserve their source wording; capitalization is retained.

| ID | Approved invariant | Source |
| --- | --- | --- |
| I1 | No financial execution without an explicit authorized instruction. | v1.0 §24 |
| I2 | AI-generated intent and execution authority are separate objects. | v1.0 §24 |
| I3 | Policies are external to agent reasoning and independently enforceable. | v1.0 §24 |
| I4 | Every executable action must be attributable to a policy context. | v1.0 §24 |
| I5 | Material actions may require independent human approval. | v1.0 §24 |
| I6 | Every executed transaction produces traceable evidence. | v1.0 §24 |
| I7 | Execution must support reconciliation against observed financial state. | v1.0 §24 |
| I8 | Traditional and on-chain rails use the same governance abstraction whenever possible. | v1.0 §24 |
| I9 | An agent's authority is contextual, not universal. | v1.0 §24 |
| I10 | Failure to validate policy, authority or required information results in no execution. | v1.0 §24 |
| I11 | A Proposed Action is never directly executable. | v1.1 §27 |
| I12 | Authority Envelope and Treasury Policy remain independent governance objects. | v1.1 §27 |
| I13 | Every governance decision records its policy and authority versions. | v1.1 §27 |
| I14 | An approval is bounded to a defined action and conditions and cannot act as unlimited delegated authority. | v1.1 §27 |

## Evaluation boundary

This is an architectural register, **not a claim that all fourteen invariants were empirically demonstrated**. Phase A used fixed proposals and simulated execution. Its D01 and separately versioned post-hoc D02 records exercise selected governance, approval, instruction-gating, rail, audit and reconciliation properties; consult [`../phase-a/EVIDENCE_MAP.md`](../phase-a/EVIDENCE_MAP.md) and the experiment reports for exact case-level evidence and discrepancies. In particular, Phase A did not evaluate whether AI agents generated sound intent, and simulated receipts cannot establish independent settlement truth.

The general design boundary is that probabilistic components have no unrestricted authority to move corporate money. The Governance Agent is distinct from the deterministic Control Plane. These are prior-art-grounded design constraints rather than individual novelty claims.
