# BG-Dev — A Board Game Design Studio for Claude Code

This repository is a **human + AI board game design studio**. It turns Claude Code into a
collaborative studio: you (the human) are the **Creative Director**; Claude runs the studio and
dispatches a team of specialist agents across the whole lifecycle of a tabletop game — from a blank
page to a print-and-play prototype, a Tabletop Simulator module, 3D components, a sell sheet, and a
publishing/compliance plan.

The guiding principles: **human in the loop throughout, quick and fun decision-making, tight
iteration loops, and one living source of truth per game.**

**Current studio focus (house style):** design **2-player games first**, spanning **both co-op and
competitive duels** — co-op is a first-class focus, not an afterthought. Prize **elegance** (high depth
from low complexity, ~1.5–2.5 weight, ~20–40 min). A signature love is **constrained-communication
co-op** (Hanabi / Sky Team / SAIL) and **tug-of-war / race duels** (Splendor Duel / LOTR: Duel for
Middle-earth / Patchwork). Target **Screentop.gg** as the default playtest platform (free, browser,
join-by-link, remote or in person); TTS / Tabletopia / print-and-play are alternates.

**Read `knowledge/designer-profile.md`** for the full taste signature and design values, and point every
dispatched `bg-*` agent at it — it's the studio's north star.

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
| Creative identity | `bg-theme` | Owns & guards the felt identity — concept, theme, tone/vibe, story/lore, look & feel, naming — keeping it coherent while it *evolves* with the design (the MDA "aesthetics" leg). |
| Research | `bg-research` | Market/competitive research — comparable games, gaps, audience, what's been done. |
| Explore / Brainstorm | `bg-explore` | Divergent exploration of the design space; mechanism blends, twists, "what ifs". |
| Design | `bg-design` | Systems design — core loop, components, rules architecture, economy/math, balance. |
| Architecture | `bg-architect` | Player modes (solo/duel/multi/party), campaigns, and base-vs-expansion scope; component reuse; plays well separately & combined. |
| Development | `bg-developer` | Turns design into concrete artifacts: card/component data, rules spec, build code. |
| Prototyping | `bg-prototyper` | Produces playable outputs: **Screentop.gg** deck (default) / TTS module, print-and-play PDF, 3D pieces. |
| Information design | `bg-infodesign` | Functional graphic design — icon system, visual hierarchy, at-a-glance readability so players parse components without the rulebook (distinct from `bg-theme`'s felt identity). |
| Accessibility | `bg-access` | **Guardian.** Colour-blind safety (redundant encoding), contrast/legibility, cognitive/motor/communication load, price — who can actually play. Runs `tools/access/check_access.py`. |
| Critique | `bg-critic` | Adversarial red-team: hunts dominant strategies, dead turns, swinginess, co-op alpha-player leaks — before you spend playtests. |
| Elegance | `bg-elegance` | Guards the complexity budget (set at start), hunts what to cut/merge, keeps the rulebook + player aid succinct/clear/fun (incl. the editorial pass), disciplined FAQ. |
| Testing | `bg-playtest` | Playtest plans (incl. FTUE/blind-test), session logging, feedback synthesis, balance analysis, and simulation (`tools/sim`). |
| Funding / route | `bg-funding` | **How the game is released** — free / POD / pitch-to-publisher / crowdfunding, ranked by upfront cost & risk. Defaults to minimal out-of-pocket. Owns the money decision before marketing copy. |
| Marketing | `bg-marketing` | Pitch, elevator, box copy, sell sheet, crowdfunding page, audience strategy — for the route `bg-funding` chose. |
| Publishing | `bg-publishing` | IP / copyright / trademark / compliance for **Ireland, UK, USA**; contracts; sensitivity-risk flag. |
| Production | `bg-production` | Physical make & ship — manufacturing, component engineering, sourcing, freight/tariffs, fulfilment, pledge-manager ops. Runs print pre-flight. Deferred until a physical run (skip if licensed). |

**How to invoke an agent:** use the `Agent` tool with the matching `subagent_type` (e.g.
`bg-design`). Give it the game slug and point it at that game's `game-bible.md`. When work is
independent, launch agents in parallel.

**The guardian sweep:** after every `bg-design` / `bg-developer` pass, auto-run the guardians in
parallel before advancing — **`bg-theme`** (does the fiction still fit the changed mechanics? re-theme
vs drift/restriction), **`bg-elegance`** (still within the complexity budget?), and — when the pass
touched **component data / the theme** — **`bg-access`** (colour-blind/contrast/legibility floor still
met?) and **`bg-infodesign`** (still parseable at a glance?). Cheap by default; only surface to the human
when one actually flags something. (Full cadence in the `board-game-studio` skill.)

---

## One source of truth per game

Every game lives in `games/<slug>/` and is anchored by a **living `game-bible.md`** — the shared
document the human and every agent read and update. Supporting files:

```
games/<slug>/
├── game-bible.md        # THE living design document — single source of truth
├── identity.md          # THE living creative identity — concept/theme/tone/lore/look&feel/naming (bg-theme)
├── decision-log.md      # every key decision + the rationale (fast to skim)
├── design/              # deeper design notes, math/economy spreadsheets, rules drafts
├── components/          # component DATA (CSV/JSON) — cards, tiles, tokens (the real source)
├── build/               # SCRATCH renders (PDF/PNG/TTS/STL) — gitignored, fully regenerated
├── exports/             # COMMITTED deliverables — curated shareable renders (deck sheets, cover, rulebook)
├── make.sh              # regenerates build/ from data, then snapshots deliverables into exports/
├── playtests/           # playtest logs and feedback synthesis
├── builds/              # frozen build snapshots (build-N/) + BUILDS.md ledger — see "Scaling" below
├── art/                 # art briefs, references, and assets
└── marketing/           # pitch, sell sheet, campaign copy
```

### Scaling a project: products, modules, series & builds

Start flat (above) — a focused game needs nothing more. **Grow only as scope demands** (restraint):
- **Expansion or a distinct mode** → add a self-contained module folder: `games/<slug>/expansions/<exp>/`
  or `games/<slug>/modes/<mode>/`, each with its own `…-bible.md`, `design/`, `components/`, `sim/`,
  `playtests/`, `exports/`, and a combined-with-base `complexity-budget.json`. Iterate a module
  independently; `make.sh` builds base + modules.
- **Whole-product oversight** → once a game has ≥1 module, add **`product.md`** (from
  `templates/product.md`): base + every module at a glance, the combined component/complexity view, and
  the *plays-well separately & combined* status. Owned by `bg-architect`.
- **Series** (several standalone products sharing IP/theme) → keep each as its own `games/<slug>/`,
  linked by a `series/<name>.md` manifest (shared assets + member list); each `product.md` notes its series.
- **Builds (versioning)** → `builds/build-N/` are **frozen snapshots** + a `BUILDS.md` ledger, managed by
  `python tools/version/build_snapshot.py {cut|list|restore}`. **Cut a build at each known-good / fun
  state.** If a direction stops being fun, `restore` build N onto a fresh git branch and continue —
  independently or as part of the whole. Snapshots are self-contained (source + exports; `--source-only`
  skips regenerable renders). Snapshots exclude `build/` and `builds/` themselves.

Rule: **data is the source; renders are regenerated.** Cards/tiles/tokens are defined as data
(CSV/JSON) and rendered by the 2D/3D tooling. Never hand-edit generated files. `build/` is disposable
scratch (gitignored); the **curated deliverables you want on GitHub / to share** (deck sheets, cover,
rulebook PDF, board, tokens) are snapshotted into **`exports/` (committed)** by the game's `make.sh`.
Regenerate anytime — if the data changes, re-run `make.sh` and commit the refreshed `exports/`.

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

### Playtest simulator (`tools/sim/`)

Encode a game's rules once as `games/<slug>/sim/<slug>.py` and play it thousands of times to expose
dominant strategies, balance, and score spreads **before** human playtesting (stdlib-only). Every run
ends with an auto **Health read** (dominant line? intransitive depth?). Owned by `bg-playtest`; see the
playbook `knowledge/simulation-and-balance.md`, `tools/sim/README.md`, and the worked example
`games/beacon/sim/beacon.py`.

### Reference data — BoardGameGeek (`tools/bgg/`)

`python tools/bgg/bgg_lookup.py --name "<game>"` fetches **deterministic** facts from BGG's XML API —
community **weight** (1–5), player count, playtime, mechanisms, rank — for grounding research/ideation.
`--suggest-budget [--out …]` seeds a `complexity-budget.json` from a reference game's weight ("budget it
like *Arcs*"). Needs egress to boardgamegeek.com (some managed sessions block it — fall back to cited
WebSearch). Offline-testable via `--thing-xml`.

