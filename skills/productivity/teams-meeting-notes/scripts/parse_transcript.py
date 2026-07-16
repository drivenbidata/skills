#!/usr/bin/env python3
"""
Parse a Microsoft Teams transcript file into a clean Speaker: text log.

Supports:
  - WebVTT (.vtt) — Teams' default transcript export
  - Word docx (.docx) — Teams' "Save transcript" output

Usage:
    python parse_transcript.py <path-to-transcript>

Prints normalized lines to stdout, one utterance per line:
    Jeff Ford: Good morning, let's get started.
    Mia Chen: I have an update on the deployment.

This strips timestamps and merges contiguous utterances from the same
speaker, so downstream synthesis can focus on content rather than form.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VTT_SPEAKER_RE = re.compile(r"<v\s+([^>]+?)>(.*?)</v>", re.IGNORECASE | re.DOTALL)
TIMESTAMP_RE = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?\s*$")
DOCX_SPEAKER_LINE_RE = re.compile(
    r"^([A-Z][\w'.-]+(?:\s+[A-Z][\w'.-]+){0,3})\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*(.*)$"
)


def parse_vtt(text: str) -> list[tuple[str, str]]:
    """Return list of (speaker, utterance) tuples from a VTT string."""
    utterances: list[tuple[str, str]] = []
    for match in VTT_SPEAKER_RE.finditer(text):
        speaker = match.group(1).strip()
        utterance = re.sub(r"\s+", " ", match.group(2).strip())
        if utterance:
            utterances.append((speaker, utterance))
    # Fallback: some VTT files use plain "Name: text" cues
    if not utterances:
        for block in re.split(r"\n\s*\n", text):
            lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
            if not lines:
                continue
            # Skip the cue identifier and timestamp lines
            content_lines = [l for l in lines if "-->" not in l and not TIMESTAMP_RE.match(l)]
            for line in content_lines:
                m = re.match(r"^([A-Z][\w'.\-\s]{0,40}?):\s*(.+)$", line)
                if m:
                    utterances.append((m.group(1).strip(), m.group(2).strip()))
    return utterances


def parse_docx(path: Path) -> list[tuple[str, str]]:
    """Return list of (speaker, utterance) tuples from a docx transcript."""
    try:
        from docx import Document  # type: ignore
    except ImportError:
        print(
            "ERROR: python-docx not installed. Run: pip install python-docx --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(2)

    doc = Document(str(path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    utterances: list[tuple[str, str]] = []
    current_speaker: str | None = None
    buffer: list[str] = []

    def flush():
        nonlocal buffer, current_speaker
        if current_speaker and buffer:
            utterances.append((current_speaker, " ".join(buffer).strip()))
        buffer = []

    for line in paragraphs:
        # Single-line layout: "Jeff Ford   0:01   Good morning..."
        m = DOCX_SPEAKER_LINE_RE.match(line)
        if m:
            flush()
            current_speaker = m.group(1).strip()
            tail = m.group(3).strip()
            if tail:
                buffer.append(tail)
            continue
        # Two-line layout: speaker line then dialogue line
        # Detect speaker-only line: short, title-case, optionally with trailing timestamp
        speaker_only = re.match(r"^([A-Z][\w'.-]+(?:\s+[A-Z][\w'.-]+){0,3})(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\s*$", line)
        if speaker_only and len(line) < 80:
            flush()
            current_speaker = speaker_only.group(1).strip()
            continue
        # Otherwise it's dialogue continuation
        buffer.append(line)
    flush()
    return utterances


def normalize_speaker(name: str) -> str:
    """Collapse whitespace and strip trailing punctuation from a speaker name."""
    return re.sub(r"\s+", " ", name).strip().rstrip(":")


def merge_contiguous(utterances: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Merge back-to-back utterances from the same speaker."""
    merged: list[tuple[str, str]] = []
    for speaker, text in utterances:
        speaker = normalize_speaker(speaker)
        if merged and merged[-1][0] == speaker:
            merged[-1] = (speaker, merged[-1][1] + " " + text)
        else:
            merged.append((speaker, text))
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Path to a .vtt or .docx transcript")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: {path} does not exist", file=sys.stderr)
        return 1

    suffix = path.suffix.lower()
    if suffix == ".vtt":
        utterances = parse_vtt(path.read_text(encoding="utf-8", errors="replace"))
    elif suffix == ".docx":
        utterances = parse_docx(path)
    else:
        print(
            f"ERROR: unsupported extension '{suffix}'. Use .vtt or .docx, or for plain text "
            "just read the file directly.",
            file=sys.stderr,
        )
        return 1

    utterances = merge_contiguous(utterances)
    if not utterances:
        print("(no utterances parsed — file may be empty or in an unexpected layout)", file=sys.stderr)
        return 1

    for speaker, text in utterances:
        print(f"{speaker}: {text}")

    # Also print a unique attendee list to stderr so the caller can grep it out
    seen = []
    for s, _ in utterances:
        if s not in seen:
            seen.append(s)
    print("\n--- Attendees inferred from speaker tags ---", file=sys.stderr)
    for s in seen:
        print(s, file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
