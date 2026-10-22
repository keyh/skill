# 来源、许可与整理规则

## 快照范围

快照日期为2026-10-22，检查了本机 Codex 用户技能目录、系统技能目录、通用 Agents 技能目录，以及本次会话提供技能的插件包目录。按“技能根目录下存在 `SKILL.md`”统计入口，父技能内嵌的参考技能随父包收录，不重复统计。

- 本地与系统入口：142个。
- 插件入口：200个，其中包括插件内部辅助技能。
- 合计：342个；332个包含源文件，10个仅保留获取说明。

### 2026-10-22 Claude 同步（第二批）

检查了 Claude 的官方技能目录、账号同步技能目录和插件目录（Unity、Canva、设计工作流、3D CAD）。按 [同步与查重规则](SYNC-AND-DEDUP.md) 比对后：

- 45 个与仓库逐字节一致（Unity 31、设计工作流 7、Canva 6、CAD 1），未重复上传。
- 新收录 9 个：`textbook-knowledge-graph`、`claude--skill-creator`、`deep-research`、`docs`、`google-workspace`、`morning`、`import-memory`、`product-self-knowledge`、`canva--cli`。
- 新登记 9 个仅目录记录：Claude 官方 docx、pdf、pptx、xlsx、file-reading、pdf-reading、built-in-browser、chrome-browser、computer-use，其许可禁止平台外复制。
- 2 个同名但版本不同：`frontend-design`、`web-motion-reference`，未覆盖，见 [版本差异记录](VERSION-CONFLICTS.md)。
- Claude 运行环境自带、磁盘上没有文件的辅助技能（如 artifact-design、dataviz、cowork-plugin）未收录。
- 额外发现20个官方模板缓存入口，因本次会话未列为可用插件，只记入 [cache-only.json](../catalog/cache-only.json)，不计入已安装技能数量，也不复制正文。

## 来源记录

`SOURCE.json` 和 [skills.json](../catalog/skills.json) 保留可确认的来源仓库、上游提交、插件版本、原始名称、已知本地修改说明和原始 `SKILL.md` 的SHA-256。缺失的提交号或许可证不补造；“来源项目”不等于已确认当前快照对应某个远端提交。

来自既有 `LOCAL-INSTALL.json` 的仓库与提交信息被提取为来源记录；其中的安装机器运行时绝对路径不进入新的来源记录。原始安装记录被排除，具体见 [exclusions.json](../catalog/exclusions.json)。原始技能正文没有统一改写或翻译，中文说明是另加的文件。

## 许可

各技能、脚本、资产和嵌套组件仍归原作者所有，遵循各自已有的LICENSE、NOTICE及其他适用条款。本仓库不是统一重新授权的发行版，也不因为私密存放就获得额外使用权。

- 存在原许可文件的，随源文件保留；插件根目录的许可与整包一起保存。
- MIT、Apache、AGPL等不同许可分别保留，不能用一个仓库许可证替代。
- Dashi PPT 内含专有导出组件，按完整技能保留原位置及其许可，不作为独立组件提取。其使用范围以该组件原许可为准。
- Unity材料保留Unity Companion许可说明，适用范围以原许可为准。
- 没有找到完整许可文件的，清单明确标注；本次不把“已安装”推定为“可任意公开再分发”。
- 官方Word文档技能存在明确的平台外复制限制，正文和资源未收录，见 [兼容性说明](COMPATIBILITY.md)。Claude 官方的 docx/pdf/pptx/xlsx/file-reading/pdf-reading/浏览器/电脑操作技能同理。
- Claude 的 `deep-research`、`docs`、`google-workspace`、`morning`、`import-memory`、`product-self-knowledge` 本地没有许可文件，按“未发现完整许可文件；不视为获得额外授权”收录，仅供本人私密备份。

## 排除内容

没有复制账号令牌、密钥、AI聊天记录、个人记忆、Git凭据或全局配置。清理了`.DS_Store`、Python缓存、依赖安装目录和本机安装记录。插件的自动工具注册配置、服务端运行环境和hooks没有迁入安装流程。部分原始技能包保留了示例代码或说明文档，这些内容不自动执行。

上传前进行了常见令牌/私钥模式与敏感文件名检查；这种静态检查不能替代所有形式的安全审计。仓库中保存的是用户已安装技能的整理快照，没有重新宣称所有上游代码已通过完整安全审计。

## 后续更新

更新时重新清点来源，不把插件缓存中出现的每个目录自动视为启用状态。保留英文唯一编号、原始来源与许可，重新生成中文目录、JSON/CSV和文件校验值，再验证安装与共享引用。确认仓库仍为私密后提交同步。不要将本机凭据或业务资料混入更新。
