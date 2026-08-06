# Travel Agents: Taiwan — Design Doc (v3.1 · the vendor-courting engine)

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.
**v3 = the v2.1 vendor-courting engine (LOCKED direction, 2026-08-06).** Slug `travel-agents`.

> **v3.1 (2026-08-06) — two playtest-driven changes, engine unchanged.** Both from the CD after the
> bg-developer imbalance flag + the first feel-reads:
> 1. **Movement rebalance (Change 1).** The locked real-dish recipes made ingredient demand lopsided —
>    **pork named on 10 vendors, rice 7, but pearls / oysters / milkfish on exactly 1 each** — so
>    Central/South barely bit, their discount ramps were starved, and a **stay-home-North line** loomed.
>    v3.1 re-costs the vendors to a **target demand distribution** (below) so **every region is a
>    meaningful sourcing destination** and players **must travel** to source across the island.
>    `bg-developer` re-costs `vendors.csv` (and flattens `ingredients.csv` supply) to this spec. **Zero
>    new rules** — pure re-costing of existing components.
> 2. **The Poach (Change 2) — a new *conditional* same-location action.** When both agents are in the
>    **same region**, on your turn you may **Poach**: take 1 random specialty from the rival's Larder,
>    paying **−1 Reputation**. A cheeky agent-vs-agent swipe (never a vendor or place), a real
>    risk-reward, and a reason to **track the rival's position** — synergising with Change 1 (more travel
>    → more encounters).
>
> Everything else in v3 stands: the recipes-by-region engine, the Hot-List→Vendor-Board race, the Buzz
> brake, the hybrid tracks, the 5 characters. Full detail: *Movement rebalance* and *The Poach* sections.
Evolves v2 ("Rivals on a Living Island"): the **recipes-by-region** sourcing engine, the **public rival
race**, the **secret +7 signature mission**, the **live VP tracker**, and **Extract** all carry over.
What changes is the **scoring beat and the depth**: you no longer *Plate a dish* (a chef's verb — off
identity). You **court a Vendor to secure their exclusive blessing** on your tour, paying **two inputs**
(fresh **ingredients** + **Buzz**); each secured vendor is an **engine piece** feeding **several scoring
vectors**. This is the CD's "past collection, into an engine" pivot (Splendor Duel / Duel for
Middle-earth / Arnak band).

Primary brief: `design/explore-v2.1-engine.md` (the four adopted forks). Sensitivity rails bind
throughout (`identity.md` §9): securing exclusive rights reads as **a vendor granting their blessing to
the agent they like best**, never an agent monopolising or extracting a place.

> **One-line frame:** two rival travel agents race to build Taiwan's best food **tour** — source real
> regional ingredients, generate **Buzz**, and spend both to **win over the island's vendors** (each an
> engine piece that makes the next courting cheaper), climbing **Prestige**, **Reputation** and
> **Region-Coverage** toward the hidden **signature tour**. Most impressive tour is **Top Agent**.

---

## What changed from v2 (the engine pivot — honest ledger for `bg-elegance`)

This is a **redirect of the scoring beat + a deliberate, CD-sanctioned depth increase**, not a pile-on.

