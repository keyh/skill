---
name: textbook-detail-page
description: 把一本教材的电子稿（Word，按项目 / 章分文件）转换成灵枢医学数字教材详情页（单文件 HTML，三种身份 × 12 个栏目，含知识图谱与能力图谱）。当用户提供教材稿件并要求生成、更新或检查教材详情页时使用。
---

# 教材详情页生成

## 这个 skill 做什么

把一本教材的稿件变成和《老年疾病照护》详情页**同一套页面、同一个标准**的 HTML 详情页。
页面本身是现成的模板（`template.html`），**不要重画页面**；你的工作是产出一份数据文件 `book.json`，再用脚本把数据填进模板。

```
稿件 docx ──脚本抽取──▶ projects.json + capability.json ─┐
                                                        ├─ assemble.py ──▶ book.json ──build_page.py──▶ 详情页.html
你撰写 book.meta.json（基本信息 + 文案 + 稿件里没有的数量）─┘                                   └─ check_page.js 检查
```

三类内容，来源不同，页面上也会分别标注：

| 来源 | 内容 | 谁来做 |
|---|---|---|
| 稿件解析 | 目录、任务、学习目标、项目导读、思政园地、赛证直通、AI 提问语、五级能力结构（流程 / 技能点 / 知识点）、能力进阶表 | 脚本自动抽取，**不要手工改数字** |
| 人工录入 | 书名、ISBN、主编、版次、定价、适用专业、团队、政策依据、资源数量 | 由编辑提供；没有的留空或用占位，**不要编造** |
| AI 生成 · 待审核 | 简介、重点难点、问题图谱、思政主线、岗位画像、适配结论等文案 | 你根据稿件撰写，必须能在稿件中找到依据 |

## 工作步骤

### 第 0 步：准备环境

- Python 3.10+，`pip install python-docx lxml`；Node 18+；检查页面需要 `npm i playwright && npx playwright install chromium`（可选，但交付前必须跑一次）。
- 稿件整理到一个目录，命名为 `P01.docx … Pnn.docx`，一个项目（或一章）一个文件。`.doc` 先另存为 `.docx`。
- 稿件是未出版的受版权保护内容：只在本地处理，不要上传到仓库或公开位置；交付物只有 `book.json` 和生成的 HTML。

### 第 1 步：读稿件，判断体例

打开两三个文件，确认：

1. 一级单元是“项目”还是“章”；二级单元是“任务”还是“节”。
2. 栏目是否用【栏目名】标出：【项目导读】【学习目标】【任务导入】【任务准备】【赛证直通】【任务筹划】【AI提问语】【任务实施】【任务检测】【思政园地】【任务评价】【拓展训练】【能力图谱】。
3. 任务评价是否为表格（评价维度 / 评价标准 / 分值），项目末尾是否有能力图谱表（能力层级 / 能力模块 / 能力点 / 场景 / 达成标准 / 实践要求）。

对照 `references/extraction.md` 的“体例要求”：
- 完全符合 → 直接走第 2 步。
- 栏目名不同（如【课前准备】代替【任务准备】）→ 改 `scripts/extract_cap.py` 和 `scripts/extract_book.py` 顶部的常量，再走第 2 步。
- 没有任务实施 / 任务评价 / 知识准备这三类内容（学科体例的本科教材）→ 跳过能力结构，`assemble.py` 不传 capability.json，页面的知识图谱、能力图谱栏目会显示“尚未导入”的占位，其余栏目正常。在 `book.meta.json` 里把 `terms` 改成章 / 节。

### 第 2 步：跑抽取脚本

```bash
S=skills/textbook-detail-page/scripts
python3 -I $S/extract_book.py  稿件目录/ projects.json        # 目录、目标、导读、思政、赛证、AI 提问语
python3 -I $S/extract_cap.py   稿件目录/ cap.json             # 五级结构 + 能力进阶表
python3 -I $S/relations.py     cap.json rel.json              # 知识点→技能点、跨项目关联（预生成）
python3 -I $S/gen_capability.py rel.json capability.json [--pending pending.txt] [--certs certs.json]
```

每一步都会打印每个项目抽到的数量。**逐行看**：某个项目的任务数、知识点数、技能点数明显偏少或为 0，说明稿件体例有出入，回到稿件核对后调整脚本常量重跑，不要在后面手工补数。

- `certs.json`：这本教材在【赛证直通】里点名的证书与赛项的识别规则（类型、名称、正则）。先 `grep` 稿件里的证书名称再写，不要沿用示例里的养老类规则。
- `pending.txt`：如果你在修订稿件时**补写**了赛证对接说明，把这些任务列进去（每行 `项目.任务`），它们会显示“待作者确认”，不计入对接率。

### 第 3 步：撰写 book.meta.json

以 `example/book.meta.json` 为样板，字段说明见 `references/content-model.md`。按这个顺序填：

