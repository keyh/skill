# book.json 字段说明

`book.json` = `defaults.json` ⊕ `book.meta.json`（你写的）⊕ `projects.json`（抽取）⊕ `capability.json`（抽取）。
`assemble.py` 负责合成；下面标注每个字段**由谁提供**、**显示在哪里**。

来源标记：〔录〕编辑录入 · 〔抽〕脚本从稿件抽取 · 〔写〕你根据稿件撰写（页面标为“AI 生成 · 已审核”）· 〔算〕assemble.py 计算 · 〔默〕defaults.json 有默认值，可覆盖。

## 1. 基本信息（首屏）

| 字段 | 来源 | 说明 | 示例 |
|---|---|---|---|
| `id` | 录 | 教材编号，门户工程里的 book id | `"b09"` |
| `title` | 录 | 书名（标题、面包屑） | `"老年疾病照护"` |
| `coverTitle` | 录 | 封面书名，用 `<br>` 分两行，每行 ≤ 5 字为佳 | `"老年疾病<br>照护"` |
| `titleEn` | 录 | 英文名（全大写） | `"GERIATRIC DISEASE CARE"` |
| `major` | 录 | 面向专业，h1 下方 | `"智慧健康养老服务与管理专业"` |
| `level` `edition` | 录 | 层次、版次，首屏标签 | `"高职专科"` `"第 1 版"` |
| `editionDate` | 录 | 版次与出版年月 | `"第 1 版 · 2026 年 8 月"` |
| `editors` `isbn` | 录 | 主编（用 ` · ` 分隔）、ISBN | |
| `audience` `hours` | 录 | 适用专业、学时建议（首屏信息栏） | `"64 学时 · 建议第 3 学期"` |
| `lead` | 写 | 首屏导语，一句话说明教材组织方式；可含 `<b>` | 见示例 |
| `publisher` | 默 | 出版单位 | |
| `plans` `price` `priceNote` `planNote` | 默 | 授权方案与默认价格；本科教材把 `plans` 中“3 学年 · 高职在校”改为“4 学年 · 本科在校”并改 `planNote` | |
| `terms` | 默 | 单元名称：`unit1` 一级单元（项目 / 章）、`unit2` 二级（任务 / 节）、`unit2Full`（工作任务 / 学习任务）、`abbr`（P / C）、`ring`（导读项目环中心字样） | |

## 2. 出版与使用

| 字段 | 来源 | 说明 |
|---|---|---|
| `meta.isbn` `meta.paper {edition,date}` | 录 | 纸书版次 |
| `meta.plan` `meta.planNote` | 录 | 规划教材名称与说明；**未入选填 `null`**，页面自动显示“新书 · 申报中” |
| `meta.awards[]` | 录 | `{title, note}`；没有填 `[]` |
| `meta.versions[]` | 录 | 数字版本 `{v, date, note}`，至少一项；只有一项时页面按“首个版本”显示 |
| `meta.next` | 录 | 下次修订时间，可空 |
| `live` | 录/默 | 使用数据 `{students, termStudents, schools, provinces, teachers, classes, completion, semesters[[学期,学生,院校]…]}`；**新书填 `null`**，数据带、应用证据栏目显示空状态 |

## 3. 结构与统计

