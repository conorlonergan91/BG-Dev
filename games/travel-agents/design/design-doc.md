# Travel Agents: Taiwan — Design Doc (v2)

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.
**Interaction model C "Rivals on a Living Island" (LOCKED, 2026-08-06).** Slug `travel-agents`.
Supersedes v1 (spine A "Rival Agents, Shared Beat"): the sourcing engine is retained; the co-op
tip-economy is **cut** and replaced by a direct rival contest + a living-island event layer.

> **Fiction labels (CD re-skin, 2026-08-06):** the players are rival **travel agents** building the
> best Taiwan foodie **tour**, who comedically *behave* like covert agents. Mechanics below are model C
> **unchanged**; only the theme names change. Where a name is `bg-theme`'s to finalise against
> `identity.md` it's flagged *[fiction → bg-theme]*. Mechanically-neutral labels kept from v1
> (Larder / Menu / Dish / Stock Up / Travel / Plate) are unchanged.

> **One-line frame:** two rival travel agents race to build the best Taiwan food **tour** — source real
> ingredients from the regions that supply them and **Plate** the island's great dishes into your tour,
> while you both race to lock the same **Hot-List** spots, chase a **secret signature itinerary**, and
> ride an island that won't sit still (festivals open windows, typhoons shut roads). Most impressive
> tour is named **Top Agent**.

---

## What changed from v1 (the model-C swap, for `bg-elegance`)

This is a **swap, not a pile-on.** Honest ledger:

| Cut (−) | Added (+) |
|---------|-----------|
| **Dead-drop** action (keyword + rule) | **Hot-List** — a public race-to-claim row (reuses the Operation card type) |
| **Insider Tip** tokens + spend rules (keyword + **component type**) | **Conditions** — a lean, telegraphed island-event deck |
| **Flat Grand Dossier payout** (+2/3/4/5 to all) + **triggerer's-pick** sub-race (a scoring line + a mini-race) | **Briefs** — a *minimal* head-office directive set (boost / risky gamble / light nudge) |
| The "is helping a rival rational?" **balance knife-edge** (sim had to bribe it with +1 VP) | A **live VP tracker** (open score raced in the open) |

Net: we retire **2 keywords** (Dead-drop, Insider Tip), **one whole scoring line** (flat Dossier
payout), and **one balance knife-edge**; we add **2–3 keywords** (Hot-List, Condition, Brief). The
Insider Tip's flexible-leverage job (extra source / wild / extra hop) is **re-homed into the Briefs**,
so no capability is lost. Actions drop from **5 → 4** (Stock Up / Travel / Plate / Extract; claiming a
Hot-List spot rides on a Plate, and playing a Brief is free). See *Complexity budget* for the weight
call.

---

## Design goals

- **Target weight ~2.0–2.1, ceiling 2.2** (`complexity-budget.json`; `bg-elegance` guards). The
  interaction layer is deliberately growing from v1's ~1.8, so **every addition must earn its rules** —
  we take the two highest interaction-per-rule pieces (Hot-List + Conditions) and keep Briefs *minimal*.
- **2-player first.** Every new interaction is designed to be fun *head-to-head*; 3–4p is a scaling
  delta, not a redesign. The sharpest, most resentment-prone case (a two-person snipe) is the one we
  design and sim against.
