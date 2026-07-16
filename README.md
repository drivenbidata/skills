# skills

Agent skills by **drivenbidata** — reusable, composable skills for Claude Code, Cowork, and other Agent Skills–compatible harnesses. Small, easy to adapt, and model-agnostic.

Each skill is a self-contained folder with a `SKILL.md`. The repo also ships as an installable [Claude Code plugin](https://code.claude.com/docs/en/plugins), so you can subscribe to the whole set instead of copying files by hand.

## Install

### As a Claude Code plugin (managed, auto-updating)

```
/plugin marketplace add drivenbidata/skills
/plugin install drivenbidata-skills@drivenbidata
```

Or from your shell:

```bash
claude plugin marketplace add drivenbidata/skills
claude plugin install drivenbidata-skills@drivenbidata
```

### Copy individual skills (editable)

Clone the repo and symlink the skills you want into your agent's skills directory:

```bash
git clone https://github.com/drivenbidata/skills.git
cd skills
./scripts/link-skills.sh   # links every skill into ~/.claude/skills and ~/.agents/skills
```

A `git pull` then keeps your installed skills up to date.

## Layout

```
skills/
  <category>/
    <skill-name>/
      SKILL.md        # required: YAML frontmatter (name, description) + instructions
      ...             # optional supporting files (references, scripts, templates)
    README.md         # index of the skills in this category
```

Categories are just folders — add ones that fit your work (e.g. `engineering/`, `data/`, `productivity/`, `misc/`). See [`skills/README.md`](./skills/README.md) for the conventions and how to add a new skill.

## Repo conventions

Agent-facing conventions live in [`CLAUDE.md`](./CLAUDE.md); what this repo is and why lives in [`CONTEXT.md`](./CONTEXT.md).

## License

[MIT](./LICENSE).
