# Determinations — survey of self-reported verifier claims

Frame v3, hash `f97c68ded95ba8c3c236c985e1063d83ffc1bfc74e319883b47ee61c626943fe`,
50 papers, `seed=20260802`. Contract: [CONTRACT.md](CONTRACT.md).

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

Reading the sample surfaced a boundary the rule does not settle: **what about a paper
whose entire contribution is a detector or classifier?** Its precision is simultaneously a
checking component's performance and the paper's headline result.

**Reading adopted:** those are **out of scope**. A standalone detector has no *own*
verification component — it *is* the artifact under evaluation, scored by its authors
against a labelled set. That is ordinary supervised evaluation, and including it would
swamp the survey with routine ML papers while diluting the question asked.

The class targeted has three parts together: the system **does** something (generates,
answers, acts); it contains an **internal check** on its own output; and the paper reports
**how well that internal check does** — *"the verifier caught 8 of 40 errors"*, where the
errors are the system's own.

**Second rule, recorded when it first bit:** where inclusion is genuinely borderline,
**include**. A larger denominator can only hold the computable fraction down or leave it
unchanged, so erring this way runs against whatever this survey would prefer to find.
Marked `(borderline)` where used.

**Why recorded rather than quietly applied:** the boundary was found by reading, not fixed
in advance, so it is exactly the sort of decision that can be bent toward a nicer number.
Written down before any paper was resolved under it, so a reader can reject the rule itself
and re-derive the counts. Every call citing it is marked `[note]`.

**Known cost, accepted:** this excludes standalone guardrails a reasonable person might
include. Those exclusions are logged individually and counted, so the rule's effect on the
result is visible rather than buried. **20 of 50 fall out at this stage, 8 of them under
this note specifically.**

---

## Stage 1 — inclusion, from abstracts

`OUT` is final. `READ` means the abstract cannot settle it and the results section decides.

