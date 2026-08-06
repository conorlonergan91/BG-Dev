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
  of them. Your Larder starts empty and sits **face-up in the open** all game (see below).
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
| **Dead-drop** | your turn + give 1 ingredient | Give **1 ingredient from your Larder to a rival** ("a hot tip on where the good stuff is"). Gain **1 Insider Tip**, score **+1 VP**, and advance the **Grand Dossier +1**. | The cooperation engine. The **+1 VP** (sim-adopted) is what pays for the turn and makes it rational — see *Interaction & tension*. At 3–4p a player may **receive at most 1 Dead-drop per round**. |
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
| **Dead-drop VP (+1 each; sim-adopted fix)** | ~+3–6 | **Yes — this is what makes cooperating rational (see below)** |
| Grand Dossier Discovery bonuses — flat base (2+3+4+5) | +14 to *everyone* | No — a rising tide (the warm co-op *feel*) |
| Grand Dossier **triggerer's pick** (4 milestones × Insider Tip *or* +1 VP) | up to +4 spread across triggerers | **Slightly** — a light race to be the one who crosses a milestone |
| Insider Tips used | soft ~+2–4 | Slightly — efficiency edge |
| **Total** | **~52–58** | Winner decided by dishes + Assignment + **Dead-drop VP** + tip/trigger efficiency |

> **The +1 VP per Dead-drop is the sim-validated fix (adopted 2026-08-06).** As originally written the
> Dead-drop paid only an Insider Tip, and simulation showed hoarding *dominated* (Hoarder 66.8% vs
> Generous 24.0% at 2p) — a full turn spent to arm a rival wasn't worth one Tip. Paying the giver **+1 VP**
> directly covers the turn cost and flips it to rational (**Generous 47.0% vs Hoarder 41.1%** — the target
> "G ≥ H by a small margin"). Kept at **exactly +1** (+2 over-corrects) with the **≤1-received-per-round**
> cap intact. See `playtests/sim-notes.md`.

---

## Scoring / win condition

At game end, each player totals their **Traveller's Log**:
1. **Plated dishes** — sum of VP (3 / 4 / 5).
2. **Assignment** — +7 if completed (revealed now), else 0.
3. **Dead-drop VP** — **+1 VP for each Dead-drop you made** (the sim-adopted fix that makes cooperating
   rational — banked as you go; see the scoring-model note above and `playtests/sim-notes.md`).
4. **Grand Dossier Discovery bonuses (payout C — Hybrid, CD call):** each of the **4 milestones** pays a
   **flat base to every player** (+2 / +3 / +4 / +5 — the celebratory "we did the tour" rising tide, not a
   ranking lever), **and** the player whose Plate/Dead-drop *crossed* that milestone picks **one small
   reward: an Insider Tip *or* +1 VP.** Bank the +1 VP into your Log immediately; it's the only part of
   the Dossier that moves the ranking.
5. **Leftover Insider Tips** — 0 VP (they're leverage, spend them). *(Optional variant: 1 VP per 2
   unused Tips, to remove a "hoard Tips" corner case — flag for sim.)*

Highest total wins. **Tiebreak:** most dishes plated, then furthest-travelled (regions visited).

**Guard against a single dominant strategy:**
- **"Only big dishes":** blocked by flat VP/turn (small dishes are *more* efficient per turn).
- **"Ignore the Dossier / never tip":** *was* the top risk, and the sim showed it dominated as originally
  written — now fixed by the **+1 VP per Dead-drop** (see the scoring-model note): tipping surplus is
  strictly better than discarding, so hoarding drops from dominant to mid-pack.
- **"Point-salad":** avoided — only three real scoring avenues (dishes, one Assignment, shared Dossier).
  The Dossier's flat base is equal-to-all (can't be gamed into a runaway); only its small **triggerer's
  pick** (max +4 VP across the whole game, spread across whoever crosses milestones) touches the ranking.

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

