# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design** (interaction model C locked; design-doc v2)

## One-liner
<!-- The hook a stranger would repeat. -->
You and your rival run competing **travel agencies** racing to build the best Taiwan food **tour** — ride
the rails, source real regional ingredients, plate the island's great dishes, and lock the must-visit
stalls before your rival does. You just *behave* like covert agents about it. Best tour = **Top Agent**.

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
- **Weight (BGG 1–5):** aim ~1.8, acceptable up to **~2.2** if gameplay needs it (lighter is better, but don't let the budget hamper the fun — CD 2026-08-06). Band: TtR Europe ~1.9, Let's Go! To Japan ~2.25.
- **Players:** 2–4 (this game leads with a first-class **2-player duel** by its own design choice, then scales to a 3–4p race)
- **Playtime:** ~30–45 min (TBD)
- **Tone:** silly / warm / adventurous
- **Comparable:** *Let's Go! To Japan* meets *Ticket to Ride*, with a dash of *Couture* and *Agent Avenue*.
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight:** aim ~1.8; **acceptable ceiling ~2.2** (CD raise 2026-08-06 — gameplay wins over strictness; lighter still preferred)
- **Caps:** see `complexity-budget.json`. Check drift with
  `python tools/complexity/check_complexity.py --game games/travel-agents` and run **`bg-elegance`** each
  iteration. Over budget → simplify, or consciously log a raise. Never silent creep.

## Modes & scope (see knowledge/modes-and-expansions.md)
- **Player modes:** 2–4. Explore a dedicated **2-player duel** (head-to-head "who has the better trip")
  alongside a 3–4p multiplayer race. Owned by `bg-architect`.
- **Campaign?** None planned (fine!). Possible light "trip journal" replay hook later.
- **Expansion ambition:** base = the competitive food-tour race (**model C**): the public **Hot-List** +
  your secret **signature itinerary** + the living-island **Conditions** + head-office **Briefs**. (v1's
  co-op shared-Dossier + dead-drop was **cut** — not fun/on-theme.) Held hooks (not baggage): the fuller
  **"Command Centre Duel" (model B)** take-that economy as a cheap upgrade (shares this core), a deeper
  **campaign / "tour journal"** arc, and a **destination series** ("Travel Agents: &lt;place&gt;" — the
  agency's field offices worldwide) if the base sings. Owned by `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- 1–3 mechanism families and the blend; why each part needs the others (see knowledge/archetypes.md). -->
**Sourcing engine LOCKED (spine A) + interaction model C "Rivals on a Living Island" LOCKED** (CD,
2026-08-06; see `design/explore-interaction-v2.md`, `design/design-doc.md` v2). A **competitive
food-tour race**, built on:
- **Set collection with a twist — recipes by region.** A dish = a tiny recipe of 2–3 named ingredients;
  ingredients are sourced from the Taiwan **regions that actually supply them** (oysters coastal, Hakka
  mountain towns, east-coast Indigenous cuisines…). This is the generic-defeater — the map is shaped by
  real food geography, not "food + map." (from the Yes! Ginseng / Taiwan Snackbar inspirations)
- **Region routing / travel** — you move *because* the ingredient you need lives *there*.
- **The rival-contest + living-island layer (model C):** a **public Hot-List** both agents race to lock
  in (public bonus tours) + a **secret signature itinerary** (your hidden +7 headline) + a telegraphed
  **Conditions** deck (the island's festivals/weather/roads, fired by the shared **Season** clock) +
  a *minimal* set of head-office **Briefs** (safe boost / risky gamble / light nudge). This is what
  makes "rival travel agents racing to build the best tour" a thing you *do*.

## Core loop
<!-- The repeated cycle of decisions and rewards, step by step. -->
Specified in `design/design-doc.md` (v2). **A turn = ONE action:** **Stock Up** (take 2 ingredients
where you stand) · **Travel** (move one region, arrive with 1) · **Plate** (spend a recipe from your
Larder to add a Menu Dish to your tour → VP scored **live**, Season +1, then **lock in** any completed
Hot-List spot for free) · **Extract** (trigger the end-game). Free riders: **play one Brief** and **lock
in** completed Hot-List spots. You can only take a region's **specialty** while there (oysters South,
tea/pearls Central, rice/greens East, beef/pork/chicken/egg North); **pantry** staples are at the
convenience store anywhere — so you *travel because the ingredient lives there*. Your **Larder sits
face-up** (the secret **signature itinerary** is the game's *only* hidden info). **Larder caps at 7.**
The tension every turn: source toward my next Dish, **race the rival to a Hot-List spot**, or bank my
lead and wrap — all under a **living island** whose next **Condition** you can already see coming.

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
**The public Hot-List race on the same Operation cards as your secret signature itinerary, under a
telegraphed living island.** Two rival agents race to lock the island's hot spots into competing tours
while the shared **Season** clock keeps turning the island (festivals open windows, typhoons shut
roads). Fused with **recipes-by-region**, so the travel-agent fiction and the food-geography fiction
drive the *same* decisions. *(v2 — replaces the v1 co-op shared-Dossier + dead-drop twist, which was
cut: the paid one-way gift wasn't fun or on-theme even though the sim proved it rational.)*

## Components (summary)
*(Full table in `design/design-doc.md` v2; quantities being re-firmed by `bg-developer`.)* **7 component
types** (+1 over v1's 6-cap — the CD softened the cap, cost is fun-first): (1) **Map board** — Taiwan, 4
regions on a ring + HSR spine, now also carrying the **Season clock**, the **VP score track**, the
**Hot-List row (3 slots)** and the **Condition queue (2 slots)**; (2) **~24→30 Dish cards** (recipe + VP
+ Tâi-lô & 繁體; grows with North chicken/egg + East); (3) **Operation cards** — *one type, two decks:*
a **Hot-List deck** (~14–18 public bonus tours, 4–6 VP) + a **Sealed deck** (~10–12 secret signature
itineraries, +7) — reuses v1's Assignment type, so the whole Hot-List race costs **no new component**;
(4) **Condition cards** (~10–14 — the living-island event deck; *new type*); (5) **Brief cards** (~10–14
head-office directives; *new type — scope = CD decision; may collapse to a printed set → back to 6
types*); (6) **~130–150 ingredient tokens** (region specialties + pantry; adding **chicken 雞 + egg
蛋**); (7) **4 Agent pawns** (+ VP markers on the track). **Cut from v1:** Insider Tip tokens.
Conditions & Briefs stay **separate decks on purpose** (sensitivity rail — head-office vs island must
not blur).

## Win condition & scoring
Highest tour (Traveller's Log) wins → **Top Agent**. Score = **plated Dishes** (3 / 4 / 5 VP) +
**Hot-List spots locked** (4–6 VP each — the public race) + **Condition/Brief VP gains** + **secret
signature itinerary** (+7 if completed, revealed at scoring). A **live VP tracker** (score track +
marker per player) shows all *open* VP as earned — Dishes, locks, event/brief gains — so the race is
legible; the **only** off-tracker VP is the secret +7, held face-down until the reveal. **Tiebreak:**
most Hot-List spots, then most Dishes, then most regions visited. Expected 2p winner ~50–55 VP. Detail
+ balance model in `design/design-doc.md` v2. *(v2 — the v1 flat Grand Dossier payout + triggerer's
pick + +1-VP-per-Dead-drop are all cut; the Grand Dossier is repurposed into the Season clock that fires
Conditions.)*

## Rules summary
Drafted in `design/rules-draft.md` v2 (teach-in-play order). Turn = one of **Stock Up / Travel / Plate /
Extract** (+ free: play a **Brief**, **lock in** a completed Hot-List spot); Larder cap 7; the **Season**
advances +1 per Plate and per lock-in, firing a **Condition** at each milestone (telegraphed queue:
ACTIVE + NEXT); end-game triggers on **Extract** or the Season's final milestone → finish the round + one
more full round → score. **One hidden-info hook only:** the secret signature itinerary (no deduction
engine).

## Open questions & risks
- ✅ **Mechanism spine — DECIDED:** sourcing engine (spine A) + **interaction model C "Rivals on a Living
  Island"** (2026-08-06). Dead-drop + Insider Tip **cut**; Grand Dossier repurposed as the Season clock.
- ✅ **Is the "agent" wink load-bearing? — DECIDED:** yes — now via the public **Hot-List** race + secret
  **signature itinerary** + head-office **Briefs** (re-skinned to rival travel agents building a tour).
- ⚠️ **TOP RISK (v2) — the Hot-List race must be *fun-tense*, not resentment-on-snipe or a leader-runaway.**
  Attack first with the named sim **bounty-claim-share vs finishing position** (extend
  `sim/travel_agents.py`: Chaser vs Signature-focus; pass = locks spread, winner doesn't sweep) **and** a
  2p Screentop feel-test (does a snipe feel outraced-not-robbed?). Rules designed to defuse it: refilling
  3-spot pool · a snipe never wastes your plated Dishes · fully open info + live VP tracker · modest 4–6
  VP · the Season clock ties a leader's tempo to a faster endgame. Fallback knobs: per-player lock cap /
  trailing discount / faster refresh. (design-doc v2 *Interaction & tension*.)
- ⚠️ **Secondary risks:** does Fellowship survive cutting co-op (carried now by shared Condition drama +
  rivalry banter)? do the Briefs read affectionate not mean? do Conditions vary routing without erasing a
  planned plate (telegraph + tax-not-block)?
- Hold weight **~2.0–2.1, ceiling 2.2** — one clean hidden-info hook, no deduction engine; the 7th
  component type (Brief deck) is the trim point (`bg-elegance` guards).
- 2p-first, but confirm it scales cleanly to 3–4 (`bg-architect`).
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
