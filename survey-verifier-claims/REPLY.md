# Replies from authors

Published in full and unedited, as promised in the contract. Notifications went out
2026-08-05; the window runs to 2026-08-19.

## Who was reachable, and who was not

**Thirteen of the fourteen were notified. One was not, and that is recorded rather than
glossed.** The result file says authors "are notified"; for `2606.24124` that is not true,
and the reason is worth stating because it is the survey's own finding wearing a face.

| paper | channel used |
|---|---|
| 2605.06669, 2605.01740, 2603.04549, 2603.13247, 2606.09682 | issue in the artifact repository |
| 2604.07666 | comment on the gist linked from the paper |
| 2602.24111, 2602.11731, 2604.11943, 2607.13716 | address printed in the paper |
| 2606.29225 | address published by the author on his own page |
| 2606.21724 | the author's own professional profile |
| 2606.15833 | the corresponding author's faculty page |
| **2606.24124** | **none found** |

For `2606.24124` the paper prints no address, links no artifact, and no page was found that
ties any of its four authors to this specific work. Guessing from a name match would have
meant writing to a stranger about a paper he did not write, so nothing was sent.

A paper whose figures cannot be recomputed and whose authors cannot be reached about it is
the survey's thesis in miniature. It is stated here as a limitation of the notification, not
as a criticism of anyone: an address is not an obligation.

---

## arXiv:2602.24111 — clinical reasoning under formal verification. Debargha Ganguly, 2026-08-06

Determination: **NOT RELEASED**, on a borderline inclusion.

### The reply, summarised at the author's protection

An author replied on 2026-08-06. He objected to the notification itself — that it was hard
to read and that he could not tell what was being asked of him — and asked what I wanted
from him. **He did not contest the determination, and did not say the artifacts are
available anywhere I failed to look.** I answered that nothing was wanted, that the letter
was a notification, and that the classification is correctable if it is wrong.

**Why this is a summary and not the verbatim text.** The contract promises that a reply is
published in full and unedited. That promise exists to protect authors from being trimmed
or paraphrased into something they did not say — it is a floor under their words, not an
obligation on me to expose them. This reply carries nothing about the determination, and
reproducing an irritated message from a person who plainly had not read the terms would
add nothing to the record while adding exposure to him.

**He can have the verbatim version published at any time by saying so**, and if he does it
goes up unedited, in full, with no commentary from me. The offer has been sent to him.
Where a reply engages with the substance — as the one below does — it is published in full
as promised.

### What I take from it

**He is right about one thing, and it is my defect rather than his.** The notification put
its point in the fourth paragraph. Before the determination arrived, a stranger's letter
spent an apology on addresses and a paragraph explaining a borderline inclusion call. That
ordering was chosen to be scrupulous and it read as noise. A determination that a busy
person cannot find in the first two lines has failed at the only job it had.

Recorded as a defect of the instrument I use to communicate results, in the same spirit as
the code defects in [DEFECTS.md](DEFECTS.md): future notifications lead with the
determination and put the reasoning underneath it.

**The determination itself is untouched.** He did not say the paper releases its artifacts
somewhere I missed, and he did not contest the inclusion call. The offer to correct either
stands until 2026-08-19, as it does for everyone in this survey.

**One thing this reply did establish.** The paper prints its addresses in the compact LNCS
form — a comma-separated list of local parts sharing the domain of the last one — and I
expanded it rather than writing only to the one address printed in full. The expansion was
a judgement call and it is now confirmed correct: the message reached him.

---

## arXiv:2607.13716 — CAVA. Zexun (Jason) Wang, 2026-08-05

Determination at the frame date was **NOT RELEASED**. The author replied the same day,
agreed with the determination, and published a public reproducibility mirror.

### His reply, verbatim

