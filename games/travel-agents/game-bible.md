# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design — locked for CD sign-off** (design-doc **v5** — the two-Act "one glorious eating day" tightening of the v4 Buzz-majority rework: committed public Buzz on vendors, push-your-luck market decks; **TWO Acts on a day-clock** — Afternoon Crawl → Night Market → **Code Red**; **Region-Coverage folded into a Mission**; **"Bribe a Vendor" LOCKED**; five Taiwanese-social-type characters. Extract + Poach cut. **No sim run yet — gated on CD sign-off.**)

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
- **Playtime:** **~25–30 min at 2p** (v5 target; the two-Act day-clock paces to ~5–6 wins/player; sim to confirm)
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
- **Expansion ambition:** base = the competitive vendor-fight engine (**v4**): the shared **Vendor Board**
  Buzz-majority fight + two inputs (region ingredients + committed **Buzz**) + the compounding discount +
  escalating **Acts** + hybrid multi-track scoring (Prestige / Reputation / Coverage) + the secret
  **signature mission** + push-your-luck **market decks**. Held hooks (not baggage): a **6th+ character**
  (e.g. the Homesick Local) and a small vendor-pack, a deeper **campaign / "tour journal"** arc, and a
  **destination series** ("Travel Agents: &lt;place&gt;") if the base sings. Owned by `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- 1–3 mechanism families and the blend; why each part needs the others (see knowledge/archetypes.md). -->
**Sourcing engine (spine A) + a Buzz-majority "area-influence" vendor fight** (CD v4 rework, 2026-08-06;
see `design/design-doc.md` v4). A **tight two-player engine-builder** with a genuine *fight* at its centre
(Splendor Duel / LOTR Duel band, reaching toward an Arcs-Court interaction), built on:
- **Two-input engine-building with a contested currency.** You win **Vendors** off an escalating shared
  **Vendor Board** by paying **two inputs** — region-specific **fresh ingredients** + **Buzz** — but Buzz
  is no longer a private spend: it's **committed publicly ON each vendor** (Arcs-Court-like). You must be
  **on-site** to place it, both agents can pile onto the same vendor, and you **win only by out-hyping your
  rival by ≥2 while holding the ingredients**. Each vendor won is a **permanent engine piece**: a
  **compounding ingredient discount** (region icon) feeding several scoring vectors.
- **Set collection with a twist — recipes by region** (the ingredient input). Vendor costs name
  region-specific ingredients from the Taiwan **regions that actually supply them** (oysters coastal, tea
  in the hills, east-coast Indigenous produce, North's beef/pork/chicken/egg). Real food geography, not
  "food + map." The v3.1 movement rebalance carries over (anchor in-region + ~40% cross-links); **pantry
  is cut** — costs are named specialties only.
- **Push-your-luck sourcing.** Each region's market is a **face-down deck** (its 2 specialties + salted
  **hazard events**). **Visit the Local Market** = draw 3, keep 2 — a flipped typhoon fires on the spot.
  The **Convenience Store** (top card of any region, blind) and **Travel** (arrive with a card) are the
  low-variance valves.
- **Region routing / travel** — you move *because* the ingredient AND the Buzz-placement AND the Bribe are
  all region-gated. Position matters more than ever.
- **The rival fight + the escalating day:** the **Vendor Board** is the public tug-of-war (out-hype the
  rival to win a vendor); the game runs through **TWO Acts on a single day-clock** — **Act I Afternoon
  Crawl 下午 (Stalls → Eateries) → Act II Night Market 夜市 (Marquee)** — the clock **advancing on
  table-wide wins**, flipping the board to the Marquee deck at **dusk** and ending the game at **Code Red**
  (the last train home). No linear Season counter, no Extract.

## Core loop
<!-- The repeated cycle of decisions and rewards, step by step. -->
Specified in `design/design-doc.md` (v5). **A turn = ONE action:** **Visit the Local Market** (draw 3 keep
2 from your region's deck; hazards fire) · **Convenience Store** (top card of ANY region's deck, blind,
whiffs on an event) · **Travel** (move one region, draw the arriving region's top card) · **Promote**
(place 2 Buzz from supply onto vendor(s) in your current region) · **Bribe a Vendor** (in its region,
holding ≥2 more Buzz on it than your rival, pay its ingredients − discounts → win it: Prestige scored
**live**, a Rep bump, a permanent perk/discount; its Buzz clears to supply; refill the Board; advance the
**day-clock**; lock it from the rival). You can only take a region's **specialty** while there (oysters
South, tea/pearls Central, rice/greens East, beef/pork/chicken/egg North). Your **Larder sits face-up**
(the secret **signature mission** is the game's *only* hidden info). **Larder caps at 7.** The tension every
turn: dig the market for the specialty you need (risk a hazard), grab a safe blind card, travel on, pile
more Buzz onto the vendor you're fighting for — or close the Bribe before your rival out-hypes you.
*(Extract, Poach, and the Coverage scoring track are cut; breadth is now a Mission.)*

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
**Buzz is a public, committed, contested majority you pile ON the island's vendors — you win a vendor by
out-hyping your rival ON-SITE (by ≥2) while holding the ingredients its dish needs, and each vendor won is
an engine piece (a compounding ingredient discount) climbing Prestige and Reputation toward your hidden
signature tour.** The travel-agent fiction (promote a vendor, out-woo your rival, win their blessing) and
the food-geography fiction (source where the food lives) drive the *same* decisions. The runaway brake is
the **Buzz fight itself** — undiscounted, region-gated, and raise-able by your rival — so even a
fully-ramped engine must still win a contested tug-of-war for every vendor. *(v4 — reshapes v3's
private-Buzz spend into an Arcs-Court-like public majority; the "**Bribe a Vendor**" keyword is LOCKED —
the warm, comedic *"marketing opportunity"* hard sell, never corruption.)*

## Components (summary)
*(v5 target for `bg-developer`, **after CD sign-off**; full BOM regenerates in `components/manifest.md`.)*
**~6 component types** (pantry tokens gone, event tiles folded into the market decks), within the cap of
**8**: (1) **Map board** — Taiwan, 4 regions on a ring + HSR spine, carrying the **day-clock** (with a
**dusk** mark and a **last-train / Code Red** mark), the **Prestige (VP) track**, the **Reputation track**,
the **Vendor Board** slots (with per-vendor **Buzz zones**) and a face-down **market-deck** space per
region; (2) **25 Vendor cards** — three **types** (**Stalls ×11 / Eateries ×8 / Marquee ×6**) dealt across
**two Act decks** (Act I Afternoon Crawl = Stalls-on-top + Eateries-beneath; Act II Night Market =
Marquee), one per **real locked dish** (Tâi-lô + 繁體), each with cost (**named specialties only**), a
**region icon** (discount + **the region you must stand in to hype/Bribe it**), **Prestige**,
**Reputation**, a **perk**, and its **type**; **2–3 apex "Legendary" Marquee carry a printed ★ (7–8
Prestige)** — a real Michelin/Bib-Gourmand/competition accolade making them the hot targets; region-icon
balance held across N/C/S/E; (3) **~12 Mission
cards** (secret +7 vendor patterns, draw-3-keep-1 — **now the sole breadth/grand-tour carrier**); (4)
**~50–56 Market cards** — four face-down region decks of **specialty ingredient cards** (10 specialties
incl. chicken 雞 + egg 蛋) **+ event cards** (~14, hazard-leaning ~55–60%), sharing a common back; (5)
**~24 Buzz tokens** (@2p; the committed, public, contested resource — placed on vendors, cleared on a win);
(6) **5 Character mats** (one ability + one flaw each — the v5 cast: **里長伯 · 媽寶 · 網紅 · 大胃王 · 大哥**;
里長伯 & 媽寶 = KEPT kits re-lored, 大胃王 & 大哥 = NEW, numbers sim-tunable) + 4 Agent pawns +
Prestige/Rep markers + **day-clock marker** + **~4 ★ Star tokens** (the dynamic value swing — a "vendor
gets hot" boon event drops one on a Board vendor for **+2 Prestige / +1 Rep**, recyclable) (board bits).
**Cut:** **pantry tokens**, **Event tiles** as a separate type (now market cards), the **Season counter**
(→ day-clock), the **Coverage scoring key**.
Deck-size note: 25 vendors across 2 Act decks is comfortable at 2p; 3–4p may want a few more per type
(→ `bg-architect`).

## Win condition & scoring
Hybrid multi-track: the game ends by **Code Red** (the day-clock's last-train mark), **highest total VP
wins** (no sudden-death). Score = **Tour Prestige** (vendors' stars: Stalls=1 / Eateries=3 / Marquee=5–6)
+ **Reputation** end-VP by final track position (3→+2 · 6→+4 · 9→+6 · top→+9; **pure end-VP — milestone
perks cut**) + **secret signature mission** (+7 if completed, revealed at scoring — **now the carrier of
the grand-tour breadth line**). A **live tracker** (Prestige + Rep markers) shows both open vectors; the
**only** off-tracker VP is the hidden +7. **Region-Coverage is CUT as its own scoring track** (breadth →
the "all 4 regions" Mission). ≥2 paths kept competitive (tall vs rep-climb vs the grand-tour mission pull
against each other; the Buzz fight adds opponent-dependence so openings don't solve). **Tiebreak:** highest
Reputation, then most vendors, then most regions covered. Expected 2p winner **~24–32 VP** (retuned for the
shorter ~5–6-win game). Detail + balance model in `design/design-doc.md` v5.

## Rules summary
Drafted in `design/rules-draft.md` v5 (teach-in-play order). Turn = one of **Visit the Local Market
(draw 3 keep 2, hazards fire) / Convenience Store (top of any deck, blind) / Travel (move + draw arriving
region) / Promote (place 2 Buzz on in-region vendor[s]) / Bribe a Vendor**; Larder cap 7. **Buzz is
committed on vendors** (public, region-gated, both agents can pile on the same vendor). To **Bribe** you
must be **in the vendor's region**, hold **≥2 more Buzz on it than your rival**, and pay its ingredients
(− region discounts, floored); winning scores Prestige + Rep + a permanent discount icon, **clears the
vendor's Buzz to the supply**, refills the Board, advances the **day-clock +1**, and locks the rival out.
Market decks are face-down (hazards fire on Visit; single blind draws whiff). The game is **one eating day
on a day-clock** (advances +1 per table-wide win): at the **dusk** mark (2p: 6th win) the board flips from
**Act I Afternoon Crawl** (Stalls → Eateries) to **Act II Night Market** (Marquee); at the **last-train**
mark (2p: 10th win) **head office calls Code Red** → finish the round + one more full round → reveal
missions → score. (Rep-top scores +9 but doesn't call Code Red.) **One hidden-info hook only:** the secret
signature mission.

## Open questions & risks
- ✅ **Mechanism spine — DECIDED (v4 rework + v5 tightening, 2026-08-06):** sourcing engine + a
  **Buzz-majority vendor fight** (committed public Buzz, Arcs-Court-like) + **push-your-luck market decks**
  + **TWO Acts on a day-clock** (Afternoon Crawl → Night Market → Code Red). Extract + Poach + pantry cut;
  **Coverage folded into a Mission**; **"Bribe a Vendor" LOCKED**; five v5 Taiwanese-social-type characters.
  **Design locked for CD sign-off; sim gated.**
- ⚠️ **TOP RISK #1 (v4, THE make-or-break) — is the Buzz-majority tug-of-war fun/tense, not a swingy
  slap-fight or a degenerate "never commit, always snipe"?** New, load-bearing, untested. *Attack (sim +
  table):* Buzz-war frequency/depth (sane escalation vs draining the supply on one vendor); **"snipe-only"
  win-rate ≤~55%** (early commitment must be viable); loser's-tempo cost ("outraced not robbed" vs
  feels-bad); Buzz supply pressure (~24 @2p right?). *Fail fixes:* tune the ≥2 margin (≥1/≥3), Buzz/Promote,
  supply size, or a partial loser-refund.
- ⚠️ **TOP RISK #2 (v4) — no dominant track or opening under the new interaction.** Keep **tall ≈ rep-climb
  ≈ breadth** competitive; the Buzz fight should keep openings from solving (opponent-dependence). *Attack:*
  dominant-track/opening probe (no line >~55%, ≥3 viable) + 2p Screentop feel-test. *Fail fixes:* rebalance
  costs / track rewards.
- ⚠️ **TOP RISK #3 (v4) — is the push-your-luck market spicy not punishing, and does movement still
  spread?** *Attack:* hazard-hit rate per Visit; Visit vs Convenience-Store usage (is Visit worth the
  risk?); per-region sourcing share (each ≥~18%, South not starved); inter-region moves/game (region-gating
  should *increase* travel). *Fail fixes:* hazard density, reveal-count, the "brewing" telegraph knob, the
  cross-link rate.
- ⚠️ **Secondary risks:** per-character win-rate **45–55%** with no dominant char×mission combo (the
  re-homed Rookie/Gourmand are now **sim-legible**; watch the sharper Influencer in the Buzz fight); does
  the **Acts** pacing land ~7–8 wins/player in ~40–45 min; does the boon/hazard ratio feel warm not grim;
  does Fellowship survive (the comedic Buzz fight + market drama).
- ⚠️ **WEIGHT (honest):** v4 is a real increase — **~2.5–2.6 pre-trim**, at/over the 2.5 ceiling, driven by
  the Buzz-majority system. Banked: Extract/Poach/pantry cut, Season→Acts, tiles→cards (component types
  7→~6). **Hold ≤2.5** by folding **Coverage → mission-only** (recommended), then **Rep milestones → pure
  end-VP**; else **consciously raise the ceiling to ~2.6** (defensible next to Arcs/Splendor Duel+).
  `bg-elegance` guards. **← CD decision (see design-doc *Open decisions* D1–D4).**
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
