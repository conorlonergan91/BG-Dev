# Travel Agents: Taiwan Food Tour — Component Manifest

> The physical bill of materials for the 3–6-player area-majority prototype.
> **Data is the source of truth** (`components/*.csv|json`); renders in `build/` regenerate via `make.sh`
> and snapshot to `exports/`. Card counts below are the base set; the **quantity-scaling levers** (Bookings
> deck depth, face-up vendor slots, event-deck mix) scale with player count per the tables in `map.json` — no
> new component *type* is added by scaling. Card sizes/materials feed prototyping + manufacturing (see
> `knowledge/manufacturing-specs.md`). Names English-first per `names.md`; mechanics per `game-bible.md`.
> _Stamp: V7-M · 2026-08-12._

## Cards

| Component | File | Distinct | Physical | Size | Notes |
|---|---|---:|---:|---|---|
| **Vendor cards** | `vendors.csv` | **30** | 30 | poker 63.5×88.9 mm | Per region, split by `phase` into a **DAY** set (cheap low-VP engine-seeds) + a **NIGHT** set (scarce expensive trophies); drinks mixed in as low-value stalls. Face = **recipe (`ingredient_cost`) + `min_followers` crowd-floor + `vp` + region icon** (day food only). The `trending` flag marks which vendors can receive a **Trending** marker (**26** yes; the 4 ★ apex are `no` — the printed apex is the permanent marquee, distinct from the dynamic Trending). |
| **Booking cards** | `bookings.csv` | **45** | 45 | poker | The tour objectives (開團 *kāi-tuán*). Split **6 day (☀) / 8 night (☾) / 31 any-time (⟳)**; value **3–11**. Drawn into a face-up row + **Pot-Luck (隨緣開團)** blind draw; hand-limit 3, cancel-to-claim. Judged into COMPLETED 成團 / CANCELLED 取消 piles. A per-count `counts` tag sets the deck at setup (3p ≈ 38 rows, 4–6p all 45). **Not the clock** and **not reshuffled** — pure finite tour-supply. |
| **Ingredient market cards** | `ingredients.csv` | **16** | 62 | poker (or mini) | The **six generic categories**, each card art a **MIX** of real examples: **肉 Meat** (North sig) · **茶 Tea** (Central sig) · **海鮮 Seafood** (South sig) · **糧 Staples** (East sig) · **糖 Sugar** (common Central & South) · **菜 Vegetables** (common North & East). Dealt as a signature + common per region×phase market deck (8 decks × 2 rows). **Renewable** (reshuffle on empty). **Pictorial** (distinguishable by picture + shape, not colour alone) → bg-infodesign / bg-access. *(Sugar cards currently label 糖珠 Sugar & Pearls in the data — reconciliation pending a CD call; see flags.)* |
| **Event cards** | `events.csv` | **54** | 54 | poker (or mini) | The **VERB · SCOPE · DURATION** framework: scoped (⦿ self · ✦ rival · ⬢ region · ➤ neighbour · ▦ board) hazards/boons (tax-not-destroy), the **follower economy** (grow / return-to-supply), the **Trending** drop (爆紅 "Gone Viral" → drop a Trending marker; winner grows 1 follower), **2 tour catch-up boons** (重新開團 / 有人接手), and **2 table-wide 排班保養 Scheduled Maintenance** banners (island-wide, HSR down for a round). Salted into the matching region+phase market deck; a per-count subset is dealt each game (`map.json → event_deck_mix`). |
| **Character mats** | `characters.csv` | **6** | 6 | landscape mat | The Old Councillor (里長伯) · The Homebody (媽寶) · The Big Eater (大胃王) · The Influencer (網紅) · The Big Boss (老大) · The Globetrotter (阿嬤). Ability + flaw are **icon-only** on the mat (rulebook carries the words); each row carries `ability_code` + `flaw_code`, plus `max` (pool size — 6; the Influencer 8) and `start_meeples` (on-board at setup: 2). Printed tri-lingual (English · 繁體 · Tâi-lô). |

**Base card totals: 145 distinct card faces / 191 physical cards** (vendors 30 + bookings 45 + ingredients 16→62 + events 54), **+ 6 character mats**.

### Recipe-chip glyph key (render helper, NOT a physical component)
`recipe-glyphs.csv` maps the ingredient ids → 繁體 label + colour for the vendor recipe chips. Passed to the
card renderer via `--tokens-csv`; **never printed as a component**. *(`*-split.csv` variants belong to the
parked 8-type-taxonomy branch — flag-gated, not in the ship config.)*

### Vendor deck — regions, phases & apex
30 vendors across four regions; **18 day + 12 night**. Day **food** seeds carry their region's discount icon
(they ARE the engine); day **drinks** (◇) and **all night** vendors (trophies + ★ apex) carry **no icon**.
One ★ apex per region, all in the night set. Night trophies are expensive (cost 5–9) and high-VP.

