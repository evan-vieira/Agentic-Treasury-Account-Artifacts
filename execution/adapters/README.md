# Execution adapter boundary

The current [Reference Architecture v1.2](../../REVIEWER_GUIDE.md), an editorial revision of v1.1, defines adapters for bank transfers, instant payments, FX, stablecoins, tokenized deposits, tokenized investments and blockchain settlement. Their common input is an `AuthorizedInstruction`, never an agent's `ProposedAction` or free-form reasoning.

The Phase A simulator implements selected **synthetic** bank, FX, stablecoin, fund and cross-border profiles in [`../../phase-a/src/engine.py`](../../phase-a/src/engine.py). Tokenized-deposit execution was not separately exercised. No live provider integration, cryptographic instruction signature, real finality or production adapter contract is present in this directory. D02/T15b tests a provider/rail mismatch after governance authorization in the simulated adapter.
