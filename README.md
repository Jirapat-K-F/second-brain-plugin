# second-brain-plugin

Private Claude plugin marketplace for my Obsidian second brain (`D:\MySecondBrain`).
This folder is `80-Skills/` inside the vault and is its own git repo.

| Skill | What it does |
|---|---|
| `second-brain:log-session` | writes a session note + daily-note link |
| `second-brain:research` | checks the vault first, then saves sourced research |
| `second-brain:new-experiment` | captures and tracks things to try |
| `second-brain:weekly-review` | weekly vault health check with safe fixes |

## Change a skill
1. Edit `plugins/second-brain/skills/<skill>/SKILL.md` (in Obsidian or any editor).
2. Bump `version` in `plugins/second-brain/.claude-plugin/plugin.json` (e.g. 1.0.0 -> 1.0.1).
3. `git add . ; git commit -m "..." ; git push`
4. Claude app/Cowork picks up the update from the marketplace; in Claude Code run `/plugin marketplace update second-brain-plugin`.

## Install (once per account)
- Claude app: Customize > Plugins > Add marketplace > `<your-github-username>/second-brain-plugin`, then install **second-brain**.
- Claude Code (if it isn't synced from your account): `/plugin marketplace add <your-github-username>/second-brain-plugin` then `/plugin install second-brain@second-brain-plugin`.
