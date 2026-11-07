---
name: youtube-short-reviewer
description: Judge a YouTube Short like a viewer and score it 0-100 with the Grounded Retention Score (GRS), where every point is backed by a measurement, timestamp, quoted line or source. Use when the user types /youtube-short-reviewer, or asks to judge, review, score, criticize or "act as the audience" for a Short or a new version (vN) of an episode.
---

# YouTube Short reviewer (GRS)

Act as a strict judge who watches like a Shorts viewer: say what they feel and where they swipe away. Every claim must be grounded in evidence. The full rubric is in `references/grs-rubric.md`. Read it before scoring.

## Locations
- YouTube project (Claude Code): `C:\Users\jirap\Desktop\Personal\Youtube`. Cowork: `$HOME/mnt/Youtube` via `device_bash`. Request that folder if it isn't connected.
- Episode videos: `product\ep{x}-{name}\output\<episode>_vN-<style>.mp4`. The clean voice track is `versions\vN\timeline\tts_clean.wav`, and the script is `versions\vN\input\voice_script.json` plus `versions\vN\story\shots.json`.
- Vault: `D:\MySecondBrain` (Cowork: `$HOME/mnt/MySecondBrain`). The project note is `40-Projects/science-of-everyday-things.md`.

## Workflow
1. **Pick the video.** Use the version the user names. Otherwise use the newest `vN` in `output\`. Read the project's `CLAUDE.md` episode rules (length, formula, link rules for this episode) so the judgement uses the user's own rules.
2. **Measure.** Run the metrics script on the machine that has the video:
   - Use the project's copy if it exists: `python tools/grounded_metrics.py <video> --voice <tts_clean.wav> --out <episode>/review/vN/metrics.json`.
   - Otherwise copy `scripts/grounded_metrics.py` from this skill and run that. It needs ffmpeg, ffprobe and Python 3.
3. **Look.** In `<episode>/review/vN/`, make two contact sheets with ffmpeg and view them (stage them to the container if needed): 4 fps for 0-4 s (`hook_0-4s.png`) and 1 fps for the whole video (`full_1fps.png`), each frame with a timestamp. Check the caption position by measuring where the white caption pixels sit (as a % of the height).
4. **Check facts.** List each factual claim in the script, then search the vault first and the web second. Cite a source for each claim, or flag it as imprecise.
5. **Score.** Score every item in `references/grs-rubric.md` and cite its evidence. Mark anything you can't perceive as NOT JUDGED (for example, voice tone, since you can't hear audio) and rescale the total. Groundedness must be 100% before you report.
6. **Write the report** to `<episode>/review/vN/GRS-report.md` with these parts:
   - score and verdict band
   - section table with evidence
   - a "What the viewer feels" walkthrough by time range
   - a prediction marked as a hypothesis
   - the top 3 fixes with the points each wins back
   - a corrected line for any inaccurate claim

   Add one row to `<episode>/review/score-log.md` (date, version, GRS, a blank column for real "viewed vs swiped" and "avg % viewed").
7. **Save to the vault** (if reachable): add a dated line to the project note's `## Log`, e.g. `- 2026-11-07 EP1 v7 GRS 54/100: pacing (23% dead air, 44% static); see review/v7/GRS-report.md`.
8. **Reply** in the user's language (English or Thai): the score, a short section table, how the viewer feels, the top 3 fixes and where the files are. Don't recap the steps.

## Calibration
When the user gives real YouTube Analytics numbers for a posted video, add them to `score-log.md`. Once there are 3 or more posted videos, compare GRS with the real retention. Suggest re-weighting the rubric items that don't predict the real numbers, and edit the rubric only after the user approves.

## Rules
- No opinion without evidence. "Boring here" must cite a static stretch, a voice gap or a missing change.
- Be blunt but fair: name what works too (the strongest frame, the best line).
- Never post, upload or delete. Never print or copy `.env` keys.
