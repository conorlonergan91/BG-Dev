# Travel Agents: Taiwan — Component Manifest (v6.2)

> The physical bill of materials for the **v6.2** Screentop prototype. **Data is the source of truth**
> (`components/*.csv|json`); renders in `build/` regenerate via `make.sh`. Counts are the 2-player base
> (the design home); the vendor/ticket/Buzz supply and the clock marks scale up with player count
> (`bg-architect`). Card sizes/materials feed prototyping + manufacturing (see
> `knowledge/manufacturing-specs.md`).

## Cards

| Component | File | Cards (2p) | Size | Notes |
|---|---|---:|---|---|
| **Vendor deck** | `vendors.csv` | **24** | poker 63.5×88.9 mm | Per region, split by `phase` into a DAY deck + a NIGHT deck; drinks mixed in as the low-value vendors. Face-up: North 2, others 1. |
| **Tour Tickets** | `missions.csv` | **27** | poker | 12 daytime + 12 nighttime + 3 general. Variable setup: draw 5 per phase (rest to box); reveal a row of 3. |
| **Ingredient market** | `ingredients.csv` | **62** | poker (or mini) | The Visit / Convenience Store / Travel draw. 5-palette; 糖 only in C & S. Renewable (discards recycle). See per-deck split below. |
| **Event cards** | `events.csv` | **20** | poker (or mini) | Scoped ⦿/⬢/➤, hazard-leaning (~60%), tax-not-destroy. Shuffled into the matching region+phase ingredient deck; **night decks event-heavier** (12 night vs 8 day). |
| **Character mats** | `characters.csv` | **4** | mat (rendered as cards in the prototype) | 里長伯 · 媽寶 · 大胃王 · 網紅, each ability + flaw public. See `character-mats.md` (reserve dials + the 大哥 build-scope flag). |

**Total cards: ~137** (24 + 27 + 62 + 20 + 4).

### Vendor deck — the day/night split (drinks = the low-value vendors)
| Region | Face-up | Day vendors | Night vendors | Drinks | Apex ★ |
|---|:--:|---|---|---|---|
| North 北 (pork) | **2** | 肉包, 蛋餅, 豆漿(drink) | 胡椒餅, 牛肉麵, ★大香腸, 珍奶(drink) | 豆漿, 珍奶 | 大香腸 (P7) |
| Central 中 (tea) | 1 | 肉圓, 麵線, 珍珠奶茶(drink) | 大腸包小腸, ★逢甲名物, 冬瓜茶(drink) | 珍珠奶茶, 冬瓜茶 | 逢甲名物 (P6) |
| South 南 (seafood) | 1 | 虱目魚粥, 碗粿, 木瓜牛奶(drink) | 蚵仔煎, 棺材板, ★擔仔麵 | 木瓜牛奶 | 擔仔麵 (P7) |
| East 東 (rice) | 1 | 竹筒飯, 米糕 | 麻糬, ★石板烤肉, 洛神花茶(drink) | 洛神花茶 | **石板烤肉 (P8)** |

Counts: N 7 · C 6 · S 6 · E 5 = **24 vendors** (6 drinks; 4 apex ★, one per region, all night).

### Ingredient market — the per-region DAY / NIGHT decks
| Deck (`deck` tag) | Signature cards | 糖 Sugar (K) | Event cards | Deck size |
|---|---:|---:|---:|---:|
| north-day | 8 pork | — | 3 | 11 |
| north-night | 6 pork | — | 3 | 9 |
| central-day | 6 tea | 3 | 2 | 11 |
| central-night | 5 tea | 3 | 3 | 11 |
| south-day | 6 seafood | 3 | 3 | 12 |
| south-night | 5 seafood | 3 | 3 | 11 |
| east-day | 8 rice | — | 2 | 10 |
| east-night | 6 rice | — | 3 | 9 |

Ingredient cards total **62**; event cards total **20** (day 8 / night 12). (The prototyper shuffles each
region+phase's ingredient cards + matching-`deck` events into one face-down pile.)

## Tokens, markers & tracks (`tokens.csv`, board renders)

| Component | File / source | Qty (2p) | Notes |
|---|---|---:|---|
| Ingredient tokens (5) | `tokens.csv` | 豬14 · 茶14 · 海14 · 米12 · 糖16 = **70** | The 5-palette. Also the glyph source for vendor recipe chips. (On Screentop the market *cards* carry the ingredient; tokens are the physical Larder currency.) |
| Buzz tokens | `tokens.csv` | **24** | The promotional currency; only ever in the supply or on a vendor. |
| ★ Star tokens | `tokens.csv` | **4** | The accolade value-swing boon (+2 Prestige / +1 Rep to whoever wins the vendor). |
| Agent pawns | `tokens.csv` | 4 (2 used @2p) | One per agent, on the region ring. |
| Prestige (VP) markers | `tokens.csv` | 4 | One per player on the Prestige track. |
| Reputation markers | `tokens.csv` | 4 | One per player on the Reputation track. |
| Vendor-claims clock marker | `tokens.csv` | 1 | Shared, on the clock track. |
| 成團 / 遺珠 pile markers | `tokens.csv` | 2 + 2 | Win-pile (Published Tours) / lose-pile (Ones That Got Away) area markers, per player. |
| **Region-ring board** | `map.json` | 1 | 4 regions on the diamond, ring + HSR spine, face-up slot counts. |
| **Prestige track** | make.sh (scoretrack 0–50) | 1 | |
| **Reputation track** | make.sh (scoretrack 0–12, milestones 3/6/9/12) | 1 | |
| **Vendor-claims clock track** | make.sh (scoretrack 0–10, DUSK@5 / LAST TRAIN@10 @2p) | 1 | Marks grow with player count. |
| Player aid | `player-aid.json` | 1–2 | ≤22 lines (complexity budget). |

## Component-type count (complexity budget: max 8)
Cards (vendors / tickets / ingredients / events — one card type), character mats, region board,
tracks (Prestige / Reputation / clock), tokens (ingredient / Buzz / star / markers / pawns), pile
areas. Card *count* is high (~137) but component **types** stay within budget — the v6.2 growth is card
count + day/night colour, not new physical types. (bg-elegance owns the formal complexity check.)

## Notes / flags
- **Central tea-export fix applied:** North's 牛肉麵 (night) now needs Central 茶 (was Seafood), closing
  the cross-region demand loop N→C→S→E→N so tea is exported and Central stops being a pure importer.
- **East 石板烤肉 (Indigenous-forward):** #1 pre-art item — **paid Taiwanese/Indigenous consultant
  sign-off on dish + naming + framing BEFORE art**.
- **繁體 + Tâi-lô** on every vendor/dish; romanisations are first-pass → native reviewer to bless.
- **成團 / 遺珠 scoring is a RULE, not per-card data** — tickets carry only value + pattern + phase tag.
