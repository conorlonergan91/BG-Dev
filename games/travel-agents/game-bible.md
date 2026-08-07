# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design — v6.2 PROPOSAL, content drafted, pending
> a sim pass + CD lock.** v6.2 restructures the board into **region vendor markets** and makes **missions
> the spine** (a face-up ticket row + a mission clock). It **supersedes v6.1's central Ladder, the
> ladder-vs-drinks FORK, off-clock/region-free beverages, and the single secret +7 mission**: there is now
> **one kind of vendor** (food and drinks alike; drinks are just the low-value ones), each of the 4 regions
> has **its own face-down vendor pile** (daytime stacked on nighttime), **1–2 face-up per region** (North 2,
> the rest 1), and the day runs **Day → Night → the last train home**. What stands from before: the
> **Buzz-majority public hype-fight**, the **5-ingredient palette** (4 signatures + 1 common), the **five
> Taiwanese-social-type characters**, and the sensitivity rails. Full current spec:
> `design/v6.2-content-draft.md`. (v6.1 detail retained in `design/design-doc.md` as history.)

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
- **The Day → Night clock + Tour Tickets (the spine, v6.2).** The day runs **Act I (daytime vendors) →
  dusk → Act II (nighttime vendors) → the last train home**. **The dusk flip is a big, thematic turnover:**
  the *entire* day layer is cleared island-wide — **both the day vendor decks AND the day ingredient market
  decks** are removed (not just the face-up cards) and replaced by **night decks** (recoloured; the night
  ingredient decks are **event-heavier** — the bustling night-market feel), while **players keep their
  Larder**. **Missions ("Tour Tickets") are the heartbeat:** a **face-up row of 3**, claimed as an action,
  scored **retroactively** (+value / −½ if unfinished), drawn from **daytime / nighttime / general** pools
  (12 per phase in the box, **5 drawn per phase per game**). The **clock is driven by missions** — the day
  advances as **claimed missions are completed** (to A/B vs a vendor-claim clock in sim).

