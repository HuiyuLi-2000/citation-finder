#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys

SENTENCE_ENDINGS = re.compile(
    r'(?<=[。！？!?；;：:])\s*'
    r'|(?<=\.)\s*(?!\d)'
    r'|(?<=，)\s*'
    r'|(?<=,)\s*(?!\d)'
    r'|(?<=\n)\s*'
)
MAX_WORDS = 30


MIN_WORDS = 5


def _split_sentences(text: str) -> list[str]:
    raw = SENTENCE_ENDINGS.split(text.strip())
    fragments = [s.strip() for s in raw if s.strip()]
    merged = []
    for frag in fragments:
        if merged and len(frag.split()) < MIN_WORDS:
            merged[-1] = merged[-1] + " " + frag
        else:
            merged.append(frag)
    return merged


def _truncate_long(claim: str) -> str:
    words = claim.split()
    if len(words) <= MAX_WORDS:
        return claim
    return " ".join(words[:MAX_WORDS])


def _needs_citation(claim: str) -> bool:
    claim_lower = claim.lower()

    skip_patterns = [
        r'^(in this paper|in this work|in this study|in this article|we propose|we present|we introduce|we show|we demonstrate|our approach|our method|our contribution)',
        r'^(the remainder of|the rest of|section \d|chapter \d|the following section)',
        r'^(table \d|figure \d|algorithm \d|equation \d)',
    ]
    for pat in skip_patterns:
        if re.search(pat, claim_lower):
            return False

    cite_signals = [
        r'has been (shown|proven|demonstrated|established|found)',
        r'it is (well known|widely accepted|generally believed|commonly understood)',
        r'(previous|prior|existing|recent|earlier) (work|study|studies|research|literature|efforts)',
        r'(according to|based on|following) (the|a|previous|prior)',
        r'(important|fundamental|crucial|essential|significant|notable|remarkable)',
        r'(first proposed|introduced by|developed by|demonstrated in)',
        r'(outperform|surpass|exceed|improve upon)',
        r'(state-of-the-art|SOTA|cutting-edge)',
        r'(widely used|commonly used|frequently employed)',
        r'(evidence|empirical|theoretical|experimental) (shows|suggests|indicates|demonstrates)',
    ]
    for pat in cite_signals:
        if re.search(pat, claim_lower):
            return True

    if re.search(r'\b[A-Z][a-z]+ (et al\.|and \w+ )?\(\d{4}\)', claim):
        return True

    factual_patterns = [
        r'\d+\.?\d*%',
        r'\$\d',
        r'(increased|decreased|reduced|improved|achieved) by',
        r'(accuracy|performance|efficiency|effectiveness) of',
    ]
    for pat in factual_patterns:
        if re.search(pat, claim_lower):
            return True

    return True


def extract_claims(text: str) -> list[dict]:
    sentences = _split_sentences(text)
    claims = []

    for i, sent in enumerate(sentences):
        if not _needs_citation(sent):
            continue
        query = _truncate_long(sent)
        claims.append({
            "id": i + 1,
            "original": sent,
            "query": query,
            "truncated": len(sent.split()) > MAX_WORDS,
        })

    return claims


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract citation-worthy claims from text"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Input text string")
    group.add_argument("--input-file", help="Path to input text file")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file (default: stdout)")

    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                text = f.read()
        except (OSError, IOError) as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return 1
    else:
        text = args.input

    claims = extract_claims(text)

    output = json.dumps(claims, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Extracted {len(claims)} claims → {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