| Cut / banked (−) | Added / spent (+) |
|---|---|
| **Plate a Dish** (spend recipe → VP) | **Court a Vendor** (spend **ingredients + Buzz** → secure it) — the two-input engine beat |
| **Briefs** deck (whole subsystem + keyword) | **Buzz** — the second, fungible currency + **Promote** action (re-homes the Brief's flexible-resource job) |
| **Conditions queue** (ACTIVE/NEXT slots + Season-fire machinery) | **Events salted into the Market**, firing **on refill** (fewer moving parts than the queue) |
| Hot-List as a *separate* board | **merged INTO the Vendor Board** — the public race *is* courting vendors |
| Single flat VP total | **Compounding discount engine** + **Reputation track** + **Region-Coverage** — the multi-vector depth |
| Symmetric players | **5 Agent Characters** (1 ability + 1 flaw each) |

**Honest weight call:** this lands around **~2.3–2.4** (Splendor Duel ~2.3, 7WD/LOTR-Duel ~2.4, Arnak
~2.7) — squarely in the raised band (`complexity-budget.json`: aim 2.2, ceiling 2.5). The two-input
economy + the discount ramp + two real tracks are the deliberate spend; cutting Briefs and the Conditions
queue, and merging Hot-List into the Board, bank the weight so it does **not** drift to the ceiling.
Trim order held in reserve (see *Complexity budget*).

---

## Design goals

- **Target weight ~2.2–2.4, ceiling 2.5.** A **tight two-player engine** in the Splendor Duel / LOTR
  Duel mould — NOT a heavy euro. Every rule earns its place; `bg-elegance` guards the ledger.
- **2-player first.** The duel is the design home; 3–4p is a scaling delta (see *Player counts*). The
  sharpest balance case — a two-person race for the same vendor and the same ramp — is what we design and
  sim against.
- **Aesthetics (locked, `identity.md`):** **Discovery (lead)** — the Market, the Vendor Board and the
  events reveal and remake the island; **Fellowship** — warm rivalry over the shared Board + shared event
  drama; **Challenge** — the routing + two-input engine puzzle (kept tight, ~2.3, not a heavy optimiser).
- **The meaningful decision every turn:** *do I source the specialty a vendor needs (and race the rival
  to the Market before the last one's gone), bank Buzz, or spend both to court now — and which vector does
  this vendor push me up?* No forced move: Travel always arrives with an ingredient; Promote always yields
  Buzz; the Board always offers several affordable-soon vendors.
- **Taiwan does real work** (unchanged core strength): the region↔ingredient web is real food geography —
  rename the setting and the recipes break. Dishes/vendors named Tâi-lô + 繁體, never mangled.
- **Design the two make-or-break risks out** (see *Interaction & tension* and *Riskiest assumptions*):
  **(a) no dominant track or opening**, **(b) no economy runaway** past the end-clock.

---

## Core loop (detailed)

A turn is **one action**; short turns, low downtime (crucial at 2p). Each cycle you optimise: *which
input am I short — the region-specific ingredients a target vendor needs, or Buzz — and is now the moment
to court before my rival locks that vendor (and its discount icon) away?*

1. **Read the board.** The tiered **Vendor Board** shows the vendors both agents are courting from (each
   printed with its cost = named ingredients + Buzz, its **region icon**, its **Prestige**, its **Rep**,
   and its **perk**). Your **secret signature mission** points at a vendor pattern worth **+7**. The
   face-up region **Markets** show which specialties are available where (and how contested). Your
   **Prestige** (VP track) and **Reputation** (Rep track) markers show two of your vectors live.
2. **Take one action** (see *Actions*): **Stock Up**, **Travel**, **Promote**, **Court a Vendor**, or
   **Extract**.
3. **Court a Vendor** is the beat that pays. Pay its ingredients **(minus your region discounts)** + its
   **Buzz** (never discounted). The vendor joins your **tour**, and *all at once* you gain: **Prestige**
   (VP, live on the track), a **Reputation** bump (marker up), its **engine perk** (usually a permanent
   region **discount icon** that makes future vendors cheaper — the ramp), and a **Region-Coverage** tick
   if it's your first vendor in that region. Then **refill** the Board slot from that tier's deck, advance
   the **Season** end-timer **+1**, and — because the vendor has chosen *you* — the rival is **locked out**
   of that specific vendor.
4. **The Market lives.** When you Stock Up and refill the face-up Market, a flipped **Event** ("Condition")
   fires on the spot — a region-thematic festival window, a typhoon reroute, a warm local — boon-skewed,
   tax-not-destroy. Taking the last of a scarce specialty forces your rival to reroute.
5. **Decide when to wrap.** **Extract** ("file the finished tour / catch the last train home") triggers
   the wind-down; or the **Season** timer fills (Rep-top no longer ends the game — see *End-trigger*).
   Whichever fires first → finish the round + one full round → **reveal missions** → score.

The loop compounds **legibly and with a brake**: each vendor makes a *class* of future vendors cheaper in
ingredients, so your courting **rate** climbs — but every vendor still costs **Buzz**, which is never
discounted and comes one action at a time, so the ramp accelerates the contested half (ingredients) while
the reliable half (Buzz) stays a fixed per-vendor tax. That Buzz floor is the primary anti-runaway brake
(see *Economy* and *Interaction & tension*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** — 4 regions on a ring: **North 北 – Central 中 – South 南 – East 東**;
  an **HSR** spine links North↔South down the west coast. The board also carries the **Season end-timer**,
  the **VP (Prestige) track**, the **Reputation track**, the tiered **Vendor Board** (3 rows), and each
  region's **Market slots**.
- Build each region's **Market supply**: its specialty ingredient tokens **+ ~2–3 Event tiles** shuffled
  in; draw to fill that region's face-up Market slots. **Pantry** tokens form an **unlimited** open pile
  (the convenience store, available anywhere).
- Build the **Vendor deck**, split by tier (**T1 Stalls / T2 Eateries / T3 Marquee**); shuffle each tier
  separately and deal the Board rows face-up (2p: **3 per tier**).
- Form the **Buzz** token pool (open supply).
- Each agent: choose/deal an **Agent Character** (ability + flaw, public); take a pawn (start on opposite
  regions — one North, one South); place **VP** and **Rep** markers at 0; take an empty tour area. Larder
  (ingredients) starts empty and sits **face-up** all game. Deal **3 Mission cards, secretly keep 1**
  (your signature mission, +7), return 2 unseen.

**A turn = choose ONE action:** **Stock Up · Travel · Promote · Court a Vendor · Extract** — **plus a
conditional sixth, Poach**, available only when a rival's pawn shares your region (v3.1; detailed below).
Then if your Larder (ingredients) exceeds **7**, discard down to 7. Play passes clockwise (the
Influencer's flaw = goes last; see *Characters*).

**End-trigger (either, whichever first):**
- A player takes the **Extract** action, **or**
- The **Season** end-timer reaches its final mark (advances +1 per Court by anyone).

**Reputation-top does NOT end the game** (sim-fix, 2026-08-06): reaching Rep-top scores its **+9** but is
**not** an end-trigger. Why: with Rep-top ending the game it fired 100% of games at only ~5 courts/player,
so the Season timer never paced anything and the *engine never ramped* (an engine game whose engine
doesn't build). Decoupling it lets the Season timer (final mark ~16 courts at 2p) pace the game →
**~8–9 courts/player, ~23 turns**, the discount ramp fully develops, and track balance tightens
(sim-verified: Probe-1 leader 54.7% → 51.9%).

Then: **finish the current round** (equal turns for all), play **one more full round**, then **reveal
signature missions** and score. A fair, unswingy wind-down; the extra full round guarantees the trailing
player answers the trigger.

Target length: **~40–50 min at 2p**, roughly **18–22 turns per player**.

---

## Actions

A turn = ONE of five. All are simple (Splendor is essentially *take-tokens / buy-card*; we split "take"
into ingredients / Buzz / travel because they carry the routing + risk texture the theme needs).

| Action | Cost | Effect | Notes |
|--------|------|--------|-------|
| **Stock Up** | your turn | Take **2 ingredients** from your current region's face-up Market (its **specialties** and/or **pantry**). Then **refill** the Market slots from the region supply — each flipped **Event** fires now (see *Market & Events*). | The ingredient workhorse. Taking the last of a scarce specialty forces the rival to reroute. Take-2 = up to two refill flips = more event exposure (push-your-luck, no extra rule). |
| **Travel** | your turn | Move your Agent to an **adjacent** region on the ring (HSR: North↔South counts adjacent); on arrival take **1 ingredient** there (and refill/fire as above). | Never a dead turn — you always arrive with something. |
| **Promote** | your turn | Take **2 Buzz** from the supply (the always-available soft input). | The second currency. Safe, uncontested, never event-risky — the calm axis opposite the contested ingredients. |
| **Court a Vendor** | your turn + pay cost | Choose a Board vendor; pay its **named ingredients minus your region discounts** (floored at 0) **+ its Buzz (never discounted)**. Gain its **Prestige** (VP live), **Rep** bump, **perk** (usually a region discount icon), and a **Coverage** tick if new region. Refill the Board slot; **Season +1**; the vendor is locked from the rival. | The scoring + engine beat. The one action that advances the end-timer. |
| **Extract** | your turn | Trigger the end-game wind-down (finish the round + one more full round). Your signature mission stays face-down until scoring. | Push-your-luck tempo: wrap while ahead vs court one more. |
| **Poach** *(conditional — v3.1)* | your turn **+ −1 Reputation** | **Only if a rival's pawn shares your region.** Take **1 random specialty ingredient** from that rival's Larder into yours (pantry ignored; if they hold no specialties, there's nothing to Poach). Move your **Rep marker down 1** (floored at 0 — no Rep, no Poach). Does **not** refill the Market, fire an event, or advance the Season. | The cheeky same-location swipe. Situational tempo/denial, not a staple — see *The Poach*. |

**Five core actions + one conditional** (Poach). Every turn has multiple live options with real
trade-offs (source the contested specialty vs bank safe Buzz vs court-now-and-ramp vs wrap-it — vs, when
you're nose-to-nose with your rival, swipe the thing they just hauled), under a Market that can hand you a
festival or a typhoon. No forced/obvious move.

---

## Components

| Component | Qty | Notes |
|-----------|-----|-------|
| **Map board** (Taiwan) | 1 | 4 regions on a ring + HSR spine; carries the **Season end-timer**, the **VP/Prestige track**, the **Reputation track**, the tiered **Vendor Board** (3 rows) and each region's **Market slots**. |
| **Vendor cards** | ~44–52 | Tiered: **T1 Stalls** (~20), **T2 Eateries** (~16), **T3 Marquee** (~10). Each: cost (named ingredient icons + Buzz), **region icon** (= discount + coverage), **Prestige**, **Rep**, **perk**, name (Tâi-lô + 繁體). *Reuses/renames v2's Dish/Operation card type — the vendor is the old "Dish/Hot-List" merged into one engine card.* |
| **Mission cards** | ~12–16 | Secret signature patterns (+7). Draw-3-keep-1. Same card stock as vendors; distinct content. |
| **Ingredient tokens** | ~150 | Region **specialties** (N: beef/pork/**chicken 雞**/**egg 蛋**; C: tea/pearls; S: oysters/milkfish; E: rice/greens) + fungible **pantry** (unlimited). Open supply. |
| **Buzz tokens** | ~50 | The second currency. Open supply. **New type.** |
| **Event tiles** ("Conditions") | ~10–14 | Region-thematic events salted into the region Market supplies; fire on refill. Secular only. **New type** (was v2's Condition *cards* + queue — now tiles in the Market, no queue). |
| **Character mats** | 5 | 1 ability + 1 flaw each (see *Characters*). **New type.** |
| **Agent pawns + markers** | 4 + 8 | Pawns on the map; VP + Rep markers on their tracks (board bits, not a distinct "type"). |

**Component types ≈ 7** (board / Vendor cards / Mission cards / ingredient tokens / Buzz tokens / Event
tiles / Character mats) — within the raised cap of **8** (`complexity-budget.json`). New vs v2: **Buzz
tokens**, **Character mats**, **Event tiles**. Banked vs v2: **Brief cards cut**; the **Conditions
card-deck + queue** collapse to Event tiles in the Market; **Hot-List** is no longer a separate row (it
*is* the Vendor Board). Missions reuse vendor card stock. Honest flag to `bg-elegance`/`bg-architect`:
Buzz + Characters are the real new-type spend — they're the depth the CD asked for.

### Ingredients — the region↔ingredient web (retained + extended)

Retained from v2, now the **ingredient input** to courting. **New from the locked North picks**
(雞排 / 火雞肉飯 / 卡拉雞腿堡 / 蛋餅): **chicken 雞** and **egg 蛋** — both **North** specialties
(night-market + breakfast-shop identity). North now carries **4** specialties (beef/pork/chicken/egg) vs
2 elsewhere.

**Framework rules (systems-level; final list by `bg-developer`):**
- Every region remains the **sole source of ≥1 ingredient named on cross-region vendors**, so Travel stays
  motivated — the non-negotiable that keeps the "travel because the food lives there" engine alive.
- **Watch — North is now the richest region (4 specialties).** Two guards: (1) keep **vendor region-icons
  balanced across all four regions** regardless of ingredient counts (so North isn't the auto-ramp
  region); (2) keep enough **cross-region** and **East/South/Central-icon marquee** vendors that the
  Coverage bonus and the tall line *pull players out of* North. `bg-developer` to keep North from being a
  stay-home ramp trap.
- **Pantry is unlimited** (the anti-stuck valve on the hard axis) but still costs an action to gather.

> **Sensitivity (binds — `identity.md` §9):** East specialties draw on **Indigenous** cuisines — generic,
> respectful labels, consultant before art/print. Han/Hakka/Indigenous/newer-community range across
> vendors. Taiwan as itself; Traditional characters; Tâi-lô + 繁體, never mangled.

### Movement rebalance (v3.1) — the target demand distribution (`bg-developer` re-costs to this)

**The problem (bg-developer flagged, CD confirmed).** v3's vendor costs were faithful to real recipes, and
real Taiwanese food leans hard on a few workhorses — so ingredient **demand** came out lopsided:

| | pork | rice | chicken | tea | egg | beef | greens | pearls | oysters | milkfish |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **v3 vendors naming it** | **10** | **7** | 4 | 3 | 3 | 3 | 2 | **1** | **1** | **1** |

Rolled up by **region of sourcing** (which region you must physically stand in to take that specialty),
the v3 deck demanded: **North ~20 tokens · East ~9 · Central ~5 · South ~2.** South is a ghost town — two
tokens' worth of pull across the *entire* deck. So Central/South specialties barely bite, **each region's
discount ramp is only fed if that region's vendors actually name that region's specialties** (they didn't —
火雞肉飯/S named chicken+rice, 爌肉飯/C named pork+rice, 牛肉湯/S named beef), and a **stay-home North (±East)
line** can court most of the deck without ever routing South or Central. The travel engine doesn't bite.

**Why it happened (and the license to fix it).** The costs were pinned to *literal recipes*. The CD grants
license to **deviate from strict recipe faithfulness** where movement needs it — read a vendor's cost as
*"what it takes to feature them on your tour"* (the ingredients you supply **+ the regional connections you
bring**), **not** a literal ingredient list. Hard rail (binds): **real dishes are never mangled** — keep
the *anchor* ingredient true to the dish; use the CD's framing only for the *cross-region link* token, and
route any deviation through the consultant. Don't put oysters "in" a dish that has none — frame the South
token as *the Southern leg / connection you arrange to seat this vendor on the tour.*

**The four re-costing principles (`bg-developer` applies across all 25 vendors):**

1. **Anchor in-region.** Every vendor names **≥1 specialty from its own icon-region.** This is the
   structural fix: with icon balance **N7·C6·S6·E6**, anchoring alone demands each region's specialties
   ~6–7× (once per same-region vendor) and — crucially — **feeds that region's discount ramp** (holding
   South icons finally discounts something South vendors actually cost). T1 stalls = 1 in-region specialty
   + pantry; T2/T3 = ≥1 in-region + often a cross-link.
2. **Cross-region links on ~40% of vendors (concentrated in T2/T3).** Name **1 ingredient from a
   *different* region** than the icon, to force a trip — but **spread the links evenly** so each region is
   both a source-of-links and a receiver, instead of every cross-link defaulting to North-pork / East-rice.
   This is what produces actual *inter-region* travel (anchoring alone could let a player camp one region
   and court locally — the links are the load-bearing anti-camp lever; see *Riskiest assumptions*).
3. **Cap the workhorses.** **pork ≤5 vendors** (from 10), **rice ≤5** (from 7). Redistribute the freed
   demand onto **oysters / milkfish / pearls / greens.**
4. **Per-specialty floor: every specialty named on ≥3 vendors.** Kills the dead tokens (pearls/oysters/
   milkfish were on 1). No region's specialty is a museum piece.

**Target demand distribution (the number `bg-developer` re-costs toward — a guide, ±1 is fine):**

| Specialty | Region | v3 (vendors) | **v3.1 target** |
|---|---|---:|---:|
| pork | N | 10 | **4–5** |
| chicken | N | 4 | **3–4** |
| beef | N | 3 | **2–3** (marquee-held) |
| egg | N | 3 | **2–3** |
| tea | C | 3 | **5–6** |
| pearls | C | 1 | **3** |
| oysters | S | 1 | **4** |
| milkfish | S | 1 | **3–4** |
| rice | E | 7 | **4–5** |
| greens | E | 2 | **3–4** |

→ **regional sourcing demand:** North ~28–30% · Central ~22–24% · South ~22–24% · East ~22–24% (North
stays modestly richest — it has 4 specialties — but no region is starved; South rises from ~6% to ~23%,
the headline fix).

5. **Marquees stay single-region but Buzz-heavy.** Keep 牛肉麵 (N, beef), 珍珠奶茶 (C, tea+pearls), 小籠包
   (N, pork), 虱目魚粥 (S, milkfish) iconic and single-region — they are **not** a stay-home trap because
   they're **few**, their **Buzz is undiscountable** (a fixed tax that doesn't ramp), and Coverage + the
   spread of anchored/cross-link vendors pull you across the island regardless.

6. **Supply follows demand (`ingredients.csv` flag).** Re-flatten token **supply** to track the new
   demand — bring **pork 18→~12, rice 16→~12** down and **oysters/milkfish/pearls 8→~10–12** up — so
   scarcity ≈ **2× per-region solo demand** is roughly even across all four regions (no pork glut, no
   oyster drought). This keeps the Market-contention texture even, and makes the South/Central **boon
   events** (Mango Season, Oyster Glut, Bubble-Tea Festival) finally matter (their specialties are now
   demanded). *Event tiles themselves need no respec — flag to `bg-theme` (events pass in parallel): the
   rebalance only makes South/Central events bite harder, a plus for the "funnier events" work.*

**How this makes the engine bite in all four regions.** (a) *Sourcing:* you must stand in a region to take
its specialty, and each region is now demanded ~9× across the deck → you route to all four over a game.
(b) *Discount ramp:* the per-region ramp finally saves something on that region's own vendors (anchor
principle) → every region's ramp is worth building, not just North's. (c) *Travel:* the ~40% cross-links
force trips *between* regions, spread so no single region is the default detour. (d) *Coverage/missions*
(unchanged) now have real sourcing reasons behind the breadth, not just a scoring nudge.

### Vendors — the engine cards (the merged Dish + Hot-List, now a shop)

A **Vendor** is a stall/cook who agrees to feature on your tour. Courting one = paying **what the stall
needs to shine**: **(a) fresh ingredients** (region-specific — the vendor's signature dish defines them;
real food geography does the work) **+ (b) Buzz** (you *promote* them, promising customers and hype — the
travel agent's actual job, and the anti-extraction linchpin: courting = *showcasing/helping*, never
taking). Three tiers on a Splendor-style Board:

| Tier | ~Count | Ingredient cost | Buzz | Prestige (VP) | Rep | Perk |
|------|-------:|-----------------|-----:|--------------:|----:|------|
| **T1 Stalls** | ~20 | **2** (1 region) | **1** | **1** | **+1** | its **region discount icon** (the base ramp) |
| **T2 Eateries** | ~16 | **3** (2 regions) | **2** | **3** | **+2** | region icon **+ one** of {Promote +1 Buzz · once/turn treat 1 pantry as a wild specialty when courting · +1 Rep on each future court} |
| **T3 Marquee** | ~10 | **3–4** (2–3 regions) | **3–4** | **5–6** | **+2/+3** | a **strong** perk: a **wild region icon** (counts as any 1 region for discount *and* coverage), **or** +2 Rep on courting, **or** counts as **2** region icons |

**The discount ramp (the Splendor engine).** Each secured vendor carries a **region icon** (N/C/S/E, or
wild). Holding *k* vendors with the X-icon reduces the **X-region ingredient** portion of any future
vendor by *k* (floored at 0). Early vendors are dear and slow; each one signed makes a *class* of future
vendors cheaper. **Buzz is never reduced** — this is the brake (below).

### Missions — the secret +7 (draw-3-keep-1)

Deal **3**, secretly **keep 1**, discard 2 unseen. A mission is a **secret vendor pattern** worth **+7 at
scoring** (binary). Starter pool (variety on purpose, so it doesn't just reinforce one track):
- *"3 vendors in the South"* (regional crawl) · *"a vendor in all 4 regions"* (grand tour — overlaps
  Coverage) · *"3 T1 Stalls"* (the humble-eats tour) · *"2 T3 Marquee vendors"* (the fine-dining tour) ·
  *"a vendor of each of 3 named cuisines"* · *"vendors totalling ≥ 18 Prestige"* (go tall) · *"5 vendors,
  any"* (the volume tour) · *"a Marquee + its two feeder-region Stalls."*
Why a **pick, not a random deal:** with **public characters** and **multiple tracks**, the pick lets you
steer your character/track synergy on purpose and **launders the char×mission balance problem** — a broken
combo can't be randomly gifted; you choose it, the opponent sees your character and contests.

---

## Economy & math

The two-input economy is the make-or-break. Numbers below are first-pass — the sim's job is to attack
them (see *Riskiest assumptions* and the sim plan in `explore-v2.1-engine.md` §8).

**Income vs spend (per action):**

| Action | Yield |
|--------|-------|
| Stock Up | +2 ingredients (region-gated) |
| Travel | +1 ingredient + reposition |
| Promote | +2 Buzz (→ +3 for the Influencer / with a Buzz-income perk) |
| Court | −(ingredients − discount) − Buzz; +Prestige +Rep +perk +coverage |

**Courting cost vs reward, and the ramp** (illustrative vendors):

| Vendor | Base cost | Cost at mid-ramp* | Reward (Prestige + Rep) | ~Turns | VP/turn** |
|--------|-----------|-------------------|-------------------------|-------:|----------:|
| T1 Oyster-Omelette Stall (S) | 2×S + 1 Buzz | 1×S + 1 Buzz | 1 + (+1 Rep) | ~1.5 | ~1.1 |
| T2 Beef-Noodle Institution (N) | 2×N +1P + 2 Buzz | 1 ingr + 2 Buzz | 3 + (+2 Rep) + perk | ~2.5 | ~1.7 |
| T3 Banquet Master (N+S+E) | 1×N+1×S+1×E + 3 Buzz | 1 ingr + 3 Buzz | 6 + (+3 Rep) | ~4 | ~1.9 |

\* *mid-ramp = holding ~1 icon per named region.* \*\* *counting ~0.7 VP per Rep point via end-track VP.*

**Balance assumptions (attack these):**
1. **VP/turn is flat-ish (~1.1–1.9)** so no tier is an auto-win. T2 is the intended workhorse (best raw
   rate via its perk); T1 pays **indirectly** — its cheap region icons are what make everything else
   cheap (the engine investment); T3 pays in Prestige + mission/Coverage synergy, not raw rate.
2. **The binding constraint *shifts*** — a feature, not a bug. **Early:** ingredients bind (can I get the
   contested specialty?). **Late:** the discount ramp makes ingredients trivial, so **Buzz** binds (do I
   have enough Buzz to court again?). That shift keeps the decision fresh across the game.
3. **Larder cap 7** (ingredients) forces the source→court rhythm; **Buzz uncapped** (hoarding Buzz just
   means not courting = losing tempo — self-correcting, no rule needed).
4. **Target 2p winner ~35–42 total VP.** Rough split for a balanced game: vendors' Prestige ~18–24 +
   Reputation end-VP ~4–9 + Coverage ~2–9 + signature mission 0/**7**.

**The Season end-timer.** Advances **+1 per Court** (any player). Final mark at **~16** total courts at 2p
(≈ 8 each) → wind-down. Because a *fast* courter fills the timer, the wide/ramp player **hurries the end**
they'd need to keep courting — while a *tall* player (fewer courts) leaves the timer low and gets **more
turns to reach parity**. That is a gentle, built-in catch-up co-brake (see *Interaction & tension*). A
sim/feel tuning knob; scales by count.

---

## Scoring / win condition — "Top Agent"

Hybrid multi-track: tracks **trigger the endgame and pay a bonus**, but **highest total VP wins** (no
Splendor-style sudden-death — warm, non-feel-bad, and a trailing player always has a live second vector).

At game end each agent totals four sources:
1. **Tour Prestige (VP)** — sum of your vendors' star values (T1=1, T2=3, T3=5–6). *(Live on the VP
   track.)* — the **tall / prestige-rush** line.
2. **Reputation** — end-VP by your marker's final position: **3→+2 · 6→+4 · 9→+6 · 12 (max)→+9**. You climb
   it by courting (each vendor's printed Rep). Passing **3 / 6 / 9** grants a one-time perk (below); the
   **top (12)** is an endgame trigger and pays its +9. *(Live on the Rep track.)* — the **reputation-climb
   / engine** line.
3. **Region-Coverage** — end-game breadth bonus for distinct regions among your vendors: **2 regions→2 ·
   3→5 · 4→9.** Keeps routing relevant to scoring so the travel engine still matters. — the **grand-tour /
   breadth** line.
4. **Secret signature mission** — **+7 if completed** (revealed now), else 0. *(The one hidden vector —
   face-down until the reveal, so it stays a moment and keeps a visibly-trailing player hopeful.)*

**Reputation milestone perks** (one-time, as you pass — these are what make climbing a *strategy*, not
just a parallel scorer): **pass 3** → take 2 wild ingredients now; **pass 6** → your Promote is
permanently +1 Buzz; **pass 9** → gain 1 permanent region discount icon of your choice. (Kept to three
clean perks; the top is pure VP. If weight drifts, these collapse to pure end-VP — see *Complexity
budget*.)

Highest total is **Top Agent**. **Tiebreak:** highest Reputation, then most vendors, then most regions.

### Designing out the top risk (a): no dominant track or opening

The classic tight-2p-engine failure is a solved line. Four structural guards keep **≥2 paths genuinely
competitive** (target: tall ≈ rep-climb ≈ breadth, none >~55% in sim):
- **The three tracks reward *different behaviours*, and pull against each other.** Prestige rewards *few,
  big* vendors; the discount ramp rewards *many, doubled-up in a couple of regions*; Coverage rewards
  *one spread across all four*. You cannot maximise ramp (concentrate) **and** Coverage (spread) at once —
  a real tension, not a false choice. Reputation rewards *steady courting for its perks*, converting to VP
  late.
- **Reputation is decoupled from raw Prestige.** Rep is a printed value (roughly tier), so a *tall* player
  and a *wide* player climb it at similar rates — neither the volume nor the marquee line double-dips Rep.
- **The mission is a pick** — each player steers their own keel, so no single global "best line": the
  mission diversifies what each agent is optimising.
- **No dominant opening:** an **ingredient-heavy** open ramps discounts fastest but is scarcity/event-
  exposed (a rival can take the last specialty, an event can wash a Market); a **Buzz-heavy** open is safe
  and grabs a strong T2 perk-engine early but doesn't ramp discounts. Different textures, comparable
  payoff — the sim's #1 probe.

### Designing out the top risk (b): no economy runaway

The compounding discount **must not snowball past the end-clock**. **The brake (stated plainly): the
discount applies only to the *ingredient* half of a vendor's cost; the *Buzz* half is never discounted.**
So even a fully-ramped engine still pays Buzz for every vendor, and Buzz arrives one action at a time
(+2/Promote). This **caps the courting *rate*** at roughly **1 vendor per 2 turns** even at full ramp
(1 Promote + 1 Court), versus ~1 per 3–4 turns early — a real, satisfying ramp (≈2×) but **not an
explosion** (never 1/turn). Supporting brakes:
- **Diminishing returns:** the vendors you can court fastest at full ramp are the *cheap* ones (T1, 1
  Prestige) — courting *rate* rises but *VP per court* falls.
- **Shared Board scarcity:** the rival can **snipe the vendor whose icon you needed** to ramp, capping your
  discount growth (direct interaction, "outraced not robbed").
- **The end-timer co-brake:** fast courting fills the Season timer → hurries the end → the leader can't
  bank unlimited courts; the slower/tall player gets more turns to reach parity.
- **Buzz income is soft-capped:** only the +1-Buzz perk (one T2 option) and the pass-6 Rep perk raise Buzz
  income, additively and modestly — Buzz income never compounds freely.
- **Reserve knobs if the sim flags snowball:** a trailing-player discount (first court each round costs 1
  less Buzz), a per-player vendor cap, or a Buzz-cost floor increase on the cheapest tier.

---

## Market & Events (the sourcing layer — "Conditions" folded in)

- Each region has a face-up **Market** (3–4 slots) drawn from a **finite, event-salted supply** (region
  specialty tokens **+ ~2–3 Event tiles**). **Pantry** is **unlimited** anywhere.
- **Scarcity:** finite specialty supply ≈ **2× solo demand** — two players can't both max the same
  specialty; grabbing the last forces a rival **reroute** (free interaction + anti-hoard). The **unlimited
  pantry** and **always-available Buzz** are the two anti-stuck valves — luck/scarcity costs *tempo or a
  reroute, never a court*. Supply scales **sub-linearly** with count so contention persists at 3–4p.
- **Events fire on refill.** After you Stock Up/Travel and refill a Market slot, a flipped **Event** tile
  resolves immediately (then continue refilling). Take-2 = up to two flips = more exposure (push-your-luck
  baked in). Boon-skewed **~60/40**, region-thematic, **tax-not-destroy** (hazards delay/reroute, never
  remove what you hold or a whole turn). Known composition + face-up Market telegraph the odds.
- **Season is now a pure end-timer** (fires nothing) — the v2 ACTIVE/NEXT queue + milestone-fire machinery
  is **cut**. The living-island feel now lives *in the Market*.

**Event starter set (~11; secular, boon-skewed; wording via the Taiwanese consultant before lock):**
1. **芒果季 Mango Season** *(S, boon)* — add **2** extra South specialty tokens to the South Market (a
   glut both agents can grab).
2. **蚵仔盛產 Oyster Glut** *(S, boon)* — the drawer takes **1 free** oyster.
3. **珍奶節 Bubble-Tea Festival** *(C, boon)* — the drawer takes **2 Buzz** (the town's buzzing).
4. **豐收 Bumper Harvest** *(E, boon)* — the drawer takes **2 free** East specialty tokens.
5. **觀光季 Tourist Season** *(table-wide, boon)* — every agent's **next Promote** gives **+1 Buzz**.
6. **快閃排隊 Pop-Up Queue** *(any, boon)* — the drawer may immediately **move 1 region for free** (a lift
   to the next town).
7. **食尚報導 Featured in the Guide** *(boon)* — the cheapest face-up **T1 vendor** gains **+1 Prestige**
   (tempting a court).
8. **暖心街坊 Word of Mouth** *(warm, boon)* — the drawer gains **+1 Buzz and +1 ingredient** (a kind local
   sets you up).
9. **颱風警報 Typhoon Warning** *(coast S/E, hazard)* — **wash out** the affected region's face-up
   specialty tokens (discard + refill); you lose nothing you hold — the *shelf* resets away from what you
   wanted (a reroute, not a theft).
10. **梅雨 Plum Rains** *(C, mild hazard)* — the drawer's **Stock Up this turn yields 1 fewer** (a slow
    day; tempo tax).
11. **客滿 Fully Booked** *(any, shake-up)* — clear and refill an entire Market row (can help or hurt).

Warm characters = the "get lucky" beats; **dignified hosts, never a punchline**. The **Gourmand cannot
benefit from boon events** (their flaw); the **Rookie draws 2 events / resolves 1** in their region (their
ability). *Reserve knob:* if immediate-fire feels too random in the feel-test, add a one-beat **"brewing"
telegraph** (event fires at the start of the drawer's next turn) — ~1 rule, restores preview agency.

---

## Characters — asymmetry that bends the engine

Five warm, food-obsessed **agent** archetypes (personality/role, **not** ethnic caricature — see
sensitivity), each **public** (the opponent adapts), each **one ability + one flaw on an opposing lever**.
Abilities are **flat/bounded — no compounding engine powers** (they must not stack on the vendor ramp).
Target EV ≈ 2–4 VP or ~1–2 turns of tempo; the flaw costs about the same.

| # | Character | Ability | Flaw | Lever / anti-lever |
|---|-----------|---------|------|--------------------|
| 1 | **The Night-Market Auntie 阿姨** | *Regular's Discount* — the first vendor you court in **each of your first two regions** costs **1 fewer ingredient** (she vouches for you). | *Set in her ways* — **no HSR** (N↔S); routes the ring the long way. Loves the scenic local rail, knows every backstreet (**not** a technophobe gag). | discount / anti: mobility |
| 2 | **The Eager Rookie** | *First-Timer's Luck* — when an **Event** fires in your region, **draw 2 tiles, resolve 1**. | *Bites off too much* — **Larder cap 6**. | events / anti: storage |
| 3 | **The Retired Conductor 車長** | *Off-Peak Pass* — **Travel arrives with 2** ingredients (a proud, expert retired railwayman). | *Timetable-bound* — **Stock Up takes 1** (hates standing still). | mobility / anti: camping |
| 4 | **The Influencer** | *Going Viral* — your **Promote takes +1 Buzz** (3). | *Chasing clout* — goes **last** in turn order and starts **2 resources behind**. | Buzz engine / anti: tempo |
| 5 | **The Grizzled Gourmand** | *Connoisseur* — once per turn, treat **1 pantry as any 1 specialty** when courting (courting flexibility). | *Too jaded* — **cannot gain Buzz from boon events** (still gets their other effects). | flexibility / anti: events |

*(6th, held as expansion — hardest to balance:* **The Homesick Local**, +/− tied to a self-picked home
region.)*

**No dominant character×mission combo (designed, sim-confirmed).** Each ability sits on a *different*
lever, and each has a flaw that **pulls against the mission it most helps**:
- Auntie's discount most helps the **breadth/all-4-regions** missions — capped to your **first two
  regions** so it can't compound with a grand-tour mission (the sim found the uncapped version + no-HSR
  did NOT self-balance: Auntie×grand-tour hit 82%; the first-two-regions cap fixes it → Auntie ≤53% vs any
  mission).
- Influencer's +Buzz most helps the **Buzz-hungry tall / 2-Marquee** mission — but she **starts behind and
  goes last**, paying tempo up front.
- Conductor's travel-sourcing most helps **spread/coverage** — but his **Stock Up 1** flaw slows any
  single-region stockpile (fighting the "3 in the South" mission).
- Gourmand's wild most helps **specific-cuisine** missions — but **no boons** loses the festival tempo the
  ramp likes.
- Rookie's event-luck is **generic** (no track it doubles) — the safe baseline.
The **draw-3-keep-1 pick** further launders this: a broken combo can't be gifted; you choose it and the
opponent, seeing your character, contests. Sim probe #3/#4 (post-rebalance, fixed game length): every
character **45–55%** (Auntie 52–54 · Conductor 53–55 · Rookie 51 · Influencer 46–47 · Gourmand 45–47); no
character×mission combo **>~60%** (worst ~57%).

> **Table watch-flags (the sim's honest limit).** The sim abstracts the Market **events** it can't fully
> model, so two characters are carried **as-printed pending the human FTUE session**, not tuned off the
> sim: the **Rookie** (her whole kit rides on event luck) and the **Gourmand** (his pantry-wild flexibility
> is invisible to the greedy bots — it only pays under human tight-hand pressure). The **Auntie**
> (first-two-regions) fix is sim-confident; the **Influencer** (2-behind) is a low-risk provisional nudge.
> Instrument the first playtest to record per-character results and specifically whether Rookie's event-luck
> and the Gourmand's wild earn their keep.

---

## Randomness

- **Input randomness (the bulk):** the Vendor Board reveal, the Market reveal, the Mission draw
  (mitigated by **draw-3-keep-1**), the vendor/market deck orders — all telegraphed/face-up; you **adapt**.
- **A bounded slice of output randomness:** the **event-on-refill** flip resolves *after* you chose to
  Stock Up. Deliberately bounded to *spice, not decide*: **boon-skewed ~60/40**, **tax-not-destroy**,
  known deck composition, and the **pantry + Buzz** anti-stuck valves. Take-2 is opted-into push-your-luck.
- **No dice, no post-court luck.** Suits the warm "nail your trip" tone; keeps the engine's skill legible.
- **One hidden-information hook only:** your **secret signature mission**. Larder is face-up; the Board,
  both tours, the VP track and the Rep track are all open. No deduction engine.

---

## Interaction & tension

**Direct (the spine):**
- **The Vendor Board race.** Courting a vendor **locks it from the rival** — and, crucially, locks away the
  **region icon** they may have needed to ramp, or the **marquee** they wanted for Prestige. The race lives
  in *timing and routing* ("she's one oyster from courting the seafood marquee — I grab it first, or race
  her South"). Razor-sharp at 2p. **Anti-resentment (carried from v2):** the ingredients + Buzz you spent
  still bought you Prestige + Rep + a discount + coverage, so a snipe reads as **"outraced, not robbed"** —
  and thematically the vendor simply **chose the agent who courted them best**, never a place being seized.
- **Market scarcity.** Taking the last of a contested specialty forces the rival to reroute (free,
  impersonal, anti-hoard).
- **The Poach (v3.1) — the same-location swipe.** When you and your rival are nose-to-nose in the same
  region, you can cheekily grab something they hauled. Detail below.

### The Poach (same-location steal — v3.1)

**Trigger + cost + effect** (as in *Actions*): on your turn, **if a rival's pawn shares your region**, you
may **Poach** instead of your normal action: take **1 random specialty** from that rival's Larder into
yours and move your **Reputation down 1** (floored at 0). Pantry is ignored (unlimited — nothing to swipe);
if the rival holds only pantry, there's nothing to Poach. It touches nothing else (no Market refill, no
event, no Season tick).

**What's stolen — and why *random specialty* is the fun, low-feel-bad pick** (the design call):
- **Not a vendor** (would undo scored Prestige + a discount + coverage — massively swingy, feel-bad, and it
  *violates the anti-extraction rail*: a vendor **chose** you, you can't steal a blessing). **Not the
  mission** (the only hidden info — stealing it wrecks the one secret and breaks the no-deduction rule).
  **Not Buzz** (location-independent — Promote anywhere — so it wouldn't reward *tracking movement*, the
  whole point).
- **A random specialty from the face-up Larder** is the sweet spot: it's **material the rival *traveled*
  for** (so poaching it rewards Change 1's movement and synergises with it — fuller Larders from more
  travel are juicier targets), it's **bounded** (Larder cap 7; one token ≈ half a Stock Up), and **random
  (not chosen)** keeps it **cheeky, not surgical** — you can *see* they're holding good stuff (face-up) so
  the decision to spend Rep is informed, but you can't cherry-pick the single scarce token, so it never
  becomes a precision engine-kill. Excluding pantry means a Poach that lands always *means* something.

**Why it's a real risk-reward, not a griefy staple:**
- **It costs your whole turn** — you gave up a Stock Up (+2), a Promote (+2 Buzz), or a Court. A Poach
  yields **+1 ingredient to you and −1 to them** (a 2-swing on a *contested* token), with **no** refill/
  event/reposition. So it's **usually worse than Stock Up** — you only Poach when the specific denied token
  *matters* (the rival is one oyster from the seafood marquee; a scarce specialty you can't easily source
  yourself). A situational tempo/**denial** play, not an every-turn move.
- **The Rep cost is a genuine price now** that Rep scores only at your **final** track position (v3
  end-trigger fix). Each Poach chips Rep, which converts to end-VP (bands at 3/6/9/12) **and** costs
  milestone perks (passing 3/6/9). Spam three Poaches ≈ pay ~3 Rep ≈ a whole scoring band and maybe a
  missed perk — a real, compounding tax on the material you're grabbing.
- **The Rep floor (0) is the early-game guard:** you can only Poach if you have standing to spend, i.e.
  you've **courted at least one vendor** — so it's never a turn-1 grief tool, and total Poaches are capped
  by the Rep you can afford to burn.
- **No spiral (state it plainly for `bg-elegance`/sim):** a "steal war" (A poaches B, B poaches back) is
  **self-correcting** — both burn a turn *and* a Rep for a net-zero material swing, so neither gains; and
  it has two free exits — **move away** (break co-location) or **hold a pantry-lean Larder** (nothing to
  steal). Nobody rationally sustains it. Season is untouched, so Poach is not an end-clock lever either.

**Tone (binds — `identity.md`):** warm agent-vs-agent slapstick — you're both crammed at the same
night-market corner and you swipe the oysters off their tray / call in a cheeky favour to nab the last of
something first. Targets **the rival agent only, never a vendor or the place.** The Rep ding = *"word gets
round that you play a little dirty."* Keyword proposal **"Poach"** (a cooking term *and* a
poach-a-rival's-client wink) or **"Tip-Off"** — final name is `bg-theme`'s call.

**Reserve knobs (if the sim/table flags it):** Rep cost 1→2 if spammed; 1→0 or "free rider once/turn on a
Travel/Stock Up" if it's a dead rule (see the A/B for the human); a hard "once per turn" is already implied
(Poach *is* your turn). Do **not** let it steal vendors/missions/Buzz — those break the rails above.

**Indirect:** the shared Market events (table groans at a typhoon, races to a festival); the **Season**
timer (a fast courter times the end); **Extract** tempo.

**Catch-up vs runaway (the make-or-break, designed):**
- **Against runaway:** the **Buzz floor** caps courting rate; **diminishing returns** on cheap vendors;
  **shared scarcity** caps ramp; **soft-capped Buzz income** (see *Scoring out risk (b)*).
- **For catch-up (gentle, not leader-bashing):** the **end-timer co-brake** (fast courting hurries the
  end; the slower player gets more turns), the **multi-track structure** (a trailing player always has a
  live second vector — Coverage or the hidden +7 — not a single collapsing race), and the **reserve
  trailing-discount knob**.

**Fellowship after cutting co-op:** carried by shared Market drama + warm rivalry over the Board ("you did
*not* just court my noodle guy") — matching `identity.md`'s definition of Fellowship (warm rivalry + table
talk), not mechanical co-op.

---

## Player counts & scaling

Base = **2p** (the design home). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Vendor Board per tier** | 3 | 4 | 4–5 |
| **Region Market slots** | 3–4 | 4 | 4 |
| **Specialty supply** | ≈2× solo demand | sub-linear (≈2.6×) | sub-linear (≈3.2×) |
| **Season final (courts)** | ~16 | ~24 | ~30 |
| **Reputation top** | 12 | 12 | 12 |
| **Start positions** | opposite (N & S) | spread on the ring | spread |
| **Missions** | draw 3 keep 1 | draw 3 keep 1 | draw 3 keep 1 |

Supply scales sub-linearly so contention persists; the Board widens to keep vendors available. Turn order
matters more at 3–4p (the Influencer's "goes last" flaw is heavier — `bg-architect` to confirm it stays in
the 45–55% band at count, or soften to "−1 resource only" at 3–4p). Resentment is **lower** at 3–4p (a
snipe is diffuse); the sharp case to design/sim is **2p**. **Best-at: 2p**; 3–4p is a warmer, longer race.

## Solo mode / Automa

**Medium priority** (near-expected on a mid-weight engine now; still a bonus behind the 2p duel). Sketch —
a **"Rival Agency" Automa**:
- A small **Route deck**. On its turn, flip the top card: it **courts** the highest-Prestige Board vendor
  it can "afford" against running ingredient + Buzz counters (Season +1; locks it from you — so the Board
  race still bites solo), **or** takes Buzz, **or** rotates the region it "sources" from.
- Pressure = **tempo + the Board race + the end-timer**: it courts steadily to hurry the Season and snipe
  your ramp targets. Difficulty = court-aggressiveness (deck ratio) + a target score. Upkeep near-zero
  (one flip, one lookup). **Defer to `bg-architect`; not in the base MVP.**

## Complexity budget

Target **~2.2–2.4, ceiling 2.5**; `complexity-budget.json` caps (rulebook 1650 words, keywords 15,
component types 8, aid 22 lines); `bg-elegance` guards.

- **The weight call (honest).** The engine is the deliberate spend: **Buzz + Promote** (a real second
  economy axis), the **compounding discount** (the ramp), the **Reputation track + milestones** and
  **Coverage** (the multi-vector depth), and **5 characters** (~+0.1–0.15 teach cost). We **bank**: Briefs
  **cut** (−1 deck, −1 keyword), the **Conditions queue** collapsed to Market tiles (−1 subsystem),
  Hot-List **merged** into the Board (no separate row). The two-input beat **replaces** (not adds to) the
  plate-and-score beat. **Net ~2.3–2.4** — in the aim band, off the ceiling.
- **Actions = 5 core + 1 conditional** (Stock Up / Travel / Promote / Court / Extract, **+ Poach** when
  co-located). Poach is the only v3.1 weight add: **conditional** (teaches only when two pawns meet),
  reuses existing pieces (Larder + the Rep track as its cost), no new component — an honest **~+0.05–0.1**.
  Change 1 is **weight-neutral** (pure re-costing) and arguably *reduces* teach friction: the v3
  "icon≠named-ingredient" confusion the developer flagged (a South vendor costing North pork) goes away
  when vendors **anchor in-region**, partly offsetting Poach. Net still **~2.35–2.45**, under the 2.5
  ceiling but eating headroom — `bg-elegance` guards; if it drifts past 2.5 the first trim (Rep milestones
  → pure end-VP) recovers ~0.15. *Elegance option held:* fold **Promote into Travel** to hold 4 core
  actions if the gauge drifts.
- **Keywords ≈ 12–13** (under 15): Larder · Vendor · **Court** · **Buzz** · **Promote** · region
  **discount icon** · **Prestige** · **Reputation** · **Coverage** · **Event/Condition** · signature
  **Mission** · Extract · **Poach** *(v3.1)*. (Stock Up / Travel / specialty / pantry stay plain-language.)
- **Trim order if we drift >2.5, in order:** (1) **Reputation milestone perks → pure end-VP** (recovers
  ~0.15; Rep becomes a clean parallel scorer + endgame trigger); (2) **Coverage → mission-only breadth**
  (recovers ~0.1); (3) **characters 5→4** (drop the Influencer or Gourmand — hardest to balance); (4)
  **fold Promote into Travel** (4 actions); (5) **cap the discount** (flat max) if the ramp misbehaves.
  Depth lives in the *two-input engine under a contested Board + living Market* — protect that, cut around
  it.

## Keywords / glossary

- **Larder** — your sourced ingredients, **face-up** (not a hidden hand). Cap **7** (6 for the Rookie).
- **Vendor** — a Board card (tiered) you **court** to secure; carries cost (ingredients + Buzz), a region
  **icon** (discount + coverage), **Prestige**, **Reputation**, and a **perk**.
- **Court** — the core action: pay a vendor's ingredients (− discount) + Buzz to secure it; it locks from
  the rival (they were **outraced, not robbed** — the vendor chose you).
- **Buzz** — the second, fungible currency; you **Promote** to gain it; **never discounted** (the ramp
  brake). Spent alongside ingredients to court.
- **Promote** — the action that takes Buzz.
- **discount icon** — a vendor's region badge; each held reduces that region's ingredient cost on future
  vendors by 1 (floored at 0). The compounding engine.
- **Prestige (VP)** — a vendor's star value; the headline VP vector; live on the VP track.
- **Reputation** — the parallel track climbed by courting; milestone perks + end-VP; its top ends the game.
- **Region-Coverage** — end-game breadth bonus for distinct regions among your vendors (2/5/9).
- **Event / Condition** — a region-thematic Market tile (festival / hazard / warm local) that fires on
  refill. Secular only.
- **signature Mission** — your secret **+7** vendor pattern (draw-3-keep-1); the only hidden info.
- **Extract** — the action that triggers the end-game wind-down ("file the tour / catch the last train").
- **Poach** *(v3.1)* — the conditional same-location action: when a rival shares your region, take 1 random
  specialty from their Larder and pay −1 Reputation. Warm agent-vs-agent swipe; targets the rival only.

## Open questions for playtesting (top 3)

**v3.1 adds two probes the re-sim must lead with (before re-confirming the v3 three below):**

- **A. Does movement actually spread? (Change 1's make-or-break.)** The rebalance is *designed* to even
  out demand, but even demand on paper ≠ travel in play — **anchoring in-region could let a player camp a
  region and court locally**, so the **cross-link rate (~40%) is the load-bearing knob.** *Attack:* re-cost
  the sim's vendor model to the target distribution, then measure **per-region sourcing share** (target:
  each region ≥~18% of ingredient-take actions; South rises from near-zero) and **inter-region moves per
  game** (should climb), and confirm the **stay-home-North line is no longer a top strategy** (Probe 1
  re-run — no line >~55%). *Fail fixes:* raise/lower the cross-link rate; nudge the per-specialty targets;
  strengthen Coverage/marquee pull out of North.
- **B. Is the Poach a fun risk-reward, or degenerate/griefy? (Change 2's make-or-break.)** *Attack:*
  **Poach frequency/game** (should be low, situational — not every-turn), **win-rate of a Poach-lean
  strategy** (≤~55%), **steal-war frequency** (should be ~0 — self-correcting), and **Rep spent on Poach
  vs Rep-VP forgone** (is the −1 cost real?). *Fail fixes (reserve knobs):* Rep cost 1→2 if spammed; 1→0
  or a free once/turn rider if it's a dead rule. The *feel* ("cheeky not mean") is a human-only Screentop
  question. **Bound check:** confirm a 2p duel can't spiral into griefing (the turn-cost + Rep-tax +
  move-away/lean-Larder exits should hold).

1. **No dominant track or opening? (THE make-or-break.)** Do **tall (Prestige) ≈ rep-climb ≈ breadth**
   land competitively, and is **ingredient-heavy ≈ Buzz-heavy** as an opening? *Attack:* the sim's
   dominant-track/opening probe (pass = no line >~55%, ≥3 viable) + a 2p Screentop feel-test (does one path
   *feel* solved?). *Fail fixes:* rebalance vendor costs / track rewards / discount strength.
2. **No economy runaway past the end-clock?** Does the **Buzz floor** actually cap the ramp (does a fast
   first-courter run away, or do the brakes hold)? Is the binding-constraint *shift* (ingredients→Buzz)
   real and fun? *Attack:* the runaway probe (measure court-rate ceiling, leader VP-gap over time). *Fail
   fixes:* trailing-discount, vendor cap, discount cap, higher Buzz floor.
3. **Do the characters seat in 45–55%, with no dominant char×mission combo?** And do the Market events feel
   *swingy-fun*, not *random*? *Attack:* round-robin 5×5 + mirror control; win-rate per character
   conditioned on mission; the feel-test for events. *Fail fixes:* re-tune the one offending ability/flaw;
   exclude a mission from a character's implied pool; add the "brewing" telegraph.

## Handoff notes (guardian sweep — where to look)

**v3.1 — what moved (run `bg-theme` coherence + `bg-elegance` budget on the change):**
- **The signature twist did NOT move** — the vendor-courting engine is untouched. What moved: (1) **vendor
  costs re-balanced for movement** (South/Central specialties now demanded; `bg-developer` re-costs
  `vendors.csv` + `ingredients.csv` supply to the *Movement rebalance* spec); (2) **a new conditional
  Poach action** (same-location steal, −1 Rep). Neither touches the engine, the tracks, or the Buzz brake.
- **`bg-theme` check (the load-bearing one):** does the **Poach** read **warm agent-vs-agent slapstick**
  (a cheeky swipe at your *rival*, never a vendor or place) — the anti-extraction rail must hold; the
  keyword ("Poach"/"Tip-Off") is theme's call. And do the **re-costed vendors** still keep every dish
  *real* (the anchor ingredient true; the CD "connections you bring" framing used only for cross-links,
  routed past the consultant)? — the *never-mangle* rail binds.
- **`bg-elegance` check:** the honest ledger — Poach is a **conditional 6th action** (~+0.05–0.1, no new
  component), Change 1 is weight-neutral and may *reduce* teach friction (icon-matches-cost now). Net
  ~2.35–2.45, headroom thinning; first trim (Rep milestones → pure end-VP) held in reserve.
- **`bg-theme` events pass (in parallel):** the rebalance needs **no event respec** — it only makes
  South/Central boon events (Mango Season, Oyster Glut, Bubble-Tea Festival) bite harder (their specialties
  are now demanded). Keep the events market-compatible; a plus for the "funnier events" work.
- **`bg-playtest`:** re-cost the sim vendor model to the target distribution + add the Poach action, then
  run probes **A (movement spread)** and **B (Poach risk-reward)** above before re-confirming the v3 three.

---

**The signature twist has moved.** v2's twist was the Hot-List race on the same cards as the secret
itinerary. **v3's signature twist is: you *court the island's vendors* — paying fresh ingredients + Buzz —
and each secured vendor is an engine piece (a compounding discount) that also climbs Prestige, Reputation
and Coverage toward your hidden signature tour; the shared Vendor Board is the rival race.** Trigger
`bg-theme` (does *courting = the vendor granting their blessing to the agent they like best* read warm and
anti-extraction? is Buzz-as-promotion coherent? are the 5 characters warm/varied, not caricature? events
secular?), `bg-elegance` (is the ~2.3–2.4 ledger honest — Buzz + Characters + Event tiles as new types,
Briefs cut, queue collapsed, Hot-List merged?), and — because component data + theme moved — `bg-access`
(the busier board: Vendor Board + two tracks + region Markets keep dual-coding) and `bg-infodesign` (is a
vendor card parseable at a glance — cost / icon / Prestige / Rep / perk?).

**Cut mechanics to sweep for stranded names/rules:** **Plate**, **Dish** (now Vendor), **Briefs**, the
**Conditions queue** (ACTIVE/NEXT), the **Hot-List** as a separate row — check nothing in
components/rulebook/sim still references them.

**New rules the fiction must explain:** **Buzz/Promote** ("bring people to the food"), **Court** ("the
vendor blesses your tour"), the **discount icon** ("regulars vouch for you — the next stall's an easier
sign"), **Reputation** ("your standing as an agent"), **Region-Coverage** ("the grand tour"), **Events in
the Market** ("the island living its life"), **Extract** ("catch the last train").

**`bg-developer` data:** vendor cards (cost = named ingredients + Buzz; region icon; Prestige/Rep/perk) by
tier; the Mission pool (+7 patterns, draw-3-keep-1); the Buzz supply; the Reputation track + milestone
perks + Coverage bonus printed on the board; region Market supplies with **~2–3 Event tiles each**; 5
Character mats; add **chicken 雞 + egg 蛋** North tokens; keep vendor region-icons **balanced across
regions** despite North's 4 specialties.

**`bg-playtest`:** rework `sim/travel_agents.py` to model **court-a-vendor + two inputs + the discount
ramp + the three tracks**, then run the three probes above (dominant-track/opening, economy-runaway,
per-character 45–55%) + an early 2p Screentop feel-test for engine satisfaction + event feel.
