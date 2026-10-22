"""从稿件抽取项目级内容（目录、学习目标、项目导读、思政园地、赛证直通、AI 提问语），输出 projects.json。
用法：python3 -I extract_book.py <稿件目录> <输出 json>
稿件目录内文件命名为 P01.docx … Pnn.docx（每个项目 / 章一个文件）。

抽取规则（可按稿件体例调整顶部的常量）：
- 项目标题：文件第一段，去掉“项目X”前缀与“（N 学时）”；
- 任务标题：形如“任务1 ……”的段落（不在【任务实施】栏目内）；
- 学习目标：【学习目标】下的“知识目标 / 技能目标 / 素质目标”小标题及其编号条目；
- 项目导读：【项目导读】后的第一段正文（跳过行内编辑批注）；
- 思政园地 / 赛证直通 / AI 提问语：各任务对应栏目的首段，项目级取第一个任务的。
"""
import sys, os, re, json
import docx

SECTION_RE = re.compile(r'^【(.+?)】\s*(.*)$')
TASK_RE = re.compile(r'^任务\s*(\d+)[\s.．]*(.+)$')
OBJ_HEADS = ['知识目标', '技能目标', '素质目标']
INTRO_SECTION, OBJ_SECTION = '项目导读', '学习目标'
TASK_FIELDS = {'思政园地': 'sz', '赛证直通': 'cert', '赛政直通': 'cert', 'AI提问语': 'ai', 'AI提示语': 'ai'}
CN = '一二三四五六七八九十'


def clean(s):
    return re.sub(r'[ \t　\xa0]+', ' ', s).strip()


def parse(path, n):
    d = docx.Document(path)
    paras = [clean(p.text) for p in d.paragraphs]
    paras = [p for p in paras if p]
    proj = {'n': n, 't': '', 'tasks': [], 'obj': {}, 'intro': '', 'sz': '', 'cert': '', 'ai': ''}
    proj['t'] = re.sub(r'[（(]\d+\s*学时[)）]', '', re.sub(r'^项目[' + CN + r'\d]+[：:\s]*', '', paras[0])).strip()
    section, obj_head, task_i = None, None, -1
    task_fields = []   # per task: {sz, cert, ai}
    for t in paras[1:]:
        m = SECTION_RE.match(t)
        if m:
            section = m.group(1).replace(' ', '')
            rest = m.group(2).strip()
            obj_head = None
            if section in TASK_FIELDS and task_i >= 0 and rest and len(rest) > 12:
                task_fields[task_i].setdefault(TASK_FIELDS[section], rest)
            continue
        m = TASK_RE.match(t)
        if m and len(t) < 40 and section != '任务实施':
            proj['tasks'].append(m.group(2).strip(' ：:'))
            task_fields.append({})
            task_i += 1
            section = None
            continue
        if section == INTRO_SECTION and not proj['intro'] and len(t) > 30:
            proj['intro'] = t
        elif section == OBJ_SECTION:
            head = re.sub(r'^[一二三四五六七八九十\d]+[、.．]\s*', '', t).strip('：:')
            if head in OBJ_HEADS:
                obj_head = head
                proj['obj'].setdefault(head, [])
            elif obj_head:
                item = re.sub(r'^[\d①-⑳]+[.．、）)]?\s*', '', t)
                if len(item) > 4:
                    proj['obj'][obj_head].append(item)
        elif section in TASK_FIELDS and task_i >= 0:
            key = TASK_FIELDS[section]
            if key not in task_fields[task_i] and len(t) > 12 and not re.match(r'^(\d+[.．、]|[（(]?[一二三四][)）、]|单项|多项|判断)', t):
                task_fields[task_i][key] = t
    proj['taskFields'] = task_fields
    for k in ('sz', 'cert', 'ai'):
        proj[k] = next((f[k] for f in task_fields if f.get(k)), '')
    return proj


def main():
    src, out = sys.argv[1], sys.argv[2]
    files = sorted(f for f in os.listdir(src) if re.match(r'^P\d+\.docx$', f))
    res = [parse(os.path.join(src, f), int(f[1:-5])) for f in files]
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in res:
        print('P%02d %-16s 任务%d 目标%s 导读%d 思政%d 赛证%d AI%d' % (p['n'], p['t'][:16], len(p['tasks']), [len(v) for v in p['obj'].values()], len(p['intro']),
              sum(1 for f in p['taskFields'] if f.get('sz')), sum(1 for f in p['taskFields'] if f.get('cert')), sum(1 for f in p['taskFields'] if f.get('ai'))))


main()
