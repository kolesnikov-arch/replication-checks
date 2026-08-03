# Determinations — survey of self-reported verifier claims

Frame v2, hash `c1dceec6b1d46d2a94c93578b1b6c5a0af5061945683649705b6c5cbaebc3b04`,
25 papers, `seed=20260802`. Contract: [CONTRACT.md](CONTRACT.md).

Two stages per paper, both logged with a reason:

1. **Inclusion** — does it report a quantitative figure about how well *its own*
   verification component performs?
2. **Determination** — if included, is that figure recomputable from what was released:
   `COMPUTABLE` / `RELEASED, NOT COMPUTABLE` / `NOT RELEASED`.

---

## Interpretive note, recorded before it was applied

The contract's inclusion rule reads: *"reports at least one quantitative figure describing
how well its **own** verification component performs — not the end-task score the system
achieves with it."*

Reading the sample surfaced a boundary the rule does not settle explicitly: **what about a
paper whose entire contribution is a detector or classifier?** Its precision is
simultaneously the performance of a checking component and the paper's headline result.

**Reading adopted:** such papers are **out of scope**. A standalone detector has no *own*
verification component — it *is* the artifact under evaluation, scored by its authors
against a labelled set. That is ordinary supervised evaluation, and it would swamp this
survey with routine ML papers while diluting the question actually being asked.

The class this survey targets has three parts together: the system **does** something
(generates code, answers, acts); it contains an **internal check** on its own output; and
the paper reports **how well that internal check does**. That is the shape of the claim
which motivated the survey — *"the verifier caught 8 of 40 errors"*, where the errors are
the system's own.

**Why this is recorded rather than quietly applied:** the boundary was found by reading,
not fixed in advance, so it is exactly the kind of decision that can be bent to produce a
nicer number. Written down first, before any paper was resolved under it, so that a reader
can disagree with the rule itself and re-derive the counts. Every borderline call below
cites it.

**Known consequence, accepted:** this reading excludes some papers a reasonable person
would include — a standalone guardrail evaluated on its own bypass rate, for instance.
Those exclusions are logged individually with this note as the reason, and their count is
published, so the effect of the rule on the result is visible rather than buried.

---

## Stage 1 — inclusion pass (from abstracts; borderline cases go to the paper)

| # | id | call | reason |
|---|---|---|---|
| 1 | 2508.18513 | **OUT** | healthcare privacy / sepsis prediction. `admission` is hospital admission; `precision`/`recall` are the prediction model's. No checking component of any kind |
| 2 | 2510.07642 | READ | generator–verifier pipeline over SQL policy. Abstract reports *system* refusal precision; whether the verifier's own decision quality is reported separately needs the results section |
| 3 | 2512.05925 | READ | a Paper Correctness Checker applied to others' papers. Likely reports its own precision, but the object checked is third-party work — the exclusion for *"the verifier under measurement belongs to someone else"* may cut the other way. Needs the paper |
| 4 | 2512.08326 | READ | Argus, sensitive-information leakage detection, headline is reducing false positives. Standalone detector → likely **OUT** under the interpretive note; confirming against the results section |
| 5 | 2512.12492 | READ | detector + VLM verifier, two-stage. Abstract reports detection precision/recall (end-task). Whether the verifier's own accuracy appears needs the paper |
| 6 | 2602.24111 | READ | neurosymbolic verifier auditing a VLM's *own* report consistency — the target shape. Needs the paper for whether the verifier's accuracy is quantified |
| 7 | 2603.04549 | READ | A-MAC memory admission control inside an agent — the target shape. Needs the paper for a figure on the controller itself |
| 8 | 2603.11875 | READ | Mirror prompt-injection screen, 95.97% recall / 92.07% F1 on a 524-case holdout. Standalone detector → likely **OUT** under the note; confirming |
| 9 | 2603.13247 | READ | ILION, deterministic execution gate for agent actions. Gate sits between agent and effect — plausibly in scope; needs the paper |
| 10 | 2603.16723 | **OUT** | federated learning for postoperative outcomes. `admission` is ICU admission. No checking component |
| 11 | 2603.20637 | READ | AEGIS vulnerability detection. Standalone detector → likely **OUT** under the note; confirming |
| 12 | 2604.07666 | READ | studies how much verifier noise RLVR tolerates, injecting known error rates. About verifier accuracy in general rather than a measurement of the authors' own verifier — needs the paper |
| 13 | 2604.11943 | READ | ProbeLogits, a kernel-level safety check on an agent's action using the same model's logits. Target shape; needs the paper |
| 14 | 2605.01727 | **OUT** | measures *other people's* models as news classifiers. Explicitly excluded: the component under measurement belongs to someone else |
| 15 | 2605.03065 | **OUT** | `critic` is the RL critic network in an actor–critic policy. Not a checking component |
| 16 | 2605.06669 | READ | evaluates the authors' own multi-layer safeguard inside an LLM tutor, reporting bypass and false-positive rates. Target shape; needs the paper |
| 17 | 2605.19075 | READ | CRAFT, a critic loop that verifies and repairs claims before consolidation. Headline figures are end-task; needs the paper |
| 18–25 | — | pending | not yet read |

Counts so far: **5 OUT**, **12 to read**, 8 not yet reached.

---

## Stage 2 — determinations

Not started. Begins once inclusion is settled for all 25, so that the denominator is fixed
before any artifact is opened.
