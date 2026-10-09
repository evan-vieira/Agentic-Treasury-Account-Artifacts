# Agentic Treasury Account — research artifacts

Code, synthetic data, evaluation records and verification tools accompanying **Agentic Treasury Accounts: Programmable Money, Stablecoins and AI Agents as the Executive Layer of On-Chain Corporate Finance**, by Evandro Camilo Vieira.

Start with the [reviewer guide](REVIEWER_GUIDE.md), then the [reproduction instructions](REPRODUCIBILITY.md). The manuscript is supplied separately for editorial review. This repository has an independent history and contains no manuscript DOCX/PDF, editorial correspondence or private repository history.

## Evidence included

| Record | Design and denominator | Entry points |
| --- | --- | --- |
| **D01** | Fixed proposals, 47 synthetic case labels, ten deterministic replays per label: 470 runs. No LLM calls. | [Phase A map](phase-a/EVIDENCE_MAP.md), [summary](phase-a/results/summary.json), [case table](phase-a/results/case_summary.csv) |
| **D02** | Five post-hoc variants, ten replays each: 50 runs reported separately. | [Supplementary report](phase-a/SUPPLEMENTARY_REPORT.md), [results](phase-a/results-supplementary/) |
| **D03** | Phase B v1.3, eight cases and 32 sequential calls to `gpt-4.1-2025-04-14`. | [Phase B map](phase-b/EVIDENCE_MAP.md), [protocol](phase-b/v1.3/ata-phase-b/PROTOCOL.md), [final run](phase-b/v1.3/ata-phase-b/runs/20260924T034232955184Z/) |

The complete D03 package retains earlier v1.0–v1.2 development runs, including failures. Their outcomes are excluded from the final D03 denominator. The original manifest covers 837 files; the manifest itself is an additional file. The bundled copy of Sprint 3D is a dependency, not an additional experiment.

## Distribution revision and reuse

This is the **G3 distribution revision of v1.0, dated 9 October 2026**. It adds
licensing, citation metadata and clearer reproduction commands. The experimental
versions and frozen records remain unchanged. The earlier `v1.0` tag remains at
`514d0fedccfc146ccb775eb2d4dda1729a60e43c`; use the exact new snapshot/commit
identified with the G3 archive for deposit and citation.

- **Software: MIT. Data and documentation: CC BY 4.0.** See [LICENSE.md](LICENSE.md)
  and the complete [file license map](LICENSE-MAP.json).
- **Citation:** [software metadata](CITATION.cff) and
  [data/evaluation metadata](citation/DATA-CITATION.cff).
- **Dataverse:** [deposit settings](DATAVERSE-DEPOSIT.md) and
  [component-license text](DATAVERSE-TERMS.txt). The DOI is still pending.

## Verify without model access

Use Python 3.12 and PyYAML 6.0.3, the recorded D01/Phase B environment.
D02 originally ran under Python 3.13.5. Extract the deposited archive and open
its root directory, or clone this repository and record `git rev-parse HEAD`.
A clone of `main` retrieves its current state; use the deposit's exact commit
when reproducing that snapshot. Git and `.git` are unnecessary for the archive.

Create and activate a virtual environment as shown in
[REPRODUCIBILITY.md](REPRODUCIBILITY.md). From the repository/archive root:

```bash
python -m pip install -r phase-a/requirements.txt
python scripts/verify_public_artifact.py
python phase-a/scripts/verify_frozen.py
python scripts/verify_phase_b.py
python scripts/check_design.py
```

These checks make no API calls and do not rerun the experiments. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for offline tests, isolated deterministic replays, and the distinction between archive verification and a new model experiment.

## Reference design

The [architecture](architecture/README.md), [six proposed agent contracts](agents/README.md), and schemas under `authority/`, `policies/`, `approvals/`, `execution/`, `settlement/` and `audit/` are design artifacts. Their complete interfaces were not validated by the experiments. D01/D02 use the simulator's flat fixtures; D03 uses its own executed Python contract and four prompted stages.

## Provenance and interpretation

The experimental evidence originated at commit `1760109544f4420cfa21a06994ea38f1e2382c86`; the selected source snapshot was `6fcd42d057317a6b815fd6513316e0213416a440`. These are provenance identifiers, not commits to check out in this independent repository. [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json) records the original blob IDs and exported checksums. [MANIFEST-SHA256.json](MANIFEST-SHA256.json) covers the distributed files.

The frozen technical reports are retained in their original language and wording, including Portuguese Phase B reports and historical publication-status statements. The current English [reviewer guide](REVIEWER_GUIDE.md) and [Phase B README](phase-b/README.md) provide navigation and interpretation; historical statements do not describe the present repository status.

All treasury entities, balances, providers, approvals, rails and settlement receipts are fictional or simulated. The evidence does not establish live financial integration, production security, economic superiority, general agent competence or independent external reproduction. D01's T14/T15 discrepancies remain visible. D03 observed no DENY among seven evaluated proposals; the eighth case was an abstention without a Control Plane decision.

Cite the exact public commit used and report D01, D02 and D03 separately. The component license grants are defined in [LICENSE.md](LICENSE.md). Making these artifacts available does not indicate acceptance or publication of the manuscript by a journal.
