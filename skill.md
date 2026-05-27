---
name: citation-finder
description: Find and insert citation support for academic claims. Identifies statements requiring literature backing, searches scholarly databases (OpenAlex, Crossref, Zotero, Exa, Google Scholar), ranks results by recency (40%), journal tier (30%), and support degree (30%), and inserts citations into the original text. Use when the user asks to find citations, add references, support claims with literature, locate papers for specific statements, or any task involving citation, reference, literature support, 文献支撑, 引用, 找文献, cite, or adding academic backing to text.
---

# Citation Finder

为用户的学术文本识别需要文献支撑的声明，搜索真实数据库，评估相关性后将引用插回原文。

## Agent Instructions

**语言**：与用户输入文本同语言回答（中文输入用中文回答，英文输入用英文回答）。代码和命令输出用英文。

**行为底线**：
- 永不编造论文、引用、DOI。只返回数据库实际命中的结果。
- 论文缺摘要时 support_score 默认低分，**不许**靠标题猜支撑度。
- 找不到支撑文献就直说，**不许**用弱相关论文凑数。
- 精度优先：3 篇强支撑 > 10 篇泛相关。

**输出**：
- `{filename}_annotated.md`：带 `[N]` 编号的原文 + 文末参考文献列表
- `references.bib`：所有引用的 BibTeX
- 简短总结：引用了什么 + 哪些声明没找到支撑

## 主流程（4 步）

整个流程对 agent 而言只有 4 步。其中**搜索阶段是 agent 唯一需要做并行调度的环节**——同一条消息内并行发出 `search_all.py` 和 Zotero MCP 两个调用，本地文件搜索则在 `search_all.py` 完成后由 agent 执行。

**核心原则：每个声明只保留一个 `claim_N.json`，所有步骤 in-place 更新该文件。**

```
┌─ Step 1 输入 + 声明提取 (agent + 脚本)
│   读文件 → claim_extractor.py 切句+过滤 → claims.json
│   读取 claims.json 逐声明搜索（>30词截断，中文翻英文）
│
├─ Step 2 搜索 (分步)
│   (1) 网页搜索：search_all.py → claim_N.json
│   (2) 本地文件：用户指定时，agent 搜索指定文件，相关且未重复的论文加入 claim_N.json
│   (3) Zotero MCP：可用时搜索，未重复的论文 merge 进 claim_N.json
│
├─ Step 3 支撑度评估 + 排序筛选 (脚本)
│   support_llm.py 填 support_score (0~1 浮点数)
│   enrich-tiers 算 composite_score
│   rank_and_filter.py 排序 + 筛选（≤10 篇，unverified ≤3 且仅 strong+partial<5 时才推）
│
└─ Step 4 输出 (agent + 脚本)
    合并所有 claim_N.json → final_papers.json
    final_papers.json → format_bibtex.py → references.bib
    agent 写 {filename}_annotated.md
```

`search_all.py` 内部 3 路并行（线程1: OpenAlex+Crossref / 线程2: Exa / 线程3: Google Scholar），自动去重 + 黑名单过滤 + 补算 tier/recency。`merge` 子命令复用同样的去重和补算逻辑来合并 Zotero 结果。这些都不是 agent 关心的事，agent 只调脚本即可。

---

## Step 1：输入 + 声明提取

### 1.1 读文件

| 格式 | 处理 |
|------|------|
| 直接文本 | 直接使用 |
| `.md` | Read 工具读取，保留结构 |
| `.tex` | 解析 `\cite{}`，已引用的句子跳过 |
| `.pdf` | PyMuPDF/pdfplumber 提取 |
| `.docx` | python-docx 提取 |

### 1.2 长度路由

| 长度 | 模式 |
|------|------|
| ≤ 1 句（~100 字） | 单句模式：直接搜索 |
| 1 段 ~ 1 节（~100-3000 字） | 段落模式：`claim_extractor.py` 切句+过滤 → 逐声明搜索 |
| > 3000 字 | 长文模式：分批处理 |

### 1.3 声明提取（段落模式）

段落模式下，用 `claim_extractor.py` 自动处理：

```bash
python scripts/claim_extractor.py \
  --input "段落文本" \
  --output claims.json

# 或从文件读取
python scripts/claim_extractor.py \
  --input-file input.md \
  --output claims.json
```

