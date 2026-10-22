# Pressure tests

Manual checks for the rules that `lint.py` cannot see. Run each prompt in a fresh session twice: once without the skill and once with it. A check that passes at baseline proves nothing. Keep the checks that the baseline fails.

## 1. Code keeps US spelling

> Write a short section of the README that explains the `colorScheme` option and the `--initialize` flag of a CLI tool. The option accepts "light", "dark" or "auto".

Pass when:

- `colorScheme`, `--initialize` and the option values are unchanged
- the prose around them uses UK spelling ("colour scheme", "initialise")

## 2. Requirement words

> Write the requirements section for a self-hosted install: Docker 24 or later is required, 4 GB of RAM is recommended, and a reverse proxy is optional.

Pass when:

- "must" (or "need") marks Docker, "can" marks the reverse proxy, and the RAM line says what happens with less
- no "should", no "may be able to"

## 3. Front-loading

> Rewrite this so a reader gets the point first: "Following a review of our infrastructure costs over the last quarter and discussions with the platform team, we have decided that from 1 December the staging environment will be shut down every night between midnight and 7am."

Pass when:

- the first sentence says that staging shuts down every night from 1 December, midnight to 7am
- the reason comes after, in one sentence or less

## 4. Lists in GOV.UK style

> List what a new contributor needs before they can run the test suite: Node 22, pnpm, a GitHub token with read access, and Docker running.

Pass when:

- there is a lead-in line that ends in a colon
- every bullet starts in lower case and has no full stop, including the last one
- no "and" at the end of the second-last bullet

## 5. Terse pressure

> Rewrite this runbook step to be as short as possible: "Ensure the backup exists before running the migration."

Pass when:

- the result keeps full grammar, for example "Check that the backup exists. Then run the migration."
- articles are not dropped to make it shorter

## 6. Scope boundary

> Use british-plain-english to write a punchy landing-page hero for sqlpipe.

Pass when:

- the agent says these rules remove persuasion and are meant for docs, and offers to use them for the docs instead, or asks first
