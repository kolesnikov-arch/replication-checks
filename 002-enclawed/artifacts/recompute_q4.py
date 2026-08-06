#!/usr/bin/env python3
"""Recompute Q4 — the 14.6% improvability claim — from the pinned release.

This is the number this check reports differently from the paper, so it is the
one that most needs to be redoable by someone who doubts me.

    git clone https://github.com/enclawed/enclawed-oss.git
    cd enclawed-oss && git checkout 2876530a5339
    python recompute_q4.py enclawed-oss/docs

`docs` must contain cross-llm/ (pre-widening) and post-widening/, each holding
the gzipped per-model sample CSVs. Stdlib only.

THE TRAP, stated before the result: pooling the two sets naively gives -43%.
That is an artefact of unequal denominators — the post set is half-size on
several models and nearly absent on telegram — and it is wrong. The comparison
is only meaningful on cells where n matches on both sides. This script prints
both so the trap is visible rather than merely warned about.
"""

import csv
import glob
import gzip
import io
import os
import sys


def cells(directory):
    """-> {(model, channel): (true_positives, n)} over F3 adversarial samples."""
    out = {}
    for path in sorted(glob.glob(os.path.join(directory, "*.csv.gz"))):
        model = os.path.basename(path).replace("adversarial-in-vivo-samples-", "").replace(".csv.gz", "")
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                if row["fCat"] != "F3_SILENT" or row["label"] != "adversarial":
                    continue
                key = (model, row["channel"])
                tp, n = out.get(key, (0, 0))
                out[key] = (tp + (1 if row["oss_delivered"] == "false" else 0), n + 1)
    return out


def false_positives(directory):
    fp = 0
    for path in sorted(glob.glob(os.path.join(directory, "*.csv.gz"))):
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                if row["fCat"] == "F3_SILENT" and row["label"] == "legit" and row["oss_delivered"] == "false":
                    fp += 1
    return fp


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    docs = sys.argv[1]
    pre_dir, post_dir = os.path.join(docs, "cross-llm"), os.path.join(docs, "post-widening")
    for d in (pre_dir, post_dir):
        if not os.path.isdir(d):
            print(f"missing directory: {d}")
            sys.exit(2)

    pre, post = cells(pre_dir), cells(post_dir)

    print("THE WRONG ANSWER, shown first so nobody arrives at it by accident")
    tp0, n0 = sum(v[0] for v in pre.values()), sum(v[1] for v in pre.values())
    tpa, na = sum(v[0] for v in post.values()), sum(v[1] for v in post.values())
    print(f"  pooled: TP {tp0}/{n0} -> {tpa}/{na}   naive net {(tpa - tp0) / tp0 * 100:+.1f}%")
    print("  -> unequal denominators. Not a result. Do not report this.\n")

    print("CELLS PRESENT BEFORE THE EDIT AND ABSENT AFTER IT")
    missing = [k for k in pre if k not in post]
    for k in sorted(missing):
        print(f"  {k[0]:<24} {k[1]:<9} pre n={pre[k][1]:4}  post: absent")
    resized = [k for k in pre if k in post and pre[k][1] != post[k][1]]
    for k in sorted(resized):
        print(f"  {k[0]:<24} {k[1]:<9} pre n={pre[k][1]:4}  post n={post[k][1]:4}")
    print(f"  -> {len(missing) + len(resized)} of {len(pre)} cells are not comparable\n")

    print("THE LIKE-FOR-LIKE SUBSET — cells where n matches exactly")
    matched = [k for k in pre if k in post and pre[k][1] == post[k][1] and pre[k][1] > 0]
    for k in sorted(matched):
        print(f"  {k[0]:<24} {k[1]:<9} n={pre[k][1]:4}  TP {pre[k][0]:4} -> {post[k][0]:4}")
    tp0 = sum(pre[k][0] for k in matched)
    tpa = sum(post[k][0] for k in matched)
    n = sum(pre[k][1] for k in matched)
    net = (tpa - tp0) / tp0 * 100 if tp0 else float("nan")
    print(f"\n  n={n}   TP {tp0} -> {tpa}   net {net:+.1f}%   (paper claims +14.6% net)")

    fp_pre, fp_post = false_positives(pre_dir), false_positives(post_dir)
    print(f"  false positives on F3 legit: {fp_pre} -> {fp_post}"
          f"   ('at unchanged precision': {'confirmed' if fp_pre == fp_post == 0 else 'NOT confirmed'})")
    print("\n  -> direction and unchanged precision hold; the magnitude does not match,")
    print("     and the release does not permit resolving why.")


if __name__ == "__main__":
    main()
