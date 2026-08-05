# Check 002 — enclawed: pre-registered protocol

**Frozen before the release is opened.** This file is committed first; its commit hash goes
to the authors with the result and into the published write-up. Nothing below is revised
after any answer is known; a change requires a new version of this file stating why, with
the previous version retained.

## Subject

**arXiv:2605.01740** — *Architectural Obsolescence of Unhardened Agentic-AI Runtimes: a
production-CLI in-vivo comparison of OpenClaw and enclawed-oss on F1–F4 detection, extension
parity, and improvability.*

Artifact: `enclawed/enclawed-oss`, pinned at commit `2876530a5339` as of 2026-08-05.

## Prior exposure, disclosed before anything else

**This release has already been opened once, by me, and its headline already recomputed.**
On 2026-08-03 it entered the survey of self-reported verifier claims as one of fourteen
papers, was determined `COMPUTABLE`, and the aggregate figures were recomputed from
`docs/adversarial-in-vivo-samples.csv`: 1,600 rows, 800 legitimate and 800 adversarial,
upstream recall 0.000, both hardened subjects precision = recall = 1.000. They matched the
paper.

So the ordinary promise — *the method is frozen before the data is opened* — cannot be made
here in its plain form, and pretending otherwise would be the exact defect this repository
exists to expose. What is frozen instead:

1. The questions below were written **before** any file in the release was opened for this
   check, and none of them is answered by the survey's recomputation.
2. The survey asked whether the published numbers come back out of the published files.
   They do. **That is this check's starting point, not its finding**, and it is stated as a
   confirmation in the result regardless of what follows.
3. The paper itself was read to state the claims precisely. Reading a paper's claims is not
   opening its data; the release is not touched again until this file is committed.

## Claims under check, quoted

- **C1.** *"OpenClaw recall is 0.000 on every F1–F4 category"* — Table 3, n = 1600, n = 100
  per cell, through OpenClaw's production CLI.
- **C2.** *"both hardened subjects reach P = R = accuracy = 1.000"* on the same input.
- **C3.** *"A tree-walk of OpenClaw's 14,419 first-party source files returns zero matches
  for any of the seven primitives"* — Table 2, described as *"the topology of obsolescence"*.
- **C4.** *"a six-line append-only widening of the production DLP catalog raises per-channel
  F3 TP counts by 14.6% net at unchanged precision"*.
- **C5.** The stress-test extension, *"Table 4 pushes n to 80,000 to tighten the FPR upper
  bound"*, with the Wilson bound at k = 0 quoted as ≈ 0.036 at n = 100 and ≈ 3.84 × 10⁻⁴ at
  n = 10⁴.

## Questions — fixed here, five, each with its verdict rule

Each resolves to **REPRODUCES**, **REPRODUCES WITH DEVIATION** (a named difference in rule
or sample accounts for it), or **NOT COMPUTABLE** (the release does not permit the check).
A question may also resolve **OUT OF SCOPE** if the claim's form does not fit the rule below,
and that is reported rather than forced.

### Q1 — Does the row structure reconstruct the cells?

The headline is stated as n = 1600 with n = 100 per cell. The release carries 1,600 rows
split 800 legitimate / 800 adversarial. **Do the rows partition into cells of 100 that
correspond to the table as printed?**

- REPRODUCES: a grouping exists in the released columns that yields the printed cells.
- DEVIATION: a grouping exists but the cell sizes or the count of cells differ from the
  paper, and the difference is named.
- NOT COMPUTABLE: no released column identifies the cell a row belongs to.

### Q2 — Is the ground truth independent of the subject being scored?

This is condition A of the survey contract, and the survey did **not** test it — it tested
that labels are present, not where they came from. The harness is described as generating
deterministic templates from the project's own catalogs, including the DLP regex catalog.

**Is the label of an adversarial sample derivable from the same artifact the hardened
subject matches on?** If the templates are built from the catalog the detector implements,
then recall 1.000 is a property of the construction and not a measurement of detection.

