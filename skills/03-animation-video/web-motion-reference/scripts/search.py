#!/usr/bin/env python3
"""检索网页动效 / 3D 参考库。

用法（在 skill 目录下运行，或给出脚本的完整路径）：
  python3 scripts/search.py 粒子 经络 --use 登录背景 --min-fit 4
  python3 scripts/search.py 水墨 --pool opus,lib --tier A,B --limit 8
  python3 scripts/search.py --use AI形象 --tone 科技 --min-web 4
  python3 scripts/search.py --show tresjs/coffee-smoke        # 一条的全部字段
  python3 scripts/search.py --poster webgl_points_waves       # 下载封面/截图，打印本地路径，再用 Read 看图
  python3 scripts/search.py --stats                           # 各池子条数与标签分布

关键词：任意中文或英文，在标题、描述、标签、技法、改造思路里做子串匹配；
常见说法会自动扩展同义词（如“经络”→流线，“知识图谱”→网络图谱）。
过滤：--use / --visual / --tone / --palette 取词表里的标签，逗号分隔表示“任一”。
池子：opus（Opus 5.5 动效合集，只有思路）、three（three.js 官方示例，MIT）、lib（开源效果库示例）。
许可：--tier A（可取代码）/ B（可用但只放链接、有条件）/ C（只看思路）。
"""
import argparse, json, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, '..', 'index')
POOLS = {'opus': 'opus55.jsonl', 'three': 'threejs.jsonl', 'lib': 'libraries.jsonl'}

SYN = {
    '经络': ['流线', '光流', '经脉', '脉络', 'meridian'],
    '星河': ['星空宇宙', '粒子', '星系', '银河'],
    '知识图谱': ['网络图谱', '图谱', '节点', '连线', 'graph'],
    '图谱': ['网络图谱', '节点', '连线'],
    '水墨': ['墨', '宣纸', '笔触手绘', '国画', 'ink'],
    '国风': ['东方', '水墨', '书法', '宣纸', '印章'],
    '中医': ['东方', '人体医学', '草药', '本草', '针灸', '穴位'],
    '人体': ['人体医学', '器官', '解剖'],
    '书': ['书本纸张', '翻页', '纸'],
    '翻书': ['书本纸张', '翻页'],
    '背景': ['区块背景', '登录背景', '首页Hero'],
    '首屏': ['首页Hero'],
    'hero': ['首页Hero'],
    '登录': ['登录背景'],
    'ai': ['AI形象', '智能'],
    '转场': ['转场过渡', '过渡', '切换'],
    '加载': ['加载等待', 'loading'],
    '文字': ['文字排版', '标题文字动效', '排版'],
    '滚动': ['scroll', 'ScrollTrigger', '滚动叙事'],
    '数据': ['图表数据', '数据可视化'],
    '粒子': ['Points', '光点'],
    '光': ['光效辉光', '辉光', 'bloom'],
    '烟': ['流体烟雾', '烟雾', '热气'],
    '地球': ['地球地图', 'globe'],
    '隧道': ['隧道穿梭', '穿梭'],
}
TAG_FIELDS = ('visual', 'use', 'tone')
TEXT_W = (('title', 3), ('desc', 2), ('tech', 1), ('idea', 1), ('tip', 1), ('notes', 0.5), ('id', 1), ('source', 1), ('group', 0.5))


def load(pools):
    rows = []
    for p in pools:
        path = os.path.join(INDEX, POOLS[p])
        with open(path, encoding='utf-8') as f:
            rows += [json.loads(l) for l in f if l.strip()]
    return rows


def terms_for(word):
    w = word.lower()
    out = [w]
    for k, v in SYN.items():
        if k.lower() == w:
            out += [x.lower() for x in v]
    return out


def score(r, words, any_mode=False):
    if not words:
        return 0.0
    total = 0.0
    hit = 0
    tags = ' '.join(' '.join(r.get(k, [])) for k in TAG_FIELDS).lower() + ' ' + str(r.get('palette', '')).lower()
    stack = ' '.join(r.get('stack', [])).lower() if isinstance(r.get('stack'), list) else ''
    for word in words:
        best = 0.0
        for i, t in enumerate(terms_for(word)):
            weight = 1.0 if i == 0 else 0.6  # 同义词打折
            s = 0.0
            if t in tags:
                s += 3
            if t in stack:
                s += 1.5
            for field, w in TEXT_W:
                if t in str(r.get(field, '')).lower():
                    s += w
            best = max(best, s * weight)
        if best == 0:
            if not any_mode:
                return -1  # 默认每个关键词都要命中（含同义词）
            continue
        hit += 1
        total += best
    return total if hit else -1


def any_tag(r, field, wanted):
    if not wanted:
        return True
    val = r.get(field, [])
    vals = val if isinstance(val, list) else [val]
    return any(w in vals for w in wanted)


