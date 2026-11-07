---
name: plan-episode
description: Plan the next episode of the Thai YouTube Shorts series วิทย์ของของใช้ end to end - run pick-topics (research + 5 product candidates), let the user choose a title, run write-episode (Thai script + scene storyboard), let the user approve it, then save it to the Second Brain vault and the laptop's Youtube folder ready for /make-episode. Use whenever the user says "plan the next episode", "next EP", "EP ต่อไป", "วางแผนคลิปถัดไป", types /plan-episode, or wants to go from idea to approved script in one go - on the laptop or from the phone in Cowork.
---

# plan-episode

A pipeline from "what should we make next?" to "the approved script is ready to produce". It calls two skills and stops twice for the user. Both stops use the AskUserQuestion tool (buttons); never ask with plain text.

## Steps
1. **Where are we?** Find the vault and the Youtube folder:
   - Claude Code: `D:\MySecondBrain` and `C:\Users\jirap\Desktop\Personal\Youtube`.
   - Cowork: `$HOME/mnt/...` via `device_bash`.
   If they're unreachable, say so in one line and continue in offline mode: everything goes into this session's "Pending sync - <date>" artifact (see the two skills).
   Work out the next EP number from the project note's episode list and the `product/` folders.
2. **Candidates:** run `pick-topics`. It saves the 5 candidates in the vault, or in the artifact if offline.
3. **Check-in 1, the title.** Buttons: the top 4 titles, each with its score and a one-line why. The tool allows 4 options, so name #5 in the question text. The user can pick one or type "Other" (their own idea, or "none, try again").
   - "try again": run pick-topics once more with the rejected ideas excluded.
   - Their own idea: still run the quick fact and animatability check from write-episode and warn them if it's weak.
4. **Script:** run `write-episode` for the chosen title.
5. **Check-in 2, the script + storyboard.** Show the lines with character counts, the estimated length, the storyboard table and the sources, then ask with buttons:
   - approve
   - approve with edits (they type the edits; apply them, re-check length and facts, then show again)
   - rewrite with a different angle (e.g. versus format, more myth-bust)
   - stop
   Up to 3 rewrite rounds; after that, ask whether to keep the best draft.
6. **Save the approved version:** set the vault section status to `approved` and write the Youtube files (`script/voice_script.json`, `script/storyboard.md`). Offline: mark them in the artifact's To-sync list.
7. **Finish:**
   - Log the session with `log-session` (it goes in the artifact when offline).
   - Tell the user the next step: on the laptop, start Claude Code in the Youtube folder and run `/make-episode product\ep<n>-<name>`.

## Laptop comes back
When the user says the laptop is open (in any session), read the "Pending sync" artifact(s) (Artifact `read`), write each To-sync item to its path, and tick it off. Then run the write-episode Youtube step if the script is approved.
