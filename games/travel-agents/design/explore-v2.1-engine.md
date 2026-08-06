# Travel Agents: Taiwan — Explore v2.1: The Vendor-Courting Engine

`bg-explore`, 2026-08-06. **Fresh CD direction — a core reframe of model C v2** (`design/design-doc.md`).
The scoring beat is no longer *"cook/Plate a dish"* (that's a chef) — you are a **travel agent** who
**courts vendors to secure exclusive rights** to feature their stall on your tour. **Securing a vendor is
the core scoring + engine beat.** This doc proposes the integrated v2.1 core (vendor-courting, two
inputs, the engine, the tracks), then folds on the layers already explored (events-in-sourcing, limited
region pools, agent characters, start-of-game mission draft), then lays out the CD forks, the riskiest
assumption, and the sim plan.

**Budget (raised, CD):** aim **~2.2**, ceiling **~2.5** — the **Splendor Duel / Duel for Middle-earth /
Arnak** band. Real depth is now on the table; every rule still earns its place. `bg-elegance` guards.

**KEEP from v2 (explicitly):** **recipes-by-region** as the ingredient input (the "travel because the
food lives there" engine); the **public rival race** (the v2 Hot-List, now the **Vendor Board**); the
**secret signature itinerary (+7)** as the hidden headline; the **live tracker(s)**; **Extract**.
Discovery still leads; Fellowship via shared market/rivalry drama; Challenge via the routing + engine
puzzle. **References the CD named:** Splendor Duel (tokens→cards→engine + multiple win vectors), Duel for
Middle-earth / 7 Wonders Duel (several win paths in a tight 2p box), Arnak (a parallel progression track
beside VP).

---

## 0. TL;DR — the v2.1 engine at a glance

You collect **two inputs** — **fresh ingredients** (region-specific, the v2 sourcing engine) and
**Buzz** (a new fungible promotional currency) — and spend them to **court Vendors** off a shared,
tiered **Vendor Board**. Each secured vendor is an **engine piece** (a permanent discount that compounds,
à la Splendor) **and** feeds **multiple scoring vectors** (Tour Prestige, Reputation, Region Coverage),
so there are **several viable paths to Top Agent**. The v2 layers ride on top: **events + scarcity** live
in the ingredient market; **characters** give each agent an ability+flaw that bends the engine; the
**hidden mission** is a secret vendor pattern worth +7.

| v2 (model C) | v2.1 (proposed) |
|---|---|
| **Plate a Dish** (spend a recipe → VP) | **Court a Vendor** (spend **ingredients + Buzz** → secure it) — the two-input engine beat |
| Dishes / Menu | **Vendors / Vendor Board** (tiered, refilling; recipes-by-region = *what a vendor needs*) |
| **Hot-List** (separate public bonus row) | **merged INTO the Vendor Board** — the public race *is* courting vendors (−1 subsystem) |
| Single live VP total | **Multiple vectors**: Tour Prestige (VP) + Reputation track + Region-Coverage bonus (+ hidden mission) |
| Ingredients only | **Ingredients + Buzz** — a real two-input economy (past *Yes! Ginseng* collection) |
| — | **Vendor bonuses = permanent discounts that compound** (the engine ramp) |
| Conditions deck + Season queue | **Events salted into the ingredient market** (fire on refill) |
| Briefs deck | **CUT** — jobs re-homed (gamble/luck→events; flexible resource→Buzz; blocking→scarcity; boost→characters) |
| Symmetric players | **Agent Characters** (1 ability + 1 flaw) |
| draw-2-keep-1 objective | **draw-3-keep-1 mission pick** (hidden +7 vendor pattern) |

**Honest weight:** this is a **real depth increase** over v2's plate-and-score — a two-input economy + an
engine-ramp + 2–3 scoring vectors lands around **~2.2–2.4** (Splendor Duel ~2.2, 7WD ~2.2, Arnak ~2.8).
That is **in the raised band** and is the depth the CD asked for. We *bank* real simplifications
(Hot-List merged into the board, Briefs cut, the Season/queue coupling gone) to pay for the engine, so it
does **not** balloon toward the ceiling. `bg-elegance` to hold ~2.2–2.4.

---

## 1. The recommended integrated core

### 1a. The core beat — Court a Vendor *(replaces Plate a Dish)*

A **Vendor** is a stall/cook you sign to your tour. To **court** one you pay its price = **named
ingredients + Buzz** (minus your discounts, see engine). The vendor joins your **tour**, and you gain,
all at once:
- **Tour Prestige (VP)** — the vendor's star value (the headline scoring vector);
- **a Reputation bump** — advances you on the Reputation track (the second vector);
- **an engine perk** — an ongoing bonus, usually a **permanent discount** of its region/cuisine that
  makes *future* vendors cheaper (the compounding ramp);
- possibly a **Region-Coverage** tick (a vendor in a new region).

Then refill the Vendor Board, advance the **Season** end-clock, and — because courting **locks the vendor
away from your rival** — the public race resolves (the v2 Hot-List snipe, re-themed: *you signed them
first*).

**Why two inputs (the CD's "get past collection").** A vendor needs both **what a stall needs to shine**:
- **(a) fresh ingredients** — region-specific, sourced where they live (recipes-by-region intact; the
  vendor's signature dish defines the named ingredients — real Taiwan food geography still does the
  work);
- **(b) Buzz** — you **promote** them, promising customers and hype. This is **literally the travel
  agent's job** (bring people *to* the food), which nails the identity's anti-extraction linchpin:
  courting = *showcasing/helping the vendor*, never taking from them.

Two inputs with **deliberately different textures**: ingredients are **specific, contested, travel-gated,
event-risky**; Buzz is **fungible, always-obtainable, safe**. The interplay ("I have the oysters but not
the Buzz; do I Promote or race the rival to the vendor now?") is the new decision spine.

### 1b. The engine — vendor bonuses compound *(the Splendor ramp)*

Most vendors carry a small **bonus icon** (a region/cuisine). Your courting cost is reduced by **1 per
matching bonus you already hold**, exactly like Splendor's permanent gem discounts. So:
- early vendors are cheap and slow; each one you sign makes a *class* of future vendors cheaper;
- a leader who courts first ramps faster → **this is the runaway risk the sim must watch** (§8), braked
  by the shared end-clock (a faster courter hurries the end) and the rival race (they can snipe your ramp
  targets).

Higher **tiers** of vendor (Board is tiered like Splendor's rows) cost more, give more Prestige/Rep, and
carry stronger perks (a bigger discount, a **Buzz generator**, a **sourcing perk**, or a **Reputation
engine**). The engine is genuine: tokens (ingredients + Buzz) → cards (vendors) → compounding
discounts → multiple win vectors.

### 1c. The tracks — several paths to Top Agent *(the depth)*

Kept to **two real vectors + a coverage rider + the hidden mission** — Splendor-Duel-tight, not a heavy
euro:

1. **Tour Prestige (VP)** — sum of your vendors' star values. The **prestige-rush** line (court high-tier
   vendors fast).
2. **Reputation track** — a parallel progression (Arnak-style) climbed by courting (each vendor gives
   Rep) and by certain vendors/actions. **Milestones grant engine perks** (a free discount, +Buzz income,
   a wild) **and end-game VP**. The **reputation-climb** line (court rep-heavy vendors, snowball perks).
3. **Region Coverage** — an end-game **set-collection bonus** for breadth (a vendor in each of the 4
   regions scores escalating VP). One scoring line, not a subsystem — keeps **routing** relevant to
   scoring so the travel engine still matters. The **breadth/grand-tour** line.
4. **Hidden mission (+7)** — a secret vendor pattern (see §2d), the dramatic reveal.

These are **genuinely different strategies** (rush tall vs climb rep vs spread wide vs chase your secret
pattern), which is the multi-path depth. **Endgame (Fork 2):** recommend the tracks **trigger** the
wind-down and pay a bonus, but **highest total VP wins** (warm, non-feel-bad) rather than brutal
Splendor-style sudden-death.

### 1d. The revised core loop / actions

Short turns, low downtime (2p-tight). A turn = **one action**:
| Action | Effect |
|---|---|
| **Stock Up** | take **2 ingredients** at your region's Market (events + scarcity ride here, §2a). |
| **Travel** | move 1 region (HSR N↔S), arrive with **1 ingredient**. |
| **Promote** | take **Buzz** (the second currency) — the always-available soft input. |
| **Court a Vendor** | pay ingredients + Buzz (− discounts) → secure a Vendor (Prestige + Rep + perk + coverage); refill the Board; Season +1; lock it from the rival. |
| **Extract** | trigger the end-game wind-down. |

Five action-types, all simple (Splendor is essentially take-tokens / buy-card; we split "take" into
ingredients / Buzz / travel because they carry the routing + risk texture). **Elegance option (Fork
held):** fold **Promote** into **Travel** ("tour a region → arrive with 1 ingredient + 1 Buzz") to hold
**4 actions** if `bg-elegance` wants — at the cost of tying Buzz to movement.

---

## 2. The layers, folded onto the engine

### 2a. Events + scarcity = the ingredient Market *(gates input a)*
Unchanged in spirit from the prior explore pass, now feeding the *ingredient* input:
- Each region has a **face-up Market row** (4 slots) refilled from a **finite, event-salted supply**;
  **pantry** (generic ingredient) is **unlimited** anywhere.
- **Stock Up** takes up to 2 face-up goods; refilling flips can surface a **region-specific event** (boon
  or light hazard) → **risk on every stockpile**, and **take-2 = two flips = more risk** (push-your-luck
  baked in, no extra rule).
- **Scarcity:** finite specialty supply → grabbing the last forces a rival reroute (free interaction +
  anti-hoard); the **unlimited pantry + always-available Buzz** are the **two safety valves** so no one is
  ever hard-stuck. Rough counts: region deck **~12–16 goods + ~3 events**, row of 4, supply **≈2× solo
  demand** so two players can't both max out (Fork 3 tunes tightness). Scales **sub-linearly** with count
  so contention persists at 3–4p.
- **Season → end-timer only** (fires nothing now; +1 per Court → final milestone can end the game). The
  v2 ACTIVE/NEXT queue + milestone-fire machinery is **cut**.

### 2b. Agent characters = asymmetry that bends the engine
Five warm, food-obsessed **agent** archetypes (personality/role, **not** ethnic caricature — §9), each
**public** (opponent adapts) with **one ability + one flaw on an opposing lever**, now hooked to the
engine:

| # | Character (fiction → bg-theme/consultant) | Ability | Flaw | Engine lever |
|---|---|---|---|---|
| 1 | **The Night-Market Auntie 阿姨** | *Regular's Discount* — the first vendor you court in each region costs **1 fewer ingredient** (she vouches for you). | *Set in her ways* — **no HSR** (routes the long way). | vendor discount / anti: travel |
| 2 | **The Eager Rookie** | *First-Timer's Luck* — when an **event** fires at your region, **draw 2, resolve 1**. | *Bites off too much* — **Larder cap 6**. | events / anti: storage |
| 3 | **The Retired Conductor 車長** | *Off-Peak Pass* — **Travel arrives with 2** ingredients. | *Timetable-bound* — **Stock Up takes 1** (hates standing still). | mobility / anti: camp |
| 4 | **The Influencer** | *Going Viral* — your **Promote takes +1 Buzz**. | *Chasing clout* — goes **last** in turn order; starts 1 resource behind. | Buzz engine / anti: tempo |
| 5 | **The Grizzled Gourmand** | *Connoisseur* — once per turn, treat **1 pantry as any 1 specialty** when courting (the cut Brief's wild, re-homed). | *Too jaded* — **cannot benefit from boon events**. | courting flexibility / anti: events |

*(6th, held as expansion — hardest to balance:* **The Homesick Local**, +/− by a self-picked home
region; strong self-selected synergy with breadth/crawl missions.)* Abilities are flat/bounded — **no
compounding engine powers** (avoids stacking on the vendor ramp → runaway). Target EV ≈ 2–4 VP or ~1–2
turns of tempo; flaw costs ≈ the same.

### 2c. Mission draft = draw-3-keep-1 *(the hidden +7)*
Deal **3** missions, **secretly keep 1**, discard 2 unseen. The mission is now a **secret vendor
pattern** (+7): e.g., *"3 vendors in the South,"* *"a vendor of each cuisine,"* *"2 top-tier
marquee vendors,"* *"a vendor in all 4 regions."* Still the game's only hidden info; revealed at scoring.
Why a **pick** over a random deal: with **public characters** and **multiple tracks**, the pick lets you
**steer your character/track synergy on purpose** and **launders the char×mission balance problem** — a
broken combo can't be randomly gifted; you choose it, the opponent sees your character and contests.

### 2d. The Vendor Board = the ex-Hot-List public race
The v2 Hot-List **merges into the Vendor Board**: one tiered, face-up, refilling row is *both* your engine
shop *and* the public race both agents court from. Courting locks a vendor from the rival — but the
anti-resentment logic carries over intact: **the ingredients + Buzz you spent still bought you
Prestige + Rep + coverage + a discount**, so a snipe reads as **"outraced, not robbed."** Merging the
two removes a whole v2 subsystem.

---

## 3. Idea dump (so nothing is lost)

- **Second-currency candidates:** Buzz/Promotion (fungible hype — *recommend*); Reputation-as-spendable
  (spend your standing — but better as a *track*, §1c); Favour tokens / promised foot-traffic (you run
  errands / promise customers — warm but fiddlier to generate).
- **Vendor perk palette (engine pieces):** permanent **discount** (region/cuisine) · **Buzz income**
  (+Buzz when you Promote) · **sourcing perk** (source a region remotely / +1 there) · **Reputation
  engine** (extra Rep per court) · **coverage helper** (counts as 2 regions). Most vendors carry a
  discount (the core ramp); higher tiers carry the stronger perks.
- **Track options:** Prestige (VP) · Reputation (Arnak-style progression w/ milestone perks) · Region
  Coverage (breadth set-bonus) · a **Cuisine-variety** set (Hakka/Indigenous/night-market/breakfast — a
  possible 4th vector, held to avoid point-salad).
- **Event starter set (~12, secular, boon-skewed ~60/40, tax-not-destroy):** Oyster Glut (S, boon) ·
  Mango Season (S, festival boon) · Typhoon Warning (coast, +1 travel tax) · Landslide (C↔E pass shut) ·
  Bubble-Tea Festival (C, +1 sourcing) · Bumper Harvest (E, refill +2) · Plum Rains (C, small tax) ·
  Night-Market Anniversary (N/table, first-court +1) · Fully Booked (any, row shake-up) · The Generous
  Auntie (warm, free specialty to drawer) · The Scooter Kid (warm, free move to drawer) · Word of Mouth
  (warm, a Board vendor's Prestige +1). Warm characters = the "get lucky" beats; dignified hosts (§9).
- **Rejected / not now:** a 4th "cuisine-variety" track (point-salad creep); Splendor-style sudden-death
  win (feels-bad at the warm end — see Fork 2); keeping a separate Hot-List row *and* a Vendor Board
  (redundant — merge).

---

## 4. The forks the CD must decide (tight A/B/C)

### FORK 1 — the "something else" second currency
- **A. Buzz / Promotion** — fungible hype you generate (Promote) and spend beside ingredients; **=the
  agent's actual job** (promote & showcase), anti-extraction-perfect; clean, safe soft-axis. **← RECOMMEND.**
- **B. Reputation-as-spendable** — spend your standing to court. Con: conflates the *track* with the
  *currency*; better to keep Reputation a **track** (Fork 2) and use a separate soft currency.
- **C. Favour tokens / promised foot-traffic** — you run favours / promise customers. Warm and thematic,
  but a fiddlier generation loop than "take Buzz."
- **Recommendation: A (Buzz), with Reputation kept as a *track* not a currency.**

### FORK 2 — track structure / win vectors
- **A. Single VP total** — all vectors feed one score, highest wins. Gentle, gateway-friendly; least
  "several ways to win" tension.
- **B. Splendor-Duel multiple instant-win thresholds** — reach a cap on Prestige *or* Reputation *or*
  Coverage = win now. Punchy, maximal "paths to win," but **sudden-death feels-bad** at the warm/family
  end and is swingier.
- **C. Hybrid** — hitting the **top of a track triggers the end-game** and pays a **bonus**, but
  **highest total VP wins**. Multi-track tension **without** brutal sudden-death; keeps Extract/Season as
  co-triggers. **← RECOMMEND.**
- **How many vectors:** recommend **2 real (Prestige + Reputation) + Coverage end-bonus + hidden
  mission** — depth without point-salad. (A 4th "cuisine" track is the first thing to add *or* cut.)

### FORK 3 — event delivery + ingredient scarcity *(the sourcing layer)*
- **A. Face-up Market, events fire on refill; supply ≈2× solo demand** — targeted courting stays viable,
  risk every Stock Up, scarcity bites without lockout. **← RECOMMEND.**
- **B. Blind region bag (push-your-luck) + tighter supply** — max luck/drama, but **breaks targeted
  ingredient acquisition** (you can't reliably get the *named* specialty a vendor needs); only if the CD
  wants significantly more swing.
- **C. Hybrid — safe Market + opt-in "dig deeper" blind push** for a bonus at event risk (+1 rule); the
  natural upgrade if the feel-test wants more push.
- **Recommendation: A**, pantry **unlimited** + Buzz always-available as the two anti-stuck valves.

### FORK 4 — character-set direction
- **A. 5 archetypes as specced (§2b)** — the MVP. **← RECOMMEND.**
- **B. 4** (drop Influencer or Gourmand) — de-risk balance/weight.
- **C. 6+ incl. home-region variable** — most replay, hardest to balance; hold as expansion.
- **Recommendation: A (5), fall to B if the sim can't seat all five in the 45–55% band.**

---

## 5. Weight ledger (honest — for `bg-elegance`)

**Adds (+):** the **Buzz** second currency + **Promote** (or fold into Travel) — a real second economy
axis; **vendor engine perks / compounding discounts** — the engine ramp (the biggest single spend, and
the point of the redirect); **Reputation track** + **Coverage bonus** — the multi-vector depth;
**characters** (asymmetry teach cost, ~+0.1–0.15); events/scarcity + mission-draft (as before).

**Cuts / banks (−):** **Hot-List merged into the Vendor Board** (−1 subsystem); **Briefs cut** (−1 deck,
−1 keyword — Buzz now covers the flexible-resource job); **Conditions queue + Season-fire machinery cut**
(events → the market); the two-input engine **replaces** (not adds to) the plate-and-score beat.

**Net: ~2.2–2.4** — a genuine, *intended* step up from v2's ~2.0, squarely in the raised band (Splendor
Duel ~2.2 / 7WD ~2.2 / Arnak ~2.8). The engine is the deliberate spend; the merges/cuts keep it off the
2.5 ceiling. **Trim order if we drift >2.5:** (1) drop the Coverage vector to a flat mission-only breadth
reward; (2) fold Promote into Travel (4 actions); (3) characters 5→4; (4) collapse Reputation milestones
to a single end-game payout.

---

## 6. Keeping the depth + luck fun, not fiddly or frustrating

- **Two anti-stuck valves** (unlimited **pantry** on the hard axis, always-available **Buzz** on the soft
  axis) → luck/scarcity cost **tempo/a reroute, never a plate** — the same anti-feel-bad spine as the v2
  snipe.
- **Known deck composition + face-up Market** → event odds telegraphed at the deck level; you choose
  named ingredients you can see; take-2 risk is opted into knowingly.
- **Hazards tax/delay, never destroy; events skew boon** (upside every turn); warm "get lucky" beats.
- **The hidden mission** = a stable self-chosen keel the swing rocks around.
- **Multi-track = graceful losing** (Fork 2C, no sudden-death) → a trailing player always has a live
  second vector, not a single collapsing race.
- **Reserve knob:** if immediate-fire events feel random, add the **one-beat "brewing" telegraph** (event
  fires at the start of the drawer's next turn) — ~1 rule, restores v2's preview agency.

---

## 7. Riskiest assumption

**That the multi-track vendor engine has no dominant track or dominant opening** — the classic
tight-2p-engine failure (Splendor Duel / 7WD balance problem). If **prestige-rush strictly beats
reputation-climb beats breadth**, or if one currency (ingredients *or* Buzz) is always the binding
bottleneck, or if the compounding discount lets a first-mover **run away**, then the CD's whole "several
paths to Top Agent" depth **collapses into a solved line** — which is the core of this redirect. The
two-input economy tuning (courting costs vs Prestige/Rep rewards vs discount strength vs the end-clock
brake) is where this lives, and it is the make-or-break.

**Second-riskiest:** **character asymmetry balance + no dominant character×mission combo** (a tuning
problem, solvable by the sim). **Third:** **immediate-fire events feel fun-swingy not random** (a *feel*
question — needs the Screentop feel-test, not just the sim).

---

## 8. Sim plan (a real rework of `sim/travel_agents.py`)

The harness modelled plate-a-dish; it needs to model **court-a-vendor + two inputs + the discount engine
+ the tracks**. Then probe:

1. **Dominant track / opening (THE probe).** Bots each commit to a strategy over a shared courting brain:
   **Prestige-rush** vs **Reputation-climb** vs **Coverage-breadth**, and **ingredient-heavy** vs
   **Buzz-heavy** openings. **Pass:** no single track/opening **>~55–58%**; ≥3 strategies viable. **Fail:**
   rebalance vendor costs / track rewards / discount strength.
2. **Two-input economy + runaway.** Measure whether ingredients or Buzz is the persistent bottleneck, and
   whether the **compounding discount snowballs** (does the first big courter run away?). **Pass:** a real
   ramp exists but the **end-clock + rival race cap it** (leader's fast courting hurries the end / their
   ramp targets get sniped). **Fail:** add a catch-up (trailing discount) or **cap discounts**.
3. **Character balance.** Round-robin all **5×5** pairings at 2p (bots differ only by ability/flaw) +
   a **mirror control** (same char ≈ 50/50). **Pass:** every char **45–55%**, none **>58%/<42%**. **Fail:**
   re-tune the single offending ability/flaw (asymmetry is modular).
4. **Character×mission synergy.** Win-rate per character **conditioned on the drafted mission**. **Pass:**
   no combo **>~60%**. **Fail:** nerf the ability or exclude that mission from that char's pool. **Also:**
   compare draw-3-keep-1 vs draw-2-keep-1 — the draft should **reduce** char×mission variance (confirms
   §2c).
5. **Anti-hoard + frustration (the sourcing layer).** Hoarder (camp + stockpile) vs Router (spread +
   adapt): **pass** = Hoarder not dominant. **Hard-stuck rate ≈ 0** (pantry + Buzz valves work);
   forced-reroute non-zero but not constant; **correlation of net event-luck with winning = modest**
   (events spice, don't decide).

Bots are a **floor, not a ceiling** — they rule out a solved track/opening, an unfair character, and
broken economy math; they **cannot** judge whether the engine and immediate events *feel* fun/warm. Run
an early **2p Screentop feel-test** in parallel for risks #1 (is the engine satisfying / is a path
solved-feeling?) and #3 (do events feel swingy-fun or random?).

---

## 9. Sensitivity rails (binding — consultant via `bg-publishing`; coherence via `bg-theme`)

- **Vendors are Taiwanese cooks/stall-owners = real people as subjects.** They are courted by being
  **helped and promoted** (fresh ingredients + Buzz/customers) — **celebration, not extraction**, which
  is the identity's load-bearing frame. Depict them **warm, varied, dignified** (age/region/ethnicity
  range: Han, Hakka, Indigenous, newer communities), **never** exotic scenery, obstacles, or punchlines.
  "Securing exclusive rights" must read as *the vendor choosing to partner with the agent they like best*,
  **not** an agent extracting/monopolising a place — `bg-theme` to nail the fiction so it reads as a
  vendor **granting** their blessing. **New consultant item.**
- **Characters (player avatars):** warm, food-obsessed **agent** archetypes (auntie, rookie, conductor…),
  **not** ethnic caricatures; **passionate/ideally local promoters** (anti-extraction). Names/art
  especially → consultant.
- **Events secular only** (no temple/deity/ghost-month/funerary as mechanics or gags); warm characters
  dignified; hazards comic tax/delay, never disaster-porn. Cutting Briefs removes the "head office"
  directive layer entirely → **no** "head office controls the island" read; events are purely the island
  acting on you (safer than v2).
- **Dish/vendor names** Tâi-lô + 繁體, never mangled; Traditional characters only; Taiwan as itself.

---

## 10. Handoff

- **CD:** decide **Forks 1–4** (§4) — priority is Fork 1 (second currency) + Fork 2 (track structure),
  which define the engine; Fork 3 (events/scarcity) + Fork 4 (characters) are the layers.
- **`bg-elegance`:** guard the §5 ledger — confirm ~2.2–2.4 (not toward 2.5), and that merges/cuts
  (Hot-List→Board, Briefs cut, queue cut) actually banked their weight against the engine's spend.
- **`bg-playtest`:** the §8 sim rework (dominant-track + economy-runaway are the make-or-break probes) +
  an early 2p Screentop feel-test for the engine and event feel.
- **`bg-theme`:** own the fiction — courting/Buzz as *helping/promoting* (not extracting), the Vendor
  Board, vendors-granting-their-blessing, events, the five characters; confirm §9.
- **`bg-developer`:** vendor card data (cost = named ingredients + Buzz; bonus icon; Prestige/Rep/perk),
  the tiered Board, the Buzz supply, the Reputation track + Coverage bonus on the board, region
  supply/event encoding, 5 character mats, the draw-3-keep-1 mission pool (+7 vendor patterns).
- **`bg-architect`:** 3–4p scaling (sub-linear scarcity, Board size, turn order w/ the Influencer's "last"
  flaw), whether tracks/instant-win change at count, and the Automa against the engine.