**One hidden-information hook only — the Larder is PUBLIC** (bg-elegance ruling, applied). Every player's
**Larder sits face-up in the open**; ingredients are never a concealed hand. The **only** hidden
information in the game is your secret **Assignment**. This is deliberate: a concealed Larder would smuggle
in a *second* hidden layer (rivals deducing your recipe from a hidden hand) — exactly the deduction engine
the ~1.8 budget forbids. Making the Larder public *sharpens* the intended read: rivals can see **what** you
hold but not **why** (which Assignment it serves), so the single hidden hook does all the concealment work.
**Nothing else in the spec depends on the Larder being secret** — the Dead-drop's decision is the giver's
own choice (they pick recipient and ingredient), the Menu race is open, and the "is their beef-run a real
op or a feint?" tension lives entirely in the hidden **Assignment**, not the visible ingredients.

---

## Interaction & tension

**Indirect (the spine):**
- **The Menu race** — a rival can plate the dish you were routing toward (light "grab it first"
  tension; the reason to watch the board).
- **The Grand Dossier trigger-race** (payout C) — being the player whose Plate/Dead-drop *crosses* a
  milestone lets you pick a small prize (**an Insider Tip *or* +1 VP**) inside the shared payout. It adds
  a light "be the one to tip it over" race — see the runaway/kingmaking check below.
- **End-tempo** — **Extract** and the Dossier's final milestone are levers on when the game ends; a
  leader wants to end it, a trailer wants more turns.

**Direct-but-warm:** the **Dead-drop** — you literally hand a rival an ingredient. Framed as generosity
("you HAVE to try this"), it's the Fellowship mechanic and the crux of the semi-co-op knife-edge.

### Making cooperation individually rational (designing the top risk out)

The failure modes to beat: **(1)** "hoard, never tip" dominates → dead co-op sticker; **(2)** kingmaking
→ tips arbitrarily decide the winner. Here is exactly why neither should happen, with the numbers:

**Why tipping is rational (beats "always hoard") — corrected by the sim.** The original theory below
*over-valued* the Insider Tip: it assumed Tip + Dossier ≈ enough to justify the turn. **Simulation
falsified that** — a Dead-drop costs a *whole turn* plus arms a rival plus speeds the end-clock, and one
Tip didn't cover it, so hoarding dominated (66.8% vs 24.0%). The **+1 VP per Dead-drop** (adopted) is the
piece that actually closes the gap:
- The **Larder cap of 7** forces surplus. A surplus ingredient you'd otherwise **discard for nothing** is
  now **dead-dropped for +1 VP + 1 Insider Tip + a Grand Dossier step** — **strictly, clearly** better
  than discarding.
- Net for the giver on a **surplus** tip: **+1 VP (banked, theirs) + 1 Insider Tip + fractional Dossier
  push − a soon-dead ingredient.** The **+1 VP is the load-bearing term** — it pays the turn directly.
  Sim result with the fix: **Generous 47.0% vs Hoarder 41.1%** (rational, no runaway).
