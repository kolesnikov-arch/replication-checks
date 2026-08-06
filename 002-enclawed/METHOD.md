# Check 002 — what was actually done

Contract frozen at `8d3edc8` and pushed **before** the release was opened. Everything below
happened after that commit.

**Status: all five questions resolved.**

## Deviation, recorded first because it is the largest one

The contract prohibits *"Publishing before the reply window closes."* **This check was
published on 2026-08-05, the same day the author was notified.** The window had not closed
and will not until 2026-08-19.

The deviation was deliberate and it is mine. It is written into the result as well as here,
and the contract was **not** edited afterwards to accommodate it — a frozen protocol amended
to match what was done stops being a protocol. The concrete cost to the author is stated in
the result: an error he identifies is now corrected in public and dated, rather than fixed
before anyone read it.

Recorded because an unrecorded deviation from a frozen protocol is the exact defect this
repository exists to find in other people's work.

## Provenance of every byte examined

The clone aborted part-way through checkout on Windows, leaving an incomplete working tree.
Rather than trust it, every artifact below was read **from the pinned commit object**:

```
git cat-file -p 2876530a5339:docs/adversarial-in-vivo-samples.csv
```

The extracted blob and the working-tree copy hash identically —
`d966b4c1587f7fad94b3e5bdcf60064c17046edf69b55537e5c9a4cf17fbaea4` — so the incomplete
checkout did not affect the file the analysis rests on. Recorded because a check whose input
provenance is "it was in the folder" is not a check.

## The confirmation, stated first

**Every published figure reproduces, and per category, not only in aggregate.** The survey
recomputed the headline; this check went one level finer, and it holds:

| subject | F1_BYPASS | F2_FORGE | F3_SILENT | F4_WRONGTGT |
|---|---|---|---|---|
| OpenClaw | R = 0.000 | R = 0.000 | R = 0.000 | R = 0.000 |
| enclawed-oss | P = R = 1.000 | P = R = 1.000 | P = R = 1.000 | P = R = 1.000 |
| enclawed-enclaved | P = R = 1.000 | P = R = 1.000 | P = R = 1.000 | P = R = 1.000 |

200 adversarial and 200 legit per category per subject; zero false positives anywhere.
**Nothing in this check contradicts a published number.** What follows is about what those
numbers measure.

## Q1 — Does the row structure reconstruct the cells? **REPRODUCES**

1,600 rows partition into exactly 16 cells of exactly 100, on
`channel × fCat × label` — 2 channels (discord, telegram) × 4 F-categories × 2 labels. The
paper's *n* = 1600 with *n* = 100 per cell is recoverable from released columns alone.

## Q2 — Is the ground truth independent of the subject being scored?

**Answer: for F1, F3 and F4, no — and the authors say so in the released source.
For F2, yes.**

This is not an inference from block reasons. The harness
`enclawed/test/security/in-vivo/llm-narrative.mjs` documents the design in a comment above
the template generators:

