# G6/G7 — scenario grouping and count composition

Verified on **9 October 2026** against artifact tag `v1.0-dataverse.1`, commit
`fbe6559bdfb53819b0ed7d825eddcfe716868434`. All **19 checks passed**.
The [machine-readable record](G6-G7-VERIFICATION.json) separates the read-only
tag audit from the subsequent editorial resolution. G6 and G7 are closed for
Manuscript v1.7 and Evaluation and Results v1.9, supplied separately for review.
No experiment was rerun and no frozen evidence file, outcome or denominator changed.

## G6 — scenario grouping

The 15 adverse cases in [cases.json](phase-a/resolved/cases.json) are grouped as follows:

| Scenario | Adverse cases |
| --- | --- |
| S01 | T01, T03, T09 |
| S02 | T04, T05, T10, T12, T15 |
| S03 | T06, T14 |
| S04 | T02, T07, T08, T11, T13 |

The original D01 cohort contains 33 labels. Within that cohort, S03 has no
`REQUIRE_ADDITIONAL_INFORMATION` outcome. Among the added safeguards, **X08 in
S03 does return that outcome for an invalid amount**. Evaluation Table 8.2 and
the manuscript's scenario-coverage statement now identify that scope explicitly;
the table is not an exhaustive inventory of all 47 D01 labels.

## G7 — 90/100 settlements and both 10/10 results

The nine case labels contributing reconciled settlements are S01-A, S03-A,
S01-B-APPROVED, S02-A-APPROVED, S02-B-APPROVED, S03-B-APPROVED,
S04-A-APPROVED, S04-B-APPROVED and the **first execution in T09**.
Ten replays of each yield **90 RECONCILED settlements**. T13 contributes the
remaining ten settlements, all deliberately mismatched and classified as
**EXCEPTION (10/10)**.

Use [case_summary.csv](phase-a/results/case_summary.csv) and
[runs.jsonl](phase-a/results/runs.jsonl) together. The CSV records each case's
final state and exposes 80 terminal RECONCILED runs. Its T09 row records
`EXECUTION_REJECTED` and reconciliation `N/A`. T09's ten earlier successful
reconciliations appear in the raw `execution_detail.first_execution` records
and `RECONCILIATION` audit events. The CSV is correct as recorded.

**T09 is the only duplicate-instruction case in D01.** Its second attempt is
rejected with `DUPLICATE_INSTRUCTION` in all ten replays (10/10). Each replay has
one adapter submission; the rejected attempt creates no extra settlement.
These are repetitions of one designed case, not independent duplicate attempts.
D01, D02 and D03 denominators remain separate.

## Evidence hashes

| File | SHA-256 |
| --- | --- |
| `phase-a/resolved/cases.json` | `76c346e2ddfbcc9629728eeb232915be52c515dad05b06a6620b921caf8b9b42` |
| `phase-a/results/case_summary.csv` | `cdf1ae2fbd77cc2e22a67fc71d2ca9d70184e08df028620d098f152815a78fe1` |
| `phase-a/results/runs.jsonl` | `5df3aab863fdedb7f649bb2120ab7741cac2687275d6d45499f9f9b79a4a5f43` |
| `phase-a/results/summary.json` | `3cc71d2ee86cf42b6d6d251f0415a6d4dd5af301a162a91f4b259760d9195501` |

## Release boundary

This verification note and its JSON record were added to `main` after the tag.
They are not files inside the existing tagged archive. Tag `v1.0-dataverse.1`
and its prepared deposit archive remain unchanged. The 944-entry root-manifest
check in the audit record applies to that tag; the current root manifest covers
the current `main` inventory. The original D01/D02 and 837-entry D03 manifests
remain intact. This documentation update assigns no DOI, creates no deposit,
and makes no claim of independent external reproduction or closure of other gates.
