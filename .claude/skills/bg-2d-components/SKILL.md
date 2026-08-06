---
name: bg-2d-components
description: Generate 2D board game components — cards, tiles, player boards, game boards, tokens, rulebook pages — from component data. Use whenever you need to render or lay out printable/playable 2D parts. Covers the code-native pipeline (data CSV/JSON → SVG/HTML template → print-ready PDF / PNG / Tabletop Simulator deck sheets), manufacturer specs (sizes, bleed, DPI), print-and-play layout, and when to use the Figma MCP for collaborative visual layout.
---

# 2D component pipeline

The studio's 2D approach is **code-native and deterministic**: component **data** is the source of
truth; templates render it to print-ready and TTS-ready output. Everything is plain text, diffable,
and re-runnable — regenerate on every data change; never hand-edit renders.

```
data (CSV/JSON)  →  template (SVG or HTML/CSS)  →  render  →  PDF (print) / PNG / deck sheet (Screentop/TTS)
```

## When to use what

- **Cards / tokens / tiles (batch, data-driven):** the code pipeline below. This is the default.
- **Boards / player mats / rulebook (visual, human-in-the-loop):** the code pipeline for a
  data-driven board, **or** the **Figma MCP** when the human wants to art-direct layout interactively
  (Figma is the only production-grade design MCP — good for boards/rulebooks; still export + treat as
  final art). See `CLAUDE.md` for the Figma endpoint.
- **Quick prototype to play now:** render a deck sheet for **Screentop.gg** (the studio default — see
  below) — this is the fast path. TTS / Tabletopia use the same grid-sheet format.

## The recommended stack (free / open, macOS-friendly)

Starter code lives in `tools/cards/` — copy/adapt it per game into `games/<slug>/`.

- **Data:** CSV or JSON, one row/object per component. Every field a template needs (id, name, type,
  cost, text, values, quantity, art-note, tags).
- **Template:** **SVG** (via Jinja2 / string substitution) for exact mm placement and highest
  fidelity — the recommended default; **or** HTML/CSS with **CSS Paged Media** for text-heavy layouts.
- **Render:**
  - SVG → PDF/PNG: `cairosvg` or **Inkscape CLI** (`inkscape --export-type=pdf`).
  - HTML/CSS → PDF (**true CMYK + bleed/crop marks**): **WeasyPrint** (best open option). Paged.js for
    JS-heavy rulebook pagination. (Puppeteer/Playwright forces RGB @96 DPI — fine for TTS/preview, weak
    for CMYK manufacturing.)
- **Deps:** `pip install -r tools/cards/requirements.txt` (`weasyprint cairosvg jinja2 pandas`).
  Optional: Inkscape, `playwright` for RGB preview/TTS sheets.

## Style — themes & a cover (cheap, do it by default)

Even a prototype should carry a basic sense of style so a playtester feels the vibe. It's free with our
vector pipeline, so **always apply a theme and generate a rough cover** — don't ship grey boxes.

- **Themes** live in `tools/cards/themes.py` (palette + type styling + per-suit colour & emblem). Pick
  one with `--theme` when rendering cards:
  `build_cards.py --csv <cards.csv> --out <build> --theme nautical --formats screentop`
  Ships with `clean`, `nautical`, `ember` (dark/dungeon), `parchment`, `cozy`. A card's `type` column
  maps to a suit colour+emblem; add/edit themes freely (one dict entry each).
- **Cover image** (procedural, themed, no assets): a placeholder box/title image for Screentop/TTS or a
  sell sheet:
  `build_cover.py --title "Beacon" --subtitle "Two keepers. One coast." --theme nautical --players 2 --time "20 min" --weight 1.8 --out build/cover.png`
- **Choose the theme to match the mood**, and record the choice (game-bible / manifest) so renders stay
  consistent. It's a *placeholder vibe* — flag that real art comes later (and mind the human-vs-AI-art
  stance in `knowledge/trends-2026.md`).

## Boards, tracks & tokens (`tools/boards/build_board.py`)

