# skills

Agent skills by [@dannyhw](https://github.com/dannyhw).

## Skills

| Skill | What it does |
|---|---|
| [british-plain-english](skills/british-plain-english/SKILL.md) | Plain British English for docs and chat replies, based on the GOV.UK writing guidelines. [Evals](evals/british-plain-english/README.md). |

## Install

```sh
npx skills add dannyhw/skills
```

## Layout

```
skills/
  <skill-name>/
    SKILL.md        frontmatter (name, description) + instructions
    ...             optional scripts/, references/, assets/
```

## Local development

Symlink every skill into `~/.claude/skills` so edits are picked up live:

```sh
./scripts/link.sh
```

Evals live in `evals/<skill-name>/`, outside the skill folder, so they are not installed with the skill.

## Credits

- british-plain-english adapts the [GOV.UK writing guidelines](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/) and [A to Z style guide](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/). Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
- The skill structure, the AI-overused word list (`slop.tsv`) and the benchmark method are adapted from [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) (MIT).
