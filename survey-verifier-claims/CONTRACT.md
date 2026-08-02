# Survey — self-reported verifier claims: pre-registered frame

**Frozen before collection.** The selection rule below is committed first; the enumerated
list of papers it produces is committed as a **hash only** and revealed with the results.
Nothing here is revised after any determination is made; a change requires a new version
of this file stating why, with the previous version retained.

## Question — one

> Of papers that publish a quantitative claim about the performance of **their own**
> verification component, what fraction released enough for a third party to recompute
> that claim?

This is a base rate over a population. It is not a ranking, and it does not assess whether
any published number is correct — only whether it is checkable by someone who was not
there.

## Why a hash and not a list

Publishing the enumerated list before collection would change the thing being measured:
an author who sees a forthcoming audit can add telemetry to their repository, and the
result would then measure reactions to this survey rather than the state of the practice.

So: the selection **rule** is public now; the **list** is frozen, its SHA256 published at
freeze, and the list itself released with the results. Anyone can then verify it was not
edited. Same primitive as the evidence attestation used elsewhere in this work.

## Selection frame — fixed here, before collection

**Source.** arXiv, via the public API. No other venue; a second source would need its own
frame.

**Categories.** Primary or cross-listed in `cs.SE`, `cs.AI`, `cs.CL`, `cs.LG`.

**Window.** Submissions dated **2025-08-01 through 2026-07-31** inclusive, by first
version date. A twelve-month window ending before this freeze, so no paper can enter or
leave by being posted after the rule existed.

**Candidate retrieval.** Abstract matches at least one term from each of two sets:

- component: `verifier`, `verification loop`, `validator`, `checker`, `critic`,
  `self-check`, `guard`, `admission`
- claim: `false accept`, `false alarm`, `false positive`, `precision`, `recall`,
  `catch rate`, `confusion matrix`, `detection rate`

Matching is case-insensitive on the abstract text as returned by the API. The retrieval
script is committed with this contract and is the definition of record; where prose and
script disagree, the script governs.

**Inclusion.** The paper reports at least one quantitative figure describing how well its
**own** verification component performs — not the end-task score the system achieves with
it. The distinction is the whole survey: `+11 points on the benchmark` is out of scope,
`the verifier caught 8 of 40 errors` is in scope.

**Exclusion.** Surveys and position papers. Papers where the verifier under measurement
belongs to someone else — third-party evaluation is a different act and is not what this
counts. Papers with no self-reported verifier figure after reading the results section.

**Size.** If the frame yields more than 25 papers, a random sample of 25 is drawn with
`seed=20260802` and the seed and the full enumeration are published together. If it yields
fewer than 10, see stop conditions.

## Determination per paper — three states

For each paper, the artifact it points to (repository, supplementary archive, dataset) is
**pinned by commit SHA or version at the collection date** and examined against three
mechanical conditions. To recompute a claim of the form *our checker caught X of Y*, the
release must permit, per unit of analysis:

| # | condition |
|---|---|
| A | ground-truth correctness determinable independently of the authors' own labels |
| B | whether the checker fired on that unit |
| C | the two linked — the same identifier joins A and B |

Where the claim involves repair, a fourth applies: **D** — the pre-intervention artifact
or answer is recoverable.

| state | condition |
|---|---|
| **COMPUTABLE** | all applicable conditions met |
| **RELEASED, NOT COMPUTABLE** | an artifact exists; at least one condition fails; which ones is recorded |
| **NOT RELEASED** | no artifact, or the link is dead at the collection date |

Nothing is recomputed in the survey. Whether a `COMPUTABLE` claim actually reproduces is a
separate, deeper act — that is what the numbered checks in this repository do, and any
such paper becomes a candidate for one.

## Metrics

Proportion of the frame in each state, each with a Clopper–Pearson 95% interval, plus a
per-condition breakdown of which of A–D fail most often. No point estimate without an
interval.

## Prior case

`001-leni` was checked in depth before this frame existed. If arXiv:2607.17044 falls
inside the frame it enters as an ordinary member; the fact that it was examined first, and
that its examination motivated this survey, is declared in the result rather than hidden.
Its determination is recomputed under the conditions above, not carried over.

## Right of reply — deliberately lighter than a deep check

The per-check policy in this repository sends the result to the authors before publication
with 14 days. Applied to a survey of 25 papers that would mean 25 advance letters, which
is precisely the leakage the hash exists to prevent.

So, for the survey only:

1. Authors are notified **at publication**, not before.
2. A **14-day correction window** runs from publication. Factual corrections are folded in
   and attributed to whoever supplied them.
3. Any reply is published in full and unedited.

This is defensible because a survey determination is a mechanical statement about which
fields a pinned artifact contains, not an interpretation of anyone's results. **Deep
checks keep the strict policy unchanged.**

## Stop conditions

- **Frame yields fewer than 10 papers** → publish that the frame is too narrow to support
  a rate, with the enumeration. Do **not** widen the rule afterwards; a wider rule is a
  new contract with a new freeze.
- **Most papers come out `COMPUTABLE`** → publish it. "The practice is in better shape
  than expected" is a result and is not a reason to reframe, delay, or go looking for a
  worse-looking subset.
- **A paper cannot be classified** because the claim's form does not fit conditions A–D →
  it is reported as unclassifiable with the reason, not forced into a state.

## Prohibited

- Widening, narrowing or re-running the selection rule after any determination is made.
- Choosing papers by how likely they are to fail. The rate is the product; selecting on
  the outcome destroys it.
- Dropping a paper because its determination is inconvenient.
- Publishing the rate without the enumeration and the seed.
- Any offer, availability note, or link to anything for sale.

---

**Freeze record**

| | |
|---|---|
| frame frozen on | `________________________` |
| this contract's commit | `________________________` |
| retrieval script commit | `________________________` |
| enumerated list SHA256 | `________________________` |
| collection began | `________________________` |
| list revealed | with the published result |
