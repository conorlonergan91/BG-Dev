# Travel Agents: Taiwan — Component Manifest

Single source of truth for the physical bill of materials. Feeds prototyping (Screentop.gg) and, later,
manufacturing. **Data is the source; renders in `build/` are disposable** (regenerate with `./make.sh`).

Cards are poker size (63.5 × 88.9 mm). Region colours are **first-pass** from `identity.md`
(`night-market`) and are **not locked** — pending the `bg-access` colour-blind check. Every ingredient
type is **dual-coded** (colour **and** a non-colour channel: a distinct emblem/icon + a text/繁體 label),
never colour alone.

## Component types = 6  (exactly at the budget cap — `complexity-budget.json: max_component_types 6`)

| # | Component type | Qty | Size / material | Data / source | Notes |
|---|----------------|-----|-----------------|---------------|-------|
| 1 | **Map board** (Taiwan) | 1 | folding board, ~A3+ | `components/map.json` → `build_board.py --type mat` | 4 regions on a ring + HSR spine; **Grand Dossier** track + shared **score** track printed along the edge. One board absorbs three functions to save a type. |
| 2 | **Dish cards** | 24 | poker | `components/dishes.csv` → `build_cards.py` | 18 × 2-ingredient (3 VP) · 3 × 3-ingredient (4 VP) · 3 × Signature (5 VP). Recipe + VP + name (romanised **and** 繁體) + region tag. |
| 3 | **Assignment cards** | 15 | poker | `components/assignments.csv` → `build_cards.py` | Secret "Operation: ___" objectives, +7 VP each on completion. |
| 4 | **Ingredient tokens** | 120 | ~22 mm punch tokens / wood | `components/ingredients.csv` | **9 types:** 8 region specialties × 12 + **pantry** × 24. Open supply. Colour = region, emblem+label = the specific ingredient. |
| 5 | **Insider Tip tokens** | 30 | ~20 mm punch tokens | `components/tokens.csv` (`tip`) | The flexible Dead-drop / milestone reward. |
| 6 | **Agent pawns** | 4 | meeple / standee | `components/tokens.csv` (`pawnA–D`) | One per player, on the map. |
| — | *Grand Dossier marker + score markers* | 1 + 4 | cubes / discs | rendered on the board tracks | **Not a distinct type** — they ride the map board's printed tracks. |
| — | *Player aid* | 2 | card / landscape | `components/player-aid.json` → `build_board.py --type aid` | Reuses card stock — **not a new type**. One per player. |

**Budget status: 6 / 6 — held.** No headroom for a 7th type; new content must reuse these. (Per the CD's
note in `complexity-budget.json`, a 7th type is *allowed* if the game genuinely needs it, since cost is
recoverable — but nothing here needs one. Not flagging `bg-elegance`.)

## Ingredient supply (the region ↔ ingredient web)

| Region | Colour (first-pass) | Specialty 1 | Specialty 2 | Qty each |
|--------|--------------------|-------------|-------------|----------|
| North 北  | Lantern vermilion `#D64545` | Beef 牛肉 | Pork belly 五花肉 | 12 |
| Central 中 | Jade teal `#1F8A7A` | Tea 茶葉 | Tapioca pearls 粉圓 | 12 |
| South 南  | Golden amber `#E6A930` | Oysters 蚵仔 | Milkfish 虱目魚 | 12 |
| East 東   | Dusk indigo `#26324D` | Mountain rice 池上米 | Wild greens 野菜 | 12 |
| Anywhere  | Slate `#8A8F98` | **Pantry 補給** (fungible) | — | 24 |

→ 8 × 12 + 24 = **120 tokens.** (`bg-access` red/green flag: vermilion N vs jade-teal C, with amber S
between — the emblem + 繁體 label carry the dual-code; expect to nudge hues in the render pass.)

## Dish deck at a glance (24)

- **By VP:** 18 × 3 VP (2-ingredient) · 3 × 4 VP (3-ingredient, all cross-region) · 3 × 5 VP (Signature, 3 regions).
- **Specialty coverage** (appearances across the deck): beef 4 · pork 6 · tea 4 · pearls 3 · oysters 4 ·
  milkfish 5 · rice 5 · greens 4.  (Pearls sits at 3 — see balance notes.)
- **Cross-region dishes:** 6 of 24 (~25%) — the 3 value-4 (bento / braised pork / milkfish rice) + 3 Signatures.
- **Pantry appears in 19 of 24 dishes** (each dish uses at most 1 pantry).

## Screentop.gg build

Run **`./make.sh`** from `games/travel-agents/` — it regenerates everything into `build/` and snapshots
deliverables into `exports/`. Individual steps (theme `night-market` **must be added to
`tools/cards/themes.py` first** — a prototyper task; until then it falls back to the `clean` theme):

- Dishes deck: `build_cards.py --csv components/dishes.csv --out build --theme night-market --formats png screentop`
- Assignments deck: `build_cards.py --csv components/assignments.csv --out build --theme night-market --formats png screentop`
- Map board: `build_board.py --type mat --spec components/map.json --theme night-market --out build/map.png`
- Grand Dossier track (2p, 16 spaces): `build_board.py --type track --spaces 16 --title "Grand Dossier" ...`
- Ingredient / Tip / pawn token key: `build_board.py --type tokens --from-csv components/tokens.csv ...`
- Player aid: `build_board.py --type aid --spec components/player-aid.json ...`
- Cover + rulebook: `build_cover.py` / `build_rulebook.py` (see `make.sh`).

> `components/ingredients.csv` is authoritative for **per-type supply counts**; `components/tokens.csv` is
> a one-swatch-per-type **render key** (qty 1 each) for the prototype token sheet — do not read counts from it.

## For manufacture (later)

39 poker cards (24 dishes + 15 assignments) + 2 player aids · 120 ingredient + 30 tip punch tokens ·
4 pawns · 1 folding board · marker cubes/discs → a small-to-medium box. Add 3 mm bleed and export CMYK per
`knowledge/manufacturing-specs.md`. Owned onward by `bg-production`.
