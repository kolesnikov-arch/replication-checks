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
result is visible rather than buried. **Final: 11 of the 35 exclusions rest on this note.**
A reader who rejects the note can add those 11 back and re-derive everything.

---

## Stage 1 — inclusion, from abstracts

`OUT` is final. `READ` means the abstract cannot settle it and the results section decides.

| id | call | reason |
|---|---|---|
| 2508.18513 | OUT | sepsis prediction; `admission` is hospital admission. No checking component |
| 2510.07642 | OUT | verifier-swap ablation shows how verifier choice moves *system* precision/recall; the verifier's own false-permit rate is never isolated. Datasets and code released, but no claim about the verifier to check |
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
| **2606.15833** | **IN** | reports their own verifier against gold deleted triples: edge precision 15.2% / 21.4%, false-rejection rate 24.4% / 50.2%. Code, prompts and eval scripts stated as released |
| 2606.21690 | OUT `[note]` | phishing pipeline; `Domain Guard` is a component name, engines benchmarked standalone |
| **2606.21724** | **IN** | DISC reports judge precision 71.3% / recall 85.6%, true-positive fix rate 66.2%, false-positive destruction rate 54.8%. No artifacts mentioned |
| 2606.26686 | OUT `[note]` | LeanGuard, standalone guardrail |
| 2607.07146 | OUT | the `validator` is a human expert adjudicating, not a component |
| 2607.19396 | OUT | benchmark evaluating PromptGuard and baselines — third-party clause |
| 2509.18868 | OUT | survey/taxonomy of LLM memory — surveys excluded by contract |
| 2510.11822 | OUT `[note]` | measures 14 off-the-shelf judges (TPR >96%, TNR <25%) and proposes an ensemble reaching 95.5% / 30.9%. The ensemble is the deliverable, not a check on the system's own output |
| 2510.21272 | OUT | has a semantic sanity checker, but reports only its *contribution* — system precision 0.90 → 0.83 without it — never its own accuracy |
| 2511.22521 | OUT | reports only a 92.7% retention rate — how often the validator fired, not how often it was right — plus downstream mAP. Artifacts *are* released; there is simply no claim about the validator to check |
| 2602.07954 | OUT `[note]` | Bielik Guard, standalone safety classifiers |
| 2602.10494 | OUT | critique component shown only through end-task ablation gains; no intrinsic accuracy. Code "will be released soon" |
| **2602.11731** | **IN** (borderline) | its LLM-as-judge verifier is calibrated against domain experts to **96% agreement on 1,000 instances** before use. A quantitative figure about the checking component; included under *when borderline, include* |
| 2603.12071 | OUT | LoV3D's Verifier checks reasoning-label consistency but no detection rate or false-positive rate is reported; only end-to-end 93.7% and region-level 82.6%. Code link is an anonymised review repository |
| 2605.00034 | OUT | only aggregate pipeline numbers (fallback 42% → 9.7%, 83.9% detection); the Oracle/Validator and Safety Checker are never scored individually. Replication package released |
| **2605.01740** | **IN** | measures upstream OpenClaw *and* the authors' own hardened runtime: precision = recall = F1 = 1.000 per F-category at n=1600, Wilson bound 3.84e-4 at n=10,000. Public harness plus a CSV of per-sample ground truth and per-subject decisions |
| 2605.14665 | **OUT — call reversed, see below** | included at first on a figure quoted in a secondary source; direct reading of the PDF shows the paper names its metrics (citation grounding, hallucinated precedent, conflict detection) and reports **no number for any of them**. It does not report a figure, so it does not belong in a survey of papers that do |
| 2605.24834 | OUT `[note]` | Reflect-Guard, standalone safety classifier |
| 2605.25447 | OUT | GeoSVG-RL; `precision` is geometric, `critic` is RL |
| 2605.26663 | OUT `[note]` | authors' own verifiers, with real decision quality (NEI recall 0.691 vs 0.000, false-Support error 0.870) — but the verifier is the object of study, not an internal check on something the system produced. Same class as 2607.25069 and 2510.11822 |
| 2605.28830 | OUT | benchmarks 14 *open-source* guard models — third-party clause |
| 2606.09266 | OUT | acoustic metamaterial inverse design |
| 2606.09278 | OUT | geometric synthesis; `precision` is numerical |
| **2606.09682** | **IN** | AutoMegaKernel: a frozen schedule-IR validator certifies agent-proposed schedules; **"across 7,160 adversarial schedules (6,091 unsafe) it had zero false-accept"** — the system acts, an internal check gates it, and the check's own error count is the reported figure |
| **2606.24124** | **IN** | VeryTrace, textbook: acceptance precision 0.895, recall 0.886, **false-accept rate 0.097**, false-reject 0.114. No artifact URL |
| **2606.29225** | **IN** | PolicyGuard reports per-call verdict confusion matrices, policy-violation recall by vendor, block rates. Release promised, no URL |
| 2607.06600 | OUT | MiLSD line-segment detector; `precision` is detection accuracy |
| **2607.13716** | **IN** | CAVA reports its own catch rate 1.000 and false-positive control 1.000 over 96 seeds / 384 variants. Harness and REPRODUCE.md referenced; parser packs and policy thresholds proprietary |
| 2607.17987 | OUT | reports a funnel (3,217 → 1,643 → 201 → 44 → 13) and states plainly it cannot compute precision or recall without a labelled benchmark. A funnel is an operating statistic, not a performance figure — same reading as 2511.22521 |
| 2607.20852 | OUT | reports monitor TPR/FPR in detail (Qwen-7B misses 94.0% of hidden bugs at 5% FPR) but the monitors are off-the-shelf models — third-party clause |
| 2607.25069 | OUT `[note]` | the LoRA verifier *is* the shared-task system; its macro-F1 is the leaderboard score, not a check on the system's own output |

