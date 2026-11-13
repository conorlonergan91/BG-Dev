# BG-Dev

A board game design studio that runs inside Claude Code. You act as creative director; Claude Code dispatches specialist agents across the whole life of a game, from the first idea to a printable prototype and a publishing plan.

I built it to find out how far a team of narrow, well-briefed agents could take a creative project when every decision still goes through a person, and when anything that can be checked is checked by a script instead of a model.

## What it does

- **Runs a design pipeline:** ideation, research, exploration, design, development, prototyping, testing, marketing and publishing.
- **Keeps the human in charge.** The orchestrating skill proposes, you decide, and each decision is written to the game's decision log.
- **Produces real components.** Cards, boards, tracks, tokens and player aids are generated from data files as SVG, PNG and print-and-play PDF.
- **Tests balance by simulation.** A simulator plays a game thousands of times to expose dominant strategies before a human playtest.
- **Guards against creep.** A complexity gauge, a consistency linter and a cost estimate run against each game's own budget.
- **Snapshots builds.** Whole-product builds can be frozen, listed and restored, so a direction that stops being fun can be rolled back.

## How it fits together

```
You (creative director)
   │  /bg, /bg-new, /bg-status, /bg-decide, /bg-artmock
   ▼
board-game-studio skill ── orchestrates, logs decisions
   │
   ├── 27 specialist agents (.claude/agents/)
   │     ideation · research · explore · design · developer · prototyper · playtest
   │     critic · elegance · architect · playstrat · producer · archivist · continuity
   │     theme · art-director · graphic-designer · infodesign · ux · ai-prompt
   │     copywriter · rulebook · access · marketing · funding · production · publishing
   │
   ├── Deterministic tools (tools/, Python)
   │     cards · boards · print · rulebook · sim · lint · complexity · cost
   │     bgg · version · preflight · access · art · mockup · agents
   │
   └── Knowledge base (knowledge/, 20 documents)
         design fundamentals, manufacturing specs, accessibility, publishing and IP
```

| Path | What it holds |
|---|---|
| `.claude/agents/` | 27 agent definitions, one per discipline |
| `.claude/skills/` | 3 skills: the studio orchestrator, the 2D component pipeline, the 3D component pipeline |
| `.claude/commands/` | 5 slash commands |
| `tools/` | 15 Python tool folders; the agents call these instead of guessing |
| `knowledge/` | Reference documents the agents read |
| `templates/` | Game bible, design document, playtest log, decision log, sell sheet |
| `games/` | The games themselves: `beacon` and `travel-agents` are in progress |

## Stack

- Claude Code agents, skills and slash commands (Markdown definitions)
- Python for all tooling
- SVG, PNG and PDF output for components and rulebooks
- Optional MCP servers: Blender for 3D pieces, Figma for layout

## Run it locally

1. Open this repository in Claude Code.
2. Type `/bg` to open the studio.
3. Type `/bg-new my-game` to scaffold a game under `games/my-game/`.

No setup is needed to start designing. For the 2D pipeline, install the Python dependencies:

```bash
pip install -r tools/cards/requirements.txt
```

The 3D pipeline needs Blender open with the `blender-mcp` add-on connected; the Figma integration needs Figma desktop's Dev Mode MCP server. Both are configured in `.mcp.json` and both are optional.

## What is committed and what is not

Each game's data and documents are committed. `build/` folders are scratch and ignored. `exports/` folders hold curated deliverables and are committed on purpose, which is why the repository is large. Art under `art/mockups/` is AI-generated mock-up art for playtesting only, not final art.

## How it was built

This project was built with Claude Code. Almost all commits were authored by Claude working to my direction over one week in August 2026; I set the goals, made the design decisions and reviewed the results. `CLAUDE.md` is the full operating guide the agents follow.

## Publishing scope

The publishing agent and `knowledge/publishing-ip.md` cover Ireland, the UK and the USA. This is general information to help with planning, not legal advice.
