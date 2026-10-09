# Phase B v1.3

Python 3.12 and PyYAML 6.0.3. Read PROTOCOL.md for the prospectively frozen changes and claim boundaries. Credentials are loaded privately through OPENAI_API_KEY and are never included in artifacts.

Set ATA_MODEL_ID to the exact model snapshot before freezing; this experiment uses gpt-4.1-2025-04-14. The default endpoint is https://api.openai.com/v1/chat/completions.

```
python phase_b.py preflight
python phase_b.py freeze
python phase_b.py run
python phase_b.py summarize
```

For an interrupted v1.3 run, preserve the identical frozen files and all partial artifacts:

```
python phase_b.py run --resume RUN_ID
python phase_b.py summarize
```

Retries cannot repair content or bypass exhausted frozen budgets, quota/authentication failures or ambiguous unfinished attempts. The transport policy is frozen, not controlled by ATA_MAX_CALLS. Calls are sequential, 15 seconds apart or slower when indicated by the API. Four stages per case make 32 model calls; the separate tamper test makes no model call.

contracts.py documents and validates the output interface, including required S02 jurisdiction and route consistency. calculations.py computes verified arithmetic from the chosen action and checks the governance report; it never repairs economic choices. The model still chooses the proposed action. The unchanged Sprint 3D Engine decides authority/policy and simulates settlement. All treasury data are fictional. No banking integration is used.

Run offline tests with `python -m unittest discover -s tests -v`. Test fixtures are clearly labeled and are not empirical model outputs. Prior versions are under ../prior-runs, outside this version's runs directory and denominators. Original D01/D02-related results remain separate under ../ata-sprint3d/results.
