# Defects in the instrument

Five failures of this survey's measurement code, found between the freeze and the first
determination. Four of the five did not raise an error. They returned a smaller denominator,
a cleaner sample, or a field that was always empty.

The survey asks whether other people's releases permit an independent check. This file
records the same question applied to the code that ran it.

Each entry states what the code did, how it was found, and where the repair is recorded.
Entries that cannot be traced to a committed artifact say so.

| # | defect | silent | traceable to |
|---|---|---|---|
| 1 | `critic` matched inside `critical` | yes | [CONTRACT-v2.md](CONTRACT-v2.md), frame hash voided |
| 2 | confidence interval computed inverted | no | author's account only |
| 3 | XML element with no children read as false | yes | `run.log` line 3, `select.py:183` |
| 4 | empty result file and checksum written on network failure | yes | amendment `83273ef`, `select.py:211` |
| 5 | published hash taken over memory, file written with CRLF | yes | `select.py:316-319` |

---

## 1 — Substring matching in the v1 term filter

The v1 matcher tested whether a term appeared anywhere in the abstract as a substring, so
`critic` matched `critical` and `criticism`, and `admission` matched hospital admission.

Measured on the retrieved cache afterwards: 1,109 of the 1,382 papers in the v1 frame — 80%
— contained no matching term at all. The v1 sample of 25 was dominated by angiography,
astrocyte imaging, robot badminton and 4-bit quantization. One of the 25 was on topic.

Silent. The frame was built, the hash computed and the sample drawn without error. Every
number downstream would have been a rate over the wrong population.

Found by reading the drawn sample rather than the count.

Repaired in v2: term matching requires word boundaries. That was the only change. The term
lists, categories, window, inclusion rules, cap and seed were left alone, because a rule
rewritten around observed output is no longer pre-registered. The v1 frame hash
`d50b15e8…46fbba` is void as a frame and kept only as a record of what was frozen.

Known cost, carried deliberately: `precision` still admits quantization papers. They are
removed at the reading stage with a logged reason, and the count is published — 7 of the 35
exclusions.

## 2 — Inverted confidence interval

The interval was returned as `[1.0, 0.0]`, lower bound above upper.

Not silent. It is the only one of the five that was not, and it was fixed in minutes.

Not traceable to a committed artifact. The interval code is not part of `select.py`, so this
entry rests on the author's account rather than on a diff. It is listed anyway: dropping the
one defect that has no paper trail would make this list incomplete.

## 3 — Truth test on an empty XML element

`primary_category` was read with a truth test on the parsed element. An element with no
children evaluates as false in ElementTree, so the test failed on every record and the
fallback was used every time. The field is `null` in all 33,805 cached records.

Silent, though not invisible: Python's deprecation warning appears in the run log, third
line, from the collection run itself.

```
select.py:183: DeprecationWarning: Testing an element's truth value will always return
True in future versions. Use specific 'len(elem)' or 'elem is not None' test instead.
```

It was printed and not read.

It changed nothing in the result. `in_frame` reads `categories`, never `primary`, so the
enumerated list is byte-identical before and after the repair — checked, and recorded in the
contract's amendment table. It is still listed: whether a defect reaches the result depends
on which field the rule happens to read, not on the defect.

## 4 — Result file written after a failed request

On a failed request the retrieval loop caught the exception, continued, and at the end wrote
a result file and its checksum from whatever had been collected. A network outage would
therefore have produced a complete-looking artifact — list, hash and run log — describing a
smaller population than the frame, with nothing to indicate it.

Silent, and the most dangerous of the five: the output cannot be distinguished from a
successful run by inspection. The hash is valid; it commits to the wrong list.

Repaired in `83273ef`: a failed request aborts the run and writes nothing. `select.py:211`
carries the reason in its docstring.

## 5 — Hash computed over memory, file written with CRLF

The frame hash was computed over the canonical text in memory. The file was then written on
Windows, where the default text mode converts every `\n` to `\r\n`.

Anyone who downloaded `frame.txt` and ran `sha256sum` would have got a different digest from
the one published beside it, and would reasonably have concluded that the list had been
changed after the fact.

Silent. A hash published as a commitment has no value if it fails for the first person who
checks it.

Repaired at `select.py:319`: the file is opened with `newline=""`, so the bytes hashed are
the bytes on disk. The reason is recorded in `CONTRACT.md` next to the freeze record as well
as in the code.

---

## Not counted here

Two further changes appear in the contract's amendment table and are not counted as defects.
`83273ef` also verified TLS on the retrieval requests, and `35016ec` walks the window in
calendar months because arXiv caps a single result set near 10,000. Both are recorded there
as changes to how candidates were fetched. The record does not settle whether the TLS change
repaired an actual failure, so it is not claimed as one.

Two further defects are outside the measurement code. They are listed separately rather than
counted above.

### The published hash did not verify after a clone

Defect 5 was repaired in the writer. On 2026-08-05, two days after publication, a fresh clone
was taken and the hash checked the way the contract tells a reader to check it.

```
published:      f97c68ded95ba8c3c236c985e1063d83ffc1bfc74e319883b47ee61c626943fe
fresh clone:    9526aa8fbf5008c79013879da813c2582d8fc753c4f2a17f6e6cd1267405ab8a
```

The repository carried no `.gitattributes`, so on Windows, where `core.autocrlf` defaults to
true, git converted the line endings on checkout. The file the author hashed and the file a
reader downloads were different bytes.

Repairing the writer was not sufficient because the transport modified the file afterwards.

Repaired by pinning `-text` in `.gitattributes`, verified by cloning again.

### An artifact pin that did not resolve

On 2026-08-05 the artifact pin for `2604.07666` was found to be unresolvable. It had been
written as `1b66fb59091e`, a twelve-character abbreviation copied from the habit of the
commit SHAs in the same table. Gist identifiers are thirty-two characters and GitHub does not
resolve abbreviations, so the pin returned 404 for every reader. The gist had not been
deleted.

Corrected to the full address, owner and revision.

Both of these were found by following a published instruction and getting a different answer
— which is the only way this class of error is found, and the reason the contract tells
readers to run the check.

## Standard

The count in this file governs the count stated anywhere else. A defect that cannot be
described precisely enough to be checked is not added to make the number rounder. A
miscount, if found later, is corrected here rather than in the places that quote it.
