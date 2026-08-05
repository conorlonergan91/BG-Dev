---
name: bg-2d-components
description: Generate 2D board game components — cards, tiles, player boards, game boards, tokens, rulebook pages — from component data. Use whenever you need to render or lay out printable/playable 2D parts. Covers the code-native pipeline (data CSV/JSON → SVG/HTML template → print-ready PDF / PNG / Tabletop Simulator deck sheets), manufacturer specs (sizes, bleed, DPI), print-and-play layout, and when to use the Figma MCP for collaborative visual layout.
---

# 2D component pipeline

The studio's 2D approach is **code-native and deterministic**: component **data** is the source of
truth; templates render it to print-ready and TTS-ready output. Everything is plain text, diffable,
and re-runnable — regenerate on every data change; never hand-edit renders.

```
data (CSV/JSON)  →  template (SVG or HTML/CSS)  →  render  →  PDF (print) / PNG / TTS deck sheet
```

## When to use what

- **Cards / tokens / tiles (batch, data-driven):** the code pipeline below. This is the default.
- **Boards / player mats / rulebook (visual, human-in-the-loop):** the code pipeline for a
  data-driven board, **or** the **Figma MCP** when the human wants to art-direct layout interactively
  (Figma is the only production-grade design MCP — good for boards/rulebooks; still export + treat as
  final art). See `CLAUDE.md` for the Figma endpoint.
- **Quick prototype to play now:** render TTS deck sheets (see below) — this is the fast path.

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

## Print specs to bake in (from `knowledge/manufacturing-specs.md`)

- **Poker card = 63.5 × 88.9 mm = 750 × 1050 px @300 DPI** (trimmed); full-bleed ≈ 825 × 1125 px.
- **300 DPI**, **CMYK** for final print (RGB only for PnP/TTS).
- **~3 mm / ⅛″ bleed** every side; keep critical art/text **3–5 mm inside the cut**.
- Manufacturer output: **per-card PNGs** for The Game Crafter / MakePlayingCards; **multi-page PDF, one
  face per page** for PrintNinja / Panda. Always fetch the manufacturer's current dieline.

## Tabletop Simulator export (default prototype target)

- Deck **sheet grid up to 10×7** (≤70 cards/sheet), **≤4096×4096 px** → per-card ceiling **≈409×585 px**.
- Downsample print-DPI art to fit; last cell of the sheet is typically the shared card **back**.
- Output one PNG per deck sheet + a short setup note (which decks/objects to load). RGB is fine.

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
