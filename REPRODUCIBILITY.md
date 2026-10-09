# Verification and reproduction

Run all commands from the directory specified below. Financial workflows use synthetic data and simulated adapters. No account credentials or model API key are needed for archive verification, design checks, offline tests or Phase A replay.

## Environment

The original D01 and Phase B records specify Python 3.12 and PyYAML 6.0.3. D02 records Python 3.13.5. Install the pinned dependency in a separate environment:

```bash
python -m venv .venv
```

On macOS/Linux (bash/zsh):

```bash
source .venv/bin/activate
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1`. If activation is not
available, use `.venv/bin/python` (macOS/Linux) or `.venv\Scripts\python.exe`
(Windows) in place of `python` in the commands. Then:

```bash
python -m pip install -r phase-a/requirements.txt
```

## Read-only archive checks

From the repository root:

```bash
python scripts/verify_public_artifact.py
python phase-a/scripts/verify_frozen.py
python scripts/verify_phase_b.py
python scripts/check_design.py
```

| Check | Expected result |
| --- | --- |
| Public package | All distributed files match the root SHA-256 manifest; no unexpected tracked artifact files. |
| Phase A | 44 delivery files, seven supplementary files and 26 original fixtures match; 470 D01 and 50 D02 archived records. |
| Phase B | 837 package entries, 29 frozen inputs and 32 raw final responses match; eight cases, seven proposals, one abstention, four simulated reconciliations. |
| Reference design | Ten schemas, six proposed contracts, six layers, fourteen invariants and 33 observed reason codes. This checks syntax/inventory only. |

The root manifest excludes itself. It also records per-file origins in `SOURCE_PROVENANCE.json`. Hash verification establishes byte identity to this distribution, not scientific validity or independent replication.

## Offline software tests

From `phase-a/`:

```bash
python -m unittest discover -s tests -v
```

Expected: 13 passing software tests.

From `phase-b/v1.3/ata-phase-b/`:

```bash
python -m unittest discover -s tests -v
```

Expected: 34 passing software tests. Network transport is mocked, and an offline placeholder is used in place of a credential. These tests are not new observations from an LLM and are not added to D01–D03 denominators.

## New deterministic replays

The runners write into `results/` and `results-supplementary/`. Preserve the
archived copy. From the repository/archive root, this command creates a sibling
working copy (and fails instead of overwriting an existing destination):

```bash
python -c "from pathlib import Path; import shutil; shutil.copytree('phase-a', Path.cwd().parent / 'ata-phase-a-replay')"
cd ../ata-phase-a-replay
```

In this separate working copy, with the same virtual environment active:

```bash
python src/run.py
python supplementary/run_supplementary.py
```

Compare `results/summary.json`, `results/case_summary.csv` and
`results-supplementary/summary.json` with the originals. Ignore only the summary
fields `started_at`, `completed_at` and `python` when comparing environments.
For D01, expect 470 runs, 27/27 governance matches, 31/33 exact and 32/33 semantic
matches, zero unauthorized executions and 90/100 reconciled settlements.
For D02, expect 50 separate runs with all expected matches and deterministic
case results. Keep the D01 and D02 counts separate. New timestamps and generated audit values may prevent byte-for-byte identity, even when the deterministic outcomes agree. Do not update the archived manifests to conceal a difference. Report D01's T14/T15 discrepancies and keep D02 separate.

## New model experiments

A new Phase B model run is optional and is **not** required to inspect the final raw responses. It requires separately provisioned credentials, model access and API expenditure. Copy the complete `phase-b/v1.3/` package to a separate working directory and follow its original protocol. Preserve the requested and returned model IDs, prompts, parameters, failures and changes. Do not overwrite this archive. Temperature zero does not guarantee identical future model responses.

## License and citation scope

The software is MIT-licensed; data and documentation are CC BY 4.0 as mapped
in [LICENSE.md](LICENSE.md). Use the root [CITATION.cff](CITATION.cff) for software
and [citation/DATA-CITATION.cff](citation/DATA-CITATION.cff) for the data/evaluation
record. Identify the exact commit and, once published, the archival DOI.

## Publication preparation checks

The preparation record in [VERIFICATION.md](VERIFICATION.md) records the environment and checks performed on this export. The exported repository begins with a new root commit. The private repository and its earlier Git history are not required to inspect or verify the distributed evidence.
