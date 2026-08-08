# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design — v6.3.1 BALANCE-VALIDATED (re-sim);
> ready for the bg-developer DATA REBUILD + the human FTUE (2026-08-08, CD DESIGN LOCK). The four v6.3.1 CD
> reworks are re-sim-validated (`sim-notes.md §v6.3.1`) and the CD's three final balance calls are LOCKED —
> CD-4 soft night-cost curve, CD-1 里長伯 −1/+1 as-is, CD-2 Scheduled Maintenance ×2. `design/v6.3-content-draft.md`
> is canon.** **★ Headline: TICKETS-ONLY
> scoring** — Tour Tickets are the **sole** scoring vector; **vendors give NO points** (a vendor is purely
> the ENGINE — its region-discount ramp + the stop you assemble to complete tickets); this structurally
> killed the `ignore_obj` grind-the-fattest-vendor exploit (80.7% → 43.8%). The **ticket deck is EXPANDED to
> ~44 tickets** (region pairs, cross-region →X dishes, single-region depth, deeper collections, food-count
> ladders). **Milestones ("Rave Reviews") = `perplayer`** (each player earns their own boon — no leader
> pump) and **re-homed onto a Tours-Completed counter** (your 2nd & 4th completed tour). A vendor keeps a
> printed **value** ATTRIBUTE (referenced by value-tickets + keeps the ★ apex the marquee get) — but it is
> **not a score track**; the former "Bookings" score track is retired (rename flagged for bg-theme). v6.3
> also gives **Reputation→Reach teeth** (a live cap on committed Buzz; earned by Travel + events, not
> vendors; no longer scores; + Rep sinks), **kills the perk field**, and collapses **ticket pools 3→2**. New
> tiebreak: **most vendors → most regions → fewest LOSE-pile tickets.** **★ v6.3.1 — FOUR CD CHANGES folded
> (2026-08-07 PM, economy-changing → validated by the SAME gated re-sim):** **(CD-1)** 里長伯 reworked to a
> **home-region** kit (−1 discount in one home region; **+1-ingredient away-tax** elsewhere; no-HSR flaw
> REMOVED) — supersedes the first-region-only tune (A/B CLOSED); **(CD-2)** new **table-wide** event
> **排班保養 "Scheduled Maintenance"** (HSR down for everyone one round — re-homes the no-HSR concept; its
> own island-wide banner, NOT a ⦿/⬢/➤ scope); **(CD-3)** all agents **start in Taipei** (North hub —
> replaces the split N/S 2p start); **(CD-4)** the **night-cost curve** (night vendors cost meaningfully
> more so a ramped discount engine affords the night marquee but can't zero-out sourcing; the LOTR:Duel
> model). **★ v6.3.1 BALANCE-VALIDATED + LOCKED (2026-08-08):** the re-sim (`sim-notes.md §v6.3.1`)
> validated all four; night sourcing stays alive (113% of day), free marquee bribes cut 1.73→0.95, seat
> balance ok at every count, `ignore_obj` stays dead. **The CD's three final calls: CD-4 = SOFT curve,
> curve-only** (night "both" foods → 3, apex ★ → 4 / top apex 5, every night marquee cross-region biased;
> DAY held as printed; steep +2 and the min-1 floor both rejected); **CD-1 = 里長伯 −1 home / +1 away AS-IS**
> (lands 55% top-of-band, CD-accepted; start-Reach 2 like everyone — NO start-Reach change); **CD-2 =
> Scheduled Maintenance ×2 copies** (a felt ~12% beat). **⚠ CANON vs sim default:** the committed sim module
> defaults to `TA_COUNCILLOR_REACH=1` and `TA_MAINT_COUNT=1` — CANON is start-Reach 2 and 2 Maintenance
> copies; bg-developer/bg-playtest build to canon. **Next: the bg-developer DATA REBUILD (now unblocked),
> then the 2p FTUE.** Full: `design/v6.3-content-draft.md` §"v6.3 → v6.3.1 — FOUR CD CHANGES".
>
> _(v6.2 baseline, still the balance reference:)_ v6.2
> restructures the board into **region vendor markets**, paces the day on the **vendor-claims clock**, and
> makes **Tour Tickets** the objective spine (a face-up ticket row scored into a **win-pile / lose-pile**).
> It **supersedes v6.1's central Ladder, the ladder-vs-drinks FORK, off-clock/region-free beverages, and the
> single secret +7 mission**: there is now **one kind of vendor** (food and drinks alike; drinks are just the
> low-value ones), each of the 4 regions has **its own face-down vendor pile** (daytime stacked on
> nighttime), **1–2 face-up per region** (North 2, the rest 1), and the day runs **Day → Night → the last
> train home**, advancing **as vendors are claimed** (dusk = 5th table-wide claim, last train = 10th @2p).
> What stands from before: the **Buzz-majority public hype-fight**, the **5-ingredient palette** (4
> signatures + 1 common), the **five Taiwanese-social-type characters**, and the sensitivity rails. Full
> current spec: `design/v6.2-content-draft.md`. (v6.1 detail retained in `design/design-doc.md` as history.)

