# CLAUDE.md

Conventions for agents working in this repository.

## Adding a skill

1. Create `skills/<category>/<skill-name>/SKILL.md`. Use lowercase-kebab-case for both the category and the skill folder.
2. `SKILL.md` must start with YAML frontmatter:

   ```yaml
   ---
   name: <skill-name>            # must match the folder name
   description: <one line that tells the model exactly when to use this skill>
   ---
   ```

   The `description` is what a model matches against to decide whether to invoke the skill — make it specific, and include concrete trigger phrasing.
3. Put supporting material (references, templates, scripts) alongside `SKILL.md` in the same folder. Keep each skill self-contained.
4. Add the skill's path to the `skills` array in [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) so it ships with the plugin.
5. Add a one-line entry for it in the category's `README.md` index.

## Principles

- **One skill, one job.** Prefer several small composable skills over one large one.
- **Editable and adaptable.** Write skills others can fork and tweak; avoid hidden coupling between skills.
- **Model-agnostic.** Don't rely on a specific model's quirks.

## Housekeeping

- `scripts/list-skills.sh` — list every `SKILL.md` in the repo.
- `scripts/link-skills.sh` — symlink all skills into local agent skill directories for testing.
- Keep `plugin.json` and the category READMEs in sync with what's actually in `skills/`.
