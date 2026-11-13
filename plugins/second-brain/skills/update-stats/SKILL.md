---
name: update-stats
model: haiku
description: Pull the real numbers of posted วิทย์ของของใช้ episodes from every platform (YouTube Analytics API, Buffer for TikTok/Instagram, the user's screenshots for Facebook) at the 48 h / 7 day / 28 day check points, and write them to the vault project note's ## Posted episodes table and each episode's review\score-log.md next to its GRS. Use when the user types /update-stats, asks for "stats", "numbers", "views", "how did EPx do", "ยอดวิว", when a check point is due, or from the weekly review.
---

# Update stats

Real numbers per episode × platform, saved where the next topic pick and the GRS reviews can use them.

## Paths
- Vault: `D:\MySecondBrain` (Cowork: `$HOME/mnt/MySecondBrain` via `device_bash`). Project note: `40-Projects/science-of-everyday-things.md`.
- Youtube folder (laptop only): `C:\Users\jirap\Desktop\Personal\Youtube`. Scripts in `tools\stats\` (setup notes: `tools\stats\HANDOFF.md`).
- Laptop not reachable (Cowork on the phone): do the Buffer part only, put the numbers in a "Pending sync" artifact, and write them to the vault when the user says the laptop is open.

## 1. What is due
Read `## Posted episodes` in the project note. One row per EP × platform:
`| EP | platform | url/id | posted | views | avg % viewed | viewed vs swiped | likes | comments | shares | checked |`
- Check points: **48h, 7d, 28d** after `posted` (Bangkok time). `checked` holds the last one done, e.g. `2026-11-10 48h`.
- A row is due when the next check point's time has passed. Nothing due and the user didn't ask → say when the next one is and stop.
- If the user asks anyway, update the numbers; label `checked` with the date + `extra`.

## 2. Collect
**YouTube** (laptop): `python tools/stats/yt_analytics.py --json <scratchpad>/yt.json` from the Youtube folder. Match rows by video id. Gives views, likes, comments, shares, averageViewPercentage, averageViewDuration. No comment text: that endpoint needs the full-account `youtube.force-ssl` scope, which we don't ask for.
- "YOUTUBE LOGIN EXPIRED" → ask the user to run `python tools/stats/auth_youtube.py` (browser login as howitworksth; the app is in Testing, so this happens every 7 days), then rerun.
- Analytics lags 1-2 days: zeros on a video under 2 days old are normal; don't record them as a check point.

**TikTok + Instagram** (Buffer MCP): `get_account` → org id; `list_posts` with `status: ["sent"]`, `includeMetrics: true`. Match a post to an episode by its video asset title (`ep1-air-fryer_v9.mp4` → EP1) and `channelService`.
- TikTok: views, reactions (likes), comments, shares; **avg % viewed = averageTimeWatched ÷ (durationMs/1000) × 100**, rounded to 1 decimal.
- Instagram: `metrics` is often `null` → leave blank and ask for an Insights screenshot (below).
- Use Buffer's post id as `url/id` for TikTok/Instagram until the user gives the real link.

**Facebook + gaps** (the user): ask once, with buttons: "Add screenshots for Facebook / Instagram / YouTube 'viewed vs swiped away'?" → send screenshots / skip. Read Meta Business Suite, Instagram Insights and YouTube Studio screenshots. Never invent a number: unknown stays blank.

## 3. Write
1. **`## Posted episodes`**: overwrite each row's numbers with the newest, set `checked`. New episode/platform → add a row. Keep the table sorted by EP, then platform (YouTube, TikTok, Instagram, Facebook).
2. **`product\epX-name\review\score-log.md`** (laptop): one row per check point per platform, under the existing columns:
   `| <date> | <version> (<platform> <checkpoint>) | <GRS of that version> | <viewed vs swiped> | <avg % viewed> | views N, likes N, comments N, shares N |`
3. **Comments** (topic ideas, when the counts show new ones): ask the user to paste or screenshot them, then under `### Comments` at the end of `## Posted episodes`, add new ones as `- EPx <platform>: "<short quote>" → <product/question it suggests>`. Skip spam and duplicates. These feed `second-brain:pick-topics`.
4. **Project note `## Log`**: `- YYYY-MM-DD — stats <checkpoint>: EPx YouTube N views / X% viewed, TikTok …` (one line per run).

## 4. Tell the user
A short table: EP × platform → views, avg % viewed, change since the last check point. Then one line comparing real avg % viewed with the predicted GRS (e.g. "EP1 GRS 89 → 62% viewed on YouTube"), plus the date of the next check point.
