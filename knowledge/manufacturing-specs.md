# Manufacturing & Export Specs (Cards, Print-on-Demand, TTS)

Bake these constants into every 2D template. See the `bg-2d-components` skill for the pipeline.

## Card sizes (trimmed)

| Name | Inches | mm | px @300 DPI (trimmed) |
|------|--------|----|-----------------------|
| Poker (standard) | 2.5 × 3.5 | 63.5 × 88.9 | 750 × 1050 |
| Bridge | 2.25 × 3.5 | 57 × 89 | 675 × 1050 |
| Tarot | 2.75 × 4.75 | 70 × 120 | 825 × 1425 |
| Mini | 1.75 × 2.5 | 44 × 63 | 525 × 750 |
| Square (common) | 2.5 × 2.5 | 63.5 × 63.5 | 750 × 750 |

**Poker is the default.** Full-bleed poker ≈ 825 × 1125 px (add ~1/8″ bleed each side).

## Bleed, safe zone, colour, DPI (rules of thumb across manufacturers)

- **300 DPI** for print; **CMYK** for final manufacturing (RGB only for at-home PnP and TTS).
- **~3 mm / 1/8″ bleed** on every side (art must extend into it).
- **Keep critical art/text ~3–5 mm inside the cut** (safe zone).
- **Avoid thin uniform borders** — trim variance (a couple mm) makes them look off-centre.

## Manufacturer quick reference

| Manufacturer | Bleed | Safe zone | Colour / DPI | File format |
|---|---|---|---|---|
| **The Game Crafter** (POD, prototypes) | 1/8″ | 1/4″ | 300 DPI | **per-card PNG** faces; provides templates |
| **MakePlayingCards (MPC)** (POD cards) | 1/8″ | +1/8″ inside | 300 DPI | per-card images; poker min upload ~822×1122 |
| **PrintNinja** (offset, mid runs) | 3 mm / 0.125″ | text ≥5 mm from cut | **CMYK, 300 DPI** | **multi-page PDF, one card face per page** |
| **Panda Game Manufacturing** (full offset) | ~3 mm (confirm per-SKU dieline) | ~3–5 mm | CMYK, 300 DPI | PDF/dielines (request current spec) |

> Always request the manufacturer's **current dieline/template** before final files — specs differ per
> SKU and change over time.

## Digital-table export — **Screentop.gg (studio default), TTS, Tabletopia**

All three share the **grid deck-sheet** format below, so one render feeds any of them. **Screentop.gg**
is the studio default (free, browser, join-by-link — best for playtesting with a friend, remote or in
person; free plan = 3 games, 32 MB each). Export a deck **sheet** + a **standalone back** PNG and set
the deck's columns/rows to the grid.

- Grid up to **10×7** (70 cards per sheet image).
- **4096 × 4096 px texture cap** per sheet → practical per-card ceiling ≈ **409 × 585 px**.
- Downsample 300-DPI source to fit; readable and cuts file size ~95–99%.
- RGB is fine for TTS. One image = one deck sheet; the last cell is often the card back.

## Print-and-play (PnP) layout

- Modes: Standard, Standardbleed, **Gutterfold**, Gutterbleed. **Gutterfold** prints front+back on one
  sheet — cut loosely, fold on the dotted line, glue, final-cut → guaranteed front/back registration on
  home duplex printers.
- Include crop/registration marks; keep fold lines faint so auto-crop doesn't catch them.
- Tools: PnP PDF Creator (imposition/cut marks); this studio's `tools/cards` pipeline tiles sheets too.

## Barcodes

- Needed only for retail/distribution, not direct/convention sales. Official route = **GS1** (EAN-13
  Europe / UPC-A North America), annual fee. Major retailers/Amazon often require genuine GS1 numbers;
  cheap resold barcodes work for small shops but can be rejected — check your channel first.

*Sources: The Game Crafter, MakePlayingCards, PrintNinja, GS1 (verify current specs live).*