## One-liner
<!-- The hook a stranger would repeat. -->
You and your rival run competing **travel agencies** racing to build the best Taiwan food **tour** — ride
the rails, source real regional ingredients, drum up **Buzz** to **win over the island's vendors**, and
tick off your **itinerary** before the last train home. You just *behave* like covert agents about it.
Best tour = **Top Agent**.

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
  the last train home.* (full framing in `identity.md` — bg-theme is updating it to v6.2)
- **Tone/vibe:** warm, funny, adventurous; the **secret-agent wink is first-class** (a rule-earning layer,
  kept comedic) over the wholesome travel-agent day job.
- **Details:** see `identity.md`.

## Positioning
- **Weight (BGG 1–5):** aim ~2.2, acceptable up to **~2.5**. Band: Splendor Duel ~2.3 · LOTR: Duel ~2.4 ·
  Arnak ~2.7. **v6.2 watch:** the mission/ticket subsystem + region markets may push *table-state*
  complexity even if rules count holds — bg-elegance is re-reading the v6.2 budget.
- **Players:** 2–4 (leads with a first-class **2-player duel**, then scales to a 3–4p race)
- **Playtime:** **~25–30 min at 2p** (the day-clock paces to ~5–6 vendors/player; sim to confirm v6.2)
- **Tone:** silly / warm / adventurous
- **Comparable:** *Splendor Duel* / *Arnak*-style engine-building + *Ticket to Ride* objective-tickets,
  wrapped in a warm Taiwan food-tour with a secret-agent wink.
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight:** aim ~2.2; **acceptable ceiling ~2.5**. v6.2 net: it **removes** real special-casing
  (the central Ladder, the ladder/drinks fork, off-clock beverages, the single secret mission, the
  "ladder-only clock" clause → one unified vendor rule) and **adds** region vendor markets + a mission
  clock + a face-up ticket row. bg-elegance is weighing whether that's a wash, lighter, or a creep.
- **Caps:** `complexity-budget.json`. Check with `python tools/complexity/check_complexity.py --game
  games/travel-agents` and run **`bg-elegance`** each iteration. Never silent creep.

## Modes & scope
- **Player modes:** 2–4. A dedicated **2-player duel** (head-to-head) + a 3–4p race. Owned by `bg-architect`.
- **Campaign?** None planned. Possible light "trip journal" replay hook later (the 12→5 mission draw already
  gives strong game-to-game variety).
