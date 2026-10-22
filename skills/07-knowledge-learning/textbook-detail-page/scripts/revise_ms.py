"""对《老年疾病照护》二稿做修订（修订模式 + 批注），与数字教材详情页的五级结构数据同步。
用法：python3 revise_ms.py <稿件目录> <输出目录>
每个文件：解包 → 合并碎片 run → 按操作清单修改 document.xml（w:ins / w:del）→ 加批注 → 重新打包。
"""
import sys, os, re, copy, shutil, subprocess, zipfile, json
from lxml import etree

# docx 工具脚本目录（merge_runs.py、comment.py、validate.py 等），通过环境变量 DOCX_SCRIPTS 指定
SKILL = os.environ.get('DOCX_SCRIPTS', 'docx-scripts')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
q = lambda t: '{%s}%s' % (W, t)
AUTHOR = 'Claude'
DATE = '2026-10-10T00:00:00Z'
_id = [90000]


def nid():
    _id[0] += 1
    return str(_id[0])


def ptext(p):
    """段落可见文字：w:t（含修订插入），不含 w:delText"""
    return ''.join(t.text or '' for t in p.iter(q('t')) if not any(a.tag == q('del') for a in t.iterancestors()))


def body_paras(root):
    return [p for p in root.iter(q('p')) if not any(a.tag == q('tbl') for a in p.iterancestors())]


def find(paras, target, anchor=None, nth=0, after_idx=None):
    start = 0
    if anchor:
        hits = [i for i, p in enumerate(paras) if re.search(anchor, ptext(p).strip())]
        if not hits:
            raise ValueError('anchor not found: ' + anchor)
        start = hits[0]
    if after_idx is not None:
        start = max(start, after_idx)
    hits = [i for i in range(start, len(paras)) if re.search(target, ptext(paras[i]).strip())]
    if len(hits) <= nth:
        raise ValueError('target not found: %s (anchor %s)' % (target, anchor))
    return hits[nth]


def mk_run(rpr, text, deleted=False):
    r = etree.Element(q('r'))
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = etree.SubElement(r, q('delText') if deleted else q('t'))
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r


def wrap(tag, run):
    w = etree.Element(q(tag))
    w.set(q('id'), nid()); w.set(q('author'), AUTHOR); w.set(q('date'), DATE)
    w.append(run)
    return w


def replace_in(p, old, new):
    """把段落中第一处 old 改为 new（修订），只标记实际变动的字符。返回修订节点（供批注）。"""
    full = ptext(p)
    k0 = full.find(old)
    if k0 >= 0 and old and new:
        a = 0
        while a < min(len(old), len(new)) and old[a] == new[a]:
            a += 1
        b = 0
        while b < min(len(old), len(new)) - a and old[-1 - b] == new[-1 - b]:
            b += 1
        core_old, core_new = old[a:len(old) - b], new[a:len(new) - b]
        if core_old:
            try:
                return _replace_run(p, core_old, core_new, full, k0 + a)
            except ValueError:
                pass
    if k0 >= 0:
        return _replace_run(p, old, new, full, k0)
    raise ValueError('text not found: ' + old)


def _replace_run(p, old, new, full, at):
    """在可见文字的 at 位置替换 old（可跨多个 run）"""
    pos = 0
    first_ins = None; first_del = None
    end = at + len(old)
    runs = []
    for t in p.iter(q('t')):
        if any(a.tag == q('del') for a in t.iterancestors()):
            continue
        s = t.text or ''
        runs.append((t, pos, pos + len(s)))
        pos += len(s)
    hit = [(t, a, b) for t, a, b in runs if b > at and a < end]
    if not hit:
        raise ValueError('span not found')
    for idx, (t, a, b) in enumerate(hit):
        r = t.getparent()
        if any(x.tag == q('ins') for x in r.iterancestors()):
            raise ValueError('target inside existing insertion: ' + old)
        s = t.text or ''
        lo, hi = max(at, a) - a, min(end, b) - a
        rpr = r.find(q('rPr'))
        parent = r.getparent(); pos2 = parent.index(r)
        nodes = []
        if s[:lo]:
            nodes.append(mk_run(rpr, s[:lo]))
        d = wrap('del', mk_run(rpr, s[lo:hi], True))
        nodes.append(d)
        if first_del is None:
            first_del = d
        if idx == len(hit) - 1 and new:
            first_ins = wrap('ins', mk_run(rpr, new))
            nodes.append(first_ins)
        if s[hi:]:
            nodes.append(mk_run(rpr, s[hi:]))
        parent.remove(r)
        for j, nd in enumerate(nodes):
            parent.insert(pos2 + j, nd)
    return first_ins if first_ins is not None else first_del