def fmt(r, wide=False):
    tag = f"[{r['pool']}|{r.get('tier', '?')}]"
    head = f"{tag} {r['id']}  适配{r.get('fit', '-')}/网页{r.get('web', '-')}  {r.get('title', '')}"
    desc = r.get('desc', '')
    if not wide and len(desc) > 64:
        desc = desc[:64] + '…'
    lines = [head, f"    {desc}"]
    meta = '用途:' + '、'.join(r.get('use', [])) + '  调性:' + '、'.join(r.get('tone', [])) + '  技法:' + r.get('tech', '')
    lines.append('    ' + meta)
    if r.get('idea'):
        lines.append('    灵枢改造: ' + r['idea'])
    return '\n'.join(lines)


def find(rows, rid):
    for r in rows:
        if r['id'] == rid:
            return r
    for r in rows:  # 前缀匹配，方便只记住一半 id
        if r['id'].startswith(rid):
            return r
    return None


def poster(r):
    url = r.get('poster')
    if not url:
        return print('这一条没有封面图；lib 池请打开 demo 链接查看。')
    out_dir = os.path.join('/tmp', 'wmr_posters')
    os.makedirs(out_dir, exist_ok=True)
    ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'
    dst = os.path.join(out_dir, r['id'].replace('/', '_') + ext)
    res = subprocess.run(['curl', '-sS', '-f', '-L', '--max-time', '30', '-o', dst, url], capture_output=True, text=True)
    if res.returncode != 0:
        return print('下载失败（网络可能不允许）：', url, res.stderr.strip()[:200])
    if ext == '.webp':  # 部分环境的 Read 不认 webp，转成 jpg
        try:
            from PIL import Image
            jpg = dst[:-5] + '.jpg'
            Image.open(dst).convert('RGB').save(jpg, quality=85)
            dst = jpg
        except Exception:
            pass
    print(dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('words', nargs='*')
    ap.add_argument('--pool', default='opus,three,lib')
    ap.add_argument('--tier', default='')
    ap.add_argument('--use', default='')
    ap.add_argument('--visual', default='')
    ap.add_argument('--tone', default='')
    ap.add_argument('--palette', default='')
    ap.add_argument('--stack', default='', help='技术栈/技法子串，逗号分隔表示“任一”，如 Canvas,CSS,SVG')
    ap.add_argument('--no-webgl', action='store_true', help='排除用到 three.js / WebGL / GLSL / TSL 的条目')
    ap.add_argument('--any', action='store_true', help='关键词改为“命中任一即可”，命中越多排越前')
    ap.add_argument('--min-fit', type=int, default=0)
    ap.add_argument('--min-web', type=int, default=0)
    ap.add_argument('--limit', type=int, default=12)
    ap.add_argument('--show')
    ap.add_argument('--poster')
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--json', action='store_true', help='输出 JSON（每行一条）')
    a = ap.parse_args()

    pools = [p.strip() for p in a.pool.split(',') if p.strip() in POOLS]
    rows = load(pools)
    split = lambda s: [x.strip() for x in s.split(',') if x.strip()]

    if a.show or a.poster:
        r = find(rows, a.show or a.poster)
        if not r:
            sys.exit('没有找到：' + (a.show or a.poster))
        if a.show:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            poster(r)
        return

    if a.stats:
        from collections import Counter
        print({p: sum(1 for r in rows if r['pool'] == p) for p in pools})
        for k in ('use', 'visual', 'tone'):
            print(k, Counter(t for r in rows for t in r.get(k, [])).most_common())
        print('palette', Counter(r.get('palette') for r in rows).most_common())
        print('tier', Counter(r.get('tier') for r in rows).most_common())
        return

    tiers = split(a.tier)
    out = []
    for r in rows:
        if tiers and r.get('tier') not in tiers:
            continue
        if r.get('fit', 0) < a.min_fit or r.get('web', 0) < a.min_web:
            continue
        if not (any_tag(r, 'use', split(a.use)) and any_tag(r, 'visual', split(a.visual))
                and any_tag(r, 'tone', split(a.tone)) and any_tag(r, 'palette', split(a.palette))):
            continue
        tech_text = (' '.join(r.get('stack', [])) if isinstance(r.get('stack'), list) else '') + ' ' + r.get('tech', '')
        tl = tech_text.lower()
        if split(a.stack) and not any(x.lower() in tl for x in split(a.stack)):
            continue
        if a.no_webgl and (r['pool'] == 'three' or any(x in tl for x in ('three', 'webgl', 'glsl', 'tsl', 'shader', '着色器', 'webgpu', 'ogl', 'tres'))):
            continue
        s = score(r, a.words, a.any)
        if s < 0:
            continue
        out.append((s + r.get('fit', 0) * 1.5 + r.get('web', 0) * 0.5, r))
    out.sort(key=lambda x: -x[0])
    if not out:
        print('没有结果。试试：减少关键词、去掉过滤条件、换同义说法，或用 --stats 看有哪些标签。')
        return
    print(f'共 {len(out)} 条，显示前 {min(a.limit, len(out))} 条（按相关度 + 灵枢适配度排序）\n')
    for _, r in out[:a.limit]:
        print(json.dumps(r, ensure_ascii=False) if a.json else fmt(r))
        if not a.json:
            print()


if __name__ == '__main__':
    main()
