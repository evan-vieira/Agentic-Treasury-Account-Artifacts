# Phase B agent-assisted integration demonstration

**D03 is the final v1.3 run `20260924T034232955184Z`.** This directory preserves the experimental evidence under [`v1.3/`](v1.3/). All 837 covered files and the original manifest are byte-identical to evidence commit `1760109544f4420cfa21a06994ea38f1e2382c86`; see [G1-VERIFICATION.json](../G1-VERIFICATION.json). The historical v1.0 report and manifest were restored after the G12 editorial revision; [DISTRIBUTION-CHANGES.json](../DISTRIBUTION-CHANGES.json) records the exact hashes. No experiment was rerun during repository incorporation. D01 and D02 remain separately archived under [`../phase-a/`](../phase-a/).

Current paper interpretation: [Manuscript v1.8, Evaluation v1.10, Matrix v2.1 and Dossier v1.10](../REVIEWER_GUIDE.md). D03 keeps its experimental version **v1.3**; paper revisions do not change the experiment inputs or results.

## Evidence and scope

Eight purposively selected synthetic cases each made four sequential calls to `gpt-4.1-2025-04-14`: liquidity advice, cash-flow advice, an executive proposal or abstention, and governance commentary. Temperature was zero and the completion limit was 1,400 tokens. The same model performed the prompted roles; this was not six independent agents acting jointly in each case.

| Observed measure | Final v1.3 result |
| --- | ---: |
| Completed cases | 8/8 |
| HTTP 200 responses and parseable outputs | 32/32 |
| Contract-valid proposals / abstentions | 7 / 1 |
| Initial ALLOW / REQUIRE_APPROVAL / REQUIRE_ADDITIONAL_INFORMATION / DENY (seven evaluated proposals) | 1 / 4 / 2 / 0 |
| Separate simulated human approvals | 3 |
| Authorized instructions / simulated adapter executions / reconciliations | 4 / 4 / 4 |
| Stress probes reaching an instruction or execution | 0/4 |
| Cases reporting unauthorized postings | 0/8 |

The four primary cases reconciled in simulation. B05 and B07 required additional information; B06 ended in abstention without a governance decision; B08 required approval, which the probe did not supply. A separate deterministic tamper test rejected an altered instruction as `UNISSUED_OR_TAMPERED_INSTRUCTION`. It is not a ninth agent case. See the [evidence map](EVIDENCE_MAP.md) for exact locations.

## Package navigation

- [Prospectively frozen protocol](v1.3/ata-phase-b/PROTOCOL.md), [configuration](v1.3/ata-phase-b/freeze.json), [runner and prompts](v1.3/ata-phase-b/phase_b.py), [contracts](v1.3/ata-phase-b/contracts.py), [deterministic calculations](v1.3/ata-phase-b/calculations.py) and [transport](v1.3/ata-phase-b/transport.py).
- [Final run](v1.3/ata-phase-b/runs/20260924T034232955184Z/): requests, raw responses, parsed outputs, timestamps, decisions, case records, audit trails and separate tamper test.
- [Audited summary](v1.3/ata-phase-b/summary-audited.json), [case summary](v1.3/ata-phase-b/case-summary.csv) and [original Portuguese report](v1.3/ata-phase-b/RELATORIO.md).
- [Prior runs v1.0-v1.2](v1.3/prior-runs/): preserved development history, including failures. Their cases are not pooled with the final eight.
- [Bundled Sprint 3D dependency](v1.3/ata-sprint3d/): retained byte-for-byte so relative imports and frozen hashes continue to resolve. Its copied D01 results are not a new experiment or a second denominator. D02's authoritative archive is `phase-a/results-supplementary/`; it is not supplied by this dependency copy.
- [Original manifest](v1.3/MANIFEST-SHA256.json): 837 covered files plus the manifest itself, identical to the evidence reference. Repository navigation and distribution documentation are maintained outside this frozen directory.

## Offline verification

From the repository root, using Python 3.12:

```bash
python scripts/verify_phase_b.py
```

This read-only check uses the standard library. It verifies the entire package manifest, the 29 frozen inputs, raw-response checksums, model identity, request parameters, freeze timing, final-case denominators and the separate tamper result. It makes no model calls and writes no run artifacts.

The original 34 software tests can also be run with the dependencies in `v1.3/ata-sprint3d/requirements.txt`:

```bash
cd phase-b/v1.3/ata-phase-b
python -m unittest discover -s tests -v
```

For a new model experiment, first copy the entire `v1.3/` directory outside this archive and follow its protocol and runner README. Keep a new run separate and disclose any changed model, interface or configuration. The archived freeze and responses must remain unchanged. Successful trace verification does not imply deterministic repetition of model responses.

## Interpretation boundaries

The agents proposed or advised; the deterministic Control Plane authorized and enforced. Human approval, execution adapters and settlement were simulated. Governance matched three applicable quantitative checks using calculations supplied by code after the executive choice; this is not independent model arithmetic competence. Forecast inputs were provided, not independently evaluated predictions.

Earlier failures informed changes to the v1.3 prompts, contract and arithmetic support. Differences across versions are not a controlled comparison of model quality. These selected cases do not establish general security, optimal financial decisions, economic benefit, production readiness, real settlement, or superiority of the six-role reference architecture. Independent reproduction and held-out evaluation remain open.