| Region | Day (5/5/4/4) | Night | Apex ★ (night, no-icon) |
|---|---|---|---|
| **North 北** (10) | Pork Bao, Egg Crepe, Soy Milk◇, Rice Ball, Gua Bao | Pepper Bun, ★Beef Noodle, Big Sausage, Bubble Tea◇, Bubble Tea◇ (dup) | **★ Beef Noodle (牛肉麵)** |
| **Central 中** (7) | Ba-wan, Misua, Bubble Tea◇, Wintermelon Tea◇, Thick Noodle Soup | Sausage-in-Sausage, ★Fengjia Signature | **★ Fengjia Signature (逢甲名物)** |
| **South 南** (7) | Milkfish Congee, Rice Bowl Cake, Papaya Milk◇, Oyster Omelette | Chiayi Turkey Rice, Coffin Bread, ★Tan-tsú-mī | **★ Tan-tsú-mī (擔仔麵)** |
| **East 東** (6) | Bamboo-Tube Rice, Rice Cake, Roselle Tea◇, Scallion Pancake | Mochi, ★Stone-Slab BBQ | **★ Stone-Slab BBQ (石板烤肉)** — top apex |

Counts: **N 10 · C 7 · S 7 · E 6 = 30** (◇ = 7 drinks; 4 apex ★). The night set is **11 unique + 1
duplicate** (a second cheap 珍奶 Bubble Tea clock-filler). Most night dishes are cross-region (a two-region
engine). `vp = ingredient_cost + min_followers − 2` (range **0–11** per `game-bible.md`).

## Tokens, markers & follower meeples (`tokens.csv`)

Followers are physical, colour-coded **meeples** — a fixed per-colour pool per player (component count enforces
the ceiling; no dial tracking). A follower is only ever in your **supply**, on **your board**, or committed
**on a stall**; win a contested stall → your followers come home to your board, lose it → back to **your own**
supply (they never join the winner).

| Component | Qty (max 6p) | Notes |
|---|---:|---|
| **Follower meeples** 粉 | **48** (6 colours × 8) | Per-player, per-colour pool — **not** a shared table pool. 8 per colour so any colour can field the Influencer's pool of 8; the other five characters use 6. Colours match the agent pawns (A–F). Setup: 2 on your board (`start_meeples`), the rest in your colour's supply. |
| **Trending marker** 紅 | **4** | The dynamic 爆紅 going-viral marker (Gone Viral drops it; whoever WINS that vendor grows 1 follower). Distinct from the printed ★ apex. |
| **Rave-Review / Tours-Completed marker** 團 | **6** (1/player) | Per-player; hosts the 好評 boons at your 2nd & 4th completed tour. |
| **HSR-closed marker** 停 | **1** | Sits on the 停 HSR slot while a Scheduled Maintenance card is active (N↔S closed). |
| **COMPLETED 成團 pile marker** 成 | **6** | Win-pile area marker, per player. |
| **CANCELLED 取消 pile marker** 取 | **6** | Lose-pile area marker, per player. |
| **Agent pawns** | **6** | One per agent on the region ring — all start in **Taipei (North hub)**. |
| **Closing-Time die** 關 | **1** | The game's only die — a **custom d6**: 4 region faces **North / Central / South / East** (each drawn with that region's colour + emblem + 繁體 — dual-coded, CVD-safe) + **2 BLANK** faces (a 1/3 reprieve). The vendor clock's forcing function: a region face closes that region's oldest face-up stall (contested or not — committed followers come home, no penalty). Day cadence: roll after L rounds (L=2 at 3p, L=3 at 4–6p); night cadence: every round. **bg-architect flag:** a custom-printed d6 is a real COGS line vs stock — fallback is a stock d6 + a region↔number key (1–4 = N/C/S/E, 5–6 = BLANK). |
| **Closing-Time track marker** 關 | **1** | Sits on the **3-space round track (1 · 2 · 3)** printed on the board's clock band; advance 1 per round, then roll the die per the cadence and reset. The track prints on the board (`map.json` art), so only the marker is a punch-out token. |

## Board & aid

| Component | File / source | Qty | Notes |
|---|---|---:|---|
| **Region-ring board** | `map.json` | 1 | One **neutral shared 3–6-player** board readable from any seat: 4-region diamond (北 red triangle · 中 teal diamond · 東 dark-blue square · 南 gold circle), ring + HSR spine (N↔S), phase-split face-up vendor slots + market decks, **Taipei common-start hub**, 停 Scheduled-Maintenance HSR slot, the **Closing-Time 3-round clock band**, and per-colour follower supply trays. |
| **Player aid** | `player-aid.json` | 6 (1/player) | Poker-card-sized, **double-sided**: a shared FRONT listing the six turn actions (label + one-line reminder; full teach → rulebook), and one BACK per character with that agent's ability + flaw in brief, tinted in the character's colour (漢字 + Tâi-lô + catchphrase). Pulls display fields from `characters.csv` so it can't drift. |

