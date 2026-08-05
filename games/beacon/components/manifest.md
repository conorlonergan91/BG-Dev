# Beacon — Component Manifest

Feeds prototyping (Screentop.gg) and, later, manufacturing. Cards are poker size (63.5 × 88.9 mm).

| Component | Qty | Size | Data / source | Notes |
|-----------|-----|------|---------------|-------|
| Ship cards | 24 | poker | `components/ships.csv` | 3 suits × values 1–4, two each |
| Signal cards | 12 | poker | `components/signals.csv` (qty 2 each) | two identical sets of 6 (0–5), one per player |
| Tide track | 1 | ~200 × 60 mm board strip | `build_board.py --type track` | 7 spaces, centre marked |
| Tide marker | 1 | token | `build_board.py --type tokens` | starts centre |
| First-Keeper token | 1 | token | `build_board.py --type tokens` | initiative marker |
| Harbour zones | 2 | play-area label | `build_board.py --type mat` (optional) | one per player; can be printed mats or just table space |
| Rules sheet + player aid | 1 | A5 / card | `design/rules-draft.md` | teach-in-play-order |

## Screentop.gg build
- Ships → one deck (24 cards) + shared back.
- Signals → one deck of 12 (or two 6-card decks, one per player).
- Tide track + tokens → image assets placed on the table; a marker piece to slide.
- Build sheets (theme = **nautical**):
  `python ../../tools/cards/build_cards.py --csv components/ships.csv --out build --theme nautical --formats screentop`
  (and again for `signals.csv`).
- Cover image: `python ../../tools/cards/build_cover.py --title "Beacon" --subtitle "Two keepers. One coast." --theme nautical --players 2 --time "20 min" --weight 1.8 --out build/cover.png`
- Tide track: `python ../../tools/boards/build_board.py --type track --spaces 7 --title "The Tide" --left-label "Keeper A harbour" --right-label "Keeper B harbour" --theme nautical --out build/tide-track.png`
- Tokens: `python ../../tools/boards/build_board.py --type tokens --labels "Tide,1st" --shape circle --theme nautical --out build/tokens.png`

## For manufacture (later)
36 poker cards total → a small-box card game. Add bleed (3 mm) and export CMYK per
`knowledge/manufacturing-specs.md`; a track/tokens punchboard; small box.
