---
name: pick-topics
description: Research and rank the next episode ideas for the user's Thai YouTube Shorts series วิทย์ของของใช้ (science inside everyday products, 2D stickman) and store 5 product candidates in the Second Brain vault - using what the channel has done so far, real audience numbers (views, % viewed, comments), Shopee demand, season and how easy the science is to animate. Use whenever the user asks what the next episode should be, wants product or topic ideas for the series, asks "EP ต่อไปทำอะไรดี", or when plan-episode calls it. Works in Claude Code and in Cowork (phone).
---

# pick-topics

Gives the user 5 ranked product candidates for the next episode. The ranking rests on evidence: what the channel already learned, what the audience did, and what sells. Saves them in the vault.

## Where things are
- **Vault:** Claude Code `D:\MySecondBrain`. Cowork: `$HOME/mnt/MySecondBrain` via `device_bash`.
  - Project note: `40-Projects/science-of-everyday-things.md`.
  - Research: `20-Research/`.
- **YouTube work folder (on the laptop):** Claude Code `C:\Users\jirap\Desktop\Personal\Youtube`. Cowork: `$HOME/mnt/Youtube`.
  - `CLAUDE.md` has the episode rules.
  - `product/<ep>/review/score-log.md` has predicted GRS scores plus real numbers.
- **Laptop unreachable** (no mounts in Cowork, `device_bash` fails): don't stop. Do the web research, then follow "Offline" at the end.

## Steps
1. **Learn what we know** (vault first, as the `research` skill does):
   - **Project note:**
     - `## Key decisions` (style rules, link policy: EP1-3 have no affiliate link)
     - the "First 10 episodes" list (the starting pool)
     - `## Posted episodes` (real numbers, if any)
     - `## Log`
   - **Research notes:** `shopee-thailand-top-products-for-shorts`, `thai-affiliate-options-short-video`, `youtube-channel-thailand-2026`, plus any `episode-candidates-*` notes (don't re-suggest rejected or done items without a new reason).
   - **On the laptop, if reachable:**
     - every `product/*/review/score-log.md`: which versions scored well and why
     - the "Current status" section of `CLAUDE.md`
2. **Audience data**, whatever exists:
   - **The user's own numbers.** If `## Posted episodes` is empty and no episode is marked posted, skip this question: there's nothing to ask about yet. Otherwise ask once with buttons: "Do you have new numbers to add?" Options: paste numbers / send screenshots / no new numbers. Read screenshots of YouTube Studio, TikTok or FB insights.
   - **YouTube API**, if the laptop is reachable and `YOUTUBE_API_KEY` is in the Youtube folder's `.env`. Run `python scripts/yt_stats.py --env <Youtube>/.env <video ids>`. The video ids come from `## Posted episodes`. You get views, likes, comment count and the top comments.
   - Save new numbers to the project note's `## Posted episodes` table (create it if missing):
     `| EP | platform | url/id | posted | views | avg % viewed | viewed vs swiped | likes | comments | checked |`
   - **Comments are topic gold.** Note which products, menus or questions people mention.
3. **Fresh research** (web, recent): Shopee Thailand best-sellers and campaigns (next double-date sale), seasonal needs (hot season, PM2.5, rainy season, school term, festivals), trending everyday-product questions in Thai. Prefer primary sources and note URLs.
4. **Build the pool:**
   - the not-yet-made items from the "First 10" list
   - new ideas from research and comments
   - drop anything already made, and beauty result-claims (mechanism explainers only)
5. **Score each idea 1-5** on the four things the user chose:
   - **Audience fit:** like what got the best numbers or comments. With no posted data yet, use the GRS lessons: strong myth-bust hooks scored well.
   - **Shopee demand:** a top seller, decent price, commission potential. Links start at EP4, so for EP2-3 this is future value.
   - **Season / timing:** relevant within ~2-4 weeks of the likely post date.
   - **Animatable + myth-bust:** a clear "you think X, but actually Y" hook, and 2-3 inside "stations" that are easy to draw (moving parts, heat, air, light, electricity) without real footage.
   Total = sum. Prefer variety: not 3 kitchen appliances in a row.
6. **Write the top 5** to `20-Research/episode-candidates-YYYY-MM-DD.md` (`type: research`, `tags: [personal, youtube, episode-ideas]`, sources with dates). For each candidate:
   - Thai working title (the hook as a myth-bust, ≤ ~30 Thai chars)
   - product + Shopee category
   - the science idea, plus 2-3 station ideas
   - why now
   - score breakdown
   - risk (claims to fact-check, hard visuals)
   Add a "Not picked" line for strong ideas that missed the top 5. Link the note from the project note (`## Log` line).
7. **Show the user** the 5 as buttons (AskUserQuestion: title + score + one-line why). The tool shows at most 4 options, so put #1-4 as buttons, name #5 in the question text ("type it in Other"), and include the note's path. Record the pick in the note (`picked:` line) and in the project note's episode list.

## Offline (laptop unreachable)
Put everything in one artifact page for this session, titled "Pending sync - <date>":
- the full candidate note in Markdown, exactly as it would be saved
- a **To sync** checklist (target path, then what to write: new file / append line / table row)
- the user's pick
When the user later says the laptop is open (any session), write each item and tick it off in the artifact.
