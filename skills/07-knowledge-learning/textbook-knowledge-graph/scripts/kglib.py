"""Shared helpers for the textbook knowledge graph scripts (stdlib only)."""
import json
from collections import defaultdict, deque

TYPES = {
    'CONCEPTUAL': '概念',
    'PROCEDURAL': '操作',
    'REPRESENTATIONAL': '识读',
    'LANGUAGE': '术语',
    'META': '素养',
}
STRENGTHS = {'hard', 'soft'}
STATUS = {'ai', 'reviewed', 'confirmed', 'rejected'}


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')


def live_edges(kg, include_soft=True):
    """Edges that count: not rejected; optionally hard only."""
    out = []
    for e in kg.get('edges', []):
        if e.get('status') == 'rejected':
            continue
        if not include_soft and e.get('strength') != 'hard':
            continue
        out.append(e)
    return out


def adjacency(kg, include_soft=True):
    """prereqs[t] = set of direct prerequisites of t; unlocks[p] = set of topics p directly unlocks."""
    prereqs, unlocks = defaultdict(set), defaultdict(set)
    for e in live_edges(kg, include_soft):
        prereqs[e['topicId']].add(e['prerequisiteId'])
        unlocks[e['prerequisiteId']].add(e['topicId'])
    return prereqs, unlocks


def find_cycle(ids, prereqs):
    """Return one cycle as a list of ids, or None."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    parent = {}
    for start in ids:
        if color[start] != WHITE:
            continue
        stack = [(start, iter(sorted(prereqs.get(start, ()))))]
        color[start] = GREY
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[node] = BLACK
                stack.pop()
                continue
            if nxt not in color:
                continue
            if color[nxt] == GREY:
                cyc = [nxt, node]
                p = node
                while p != nxt and p in parent:
                    p = parent[p]
                    cyc.append(p)
                return list(reversed(cyc))
            if color[nxt] == WHITE:
                parent[nxt] = node
                color[nxt] = GREY
                stack.append((nxt, iter(sorted(prereqs.get(nxt, ())))))
    return None


def ancestors(node, prereqs):
    seen, q = set(), deque(prereqs.get(node, ()))
    while q:
        x = q.popleft()
        if x in seen:
            continue
        seen.add(x)
        q.extend(prereqs.get(x, ()))
    return seen


def descendants(node, unlocks):
    return ancestors(node, unlocks)


def topo_order(ids, prereqs, key=None):
    """Kahn's algorithm; ties broken by key (e.g. book order). Assumes a DAG."""
    indeg = {i: 0 for i in ids}
    for t in ids:
        indeg[t] = len([p for p in prereqs.get(t, ()) if p in indeg])
    ready = sorted([i for i in ids if indeg[i] == 0], key=key)
    out = []
    unlocks = defaultdict(set)
    for t in ids:
        for p in prereqs.get(t, ()):
            if p in indeg:
                unlocks[p].add(t)
    while ready:
        n = ready.pop(0)
        out.append(n)
        for m in unlocks.get(n, ()):
            indeg[m] -= 1
            if indeg[m] == 0:
                ready.append(m)
        ready.sort(key=key)
    return out


def depth(ids, prereqs):
    """Longest prerequisite chain ending at each node (roots = 0)."""
    order = topo_order(ids, prereqs)
    d = {}
    for n in order:
        ps = [p for p in prereqs.get(n, ()) if p in d]
        d[n] = 1 + max(d[p] for p in ps) if ps else 0
    return d


def pagerank(ids, prereqs, damping=0.85, iters=60):
    """Importance flows from a topic to its prerequisites: foundations that many topics rest on score high."""
    n = len(ids)
    if n == 0:
        return {}
    rank = {i: 1.0 / n for i in ids}
    out_deg = {i: len([p for p in prereqs.get(i, ()) if p in rank]) for i in ids}
    for _ in range(iters):
        new = {i: (1 - damping) / n for i in ids}
        sink = sum(rank[i] for i in ids if out_deg[i] == 0)
        for i in ids:
            new[i] += damping * sink / n
        for t in ids:
            if out_deg[t]:
                share = damping * rank[t] / out_deg[t]
                for p in prereqs.get(t, ()):
                    if p in new:
                        new[p] += share
        rank = new
    top = max(rank.values())
    return {i: round(v / top, 4) for i, v in rank.items()}


def weighted_pagerank(kg, ids, soft_weight=0.4, damping=0.85, iters=60):
    """Like pagerank(), but a soft edge passes only soft_weight of the importance a hard edge passes."""
    n = len(ids)
    if n == 0:
        return {}
    idset = set(ids)
    out = {i: [] for i in ids}
    for e in live_edges(kg):
        t, p = e['topicId'], e['prerequisiteId']
        if t in idset and p in idset:
            out[t].append((p, 1.0 if e.get('strength') == 'hard' else soft_weight))
    rank = {i: 1.0 / n for i in ids}
    for _ in range(iters):
        new = {i: (1 - damping) / n for i in ids}
        sink = sum(rank[i] for i in ids if not out[i])
        for i in ids:
            new[i] += damping * sink / n
        for t in ids:
            tot = sum(w for _, w in out[t])
            for p, w in out[t]:
                new[p] += damping * rank[t] * w / tot
        rank = new
    top = max(rank.values())
    return {i: round(v / top, 4) for i, v in rank.items()}


def unit_of(node):
    u = node.get('unit')
    return u if isinstance(u, int) else None
