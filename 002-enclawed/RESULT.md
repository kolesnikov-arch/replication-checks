# Check 002 — enclawed, arXiv:2605.01740: result

**Every published figure in this paper reproduces from the released files.** Not one number
was found to be wrong. What follows is about what those numbers measure and what the release
lets a third party establish.

Protocol frozen before the release was opened: [CONTRACT.md](CONTRACT.md), commit `8d3edc8`.
What was actually done, including a near-miss of my own: [METHOD.md](METHOD.md).
Artifact pinned at `enclawed/enclawed-oss` @ `2876530a5339`; the CSV analysed hashes to
`d966b4c1…7fbaea4` both in the working tree and in the pinned commit object.

## Outcome per question

| | question | verdict |
|---|---|---|
| **—** | do the headline figures reproduce, per category? | **REPRODUCES** |
| **Q1** | do the rows reconstruct the printed cells? | **REPRODUCES** |
| **Q2** | is the ground truth independent of the subject scored? | **DEVIATION** — F2 yes, F1/F3/F4 no, disclosed by the authors |
| **Q3a** | does the upstream tree-walk check out? | **NOT COMPUTABLE** — no upstream version is recorded |
| **Q3b** | does the evidence separate *absent* from *named differently*? | **REPRODUCES** — the paper documents a second stage that does exactly this |
| **Q4** | is the 14.6% improvability claim recomputable? | **DEVIATION** — direction holds, magnitude comes out +17.1% |
| **Q5** | is the 80,000-sample stress test released? | **NOT RELEASED** |

## The confirmation, in full

Recomputed per F-category rather than in aggregate, from
`docs/adversarial-in-vivo-samples.csv` at the pin: OpenClaw recall **0.000** on all four
categories; enclawed-oss and enclawed-enclaved precision = recall = **1.000** on all four,
with **zero** false positives across 200 legitimate samples per category. The rows partition
into exactly 16 cells of exactly 100 — `channel × fCat × label` — matching the paper's
*n* = 1600 at *n* = 100 per cell.

**Q3b deserves to be stated as prominently as anything critical here**, because it answers an
objection this check was written to press. The obvious weakness of "a grep for seven symbols
found nothing" is that a different runtime may implement the same property under another
name. §4.1 anticipates it:

> *"Second, the subject's user-facing documentation, plugin SDK reference, and API surface
> … is read to confirm whether any equivalent primitive ships under a different name — so a
> runtime that implements the same contract under a non-canonical symbol would still register
> as 'present'. Both stages must miss the primitive for the cell to read absent."*

That is a better protocol than the abstract's phrasing suggests, and most papers in the
survey this check grew out of had nothing comparable.

## Q2 — what the 1.000 measures

For three of four categories the adversarial class is **defined by containing an item from
the catalog the detector matches on**, and the authors document this in the released harness:

