# Travel Agents: Taiwan — Component Manifest (v6.3.1)

> The physical bill of materials for the **v6.3.1** Screentop prototype (TICKETS-ONLY scoring · soft
> night-cost curve). **Data is the source of truth** (`components/*.csv|json`); renders in `build/`
> regenerate via `make.sh` and snapshot to `exports/`. Counts are the 2-player base (the design home);
> the vendor/ticket/Buzz supply and the clock marks scale up with player count (`bg-architect`). Card
> sizes/materials feed prototyping + manufacturing (see `knowledge/manufacturing-specs.md`).

## Cards

| Component | File | Cards (2p) | Size | Notes |
|---|---|---:|---|---|
| **Vendor deck** | `vendors.csv` | **24** | poker 63.5×88.9 mm | Per region, split by `phase` into a DAY deck + a NIGHT deck; drinks mixed in as the low-value vendors. Face-up: North 2, others 1. Face = **Draw (人氣) attribute + region icon-or-none** — NO score, NO Rep, NO perk (vendors don't score). |
| **Tour Tickets** | `missions.csv` | **45** | poker | The **SOLE scoring vector.** DAY deck 20 + NIGHT deck 25 = **44 distinct patterns / 45 physical cards** (遍地開花 Blossoming is printed once per deck → two cards `g_travel3d`/`g_travel3n`). Draw 5 per phase (rest to box); reveal a row of 3. A ticket's **deck is its judging trigger** (DAY at dusk, NIGHT at last train). |
| **Ingredient market** | `ingredients.csv` | **62** | poker (or mini) | The Visit / Convenience Store / Travel draw. 5-palette; 糖 only in C & S. Renewable (discards recycle). See per-deck split below. |
| **Event cards** | `events.csv` | **27** | poker (or mini) | Scoped ⦿/⬢/➤ hazards/boons (tax-not-destroy) **+ the Reach economy** (3 Reach-gain, 2 Reach-sink 負評/出包) **+ 2 table-wide 排班保養 "Scheduled Maintenance"** (its own island-wide banner, NOT a scoped card). Shuffled into the matching region+phase ingredient deck; **night decks event-heavier**. |
| **Character mats** | `characters.csv` | **5** | mat (rendered as cards in the prototype) | 里長伯 · 媽寶 · 大胃王 · 網紅 · 大哥, each ability + flaw public. See `character-mats.md` (locked kits + reserve dials). |

**Total cards: 163** (24 + 45 + 62 + 27 + 5).

### Vendor deck — the day/night split + the CD-4 night-cost curve (drinks = the low-value vendors)
`{N:1}` = 1 pork · `K` = the common (sugar) · `→X` = cross-region pull · ★ = apex (no icon).
**Draw** = the printed 人氣 attribute (referenced by value-tickets + marks the ★ apex) — **not a score.**

| Region | Face-up | Day vendors (cost) | Night vendors (cost) | Apex ★ |
|---|:--:|---|---|---|
| North 北 (pork) | **2** | 肉包 {N:1}, 蛋餅 {N:1}, 豆漿◇{K:1} | 胡椒餅 {N:2,C:1}→C, 牛肉麵 {N:2,S:1}→S, ★大香腸 {N:3,S:1}→S, 珍奶◇{K:1} | 大香腸 (Draw 7, cost 4) |
| Central 中 (tea) | 1 | 肉圓 {C:1}, 麵線 {C:1}, 珍珠奶茶◇{K:1}, 冬瓜茶◇{K:1} | 大腸包小腸 {C:2,S:1}→S, ★逢甲名物 {C:2,S:2}→S | 逢甲名物 (Draw 6, cost 4) |
| South 南 (seafood) | 1 | 虱目魚粥 {S:1}, 碗粿 {S:1}, 木瓜牛奶◇{K:1} | 蚵仔煎 {S:2,N:1}→N, 棺材板 {S:2,E:1}→E, ★擔仔麵 {S:3,E:1}→E | 擔仔麵 (Draw 7, cost 4) |
| East 東 (rice) | 1 | 竹筒飯 {E:2}, 米糕 {E:1}, 洛神花茶◇{K:1} | 麻糬 {E:2,C:1}→C, ★石板烤肉 {E:3,N:2}→N | **石板烤肉 (Draw 8, cost 5 — TOP)** |

Counts: **N 7 · C 6 · S 6 · E 5 = 24 vendors** (◇ = 6 drinks; 4 apex ★, one per region, all night, no icon).
*(Spec note: `v6.3-content-draft.md` twice says "7 drinks" but its enumerated CD-4 table lists **6**; the
enumerated table is the source of truth → **6 drinks** built.)*

**The LOCKED CD-4 soft night curve (baked into `vendors.csv`):** DAY discount-only foods + drinks held as
printed (~1 ingredient). NIGHT "both" foods → **cost 3** (胡椒餅, 牛肉麵, 大腸包小腸, 蚵仔煎, 棺材板, 麻糬);
apex ★ → **cost 4** (大香腸, 逢甲名物, 擔仔麵) **except the top apex 石板烤肉 → cost 5** (Draw 8). **Every
night marquee is cross-region** (needs a two-region engine to zero out — the load-bearing guard).
**Central tea-export fix in place:** 胡椒餅 {N:2,**C:1**} and 麻糬 {E:2,**C:1**} give Central tea its export,
closing the N→C→S→E→N loop.

### Ingredient market — the per-region DAY / NIGHT decks (with events shuffled in)
| Deck (`deck` tag) | Signature cards | 糖 Sugar (K) | Event cards | Deck size |
|---|---:|---:|---:|---:|
| north-day | 8 pork | — | 3 | 11 |
| north-night | 6 pork | — | 5 *(incl. 1 Scheduled Maintenance)* | 11 |
| central-day | 6 tea | 3 | 2 | 11 |
| central-night | 5 tea | 3 | 4 | 12 |
| south-day | 6 seafood | 3 | 3 | 12 |
| south-night | 5 seafood | 3 | 5 *(incl. 1 Scheduled Maintenance)* | 13 |
| east-day | 8 rice | — | 1 | 9 |
| east-night | 6 rice | — | 4 | 10 |

Ingredient cards total **62**; event cards total **27** (day 9 / night 18). The **2 Scheduled Maintenance**
cards live in the **North NIGHT** and **South NIGHT** decks (the HSR endpoints — set aside for dusk). The
prototyper shuffles each region+phase's ingredient cards + matching-`deck` events into one face-down pile.

## Tokens, markers & tracks (`tokens.csv`, board renders)

| Component | File / source | Qty (2p) | Notes |
|---|---|---:|---|
| Ingredient tokens (5) | `tokens.csv` | 豬14 · 茶14 · 海14 · 米12 · 糖16 = **70** | The 5-palette. Also the glyph source for vendor recipe chips. |
| Buzz tokens | `tokens.csv` | **24** | Committed public on vendors; **capped by your Reach.** Only ever in supply or on a vendor. |
| ★ Star tokens | `tokens.csv` | **4** | The accolade value-swing boon — **+2 Draw** to whoever wins the vendor. |
| Reach markers | `tokens.csv` | 4 | One per player on the Reach track (the Buzz cap; **start at 2; NOT a score**). |
| Tours-Completed markers | `tokens.csv` | 4 | One per player on the Tours-Completed counter (hosts the per-player Rave Reviews at the 2nd & 4th tour). |
| Vendor-claims clock marker | `tokens.csv` | 1 | Shared, on the day-clock track. |
| HSR-closed reminder marker | `tokens.csv` | 1 | Sits on the HSR spine while a **Scheduled Maintenance** card is active (N↔S closed). |
| 成團 / 取消 pile markers | `tokens.csv` | 2 + 2 | Win-pile (COMPLETED 成團) / lose-pile (CANCELLED 取消) area markers, per player. |
| Agent pawns | `tokens.csv` | 4 (2 used @2p) | One per agent, on the region ring — **all start in Taipei (North hub)**. |
| **Region-ring board** | `map.json` | 1 | 4 regions on the diamond, ring + HSR spine, face-up slot counts, **Taipei common-start hub**, HSR-closed reminder slot. |
| **Reach track** | make.sh (scoretrack 0–12) | 1 | Buzz cap; start at 2. NOT a score. |
| **Tours-Completed counter** | make.sh (scoretrack 0–8, Rave Reviews @2 / @4) | 1 | Repurposed from the old Bookings/VP track. Per-player, monotonic. |
| **Vendor-claims clock track** | make.sh (scoretrack 0–10, DUSK@5 / LAST TRAIN@10 @2p) | 1 | Marks grow with player count. |
| Player aid | `player-aid.json` | 1–2 | 16 lines (≤22 budget). |

**No score/VP track** — the score is the Tour-Ticket tally (§9 of the rules), tallied once at game end.

## Component-type count (complexity budget: max 8)
Cards (vendors / tickets / ingredients / events — one card type), character mats, region board, tracks
(Reach / Tours-Completed / clock), tokens (ingredient / Buzz / star / markers / pawns), pile areas. Card
*count* is high (163) but component **types** stay within budget — **and v6.3 REMOVED a whole track type**
(the live VP/score track is gone under tickets-only). (bg-elegance owns the formal complexity check.)

## Notes / flags
- **TICKETS-ONLY scoring (v6.3):** vendors give NO points; the score is Σ WIN-pile COMPLETED 成團 value − Σ
  floor(value/2) LOSE-pile CANCELLED 取消. Draw is a printed attribute only.
- **CD-4 soft night curve + Central tea-export fix** baked into `vendors.csv` (see the vendor table above).
- **Scheduled Maintenance ×2** (island-wide banner event) in the N/S NIGHT decks — needs its own frame +
  HSR-closed board marker (→ bg-infodesign).
- **里長伯 rework:** home-region −1 / +1 away-tax, start-Reach 2. Two mat icons (home-discount + away-tax)
  → bg-infodesign. See `character-mats.md`.
- **East 石板烤肉 (Indigenous-forward):** #1 pre-art item — **paid Taiwanese/Indigenous consultant sign-off
  on dish + naming + framing BEFORE art**.
- **繁體 + Tâi-lô** on every vendor/dish; romanisations are first-pass → native reviewer to bless.
- **COMPLETED 成團 / CANCELLED 取消 scoring is a RULE, not per-card data** — tickets carry only value + pattern + phase tag.
