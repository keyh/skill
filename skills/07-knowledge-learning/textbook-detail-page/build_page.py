"""把教材数据（book.json）填入页面模板，生成单文件详情页。
用法：python3 build_page.py <book.json> <out.html> [--template template.html] [--defaults defaults.json] [--new-book]

- book.json 中缺省的字段用 defaults.json 补齐（平台通用文案：AI 场景、四种模式、评价权重等）；
- --new-book：生成“新书状态”页面（无使用数据、仅首个数字版本、未入选规划），用于教材上线前的演示。
"""
import sys, json, re, os, html, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('book')
ap.add_argument('out')
ap.add_argument('--template', default=os.path.join(HERE, 'template.html'))
ap.add_argument('--defaults', default=os.path.join(HERE, 'defaults.json'))
ap.add_argument('--new-book', action='store_true')
args = ap.parse_args()


def merge(base, over):
    if isinstance(base, dict) and isinstance(over, dict):
        r = dict(base)
        for k, v in over.items():
            r[k] = merge(base.get(k), v) if k in base else v
        return r
    return over if over is not None else base


book = json.load(open(args.book, encoding='utf-8'))
defaults = json.load(open(args.defaults, encoding='utf-8')) if os.path.exists(args.defaults) else {}
D = merge(defaults, book)

# ---- 校验：页面逻辑依赖的字段 ----
REQUIRED = ['id', 'title', 'coverTitle', 'level', 'edition', 'editionDate', 'editors', 'isbn', 'audience', 'hours', 'lead',
            'meta', 'stat', 'jobs', 'questions', 'ideologyLines', 'policies', 'team', 'short', 'stages', 'plans', 'projects', 'terms', 'text']
missing = [k for k in REQUIRED if k not in D]
assert not missing, '缺少字段：%s' % missing
P = D['projects']
assert len(P) >= 1 and all('n' in p and 't' in p and 'tasks' in p for p in P), 'projects[] 每项需有 n / t / tasks'
assert len(D['short']) == len(P), 'short 的长度必须等于项目数'
covered = sorted(n for st in D['stages'] for n in st[1])
assert covered == [p['n'] for p in P], 'stages 必须恰好覆盖全部项目序号一次：%s' % covered
for st in D['stages']:
    assert len(st) == 3 and st[2].startswith('#'), 'stages 每项为 [阶段名, [项目序号…], 颜色]'
for k in ['kp', 'video', 'ppt', 'doc', 'img', 'quiz', 'cases', 'sz', 'cert', 'ai', 'vr', 'cards', 'nodes', 'modules']:
    assert k in D['stat'], 'stat 缺少 %s' % k
assert D['meta'].get('versions'), 'meta.versions 至少一个数字版本'
if D.get('capability'):
    C = D['capability']
    assert len(C['projects']) == len(P), 'capability.projects 数量须与 projects 一致'
    for p, c in zip(P, C['projects']):
        assert len(p['tasks']) == len(c['tasks']), '项目 %s 的任务数在 projects 与 capability 中不一致' % p['n']
    assert 'stats' in C and 'tasks' in C['stats'], 'capability.stats 缺失'

if args.new_book:
    D['live'] = None
    D['meta'] = dict(D['meta'], plan=None, planNote=None, awards=[], versions=D['meta']['versions'][:1])
    D['text'] = dict(D['text'], feedback=[])

# ---- 注入 ----
s = open(args.template, encoding='utf-8').read()
data_js = 'const D=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';'
assert s.count('/*__DATA__*/') == 1
s = s.replace('/*__DATA__*/', data_js)


def fill(m):
    key = m.group(1)
    raw = key.startswith('{')
    key = key.strip('{}')
    assert key in D, '模板占位符 {{%s}} 在数据中没有对应字段' % key
    v = str(D[key])
    return v if raw else html.escape(v, quote=False)

s = re.sub(r'\{\{(\{?[a-zA-Z0-9_]+\}?)\}\}', fill, s)
assert '{{' not in s.split('<script>')[0]
open(args.out, 'w', encoding='utf-8').write(s)
print('ok', args.out, len(s))
