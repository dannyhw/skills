# Evals for british-plain-english

A small benchmark that compares 3 conditions on the same prompts:

- `baseline`: no system prompt
- `micro`: one line, "Write in plain British English: UK spelling, short sentences, no jargon."
- `skill`: the full `SKILL.md` appended to the system prompt

The `micro` condition is there on purpose. A skill has to beat the one-line instruction that a user could type themselves, not only an empty prompt.

## Files

| File | What it does |
|---|---|
| `lint.py` | Counts the mechanical rule breaks: US spelling, negative contractions, should/may/might, eg/ie/etc, em dashes, semicolons, "please", US dates and times, long sentences, AI-overused words, bold, title-case headings, capitalised bullets. Code and identifiers are removed first. Run `python3 lint.py --self-test` after each change. |
| `run.py` | Runs every scenario through `claude -p` for each condition, caches the outputs and prints the tables. `--report-only` scores the cached outputs without calling the model. |
| `scenarios.json` | 6 document prompts and 6 chat-reply prompts. The document prompts use words that tempt US spelling (organization, color, canceled, license) and dates and times. |
| `slop.tsv` | 69 AI-overused words, from the SimpleEnglish project (MIT). |
| `pressure-tests.md` | Manual checks for what the linter cannot see. |
| `results/` | Raw outputs and scores, one folder per run. |

## Results, 22 October 2026

`claude-sonnet-5-5`, effort low, `--setting-sources ""`, one generation per cell. Totals over 6 outputs per row.

Documents:

| condition | words | US spelling | negative contraction | please | bold | slop word | hits per 100 words |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 140 | 11 | 6 | 1 | 12 | 2 | 3.90 |
| micro | 138 | 1 | 2 | 3 | 20 | 1 | 3.81 |
| skill | 134 | 0 | 0 | 0 | 0 | 0 | 0.23 |

Chat replies:

| condition | words | US spelling | negative contraction | bold | headers | bullets | hits per 100 words |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 327 | 7 | 19 | 61 | 3 | 46 | 7.65 |
| micro | 294 | 0 | 10 | 54 | 5 | 35 | 6.33 |
| skill | 270 | 0 | 0 | 0 | 0 | 0 | 1.05 |

What this shows:

- the one-line prompt already fixes almost all the US spelling, so spelling alone does not justify the skill
- the skill adds what the one-line prompt does not: no negative contractions, no "please", no bold or bullet walls in replies, no buzzwords
- no condition produced em dashes on this model, so that rule is now insurance, not a measured gain
- "may" survives in all conditions because the model uses it for real uncertainty ("the server may have created the order"), which the GOV.UK rule allows. The linter cannot tell the 2 uses apart.
- skill replies are still about 270 words, and some sentences go over 25 words

Limits: one run per cell, one model, and the linter was written against the same rules as the skill. That last point is the trap that the SimpleEnglish audit found in its own benchmark: a linter score measures rule obedience, not whether a reader understands faster. Read the documents in `results/` before you trust a number, and use `pressure-tests.md` for the parts that need a human.

## Run it

```sh
python3 evals/british-plain-english/run.py --out evals/british-plain-english/results/$(date +%F)
python3 evals/british-plain-english/run.py --out evals/british-plain-english/results/2026-10-22 --report-only
```

A full run is 36 `claude -p` calls and costs about $1 to $2.
