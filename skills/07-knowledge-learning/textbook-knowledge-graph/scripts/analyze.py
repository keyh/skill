#!/usr/bin/env python3
"""分析 kg.json：中心度、深度、先修闭包、重点/难点候选、学习路径；导出审核表和可视化页面。

用法：
  python3 scripts/analyze.py kg.json --write            # 把 centrality / depth / unlocks 写回 kg.json
  python3 scripts/analyze.py kg.json --report report.md  # 生成分析报告（重点、难点、桥梁知识点、各项目概况）
  python3 scripts/analyze.py kg.json --path kp_p03_101   # 学会这个知识点之前要按什么顺序学什么（可给多个 id）
  python3 scripts/analyze.py kg.json --frontier kp_p01_101 kp_p03_101   # 已掌握这些，现在可以学什么（带理由）
  python3 scripts/analyze.py kg.json --frontier mastered.txt            # 每行一个 id 的已掌握清单
  python3 scripts/analyze.py kg.json --review review.csv # 导出边与节点审核表（Excel 可直接打开）
  python3 scripts/analyze.py kg.json --viewer graph.html # 用 assets/kg-viewer.html 生成可交互的 3D 图谱页面
"""
import argparse, csv, json, os, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kglib import load, save, TYPES, adjacency, find_cycle, ancestors, descendants, topo_order, depth, weighted_pagerank, unit_of

# 口径说明：软边表示“先学会更顺”，不能沿着它一路传递——软边连起来会串成几十层的“链”，
# 让综合性知识点看起来要先学上百个知识点。所以层级、先修闭包、难点、学习路径只按硬边算；
# 软先修只看直接的一层；中心度把软边按 0.4 的权重计入。


def compute(kg):
    nodes = {n['id']: n for n in kg['nodes']}
    ids = list(nodes)
    prereqs, unlocks = adjacency(kg)
    if find_cycle(ids, prereqs):
        sys.exit('图里有循环依赖，先运行 validate.py 修正。')
    hpre, hun = adjacency(kg, include_soft=False)
    soft_children = defaultdict(set)
    for e in kg['edges']:
        if e.get('status') != 'rejected' and e.get('strength') == 'soft':
            soft_children[e['prerequisiteId']].add(e['topicId'])
    dep = depth(ids, hpre)
    pr = weighted_pagerank(kg, ids)
    m = {}
    for i in ids:
        anc, desc = ancestors(i, hpre), descendants(i, hun)
        reach = desc | soft_children.get(i, set())
        cross = {unit_of(nodes[d]) for d in reach if unit_of(nodes[d])} - {unit_of(nodes[i])}
        m[i] = {'depth': dep[i], 'centrality': pr[i], 'ancestors': len(anc), 'unlocks': len(desc),
                'softPrereqs': len(prereqs.get(i, set()) - hpre.get(i, set())),
                'softChildren': len(soft_children.get(i, set())),
                'crossUnits': sorted(x for x in cross if x)}
    return nodes, prereqs, unlocks, m


def order_key(nodes):
    def k(i):
        n = nodes[i]
        a = (n.get('anchors') or [[999, 999, 999]])[0]
        return (n.get('unit') or 999, a[1] if len(a) > 1 else 0, a[2] if len(a) > 2 else 0, i)
    return k


