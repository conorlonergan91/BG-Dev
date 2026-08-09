# V7+ — Generic Ingredient Categories (CD direction, 2026-08-09)

**The move (CD):** replace the 5 *specific* ingredients (pork · tea · seafood · rice · sugar) with a small
set of **generic categories** — e.g. **Meat · Vegetables · Fish · Tea · Sugar · Pantry** (final set TBD) —
whose **card illustration shows a MIX** (the "Meat" card depicts chicken, pork belly, beef, etc.). Reference:
a game the CD named that uses generic ingredient categories (confirm which — noted as "Yes Ginseng?"; the
mechanic, not the title, is the point).

**Why:** trading ingredient *specificity* for dish *breadth* opens the deck to **far more Taiwan dishes**
(deepening the culture-sharing theme), and it **elegantly solves the Chiayi turkey-rice problem** — turkey
rice becomes a **Meat** dish, no bespoke poultry ingredient needed (this supersedes the S04 A/B/C call:
turkey rice is now essentially free, so a Chiayi 火雞肉飯 vendor can exist without reopening the ingredient
system for it specifically).

## Design requirements (for the bg-design taxonomy pass — do AFTER the current bg-infodesign render lands)
1. **Define the generic set** (~6 categories). Candidate: Meat / Vegetables / Fish / Tea / Sugar / Pantry
   (Pantry = rice/noodles/flour/dry-goods staples). Confirm count + names with the CD if it drifts from this.
2. **PRESERVE the validated economy skeleton.** The current design's balance rests on a
   **regional-signature + common** structure (pork=North · tea=Central · seafood=South · rice=East ·
   sugar=common C&S) that makes **travel + cross-region dishes** matter, plus the CD-4 soft night-cost curve.
   The generic set MUST keep that skeleton — each region a signature category, one or two commons — so
   sourcing/travel/night-cost still behave. Map old→new (e.g. pork→Meat[N] · tea→Tea[C] · seafood→Fish[S] ·
   rice→Pantry[E] · sugar→Sugar[common] · + Vegetables as the new common/second axis) — bg-design fixes the
   exact mapping to hold the economy.
3. **Re-express the vendor recipes** (`vendors.csv`) in the generic categories, **preserving each dish's
   difficulty** (ingredient count + cross-region shape) so the tickets/sourcing balance is unchanged in
   structure; then diversify dishes for variety WITHIN that difficulty envelope.
4. **Ingredient cards** = one per generic category, illustration a **mix** of real Taiwan examples
   (art-brief per category, citing `art/art-style.md`; distinguishable by picture + shape, not colour — loop
   bg-access). Update `recipe-glyphs.csv` to the generic set.
5. **Balance assessment → likely a GATED re-sim.** Changing the ingredient taxonomy + diversifying dishes
   touches the economy the sim validates. bg-design assesses the magnitude: a near-structural mirror = small
   delta (maybe a light confirm); genuine dish diversification = **flag a CD-gated re-sim** before locking.
6. **Unlocks (list for the CD):** turkey rice (Chiayi, Meat), plus broad new dishes across meat/veg/fish/
   pantry — a much wider tour of Taiwan's food. Enumerate example new vendor dishes when re-expressing.

## Sequencing
The current bg-infodesign structural pass renders the **5-specific** ingredient cards + recipe-chips as
**interim** — superseded by this taxonomy redesign. Order: (a) bg-infodesign structural pass lands → (b)
bg-design taxonomy + recipe remap (+ balance assess) → (c) CD-gated re-sim if flagged → (d) re-render the
generic ingredient cards + vendor recipe-chips + art-briefs.

---

# ✅ FINAL TAXONOMY + REGION MAPPING + RECIPE CONVERSION (bg-design, 2026-08-09, auto-drive)

Executed in `components/ingredients.csv` + `vendors.csv` + `recipe-glyphs.csv`. Lint **0 errors**. Beacon +
`build_cards.py` untouched (data + design only; the generic ingredient-card ART / emblem-shape render is the
deferred bg-infodesign pass). **The economy skeleton is preserved structurally** — see the balance verdict.

## 1. The generic category set — SIX

