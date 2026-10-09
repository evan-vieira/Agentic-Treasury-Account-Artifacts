# Phase B runner

This is a separate, prospective supplement to ATA Sprint 3D. It needs the sibling `ata-sprint3d` folder and Python 3.12 + PyYAML 6.0.3. It makes model calls only when explicitly invoked with `run` after `freeze`. The default endpoint is `https://api.openai.com/v1/chat/completions`; a compatible endpoint can be specified with `ATA_MODEL_ENDPOINT`. All execution remains in the local simulated Control Plane.

```bash
export OPENAI_API_KEY='set privately in your terminal'
export ATA_MODEL_ID='your exact available model identifier'
python phase_b.py freeze
python phase_b.py run
python phase_b.py summarize
```

`freeze` checks the key is present but never stores or prints it. It writes `freeze.json` containing the model, endpoint origin, parameters, hashes and prompt version before any calls. `run` creates a uniquely named directory inside `runs/`, saves every response and attempt, and refuses changed frozen inputs. A new `freeze` needs a new package version; do not overwrite the previous experiment after execution. API costs depend on the model. `ATA_MAX_CALLS` may impose a lower budget and results in a partial run.

To verify the integration without model access: `python phase_b.py preflight`. This validates files, imports the simulator, and confirms no Phase B empirical evidence exists. It does not call a model and must not be reported as an executed Phase B.
