---
name: new-experiment
description: Capture or update a personal experiment in the user's Second Brain vault (D:\MySecondBrain) - something they want to try, like a YouTube video idea, a tool, a coding trick, a habit or a workflow. Use when the user shares a link or idea "to try later", types /new-experiment, or says they started, finished or gave up on something they were trying.
---

# Experiments

Experiments live in `30-Experiments/`, one note each, and move through
`idea → trying → done | dropped` (later `archived`). The Home note shows them as boards.

## Vault location
Claude Code: `D:\MySecondBrain`. Cowork: `$HOME/mnt/MySecondBrain` (via `device_bash`).

## Capture a new idea
1. Check it isn't already there: `grep -ril "keyword" 30-Experiments`. If it is, update that note instead.
2. Create `30-Experiments/<short-slug>.md`:

```markdown
---
type: experiment
status: idea
category: youtube        # youtube | tool | coding | habit | learning | other
source: https://youtube.com/watch?v=...
effort: small            # small | medium | large
created: 2026-11-05
started:
finished:
verdict:
tags: [personal]
---
# Build a home lab dashboard

## What I'll try
One or two sentences, concrete.

## Why it interests me
In the user's words if they said why.

## Steps
- [ ] First small step

## Log
- 2026-11-05 — added as an idea

## Result

## Verdict
```
3. Only what the user said goes in "Why it interests me". If they shared a video and want it summarised, use the `second-brain:research` skill and link the research note from `## What I'll try`. Don't fetch transcripts unless asked.
4. Reply in one line: "Added experiment `[[short-slug]]` (idea)."

## Update an experiment
- **Started** → `status: trying`, `started: today`, log line.
- **Progress** → add a dated line under `## Log`, tick steps.
- **Finished** → `status: done`, `finished: today`, fill `## Result`, ask for (don't invent) the `verdict`: keep / drop / maybe.
- **Gave up** → `status: dropped`, `finished: today`, one log line with the reason if given.
Body in the user's language (English or Thai); properties in English.
