# Phase B runner v1.1

Transport-only revision with frozen pacing, bounded retries and per-call checkpoints. Review PROTOCOL.md before execution. Python 3.12 and PyYAML 6.0.3 are required. Reuse the existing private OPENAI_API_KEY; never write it into this package.

```
python phase_b.py preflight
python phase_b.py freeze
python phase_b.py run
python phase_b.py summarize
```

Set ATA_MODEL_ID to the exact available snapshot before freeze. The experiment executed here uses gpt-4.1-2025-04-14. Retry settings are in freeze.json under transport_policy. ATA_MAX_CALLS from v1.0 is replaced by the frozen max_http_attempts_per_run, which counts all HTTP attempts.

To recover a stopped v1.1 run without repeating saved responses:

```
python phase_b.py run --resume RUN_ID
python phase_b.py summarize
```

Resume requires identical frozen inputs, run freeze, request bodies and response checksums. An attempt without final metadata is ambiguous and stops for review. Permanent errors and exhausted frozen budgets cannot be solved by repeatedly resuming. HTTP 200 content is never regenerated.

The prior v1.0 run is under ../prior-runs/v1.0/ata-phase-b and is excluded from v1.1 denominators. The historical Sprint 3D results are under ../ata-sprint3d/results; they are never pooled with Phase B. Runs here contain only fictional treasury fixtures. No banking API is used.
