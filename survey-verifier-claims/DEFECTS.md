# Defects in the instrument

Five failures of this survey's own measurement code, found between the freeze and the
first determination. **Four of the five never raised an error.** They did not crash; they
returned a smaller denominator, a cleaner sample, or a field that was quietly always
empty.

This file exists because the survey it belongs to asks other people whether their released
artifacts permit an independent check. That question is not askable by someone who has not
written down what went wrong with his own.

Each entry says what the code did, how it was caught, and where the repair is recorded.
Where an entry cannot be traced to a committed artifact, that is stated.

| # | defect | silent? | traceable to |
|---|---|---|---|
| 1 | `critic` matched inside `critical` | yes | [CONTRACT-v2.md](CONTRACT-v2.md), frame hash voided |
| 2 | confidence interval computed inverted | **no** | author's account only |
| 3 | XML element with no children read as false | yes | `run.log` line 3, `select.py:183` |
| 4 | empty result file and a checksum written on network failure | yes | amendment `83273ef`, `select.py:211` |
| 5 | published hash taken over memory, file written with CRLF | yes | `select.py:316-319` |

---

## 1 — A substring match pulled in eight hundred papers about intensive care

The v1 matcher tested whether a term appeared **anywhere in the abstract as a substring**.
So `critic` matched `critical` and `criticism`, and `admission` matched hospital admission.

Measured on the retrieved cache afterwards: **1,109 of the 1,382 papers in the v1 frame —
80% — contained no matching term at all.** The v1 sample of 25 was accordingly dominated by
angiography, astrocyte imaging, robot badminton and 4-bit quantization. Exactly one of the
25 was on topic.

**Silent.** Nothing failed. The frame was built, the hash computed, the sample drawn, and
every number downstream would have been a rate over a population of papers about critical
care.

**Caught** by reading the drawn sample rather than trusting the count.

**Repaired** in v2: term matching requires word boundaries. That is the only change — the
term lists, categories, window, inclusion rules, cap and seed were deliberately left
alone, because a rule rewritten around observed output is no longer pre-registered. The v1
frame hash `d50b15e8…46fbba` is **void as a frame** and retained only as a record of what
was frozen.

**Known cost, carried on purpose:** `precision` still admits quantization papers. They are
removed at the reading stage with a logged reason, and the count of such removals is
published (7 of the 35 exclusions).

## 2 — A confidence interval returned upside down

The interval came back as `[1.0, 0.0]` — lower bound above upper.

**Not silent**, and it is the only one of the five that was not. An impossible interval
announces itself; that is why it was fixed in minutes and why it is the least interesting
entry here.

**Not traceable to a committed artifact.** The interval code is not part of `select.py`,
and this entry rests on the author's account rather than on a diff a reader can open. It is
listed anyway, because omitting the one defect with no paper trail would make this file a
selection rather than a record.

## 3 — A field that was always empty, because an empty element is false

`primary_category` was read with a truth test on the parsed XML element. An element with no
children evaluates as false in ElementTree, so the test failed on every record and the
fallback won every time. The field was `null` in all 33,805 cached records.

**Silent**, but not quite invisible: Python's own deprecation warning is in the run log,
third line, from the collection run itself —

```
select.py:183: DeprecationWarning: Testing an element's truth value will always return
True in future versions. Use specific 'len(elem)' or 'elem is not None' test instead.
```

It was printed, and it was scrolled past, which is the ordinary way a silent defect
survives.

**It moved nothing.** `in_frame` reads `categories`, never `primary`, so the enumerated
list is byte-identical before and after the repair — checked, and recorded in the contract's
amendment table. A defect that turned out not to reach the result is still a defect; it
reached nothing by luck of which field the rule happened to read.

## 4 — A connection error, written out as a finding

On a failed request the retrieval loop caught the exception, carried on, and at the end
wrote a result file and its checksum from whatever it had. A network outage therefore
produced a complete-looking artifact: a list, a hash, a run log — describing a smaller
population than the frame, with nothing on its face to say so.

**Silent, and the most dangerous of the five**, because its output is indistinguishable
from a successful run by inspection. The hash is real. It just commits to the wrong list.

**Repaired** in `83273ef`: any failed request aborts the run and writes nothing.
`select.py:211` now carries the reason in its docstring so the behaviour is not
re-optimised away later.

## 5 — A published hash that would not have verified against its own file

The frame hash was computed over the canonical text **in memory**. The file was then
written to disk on Windows, where the default text mode turns every `\n` into `\r\n`.

Anyone who downloaded `frame.txt` and ran `sha256sum` would have got a different digest
from the one published beside it — and would have concluded, reasonably, that the list had
been swapped after the fact.

**Silent, and the one that still bothers.** A commitment device is worth exactly its
verifiability by a stranger. One that fails the first stranger who checks it does not merely
fail: it accuses its author of the specific dishonesty it was built to rule out.

**Repaired** at `select.py:319` — the file is opened with `newline=""`, so the bytes hashed
are the bytes on disk. The reason is written into `CONTRACT.md` next to the freeze record,
not only into the code.

---

## What is not in this list

**Two further changes appear in the contract's amendment table and are not counted here.**
`83273ef` also verified TLS on the retrieval requests, and `35016ec` walks the window in
calendar months because arXiv caps a single result set near 10,000. Both are recorded there
as changes to how candidates were fetched. Whether the TLS change repaired an actual
failure or was precautionary is not something the record settles, and it is not claimed as
a defect here.

**Two defects outside the instrument.** Recorded separately, because counting either as a
sixth code defect would inflate the number above.

### The published hash did not verify for anyone who cloned the repository

Defect 5 was repaired in the code: `select.py` writes `frame.txt` with `newline=""`, so the
bytes hashed are the bytes on disk. On 2026-08-05, two days after publication, a fresh
clone was taken and the hash checked the way the contract tells a reader to check it.

```
published:      f97c68ded95ba8c3c236c985e1063d83ffc1bfc74e319883b47ee61c626943fe
fresh clone:    9526aa8fbf5008c79013879da813c2582d8fc753c4f2a17f6e6cd1267405ab8a
```

The repository carried no `.gitattributes`, so on Windows — where `core.autocrlf` defaults
to true — git converted every line ending on checkout. The file the author hashed and the
file a reader downloads were different bytes.

**The same failure as defect 5, through a mechanism one layer further out.** Fixing the
writer was not enough, because the transport rewrote the file afterwards. A commitment
device is only as good as the last thing that touches it before a stranger reads it, and
the code was not the last thing.

Repaired by pinning `-text` in `.gitattributes`, verified by cloning again.

Found the same way as the entry below: by a reader following the instruction and getting a
different answer. That is the only test that finds this class, and it is why the contract
tells readers to run it.

### An artifact pin that resolved to nothing

On 2026-08-05 the artifact pin for `2604.07666` was found to be unresolvable. It had been
written as `1b66fb59091e` — a twelve-character abbreviation, by habit from the commit SHAs
in the same table. Gist identifiers are thirty-two characters and GitHub does not resolve
abbreviations, so the pin returned 404 for every reader, including its author. The gist was
never deleted.

Corrected to the full address, owner and revision. Found by trying to use the pin as a
channel to reach the authors — that is, by a reader following it, which is the only test
that ever finds this class of error.

## The standard this file is held to

The count in this file governs the count stated anywhere else. If a defect cannot be
described precisely enough to be checked, it is not added to make a number rounder, and if
one is later found to have been miscounted, the correction appears here rather than being
edited into silence.
