#!/usr/bin/env python3
"""Compare local skill folders with this repository before uploading.

Read-only: it never copies, installs, or edits anything.

Usage:
  python3 scripts/check_duplicates.py ~/.claude/skills/my-skill
  python3 scripts/check_duplicates.py ~/.codex/skills --all      # every child folder with SKILL.md
  python3 scripts/check_duplicates.py ~/.codex/skills --all --json

Result per local skill:
  IDENTICAL          same name, every file byte-identical -> do not upload
  SAME-CONTENT       SKILL.md identical to an entry with another name -> do not upload, tell the human
  VERSION-DIFFERENT  same original name, files differ -> do not overwrite; tell the human and follow
                     docs/SYNC-AND-DEDUP.md "版本不同时如何合并"
  NEW                not in the repository -> upload following docs/SYNC-AND-DEDUP.md
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ADDED_BY_REPO = {'SKILL-INFO.zh-CN.md', 'SOURCE.json'}
IGNORED = {'.DS_Store', 'LOCAL-INSTALL.json'}
IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(folder, skip_repo_files=False):
    result = {}
    for p in sorted(folder.rglob('*')):
        if any(part in IGNORED_DIRS for part in p.relative_to(folder).parts):
            continue
        if not p.is_file() or p.name in IGNORED or p.name.endswith(('.pyc', '.pyo')):
            continue
        rel = p.relative_to(folder).as_posix()
        if skip_repo_files and rel in ADDED_BY_REPO:
            continue
        result[rel] = sha(p)
    return result


def skill_name(folder):
    text = (folder / 'SKILL.md').read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'^name:\s*["\']?([^"\'\n]+)', text, re.M)
    return m.group(1).strip() if m else folder.name


def compare(folder, catalog):
    folder = folder.expanduser().resolve()
    name = skill_name(folder)
    local = file_hashes(folder)
    local_md = local.get('SKILL.md')
    out = {'local': str(folder), 'name': name, 'status': 'NEW', 'matches': []}
    for entry in catalog['skills']:
        same_name = name in (entry['name'], entry['install_name'])
        same_md = local_md == entry['source'].get('original_skill_sha256')
        if not (same_name or same_md):
            continue
        match = {'id': entry['id'], 'path': entry['path'], 'status': entry['status']}
        if entry['status'] != 'source-included':
            match['result'] = 'IDENTICAL' if same_md else 'VERSION-DIFFERENT'
            match['note'] = 'catalog-only entry: only SKILL.md hash recorded'
        else:
            repo = file_hashes(ROOT / entry['path'], skip_repo_files=True)
            diff = sorted(k for k in set(repo) | set(local) if repo.get(k) != local.get(k))
            if not diff:
                match['result'] = 'IDENTICAL'
            elif same_name:
                match['result'] = 'VERSION-DIFFERENT'
                match['only_local'] = [k for k in diff if k not in repo]
                match['only_repo'] = [k for k in diff if k not in local]
                match['changed'] = [k for k in diff if k in repo and k in local]
            else:
                match['result'] = 'SAME-CONTENT'
        out['matches'].append(match)
    results = {m['result'] for m in out['matches']}
    for status in ('IDENTICAL', 'SAME-CONTENT', 'VERSION-DIFFERENT'):
        if status in results:
            out['status'] = status
            break
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('paths', nargs='+', type=Path)
    ap.add_argument('--all', action='store_true', help='treat each path as a parent folder of skills')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    catalog = json.loads((ROOT / 'catalog/skills.json').read_text(encoding='utf-8'))
    folders = []
    for p in args.paths:
        p = p.expanduser()
        if args.all:
            folders += sorted(x for x in p.iterdir() if (x / 'SKILL.md').is_file())
        elif (p / 'SKILL.md').is_file():
            folders.append(p)
        else:
            print(f'skip (no SKILL.md): {p}', file=sys.stderr)
    reports = [compare(f, catalog) for f in folders]
    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return
    for r in reports:
        ids = ', '.join(f"{m['id']}={m['result']}" for m in r['matches']) or '-'
        print(f"{r['status']:18} {r['name']:40} {ids}")
        for m in r['matches']:
            if m.get('result') == 'VERSION-DIFFERENT' and 'changed' in m:
                print(f"    changed={m['changed'][:6]} only_local={m['only_local'][:6]} only_repo={m['only_repo'][:6]}")
    counts = {}
    for r in reports:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print('SUMMARY:', ', '.join(f'{k}={v}' for k, v in sorted(counts.items())))


if __name__ == '__main__':
    main()
