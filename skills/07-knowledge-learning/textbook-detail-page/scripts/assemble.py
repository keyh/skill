"""把三份输入合成页面数据 book.json：
  book.meta.json   人工 / 模型撰写的部分（基本信息、文案、资源数量、团队、政策……，见 references/content-model.md）
  projects.json    extract_book.py 从稿件抽取的项目级内容
  capability.json  gen_capability.py 生成的五级能力结构（可省略，省略时页面图谱栏目显示占位）
用法：python3 -I assemble.py book.meta.json projects.json [capability.json] -o book.json

所有能从稿件算出来的数字（任务数、知识点、技能点、流程、思政点、赛证点、各项目知识点数、赛证对接率、特色卡里的数量）
都在这里计算并写入，不要在 book.meta.json 里手填；手填的只有稿件里没有的资源数量（视频、课件等）。
"""
import sys, json, argparse, re

ap = argparse.ArgumentParser()
ap.add_argument('meta'); ap.add_argument('projects'); ap.add_argument('capability', nargs='?')
ap.add_argument('-o', '--out', required=True)
ap.add_argument('--intro-len', type=int, default=110, help='项目简介截取长度')
ap.add_argument('--snippet-len', type=int, default=110, help='思政园地 / AI 提问语截取长度')
A = ap.parse_args()

M = json.load(open(A.meta, encoding='utf-8'))
P = json.load(open(A.projects, encoding='utf-8'))
C = json.load(open(A.capability, encoding='utf-8')) if A.capability else None


def cut(s, n):
    s = (s or '').strip()
    return s if len(s) <= n else s[:n]


projects = []
for i, p in enumerate(P):
    c = C['projects'][i] if C else None
    q = {'n': p['n'], 't': p['t'], 'tasks': p['tasks'], 'obj': p.get('obj', {}),
         'intro': cut(p.get('intro'), A.intro_len), 'sz': cut(p.get('sz'), A.snippet_len), 'cert': p.get('cert', ''), 'ai': cut(p.get('ai'), A.snippet_len)}
    if c:
        q['kp'] = sum(len(t['know']) for t in c['tasks'])
        q['skill'] = sum(len(g['i']) for t in c['tasks'] for g in t['skills'])
    ov = (M.get('projectOverrides') or {}).get(str(p['n']), {})
    q.update(ov)   # 例如 {"hours": 6, "intro": "……"}
    projects.append(q)

NT = sum(len(p['tasks']) for p in projects)
tf = [f for p in P for f in p.get('taskFields', [])]
stat = dict(M.get('stat', {}))
stat.update({
    'sz': sum(1 for f in tf if f.get('sz')), 'cert': sum(1 for f in tf if f.get('cert')), 'ai': sum(1 for f in tf if f.get('ai')),
})
if C:
    s = C['stats']
    stat.update({'kp': s['know'], 'skill': s['skills'], 'step': s['steps']})
    stat.setdefault('nodes', s['know'] + s['knowSub'])
    stat.setdefault('modules', len(projects))
for k in ['kp', 'video', 'ppt', 'doc', 'img', 'quiz', 'cases', 'vr', 'cards', 'nodes', 'modules']:
    assert k in stat, 'stat 缺少 %s（稿件里没有的资源数量要写在 book.meta.json 的 stat 里）' % k

# 赛证对接率：来自能力结构统计中“作者写明对接”的任务数
jobs = M.get('jobs')
if C and not jobs:
    labels = M.get('jobLabels', {})
    conf = C['stats'].get('certCoverConfirmed') or C['stats']['certCover']
    jobs = [[labels.get(name, name), round(v / NT * 100), '%d / %d 个任务' % (v, NT)] for name, v in conf.items() if v and name in labels] or \
           [[name, round(v / NT * 100), '%d / %d 个任务' % (v, NT)] for name, v in conf.items() if v]
assert jobs, '缺少 jobs（有能力结构时自动计算；否则在 book.meta.json 里提供）'

text = dict(M.get('text', {}))
# 特色卡：数量自动填入
if 'features' not in text:
    text['features'] = [['任务体例', '%d 环节，课堂主线 %d 环节' % (len(text.get('taskFlow', [0] * 11)), len(text.get('taskFlowMain', [0] * 4))), '#4f7df3'],
                        ['思政园地', '嵌入任务流程，%d 处' % stat['sz'], '#ef5e9c'], ['赛证直通', '岗课赛证逐任务对接', '#f29a3a'], ['AI 提问语', '教材原生 AI 入口，%d 条' % stat['ai'], '#2bb5c9']]

book = {k: v for k, v in M.items() if k not in ('stat', 'text', 'jobs', 'jobLabels', 'projectOverrides')}
book.update({'projects': projects, 'stat': stat, 'jobs': jobs, 'text': text, 'capability': C})
assert len(book.get('short', [])) == len(projects), 'short（项目简称）数量须等于项目数 %d' % len(projects)

# 文案里的数字与统计不一致时提醒（不阻断）
flat = json.dumps(text, ensure_ascii=False)
for num, what in [(NT, '任务数'), (stat['kp'], '知识点数'), (stat['sz'], '思政园地数')]:
    for m in set(re.findall(r'\d+', flat)):
        pass
hits = re.findall(r'(\d+) 个任务', flat)
for h in hits:
    if int(h) != NT and int(h) > NT:
        print('提醒：文案中出现 “%s 个任务”，而稿件任务总数为 %d，请核对' % (h, NT))

json.dump(book, open(A.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', A.out, '项目', len(projects), '任务', NT, '知识点', stat.get('kp'), '技能点', stat.get('skill'), '思政', stat['sz'], '赛证', stat['cert'], 'AI', stat['ai'])