def _old_replace_in(p, old, new):
    for t in p.iter(q('t')):
        if any(a.tag == q('del') for a in t.iterancestors()):
            continue
        s = t.text or ''
        k = s.find(old)
        if k < 0:
            continue
        r = t.getparent()
        if any(a.tag == q('ins') for a in r.iterancestors()):
            raise ValueError('target inside existing insertion: ' + old)
        rpr = r.find(q('rPr'))
        parent = r.getparent(); pos = parent.index(r)
        nodes = []
        if s[:k]:
            nodes.append(mk_run(rpr, s[:k]))
        if old:
            nodes.append(wrap('del', mk_run(rpr, old, True)))
        ins = wrap('ins', mk_run(rpr, new)) if new else None
        if ins is not None:
            nodes.append(ins)
        if s[k + len(old):]:
            nodes.append(mk_run(rpr, s[k + len(old):]))
        parent.remove(r)
        for j, nd in enumerate(nodes):
            parent.insert(pos + j, nd)
        return ins if ins is not None else nodes[1]
    raise ValueError('text not found in paragraph: ' + old + ' | ' + ptext(p)[:40])


def prefix(p, text):
    """在段落开头插入文字（修订）"""
    for r in p.iter(q('r')):
        if r.find(q('t')) is not None and not any(a.tag in (q('del'), q('ins')) for a in r.iterancestors()):
            ins = wrap('ins', mk_run(r.find(q('rPr')), text))
            r.addprevious(ins)
            return ins
    raise ValueError('no run for prefix')


def new_para(ref, text, run_ref=None):
    """仿照 ref 段落格式新建一个“插入的段落”"""
    p = etree.Element(q('p'))
    ppr = ref.find(q('pPr'))
    ppr = copy.deepcopy(ppr) if ppr is not None else etree.Element(q('pPr'))
    for x in ppr.findall(q('numPr')):
        ppr.remove(x)
    rpr_mark = ppr.find(q('rPr'))
    if rpr_mark is None:
        rpr_mark = etree.SubElement(ppr, q('rPr'))
    for x in list(rpr_mark):
        if x.tag in (q('ins'), q('del')):
            rpr_mark.remove(x)
    m = etree.Element(q('ins')); m.set(q('id'), nid()); m.set(q('author'), AUTHOR); m.set(q('date'), DATE)
    rpr_mark.insert(0, m)
    p.append(ppr)
    src = run_ref if run_ref is not None else ref
    rr = None
    for r in src.iter(q('r')):
        if r.find(q('t')) is not None:
            rr = r.find(q('rPr')); break
    ins = wrap('ins', mk_run(rr, text))
    p.append(ins)
    return p, ins


def add_comment(unpacked, node_start, node_end, text):
    out = subprocess.run([sys.executable, os.path.join(SKILL, 'comment.py'), unpacked, text, '--author', AUTHOR, '--initials', 'C'], capture_output=True, text=True, cwd=SKILL)
    if out.returncode:
        raise RuntimeError(out.stderr)
    m = re.search(r'commentRangeStart w:id="(\d+)"', out.stdout)
    cid = m.group(1)
    s = etree.Element(q('commentRangeStart')); s.set(q('id'), cid)
    e = etree.Element(q('commentRangeEnd')); e.set(q('id'), cid)
    ref = etree.Element(q('r')); rp = etree.SubElement(ref, q('rPr')); st = etree.SubElement(rp, q('rStyle')); st.set(q('val'), 'CommentReference')
    cr = etree.SubElement(ref, q('commentReference')); cr.set(q('id'), cid)
    node_start.addprevious(s)
    node_end.addnext(e)
    e.addnext(ref)


