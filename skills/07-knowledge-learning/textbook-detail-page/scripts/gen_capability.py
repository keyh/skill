"""把抽取与关系结果整理为能力结构数据 capability.json（页面 D.capability）。
用法：python3 -I gen_capability.py rel.json capability.json [--pending pending.txt] [--certs certs.json] [--js bookCapability.js]
- pending.txt：每行一个“项目.任务”（如 1.3），表示该任务的赛证对接说明是修订时补写、待作者确认的，不计入对接统计；
- certs.json：赛证识别规则 [[类型, 名称, 正则], …]，默认为养老照护类教材的规则，其他教材按稿件中点名的证书与赛项改写；
- --js：同时输出 Vue 工程用的 src/api/bookCapability.js。
"""
import sys, json, re, argparse

ap = argparse.ArgumentParser()
ap.add_argument('rel'); ap.add_argument('out')
ap.add_argument('--pending'); ap.add_argument('--certs'); ap.add_argument('--js')
ARGS = ap.parse_args()
PENDING = set()
if ARGS.pending:
    for line in open(ARGS.pending, encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#'):
            a, b = line.split('.')
            PENDING.add((int(a), int(b)))
STOP_SUB = set('询问 评估 措施 其他 注意事项 概述 定义 原则 方法 要点 内容 目的 意义 分类 特点 表现'.split())


def lcs(a, b):
    best = ''
    for i in range(len(a)):
        for j in range(i + 1, len(a) + 1):
            s = a[i:j]
            if len(s) <= len(best):
                continue
            if s in b:
                best = s
            else:
                break
    return best


def trim_term(t):
    t = re.sub(r'^[的与及和之、，。（）()\s]+|[的与及和之、，。（）()\s]+$', '', t)
    return t


CERTS = [
    ('赛', '技能大赛养老照护赛项', r'养老照护赛项|健康养老照护赛项|照护赛项'),
    ('证', '养老护理员', r'养老护理员'),
    ('证', '健康照护师', r'健康照护师|长期照护师'),
    ('证', '社群健康助理员', r'社群健康助理员'),
    ('标', '临床指南与专家共识', r'指南|共识'),
]
if ARGS.certs:
    CERTS = [tuple(x) for x in json.load(open(ARGS.certs, encoding='utf-8'))]


def main():
    data = json.load(open(ARGS.rel, encoding='utf-8'))
    cap, related = data['cap'], data['related']
    projects = []
    for p in cap:
        tasks = []
        for t in p['tasks']:
            know = []
            for k in t['knowledge']:
                subs, seen = [], set()
                for s in k['subs']:
                    s = s.strip(' ：:，。')
                    if len(s) < 2 or s in STOP_SUB or s in seen or s == k['title']:
                        continue
                    seen.add(s)
                    subs.append(s)
                know.append({'t': k['title'].strip(' ：:，。'), 's': subs[:8]})
            skills = [{'d': g['dim'].strip(' /'), 'v': g['total'], 'i': [[it['text'], it['score']] for it in g['items']]} for g in t['skills']]
            support = []
            for ki, gi, ii, term in t.get('support', []):
                ktext = know[ki]['t'] + ' ' + ' '.join(know[ki]['s'])
                stext = skills[gi]['i'][ii][0]
                tm = trim_term(lcs(stext, ktext)) or term
                support.append([ki, gi, ii, tm])
            cert = t.get('cert', '')
            raw_cert = cert
            quiz = bool(cert) and (bool(re.match(r'^(\d+[.．、]|[（(]?[一二三四][)）、]|单项|多项|判断)', cert)) or '（ ）' in cert or '( )' in cert or '（  ）' in cert)
            if quiz:
                cert = ''
            tags = [k for k, name, rx in CERTS if re.search(rx, cert)]
            ideo = t.get('ideology', '')
            ideo = re.split(r'(?<=[。！？])', ideo)[0][:70] if ideo else ''
            tasks.append({
                'title': t['title'],
                'steps': [{'t': s['title'], 'a': s['actions']} for s in t['steps']],
                'skills': skills,
                'know': know,
                'support': support,
                'cert': cert,
                'certQuiz': quiz,
                'certPending': (p['n'], t['n']) in PENDING,
                'certTags': [name for _, name, rx in CERTS if re.search(rx, raw_cert)],
                'ideology': ideo,
            })
        ladder = []
        prev = ('认知层', '基础能力')
        LAYER = {'基础能力': ('认知层', '基础能力'), '核心能力': ('实践层', '核心能力'), '拓展能力': ('拓展层', '提升能力'), '提升能力': ('拓展层', '提升能力')}
        for r in p['ladder']:
            lv = re.sub(r'[\u200b\s]', '', r['level'])
            m = re.match(r'^(.+?层)[（(]?(.*?)[)）]?$', lv)
            if not lv:
                layer, desc = prev
            elif m:
                layer, desc = m.group(1), m.group(2)
                if layer == '发展层':
                    layer = '拓展层'
            else:
                layer, desc = LAYER.get(lv, (lv, ''))
            prev = (layer, desc)
            ladder.append({'layer': layer, 'desc': desc, 'm': r['module'], 'p': [x for x in r['points'] if x][:5], 'scene': r['scene'], 'std': r['standard'], 'act': r['practice']})
        projects.append({'n': p['n'], 'title': p['title'], 'tasks': tasks, 'ladder': ladder})
    rel = []
    seen = set()
    for a, b, term in related:
        ka = cap[a[0] - 1]['tasks'][a[1]]['knowledge'][a[2]]['title']
        kb = cap[b[0] - 1]['tasks'][b[1]]['knowledge'][b[2]]['title']
        tm = trim_term(lcs(ka, kb)) or term
        key = (tuple(a), tuple(b))
        if key in seen or len(tm) < 2:
            continue
        seen.add(key)
        rel.append([a, b, tm])
    out = {'projects': projects, 'related': rel}
    T = sum(len(p['tasks']) for p in projects)
    stats = {
        'tasks': T,
        'steps': sum(len(t['steps']) for p in projects for t in p['tasks']),
        'skills': sum(len(g['i']) for p in projects for t in p['tasks'] for g in t['skills']),
        'know': sum(len(t['know']) for p in projects for t in p['tasks']),
        'knowSub': sum(len(k['s']) for p in projects for t in p['tasks'] for k in t['know']),
        'support': sum(len(t['support']) for p in projects for t in p['tasks']),
        'related': len(rel),
        'ladder': sum(len(p['ladder']) for p in projects),
    }
    cov = {}
    for _, name, rx in CERTS:
        cov[name] = sum(1 for p in projects for t in p['tasks'] if name in t['certTags'])
    stats['certCover'] = cov
    stats['certCoverConfirmed'] = {name: sum(1 for p in projects for t in p['tasks'] if name in t['certTags'] and not t['certPending']) for _, name, rx in CERTS}
    stats['certAny'] = sum(1 for p in projects for t in p['tasks'] if t['cert'] or t['certQuiz'])
    stats['certStated'] = sum(1 for p in projects for t in p['tasks'] if t['cert'])
    stats['certPending'] = sum(1 for p in projects for t in p['tasks'] if t['certPending'])
    stats['ideology'] = sum(1 for p in projects for t in p['tasks'] if t['ideology'])
    out['stats'] = stats
    json.dump(out, open(ARGS.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    if ARGS.js:
        js = '''/**
 * 教材能力结构数据（教材稿件结构化导入，由 gen_capability.py 生成）。
 * 字段见 skill 的 references/content-model.md 中 capability 一节。
 */
const CAPABILITY = {
  BOOK_ID: ''' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '''
}

export function findBookCapability (id) {
  return CAPABILITY[id] || null
}

export function fetchBookCapability (id) {
  return Promise.resolve(findBookCapability(id))
}
'''
        open(ARGS.js, 'w', encoding='utf-8').write(js)
    print(json.dumps(stats, ensure_ascii=False))


main()
