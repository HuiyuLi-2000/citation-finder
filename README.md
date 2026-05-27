# Citation Finder

为学术文本自动识别需要文献支撑的声明，搜索真实学术数据库，评估相关性后将引用插回原文。

> ⚠️ 永不编造论文、引用或 DOI。只返回数据库实际命中的结果。

## 特性

- **6 源搜索**：OpenAlex / Crossref / Exa / Google Scholar / 本地文件 / Zotero MCP
- **智能声明提取**：自动切句、过滤无需引用的句子、长句截断
- **三维评分排序**：期刊等级 (30%) + 支撑度 (30%) + 时效性 (40%)
- **LLM 支撑度评估**：可选接入 OpenAI 兼容 API，对论文-声明匹配度打分
- **多格式输出**：带引用标记的 Markdown + BibTeX

## 工作流程

```
┌─ Step 1  输入 + 声明提取
│   读文件 → claim_extractor.py 切句+过滤 → claims.json
│
├─ Step 2  搜索
│   (1) search_all.py → 4 源并行搜索 → claim_N.json
│   (2) 本地文件搜索（可选）
│   (3) Zotero MCP 搜索（可选）
│
├─ Step 3  支撑度评估 + 排序筛选
│   support_llm.py → support_score
│   enrich-tiers → composite_score
│   rank_and_filter.py → 排序 + 筛选
│
└─ Step 4  输出
    format_bibtex.py → references.bib
    agent 写 {filename}_annotated.md
```

## 安装

```bash
pip install -r requirements.txt
```

依赖说明：

| 包 | 必需 | 说明 |
|---|---|---|
| `requests` | ✅ | OpenAlex / Crossref API 调用 |
| `exa-py` | ❌ | Exa 搜索，未安装时自动跳过 |
| `scholarly` | ❌ | Google Scholar 搜索，未安装时自动跳过 |

## 配置

在项目根目录创建 `.env` 文件：

```env
EXA_API_KEY=your_exa_api_key
USE_LLM_SUPPORT=true
LLM_API_KEY=your_llm_api_key
LLM_API_ENDPOINT=your_endpoint
LLM_MODEL=your_model
```

| 变量 | 必需 | 说明 |
|---|---|---|
| `EXA_API_KEY` | ❌ | Exa 搜索 API Key，不配置则跳过 Exa 源 |
| `USE_LLM_SUPPORT` | ❌ | 是否启用 LLM 支撑度评估，默认 false |
| `LLM_API_KEY` | ❌ | LLM API Key，启用 LLM 评估时必需 |
| `LLM_API_ENDPOINT` | ❌ | OpenAI 兼容的 API 端点 |
| `LLM_MODEL` | ❌ | 模型名称 |

## 使用
本项目是一个通用Skill，供 AI Agent 参考安装和调度执行。以下为 Agent 运行时的完整流程。

### 完整流程（4 步）

**Step 1 — 声明提取**

```bash
python scripts/claim_extractor.py --input-file input.md --output claims.json
```

**Step 2 — 搜索**

```bash
python scripts/search_all.py \
  --query "deep learning protein structure prediction" \
  --email your@email.com \
  --output claim_1.json
```

**Step 3 — 评分 + 排序**

```bash
# LLM 支撑度评估（可选）
python scripts/support_llm.py --claim "声明文本" --papers claim_1.json --skip-scored

# 计算 composite_score
python scripts/citation_finder.py enrich-tiers --input claim_1.json --email your@email.com

# 排序筛选
python scripts/rank_and_filter.py --input claim_1.json
```

**Step 4 — 输出**

```bash
python scripts/format_bibtex.py --input final_papers.json --output references.bib
```

### 单独搜索（调试用）

```bash
python scripts/citation_finder.py search \
  --query "transformer attention mechanism" \
  --sources openalex crossref \
  --email your@email.com \
  --output results.json
```

## 评分体系

每篇论文的 `composite_score` 由三项加权：

```
composite_score = tier_score × 0.3 + support_score × 0.3 + recency_score × 0.4
```

| 维度 | 权重 | 说明 |
|---|---|---|
| `tier_score` | 0.3 | 期刊/会议水平（Nature/Science → CCF-A → …） |
| `support_score` | 0.3 | 论文对声明的支撑程度（LLM 或 agent 评估，0~1） |
| `recency_score` | 0.4 | 发表时效性 |

筛选规则：每声明 ≤ 10 篇，支撑度 < 0.3 的论文 ≤ 3 篇且仅在强支撑不足时保留。

## 输出示例

```markdown
Deep learning has revolutionized protein structure prediction [1,2,3].

---

## References

[1] Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold.
    *Nature*, 596, 583-589. 【support=0.95 | Nature | tier=1.0】

[2] Baek, M., et al. (2021). Accurate prediction of protein structures and interactions.
    *Science*, 373(6557), 871-876. 【support=0.90 | Science | tier=1.0】

[3] Radford, A., et al. (2019). Language models are unsupervised multitask learners.
    *OpenAI*. ⚠️未验证 【support=0.20 | tier=0.3】
```

## 项目结构

```
citation-finder/
├── .env                        # API 密钥配置（不入库）
├── requirements.txt
├── skill.md                    # Agent 指令文档
├── data/
│   ├── blacklist_journals.csv  # 期刊黑名单
│   └── priority_journals.csv   # 优先期刊列表
├── scripts/
│   ├── claim_extractor.py      # 声明提取
│   ├── citation_finder.py      # 搜索入口 + merge/enrich-tiers 子命令
│   ├── search_all.py           # 4 源并行搜索
│   ├── exa_search.py           # Exa 搜索
│   ├── search_google_scholar.py # Google Scholar 搜索
│   ├── support_llm.py          # LLM 支撑度评估
│   ├── rank_and_filter.py      # 排序筛选
│   ├── format_bibtex.py        # BibTeX 生成
│   ├── dedup.py                # 去重
│   ├── tier_utils.py           # 期刊等级计算
│   └── journal_tier_lookup.py  # 期刊等级查询 CLI
└── references/
    ├── api-reference.md        # OpenAlex / Crossref API 速查
    ├── claim-types.md          # 声明分类与过滤规则
    ├── data-schema.md          # 统一数据结构定义
    ├── journal-tiers.md        # 期刊等级评分表
    ├── search-strategy.md      # 搜索源策略详解
    └── support-grading.md      # 支撑度评分标准
```
