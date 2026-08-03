"""Selection script for the survey — the definition of record.

CONTRACT.md states the frame in prose; where prose and this script disagree,
this script governs. Run it, freeze its output, publish the SHA256, reveal the
list with the results.

    python select.py                 # retrieve, filter, write, hash
    python select.py --offline       # re-derive list + hash from a saved cache

Two stages, deliberately separated:

  server-side  narrows arXiv to plausible candidates. Convenience only — arXiv's
               phrase handling is not fully specified, so nothing rests on it.
  local        applies the frame exactly, over the abstract text as returned.
               This is the authority. Re-running the local stage over the cache
               reproduces the list byte for byte without touching the network.

What the script does NOT do: decide whether a paper actually reports a figure
about its *own* verification component. That is a reading judgement, made per
paper afterwards and logged with a reason in DETERMINATIONS.md. This script
produces the denominator, not the answer.

Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------- the frame
# Frozen in CONTRACT.md. Changing anything below is a new contract, not an edit.

CATEGORIES = ["cs.SE", "cs.AI", "cs.CL", "cs.LG"]
WINDOW_FROM = "202508010000"   # 2025-08-01, inclusive
WINDOW_TO = "202607312359"     # 2026-07-31, inclusive

COMPONENT_TERMS = [
    "verifier", "verification loop", "validator", "checker",
    "critic", "self-check", "guard", "admission",
]
CLAIM_TERMS = [
    "false accept", "false alarm", "false positive", "precision", "recall",
    "catch rate", "confusion matrix", "detection rate",
]

SAMPLE_CAP = 25
SAMPLE_SEED = 20260802
MIN_FRAME = 10        # below this the frame is too narrow — see stop conditions

API = "http://export.arxiv.org/api/query"
PAGE = 100
DELAY_S = 3.0         # arXiv asks for 3 seconds between requests
NS = {"a": "http://www.w3.org/2005/Atom"}

HERE = Path(__file__).parent
CACHE = HERE / "cache_arxiv.jsonl"
LIST_OUT = HERE / "frame.txt"
META_OUT = HERE / "frame.json"


def _norm(text: str) -> str:
    """Normalise text so hyphen and space are equivalent, on both sides.

    Papers write 'false-alarm rate' where the frame says 'false alarm', and the
    API wraps 'self-check' across a line as 'self- check'. Any of these missed
    silently corrupts a denominator, which is the worst failure this survey has.

    So every run of hyphens and whitespace collapses to one space, and the SAME
    function is applied to the frame's terms before matching. 'self-check',
    'self check' and 'self-\\ncheck' all become 'self check'.
    """
    t = text.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    t = re.sub(r"[-\s]+", " ", t)
    return t.strip().lower()


def matched_terms(text: str, terms: list[str]) -> list[str]:
    """Terms are normalised too — matching is symmetric or it is not a rule."""
    haystack = _norm(text)
    return [t for t in terms if _norm(t) in haystack]


def in_frame(rec: dict) -> tuple[bool, list[str], list[str]]:
    """The frame, applied locally. This is the authority."""
    comp = matched_terms(rec["abstract"], COMPONENT_TERMS)
    claim = matched_terms(rec["abstract"], CLAIM_TERMS)
    in_cat = any(c in rec["categories"] for c in CATEGORIES)
    return (bool(comp) and bool(claim) and in_cat), comp, claim


# ------------------------------------------------------------------ retrieval

def fetch_page(term: str, start: int) -> bytes:
    cats = " OR ".join(f"cat:{c}" for c in CATEGORIES)
    query = (
        f'abs:"{term}" AND ({cats}) '
        f"AND submittedDate:[{WINDOW_FROM} TO {WINDOW_TO}]"
    )
    url = f"{API}?" + urllib.parse.urlencode({
        "search_query": query,
        "start": start,
        "max_results": PAGE,
        "sortBy": "submittedDate",
        "sortOrder": "ascending",
    })
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def parse(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("a:entry", NS):
        raw_id = e.findtext("a:id", "", NS)
        m = re.search(r"abs/([^v]+)v?(\d*)", raw_id)
        if not m:
            continue
        out.append({
            "id": m.group(1),
            "version": m.group(2) or "1",
            "title": _norm(e.findtext("a:title", "", NS)).strip(),
            "abstract": e.findtext("a:summary", "", NS).strip(),
            "published": e.findtext("a:published", "", NS),
            "categories": [c.get("term") for c in e.findall("a:category", NS)],
            "primary": (e.find("a:primary_category", {
                "a": "http://arxiv.org/schemas/atom"}) or ET.Element("x")).get("term"),
        })
    return out


def retrieve() -> list[dict]:
    seen: dict[str, dict] = {}
    for term in COMPONENT_TERMS:
        start, got = 0, 0
        while True:
            print(f"  abs:\"{term}\" start={start} ...", end="", flush=True)
            try:
                recs = parse(fetch_page(term, start))
            except Exception as exc:                      # noqa: BLE001
                print(f" ОШИБКА: {exc}")
                break
            print(f" {len(recs)}")
            for r in recs:
                seen.setdefault(r["id"], r)
            got += len(recs)
            if len(recs) < PAGE:
                break
            start += PAGE
            time.sleep(DELAY_S)
        print(f"  -> {term}: {got}")
        time.sleep(DELAY_S)
    return list(seen.values())


# --------------------------------------------------------------------- output

def write_cache(records: list[dict]) -> None:
    with CACHE.open("w", encoding="utf-8") as fh:
        for r in sorted(records, key=lambda x: x["id"]):
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_cache() -> list[dict]:
    if not CACHE.is_file():
        sys.exit(f"нет кеша {CACHE.name} — сначала прогон без --offline")
    with CACHE.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="re-derive from cache, no network")
    args = ap.parse_args()

    if args.offline:
        records = read_cache()
        print(f"кеш: {len(records)} записей")
    else:
        print("забираю с arXiv (3 с между запросами, это надолго)")
        records = retrieve()
        write_cache(records)
        print(f"кеш записан: {len(records)} уникальных")

    frame = []
    for r in sorted(records, key=lambda x: x["id"]):
        ok, comp, claim = in_frame(r)
        if ok:
            frame.append({**r, "component_terms": comp, "claim_terms": claim})

    print(f"\nв рамке: {len(frame)} из {len(records)} кандидатов")

    sampled = frame
    if len(frame) > SAMPLE_CAP:
        rnd = random.Random(SAMPLE_SEED)
        sampled = sorted(rnd.sample(frame, SAMPLE_CAP), key=lambda x: x["id"])
        print(f"выборка {SAMPLE_CAP} со seed={SAMPLE_SEED}")

    # Canonical form: one id per line, sorted. This exact text is what is hashed.
    canonical = "\n".join(r["id"] for r in sampled) + "\n"
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    LIST_OUT.write_text(canonical, encoding="utf-8")
    META_OUT.write_text(json.dumps({
        "sha256_of_frame_txt": digest,
        "frame_size_before_sampling": len(frame),
        "candidates_retrieved": len(records),
        "sampled": len(sampled),
        "sample_seed": SAMPLE_SEED if len(frame) > SAMPLE_CAP else None,
        "window": [WINDOW_FROM, WINDOW_TO],
        "categories": CATEGORIES,
        "component_terms": COMPONENT_TERMS,
        "claim_terms": CLAIM_TERMS,
        "entries": sampled,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{LIST_OUT.name}  ({len(sampled)} id)")
    print(f"SHA256  {digest}")
    print("\n^ этот хеш идёт в CONTRACT.md при заморозке.")
    print("  frame.txt и frame.json НЕ публиковать до публикации результата.")

    if len(frame) < MIN_FRAME:
        print(f"\nСТОП-УСЛОВИЕ: в рамке {len(frame)} < {MIN_FRAME}.")
        print("Публикуется, что рамка слишком узка. Правило НЕ расширять —")
        print("более широкая рамка это новый контракт с новой заморозкой.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
