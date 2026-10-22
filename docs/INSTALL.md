# 安装与跨 AI 使用

## 1. 让其他 AI 获得仓库访问权限

仓库地址：[keyh/skill](https://github.com/keyh/skill)。私密仓库不能通过匿名链接读取。

- 在其他 AI 中连接你的 GitHub 账号，并在连接器的仓库授权中允许访问 `keyh/skill`。
- 有本地终端的 AI，可使用你已经授权的 Git 凭据、SSH 或 GitHub CLI 克隆。
- 如果使用单独的 GitHub 账号，需要你在仓库设置中为该账号授予访问权限；仅提供仓库链接不会自动授予权限。
- 不要把令牌写进聊天、脚本、仓库文件或带密码的 URL。本仓库没有复制本机登录信息。

```bash
# 方式一：已登录的 GitHub CLI
gh repo clone keyh/skill
# 方式二：已配置好的 HTTPS 凭据
git clone https://github.com/keyh/skill.git
# 方式三：已配置好的 SSH
git clone git@github.com:keyh/skill.git
```

三种方式选一种即可。完成后进入克隆目录。已有副本更新时先保留自己的修改，再使用 Git 的常规同步流程；不要盲目强制覆盖。

## 2. 校验与选型

```bash
python3 scripts/verify.py
python3 scripts/install.py --list
```

先读 [完整目录](../CATALOG.md)，再读选中技能的 `SKILL-INFO.zh-CN.md`。目录中的唯一编号用于 `--skill` 参数。

```bash
# 选择单个技能
python3 scripts/install.py --skill ppt-master --dest /absolute/path/to/ai-skills --dry-run

# 选择组合
python3 scripts/install.py --preset knowledge --dest /absolute/path/to/ai-skills --dry-run

# 选择整个分类：应先检查其中技能是否符合目标环境
python3 scripts/install.py --category 03-animation-video --dest /absolute/path/to/ai-skills --dry-run
```

确认预览符合需求后，去掉 `--dry-run` 执行。`--dest` 必须使用目标 AI 实际支持的技能目录。安装器不修改 AI 的全局设置。

## 3. Codex 安装示例

```bash
python3 scripts/install.py --skill web-motion-reference --dest "$HOME/.codex/skills" --dry-run
python3 scripts/install.py --skill web-motion-reference --dest "$HOME/.codex/skills"
```

自定义 `CODEX_HOME` 时，请显式把 `--dest` 指向对应的 `skills` 目录。技能是否自动发现、何时刷新，由目标客户端决定；必要时重新打开会话或重启客户端。

也可由目标 Codex 自带的 `skill-installer` 按 GitHub 路径安装**独立技能**，例如 `skills/04-presentations/ppt-master`。插件包的共享资源不一定都在单个技能目录内，因此插件技能优先使用本仓库安装器或原平台的官方插件安装方式。

## 4. 插件来源的技能

```bash
python3 scripts/install.py --skill design--design-critique --dest /absolute/path/to/ai-skills --dry-run
python3 scripts/install.py --skill design--design-critique --dest /absolute/path/to/ai-skills
```

安装器会把完整技能包放入目标目录的 `.skill-bundles/插件名/`，再为选中的技能建立目录符号链接。这样 `../其他技能/` 和 `../../references/` 等相对引用仍然有效。**整包资源被保留，不代表所有入口都已启用。**

这一方式需要系统允许创建目录符号链接；本次验证环境为 macOS。Windows 或不读取符号链接的 AI，请保留克隆目录的完整插件结构，并让 AI 按完整路径读取技能，或者通过该平台的插件管理器安装。不要只复制单个 `SKILL.md`。

本仓库保留技能与配套资料，不包含连接器服务端、登录凭据、全局 hooks 或自动工具注册配置。Figma、Canva、Unity、Google、Notion 等工具需要另外安装或连接，并在目标环境中匹配工具名称。插件命名空间、`${CLAUDE_PLUGIN_ROOT}` 等平台变量也可能需要目标客户端适配。

## 5. 同名、已有版本与卸载

- 安装器拒绝覆盖已有目录或链接。不同来源但原始名称相同的技能，不能在同一次安装中写入同一个名称；应选择一个版本，或使用独立目标目录。
- 对已存在的共享包，安装器只在逐文件内容完全一致时复用；不同快照请先安装到新的目标目录。
- 卸载独立技能：从目标技能目录移除该次安装产生的目录。卸载插件入口：移除该入口的符号链接；仅在没有任何入口使用共享包时，才移除对应 `.skill-bundles/插件名`。
- 移除目标副本不会改动 GitHub 仓库或本机原始安装来源。

## 6. 业务依赖

安装器不下载依赖，不执行第三方脚本，不替你注册外部服务。首次使用时，按选中技能说明配置 Python/Node、Firecrawl、OpenSpec、Remotion、图像工具或 MCP。涉及收费服务、云端上传、消息发送等具体业务操作，应由当前任务授权决定。
