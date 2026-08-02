# Replication checks

One published claim at a time, checked against what its authors released themselves.

This is not a benchmark, not a ranking, and not a service. A benchmark measures a
population; this checks a specific statement by specific people, and asks a narrow
question: **does the published number come back out of the published files?**

## Rules

These are the whole point. Without them this is an opinion with a repository attached.

1. **The method is frozen before the data is opened.** Each check's protocol is
   committed first; the commit hash goes to the authors and into the published result.
   Nothing about the analysis is decided after the numbers are visible.
2. **Published claims against published data only.** Nothing private, nothing obtained
   around a licence. If there is not enough released to check a claim, that finding *is*
   the result, and it is stated as a fact about the release — not as an accusation.
3. **The result is published either way, and confirmations carry equal weight.**
   "It reproduces" gets the same format and the same visibility as anything else. The
   first time a positive result goes unpublished, this stops being a check and becomes a
   hunt, and hunts are not believed.
4. **Right of reply before publication.** Authors receive the result and 14 days to
   respond. Their reply is published in full, unedited, alongside it. If they identify a
   factual error, it is corrected before publication and the correction is attributed.
5. **My own errors are published the same way.** A mistake in a check is corrected
   through the same channel, not quietly edited into the original file.
6. **No asks.** A check never carries an offer of services, a note about availability,
   or a link to anything for sale.

Comparative claims of the form "their layer is worse than mine" are out of scope by
construction: different tasks, different oracles, different framings.

## Checks

| # | subject | claim under check | status |
|---|---|---|---|
| [001](001-leni/) | Leni Inc. — [arXiv:2607.17044](https://arxiv.org/abs/2607.17044) | verifier confusion matrix: catch ≈0.20, fix 0.75, false alarms ≈0/357 | **NOT COMPUTABLE** — [result](001-leni/RESULT.md) · awaiting authors' reply |

Each check lives in its own directory:

```
NNN-<subject>/
├── CONTRACT.md    pre-registered protocol, frozen before the data
├── METHOD.md      what was actually done, including deviations from the contract
├── RESULT.md      numbers, intervals, and which of three outcomes was reached
├── REPLY.md       the authors' response in full, if there was one
└── artifacts/     scripts and output, runnable by a third party
```

## Outcomes

Every check resolves to one of three, and all three are published identically:

- **REPRODUCES** — the published numerators and denominators come back out of the files.
- **REPRODUCES WITH DEVIATION** — different numbers, with the difference traced to a
  named difference in labelling rule or sample.
- **NOT COMPUTABLE** — the claim cannot be recomputed from what was released. This is a
  statement about the completeness of a release, and carries no implication that the
  claim is false.

## Who

Dmitriy Kolesnikov — independent researcher.
ORCID [0009-0008-4229-8809](https://orcid.org/0009-0008-4229-8809)

Prior work, for calibration on what to expect from me: three pre-registered studies of
independent verification in AI coding pipelines, DOI
[10.5281/zenodo.21721311](https://doi.org/10.5281/zenodo.21721311). That record includes
a detector of mine whose blind-reviewed precision came out at 6.9%, published against my
own tool, and a finding that my own verdict layer left 15 of 17 wrong patches wrong — it
changed where the errors went, not what they were.

If a check here is wrong, say so and it will be corrected in public under rule 5.

## Licence

Text and results: CC BY 4.0. Scripts: MIT. Material from the subjects of a check remains
under whatever licence its authors published it with, and is cited accordingly.