Cards aren't the whole game. Render the other 2D bits themed to match the deck:
- **Track** (tug-of-war / score / round track): `--type track --spaces N --title ... --left-label ...
  --right-label ...` → a strip with a centred start and directional end labels (e.g. Beacon's Tide).
- **Tokens** (markers/resources): `--type tokens --labels "Tide,1st" --shape circle|square|hex`
  (or `--from-csv label[,color][,qty]`) → a token sheet tiled for cutting.
- **Player mat / board**: `--type mat --spec mat.json` → a titled panel with labelled zones (copy
  `tools/boards/sample_mat.json`).
- **Player aid / quick-reference**: `--type aid --spec aid.json` → a themed reference sheet (auto-fits
  height) from `{title, subtitle, sections:[{heading, lines:[...]}]}`. Generate one for every game — a
  good aid is what makes a filler teachable in one pass.
All take `--theme` (shared with the cards) and output SVG→PNG/PDF. Upload them into Screentop/TTS as
image assets/tiles alongside the decks.

## Scratch vs committed renders (build/ vs exports/)
`build/` is **disposable scratch** (gitignored). Snapshot the **curated, shareable deliverables** (deck
sheets, cover, rulebook, board, tokens, player aid) into **`games/<slug>/exports/` (committed)** via the
game's `make.sh` — so the repo has viewable assets that stay fully reproducible from the data. Change
the data → re-run `make.sh` → commit the refreshed `exports/`.

## Print specs to bake in (from `knowledge/manufacturing-specs.md`)

- **Poker card = 63.5 × 88.9 mm = 750 × 1050 px @300 DPI** (trimmed); full-bleed ≈ 825 × 1125 px.
- **300 DPI**, **CMYK** for final print (RGB only for PnP/TTS).
- **~3 mm / ⅛″ bleed** every side; keep critical art/text **3–5 mm inside the cut**.
- Manufacturer output: **per-card PNGs** for The Game Crafter / MakePlayingCards; **multi-page PDF, one
  face per page** for PrintNinja / Panda. Always fetch the manufacturer's current dieline.

## Digital playtest export — Screentop.gg (default), TTS, Tabletopia

All three use the same **grid deck-sheet** format, so one render feeds any of them:

- Grid up to **10×7** (≤70 cards/sheet), **≤4096×4096 px** → per-card ceiling **≈409×585 px**.
  Downsample print-DPI art to fit; RGB is fine. Emit **one PNG per deck sheet + a standalone back PNG**.
- Build it: `python tools/cards/build_cards.py --csv <cards.csv> --out <build> --formats screentop`
  (produces `sheets/<slug>_sheet_N.png` + `sheets/<slug>_back.png`).

**Screentop.gg (studio default — free, browser, best for playtesting with a friend):**
- Free plan: 3 games, 32 MB/game. Create a game → add a **Deck** → upload the sheet as the deck **face**
  and the standalone **back** image → set columns/rows to the grid. Add a board/tokens as image assets.
- Share the **room link**; your friend joins in a browser (no install, works remote or in person).
- Always include a short **setup note** (which decks/pieces, starting layout) with the render.

**Tabletop Simulator (Steam, ~€20 each):** Objects → Components → Custom → Deck; set Width/Height to the
grid, Face = sheet, Back = standalone back. Richest/most tactile; each player needs a copy.
**Tabletopia (free tier, browser):** build components from the same images; more setup, nicer visuals.

## Print-and-play layout

- Prefer **gutterfold** (front+back on one sheet, fold on the dotted line, glue, then final-cut) for
  reliable duplex registration at home. Add crop/registration marks; keep fold lines faint.

## Workflow checklist

1. Confirm component data is clean and complete in `games/<slug>/components/`.
2. Pick template (SVG default; HTML for text-heavy/rulebook).
3. Render the **target** the task needs: TTS sheet (prototype), PNG (review), CMYK PDF (manufacture).
4. Verify the output opens and looks right; report the exact build command.
5. Never hand-edit `build/` — fix the data or template and re-render.

## Notes

- Keep data and template strictly separate — no data baked into templates.
- Iconography should be language-independent where possible (helps international print + rules).
- If a dep/tool is missing, produce what you can and tell the human exactly what to install.
