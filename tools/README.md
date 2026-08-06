# tools/

Reusable, code-native build tooling for components. Copy/adapt per game into `games/<slug>/`.

## `cards/` — 2D card pipeline

CSV → SVG → PNG / PDF + Tabletop Simulator deck sheet. See the `bg-2d-components` skill for the full
approach and manufacturer specs.

```bash
cd tools/cards
pip install -r requirements.txt          # cairosvg + Pillow (macOS: brew install cairo pango)
python build_cards.py --csv example_deck.csv --out out --theme nautical
open out/sheets/example_deck_sheet_1.png # the Screentop.gg / TTS deck sheet

# a rough themed cover for the simulator (procedural, no assets):
python build_cover.py --title "My Game" --subtitle "a tiny duel" --theme nautical \
    --players 2 --time "20 min" --out out/cover.png
```

**Themes** (`themes.py`, pick with `--theme`): `clean`, `nautical`, `ember`, `parchment`, `cozy`.
A card's `type` column maps to a suit colour + emblem.

- **No deps installed?** The script still writes per-card **SVGs** — a useful baseline. PNG/PDF/TTS need
  `cairosvg` (and `Pillow` for TTS sheets).
- **Data is the source of truth.** Edit the CSV, re-run, diff the output. Never hand-edit renders.
- Outgrowing the built-in SVG generator? Switch to Jinja2 SVG templates or a WeasyPrint HTML/CSS
  pipeline for true CMYK + bleed (see the 2D skill).

## `boards/` — tracks, tokens & player mats

Cards aren't everything — most games need a track, some tokens, and maybe a board/mat. `build_board.py`
renders these as themed vector SVG → PNG/PDF, sharing the card themes so everything matches.

```bash
# a tug-of-war / score track (e.g. Beacon's Tide):
python boards/build_board.py --type track --spaces 7 --title "Tide" \
    --left-label "Keeper A" --right-label "Keeper B" --theme nautical --out out/tide-track.png

# a token sheet (markers/resources), tiled for cutting:
python boards/build_board.py --type tokens --labels "Tide,1st" --shape circle --theme nautical --out out/tokens.png

# a player mat / board from a JSON spec (copy boards/sample_mat.json):
python boards/build_board.py --type mat --spec boards/sample_mat.json --theme nautical --out out/mat.png

# a player-aid / quick-reference sheet from a JSON spec (title + sections):
python boards/build_board.py --type aid --spec <game>/components/player-aid.json --theme nautical --out out/aid.png
```

## `lint/` — consistency linter (stdlib-only)

Keeps the "data is the source of truth" promise honest as data/rules/manifest drift.

```bash
python lint/check_game.py --game games/beacon --theme nautical
```
Checks: unique card ids, numeric value/cost, positive integer quantities, recommended columns, card
`type`s that a theme actually colours, and that any `sim/*.py` still imports and exposes GAME +
STRATEGIES. Non-zero exit on errors — good as a pre-commit sanity check.

## `version/` — build snapshots (stdlib-only)

Freeze / list / restore whole-product "builds" so you can revert to a known-good state and branch off it.

```bash
python version/build_snapshot.py cut     --game games/beacon --note "v0.3, balanced & fun"
python version/build_snapshot.py list    --game games/beacon
python version/build_snapshot.py restore --game games/beacon --build 3 --yes   # onto a fresh branch
```
A build = a self-contained snapshot in `games/<slug>/builds/build-N/` + a `BUILDS.md` ledger. Excludes
`build/`/`builds/`; `--source-only` also skips regenerable `exports/`. Owned by `bg-architect`.

## `bgg/` — BoardGameGeek reference lookups (stdlib-only)

Deterministic facts (community **weight** 1–5, players, playtime, mechanisms, rank) for grounding
research/ideation and seeding a complexity budget from a real game.

```bash
python bgg/bgg_lookup.py --name "Arcs"                      # reference card
python bgg/bgg_lookup.py --name "Arcs" --suggest-budget     # complexity-budget.json seeded from its weight
python bgg/bgg_lookup.py --thing-xml bgg/sample_thing.xml   # offline parse test (no network)
```
Needs outbound access to boardgamegeek.com; some managed-session egress policies block it (403 from the
proxy) — then fall back to cited WebSearch. Owned by `bg-research` / `bg-elegance`.

## `complexity/` — complexity-drift gauge (stdlib-only)

Objective proxies for rules overhead vs the game's target, so weight doesn't creep as you iterate.

```bash
python complexity/check_complexity.py --game games/beacon          # report
python complexity/check_complexity.py --game games/beacon --strict # exit 1 if over budget
```
Reads `games/<slug>/complexity-budget.json` (set at project start; copy `templates/complexity-budget.json`)
and reports rulebook words, glossary keyword count, exception density, component types, and player-aid
length. Owned by the `bg-elegance` agent; see `knowledge/elegance-and-clarity.md`.

## `rulebook/` — rules markdown → themed rulebook

```bash
python rulebook/build_rulebook.py --md games/beacon/design/rules-draft.md \
    --title "Beacon" --theme nautical --out games/beacon/build/rulebook.pdf
```
Always writes a themed `.html`; writes `.pdf` too if WeasyPrint is installed
(`pip install weasyprint markdown`; macOS also `brew install pango gdk-pixbuf`). Rules stay as
diffable markdown (the source of truth); this just lays them out.

## 3D components

Driven live through the Blender / FreeCAD / OpenSCAD **MCP servers** rather than a script here — see the
`bg-3d-components` skill.
