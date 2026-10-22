#!/usr/bin/env python3
"""从详情页 skill 的 book.json（或单独的 capability.json）生成知识图谱骨架 kg.json。

每个【任务准备】里的知识点生成一个候选节点：带出处（anchors）、细目（sub）、所在任务的技能点和流程，
以及原有的关键词关联（hints），供模型补写字段、合并拆分、建立先修关系。

用法：
  python3 scripts/from_capability.py book.json -o kg.json
  python3 scripts/from_capability.py book.json -o kg.json --units 1-4      # 只取部分项目（试跑或分批）
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kglib import load, save


def parse_units(spec, total):
    if not spec:
        return list(range(1, total + 1))
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('book')
    ap.add_argument('-o', '--out', default='kg.json')
    ap.add_argument('--units', default='', help='项目序号，如 1-4 或 1,3,5')
    a = ap.parse_args()

    book = load(a.book)
    cap = book.get('capability', book)  # 也接受单独的 capability.json
    if not cap or 'projects' not in cap:
        sys.exit('没有找到 capability.projects；本工具需要详情页 skill 抽取出的能力结构。')
    projects = cap['projects']
    units = set(parse_units(a.units, len(projects)))
    stage_of = {}
    for name, ns, color in book.get('stages', []):
        for n in ns:
            stage_of[n] = name
    short = book.get('short', [])

    nodes, hints = [], []
    seq = 0
    for p in projects:
        if p['n'] not in units:
            continue
        for ti, t in enumerate(p['tasks']):
            skills = [d['d'] for d in t.get('skills', [])]
            steps = [s['t'] for s in t.get('steps', [])]
            for ki, k in enumerate(t.get('know', [])):
                seq += 1
                nodes.append({
                    'id': f"kp_p{p['n']:02d}_{ti + 1}{ki + 1:02d}",
                    'name': k['t'],
                    'type': None,
                    'unit': p['n'],
                    'stage': stage_of.get(p['n']),
                    'domain': short[p['n'] - 1] if len(short) >= p['n'] else p['title'],
                    'description': None,
                    'evidence': [],
                    'assessmentPrompt': None,
                    'standards': [],
                    'sub': k.get('s', []),
                    'anchors': [[p['n'], ti, ki]],
                    'context': {'task': t['title'], 'skills': skills, 'steps': steps, 'cert': t.get('certTags', [])},
                    'status': 'ai',
                })
    keep = {(x['anchors'][0][0], x['anchors'][0][1], x['anchors'][0][2]): x['id'] for x in nodes}
    for a_, b_, kw in cap.get('related', []):
        ka, kb = tuple(a_), tuple(b_)
        if ka in keep and kb in keep:
            hints.append({'a': keep[ka], 'b': keep[kb], 'keyword': kw})

    kg = {
        'version': 'kg-1',
        'book': {k: book.get(k) for k in ('id', 'title', 'major', 'level', 'edition') if book.get(k)},
        'units': [{'n': p['n'], 'title': p['title'], 'short': short[p['n'] - 1] if len(short) >= p['n'] else None,
                   'stage': stage_of.get(p['n'])} for p in projects if p['n'] in units],
        'stages': book.get('stages', []),
        'nodes': nodes,
        'edges': [],
        'hints': hints,
        'clusters': [],
        'provenance': {
            'source': os.path.basename(a.book),
            'note': '节点骨架由 from_capability.py 生成；type/description/evidence/assessmentPrompt/edges 待补写，全部为 AI 预生成，须编辑审核。',
        },
    }
    save(kg, a.out)
    print(f'{len(nodes)} 个候选节点，{len(hints)} 条原关键词关联（hints）→ {a.out}')


if __name__ == '__main__':
    main()
