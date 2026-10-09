"""Verify this review-artifact distribution without API calls or writes."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {'.git', '.venv', '__pycache__'}


def included(path):
    parts = path.relative_to(ROOT).parts
    return not (IGNORED_PARTS.intersection(parts) or path.suffix in {'.pyc', '.pyo'})


def main():
    manifest = json.loads((ROOT / 'MANIFEST-SHA256.json').read_text())
    errors = []
    for name, expected in manifest.items():
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT.resolve()):
            errors.append('Unsafe path: ' + name)
        elif path.is_symlink() or not path.is_file():
            errors.append('Missing or non-regular file: ' + name)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append('Hash mismatch: ' + name)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and included(p)}
    extras = actual - set(manifest) - {'MANIFEST-SHA256.json'}
    errors.extend('Unexpected file: ' + name for name in sorted(extras))
    if errors:
        print('FAIL: ' + '; '.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(manifest)} distributed files match SHA-256 and inventory')
    print('No model calls, writes or scientific-validity claim are made by this check')
    return 0


if __name__ == '__main__':
    sys.exit(main())