脚本按标点切句 → 过滤无需引用的句子 → >30 词截断 → 输出 `claims.json`。切句和过滤的详细规则见 [references/claim-types.md](references/claim-types.md)。

---

## Step 2：搜索（分步）

6 个搜索源（OpenAlex / Crossref / Exa / Google Scholar / 本地文件 / Zotero MCP），前 4 个由 `search_all.py` 内部并行，本地文件和 Zotero 由 agent 执行。详见 [references/search-strategy.md](references/search-strategy.md)。

### (1) 网页搜索

每个声明调一次 `search_all.py`，所有声明可并行：

```bash
python scripts/search_all.py \
  --query "Zadeh paradox Dempster rule counterintuitive" \
  --email user@example.com \
  --output claim_1.json
```

### (2) 本地文件搜索（可选）

用户指定了本地文件时，agent 读取指定文件，检查是否有与某个声明相关且尚未在 `claim_N.json` 中的论文。如果有，按统一字段格式加入 `claim_N.json`。未指定则跳过。

### (3) Zotero MCP 搜索

Zotero MCP 可用时，依次搜索与各声明相关的文献。

**搜索方式**：使用 `mcp_zotero-mcp_search_library` 工具，**fulltext 模式**搜索，直接用 claim 原文作为查询（不提取关键词），每条声明最多返回 10 条结果：

```
mcp_zotero-mcp_search_library(
    fulltext="{claim原文}",
    fulltextMode="both",
    limit=10,
    mode="standard"
)
```

**参数说明**：
- `fulltext`：搜索查询，直接用 claim 的 original 字段（已判断需要引用的声明原文），不做关键词提取
- `fulltextMode="both"`：同时搜索附件 PDF 全文和笔记
- `limit=10`：每条声明最多返回 10 条

Agent 拿到 MCP 返回结果后，提取每篇论文的元数据（title/authors/year/doi/venue/abstract），按统一字段格式写入 `zotero_N.json`，然后调用 `merge` 子命令合并：

```bash
python scripts/citation_finder.py merge \
  --claim claim_N.json \
  --zotero zotero_N.json \
  --email user@example.com

del zotero_N.json
```

Zotero MCP 不可用时，静默跳过，最后告知用户。

### search_all.py 关键参数

`--query`（必填）/ `--limit 10` / `--year-from` / `--email` / `--use-proxy`（Google Scholar 防封）/ `--output`

完整参数和搜索源细节见 [references/search-strategy.md](references/search-strategy.md)。

---

## Step 3：支撑度评估 + 排序

### 三项分数

每篇论文最终的 `composite_score` 由三项加权而成：

```
composite_score = tier_score × 0.3 + support_score × 0.3 + recency_score × 0.4
```

**tier_score**（期刊/会议等级）— 由 `search_all.py` 自动填好，agent 不算。详见 [references/journal-tiers.md](references/journal-tiers.md)。

**recency_score**（时效性）— 同样由脚本自动填好。详见 [references/journal-tiers.md](references/journal-tiers.md)。

**support_score**（支撑度）— Step 3 的核心工作。LLM 输出 0~1 浮点数评分。`.env` 已配 `USE_LLM_SUPPORT=true`，默认调 LLM：

```bash
python scripts/support_llm.py \
  --claim "声明文本" \
  --papers claim_N.json \
  --skip-scored
```

评分参考：0.9-1.0 直接验证 / 0.6-0.8 相关但未直接验证 / 0.3-0.5 背景知识 / 0.0-0.2 矛盾或无法判断。详见 [references/support-grading.md](references/support-grading.md)。

### 算 composite

`support_llm.py` 填完 support_score 后，再跑一次 `enrich-tiers` 即可算出 composite_score（脚本检测到 support 不为 None 会自动算）：

```bash
python scripts/citation_finder.py enrich-tiers \
  --input claim_N.json \
  --email user@example.com
```

### 排序与筛选

`rank_and_filter.py` 按 composite_score 降序排序，自动执行筛选规则：

1. 每声明保留 ≤ **10 篇**
2. support_score < 0.3 的论文（unverified）≤ **3 篇**，且仅 support_score ≥ 0.6（strong+partial）不足 5 篇时才推
3. unverified 论文在参考文献列表标注 ⚠️

```bash
python scripts/rank_and_filter.py --input claim_N.json
```

