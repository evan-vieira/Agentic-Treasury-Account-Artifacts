# Reference design package

**Status: proposed architecture, not a tested six-agent implementation.** The current document sources are *Agentic Treasury Account Reference Architecture v1.2*, *Policy Schema & Authority Model v1.1*, and *Research Charter v1.5*, as described in the [reviewer guide](../REVIEWER_GUIDE.md). They are a design artifact separate from the byte-frozen [`../phase-a/`](../phase-a/) experiment.

The six agent contracts in [`../agents/`](../agents/) describe expected interfaces, not executed model prompts or observed agent behavior. The JSON Schemas in `authority/`, `policies/`, `approvals/`, `execution/`, `settlement/`, and `audit/` define **proposed interoperable shapes**. The Phase A Python engine uses its own flat fixture representations; no claim is made that it consumes or validates these schemas.

| Current source | Original transcription source | Design elements represented |
| --- | --- | --- |
| Reference Architecture v1.2 | v1.0 §24 and v1.1 (23 September 2026) | Six layers, agents, TB1–TB5, I1–I14, authority/policy separation, approvals and lifecycle |
| Policy Schema & Authority Model v1.1 | v1.0 (23 September 2026) | Principal, Proposed Action, Authority Envelope, Treasury Policy, decisions, approvals, instruction and audit shapes |
| Research Charter v1.5 | v1.3 | Research scope, evidence boundaries and repository compendium |

Architecture v1.2 and Policy Schema v1.1 are editorial revisions. The YAML architecture filename/version and JSON Schema IDs retain **design-package v1.1** because no interface shape or rule changed. Source metadata identifies both the current documents and original transcription sources. “Control Plane” names the deterministic mechanism within the Governance and Authority Plane. The original source references below are provenance, not pointers to current paper versions.

The ten original invariants I1–I10 were transcribed from the approved v1.0 source into [`invariants.md`](invariants.md). The four v1.1 additions remain I11–I14. The complete register is an architectural specification; Phase A exercised selected properties rather than validating all fourteen invariants in production.

Run `python scripts/check_design.py` from the repository root to check the JSON and YAML syntax, schema identifiers, references and contract inventory. This is a **design-package integrity check**, not Phase B evaluation or a claim that the Phase A engine implements every field.

The separately archived [D03 / Phase B v1.3](../phase-b/README.md) demonstrates model-generated intent entering the deterministic workflow in eight synthetic cases. Its implemented Python output contract and prompted roles differ from these proposed schema/interface artifacts. D03 supplies bounded integration evidence; it does not establish that all fourteen invariants or the full six-role architecture were validated.
