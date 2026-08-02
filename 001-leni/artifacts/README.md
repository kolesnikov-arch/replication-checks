# artifacts — check 001

## State

`check.py` was written and committed **before the subject's data was opened**, per
`../CONTRACT.md`. Writing the analysis before the data is a stronger form of
pre-registration than freezing prose alone: the labelling rules exist as executable
code, so they cannot drift once numbers are visible.

Everything above the `ADAPTER` banner in `check.py` is frozen. `load_runs` is the only
function that may be completed after the data is first read. If completing it appears to
require changing a rule above the banner, that is a finding to report in `METHOD.md`, not
an edit to make.

## Self-validation before the data

`clopper_pearson` was checked against five known values, including two published in the
author's own preprint (DOI 10.5281/zenodo.21721311), reproducing them exactly:

| case | computed | expected |
|---|---|---|
| 17/50 (own preprint, ungated arm) | [0.2121, 0.4877] | [0.212, 0.488] |
| 0/50 (own preprint, gated arm) | [0.0000, 0.0711] | [0.0, 0.071] |
| 8/40 (subject's catch rate) | [0.0905, 0.3565] | [0.0904, 0.3565] |
| 6/8 (subject's fix rate) | [0.3491, 0.9681] | [0.3491, 0.9681] |
| 0/357 (subject's false alarms) | [0.0000, 0.0103] | [0.0, 0.0103] |

One defect was found and fixed during this validation: the bisection helper was written
for a decreasing objective while both Clopper–Pearson bounds are increasing in *p*,
which produced inverted intervals. Recorded here because it was caught before the data,
which is the argument for writing the analysis first.

## Note on intervals of the published figures

The three intervals above for the subject's figures are computed from the numerators and
denominators stated in the paper's abstract. No repository data was used, and this is
**not** part of the contract's question, which concerns reproduction only. It belongs in
the limitations section of the result, not in any headline.

## Requirements

Stdlib only. `python check.py <path-to-checkout>`.
