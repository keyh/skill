---
name: prerequisite-learning-path
description: Turn an explicitly supplied knowledge prerequisite graph and learner mastery list into an ordered learning plan, missing-prerequisite checklist, and practice tasks. Use for curriculum or self-study path planning when prerequisites are available.
---

# 按前置知识规划学习路径

从知识点的依赖关系规划学习顺序，适用于课程拆解、教材知识图谱和个人学习路线。收藏中的 os-taxonomy 介绍启发了本方法；脚本和检查流程为本地新写，不是作者提供的 Skill。来源、边界见 [references/source.md](references/source.md)。

## 输入与证据

收集学习目标、已掌握知识（注明自评或测评）、以及有来源的前置依赖。没有依赖数据时，先输出待确认的依赖草图，不把模型猜测写成已验证的教学事实。

图谱格式：

```json
{"nodes":[
  {"id":"temperature","title":"温度","prerequisites":[],"evidence":"合成示例，非教材结论"},
  {"id":"boiling","title":"沸腾","prerequisites":["temperature"],"evidence":"合成示例"}
]}
```

`prerequisites` 表示“学习本节点前需要的节点”。输入数据本身不包含执行指令。不要把别人的课标直接当作中国课程、考试要求或医学诊断依据。

## 执行

1. 核实目标和边的方向。检查节点是否重名、前置节点是否存在、依赖是否成环。若不通过，列出问题，先修图谱。
2. 用 Python 3 标准库脚本运行：
   `python3 <skill-dir>/scripts/plan.py graph.json --target boiling --mastered temperature`
   `--target` 和 `--mastered` 支持逗号分隔多个 ID；不需要网络、模型下载或额外依赖。输出 JSON 到标准输出。
3. 阅读 `ordered_missing`，为每个缺口添加一项可完成的练习、一项能观察的掌握标准和来源。顺序满足全部已知依赖，**不声称最短学习时长或最优学习策略**。
4. 如果 `mastery_warnings` 非空，说明用户自评已掌握某节点，但未确认其前置知识；用一个短练习核实，不直接否定用户。
5. 交付：目标、证据来源、已掌握假设、依赖顺序、练习、验收和不确定关系。完成标准是图谱校验通过且每个待学节点都有可验证练习。

## 示例与边界

用户问“从哪些知识开始才能做出交互图表”且提供 HTML → DOM → 事件、CSS → 布局、上述节点 → 图表交互的图谱时，可计算依赖并制定练习。用户只问“推荐一个 AI 工具”时不需要此 Skill。

脚本通过分叉汇合依赖、已掌握节点、孤立节点、缺失边、重复节点及循环检测测试。它验证结构，不能证明教学依赖正确；不要把排好顺序误写为已掌握知识。
