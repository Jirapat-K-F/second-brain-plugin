---
name: log-session
model: haiku
description: Write or update the session log note in the user's Second Brain Obsidian vault (D:\MySecondBrain). Use at the end of any session where real work happened (files made or changed, research done, a decision or plan settled), or when the user types /log-session or /second-brain:log-session or asks to log, record or save this session.
---

# Log session

Writes one note per session plus a line in that day's daily note, so the user can see later what was done, decided and left open — across Claude Code, Cowork and the Claude app.

## Finding the vault
- Claude Code (Windows): `D:\MySecondBrain`
- Cowork / cloud session: `$HOME/mnt/MySecondBrain` via `device_bash`. Write files with a quoted heredoc (`cat > file <<'EOF'`) so `$` and backticks survive.
- Not reachable: tell the user in one line and offer to log when the folder is attached. Don't write the note anywhere else.

## 1. Decide personal or work
Company work → `50-Work/Sessions/YYYY-MM/` and daily note `50-Work/Daily/YYYY-MM-DD.md`.
Everything else → `10-Sessions/YYYY-MM/` and daily note `10-Sessions/Daily/YYYY-MM-DD.md`.
Never mention company work in the personal daily note. If unsure, ask.

## 2. Find or create the note
- If you already wrote a note for this session (same `session_id`, or earlier in this conversation), update that note instead of creating a new one.
- New file name: `YYYY-MM-DD-HHMM-short-slug.md` — Bangkok time when the session started, 3–5 word English kebab-case slug (e.g. `2026-11-05-1813-second-brain-setup.md`).

## 3. Write it
```markdown
---
type: session
date: 2026-11-05
time: "18:13"
tool: claude-code        # claude-code | cowork | claude-app
account: personal        # personal | work
session_id: abc123       # Claude Code: the ID from the SessionStart hook; otherwise leave empty
project: "[[robotaxi-capstone]]"   # optional, quoted link
status: complete
tags: [personal]         # [work] for company sessions; add topic tags
---
# Second brain setup

## Goal
One or two sentences: what the user wanted.

## What was done
- Concrete outcomes, with links to notes/files created or changed.

## Decisions
- Decisions the user made, with the reason if they gave one.

## Open threads
- [ ] Things left to do next time.

## Notes touched
- [[2026-11-05]]
- [[other-note]]
```
Rules:
- Record what the user decided and what was produced — not a transcript and not your own reasoning.
- Headings and properties in English; body in the language the user used (English or Thai).
- No secrets (passwords, keys, ID or card numbers).
- Link every research note, experiment or project note touched with `[[file-name]]`.

## 4. Update the daily note
Open (or create from `90-System/Templates/daily.md`) the right daily note. `## Sessions` is the last section, so append to the end of the file:
`- 18:13 [[2026-11-05-1813-second-brain-setup]] — one-line summary`
Skip if that link is already there.

## 5. Update the project note
If the session belongs to a project note in `40-Projects/` (or `50-Work/Projects/`), append to its `## Log` section:
`- 2026-11-05 — [[2026-11-05-1813-second-brain-setup]]: one-line summary`

## 6. Tell the user
One line, e.g. "Logged this session → `2026-11-05-1813-second-brain-setup`." No recap of the note.