### Stage 1 is complete: **35 OUT · 15 IN**, all 50 resolved with a reason.

**The denominator is 15.** It is fixed here, before any artifact is opened.

Why the 35 fell out: 11 under the interpretive note (the checker *is* the deliverable),
6 under the contract's third-party clause, 1 survey, 7 where the matched term was
incidental (hospital and ICU admission, an RL critic, a product name, a human
adjudicator, two numeric uses of `precision`), and **10 where a verification component
exists and is simply never measured** — only credited through an end-task ablation.

At n=15 the interval will be wide: five computable out of fifteen would read
[0.12, 0.62]. The contract anticipated this and fixed the response in advance — if the
surviving denominator cannot support a claim, that is what gets published, not grounds to
keep extending until the number firms up.

**Descriptive by-product, not the pre-registered question.** Ten of the fifty build a
verification component and report only what the end task scores with and without it —
CRAFT, the ASTE verifier, DocVAL, PMDetector, Canvas of Thought, LoV3D, the SQL-policy
verifier, the multi-agent Rust checker, and others. Their verifier is never measured, only
credited. That is the same practice this survey's first deep check
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

Denominator fixed at 15 before the first artifact was opened. Each artifact pinned by
commit at the collection date, per the contract.

| id | artifact @ pin | state | which condition fails |
|---|---|---|---|
| **2605.06669** | `alemaiorano/educational-llm-guardrails-bench` @ `51628e8f0ae7` | **COMPUTABLE** | none — and **reproduced**: 369 injections / 198 blocked = 46.34% bypass, 111 benign / 0 blocked = 0.00% FPR. Every published figure recomputed exactly from `results/eval_multi-layer.csv` |
| **2605.01740** | `enclawed/enclawed-oss` @ `2876530a5339` | **COMPUTABLE** | none — and **reproduced**: from `docs/adversarial-in-vivo-samples.csv` (1,600 rows, 800 legit / 800 adversarial) OpenClaw recall 0.000, both hardened subjects precision = recall = 1.000. Matches the paper |
| 2603.04549 | `GuilinDev/Adaptive_Memory_Admission_Control_LLM_Agents` @ `40407aec883b` | RELEASED, NOT COMPUTABLE | **A, B, C.** 20 files, zero data files. Code only: scorers, features, baselines. The ~1,500 ground-truth admission labels and the controller's per-item decisions are not in the release |
| 2603.13247 | `Athonitul/ilion-framework-simulator` @ `94efd5cc3101` | RELEASED, NOT COMPUTABLE | **B, C.** `benchmark/benchmark_v2.csv` gives 400 cases with `expected_verdict` — ground truth is there — but nothing records what the gate actually decided. A benchmark specification, not a run record |
| 2606.09682 | `RightNow-AI/AutoMegaKernel` @ `a514bbc20a03` | RELEASED, NOT COMPUTABLE | **A, and C.** `paper/results/validator_soundness.json` is unusually complete — full confusion matrix, breakdowns by mutant class and reject reason, an explicitly empty `false_accepts` list — but it is aggregate, with no per-schedule record. And condition A fails on the authors' own disclosure: *"The E2 dynamic oracle shares code with the system"*, so ground truth is not independent of the system being judged. Recorded on their statement, not our inference |
| 2604.07666 | gist `AndreasPlesner-hs/1b66fb59091e62496906b0b35960fdc3` @ rev `67ca79b0c082` (single revision, 2026-04-07) | RELEASED, NOT COMPUTABLE | **B, C.** The Reproducibility appendix links one unlisted gist holding a single 158-line file, `tinker_example.py`, which samples the untrained base model on MBPP validation to explain why the paper's pre-training numbers differ from the Qwen team's technical report. It is not an artifact of the verifier claim at all: the per-batch verifier decisions behind the precision and recall plotted in Figure 5 are not in it (B), and nothing joins them to the unit-test outcomes (C). **Condition A holds** — the ground truth is MBPP's own unit tests, independent of the verifier and of the authors' labels, and the paper says so explicitly |
| 2606.15833 | — | NOT RELEASED | *"Code, prompts, and evaluation scripts are released"* — with no location anywhere in the paper |
| 2607.13716 | — | NOT RELEASED **at the frame date** | artifact manifest cites internal paths (`docs/research/papers/cava`, `benchmarks/source-benchmark.mjs`); **no artifact URL.** The paper's nine links are all third-party standards and references (in-toto, Sigstore, OpenTelemetry, NIST, OWASP). **After notification the author published a public mirror on 2026-08-05 and it re-checks as COMPUTABLE and recomputed on 2026-08-06 — see [REPLY.md](REPLY.md). The determination above is not revised: it is what the pin recorded, and the count stays 2/14** |
| 2606.29225 | — | NOT RELEASED | Ethics statement promises a future release of prompts and policy schemas, with no address. The paper's four links are all vendor model cards cited as sources; **no artifact URL** |
| 2602.24111 | — | NOT RELEASED | no URL anywhere; the 100 spot-checked SMT translations are not obtainable |
| 2602.11731 | — | NOT RELEASED | no URL anywhere; the 1,000-instance expert-agreement set is not obtainable |
| 2604.11943 | — | NOT RELEASED | **no artifact URL.** The paper's only link is to a third party's repository cited as a tool (`meta-llama/PurpleLlama`); nothing of the authors' own is released. The author also discloses that ground-truth labels were *"assigned by a single annotator (the system developer)"* — condition A would fail even had the data shipped |
| 2606.21724 | — | NOT RELEASED | no URL anywhere; per-item judge decisions behind 71.3% / 85.6% are not obtainable |
| 2606.24124 | — | NOT RELEASED | no URL anywhere; the ProcessBench per-item data behind a false-accept rate of 0.097 is not obtainable |

