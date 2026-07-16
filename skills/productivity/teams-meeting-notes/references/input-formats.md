# Recognizing and parsing Teams transcript formats

Teams exports meeting material in several shapes. Each carries different signal and has different failure modes.

## VTT (.vtt)

WebVTT format with timestamps and speaker tags. This is what Teams exports when you download the transcript from a meeting recording.

**Looks like:**
```
WEBVTT

00:00:01.234 --> 00:00:04.567
<v Jeff Ford>Good morning, let's get started.</v>

00:00:05.000 --> 00:00:09.123
<v Mia Chen>I have an update on the deployment.</v>
```

**Notes:**
- Speaker is wrapped in `<v Name>...</v>` tags
- Same speaker may appear with name variants across the file — normalize them
- The first timestamp gives the meeting start time; use the file's metadata or the user's prompt for the actual date
- Run `scripts/parse_transcript.py <path>` to get a clean `Speaker: text` log

## DOCX (.docx)

Word document downloaded from a meeting recording's "Save transcript" option. Usually has speaker name on one line, dialogue on the next, sometimes with timestamps.

**Looks like:**
```
Jeff Ford   0:01
Good morning, let's get started.

Mia Chen    0:05
I have an update on the deployment.
```

**Notes:**
- Speaker line typically contains a name and timestamp separated by whitespace
- Some exports put speaker, time, and dialogue all on one line
- Run `scripts/parse_transcript.py <path>` — it uses python-docx to read the file and normalizes both layouts

## Teams meeting recap (pasted or text file)

The AI-generated summary Teams produces automatically. Already heavily compressed — bullets, sections like "Topics discussed" and "Next steps."

**Looks like:**
```
Meeting recap — Daily standup, June 1, 2026

Topics discussed
- Deployment of v2.4 to staging
- Customer feedback from the pilot
- Decision on hiring timeline

Follow-ups
- Mia to deploy v2.4 to prod Tuesday
- Jeff to schedule a customer call this week
```

**Notes:**
- No speaker attribution; don't fabricate it. Attendees are usually listed at the top or in a separate "Participants" section
- Follow-ups map cleanly to action items
- Often missing the "Discussion" texture that makes notes useful — be upfront that some sections are sparser when the source is a recap

## Plain text / pasted

User just pastes dialogue into the chat. Quality varies wildly.

**Notes:**
- Look for speaker prefixes (`Name:`, `[Name]`, all-caps names on their own line) and use them
- If no speaker structure at all, you'll need to synthesize without attribution — that's fine, just be honest in the output
- Ask for the date if you can't find one in the text — once, not repeatedly

## Common gotchas

- **Multiple speakers, one name**: "Jeff" might be Jeff Ford or Jeff Garcia. If two distinct voices share a first name, ask the user before assuming.
- **Bot/system messages**: Teams sometimes injects "Recording started" or "X joined the meeting" — drop these from the dialogue but use the join events to build the attendee list.
- **Side conversations and tangents**: A 60-minute meeting often has 10 minutes of off-topic content. Cut it. The point is signal, not completeness.