### Guardrails (`tools/lint/`, `tools/rulebook/`, `tools/access/`, `tools/cost/`, `tools/preflight/`)

- **Linter** — `python tools/lint/check_game.py --game games/<slug> --theme <name>`: validates card data
  (unique ids, numeric fields, quantities, theme suit coverage) and that sim modules still import.
  Stdlib-only; run it as a quick sanity check (ideally before committing component changes).
- **Rulebook generator** — `python tools/rulebook/build_rulebook.py --md <rules.md> --theme <name> --out
  <build>/rulebook.pdf`: rules markdown → themed A5 HTML/PDF. Rules stay diffable markdown; this lays
  them out.
- **Complexity gauge** — `python tools/complexity/check_complexity.py --game games/<slug>`: objective
  drift proxies (rulebook words, keywords, exceptions, component types, player-aid length) vs the
  game's `complexity-budget.json`. Owned by `bg-elegance`; set the budget at project start and guard it.
- **Accessibility linter** — `python tools/access/check_access.py --game games/<slug> --theme <name>`:
  simulates protanopia/deuteranopia/tritanopia on the theme palette (Machado matrices, CIELAB ΔE) and flags
  colour-only suit collisions (dual-coding by emblem aware); checks WCAG text contrast. Owned by `bg-access`.
