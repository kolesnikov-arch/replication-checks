# Survey — self-reported verifier claims: pre-registered frame (v2)

**Frozen before collection.** The selection rule below is committed first; the enumerated
list of papers it produces is committed as a **hash only** and revealed with the results.
Nothing here is revised after any determination is made; a change requires a new version
of this file stating why, with the previous version retained.

---

## v2 — why this version exists

**v1 is retained verbatim in [CONTRACT-v1.md](CONTRACT-v1.md). Its frame hash
`d50b15e8…46fbba` is void as a frame and is kept only as a record of what was frozen.**

v1's matcher tested whether a term appeared **anywhere in the abstract as a substring**.
It therefore matched `critic` inside `critical` and `criticism`. Measured on the retrieved
cache: **1,109 of the 1,382 papers in the v1 frame — 80% — contained no such term at all.**
The v1 sample of 25 was accordingly dominated by papers on angiography, astrocyte imaging,
robot badminton and 4-bit quantization, of which exactly one was on topic.

**What changed:** term matching now requires word boundaries. That is all.

**What deliberately did not change:** the term lists, the categories, the window, the
inclusion and exclusion rules, the sample cap and the seed. Matching a substring is not
applying the rule this contract states, so fixing it is a defect repair in the instrument.
Editing the *terms* would be something else entirely — by now their weaknesses are known
**from the data**, and a rule rewritten around observed output is no longer pre-registered.

**A known weakness is therefore carried into v2 on purpose.** `precision` and `recall` are
ambiguous: in a quantization paper `precision` means bit width. Those papers still enter
the frame. They are removed at the reading stage under the inclusion rule, **each with its
reason logged**, and the count of such removals is published. The result then carries two
numbers — how many the frame admitted, and how many actually report a figure about their
own verification component — because either alone would mislead.

This amendment was made **before any determination**. No finding rests on the v1 frame.

## Question — one

> Of papers that publish a quantitative claim about the performance of **their own**
> verification component, what fraction released enough for a third party to recompute
> that claim?

This is a base rate over a population. It is not a ranking, and it does not assess whether
any published number is correct — only whether it is checkable by someone who was not
there.

## What the hash does, and what it does not

**Corrected 2026-08-02, before collection.** An earlier draft of this section claimed the
hash keeps the population hidden from the papers' authors. That claim was wrong and is
withdrawn.

`select.py` is public, and it is the definition of record. Anyone — including any author
in scope — can run it and derive the same list, seed included. **The population is
knowable by construction, and that is accepted deliberately:** a selection rule that is
not public is not a pre-registration, it is a promise.

What the hash actually does is **bind the author of this survey, not its subjects.** It
proves the sample was not trimmed, extended or re-drawn after the determinations started
to come in — which is the first thing a reader should suspect and the only thing a
commitment device can settle. The list is published with the results so that the
commitment can be checked.

The real protection against a repository quietly gaining the missing fields after this
frame existed is not secrecy but **pinning**: every artifact is fixed to a commit SHA or
version at the collection date, and any later addition is visible as a change after that
pin. That is stated under *Determination* below and is not optional.

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

Matching is case-insensitive on the abstract text as returned by the API, **requires word
boundaries** (v2 — `critic` does not match `critical`), and treats a hyphen and a space as
equivalent on both sides, so that `self-check`, `self check` and a line-wrapped `self-
check` are one term. The retrieval script is committed with this contract and is the
definition of record; where prose and script disagree, the script governs.

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
with 14 days. Applied to a survey of 25 papers that would mean 25 advance letters — a
volume of unsolicited mail that turns a measurement into an outreach campaign, and one
that would reach authors before any determination about them had been made.

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
| frame frozen on | 2026-08-02 |
| frame rule frozen at commit | `74fbef2` (v1) · word-boundary repair in v2, this commit |
| collection ran at commit | `35016ec` |
| **enumerated list SHA256 (v2, binding)** | **`c1dceec6b1d46d2a94c93578b1b6c5a0af5061945683649705b6c5cbaebc3b04`** |
| ~~v1 hash~~ | ~~`d50b15e8…46fbba`~~ — void as a frame, see the v2 note above |
| candidates retrieved | 33,805 |
| in frame before sampling | **168** (v1: 1,382, of which 1,109 were substring artefacts) |
| sampled | 25, `seed=20260802` |
| list revealed | with the published result |

Verify the hash against the file when it is released: `sha256sum frame.txt`. The bytes
hashed are the bytes on disk — line endings are written explicitly, because a hash that
fails to verify against its own file reads as a swapped list.

### Amendments to retrieval between freeze and collection

The frame rule — terms, categories, window, inclusion, sample cap, seed, and `in_frame` —
is unchanged since `74fbef2`. Everything below changed **how candidates were fetched or
written**, never which papers the frame contains, and each is re-derivable offline from
the cache:

| commit | change | why it cannot move the frame |
|---|---|---|
| `83273ef` | verified TLS; abort instead of writing on a failed request; one union query instead of eight sweeps | a union of ORs is the same set; aborting writes nothing |
| `35016ec` | walk the window in calendar months | union of consecutive months = the year window; coverage asserted continuous, bounds match |
| this commit | `primary_category` extraction; explicit newline on write | `in_frame` reads `categories`, never `primary`; the list is byte-identical before and after, checked |

**Known discrepancy, recorded rather than reconciled:** arXiv's `totalResults` for the
union reported 33,806; 33,805 unique records were retrieved. One record's worth. It is not
chased because the difference cannot reach the sample without also changing the hash, and
the hash is what the result is bound to.
