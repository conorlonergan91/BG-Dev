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

## 3D components

Driven live through the Blender / FreeCAD / OpenSCAD **MCP servers** rather than a script here — see the
`bg-3d-components` skill.
