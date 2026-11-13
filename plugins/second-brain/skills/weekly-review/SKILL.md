---
name: weekly-review
model: sonnet
description: Run the weekly quality review of the user's Second Brain Obsidian vault (D:\MySecondBrain) - find broken links, orphan notes, missing properties, stale inbox items, stuck experiments, session stubs and outdated research, apply only safe fixes, and write a review report. Use on the Sunday 19:40 schedule, when the review is overdue and the user agrees, or when the user types /weekly-review or asks to check or clean up the vault.
---

# Weekly review

Goal: keep the vault trustworthy without changing anything that needs the user's judgment.
Safe, mechanical fixes are applied; everything else becomes a checklist for the user.

## Vault location
Claude Code: `D:\MySecondBrain`. Cowork / scheduled run: `$HOME/mnt/MySecondBrain` (via `device_bash`). If the vault isn't reachable, say so and stop.

## 1. Run the check
```bash
python <this-skill-folder>/scripts/vault_check.py <vault> --fix
```
`<this-skill-folder>` is the folder this SKILL.md was loaded from. In the vault the same script is at `80-Skills/plugins/second-brain/skills/weekly-review/scripts/vault_check.py` — use that path if the skill folder isn't reachable from the shell. Use `python3` on Linux/Cowork. It prints JSON: `fixed` (already applied) and `issues`.
If Python isn't available, do the same checks by reading notes with grep/find and apply only the fixes listed under step 2.

## 2. Safe fixes (do these without asking)
Already done by `--fix`:
- add a missing `type` from the note's folder; add a missing `personal` / `work` tag from its folder
- repoint a broken `[[link]]` when exactly one note matches after ignoring case/spaces/underscores

Do yourself:
- **`daily_missing_session_link`** → append `- HH:MM [[session-note]] — one-line summary` to the end of that daily note (create it from `90-System/Templates/daily.md` if missing). Work sessions go only in `50-Work/Daily/`.
- **Inbox items that already have a real `type`** (e.g. `type: experiment` sitting in `00-Inbox/`) → move them to that type's folder. Company material goes under `50-Work/`.

Never: delete notes, rewrite note bodies, change `status`/`verdict`, rename files, move anything out of `50-Work/`, or touch `.obsidian/` and `80-Skills/` (the plugin repo).

## 3. Things for the user (report, don't fix)
broken links with zero or several candidates, orphans, bad file names, notes tagged `work` outside `50-Work/`, inbox items older than 7 days, experiments `trying` for more than 14 days, ideas older than 60 days, session stubs, research `current` but not updated for 180+ days, invalid types or type/folder mismatches.
For each, give a concrete suggested action (e.g. "link it from [[robotaxi-capstone]]", "mark dropped?", "fill in from your memory of that session").

## 3b. Episode stats
If a วิทย์ของของใช้ episode check point (48h / 7d / 28d) is due in the project note `40-Projects/science-of-everyday-things.md` → `## Posted episodes`, run `second-brain:update-stats` (personal only; skip in a scheduled run if the laptop or Buffer isn't reachable, and list it under "needs you").

## 4. Write the reports
Week label = ISO week, e.g. `2026-W45` (Bangkok time).
- **Personal report** → `90-System/Reviews/2026-W45.md`. Must not name or describe any `50-Work/` note — just "N work items, see the work report".
- **Work report** (only if there are work items) → `50-Work/Reviews/2026-W45.md`.

```markdown
---
type: review
week: 2026-W45
date: 2026-11-08
tags: [personal]          # [work] for the work report
---
# Weekly review 2026-W45

## Summary
Two or three sentences: overall health and the most important thing to do.

## Fixed automatically
- [[note]] — what was fixed

## Needs you
- [ ] [[note]] — problem → suggested action

## Stats
| Notes | Sessions | Research | Experiments (trying / ideas) | Inbox |
|---|---|---|---|---|
```
If a report for this week already exists, update it instead of creating a second one.

## 5. Tell the user
A short message: how many fixes were made, and the top 3 "needs you" items. In a scheduled run, send it as a message so it reaches the user.
