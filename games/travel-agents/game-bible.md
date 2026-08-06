# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design** (v2.1 vendor-courting engine locked; design-doc v3)

## One-liner
<!-- The hook a stranger would repeat. -->
You and your rival run competing **travel agencies** racing to build the best Taiwan food **tour** — ride
the rails, source real regional ingredients, drum up **Buzz**, and spend both to **win over the island's
vendors** (each one you sign makes the next easier to court). You just *behave* like covert agents about
it. Best tour = **Top Agent**.

## Core fantasy / player role
<!-- Who you are, what you're doing, the feeling (the "kind of fun"). -->
You run a travel agency (so does your rival), racing to assemble the single best Taiwan foodie **tour** —
and you take it *so* seriously you behave like a covert agent about it (trench coat over the Hawaiian
shirt, guarding your dossier, muttering into an earpiece). The literal job is wholesome: showing off the
island's best food. "Secret agent" is pure wordplay on **travel agent** — the title is literal, and
that's the gag. Kinds of fun (**locked**): **Discovery** (lead) + **Fellowship** (warm rivalry) +
**Challenge**.

## Creative identity (concept · theme · tone · look & feel)
- **North star:** *The mission is the meal — race your rival to build the island's best food tour before
  the last train home.* (full framing in `identity.md`)
- **Tone/vibe:** warm, funny, adventurous; the **secret-agent wink is first-class** (a rule-earning layer,
  kept comedic) over the wholesome travel-agent day job (Creative Director, 2026-08-06).
- **Details:** see `identity.md`.

