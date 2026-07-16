---
name: teams-meeting-notes
description: Turn Microsoft Teams meeting transcripts into structured markdown notes for a wiki, project folder, or Claude Project. Use this whenever the user shares a Teams transcript (VTT, DOCX, plain text, or the auto-generated Teams recap) and wants meeting notes, a summary, an action-items list, or a wiki page produced from it — even if they just say "summarize this meeting" or "turn this into a doc." Also use when the user mentions a Teams recording, meeting minutes, standup notes, project sync notes, or asks for action items pulled from a call. The output is a single markdown file with YAML frontmatter (date, attendees, tags, project) plus sections for discussion, decisions, action items, open questions, and next steps, named meeting-title-YYYY-MM-DD.md — designed so Claude can retrieve and filter meetings later.
---

# Teams meeting notes

You help the user turn raw Microsoft Teams meeting material into a clean, useful markdown file they can drop into a wiki or project repo. The goal is notes a teammate who missed the meeting can actually use — not a dump of the transcript.

## When this skill applies

The user has a Teams meeting artifact (transcript, recording transcript export, recap, or pasted text) and wants structured notes. They might say any of:

- "Here's the transcript from this morning's standup — write it up for the wiki"
- "Summarize this meeting and pull out action items"
- "Turn this Teams recap into meeting minutes"
- "Make me a project doc from yesterday's planning call"

Treat all of these as in scope.

## Workflow

1. **Identify the input format** — VTT, DOCX, Teams recap text, or plain pasted text. Each format carries different signal; see `references/input-formats.md` for parsing notes and gotchas.
2. **Get clean text from the input.** For long or noisy `.vtt` and `.docx` files, run `scripts/parse_transcript.py <input-path>` — it strips timestamps and merges contiguous utterances into a `Speaker: text` log. For short transcripts you can already read cleanly, or for pasted text and Teams recaps, skip the script and work directly with what you have. The point is signal, not ceremony.
3. **Check for missing essentials and stop to ask** — see "Confirming missing essentials" below. Do this BEFORE synthesizing the notes; getting the date or attendees wrong contaminates the whole file and the frontmatter, which is exactly what later retrieval keys on.
4. **Synthesize the notes** following the template in `references/output-template.md`. Synthesis is the part only you can do well — see "Synthesis principles" below.
5. **Pick a filename**: `meeting-title-YYYY-MM-DD.md`. Lowercase, kebab-case title, ISO date. If the title isn't obvious, infer it from the discussion (e.g., `q3-roadmap-planning-2026-06-01.md`).
6. **Write the file.** If the user supplied a path in their request, use that. Otherwise use the default output directory from the "Configuration" section below. If no default is configured, write to the outputs folder and tell the user (once per session) that they can set a default by editing the Configuration section.
7. **Present the file** to the user.

## Confirming missing essentials

Two pieces of information must be right before you write anything — the **date** and the **attendees**. If either is missing or ambiguous from the transcript, stop and ask the user before synthesizing. Don't fall back to "today's date" or to a generic mic label like "Whitby Guidance Room" — those silently corrupt the file's frontmatter and break retrieval later.

**Date.** Look for the date in the filename, in the VTT/DOCX text, or in the user's prompt ("yesterday's planning call", "the May 28 standup"). If you can't pin down a specific ISO date, ask once:

> *"I couldn't find the meeting date in the transcript. What was the date of the meeting? (YYYY-MM-DD)"*

Don't guess from the upload timestamp — meetings are often uploaded days after they happen.

**Attendees.** If the speaker tags in the transcript give you a clean list of named individuals, you're done. But if either of these is true — the transcript shows only one or two unique speakers when context clearly implies more (common with conference-room mics), or attendee names appear inside dialogue but not as speaker tags — ask the user to supply the attendee list. Phrase it as:

> *"The transcript captures speakers under a single room mic, so I can't pull a clean attendee list. Could you tell me who was there? You can paste names (or names + emails), or drop a screenshot of the Teams participants panel and I'll read it."*

Then accept whichever form they send:
- **Pasted text** (names, "Name <email>" lines, or a comma-separated list) — parse out names directly. If emails are included, drop the email domains and keep just the human names; the frontmatter is for retrieval, not contact info.
- **A screenshot of the Teams participants panel** — the image is in your context; read the names off it directly. If a name is cut off or unclear in the screenshot, ask which one it is rather than guessing.

In both cases, normalize to one canonical form per person (first name + last name where available, first name + last initial as fallback).

Don't ask for attendees if the transcript gives them to you cleanly — the prompt is friction, and unnecessary friction makes the skill annoying. Ask only when the data genuinely isn't there.

## Configuration

Default output directory: _(not set — set your own default here, e.g. `C:\Users\yourname\OneDrive\Meeting-notes`)_

If left unset, notes are written to the outputs folder and you'll be told once per session how to set a default here.

A user-supplied path in any individual request always wins over this default.

## Designed for Claude Projects

These files are meant to be dropped into a Claude Project (or a wiki Claude indexes). The YAML frontmatter at the top of the template — `date`, `attendees`, `tags`, `project`, `meeting_type` — is the handle Claude uses to retrieve and filter meetings later. Treat the frontmatter as the most important part of the file, not an afterthought:

- **Tags do the heavy lifting for retrieval.** Pick three to five lowercase kebab-case topic tags drawn from the actual Discussion sections (`search-latency`, `q3-hiring`, `acme-renewal`). Specific tags beat broad ones because they're what someone would actually search for months later.
- **Attendees are listed as a YAML array** so each name is a discrete searchable token, not a freeform string.
- **`project:`** lets the user (or Claude) filter for "all meetings about Project X." Fill it when obvious, leave it `""` otherwise — don't guess.
- **Filenames stay sortable** by ISO date, so chronological listings work without any extra index file.

## Synthesis principles

A good meeting note serves three audiences: (a) someone who attended and needs to remember what they committed to, (b) someone who missed the meeting and needs to catch up in two minutes, (c) future-you searching the wiki six months later. Write for all three.

**Be ruthless about signal.** Transcripts are 80% noise — greetings, tangents, "can you hear me?", repeated phrasing. The discussion section is not a transcript summary; it's a record of the substantive topics, framed so a reader can understand what happened without scrolling through dialogue.

**Distinguish discussion, decisions, and actions.** These are different things and conflating them is the most common failure mode:

- *Discussed* = topics the group talked about, with the key points or tradeoffs surfaced
- *Agreed upon* = informal consensus the group reached during the conversation
- *Decisions* = formal, named decisions with a clear rationale (often a subset of "agreed upon," but worth pulling out when they're load-bearing for the project)
- *Action items* = specific work assigned to a specific person, ideally with a date
- *Next steps* = what happens next at the meeting/project level (e.g., "Reconvene Tuesday once Mia has draft", "Move to design review")
- *Open questions / blockers* = things raised that weren't resolved — these are the most-often-missed items and the most valuable to capture

If the meeting genuinely has no decisions or no open questions, write "None" rather than fabricating content. Empty sections are honest signal.

**Attribute action items.** Every action item should have an owner. If the transcript is ambiguous about who ow