| 字段 | 来源 | 说明 |
|---|---|---|
| `projects[]` | 抽 | 每项 `{n, t, tasks[], obj{知识目标,技能目标,素质目标}, intro, sz, cert, ai, kp, skill, hours?}`；`kp` `skill` 由能力结构算出；`intro` `sz` `ai` 截取前 110 字 |
| `projectOverrides` | 写 | 在 `book.meta.json` 里按项目序号覆盖个别字段，如 `{"16": {"intro": "…", "hours": 6}}`（稿件导读被编辑批注污染时用） |
| `short[]` | 写 | 项目简称 2–5 字，数量 = 项目数；用于项目环、知识网络、表格 |
| `stages[]` | 写 | `[阶段名, [项目序号…], 颜色]`，3–6 个阶段，恰好覆盖每个项目一次；颜色从调色板取：`#2bb5c9 #4f7df3 #8b6cf0 #ef5e9c #35b37e #f29a3a` |
| `stat` | 录 + 算 | 录入：`video ppt doc img quiz cases vr cards nodes modules`；计算：`kp skill step sz cert ai`；`projects` `tasks` 页面自算 |
| `capability` | 抽 | 五级能力结构，见第 6 节；没有填 `null` |
| `jobs[]` | 算 | `[名称, 对接任务占比%, "x / N 个任务"]`，由 `capability.stats.certCoverConfirmed` 与 `jobLabels` 生成；无能力结构时在 meta 里手写 |
| `jobLabels` | 写 | `certs.json` 中的证书名 → 页面全称 |
| `abilities[]` | 写 | 三维目标归纳 `{g: 知识/技能/素质, c: 颜色, items[[能力项, 覆盖项目数]]}`；覆盖项目数要数稿件的学习目标，不要估 |
| `questions` | 写 | 问题图谱：`global[[问题, 关联项目数]]`（3 条）、`proj[[问题, 项目序号]]`（8 条）、`task[[问题, 类型]]`（6 条，类型取 操作/沟通/记录/应急/教育/伦理）；问题来自任务导入情境与任务检测 |
| `ideologyLines[]` | 写 | 思政主线 `[主线名, 颜色, 要点, 分布说明, [项目序号…]]`，4 条，从各项目思政园地归纳 |
| `team[]` | 录 | `[角色, 姓名, 单位, 分工]`，主编、副主编、主审 |
| `policies[]` | 录/默 | `[文件名, 发文单位, 文号, 链接]`，按教材类别更换 |

## 4. 文案 `text.*`

按栏目列出。标“默”的在 `defaults.json` 有通用版本，与教材相关时才覆盖。

**教材导读**
- `guideTitle` `guideLead` 写：一句话标题 + 两三句导语，提到阶段数、项目数、任务数（与统计一致）
- `features` 算：四张特色卡（任务体例 / 思政园地 / 赛证直通 / AI 提问语），数量自动填；体例不同的教材可在 meta 里覆盖
- `audienceRows` 录：`[专业, 课程性质 · 学期, 路径完整度%, 颜色]`；`audienceJobs` 录：面向岗位
- `objectiveSummary` 写：`{知识目标, 技能目标, 素质目标}` 各一句概括
- `modesViz` 默：四种学习模式

**核心数据 / 内容导航**
- `imageLabel` 默：图像资源的叫法（操作图像 / 舌脉图像）
- `denseHours` 默、`unitHours` 默：建议学时
- `stripWords` 写：项目名中可省略的公共词（用于图表短标签），如 `["老年人照护","老年疾病"]`
- `hard {key[], hard[], digital}` 写：重点、难点各 4 条，来自项目导读与学习目标；`digital` 一句话说明难点的数字化处理

**知识图谱 / 能力图谱**
- `relatedNote` 写：跨项目关联的一句解释（“同一知识在不同疾病情境中复现”）
- `stepsNote` 写：流程来源说明
- `learnRole` 写：学习路径第二步“进入任务情境”的说明（“以照护员身份接任务”）
- `certColumns` 写：岗课赛证明细表的列 `[证书名（与 certs.json 一致）, 一字类型 赛/证/标, 颜色]`
- `sampleTaskLabel` 写：示例任务的叫法（“项目三任务 1”）

**问题图谱**
- `questionProjSub` 写：项目层问题的副标题（“从疾病照护角度分解”）
- `questionChain` 写：4 步问题链 `[环节, 问题, 回答, 出处任务]`，取一个真实任务情境

