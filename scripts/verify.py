#!/usr/bin/env python3
"""Verify this repository snapshot without executing any skill."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    manifest = json.loads((root / 'catalog/files.sha256.json').read_text(encoding='utf-8'))
    failures = []
    for relative, expected in manifest['files'].items():
        p = root / relative
        if not p.is_file() or p.is_symlink():
            failures.append(relative + ': missing or symlink')
        elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            failures.append(relative + ': checksum mismatch')
    skills = json.loads((root / 'catalog/skills.json').read_text(encoding='utf-8'))
    ids = [s['id'] for s in skills['skills']]
    if len(ids) != len(set(ids)) or len(ids) != skills['count']:
        failures.append('catalog: duplicate ids or wrong count')
    for skill in skills['skills']:
        if skill['status'] == 'source-included':
            path = root / skill['path'] / 'SKILL.md'
            if not path.is_file():
                failures.append(skill['id'] + ': missing SKILL.md')
            elif hashlib.sha256(path.read_bytes()).hexdigest() != skill['source']['original_skill_sha256']:
                failures.append(skill['id'] + ': changed original SKILL.md')
    if failures:
        raise RuntimeError('\n'.join(failures))
    return len(manifest['files']), len(ids)


if __name__ == '__main__':
    try:
        files, skills = verify()
        print(f'PASS: {files} files, {skills} catalog entries; all checksums match.')
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
