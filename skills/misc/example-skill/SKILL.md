---
name: example-skill
description: Template skill demonstrating the SKILL.md format. Not meant to be invoked — copy this folder to start a real skill, then replace the name, description, and body.
---

# example-skill

This is a template. A real skill's body is the instructions the agent follows when the skill is invoked.

## When to use

Describe, in concrete terms, the situations this skill is for. The one-line `description` in the frontmatter is what a model matches against to decide whether to reach for the skill — make it specific and include natural trigger phrasing.

## Process

1. Lay out the steps the agent should take.
2. Reference any supporting files in this folder (templates, scripts, reference docs).
3. Keep it focused — one skill should do one job well.

## Notes

- Folder name, frontmatter `name`, and any references should all match.
- Register the skill in `.claude-plugin/plugin.json` and the category `README.md` when you add it.