- REPRODUCES: the labelling is traceable to something the subject does not consult.
- DEVIATION: the labelling shares an artifact with the detector, and the extent is named.
- NOT COMPUTABLE: the release does not let a reader tell.

**This question can only make the claim weaker or leave it unchanged. It is asked anyway,
and its answer is published whichever way it falls** — including "the labelling is clean",
which is the outcome the survey's recomputation makes likely.

### Q3 — Does "zero matches for seven canonical symbols" support "the primitives are absent"?

C3 is the load-bearing structural claim: *the gap is not a flag or a knob, it is the seven
primitives.* Table 2 names the symbols searched — `lockTrustRoot`, `sealBootstrap` and five
others.

Two separable sub-questions:

- **Q3a, arithmetic:** does a tree-walk of upstream OpenClaw at a stated pin return zero
  matches for those symbols, and is the first-party file count near 14,419? This is
  reproducible by clone and search.
- **Q3b, inference:** a symbol search finds *these names*. A different runtime may implement
  the same property under different names, or may satisfy it structurally without a named
  symbol at all. **Does the release document any search for the property rather than the
  name?**

Q3b is not a claim that upstream has the primitives. It asks whether the published evidence
distinguishes *absent* from *named differently* — the same question this repository asks of
everyone, including itself.

### Q4 — Is the improvability claim recomputable?

C4 quotes a 14.6% net gain in per-channel F3 true positives at unchanged precision from a
six-line edit. **Are the pre-edit and post-edit per-channel counts in the release?** This
is condition D of the survey contract — where repair is claimed, the pre-intervention state
must be recoverable.

### Q5 — Is the stress test released?

C5 reports Table 4 at n = 80,000. The release examined in the survey holds 1,600 rows.
**Is there a released artifact behind the 80,000-sample run and the tightened FPR bound?**

If not, this paper is computable for its headline and not for its stress test, and both
halves are reported. The Wilson arithmetic itself (k = 0, n = 100 → ≈ 0.036; n = 10⁴ →
≈ 3.84 × 10⁻⁴) is checked as stated regardless, since it needs no data.

## What this check does not do

- **No security assessment.** Whether either runtime is safe to deploy is not asked, not
  measured, and will not be implied.
- **No comparative claim of ours.** "Their layer versus mine" is out of scope by
  construction, as in every check here.
- **No contact with OpenClaw.** C1 and C3 are claims about a third party's software, and
  this check verifies what the authors published about it. Recruiting the third party into
  a dispute about someone else's paper is not a check; it is a campaign.
- **No claim that a published number is false.** `NOT COMPUTABLE` says a release does not
  permit a recomputation. It never says the figure is wrong.

## Right of reply — the strict policy, unchanged

Deep checks keep the full policy; only the survey ran the lighter one.

1. The complete result goes to the authors **before publication**.
2. They have **14 days**.
3. Their reply is published in full and unedited in `REPLY.md`.
4. A factual error they identify is corrected before publication and attributed to them.
5. If the two hardened subjects are theirs and the comparison is favourable, that is
   published in exactly the same format and with the same prominence as anything else.

## Stop conditions

- **Everything reproduces** → publish that. A confirmation is a result. Rule 3 of this
  repository exists because the first unpublished positive turns a check into a hunt.
- **A question cannot be classified** → report it unclassifiable with the reason, not forced
  into a verdict.
- **The check's own instrument is found defective** → the defect is published alongside, in
  the same file, as in `survey-verifier-claims/DEFECTS.md`.

## Prohibited

- Adding a question after an answer is known. A new question requires a new version of this
  file, dated, with the reason, before its answer exists.
- Dropping a question because its answer is inconvenient — in either direction.
- Any offer, availability note, or link to anything for sale, in the result or in the letter
  to the authors.
- Publishing before the reply window closes.

---

**Freeze record**

| | |
|---|---|
| contract frozen at commit | *(this commit)* |
| artifact pin | `enclawed/enclawed-oss` @ `2876530a5339` |
| paper version read | arXiv:2605.01740v1 |
| prior exposure | survey determination 2026-08-03, headline recomputed and matched |
| release opened for this check | **not before this file is committed** |
