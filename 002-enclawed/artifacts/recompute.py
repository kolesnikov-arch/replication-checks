#!/usr/bin/env python3
"""Recompute every number in ../RESULT.md from the pinned release.

This check told four papers that a figure nobody can recompute is not a figure.
It would be indefensible to publish its own numbers without the means to redo
them, so this script exists and its output is the source of the result file.

The subject's data is not vendored here — it belongs to its authors and lives in
their repository. Point this script at their file; it verifies the hash before
reading a byte.

    git clone https://github.com/enclawed/enclawed-oss.git
    cd enclawed-oss && git checkout 2876530a5339
    python recompute.py enclawed-oss/docs/adversarial-in-vivo-samples.csv

Stdlib only, no dependencies.
"""

import csv
import hashlib
import statistics
import sys
from collections import Counter, defaultdict

PINNED_SHA256 = "d966b4c1587f7fad94b3e5bdcf60064c17046edf69b55537e5c9a4cf17fbaea4"
SUBJECTS = [("oc", "OpenClaw"), ("oss", "enclawed-oss"), ("enc", "enclawed-enclaved")]


def load(path):
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    print(f"file    : {path}")
    print(f"sha256  : {digest}")
    if digest != PINNED_SHA256:
        print(f"EXPECTED: {PINNED_SHA256}")
        print("\nMISMATCH. This is not the file the result was computed from.")
        print("Either the pin is wrong or the file changed. Do not trust anything below.")
        sys.exit(2)
    print("        : matches the pin recorded in RESULT.md\n")
    return list(csv.DictReader(raw.decode("utf-8").splitlines()))


def q1_cells(rows):
    print("Q1 — do the rows reconstruct the printed cells?")
    cells = Counter((r["channel"], r["fCat"], r["label"]) for r in rows)
    sizes = sorted(set(cells.values()))
    print(f"  rows {len(rows)} · cells {len(cells)} · cell sizes {sizes}")
    print(f"  labels: {dict(Counter(r['label'] for r in rows))}")
    ok = len(rows) == 1600 and len(cells) == 16 and sizes == [100]
    print(f"  -> 16 cells of 100: {'REPRODUCES' if ok else 'DOES NOT HOLD'}\n")
    return ok


def confusion(rows):
    print("C1/C2 — per-category confusion, all three subjects")
    print("  blocked = delivered is false; adversarial blocked = TP, legit blocked = FP")
    for key, name in SUBJECTS:
        print(f"  {name}")
        for f in sorted({r["fCat"] for r in rows}):
            sub = [r for r in rows if r["fCat"] == f]
            tp = sum(1 for r in sub if r["label"] == "adversarial" and r[key + "_delivered"] == "false")
            fn = sum(1 for r in sub if r["label"] == "adversarial" and r[key + "_delivered"] == "true")
            fp = sum(1 for r in sub if r["label"] == "legit" and r[key + "_delivered"] == "false")
            tn = sum(1 for r in sub if r["label"] == "legit" and r[key + "_delivered"] == "true")
            rec = tp / (tp + fn) if tp + fn else float("nan")
            pre = tp / (tp + fp) if tp + fp else float("nan")
            print(f"    {f:<12} TP={tp:3} FN={fn:3} FP={fp:3} TN={tn:3}  R={rec:.3f} P={pre:.3f}")
    print()


def identical_subjects(rows):
    print("Observation — are the two hardened subjects two subjects?")
    same_d = sum(1 for r in rows if r["oss_delivered"] == r["enc_delivered"])
    same_r = sum(1 for r in rows if r["oss_block_reason"] == r["enc_block_reason"])
    print(f"  oss_delivered == enc_delivered      on {same_d} of {len(rows)}")
    print(f"  oss_block_reason == enc_block_reason on {same_r} of {len(rows)}")
    print(f"  -> {'one result printed twice' if same_d == same_r == len(rows) else 'they differ somewhere'}\n")


def distinct_stimuli(rows):
    print("Observation — how many DISTINCT texts sit behind each n of 200?")
    print("  this is what a Wilson bound at k=0 over n treats as independent trials")
    for f in sorted({r["fCat"] for r in rows}):
        a = {r["content"] for r in rows if r["fCat"] == f and r["label"] == "adversarial"}
        l = {r["content"] for r in rows if r["fCat"] == f and r["label"] == "legit"}
        both = a & l
        print(f"  {f:<12} distinct adversarial {len(a):3} · distinct legit {len(l):3} · in both {len(both):3}")
    print("  -> F2 texts appearing in both classes are why F2 detection is structural, not content-based\n")


def redaction(rows):
    print("Observation — where did the released content get redacted?")
    for f in sorted({r["fCat"] for r in rows}):
        a = [r for r in rows if r["fCat"] == f and r["label"] == "adversarial"]
        l = [r for r in rows if r["fCat"] == f and r["label"] == "legit"]
        ra = sum(1 for r in a if "[REDACTED]" in r["content"])
        rl = sum(1 for r in l if "[REDACTED]" in r["content"])
        print(f"  {f:<12} [REDACTED] in adversarial {ra:3}/{len(a)} · in legit {rl:3}/{len(l)}")
    print("  -> where it is 200/0, a one-token rule separates the released classes\n")


def block_reasons(rows):
    print("Q2 — what fired, per category (enclawed-oss)")
    for f in sorted({r["fCat"] for r in rows}):
        c = Counter(r["oss_block_reason"] for r in rows if r["fCat"] == f and r["label"] == "adversarial")
        for reason, n in c.most_common():
            print(f"  {f:<12} {n:3}x  {reason}")
    print("  -> F1/F3/F4 fire on catalog items the harness inserts; F2 fires on a projection\n")


def wilson_upper(k, n, z=1.959963985):
    p = (k + z * z / 2) / (n + z * z)
    d = z / (n + z * z) * ((k * (n - k) / n + z * z / 4) ** 0.5)
    return min(1.0, p + d)


def q5_wilson():
    print("Q5 — the Wilson arithmetic, which needs no data")
    for n, claim in ((100, "≈0.036"), (10 ** 4, "3.84e-4"), (10 ** 6, "≈3.7e-6")):
        print(f"  k=0, n={n:<8} upper 95% = {wilson_upper(0, n):.6g}   paper: {claim}")
    print("  -> exact at n=1e4; the other two are rounded slightly low, immaterial\n")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    rows = load(sys.argv[1])
    q1_cells(rows)
    confusion(rows)
    block_reasons(rows)
    identical_subjects(rows)
    distinct_stimuli(rows)
    redaction(rows)
    q5_wilson()
    print("Q4 is not in this script: it reads docs/cross-llm/ and docs/post-widening/")
    print("from the same release. See recompute_q4.py.")


if __name__ == "__main__":
    main()
