# Check 001 — Leni Inc.: result

**Verdict: NOT COMPUTABLE.**

The verifier confusion matrix published as Table 4 of arXiv:2607.17044 cannot be
recomputed from the files released at `leni-agent-evals` commit `72bd5703`. This is a
statement about what the release contains. It is not a finding that the published numbers
are wrong, and nothing below should be read as one.

Protocol frozen as commit `f6ffe60` before any of these files was opened; the labelling
rules were committed as executable code, not only prose. Contract: [CONTRACT.md](CONTRACT.md).

## Read this first

At n=8 and n=40 these are small-sample quantities, and that governs every number here.
Computed from the paper's own numerators and denominators, the published figures carry
Clopper–Pearson 95% intervals of **catch 0.20 [0.09, 0.36]**, **fix 0.75 [0.35, 0.97]**,
**false alarm 0.00 [0.00, 0.010]**. The fix rate is consistent with anything from worse
than a coin flip to near-perfect. That is a property of n=8, not a criticism of the
authors, who state the false-alarm bound in the paper themselves.

## What does reproduce, exactly

The release supports the paper's headline SpreadsheetBench figures without adjustment.
The reported configuration is identifiable by the `benchmark_code` field
(`spreadsheetbench_direct_codeagent-v3-final`), 400 runs over 400 tasks, one run each:

| paper | released data | |
|---|---|---|
| 91.25% (365/400) | 365/400 | matches |
| cell-level 254/275 | 254/275 | matches |
| sheet-level 111/125 | 111/125 | matches |
| degraded 14 April run, 356/400 | `…-v3` config, 356/400 | matches |

Table 4's **margins** are also consistent with the released pass/fail record: the paper's
357 correct confirmations + 6 repaired + 2 non-loop passes = 365 passed, and 32 missed
errors + 2 unrepaired flags + 1 non-loop failure = 35 failed. Both totals agree with the
data exactly.

**What is not recoverable is the interior of the table** — which task sits in which cell.

## What is missing

1. **No verifier events in any trajectory.** Across the reported 400 runs the only tool
   appearing in `intermediate_steps` is `Code_Agent_v2_direct`, and every run carries
   exactly one step. A loop that executes, observes, compares and corrects is not
   representable in a single step. A keyword scan of all trajectories returns no
   `Cell-S`, no `verifier`; the eight occurrences of "flag" were inspected individually
   and are all spreadsheet content ("binary flags", "flag column"), not telemetry.
2. **No before/after artifact.** Every task in the reported configuration has exactly one
   run, so the pre-intervention answer needed for the fix rate — and for the false-alarm
   counterfactual — does not exist in the release.
3. **No loop-trigger field.** The 3 tasks that completed without triggering the loop
   cannot be separated from the 397 that did.
4. **No per-run verifier label.** Flagged (8), confirmed-correct (357) and missed-error
   (32) runs are indistinguishable from one another.

Consequently neither pass of the pre-registered protocol can run: pass 1 has no authors'
labels to reconstruct, and pass 2 has no detection events to consume. No figures are
reported for either, because with the telemetry absent they would be arithmetic on zeros
rather than measurements.

## This gap is disclosed by the authors

The paper states it plainly, in its own artifact section:

> the loop-action telemetry of Table 4 currently exists in the run transcripts rather
> than as structured fields and is being extracted for the release

So the release is incomplete for this specific claim **by the authors' own account**, with
extraction described as in progress. This check confirms that statement from the outside
and makes its consequence precise: Table 4 is, as of this commit, the one headline result
in the paper that a third party cannot verify, while every other SpreadsheetBench figure
checked here reproduces exactly.

It is worth recording what the release does that most do not: it ships unfavorable and
superseded runs, including the degraded 14 April campaign, and it is accompanied by a
pre-registration of follow-up experiments frozen on 2026-07-12. Publishing the data that
makes your own gap visible is the behaviour that made this check possible at all.

## What would close it

Per-run fields for the reported configuration: whether the loop triggered, whether the
verifier flagged or confirmed, and the pre-intervention answer where a repair occurred.
Four columns would move this claim from `NOT COMPUTABLE` to checkable by anyone.

## Limits of this check

- Only Table 4 was examined. The paper's other claims (+11.0 pp on SpreadsheetBench,
  BullshitBench, GAIA, the +1.5-point isolated contribution, the specialist-swap
  ablation, the valid-premise control) were outside the contract and were not checked.
- `NOT COMPUTABLE` says nothing about whether catch 0.20, fix 0.75 and false alarm 0/357
  are correct. They may be exactly right. They are, from this release, unverifiable.
- No comparison with the author's own verification work is offered or implied; the metrics
  sit on different tasks and different oracles, and such a comparison would be an
  overclaim.
- One defect in this check's own pre-registered design was found on contact with the data
  and is reported rather than patched — see [METHOD.md](METHOD.md).

## Reproducing this

```
git clone https://github.com/arnabdastidar/leni-agent-evals && \
  git -C leni-agent-evals checkout 72bd5703433c9b2f4f2444347bd96a77189f0d59
python artifacts/check.py leni-agent-evals
```

Stdlib only. Output: [artifacts/run_output.txt](artifacts/run_output.txt).

## Right of reply

The authors received notice of intent before the data was opened, and receive this result
before publication with 14 days to respond. Their reply will appear in full and unedited
in `REPLY.md`. If they identify a factual error here it will be corrected before
publication and attributed.
