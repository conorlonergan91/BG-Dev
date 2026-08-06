# Travel Agents: Taiwan — Design Doc (v4 · the Buzz-majority / Acts rework)

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.
**v4 = a substantial CD-directed rework of the v3.1 vendor-courting engine** (decision-log TOP entry,
2026-08-06). Slug `travel-agents`. Working keyword **"Bribe"** replaces **Court** throughout — `bg-theme`
owns the final name (must stay cheeky-warm, not corrupt). Where this doc says *Bribe / Promote / Act /
Lunch-Box Granny*, treat them as working labels the parallel `bg-theme` pass will finalize.

> **The v4 spine (what makes it *this* rework):** the private Buzz currency becomes a **committed,
> public, contested majority placed ON each vendor** (Arcs-Court-like) — you must be *on-site* to pile
> Buzz on a prize vendor, both agents can pile onto the same one, and you only **win it by out-hyping
> your rival by ≥2 while holding its ingredients**. The market becomes a **face-down push-your-luck deck**
> (draw 3, keep 2; hazards fire), the linear Season counter becomes **escalating Acts** (Stalls → Eateries
> → Marquee — vendors get harder as the game goes on), and events lean **hazard-heavy** inside the market
> decks. **Extract and Poach are cut.** The recipes-by-region ingredient engine, the discount ramp, the
> three scoring vectors + secret mission, and the 5 characters (Conductor re-themed to a **lunch-box
> granny**) all **carry over**.

Sensitivity rails bind throughout (`identity.md` §Sensitivity): winning a vendor reads as **the vendor
choosing the agent who hyped them best** — never an agent seizing, cornering, or corrupting a place.
"Bribe" is a **comedic** slip-the-auntie-a-little-extra-buzz caper, not real corruption (a `bg-theme`
naming/tone flag — below).

> **One-line frame:** two rival travel agents race across Taiwan through **three escalating Acts** —
> source real regional ingredients from face-down region **markets** (push-your-luck: a typhoon may be the
> next card), and pile **Buzz** onto the island's vendors to **win them over** (you must be on-site, and
> you must out-hype your rival). Each vendor won is an engine piece (a compounding ingredient discount)
> climbing **Prestige**, **Reputation** and **Coverage** toward a hidden **signature tour**. Best tour is
> **Top Agent**.

---

## What changed from v3.1 (the honest ledger for `bg-elegance`)

This is a **real systems rework**, not a re-cost. Several changes interlock. Honest ± ledger:

| Cut / banked (−) | Added / spent (+) |
|---|---|
| **Private Buzz currency** + the passive "undiscountable-Buzz tax" brake | **Buzz-majority on vendors** — committed, public, region-gated, contested (the headline spend; the new interactive brake) |
| **Stock Up** (take 2 from a face-up Market) | **Visit the Local Market** — draw 3 / keep 2 from a face-down region **deck**, hazards fire (the push-your-luck spine) |
| "**pantry available anywhere**" + the pantry ingredient type | **Convenience Store** — a separate action: top card of ANY region's deck, blind (the flexible valve) |
| **Extract** action (player end-trigger) | **Acts** — the game advances/ends by act conditions; **board escalates** (Stalls → Eateries → Marquee) |
| **The 16-Season linear counter** | (folded into the Act-advance condition) |
| **The Poach** (conditional steal) | (cut — the Buzz-majority contest *is* the co-location interaction now) |
| **Event tiles** salted in a finite face-up supply, boon-skewed 60/40 | **Events as cards inside the market decks**, **hazard-leaning ~55–60%** (fire when you Visit) |
| **Retired Conductor** character | **Lunch-Box Granny** (draw the *leaving* region on Travel) |

**Honest weight call (stated up front, expanded in *Complexity budget*):** v4 is a **genuine weight
increase**. Pre-trim I estimate **~2.5–2.6 — at or slightly over the 2.5 ceiling** — driven almost
entirely by the **Buzz-majority system** (the CD's headline ask). I bank what I can (Extract cut, Poach
cut, pantry folded, Season→Acts, event tiles→market cards, **component types 7→~6**). To hold **≤2.5** I
recommend **one further trim** (Coverage → mission-only). If the CD wants to keep every track, this needs a
**conscious ceiling raise to ~2.6** — defensible next to Arcs (~3.0) / Splendor Duel+ (~2.3–2.5).
`bg-elegance` guards; see the decision set.

---

## Design goals

- **A tight two-player engine with a real *fight* at its centre.** v3.1's interaction was mostly "race to
  pay first"; v4's Buzz-majority makes each prize vendor a **public, escalating, on-site tug-of-war** — the
  Arcs-Court tension the CD asked for, in a lighter frame.
- **Target weight ~2.4–2.5, ceiling 2.5 (pending the raise decision).** Depth from the Buzz contest +
  push-your-luck market + Acts; complexity banked by cutting Extract/Poach/pantry.
- **2-player first.** The duel is the design home; the Buzz-majority is sharpest as a two-person
  tug-of-war. 3–4p is a scaling delta (majority = ≥2 over the *highest* rival).
- **Aesthetics (locked, `identity.md`):** **Discovery (lead)** — face-down markets and escalating acts
  keep revealing the island; **Fellowship** — the shared, comedic fight over a prize vendor and the market
  drama; **Challenge** — the routing + two-input + when-do-I-commit puzzle.
- **The meaningful decision every turn:** *do I dig the market for the specialty I need (and risk a
  typhoon), grab a safe blind card at the convenience store, travel on, pile more Buzz onto the vendor I'm
  fighting for — or close the Bribe now before my rival out-hypes me?* No forced move.
- **Taiwan does real work** (unchanged): the region↔ingredient web is real food geography — rename the
  setting and the recipes break. Dishes named Tâi-lô + 繁體, never mangled.
- **Design the make-or-break risks out:** **(a)** the Buzz contest is fun/tense, not a swingy
  slap-fight or a "never commit early, always snipe" degenerate; **(b)** no economy runaway past the acts;
  **(c)** the push-your-luck market is spicy, not punishing; **(d)** movement still spreads across regions.

---

## Core loop (detailed)

A turn is **one action**; short turns, low downtime. Each cycle you weigh three questions: *which input am
I short — the region-specific ingredients a vendor needs, or the Buzz majority on it? am I on-site to act
on it? and is now the moment to close before my rival swoops?*

