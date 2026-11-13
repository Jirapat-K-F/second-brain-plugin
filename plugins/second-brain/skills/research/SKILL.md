---
name: research
model: sonnet
description: Research any topic using the user's Second Brain vault (D:\MySecondBrain) as memory - check existing research notes first, research only what is missing or stale, then save or update a sourced research note. Use whenever the user asks to research, look up, compare, investigate or find out about something, or asks what they already know about a topic.
---

# Research with memory

The vault is the long-term memory for research. Always look there first, and always save what you find.

## Vault location
Claude Code: `D:\MySecondBrain`. Cowork: `$HOME/mnt/MySecondBrain` (via `device_bash`). Company topics live in `50-Work/Research/`; everything else in `20-Research/`.

## 1. Check the vault first
Search file names and contents for 2–3 keywords (English and Thai if relevant):
```bash
grep -ril -e "keyword1" -e "keyword2" 20-Research 50-Work/Research 30-Experiments 2>/dev/null
```
Read any matching notes. Then decide:
- **Good enough** (answers the question, `status: current`, and recent enough for the topic — prices, products, people and news go stale in weeks; concepts and history don't): answer from the note, say when it was last updated, and ask if the user wants a refresh. Stop here.
- **Partly there or stale**: research only the missing or outdated part.
- **Nothing**: research from scratch.

## 2. Research
Use web search / fetch (and connected apps when the question is about the user's own data). Prefer primary sources. Note the URL and title of every source you rely on.

## 3. Save
One note per topic: `20-Research/<topic-slug>.md` (company: `50-Work/Research/<topic-slug>.md`).
- **Existing note** → update it in place: refresh `## Summary`, add new findings, add `## Update YYYY-MM-DD` if the change is notable, set `updated:` to today, add new URLs to `sources`, and set `status: current`. If findings contradict the old note, say so in the note.
- **New note** → use this shape:

```markdown
---
type: research
topic: Obsidian sync options
created: 2026-11-05
updated: 2026-11-05
status: current          # current | needs-update | archived
sources:
  - https://example.com/page
tags: [personal, obsidian]
---
# Obsidian sync options

## Summary
- 3–6 bullets a future reader can act on.

## Key findings
- Findings with the specifics that matter (numbers, versions, dates).

## Details
Longer explanation, comparisons, tables.

## Sources
- [Page title](https://example.com/page) — accessed 2026-11-05

## Related
- [[related-note]]
```
Rules:
- Paraphrase in your own words; at most a short quote per source. Never paste articles.
- Properties and headings in English; body in the user's language (English or Thai).
- Link related notes (projects, experiments, other research) under `## Related`, and add a backlink from the project note if one exists.

## 4. Answer the user
Answer the question normally, with sources, and add one line: "Saved to `[[topic-slug]]`." (or "Updated …").
If real work happened this session, `second-brain:log-session` will link the research note.