| Category | 繁體 | glyph | Role | Illustration = a MIX of… |
|---|---|---|---|---|
| **Meat** | 肉 | 肉 | **North signature** | pork belly · beef shank · sausage · poultry (incl. turkey) |
| **Tea** | 茶 | 茶 | **Central signature** | high-mountain oolong · black tea · the bubble-tea leaf base |
| **Seafood** | 海鮮 | 海 | **South signature** | oyster · milkfish · shrimp · clam · squid |
| **Pantry** | 糧 | 糧 | **East signature** | valley rice · glutinous rice · noodles · flour |
| **Sugar** | 糖 | 糖 | **COMMON — sourced in Central & South** | cane sugar (unchanged) |
| **Vegetables** | 菜 | 菜 | **COMMON — sourced in North & East** *(NEW 2nd axis)* | greens · cabbage · radish · bamboo shoot · scallion · roselle · wintermelon |

**Refinement vs the CD's candidate (`Meat·Vegetables·Fish·Tea·Sugar·Pantry`):** the one change is
**Fish → Seafood (海鮮)**. "Fish" is too narrow to name oyster omelette / shrimp noodles / clams — 海鮮 is
the correct generic, is the *already-current* term (zero churn on the id `seafood`), and its illustration
still shows the mix. Everything else matches the CD's set exactly.

**Why 6 and not 5:** a straight 5-way rename (Meat/Tea/Seafood/Pantry/Sugar) would be a pure mirror but
delivers no *breadth* — the whole point is more Taiwan food. **Vegetables** is the added axis; it is a
**second COMMON**, deliberately **mirroring Sugar** so the "signature + a common" skeleton stays intact and
in fact becomes *symmetric across all four regions* (see §2).

**Emblem shapes → bg-infodesign hand-off** (shapes live in `tools/cards/themes.py`, an ART render pass —
deferred here). Recommended, dual-coded (shape + colour, never colour alone; loop bg-access on the new
green): meat = **hex** (red, inherits `pork`) · tea = **triangle** · seafood = **square** · pantry =
**circle** (indigo, inherits `rice`) · sugar = **beam** · **veg = a NEW leaf emblem** (green `#4C9A5A`; a
`diamond` is the safe fallback if the render set is fixed). ⚠ **bg-access:** meat-red vs veg-green is a
red/green pair — the *distinct emblem* is the required redundant encoding; verify ΔE + emblem-distinctness.

## 2. Region mapping — PRESERVES the validated signature + common skeleton

The old skeleton: **pork=N sig · tea=C sig · seafood=S sig · rice=E sig · sugar=common (C&S)**. N & E had
**no common** (pure-signature decks); C & S had signature + sugar.

The new skeleton makes it **symmetric — every region = its signature + ONE common, two commons forming two
cross-axes:**

| Region | Signature | Local common | Old → new |
|---|---|---|---|
| **North 北** | **Meat 肉** | **Vegetables 菜** *(new)* | pork → Meat; + veg axis |
| **Central 中** | **Tea 茶** | Sugar 糖 | tea → Tea (unchanged) |
| **South 南** | **Seafood 海鮮** | Sugar 糖 | seafood → Seafood (unchanged) |
| **East 東** | **Pantry 糧** | **Vegetables 菜** *(new)* | rice → Pantry; + veg axis |

**Two cross-axes now:** to source **Sugar** you visit C or S; to source **Vegetables** you visit N or E.
This doubles the cross-region common texture (e.g. a Central 冬瓜茶 wintermelon drink now pulls 菜 from N/E,
exactly mirroring how a North 珍奶 pulls 糖 from C/S).

