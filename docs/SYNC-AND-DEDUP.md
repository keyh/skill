# 同步与查重规则（所有 AI 通用）

本仓库由多个 AI（Claude、Codex 等）共同备份。**任何 AI 新安装技能后，都按本文件把它同步到这里**，并先查重。目标：同一个技能只存一份；版本不同的不互相覆盖，交给人决定。

## 一、上传前先查重

```bash
git pull
python3 scripts/check_duplicates.py <新技能目录>            # 单个
python3 scripts/check_duplicates.py <技能父目录> --all      # 批量，如 ~/.claude/skills、~/.codex/skills
```

脚本只读，不改任何文件。比较方式：先按原始 `name`（SKILL.md 头部）找同名条目，再逐个文件比 SHA-256（忽略本仓库新增的 `SKILL-INFO.zh-CN.md`、`SOURCE.json`）。

| 结果 | 含义 | 怎么做 |
|---|---|---|
| `IDENTICAL` | 同名且所有文件逐字节一致 | **不上传** |
| `SAME-CONTENT` | 名字不同，但 SKILL.md 与已有条目一致 | **不上传**，告诉主人有别名 |
| `VERSION-DIFFERENT` | 同名，但文件有差异 | **不覆盖**，记到 [VERSION-CONFLICTS.md](VERSION-CONFLICTS.md) 并提醒主人，按下文「版本不同时如何合并」处理 |
| `NEW` | 仓库里没有 | 按下文「新增技能」上传 |

同名但**来源完全不同**（不同作者写的同名技能，例如 OpenAI 和 Anthropic 各自的 `skill-creator`、`pdf`）也会显示 `VERSION-DIFFERENT`。看 `SOURCE.json` 的来源和正文判断：如果是两个不同的技能，就作为「变体」并存（见方案 C），不算版本冲突。

## 二、新增技能

1. 选分类：沿用 `catalog/skills.json` 里的 16 个分类编号（`01-web-ui` … `16-agent-tools`），不要新建分类。
2. 目录：
   - 独立技能 → `skills/<分类>/<原始技能名>/`
   - 插件里的技能 → `plugins/<分类>/<插件名>/skills/<技能名>/`，保留插件整包的相对目录关系
   - 与已有条目同名的变体 → 目录和编号用 `<来源>--<原始名>`，例如 `claude--skill-creator`；`install_name` 仍写原始名
3. 原样复制源文件，**不改动 SKILL.md**；排除 `.DS_Store`、`__pycache__`、`node_modules`、本机安装记录、任何密钥和登录状态。
4. 在技能目录里新增两个文件：
   - `SOURCE.json`：`kind`（local/system/plugin）、`source_root`（例如 `claude-user-synced`、`codex-user`、`claude-plugin-cache`）、`source_relative_path`、`original_skill_sha256`，能确认的再加 `upstream_url`、`version`
   - `SKILL-INFO.zh-CN.md`：中文名、用途、分类、兼容性、依赖、许可、来源（照抄已有文件的格式）
5. 在 `catalog/skills.json` 加条目（字段与已有条目一致），更新顶部各项计数；同步更新 `catalog/skills.csv`、`CATALOG.md` 对应分类表格和标题计数、分类目录下的 `README.md`。
6. 许可检查：如果 LICENSE 明确禁止在平台外保留或复制（例如 Claude 官方 docx/pdf/pptx/xlsx、Codex 官方 documents），**不复制正文**，只在 `skills.json` 里登记为 `"status": "catalog-only"`，并在 [COMPATIBILITY.md](COMPATIBILITY.md#不复制正文的技能) 说明从哪里获取。
7. 重新生成 `catalog/files.sha256.json`（排除 `.git`、Python 缓存和它自身），运行：
   ```bash
   python3 scripts/verify.py
   python3 scripts/test_install.py
   ```
8. 确认仓库仍是私密的，再提交。提交信息写明：新增了哪些、跳过了哪些重复、哪些有版本差异。

## 三、版本不同时如何合并

不要自己决定覆盖。把差异写进 [VERSION-CONFLICTS.md](VERSION-CONFLICTS.md)，然后让主人从下面选一个：

- **方案 A：保留仓库版本**（新版只是本机小改动、或改坏了）——什么都不做，在冲突记录里标「已决定：保留仓库版」。
- **方案 B：用新版本替换**（新版是上游更新、修了问题）——用新文件替换技能目录（保留 `SKILL-INFO.zh-CN.md`），更新 `SOURCE.json` 和 `skills.json` 里的 `original_skill_sha256`、`version`、`source_file_count`，重新生成校验值并验证。旧版在 Git 历史里可找回。
- **方案 C：两个都保留**（来源不同、或两版各有用处）——新版放到 `<来源>--<原始名>` 目录作为变体，编号不同、安装名相同；安装时同一个目录只能选一个。
- **手工合并**（两版各自改了不同地方）——用 `diff -ru <仓库版目录> <新版目录>` 看差异，把需要的改动合并成一份，按方案 B 的步骤更新记录。

查看差异：

```bash
diff -ru skills/<分类>/<技能名> <本机技能目录> -x SKILL-INFO.zh-CN.md -x SOURCE.json
```

## 四、不要做的事

- 不覆盖、不删除别的 AI 上传的条目，除非主人明确同意。
- 不上传账号令牌、密钥、聊天记录、个人记忆、业务资料。
- 不启用 hooks、后台服务、自动更新或 MCP 注册。
- 不把仓库改成公开。
