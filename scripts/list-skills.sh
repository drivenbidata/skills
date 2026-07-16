#!/usr/bin/env bash
set -euo pipefail

# List every SKILL.md in the repo (paths relative to repo root).
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
find skills -name SKILL.md -not -path '*/node_modules/*' | sort
