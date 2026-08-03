# Survey — self-reported verifier claims: result

**Of 14 papers that publish a quantitative figure about their own verification component,
2 release enough for a third party to recompute it.**

Read the interval before the point estimate. At n=14 the computable share is 14.3% with a
Clopper–Pearson 95% interval of **[1.8%, 42.8%]** — 41 percentage points wide. This does
not establish that the rate is one in seven. What it supports, because the complement's
lower bound sits at 57.2%, is the weaker claim: **most such figures are not independently
checkable.** Anything tighter is not carried by this sample, and the contract fixed in
advance that this is what gets published rather than grounds to keep extending.

Protocol frozen before the data: [CONTRACT.md](CONTRACT.md) (v3; v1 and v2 retained).
Every determination with its reason: [DETERMINATIONS.md](DETERMINATIONS.md).
Frame list: [frame.txt](frame.txt), SHA256
`f97c68ded95ba8c3c236c985e1063d83ffc1bfc74e319883b47ee61c626943fe`.

## Result

| state | n | share | Clopper–Pearson 95% |
|---|---|---|---|
| **COMPUTABLE** | 2 | 14.3% | [1.8%, 42.8%] |
| RELEASED, NOT COMPUTABLE | 4 | 28.6% | [8.4%, 58.1%] |
| NOT RELEASED | 8 | 57.1% | [28.9%, 82.3%] |

`NOT COMPUTABLE` is a statement about what a release contains. It carries no implication
that any published number is wrong.

## The two that could be checked, both reproduced

Neither was merely judged computable. Both were recomputed, and both matched.

**arXiv:2605.06669** — multi-layer safeguard in an LLM tutor, artifact
`alemaiorano/educational-llm-guardrails-bench` @ `51628e8f0ae7`. From
`results/eval_multi-layer.csv`: 369 injections of which 198 blocked → **46.34% bypass**;
111 benign of which 0 blocked → **0.00% false positives**. The paper reports 46.34% and
0.00%.

**arXiv:2605.01740** — hardened agentic runtime, artifact `enclawed/enclawed-oss` @
`2876530a5339`. From `docs/adversarial-in-vivo-samples.csv`, 1,600 rows with per-sample
ground truth and per-subject decisions: upstream recall **0.000**, both hardened subjects
precision = recall = **1.000**. The paper reports the same.

That two of two reproduced is worth stating plainly. The finding is not that published
verifier numbers are wrong — where the release permitted a check, the numbers held. The
finding is that the release usually does not permit one.

## Why the other twelve could not be checked

Each fails a named condition from the contract: (A) ground truth determinable
independently of the authors' own labels, (B) a record of whether the checker fired,
(C) an identifier linking the two, (D) where repair is claimed, the pre-intervention state.

**Released, but not computable — 4.**

- `2603.04549` — 20 files, none of them data. Code only; the ~1,500 ground-truth admission
  labels and the controller's per-item decisions are absent. Fails A, B, C.
- `2603.13247` — ships 400 benchmark cases with `expected_verdict`. Ground truth is
  present; nothing records what the gate decided. A specification, not a run record.
  Fails B, C.
- `2606.09682` — publishes an unusually complete aggregate confusion matrix, including an
  explicitly empty list of false accepts. No per-schedule record, and condition A fails on
  the authors' own disclosure: *"the E2 dynamic oracle shares code with the system."*
  Recorded on their statement rather than our inference.
- `2604.07666` — a reproducibility gist exists but is an inference-and-scoring script; it
  contains no per-sample verifier decision. Fails B, C.

**Not released — 8.** Of these, two state that code and scripts *are* released and give no
location anywhere in the paper; one promises a future release; one cites internal
repository paths with no public URL; four give nothing. One of the four also discloses that
its ground-truth labels were *"assigned by a single annotator (the system developer)"* —
condition A would have failed even had the data shipped.

## How the 14 were arrived at

Frame: arXiv, categories cs.SE / cs.AI / cs.CL / cs.LG, submissions 2025-08-01 to
2026-07-31, abstract matching at least one component term and one claim term. 33,805
candidates retrieved, 168 in frame, 50 sampled with `seed=20260802`.

Of the 50, **35 were excluded at the reading stage, each with a logged reason**: 11 because
the checker is the paper's deliverable rather than an internal check on the system's own
output; 6 because the component measured belongs to someone else; 1 survey; 7 where the
matched term was incidental (hospital admission, ICU admission, an actor–critic network, a
product name, a human adjudicator, two numeric uses of "precision"); and **10 where a
verification component exists and is simply never measured** — credited only through an
end-task ablation.

## Limitations, including the ones that flatter this result

- **n=14.** The interval is 41 points wide. The point estimate should not be quoted alone.
- **The interpretive note.** Excluding papers whose deliverable *is* a checker is a reading
  of the contract's inclusion rule, adopted mid-survey and recorded before it was applied.
  11 exclusions rest on it. A reader who rejects it can add them back and re-derive.
- **The term lists were frozen after v1 despite known weakness.** "Precision" admits
  quantization papers. Fixing that after seeing the data would have made the rule no longer
  pre-registered, so the weakness shipped and its cost is the 7 incidental exclusions.
- **One inclusion call was reversed after determinations began**, and it moves the headline
  the way this survey would prefer. `2605.14665` was included on a figure quoted in a
  secondary source; the PDF names its metrics and reports no number for any. That paper has
  a released dataset, so dropping it lifts the computable share from 2/15 to 2/14. Put it
  back and the result is **13.3%, CI95 [1.7%, 40.5%]**.
- **Not a claim about correctness.** Nothing here says a published verifier figure is
  wrong. Where checking was possible, both held.

## A by-product, deliberately not the headline

Ten of the fifty build a verification component and report only what the end task scores
with and without it. Their verifier is never measured, only credited.

That is arguably a more interesting question than the one asked here, and it is exactly why
it is not promoted: the contract asks about computability among papers that *do* report a
figure, and swapping in a better question after seeing the data is the move this protocol
exists to prevent. It is reported as a count.

## Reproducing this

```
python select.py --offline      # re-derives frame.txt and its hash from the cache
sha256sum frame.txt             # must equal the hash above
```

The determination for each paper, with the condition it fails, is in
[DETERMINATIONS.md](DETERMINATIONS.md). Disagreement with any single call changes the
count; the reasons are there so that it can.

## Right of reply

Authors of the 14 papers in the denominator are notified at publication and have **14 days**
to respond. Any reply is published in full and unedited in `REPLY.md`. A factual error
identified by an author is corrected and the correction attributed. Silence is not
commented on.

This is lighter than the per-check policy in this repository, which sends a result to
authors *before* publishing. The reason is stated in the contract: a determination here is
a mechanical statement about which fields a pinned artifact contains, not an
interpretation of anyone's results.
