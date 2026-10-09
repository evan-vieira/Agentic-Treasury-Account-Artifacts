# Reviewer guide

This guide provides an English route through the evidence supporting the separately supplied manuscript. It is aligned with Manuscript v1.10, Evaluation and Results v1.11, Claim–Evidence Matrix v2.2 and Source Dossier v1.11 (G4/G9 bibliographic revisions and G10 manuscript typesetting of 9 October 2026). These versions preserve the G6/G7 clarifications. Manuscript v1.10 changes formatting only; its scientific text, four tables and 91 endnotes retain v1.9 content. Those editorial documents are supplied separately for review.

This guide on `main` reflects the current documents. The deposited snapshot remains release `v1.0-dataverse.2`, commit `0d252375e6a87280ae3a32bbf9077f744c90514a`. Harvard Dataverse assigned DOI [10.7910/DVN/EUZE5V](https://doi.org/10.7910/DVN/EUZE5V); the deposit was submitted for review and observed as unpublished on 9 October 2026. See the [status record](README.md#harvard-dataverse-status--9-october-2026).

## Suggested reading order

1. Read the scope and limitations in [README.md](README.md).
2. Inspect the [architecture](architecture/README.md), [trust boundaries](architecture/trust-boundaries.md) and [invariants](architecture/invariants.md). These specify proposed controls; they are not all empirically validated.
3. Check D01 in [case_summary.csv](phase-a/results/case_summary.csv), [runs.jsonl](phase-a/results/runs.jsonl), [summary.json](phase-a/results/summary.json) and [REPORT.md](phase-a/REPORT.md). Consult the [G6/G7 verification](G6-G7-VERIFICATION.md) for scenario grouping and settlement-count composition. Preserve the distinction between exact and semantic expectation matches.
4. Inspect the separate D02 [protocol](phase-a/results-supplementary/protocol.json), [summary](phase-a/results-supplementary/summary.json) and [raw records](phase-a/results-supplementary/runs.jsonl).
5. Read the D03 [protocol](phase-b/v1.3/ata-phase-b/PROTOCOL.md), [freeze](phase-b/v1.3/ata-phase-b/freeze.json), [executed contracts](phase-b/v1.3/ata-phase-b/contracts.py), [runner/prompts](phase-b/v1.3/ata-phase-b/phase_b.py) and [case summary](phase-b/v1.3/ata-phase-b/case-summary.csv). Inspect individual requests and responses in the [final run](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/).
6. Review [earlier Phase B runs](phase-b/v1.3/prior-runs/) and the [reproduction instructions](REPRODUCIBILITY.md).

## Claims and their evidence

| Question to examine | Evidence | Interpretation boundary |
| --- | --- | --- |
| Did D01 governance decisions match expectations? | [D01 summary](phase-a/results/summary.json): 27/27 governance cases; 31/33 original labels exact, 32/33 allowing T14 semantic equivalence. | T14 expected `FAIL_CLOSED_OR_ESCALATE` but observed `DENY`; T15 reached a governance denial before its intended adapter check. |
| How are the 90/100 settlements and 10/10 duplicate rejections composed? | [G6/G7 record](G6-G7-VERIFICATION.md), [case table](phase-a/results/case_summary.csv) and [raw runs](phase-a/results/runs.jsonl). | Eight labels contribute 80 terminal reconciliations; T09 contributes ten earlier reconciliations before its duplicate rejection. T13 supplies ten injected exceptions. T09 is the sole duplicate case; its rejected attempt creates no additional settlement. |
| Were deterministic decisions repeatable? | [47 case labels](phase-a/results/case_summary.csv), [470 raw replays](phase-a/results/runs.jsonl). | Replays of designed cases are not independent financial observations. |
| Are authority and policy separately enforced? | D02 A1/A2 paired variants in the [supplementary report](phase-a/SUPPLEMENTARY_REPORT.md). | Removal of controls in selected fixtures is not proof of universal architectural necessity. |
| Was downstream adapter validation exercised? | D02 T15b in [supplementary results](phase-a/results-supplementary/summary.json). | `PROVIDER_RAIL_MISMATCH` after authorization; a separate test that does not replace D01 T15. |
| Did model outputs enter the deterministic workflow? | D03 [audited summary](phase-b/v1.3/ata-phase-b/summary-audited.json): seven proposals and one abstention in eight cases; 32 calls. | One model performed four sequential roles; this is not a comparison of independent agents or the six proposed interfaces. |
| Were simulated workflows completed? | D03 B01–B04 [case records](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/): four instructions, executions and reconciliations; three separate-role simulated approvals. | No live bank, blockchain settlement or human authentication system was tested. |
| How did stress probes behave? | [B05](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/B05/result.json) and [B07](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/B07/result.json): information required; [B06](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/B06/result.json): abstention; [B08](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/B08/result.json): approval required and not supplied. | No instruction or execution in these four cases. No DENY in final D03. C54 concerns B05/B07; approval and tamper controls have separate claim mappings. |
| Was post-authorization tampering rejected? | D03 [separate tamper test](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/tamper-test/result.json). | Deterministic control test; not a ninth agent case. |
| Were quantitative governance checks independent model arithmetic? | [calculation audit](phase-b/v1.3/ata-phase-b/calculation-audit.json) and [calculations.py](phase-b/v1.3/ata-phase-b/calculations.py). | Arithmetic was supplied by code; forecasting inputs were provided. |

## Scenario identifiers

The scenario families are S01 liquidity, S02 FX/stablecoin, S03 yield allocation and S04 cross-border. Inspect [resolved/cases.json](phase-a/resolved/cases.json) for exact scenario membership, including adverse cases and approved variants. “Yield Allocation” is the current editorial label for S03; original fixture names remain byte-preserved. Do not attribute outcomes from other families to S03.

The S03 no-information-required statement applies only to the original 33-case cohort. Added safeguard X08 in S03 returns `REQUIRE_ADDITIONAL_INFORMATION` for an invalid amount. The [G6 grouping table](G6-G7-VERIFICATION.md#g6--scenario-grouping) identifies all 15 adverse cases.

The raw D01 summary uses historical field names containing `preregistered`. Current interpretation is **pre-specified cases**; those field names do not establish external preregistration.

## Phase B development history

| Version | Archived outcome | Why retained |
| --- | --- | --- |
| v1.0 | Three completed cases before an HTTP 429 stop; two invalid proposals; no execution. | Transport and contract failures informed later revisions. |
| v1.1 | Eight completed cases, 30 calls; three valid proposals, four invalid proposals, one abstention; no execution. | Records a completed run whose interface behavior did not achieve the intended primary workflows. |
| v1.2 | Eight cases, 32 calls; seven valid proposals, one abstention; three simulated reconciliations. | Records the interface and arithmetic issues addressed in the final revision. |
| v1.3 (D03) | Eight cases, 32 calls; seven valid proposals, one abstention; four simulated reconciliations. | Final evaluated integration package. |

Earlier cases are not pooled with D03. Changes to prompts, contracts and arithmetic support make these development runs unsuitable as a controlled comparison of model quality. Original Portuguese reports and English protocols remain available inside each archived package; this guide is a summary, not a replacement for the raw record.

## What is outside the package

The manuscript, source dossiers, editorial decisions, reviewer correspondence, commercial Addly documents and private Git history are excluded. Technical reports, experimental protocols and raw model prompts/responses are included because they are needed to assess the evidence. Independent reproduction and stronger empirical claims require additional work beyond reviewing this archive.
