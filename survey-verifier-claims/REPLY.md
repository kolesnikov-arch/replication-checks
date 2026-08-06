# Replies from authors

Published in full and unedited, as promised in the contract. Notifications went out
2026-08-05; the window runs to 2026-08-19.

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
