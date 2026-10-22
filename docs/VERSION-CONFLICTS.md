# 版本差异记录

同名技能出现不同版本时记在这里，等主人决定合并方式（方案说明见 [SYNC-AND-DEDUP.md](SYNC-AND-DEDUP.md#三版本不同时如何合并)）。决定后在「状态」里写明结果。

## 2026-10-22 · Claude 同步时发现

### `frontend-design`（skills/01-web-ui/frontend-design）

- **差异**：只有 `SKILL.md` 第 39 行一个词。仓库版写的是 “Anthropic's own **Codex**-interaction accent”，Claude 本机版（上游原文）写的是 “Anthropic's own **Claude**-interaction accent”。
- **判断**：两份是同一个上游技能（Anthropic，Apache-2.0）。仓库版是上传时把 “Claude” 批量替换成 “Codex” 造成的，这一处替换让句子意思不对（#D97757 是 Claude 的强调色，不是 Codex 的）。
- **建议**：方案 B，用上游原文替换仓库版。
- **状态**：待主人决定。

### `web-motion-reference`（skills/03-animation-video/web-motion-reference）

- **差异**：只有 `SKILL.md` 第 2 行格式不同：Claude 本机版是 `name: "web-motion-reference"`（带引号），仓库版是 `name: web-motion-reference`（不带引号）。正文和其余 22 个文件完全一致。
- **判断**：两份含义相同，YAML 解析结果一样，属于纯格式差异。
- **建议**：方案 A，保留仓库版，无需处理。
- **状态**：待主人确认。

### 同名不同来源（不算冲突，已作为变体并存）

| 原始名 | 仓库已有 | 本次处理 |
|---|---|---|
| `skill-creator` | OpenAI 版 `skill-creator` | Anthropic 版收录为 `claude--skill-creator`（含评测、描述优化、打包脚本）。安装名都是 `skill-creator`，同一目录只能装一个。 |
| `pdf` | OpenAI 插件版 `pdf--pdf` | Claude 官方版许可禁止平台外复制，只登记为 `claude--pdf`（catalog-only）。 |
| `cli` | Hugging Face 的 `hugging-face--cli` | Canva 的命令行技能原始名是 `canva-cli`，收录为 `canva--cli`，没有冲突。 |
