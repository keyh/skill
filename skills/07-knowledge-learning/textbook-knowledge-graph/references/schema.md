# kg.json 格式

字段名尽量沿用 Marble os-taxonomy（`name` `description` `evidence` `assessmentPrompt` `standards` `centrality`，边的 `topicId` `prerequisiteId` `strength` `reason`），方便对照和复用工具；把“年龄”换成教材的“项目 / 章”，并增加出处与审核状态。

```json
{
  "version": "kg-1",
  "book": { "id": "b09", "title": "老年疾病照护", "major": "…", "level": "高职专科" },
  "units": [ { "n": 3, "title": "高血压老年人照护", "short": "高血压", "stage": "常见慢病" } ],
  "stages": [ ["常见慢病", [2,3,4,5,6,7], "#4f7df3"] ],
  "nodes": [ { …节点… } ],
  "edges": [ { …先修边… } ],
  "hints": [ { "a": "kp_…", "b": "kp_…", "keyword": "健康教育" } ],
  "clusters": [ { "unit": 3, "summary": "…" } ],
  "provenance": { "source": "book.json", "note": "…" }
}
```

## 节点 `nodes[]`

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | `kp_` 开头，字母数字下划线，**发布后不再改**（学习记录、题目都会引用它）。骨架生成的形如 `kp_p03_101`（项目 3、任务 1、第 01 个知识点）；合并或新增的节点用 `kp_base_xxx`、`kp_p03_x01` 之类可读编号 |
| `name` | 是 | 知识点名称，≤ 20 字，用教材里的叫法 |
| `type` | 是 | `CONCEPTUAL` 概念 / `PROCEDURAL` 操作 / `REPRESENTATIONAL` 识读 / `LANGUAGE` 术语 / `META` 素养，含义见 authoring.md |
| `unit` | 是 | 所属项目 / 章序号（整数）。跨项目的基础节点放在它**第一次被讲**的项目 |
| `stage` `domain` | 否 | 阶段名、领域短名（用于着色和分组） |
| `description` | 是 | 一两句话，≤ 120 字：这个知识点讲的是什么、学完能理解或做到什么 |
| `evidence` | 是 | 2–4 条**可观察**的达标证据，以“能”开头 |
| `assessmentPrompt` | 建议 | 一个检测问题，教师可以直接问、AI 可以用来反问。需要称呼学生时写占位符 `{{name}}`，展示前替换成学生称呼或“你”，不写真实姓名 |
| `standards` | 否 | 对接编号，见下文“对接编号” |
| `sub` | 否 | 稿件里的细目（骨架自动带入） |
| `anchors` | 是 | 出处 `[项目, 任务序号, 知识点序号]`，后两位从 0 开始，与 capability.json 一致；合并节点有多个出处 |
| `context` | 否 | 骨架带入的任务名、技能维度、流程、赛证标签，供写作参考；交付前可删 |
| `status` | 是 | `ai` / `reviewed` / `confirmed` / `rejected` |
| `notes` | 否 | 依据说明、待确认事项 |
| `centrality` `depth` `unlocks` | 算 | `analyze.py --write` 写入：中心度（0–1）、所在先修层、可解锁的后续知识点数 |

## 先修边 `edges[]`

```json
{ "topicId": "kp_p03_301", "prerequisiteId": "kp_p03_101", "strength": "hard",
  "reason": "要先能判断血压分级，才能确定监测频率和就医时机", "status": "ai" }
```

- 读法：`topicId` **依赖** `prerequisiteId`；反过来就是“解锁”。
- `strength`：`hard`（不会就学不了）或 `soft`（会了学得更好）。
- `reason`：一句话，说明为什么必须先学，最好点出具体用到了什么。
- `status`：同节点。被编辑否决的边保留并标 `rejected`，分析和页面会忽略它，但可追溯。

## 对接编号 `standards[]`

格式 `来源:编号`，来源在本书内统一：

| 前缀 | 含义 | 示例 |
|---|---|---|
| `skill:` | 本书技能点（任务评价表的维度） | `skill:P3T1-血压测量` |
| `task:` | 本书工作任务 | `task:P3T2` |
| `cert:` | 证书或赛项模块（与 certs.json 名称一致） | `cert:养老护理员:生活照护` |
| `exam:` | 执业资格 / 等级考试大纲条目（只放编号与名称） | `exam:护士执业资格:第三单元` |
| `std:` | 课程标准、专业教学标准条目 | `std:专业教学标准:能力要求3` |

## 编辑提示 `editorial`（可选）

整理全书时发现的编排问题，`analyze.py --report` 会写进报告：

```json
{ "repeats": [ { "base": "kp_p03_403", "baseName": "…", "baseUnit": 3, "repeat": "kp_p05_403", "repeatName": "…", "repeatUnit": 5 } ],
  "forwardUse": [ { "users": ["kp_p03_404"], "userNames": ["…"], "taughtIn": "kp_p16_104", "note": "前面项目已要求使用，后面才系统讲；建议加提示" } ] }
```

- `repeats`：同一通用内容在多个项目重复讲。不跨项目合并节点（每处都有稿件出处），而是用软边把后者连到第一次讲的节点，由编辑决定是否精简。
- `forwardUse`：先用后讲。不建反向边，只作为编排建议。

## 集群摘要 `clusters[]`（可选）

每个项目（或阶段）一段 60–120 字的导读，写给学生：这一块学什么、和前后怎么连。可用于详情页知识图谱栏目的分组说明。