CERT_NOTE = '【待作者确认】原稿本任务的“赛证直通”只有练习题，未写明对接的赛项或证书。此句参照本书同类任务的写法补写，请核实对接对象、证书等级与考核模块后接受或修改。（同步自数字教材详情页“岗课赛证”统计）'
STD = '《养老护理员国家职业技能标准（2019年版）》'
CERT = {
    (1, 3): f'本任务对接{STD}相关要求，重点考查协助老年人安全用药、用药后观察记录及岗位职责边界。',
    (1, 4): f'本任务对接{STD}相关要求，重点考查与老年人及家属的有效沟通、冲突化解及照护中的人文关怀。',
    (2, 1): f'本任务对接{STD}中老年人身体状况观察与评估的相关要求。',
    (2, 2): f'本任务对接{STD}中老年人健康状况观察与照护需求分析的相关要求。',
    (2, 3): f'本任务对接{STD}中照护计划制订的相关要求。',
    (2, 4): f'本任务对接{STD}中饮食照护、活动照护与健康教育的相关要求。',
    (5, 2): '本任务对接职业院校技能大赛健康养老照护赛项中生活照护相关考核要点。',
    (6, 1): '本任务对接全国职业院校技能大赛养老照护赛项中健康评估相关考核要点，以及养老护理员职业技能等级证书（中级/高级）考试中健康观察与评估的能力要求。',
    (6, 2): '本任务对接全国职业院校技能大赛养老照护赛项中生活照护相关考核要点，以及养老护理员职业技能等级证书（中级/高级）考试中生活照护与健康教育的能力要求。',
    (6, 3): '本任务对接全国职业院校技能大赛养老照护赛项中协助老人服药相关考核要点，以及养老护理员职业技能等级证书（中级/高级）考试中安全用药协助与氧疗观察的能力要求。',
    (6, 4): '本任务对接全国职业院校技能大赛养老照护赛项相关考核要点，以及养老护理员职业技能等级证书（中级/高级）考试中康复训练指导的能力要求。',
    (6, 5): '本任务对接全国职业院校技能大赛养老照护赛项相关考核要点，以及养老护理员职业技能等级证书（中级/高级）考试中健康观察、异常报告与健康教育的能力要求。',
    (12, 2): '本任务对接全国职业院校技能大赛养老照护赛项及世界职业院校技能大赛健康养老照护赛项。',
    (13, 1): f'本任务对接{STD}相关要求，以下题目内容参照《中国血脂管理指南（2023年）》。',
    (13, 2): f'本任务对接{STD}相关要求，以下题目内容参照《中国高尿酸血症与痛风诊疗指南（2024版）》。',
    (13, 3): f'本任务对接{STD}相关要求，以下题目内容参照《中国老视矫正多专科管理专家共识（2026年）》。',
    (13, 4): f'本任务对接{STD}中皮肤观察与压力性损伤预防的相关要求。',
}
CN = '一二三四五六七八九十'


def task_anchor(n):
    return r'^任务\s*%d[\s.．：:]*\S' % n


def ops_for(pn):
    """返回 [(kind, args...)]；kind: cert / replace / prefix / insert_before"""
    ops = []
    for (p, t), text in CERT.items():
        if p == pn:
            ops.append(('cert', t, text))
    if pn == 2:
        ops.append(('insert_before', task_anchor(1), r'^第一步\s*评估前准备', '【任务实施】', r'^【任务实施】', '体例统一：原稿任务1的“任务实施”缺少栏目标记，已补加，与其他任务一致。'))
        ops.append(('steps_cn', r'^步骤([一二三四五六七八九十]+)', '体例统一：全书流程步骤统一写作“第×步”，原稿本项目任务2—4写作“步骤×”。'))
    if pn == 7:
        ops.append(('replace', None, r'^【赛政直通】', '【赛政直通】', '【赛证直通】', '错字：“赛政直通”应为“赛证直通”。'))
        ops.append(('replace', None, r'^项目七.*（4学时）', '（4学时）', '', '标题中的学时说明建议移至学时分配表或项目导读，项目标题与其他项目保持一致。'))
    if pn == 8:
        ops.append(('insert_before', task_anchor(4), r'^一[、.．]\s*知识准备', '【任务准备】', r'^【任务准备】', '体例统一：原稿任务4缺少“任务准备”栏目标记，已补加。'))
    if pn in (9, 16):
        ops.append(('colon_steps', '体例统一：全书流程步骤写作“第×步 标题”，删去步骤序号后的冒号。'))
    if pn == 12:
        ops.append(('replace', task_anchor(3), r'^表2-3-3', '表2-3-3', '表12-3-3', '表号错误：本任务前一表为“表12-3-2”，此处应为“表12-3-3”。'))
    if pn == 14:
        ops.append(('replace', None, r'^任务3[：:]', '任务3：', '任务3 ', '体例统一：任务标题写作“任务3 标题”，删去冒号。'))
    return ops