def report(kg, nodes, prereqs, unlocks, m, out):
    L = [f"# 知识先修图谱分析：{kg.get('book', {}).get('title', '')}", '']
    hard = sum(1 for e in kg['edges'] if e.get('strength') == 'hard' and e.get('status') != 'rejected')
    soft = sum(1 for e in kg['edges'] if e.get('strength') == 'soft' and e.get('status') != 'rejected')
    st = Counter(n.get('status', 'ai') for n in kg['nodes'])
    L.append(f"- 节点 {len(nodes)}，先修边 {hard + soft}（硬 {hard} / 软 {soft}）；按硬依赖，最长先修链 {max((v['depth'] for v in m.values()), default=0) + 1} 层")
    L.append('- 口径：层级、先修数量、难点、学习路径只按硬依赖计算；软依赖只看直接一层（建议先看）；中心度把软依赖按 0.4 的权重计入。')
    L.append('- 类型：' + '、'.join(f'{TYPES.get(t, t)} {c}' for t, c in Counter(n.get('type') for n in kg['nodes']).most_common()))
    L.append('- 审核状态：' + '、'.join(f'{k} {v}' for k, v in st.items()) + '（ai = AI 预生成待审核）')
    L.append('')
    name = lambda i: f"{nodes[i]['name']}（P{nodes[i].get('unit', '?')}）"

    L += ['## 重点候选：被最多后续知识依赖的基础知识点', '', '中心度高，说明很多后续内容建立在它上面；适合作为重点讲透、配套资源优先建设。', '']
    for i in sorted(m, key=lambda x: -m[x]['centrality'])[:12]:
        parts = []
        if m[i]['unlocks']:
            parts.append(f"是 {m[i]['unlocks']} 个知识点的必备前置（直接或间接）")
        if m[i]['softChildren']:
            parts.append(f"被 {m[i]['softChildren']} 个知识点列为建议先看")
        if m[i]['crossUnits']:
            parts.append(f"涉及 {len(m[i]['crossUnits'])} 个其他项目")
        L.append(f"- {name(i)}：中心度 {m[i]['centrality']}；" + '，'.join(parts))
    L += ['', '## 难点候选：硬性前置要求最多、先修链最长的知识点', '', '学它之前必须掌握的东西最多；适合安排复习提示、拆分讲解或数字化支架。', '']
    for i in sorted(m, key=lambda x: (-m[x]['ancestors'], -m[x]['depth']))[:12]:
        L.append(f"- {name(i)}：必须先掌握 {m[i]['ancestors']} 个知识点，链长 {m[i]['depth'] + 1} 层" + (f"，另有 {m[i]['softPrereqs']} 个建议先看" if m[i]['softPrereqs'] else ''))
    L += ['', '## 桥梁知识点：支撑其他项目的知识', '', '学生在后面项目遇到困难时，最可能要回到这些知识点；页面上可以做“回看”入口。', '']
    for i in sorted([x for x in m if m[x]['crossUnits']], key=lambda x: -len(m[x]['crossUnits']))[:12]:
        L.append(f"- {name(i)} → 项目 {'、'.join(map(str, m[i]['crossUnits']))}")
    L += ['', '## 各项目概况', '', '| 项目 | 节点 | 项目内先修边 | 依赖前面项目的边 | 被后面项目依赖的边 |', '|---|---|---|---|---|']
    units = sorted({n.get('unit') for n in kg['nodes'] if n.get('unit')})
    for u in units:
        nn = [i for i in nodes if nodes[i].get('unit') == u]
        inner = back = fwd = 0
        for e in kg['edges']:
            if e.get('status') == 'rejected':
                continue
            tu, pu = nodes[e['topicId']].get('unit'), nodes[e['prerequisiteId']].get('unit')
            if tu == u and pu == u:
                inner += 1
            elif tu == u and pu != u:
                back += 1
            elif pu == u and tu != u:
                fwd += 1
        title = next((x.get('title') for x in kg.get('units', []) if x.get('n') == u), '')
        L.append(f'| P{u} {title} | {len(nn)} | {inner} | {back} | {fwd} |')
    conflicts = [e for e in kg['edges'] if e.get('status') != 'rejected'
                 and (nodes[e['prerequisiteId']].get('unit') or 0) > (nodes[e['topicId']].get('unit') or 0)]
    if conflicts:
        L += ['', '## 编排顺序提示', '', '下面的先修知识点出现在更靠后的项目里。要么关系方向有误，要么教材应在前面补一句提示或链接。', '']
        for e in conflicts:
            L.append(f"- {name(e['prerequisiteId'])} → {name(e['topicId'])}（{e['strength']}）：{e.get('reason', '')}")
    ed = kg.get('editorial') or {}
    if ed.get('repeats'):
        L += ['', '## 编辑提示：重复讲授', '', '下面的通用内容在多个项目里重复讲。图谱里已用软边把后者连到第一次讲的地方；是否合并通用部分、病种项目只留特有内容，请编辑决定。', '']
        for r in ed['repeats']:
            L.append(f"- {r['baseName']}（P{r['baseUnit']}）→ {r['repeatName']}（P{r['repeatUnit']}）")
    if ed.get('forwardUse'):
        L += ['', '## 编辑提示：先用后讲', '']
        for f_ in ed['forwardUse']:
            L.append(f"- {'、'.join(f_.get('userNames', []))}：{f_.get('note', '')}")
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('报告 →', out)


