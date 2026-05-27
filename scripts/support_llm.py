#!/usr/bin/env python3
"""
LLM-based support score evaluation for citation-finder.

Calls an OpenAI-compatible LLM API to evaluate how well papers
support a given claim, returning results in citation-finder's
standard data structure format.

Config (in .env):
    USE_LLM_SUPPORT=true|false
    LLM_API_KEY=your_key
    LLM_API_ENDPOINT=your_endpoint
    LLM_MODEL=your_model

Usage:
    python scripts/support_llm.py --claim "Deep learning revolutionized protein structure prediction" --papers results.json
    python scripts/support_llm.py --claim "..." --papers results.json --output scored.json
    python scripts/support_llm.py --claim "..." --papers results.json --skip-scored
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

SYSTEM_PROMPT = """\
You are an academic citation support evaluator. Given a research claim and a paper's \
metadata (title, abstract, venue, year, authors), evaluate how well the paper supports \
the claim on a continuous scale from 0.0 to 1.0.

Scoring guidelines:
- 0.9-1.0: The paper directly describes, validates, or demonstrates the claim's core assertion.
- 0.6-0.8: The paper is topically related but does not directly validate the claim's specific assertion.
- 0.3-0.5: The paper provides domain background or context but does not directly support the claim.
- 0.0-0.2: The paper presents evidence that contradicts the claim, or support cannot be determined \
(e.g., no abstract available).

Respond with ONLY a JSON object (no markdown, no explanation outside the JSON):
{"support_score": 0.85, "reasoning": "brief one-sentence explanation"}\
"""


def _load_dotenv() -> None:
    env_path = SKILL_DIR / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def _get_config() -> dict[str, str | bool]:
    _load_dotenv()
    return {
        "use_llm_support": os.getenv("USE_LLM_SUPPORT", "false").lower() in ("true", "1", "yes"),
        "api_key": os.getenv("LLM_API_KEY", "").strip(),
        "api_endpoint": os.getenv("LLM_API_ENDPOINT", "").strip(),
        "model": os.getenv("LLM_MODEL", "").strip(),
    }


def _build_user_prompt(claim: str, paper: dict[str, Any]) -> str:
    parts = [f"Claim: {claim}", ""]
    title = paper.get("title", "")
    if title:
        parts.append(f"Paper Title: {title}")
    authors = paper.get("authors", [])
    if authors:
        author_str = ", ".join(authors[:5])
        if len(authors) > 5:
            author_str += " et al."
        parts.append(f"Authors: {author_str}")
    year = paper.get("year")
    if year:
        parts.append(f"Year: {year}")
    venue = paper.get("venue", "")
    if venue:
        parts.append(f"Venue: {venue}")
    abstract = paper.get("abstract", "")
    if abstract:
        max_len = 2000
        if len(abstract) > max_len:
            abstract = abstract[:max_len] + "..."
        parts.append(f"Abstract: {abstract}")
    else:
        parts.append("Abstract: [not available]")
    return "\n".join(parts)


def _parse_llm_response(text: str) -> dict[str, Any]:
    text = text.strip()
    json_match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
    if not json_match:
        return {"support_score": 0.2, "reasoning": "Failed to parse LLM response"}
    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return {"support_score": 0.2, "reasoning": "Invalid JSON in LLM response"}

    raw_score = data.get("support_score")
    try:
        score = float(raw_score)
    except (TypeError, ValueError):
        return {"support_score": 0.2, "reasoning": f"Invalid support_score: {raw_score}"}
    score = max(0.0, min(1.0, round(score, 2)))
    reasoning = data.get("reasoning", "")
    return {"support_score": score, "reasoning": reasoning}


def evaluate_support(
    claim: str,
    paper: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if config is None:
        config = _get_config()

    if not config.get("use_llm_support"):
        return {"support_score": 0.2, "reasoning": "LLM support evaluation disabled"}

    api_key = config.get("api_key", "")
    endpoint = config.get("api_endpoint", "")
    model = config.get("model", "")

    if not api_key or not endpoint or not model:
        return {"support_score": 0.2, "reasoning": "LLM config incomplete (key/endpoint/model)"}

    user_prompt = _build_user_prompt(claim, paper)

    chat_url = endpoint.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 256,
    }

    try:
        resp = requests.post(chat_url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            return {
                "support_score": 0.2,
                "reasoning": f"LLM API error: HTTP {resp.status_code}",
            }
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            return {"support_score": 0.2, "reasoning": "Empty LLM response"}
        return _parse_llm_response(content)
    except requests.RequestException as e:
        return {"support_score": 0.2, "reasoning": f"Request failed: {e}"}
    except (ValueError, KeyError, IndexError) as e:
        return {"support_score": 0.2, "reasoning": f"Parse error: {e}"}


def score_papers(
    claim: str,
    papers: list[dict[str, Any]],
    skip_scored: bool = False,
    delay: float = 0.5,
) -> list[dict[str, Any]]:
    config = _get_config()
    if not config.get("use_llm_support"):
        print("LLM support evaluation is disabled (USE_LLM_SUPPORT not true). Skipping.", file=sys.stderr)
        return papers

    for i, paper in enumerate(papers):
        if skip_scored and paper.get("support_score") is not None:
            print(f"  [{i+1}/{len(papers)}] Skipping (already scored): {paper.get('title', '')[:60]}", file=sys.stderr)
            continue
        print(f"  [{i+1}/{len(papers)}] Evaluating: {paper.get('title', '')[:60]}", file=sys.stderr)
        result = evaluate_support(claim, paper, config=config)
        paper["support_score"] = result["support_score"]
        if result.get("reasoning"):
            paper["support_reasoning"] = result["reasoning"]
        if i < len(papers) - 1:
            time.sleep(delay)

    return papers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate paper support scores using an LLM API"
    )
    parser.add_argument("--claim", required=True, help="The claim to evaluate support for")
    parser.add_argument("--papers", required=True, help="Path to JSON file with paper list")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file (default: overwrite --papers in-place)")
    parser.add_argument("--skip-scored", action="store_true", help="Skip papers that already have support_score")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API calls in seconds (default: 0.5)")

    args = parser.parse_args()

    try:
        with open(args.papers, "r", encoding="utf-8") as f:
            papers = json.load(f)
    except (OSError, IOError, json.JSONDecodeError) as e:
        print(f"Error reading papers file: {e}", file=sys.stderr)
        return 1

    if not isinstance(papers, list):
        papers = [papers]

    print(f"Evaluating support for {len(papers)} papers against claim:", file=sys.stderr)
    print(f"  \"{args.claim[:100]}\"", file=sys.stderr)

    papers = score_papers(
        claim=args.claim,
        papers=papers,
        skip_scored=args.skip_scored,
        delay=args.delay,
    )

    scored = sum(1 for p in papers if p.get("support_score") is not None)
    print(f"Scored: {scored}/{len(papers)} papers", file=sys.stderr)

    output = json.dumps(papers, indent=2, ensure_ascii=False)
    target = args.output or args.papers
    with open(target, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Wrote to {target}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
