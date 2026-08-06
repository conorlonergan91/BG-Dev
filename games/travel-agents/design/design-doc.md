# Travel Agents: Taiwan — Design Doc

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.
Spine A **"Rival Agents, Shared Beat"** (LOCKED, 2026-08-06). Slug `travel-agents`.

> **One-line frame:** a warm competitive food-travel duel where a secret **Assignment** drives your
> trip, but the surplus in your **Larder** is worth more handed to a rival than hoarded — because a
> **Dead-drop** banks you a flexible **Insider Tip** and nudges the shared **Grand Dossier** everyone
> profits from. Race to plate real Taiwanese dishes across an island shaped by real food geography.

---

## Design goals
- **Target weight ~1.8** (Ticket to Ride / Splendor band). **One** hidden-info hook only: the secret
  **Assignment**. Everything else is open information — no deduction engine.
- **Aesthetics (locked):** Discovery (lead) + Fellowship + Challenge. The market/menu *reveals*, the
  Dead-drop and Grand Dossier make cooperation *real* (not just warm rivalry), the trip is a light
  optimisation puzzle.
- **The meaningful decision at the heart of the game (every turn):** *advance my secret mission, feed
  the shared tour, or convert my surplus into leverage?* — travel toward what I need, stock the local
  specialty, cash in a dish (timing the Grand Dossier), or dead-drop surplus to a rival for an Insider
  Tip.
- **Design the top risk out:** make the Dead-drop **individually rational often enough** that players
  actually cooperate, without a dominant "hoard, never tip" line or kingmaking (see *Interaction &
  tension* and *First-pass balance model*).
- **Taiwan does real work:** the region↔ingredient↔dish web is real food geography; rename the setting
  and it breaks (re-skin-test defeater). Real dishes, romanised + 繁體, never mangled.

---

## Core loop (detailed)

A player's turn is **one action** from a menu of four. Turns are short; downtime is low (crucial at
2p). Each cycle you are optimising: *which ingredients do I still need for my next dish / my secret
Assignment, and is it worth a turn to travel for them, or to convert surplus into an Insider Tip?*

1. **Read the board.** Your secret **Assignment** points at a shape of trip (a regional crawl, a
   variety tour, two hero dishes…). The face-up **Menu** shows which dishes are plate-able now. The
   **Grand Dossier** shows how close the table is to the next shared **Discovery bonus** (and to the
   end).
2. **Source what you need.** *Stock Up* (2 ingredients where you stand) or *Travel* (move one region,
   arrive with 1). You can only take a region's **specialty** in that region; **pantry** supplies are
   available anywhere (the convenience store).
3. **Plate a dish.** Spend a Menu dish's recipe from your **Larder** → the Dish card enters your
   **Traveller's Log** (VP), the **Grand Dossier** advances +1, and you check your Assignment.
4. **Convert surplus into leverage.** Your Larder caps at **7**. Rather than discard a surplus
   ingredient, **Dead-drop** it to a rival: they get the ingredient, *you* get an **Insider Tip**
   (a flexible boost) and the Grand Dossier advances +1.
