# Phase B v1.1 — transport amendment, preregistered before calls

This amendment supersedes the stop/restart policy of v1.0 for this new experiment. The earlier run `20260924T022249819508Z` remains archived, including 11 HTTP 200 responses, one HTTP 429 and 3/8 completed cases. This v1.1 run is a new, separately reported eight-case experiment, not a continuation pooled with v1.0. D01/D02 denominators are unchanged.

## Frozen operational rules

- Same exact requested model `gpt-4.1-2025-04-14`, temperature 0, max_completion_tokens 1400; same prompts, case order, synthetic dataset, economic mapping and Control Plane evaluation.
- At least 15 seconds between request starts. Use server rate-limit remaining/reset headers to extend waits when fewer than 7,000 estimated tokens or one request remain. This is a conservative scheduling reserve, not an exact tokenizer.
- Retry only temporary HTTP 429 rate-limit errors, HTTP 500/502/503/504 and network errors. Quota, billing, authentication and other permanent errors stop execution. A network timeout can leave remote completion unknown; preserve this uncertainty and any billed usage may exceed observed responses.
- At most 6 total attempts per logical call and 100 attempts across a run, counting failures. At most 600 seconds elapsed across retries of one call. Exponential waits start at 5 seconds, cap at 120 seconds, and add 0–1 seconds jitter. Server Retry-After (seconds or date) and applicable reset hints are lower bounds, never shortened. Any pending wait above 180 seconds defers execution for a later resume instead of sending early.
- Successful HTTP 200 content is never regenerated. Invalid JSON/non-object content is a terminal model-output failure: preserve it, count the case failure, continue to the next independent case. Invalid proposals, abstentions and governance denials are outcomes, not retry triggers.
- Every attempt has an immutable request, original HTTP response bytes (or explicitly labeled local transport-error record), timestamps, checksum, selected response headers, parse output/error and transport error metadata.
- `run --resume RUN_ID` reuses saved HTTP 200 responses only when the request and response checksum match. Completed cases are reused. An incomplete attempt with unknown outcome requires review; it is never silently replaced. Attempt/time limits persist across restarts. A process lock prevents concurrent runs against this version.
- New freeze includes this amendment via PROTOCOL.md, runner and transport code hashes plus the original experimental input hashes. Do not modify frozen files in place.

## Known v1.0 implementation limitations retained

The actual order uses Liquidity as executive on S01 before the forecasting call: three calls on B01/B05 and four on each other case, 30 total. Its S01 executive prompt does not receive an authority envelope. Governance prior_advice does not include the executive proposal. The stale probe changes balance data before generation. The missing-jurisdiction probe adds objective text without removing jurisdiction-related data. The post-proposal tamper test described in the original protocol is not implemented; report it as not executed, even if an eligible approval occurs. These are not corrected by this transport-only amendment and constrain interpretation.

All original protocol text below the amendment remains applicable except where these operational rules and explicit implementation clarifications supersede it. There is no guarantee of continuous API availability or of valid/approved economic proposals.
