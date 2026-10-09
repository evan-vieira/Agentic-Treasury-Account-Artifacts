"""Verify archived Phase A manifests and record counts without modifying files."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def check_manifest(name):
    manifest = json.loads((ROOT / name).read_text())
    bad = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            bad.append(item["path"])
    print(f"{name}: {len(manifest['files']) - len(bad)}/{len(manifest['files'])} files match")
    return bad


def count_lines(name):
    with (ROOT / name).open("rb") as f:
        return sum(1 for _ in f)


def main():
    bad = check_manifest("metadata/delivery-manifest.json")
    bad += check_manifest("metadata/supplementary-manifest.json")
    original = json.loads((ROOT / "metadata/sprint3c-manifest.json").read_text())
    original_bad = []
    for item in original["files"]:
        path = ROOT / item["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            original_bad.append(item["path"])
    print(f"original fixture manifest: {len(original['files']) - len(original_bad)}/{len(original['files'])} match")
    bad += original_bad
    d01 = json.loads((ROOT / "results/summary.json").read_text())
    d02 = json.loads((ROOT / "results-supplementary/summary.json").read_text())
    for label, actual, expected in [
        ("D01 raw runs", count_lines("results/runs.jsonl"), 470),
        ("D01 summary runs", d01["total_runs"], 470),
        ("D02 raw runs", count_lines("results-supplementary/runs.jsonl"), 50),
        ("D02 summary runs", d02["total_supplementary_runs"], 50),
    ]:
        print(f"{label}: {actual}/{expected}")
        if actual != expected:
            bad.append(label)
    if bad:
        print("FAIL:", ", ".join(bad), file=sys.stderr)
        return 1
    print("PASS: frozen Phase A records verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