- **Cost gauge** — `python tools/cost/check_cost.py --game games/<slug>`: estimates the bill of materials
  and COGS vs `component-cost-budget.json` (component types, pieces, unique cards, COGS % of retail). The
  cost analog of the complexity gauge. Owned by `bg-architect` (+ `bg-funding`).
- **Print pre-flight** — `python tools/preflight/check_print.py --game games/<slug>`: validates a game's
  `print-spec.json` (bleed, safe margin, DPI, CMYK, card size, min font) before a physical run. Owned by
  `bg-production`; skipped for Screentop-only / licensed games.

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
- `theme-and-identity.md` — the felt identity: concept/theme/tone/lore/look&feel/naming, the kinds of fun, theme↔mechanic resonance, the restraint ladder (owned by `bg-theme`).
- `information-design.md` — functional graphic design: icon systems, visual hierarchy, at-a-glance readability (owned by `bg-infodesign`).
- `accessibility.md` — the Meeple-Centred Design categories + redundant-encoding rule; colour-blind/contrast/cognitive/motor/communication (owned by `bg-access`).
- `representation-and-sensitivity.md` — when a theme touches real cultures: the trigger + checklist (owned by `bg-theme` + `bg-publishing`).
- `process-and-playtesting.md` — the indie pipeline, rules-writing, blind-testing + FTUE instrumentation.
- `simulation-and-balance.md` — pressure-testing balance *and* fun (decision density, randomness, tension curve) with `tools/sim`.
- `elegance-and-clarity.md` — the complexity budget, the cut test, rulebook/aid clarity + the editorial pass.
- `cost-and-manufacturability.md` — design for cheap: component-type/box/size levers, COGS budget, tariffs (owned by `bg-architect`).
- `funding-and-route-to-market.md` — free / POD / pitch / crowdfunding, ranked by upfront cost & risk (owned by `bg-funding`).
- `manufacturing-and-fulfillment.md` — making & shipping a physical run: sourcing, freight/tariffs, 3PL, pledge manager (owned by `bg-production`).
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

## Git & commit conventions

Work on branch `claude/board-game-design-agents-81gkkl`.

**Commit early and often, and push as you go** (the maintainer's explicit preference):
- **Small, logical commits** — one coherent change per commit, not a big end-of-session dump. A new
  design stage, a component-data change, a rules revision, a tooling tweak → each its own commit.
- **Messages explain the WHY, not just the what.** The subject line says what changed; the body says
  *why it changed* — the motivation, the design reasoning, the trade-off or alternative rejected. A
  reader (or future session) should understand the intent without re-reading the diff. Mirror the
  `decision-log.md` habit: capture rationale, not just mechanics.
- **Push after each meaningful commit** (`git push -u origin <branch>`), so work is never stranded in
  the ephemeral container. Retry with backoff on network errors.
- Do **not** open a PR unless the user explicitly asks.

Example subject + body:
> `Swap Beacon's signal-reclaim rule for the "tide turns" initiative handoff`
> *Why: signal-reclaim added per-Night bookkeeping and was hard to teach; handing the Night's Tide-loser
> first-keeper next Night gives the same catch-up valve with zero extra components. Keeps weight ~1.8.*
