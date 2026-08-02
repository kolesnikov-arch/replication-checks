# Check 001 — Leni Inc.: what was actually done

Companion to [CONTRACT.md](CONTRACT.md) (frozen as `f6ffe60`) and
[RESULT.md](RESULT.md). This file records the procedure, every deviation from the
protocol, and one defect in the protocol itself.

## Order of operations

| step | when |
|---|---|
| protocol committed, target pinned (`72bd5703`, paper v1) | 2026-08-02, commit `f6ffe60` |
| letter of intent sent to the corresponding author | 2026-08-02 |
| subject's data first opened | 2026-08-02, after the above |
| result sent to the authors | pending, before publication |

Nothing about the analysis was decided after the numbers were visible. The rules were in
executable form before the clone.

## Procedure

1. Cloned `leni-agent-evals` and checked out the pinned commit. Verified `HEAD` matches
   the contract.
2. Read `README.md` and `experiments_protocol.md`; extracted `paper.pdf` to text and
   located the claim under check as **Table 4** (`paper.txt` lines 540–553).
3. Identified the reported run set. There is no configuration column named as such, but
   `benchmark_code` separates the four configurations cleanly;
   `spreadsheetbench_direct_codeagent-v3-final` gives 400 runs over 400 tasks and
   reproduces the paper's 365/400, 254/275 and 111/125 exactly, confirming it is the
   reported set. The `…-v3` configuration reproduces the degraded 14 April run at 356/400.
4. Searched for the telemetry the contract's rules consume:
   - enumerated every `tool` and `type` across all trajectories in the release;
   - counted steps per run in the reported configuration;
   - keyword-scanned all trajectory text for `cell-s`, `verifier`, `verify`, `recalc`,
     `flag`, `confirm`, `mismatch`, `oracle`, `compare`, `iteration`, `repair`, `rescue`;
   - inspected each of the eight `flag` occurrences individually.
5. Checked whether repairs are recoverable: counted runs per task in the reported set.
6. Ran `artifacts/check.py`, which encodes all of the above as pass/fail conditions.

## Findings that determined the verdict

- Only `Code_Agent_v2_direct` appears as a tool in the reported configuration, and every
  one of its 400 runs carries exactly **one** step. The four-stage loop is not present.
- All eight `flag` occurrences are spreadsheet content, not telemetry.
- Every task in the reported set has exactly one run: no before/after pair exists.
- No loop-trigger field and no per-run verifier label exist.

Itemised in [RESULT.md](RESULT.md).

## Deviation from the contract: none in the rules

Nothing above the `ADAPTER` banner in `artifacts/check.py` was modified after the data was
opened. The diff between the frozen commit and the published one touches only `load_runs`,
the `TelemetryUnavailable` exception, the `REPORTED_CONFIG` constant, and the branch in
`main` that prints the verdict — all of which sit in the adapter region the contract
reserves for post-data completion.

## Defect in the pre-registered design, reported not patched

The frozen `Run` dataclass types `detection_events` as an integer defaulting to 0. That
conflates two different facts: *the verifier did not fire on this run* and *whether it
fired is not recorded*. Loading the release with `detection_events=0` everywhere and
running the frozen `classify_pass2` would have printed a catch rate of 0/35 — a number
that looks like a measurement and is an artifact of missing data.

Per the contract and `artifacts/README.md`, a rule that needs changing on contact with the
data is a finding to report, not an edit to make. So the rule stands as frozen, the
adapter refuses to fabricate by raising `TelemetryUnavailable` instead of returning zeros,
and the defect is recorded here.

**It does not change the verdict.** The contract's `NOT COMPUTABLE` outcome is defined by
the release lacking the inputs the rules consume, which is what was found; and the frozen
`verdict()` function returns `NOT COMPUTABLE` independently, because pass 1 cannot be
reconstructed either. Carried forward: future contracts in this series will use an
explicit three-valued type for observations that may be absent.

## Earlier defect, found before the data

During validation of `clopper_pearson` against known values — before the clone — the
bisection helper was found to assume a decreasing objective while both Clopper–Pearson
bounds increase in *p*, producing inverted intervals. Fixed and re-validated against five
known values, including 17/50 and 0/50 from the author's own preprint, which it now
reproduces exactly. Recorded because it is the argument for writing the analysis first.

## Tools

Python 3, standard library only for the published check. `pandas` and `pdftotext` were
used for exploration in step 2–5; every determination they informed is re-derived by
`artifacts/check.py` with the standard library alone, so the published result does not
depend on them.