def learn_path(kg, nodes, prereqs, targets, with_soft):
    hpre, _ = adjacency(kg, include_soft=False)
    walk = prereqs if with_soft else hpre
    need = set()
    for t in targets:
        if t not in nodes:
            sys.exit(f'没有这个节点：{t}')
        need |= ancestors(t, walk) | {t}
    order = topo_order(list(need), walk, key=order_key(nodes))
    print(f"学习路径（{'硬 + 软依赖全链，通常偏长' if with_soft else '按硬依赖'}，共 {len(order)} 步）：")
    for k, i in enumerate(order, 1):
        n = nodes[i]
        mark = '★' if i in targets else ' '
        print(f"{k:>3}. {mark} [P{n.get('unit', '?')}] {n['name']}  ({i})")
    if not with_soft:
        sug = set()
        for i in need:
            sug |= prereqs.get(i, set()) - hpre.get(i, set())
        sug -= need
        if sug:
            print('建议先看（软依赖，直接一层）：' + '、'.join(f"{nodes[s]['name']}(P{nodes[s].get('unit', '?')})" for s in sorted(sug, key=order_key(nodes))))


def frontier(kg, nodes, mastered, need_soft, limit=15):
    """已掌握集合 → 现在可以学的知识点（所有硬先修都已掌握），附理由，可直接用于“解释性推荐”。"""
    unknown = [x for x in mastered if x not in nodes]
    if unknown:
        print('忽略不存在的 id：' + '、'.join(unknown))
    mastered = {x for x in mastered if x in nodes}
    pre = defaultdict(list)
    for e in kg['edges']:
        if e.get('status') != 'rejected':
            pre[e['topicId']].append(e)
    ready, blocked = [], []
    for i in sorted(nodes, key=order_key(nodes)):
        if i in mastered:
            continue
        must = [e for e in pre[i] if e['strength'] == 'hard' or need_soft]
        missing = [e for e in must if e['prerequisiteId'] not in mastered]
        (blocked if missing else ready).append((i, must, missing))
    # 推荐顺序：软先修也已掌握得多的优先，再按教材顺序；硬边稀疏时“可学”会很多，只列前 limit 个
    def soft_gap(i):
        return sum(1 for e in pre[i] if e['strength'] == 'soft' and e['prerequisiteId'] not in mastered)
    ready.sort(key=lambda x: (soft_gap(x[0]), order_key(nodes)(x[0])))
    print(f'已掌握 {len(mastered)} 个；现在可以学 {len(ready)} 个（{"硬 + 软先修都已掌握" if need_soft else "硬先修都已掌握"}），'
          f'按推荐顺序列前 {min(limit, len(ready))} 个：')
    for i, must, _ in ready[:limit]:
        why = '；'.join(f"已会「{nodes[e['prerequisiteId']]['name']}」：{e.get('reason', '')}" for e in must)
        if not why:
            soft = [nodes[e['prerequisiteId']]['name'] for e in pre[i] if e['prerequisiteId'] not in mastered]
            why = ('没有硬性先修；先学「' + '」「'.join(soft) + '」会更顺') if soft else ('没有硬性先修' if pre[i] else '起点知识，无先修')
        print(f"  · [P{nodes[i].get('unit', '?')}] {nodes[i]['name']}（{i}）— {why}")
    near = sorted(blocked, key=lambda x: len(x[2]))[:8]
    if near:
        print('只差一两步的：')
        for i, _, missing in near:
            print(f"  · {nodes[i]['name']}：还需先学 " + '、'.join(nodes[e['prerequisiteId']]['name'] for e in missing))


