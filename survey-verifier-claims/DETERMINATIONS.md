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
| **2604.11943** | **IN** | ProbeLogits reports its own gate metrics: F1 0.980 / precision 1.000 / recall 0.960 on 260 OS actions, and ≈22% false-positive rate on ToxicChat. No artifacts mentioned |
| 2605.01727 | OUT | measures other people's models as classifiers — third-party clause |
| 2605.03065 | OUT | `critic` is the RL critic network |
| **2605.06669** | **IN** | safeguard pipeline's own numbers: 46.34% bypass, 0.00% false positives, 111/111 benign passed, 198/369 attacks blocked. Code and data linked |
| 2605.19075 | OUT | ablation reports only end-task citation F1 (0.635 → 0.601); the critic's own accept/reject accuracy is never measured. Code released, but no claim to check |
| 2605.31446 | OUT | all reported metrics are end-to-end ASTE F1 after filtering; verifier-only decision quality absent |
| 2606.05185 | OUT | `guard` is a product name (Event Guardian); crowd-monitoring CV |
| 2606.15833 | READ | asks whether textual verifiability tracks correctness, against gold triples |
| 2606.21690 | OUT `[note]` | phishing pipeline; `Domain Guard` is a component name, engines benchmarked standalone |
| **2606.21724** | **IN** | DISC reports judge precision 71.3% / recall 85.6%, true-positive fix rate 66.2%, false-positive destruction rate 54.8%. No artifacts mentioned |
| 2606.26686 | OUT `[note]` | LeanGuard, standalone guardrail |
| 2607.07146 | OUT | the `validator` is a human expert adjudicating, not a component |
| 2607.19396 | OUT | benchmark evaluating PromptGuard and baselines — third-party clause |
| 2509.18868 | OUT | survey/taxonomy of LLM memory — surveys excluded by contract |
| 2510.11822 | READ | agreeableness bias in LLM judges; own mitigation vs third-party measurement unclear |
| 2510.21272 | READ | PMDetector, DeFi price manipulation; likely standalone |
| 2511.22521 | OUT | reports only a 92.7% retention rate — how often the validator fired, not how often it was right — plus downstream mAP. Artifacts *are* released; there is simply no claim about the validator to check |
| 2602.07954 | OUT `[note]` | Bielik Guard, standalone safety classifiers |
| 2602.10494 | READ | Canvas of Thought; `validator` role inside the reasoning loop |
| 2602.11731 | READ | optical decompression; term match looks incidental |
| 2603.12071 | READ | LoV3D brain-MRI pipeline; mentions hallucination control |
| 2605.00034 | READ | symbolic execution + agents including an Oracle/Validator and Safety Checker |
| **2605.01740** | **IN** | measures upstream OpenClaw *and* the authors' own hardened runtime: precision = recall = F1 = 1.000 per F-category at n=1600, Wilson bound 3.84e-4 at n=10,000. Public harness plus a CSV of per-sample ground truth and per-subject decisions |
| 2605.14665 | READ | Falkor-IRAC, graph-constrained legal generation with verification |
| 2605.24834 | OUT `[note]` | Reflect-Guard, standalone safety classifier |
| 2605.25447 | OUT | GeoSVG-RL; `precision` is geometric, `critic` is RL |
| 2605.26663 | READ | NEI-CAP; diagnoses what a verifier's score can hide |
| 2605.28830 | OUT | benchmarks 14 *open-source* guard models — third-party clause |
| 2606.09266 | OUT | acoustic metamaterial inverse design |
| 2606.09278 | OUT | geometric synthesis; `precision` is numerical |
| **2606.09682** | **IN** | AutoMegaKernel: a frozen schedule-IR validator certifies agent-proposed schedules; **"across 7,160 adversarial schedules (6,091 unsafe) it had zero false-accept"** — the system acts, an internal check gates it, and the check's own error count is the reported figure |
| **2606.24124** | **IN** | VeryTrace, textbook: acceptance precision 0.895, recall 0.886, **false-accept rate 0.097**, false-reject 0.114. No artifact URL |
| **2606.29225** | **IN** | PolicyGuard reports per-call verdict confusion matrices, policy-violation recall by vendor, block rates. Release promised, no URL |
| 2607.06600 | OUT | MiLSD line-segment detector; `precision` is detection accuracy |
| **2607.13716** | **IN** | CAVA reports its own catch rate 1.000 and false-positive control 1.000 over 96 seeds / 384 variants. Harness and REPRODUCE.md referenced; parser packs and policy thresholds proprietary |
| 2607.17987 | READ | relational inconsistency analysis of smart contracts |
| 2607.20852 | READ | can a weaker LLM verifier catch residual bugs; benchmark of verifiers generally |
| 2607.25069 | READ | CheckThat! system; the verifier *is* the system, likely OUT under the note |

**Stage 1 progress: 25 OUT · 12 IN · 13 still to read.** (updated as papers are resolved)

**Descriptive by-product, not the pre-registered question.** A pattern is showing among
the papers read in full: several build a verification component and report only what the
end task scores with and without it — CRAFT, the ASTE verifier, DocVAL. Their verifier is
never measured, only credited. That is the same practice this survey's first deep check
found in a production system, and it will be reported as an observation with its count,
never as the headline: the contract asks about computability among papers that *do*
report, and retrofitting a nicer question after seeing the data is the one move the whole
protocol exists to prevent.

Of the 20 exclusions: 8 under the interpretive note (standalone detectors), 4 under the
contract's third-party clause, 1 survey, and 7 where the matched term was incidental —
hospital and ICU admission, an RL critic, a product name, a human adjudicator, and two
uses of `precision` meaning numeric precision. That last group is the known cost of
keeping the term lists frozen after v1, as stated in the contract.

---

## Stage 2 — determinations

Not started. Begins once inclusion is settled for all 50, so the denominator is fixed
before any artifact is opened.
