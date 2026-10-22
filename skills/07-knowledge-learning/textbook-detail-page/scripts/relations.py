"""在抽取结果上计算两类关系（启发式，属于“AI 预生成，待编辑审核”）：
1. 支撑：同一任务内，知识点 → 技能点（评价标准条目），按共有的有区分度的词片段判断；
2. 关联：跨项目的知识点，按共有的有区分度的词片段判断。
用法：python3 -I relations.py cap.json out.json
"""
import sys, json, re, math
from collections import Counter

STOP = set('老年 年人 照护 护理 能够 能力 规范 正确 准确 完成 进行 实施 指导 相关 常见 主要 方法 要点 基本 内容 情况 老人 疾病 健康 管理 评估 记录 合理 及时 具体 明确 一般 其他 注意 事项 原则 措施 询问 掌握 了解 熟悉 识别 判断 分析 制订 制定 方案 计划 能对 能根 根据 结合 并能 能按 能识 能正 能规 能准 能完 能运 能指 能及 能制 能结 能与 能在 能说 能列 并且 以及 包括 采用 使用 要求 标准 过程 体现 操作 团队 协作 沟通 人文 关怀 尊重 安全 意识 职业 素养 信息 资料'.split())


def grams(text, n):
    text = re.sub(r'[^一-鿿A-Za-z0-9]', ' ', text)
    out = set()
    for part in text.split():
        for i in range(len(part) - n + 1):
            g = part[i:i + n]
            if n == 2 and g in STOP:
                continue
            if re.search(r'[的与及和之其对在为或并等中]', g) or '老年' in g or '年人' in g or '照护' in g or g[:2] in STOP or g[-2:] in STOP:
                continue
            out.add(g)
    return out


def main():
    cap = json.load(open(sys.argv[1]))
    # 文档频率：以“任务内每一条技能点 / 每个知识点”为文档
    docs = []
    for p in cap:
        for t in p['tasks']:
            for g in t['skills']:
                for it in g['items']:
                    docs.append(grams(it['text'], 2) | grams(it['text'], 3))
            for k in t['knowledge']:
                docs.append(grams(k['title'] + ' ' + ' '.join(k['subs']), 2) | grams(k['title'], 3))
    df = Counter(g for d in docs for g in d)
    N = len(docs)
    idf = lambda g: math.log(N / (1 + df[g]))

    def key(g):
        return idf(g) > 2.6  # 出现在不足约 7% 的条目中

    nsup = 0
    for p in cap:
        for t in p['tasks']:
            links = []
            for ki, k in enumerate(t['knowledge']):
                kg = {g for g in (grams(k['title'] + ' ' + ' '.join(k['subs']), 2) | grams(k['title'] + ' ' + ' '.join(k['subs']), 3)) if key(g)}
                flat = [(gi, ii, it) for gi, g in enumerate(t['skills']) for ii, it in enumerate(g['items'])]
                scored = []
                for gi, ii, it in flat:
                    sg = grams(it['text'], 2) | grams(it['text'], 3)
                    common = kg & sg
                    if not common:
                        continue
                    sc = sum(idf(g) for g in common)
                    soft = re.search(r'素养|人文|职业|团队|协作|沟通|态度|伦理', t['skills'][gi]['dim'])
                    if sc >= 6 or (not soft and max(idf(g) for g in common) >= 3.4):
                        scored.append((sc, gi, ii, max(common, key=len)))
                scored.sort(reverse=True)
                for sc, gi, ii, term in scored[:3]:
                    links.append([ki, gi, ii, term])
            t['support'] = links
            nsup += len(links)
    # 跨项目关联：知识点标题之间
    allk = [(p['n'], ti, ki, k['title']) for p in cap for ti, t in enumerate(p['tasks']) for ki, k in enumerate(t['knowledge'])]
    kgr = [{g for g in (grams(x[3], 2) | grams(x[3], 3) | grams(x[3], 4)) if key(g)} for x in allk]
    rel = []
    for a in range(len(allk)):
        for b in range(a + 1, len(allk)):
            if allk[a][0] == allk[b][0]:
                continue
            common = kgr[a] & kgr[b]
            if not common:
                continue
            sc = sum(idf(g) for g in common)
            longest = max(common, key=len)
            if sc >= 9 and len(longest) >= 3:
                rel.append([list(allk[a][:3]), list(allk[b][:3]), longest])
    json.dump({'cap': cap, 'related': rel}, open(sys.argv[2], 'w'), ensure_ascii=False)
    print('support links', nsup, 'related', len(rel))
    for r in rel[:40]:
        a, b, term = r
        ta = cap[a[0] - 1]['tasks'][a[1]]['knowledge'][a[2]]['title']
        tb = cap[b[0] - 1]['tasks'][b[1]]['knowledge'][b[2]]['title']
        print(' P%d %s  <->  P%d %s   [%s]' % (a[0], ta, b[0], tb, term))
    for pi, ti in ((2, 0), (2, 1), (4, 2), (7, 0)):
        t = cap[pi]['tasks'][ti]
        print('--', t['title'])
        for ki, gi, ii, term in t['support']:
            print('  %s  ->  %s [%s]' % (t['knowledge'][ki]['title'], t['skills'][gi]['items'][ii]['text'][:40], term))


main()