def review_csv(kg, nodes, m, out):
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['类别', '编号', '先修知识点', '所在项目', '→ 知识点', '所在项目', '强度', '理由 / 描述', '达标证据', '状态', '审核意见（接受 / 修改 / 删除）'])
        for e in kg['edges']:
            p, t = nodes[e['prerequisiteId']], nodes[e['topicId']]
            w.writerow(['先修关系', f"{p['id']}→{t['id']}", p['name'], p.get('unit'), t['name'], t.get('unit'),
                        '硬' if e['strength'] == 'hard' else '软', e.get('reason', ''), '', e.get('status', 'ai'), ''])
        for n in kg['nodes']:
            w.writerow(['知识点', n['id'], '', '', n['name'], n.get('unit'), TYPES.get(n.get('type'), n.get('type')),
                        n.get('description', ''), '；'.join(n.get('evidence', [])), n.get('status', 'ai'), ''])
    print('审核表 →', out)


def viewer(kg, m, out):
    tpl_path = os.path.join(HERE, '..', 'assets', 'kg-viewer.html')
    with open(tpl_path, encoding='utf-8') as f:
        tpl = f.read()
    slim = {
        'book': kg.get('book', {}), 'units': kg.get('units', []), 'stages': kg.get('stages', []),
        'nodes': [{k: n.get(k) for k in ('id', 'name', 'type', 'unit', 'stage', 'domain', 'description', 'evidence', 'assessmentPrompt', 'status')}
                  | {'depth': m[n['id']]['depth'], 'centrality': m[n['id']]['centrality']} for n in kg['nodes']],
        'edges': [{k: e.get(k) for k in ('topicId', 'prerequisiteId', 'strength', 'reason', 'status')}
                  for e in kg['edges'] if e.get('status') != 'rejected'],
    }
    data = json.dumps(slim, ensure_ascii=False).replace('</', '<\\/')
    html = tpl.replace('/*__KG_DATA__*/null', data).replace('__KG_TITLE__', (kg.get('book', {}).get('title') or '知识先修图谱'))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('图谱页面 →', out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('kg')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--report')
    ap.add_argument('--path', nargs='+')
    ap.add_argument('--with-soft', action='store_true', help='学习路径沿软依赖也一路追溯（通常会很长，只在研究关系时用）')
    ap.add_argument('--frontier', nargs='*', metavar='ID', help='已掌握的知识点 id（或一个每行一个 id 的文本文件），列出现在可以学的')
    ap.add_argument('--need-soft', action='store_true', help='计算可学范围时，软先修也要求已掌握')
    ap.add_argument('--review')
    ap.add_argument('--viewer')
    a = ap.parse_args()
    kg = load(a.kg)
    nodes, prereqs, unlocks, m = compute(kg)
    if a.write:
        for n in kg['nodes']:
            n['centrality'] = m[n['id']]['centrality']
            n['depth'] = m[n['id']]['depth']
            n['unlocks'] = m[n['id']]['unlocks']
        save(kg, a.kg)
        print('已写回 centrality / depth / unlocks →', a.kg)
    if a.report:
        report(kg, nodes, prereqs, unlocks, m, a.report)
    if a.path:
        learn_path(kg, nodes, prereqs, set(a.path), a.with_soft)
    if a.frontier is not None:
        ids = []
        for x in a.frontier:
            if os.path.isfile(x):
                with open(x, encoding='utf-8') as f:
                    ids += [l.strip() for l in f if l.strip()]
            else:
                ids.append(x)
        frontier(kg, nodes, ids, a.need_soft)
    if a.review:
        review_csv(kg, nodes, m, a.review)
    if a.viewer:
        viewer(kg, m, a.viewer)
    if not any([a.write, a.report, a.path, a.review, a.viewer, a.frontier is not None]):
        top = sorted(m, key=lambda x: -m[x]['centrality'])[:8]
        print('中心度前 8：' + '、'.join(f"{nodes[i]['name']}({m[i]['centrality']})" for i in top))
        print('更多：--report / --path / --review / --viewer，见 --help')


if __name__ == '__main__':
    main()