## Core loop
<!-- The repeated cycle of decisions and rewards. -->
Full spec in `design/v6.2-content-draft.md`. **A turn = ONE action:**
- **Visit the Local Market** (flip 3 of your region's ingredient deck, keep 2; events fire by scope) ·
- **Convenience Store** (top card of ANY region's ingredient deck, blind — grab the common, or fire a
  scoped event, incl. onto a rival's region) ·
- **Travel** (move one region — HSR links N↔S — draw the arriving region; an event whiffs) ·
- **Promote** (place 2 Buzz onto vendor(s) you're with in this region) ·
- **Bribe a Vendor** (be on-site, hold ≥2 more Buzz than your rival, pay its ingredients − discounts → win
  it: Prestige scored **live**, a Rep bump, a perk; its Buzz clears to supply; refill the slot; lock it) ·
- **Claim a Tour Ticket** (take one from the face-up row of 3; it refills — a public commitment scored
  retroactively at game end).

You court whatever's **face-up in the region you stand in** (1–2 vendors + the day's layer). **Larder caps
at 7.** The tension every turn: chase the region's face-up prize, dig for the ingredient you're short,
grab a cheap drink when it's the efficient local play, commit to a ticket (and race to finish it before the
penalty bites), or reach into a rival's region with a scoped Convenience-Store event. Day flips to night as
the itinerary fills; when the night winds down, catch the **last train home**.

## Signature twist
<!-- The one memorable hook that makes it *this* game. -->
**Buzz is a public, committed, contested majority you pile ON the island's vendors — you win a vendor by
out-hyping your rival ON-SITE (by ≥2) while holding the ingredients its dish needs, and each food vendor
won is an engine piece (a compounding ingredient discount) climbing Prestige and Reputation.** The
travel-agent fiction (promote a vendor, out-woo your rival, win their blessing) and the food-geography
fiction (source where the food lives) drive the *same* decisions. The runaway brake is the **Buzz fight
itself** — undiscounted, region-gated, raise-able by your rival. **v6.2 sets this against your ITINERARY:**
missions ("Tour Tickets") are the game's spine — claimed openly, raced against a −½ penalty, and the thing
that **paces the day toward night**. *(The "**Bribe a Vendor**" keyword is LOCKED — the warm, comedic
"marketing opportunity," never corruption.)*

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
- **Map board** — Taiwan, 4 regions on a ring + HSR spine (N↔S), carrying the **Day→Night clock** (dusk +
  last-train marks), the **Prestige (VP) track**, the **Reputation track**, and — **per region** — a
  face-down **vendor-deck** space with **1–2 face-up slots** (North 2, others 1) **and** a face-down
  **ingredient-deck** space (each holds the **day** deck in Act I, swapped for the **night** deck at dusk).
- **~48 Vendor cards** — a **day set + a night set per region** (drinks are the low-value vendors mixed into
  each; recoloured day vs night), one per real locked dish (繁體 + Tâi-lô), each with cost (5-palette), a
  **region icon** *(food only — the ramp; drinks carry none)*, **Prestige**, **Reputation**, and a **perk**.
  **One apex (★) vendor per region in the night set** (comparable value — the rotating top prize); the
  dynamic **★ Star token** can make a vendor hot mid-game (+2 Prestige/+1 Rep, recyclable).
- **~27 Tour-Ticket (Mission) cards** — **12 daytime + 12 nighttime + a small general pool**; **draw 5 per
  phase per game** (rest to the box). A **face-up shared row of 3** (bg-theme locked open tickets, not
  hidden); scored **retroactively** (+value / −½ if unfinished).
- **ingredient Market cards** — a **day deck + a night deck per region** (5-palette: 4 signatures + the
  common in C & S) **+ scoped event cards** (each tagged ⦿/⬢/➤; hazard-leaning; tax-not-destroy) — the
  **night decks run event-heavier** (the hectic night-market feel). Recoloured day vs night.
- **~24 Buzz tokens** (@2p; committed, public, contested — placed on vendors, cleared on a win).
- **5 Character mats** (ability + flaw — **里長伯 · 媽寶 · 網紅 · 大胃王 · 大哥**) + 4 Agent pawns +
  Prestige/Rep markers + the **day-clock marker** + **~4 ★ Star tokens**.
**Component-load flag (bg-elegance / bg-infodesign):** two face-down piles per region + 5 face-up vendors +
a 3-ticket row — confirm the table stays parseable.

## Win condition & scoring
Hybrid multi-track: the game ends at the **last train home**, **highest total VP wins** (no sudden-death).
Score = **Tour Prestige** (sum of your vendors' values — drinks 2 / daytime food 1–3 / nighttime food 4–6 /
★ apex 6–8) + **Reputation** end-VP by final track position (3→+2 · 6→+4 · 9→+6 · top→+9) + **Tour Tickets**
(**+value each if completed, −floor(value/2) each if unfinished** — the retroactive, press-your-luck
objective layer). ≥3 paths kept competitive (see the five playstyles); the Buzz fight adds
opponent-dependence so openings don't solve. **Tiebreak:** highest Reputation, then most vendors, then most
regions covered. Expected 2p winner **~22–32 VP**. Detail + balance model in `design/v6.2-content-draft.md`.

## Rules summary
Turn = one of **Visit / Convenience Store / Travel / Promote / Bribe a Vendor / Claim a Tour Ticket**;
Larder cap 7. **Buzz is committed on vendors** (public; region-gated; both agents can pile on). To **Bribe**:
be **with the vendor**, hold **≥2 more Buzz than your rival**, pay its ingredients (− region discounts);
winning scores Prestige + Rep + a perk, clears the vendor's Buzz to supply, refills the slot, locks the
rival out. Ingredient market decks are face-down; **events fire by scope on Visit + Convenience Store**
(Travel whiffs). **Day → Night:** at **dusk** the whole day layer is cleared island-wide — **both the day
vendor decks and the day ingredient decks** are removed and replaced by **night decks** (recoloured, and the
night ingredient decks run event-heavier); **players keep their Larder**. At the **last-train** mark →
finish the round + one more full round → score. **The clock is mission-driven** (completing claimed Tour
Tickets advances it — to A/B vs a vendor-claim clock in sim). Full teach order → `design/rules-draft.md` (to be updated to v6.2 at build).

## Open questions & risks
- ✅ **Spine — DECIDED (v6.2):** region vendor markets + Buzz-majority fight + push-your-luck ingredient
  decks + a **Day→Night mission clock** + **Tour Tickets** + the 5-ingredient palette. Drinks are low-value
  vendors (fork/off-clock gone). Five intended playstyles. **Content drafted; pending a sim pass + CD lock.**
- ⚠️ **RISK #1 (carried, make-or-break) — is the Buzz-majority fight fun/tense, not degenerate?** And in
  v6.2, **does spreading vendors across region markets make it too RARE** (players courting different
  regions rarely collide)? The sim reads contested-win frequency; the *feel* is a table question. 大哥's
  tie-win is still the dominance probe — **H2 unresolved (needs a 4th option)**.
- ⚠️ **RISK #2 (the fork's successor) — do all FIVE playstyles live** (each ≤~55%, some intransitivity),
  and is a **well-timed mix** a good line? v6.1 sim showed a drinks *lean* was a trap and flat drink value
  couldn't fix it; **Tour Tickets** (a greedy-visible payoff) moved a mix toward parity — v6.2 is meant to
  finish the job (drinks as the cheap local play + mix/drink tickets). *Disruptive* is the weakest-supported
  today (take-that is light in sim) — watch whether it's a viable lean or just a spoiler.
- ⚠️ **RISK #3 — does travel actually SPREAD** across all four regions (East not starved), now that value is
  distributed (one ★ per region, cross-region cycle N→S→E→N, coverage tickets, scoped events)? Sim reads
  per-region sourcing/claim share + inter-region moves.
- ⚠️ **PACING — the clock.** Mission-clock vs vendor-claim clock (the sim A/Bs which paces better). The
  all-vendor-claims clock introduced a **rush** risk (cheap claims race the end); the mission clock is the
  proposed fix. Confirm ~25–30 min across the random 12→5 mission draws (length variance is the watch).
- ⚠️ **Characters:** each **45–55%**, no dominant char×mission combo. Live: **大哥 too strong (H2), 網紅
  hot, 媽寶 weak** (from the v6.1 sim); 大胃王 fine (ship H1-A).
- ⚠️ **WEIGHT / table-state:** bg-elegance re-reading v6.2 (removed special-casing vs added
  markets/clock/tickets); the component-load flag above.
- **Sensitivity:** a **real place & culture (Taiwan)** — the **East region is Indigenous-forward** (generic
  respectful labels, consultant before art), "Bribe"/大哥 warmth rails, 繁體 + Tâi-lô discipline. Owned by
  `bg-theme` + `bg-publishing`; paid Taiwanese cultural + language consultant before art/print.

## Status by stage
- [x] Ideation
- [x] Research
- [x] Exploration
- [ ] Design ← **in progress** (v6.2 proposal: content drafted, sim pass + CD lock pending)
- [ ] Development
- [ ] Prototype (Screentop.gg / PnP)
- [ ] Playtesting
- [ ] Marketing
- [ ] Publishing / IP

## Links
- Current spec: `design/v6.2-content-draft.md` · Deeper (v6.1 history): `design/design-doc.md`
- Identity: `identity.md` · Decisions: `decision-log.md` · Sim: `playtests/sim-notes.md`