**Card distribution — deck depths & the 62-card total held EXACTLY** (veg added to N & E by *shaving*
signature, not by growing the deck — so market-draw dynamics don't shift structurally):

| Region · phase | Signature cards | Common cards | Depth (old → new) |
|---|---|---|---|
| N day | Meat ×6 | Veg ×2 | 8 → **8** |
| N night | Meat ×5 | Veg ×1 | 6 → **6** |
| C day | Tea ×6 | Sugar ×3 | 9 → **9** |
| C night | Tea ×5 | Sugar ×3 | 8 → **8** |
| S day | Seafood ×6 | Sugar ×3 | 9 → **9** |
| S night | Seafood ×5 | Sugar ×3 | 8 → **8** |
| E day | Pantry ×6 | Veg ×2 | 8 → **8** |
| E night | Pantry ×5 | Veg ×1 | 6 → **6** |

**Totals (unchanged 62):** Meat 11 · Tea 11 · Seafood 11 · Pantry 11 · Sugar 12 · Veg 6.
Signature draw-rate delta: N/E signature was 100% of the non-event draw; now **~75% day / ~83% night**
(diluted by the light veg load) — this, plus the demand redistribution below, is the balance delta.

## 3. Old → new recipe conversion table (all 24 vendors)

Every vendor's **cost total (= ingredient count), cross-region span-COUNT, CD-4 tier, and drink/icon status
are byte-preserved.** Diversification changes only *which* generic types are demanded (and the turkey-rice
re-cast). `[R]` = rename only.

| ID · dish | Old recipe | New recipe | Cost | Span | Note |
|---|---|---|---|---|---|
| N01 肉包 | pork | **meat** | 1 | N | [R] |
| N02 蛋餅 | pork | **meat** | 1 | N | [R] |
| N03 豆漿 | sugar | **sugar** | 1 | — | [R] drink |
| N04 胡椒餅 | pork·pork·tea | **meat·meat·tea** | 3 | N,C | [R] · tea-export kept |
| N05 牛肉麵 | pork·pork·seafood | **meat·pantry·veg** | 3 | N,E | **DIVERSIFIED** — beef + hand-pulled noodles + pickled greens; cross S→E; +veg |
| N06 ★ 大香腸 | pork·pork·pork·seafood | **meat·meat·meat·seafood** | 4 | N,S | [R] apex (protected) |
| N07 珍奶 | sugar | **sugar** | 1 | — | [R] drink |
| C01 肉圓 | tea | **tea** | 1 | C | [R] |
| C02 麵線 | tea | **tea** | 1 | C | [R] |
| C03 珍珠奶茶 | sugar | **sugar** | 1 | — | [R] drink |
| C04 大腸包小腸 | tea·tea·seafood | **tea·tea·pantry** | 3 | C,E | **DIVERSIFIED** — sausage in a glutinous-rice sausage; cross S→E (keeps 2× tea local demand) |
| C05 ★ 逢甲名物 | tea·tea·seafood·seafood | **tea·tea·seafood·seafood** | 4 | C,S | [R] apex (protected) |
| C06 冬瓜茶 | sugar | **veg** | 1 | — | **DIVERSIFIED** — wintermelon = 菜 gourd; drink now pulls veg (cross common) |
| S01 虱目魚粥 | seafood | **seafood** | 1 | S | [R] |
| S02 碗粿 | seafood | **seafood** | 1 | S | [R] |
| S03 木瓜牛奶 | sugar | **sugar** | 1 | — | [R] drink |
| **S04 火雞肉飯** | seafood·seafood·pork *(蚵仔煎)* | **meat·pantry·veg** | 3 | N,E | **TURKEY RICE** — the "free B"; Chiayi 火雞肉飯 = shredded turkey + rice + pickled daikon; homeless-in-South (no local seafood) |
| S05 棺材板 | seafood·seafood·rice | **seafood·seafood·pantry** | 3 | S,E | [R] |
| S06 ★ 擔仔麵 | seafood·seafood·seafood·rice | **seafood·seafood·seafood·pantry** | 4 | S,E | [R] apex (protected) |
| E01 竹筒飯 | rice·rice | **pantry·pantry** | 2 | E | [R] |
| E02 米糕 | rice | **pantry** | 1 | E | [R] |
| E03 麻糬 | rice·rice·tea | **pantry·pantry·tea** | 3 | E,C | [R] · tea-export kept |
| E04 ★ 石板烤肉 | rice·rice·rice·pork·pork | **pantry·pantry·pantry·meat·meat** | 5 | E,N | [R] top-apex (protected) |
| E05 洛神花茶 | sugar | **veg** | 1 | — | **DIVERSIFIED** — Taitung roselle = 菜; East-local veg drink |

**Design rules held while diversifying:**
- **Apexes (N06·C05·S06·E04) are pure renames** — the CD-4 night curve is most sensitive at the marquees, so
  they are protected from re-shaping.
- **Day discount-only foods keep their own region's signature** (so the region-icon discount stays
  meaningful and single-region) — renames only.
- **Diversification is confined to the "both"-tier night dishes + 2 plant-drinks + turkey rice**, each
  preserving cost, span-count and tier.
- **Tea export demand preserved exactly** (N04 + E03 still →C) — the RISK #3 four-region-loop fix stands.

## 4. Turkey rice (S04) — the S04 A/B/C is RESOLVED as "free B"