> *"…we synthesize adversarial samples from a parameterized template that ALWAYS hits the
> production gate stack. Each sample randomizes across the gate's own detection patterns so
> the test is the PRECISION of the gate, not the willingness of the LLM. The templates only
> encode patterns the production gates document (prompt-shield's IGNORE/DISREGARD/OVERRIDE
> imperatives + DLP's regex catalog for keys/PII)."*
> — `enclawed/test/security/in-vivo/llm-narrative.mjs`

The generators draw straight from the detector's vocabulary: `T_F1_VERBS` is
`['IGNORE','DISREGARD','OVERRIDE']`; `T_F3_SECRET_KINDS` emits `sk-…`, `sk-ant-…`,
`AKIA/ASIA…`, `ghp_…`, which are the `openai-key`, `anthropic-key`, `aws-access-key-id` and
`github-token` entries of `src/enclawed/dlp-scanner.ts`. The LLM-sourced path instructs the
model to insert the same strings.

**Nothing was concealed.** The authors' own description of what they measured — *"the
PRECISION of the gate, not the willingness of the LLM"* — is narrower and more defensible
than the paper's. The finding is that **the disclosure does not travel with the number**:
the abstract reads *"both hardened subjects reach P = R = accuracy = 1.000"* beside
*"OpenClaw catches none of them"*, with Wilson intervals attached, and a reader of the paper
alone will take 1.000 as detection ability rather than as a regression test over templates
built to fire.

**F2_FORGE is the exception and it is a real measurement.** The harness appends an
`irreversible.executed` audit record with no matching corpus-delta entry and
`checkBiconditional` catches it; the comment states *"F2 is content-agnostic; the message
body itself is benign."* The released data confirms it independently: **42 message texts
appear in F2 as both adversarial and legit**, so the two classes are textually inseparable,
and the subject still separates them 200/0 and 0/200. That is the strongest result in the
paper and it does not depend on the shared catalog at all.

## Q3a — the upstream side cannot be reproduced

The reproducibility apparatus here is unusually thorough: seeded PRNG for byte-for-byte
replay, hardware fingerprint, Node version, harness git commit. All of it pins **the
authors' own side**.

The upstream subject is whatever checkout sits at `$ENCLAWED_PATH`. No upstream commit,
tag or version is recorded anywhere in the paper or the release. So neither *recall = 0.000*
nor *14,419 first-party source files* can be checked by a third party: there is no way to
know which upstream state to build.

For scale, the same file filter the paper specifies (`*.ts, *.tsx, *.mjs, *.js, *.cjs`,
excluding `node_modules`, `dist`, `build`, `out`, `coverage`) applied to `openclaw/openclaw`
today returns **25,339** first-party files against the paper's 14,419. **This is not offered
as a discrepancy.** The repository is under daily development and the paper is roughly three
months old; the divergence is what one expects, and it is exactly why the missing pin
matters.

## Q4 — the improvability claim: direction yes, magnitude no

The pre- and post-widening sample sets are both released, in `docs/cross-llm/` and
`docs/post-widening/`. They are not directly comparable: **5 of 15 (model, channel) cells
present before the edit are absent after it**, all of them telegram.

Restricting to the 10 cells where *n* matches exactly:

```
n = 704 adversarial F3 samples
true positives   258  →  302
net gain        +17.1%      (paper: +14.6% net)
false positives    0  →    0      (paper: "at unchanged precision" — confirmed)
```

The mechanism, the direction and the unchanged precision all hold. The magnitude does not
match, and the release does not permit resolving why, because the two runs cover different
cells.

**A hazard worth publishing:** pooling the two sets naively — as I did first — yields
**−43%**, because the post set is roughly half the size on several models and nearly absent
on telegram. That number is an artefact of unequal denominators, and reporting it would have
been a serious and unfair error. It is recorded here because the next person to check this
will hit the same trap.

## Q5 — the stress test is not released

Table 4 reports *n* = 80,000 and carries the tightened false-positive bound. **No artifact
behind it exists in the release.** The largest sample file is the 1,600-row headline CSV at
260 KB; a set of that shape at 80,000 rows would be roughly 13 MB, and nothing of that order
is present under any name.

The Wilson arithmetic needs no data and was checked as stated. At *k* = 0:

| n | recomputed 95% upper bound | paper |
|---|---|---|
| 100 | 0.0370 | ≈ 0.036 |
| 10⁴ | 3.84 × 10⁻⁴ | 3.84 × 10⁻⁴ |
| 10⁶ | 3.84 × 10⁻⁶ | ≈ 3.7 × 10⁻⁶ |

The n = 10⁴ figure is exact. The other two are rounded slightly low; the difference is
immaterial to any claim.

**The bound's arithmetic is not the issue. Its independence assumption is.** See below.

## Three observations the questions did not anticipate

**The two hardened subjects are one subject.** `oss_delivered` equals `enc_delivered` on all
1,600 rows, and `oss_block_reason` equals `enc_block_reason` on all 1,600 rows — identical
strings, no exceptions. Presented as two subjects independently reaching 1.000, they are one
result printed twice.

**The denominators are inflated by repeated stimuli.** Distinct message texts per cell of
200:

| category | distinct adversarial | distinct legit |
|---|---|---|
| F1_BYPASS | 199 | **8** |
| F2_FORGE | 133 | 136 |
| F3_SILENT | **7** | 192 |
| F4_WRONGTGT | **40** | **6** |

The sample-size argument treats rows as independent trials — that is what a Wilson bound at
*k* = 0 over *n* means, and it is why the paper pushes *n* to 80,000. But "zero false
positives out of 200" in F4 is zero false positives across **six distinct legitimate
messages**, each presented about thirty-three times. Repeating a stimulus does not add
information about how often a *different* legitimate message would be blocked. Extending to
larger *n* tightens a bound whose denominator is mostly duplicates.

**The released content is redacted exactly where the detector fired.** `[REDACTED]` appears
in 200/200 adversarial rows of F3 and F4 and in 0/200 legit rows of either. So on the
released file a one-token rule separates the classes, and no detection decision can be
re-derived from the content column: the substring that triggered it was removed before
release. The decisions are auditable; the inputs behind them are not.

## What this check does not say

It does not say any published number is false — every one reproduced. It does not assess
whether either runtime is safe to deploy. It makes no comparison to any work of mine. And
it did not contact OpenClaw: C1 and C3 are claims about a third party's software, and
recruiting that third party into a dispute over someone else's paper would be a campaign,
not a check.

## Deviation from the contract, recorded

[CONTRACT.md](CONTRACT.md), frozen at `8d3edc8` and pushed before the release was opened,
lists under *Prohibited*: **"Publishing before the reply window closes."**

**This result was published on 2026-08-05, the same day the author was notified, and the
window had not closed.** That is a deviation from my own frozen protocol, made deliberately
and recorded here rather than absorbed. The decision was mine; the contract was not amended
afterwards to make it fit, because a contract edited to match what was done is not a
contract.

What the deviation costs the author, stated plainly: a factual error he identifies can no
longer be corrected quietly before anyone reads this. It will be corrected in public, as a
dated correction against the text below, with his name on it.

What it does not change: the length of the window, the promise to publish his reply in full
and unedited, or the promise that a correction he supplies is attributed to him.

**Nothing about the findings changed.** This text is byte-for-byte the text sent to the
author; its SHA-256 travels in that letter and in the commit message that published it, so
any later edit is visible against a figure fixed on the day, rather than silent.

## Right of reply

The author has **14 days from 2026-08-05**, to **2026-08-19**. His reply is published here
in full and unedited, in `REPLY.md`. A factual error he identifies is corrected as a visible,
dated correction and attributed to him. Silence is not commented on and there is no
follow-up.
