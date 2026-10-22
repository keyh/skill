#!/usr/bin/env python3
"""Install selected skill files. Never run a skill, download dependencies, or change AI settings."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

from verify import ROOT, verify


def present(path):
    return path.exists() or path.is_symlink()


def package_matches(source, destination):
    """Allow reusing a previously copied bundle only if every file is identical."""
    if not destination.is_dir() or destination.is_symlink():
        return False
    source_files = {p.relative_to(source) for p in source.rglob('*') if p.is_file()}
    target_files = {p.relative_to(destination) for p in destination.rglob('*') if p.is_file()}
    if source_files != target_files:
        return False
    return all(not (destination / p).is_symlink() and
               hashlib.sha256((source / p).read_bytes()).digest() ==
               hashlib.sha256((destination / p).read_bytes()).digest()
               for p in source_files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List all catalog entries')
    parser.add_argument('--skill', nargs='+', default=[], metavar='ID')
    parser.add_argument('--category', action='append', default=[])
    parser.add_argument('--preset', action='append', default=[])
    parser.add_argument('--dest', type=Path, help='The target AI skill directory; explicit path required')
    parser.add_argument('--dry-run', action='store_true', help='Validate and preview without writing')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog/skills.json').read_text(encoding='utf-8'))
    entries = {x['id']: x for x in catalog['skills']}
    presets = json.loads((ROOT / 'catalog/presets.json').read_text(encoding='utf-8'))
    if args.list:
        for item in catalog['skills']:
            print(f'{item["id"]}\t{item["title_zh"]}\t{item["status"]}\t{item["portability"]}')
        return
    selected_ids = list(args.skill)
    for name in args.preset:
        if name not in presets:
            parser.error('Unknown preset: ' + name)
        selected_ids.extend(presets[name]['skills'])
    for cat in args.category:
        if cat not in catalog['categories']:
            parser.error('Unknown category: ' + cat)
        selected_ids.extend(x['id'] for x in catalog['skills'] if x['category'] == cat)
    selected_ids = list(dict.fromkeys(selected_ids))
    if not selected_ids or args.dest is None:
        parser.error('Select --skill / --preset / --category and provide --dest. Use --list to browse.')
    if any(x not in entries for x in selected_ids):
        parser.error('Unknown skill ids: ' + ', '.join(x for x in selected_ids if x not in entries))
    selected = [entries[x] for x in selected_ids]
    blocked = [x['id'] for x in selected if x['status'] != 'source-included']
    if blocked:
        parser.error('Catalog only; use the original platform: ' + ', '.join(blocked))
    names = [x['install_name'] for x in selected]
    if len(names) != len(set(names)):
        parser.error('Selected variants share original skill names. Choose one variant per name.')
    verify()
    dest = args.dest.expanduser().resolve()
    if dest == ROOT or ROOT in dest.parents:
        parser.error('Install outside this repository to keep the snapshot unchanged.')
    for item in selected:
        if present(dest / item['install_name']):
            parser.error('Refusing to overwrite existing skill: ' + str(dest / item['install_name']))
    bundles = sorted(set(x['bundle_path'] for x in selected if x['bundle_path']))
    if bundles and (dest / '.skill-bundles').is_symlink():
        parser.error('Refusing a symlink bundle storage directory.')
    for bundle in bundles:
        target = dest / '.skill-bundles' / Path(bundle).name
        if present(target) and not package_matches(ROOT / bundle, target):
            parser.error('Existing bundle differs. Use a separate destination: ' + str(target))
    for item in selected:
        print(f'{item["id"]} -> {dest / item["install_name"]}')
        if item['bundle_path']:
            print('  Entire plugin skill bundle will be retained; the selected entry is linked to it.')
        print('  ' + item['dependencies_zh'])
    if args.dry_run:
        print(f'DRY RUN: {len(selected)} selected skills. No files or settings changed.')
        return
    dest.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.skill-install-', dir=str(dest)))
    created = []
    try:
        # Prepare all files before publishing. Plugin bundles retain sibling and shared references.
        for bundle in bundles:
            target = dest / '.skill-bundles' / Path(bundle).name
            if not present(target):
                shutil.copytree(ROOT / bundle, staging / 'bundles' / Path(bundle).name)
        for item in selected:
            if not item['bundle_path']:
                shutil.copytree(ROOT / item['path'], staging / 'entries' / item['install_name'])
            else:
                target = dest / '.skill-bundles' / Path(item['bundle_path']).name / 'skills' / item['install_name']
                link = staging / 'entries' / item['install_name']
                link.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(str(target), str(link), target_is_directory=True)
        for bundle in bundles:
            target = dest / '.skill-bundles' / Path(bundle).name
            pending = staging / 'bundles' / Path(bundle).name
            if pending.exists():
                target.parent.mkdir(exist_ok=True)
                if present(target):
                    raise RuntimeError('Destination appeared during install: ' + str(target))
                os.rename(str(pending), str(target))
                created.append(target)
        for item in selected:
            target = dest / item['install_name']
            if present(target):
                raise RuntimeError('Destination appeared during install: ' + str(target))
            os.rename(str(staging / 'entries' / item['install_name']), str(target))
            created.append(target)
        for item in selected:
            installed = dest / item['install_name'] / 'SKILL.md'
            if hashlib.sha256(installed.read_bytes()).hexdigest() != item['source']['original_skill_sha256']:
                raise RuntimeError('Installed checksum mismatch: ' + item['id'])
    except Exception:
        for path in reversed(created):
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    print(f'INSTALLED: {len(selected)} skills. No hooks, accounts, MCP servers, or dependencies enabled.')
    print('Reload or restart your AI tool if required. Platform-specific tools need separate setup.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
