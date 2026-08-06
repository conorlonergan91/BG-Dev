# Travel Agents: Taiwan — Component Manifest (v3.1 · movement-rebalanced + The Poach)

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
| 4 | **Ingredient tokens** | tokens | 143 | ~20 mm punchboard discs, dual-coded colour + 繁體 | `ingredients.csv` / `tokens.csv` |
| 5 | **Buzz tokens** | tokens | 50 | ~16 mm punchboard discs, purple + 讚 | `tokens.csv` |
| 6 | **Event tiles** | tiles | 13 | ~45 mm square punchboard | `events.csv` |
| 7 | **Character mats** | mats | 5 | ~120×90 mm mini-mat, 2 mm board | `characters.csv` |
| — | Agent pawns | board bits | 4 | wooden meeples (1 per player colour) | `tokens.csv` |
| — | Prestige markers | board bits | 4 | wooden cubes (gold) | `tokens.csv` |
| — | Reputation markers | board bits | 4 | wooden cubes (teal) | `tokens.csv` |
| — | Season timer marker | board bits | 1 | wooden disc (vermilion) | `tokens.csv` |

## Vendor deck (25) — tiered · **v3.1 movement re-cost**

| Tier | Fiction | Count | Ingredient cost | Buzz | Prestige | Rep | Perk |
|------|---------|------:|-----------------|-----:|---------:|----:|------|
| **T1 Stalls 攤** | humble street snacks | 11 | 2 (1 region) | 1 | 1 | +1 | its region discount icon |
| **T2 Eateries 小吃** | sit-down staples | 8 | 3 (usually 2 regions) | 2 | 3 | +2 | region icon + one of {Promote +1 Buzz · pantry-wild · +1 Rep/court} |
| **T3 Marquee 名店** | icons & banquets | 6 | 3 (1–2 regions) | 3–4 | 5–6 | +2/+3 | strong: wild icon · double icon · +2 Rep/court |

**Region-icon balance (whole deck):** North 7 · Central 6 · South 6 · East 6 — unchanged. Because **every
vendor is now anchored in its own icon-region** (v3.1), the icon balance *is* the primary sourcing-demand
distribution: **N 28% · C 24% · S 24% · E 24%** (South up from ~6%). One vendor = one **real** locked dish
(Tâi-lô primary + 繁體; Indigenous/place dishes use their own romanisation). 2p deals **3 per tier**
face-up; refill from that tier's deck on each Court. (3p: 4/tier · 4p: 4–5/tier — see design-doc scaling.)

**Per-specialty demand (vendors naming each — v3.1 target hit):** pork 5 · chicken 4 · beef 2 · egg 3 (N) ·
tea 5 · pearls 3 (C) · oysters 4 · milkfish 3 (S) · rice 4 · greens 4 (E). Workhorses capped (pork/rice ≤5);
every specialty ≥3 vendors except **beef 2** (deliberately marquee-held/premium). ~8 vendors (≈32%) carry a
**cross-region link** to force inter-region trips. **`connect-flag`** tagged vendors (V08 爌肉飯, V08b 肉圓,
V09 火雞肉飯, V11 花蓮扁食, V17 太陽餅, V19 擔仔麵, V20 蝦捲, V24 牛肉湯) carry an in-region token framed as
*"the regional leg/connection you bring"* (not a literal added ingredient) — the anchor stays true to the
dish, only the framed token is the connection → **route the framing wording past the paid consultant**.

## Ingredient tokens (143) — the region↔ingredient web

| Ingredient | 繁體 | Region | Pool | Notes |
|-----------|------|--------|-----:|-------|
| Beef | 牛 | North | 11 | 牛肉麵, Tainan beef soup (marquee-held) |
| Pork | 豬 | North | 12 | comfort-food protein — **capped at 5 vendors** (was 10) |
| Chicken | 雞 | North | 11 | cutlet, karaage, turkey rice, maqaw soup |
| Egg | 蛋 | North | 11 | egg crepe, oyster omelette, breakfast 加蛋 |
| Tea | 茶 | Central | 12 | oolong, black tea, bubble tea — 5 vendors |
| Tapioca pearls | 圓 | Central | 11 | **now 3 vendors** (bubble tea, Dongding, ba-wan) |
| Oysters | 蚵 | South | 11 | **now 4 vendors** (Tainan/Chiayi 東石 coast) |
| Milkfish | 魚 | South | 11 | **now 3 vendors** (congee, shrimp roll, beef soup) |
| Rice | 米 | East | 12 | **capped at 4 vendors** (was 7) — bento, bamboo rice, mochi |
| Mountain greens | 菜 | East | 11 | fern/chayote/maqaw (Indigenous) — 4 vendors |
| **Pantry** | 補 | Any | **∞** (print ~30) | UNLIMITED convenience store; never discounted |

Pools **flattened to even scarcity** (v3.1): every specialty now 11–12 tokens (was 8–18), ≈ 2× per-region
solo demand — no specialty trivially abundant or impossibly scarce. Grabbing the last still forces a rival
reroute. Pantry unlimited + Buzz always-available = the two anti-stuck valves. Pools scale sub-linearly at 3–4p.

## Buzz tokens (50)
The second, fungible currency. Gained via **Promote** (2/action; 3 for the Influencer or a Buzz-income
perk). Spent alongside ingredients to Court — **never discounted** (the anti-runaway brake). Open supply.

## Event tiles (13) — salted into the region Markets, fire on refill · **v3.1 comedy rework**
Boon-skewed **~60/40** (8 boon / 4 hazard + 1 shakeup), region-thematic, **secular**, tax-not-destroy.
Setup: shuffle ~2–3 tiles into each region's Market supply; "any/table-wide" tiles go into any region's
supply. Region tiles: South (Mango Season), Central (Bubble-Tea Festival, Plum Rains), North (Scooter
Gridlock), coastal (Typhoon Day → salts into **both** South + East) + 8 any/table tiles (Aunty Insists,
4 a.m. Convenience Store, Stinky-Tofu Dare, The 3:47 to Zuoying, Queue That Ate the Block, Food Blogger's
Big Break, Sold Out, Fully Booked). **Two special payloads:** *Stinky-Tofu Dare* (push-your-luck: reveal
the top supply tile — specialty = free + 1 Buzz, event = resolve it too, decline = 1 Buzz); *Typhoon Day*
(catch-up: coastal washout-refill + every non-leader on the Prestige track takes 2 Buzz; tie-for-lead → all
benefit). Reserve swap-ins (not in the 13): Oyster Glut (S boon), Bumper Harvest (E boon).

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
