"""Check 001 — Leni Inc. verifier confusion matrix.

Written and committed BEFORE the subject's data was opened, per CONTRACT.md.

The rules live above the adapter. `load_runs` is the only function that may be
completed after the data is first read; everything below the ADAPTER banner is
frozen. If completing the adapter appears to require changing a rule, that is a
finding to report, not an edit to make.

No dependencies: stdlib only, so a third party can run it without installing
anything.
Usage: python check.py <path-to-leni-agent-evals-checkout>
"""

from dataclasses import dataclass, field
from math import comb
from typing import Optional
import sys

# Published figures under check, transcribed from arXiv:2607.17044v1.
PUBLISHED = {
    "catch": (8, 40),        # "catch rate about 0.20", 8 true errors of 40
    "fix": (6, 8),           # "fix rate 0.75", 6 of 8 flagged repaired
    "false_alarm": (0, 357),  # "no false-alarm regressions"
}

REPO_COMMIT = "72bd5703433c9b2f4f2444347bd96a77189f0d59"


def _binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Bin(n, p). Exact terms, stdlib only."""
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def _bisect(f, lo: float, hi: float, iters: int = 100) -> float:
    """Root of an INCREASING f on [lo, hi]. Both callers below are increasing in
    p; passing a decreasing function here returns an endpoint, not a root."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Exact binomial interval. Contract: no point estimate without one.

    Lower bound solves P(X >= k | p) = alpha/2; upper solves P(X <= k | p) =
    alpha/2. Both by bisection on the exact binomial CDF, so no scipy.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else _bisect(
        lambda p: (1 - _binom_cdf(k - 1, n, p)) - alpha / 2, 0.0, 1.0
    )
    hi = 1.0 if k == n else _bisect(
        lambda p: alpha / 2 - _binom_cdf(k, n, p), 0.0, 1.0
    )
    return (lo, hi)


@dataclass
class Run:
    """One evaluation run.

    `matches_reference` must come from the benchmark's own official scorer, never
    from the authors' label and never from judgement (CONTRACT, pass 2).
    `counterfactual_matches` is the answer the run would have given without
    verifier intervention, where recoverable; None where not.
    """
    run_id: str
    benchmark: str
    matches_reference: bool
    detection_events: int = 0
    authors_label: Optional[str] = None
    counterfactual_matches: Optional[bool] = None
    raw: dict = field(default_factory=dict)


@dataclass
class Counts:
    errors: int = 0
    caught: int = 0
    fixed: int = 0
    false_alarms: int = 0
    false_alarm_denominator: int = 0
    excluded_unrecoverable: int = 0
    notes: list[str] = field(default_factory=list)


class NotExecutable(Exception):
    """Pass 1 could not be reconstructed unambiguously. Per CONTRACT this is
    recorded as such and NOT approximated to make a number appear."""


# ---------------------------------------------------------------- frozen rules

def classify_pass2(runs: list[Run]) -> Counts:
    """Independent labelling rule, fixed in CONTRACT.md before the data."""
    c = Counts()
    for r in runs:
        is_error = not r.matches_reference
        detected = r.detection_events > 0

        if is_error:
            c.errors += 1
            if detected:
                c.caught += 1
        else:
            # False-alarm denominator: correct runs where the counterfactual is
            # recoverable. Unrecoverable ones are excluded and counted.
            if r.counterfactual_matches is None:
                if detected:
                    c.excluded_unrecoverable += 1
                continue
            c.false_alarm_denominator += 1
            if detected and r.counterfactual_matches:
                c.false_alarms += 1

    # Fixed: of runs marked caught, those whose final answer matches reference.
    # A caught run is by construction an error, so under this rule `fixed` counts
    # runs that were errors at detection time and correct at the end. That is only
    # observable if the pipeline records the pre-intervention answer.
    fixed = 0
    unobservable = 0
    for r in runs:
        if r.detection_events > 0 and r.counterfactual_matches is not None:
            if not r.counterfactual_matches and r.matches_reference:
                fixed += 1
        elif r.detection_events > 0:
            unobservable += 1
    c.fixed = fixed
    if unobservable:
        c.notes.append(
            f"{unobservable} detected runs have no recoverable pre-intervention "
            f"answer; fix rate is computed on the remainder"
        )
    return c


