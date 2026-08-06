# Travel Agents: Taiwan — Component Manifest (v3 · the vendor-courting engine)

Full bill of materials. **Data is the source of truth** (`components/*.csv|json`); renders regenerate via
`make.sh`. Quantities are for the **2-player base game** (3–4p deltas noted where they matter).

**Component types = 7** (within the raised cap of 8, `complexity-budget.json`):
board · Vendor cards · Mission cards · ingredient tokens · Buzz tokens · Event tiles · Character mats.
(Agent pawns + track markers are board bits, not a distinct type.)

| # | Component | Type | Qty | Size / material | Source file |
|---|-----------|------|----:|-----------------|-------------|
| 1 | **Taiwan map board** | board | 1 | ~A2 folded, 2 mm greyboard | `map.json` |
| 2 | **Vendor cards** | cards | 25 | 63.5×88.9 mm poker, 300 gsm linen | `vendors.csv` |
| 3 | **Mission cards** | cards | 9 | 63.5×88.9 mm poker (same stock as vendors) | `missions.csv` |
| 4 | **Ingredient tokens** | tokens | 144 | ~20 mm punchboard discs, dual-coded colour + 繁體 | `ingredients.csv` / `tokens.csv` |
| 5 | **Buzz tokens** | tokens | 50 | ~16 mm punchboard discs, purple + 讚 | `tokens.csv` |
| 6 | **Event tiles** | tiles | 11 | ~45 mm square punchboard | `events.csv` |
| 7 | **Character mats** | mats | 5 | ~120×90 mm mini-mat, 2 mm board | `characters.csv` |
| — | Agent pawns | board bits | 4 | wooden meeples (1 per player colour) | `tokens.csv` |
| — | Prestige markers | board bits | 4 | wooden cubes (gold) | `tokens.csv` |
| — | Reputation markers | board bits | 4 | wooden cubes (teal) | `tokens.csv` |
| — | Season timer marker | board bits | 1 | wooden disc (vermilion) | `tokens.csv` |

## Vendor deck (25) — tiered

| Tier | Fiction | Count | Ingredient cost | Buzz | Prestige | Rep | Perk |
|------|---------|------:|-----------------|-----:|---------:|----:|------|
| **T1 Stalls 攤** | humble street snacks | 11 | 2 (1 region) | 1 | 1 | +1 | its region discount icon |
| **T2 Eateries 小吃** | sit-down staples | 8 | 3 (usually 2 regions) | 2 | 3 | +2 | region icon + one of {Promote +1 Buzz · pantry-wild · +1 Rep/court} |
| **T3 Marquee 名店** | icons & banquets | 6 | 3 (1–2 regions) | 3–4 | 5–6 | +2/+3 | strong: wild icon · double icon · +2 Rep/court |

**Region-icon balance (whole deck):** North 7 · Central 6 · South 6 · East 6 — kept near-even despite
North carrying 4 specialties (design-doc guard #1). One vendor = one **real** locked dish (Tâi-lô primary
+ 繁體; Indigenous/place dishes use their own romanisation, not forced Hokkien). 2p deals **3 per tier**
face-up; refill from that tier's deck on each Court. (3p: 4/tier · 4p: 4–5/tier — see design-doc scaling.)

## Ingredient tokens (144) — the region↔ingredient web

| Ingredient | 繁體 | Region | Pool | Notes |
|-----------|------|--------|-----:|-------|
| Beef | 牛 | North | 12 | 牛肉麵, Tainan beef soup |
| Pork | 豬 | North | 18 | **workhorse — 10 vendors name it** |
| Chicken | 雞 | North | 12 | **NEW v3** — cutlet, karaage, turkey rice, maqaw soup |
| Egg | 蛋 | North | 10 | **NEW v3** — egg crepe, oyster omelette, breakfast 加蛋 |
| Tea | 茶 | Central | 12 | oolong, black tea, bubble tea |
| Tapioca pearls | 圓 | Central | 8 | **thin demand — 1 vendor** (bubble tea) |
| Oysters | 蚵 | South | 8 | **thin demand — 1 vendor** (oyster omelette) |
| Milkfish | 魚 | South | 8 | **thin demand — 1 vendor** (milkfish congee) |
| Rice | 米 | East | 16 | 7 vendors name it (bentos, congee, mochi) |
| Mountain greens | 菜 | East | 10 | fern/chayote/maqaw (Indigenous) |
| **Pantry** | 補 | Any | **∞** (print ~30) | UNLIMITED convenience store; never discounted |

Finite specialty pools ≈ 2× solo demand (grabbing the last forces a rival reroute). Pantry unlimited +
Buzz always-available = the two anti-stuck valves. Pools scale sub-linearly at 3–4p.

## Buzz tokens (50)
The second, fungible currency. Gained via **Promote** (2/action; 3 for the Influencer or a Buzz-income
perk). Spent alongside ingredients to Court — **never discounted** (the anti-runaway brake). Open supply.

## Event tiles (11) — salted into the region Markets, fire on refill
Boon-skewed (~8 boon / 3 hazard-or-shakeup), region-thematic, secular, tax-not-destroy. Setup: shuffle
~2–3 tiles into each region's Market supply; the "any/table-wide" tiles go into any region's supply.
Region tiles: South (Mango Season, Oyster Glut, Typhoon), Central (Bubble-Tea Festival, Plum Rains), East
(Bumper Harvest), + 5 table/any tiles (Tourist Season, Pop-Up Queue, Featured in the Guide, Word of Mouth,
Fully Booked). Typhoon salts into **both** coastal supplies (South + East).

## Mission cards (9) — secret signature tour, +7
Draw 3, secretly keep 1. Binary at scoring. Machine-target grammar (for the sim/linter; human rule in the
card's `effect`): `vendors_region:X>=n` · `vendors_all_regions` · `tier1_vendors>=n` · `tier3_vendors>=n`
· `vendors_total>=n` · `prestige_total>=n` · `marquee_plus_two_stalls`.

## Character mats (5) — public asymmetry (1 ability + 1 flaw)
Night-Market Auntie 阿姨 · Eager Rookie 菜鳥 · Retired Conductor 車長 · The Influencer 網紅 · Grizzled
Gourmand 老饕. **Table-watch flags** (validate at the human FTUE, not off the sim): Rookie (event-luck)
and Gourmand (pantry-wild) — both event-coupled kits the sim abstracts.

## Sensitivity rails honoured
Real dishes never mangled; **Traditional characters** only; Tâi-lô primary where the dish is Hokkien,
native romanisation for Indigenous/place dishes (not forced Hokkien). East draws on **distinct** Indigenous
peoples (Amis 阿美族 bamboo rice, Atayal 泰雅族 maqaw soup) — not a flattened "generic Indigenous". All
Chinese text + romanisation and Indigenous dish/people names route through the paid Taiwanese consultant +
native reviewer before art/print (→ `bg-publishing`).