1. **Read the board.** The **Vendor Board** shows this Act's vendors (each with its ingredient cost, its
   **region icon**, its **Prestige/Rep/perk**, and **the Buzz both agents have piled on it**). Your secret
   **signature mission** points at a vendor pattern worth **+7**. The four **region market decks** are
   face-down (you know each region's two specialties + that hazards lurk). Your **Prestige** and
   **Reputation** markers show two vectors live; the **Act track** shows how close this act is to turning.
2. **Take one action** (see *Actions*): **Visit the Local Market**, **Convenience Store**, **Travel**,
   **Promote**, or **Bribe a Vendor**.
3. **Sourcing is a gamble now.** *Visit the Local Market* (in your region) flips the top 3 of that region's
   deck: any **hazard** fires on the spot (a typhoon, a sold-out sign), then you keep up to **2** of the
   **specialties** you turned up. *Convenience Store* and *Travel* each take a single blind top card
   (specialty → keep it; event → the shelf was bare, nothing fires).
4. **Buzz is a public fight.** *Promote* places Buzz from the supply **onto vendor(s) in your current
   region** — committed, visible, and your rival can pile onto the same vendor. You can only close a
   **Bribe** on a vendor when you're **in its region**, hold **≥2 more Buzz on it than your rival**, and
   can **pay its ingredients** (minus your discounts). Winning it clears all its Buzz back to the supply,
   scores you Prestige + Rep + its perk + a Coverage tick, and **advances the Act** toward its turn.
5. **Acts escalate and end the game.** When enough vendors have been won this act, the board **sweeps and
   re-stocks from the next, harder tier** (Stalls → Eateries → Marquee). When the **final Act's** condition
   is met → finish the round + one full round → **reveal missions** → score. No Extract; the acts pace and
   end the game.

The loop compounds **legibly and with a brake**: each vendor makes a *class* of future vendors cheaper in
**ingredients** (the ramp) — but every vendor still demands you **win an undiscounted, region-gated,
contested Buzz majority**, one Promote at a time, on-site. That Buzz fight is the primary anti-runaway
brake (see *The Buzz-majority system* and *Economy*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** — 4 regions on a ring: **North 北 – Central 中 – South 南 – East 東**; an
  **HSR** spine links North↔South down the west coast. The board carries the **Act track**, the **VP
  (Prestige) track**, the **Reputation track**, the **Vendor Board** slots, and a face-down **market deck**
  zone per region.
- Build the **four region market decks**: each = its **two specialty ingredient cards** (several copies
  each) **+ 3–4 event cards** (hazard-leaning), shuffled face-down. (No pantry pile — the Convenience Store
  replaces it.)
- Sort the **Vendor deck** into three Act tiers — **Act 1 Stalls / Act 2 Eateries / Act 3 Marquee**;
  shuffle each. Deal the **Act 1** vendors to fill the Board (2p: **5 slots**). Set the **Act track** to
  Act 1.
- Form the **Buzz** supply (open pool; **~24 at 2p** — see *Economy*).
- Each agent: choose/deal an **Agent Character** (ability + flaw, public); take a pawn (start on opposite
  regions — one North, one South); place **VP** and **Rep** markers at 0; take an empty tour + Larder area.
  The Larder (ingredient cards) sits **face-up** all game. Deal **3 Mission cards, secretly keep 1** (your
  signature mission, +7), return 2 unseen.

**A turn = choose ONE action:** **Visit the Local Market · Convenience Store · Travel · Promote · Bribe a
Vendor.** Then if your Larder exceeds **7** ingredients, discard down to 7 (to that region's market
discard). Play passes clockwise (the Influencer's flaw = goes last; see *Characters*).

**End-trigger:** when the **final Act (Act 3)** advance-condition is met (see *Acts & end-game*), **finish
the current round** (equal turns for all), play **one more full round**, then **reveal signature missions**
and score. A fair, unswingy wind-down; the extra full round guarantees the trailing player answers the
trigger. **Reputation-top scores its bonus but does not end the game** (carried from v3.1's sim-fix).

Target length: **~40–45 min at 2p**, roughly **22–26 turns per player**, **~7–8 vendors won per player**.

---

## Actions

A turn = ONE of five. Each is simple; the depth is in *when* and *where*.

| Action | Where | Effect | Notes |
|--------|-------|--------|-------|
| **Visit the Local Market** | your current region | Reveal the top **3** cards of this region's market deck. Resolve **any event** revealed immediately (**hazards fire**), discard them. Keep up to **2** of the revealed **specialty** cards (to your Larder); discard the rest. | The ingredient workhorse **and** the push-your-luck spine. More hazards in the deck = more chance a flip both hurts you and eats an ingredient slot. |
| **Convenience Store** | anywhere | Reveal the **top 1** card of **any one** region's market deck. Specialty → take it. Event → discard it, **nothing fires** ("shelf was picked clean"). | The flexible, reliable-ish valve: sourcing from *any* region without travelling, but only 1 blind card and it can whiff. Replaces the old pantry. |
| **Travel** | to an adjacent region | Move your Agent to an **adjacent** region (HSR: North↔South counts adjacent); then reveal the **top 1** card of the **arriving** region's deck (specialty → take it; event → whiff, nothing fires). | Never a dead turn — you (usually) arrive with something. *Lunch-Box Granny draws the region she LEFT instead.* |
| **Promote** | your current region | Place **2 Buzz** from the supply onto **vendor(s) in your current region** (2 on one, or 1 on each of two). Buzz stays on the card, public; the rival may also Buzz the same vendor. | The Buzz-placement action. Region-gated — you can only hype vendors you're standing with. *Influencer places 3; Lunch-Box Granny places 1.* |
| **Bribe a Vendor** | in the vendor's region | Choose a Board vendor **in your current region** on which you hold **≥2 more Buzz than your rival**; **pay its ingredients** (− your region discounts, floored at 0). Take it to your tour → gain **Prestige** (VP live), a **Rep** bump, its **perk** (usually a region discount icon), and a **Coverage** tick if a new region. **All Buzz on it (yours + rival's) returns to the supply.** Refill the Board slot from the current Act deck; **advance the Act track +1**; the vendor is locked from the rival. | The scoring + engine beat, now gated by **position + majority + ingredients**. The only action that advances the Act. |

**Five actions, no conditional sixth.** (Poach is **cut** — see *Interaction*.) Every turn has multiple
live options with real trade-offs: dig the market (risk), grab a safe blind card, reposition + draw, pile
Buzz onto a contested prize, or close a Bribe. No forced/obvious move.

**Two rules stated once, to keep the ruleset small:**
- **Hazards fire only when you Visit the Local Market.** A hazard revealed by *Travel* or the *Convenience
  Store* (single blind draws) is simply discarded — "that shelf was bare," no ingredient, nothing fires.
  (Protects the travel engine; makes *Visit* the true push-your-luck.)
- **Buzz lives only in the supply or ON a vendor.** There is no private Buzz pool. You never "hold" Buzz;
  you place it, and it is either won-and-cleared or fizzled-and-cleared.

---

## The market decks & events (the push-your-luck sourcing layer)

- **Four face-down region decks.** Each region's deck = its **two specialty types** (several copies) **+
  3–4 event cards**, shuffled. You know each region's specialties (printed on the board) and that hazards
  lurk — you don't know the order. *(This replaces v3.1's telegraphed face-up Market: sourcing is now
  blind and opted-into — the deliberate variance the CD wants.)*
- **Visit the Local Market** is the risk/reward: 3 flips, hazards fire, keep 2 specialties. If two of your
  three flips are events, you keep only 1 (or 0) specialty **and** eat the hazard effects — the genuine
  push-your-luck. **Convenience Store / Travel** are the low-variance single blind draws (whiff, don't
  fire).
- **Events lean hazard (~55–60% hazard / ~40–45% boon across the pooled decks)** — the CD's "cut the boon
  skew." They stay **warm-comedic** and **tax-not-destroy** (a hazard delays, reroutes, or taxes tempo;
  it never removes an ingredient you already hold or a whole turn). The boon minority keeps a Visit from
  being pure dread and preserves the "living island" warmth.
- **Where events sit:** hazards are **per-region cards in that region's deck** (a typhoon in the coastal
  South/East decks, plum rains in Central, scooter gridlock in the North). A few **table-wide** events
  (e.g. a food-blogger frenzy, an island-wide typhoon day) are cards whose *effect* reaches everyone but
  still live in a region deck and fire when that region is Visited. `bg-developer` rebuilds `events.csv`
  to this composition (drop the boon skew; re-home tiles into the four decks).
