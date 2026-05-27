#!/usr/bin/env python3

import argparse
import json

from tier_utils import (
    _request_with_retry,
    compute_direct_tier_score,
    lookup_openalex_source,
    lookup_openalex_source_by_name,
    OPENALEX_SOURCES,
)


def lookup_by_issn(issn, mailto=None):
    return lookup_openalex_source(issn, mailto=mailto)


def lookup_by_name(name, mailto=None):
    return lookup_openalex_source_by_name(name, mailto=mailto)


def format_source(source):
    stats = source.get("summary_stats", {})
    return {
        "name": source.get("display_name", ""),
        "issn_l": source.get("issn_l", ""),
        "issn": source.get("issn", []),
        "type": source.get("type", ""),
        "host_organization": source.get("host_organization_name", ""),
        "2yr_mean_citedness": stats.get("2yr_mean_citedness"),
        "h_index": stats.get("h_index"),
        "i10_index": stats.get("i10_index"),
        "works_count": source.get("works_count"),
        "is_in_doaj": source.get("is_in_doaj"),
        "is_oa": source.get("is_oa"),
        "tier_score": compute_direct_tier_score(openalex_data=source),
    }


def main():
    parser = argparse.ArgumentParser(description="Look up journal/conference tier info via OpenAlex Sources API")
    parser.add_argument("--issn", default=None, help="ISSN to look up (e.g. 0028-0836)")
    parser.add_argument("--name", default=None, help="Journal or conference name to search")
    parser.add_argument("--email", default=None, help="Email for OpenAlex fast pool")
    args = parser.parse_args()
    if not args.issn and not args.name:
        parser.error("At least one of --issn or --name is required")

    results = []
    if args.issn:
        source = lookup_by_issn(args.issn, mailto=args.email)
        if source:
            results.append(format_source(source))
        else:
            results.append({"issn": args.issn, "error": "not found"})
    if args.name:
        source = lookup_by_name(args.name, mailto=args.email)
        if source:
            results.append(format_source(source))
        else:
            results.append({"name": args.name, "error": "not found"})
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