---

## Step 4：输出

### 流程

```
合并所有 claim_N.json → final_papers.json
  → python scripts/format_bibtex.py --input final_papers.json --output references.bib
  → agent 写 {filename}_annotated.md（原文 + [N] + 文末列表）
```

### 输出目录

```
输出目录/
├── claim_1.json ... claim_N.json   各声明候选论文（含完整分数）
├── {filename}_annotated.md         原文 + 引用标记 + 文末参考文献
├── references.bib                  BibTeX 条目
└── final_papers.json               合并所有声明后的最终论文列表
```

### 引用标记规则

- 数字编号：`[1]`、`[1,2,3]`
- 同一声明内多篇按 composite_score 降序编号
- 不同声明搜到同一篇论文只分配一个编号

### `{filename}_annotated.md` 范本

```markdown
Deep learning has revolutionized protein structure prediction [1,2,3].
Transformer architectures have become the dominant paradigm in NLP [4,5].

---

## References

[1] Jumper, J., Evans, R., et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*, 596, 583-589. doi:10.1038/s41586-021-03819-2 【support=0.95 | Nature | tier=1.0】

[2] Baek, M., et al. (2021). Accurate prediction of protein structures and interactions using a three-track neural network. *Science*, 373(6557), 871-876. doi:10.1126/science.abj8754 【support=0.90 | Science | tier=1.0】

[3] Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS*. 【support=0.85 | CCF-A | tier=1.0】

[4] Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL*. 【support=0.45 | CCF-A | tier=1.0】

[5] Radford, A., et al. (2019). Language models are unsupervised multitask learners. *OpenAI*. ⚠️未验证 【support=0.20 | tier=0.3】
```

---

## 异常处理

| 场景 | 处理 |
|------|------|
| API 无结果 | 调整查询词重试 1 次，仍无则依赖其他源 |
| 所有源均无结果 | 明确告知"未找到支撑文献"，建议手动搜索 |
| Zotero MCP 不可用 | 静默跳过，最后告知用户 |
| PDF/Word 解析失败 | 告知用户，建议提供纯文本 |
| LLM 调用失败 | Fallback 到 agent 评估摘要 |

---

## 脚本入口速查

agent 直接调用的只有这 8 个：

| 脚本 | 用途 | 调用时机 |
|------|------|---------|
| `scripts/claim_extractor.py` | 切句 + 过滤 + 截断 | Step 1，段落模式下使用，输出 `claims.json` |
| `scripts/search_all.py` | 4 源并行搜索（OpenAlex/Crossref/Exa/Google Scholar） | Step 2(1)，每个声明调一次，输出 `claim_N.json` |
| `scripts/citation_finder.py merge` | 合并 Zotero 结果 + 补算 tier/recency | Step 2(3)，Zotero 结果拿到后调一次，写回 `claim_N.json` |
| `scripts/citation_finder.py enrich-tiers` | 算 composite_score | Step 3，support_llm 之后调一次，写回 `claim_N.json` |
| `scripts/citation_finder.py search` | 单独搜索 OpenAlex/Crossref | 调试用，agent 一般不直接调 |
| `scripts/support_llm.py` | LLM 支撑度评估（0~1 浮点数） | Step 3，写回 `claim_N.json` |
| `scripts/rank_and_filter.py` | 排序 + 筛选（≤10 篇，unverified 规则） | Step 3，enrich-tiers 之后调一次，写回 `claim_N.json` |
| `scripts/format_bibtex.py` | 生成 BibTeX | Step 4 |

---

## 参考文档

| 文件 | 内容 |
|------|------|
| [references/data-schema.md](references/data-schema.md) | 统一数据结构字段定义、各层转换规则、合并优先级 |
| [references/claim-types.md](references/claim-types.md) | 三层融合判断框架、话语角色分类详解、信号词表 |
| [references/search-strategy.md](references/search-strategy.md) | 6 源细节、API 调用、查询构造、去重逻辑 |
| [references/journal-tiers.md](references/journal-tiers.md) | tier_score 评分表、recency_score 评分表、会议白名单 |
| [references/support-grading.md](references/support-grading.md) | 支撑度浮点评分标准、摘要比对方法、unverified 规则 |
| [references/api-reference.md](references/api-reference.md) | OpenAlex / Crossref API 端点、参数、字段速查 |