def classify_pass1(runs: list[Run]) -> Counts:
    """The authors' own labelling rule, reconstructed from paper and scripts.

    Raise NotExecutable if it cannot be recovered unambiguously.
    """
    if not any(r.authors_label for r in runs):
        raise NotExecutable(
            "no author-supplied labels found in the release; the authors' rule "
            "cannot be reconstructed from the files"
        )
    c = Counts()
    for r in runs:
        label = (r.authors_label or "").lower()
        if label in ("error", "true_error"):
            c.errors += 1
            if r.detection_events > 0:
                c.caught += 1
        elif label in ("false_alarm", "spurious"):
            c.false_alarms += 1
        if label in ("caught_fixed", "repaired"):
            c.fixed += 1
    c.false_alarm_denominator = sum(1 for r in runs if r.matches_reference)
    return c


def verdict(pass1: Optional[Counts], pass2: Counts) -> str:
    """REPRODUCES / REPRODUCES WITH DEVIATION / NOT COMPUTABLE."""
    if pass1 is None:
        return "NOT COMPUTABLE"
    published_match = (
        (pass1.caught, pass1.errors) == PUBLISHED["catch"]
        and (pass1.fixed, pass1.caught) == PUBLISHED["fix"]
        and (pass1.false_alarms, pass1.false_alarm_denominator) == PUBLISHED["false_alarm"]
    )
    return "REPRODUCES" if published_match else "REPRODUCES WITH DEVIATION"


def report(label: str, k: int, n: int) -> str:
    if n == 0:
        return f"  {label:<16} n/a (denominator 0)"
    lo, hi = clopper_pearson(k, n)
    return f"  {label:<16} {k}/{n} = {k / n:.3f}  CI95 [{lo:.3f}, {hi:.3f}]"


# ------------------------------------------------------------------- ADAPTER
# The ONLY part that may be completed after the data is first opened.
# Completing it must not require touching anything above this banner.

def load_runs(checkout_path: str) -> list[Run]:
    raise NotImplementedError(
        "Adapter not yet written. Per CONTRACT.md the data is opened only after "
        "(1) this protocol is committed and (2) the letter of intent is sent. "
        "Fill this in against the released schema at commit "
        f"{REPO_COMMIT}, changing nothing above the ADAPTER banner."
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    runs = load_runs(sys.argv[1])
    print(f"check 001 — Leni · repo {REPO_COMMIT[:7]} · {len(runs)} runs\n")

    try:
        p1 = classify_pass1(runs)
    except NotExecutable as e:
        p1 = None
        print(f"pass 1 (authors' rule): NOT EXECUTABLE — {e}\n")
    else:
        print("pass 1 (authors' rule)")
        print(report("catch", p1.caught, p1.errors))
        print(report("fix", p1.fixed, p1.caught))
        print(report("false alarm", p1.false_alarms, p1.false_alarm_denominator))
        print()

    p2 = classify_pass2(runs)
    print("pass 2 (independent rule, pre-registered)")
    print(report("catch", p2.caught, p2.errors))
    print(report("fix", p2.fixed, p2.caught))
    print(report("false alarm", p2.false_alarms, p2.false_alarm_denominator))
    if p2.excluded_unrecoverable:
        print(f"  excluded (unrecoverable counterfactual): {p2.excluded_unrecoverable}")
    for n in p2.notes:
        print(f"  note: {n}")

    print(f"\npublished: catch {PUBLISHED['catch']}, fix {PUBLISHED['fix']}, "
          f"false alarm {PUBLISHED['false_alarm']}")
    print(f"verdict: {verdict(p1, p2)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
