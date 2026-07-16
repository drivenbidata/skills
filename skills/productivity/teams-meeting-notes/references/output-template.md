# Output template

Use this structure exactly. The headings and their order are the contract — downstream wiki tooling, Claude Projects retrieval, and human readers all depend on consistency across files.

```markdown
---
date: {YYYY-MM-DD}
meeting_type: {standup | planning | review | 1:1 | project-sync | partner-sync | other}
attendees: [{Name}, {Name}, {Name}]
tags: [{topic-tag}, {topic-tag}, {topic-tag}]
project: {project-name-or-empty-string}
related: []
---

# {Meeting title}

**Date:** {YYYY-MM-DD}
**Duration:** {e.g., 45 min, or "Not captured"}
**Meeting type:** {Standup | Planning | Review | 1:1 | Project sync | Other}

## Attendees
- {Name} ({role or team if known})
- {Name}
- ...

## Summary
{2–4 sentences. What was this meeting about, what was the headline outcome. A reader should be able to read just this and know if they need to read further.}

## Discussion
### {Topic 1}
{What was discussed — key points, tradeoffs, who raised what. 1–4 short paragraphs or a tight bullet list.}

### {Topic 2}
{...}

## Decisions
- **{Decision title}** — {what was decided and why.}
- **{Decision title}** — {...}

(If no formal decisions were made, write "None this meeting.")

## Agreed upon
- {Lighter-weight consensus items that aren't load-bearing decisions but should be remembered.}

## Action items
| Owner | Task | Due |
|-------|------|-----|
| {Name} | {Specific deliverable} | {YYYY-MM-DD or "TBD"} |
| {Name} | {...} | {...} |

(If an owner is uncertain, append "(?)" to the name.)

## Open questions / blockers
- {Question or blocker that was raised but not resolved. Include who raised it if relevant.}
- {...}

## Next steps
- {What happens at the meeting/project level — reconvene, hand off, escalate, etc.}
- {...}

## Related meetings
{Optional. If this is a recurring series or follow-up, link sibling files by filename.}
- [{previous-meeting-title-YYYY-MM-DD.md}]({previous-meeting-title-YYYY-MM-DD.md})

---
*Notes generated from {VTT transcript | DOCX transcript | Teams recap | pasted notes}.*
```

## Frontmatter rules

The YAML frontmatter at the top is what makes these files first-class citizens in a Claude Project — retrieval, filtering, and citation all key off of it. Fill it accurately:

- `date`: ISO format. Same date as the body. The frontmatter is the source of truth for date filtering.
- `meeting_type`: lowercase, kebab-case. Pick the closest match. If genuinely none fits, use `other`.
- `attendees`: list of full names as they appear in the transcript, normalized to one canonical form per person. Use a YAML list (square brackets) so each name is a discrete searchable token.
- `tags`: three to five lowercase, kebab-case topic tags derived from the Discussion section. These are how Claude finds "the meeting where we talked about latency" six weeks later. Prefer specific (`search-latency`, `q3-hiring`) over vague (`engineering`, `priorities`). Don't pad — three sharp tags beat seven fuzzy ones.
- `project`: the project or workstream the meeting belongs to, if obvious. Empty string `""` if not.
- `related`: leave as `[]` unless you can confidently identify a prior file in the same series. Bad guesses hurt more than empty values.

## Formatting rules

- Use `##` for section headings and `###` for topics within Discussion. Don't change the levels — the wiki TOC depends on them.
- Dates are always ISO (`2026-06-01`), never "June 1" or "6/1/26". This is what makes the files sortable, grep-friendly, and filterable from frontmatter.
- Action items go in a markdown table — easier to scan than bullets and renders well in most wikis.
- Keep each topic in Discussion focused on one thing. If the meeting jumped between subjects, restructure into clean topics rather than preserving the chronological mess.

## What to omit

- Timestamps from VTT (they add noise; the date is enough)
- Speaker attribution for every sentence in Discussion (attribute when it matters — disagreement, commitment, key insight — not for routine statements)
- Filler from recaps like "The team had a great conversation about..."