1. **基本信息**（人工录入）：书名、封面两行标题、英文名、专业、层次、版次、主编、ISBN、适用专业、学时、定价方案。编辑没给的写 `"待补充"`，不要编。
2. **结构**：`short`（每个项目 2–5 字简称，数量必须等于项目数）、`stages`（把项目分成 3–6 个学习阶段，必须恰好覆盖全部项目序号一次）。
3. **资源数量** `stat`：视频、课件、文档、图像、试题、案例、虚仿、图卡、知识节点、知识模块。由编辑或平台提供；没有就按“每任务 1 套课件、1 段视频”的规划值填，并在 `text.media` 等处说明是规划数。
4. **文案** `text.*`：每一条都要能从稿件找到依据（重点难点来自各项目导读和任务目标；问题图谱的问题来自任务导入的情境与任务检测；思政主线来自各项目思政园地的归纳；岗位画像和证书来自赛证直通）。写的时候顺手记下依据所在的项目。
5. **团队、政策**：编辑提供；政策依据按教材类别更换（高职用教职成文件与专业教学标准，本科用本科教材相关文件）。
6. `jobLabels`：`certs.json` 里的证书名 → 页面显示的全称。

`book.meta.json` **不要写**任务数、知识点数、技能点数、思政点数、赛证点数、各项目知识点数、赛证对接率——这些全部由 `assemble.py` 从抽取结果计算。文案里如果要提到数量（如“16 个项目、66 个任务”），先跑一遍第 4 步看打印出来的统计，再写进去。

### 第 4 步：合成、生成、检查

```bash
python3 -I $S/assemble.py book.meta.json projects.json capability.json -o book.json
python3 -I skills/textbook-detail-page/build_page.py book.json 详情页.html
python3 -I skills/textbook-detail-page/build_page.py book.json 详情页_新书状态.html --new-book
node $S/check_page.js 详情页.html          # 36 个栏目 × 两种宽度：无报错、无横向溢出、无空块、无 undefined
```

`build_page.py` 会校验字段完整性与一致性，报错信息直接说明缺什么。`check_page.js` 输出 `OK` 才算完成。然后按 `references/qa.md` 的清单人工过一遍（打开 HTML，三种身份各点一轮）。

### 第 5 步：交付

- 交付 `详情页.html`、`详情页_新书状态.html`、`book.json`，并附一段说明：哪些数字来自稿件统计、哪些是规划值、哪些文案待编辑审核、稿件中发现的问题（缺栏目、数字不一致、编辑批注残留）。
- 如需进入门户 Vue 工程：`python3 -I $S/to_vue.py book.json out/`，得到 `<id>.detail.json` 与 `<id>.capability.json`，并入 `apps/portal/src/api/bookDetail.js` 与 `bookCapability.js`。

## 必须遵守的规则

1. **不改模板**。页面结构、栏目、配色、交互都在 `template.html` 里，所有教材共用。发现模板的问题，单独提出，不要为某本书改模板。
2. **数字只来自计算**。页面上出现的每个统计数字要么是脚本从稿件算出来的，要么是编辑提供的资源数量。文案里引用数量时与统计一致。
3. **不编造**。没有的信息（获奖、使用数据、院校反馈、主编头衔）留空：`live` 填 `null` 页面会显示“新书上线”；`meta.plan` 填 `null` 显示“申报中”；`text.feedback` 填 `[]`。
4. **区分“作者写的”和“你补的”**。你在修订稿件时补写的内容（赛证对接、缺失的栏目）要列入 `pending.txt`，页面会标“待作者确认”。
5. **稿件不离开本地**，交付物里不含稿件原文件。
6. **做完要检查**。`check_page.js` 不通过不交付。

## 文件清单

| 文件 | 作用 |
|---|---|
| `template.html` | 页面模板（V27 规格，与门户 Vue 工程详情页一致） |
| `defaults.json` | 平台通用的默认文案与定价方案，`book.meta.json` 未写的字段用它补 |
| `build_page.py` | 数据 → HTML，含字段校验 |
| `scripts/extract_book.py` | 稿件 → 项目级内容 |
| `scripts/extract_cap.py` `relations.py` `gen_capability.py` | 稿件 → 五级能力结构 + 关系 |
| `scripts/assemble.py` | 合成 book.json，计算全部统计 |
| `scripts/check_page.js` | 生成后的页面检查 |
| `scripts/to_vue.py` | book.json → Vue 工程数据 |
| `scripts/accept_simple.py` | 接受 Word 修订（稿件带修订时先跑） |
| `scripts/revise_ms.py` `make_list.js` | 以修订模式修改稿件并生成修订清单（需要改稿时用，见 `references/extraction.md`） |
| `references/content-model.md` | book.json 每个字段的含义、来源、在页面上的位置 |
| `references/extraction.md` | 稿件体例要求与抽取规则 |
| `references/page-spec.md` | 页面规格：栏目、内容块、设计标准 |
| `references/qa.md` | 交付前检查清单 |
| `example/` | 《老年疾病照护》的 `book.meta.json`、完整 `book.json`、`pending.txt`、`certs.json` |
