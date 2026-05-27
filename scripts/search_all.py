#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from citation_finder import search as api_search, year_normalize
from dedup import deduplicate
from exa_search import search_exa
from search_google_scholar import search_google_scholar

try:
    from tier_utils import compute_paper_tier_score, filter_blacklisted
    _TIER_AVAILABLE = True
except ImportError:
    _TIER_AVAILABLE = False


def _enrich_tiers(papers: list[dict], email: str | None = None) -> list[dict]:
    if not _TIER_AVAILABLE:
        return papers
    for paper in papers:
        if paper.get("tier_score", 0) > 0:
            continue
        paper["tier_score"] = round(compute_paper_tier_score(paper, mailto=email), 4)
        paper["recency_score"] = round(year_normalize(paper.get("year")), 4)

    for paper in papers:
        if paper.get("support_score") is not None and paper.get("composite_score") is None:
            tier = paper.get("tier_score", 0) or 0
            recency = paper.get("recency_score", 0) or 0
            support = paper.get("support_score", 0) or 0
            paper["composite_score"] = round(tier * 0.3 + support * 0.3 + recency * 0.4, 4)

    return papers


def search_all(
    query: str,
    limit: int = 10,
    year_from: int | None = None,
    email: str | None = None,
    use_proxy: bool = False,
) -> list[dict]:
    all_results: list[dict] = []
    errors: list[str] = []

    def _run_api():
        try:
            return api_search(query=query, year_from=year_from, limit=limit, email=email, skip_dedup=True)
        except Exception as e:
            errors.append(f"API(OpenAlex+Crossref): {e}")
            return []

    def _run_exa():
        try:
            return search_exa(query=query, max_results=limit, category="research paper")
        except Exception as e:
            errors.append(f"Exa: {e}")
            return []

    def _run_scholar():
        try:
            return search_google_scholar(
                query=query, limit=limit, year_start=year_from,
                sort_by="relevance", use_proxy=use_proxy,
            )
        except Exception as e:
            errors.append(f"GoogleScholar: {e}")
            return []

    tasks = {
        "api": _run_api,
        "exa": _run_exa,
        "scholar": _run_scholar,
    }

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {executor.submit(fn): name for name, fn in tasks.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                count = len(result) if result else 0
                print(f"  [{name}] {count} results", file=sys.stderr)
                if result:
                    all_results.extend(result)
            except Exception as e:
                errors.append(f"{name}: {e}")

    if errors:
        for err in errors:
            print(f"  Warning: {err}", file=sys.stderr)

    print(f"  Total before dedup: {len(all_results)}", file=sys.stderr)
    all_results = deduplicate(all_results)
    all_results = filter_blacklisted(all_results)
    print(f"  Total after dedup:  {len(all_results)}", file=sys.stderr)

    all_results = _enrich_tiers(all_results, email=email)

    return all_results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified parallel search across all citation-finder sources"
    )
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Results per source (default: 10)")
    parser.add_argument("--year-from", type=int, default=None, help="Filter by publication year")
    parser.add_argument("--email", default=None, help="Email for API polite/fast pools")
    parser.add_argument("--use-proxy", action="store_true", help="Use proxy for Google Scholar")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")

    args = parser.parse_args()

    print(f"Searching: {args.query}", file=sys.stderr)
    results = search_all(
        query=args.query,
        limit=args.limit,
        year_from=args.year_from,
        email=args.email,
        use_proxy=args.use_proxy,
    )
    print(f"Final: {len(results)} unique papers", file=sys.stderr)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
