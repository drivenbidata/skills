# skills

Every skill lives at `skills/<category>/<skill-name>/SKILL.md`.

## Categories

Categories are just folders — group skills however fits your work. Common ones:

- `engineering/` — code work: reviews, debugging, design, refactoring.
- `data/` — data / BI / analytics workflows.
- `productivity/` — writing, planning, handoffs, meta-skills.
- `misc/` — everything else, and examples.

Give each category a `README.md` that indexes its skills with a one-line description each.

## Adding a skill

1. Make `skills/<category>/<skill-name>/SKILL.md` with frontmatter:

   ```yaml
   ---
   name: my-skill
   description: One specific line telling the model exactly when to use this.
   ---
   ```

2. Keep supporting files in the same folder.
3. Register the skill's path in [`../.claude-plugin/plugin.json`](../.claude-plugin/plugin.json).
4. Add it to the category README index.

See [`misc/example-skill/SKILL.md`](./misc/example-skill/SKILL.md) for a minimal template.
