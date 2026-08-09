# Travel Agents: Taiwan — Component Manifest (V7)

> The physical bill of materials for the **V7** multiplayer (3–6 players, area-majority) prototype.
> **Data is the source of truth** (`components/*.csv|json`); renders in `build/` regenerate via `make.sh`
> and snapshot to `exports/`. Counts below are the **base card set**; the **quantity-scaling levers**
> (Followers pool, Bookings deck depth, ingredient market depth, face-up vendor slots) scale with player
> count per the tables in `map.json` — no new component *type* is added by scaling. Card sizes/materials
> feed prototyping + manufacturing (see `knowledge/manufacturing-specs.md`).

## Cards

| Component | File | Cards | Size | Notes |
|---|---|---:|---|---|
| **Vendor deck** | `vendors.csv` | **24** | poker 63.5×88.9 mm | Per region, split by `phase` into a DAY deck + a NIGHT deck; drinks mixed in as low-value vendors. Face = **Draw (人氣) attribute + region icon-or-none** (vendors DON'T score). New `trending` column marks which vendors can receive a **Trending** marker (20 yes; the 4 printed ★ apex are `no` — a printed apex is the permanent marquee, distinct from the dynamic Trending). |
| **Bookings deck** | `bookings.csv` | **45** | poker | The **SOLE scoring vector** (was "Tour Tickets"/"missions"). 繁體 **開團** *kāi-tuán*. DAY 20 + NIGHT 25 = **44 distinct patterns / 45 physical cards** (遍地開花 printed once per deck). **The Bookings deck IS the deck-driven clock** — DAY-deck-out → 黃昏 DUSK, NIGHT-deck-out → 末班車 LAST TRAIN, via **2 seeded boundary cards** (see below). Judged into COMPLETED 成團 / CANCELLED 取消 piles. |
| **Booking boundary cards** | (seed into `bookings.csv` decks at print) | **2** | poker | **黃昏 DUSK** at the bottom of the DAY deck; **末班車 LAST TRAIN** at the bottom of the NIGHT deck. Self-announcing clock. *(Currently a rules/print instruction; add as 2 rows or a print-seed note in the deck build — flagged to bg-infodesign.)* |
| **Ingredient / food market cards** | `ingredients.csv` | **62** | poker (or mini) | **Ingredients are CARDS now** (the v6.4 model change), drawn on a Visit / Convenience Store / (媽寶) Travel. 5 types — 豬肉 pork · 茶 tea · 海鮮 seafood · 米 rice · 糖 sugar — per-region day/night decks; renewable (reshuffle on empty). **Pictorial** (a drawn ingredient, no CJK reliance) → bg-infodesign / bg-access. |
| **Event cards** | `events.csv` | **27** | poker (or mini) | Scoped ⦿/⬢/➤ hazards/boons (tax-not-destroy) + the **Followers-max economy** (3 dial-gain, 2 dial-drop 負評/出包) + the **Trending** event (爆紅 "Gone Viral" → drop a Trending marker; winner gains +1 Followers-max) + **2 table-wide 排班保養 "Scheduled Maintenance"** (island-wide banner). Shuffled into the matching region+phase ingredient deck. |
| **Character boards** | `characters.csv` | **6** | landscape mat | 里長伯 The Old Councillor · 媽寶 The Homebody · 大胃王 The Big Eater · 網紅 The Influencer · 大哥 The Big Brother · 阿嬤 The Globetrotter. Ability + flaw are **icon-only** on the board (rulebook carries the words); each row carries `ability_code` + `flaw_code`. |

**Total base cards: 158** (24 + 45 + 62 + 27) + **6 character boards** + **2 boundary cards**.

### Recipe-chip glyph key (render helper, NOT a physical component)
`recipe-glyphs.csv` maps the 5 ingredient ids → 繁體 label + colour for the vendor recipe chips. It exists
because the ingredient **tokens** were dropped (ingredients are cards); it is passed to the card renderer via
`--tokens-csv` and is **never printed as a component**.

### Vendor deck — the CD-4 soft night-cost curve (validated, carried from v6.3.1)
`{N:1}` = 1 pork · `K` = the common (sugar) · `→X` = cross-region pull · ★ = printed apex (no icon).

| Region | Face-up (4p) | Day vendors (cost) | Night vendors (cost) | Apex ★ |
|---|:--:|---|---|---|
| North 北 (pork) | **2** | 肉包 {N:1}, 蛋餅 {N:1}, 豆漿◇{K:1} | 胡椒餅 {N:2,C:1}→C, 牛肉麵 {N:2,S:1}→S, ★大香腸 {N:3,S:1}→S, 珍奶◇{K:1} | 大香腸 (Draw 7, cost 4) |
| Central 中 (tea) | 2 | 肉圓 {C:1}, 麵線 {C:1}, 珍珠奶茶◇{K:1}, 冬瓜茶◇{K:1} | 大腸包小腸 {C:2,S:1}→S, ★逢甲名物 {C:2,S:2}→S | 逢甲名物 (Draw 6, cost 4) |
| South 南 (seafood) | 2 | 虱目魚粥 {S:1}, 碗粿 {S:1}, 木瓜牛奶◇{K:1} | 蚵仔煎 {S:2,N:1}→N, 棺材板 {S:2,E:1}→E, ★擔仔麵 {S:3,E:1}→E | 擔仔麵 (Draw 7, cost 4) |
| East 東 (rice) | 1 | 竹筒飯 {E:2}, 米糕 {E:1}, 洛神花茶◇{K:1} | 麻糬 {E:2,C:1}→C, ★石板烤肉 {E:3,N:2}→N | **石板烤肉 (Draw 8, cost 5 — TOP)** |

Counts: **N 7 · C 6 · S 6 · E 5 = 24 vendors** (◇ = 6 drinks; 4 apex ★, all night, no icon). Every night
marquee is cross-region (needs a two-region engine). *(Face-up counts shown at 4p; per-count slots in `map.json`.)*

## Tokens, markers & the dial (`tokens.csv`)

| Component | Qty (max 6p) | Notes |
|---|---:|---|
| **Followers** 粉 | **60** | Committed public on vendors; capped by your Followers-max dial. Only ever in supply or on a vendor. (Table pool scales ≈ round(24·(1+0.375·(N−2))) → 33/42/51/60.) |
| **Followers-max dial** | **6** (1/player) | The per-player live ceiling on total committed Followers (start 2 · 網紅 4). Earned by Travel + events; the lost-war sink drops it (−1 day / −2 night, floor = start). **Replaces the old Reach marker/track.** NOT a score. |
| **Trending marker** 紅 | **4** | The DYNAMIC 爆紅 going-viral marker (Gone Viral drops it; winning that vendor grants +1 Followers-max). **Renamed from the ★ Star token.** Distinct from the printed ★ apex. |
| **Rave-Review / Tours-Completed marker** 團 | **6** (1/player) | Per-player; hosts the 好評 boons at your 2nd & 4th completed tour. |
| **HSR-closed marker** 停 | **1** | Sits on the 停 HSR slot while a Scheduled Maintenance card is active (N↔S closed). |
| **COMPLETED 成團 pile marker** | **6** | Win-pile area marker, per player. |
| **CANCELLED 取消 pile marker** | **6** | Lose-pile area marker, per player. |
| **Agent pawns** | **6** | One per agent on the region ring — all start in **Taipei (North hub)**. Scaled 4 → 6 for the 3–6p roster. |

**DROPPED from tokens.csv (V7):** the 5 ingredient tokens (pork/tea/seafood/rice/sugar — ingredients are
CARDS now → `ingredients.csv`; the render glyph key moved to `recipe-glyphs.csv`) and the **vendor-claims
clock marker** (the clock is deck-driven now). The old **Reach marker** became the **Followers-max dial**;
the old **★ Star token** became the **Trending marker**.

## Board & aid

| Component | File / source | Qty | Notes |
|---|---|---:|---|
| **Region-ring board** | `map.json` | 1 | **Neutral shared N-player** board (no across-the-table mirror): 4-region diamond, ring + HSR spine, phase-split face-up vendor slots, **Taipei common-start hub**, 停 Scheduled-Maintenance slot. **No score/clock track** (deck-driven clock). RENDER REBUILD owed → bg-infodesign. |
| **Player aid** | `player-aid.json` | 1–2 | Stripped to the **"On your turn"** actions only (the rest → rulebook). |

**No score/VP track, no clock track** — scoring is the Bookings tally (§ rules), and the clock is the
Booking deck itself.

## Per-count quantity scaling (data in `map.json`)
| | 3p | 4p | 5p | 6p |
|---|---:|---:|---:|---:|
| **Bookings — DAY deck** (3·(N+1)) | 12 | 15 | 18 | 21 |
| **Bookings — NIGHT deck** (4·(N+1)) | 16 | 20 | 24 | 28 |
| **Followers pool** | 33 | 42 | 51 | 60 |
| **Face-up vendor slots** N/C/S/E | 2/2/1/1 | 2/2/2/1 | 2/2/2/2 | 3/2/2/2 |

The 45-card Bookings set covers the deepest single-phase draw; at higher counts the common/easy patterns are
duplicated to keep the shared face-up row refilling (a print-quantity step, not new patterns). The DAY/NIGHT
deck sizes above are the **clock** — seed the 黃昏 / 末班車 boundary card below each.

## Component-type count (complexity budget: max 8)
Cards (vendors / bookings / ingredient-food / events — one card *type*), character boards, region board,
tokens (Followers / dial / Trending / pile+Rave markers / 停 / pawns). **7/8** — the Followers-max **dial is
the old Reach dial** (no new type); boundary cards live inside the Bookings deck. (bg-elegance owns the check.)

## Notes / flags
- **TICKETS-ONLY scoring:** vendors give NO points; score = Σ COMPLETED 成團 value − Σ floor(value/2) CANCELLED 取消.
- **Deck-driven clock:** the Bookings deck IS the clock — needs the 2 seeded boundary cards (黃昏 / 末班車) at print.
- **Ingredients are pictorial CARDS** (5 types) → bg-infodesign (art) + bg-access (distinguishable by picture + shape, not colour alone).
- **6 character boards, icon-only ability/flaw** → bg-infodesign owes glyphs for the new codes `start_max_4` (Influencer), `win_ties` (Big Brother), `travel_anywhere` (Globetrotter). Existing glyphs: `discount_home`, `away_tax`, `travel_draw_left`, `visit_keep3`, `hazard_twice_visit`, `goes_last`, `none`.
- **East 石板烤肉 (Indigenous-forward):** #1 pre-art item — paid Taiwanese/Indigenous consultant sign-off on dish + naming + framing BEFORE art.
- **繁體 + Tâi-lô** on every vendor/dish; romanisations first-pass → native reviewer (incl. 開團 blessing) to confirm.
- **BINDING wording rail:** frame any Followers/dial loss as *the crowd ebbing / drifting to a rival's stall*, never a bare "−N".
- **Paid Taiwanese cultural + language consultant before art/print is STILL required** (not discharged by this pass).