- Net for the giver on a **useful** (non-surplus) tip: **+1 VP +Tip +Dossier − (a needed ingredient) ≈
  still marginal**, and the receiver may net more — so a rational player still *won't* hand a threatening
  rival something they need. That stays the **interesting** decision (tip a trailing rival for the VP +
  goodwill / Dossier timing; don't arm the leader), not a dominant "spam dead-drops" line — though the
  human session should watch for VP-farming; fallback = restrict the +1 VP to at-cap/surplus drops.

**Why it isn't kingmaking:**
- **At 2p there is no kingmaking** (one rival). The decision is cleanly "does my Tip + Dossier gain beat
  the help I give my only opponent?" — yes for surplus, a judgement call for useful. Clean duel.
- **At 3–4p:** the giver **chooses recipient and ingredient**, and the reward (the Insider Tip) is
  **theirs regardless of recipient** — so the incentive is self-focused, not "boost my ally." A player
  may **receive at most one Dead-drop per round** (no gang-feeding a kingmade player). The help is small
  (1 ingredient) relative to the giver's flexible Tip, so tips rarely swing *who wins*.

**The payout-C triggerer's pick — runaway / kingmaking check.** The Hybrid reward adds a light race to be
the player who *crosses* a milestone (pick an Insider Tip or +1 VP). Two effects to watch:
- **Runaway:** a leader plates fastest, so they tend to trigger more milestones and collect more picks —
  a mild positive-feedback nudge toward the leader. It is **deliberately tiny and hard-capped: only 4
  triggers exist all game, worth ≤+1 VP each (≤+4 VP total, split across whoever triggers).** That's well
  under one dish's swing and far under the +7 Assignment, so it can flavour tempo without snowballing. If
  sim shows a leader routinely sweeping most of the 4 picks *and* converting that into wins, the fix is to
  cap it (e.g., a player may claim **at most 2** triggerer-picks per game) or drop the +1-VP option so the
  pick is only an Insider Tip (reverting toward payout A).
- **Kingmaking (3–4p):** the pick goes to the **triggerer themselves**, never to a chosen rival, so it
  creates **no "boost my ally" lever** — it can't kingmake directly. The only indirect angle is a trailing
  player deliberately *timing* a Dead-drop to deny a leader a milestone pick; that's legitimate tempo play,
  not kingmaking.
- **Sim task (add to the run):** track **milestone-trigger share vs finishing position** — does the eventual
  winner claim a disproportionate share of the 4 picks (runaway signal)? And does the +1-VP option ever
  decide a game on its own (margin ≤ the picks claimed)? *Pass:* picks are spread and rarely decisive.
  *Fail:* apply the per-player pick cap or drop the +1-VP option.

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

- **Larder** — your ingredients, sat **face-up in the open** in front of you (**not** a hidden hand).
  Cap **7**; discard down at end of turn.
- **Menu** — the shared face-up row of Dish cards available to plate; refills from the Dish deck.
- **Dish** — a recipe card (2–3 ingredients) worth VP; plated into your Traveller's Log.
- **Assignment** — your **secret** objective (the one hidden-info hook); +7 VP if completed, revealed at
  scoring.
- **Grand Dossier** — the shared track the whole table advances (+1 per Plate or Dead-drop); each
  milestone pays every player a flat Discovery bonus **and** lets the triggerer pick a small reward
  (an Insider Tip *or* +1 VP — payout C); its final milestone can end the game.
- **Insider Tip** — a flexible token (extra source / wild ingredient / extra travel hop). Earned by
  Dead-dropping and by triggering Dossier milestones.
- **Dead-drop** — give a rival 1 ingredient; **score +1 VP**, gain 1 Insider Tip, and advance the Grand
  Dossier. The cooperation engine (the +1 VP is the sim-adopted fix that makes it rational).
- **Extract** — the action that triggers the end-game wind-down.

---

## Open questions for playtesting

1. **The knife-edge — SIM-RESOLVED, now a feel-test.** Is the Dead-drop tuned so cooperation is
   individually rational without a dominant hoard line or kingmaking? **Sim verdict:** as originally
   written it FAILED (Hoarder 66.8% vs Generous 24.0%); **+1 VP per Dead-drop** (adopted) flips it to a
   PASS (Generous 47.0% vs Hoarder 41.1%), with kingmaking bounded (~3pt) and payout-C picks non-decisive
   (~2.6%). The **only remaining question is the human one the sim can't judge**: does tipping now *feel*
   worth it, and is "arm my rival?" a live decision? → a 2p Screentop session. Also watch for **VP-farming**
   (spamming Dead-drops of non-surplus just for the +1 VP); fallback = restrict the +1 VP to at-cap/surplus
   drops, or cap dead-drops/round.
2. **Grand Dossier teeth (payout C, CD-chosen).** The Hybrid gives the flat base *plus* a triggerer's
   pick (Insider Tip or +1 VP). Does the pick add a satisfying "tip it over" race without a leader-runaway
   (see the check above)? Watch **milestone-trigger share vs finishing position**. If the pick proves
   ignorable, strengthen it (raise the +1-VP option); if it snowballs to the leader, cap it at 2 picks per
   player or drop the +1-VP option toward flat (payout A).
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
