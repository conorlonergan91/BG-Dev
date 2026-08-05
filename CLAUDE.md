# BG-Dev — A Board Game Design Studio for Claude Code

This repository is a **human + AI board game design studio**. It turns Claude Code into a
collaborative studio: you (the human) are the **Creative Director**; Claude runs the studio and
dispatches a team of specialist agents across the whole lifecycle of a tabletop game — from a blank
page to a print-and-play prototype, a Tabletop Simulator module, 3D components, a sell sheet, and a
publishing/compliance plan.

The guiding principles: **human in the loop throughout, quick and fun decision-making, tight
iteration loops, and one living source of truth per game.**

**Current studio focus (house style):** design **2-player games first** (tight direct tension, no
"bash the leader"; touchstones: 7 Wonders Duel, The Crew, Fox in the Forest, Patchwork, Jaipur,
Sky Team), and target **Screentop.gg** as the default playtest platform (free, browser, join-by-link,
works remote or in person). TTS / Tabletopia / print-and-play are alternates.

---

## How to start

- Run **`/bg`** (or say *"open the studio"*) to launch or resume the studio. This invokes the
  `board-game-studio` skill, which is the orchestrator.
- Run **`/bg-new <name>`** to scaffold a new game project under `games/<slug>/`.
- Run **`/bg-status`** to see where the current game is in the pipeline.
- Run **`/bg-decide`** when you want to force a quick, focused decision to keep momentum.

If the user asks anything about designing, prototyping, testing, marketing, or publishing a board
game, **invoke the `board-game-studio` skill** — do not freelance it. The skill defines the studio
operating protocol and the human-in-the-loop cadence.

---

## The composable pipeline (specialist agents)

The studio is a **composable pipeline** of discrete subagents in `.claude/agents/`. They are not
strictly linear — the Creative Director (main Claude) picks whichever stage the game needs next, and
agents can be re-run at any time. Each agent has a **contract**: it reads from and writes back to the
game's living documents (see "One source of truth" below), so they chain cleanly.

| Stage | Agent | What it does |
|-------|-------|--------------|
| Ideation | `bg-ideation` | Generates and frames concepts (theme × mechanism hooks), blank-slate or from a seed. |
| Research | `bg-research` | Market/competitive research — comparable games, gaps, audience, what's been done. |
| Explore / Brainstorm | `bg-explore` | Divergent exploration of the design space; mechanism blends, twists, "what ifs". |
| Design | `bg-design` | Systems design — core loop, components, rules architecture, economy/math, balance. |
| Development | `bg-developer` | Turns design into concrete artifacts: card/component data, rules spec, build code. |
| Prototyping | `bg-prototyper` | Produces playable outputs: **Screentop.gg** deck (default) / TTS module, print-and-play PDF, 3D pieces. |
| Testing | `bg-playtest` | Playtest plans, session logging, feedback synthesis, balance analysis, solo/simulation. |
| Marketing | `bg-marketing` | Pitch, elevator, box copy, sell sheet, crowdfunding page, audience strategy. |
| Publishing | `bg-publishing` | IP / copyright / trademark / compliance for **Ireland, UK, USA**; self-publish vs pitch. |

**How to invoke an agent:** use the `Agent` tool with the matching `subagent_type` (e.g.
`bg-design`). Give it the game slug and point it at that game's `game-bible.md`. When work is
independent, launch agents in parallel.

---

## One source of truth per game

Every game lives in `games/<slug>/` and is anchored by a **living `game-bible.md`** — the shared
document the human and every agent read and update. Supporting files:

```
games/<slug>/
├── game-bible.md        # THE living design document — single source of truth
├── decision-log.md      # every key decision + the rationale (fast to skim)
├── design/              # deeper design notes, math/economy spreadsheets, rules drafts
├── components/          # component DATA (CSV/JSON) — cards, tiles, tokens (the real source)
├── build/              # GENERATED output (PDF/PNG/TTS/STL) — gitignored, regenerated from data
├── playtests/           # playtest logs and feedback synthesis
├── art/                 # art briefs, references, and assets
└── marketing/           # pitch, sell sheet, campaign copy
```

Rule: **data is the source; renders are disposable.** Cards/tiles/tokens are defined as data
(CSV/JSON) and rendered by the 2D/3D tooling. Never hand-edit generated files in `build/`.

---

## Tooling

Two tooling skills describe the concrete pipelines. Read the relevant one before producing components.

- **`bg-2d-components`** — cards, tiles, player boards, game boards, tokens, rulebook layout.
  Code-native pipeline: **data (CSV/JSON) → SVG/HTML template → print-ready PDF / PNG / Screentop or TTS deck sheet.**
  Free/open, deterministic, diffable. Optional Figma MCP for visual/board layout with a human.
- **`bg-3d-components`** — miniatures, dice, custom pieces, inserts, boxes via **Blender MCP**
  (organic/aesthetic + renders) and **FreeCAD / OpenSCAD MCP** (precision, print-first parts).

### MCP servers (`.mcp.json`)

- **`blender`** — `uvx blender-mcp`. Requires Blender open with the "Blender MCP" addon installed and
  **"Connect to Claude"** clicked (socket on `localhost:9876`). See `bg-3d-components`.
- **`figma`** — Figma desktop's Dev Mode MCP server at `http://127.0.0.1:3845/mcp`. Enable it in
  Figma → Preferences → "Enable Dev Mode MCP Server". (Older builds use the `/sse` endpoint.)

Both are optional — the studio works fully without them (code-native 2D + TTS). Wire them up when you
want 3D pieces (Blender) or collaborative visual layout (Figma).

### Recommended free installs (macOS)

- `uv` (for `uvx blender-mcp`): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Blender (free): https://www.blender.org/download/  + the Blender MCP addon.
- Python deps for the 2D pipeline: `pip install -r tools/cards/requirements.txt`
  (`weasyprint`, `cairosvg`, `jinja2`, `pandas`). Optional: Inkscape CLI, and `playwright` for RGB
  TTS/preview sheets.

---

## Knowledge base

`knowledge/` holds the studio's up-to-date reference material. Agents cite and build on it.

- `archetypes.md` — mechanism families + canonical reference games + how blends work.
- `reference-games.md` — landmark designs and what each is known for; award context.
- `design-fundamentals.md` — MDA, core loop, agency, randomness, feedback, weight, solo/Automa.
- `process-and-playtesting.md` — the indie pipeline and rules-writing + blind-testing best practice.
- `trends-2026.md` — what's current (cozy games, solo, crowdfunding shift, market pressures).
- `manufacturing-specs.md` — card sizes, bleed, DPI, POD specs, TTS export limits.
- `publishing-ip.md` — IP/copyright/trademark/compliance for IE/UK/US (general info, not legal advice).

---

## Operating style (for Claude)

- **Keep the human in the loop, but keep it moving.** Present tight, opinionated options (A/B/C with a
  recommendation) rather than open-ended questions. Decide fast, log it, iterate.
- **Update the living docs as you go.** Every meaningful choice → `game-bible.md` + `decision-log.md`.
- **Make it fun.** This is a creative project. Be energetic, celebrate milestones, name things, and
  keep prototypes playable early and often.
- **Prefer playable over polished.** Get to a testable Screentop.gg / paper prototype fast, then
  iterate on the real thing.
- **Cite the knowledge base** when giving design/publishing advice, and flag when something should be
  re-checked live (rankings, fees, legal/compliance specifics).

## Git

Work on branch `claude/board-game-design-agents-81gkkl`. Commit with clear messages. Only push when
the work is complete or the user asks. Do not open a PR unless explicitly requested.
