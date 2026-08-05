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
```

## 3D components

Driven live through the Blender / FreeCAD / OpenSCAD **MCP servers** rather than a script here — see the
`bg-3d-components` skill.
