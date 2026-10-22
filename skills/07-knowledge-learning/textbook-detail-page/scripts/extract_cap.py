"""从工作任务式教材稿件抽取五级能力结构（项目—任务—流程—技能点—知识点）与项目能力进阶表。
用法：python3 -I extract_cap.py <稿件目录> <输出 json>
"""
import sys, re, json, os
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

CNUM = '一二三四五六七八九十'
SECTIONS = set('项目导读 学习目标 任务导入 任务准备 赛证直通 赛政直通 任务筹划 AI提问语 任务实施 操作提示 任务检测 思政园地 任务评价 拓展训练 能力图谱'.split())


NUMFMT = {}


def load_numbering(doc):
    NUMFMT.clear()
    try:
        part = doc.part.numbering_part
    except Exception:
        return
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    el = part.element
    absmap = {}
    for ab in el.findall(W + 'abstractNum'):
        lv = {}
        for l in ab.findall(W + 'lvl'):
            f = l.find(W + 'numFmt'); t = l.find(W + 'lvlText')
            lv[l.get(W + 'ilvl')] = (f.get(W + 'val') if f is not None else '', t.get(W + 'val') if t is not None else '')
        absmap[ab.get(W + 'abstractNumId')] = lv
    for n in el.findall(W + 'num'):
        a = n.find(W + 'abstractNumId')
        if a is not None:
            NUMFMT[n.get(W + 'numId')] = absmap.get(a.get(W + 'val'), {})


def num_prefix(p):
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    ppr = p._p.find(W + 'pPr')
    if ppr is None:
        return ''
    np_ = ppr.find(W + 'numPr')
    if np_ is None or np_.find(W + 'numId') is None:
        return ''
    nid = np_.find(W + 'numId').get(W + 'val')
    il = np_.find(W + 'ilvl'); il = il.get(W + 'val') if il is not None else '0'
    fmt, txt = NUMFMT.get(nid, {}).get(il, ('', ''))
    if not txt or fmt in ('bullet', 'none'):
        return ''
    rep = '一' if 'chinese' in fmt.lower() or 'ideograph' in fmt.lower() else '1'
    return re.sub(r'%\d', rep, txt)


def blocks(doc):
    for el in doc.element.body.iterchildren():
        tag = el.tag.split('}')[1]
        if tag == 'p':
            yield Paragraph(el, doc)
        elif tag == 'tbl':
            yield Table(el, doc)


def clean(s):
    s = s.replace('　', ' ').replace('\xa0', ' ')
    return re.sub(r'[ \t]+', ' ', s).strip()


def cells(row):
    out, last = [], None
    for c in row.cells:
        if c._tc is last:
            continue
        last = c._tc
        # 单元格内换行保留为 \n（不能用“/”代替：评价标准里有“180/120 mmHg”“缓释/控释”这样的原文斜杠）
        out.append('\n'.join(x for x in (clean(l) for l in c.text.split('\n')) if x))
    return out


def short_title(t, limit=24):
    """“1.收缩压增高、脉压增大  收缩压……” → “收缩压增高、脉压增大”"""
    m = re.match(r'^\d+[.．、]\s*(.+)$', t)
    if not m:
        return None
    body = m.group(1)
    for sep in ('  ', '\t', '：', ':', '。', '；'):
        if sep in body:
            head = body.split(sep)[0].strip()
            if 2 <= len(head) <= limit:
                return head
            return None
    return body.strip() if 2 <= len(body) <= limit else None


