# Verification and reproduction

Run all commands from the directory specified below. Financial workflows use synthetic data and simulated adapters. No account credentials or model API key are needed for archive verification, design checks, offline tests or Phase A replay.

## Environment

The original D01 and Phase B records specify Python 3.12 and PyYAML 6.0.3. D02 records Python 3.13.5. Install the pinned dependency in a separate environment:

```bash
python -m venv .venv
```

Activate that environment using the command for your operating system, then:

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

First make a separate copy of `phase-a/`. The runners write into `results/` and `results-supplementary/`; preserve the archived copy for comparison. In the separate copy:

```bash
python src/run.py
python supplementary/run_supplementary.py
```

Compare the new summaries and case outcomes with the archived summaries. New timestamps and generated audit values may prevent byte-for-byte identity, even when the deterministic outcomes agree. Do not update the archived manifests to conceal a difference. Report D01's T14/T15 discrepancies and keep D02 separate.

## New model experiments

A new Phase B model run is optional and is **not** required to inspect the final raw responses. It requires separately provisioned credentials, model access and API expenditure. Copy the complete `phase-b/v1.3/` package to a separate working directory and follow its original protocol. Preserve the requested and returned model IDs, prompts, parameters, failures and changes. Do not overwrite this archive. Temperature zero does not guarantee identical future model responses.

## Publication preparation checks

The preparation record in [VERIFICATION.md](VERIFICATION.md) records the environment and checks performed on this export. The exported repository begins with a new root commit. The private repository and its earlier Git history are not required to inspect or verify the distributed evidence.