- **Recycling:** ingredient cards flow deck → Larder → (spent on a Bribe) → that region's discard; when a
  deck runs dry, reshuffle its discard (fired hazards return too, so the pressure persists). A deck running
  dry mid-act is a natural scarcity beat.

**Event starter set (~14; secular, hazard-leaning, warm-comedic; wording via the consultant before lock).**
Re-uses the v3.1 comedy set, re-weighted. Hazards (the majority): **颱風假 Typhoon Day** (wash + refill the
coastal decks' next reveals; table-wide catch-up sop), **梅雨 Plum Rains** (your Visit this turn keeps 1
fewer), **完售 Sold Out** (discard the next specialty in this deck), **機車陣 Scooter Gridlock** (your next
Travel arrives empty), **客滿 Fully Booked** (shuffle this region's deck — reset the run), plus new
per-region hazards `bg-developer` fleshes out so every deck carries ~2 hazards. Boons (the minority):
**芒果季 Mango Season**, **珍奶節 Bubble-Tea Festival**, **臭豆腐大挑戰 Stinky-Tofu Dare** (opt-in
push-your-luck), **再吃一點啦 The Aunty Insists**, **網紅來了 Food Blogger** (table-wide next-Promote +1
Buzz). *Reserve knob:* if blind decks feel too swingy at the table, add a **"brewing" telegraph** (the top
card of each region deck is face-up, so you see the next flip before you Visit) — ~1 rule, restores
preview agency.

---

## The Buzz-majority system (the headline rework)

This is the big new thing. Read it as the Arcs-Court "agents on a card" mechanic, re-skinned to **hype on a
vendor** and lightened for a 2p duel.

**The rules, plainly:**
1. **Buzz is committed, public, and region-gated.** **Promote** places **2 Buzz** from the supply onto one
   or two vendors **in your current region**. Buzz sits on the vendor card, face-up, for anyone to see.
   **Both agents may pile Buzz on the same vendor.**
2. **Winning = ingredients + a ≥2 majority + presence.** To **Bribe** a vendor you must be **in its
   region**, hold **at least 2 more Buzz on it than your rival**, and **pay its ingredient cost** (− region
   discounts). The majority is checked at the instant you pay.
3. **On a win, all Buzz on that vendor clears to the supply** — winner's and loser's alike. The winner's
   hype "paid off" (spent); the loser's hype "fizzled" (the vendor chose the rival). **Neither player gets
   Buzz back into a private pool** (there isn't one). The loser lost **only tempo** — the actions they
   spent promoting — never ingredients or VP. **"Outraced, not robbed"** holds mechanically and
   thematically (the vendor simply chose the agent who wooed them best).
4. **Committing early is a risk *and* a weapon.** Every Buzz you place raises the bar a rival must clear to
   swoop (they need ≥2 over *your* current pile) — so early commitment can price a rival out. But Buzz
   placed is an action **not** spent sourcing the ingredients you also need — over-invest and you can't pay
   the Bribe when the moment comes, and a rival with the ingredients ready can force the close.
5. **No private hoarding, no windfalls.** Because Buzz never enters a private pool and clears on every
   win, it **recycles** — a modest supply (~24 at 2p) sustains the whole game and keeps every placement a
   real, scarce choice.

**Why this is the new anti-runaway brake (replacing the undiscountable-Buzz tax).** Every vendor —
however cheap its ingredients become as your discount ramp grows — still demands that you **win a
contested, region-gated, undiscounted Buzz majority, one Promote at a time, on-site**. The ramp cheapens
only the *ingredient* half; the Buzz fight never ramps and can be **actively raised by your rival**. So the
courting *rate* stays capped at roughly **1 vendor per 2–3 turns** even fully ramped (a Promote-or-two + a
Bribe + the on-site travel), and a fast/wide leader can't simply buy the board — each win is a fight they
can be made to overpay for. This is a **stronger, interactive** brake than v3.1's passive tax.

**The escalation question (a real risk to sim).** Two agents can keep piling Buzz on the same vendor,
each needing ≥2 over the other — a bidding war. Three things cap it: **(a)** you can only *win* with the
ingredients in hand and while on-site, so the war ends the instant one agent is ready to close;
**(b)** Buzz supply is finite (~24) — you physically can't over-stack every vendor; **(c)** every Buzz
placed is an action stolen from sourcing, so a runaway bidder starves their own ingredient half.
Nonetheless — *is the war fun or a slap-fight?* is **Riskiest Assumption #1** (below).

**Reconciliation with Poach.** In v3.1 Poach was the co-location swipe. In v4, **co-location is the centre
of the game** (both agents converge on contested regions to fight over vendors), so a separate "steal an
ingredient because you share a region" action would (a) fire constantly and tip griefy, and (b) duplicate
the interaction the Buzz contest already delivers, far richer. **Poach is cut.** (Banks ~0.1 weight; see
the decision set if the CD wants it kept, re-scoped.)

---

## Vendors — the engine cards (tiered by Act)

A **Vendor** is a stall/cook who agrees to feature on your tour once you've wooed them (ingredients +
winning Buzz majority). Three tiers, now mapped to the **three Acts** so the board escalates over the game:

| Act / Tier | ~Count in deck | Ingredient cost | Buzz to win (uncontested) | Prestige (VP) | Rep | Perk |
|------|-------:|-----------------|--------------:|--------------:|----:|------|
| **Act 1 · Stalls** | ~11 | **1–2** (in-region) | ≥2 | **1** | **+1** | its **region discount icon** (the base ramp) |
| **Act 2 · Eateries** | ~8 | **2–3** (1 cross-region) | ≥2 | **3** | **+2** | region icon **+ one** of {Promote +1 Buzz · once/turn treat 1 specialty as any specialty when Bribing · +1 Rep on each future Bribe} |
| **Act 3 · Marquee** | ~6 | **3–4** (2–3 regions) | ≥2 (but heavily contested) | **5–6** | **+2/+3** | a **strong** perk: a **wild region icon** · **or** Buzz-reach (place Buzz on adjacent-region vendors too) · **or** counts as **2** region icons · **or** +2 Rep on Bribing |

> **"Buzz to win ≥2" is the *floor* (uncontested).** The real cost of a marquee is that your rival is
> fighting you for it — the ≥2 majority against *their* pile is what makes late vendors hard, not a bigger
> printed number. This is why the board escalates on **contest intensity + ingredient/region breadth +
> Prestige**, not on ever-larger Buzz numbers (which would just drain the supply).

**The discount ramp (kept, unchanged in spirit).** Each secured vendor carries a **region icon** (N/C/S/E,
or wild). Holding *k* vendors with the X-icon reduces the **X-region ingredient** portion of any future
vendor by *k* (floored at 0). Early vendors are dear; each one signed makes a *class* of future vendors
cheaper in ingredients. **Buzz is never reduced** — the brake.

**Re-cost note for `bg-developer` (pantry removed).** v3.1 costs used `pantry` filler (e.g. T1 = "1
specialty + pantry"). **Pantry is cut** — re-cost the 25 vendors to **named specialties only**, preserving
the v3.1 *movement rebalance* (anchor every vendor in its own icon-region; ~40% carry a cross-region link;
cap pork ≤5 / rice ≤5; every specialty on ≥3 vendors). T1 = **1 in-region specialty** (Buzz ≥2); some T1 =
**2 in-region**. Keep every real dish real (anchor true; cross-link = "the regional leg you bring";
consultant-checked). Re-home the two orphaned **wild_pantry** perks (V08b 肉圓, V10 凍頂烏龍) to the new
**wild_specialty** perk (once/turn treat 1 specialty as any). Re-tier the deck into the three Act decks
(the existing T1/T2/T3 split maps cleanly to Act 1/2/3).

> **Sensitivity (binds — `identity.md`):** East specialties draw on **Indigenous** cuisines — generic,
> respectful labels, consultant before art/print. Taiwan as itself; Traditional characters; Tâi-lô + 繁體,
> never mangled. The "Bribe" keyword must read as **warm comedy** (hype + goodwill), never corruption —
> a `bg-theme` flag.

---

## Acts & end-game (replaces the Season counter)

**Three Acts**, each escalating the Vendor Board:
- **Act 1 — Stalls (the easy season).** Cheap vendors, low contest. This is where you **build your discount
  ramp** and stake early region positions. Board dealt from the Stalls deck.
- **Act 2 — Eateries (the middle).** Pricier, cross-region, richer perks. The ramp starts paying off.
- **Act 3 — Marquee (the finale).** The big names — expensive, multi-region, fiercely contested. Where the
  game is won or lost.

**Advancing an Act.** An Act advances when **N vendors have been won table-wide during that Act** (the
recommended trigger — see the decision set for alternatives). At 2p, **N ≈ 5 per act** (≈ 15 total wins ≈
7–8 per player across three acts). On advance: **sweep any unwon vendors** of the current tier off the
Board, deal fresh from the next Act's deck, and move the **Act track** to the new act. Any Buzz sitting on a
swept vendor **returns to the supply** (the season moved on).

**Why sweeping-on-advance is the escalation.** Cheap ramp vendors are only available *in Act 1* — grab
your discount icons early or fall behind on the ingredient half (the multi-track scoring keeps a laggard
alive via Rep / breadth / the hidden +7). This creates a clean **build-then-cash arc** and a real
tempo/pacing pressure that replaces Extract's "wrap while ahead."

**Ending the game.** When **Act 3's** advance-condition is met (its N-th win, or its deck exhausted as a
backstop) → **finish the current round + one more full round → reveal missions → score.** No Extract, no
player end-trigger; the acts do the pacing.

**The built-in catch-up co-brake (carried from v3.1's Season logic).** Because *table-wide wins* advance
the acts, a **fast** winner **hurries the end** they'd need to keep winning, while a **tall/slow** player
(fewer, bigger vendors) leaves the threshold low and gets **more turns to reach parity**. Gentle, not
leader-bashing.

---

## Missions — the secret +7 (draw-3-keep-1, unchanged)

Deal **3**, secretly **keep 1**, discard 2 unseen. A mission is a **secret vendor pattern** worth **+7 at
scoring** (binary). Starter pool (variety on purpose): *"3 vendors in the South"* · *"a vendor in all 4
regions"* (grand tour) · *"3 Act-1 Stalls"* · *"2 Act-3 Marquee vendors"* · *"a vendor of each of 3 named
cuisines"* · *"vendors totalling ≥ 18 Prestige"* (go tall) · *"5 vendors, any"* · *"a Marquee + two Stalls
of its feeder regions."* Draw-3-keep-1 (not a random deal) lets you steer your character/track synergy on
purpose and launders the char×mission balance problem (you *choose* the combo; the opponent sees your
public character and contests). *If Coverage is cut to mission-only (weight decision), the "all 4 regions"
mission absorbs the breadth vector.*

---

## Economy & math

The Buzz-majority + push-your-luck market are the make-or-break. Numbers below are first-pass — the sim's
job is to attack them (see *Riskiest assumptions*).

**Income vs spend (per action):**

| Action | Yield (EV) |
|--------|-------|
| Visit the Local Market | +~1.3–1.7 specialties (region-gated) − hazard exposure |
| Convenience Store | +~0.6–0.8 specialty (blind, any region, can whiff) |
| Travel | +~0.7 specialty + reposition |
| Promote | +2 Buzz **onto the board** (no private gain — a positional investment) |
| Bribe | − ingredients (− discount); win vendor → +Prestige +Rep +perk +Coverage; clears the vendor's Buzz |

**Cost of a vendor, in actions (the real currency).** Uncontested, a vendor costs roughly: **source its
ingredients** (1–3 Visits/draws, fewer as the ramp grows) **+ ≥1 Promote** (to reach the ≥2 floor) **+ the
Bribe** — call it **~3–4 actions early, ~2–3 actions ramped.** Contested, add a Promote or two to
out-stack the rival. So the **courting rate** sits at **~1 vendor / 2–3 turns** and never approaches
1/turn — the ramp accelerates the ingredient half but the Buzz fight is a fixed, contestable floor.

**Buzz supply sizing (2p ≈ 24).** At any moment ~2–4 vendors carry 2–6 Buzz each (≈ 8–16 committed), the
rest in supply; wins recycle it. If ~24 proves too tight (players can't contest) or too loose (no
scarcity), the supply size is the first tuning knob. Scales with player count (≈ +8–10 per extra player).

**Balance assumptions (attack these):**
1. **The binding constraint alternates** — a feature. *Early:* ingredients bind (can I dig the specialty
   out of a hazard-y deck?). *Late:* the ramp trivialises ingredients, so **the Buzz fight + position**
   bind (can I out-hype and be on-site before my rival closes?). Keeps decisions fresh.
2. **VP/turn stays flat-ish across tiers** (~1.1–1.9) so no Act's vendors are an auto-win; Act 1 pays
   **indirectly** (its cheap icons make everything else cheaper — the engine investment), Act 3 pays in
   Prestige + mission synergy, not raw rate.
3. **Larder cap 7** (ingredient cards) forces the source→spend rhythm.
4. **Target 2p winner ~32–40 total VP.** Rough split: vendors' Prestige ~20–24 + Reputation end-VP ~4–6 +
   Coverage ~2–9 *(if kept)* + signature mission 0/**7**.

---

## Scoring / win condition — "Top Agent"

Hybrid multi-track: tracks pay bonuses, **highest total VP wins** (no sudden-death — warm, and a trailing
player always has a live second vector). At game end each agent totals:
1. **Tour Prestige (VP)** — sum of your vendors' stars (Stalls 1 / Eateries 3 / Marquee 5–6). *(Live on the
   VP track.)* — the **tall / prestige** line.
2. **Reputation** — end-VP by final marker position: **3→+2 · 6→+4 · 9→+6 · 12 (max)→+9.** Climbed by
   Bribing (each vendor's printed Rep). *(Live on the Rep track.)* — the **reputation-climb** line.
   *(Milestone perks passing 3/6/9 are a weight-decision — see the trim list.)*
3. **Region-Coverage** — end-game breadth bonus for distinct regions among your vendors: **2→2 · 3→5 ·
   4→9.** *(Weight decision: fold into mission-only — see the decision set. The v4 region-gating already
   forces travel, making an explicit Coverage bonus partly redundant.)* — the **grand-tour** line.
4. **Secret signature mission** — **+7 if completed** (revealed now), else 0. *(The one hidden vector.)*

Highest total is **Top Agent**. **Tiebreak:** highest Reputation, then most vendors, then most regions.

**Designing out a dominant track (the tracks pull against each other).** Prestige rewards *few, big*
vendors; the discount ramp rewards *many, doubled-up in a couple of regions*; Coverage/breadth rewards
*one in each region*; Rep rewards *steady Bribing*. You cannot max ramp-concentration **and** breadth at
once. The v4 twist: **the Buzz fight injects opponent-dependence** — the "best line" shifts with where your
rival commits, so no opening is statically solved. (Sim probe #2.)

---

## Randomness

- **Input randomness (the bulk):** the Vendor Board reveal per act, the **face-down market decks**, the
  Mission draw (mitigated by draw-3-keep-1), the deck orders. The market is now **blind** (v3.1's face-up
  Market is gone) — a deliberate increase in variance to feed the push-your-luck.
- **Bounded output randomness (the new spice):** the **Visit** flip resolves *after* you chose to dig.
  Bounded to *spice, not decide*: you **keep 2 of 3**, hazards are **tax-not-destroy**, deck composition is
  known, and the **Convenience Store** (safe blind single draw) + **Travel** are the low-variance valves.
  Digging is opted-into push-your-luck.
- **The Buzz fight and the Bribe are pure open-information** — no dice, no post-Bribe luck. The skill of
  the engine stays legible; the luck lives only in what the market decks hand you.
- **One hidden-information hook only:** your secret signature mission. Larder, both tours, all Buzz on the
  board, and both tracks are open. No deduction engine.

---

## Interaction & tension

**Direct (the new spine — far more interactive than v3.1):**
- **The Buzz-majority tug-of-war.** The public, escalating, on-site fight over each prize vendor (see *The
  Buzz-majority system*). This is the Arcs-Court social tension the CD wants: you *see* your rival's Buzz
  piling on the seafood marquee and must decide to out-commit, race them to the ingredients, or concede and
  take a different vendor. **Anti-resentment:** a lost fight costs only tempo (your Buzz fizzles, you keep
  every ingredient) and reads as *the vendor chose them* — **"outraced, not robbed."**
- **Positional denial.** Being *on-site* gates Promote and Bribe, so simply occupying a contested region
  and stacking Buzz is a way to pressure a vendor and read your rival's intentions.
- **Market scarcity.** A region deck running dry (both agents digging the same market) is a natural
  reroute pressure.

**Catch-up vs runaway (designed):**
- **Against runaway:** the **contested Buzz floor** (every win is an undiscounted on-site fight the rival
  can force you to overpay), **diminishing returns** on cheap vendors, **finite Buzz supply**, and the
  **act-advance co-brake** (fast winning hurries the end).
- **For catch-up (gentle):** the **act-advance co-brake** (a tall/slow player gets more turns), the
  **multi-track structure** (a trailing player always has a live second vector), one **table-wide hazard**
  with a leader-excluding sop (Typhoon Day gives Buzz to everyone *except* the Prestige leader), and the
  hidden **+7**.

**Fellowship** is carried by the comedic shared fight over a prize vendor ("you did *not* just out-hype me
on my noodle guy") + the market drama (table groans at a shared typhoon) — matching `identity.md`'s warm
rivalry, not mechanical co-op. **Poach is cut** (its banter role is absorbed by the louder, funnier Buzz
fight).

---

## Characters — asymmetry that bends the engine

Five warm, food-obsessed **agent** archetypes, each **public**, each **one ability + one flaw on an
opposing lever**. Abilities are **flat/bounded — no compounding engine powers**. Target EV ≈ 2–4 VP or
~1–2 turns of tempo. **v4 changes: the Conductor is re-themed to the Lunch-Box Granny; the Gourmand's
pantry-wild ability is re-homed (pantry is gone); the Influencer's +Buzz now bites harder (it's the Buzz
fight).**

| # | Character | Ability | Flaw | Lever / anti-lever |
|---|-----------|---------|------|--------------------|
| 1 | **The Night-Market Auntie 阿姨** | *Regular's Discount* — the first vendor you Bribe in **each of your first two regions** costs **1 fewer ingredient**. | *Set in her ways* — **no HSR** (routes the ring the long way). | ingredient discount / mobility |
| 2 | **The Eager Rookie 菜鳥** | *First-Timer's Luck* — when you **Visit the Local Market**, if you reveal a hazard you may **cancel it** (discard, no fire) once per turn. | *Bites off too much* — **Larder cap 6**. | market safety / storage |
| 3 | **The Lunch-Box Granny 便當阿嬤** *(re-theme of the Conductor)* | *Lunch From Home* — when you **Travel**, draw the top market card of the region you are **LEAVING** (a lunch packed from home) instead of the region you arrive in. | *Packed my own, thanks* — when you **Visit the Local Market** you keep only **1** specialty (not 2). | travel-sourcing / market-sourcing |
| 4 | **The Influencer 網紅** | *Going Viral* — your **Promote places +1 Buzz** (3 instead of 2) — a sharper edge in the Buzz fight. | *Chasing clout* — go **last** in turn order and start **2 resources behind**. | Buzz fight / tempo |
| 5 | **The Grizzled Gourmand 老饕** | *Connoisseur* — when you **Visit the Local Market**, reveal **4** cards (keep 2) — you dig deeper and dodge more hazards. | *Too jaded* — **cannot gain Buzz from boon events** (you still get their other effects). | market depth / events |

**Design notes.**
- **The Rookie's ability is re-pointed** from "draw 2 events resolve 1" (v3.1) to a **hazard-cancel** —
  cleaner now that events live in the market decks, and (bonus) it's **sim-legible** (the sim can model a
  cancelled hazard), fixing v3.1's "event-coupled, sim can't judge" flag.
- **The Gourmand's ability is re-homed** from pantry-wild (pantry gone) to **reveal-4-keep-2**, making him
  a **market specialist** — and, like the Rookie, now **sim-legible** (deeper draws are measurable),
  fixing the other v3.1 event-coupled flag. His "no boon Buzz" flaw is milder now that boons are the event
  minority — watch it isn't *too* mild.
- **The Lunch-Box Granny is a Travel-sourcer** (a parting ingredient every move) who's **weak at the market
  haul** — a clean lever/anti-lever, distinct from the Auntie. Her ability is lateral (no raw EV gain, just
  a timing/flexibility shift), so her flaw is light to match. → `bg-theme` names her + writes the warm
  lore (granny who packs 便當, not a decline gag).
- **The Influencer's +Buzz is now much more relevant** (Buzz is the contested spine) — watch she doesn't
  over-perform in the fight; her go-last/2-behind flaw is the counterweight (may need re-tuning at count).

*(6th, held as expansion:* **The Homesick Local**, +/− tied to a self-picked home region.)*

**No dominant character×mission combo (re-verify in sim).** Each ability sits on a *different* lever, each
flaw pulls against the mission it most helps, and draw-3-keep-1 launders the rest. The **two v3.1 table-
watch flags (Rookie, Gourmand) are now sim-legible** by design — the re-sim should be able to seat all
five where v3.1 could only carry two to the table. The **Influencer** (Buzz relevance up) is the new one to
watch.

---

## Player counts & scaling

Base = **2p** (the design home; the Buzz tug-of-war is sharpest as a two-person fight). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Vendor Board slots** | 5 | 6 | 7 |
| **Buzz supply** | ~24 | ~32 | ~40 |
| **Act-advance threshold (wins/act)** | ~5 | ~7 | ~8 |
| **Market deck size** | base | +1–2 event & specialty each | +2–3 each |
| **Buzz majority rule** | ≥2 over the rival | **≥2 over the *highest* rival** | ≥2 over the highest rival |
| **Start positions** | opposite (N & S) | spread on the ring | spread |

At 3–4p the Buzz majority is **≥2 over the highest single rival** on that vendor (not the sum) — so a
vendor several players are eyeing is genuinely hard to close, and multi-way contests are chaotic-fun but
harder to balance (→ `bg-architect`; watch the Influencer's Buzz edge at count). Resentment is **lower**
at 3–4p (a lost fight is diffuse); the sharp balance case is **2p**. **Best-at: 2p**; 3–4p a warmer,
louder race.

## Solo mode / Automa

**Medium priority** (near-expected on a mid-weight engine). Sketch — a **"Rival Agency" Automa**:
- A small **Route deck**. On its turn, flip the top card: it **Promotes** (drops Buzz on the highest-
  Prestige contested Board vendor in a rotating "focus region"), **Bribes** (if it holds a ≥2 majority on a
  vendor in its focus region and its running ingredient counter can pay — locks it from you and advances
  the Act), **sources** (bumps its ingredient counter for the focus region), or **rotates** its focus
  region. Its Buzz on a vendor is real and contests *your* majority — so the fight still bites solo.
- Pressure = **the Buzz race + the act clock**. Difficulty = Buzz-aggressiveness + a target score. Upkeep
  near-zero (one flip, one lookup). **Defer to `bg-architect`; not in the base MVP.**

## Complexity budget

Target **~2.4–2.5, ceiling 2.5** (pending the raise decision); `complexity-budget.json` caps (rulebook
1650 words, keywords 15, component types 8, aid 22 lines); `bg-elegance` guards.

**The weight call (honest, expanded).** v4 **adds real system**: the **Buzz-majority** (placement rules +
region-gating + the ≥2 check + the clear-on-win resolution — the biggest single teach), **Acts** (act
state + board sweeps, more than a linear counter), and the **push-your-luck market** (draw-3-keep-2 +
the hazard-fire rule). It **banks**: **Extract cut**, **Poach cut**, **pantry folded** into the Convenience
Store (one fewer ingredient type + simpler costs), **event tiles → market cards** (one fewer component
type), **Season counter → Act condition**. **Component types drop 7→~6** (cost/BOM *improves* even as
teach-weight rises — worth flagging to `bg-architect`). Net **teach-weight ~2.5–2.6 pre-trim** — at/over
the ceiling. The Buzz-majority is the deliberate spend and the CD's headline ask.

**To hold ≤2.5, deploy in order:**
1. **Region-Coverage → mission-only** (recovers ~0.1; the v4 region-gating already forces breadth, so an
   explicit Coverage track partly double-pays). **← recommended now.**
2. **Reputation milestone perks → pure end-VP** (recovers ~0.15; Rep stays a clean parallel scorer).
3. **Fold Convenience Store's "any region" into a plain wild draw** / or **fold Promote's placement into
   Travel** (structural, last resorts).
Depth lives in **the Buzz fight under a push-your-luck market across escalating acts** — protect that, cut
around it. **If the CD would rather keep all tracks/perks, consciously raise the ceiling to ~2.6**
(defensible next to Arcs ~3.0 / Splendor Duel+ ~2.3–2.5) and log it.

**Keywords ≈ 12–13** (under 15): Larder · Vendor · **Bribe** · **Buzz** · **Promote** · region **discount
icon** · **Prestige** · **Reputation** · **Coverage** *(if kept)* · **market deck** · **hazard/event** ·
signature **Mission** · **Act**. (Visit / Convenience Store / Travel / specialty stay plain-language.)

## Keywords / glossary

- **Larder** — your sourced ingredient cards, **face-up**. Cap **7** (6 for the Rookie).
- **Vendor** — a Board card (tiered by Act) you **Bribe** to secure; carries ingredient cost, a region
  **icon** (discount + coverage), **Prestige**, **Reputation**, a **perk**, and the **Buzz piled on it**.
- **Bribe** *(working name; `bg-theme` finalizes)* — the core action: in the vendor's region, holding a ≥2
  Buzz majority, pay its ingredients (− discount) to win it (the vendor **chose you** — the rival was
  outraced, not robbed).
- **Buzz** — the committed, public, contested resource; **Promote** to place it **on vendors in your
  region**; never discounted; clears to supply on a win. The interactive anti-runaway brake.
- **Promote** — the action that places 2 Buzz on vendor(s) in your current region.
- **discount icon** — a vendor's region badge; each held reduces that region's ingredient cost on future
  vendors by 1 (floored at 0). The compounding engine (ingredients only).
- **Prestige (VP)** — a vendor's star value; the headline VP vector; live on the track.
- **Reputation** — the parallel track climbed by Bribing; end-VP by position (+ perks, weight-dependent).
- **Region-Coverage** — end-game breadth bonus (2/5/9). *(Weight decision: may fold to mission-only.)*
- **market deck** — a region's face-down deck of its 2 specialties + events; **Visit** draws 3 keeps 2
  (hazards fire); **Convenience Store**/**Travel** draw 1 (whiff, no fire).
- **hazard / event** — a warm-comedic secular event card inside a market deck; hazards tax-not-destroy.
- **signature Mission** — your secret **+7** vendor pattern (draw-3-keep-1); the only hidden info.
- **Act** — one of three escalating game phases (Stalls → Eateries → Marquee); advances on N table-wide
  wins; Act 3's end scores the game.

---

## Riskiest assumptions & the top-3 open questions for playtesting

**The single riskiest assumption:** **the Buzz-majority tug-of-war is fun and tense, not a swingy
slap-fight or a degenerate "never commit, always snipe."** This is new, load-bearing, and untested. The
re-sim must lead with it.

**Top 3 open questions (in priority order):**

1. **Is the Buzz fight fun/tense and non-degenerate? (THE make-or-break.)** *Attack (sim + table):*
   **Buzz-war frequency & depth** (do agents escalate sanely, or drain the supply on one vendor?);
   **"snipe-only" win-rate** (a strategy that never commits early and only closes at the last second —
   must be ≤~55%, i.e. early commitment must be viable); **loser's-tempo cost** (how many actions does a
   lost fight burn? is it "outraced not robbed" or feels-bad?); **supply pressure** (is ~24 Buzz right?).
   *Fail fixes:* tune the ≥2 margin (→≥1 or ≥3), the Buzz-per-Promote (2), the supply size, or partially
   refund the loser's Buzz to soften.
2. **No dominant track or opening under the new interaction?** Do **tall ≈ rep-climb ≈ breadth** stay
   competitive, and does the Buzz fight keep openings from solving (opponent-dependence)? *Attack:* the
   dominant-track/opening probe (no line >~55%, ≥3 viable). *Fail fixes:* rebalance costs / track rewards.
3. **Is the push-your-luck market spicy, not punishing — and does movement still spread?** *Attack:*
   **hazard-hit rate per Visit**, **Visit vs Convenience-Store usage** (is Visit worth the risk?),
   **per-region sourcing share** (each ≥~18%; South not starved), **inter-region moves/game** (region-
   gating should *increase* travel). *Fail fixes:* hazard density per deck, the reveal-count, the "brewing"
   telegraph knob; the cross-link rate for movement.

*(Secondary: per-character 45–55% with the re-homed Rookie/Gourmand + the sharper Influencer; the Acts
pacing to ~7–8 wins/player in ~40–45 min.)*

---

## OPEN DECISIONS for the Creative Director (A/B/C)

**D1 — Act count & advance-condition.** *(The pacing spine.)*
- **A. 3 Acts, advance on "N vendors won table-wide per act" (2p N≈5).** *(recommended.)* Cleanest pacing
  control, scales with player count, and *is* the catch-up co-brake (fast winning hurries the end). ~15
  wins → ~7–8/player → ~40–45 min.
- **B. 3 Acts, advance when the act's *vendor deck is exhausted*.** Guarantees each tier is fully used;
  con: depends on refill/deck size, less direct control, unwon vendors linger.
- **C. 3 Acts, advance on a *shared Act track* filled by weighted wins (Marquee counts more).** Familiar,
  very visible; con: it's essentially the Season counter we removed, re-skinned per act.
> *Recommendation: **A**, with deck-exhaustion (B) as a silent backstop for edge cases.*

**D2 — Buzz-gain method & the loser's-Buzz fate.** *(The heart of the rework.)*
- **A. Promote places 2 Buzz on in-region vendor(s); on a win, ALL Buzz (winner + loser) clears to the
  supply.** *(recommended.)* Simplest, symmetric, thematically clean ("hype dissipates once the deal's
  done"); the loser loses only tempo → "outraced, not robbed." The escalation risk is real → sim probe #1.
- **B. Same, but the *loser* gets a partial refund** (e.g. keep-half, rounded down, returned to the supply
  as a "credit" they may re-place next turn). Softer on early committers; adds a bookkeeping rule and a
  private-ish Buzz notion (against the "no private pool" cleanliness).
- **C. Buzz is *taken* into a small private pool first (Promote = +2), then *placed* on-site.** Closer to a
  hybrid of old + new; con: reintroduces the private-pool hoarding the rework is trying to kill.
> *Recommendation: **A** — ship the clean version, use B's partial-refund only as a sim/table fail-fix if
> early commitment proves dominated.*

**D3 — Event boon/hazard ratio (in the market decks).**
- **A. ~55–60% hazard / ~40–45% boon.** *(recommended.)* Hazard-leaning per the CD's "cut the boon skew,"
  but the boon minority keeps Visits from being pure dread and holds the warm tone.
- **B. ~50/50.** Safer/warmer; less of the "genuine risk" the CD asked for.
- **C. Market decks = specialties + *hazards only*; boons delivered separately (e.g. milestone/opt-in).**
  Maximal push-your-luck dread on every Visit; con: loses the "nice surprise" texture and adds a second
  event channel.
> *Recommendation: **A**. Also decide the reserve **"brewing" telegraph** (top card of each deck face-up) —
> I'd hold it in reserve and add only if blind decks feel too swingy at the table.*

**D4 (bonus, weight) — Poach & Coverage.**
- **Poach:** **cut** *(recommended)* — the Buzz fight is the co-location interaction now; or **keep,
  re-scoped** (only when *not* contesting a shared vendor) if the CD loved the swipe.
- **Coverage:** **fold to mission-only** *(recommended, to hold ≤2.5)* — region-gating already forces
  breadth; or **keep as a scoring track** and **raise the ceiling to ~2.6**.

---

## Handoff notes (guardian sweep — where to look)

**v4 — what moved (run `bg-theme` coherence + `bg-elegance` budget on the change):**
- **The signature twist EVOLVED.** Still "win vendors as engine pieces feeding tracks toward a hidden
  mission on a shared board race," but the **race is now a committed, public, on-site Buzz-majority fight**
  (the "Bribe"). This is exactly where theme/mechanics can desync — **`bg-theme` load-bearing checks:**
  (1) does **"Bribe"** read as **warm comedy** (piling hype/goodwill on a vendor to win their favour),
  **not** real corruption? — the anti-extraction/anti-sleaze rail; the mechanic (public Buzz you both pile
  on, vendor "chooses" the bigger fan) *supports* a warm read, but the *word* needs care. (2) The **Acts**
  framing (Stalls → Eateries → Marquee as a "season" arc) — a fiction hook to name. (3) The **Lunch-Box
  Granny** — name + warm lore (packs 便當 from home; not a decline gag); confirm she's distinct from the
  Night-Market Auntie. (4) Events now **hazard-leaning** — confirm the warm-comedic/tax-not-destroy tone
  holds and stays **secular**.
- **`bg-elegance` check (the honest ledger):** teach-weight up to **~2.5–2.6 pre-trim** (Buzz-majority is
  the spend), banked by Extract/Poach/pantry cuts + Season→Acts + tiles→cards; **component types 7→~6.**
  Deploy Coverage→mission-only to hold ≤2.5, or advise the CD's ceiling raise. Guard the rulebook word
  count (the Buzz-majority section is new prose).
- **`bg-access` / `bg-infodesign` (component data + board moved):** the board now shows **Buzz piled on
  vendor cards** (a new at-a-glance read — whose Buzz, how much, the ≥2 gap) + the **Act track** + face-
  down **market decks**. Keep dual-coding; make the Buzz-majority state parseable without counting.
- **`bg-developer` data:** re-cost the 25 vendors to **named specialties only** (pantry removed), re-tier
  into three **Act decks**; build the four **region market decks** (specialties + hazard-leaning events as
  cards); rebuild `events.csv` (drop the boon skew, re-home into decks); re-home the two **wild_pantry**
  perks → **wild_specialty**; add the **Buzz-reach** marquee perk; size the **Buzz supply** (~24 @2p);
  re-theme **Conductor → Lunch-Box Granny** (ability + flaw) and **re-point the Rookie/Gourmand** abilities
  (hazard-cancel / reveal-4-keep-2); print the **Act track** + Vendor Board Buzz zones.
- **`bg-playtest`:** rework `sim/travel_agents.py` to model **Buzz-on-vendor majority + the push-your-luck
  market decks + Acts + board escalation**, then run the three probes above **lead with Riskiest #1 (the
  Buzz fight)**. The re-homed Rookie/Gourmand are now sim-legible — seat all five.

**Cut mechanics to sweep for stranded names/rules:** **Extract**, **Poach**, **pantry**, **Stock Up**,
**the Season counter**, **event tiles / the face-up Market**, **the Retired Conductor** — check nothing in
components/rulebook/sim still references them.