**任务体验**
- `taskFlow` 默、`taskFlowMain` 默：任务体例环节与课堂主线
- `sampleTask` 写：`{project, task, scene, steps[[环节, 做法]×4]}`，用稿件原文情境
- `outcomes` 默：成果要求三栏

**赛证直通 / 岗课赛证**
- `certBadges` 写：`[证书, 说明, 颜色]`，只列稿件点名的证书与赛项
- `certModules` 写：赛项模块 `[模块, 覆盖任务说明, 考核内容]`
- `certTableCert` `certTableModule` 写：覆盖明细表默认显示的证书与模块
- `jobProfiles` 写：岗位画像 `[岗位, 能力要点, 颜色, 覆盖%]`
- `courseStandard` 写：课程标准对标两段

**配套资源 / 数智学习**
- `media` 写：`[资源名, stat 字段名, 说明]`
- `quizTypes` 录：题型与数量
- `vrNote` 写：虚仿项目
- `aiPromptProject` 写：展示 AI 提问语的项目序号；`aiCounterQuestion` 写：AI 反问示例
- `aiScenes` 默、`modes` 默、`presalesQuestions` 默

**学习评价**
- `rubric` 默、`evalWays` 默

**教师端**
- `teacherSummary` 写：选用摘要四卡 `[标题, 结论, 说明]`
- `advantages` 写：核心优势六卡
- `recommendation` 写：推荐理由一段
- `majorsTable` 录：`[专业, 课程性质, 学期, 学时, 适配度 a/b/c]`
- `coursePosition` 写：课程体系位置、对标课程标准
- `hoursPlan` 录：总学时；`examWeeks` 默：阶段考核周
- `members` 录：编委 `[角色, 姓名, 单位, 负责项目]`；`orgs` 录：单位分布 `[类型, 数量]`
- `teachingPhases` 写：三个教学阶段；`teachingTips` 默；`teacherTools` 默
- `teacherFit` 写：适配结论四卡；`reviewDocs` 默
- `contentLogic` 写：纵向 / 横向内容逻辑

**院校端**
- `schoolVerdict` 默、`publisherNote` 默、`publisherFull` 默
- `editorNote` 录：主编资质一句
- `schoolConclusion` 写：审选结论前半句（页面自动接使用数据与建议）
- `reviewProcess` 默
- `standardHead` 写：专业标准表头；`standardItems` 写：`[标准要求, 本书对应项目, a/b]`；`standardConclusion` 写：一段，数字与统计一致
- `qualitySix` 写：科学性 / 先进性 / 系统性 / 职业性 / 实践性 / 育人性各一句
- `feedback` 录：院校反馈 `[身份, 原话, 署名]`；没有填 `[]`
- `achievement` 录：`[成果名, 说明]`

## 5. 平台通用（一般不改）

`defaults.json` 里的 `publisher` `plans` `policies`（前三项与最后一项）、`text.aiScenes` `modes` `modesViz` `taskFlow` `rubric` `reviewDocs` `teacherTools` `presalesQuestions` 等。

## 6. capability（能力结构）

由 `gen_capability.py` 生成，结构：

```
{ projects: [{ n, title,
      tasks: [{ title, steps[{t, a[]}], skills[{d 维度, v 分值, i[[标准, 分值]]}], know[{t 知识点, s[] 细目}],
                support[[知识点序号, 维度序号, 标准序号, 关键词]], cert, certTags[], certQuiz, certPending, ideology }],
      ladder: [{ layer 认知层/实践层/拓展层, desc, m 模块, p[] 能力点, scene, std, act }] }],
  related: [[[项目, 任务序号, 知识点序号], [同左], 关键词], …],
  stats: { tasks, steps, skills, know, knowSub, support, related, ladder, certCover{}, certCoverConfirmed{}, certAny, certStated, certPending, ideology } }
```

`support` 与 `related` 是按共有关键词预生成的，页面标注“AI 预生成，待编辑审核”；不要手工编辑这个文件，要改就改抽取规则重跑。