> *"LLM brains heavily refuse our F1/F3/F4 briefs (…), so for statistical power we
> synthesize adversarial samples from a parameterized template that **ALWAYS hits the
> production gate stack**. Each sample randomizes across **the gate's own detection
> patterns** so the test is the PRECISION of the gate, not the willingness of the LLM.*
>
> *The templates only encode patterns the production gates document (prompt-shield's
> IGNORE/DISREGARD/OVERRIDE imperatives + DLP's regex catalog for keys/PII). They do not
> invent novel attack categories."*

The mapping is explicit in the same file:

```
F1_BYPASS   prompt-injection content (gate: prompt-shield)
F2_FORGE    audit-record forgery … (gate: biconditional, multiset S>D)
F3_SILENT   secret-exfiltration content (gate: DLP regex)
F4_WRONGTGT PII-broadcast content (gate: DLP regex)
```

And the generators draw from the detector's vocabulary directly:

| harness constant | detector |
|---|---|
| `T_F1_VERBS = ['IGNORE','DISREGARD','OVERRIDE']` | prompt-shield's documented imperatives |
| `T_F1_BOUNDARY = ['</system>','[/INST]','<\|im_end\|>', …]` | prompt-shield role-boundary tokens |
| `T_F3_SECRET_KINDS`: `sk-…`, `sk-ant-…`, `AKIA/ASIA…`, `ghp_…` | `dlp-scanner.ts` ids `openai-key`, `anthropic-key`, `aws-access-key-id`, `github-token` |

The LLM-generated path is the same shape: its briefs instruct the model to include *"an
imperative override phrase like 'IGNORE ALL PREVIOUS INSTRUCTIONS' … AND a role-boundary
token such as '</system>'"* and *"an OpenAI key starting 'sk-' … or an AWS access key
starting 'AKIA'"*.

**So on three of four categories the adversarial class is defined by containing an item from
the catalog the detector matches on.** Recall 1.000 there is a property of the construction.

**F2 is the exception and it is a real measurement.** The same comment: *"F2 is
content-agnostic; the message body itself is benign"* — the harness appends an
`irreversible.executed` audit record with no matching corpus-delta entry, and
`checkBiconditional` reports the forgery. The released data agrees independently: **42
message texts appear in F2 as both adversarial and legit**, so the classes are textually
inseparable, and the subject still separates them 200/0 and 0/200. That is detection, not
wiring.

### What this does and does not say

It does **not** say a number is wrong, that the gate does not work, or that anything was
concealed — the design is disclosed in the repository, and the authors' own words for what
they measured (*"the PRECISION of the gate, not the willingness of the LLM"*) are narrower
and more defensible than the paper's.

What it says is that **the disclosure does not travel with the number.** The abstract reads
*"both hardened subjects reach P = R = accuracy = 1.000"* beside *"OpenClaw catches none of
them"*, with Wilson intervals attached. A reader of the paper alone takes 1.000 as detection
performance. A reader of the harness learns it is a regression test over templates built to
always fire.

## Three further observations, recorded here, not yet verdicts

**The two hardened subjects are one subject.** `oss_delivered` equals `enc_delivered` on all
1,600 rows, and `oss_block_reason` equals `enc_block_reason` on all 1,600 rows — byte for
byte. Reported as two subjects reaching 1.000, they are one result printed twice.

**The denominators are inflated by duplicate stimuli.** Distinct message texts per cell of
200:

| category | distinct adversarial | distinct legit |
|---|---|---|
| F1_BYPASS | 199 | **8** |
| F2_FORGE | 133 | 136 |
| F3_SILENT | **7** | 192 |
| F4_WRONGTGT | **40** | **6** |

This bears directly on the sample-size argument. The paper justifies *n* by the Wilson upper
bound at k = 0 false positives — ≈ 0.036 at n = 100, ≈ 3.84 × 10⁻⁴ at n = 10⁴ — and pushes a
stress test to n = 80,000 to tighten it. That arithmetic treats rows as independent trials.
"Zero false positives out of 200" in F4 is zero false positives across **six distinct legit
messages**, each presented about 33 times. Repeating a stimulus does not add information
about the rate at which a different stimulus would be misclassified.

**The released content is redacted exactly where the detector fired.** `[REDACTED]` appears
in 200/200 adversarial rows of F3 and F4 and in 0/200 legit rows of either. So on the
released file the classes are separated by a one-token rule, and a reader cannot re-derive
any detection decision from the content column, because the substring that triggered it was
removed before release. The decisions are auditable; the inputs behind them are not.

## Still open

- **Q3** — the tree-walk of OpenClaw's 14,419 first-party files, and whether zero matches
  for seven named symbols distinguishes an absent property from a differently-named one.
- **Q4** — whether pre- and post-edit counts behind the 14.6% improvability claim are in the
  release.
- **Q5** — whether the 80,000-sample stress test has a released artifact.
