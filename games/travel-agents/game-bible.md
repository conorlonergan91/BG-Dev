# 🎲 Travel Agents: Taiwan Food Tour — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · **Version: V7-M** (merged PR #13, 2026-08-10).
>
> **Status:** V7-M development CLOSED at a clean, sim-validated state (N=400); the next arbiter is a human
> playtest (CD testing mainly at 3–4 players). Full pre-V7 design stratigraphy (v6.2 → v6.3 → v6.3.1 → V7)
> is preserved in `archive/game-bible-history.md`; the pre-V7 decision entries in `archive/decision-log-pre-v7.md`.

## One-liner
<!-- The hook a stranger would repeat. -->
Rival travel agencies go elbows-out through one Taiwan eating day — ride the rails between four regions,
gather ingredients, and pile your **Followers** on the island's food stalls: win a stall by drawing the
**biggest crowd** and it joins your tour, making the next one cheaper. Craft the best tours and cash the
most **Bookings** before the **last train** to be **Top Agent** — in the most over-the-top way you can.

## Core fantasy / player role
<!-- Who you are, what you're doing, the feeling (the "kind of fun"). -->
You run a travel agency, and so do your rivals — a pack of over-the-top, **battle-hungry** rival agents in
a zany, all-out dash to assemble the single best Taiwan foodie **tour** and sell the most tickets. Elbows
out, dirty tricks welcome — *on each other*, never on the island: cut a rival off at the stall, snatch the
hot vendor out from under them, and gun it for the last train. The literal job is wholesome — showing off
the island's best food — but you compete for it like it's a demolition derby. Kinds of fun (**locked**):
**Discovery** (lead) + **Fellowship** (raucous rivalry) + **Challenge**.
Full felt identity, tone, look & feel and naming: `identity.md`; canonical names & terms: `names.md`;
voice bible: `prose-identity.md`.

## Positioning
- **Weight (BGG 1–5):** aim **~2.2**, ceiling **~2.5**. Band: Splendor Duel ~2.3 · LOTR: Duel ~2.4 · Arnak ~2.7.
- **Players:** **3–6** (design home 3–5 solid, 6 a validated stretch; the 2p duel is retired).
- **Playtime:** **~30–45 min** (the deep-claiming recipes + follower fight make a meatier game than the old 2p duel).
- **Tone:** silly / raucous / over-the-top — a madcap competitive race (Wacky-Races energy); warm toward
  Taiwan and its food, elbows-out between the rival agents.