def parse(path, n):
    doc = docx.Document(path)
    load_numbering(doc)
    proj = {'n': n, 'title': '', 'tasks': [], 'ladder': []}
    task = None
    section = None
    know_on = False
    k1 = None
    step = None
    for b in blocks(doc):
        if isinstance(b, Paragraph):
            raw = num_prefix(b) + b.text
            t = clean(raw)
            rt = raw.replace('\u3000', '  ').replace('\xa0', ' ').strip()
            if not t:
                continue
            if not proj['title']:
                proj['title'] = re.sub(r'[（(]\d+\s*学时[)）]', '', re.sub(r'^项目[一二三四五六七八九十\d]+[：:\s]*', '', t)).strip()
                continue
            m = re.match(r'^【(.+?)】', t)
            if m and m.group(1).replace(' ', '') in SECTIONS:
                section = m.group(1)
                know_on = section == '任务准备'
                k1 = None
                rest = t[m.end():].strip()
                if task is not None and section in ('赛证直通', '思政园地') and rest:
                    task.setdefault('cert' if section == '赛证直通' else 'ideology', rest)
                continue
            m = re.match(r'^任务\s*(\d+)[\s.．]*(.+)$', t)
            if m and len(t) < 40 and section != '任务实施':
                task = {'n': int(m.group(1)), 'title': m.group(2).strip(' ：:'), 'steps': [], 'skills': [], 'knowledge': []}
                proj['tasks'].append(task)
                section = None
                continue
            if task is None:
                continue
            if section == '任务准备':
                if re.match(r'^一[、.．]\s*知识准备', t):
                    know_on = True
                    continue
                if re.match(r'^[二三四五六][、.．]', t) or re.search(r'(选择题|判断题|案例分析|实训操作|填空题|简答题)', t[:14]):
                    know_on = False
                    continue
                if know_on:
                    m = re.match(r'^[（(]([' + CNUM + r']+)[)）]\s*(.+)$', rt)
                    if m:
                        title = re.split(r'\s{2,}|：|:|，见|。', m.group(2))[0].strip()
                        if len(title) > 20:
                            title = re.split(r'[\s，,]', title)[0]
                        k1 = {'title': title[:30], 'subs': []}
                        task['knowledge'].append(k1)
                        continue
                    st = short_title(rt)
                    if st and k1 is not None and len(k1['subs']) < 12:
                        k1['subs'].append(st)
                    elif st and k1 is None and len(task['knowledge']) < 10:
                        task['knowledge'].append({'title': st, 'subs': []})
            elif section in ('赛证直通', '思政园地'):
                key = 'cert' if section == '赛证直通' else 'ideology'
                if key not in task and len(t) > 12:
                    task[key] = t
            elif section == '任务实施':
                m = re.match(r'^(?:第[' + CNUM + r']+步|步骤[' + CNUM + r']+)[：:\s]*(.+)$', t)
                if m:
                    step = {'title': re.split(r'[：:。]', m.group(1).strip())[0][:30], 'actions': []}
                    task['steps'].append(step)
                    continue
                if step is not None:
                    st = short_title(rt, 18)
                    if st and len(step['actions']) < 10:
                        step['actions'].append(st)
        else:
            rows = [cells(r) for r in b.rows]
            if not rows:
                continue
            head = ''.join(rows[0])
            if ('评价维度' in head or '评价项目' in head) and task is not None and not task['skills']:
                last_dim = ''
                for r in rows[1:]:
                    if len(r) < 3 or not r[1] or r[0] == r[1]:
                        continue
                    # 维度列留空的续行（未合并单元格）归入上一个维度
                    dim = r[0].replace('\n', '') or last_dim
                    if not dim:
                        continue
                    last_dim = dim
                    if re.match(r'^(总分|合计|自我|教师|小计)', dim):
                        continue
                    m = re.match(r'^(.+?)[（(](\d+)\s*分[)）]', dim)
                    name, total = (m.group(1).strip(), int(m.group(2))) if m else (dim.strip(), None)
                    sm = re.match(r'^\d+', r[2] or '')
                    score = int(sm.group(0)) if sm else None
                    parts = [x.strip() for x in re.split(r'\n|；|;', r[1]) if x.strip()]
                    parts = [re.sub(r'^\d+[.．、]\s*', '', x).rstrip('。') for x in parts]
                    g = next((x for x in task['skills'] if x['dim'] == name), None)
                    if g is None:
                        g = {'dim': name, 'total': total, 'items': []}
                        task['skills'].append(g)
                    if len(parts) == 1:
                        g['items'].append({'text': parts[0], 'score': score})
                    else:
                        if g['total'] is None:
                            g['total'] = score
                        g['items'].extend({'text': x, 'score': None} for x in parts)
                for g in task['skills']:
                    if g['total'] is None:
                        g['total'] = sum(i['score'] or 0 for i in g['items']) or None
            elif ('层级' in head and '能力' in head) or ('能力层级' in head):
                for r in rows[1:]:
                    if len(r) < 4:
                        continue
                    level = re.sub(r'\s*/\s*|\n', '', r[0])
                    r = [x.replace('\n', ' / ') if i != 2 else x for i, x in enumerate(r)]
                    proj['ladder'].append({
                        'level': level,
                        'module': re.sub(r'^\d+[.．、]\s*', '', r[1]),
                        'points': [re.sub(r'^\d+[.．、]\s*', '', x).strip(' ；;。') for x in re.split(r'\n|(?<=[；;])\s*(?=\d+[.．])', r[2]) if x.strip(' /')],
                        'scene': r[3] if len(r) > 3 else '',
                        'standard': r[4] if len(r) > 4 else '',
                        'practice': r[5] if len(r) > 5 else ''
                    })
    return proj


def main():
    src, out = sys.argv[1], sys.argv[2]
    res = []
    for n in range(1, 17):
        p = os.path.join(src, 'P%02d.docx' % n)
        res.append(parse(p, n))
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
    for p in res:
        ts = p['tasks']
        print('P%02d %-14s 任务%d 流程%d 技能维度%d 技能点%d 知识点%d/%d 赛证%d 思政%d 进阶%d' % (
            p['n'], p['title'][:14], len(ts), sum(len(t['steps']) for t in ts), sum(len(t['skills']) for t in ts),
            sum(len(g['items']) for t in ts for g in t['skills']), sum(len(t['knowledge']) for t in ts),
            sum(len(k['subs']) for t in ts for k in t['knowledge']), sum('cert' in t for t in ts), sum('ideology' in t for t in ts), len(p['ladder'])))


main()
