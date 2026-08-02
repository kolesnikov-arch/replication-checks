# Check 001 — Leni Inc.: pre-registered protocol

**Frozen before any of the subject's data was opened.** Commit hash of this file is
quoted to the authors and in the published result. Nothing below is revised after the
numbers are visible; a change requires a new version of this file stating why, with the
previous version retained.

## Subject

**Claim:** arXiv:2607.17044, *Where Does Agent Reliability Come From? A Cross-Benchmark
Decomposition of Verification Loops, Specialist Models, and Scaffolding in a Production
Enterprise Agent*, Arunabh Dastidar and the Leni Team.

**Data:** `github.com/arnabdastidar/leni-agent-evals` — MIT for scripts, CC BY 4.0 for
data. The authors state that everything reported in the paper is computable from the
files in that repository.

**Target pinned:**

| | |
|---|---|
| repository commit | `72bd5703433c9b2f4f2444347bd96a77189f0d59` |
| paper version | v1, submitted 2026-07-19 |
| pinned on | 2026-08-02 |

This check applies to that state and to no other. If the repository or the paper changes,
the result is not silently updated; a later state requires a new check.

## Disclosure before freezing

Before drafting this protocol I read **the repository README and the paper's abstract** —
the file inventory, the licences, and the authors' invitation to replicate. That much is
necessary to specify a method: one cannot describe a procedure without knowing which
files exist.

**No run outcome, no label, and no row of data was opened.** This disclosure is here
because concealing it would be precisely the behaviour this series exists to check.

## The question — one

> Does the published verifier confusion matrix — catch rate ≈0.20, fix rate 0.75, false
> alarms ≈0/357 — come back out of the released files, and what does it look like under
> an independently stated labelling rule?

The paper's other claims (+11.0 pp on SpreadsheetBench, +7–10 on BullshitBench, ≈+15 on
GAIA, the +1.5-point isolated contribution of verification, the specialist-swap ablation,
the valid-premise control) are **not part of this check**. One check, one claim.

## Why this claim

It is computed by the builders of the layer it evaluates; the authors present it as part
of their central contribution; they state it is computable from the repository; and it is
small enough (8 of 40, 6 of 8, 0 of 357) to be audited case by case without computational
resources.

## What counts as reproduction

Three outcomes, published identically:

| outcome | condition |
|---|---|
| **REPRODUCES** | under the authors' labelling rule, the same numerators and denominators come out of the files |
| **REPRODUCES WITH DEVIATION** | different numbers, with the difference traced to a named difference in labelling rule or sample composition |
| **NOT COMPUTABLE** | the matrix cannot be derived from what was released — labels absent, runs not linked to verifier events, or no denominator |

`NOT COMPUTABLE` is a statement about the completeness of a release. It carries no
implication that the published number is wrong, and will not be worded as though it did.

## Labelling rule — fixed here, before the data

Computed **twice**; both results published side by side.

**Pass 1 — the authors' rule.** Reconstructed from the paper and the repository's
scripts. If it cannot be recovered unambiguously, that is recorded as such and pass 1 is
declared not executable. It is not approximated to make a number appear.

**Pass 2 — an independent rule**, fixed in advance:

- **Error** — a run whose final answer does not match the reference under the benchmark's
  own official scorer. Not by judgement, not by the authors' label.
- **Caught** — a verifier event marked as a detection, occurring before the final answer,
  on a run classified as an error above.
- **Fixed** — a run marked caught whose final answer matches the reference.
- **False alarm** — a detection event on a run whose final answer matches the reference
  **and** would have matched without the intervention, where that is recoverable. Where it
  is not recoverable, the run is excluded from the false-alarm denominator and the number
  of exclusions is published.

**The gap between pass 1 and pass 2 is the main result**, not a side note. If the
published figure depends on the authors' labelling rule, that is exactly the thing worth
knowing, and it is reported without adjectives.

## Metrics

| metric | form |
|---|---|
| catch rate | proportion + Clopper–Pearson 95% interval |
| fix rate | proportion + Clopper–Pearson 95% interval |
| false-alarm rate | proportion + Clopper–Pearson 95% interval |
| exclusions | absolute count and reason per category |

**No point estimate is published without an interval.** At n=40 and n=8, a disagreement
over two or three labels moves the proportion by tens of percentage points. This
limitation is stated in the first paragraph of the result, not in a footnote.

## What is and is not claimed

**Claimed:** whether one specific number reproduces from one specific release.

**Not claimed:** whether Leni works; whether their approach is good; whether the result
transfers to production; any comparison with my own work. Formulations of the form "their
verifier is worse than mine" are prohibited — the metrics sit on different tasks,
different oracles, and different framings, and such a comparison would be the same class
of overclaim this series exists to catch.

## Right of reply

1. A letter of intent goes to the authors **before** the run.
2. The finished result goes to the authors **before** publication, with **14 days** to
   respond.
3. Their reply is published in full and unedited in `REPLY.md`.
4. If they identify a factual error, it is corrected before publication and the
   correction is attributed to them in the text.
5. Silence after 14 days does not block publication and is not commented on.

## Stop conditions

- **The authors' rule cannot be recovered and the independent rule cannot be applied to
  the files** → publish `NOT COMPUTABLE` with an itemised list of what is missing. The
  check ends there; guesses are not published.
- **The data turns out to have been released in error, or the licence is withdrawn** →
  work stops, nothing is published, the authors are notified.
- **The number reproduces exactly** → publish `REPRODUCES`, same format, same weight.
  This is not a null result and is not a reason to delay the instalment.

## Prohibited

- Changing the labelling rule after seeing the data.
- Adding or dropping runs to widen or narrow a discrepancy.
- Publishing partially — the whole result or nothing.
- Attaching any offer, availability note, or link to anything for sale.

---

**Freeze record**

| | |
|---|---|
| frozen on | 2026-08-02 |
| contract commit | `f6ffe602c4cd7842214eab00770cc6cbc1cb03ac` — the freeze. A commit cannot contain its own hash, so it is recorded here in the commit immediately after; the freeze is the one above, and everything it contains predates the data. |
| letter of intent sent | pending |
| data first opened | not yet |