- **Comparable:** *Splendor Duel* / *Arnak*-style engine-building + *Ticket to Ride* objective tickets,
  scaled to a 3–6p area-majority race and wrapped in an over-the-top, wacky Taiwan food-tour.
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight ~2.2; ceiling ~2.5.** Caps in `complexity-budget.json`.
- **Rulebook cap: 2280 words** (consciously raised for the V7-M content — the event framework, the
  Closing-Time die, follower meeples, agnostic tours + Pot-Luck — after `bg-elegance`'s fat cut). Rules-only
  landed 2262/2280; keywords 9/15; component types 8/8 (mono ship config).
- Check with `python tools/complexity/check_complexity.py --game games/travel-agents` and run
  **`bg-elegance`** each iteration. Never silent creep.

## Modes & scope
- **Player modes:** competitive **3–6**. Owned by `bg-architect`.
- **Campaign?** None planned.
- **Expansion ambition:** base = the competitive vendor-market engine (area-majority follower fight + region
  ingredient sourcing + the compounding discount + the vendor-depletion Day→Night clock + Bookings). Held
  hooks: a small vendor/booking pack, a **destination series** ("Travel Agents: <place>"), and the parked
  8-type ingredient split (see below) as a possible depth expansion. Owned by `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- mechanism families + the blend; why each part needs the others. -->
A **3–6-player area-majority engine-builder** with a genuine *fight* at its centre, built on:
- **Region vendor markets — a DAY engine, a NIGHT payoff.** Each of the 4 regions (**North 北 · Central 中 ·
  South 南 · East 東**) has its own face-down vendor deck — a **DAY** deck of cheap, varied, low-VP **engine
  seeds** (claim them to build your region-discount engine), then, at dusk, a **NIGHT** deck of scarce,
  expensive, high-VP **trophies** (the prizes the built engine lets you afford) — with drinks mixed in as the
  low-value stalls. The DAY is the long engine-building phase; the NIGHT is the short payoff. Face-up slots per
  region scale with player count (setup chart on the board). There are deliberately **fewer stalls than
  agents** — so you collide over them.
- **Follower meeples + area-majority (the contested currency).** You win **Vendors** (**Sign Up**) by holding
  the **biggest crowd** of your committed **follower meeples** on a stall (strict plurality; a **tie
  blocks** — the Big Boss 老大 alone wins ties) **and** paying its ingredients (minus region discounts).
  Followers live in three places — your supply, your board (rallied), on a stall (committed) — and flow
  supply → board (grow, on Travel) → stall (Promote) → home on a win / back to supply on a loss. Your pool
  is a fixed **6 meeples** (the Influencer 網紅 owns **8**); total committed ≤ your **Followers-max dial**.
- **Multi-ingredient recipes + set collection — the 6-type palette.** Every vendor is a multi-ingredient,
  mostly cross-region dish. Ingredients are the **six generic categories** (each card art a MIX): **肉 Meat**
  (N sig) · **茶 Tea** (C sig) · **海鮮 Seafood** (S sig) · **糧 Pantry** (E sig) · **糖 Sugar** (common C&S)
  · **菜 Vegetables** (common N&E). Real food geography; most night dishes force a two-region engine.
- **Push-your-luck ingredient sourcing.** Each region has a face-down market deck (its signature + commons +
  salted **events**). **Market Run** = flip 3, keep 2 (events fire by scope). **Convenience Store** = top card of
  any region, blind. **Travel** = move + grow your crowd +1 (no ingredient — except the Homebody 媽寶).
- **The vendor-depletion Day→Night clock + the Closing-Time die.** The vendors ARE the clock: **18 day
  vendors → 黃昏 DUSK** (flip to night) → **12 night vendors (11 unique + 1 duplicate) → 末班車 LAST TRAIN**
  → finish the round → end. A vendor leaves by being claimed or closed. The **Closing-Time die 關門** — one
  custom d6 `[N,C,S,E,BLANK,BLANK]`, the game's only die — is the forcing function, and it rolls on a
  **per-phase cadence**: by **DAY** it rolls only after **L** rounds (L=2 at 3p, L=3 at 4–6p) — a gentle
  cadence that protects day-engine formation; by **NIGHT** it rolls at the **end of every round** ("closing
  time"), draining the night pool down to the last train. A rolled region face closes that region's oldest
  face-up stall (contested or not — followers home to boards, kept, no penalty), BLANK = a reprieve. Booking
  decks are NOT the clock; ingredient + event decks reshuffle.
- **Bookings — the tour objectives.** A face-up row of tours you **Book** (hand-limit 3, cancel-to-claim),
  in three kinds — **⟳ any-time / ☀ day / ☾ night** — or **Pot-Luck (隨緣開團)**: decline the row, draw the
  deck's top blind. Complete a Booking (成團) when your won vendors satisfy its pattern; leave one unfinished
  and it's **Cancelled (取消)** at scoring.

## Core loop
<!-- The repeated cycle of decisions and rewards. -->
Full current spec: `design/rules-draft.md`. **A turn = ONE action** (then discard Larder down to 7):
- **Market Run** — do the rounds of the market you stand in (flip 3, keep 2; events fire) ·
- **Convenience Store** (top card of any region, blind) ·
- **Travel** (move to a neighbour, or N↔S by HSR; grow your crowd +1 — no ingredient) ·
- **Promote** (place up to 2 followers from your board onto stall(s) here) ·
- **Sign Up a vendor** (hold the biggest crowd + pay its ingredients − discounts → it joins your tour, may
  complete a held Booking; your followers come home, losers' scatter to supply; leave the slot empty) ·
- **Book a tour** (from the row, or blind via Pot-Luck).

The tension every turn: chase the region's face-up prize, dig for the ingredient you're short, grow your
crowd for the fight ahead, commit to a Booking (and race to finish it before its phase closes), or reach
into a rival's region with a scoped Convenience-Store event. Day flips to night as the day vendors run out;
when the night winds down, catch the **last train home**.

## Signature twist
<!-- The one memorable hook that makes it *this* game. -->
**Followers are a public, committed, contested majority you pile ON the island's vendors — you win a vendor
by drawing the biggest crowd ON-SITE while holding the ingredients its dish needs, and each food vendor won
is an engine piece (a compounding region-ingredient discount) — the engine you assemble to COMPLETE your
tours.** The travel-agent fiction (promote a vendor, out-woo your rivals, win their blessing) and the
food-geography fiction (source where the food lives) drive the *same* decisions. The runaway brake is the
**area-majority fight itself** — undiscounted, region-gated, raise-able by rivals — plus the lost-war
Followers-max dial-drop. *(The "**Sign Up a Vendor**" keyword is LOCKED — the warm, comedic "marketing
opportunity," never corruption.)*

## Components (summary)
*(V7-M ship config; BOM in `components/manifest.md`. Data is the source — CSVs render via `make.sh`.)*
- **Map board** — one neutral shared board readable from any seat: Taiwan, 4 regions on a ring + HSR spine
  (N↔S). North's hub = **Taipei**, the **common start** for every agent. Carries the region vendor slots
  (scaled per count) + market decks, the HSR (with a Scheduled-Maintenance reminder), the **Closing-Time
  3-round clock band**, and per-player Followers-max dials / Tours-Completed. Phase-split day/night slots.
- **30 Vendor cards** — a day set + night set per region (drinks mixed in), one per real locked dish
  (繁體 + Tâi-lô), anchored to real Taiwan food-places (`design/vendor-places.md`). Each carries a
  multi-ingredient recipe (mostly cross-region), a **`min_followers` crowd-floor** (star tier 1/2/3), and a
  **`vp`** (= cost + floor − 2, range 0–11). **Icons split the two phases:** the **day food seeds carry their
  region's discount icon** (they ARE the engine); **the day drinks and ALL night vendors — trophies and ★
  apex included — carry NO icon** (night stalls are prizes, not engine). **18 day** (cheap low-VP seeds: 13
  food each with a region icon + 5 drinks) **+ 12 night** (scarce high-VP no-icon trophies + 2 珍奶 drink
  clock-fillers; 11 unique night + 1 duplicate 珍奶 stall = 29 unique + 1 dup). One ★ apex per region in the
  night set. Data: `components/vendors.csv`.
- **45 Booking cards (開團 — the tours)** — split **6 day (☀, cancel at dusk) / 8 night (☾) / 31 any-time
  (⟳, judged at last train, never cancel at dusk)**, with a per-count `counts` tag (HEAVY `456` ×7, ON-RAMP
  `3456`+onramp ×8, CORE ×30 → 3p deck ≈38, 4–6p 45). Drawn into a face-up row; Booked from the row or blind
  via **Pot-Luck**; value **3–11**. Data: `components/bookings.csv`.
- **Ingredient market cards** — a day + night deck per region: the **6-type mono taxonomy** (`ingredients.csv`)
  + scoped **event cards** (`events.csv`). See Ingredient taxonomy below.
- **~52 Event cards** — the **VERB · SCOPE · DURATION** framework (`design-doc.md` §15): columns `scope`
  (⦿ self · ✦ rival · ⬢ region · ➤ neighbour · ▦ board), `duration` (now/turn/round/phase), `verb`,
  `target`, `value`. Hazards tax-not-destroy; rival-facing ✦ auto-target the leader (magnitude 1, a small
  minority ~7). Plus the island-wide **Scheduled Maintenance 排班保養** (HSR down for a round; 阿嬤 immune)
  on its own banner. `map.json → event_deck_mix` deals a per-count subset into each region+phase deck.
  *(RENDER: event/vendor faces don't yet draw the verb/scope/duration/vp/floor icons — a presentation pass owns that.)*
- **Follower meeples** — ~8 per colour so any player can field their pool max (網紅 8; everyone else 6);
  committed, public, contested, placed on stalls.
- **6 Character mats** — the six-agent roster (see below); English names LOCKED & BLESSED, each mat printed
  tri-lingual (Tâi-lô · English · 繁體).
- **Closing-Time die 關門 + 3-round track marker** — the game's first dice/randomness; custom d6 (4 region
  faces dual-coded colour + emblem + 繁體, 2 blank). Plus 6 agent pawns (all start Taipei), Followers-max
  dials, Tours-Completed markers, COMPLETED 成團 / CANCELLED 取消 pile markers, ★ Trending markers.

## The six characters
*(Locked V7-M kits — `components/characters.csv` is canon. English name first, always.)*
- **The Old Councillor 里長伯 (Lí-tiúⁿ-peh)** — *Old Favours (home-gated draw):* name one home region at
  setup; while there, start each turn drawing 1 ingredient from any region's market (free); away, the engine
  is dark. Flaw-free. *(V7-M rework — replaces the old home −1 / +1-away discount; balance reopened, re-sim.
  **#1 paid-consultant item:** must read as warm civic affection, never patronage.)*
- **The Homebody 媽寶 (Ma-pó)** — *sole Travel-sourcer:* on a Travel, draw the top **2** of the region you
  LEFT and keep both (event whiffs). Flaw-free.
- **The Big Eater 大胃王 (Tuā-uī-ông)** — *Bottomless:* on a Market Run, keep all **3** (may Greedy-Grab a 4th →
  return 1 follower). Flaw: hazards fire **twice** on her Market Run. **She/her.**
- **The Influencer 網紅 (Bāng-âng)** — *Going Viral:* owns **8** follower meeples (the field owns 6) — a
  deeper crowd. Flaw: takes the **last** seat each round.
- **The Big Boss 老大 (Lāu-tuā)** — *Everybody Knows 老大:* **margin dial N=1** — wins a contested stall
  unless a rival exceeds his committed followers by N or more (N=1 → he **wins ties**). Flaw-free. A
  PLAYFUL, warm fixer — **never** menacing or a triad/gang caricature; **consultant-gated** portrayal.
- **The Globetrotter 阿嬤 (A-má)** — *敬老卡 Elder Pass:* Travel reaches ANY region in one action; immune to
  Scheduled Maintenance. Each Travel-anywhere costs 1 follower to supply. Flaw-free; spry / dignified,
  age-as-superpower — never frail.

## Win condition & scoring
**TWO-TRACK VP.** At game end score **two ways**: the **`vp` printed on every vendor you won (0–11 each —
cheap day seeds score low, 1–2; scarce night trophies score high, 5–11; ★ apex 10–11)** **plus** the
**full value of every tour (Booking) you completed (3–11 each)**. Completed tours carry the bulk of a
winner's score and remain the main path to victory (sim N=400: booking-share ~67–75% vs vendor-share
~25–33%); the high-VP night trophies are the vendor track's payoff, but a vendor-only hoard is structurally
dominated (vendor-only hoarder deeply sub-fair at every count — ~12–27% win share). **Cancelled Bookings =
flat −1 each** (any Booking still unfinished in hand at the last train is cancelled too). Followers score
nothing. **Top Agent** = most points; ties break to most vendors → most regions covered → fewest cancelled
Bookings. §14 invariant: `vp = ingredient_cost + min_followers − 2`. Detail: `followers-meeples-redesign.md`
§14; vendor VP in `components/vendors.csv`, Booking values in `components/bookings.csv`.
*(⚠ see the Currency flags at the top — `rules-draft.md` §1/§9 + `names.md` §3 still read tickets-only.)*

## Ingredient taxonomy
- **MONO 6-type SHIPS** — 肉 Meat · 茶 Tea · 海鮮 Seafood · 糧 Pantry · 糖 Sugar · 菜 Vegetables (each card
  art a MIX of real examples). Balance-clean at every count (CD decision 1A, N=400 + N=300 re-smoke).
- **8-type split PARKED** — a non-destructive, flag-gated experimental branch (`SPLIT_TAXONOMY`, default OFF):
  Pantry → Rice 米 / Noodles 麵 and Sugar → Sugar 糖 / Pearls 珍珠 (`*-split.csv` stay in the tree, unused by
  the ship config). Revisit only if a human playtest says the in-region keep-2 choice is genuinely missed;
  carried a residual 5–6p hoarder tilt in keep-2 (its own payoff mode). Full rationale: `design/ingredient-taxonomy.md`.

## Rules summary
Turn = one of **Market Run / Convenience Store / Travel / Promote / Sign Up / Book**; Larder cap 7; Greedy Grab
(keep 1 extra → return 1 follower). **Followers are committed meeples on vendors** (public; region-gated;
everyone can pile on). To **Sign Up**: be with the vendor, hold the **biggest crowd** (strict plurality; tie
blocks — 老大 wins ties), pay its ingredients (− region discounts). Ingredient decks are face-down; events
fire by scope on a Market Run + Convenience Store (Travel whiffs). **Day → Night:** at **dusk** (day vendors gone)
bring the night vendors + markets online, deal a fresh night Booking row; keep your Larder and Bookings; any
unfinished ☀ day Booking is cancelled. At the **last train** (night vendors gone) finish the round → score.
**The clock is vendor depletion + the Closing-Time die.** Full teach order → `design/rules-draft.md`.

## Open questions & risks
- ✅ **Spine — LOCKED (V7-M):** area-majority follower fight + region ingredient sourcing + multi-ingredient
  recipes + vendor-depletion clock + Closing-Time die + two-track VP + Bookings/Pot-Luck. Sim-validated N=400.
- ⚠️ **RISK #1 (make-or-break, table-only) — is the area-majority fight fun/tense, not degenerate?** Sim
  contested_frac ~24–27% at multiplayer, but *feel* is unmeasurable in sim → the #1 table question.
- ⚠️ **RISK #2 — do the six characters band with no crusher, and is the Old Councillor rework balanced?**
  The V7-M kit reworks (Old Councillor home-gated draw, etc.) reopened balance → carried to the re-sim / table.
- ⚠️ **Showcase (orphan) tours** — the two premium themed crawls (bubble-tea pilgrimage, Dihua crawl) land
  ~40% completion / ~57–62% orphan = parity with the game's healthy pair tours (CD accepted, decision 2A-A);
  a premium themed crawl *should* be a ~40% gamble. Table watch.
- ⚠️ **Downtime at 5–6p** — the key high-count risk; snappy turns + simultaneous consideration to test.
- ⚠️ **WEIGHT / table-state:** within budget (weight 2.2/2.5; rulebook 2262/2280), but felt weight is in
  table-state (vendor slots + Booking row + follower pools + the die). A live FTUE check.
- **Currency flags:** see the top-of-file block — two-track-vs-tickets-only rulebook lag, the min-followers
  floor not yet in `rules-draft.md` §5, and the character-kit drift in `names.md`/`v7-plan.md`.
- **Sensitivity:** a **real place & culture (Taiwan)** — the **East region is Indigenous-forward** (E01 竹筒飯,
  E04 石板烤肉 consultant-gated), "Sign Up" / 老大 / 里長伯 warmth rails, 繁體 + Tâi-lô discipline. Owned by
  `bg-theme` + `bg-publishing`; **paid Taiwanese cultural + language consultant before art/print.** No AI final art.

## Status by stage
- [x] Ideation · [x] Research · [x] Exploration
- [x] **Design ← V7-M CLOSED:** the multiplayer area-majority core, the day-engine / night-payoff vendor
  economy, the vendor-depletion clock + per-phase Closing-Time die (day cadence L2@3p / L3@4–6p, night every
  round), two-track VP, agnostic tours + Pot-Luck, the 6-type mono taxonomy, and the six V7-M character kits —
  sim-validated N=400 (engine forms, tours lead, hoarder sub-fair, stall killed at every count).
- [x] **Development ← DONE (bg-developer):** component data built to V7-M (30 vendors, 45 bookings, 6-type
  mono ingredients + the parked split branch, ~52 events, six character mats, Closing-Time die + track).
  Linter 0 errors; `make.sh` renders; prototype kit (Screentop sheets + A4/A3 print-and-play + rulebook) current in `exports/`.
- [ ] Prototype (Screentop.gg / PnP) — kit shipped; ready for the table
- [ ] Playtesting (human, 3–4p focus — is the area-majority fight fun? do the six kits band? do tours dominate as intended?)
- [ ] Marketing · [ ] Publishing / IP · [ ] Production (deferred — Screentop-first)

## Links
- Current rules: `design/rules-draft.md` · Design canon: `design/followers-meeples-redesign.md` (V7-M) +
  `design/design-doc.md` (§15 events, §17 clock) · Ingredient taxonomy: `design/ingredient-taxonomy.md`
- Identity: `identity.md` · Names & terms: `names.md` · Voice: `prose-identity.md` · Decisions: `decision-log.md`
- History: `archive/game-bible-history.md` · `archive/identity-history.md` · `archive/decision-log-pre-v7.md`