### A stage-1 call reversed after stage 2 began — recorded, and it flatters the result

**2605.14665 was moved from IN to OUT.** It was included on a figure quoted in a secondary
source; reading the PDF directly showed the paper names its verifier metrics and reports no
number for any of them. A paper that reports no figure cannot be in a survey of papers that
report figures, so the correction is right on the merits.

It must still be flagged, because **it moves the headline in the direction this survey
would prefer.** The paper does have a released dataset, so it would have been a
`RELEASED, NOT COMPUTABLE`; dropping it lifts the computable fraction from 2/15 to 2/14.
A correction that happens to help is the kind that deserves the most scrutiny, so it is
written here rather than absorbed into a revised count. A reader who disagrees can put it
back: the result becomes 2/15 = 13.3%, CI95 [1.7%, 40.5%].

**Denominator: 14.**

---

## Result

| state | count | share | Clopper–Pearson 95% |
|---|---|---|---|
| **COMPUTABLE** | 2 | 14.3% | [1.8%, 42.8%] |
| RELEASED, NOT COMPUTABLE | 4 | 28.6% | [8.4%, 58.1%] |
| NOT RELEASED | 8 | 57.1% | [28.9%, 82.3%] |

Stated the other way round: **of 14 papers publishing a quantitative figure about their own
verification component, 12 — 85.7%, CI95 [57.2%, 98.2%] — do not release enough for a third
party to recompute it.**

**Read the interval before the point estimate.** At n=14 the computable share is consistent
with anything from 1.8% to 42.8%, a span of 41 percentage points. This does not establish
that the rate is 14%. What it does support, because the lower bound of the complement sits
at 57.2%, is the weaker and more defensible claim: **most such figures are not independently
checkable.** Any sentence tighter than that is not carried by n=14, and the contract fixed
in advance that this is what gets published rather than grounds to keep extending.

Both computable cases were not merely judged computable but **recomputed exactly**, which is
the only reason the numerator is trustworthy at all.
