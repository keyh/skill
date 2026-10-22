"""把 book.json 转成门户 Vue 工程（apps/portal）的两个数据文件：
  <id>.detail.json      → 并入 src/api/bookDetail.js 的 DETAILS[<id>]
  <id>.capability.json  → 并入 src/api/bookCapability.js 的 CAPABILITY[<id>]
用法：python3 -I to_vue.py book.json <输出目录>

Vue 工程里的 projects[] 字段名与单文件页面略有不同（title / objectives / ideology / certification / aiPrompt），这里做映射。
Vue 工程的栏目文案（StandardsPage、TeacherBasisPage 等）目前仍写在组件里；跨教材使用时，应把这些文案改为读取 detail.text，
与单文件页面共用同一份 book.json。
"""
import sys, json, os

book = json.load(open(sys.argv[1], encoding='utf-8'))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
pal = ['#4f7df3', '#35b37e', '#8b6cf0', '#ef5e9c', '#f29a3a', '#2bb5c9']
detail = {
    'header': {'en': book['titleEn'], 'major': book['major'], 'editionTag': '%s · %s' % (book['level'], book['edition']), 'editors': book['editors'],
               'isbn': book['isbn'], 'edition': book['editionDate'], 'applicable': book['audience'], 'hours': book['hours']},
    'meta': book['meta'], 'live': book.get('live'),
    'stat': dict(book['stat'], ideology=book['stat'].get('sz')),
    'abilities': [{'group': g['g'], 'items': g['items']} for g in book.get('abilities', [])],
    'jobs': book['jobs'],
    'stages': [[s[0], s[1]] for s in book['stages']], 'short': book['short'],
    'questions': {'global': book['questions']['global'], 'project': book['questions']['proj'], 'task': book['questions']['task']},
    'ideologyLines': [[s[0], s[2], s[3], s[4]] for s in book['ideologyLines']],
    'team': book['team'],
    'text': book['text'],
    'projects': [{'n': p['n'], 'title': p['t'], 'kp': p.get('kp'), 'skill': p.get('skill'), 'intro': p.get('intro', ''), 'tasks': p['tasks'],
                  'objectives': p.get('obj', {}), 'ideology': p.get('sz', ''), 'certification': p.get('cert', ''), 'aiPrompt': p.get('ai', '')} for p in book['projects']]
}
json.dump(detail, open(os.path.join(out, book['id'] + '.detail.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if book.get('capability'):
    json.dump(book['capability'], open(os.path.join(out, book['id'] + '.capability.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ok', out)
