---
name: write-episode
description: Turn a chosen episode title/product for the Thai YouTube Shorts series วิทย์ของของใช้ into a ready-to-produce Thai voice script (voice_script.json) plus a shot-by-shot scene storyboard in the series style, applying the lessons from earlier episodes' reviews (GRS) and real audience numbers. Use whenever the user has picked a product or title and wants the script, storyboard, scenes or "บท" for the next episode, or when plan-episode calls it. Works in Claude Code and in Cowork (phone).
---

# write-episode

Input: one picked candidate (title + product + science idea, usually from an `episode-candidates-*` note). Output:
- the 10-ish Thai lines (the voice script)
- a storyboard that `make-episode` / `generate-graphic` on the laptop can build from
- the factual sources behind every claim

## Where things are
Same as `pick-topics`:
- **Vault:** `D:\MySecondBrain`; Cowork `$HOME/mnt/MySecondBrain` via `device_bash`.
- **Youtube folder:** `C:\Users\jirap\Desktop\Personal\Youtube`; Cowork `$HOME/mnt/Youtube`.
- If the laptop is unreachable, follow "Offline".

## 1. Load the lessons (they're why EP1 went from GRS 54 to 89)
Read these:
- the project note: `## Key decisions` and `## Posted episodes`
- the Youtube `CLAUDE.md` "Episode rules" (if reachable)
- the newest `product/*/review/v*/GRS-report.md` (if reachable)
Current rules, which you can extend if newer notes add more:
- **Formula:** HOOK (0-3 s, a myth-bust, no greeting) → SHRINK (the host shrinks and dives into the product, a fixed signature) → 2-3 STATIONS inside (one science idea each; the first turn uses "แต่..." as a re-hook before 50%) → REVEAL, before 80% (one short punchy line that becomes the big card) → POP OUT + TIP (our own opinion, practical) → QUESTION (specific, easy to answer in a comment).
- **Hook line:** ≤ ~28 Thai characters, so it's spoken by ~3 s, and it states the surprise itself (EP1: "หม้อทอดไร้น้ำมัน ไม่ได้ "ทอด" จริงนะ!"). Also write a 3-6 word on-screen hook text.
- **Length:** the voice reads ~10 Thai chars per second (EP1 v9: 286 chars = 29.2 s of speech). Latin terms and numbers ("HEPA", "PM2.5", "20000mAh") take longer to say than their character count, so leave ~2 s of headroom. Aim for **280-340 chars total** (≈ 30-36 s with 0.25 s gaps; hard limits 30-45 s). Keep any one line ≤ ~40 chars, because long lines make long shots.
- **Lines:** about 10, conversational Thai, the excited science-show host voice. Use spaces between phrases: they set caption breaks. Avoid "..." pauses inside a line except the "แต่..." beat.
- **EP1-3:** no link line, no affiliate wording. From EP4: add `link_line` "หากสนใจ สามารถกดลิงก์ได้ที่ด้านล่างคลิปนี้เลย" (see `link_line` in EP1's script). Never show prices.
- **Beauty and health products:** mechanism only, never results or medical claims.
- **Audience data beats habit.** If `## Posted episodes` shows a pattern (e.g. versus-format or gadget episodes keep more viewers, or comments ask about X), apply it and say which number you followed.

## 2. Fact-check before writing lines
List every factual claim. For each one, look in the vault (`20-Research`) first, then the web, preferring primary or reference sources. Save new findings with the `research` skill. If a claim has no source, soften it or drop it. Spoken numbers must match on-screen labels exactly ("ลมร้อน ~200°C", not "ขดลวด 200°C", which was EP1's mistake).

## 3. Write
1. **Script:**
   - Write `segments` (the lines in order), `outside_style: "arctic"`, `inside_style` (the look that fits the product: ember for heat, arctic for cold, emerald for air/electric, sakura or retro as alternatives) and `versions: []`. The voice skill adds versions.
   - Next to the lines, show the character count per line and an estimated total in seconds.
2. **Storyboard** (Markdown table), one row per shot:
   `| shot | line | seconds | what we see (set, host action, product at real-life scale) | on-screen text | motion | sound |`
   - Keep shots ≤ 4 s (split long lines).
   - Frame 0 shows the hook text.
   - Put motion in 0.5-2 s.
   - Use hard cuts.
   - Add a reveal-card shot.
   - Give the question card motion.
   - Add a sound cue on every cut (shrink: the real whoosh; reveals: subdrop).
   - Reuse EP1's signature shrink (remote → dive into the product).
   The layout is otherwise free.
3. **Sources:** claim → source URL → line number.

## 4. Save
- **Vault:** in the project note, add a section `## EP<n> <product> (YYYY-MM-DD)` with the script table, storyboard, sources and status `draft` (`approved` after the user's OK). Add a `## Log` line.
- **Youtube folder (if reachable):**
  - `product/ep<n>-<product-kebab>/script/voice_script.json` (UTF-8, `ensure_ascii=False`)
  - `product/ep<n>-<product-kebab>/script/storyboard.md` (storyboard + sources)
  Don't overwrite an existing approved script without asking.

## Offline (laptop unreachable)
Put everything in this session's "Pending sync - <date>" artifact (create it, or add to it if it exists): the full script JSON, the storyboard and sources, and a **To sync** checklist (vault section, the two Youtube files, the `## Log` line). When the user says the laptop is open, write them and tick the boxes.
