# ATA Sprint 3C v1.0 — Synthetic Treasury Dataset & Reproducible Simulation Scenarios

This package is a **synthetic research artifact** for the Crypto Valley Association paper project.
It contains no real customer data and should not be interpreted as calibrated market data, legal guidance, or evidence of production performance.

## Frozen context
- Dataset version: `ASTERIA-STG-v1.0`
- Canonical timestamp: `2026-09-23T15:00:00Z`
- Random seed: `20260923`
- Every scenario resets to the same base state before execution.
- Synthetic market values are fixed inputs, not real-world observations.

## Evaluation phases
1. **Phase A — deterministic replay:** frozen ProposedAction fixtures, no LLM calls. Primary governance evaluation.
2. **Phase B — agent-assisted demonstration:** optional agent generation; archive model/prompt/parameters/output. Not expected to be bit-for-bit deterministic.

## Four scenarios
- S01 Intragroup Liquidity Movement
- S02 FX and Stablecoin Execution
- S03 Yield Optimization
- S04 Cross-Border Settlement

## Important evidence boundary
The project Source Dossier still marks the methodological justification for synthetic treasury datasets as an evidence gap. This package operationalizes the approved methodology; it does not by itself close that literature gap.
