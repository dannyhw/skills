# skills

Agent skills by [@dannyhw](https://github.com/dannyhw).

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
