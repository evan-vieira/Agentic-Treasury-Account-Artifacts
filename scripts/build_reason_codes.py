"""Catalog reason codes observed in archived Phase A records, without rewriting them."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "phase-a/results/runs.jsonl",
    "phase-a/results-supplementary/runs.jsonl",
]


def visit(value, codes):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "reason_codes" and isinstance(child, list):
                codes.update(code for code in child if isinstance(code, str))
            else:
                visit(child, codes)
    elif isinstance(value, list):
        for child in value:
            visit(child, codes)


codes = set()
for source in SOURCES:
    with (ROOT / source).open() as stream:
        for line in stream:
            visit(json.loads(line), codes)
record = {
    "status": "observed_phase_a_reason_codes",
    "description": "Registry of codes present in frozen D01 or D02 records; not an exhaustive policy ontology or a combined experimental denominator.",
    "sources": SOURCES,
    "codes": sorted(codes),
}
(ROOT / "policies/reason-codes.yaml").write_text(yaml.safe_dump(record, sort_keys=False))
print(f"Catalogued {len(codes)} observed reason codes")
