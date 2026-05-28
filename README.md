# Citation Finder

Automatically identifies claims in academic text that require literature support, searches real academic databases, evaluates relevance, and inserts citations back into the original text.

> ⚠️ Never fabricate papers, citations, or DOIs. Only return results that actually exist in the databases.

## Features

- **6-Source Search**: OpenAlex / Crossref / Exa / Google Scholar / Local Files / Zotero MCP
- **Smart Claim Extraction**: Automatic sentence splitting, filtering of sentences that don't need citations, and long-sentence truncation
- **Three-Dimensional Scoring & Ranking**: Journal tier (30%) + Support degree (30%) + Recency (40%)
- **LLM Support Evaluation**: Optional integration with OpenAI-compatible APIs to score paper-claim relevance
- **Multi-Format Output**: Markdown with citation markers + BibTeX

## Workflow

```
┌─ Step 1  Input + Claim Extraction
│   Read file → claim_extractor.py sentence splitting + filtering → claims.json
│
├─ Step 2  Search
│   (1) search_all.py → 4-source parallel search → claim_N.json
│   (2) Local file search (optional)
│   (3) Zotero MCP search (optional)
│
├─ Step 3  Support Evaluation + Ranking & Filtering
│   support_llm.py → support_score
│   enrich-tiers → composite_score
│   rank_and_filter.py → ranking + filtering
│
└─ Step 4  Output
    format_bibtex.py → references.bib
    agent writes {filename}_annotated.md
```

## Installation

```bash
pip install -r requirements.txt
```

Dependency details:

| Package | Required | Description |
|---|---|---|
| `requests` | ✅ | OpenAlex / Crossref API calls |
| `exa-py` | ❌ | Exa search; automatically skipped if not installed |
| `scholarly` | ❌ | Google Scholar search; automatically skipped if not installed |

## Configuration

Create a `.env` file in the project root:

```env
EXA_API_KEY=your_exa_api_key
USE_LLM_SUPPORT=true
LLM_API_KEY=your_llm_api_key
LLM_API_ENDPOINT=your_endpoint
LLM_MODEL=your_model
```

| Variable | Required | Description |
|---|---|---|
| `EXA_API_KEY` | ❌ | Exa search API key; Exa source is skipped if not configured |
| `USE_LLM_SUPPORT` | ❌ | Whether to enable LLM support evaluation; defaults to false |
| `LLM_API_KEY` | ❌ | LLM API key; required when LLM evaluation is enabled |
| `LLM_API_ENDPOINT` | ❌ | OpenAI-compatible API endpoint |
| `LLM_MODEL` | ❌ | Model name |

## Usage

This project is a general-purpose Skill designed for AI agents to reference, install, and orchestrate. Below is the complete runtime workflow for an agent.

### Complete Workflow (4 Steps)

**Step 1 — Claim Extraction**

```bash
python scripts/claim_extractor.py --input-file input.md --output claims.json
```

**Step 2 — Search**

```bash
python scripts/search_all.py \
  --query "deep learning protein structure prediction" \
  --email your@email.com \
  --output claim_1.json
```

**Step 3 — Scoring + Ranking**

```bash
# LLM support evaluation (optional)
python scripts/support_llm.py --claim "claim text" --papers claim_1.json --skip-scored

# Compute composite_score
python scripts/citation_finder.py enrich-tiers --input claim_1.json --email your@email.com

# Rank and filter
python scripts/rank_and_filter.py --input claim_1.json
```

**Step 4 — Output**

```bash
python scripts/format_bibtex.py --input final_papers.json --output references.bib
```

### Standalone Search (for debugging)

```bash
python scripts/citation_finder.py search \
  --query "transformer attention mechanism" \
  --sources openalex crossref \
  --email your@email.com \
  --output results.json
```

## Scoring System

Each paper's `composite_score` is computed from three weighted components:

```
composite_score = tier_score × 0.3 + support_score × 0.3 + recency_score × 0.4
```

| Dimension | Weight | Description |
|---|---|---|
| `tier_score` | 0.3 | Journal/venue level (Nature/Science → CCF-A → …) |
| `support_score` | 0.3 | Degree to which the paper supports the claim (LLM or agent evaluation, 0–1) |
| `recency_score` | 0.4 | Publication recency |

Filtering rules: max 10 papers per claim; papers with support < 0.3 are capped at 3 and only retained when strong-support results are insufficient.

## Output Example

```markdown
Deep learning has revolutionized protein structure prediction [1,2,3].

---

## References

[1] Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold.
    *Nature*, 596, 583-589. 【support=0.95 | Nature | tier=1.0】

[2] Baek, M., et al. (2021). Accurate prediction of protein structures and interactions.
    *Science*, 373(6557), 871-876. 【support=0.90 | Science | tier=1.0】

[3] Radford, A., et al. (2019). Language models are unsupervised multitask learners.
    *OpenAI*. ⚠️Unverified 【support=0.20 | tier=0.3】
```

## Project Structure

```
citation-finder/
├── .env                        # API key configuration (not tracked in repo)
├── requirements.txt
├── skill.md                    # Agent instruction document
├── data/
│   ├── blacklist_journals.csv  # Journal blacklist
│   └── priority_journals.csv   # Priority journal list
├── scripts/
│   ├── claim_extractor.py      # Claim extraction
│   ├── citation_finder.py      # Search entry point + merge/enrich-tiers subcommands
│   ├── search_all.py           # 4-source parallel search
│   ├── exa_search.py           # Exa search
│   ├── search_google_scholar.py # Google Scholar search
│   ├── support_llm.py          # LLM support evaluation
│   ├── rank_and_filter.py      # Ranking and filtering
│   ├── format_bibtex.py        # BibTeX generation
│   ├── dedup.py                # Deduplication
│   ├── tier_utils.py           # Journal tier calculation
│   └── journal_tier_lookup.py  # Journal tier lookup CLI
└── references/
    ├── api-reference.md        # OpenAlex / Crossref API quick reference
    ├── claim-types.md          # Claim classification and filtering rules
    ├── data-schema.md          # Unified data structure definition
    ├── journal-tiers.md        # Journal tier scoring table
    ├── search-strategy.md      # Search source strategy details
    └── support-grading.md      # Support scoring criteria
```