## Positioning
- **Weight (BGG 1–5):** aim ~2.2, acceptable up to **~2.5** (raised 2026-08-06 for the engine-building pivot — lighter still better, tight-two-player engine not a heavy euro). Band: Splendor Duel ~2.3 · LOTR: Duel for Middle-earth ~2.4 · Arnak ~2.7.
- **Players:** 2–4 (this game leads with a first-class **2-player duel** by its own design choice, then scales to a 3–4p race)
- **Playtime:** ~40–50 min at 2p (TBD)
- **Tone:** silly / warm / adventurous
- **Comparable:** *Splendor Duel* / *Arnak*-style engine-building + *Ticket to Ride* routing, wrapped in a warm Taiwan food-tour with a secret-agent wink (the CD's touchstones: *LOTR: Duel*, *Splendor Duel*, *Arnak*).
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight:** aim ~2.2; **acceptable ceiling ~2.5** (CD raise #2, 2026-08-06 — for the engine-building pivot; still a tight 2p engine, lighter preferred, every rule earns its place)
- **Caps:** see `complexity-budget.json`. Check drift with
  `python tools/complexity/check_complexity.py --game games/travel-agents` and run **`bg-elegance`** each
  iteration. Over budget → simplify, or consciously log a raise. Never silent creep.

## Modes & scope (see knowledge/modes-and-expansions.md)
- **Player modes:** 2–4. Explore a dedicated **2-player duel** (head-to-head "who has the better trip")
  alongside a 3–4p multiplayer race. Owned by `bg-architect`.
- **Campaign?** None planned (fine!). Possible light "trip journal" replay hook later.
- **Expansion ambition:** base = the competitive vendor-courting engine (**v2.1**): the shared tiered
  **Vendor Board** race + two inputs (ingredients + **Buzz**) + the compounding discount + hybrid
  multi-track scoring (Prestige / Reputation / Coverage) + the secret **signature mission** + events in the
  **Market**. (v2's Plate-a-Dish + Hot-List + Briefs were **superseded/cut**.) Held hooks (not baggage):
  a **6th+ character** (e.g. the Homesick Local) and a small vendor-pack, a deeper **campaign / "tour
  journal"** arc, and a **destination series** ("Travel Agents: &lt;place&gt;") if the base sings. Owned by
  `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- 1–3 mechanism families and the blend; why each part needs the others (see knowledge/archetypes.md). -->
**Sourcing engine (spine A) + the v2.1 vendor-courting engine LOCKED** (CD, 2026-08-06; see
`design/explore-v2.1-engine.md`, `design/design-doc.md` v3). A **tight two-player engine-builder**
(Splendor Duel / LOTR Duel band) wrapped in a competitive food-tour race, built on:
- **Two-input engine-building.** You **court Vendors** off a tiered, shared **Vendor Board** by paying
  **two inputs** — region-specific **fresh ingredients** + fungible **Buzz**. Each secured vendor is a
  **permanent engine piece**: a **compounding discount** (a region icon that makes future vendors cheaper,
  à la Splendor) that also feeds several scoring vectors.
- **Set collection with a twist — recipes by region** (the ingredient input). A vendor's cost names
  region-specific ingredients sourced from the Taiwan **regions that actually supply them** (oysters
  coastal, tea in the hills, east-coast Indigenous produce, North's beef/pork/chicken/egg). The
  generic-defeater — real food geography, not "food + map."
- **Region routing / travel** — you move *because* the ingredient a vendor needs lives *there*.
- **The rival race + living Market (model C, evolved):** the **Vendor Board** is the public race (courting
  a vendor locks the rival out of it — the ex-Hot-List, merged in); **events ("Conditions")** are salted
  into the face-up ingredient **Market** and fire on refill (festival / typhoon / warm local); the
  **Season** is now a **pure end-timer**.

## Core loop
<!-- The repeated cycle of decisions and rewards, step by step. -->
Specified in `design/design-doc.md` (v3). **A turn = ONE action:** **Stock Up** (take 2 ingredients where
you stand) · **Travel** (move one region, arrive with 1) · **Promote** (take 2 Buzz) · **Court a Vendor**
(pay ingredients − discounts + Buzz → secure a Board vendor: Prestige scored **live**, a Reputation bump, a
permanent perk/discount, a Coverage tick; refill the Board, Season +1, lock it from the rival) ·
**Extract** (trigger the end-game). You can only take a region's **specialty** while there (oysters South,
tea/pearls Central, rice/greens East, beef/pork/chicken/egg North); **pantry** staples are anywhere
(unlimited) — so you *travel because the ingredient lives there*. Your **Larder sits face-up** (the secret
**signature mission** is the game's *only* hidden info). **Larder caps at 7.** The tension every turn:
source the contested specialty a vendor needs, bank safe Buzz, or spend both to court now (before the rival
locks that vendor and its discount icon away) — and which of my vectors does it push?

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
**You court the island's vendors — paying fresh ingredients + Buzz — and each secured vendor is an engine
piece (a compounding discount) that also climbs Prestige, Reputation and Region-Coverage toward your
hidden signature tour; the shared Vendor Board is the rival race.** The travel-agent fiction (promote a
vendor, win their blessing) and the food-geography fiction (source where the food lives) drive the *same*
decisions, and the discount ramp is braked by an **undiscountable Buzz cost** so the engine never runs
away past the end-clock. *(v3 — replaces v2's "Plate a Dish + Hot-List" beat: plating is a chef's verb,
off the travel-agent identity; courting a vendor for their blessing is on-theme and carries the engine.)*

## Components (summary)
*(Firmed by `bg-developer` 2026-08-06 from the v3 data in `components/`; full BOM in
`components/manifest.md`.)* **7 component types**, within the raised cap of **8**: (1) **Map board** —
Taiwan, 4 regions on a ring + HSR spine, carrying the **Season end-timer**, the **Prestige (VP) track**,
the **Reputation track**, the tiered **Vendor Board** (3 rows) and each region's **Market slots**; (2)
**25 Vendor cards** — tiered **T1 Stalls ×11 / T2 Eateries ×8 / T3 Marquee ×6**, one per **real locked
dish** (Tâi-lô + 繁體), each with cost (named ingredients + Buzz), a **region icon** (discount + coverage),
**Prestige**, **Reputation**, a **perk**; region-icon balance **N7 · C6 · S6 · E6**; (3) **9 Mission
cards** (secret +7 vendor patterns, draw-3-keep-1; same card stock); (4) **144 ingredient tokens** — 10
finite specialties (incl. **chicken 雞 + egg 蛋**, new in the North) + **unlimited pantry**; (5) **50 Buzz
tokens** (*new type* — the second currency); (6) **11 Event tiles** (Conditions salted into the Market,
fire on refill; *new type*); (7) **5 Character mats** (*new type* — one ability + one flaw each) + 4 Agent
pawns + Prestige/Rep/Season markers (board bits). **Cut from v2:** the **Brief** deck; the separate
**Hot-List** row (merged into the Vendor Board) and the **Conditions queue** (events now in the Market).
Deck-size note: the vendor deck is **25** (one per locked real dish) — comfortable for a 2p game (~16–18
courts) but tight for headroom / 3–4p; see the CD decision in the handoff.

## Win condition & scoring
Hybrid multi-track: tracks **trigger the endgame + a bonus**, but **highest total VP wins** (no
sudden-death). Score = **Tour Prestige** (vendors' stars: T1=1 / T2=3 / T3=5–6) + **Reputation** end-VP by
track position (3→+2 · 6→+4 · 9→+6 · top→+9, with one-time perks passing 3/6/9) + **Region-Coverage**
breadth (2 regions→2 · 3→5 · all 4→9) + **secret signature mission** (+7 if completed, revealed at
scoring). A **live tracker** (Prestige + Rep markers) shows two vectors as earned; the **only** off-tracker
VP is the hidden +7. ≥2 paths kept competitive by design (tall vs rep-climb vs breadth pull against each
other; Rep is decoupled from raw Prestige). **Tiebreak:** highest Reputation, then most vendors, then most
regions. Expected 2p winner ~35–42 VP. Detail + balance model in `design/design-doc.md` v3.

## Rules summary
Drafted in `design/rules-draft.md` v3 (teach-in-play order). Turn = one of **Stock Up / Travel / Promote /
Court a Vendor / Extract**; Larder cap 7; courting pays ingredients (− region discounts, floored) + Buzz
(**never discounted — the ramp brake**); each vendor gives Prestige + Rep + a permanent discount icon +
coverage, and locks the rival out of it. Events fire on Market refill (Season is a **pure end-timer**,
+1 per court). End-game triggers on **Extract** or the **Season filling** (Rep-top scores +9 but no longer
ends the game — sim-fix so the engine has room to ramp) → finish the round + one more full round → reveal
missions → score. **One hidden-info hook only:**
the secret signature mission (no deduction engine).

## Open questions & risks
- ✅ **Mechanism spine — DECIDED:** sourcing engine (spine A) + the **v2.1 vendor-courting engine**
  (2026-08-06). Court a Vendor replaces Plate a Dish; two inputs (ingredients + **Buzz**); compounding
  discount; hybrid multi-track scoring; events folded into the Market; **Briefs cut**.
- ✅ **Is the "agent" wink load-bearing? — DECIDED:** yes — you *court vendors* (win their blessing by
  promoting them), the on-theme travel-agent beat that also carries the engine.
- ⚠️ **TOP RISK #1 (v3) — no dominant track or opening.** Must keep **tall (Prestige) ≈ rep-climb ≈
  breadth** competitive, and **ingredient-heavy ≈ Buzz-heavy** as openings. Designed out: the three tracks
  reward different behaviours and pull against each other (concentrate for ramp vs spread for coverage);
  Rep is decoupled from raw Prestige; the mission is a *pick*. *Attack:* sim dominant-track/opening probe
  (pass = no line >~55%, ≥3 viable) + 2p Screentop feel-test.
- ⚠️ **TOP RISK #2 (v3) — no economy runaway.** The compounding discount must not snowball past the
  end-clock. **The brake: the discount touches only the *ingredient* half; Buzz is never discounted**, so
  even a full ramp still pays Buzz one action at a time → court-rate capped at ~1 vendor/2 turns (vs
  ~1/3–4 early: a real ~2× ramp, not an explosion). Co-brakes: diminishing returns on cheap vendors,
  shared-Board scarcity (rival snipes your ramp icons), the end-timer (fast courting hurries the end).
  *Attack:* sim runaway probe (court-rate ceiling, leader VP-gap over time). Reserve knobs: trailing
  discount / vendor cap / discount cap.
- ⚠️ **Secondary risks:** per-character win-rate **45–55%** with no dominant char×mission combo (round-robin
  5×5 + mirror); do Market events feel *swingy-fun* not random (boon-skew + tax-not-destroy + the "brewing"
  reserve knob)?; does Fellowship survive (shared Market drama + Board rivalry)?
- Hold weight **~2.2–2.4, ceiling 2.5** (`bg-elegance` guards). Trim order: Rep milestone perks → pure
  end-VP; Coverage → mission-only; characters 5→4; fold Promote into Travel; cap the discount.
- 2p-first, but confirm it scales cleanly to 3–4 (`bg-architect`); Automa sketch now near-expected on a
  mid-weight engine.
- **Sensitivity:** the game depicts a **real place & culture (Taiwan)** — flag for `bg-theme` +
  `bg-publishing` (respectful, well-researched, avoid caricature; "Taiwanese humour" done *with* not *at*;
  paid Taiwanese cultural + language consultant before art/print).

## Status by stage
- [x] Ideation
- [x] Research
- [x] Exploration
- [ ] Design ← **in progress** (`bg-design` specifying spine A)
- [ ] Development
- [ ] Prototype (Screentop.gg / PnP)
- [ ] Playtesting
- [ ] Marketing
- [ ] Publishing / IP

## Links
<!-- design/, components/, playtests/, marketing/ artifacts as they appear. -->
- Identity: `identity.md`
- Decisions: `decision-log.md`
