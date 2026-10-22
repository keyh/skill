# 论文与研究资料检索

论文与研究资料检索。适用于网页检索、站点采集、文献研究和竞争分析相关任务；具体输入、步骤和输出见原始技能说明。

- 仓库唯一编号：`firecrawl-research-index`
- 原始技能名：`firecrawl-research-index`
- 分类：搜索与研究
- 兼容性：脚本或工具依赖
- 依赖：需要 Firecrawl CLI 及独立登录或 API 授权；部分操作会使用外部服务额度。
- 许可：本地未发现完整许可文件；不视为获得额外授权
- 来源：https://github.com/firecrawl/skills

## 原始说明

Find the papers that answer a research query in Firecrawl's research paper index — a corpus of paper abstracts whose largest share is biomedical and life-science literature (PubMed, bioRxiv, medRxiv), alongside arXiv preprints in CS, physics, and math — using semantic search, semantic and structural expansion, and in-body verification. Use this skill for literature-finding and paper-retrieval tasks of any kind, including clinical, biomedical, drug, gene, disease, and other life-science questions, whether the answer is a single paper or a full multi-paper set. The index is reached only through the `firecrawl_research_*` MCP tools or the `firecrawl research` CLI subcommands. Calling `firecrawl_search` with its `categories` option set to `["research"]` is a different feature — it filters ordinary web search to research-affiliated websites (the list includes PubMed, bioRxiv, medRxiv, arXiv, and publisher sites) and returns page results from them, without querying the paper records in this index.

[阅读 SKILL.md](SKILL.md) · [完整技能清单](../../../CATALOG.md)