With generic **Meat**, Chiayi 火雞肉飯 needs no bespoke poultry ingredient. **S04 蚵仔煎 (oyster omelette) →
火雞肉飯 (turkey rice)**: `meat · pantry · veg` (shredded turkey + rice + pickled daikon), cost 3, both-tier,
spanning N+E (2 signature regions). This **honours the family Chiayi anchor faithfully** (vendor-places.md)
*without* reopening the ingredient system — the redesign made B free. It is **homeless-in-South** (a South
vendor demanding no South seafood; its South icon still feeds the ramp) — a real, small sourcing-effort
increase flagged for the re-sim. **Oyster omelette (蚵仔煎) is displaced** from the 24 — logged as a top
candidate for a future South slot / small expansion. Rom. `hóe-ke-bah-pn̄g` is best-effort → **consultant to
confirm Tâi-lô** (binding, per the vendor-places watch-list).

## 5. Balance delta vs the sim-validated economy → RECOMMEND a CD-GATED RE-SIM

**Verdict: NOT a near-structural mirror — a genuine (but low-structural-risk, narrow-scope) economy shift.**

*What is byte-preserved (the mirror part):* every dish's **cost, cross-region span-COUNT, CD-4 tier**,
drink/icon status; the **aggregate sourcing burden** (Σ demand = 50, unchanged); **deck depths + 62-card
total**; **tea + meat total demand** (8 / 11≈12); the day-home-anchor / night-cross structure; the
four-region tea-export loop. The clock, tickets-only scoring, area-majority fight, dial-drop, and the
six-character bands **do not depend on ingredient identity at all** — they are untouched.

*What genuinely shifted (why a re-sim, not just a confirm):*
1. **Supply:** N & E signature draw diluted 100% → ~75–83% (veg added); a **6th ingredient type + a 2nd
   common with a *different* source-region pair** (veg in N/E vs sugar in C/S) — the sim currently models
   **one** common (`COMMON="K"` in `{C,S}`) and would need veg encoded as a second common.
2. **Demand redistribution** (aggregate constant, distribution moved): **Pantry 10 → 13** (East becomes the
   cross-region demand *hub*) · **Seafood 14 → 10** (South signature pressure eased) · **Sugar 6 → 4**
   (loosened; moved to veg) · **Veg 0 → 4** (new) · Tea 8, Meat ~11 (held).
3. **Two sourcing-pressure points created:** **East Pantry** (demand 13 vs 11 supply, single-region source,
   supply also diluted by veg) and **North Meat** (demand 11 vs 11, single-region, diluted) are the tightest
   ratios — the opposite corner from the eased South seafood.
4. **Turkey rice is homeless-in-South** — a vendor with no home-region ingredient forces more travel than
   the dish it replaced (both span 2 regions, but the old one sourced 2/3 locally, the new one 0/3).

**A re-sim must probe (per count 3–6, focus the home 4p + stretch 6p):**
- **Sourcing RATE per ingredient per region, day vs night** — does **East Pantry** or **North Meat** starve
  now that demand rose / supply diluted? Does **South Seafood** trivialise (eased demand)?
- **Night-curve affordability** — re-confirm the CD-4 target (night sourcing ~60–100% of the day rate) holds
  per count with the redistributed demand + the diluted N/E night decks (night veg is deliberately thin:
  1 card each in N & E).
- **Turkey-rice / homeless-vendor affordability** — is S04 (and by extension any 0-home-anchor dish)
  claimable at a fair rate, or does the double-cross (N + E) make it a dead stall?
- **Cross-region travel graph** — East is now the pull-hub (5 pantry imports); confirm no region's export
  demand collapsed and travel still spreads (the RISK #3 loop). Reserve lever if East pantry starves: bump
  East pantry supply (drop East veg 2/1 → 1/0) or re-point one pantry cross.
- **Tickets-only health unchanged** — a zero-ticket line still loses (structural; ingredient identity is
  orthogonal, so expected dead — but re-confirm the collection lanes aren't pinched by the new demand mix).
- **Veg is a live axis, not dead weight** — veg demand 4 vs supply 6 (ratio 1.5); confirm it's sourced/used,
  not ignored.

**Sim-encode notes for bg-playtest (the re-sim is GATED — NOT run here):** add a 6th type `VEG` as a second
common; make `COMMON` handling type-aware (`sugar∈{C,S}`, `veg∈{N,E}`) in the pool setup, `_return_token`,
`_is_cross` (must exclude veg too), and the sourcing bots; set N/E pools to `{sig: ~9, veg: ~3}` to match
the 6:2 / 5:1 card ratios; update the `_build_vendors()` cost table to the new recipes above. **Note a
pre-existing sim↔CSV drift** (e.g. sim 牛肉麵 →C via `CENTRAL_TEA_FIX`, CSV →S/now→E; sim 石板烤肉 soft cost 3
vs CSV canon 5) — the re-sim should encode the **CSV recipes as the source of truth**.
