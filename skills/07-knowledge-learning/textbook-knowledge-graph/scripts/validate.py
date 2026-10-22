#!/usr/bin/env python3
"""校验 kg.json：字段、引用完整性、无环、冗余边、与教材编排顺序的冲突、覆盖率。

用法：
  python3 scripts/validate.py kg.json                 # 有错误时退出码为 1
  python3 scripts/validate.py kg.json --book book.json  # 另查每个原知识点是否都被节点覆盖
  python3 scripts/validate.py kg.json --strict        # 警告也算失败（交付前用）
  python3 scripts/validate.py kg.json --fix-redundant # 删除冗余边（只删 status 为 ai 的）并写回

冗余边按强度判断：软边只要有别的路径可达就算冗余；硬边只有存在“全由硬边组成”的其他路径时才算冗余，
避免删掉一条硬依赖后只剩软路径。
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kglib import load, save, TYPES, STRENGTHS, STATUS, adjacency, find_cycle, ancestors, unit_of


def redundant_edges(kg, ids):
    prereqs, _ = adjacency(kg)
    hard_pre, _ = adjacency(kg, include_soft=False)
    direct = {}
    for e in kg.get('edges', []):
        if e.get('status') != 'rejected':
            direct.setdefault(e['topicId'], {})[e['prerequisiteId']] = e
    out = []
    for t, ps in direct.items():
        for p, e in ps.items():
            others = [o for o in ps if o != p]
            if e.get('strength') == 'hard':
                hit = any(ps[o].get('strength') == 'hard' and p in ancestors(o, hard_pre) for o in others)
            else:
                hit = any(p in ancestors(o, prereqs) for o in others)
            if hit:
                out.append(e)
    return out

ID_RE = re.compile(r'^kp_[A-Za-z0-9_]+$')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kg')
    ap.add_argument('--book')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--fix-redundant', action='store_true')
    a = ap.parse_args()
    kg = load(a.kg)
    errors, warns = [], []
    E, W = errors.append, warns.append

    nodes = kg.get('nodes', [])
    byid = {}
    for n in nodes:
        i = n.get('id')
        if not isinstance(i, str) or not ID_RE.match(i):
            E(f'节点 id 不合规：{i!r}（应为 kp_ 开头，字母数字下划线）')
            continue
        if i in byid:
            E(f'节点 id 重复：{i}')
        byid[i] = n
        tag = f'{i}「{n.get("name")}」'
        if not n.get('name'):
            E(f'{tag} 缺 name')
        if n.get('type') not in TYPES:
            E(f'{tag} type 不合规：{n.get("type")!r}（取 {"/".join(TYPES)}）')
        d = n.get('description') or ''
        if not d:
            E(f'{tag} 缺 description')
        elif len(d) > 120:
            W(f'{tag} description {len(d)} 字，超过 120 字，可能不是一个“微知识点”，考虑拆分')
        ev = n.get('evidence') or []
        if not isinstance(ev, list) or not ev:
            E(f'{tag} 缺 evidence（达标证据）')
        elif len(ev) > 4:
            W(f'{tag} evidence {len(ev)} 条，超过 4 条，考虑拆分节点')
        if not n.get('assessmentPrompt'):
            W(f'{tag} 缺 assessmentPrompt（检测问题）')
        if unit_of(n) is None:
            W(f'{tag} 缺 unit（所属项目 / 章序号），无法检查编排顺序')
        if n.get('status', 'ai') not in STATUS:
            E(f'{tag} status 不合规：{n.get("status")!r}')

    seen = set()
    for e in kg.get('edges', []):
        t, p = e.get('topicId'), e.get('prerequisiteId')
        tag = f'边 {p} → {t}'
        if t not in byid:
            E(f'{tag}：topicId 不存在')
        if p not in byid:
            E(f'{tag}：prerequisiteId 不存在')
        if t == p:
            E(f'{tag}：自己依赖自己')
        if e.get('strength') not in STRENGTHS:
            E(f'{tag}：strength 应为 hard / soft')
        if not (e.get('reason') or '').strip():
            E(f'{tag}：缺 reason')
        if e.get('status', 'ai') not in STATUS:
            E(f'{tag}：status 不合规')
        if (t, p) in seen:
            E(f'{tag}：重复')
        if (p, t) in seen:
            E(f'{tag}：与反向边同时存在')
        seen.add((t, p))

    ids = list(byid)
    prereqs, unlocks = adjacency(kg)
    cyc = find_cycle(ids, prereqs)
    if cyc:
        names = ' → '.join(f'{c}「{byid[c]["name"]}」' for c in cyc if c in byid)
        E(f'存在循环依赖：{names}')
    else:
        # 冗余边（按强度）：p 已可经 t 的其他先修间接到达
        red = redundant_edges(kg, ids)
        if a.fix_redundant and red:
            drop = {(e['topicId'], e['prerequisiteId']) for e in red if e.get('status', 'ai') == 'ai'}
            kg['edges'] = [e for e in kg['edges'] if (e['topicId'], e['prerequisiteId']) not in drop]
            save(kg, a.kg)
            print(f'已删除 {len(drop)} 条冗余边并写回 {a.kg}')
            red = [e for e in red if (e['topicId'], e['prerequisiteId']) not in drop]
            prereqs, unlocks = adjacency(kg)
        for e in red:
            W(f'冗余边 {e["prerequisiteId"]} → {e["topicId"]}（{e.get("strength")}）：已可经其他先修间接到达，只保留直接先修')
        # 编排顺序：先修出现在更靠后的项目
        for e in kg.get('edges', []):
            if e.get('status') == 'rejected':
                continue
            t, p = byid.get(e['topicId']), byid.get(e['prerequisiteId'])
            if t and p and unit_of(t) and unit_of(p) and unit_of(p) > unit_of(t):
                W(f'顺序冲突（{e.get("strength")}）：{p["id"]}「{p["name"]}」在项目 {unit_of(p)}，'
                    f'却是项目 {unit_of(t)} 的 {t["id"]}「{t["name"]}」的先修——边方向可能反了，或教材需要在前面补提示')

    isolated = [i for i in ids if not prereqs.get(i) and not unlocks.get(i)]
    if isolated and len(ids) > 1:
        W(f'{len(isolated)} 个孤立节点（没有任何先修或后继）：' + '、'.join(byid[i]['name'] for i in isolated[:12]) + ('…' if len(isolated) > 12 else ''))

    if a.book:
        book = load(a.book)
        cap = book.get('capability', book)
        covered = {tuple(an) for n in nodes for an in n.get('anchors', [])}
        units = {n.get('unit') for n in nodes}
        missing = []
        for p in cap.get('projects', []):
            if p['n'] not in units:
                continue
            for ti, t in enumerate(p['tasks']):
                for ki, k in enumerate(t.get('know', [])):
                    if (p['n'], ti, ki) not in covered:
                        missing.append(f'P{p["n"]} 任务{ti + 1}「{k["t"]}」')
        if missing:
            W(f'{len(missing)} 个原知识点没有对应节点：' + '；'.join(missing[:10]) + ('…' if len(missing) > 10 else ''))

    hard = sum(1 for e in kg.get('edges', []) if e.get('strength') == 'hard' and e.get('status') != 'rejected')
    soft = sum(1 for e in kg.get('edges', []) if e.get('strength') == 'soft' and e.get('status') != 'rejected')
    print(f'节点 {len(nodes)} · 先修边 {hard + soft}（硬 {hard} / 软 {soft}）· 错误 {len(errors)} · 警告 {len(warns)}')
    for x in errors:
        print('  ✗', x)
    for x in warns:
        print('  !', x)
    if errors or (a.strict and warns):
        sys.exit(1)
    print('✓ 通过' + ('（有警告，交付前请处理或说明）' if warns else ''))


if __name__ == '__main__':
    main()