| id | call | reason |
|---|---|---|
| 2508.18513 | OUT | sepsis prediction; `admission` is hospital admission. No checking component |
| 2510.07642 | READ · abs only | abstract gives system refusal precision; results section still needed |
| 2512.05925 | OUT `[note]` | reports its own checker's precision — 263 of 316 flagged confirmed, 83.2% — but the checker inspects *other people's* papers, so the check is not over the system's own output |
| 2512.08326 | OUT `[note]` | Argus, standalone leakage detector |
| 2512.12492 | OUT | results give only joint detector+verifier metrics; the VLM verifier's own accept/reject accuracy is never isolated |
| **2602.24111** | **IN** (borderline) | no verifier accuracy against gold, but a quantitative component figure exists: *"manual spot-checking of 100 text-to-SMT translations by formal verification experts and found no translation errors"* — 0/100 on the autoformalisation stage. Included under *when borderline, include* |
| **2603.04549** | **IN** | A-MAC reports the admission controller's own precision 0.417 / recall 0.972 against ~1,500 ground-truth admission labels. Code released |
| 2603.11875 | OUT `[note]` | Mirror, standalone prompt-injection screen |
| **2603.13247** | **IN** | ILION reports the gate's own F1 0.8515, precision 91.0%, false-positive rate 7.9%. Benchmark and code linked |
| 2603.16723 | OUT | federated learning for postoperative outcomes; `admission` is ICU admission |
| 2603.20637 | OUT `[note]` | AEGIS, standalone vulnerability detector |
| **2604.07666** | **IN** | beyond the injected-noise study, reports real model-based verifiers' own precision/recall (Qwen3-30B ≈85%/>90%, 4B ≈70%/>90%) inside their own RLVR pipeline |
| 2604.11943 | READ | ProbeLogits, kernel-level safety check on the agent's own action |
| 2605.01727 | OUT | measures other people's models as classifiers — third-party clause |
| 2605.03065 | OUT | `critic` is the RL critic network |
| 2605.06669 | READ | authors' own multi-layer safeguard inside an LLM tutor |
| 2605.19075 | READ | CRAFT critic loop verifying its own claims; headline is end-task |
| 2605.31446 | READ | post-hoc verification of the system's own extracted triplets — target shape |
| 2606.05185 | OUT | `guard` is a product name (Event Guardian); crowd-monitoring CV |
| 2606.15833 | READ | asks whether textual verifiability tracks correctness, against gold triples |
| 2606.21690 | OUT `[note]` | phishing pipeline; `Domain Guard` is a component name, engines benchmarked standalone |
| 2606.21724 | READ | DISC verify-judge-correct loop over its own reasoning — target shape |
| 2606.26686 | OUT `[note]` | LeanGuard, standalone guardrail |
| 2607.07146 | OUT | the `validator` is a human expert adjudicating, not a component |
| 2607.19396 | OUT | benchmark evaluating PromptGuard and baselines — third-party clause |
| 2509.18868 | OUT | survey/taxonomy of LLM memory — surveys excluded by contract |
| 2510.11822 | READ | agreeableness bias in LLM judges; own mitigation vs third-party measurement unclear |
| 2510.21272 | READ | PMDetector, DeFi price manipulation; likely standalone |
| 2511.22521 | READ | DocVAL, a validator filtering the system's own teacher CoT — target shape |
| 2602.07954 | OUT `[note]` | Bielik Guard, standalone safety classifiers |
| 2602.10494 | READ | Canvas of Thought; `validator` role inside the reasoning loop |
| 2602.11731 | READ | optical decompression; term match looks incidental |
| 2603.12071 | READ | LoV3D brain-MRI pipeline; mentions hallucination control |
| 2605.00034 | READ | symbolic execution + agents including an Oracle/Validator and Safety Checker |
| 2605.01740 | READ | four failure modes of an agentic runtime, confusion matrices per cell — but measured on *upstream OpenClaw* |
| 2605.14665 | READ | Falkor-IRAC, graph-constrained legal generation with verification |
| 2605.24834 | OUT `[note]` | Reflect-Guard, standalone safety classifier |
| 2605.25447 | OUT | GeoSVG-RL; `precision` is geometric, `critic` is RL |
| 2605.26663 | READ | NEI-CAP; diagnoses what a verifier's score can hide |
| 2605.28830 | OUT | benchmarks 14 *open-source* guard models — third-party clause |
| 2606.09266 | OUT | acoustic metamaterial inverse design |
| 2606.09278 | OUT | geometric synthesis; `precision` is numerical |
| **2606.09682** | **IN** | AutoMegaKernel: a frozen schedule-IR validator certifies agent-proposed schedules; **"across 7,160 adversarial schedules (6,091 unsafe) it had zero false-accept"** — the system acts, an internal check gates it, and the check's own error count is the reported figure |
| 2606.24124 | READ | VeryTrace, verification-and-repair over its own reasoning traces — target shape |
| 2606.29225 | READ | PolicyGuard, a sub-agent verifier for policy adherence — target shape |
| 2607.06600 | OUT | MiLSD line-segment detector; `precision` is detection accuracy |
| 2607.13716 | READ | CAVA, action verification and attestation for agent runtimes |
| 2607.17987 | READ | relational inconsistency analysis of smart contracts |
| 2607.20852 | READ | can a weaker LLM verifier catch residual bugs; benchmark of verifiers generally |
| 2607.25069 | READ | CheckThat! system; the verifier *is* the system, likely OUT under the note |

**Stage 1 progress: 22 OUT · 5 IN · 23 still to read.** (updated as papers are resolved)

Of the 20 exclusions: 8 under the interpretive note (standalone detectors), 4 under the
contract's third-party clause, 1 survey, and 7 where the matched term was incidental —
hospital and ICU admission, an RL critic, a product name, a human adjudicator, and two
uses of `precision` meaning numeric precision. That last group is the known cost of
keeping the term lists frozen after v1, as stated in the contract.

---

## Stage 2 — determinations

Not started. Begins once inclusion is settled for all 50, so the denominator is fixed
before any artifact is opened.
