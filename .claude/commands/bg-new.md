---
description: Scaffold a new board game project under games/<slug>/.
argument-hint: <game name or slug>
---

Scaffold a new game project. The name/slug is: $ARGUMENTS

Steps:
1. Derive a clean `slug` (lowercase, hyphenated) from the name. Confirm it with the user if ambiguous.
2. Create the project folder structure under `games/<slug>/`:
   - `game-bible.md`  (copy from `templates/game-bible.md`, fill in the title/slug/date)
   - `decision-log.md` (copy from `templates/decision-log.md`)
   - `make.sh` (copy from `templates/make.sh`; edit theme/title/decks — regenerates `build/` and snapshots `exports/`)
   - `design/`, `components/`, `playtests/`, `art/`, `marketing/`, `exports/`  (create with a `.gitkeep`)
   - (`build/` is scratch and gitignored — no need to create it; the tools make it.)
3. Then invoke the `board-game-studio` skill and, as Creative Director, ask the one framing question
   that matters most: **blank-slate ideation, or does the user have a concept to develop?** — offered
   as an A/B/C choice with a recommendation.

Keep it quick and welcoming — this is the start of something fun.
