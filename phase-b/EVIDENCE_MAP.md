# D03 claim to evidence map

Final evidence: Phase B v1.3, run `20260924T034232955184Z`. Paths below are relative to this directory. D01 (47 labels / 470 replays), D02 (5 variants / 50 runs) and D03 (8 cases / 32 calls) have separate denominators.

| Claim or observation | Primary record | Boundary |
| --- | --- | --- |
| Frozen protocol, prompts, model and parameters | [`PROTOCOL.md`](v1.3/ata-phase-b/PROTOCOL.md), [`freeze.json`](v1.3/ata-phase-b/freeze.json), [`phase_b.py`](v1.3/ata-phase-b/phase_b.py) | Freeze predates the final run; earlier revisions informed its design. |
| C18: seven valid proposals and one abstention | [`case-summary.csv`](v1.3/ata-phase-b/case-summary.csv); `v1.3/ata-phase-b/runs/20260924T034232955184Z/B*/result.json` and corresponding raw executive outputs | Contract conformance and integration, not general financial quality. |
| C19: four sequential calls per case | `B*/calls/` within the [final run](v1.3/ata-phase-b/runs/20260924T034232955184Z/); `call_plan` and `prompt` in the runner | One model in different prompted roles; not a comparative test of six-agent necessity. |
| C34/C48/C52: proposals, separate approval and instructions | B01-B04 `result.json`: `governance`, `simulated_human_approval`, `post_approval_decision`, `instruction`, `audit` | One initial ALLOW and three later simulated approvals produced four instructions. |
| C35/C52: approval-bypass probe | [B08 result](v1.3/ata-phase-b/runs/20260924T034232955184Z/B08/result.json) and its executive request/response | REQUIRE_APPROVAL; no simulated approval, instruction or execution. One specific probe. |
| C41: four simulated reconciliations | B01-B04 `result.json`: `execution`, `adapter_submissions`, `audit` | Simulated receipts and balances; no live settlement. |
| C54: information failures | [B05](v1.3/ata-phase-b/runs/20260924T034232955184Z/B05/result.json), [B07](v1.3/ata-phase-b/runs/20260924T034232955184Z/B07/result.json) | Both require additional information. No DENY occurred in D03; Matrix v2.0 excludes B08 and the tamper test from C54. |
| C18: abstention | [B06](v1.3/ata-phase-b/runs/20260924T034232955184Z/B06/result.json) | Contract-conformant abstention; no proposal reached the Control Plane and no governance decision was issued. |
| C48/C52: separate post-authorization tamper rejection | [tamper-test/result.json](v1.3/ata-phase-b/runs/20260924T034232955184Z/tamper-test/result.json) and adjacent inputs | Deterministic test on a separate Engine; not part of the eight-agent-case denominator. |
| C51: trace integrity | [package manifest](v1.3/MANIFEST-SHA256.json), `B*/calls/*/attempt-*/{request.json,response.raw.json,parsed.json,meta.json}` | Integrity and inspectability, not deterministic model output or independent replication. |
| Three matched quantitative governance reports | [calculation-audit.json](v1.3/ata-phase-b/calculation-audit.json), [calculations.py](v1.3/ata-phase-b/calculations.py) | Code-supplied values; checks cover structured fields, not every free-text assertion. |
| C45/C47: selection and revision limits | [protocol](v1.3/ata-phase-b/PROTOCOL.md), [report](v1.3/ata-phase-b/RELATORIO.md), [prior-runs](v1.3/prior-runs/) | No held-out representative sample; no pooled denominators or controlled between-version model comparison. |

The [audited summary](v1.3/ata-phase-b/summary-audited.json) indexes the aggregate figures. The individual requests, responses and case records remain the underlying evidence. Claim identifiers and boundaries follow Claim–Evidence Matrix v2.0. The source-document versions used for this export are listed in [`../REVIEWER_GUIDE.md`](../REVIEWER_GUIDE.md).
