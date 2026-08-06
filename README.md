# 🎲 BG-Dev — A Board Game Design Studio for Claude Code

A human + AI studio for designing tabletop games, end to end. You are the **Creative Director**;
Claude Code runs the studio and dispatches a team of specialist agents across the whole lifecycle:
**ideation → research → exploration → design → development → prototyping → testing → marketing →
publishing.**

Built for fast, fun, human-in-the-loop iteration — get to a playable **Tabletop Simulator** or
print-and-play prototype early, then refine the real game.

## Quickstart

1. Open this repo in Claude Code.
2. Say **`/bg`** (or *"open the studio"*) to launch the studio.
3. **`/bg-new my-game`** scaffolds a new game under `games/my-game/`.
4. Work through the pipeline with the Creative Director — it will keep the momentum and log decisions.

No setup is required to start designing. To unlock 3D pieces and visual layout, wire up the optional
MCP servers (see below).

## What's in the box

| Path | What it is |
|------|------------|
| `.claude/agents/` | The composable pipeline — 11 specialist subagents (`bg-ideation` … `bg-critic` … `bg-elegance` … `bg-publishing`). |
| `.claude/skills/board-game-studio/` | The **Creative Director** orchestrator (human-in-the-loop protocol). |
| `.claude/skills/bg-2d-components/` | Cards / boards / tracks / tokens / player aids: **data → SVG → PNG / PDF / Screentop**, themed. |
| `.claude/skills/bg-3d-components/` | Miniatures / dice / inserts / boxes via **Blender / FreeCAD / OpenSCAD MCP**. |
| `.claude/commands/` | Quick slash commands: `/bg`, `/bg-new`, `/bg-status`, `/bg-decide`. |
| `knowledge/` | Up-to-date knowledge base + `designer-profile.md` (the studio's taste north star). |
| `templates/` | Game bible, design doc, playtest log, decision log, sell sheet, `make.sh`, example data. |
| `tools/cards/` | 2D pipeline: data → themed SVG → PNG/PDF, deck sheets, **covers** (`themes.py`). |
| `tools/boards/` | Themed **tracks, tokens, mats, player aids**. |
| `tools/sim/` | **Playtest simulator** — play a game thousands of times to expose dominant strategies & balance. |
| `tools/lint/`, `tools/rulebook/` | Consistency **linter** + **rulebook** generator (markdown → themed A5 PDF). |
| `tools/complexity/` | **Complexity gauge** — proxies vs the game's budget, so weight doesn't creep as you iterate. |
| `tools/bgg/` | **BoardGameGeek lookups** — deterministic weight/players/mechanisms/rank; seed a budget "like *Arcs*". |
| `games/` | Your games live here — data + docs committed; `build/` is scratch, `exports/` holds committed deliverables. |

## Optional integrations

- **Blender MCP** (3D components + renders): install [`blender-mcp`](https://github.com/ahujasid/blender-mcp),
  keep Blender open with the addon connected. Configured in `.mcp.json`.
- **Figma MCP** (visual / board / rulebook layout): enable Figma desktop's Dev Mode MCP server.
- **2D pipeline deps**: `pip install -r tools/cards/requirements.txt`.

## Publishing scope

The `bg-publishing` agent and `knowledge/publishing-ip.md` cover **Ireland, the UK, and the USA** —
copyright, trademark, product-safety/compliance (CE/UKCA, ASTM F963/CPSIA), and self-publish vs pitch.
This is general information to help you plan, **not legal advice**; confirm registrations, contracts,
and safety testing with a qualified professional in each market.

---

*See [`CLAUDE.md`](./CLAUDE.md) for the full studio operating guide.*
