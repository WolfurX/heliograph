#!/usr/bin/env bash
# Open a GitHub issue when a run produces a critical finding.
#
# Usage: scripts/alert.sh [snapshot.json]
# Needs gh authenticated (GH_TOKEN in CI). Does nothing when the snapshot has
# no critical finding, or when an open issue already carries the same title.
set -euo pipefail

snapshot="${1:-docs/data.json}"

worst=$(jq -r '.anomalies[0].severity // "none"' "$snapshot")
if [ "$worst" != "crit" ]; then
  echo "no critical finding (worst: $worst); nothing to alert"
  exit 0
fi

title="Critical: $(jq -r '.anomalies[0].headline' "$snapshot" | cut -c1-80)"

# Exact-title match over the plain list: `--search` runs against GitHub's
# search index, which lags behind by minutes and would let a repeating
# finding open a fresh issue every run.
existing=$(gh issue list --state open --limit 100 --json title \
  | jq --arg t "$title" '[.[] | select(.title == $t)] | length')
if [ "$existing" != "0" ]; then
  echo "already reported: $title"
  exit 0
fi

{
  jq -r '.anomalies[] | "- **\(.severity | ascii_upcase)** \(.headline)\n  - \(.detail)"' "$snapshot"
  echo
  echo "Generated $(jq -r '.generated_at' "$snapshot") · run #$(jq -r '.baseline.runs' "$snapshot")"
  echo "Dashboard: https://wolfurx.github.io/heliograph/"
} | gh issue create --title "$title" --body-file -

echo "alerted: $title"