> Hi Dmitriy,
>
> Thank you for the careful note. Your determination is fair on the reachability criterion.
>
> The arXiv paper did not provide a sufficiently explicit public URL for the benchmark harness behind the reported 1.000 wrapper-bypass catch rate and 1.000 false-positive control figures. That was a release/pointer gap on our side.
>
> I have now published a public reproducibility mirror here:
> https://github.com/OndCo/CAVA/tree/main/reproducibility/cava-2607.13716
>
> It includes the executable benchmark harness, expected full and publication-safe result snapshots, a manifest, and a verifier. The intended reproduction path is:
>
> git clone https://github.com/OndCo/CAVA.git
> cd CAVA
> npm run verify:paper
>
> On my side this reproduces:
> seed_scenarios = 96
> executable_variants = 384
> wrapper_bypass_catch_rate = 1
> false_positive_control = 1
>
> The commercial production parser packs, customer connector rules, exact enterprise policy thresholds, managed evidence graph, tenant data, and private signing/KMS configuration remain outside the public artifact. The released artifact is scoped to the deterministic benchmark claim reported in the paper.
>
> If this now satisfies your protocol, please feel free to rerun and correct the record. If it still fails your criterion, I would appreciate knowing which file or field is still missing so I can make the release boundary clearer.
>
> You may publish this reply in full.
>
> Best,
> Zexun

### Re-check, 2026-08-06

Artifact: `OndCo/CAVA` @ `b1b1616`, `reproducibility/cava-2607.13716`.

**Determination as of 2026-08-06: COMPUTABLE — and recomputed.**

`node scripts/verify-snapshot.mjs` runs with zero dependencies on Node 24 and returns:

```json
{ "ok": true, "benchmark_id": "cava-paper-benchmark-v1",
  "seed_scenarios": 96, "executable_variants": 384,
  "wrapper_bypass_catch_rate": 1, "false_positive_control": 1 }
```

**A green tick from an author's own verifier is not evidence, so it was controlled twice
before being believed.**

- **Control A — is the figure recomputed or echoed?** `metrics.cava_runtime.wrapper_bypass_catch_rate`
  was altered from `1` to `0.5` in `benchmarks/latest.json` and the verifier was re-run. It
  failed on a strict comparison. Had the value been read back from the snapshot, the
  perturbed file would have agreed with itself and passed. **The metric is computed.**
- **Control B — is the shipped implementation actually on the path?** An unconditional
  `throw` was injected at the top of `canonicalizeRuntimeAction` in
  `src/app-lib/cava/shell.js`. The run aborted on it. **The released library is exercised,
  not decorative.**

Against the survey's conditions: the corpus is published in full — scenarios are defined
inline in `benchmarks/source-benchmark.mjs`, including a 24-case red-team casebook carrying
each raw event and its expected behaviour, so a reader can judge each case rather than
accept a label (**A**); per-unit decisions are derivable by running the deterministic
harness, and per-suite scores ship in the snapshot (**B**); scenarios carry identifiers
(**C**).

The withheld components he lists — production parser packs, connector rules, enterprise
thresholds, tenant data, signing configuration — are outside the benchmark claim and their
absence does not block the recomputation.

### Two errors of mine during this re-check, recorded

Both were mine, neither is a defect in his release, and both are written down because a
reader watching only the successful attempt would learn the wrong thing about how hard this
was.

1. A first attempt at control B patched `'bash'` in `src/cava-core/parser-pack.js`; the
   string was not there, the patch silently applied nothing, and the resulting pass looked
   like a finding. **A perturbation that fails to perturb reads exactly like a system that
   cannot be broken.** Caught by checking that the edit actually changed the file.
2. A second attempt broke `canonicalizeRuntimeEvent` in `src/cava-core/adapter.js` and the
   benchmark still passed. That is the wrong function: the wrapper-bypass metric runs
   through `canonicalizeRuntimeAction` in `src/app-lib/cava/`. Reported here rather than
   left to read as "the release is decorative", which is what it looked like for about a
   minute.

### What this does and does not change

**The survey's published count stays at 2 of 14.** That number is a measurement of a
population of releases as they stood at the frame date, and the contract pins every artifact
to that date precisely so that later additions are visible as later additions rather than
folded back into the result. Changing the headline because the world changed after the
measurement would destroy the meaning of the pin — and it would do so in the direction that
makes the finding milder, which is exactly the direction that deserves the most suspicion.

What is recorded instead: **on 2026-08-06 one of the fourteen releases became recomputable,
because its author was notified and closed the gap in under seven hours.** That is a fact
about the notification, not about the population, and it is the most useful thing this
survey has produced.

Under the survey contract, a `COMPUTABLE` paper becomes a candidate for a numbered deep
check. This one now qualifies.