## Per-count quantity scaling (data in `map.json`)
| | 3p | 4p | 5p | 6p |
|---|---:|---:|---:|---:|
| **Bookings — DAY deck** (3·(N+1)) | 12 | 15 | 18 | 21 |
| **Bookings — NIGHT deck** (4·(N+1)) | 16 | 20 | 24 | 28 |
| **Followers per colour** (`max`) | 6 · Influencer 8 | 6 · Influencer 8 | 6 · Influencer 8 | 6 · Influencer 8 |
| **Face-up vendor slots** N/C/S/E | 1/1/1/1 | 1/1/1/1 | 1/1/2/1 | 2/1/2/1 |
| **Events dealt per deck** (day / night) | 1 / 2 | 2 / 3 | 2 / 3 | 3 / 4 |

The follower pool is a **fixed per-colour pool = your character's `max`** (a physical component ceiling, not a
shared table pool). The FULL 30-vendor pool (18 day / 12 night) is used at every count — **no per-count pool
subset**; only the face-up slots scale (thematically: +1 South @5p → +1 North @6p, East kept thinnest), with
**slow / per-round** refill — the load-bearing lever that forces the contested crowd-fight. The 3p Bookings
deck sets aside the 7 HEAVY ≥4-claim tours (a `counts` tag) → ~38 rows; 4–6p use all 45. The DAY/NIGHT vendor
pools are the clock (18 day → 黃昏 DUSK; 12 night → 末班車 LAST TRAIN), paced by the Closing-Time die.

## Component-type count (complexity budget: max 8)
Cards (vendors / bookings / ingredients / events — one card *type*), character mats, region board, tokens
(follower meeples / Trending / pile + Rave markers / 停 / pawns / die + track marker). Reported **8/8** on the
mono ship config. (bg-elegance owns the gauge.)

## Notes / flags
- **Two-track scoring:** score = Σ printed `vp` on won vendors (0–11 each) **+** Σ full value of COMPLETED 成團
  tours (3–11 each) **−** 1 per CANCELLED 取消 Booking (flat −1). Followers score nothing.
- **The clock** is **vendor depletion + the Closing-Time die** (18 day → DUSK; 12 night → LAST TRAIN) — **not**
  the Booking decks, and **no boundary cards** are seeded.
- **Ingredients are pictorial CARDS** (6 categories) → bg-infodesign (art) + bg-access (distinguishable by
  picture + shape, not colour alone).
- **Character mats, icon-only ability/flaw** — glyphs owed by bg-infodesign for `favours_home_draw`,
  `deep_pool`, `margin_win`; the board renderer's presentation pass must render collected-follower pools +
  per-colour supply trays (no abstract dial face).
- **East Stone-Slab BBQ (石板烤肉) + Bamboo-Tube Rice (竹筒飯)** are Indigenous-forward → **paid Taiwanese/
  Indigenous consultant** sign-off on dish + naming + framing BEFORE art (#1 pre-art item).
- **繁體 + Tâi-lô** on every vendor/dish; romanisations are best-effort → native reviewer to confirm (binding
  before art/print; the 5 new day dishes + 開團 blessing included).
- **BINDING wording rail:** frame any follower loss as *the crowd ebbing / drifting to a rival's stall*, never a
  bare "−N". On a lost contest, your followers return to **your own** supply — they do **not** defect to the
  rival. Keep "meeple" out of flavour voice — always "followers / your crowd".
- **BINDING sensitivity rail:** the Old Councillor's Old Favours (`favours_home_draw`) must read as **warm
  inbound goodwill**, never patronage/favour-trading; the Big Boss (老大) is a **playful, affectionate fixer**,
  never a triad/gang caricature. Both consultant-gated portrayals.
- **Open flags (not resolved here — routed):**
  - **Vendor `vp` range** reads **0–11** in `vendors.csv` + `game-bible.md`, but `names.md` §3 still says
    "1–6" — a doc-vs-data mismatch → bg-continuity.
  - **Sugar common** is labelled **糖珠 Sugar & Pearls** in `ingredients.csv` / `recipe-glyphs.csv` but **糖
    Sugar** in `names.md` / `game-bible.md` — canonical-name call pending the CD (`names.md` §5).
  - **Followers-max "dial"** — `tokens.csv` carries **no dial component** (the pool ceiling is the meeple count),
    but `game-bible.md` + `names.md` §3 still describe a printed dial → dial-vs-meeple-pool model to reconcile
    (bg-producer / bg-continuity).
  - **Event count** is **54** in `events.csv`; `game-bible.md` rounds it to "~52" → minor reconcile.
