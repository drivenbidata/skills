# Context

## What this is

A public collection of agent **skills** maintained by drivenbidata. Skills are small, composable units of instruction that a coding/agent harness (Claude Code, Cowork, Codex, and other Agent Skills–compatible tools) can load to perform a specific task well.

## Goals

- **Composable, not a framework.** Each skill does one thing and can be adapted or removed without breaking the others.
- **Model-agnostic.** Skills should work across models and harnesses.
- **Installable.** The repo ships as a Claude Code plugin + marketplace so others can subscribe to the whole set, and individual skills can be symlinked in for local editing.

## Non-goals

- Not a process framework that owns your workflow.
- Not tied to a single vendor or model.

## Structure at a glance

- `skills/<category>/<skill>/SKILL.md` — the skills themselves.
- `.claude-plugin/` — plugin + marketplace manifests that make the repo installable.
- `scripts/` — dev helpers for listing and linking skills locally.
- `CLAUDE.md` — conventions agents should follow when adding or editing skills here.