5. **Decide when the trip ends.** When you judge your lead is set, **Extract** ("catch the last train
   home") to trigger the wind-down — or ride the shared Grand Dossier to its final milestone.

The loop compounds gently: Insider Tips earned from dead-drops let you source faster / wild-substitute
/ hop further, which lets you plate more, which advances the Dossier, which pays everyone.

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** (4 regions on a ring: North 北 – Central 中 – South 南 – East 東 –
  back to North; an **HSR** spine links North–Central–South down the west coast). The **Grand Dossier**
  track and a shared **score track** run along the board edge.
- Deal the **Menu**: 4 face-up Dish cards from the shuffled Dish deck.
- Each player: take an **Agent** pawn (start on opposite regions — one North, one South), draw **2
  Assignments and keep 1** secret (return the other), take an empty **Traveller's Log** area in front
  of them. Larder starts empty.
- Seed the Grand Dossier marker at 0. Place ingredient and Insider Tip supplies in reach.

**A turn = choose ONE action** (detailed in *Actions*): **Stock Up**, **Travel**, **Plate**,
**Dead-drop**, or **Extract**. Then, if your Larder exceeds 7, discard down to 7. Play passes clockwise.

**End-trigger (either path):**
- A player takes the **Extract** action, **or**
- The **Grand Dossier** reaches its **final milestone**.

Either way: **finish the current round** (so everyone has had an equal number of turns), then play
**one more full round**, then **score**. (A fair, unswingy wind-down — no "extract turn 1 to deny
turns" degeneracy.)

Target length: **~30–40 min at 2p**, roughly **18–24 turns per player**.

---

## Actions

| Action | Cost | Effect | Notes |
|--------|------|--------|-------|
| **Stock Up** | your turn | Take **2 ingredients** available at your current region: any mix of this region's **specialty** ingredients and **pantry** supplies. | The workhorse. Frictionless (open supply, no market decks). |
| **Travel** | your turn | Move your Agent to an **adjacent** region on the ring; on arrival, take **1 ingredient** available there. (HSR: North↔South counts as adjacent — the west-coast shortcut.) | Travel is never a dead turn — you always arrive with something. The "tax" vs Stock Up (1 vs 2) is the time cost of moving. |
| **Plate** | your turn + spend a recipe from Larder | Choose a **Menu** dish you can afford; return its recipe ingredients to supply; take the Dish card into your **Traveller's Log**; refill the Menu from the deck. Advance the **Grand Dossier +1**. | The scoring engine + the indirect race (a rival can plate the dish you wanted). |
| **Dead-drop** | your turn + give 1 ingredient | Give **1 ingredient from your Larder to a rival** ("a hot tip on where the good stuff is"). Gain **1 Insider Tip**. Advance the **Grand Dossier +1**. | The cooperation engine. See *Interaction & tension* for why it's rational. At 3–4p a player may **receive at most 1 Dead-drop per round**. |
| **Extract** | your turn | Trigger the end-game wind-down (finish the round + one more full round). Your Assignment stays secret until scoring. | Push-your-luck tempo: end it while you're ahead vs plate one more. |
| *(free, not an action)* **Spend an Insider Tip** | 1 Insider Tip | Choose one: **(a)** take 1 extra ingredient from your current region now; **(b)** treat 1 recipe ingredient as **any type** when plating (wild); **(c)** when you Travel, move **1 extra** region. | Flexible leverage — this is what makes a Dead-drop worth doing. |

Every turn has multiple viable options with real trade-offs (travel-for-what-I-need vs stock-the-local
vs plate-now vs convert-surplus vs end-it). No forced/obvious move; Travel is never empty.

---

## Components

| Component | Qty | Notes |
|-----------|-----|-------|
| **Map board** (Taiwan) | 1 | 4 regions on a ring + HSR spine; **Grand Dossier** track + shared **score track** printed along the edge. (One board absorbs three functions to save a component type.) |
| **Dish cards** | ~24 | Recipe (ingredient icons) + VP + name (romanised **and** 繁體) + a small region tag. The heroes — each a little postcard. |
| **Assignment cards** | ~14–16 | Secret objectives ("Operation: ___"). ~+7 VP each on completion. |
| **Ingredient tokens** | ~120 | **9 types**: 8 region **specialties** (2 per region) + 1 fungible **pantry**. Open supply. |
| **Insider Tip tokens** | ~30 | The flexible dead-drop reward. |
| **Agent pawns** | 4 | One per player; on the map. |
| *(Grand Dossier marker + score markers)* | — | Cubes/discs on the board tracks; not a distinct "type." |

**Component types = 6** (board / dish cards / assignment cards / ingredient tokens / tip tokens /
pawns) — **exactly at the budget cap** (`complexity-budget.json`: `max_component_types: 6`). Flag to
`bg-elegance`: no room for a seventh type; new content must reuse these.

### Ingredients — the region↔ingredient web (the Taiwan engine)

| Region | Specialty 1 | Specialty 2 | Real-geography basis |
|--------|-------------|-------------|----------------------|
| **North 北** (Taipei · Keelung · Hsinchu) | **Beef 牛肉** | **Pork belly 五花肉** | Beef noodle is Taipei-iconic; gua bao a northern night-market staple; Hsinchu Hakka pork. |
| **Central 中** (Taichung · Nantou · Changhua) | **Tea 茶葉** | **Tapioca pearls 粉圓** | Bubble tea born in Taichung; Nantou/Lugu oolong; central tea country. |
| **South 南** (Tainan · Kaohsiung · Chiayi) | **Oysters 蚵仔** | **Milkfish 虱目魚** | Tainan/Chiayi oyster farms (七股/東石); Tainan milkfish. |
| **East 東** (Hualien · Taitung · Yilan) | **Mountain rice 池上米** | **Wild greens 野菜** | Chishang/Guanshan premium rice; Indigenous & mountain cuisines. |
| **Anywhere** | **Pantry 補給** (fungible) | — | The ubiquitous **convenience store** (7-11 / 全家) — a real, beloved Taiwan feature. Noodles, egg, starch, milk, seasoning, abstracted to one flexible token. |

> **Sensitivity note (binds — see identity.md):** the East specialties draw on **Indigenous** cuisines;
> keep the label generic and respectful ("mountain rice / wild greens / mountain produce"), never
> costume or exoticise, and route through the **paid Taiwanese cultural consultant** before art/print.
> Dead-drops are framed as *sharing a recommendation* ("you HAVE to try that stall"), never *extracting*
> — the traveller is a guest and fan. Dishes named in romanisation **and** 繁體, never invented/mangled.

### Dishes — recipes (exemplars; full deck ~24)

A dish = **specialties (region-locked) + at most 1 pantry** (keeping recipes travel-motivated — a
pantry-heavy dish would be plate-anywhere and kill routing). VP: **2-ingredient = 3 · 3-ingredient = 4
· Signature (3 specialties from 3 regions) = 5**.

| Dish | 繁體 | Recipe | VP | Regions |
|------|------|--------|----|---------|
| Beef noodle soup | 牛肉麵 | Beef + Pantry | 3 | N |
| Gua bao | 刈包 | Pork belly + Pantry | 3 | N |
| Bubble tea | 珍珠奶茶 | Tea + Pearls | 3 | C |
| Tea egg | 茶葉蛋 | Tea + Pantry | 3 | C |
| Oyster omelette | 蚵仔煎 | Oysters + Pantry | 3 | S |
| Oyster vermicelli | 蚵仔麵線 | Oysters + Pantry | 3 | S |
| Bamboo-tube rice | 竹筒飯 | Rice + Wild greens | 3 | E |
| Milkfish porridge | 虱目魚粥 | Milkfish + Rice | 3 | S+E |
| Chishang bento | 池上便當 | Rice + Pork belly + Pantry | 4 | E+N |
| East-coast platter | 東部風味餐 | Wild greens + Milkfish + Pantry | 4 | E+S |
| Hakka stir-fry | 客家小炒 | Pork belly + Tea + Pantry | 4 | N+C |
| Braised-pork rice | 滷肉飯 | Pork belly + Rice + Pantry | 4 | N+E |
| Banquet platter *(Signature)* | 辦桌 | Oysters + Beef + Wild greens | 5 | S+N+E |
| Round-island feast *(Signature)* | 環島大餐 | Beef + Tea + Milkfish | 5 | N+C+S |

**Deck balance guideline:** each specialty appears in ~5–6 recipes; **~40% of the deck is cross-region**
(2+ regions) to keep travel and the "island tour" alive; ~3 Signatures as aspirational showpieces.

### Assignments (the one hidden hook) — types

Each an "Operation: ___", achievable with ~2–4 plated dishes, **+7 VP** on completion (binary).

| Type | Example | Steers you toward |
|------|---------|-------------------|
| Regional crawl | "Plate **3 dishes** using a **Southern** ingredient." | Depth in one region |
| Variety tour | "Plate dishes using an ingredient from **all 4 regions**." | Round-island breadth |
| Signature obsession | "Plate **2 specific hero dishes** (e.g., beef noodle + oyster omelette)." | Targeted routing |
| Big eater | "Plate **2 three-ingredient dishes**." | Ambitious sets |
| Night-market crawl | "Plate **4 dishes total**." | A safe volume floor |

Balance intent: completion difficulty roughly equal across the deck (~2–4 dishes / ~half your Log), so
no Assignment is a trap or a gimme. **+7 ≈ two dishes ≈ ~20% of a winning score** — a real secret-race
stake that steers your trip without making the rest of the game irrelevant.

---

## Economy & math

**Sourcing throughput.** Stock Up = +2 ingredients; Travel = +1 (and reposition). A typical
3-ingredient cross-region dish (e.g., Chishang bento: Rice(E) + Pork(N) + Pantry) takes ~3 turns to
assemble+plate: Stock Up where you are (+2) → Travel to the other region (+1) → Plate. A 2-ingredient
single-region dish takes ~2 turns.

**VP per turn (the anti-dominant-strategy check).** Deliberately kept *flat-ish* so no dish size
dominates:

| Dish | VP | ~Turns to make+plate | VP/turn |
|------|----|--------------------:|--------:|
| 2-ingredient | 3 | 2 | **1.50** |
| 3-ingredient | 4 | 3 | **1.33** |
| Signature (3-region) | 5 | ~4 | **1.25** |

Small dishes are marginally more efficient per turn, so big dishes are **not** an auto-win — they're
justified by **Assignment** and Grand Dossier synergy, not raw rate. (Key knob for sim — see below.)

**Larder cap = 7.** Guarantees surplus arises regularly → makes Dead-drop's "convert dead weight into an
Insider Tip" the core of why cooperation is rational (below). Discarding for nothing is strictly worse
than dead-dropping for a Tip.

**Insider Tip value ≈ +1 ingredient of flexibility** (an extra source, a wild, or a longer hop) ≈ ~+1
VP-equivalent amortised.

**Target game arc (2p):** ~8–9 dishes plated per player; end ~turn 20–24 each; ~30–40 min.

**Expected 2p score:**

| Source | ~VP | Affects ranking? |
|--------|----:|------------------|
| Plated dishes (~8–9 × ~3.3) | 28–30 | **Yes — the main contest** |
| Assignment (0 or 7) | 0 / 7 | **Yes — the secret swing** |
| Grand Dossier Discovery bonuses (2+3+4+5) | +14 to *everyone* | No — a rising tide (the warm co-op *feel*) |
| Insider Tips used | soft ~+2–4 | Slightly — efficiency edge |
| **Total** | **~48–52** | Winner decided by dishes + Assignment + tip efficiency |

---

## Scoring / win condition

At game end, each player totals their **Traveller's Log**:
1. **Plated dishes** — sum of VP (3 / 4 / 5).
2. **Assignment** — +7 if completed (revealed now), else 0.
3. **Grand Dossier Discovery bonuses** — the flat milestone VP banked in play (equal for all present —
   the celebratory "we did the tour" points; a rising tide, not a ranking lever).
4. **Leftover Insider Tips** — 0 VP (they're leverage, spend them). *(Optional variant: 1 VP per 2
   unused Tips, to remove a "hoard Tips" corner case — flag for sim.)*

Highest total wins. **Tiebreak:** most dishes plated, then furthest-travelled (regions visited).

**Guard against a single dominant strategy:**
- **"Only big dishes":** blocked by flat VP/turn (small dishes are *more* efficient per turn).
- **"Ignore the Dossier / never tip":** the top risk — addressed structurally below; the Larder cap +
  Insider Tip make tipping surplus a near-free gain.
- **"Point-salad":** avoided — only three real scoring avenues (dishes, one Assignment, shared Dossier),
  and the Dossier term is equal-to-all so it can't be gamed into a runaway.

---

## Randomness

- **Input randomness only** (preserves agency, per `design-fundamentals.md`):
  - The **Menu** reveal (which dishes are available now) — the Discovery engine; you *adapt* your
    routing to what's fresh, and can plate a dish out from under a rival.
  - Your **Assignment** draw — mitigated by **draw 2, keep 1** (choose the trip you want).
  - Dish-deck order.
- **No output randomness.** No dice, no to-hit, no post-decision luck. A source/travel/plate is
  deterministic once chosen. This suits the warm, "nail your trip" tone and keeps skill legible at
  ~1.8 without swing.

---

## Interaction & tension

**Indirect (the spine):**
- **The Menu race** — a rival can plate the dish you were routing toward (light "grab it first"
  tension; the reason to watch the board).
- **The Grand Dossier trigger-race** — being the player whose Plate/Dead-drop *crosses* a milestone
  earns a bonus **Insider Tip** (a small individual prize inside the shared payout).
- **End-tempo** — **Extract** and the Dossier's final milestone are levers on when the game ends; a
  leader wants to end it, a trailer wants more turns.

**Direct-but-warm:** the **Dead-drop** — you literally hand a rival an ingredient. Framed as generosity
("you HAVE to try this"), it's the Fellowship mechanic and the crux of the semi-co-op knife-edge.

### Making cooperation individually rational (designing the top risk out)

The failure modes to beat: **(1)** "hoard, never tip" dominates → dead co-op sticker; **(2)** kingmaking
→ tips arbitrarily decide the winner. Here is exactly why neither should happen, with the numbers:

**Why tipping is rational (beats "always hoard"):**
- The **Larder cap of 7** forces surplus. A surplus ingredient you'd otherwise **discard for nothing**
  can instead be **dead-dropped for +1 Insider Tip + a Grand Dossier step**. Converting dead weight into
  a flexible ~+1-VP boost is **strictly better than discarding** — the baseline case is a near-free yes.
- Net for the giver on a **surplus** tip: **+1 Insider Tip (theirs alone) + fractional Dossier push
  (pays them too) − a soon-dead ingredient ≈ +1.5 to +2 VP-equiv.** For the receiver: **+1 ingredient +
  same Dossier push ≈ +1.5 VP-equiv.** **Positive-sum, giver-favourable** → the giver comes out slightly
  ahead *and* the rival smiles (warm). This is the target dynamic.
- Net for the giver on a **useful** (non-surplus) tip: **+Tip +Dossier − (a needed ingredient, ~1 VP) ≈
  break-even**, and now the receiver may net more — so a rational player *won't* hand a threatening rival
  something they need. That's the **interesting** decision (tip a trailing rival for mild goodwill /
  Dossier timing, don't arm the leader), not a dominant line.

**Why it isn't kingmaking:**
- **At 2p there is no kingmaking** (one rival). The decision is cleanly "does my Tip + Dossier gain beat
  the help I give my only opponent?" — yes for surplus, a judgement call for useful. Clean duel.
- **At 3–4p:** the giver **chooses recipient and ingredient**, and the reward (the Insider Tip) is
  **theirs regardless of recipient** — so the incentive is self-focused, not "boost my ally." A player
  may **receive at most one Dead-drop per round** (no gang-feeding a kingmade player). The help is small
  (1 ingredient) relative to the giver's flexible Tip, so tips rarely swing *who wins*.

**The single most important open balance question** (attack first with `tools/sim` + a 2p Screentop
session): *Is the Dead-drop reward tuned so cooperation is rational without a dominant hoard line or
kingmaking?* Concretely:
- **Sim: Hoarder vs Generous-tipper (2p).** Strategy **H** never dead-drops (discards surplus over 7);
  strategy **G** dead-drops every surplus ingredient (to the safest rival) and spends Tips for tempo.
  *Pass:* **G ≥ H** by a small margin. *Fail high (H ≥ G):* Tip reward too weak → raise Insider Tip
  power, or add +1 VP per dead-drop. *Fail low (G ≫ H, or runaway):* dampen the Tip / cap tips per game.
- **Sim: Kingmaker probe (3p).** Measure how much a single player's tip-targeting choice moves the
  win-rate of the *other two*. *Pass:* small. *Fail:* tighten the per-round receive cap or reduce tip
  value.
- If the layer can't be made rational, the logged fallback is **spine B**'s explicit co-op mode (co-op
  as the win condition, not a temptation) on the same components.

**Catch-up / runaway control:** flat VP/turn (no snowball on dish size); the flat Grand Dossier bonus
is a rising tide (doesn't widen gaps); tips naturally flow to trailing players (giver avoids arming the
leader) = mild, organic rubber-banding; **Extract** lets a trailer stop the bleeding, a leader lock the
lead. No heavy-handed leader-bashing.

---

## Player counts & scaling

Base rules are written for **2p** (the design home — a genuine duel). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Menu size** | 4 | 5 | 6 |
| **Grand Dossier milestones** (stamps) | 4 / 8 / 12 / **16** | 6 / 12 / 18 / **24** | 8 / 16 / 24 / **32** |
| **Start positions** | opposite (N & S) | spread on the ring | spread on the ring |
| **Dead-drop cap** | — | ≤1 received / player / round | ≤1 received / player / round |
| **Assignments** | draw 2 keep 1 | draw 2 keep 1 | draw 2 keep 1 |

Dossier thresholds = `[n×2, n×4, n×6, n×8]` (n = player count) so the shared track scales with the
faster plating rate at higher counts and holds ~game length. Menu grows so contention stays fair as more
Agents compete for dishes. Everything else is identical — the same board, recipes, deck, and Assignment
pool carry all counts. **Best-at:** designed for **2p**; 3–4p is a warmer, chattier, slightly longer
race (more table talk, more tip targeting).

---

## Solo mode / Automa

**Low priority given positioning** (Fellowship is a core aesthetic → the game wants ≥2 humans; solo is a
bonus, not a headline). Sketch of a light **"Rival Agent" Automa** if pursued:
- The Automa has a small **Route deck**. On its turn, flip the top card: it either **plates** the
  highest-VP Menu dish it can "afford" against a running ingredient counter (then advances the Dossier),
  **travels** (rotating the region it "controls"), or **dead-drops to you** (hands you a random
  ingredient, takes a Tip) — so the shared layer still breathes solo.
- The Automa's pressure is **tempo**: it plates steadily to push the Dossier's end-clock and to snipe
  Menu dishes you wanted. Difficulty = how aggressively it plates (deck ratio) + a target score to beat.
- Keep upkeep near-zero (one card flip, one lookup). **Defer to `bg-architect`; not in the base MVP.**

---

## Complexity budget

Target **~1.8**; `complexity-budget.json` caps guarded by `bg-elegance`.
- **Component types = 6 → exactly at the cap.** No seventh type; the board absorbs map + Dossier +
  score. New content reuses existing types.
- **Keywords (glossary) = 8, under the 10 cap:** Larder · Menu · Dish · Assignment · Grand Dossier ·
  Insider Tip · Dead-drop · Extract. (Actions — Stock Up / Travel / Plate — and *region / specialty /
  pantry / Traveller's Log* are described in plain language, not defined terms.) **Five of the eight
  keywords are the agent/co-op layer** — that layer is the game's complexity load; it's the signature,
  so it earns its place, but it leaves little headroom. Flag for `bg-elegance`.
- **What gets cut if we drift over:** (1) the HSR shortcut (fold into plain adjacency); (2) Signature
  5-VP dishes (collapse to the 3/4 schedule); (3) the Extract action (let the Dossier's final milestone
  be the sole end-trigger). Depth lives in the Larder-cap ↔ Dead-drop ↔ Dossier interplay, not in the
  count of subsystems — protect that, cut around it.

---

## Keywords / glossary

- **Larder** — your held ingredients (hand). Cap **7**; discard down at end of turn.
- **Menu** — the shared face-up row of Dish cards available to plate; refills from the Dish deck.
- **Dish** — a recipe card (2–3 ingredients) worth VP; plated into your Traveller's Log.
- **Assignment** — your **secret** objective (the one hidden-info hook); +7 VP if completed, revealed at
  scoring.
- **Grand Dossier** — the shared track the whole table advances (+1 per Plate or Dead-drop); milestones
  pay every player a Discovery bonus and the triggerer a bonus Insider Tip; its final milestone can end
  the game.
- **Insider Tip** — a flexible token (extra source / wild ingredient / extra travel hop). Earned by
  Dead-dropping and by triggering Dossier milestones.
- **Dead-drop** — give a rival 1 ingredient; gain 1 Insider Tip and advance the Grand Dossier. The
  cooperation engine.
- **Extract** — the action that triggers the end-game wind-down.

---

## Open questions for playtesting

1. **The knife-edge (top priority).** Is the Dead-drop tuned so cooperation is individually rational
   without a dominant hoard line or kingmaking? → Hoarder-vs-Tipper sim (target **G ≥ H**) + Kingmaker
   probe (3p) + a 2p Screentop session watching whether players *feel* like tipping. Knobs: Insider Tip
   power, a possible +1 VP per dead-drop, the per-round receive cap, the Larder cap.
2. **Grand Dossier teeth.** Is a **flat** Discovery bonus (equal to all) engaging, or does it feel
   ignorable? Options if flat: make milestone payouts **differential** (+1 VP per dish in *your* Log
   matching that region), or keep flat and lean on the trigger-Tip + end-tempo for the strategy. Trades
   warmth vs teeth vs bookkeeping.
3. **Dish VP schedule & Assignment weight.** Is 3 / 4 / 5 flat enough that no dish size dominates, and is
   **+7** the right Assignment swing (too small = ignore your mission; too big = the rest is filler)?
   Also: is 2-ingredient-single-region plating a "just churn cheap dishes" degenerate line?

---

## Handoff notes (guardian sweep)

Mechanics that moved from the locked spine into concrete rules — **where the guardian sweep should
look:**
- **Signature twist (shared Dossier + tip-offs)** is now the **Larder-cap → Dead-drop → Insider Tip →
  Grand Dossier** loop. `bg-theme`: does "sharing a hot tip / catching the last train / the island grand
  tour" still read warm and guest-not-extractor? `bg-elegance`: 6 component types (at cap) and 8 keywords
  (5 of them the agent layer) — is the budget honestly held?
- **Recipes-by-region** is now a concrete region↔ingredient web + the **convenience-store pantry** gag.
  `bg-theme`: Indigenous/Hakka representation in the East/North specialties (consult); `bg-access`: the
  night-market palette must dual-code the 4 region colours + 9 ingredient icons (red/green risk noted).
- **New rule the fiction must still explain:** the **Larder cap** (why can't I carry more? — "you can
  only eat so much / the good stuff spoils / your bag's full") and **Extract** ("catch the last train
  home"). Confirm the fiction covers them.