- **Aesthetics (locked, `identity.md`):** **Discovery (lead)** — the island reveals & remakes itself
  (Conditions) and the Menu/Hot-List reveal; **Fellowship** — carried now by *shared island drama +
  warm rivalry banter*, not mechanical co-op (per `identity.md`'s own definition of Fellowship);
  **Challenge** — a light two-front routing puzzle (race the Hot-List *and* the shifting island).
- **The meaningful decision every turn:** *source toward my next Dish, race the rival to a Hot-List
  spot, or bank my lead and wrap the tour?* — under an island whose next **Condition** you can already
  see coming. No forced/obvious move (Travel always arrives with something; the Menu/Hot-List/Condition
  interplay keeps every turn live).
- **Taiwan does real work** (unchanged v1 strength): the region↔ingredient↔dish web is real food
  geography — rename the setting and the recipes break. Real dishes, Tâi-lô primary + 繁體, never mangled.
- **Design the top risk out:** make the **Hot-List race fun-tense**, not resentment-on-snipe or a
  leader-runaway (see *Interaction & tension* and *Riskiest assumption*).

---

## Core loop (detailed)

A turn is **one action** from four; short turns, low downtime (crucial at 2p). Each cycle you optimise:
*which ingredients do I still need for my next Dish / to lock a Hot-List spot / to advance my secret
Signature Itinerary — and is the island's current **Condition** telling me to hurry or reroute?*

1. **Read the board.** Your **secret signature itinerary** *[fiction → bg-theme; was secret Operation]*
   points at a shape of tour (a regional crawl, a variety tour, two hero dishes…). The face-up **Menu**
   shows plate-able Dishes. The **Hot-List** shows the public bonus tours both agents are racing to lock
   in. The **Season** clock shows how close the tour is to the next **Condition** — and to the end. The
   **active Condition** (and the *next* one, previewed) is modifying what's valuable where.
2. **Source what you need.** *Stock Up* (2 ingredients where you stand) or *Travel* (move one region,
   arrive with 1). You can only take a region's **specialty** in that region; **pantry** supplies are
   available anywhere (the convenience store). The active Condition may boost, tax, or block a region.
3. **Plate a Dish.** Spend a Menu Dish's recipe from your **Larder** → the Dish enters your tour (your
   Traveller's Log) for its VP (**tracked live** on the score track), the **Season** advances **+1**,
   and — as a **free rider** — you immediately **lock in** any Hot-List spot your tour now completes
   (score it live; Season **+1**; refill the Hot-List). Then check your secret Signature Itinerary
   quietly (it stays face-down).
4. **The island turns.** Whenever a Plate / lock-in pushes the Season across a **milestone**, the active
   Condition ends, the previewed one becomes active, and a new Condition is drawn to the preview slot
   (the telegraph). ~4–5 Conditions fire across a 2p game.
5. **Decide when to wrap.** When your lead looks set, **Extract** ("file the finished tour / catch the
   last train home") to trigger the wind-down — or let the Season reach its final milestone.

The loop compounds gently and legibly: plating faster advances the Season (turning the island and
firing Conditions), and locks Hot-List spots before your rival — but it also **hurries the end-clock**,
so a leader racing to lock spots is also shortening the game a trailer needs. That tension is the
built-in rubber-band (see *Interaction & tension*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** (4 regions on a ring: North 北 – Central 中 – South 南 – East 東; an
  **HSR** spine links North–Central–South down the west coast). The board also carries the **Season
  clock**, the **VP score track**, the **Hot-List row (3 slots)**, and the **Condition queue (2 slots:
  ACTIVE + NEXT)**.
- Build the two Operation sub-decks (same card type): shuffle the **Hot-List deck** and the **Sealed
  deck** separately.
- Deal the **Menu**: 4 face-up Dish cards. Deal the **Hot-List**: **3** face-up Operation cards.
- Seed the **Condition queue**: draw 1 to ACTIVE, 1 to NEXT (both face-up).
- Each player: take an **Agent** pawn (start on opposite regions — one North, one South) and a **VP
  marker** on the score track at 0; draw **2 Sealed Operations, keep 1** as your **secret signature
  itinerary** (return the other, face-down); take your empty tour (Traveller's Log) area. Your Larder
  starts empty and sits **face-up in the open** all game.
- **Briefs (scope = CD decision, see below):** deal each agent a small opening hand of **Briefs**
  (default 3). Larder empty. Season marker at 0.

**A turn = choose ONE action:** **Stock Up**, **Travel**, **Plate**, or **Extract** (detailed in
*Actions*). At the appropriate moment you may also **play one Brief** (free, not an action) and, riding
on a Plate, **lock in** any completed Hot-List spot (free). Then, if your Larder exceeds 7, discard down
to 7. Play passes clockwise.

**End-trigger (either path, unchanged from v1):**
- A player takes the **Extract** action, **or**
- The **Season** reaches its **final milestone**.

Either way: **finish the current round** (equal turns for all), then play **one more full round**, then
**score**. (A fair, unswingy wind-down.)

Target length: **~35–45 min at 2p**, roughly **18–24 turns per player**.

---

## Actions

| Action | Cost | Effect | Notes |
|--------|------|--------|-------|
| **Stock Up** | your turn | Take **2 ingredients** available at your current region (this region's **specialties** and/or **pantry**). The active **Condition** may add/tax this. | The workhorse. Frictionless (open supply). |
| **Travel** | your turn | Move your Agent to an **adjacent** region on the ring; on arrival, take **1 ingredient** there. (HSR: North↔South counts as adjacent.) Conditions may block/tax a region — see *Conditions*. | Never a dead turn — you always arrive with something. |
| **Plate** | your turn + spend a recipe from Larder | Choose a **Menu** Dish you can afford; return its recipe ingredients to supply; add the Dish to your tour (VP scored **live** on the track); refill the Menu. **Season +1.** Then **lock in** (free) any Hot-List spot your tour now completes (see below). | The scoring engine + the trigger for both the Hot-List race and the Season/Condition clock. |
| **Extract** | your turn | Trigger the end-game wind-down (finish the round + one more full round). Your secret Signature Itinerary stays face-down until scoring. | Push-your-luck tempo: wrap while ahead vs plate/lock one more. |
| *(free, not an action)* **Lock in a Hot-List spot** | — (rides on a Plate) | The instant your tour satisfies a face-up Hot-List spot's condition, take that card into your tour for its VP (scored **live**), **Season +1**, and refill the Hot-List from its deck. Multiple may lock in one turn. | The direct rival race. First to satisfy-and-lock takes it; the rival is shut out of *that* spot but the refill gives a fresh target. |
| *(free, not an action)* **Play a Brief** | discard the Brief | One-shot head-office directive: a safe self-boost, a risky self-gamble, or a light keep-your-rival-honest nudge (see *Briefs*). Max **one Brief per turn**. | The Insider Tip's flexible-leverage role, re-homed + given the Chief's/head-office voice. |

Every turn has multiple live options with real trade-offs (source-what-I-need vs race a Hot-List spot
vs plate-now-and-turn-the-island vs wrap-it), all under a telegraphed, shifting Condition. No
forced/obvious move.

---

## Components

| Component | Qty | Notes |
|-----------|-----|-------|
| **Map board** (Taiwan) | 1 | 4 regions on a ring + HSR spine; **Season clock**, **VP score track**, **Hot-List row (3 slots)** and **Condition queue (2 slots)** all printed on the one board. |
| **Dish cards** | ~24–30 | Recipe (ingredient icons) + VP + name (Tâi-lô + 繁體) + region tag. (v1 has 24; East pending + chicken/egg dishes incoming → grows toward ~30.) |
| **Operation cards** *(one type, two decks)* | ~26–30 | **Sealed deck** (~10–12): secret Signature Itineraries, +7, draw-2-keep-1. **Hot-List deck** (~14–18): public bonus tours, **4–6 VP**, dealt face-up. Same card stock/type — *reuses v1's Assignment type, no new component for the whole Hot-List race.* |
| **Condition cards** | ~10–14 | The living-island event deck (festivals / weather / roads / warm characters). Small — ~4–5 fire per game. **New component type.** |
| **Brief cards** | ~10–14 | Head-office directive deck (boost / risky gamble / light nudge). *Scope = CD decision; may collapse to a printed mini-set (no deck) — see below.* **New component type (in the deck version).** |
| **Ingredient tokens** | ~130–150 | Region **specialties** + fungible **pantry**. Adding **chicken 雞** + **egg 蛋** (see *Ingredients*). Open supply. |
| **Agent pawns + VP markers** | 4 + 4 | Pawns on the map; markers on the VP track. (Markers are bits on the board's track — not a distinct "type.") |

**Component types = 7** (board / Dish cards / Operation cards / Condition cards / Brief cards /
ingredient tokens / pawns): **one over v1's 6-type cap.** We *cut* Insider Tip tokens (−1) and *add*
Condition + Brief decks (+2). The CD has explicitly softened this cap (cost is fun-first; a 7th type is
fine when the game needs it — `decision-log`, 2026-08-06). **The Brief deck is the 7th type**, so the
CD's Briefs-scope decision (below) is *also* the "do we cross 7 types" decision: fixed-set/fold Briefs →
back to **6 types**. Flagged honestly to `bg-elegance` / `bg-architect`. Conditions and Briefs are kept
as **separate decks on purpose** — `identity.md`'s binding rail is that **head-office directives (from
within) must not blur with island conditions (that happen to you)**; merging them is a sensitivity
regression, not an elegance win.

### Ingredients — the region↔ingredient web (the Taiwan engine, retained + extended)

v1's web (8 specialties, 2 per region, + fungible pantry) is retained. **New ingredients from the
locked North dishes** (雞排 / 火雞肉飯 / 卡拉雞腿堡 / 蛋餅): **chicken 雞** and **egg 蛋**.

**Framework rule (systems-level; exact list finalised by `bg-developer` — East still pending):**
- Every region must remain the **sole source of ≥1 ingredient that appears in cross-region Dishes**, so
  Travel stays motivated — this is the non-negotiable that keeps the "travel because the food lives
  there" engine alive. A region may carry **2–4 specialties**; do **not** let any one region become so
  self-sufficient that a player can build a whole tour without leaving it (that kills routing).
- **chicken 雞** → recommend a **North specialty** (雞排 night-market; 卡拉雞腿堡 breakfast-shop; Chiayi
  火雞肉飯 is southern-adjacent — a possible South/North bridge Dish, a `bg-developer` call).
- **egg 蛋** → two clean options, a **data call, not a systems blocker**: (a) a **North specialty**
  (breakfast-shop identity), or (b) a **second everyday token alongside pantry** (egg is ubiquitous;
  茶葉蛋 / 蛋餅 both use it). Recommend **(a)** so North's breakfast-shop character earns a real token
  and North doesn't over-rely on pantry — but if North then reads as too self-sufficient, fall to (b).
- **Watch:** North now holds beef/pork/chicken(/egg) → richest region. Keep enough **cross-region**
  Dishes pulling North ingredients *out* to other regions (滷肉飯 N+E, 池上便當 E+N, etc.) so North isn't
  a stay-home trap. `bg-developer` to keep cross-region ≥ ~25% (geography-capped, as v1).

> **Sensitivity note (binds — see `identity.md`):** East specialties draw on **Indigenous** cuisines —
> generic, respectful labels ("mountain rice / wild greens"), consultant before art/print. Dishes named
> Tâi-lô + 繁體, never mangled. The travel-agent re-skin is **net safer**: agents *promote* Taiwan's food
> to clients — advocacy, not extraction.

### Dishes — recipes (v1 exemplars retained; deck grows with North + East)

Unchanged model: a Dish = **specialties (region-locked) + at most 1 pantry**. VP: **2-ingredient = 3 ·
3-ingredient = 4 · Signature (3 specialties, 3 regions) = 5**. (Full data in `components/dishes.csv`;
North chicken/egg Dishes and the East set are being finalised separately — design here is at the
systems level and does not block on the final list.)

### Operations — the Hot-List (public race) + the Sealed Signature Itinerary (secret +7)

**One card type, two grades printed on the card**, both drawn from the objective families below
(crawl / variety / obsession / big-eater / volume — same as v1's Assignments):

| Grade | Where | Count in play | VP | Info |
|-------|-------|--------------:|----|------|
| **Sealed Signature Itinerary** | secret, in front of each player | 1 / player | **+7** (binary) | **Hidden** until scoring — the one hidden hook, the dramatic reveal. |
| **Hot-List spot** | face-up on the board | **3** (2p) | **4–6** (by difficulty) | **Public** — both agents see it and race to complete-and-lock. |

- **Hot-List VP scaling:** 2-dish condition = **4**; 3-dish = **5**; a breadth/harder condition = **6**.
  Kept **below the +7 Sealed** so the secret itinerary stays the headline and the public race is the
  supporting contest, not the whole game.
- **A single plated Dish can count toward your Sealed Itinerary *and* one-or-more Hot-List spots
  simultaneously** (your tour is evaluated against every condition). This is deliberate: it makes
  routing decisions richer ("this oyster Dish advances my secret Southern crawl *and* lets me snipe the
  oyster Hot-List spot") and raises payoff density with **zero extra rules**.
- **Hot-List conditions skew to the faster/legible end** (2–3 dishes, readable "she's one oyster Dish
  away"); Sealed itineraries can be meatier (~2–4 dishes) since they're your private +7 headline.

### Conditions — the living-island event deck (Discovery + the shared drama)

A **lean, telegraphed** deck. **Trigger:** each **Season milestone** ends the ACTIVE Condition, slides
NEXT into ACTIVE, and draws a new NEXT (always previewed face-up). The preview is the agency-preserver —
you *see the storm coming* and route around it, or the festival coming and race toward it. Three
families, **secular only** (binding rail):

| Family | Effect shape | Scope | Fun |
|--------|--------------|-------|-----|
| **Festival (window opens)** | a region's specialty stocks +1 extra / its Dishes plated this window score +1 VP | one region (or table-wide) | a **hotspot both agents suddenly want** → turns the map live; contention amplifier |
| **Hazard (window shuts/taxes)** | Travel into a region costs +1 step this window, or its specialty costs your whole turn to take 1 (delay-not-destroy; prefer **tax** over hard **block**) | one region / a named pass | shared "oh no, typhoon!" reroute drama; the *island* is the antagonist, never a rival |
| **Warm character (one-off boon)** | resolve once, **symmetrically** (each agent gains the same) | table-wide | the warm heart; generous hosts, never a punchline |

**Starter set (~8; wording via the Taiwanese consultant before lock):**
1. **芒果季 Mango Season** *(festival, South)* — Dishes using a Southern ingredient plated this window
   score **+1 VP**.
2. **珍奶節 Bubble-Tea Festival** *(festival, Central)* — when you Stock Up in Central, take **+1** extra.
3. **豐收 Bumper Harvest** *(festival, East)* — when you Stock Up in the East, take **+1** extra.
4. **夜市週年慶 Night-Market Anniversary** *(festival, table-wide)* — the **first Dish each agent plates**
   this window scores **+1 VP**.
5. **颱風 Typhoon** *(hazard, East coast)* — Travelling **into the East** costs **+1 step** this window
   (tax, not block — you can still get there, it just costs tempo).
6. **土石流 Landslide** *(hazard, a mountain pass)* — Travel between **Central↔East** (the cross-island
   link) is closed this window; use the ring the long way.
7. **熱心阿姨 The Generous Auntie** *(warm one-off)* — each agent immediately takes **1 free ingredient**
   of the ACTIVE region's specialty ("she insists you take one more").
8. **送貨小哥 The Scooter Kid** *(warm one-off)* — each agent may immediately move their Agent **1 region
   for free** (a lift to the next town).

> **Venues = flavour only (not a subsystem).** Venue vocabulary rides on Conditions for free: "the
> **breakfast shop** runs a 蛋餅 special," "the **dessert** stall's 芒果冰 is the festival," "the **night
> market** throws its anniversary." No venue rules — it scored worst on fun-per-rule (exploration §4).
>
> **Sensitivity (binding):** **secular only** — festivals are food/fruit-season/market/road/weather
> events; **NO** temple/deity/ghost-month/funerary content as mechanics or gags. Characters are
> **dignified, varied hosts**, never obstacles-as-punchline. Hazards are **comic inconveniences**, never
> disaster-porn. Consultant reviews the full list before art/print.

### Briefs — the head-office directive set (minimal; scope = CD decision)

*[fiction → bg-theme; "Briefs / head-office memos / client briefs" for the v1 "Orders"]* The three
flavours the CD wants, **bounded to delay-not-destroy** and kept deliberately small:

| Brief | Flavour | Effect (examples) | Bounding |
|-------|---------|-------------------|----------|
| **"Free Sample" / Priority Clearance** | safe self-boost | choose one: take **1 extra ingredient** here · treat **1 recipe ingredient as wild** this Plate · **Travel +1** region | self-only (re-homes the cut Insider Tip's flexibility) |
| **"Deep Cover" / All-In** | **risky self-gamble** (the risk-reward the CD wants — an *input* gamble, no dice) | discard **2 ingredients now** (or skip your next Stock Up), then your **next Plate scores +2 VP** (or your next Hot-List lock-in +2) | self-only; the downside is real and immediate, the upside deferred |
| **"Sold Out!" / Beat You To It** | **light keep-rival-honest nudge** (warm sibling prank) | name a region; your rival **can't take that region's specialty on their next turn** ("the good stall's sold out") | **one-turn DELAY, never destroy**: never removes VP/ingredients/a whole turn · **symmetric access** (same deck/set) · **capped** at one Brief/turn, no chaining the same target |

**How few / how held / how played (the minimal default the doc specs):** an **opening hand of 3
Briefs** per agent (a one-time "briefing packet" — no ongoing draw engine, no sub-economy). Play **one
per turn max**, free (not an action); discard when used. That's your whole supply for the game. This is
the *minimal* Model-C dose — enough spice to answer "more direct interaction" without paying for a full
Orders economy (that's the Model-B upgrade path). **See the CD decision** for whether to trim this
further (fixed printed set → drops the 7th component type) or keep the small deck.

---

## Economy & math

**Sourcing throughput (unchanged).** Stock Up = +2 ingredients; Travel = +1 (and reposition). A typical
3-ingredient cross-region Dish takes ~3 turns to assemble+plate; a 2-ingredient single-region Dish ~2.

**VP per turn (the anti-dominant-strategy check, unchanged).** Kept flat-ish so no Dish size dominates:

| Dish | VP | ~Turns to make+plate | VP/turn |
|------|----|--------------------:|--------:|
| 2-ingredient | 3 | 2 | **1.50** |
| 3-ingredient | 4 | 3 | **1.33** |
| Signature (3-region) | 5 | ~4 | **1.25** |

Small Dishes stay marginally more efficient/turn, so big Dishes aren't an auto-win — they're justified
by Sealed-itinerary / Hot-List synergy, not raw rate.

**Larder cap = 7 (retained).** Still forces the source→plate rhythm and prevents hoarding a burst; the
**risky-gamble Brief** ("discard 2 → next Plate +2") now provides the "convert dead weight into
leverage" decision the sim liked (the job the Dead-drop used to do), minus the paid-gift weirdness.
Thematic justification unchanged: travel light, eat fresh.

**The Season clock (repurposed).** Advances **+1 per Plate** and **+1 per Hot-List lock-in**. Milestones
**fire Conditions** (they no longer pay VP). First-pass 2p schedule — *a sim/feel tuning knob:*

| | milestone marks (fire a Condition) | final (ends game) |
|-|-|-|
| **2p** | 4 · 8 · 12 · 16 | **~20–24** |

So a 2p game (~8–9 Plates + ~4–6 lock-ins per player-pair over the pair… ≈ 20–26 advances) fires **~4–5
Conditions** — a rhythm, not a barrage. Scale by count (see *Player counts*).

**Target 2p score (winner ~50–55 VP; the VP track sized 0–~55):**

| Source | ~VP | On the live tracker? |
|--------|----:|----------------------|
| Plated Dishes (~8–9 × ~3.3) | 28–30 | **Yes — live** |
| Hot-List spots locked (~2–3 × ~5) | 10–15 | **Yes — live** |
| Condition/Brief VP gains | +3–6 | **Yes — live** |
| **Secret Signature Itinerary** | **0 / 7** | **NO — face-down until the end (the reveal)** |
| **Total** | **~50–55** | winner = Dishes + Hot-List + event/brief gains + the hidden +7 |

**Balance assumptions (to attack with sim + Screentop):** (1) Hot-List spots split roughly evenly at 2p
(no runaway); (2) 4–6 VP each keeps the race meaningful but sub-headline to the +7; (3) ~4–5 Conditions
per game is enough to vary routing game-to-game without any single hazard erasing a planned plate;
(4) the minimal Brief set adds a gotcha or two without a slap-fight.

---

## Scoring / win condition — "Top Agent"

At game end each agent totals their tour (Traveller's Log):
1. **Plated Dishes** — sum of VP (3 / 4 / 5). *(Tracked live.)*
2. **Hot-List spots locked** — sum of VP (4–6 each). *(Tracked live.)*
3. **Condition / Brief VP gains** — any +VP earned along the way. *(Tracked live.)*
4. **Secret Signature Itinerary** — **+7 if completed** (revealed now), else 0. *(The one thing NOT on
   the live tracker — face-down until this reveal, so it stays a moment.)*

Highest total is named **Top Agent of the Year** *[title fluid → bg-theme/consultant]*. **Tiebreak:**
most Hot-List spots locked, then most Dishes plated, then most regions visited.

**The VP tracker (CD request, spec'd as a board element).** A **score track** printed along the board
edge (0–~55) with **one marker per player**. **All open VP is tracked live as earned** — every Plate,
lock-in, and event/brief gain moves your marker immediately. This makes the race **legible and tense**:
you always see who's ahead, which is exactly what fuels the Extract-vs-push end decision (and the
anti-runaway rubber-band — a trailer *sees* they need more turns). The **only** off-tracker VP is the
Sealed Signature Itinerary (+7), held face-down to keep the endgame reveal a genuine swing and to keep
hope alive for a visibly-trailing player.

**Guard against a single dominant strategy:**
- **"Only big Dishes":** blocked by flat VP/turn (small Dishes are *more* efficient/turn).
- **"Ignore the Hot-List, just build my own tour":** viable but not dominant — Hot-List spots overlap
  the Dishes you'd plate anyway, so ignoring them leaves ~10–15 VP on the table for the rival. The
  question the sim must answer is the *opposite* (does a greedy Hot-List-chaser run away — see below).
- **"Point-salad":** avoided — three open avenues (Dishes, Hot-List, small event/brief gains) + one
  hidden (the +7), all pulling on the *same* plated Dishes. No orthogonal salad axis (venues were cut).

---

## Randomness

- **Input randomness only** (preserves agency, per `design-fundamentals.md`):
  - The **Menu** reveal, the **Hot-List** reveal, the **Condition queue** (all telegraphed/face-up — you
    *adapt* to what's revealed). The Condition **preview** (NEXT slot) is the key agency-preserver.
  - Your **Sealed Itinerary** draw — mitigated by **draw-2-keep-1**.
  - **Brief** hand draw; deck orders.
- **No output randomness.** No dice, no post-decision luck. Suits the warm "nail your trip" tone and
  keeps skill legible at ~2.0 without swing.

**One hidden-information hook only — everything else is open** (v1 ruling retained). Larder is
face-up; the Hot-List, both tours, and the VP tracker are all open. The **only** hidden information is
your **Sealed Signature Itinerary**. Rivals see *what* you hold and plate but not *which secret tour it
serves* — the single hidden hook does all the concealment work; no deduction engine.

---

## Interaction & tension

**Direct (the new spine):**
- **The Hot-List race** — the headline new interaction. A public row both agents complete-and-lock from;
  first to satisfy a spot's condition locks it, denying the rival *that* spot (a fresh one refills). The
  race lives in **routing prioritisation** — "she's one oyster Dish from the seafood spot; I'll grab the
  variety spot first, or race her South." Razor-sharp and legible at exactly 2 players.
- **Briefs** — a light, bounded, direct lever (a self-gamble or a one-turn "sold out" nudge) — the
  affectionate gotcha the co-op v1 lacked.

**Indirect (retained):**
- **The Menu race** — a rival can plate the Dish you were routing toward.
- **The Season/Condition clock** — plating turns the island (fires the next Condition); a player can
  *time* a Plate to flip the season toward a festival they want or delay one they don't.
- **End-tempo** — **Extract** and the Season's final milestone are levers on when the game ends.

**Fellowship after cutting co-op (the §0 wager, per `identity.md`):** carried by **shared island drama**
(the table groaning together at a typhoon, cheering a festival) + **warm rivalry banter** over the
Hot-List ("you did *not* just lock my oyster spot") + the light warm Brief nudge. This matches
`identity.md`'s *own* definition of Fellowship ("warm rivalry + table talk"), not mechanical co-op.

### Designing the top risk out — the Hot-List race must be *fun-tense*

Two failure modes to beat: **(a) resentment-on-snipe** (a permanent claim stings more than losing a
refillable Menu card) and **(b) leader-runaway** (leader plates faster → locks more spots → snowballs).
The rules that keep it fair:

1. **Refilling shared pool (3 face-up).** You're rarely robbed of your *only* option — a sniped spot
   refills with a new target, and your Dishes still count toward it. (Contrast: v1's single contested
   Menu row.)
2. **A snipe never wastes your plated Dishes (the structural anti-resentment move).** The same Dishes
   that were racing a sniped spot **still scored their base VP, still advance your Sealed Itinerary, and
   still count toward the next Hot-List spot.** The snipe costs you a *bonus*, not your *plan*. This is
   the load-bearing reason a snipe reads as "outraced," not "robbed."
3. **Fully open information.** Board + both tours + the **live VP tracker** are all face-up, so a snipe
   is a race you **saw coming and lost**, not a hidden ambush. Open information is the standard defuser
   of take-that resentment.
4. **Modest, bounded swing.** Spots are 4–6 VP (below the +7 headline) and only ~4–6 lock across a whole
   game → the total Hot-List swing is bounded well under the game's decision margin.
5. **Anti-runaway via the clock.** A leader racing to lock spots also **advances the Season → hurries
   the end** a trailer needs; a trailer can push for more turns / grab the breadth spot while the leader
   is committed. **Extract** lets a trailer stop the bleeding or a leader lock the lead. Organic
   rubber-band, no leader-bashing. Tuning knobs held in reserve if the sim flags snowball: a **per-player
   lock cap**, a **trailing-player discount** (trailer completes a spot with one fewer Dish), or **faster
   Hot-List refresh**.

**Catch-up / runaway control overall:** flat VP/turn (no snowball on Dish size); the Season clock ties a
leader's tempo to a faster endgame (built-in valve); Conditions act **symmetrically** on both agents;
Briefs are bounded delay-not-destroy.

---

## Player counts & scaling

Base rules = **2p** (the design home — a genuine duel). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Menu size** | 4 | 5 | 6 |
| **Hot-List slots** | 3 | 4 | 4 |
| **Season milestones** (fire a Condition) | 4/8/12/16 | 6/12/18/24 | 8/16/24/32 |
| **Season final (ends game)** | ~20–24 | ~30 | ~36 |
| **Start positions** | opposite (N & S) | spread on the ring | spread on the ring |
| **Briefs (opening hand)** | 3 | 3 | 3 |
| **Sealed Itinerary** | draw 2 keep 1 | draw 2 keep 1 | draw 2 keep 1 |

Season thresholds scale with the faster plating/locking rate at higher counts (≈ `n × [2,4,6,8]`) to
hold game length. The Hot-List grows to keep contention fair as more agents compete (same logic as the
Menu). **Resentment risk is actually *lower* at 3–4p** (a snipe is diffuse, not personal) — the sharp
case to design/sim is **2p**. **Best-at:** designed for **2p**; 3–4p is a warmer, chattier, slightly
longer race.

---

## Solo mode / Automa

**Low priority** (Fellowship wants ≥2 humans; solo is a bonus). Updated "Rival Agent" Automa sketch:
- A small **Route deck**. On its turn, flip the top card: it **plates** the highest-VP Menu Dish it can
  "afford" against a running ingredient counter (Season +1; **locks** a Hot-List spot if its running
  tour now satisfies one — so the race still bites solo), or **travels** (rotating the region it
  "controls"), or **reacts** to the active Condition.
- Pressure = **tempo + the Hot-List race**: it plates steadily to hurry the Season and to lock spots you
  wanted. Difficulty = plate-aggressiveness (deck ratio) + a target score. Keep upkeep near-zero (one
  flip, one lookup). **Defer to `bg-architect`; not in the base MVP.**

---

## Complexity budget

Target **~2.0–2.1, ceiling 2.2**; `complexity-budget.json` caps, guarded by `bg-elegance`.

- **The weight call (honest).** We *cut* the whole co-op tip-economy (Dead-drop, Insider Tip, flat
  Dossier payout + triggerer's-pick sub-race, and the "is helping rational?" knife-edge) — roughly
  −0.3 of what those cost — and spend it on the **two highest interaction-per-rule pieces**: the
  **Hot-List** (~+0.15–0.2, but *reuses the Operation card type* and its rule is just "complete →
  lock → refill") and **Conditions** (~+0.2–0.25 — the varied event deck is the real spend; the
  telegraphed queue is one small rule). That lands ~**2.0**. **Briefs are the marginal, weakest-per-rule
  addition** (~+0.1 minimal / ~+0.2 as a full deck) — this is the piece to trim if we drift, and it's the
  explicit CD decision below.
- **Actions dropped 5 → 4** (Dead-drop gone; lock-in and Briefs are free riders) — a genuine
  simplification that partly offsets the new subsystems.
- **Component types = 7** (+1 over v1's 6): cut Insider Tip tokens, added Condition + Brief decks. The
  CD softened the cap; the **Brief-scope decision doubles as the 7-types decision** (fixed-set Briefs →
  back to 6). Conditions/Briefs stay separate decks (sensitivity rail — do not blur head-office vs
  island).
- **Keywords ≈ 9–10, under the 12 cap:** Larder · Menu · Dish · **Signature Itinerary (secret)** ·
  **Hot-List** *(verb: lock in)* · **the Season** · **Condition** · **Brief** · Extract. (Stock Up /
  Travel / Plate and region/specialty/pantry stay plain-language.)
- **What gets cut if we drift over 2.2, in order:** (1) **Briefs** (drop to a fixed printed self-boost
  rider on a warm Condition — recovers ~0.1–0.2 and the 7th type); (2) the **HSR shortcut** (fold into
  plain adjacency); (3) **Signature 5-VP Dishes** (collapse to 3/4). Depth lives in the *Hot-List race
  under a shifting island*, not the subsystem count — protect that, cut around it.

---

## Keywords / glossary

- **Larder** — your sourced ingredients, **face-up in the open** (not a hidden hand). Cap **7**.
- **Menu** — the shared face-up row of Dish cards; refills from the Dish deck.
- **Dish** — a recipe card (2–3 ingredients) worth VP; plated into your tour.
- **Signature Itinerary** *(secret; [fiction → bg-theme])* — your **hidden** Operation, the one hidden
  hook; **+7** if completed, revealed at scoring.
- **Hot-List** — the shared face-up row of public bonus tours (Operation cards, 4–6 VP) both agents race
  to complete and **lock in**; refills when one is locked.
- **the Season** *(repurposed Grand Dossier; [fiction → bg-theme])* — the shared clock; **+1 per Plate
  and per Hot-List lock-in**. Each milestone fires a **Condition**; the final milestone can end the game.
- **Condition** *([fiction → bg-theme]; was Happening/event)* — an island event (festival / hazard /
  warm character) from the telegraphed queue (ACTIVE + NEXT). Secular only.
- **Brief** *([fiction → bg-theme]; was Order)* — a one-shot head-office directive (safe boost / risky
  gamble / light nudge). Play ≤1/turn, free.
- **Extract** — the action that triggers the end-game wind-down ("file the finished tour / catch the
  last train home").

---

## Open questions for playtesting (top 3)

1. **Is the Hot-List race fun-tense, not resentment-on-snipe or a leader-runaway? (THE load-bearing
   bet.)** Attack first with the sim (below) *and* a 2p Screentop feel-test: does sniping a spot feel
   *tense-fun* or *rage-inducing*? Does the winner sweep the spots (runaway) or do they split? *Fail
   fixes:* per-player lock cap · trailing-player discount · faster refresh · lower spot VP.
2. **Do Conditions vary routing game-to-game without erasing a planned plate (agency)?** Does the
   telegraphed queue (preview NEXT) give enough warning to reroute? Is ~4–5 Conditions/game the right
   rhythm (not a barrage, not forgettable)? *Fail fixes:* preview 2 ahead · hazards *tax* not *block* ·
   retune milestone spacing.
3. **Fellowship without co-op + the Briefs' register.** Does the table groan/cheer together at
   Conditions (is Fellowship actually present now that co-op is gone)? Do Briefs read as **affectionate
   needling** or **mean**? Is the minimal Brief set enough spice, or forgettable? *Fail fixes:* bound the
   nudge harder (if mean) · add variety / fold to fixed set (if forgettable) — the CD decision below.

**Named sim (extend `games/travel-agents/sim/travel_agents.py`):** **bounty-claim-share vs finishing
position.** The v1 harness already tracks "milestone-trigger share vs finish"; re-point it at the
Hot-List. Model two strategies over the shared sourcing brain: **Chaser** (routes greedily to lock any
completable Hot-List spot ASAP) vs **Signature-focus** (routes for its Sealed +7, locks spots only
incidentally). Track the **distribution of locks between players** and the **correlation of lock-share
with winning**. *Pass:* locks spread (~50/50 ±) and the eventual winner does **not** claim a
disproportionate share — Chaser is competitive but **not dominant**. *Fail:* leader sweeps locks → apply
a per-player lock cap / trailing discount / faster refresh. Secondary sim: **Condition variance** (do
events shift optimal routing across games without a single hazard being able to erase a planned plate?).

---

## Handoff notes (guardian sweep — where to look)

Mechanics that moved from v1 into model C:
- **Signature twist has moved.** v1's twist was the shared-Dossier + tip-offs co-op loop. **v2's
  signature twist is the public Hot-List race running on the same Operation cards as your secret
  Signature Itinerary, under a telegraphed living island (Conditions) that the shared Season clock
  fires.** `bg-theme`: does "rival travel agents racing to lock the island's hot spots into competing
  tours, while the island throws weather/festivals" read warm, guest-and-fan, celebratory (the re-skin
  makes agents *promoters* of Taiwan — net safer)? Confirm the **secular-only Conditions** and
  **dignified characters** rails are honoured, and that **head-office Briefs stay distinct from island
  Conditions** (the binding anti-blur rail). `bg-elegance`: is the weight honestly held at ~2.0–2.1 —
  the swap ledger (top of doc), the 7th component type (Brief deck), and the Briefs-scope trim?
- **Cut mechanics to sweep for stranded names/rules:** **Dead-drop**, **Insider Tip**, the **flat
  Dossier payout / triggerer's pick** are gone — check nothing in components/rulebook/sim still
  references them.
- **New rules the fiction must explain:** the **Larder cap** (retained — "travel light, eat fresh"), the
  **Hot-List** ("HQ's hot-list of must-visit spots"), **Conditions** ("the island doesn't wait for
  you"), and **Extract** ("file the finished tour / catch the last train"). Confirm the fiction covers
  them.
- **`bg-developer` data:** add **chicken 雞 + egg 蛋** ingredients (framework above); build the
  **Hot-List deck** (4–6 VP objectives) + **Condition deck** (~8, starter set above) + **Brief** set
  (per the CD decision); the **VP score track** + markers on the board.
- **`bg-access`:** the board now shows the Season clock + VP track + Hot-List row + Condition queue —
  keep the night-market palette dual-coding intact across the busier board.