def run_file(src, dst, pn, log):
    tmp = os.path.abspath(dst + '.d')
    shutil.rmtree(tmp, ignore_errors=True)
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    for dp, dn, fn in os.walk(tmp):
        for f in fn:
            fp = os.path.join(dp, f)
            if os.path.islink(fp):
                os.remove(fp)
    subprocess.run([sys.executable, os.path.join(SKILL, 'merge_runs.py'), tmp], check=True, capture_output=True, cwd=SKILL)
    dx = os.path.join(tmp, 'word', 'document.xml')
    tree = etree.parse(dx)
    root = tree.getroot()
    comments = []
    for op in ops_for(pn):
        paras = body_paras(root)
        kind = op[0]
        if kind == 'cert':
            _, t, text = op
            ti = find(paras, task_anchor(t))
            nxt = [i for i in range(ti + 1, len(paras)) if re.match(r'^任务\s*\d+[\s.．：:]*\S', ptext(paras[i]).strip()) and len(ptext(paras[i]).strip()) < 40]
            end = nxt[0] if nxt else len(paras)
            mk = [i for i in range(ti, end) if re.match(r'^【赛[证政]直通】', ptext(paras[i]).strip())]
            if not mk:
                raise ValueError('no 赛证直通 in P%d T%d' % (pn, t))
            mi = mk[0]
            ref = paras[mi + 1]
            # 参照正文段落格式：取标记后第一个非空段落
            for j in range(mi + 1, min(mi + 6, end)):
                if ptext(paras[j]).strip():
                    ref = paras[j]; break
            np_, ins = new_para(ref, text)
            paras[mi].addnext(np_)
            comments.append((ins, ins, CERT_NOTE))
            log.append(['内容补写（待作者确认）', 'P%d 任务%d' % (pn, t), '赛证直通补写对接说明', text])
        elif kind == 'insert_before':
            _, anchor, target, text, style_re, note = op
            i = find(paras, target, anchor)
            refs = [p for p in paras if re.match(style_re, ptext(p).strip())]
            ref = refs[0] if refs else paras[i]
            np_, ins = new_para(ref, text)
            paras[i].addprevious(np_)
            comments.append((ins, ins, note))
            log.append(['体例统一', 'P%d' % pn, '补加栏目标记', text])
        elif kind == 'replace':
            _, anchor, target, old, new, note = op
            i = find(paras, target, anchor)
            node = replace_in(paras[i], old, new)
            if note:
                comments.append((node, node, note))
            log.append(['错字/体例' if '错' in (note or '') else '体例统一', 'P%d' % pn, '“%s”→“%s”' % (old, new or '（删除）'), note or ''])
        elif kind == 'prefix':
            _, anchor, target, text, note = op
            i = find(paras, target, anchor)
            node = prefix(paras[i], text)
            if note:
                comments.append((node, node, note))
            log.append(['体例统一', 'P%d' % pn, '补加序号“%s”' % text, ptext(paras[i]).strip()[:30]])
        elif kind == 'steps_cn':
            _, rx, note = op
            first = True; cnt = 0
            for p in paras:
                tx = ptext(p).strip()
                m = re.match(rx, tx)
                if m:
                    node = replace_in(p, '步骤' + m.group(1), '第%s步' % m.group(1))
                    if first and note:
                        comments.append((node, node, note)); first = False
                    cnt += 1
            log.append(['体例统一', 'P%d' % pn, '“步骤×”→“第×步”', '%d 处' % cnt])
        elif kind == 'colon_steps':
            _, note = op
            first = True; cnt = 0
            for p in paras:
                tx = ptext(p).strip()
                m = re.match(r'^(第[一二三四五六七八九十]+步)([：:])', tx)
                if m:
                    node = replace_in(p, m.group(1) + m.group(2), m.group(1) + ' ')
                    if first and note:
                        comments.append((node, node, note)); first = False
                    cnt += 1
            log.append(['体例统一', 'P%d' % pn, '“第×步：”→“第×步 ”', '%d 处' % cnt])
    tree.write(dx, xml_declaration=True, encoding='UTF-8', standalone=True)
    # 批注：comment.py 写入批注文件；标记写回 document.xml
    if comments:
        tree = etree.parse(dx); root = tree.getroot()
        idmap = {}
        for el in root.iter():
            if el.tag in (q('ins'), q('del')):
                idmap[el.get(q('id'))] = el
        for s, e, text in comments:
            node = idmap[s.get(q('id'))]
            add_comment(tmp, node, node, text)
        tree.write(dx, xml_declaration=True, encoding='UTF-8', standalone=True)
    if os.path.exists(dst):
        os.remove(dst)
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(tmp):
            for f in fn:
                fp = os.path.join(dp, f)
                z.write(fp, os.path.relpath(fp, tmp))
    shutil.rmtree(tmp)


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    names = json.load(open(os.path.join(src, 'names.json')))
    log = []
    for n in range(1, 17):
        s = os.path.join(src, 'P%02d.docx' % n)
        d = os.path.join(out, names[str(n)])
        if not ops_for(n):
            shutil.copy(s, d)
            continue
        run_file(s, d, n, log)
        print('P%02d ok' % n)
    json.dump(log, open(os.path.join(out, '..', 'revise_log.json'), 'w'), ensure_ascii=False, indent=1)


main()