- **Expansion ambition:** base = the competitive vendor-market engine — the region **vendor markets** +
  Buzz-majority fight + two inputs (region ingredients + committed **Buzz**) + the compounding discount +
  the **Day → Night** clock + **Tour Tickets** (the objective/mission spine) + push-your-luck ingredient
  **market decks**. Held hooks: a **6th+ character** (the Homesick Local), a small vendor/ticket pack, a
  **destination series** ("Travel Agents: &lt;place&gt;"). Owned by `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- mechanism families + the blend; why each part needs the others. -->
A **tight two-player engine-builder** with a genuine *fight* at its centre (Splendor Duel / LOTR Duel band,
reaching toward an Arcs-Court interaction), built on:
- **Region vendor markets (v6.2).** Each of the 4 regions (**North 北 · Central 中 · South 南 · East 東**)
  has **its own face-down vendor deck** — a **DAY deck** in Act I, a separate **NIGHT deck** in Act II —
  with **drinks mixed in as the low-value vendors**. Each region keeps **1–2 face-up** (North 2, others 1),
  refilled in place. No central Ladder, no ladder/drinks fork — **one kind of vendor, one courting rule**.
- **Two-input engine-building with a contested currency.** You win **Vendors** by paying **region-specific
  ingredients** + **Buzz**, where Buzz is committed **publicly ON each vendor** (Arcs-Court-like): be
  **on-site** to place it, both agents can pile on the same vendor, and you **win only by out-hyping your
  rival by ≥2 while holding the ingredients**. Each **food** vendor won is an engine piece (a compounding
  **region-icon ingredient discount**); **drinks carry no icon** (low value, no ramp).
- **Set collection by region — the 5-ingredient palette.** One **signature per region** (**N 豬肉 pork · C
  茶 tea · S 海鮮 seafood · E 米 rice**) + one **common (K 糖 sugar)** that lives in **C & S** only. Real
  food geography. ~40% of nighttime vendors are **cross-region** (a vendor here needs an ingredient from
  there) — a load-bearing travel lever.
- **Push-your-luck ingredient sourcing.** Each region also has a face-down **market deck** (its signature,
  the common in C/S, and salted **scoped events**). **Visit** = flip 3, keep 2, events fire **by scope**
  (⦿ self / ⬢ region / ➤ neighbour). **Convenience Store** = top card of ANY region, blind — **also fires
  by scope** (the take-that lever). **Travel** = move + draw the arriving region (an event whiffs).
- **The Day → Night clock + Tour Tickets (the spine, v6.2 — LOCKED).** The day runs **Act I (daytime
  vendors) → dusk → Act II (nighttime vendors) → the last train home**, paced by the **VENDOR-CLAIMS clock**:
  the day advances **as vendors are claimed** — **dusk = the 5th table-wide vendor claim, the last train =
  the 10th @2p** (the marks grow with player count; deck-exhaustion backstops end a phase if decks dry
  island-wide). **The dusk flip is a big, thematic turnover:** the *entire* day layer is cleared island-wide
  — **both the day vendor decks AND the day ingredient market decks** are removed (not just the face-up
  cards) and replaced by **night decks** (recoloured; the night ingredient decks are **event-heavier** — the
  bustling night-market feel), while **players keep their Larder**. **Tour Tickets are the objective spine:**
  a **face-up row of 3**, claimed as an action, drawn from **daytime / nighttime / general** pools (12 per
  phase in the box, **5 drawn per phase per game**). Each claimed ticket is **judged at the end of its phase**
  (daytime tickets at dusk, nighttime at the last train) and sorted into a **WIN pile** (completed) or a
  **LOSE pile** (unfinished); points are tallied **once, at game end**: Σ(win-pile values) − Σ(floor(value/2)
  per lose-pile ticket).

## Core loop
<!-- The repeated cycle of decisions and rewards. -->
Full spec in `design/v6.2-content-draft.md`. **A turn = ONE action:**
- **Visit the Local Market** (flip 3 of your region's ingredient deck, keep 2; events fire by scope) ·
- **Convenience Store** (top card of ANY region's ingredient deck, blind — grab the common, or fire a
  scoped event, incl. onto a rival's region) ·
- **Travel** (move one region — HSR links N↔S — draw the arriving region; an event whiffs) ·
- **Promote** (place 2 Buzz onto vendor(s) you're with in this region) ·
- **Bribe a Vendor** (be on-site, hold ≥2 more Buzz than your rival, pay its ingredients − discounts → win
  it: it joins your tour as an **engine piece** — its region-icon feeds the discount ramp — and may
  **complete a held ticket**; **no points, no Rep grant, no perk** — vendors don't score; its Buzz clears to
  supply, freeing your Reach cap; refill the slot; move the clock +1; lock it) ·
- **Claim a Tour Ticket** (take one from the face-up row of 3; it refills — a public commitment judged at
  the end of its phase into your win-pile / lose-pile, tallied once at game end).

You court whatever's **face-up in the region you stand in** (1–2 vendors + the day's layer). **Larder caps
at 7.** The tension every turn: chase the region's face-up prize, dig for the ingredient you're short,
grab a cheap drink when it's the efficient local play, commit to a ticket (and race to finish it before its
phase closes and it drops to your lose-pile), or reach into a rival's region with a scoped Convenience-Store
event. Day flips to night as **vendors are claimed**; when the night winds down, catch the **last train
home**.

## Signature twist
<!-- The one memorable hook that makes it *this* game. -->
**Buzz is a public, committed, contested majority you pile ON the island's vendors — you win a vendor by
out-hyping your rival ON-SITE (by ≥2) while holding the ingredients its dish needs, and each food vendor
won is an engine piece (a compounding ingredient discount) — the engine you assemble to COMPLETE your
tours.** The travel-agent fiction (promote a vendor, out-woo your rival, win their blessing) and the
food-geography fiction (source where the food lives) drive the *same* decisions. The runaway brake is the
**Buzz fight itself** — undiscounted, region-gated, raise-able by your rival. **The ITINERARY is where the
points live:** your **Tour Tickets** (booked openly from a face-up row) are the **sole scoring vector** —
raced against the phase clock into a **win-pile / lose-pile** — while vendors are pure engine (**v6.3
TICKETS-ONLY: vendors give no points**) and the **vendor-claims clock** (each vendor won ticks the day
toward night) paces the day. *(The "**Bribe a Vendor**" keyword is LOCKED — the warm, comedic "marketing
opportunity," never corruption.)*
> **v6.3 deepens the twist — Reputation now gates the Buzz.** *Your hype can't outrun your reputation:* your
> total committed Buzz may never exceed your **Reputation**, which you build by **Travelling** (spreading
> your name) and through events, and **burn** by greed (a Greedy Grab of an extra ingredient costs −1 Rep).
> So the fight gains a resource spine — the agent who travelled more can out-escalate a collision — Travel
> becomes the engine's fuel line, and Reputation **stops scoring** (gating replaces its old end-VP job).

## The five intended playstyles (the design's depth target)
The game should support several viable ways to win — the bar (and the sim's test lineup) is **all five
live, none >~55%, with some rock-paper-scissors between them**:
- **Character-lean** — play hard into your character's ability.
- **Opportunistic** — chase the currently-lucrative: ★/premium face-up vendors, high-value tickets, event windfalls.
- **Disruptive** — reach into a rival's region with scoped Convenience-Store events; deny and tax.
- **Balanced** — a mix of the above.
- **End-game driver** — complete objectives fast to slam the last train shut while ahead.

## Components (summary)
*(v6.2 target for `bg-developer`, **after CD lock**; BOM regenerates in `components/manifest.md`. Current
CSVs are still pre-v6 — the data rebuild is gated.)*
- **Map board** — Taiwan, 4 regions on a ring + HSR spine (N↔S). North's hub = **Taipei**, the **common
  start** for every agent (v6.3.1 CD-3 — replaces the split N/S 2p start; a start-marker zone + a
  `"hub":"Taipei"` note is a bg-developer map.json edit). The HSR spine carries an **HSR-closed reminder
  slot** for the Scheduled Maintenance event. It also carries the **Day→Night clock** (dusk +
  last-train marks), the **Tours-Completed counter** (repurposed from the old VP track — with the two Rave
  Review milestone marks at completed-tour 2 & 4), the **Reputation (Reach) track**, and — **per region** —
  a face-down **vendor-deck** space with **1–2 face-up slots** (North 2, others 1) **and** a face-down
  **ingredient-deck** space (each holds the **day** deck in Act I, swapped for the **night** deck at dusk).
  *(No score track — the score is the Tour-Ticket tally.)*
- **~48 Vendor cards** — a **day set + a night set per region** (drinks are the low-value vendors mixed into
  each; recoloured day vs night), one per real locked dish (繁體 + Tâi-lô), each with cost (5-palette), a
  **region icon** *(food only — the ramp; drinks carry none)*, and a printed **value** attribute *(NOT a
  score — referenced by value-tickets + marks the marquee prizes; perk field + Prestige + Rep numbers all
  GONE)*. **One apex (★) vendor per region in the night set** (top value — the rotating trophy); the dynamic
  **★ Star token** can make a vendor hot mid-game (+2 value, recyclable). **v6.3.1 CD-4 — NIGHT vendors cost
  meaningfully MORE than day vendors — LOCKED SOFT curve** (re-sim validated): DAY (discount-only foods +
  drinks) held as printed; **NIGHT "both" foods → cost 3, apex ★ → 4, top apex (石板烤肉) → 5**, and **every
  night marquee is cross-region biased** (needs a two-region engine to zero — the load-bearing guard). Steep
  +2 curve and the min-1 floor both rejected. Canon night-cost table + the placed Central tea-export fix (胡椒餅
  {N:2,C:1}, 麻糬 {E:2,C:1}) in `design/v6.3-content-draft.md` §CD-4; bg-developer bakes it into `vendors.csv`.
- **~44 Tour-Ticket cards (the EXPANDED deck — the sole scoring vector)** — **DAY deck ~20 + NIGHT deck ~25**
  (patterns: region pairs, cross-region →X dishes, single-region depth, deeper collections, food-count
  ladders, plus the base coverage/thrift/contest/value patterns — full list in `design/v6.3-content-draft.md`
  §4b–4c). **Draw 5 per phase** into a **face-up shared row of 3** (open tickets); claimed as an action,
  then sorted at the end of their phase into a **WIN pile 成團** (completed) or **LOSE pile 遺珠** (unfinished)
  and tallied once at game end (Σ win values − Σ floor(value/2) per lose ticket). *(Piles: WIN = 成團 "Tours
  That Ran" / infodesign label "Departures"; LOSE = 遺珠 "The Ones That Got Away".)*
- **ingredient Market cards** — a **day deck + a night deck per region** (5-palette: 4 signatures + the
  common in C & S) **+ scoped event cards** (each tagged ⦿/⬢/➤; hazard-leaning; tax-not-destroy) — the
  **night decks run event-heavier** (the hectic night-market feel). Recoloured day vs night. **Plus one
  special TABLE-WIDE event — 排班保養 "Scheduled Maintenance" (v6.3.1 CD-2)**: the HSR (N↔S) is down for ALL
  players for one round of turns (everyone takes the slow road around the ring); its own **island-wide
  banner frame** (NOT a ⦿/⬢/➤ scoped card — a new event *sub-type*, not a new keyword). **LOCKED at 2
  copies** — one in the **North NIGHT** deck + one in the **South NIGHT** deck (a felt ~12% beat; 1 copy was
  ~7% near-invisible; ⚠ the sim module's `TA_MAINT_COUNT=1` default is NOT canon). Fires on a Visit / CStore
  draw (a Travel flyby returns it unfired). Re-homes the retired 里長伯 no-HSR flaw as a warm, symmetric,
  table-wide friction.
- **~24 Buzz tokens** (@2p; committed, public, contested — placed on vendors, cleared on a win).
- **5 Character mats** (ability + flaw — **里長伯 · 媽寶 · 網紅 · 大胃王 · 大哥**; validated by the gated
  character re-pass re-sim (DONE — five-char band 43.5–55.2%, all in band). **里長伯 REWORKED (v6.3.1 CD-1,
  LOCKED −1/+1 as-is, 55%):** picks a **home region** at setup — his −1 discount works only there, and he
  pays a **+1-ingredient away-tax** to Bribe anywhere else; the old no-HSR flaw is **removed** (re-homed as
  the table-wide "Scheduled Maintenance" event). **Starts Reach 2 like everyone — NO start-Reach change**
  (⚠ the sim module's `TA_COUNCILLOR_REACH=1` default is NOT canon). His mat carries a home-discount marker
  + an away-tax reminder icon → bg-infodesign. FTUE watch: North home-camping (~60% picks North, ~75%
  home bribes). *(網紅 reads in band ~51% in the re-sim with its lost-turn flaw retired — a character-kit
  recommendation carried to bg-playtest/bg-developer, not part of this three-call balance lock.)* + 4 Agent
  pawns + **Reach markers + Tours-Completed markers** + the
  **vendor-claims clock marker** (day-clock track, dusk + last-train marks) + **~4 ★ Star tokens**.
**Component-load flag (bg-elegance / bg-infodesign):** two face-down piles per region + 5 face-up vendors +
a 3-ticket row — confirm the table stays parseable.

## Win condition & scoring
**v6.3 (TICKETS-ONLY LOCKED — ONE scoring vector; neither vendors nor Reputation score).** The game ends at
the **last train home** (the **10th table-wide vendor claim** @2p), **highest total wins** (no
sudden-death). **Score = your Tour Tickets, and nothing else:** each claimed ticket is judged at the end of
its deck's phase (DAY at dusk, NIGHT at the last train) into your **WIN pile 成團** / **LOSE pile 遺珠**,
tallied **once at game end** = **Σ(win values) − Σ(floor(value/2) per lose ticket)**. **Vendors do NOT
score** (Change 0) — a vendor is pure engine (discount ramp + a stop you assemble to complete tickets); it
keeps a printed **value** attribute only for the few value-referencing tickets + to mark the ★ apex prizes.
**Reputation does NOT score** — the old `3→+2 · 6→+4 · 9→+6 · top→+9` end-VP table is **DELETED**
(Reputation now gates Buzz — see Signature twist). **Milestone boons** ("Rave Reviews") sit on the
**Tours-Completed counter** at your **2nd & 4th** completed tour, `perplayer` (**each agent earns their own**
— no leader pump): Mark 1 → +1 Reach; Mark 2 → 1 ingredient of choice + next Bribe −1. **Tiebreak: most
vendors → most regions covered → fewest LOSE-pile tickets.** Expected 2p **winner ticket-score ~10–14** (sim:
winner ~12.8, margin ~6–7 on the expanded deck; a sim knob — far lower absolutes than the old value-inclusive
band, since value no longer adds in). Detail: `design/v6.3-content-draft.md`.
_(Why tickets-only: under "both" scoring a grind-the-fattest-vendor line (`ignore_obj`) won 80.7%; making
tickets the sole score structurally kills it → 43.8%. Sim-validated in `sim-notes.md §v6.3-FIX`.)_

## Rules summary
Turn = one of **Visit / Convenience Store / Travel / Promote / Bribe a Vendor / Claim a Tour Ticket**;
Larder cap 7. **Buzz is committed on vendors** (public; region-gated; both agents can pile on). To **Bribe**:
be **with the vendor**, hold **≥2 more Buzz than your rival**, pay its ingredients (− region discounts);
winning adds an **engine piece** (may complete a held ticket → +1 Tours Completed) but **scores no points**
(vendors don't score), clears the vendor's Buzz to supply (freeing your Reach cap), refills the slot, moves
the clock +1, locks the rival out. Ingredient market decks are face-down; **events fire by scope on Visit +
Convenience Store**
(Travel whiffs). **Day → Night:** at **dusk** the whole day layer is cleared island-wide — **both the day
vendor decks and the day ingredient decks** are removed and replaced by **night decks** (recoloured, and the
night ingredient decks run event-heavier); **players keep their Larder**. At the **last-train** mark →
finish the round + one more full round → score. **The clock is the VENDOR-CLAIMS clock** (each vendor
claimed advances the day; **dusk = 5th table-wide claim, last train = 10th @2p**; the marks grow with player
count; deck-exhaustion backstops end a phase). **Tour Tickets are the sole score** via the **win-pile /
lose-pile** model (judged at the end of each ticket's phase, tallied once at game end); vendors are pure
engine. Full teach order → `design/rules-draft.md` (v6.3, tickets-only).

## Open questions & risks
- ✅ **Spine — DECIDED & LOCKED (v6.2, 2026-08-07):** region vendor markets + Buzz-majority fight +
  push-your-luck ingredient decks + a **Day→Night VENDOR-CLAIMS clock** + **Tour Tickets** (win-pile /
  lose-pile) + the 5-ingredient palette. Drinks are low-value vendors (fork/off-clock gone). Five intended
  playstyles. **Sim-validated + CD-locked; the residuals below are all table/feel questions.**
- ✅ **CLOCK — DECIDED (vendor-claims, LOCKED):** the day advances as vendors are claimed (dusk 5 / last
  train 10 @2p, growing with count). The mission-clock A/B is closed (vendor-claims was tighter: sd 3.9,
  crisp mid-game dusk, ~14% stall). *Pacing watch:* bot games ran ~25 turns/player (over the 14–18 estimate)
  because the markets deliberately add travel; a human table should be tighter (~25–30 min) — lower the
  marks if it drags.
- ✅ **Characters — RESOLVED (kits LOCKED):** **大哥 = lead-by-1, no flaw** (51.7%); **媽寶 = keep-2** (45.6%,
  was 29% at keep-1); **大胃王 = H1-A** (52.6%); **網紅 = Going-Viral + misses its first night-phase turn**
  (CD refinement — a concrete lost-turn flaw replacing "starts behind"; **⚠ KEY table balance-check — may
  over-correct below 45%**, dial in reserve); 里長伯 unchanged (51.8%). No kit needs a day/night tweak.
- ⚠️ **RISK #1 (carried, make-or-break) — is the Buzz-majority fight fun/tense, not degenerate?** And does
  spreading vendors across region markets make it too RARE (players courting different regions rarely
  collide)? Sim: ~5% contested (a floor, not near-zero — no hard flag), but the *feel* is unmeasurable in
  sim → **the #1 table question** (Screentop plan §2).
- ⚠️ **RISK #2 — do all FIVE playstyles live, and is a well-timed MIX good? SIM PASS:** all five in a 43–53%
  band (none >~53%); a mix crushes the ignore-both control (73%); pure-drinks is dead (~0.5%). *Disruptive*
  is the weakest lane (46.7%) — viable, not a trap, not oppressive; if toothless at the table the fix is
  *more contest-reward*, not nastier events.
- ✅ **RISK #3 — does travel SPREAD? RESOLVED in canon.** East PASS (18% src, was 9% in v6.1). The old
  "Central under-pulled (13% src, tea had no export demand)" flag is **now fixed in the CD-4 night curve**:
  two night marquees point at C tea (胡椒餅 {N:2,C:1}, 麻糬 {E:2,C:1}), closing N→C→S→E→N into a true
  four-region loop. **Data step for bg-developer** (carry the two →C costs into `vendors.csv`; re-check C
  sourcing ≥18% after the rebuild) — NOT a rules change.
- ⚠️ **Tour-Ticket −½ penalty (elegance A/B, carried to the table):** sim saw no behavioural difference
  (bots only claim finishable tickets), so it can't judge the penalty's real job (disciplining human
  *speculative* claims). **Kept**; the Screentop session decides whether claims feel agonised-over (keep) or
  inert (bg-elegance may cut). *(Now expressed as the win/lose-pile model — same scores, simpler accounting.)*
- ⚠️ **WEIGHT / table-state:** bg-elegance's v6.2 read = within budget (~2.4, under 2.5) but felt weight is
  in **table-state** (the ticket row + 5 face-up vendors + 2 face-down piles/region); keywords ~14/15 and
  component types near-full. The win/lose-pile model *reduces* scoring prose (helps the rulebook-over-cap
  flag). Component-load parse is a live FTUE check.
- **Sensitivity:** a **real place & culture (Taiwan)** — the **East region is Indigenous-forward** (generic
  respectful labels, consultant before art), "Bribe"/大哥 warmth rails, 繁體 + Tâi-lô discipline. Owned by
  `bg-theme` + `bg-publishing`; paid Taiwanese cultural + language consultant before art/print.

## Status by stage
- [x] Ideation
- [x] Research
- [x] Exploration
- [x] Design ← **v6.3.1 BALANCE-VALIDATED + LOCKED (2026-08-08)** — the four CD reworks re-sim-validated,
  the CD's three final calls locked (CD-4 soft night curve · CD-1 里長伯 −1/+1 · CD-2 Maintenance ×2).
  *(v6.3 tickets-only lock 2026-08-07; v6.2 the prior sim-validated build.)*
- [x] **Character re-pass + v6.3.1 re-sim ← DONE** (`sim-notes.md §v6.3.1`, re-executed 2026-08-08): the
  night-half sourcing probe (113% of day — CD-4 soft curve validated), Taipei-start seat balance (ok at
  2p/3p/4p), Scheduled Maintenance impact, and the five-character band (43.5–55.2%, all in band). Owned by
  `bg-playtest`.
- [ ] **Development ← NEXT (now unblocked): bg-developer** — drop vendor scoring; rebuild `tickets.csv`
  (44-ticket deck, DAY 20/NIGHT 25); rebuild `vendors.csv` to the LOCKED soft night curve (both 3 / apex 4 /
  top 5, cross-region + the Central tea-export fix); 里長伯 mat −1/+1 start-Reach 2; seed 2 Scheduled
  Maintenance; wire Tours-Completed + `perplayer` milestones. **Build to CANON, not the sim-module defaults.**
- [ ] Prototype (Screentop.gg / PnP)
- [ ] Playtesting (the 2p FTUE — claiming-feels-joyless? ticket choice rich-not-fiddly? is the ~5% Buzz fight fun?)
- [ ] Marketing
- [ ] Publishing / IP

## Links
- Current spec: `design/v6.3-content-draft.md` (TICKETS-ONLY LOCKED) · Prior: `design/v6.2-content-draft.md` · v6.1 history: `design/design-doc.md`
- Identity: `identity.md` · Decisions: `decision-log.md` · Sim: `playtests/sim-notes.md` (§v6.3.1 — the four-CD-change re-sim + verdict)
