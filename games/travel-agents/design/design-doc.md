# Travel Agents: Taiwan — Design Doc (v6 · the economy fork: drinks as easy points, a 5-ingredient palette, beverages off the clock)

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.

**Provenance (read this first).** The mechanical spine is the **v4 Buzz-majority / push-your-luck
rework** (committed public Buzz on vendors, face-down market decks, Extract + Poach cut). **v5** tightened
it to a **≤30-minute two-Act "one glorious eating day"** on a single **day-clock**, cut Region-Coverage to
a Mission, added the **★ Star value swing**, and re-cast the five characters as Taiwanese social types.
**v6 folds in the CD's LOCKED economy-fork direction** (this doc's brief) — it **supersedes v5's
"three value-bands dealt across two Act decks" + "~10-ingredient palette" framing**:

- **The day-clock is TWO beats, not a three-band ladder.** **Act I · The Breakfast Run 早餐** (breakfast
  shops 早餐店, the morning opening) → **Act II · Night Market 夜市** (night-market stalls 夜市攤, the
  climax; the apex ★ vendors live here). **Beverage shops 飲料店 come OFF the clock** — persistent,
  region-free, "all day."
- **Beverages = the "easy points" strategic FORK** — a viable low-value / low-conflict / low-travel
  alternative to pushing the contested breakfast→night-market ladder.
- **The Convenience Store action anchors the drinks engine** (flip top 1 of any region, no travel, safe);
  beverages want the **common ingredient** it reliably yields.
- **The ingredient palette is cut to 5** — one region **signature** each (N/C/S/E) + **one common**.
- **Only ladder (breakfast/night-market) Bribes advance the day-clock; beverage Bribes do NOT** — the
  fork's structural spine (progress vs parallel easy points).
- **The vendor bands are renamed off "Marquee / Eatery / Stall"** to the real Taiwanese venue types
  (`identity.md` locks the 繁體/Tâi-lô romanisation in parallel; this doc uses the English names).

Everything v6 does **not** touch stands from v5: the Buzz-majority fight, the five characters (three KEPT
kits re-lored + 大胃王/大哥 NEW), the two live tracks + hidden +7 Mission, the ★ Star swing, and the
sensitivity rails. **One flavour simplification lands this pass (CD directive):** the end-game's **"Code
Red" spy-alarm label is DROPPED** — the finish is now just the natural **Day → Night** arc (night winds
down → the last train home). The *trigger mechanic* is unchanged in structure; only the flavour and the
name change (see *Acts & end-game*). The v4 change-ledger and the v3.1 movement rebalance still bind
`bg-developer` **except where the 5-ingredient palette re-costs everything** (see *Economy*).

> **One-line frame:** two rival travel agents race across Taiwan through **one escalating eating day** —
> source real regional ingredients from face-down region **markets** (push-your-luck: a typhoon may be the
> next card), and pile **Buzz** onto the island's vendors to **win them over** (on-site, out-hyping your
> rival). The high road is the contested **breakfast → night-market ladder** (climbs Prestige/Reputation
> toward a hidden **signature tour**, and drives the day forward); the safe road is grinding **easy points
> at the all-day drinks stands**. Play the day into the night; when the night market winds down, catch the
> last train home — best tour is **Top Agent**.

Sensitivity rails bind throughout (`identity.md` §Sensitivity): winning a vendor reads as **the vendor
choosing the agent who hyped them best** — never an agent seizing, cornering, or corrupting a place.
"Bribe" is the **warm-comedic** *"this isn't a bribe, it's a marketing opportunity"* caper — the smarm
lands on the over-the-top agent, never the vendor. Two characters (大哥 gangster-adjacent, 里長伯
politician) sit next to that keyword and carry the **#1 consultant flags** — bind the warmth hard.

---

## What changed in v6 (the honest ledger for `bg-elegance`)

v6 is a **restructure of the economy layer**, not a new spine. The net is **weight-neutral-to-lighter** —
the 10→5 palette cut is a real simplification that pays for the fork.

| Cut / banked (−) | Added / spent (+) |
|---|---|
| **~10 ingredients + a wild "pantry" token** | **5 ingredients** (4 region signatures + 1 common) — fewer token types, a lighter re-cost, a cleaner dig |
| **Three value-bands dealt across two Act decks** (Stalls-top + Eateries-beneath = Act I; Marquee = Act II) | **Two clean Act decks** (breakfast = Act I; night-market = Act II) **+ one persistent Beverage deck** off the clock — the board teaches as "the big board changes with the day; the drinks stand is always open" |
| **Beverages as a mid-rung of the ladder** | **Beverages as a parallel FORK** — region-free, common-fed, off-clock, low-conflict (one new idea: a small persistent Beverage Row) |
| **"day-clock climbs on every Bribe"** | **"day-clock climbs only on ladder Bribes"** (+1 rule clause — the fork's engine) |

**Honest weight call.** The palette cut (10→5, drop the wild pantry) is worth more than the fork costs:
fewer ingredient types = fewer icons on cards, a shorter player-aid, a smaller bill of materials, and a
dig that's easier to parse. The fork adds **one new concept** (the all-day Beverage Row) and **one rule
clause** (drinks don't tick the clock). Net **~2.4–2.5, at/under the 2.5 ceiling** — the same band v5 held,
with more of it banked. `bg-elegance` re-reads (the component gauge should now read materially lighter).

---

## Design goals

- **A tight two-player engine with a real *fight* at its centre AND a real *fork* beside it.** The
  Buzz-majority makes each **ladder** vendor a public, escalating, on-site tug-of-war (the Arcs-Court
  tension the CD asked for). The **drinks fork** gives the player who doesn't want that fight — right now,
  this game, or this turn — a viable, low-conflict way to score. Two legitimate identities in one half-hour
  box.
- **Target weight ~2.4–2.5, ceiling 2.5.** Depth from the Buzz contest + push-your-luck market + the
  progress-vs-easy-points fork; complexity banked by the 10→5 palette cut and two clean Act decks.
- **2-player first.** The duel is the design home; the Buzz-majority is sharpest as a two-person
  tug-of-war. 3–4p is a scaling delta.
- **Aesthetics (locked, `identity.md`):** **Discovery (lead)** — face-down markets + the day→night
  escalation keep revealing the island; **Fellowship** — the shared, comedic fight over a prize vendor;
  **Challenge** — routing + two-input + when-to-commit + **which-road** (ladder vs drinks), kept light.
- **The meaningful decision every turn:** *push the contested ladder (travel, dig my region signature,
  win the Buzz fight for a big night-market name) — or bank a safe, region-free drink off the convenience
  store?* And within the ladder: *dig now (risk a typhoon), grab a safe blind card, travel on, pile more
  Buzz, or close the Bribe before my rival out-hypes me?* No forced move.
- **Taiwan does real work** (unchanged): the region↔signature web is real food geography — rename the
  setting and the recipes break. The two Acts are the real Taiwan food day (breakfast → night market); the
  all-day drinks stand (手搖飲) is the very-Taiwan third texture that makes the fork feel native.
- **Design the make-or-break risks out:** **(a)** the Buzz contest is fun/tense, not a swingy slap-fight
  or a "never commit, always snipe" degenerate; **(b)** **the drinks fork is viable but not dominant** — a
  real choice, never a solved low-effort line; **(c)** the 5-ingredient dig stays a real decision, not a
  flattened one; **(d)** no economy runaway in a short game; **(e)** the 大哥 tie-win doesn't dominate the
  Buzz fight.

---

## Core loop (detailed)

A turn is **one action**; short turns, low downtime. Each cycle you weigh: *which road am I on this turn —
the contested ladder or the easy drinks — which input am I short, am I on-site to act, and is now the
moment to close before my rival swoops?*

1. **Read the board.** The **Vendor Board** has two zones:
   - **The Ladder** (the contested, clock-driving zone): breakfast-shop vendors in Act I, night-market
     vendors in Act II — each with its ingredient cost, its **region icon**, its **Prestige/Rep/perk**, and
     **the Buzz both agents have piled on it**. Region-gated: you must be on-site to Promote/Bribe.
   - **The Beverage Row** (the persistent, off-clock zone): a small fixed row of drinks vendors, **not tied
     to any region** and never swept — available all game.
   Your secret **signature mission** points at a vendor pattern worth **+7**. The four **region market
   decks** are face-down (you know each region's signature + that hazards lurk). Your **Prestige** and
   **Reputation** markers show your two live vectors; the **day-clock** shows how close the day is to dusk
   (Act II) and to the **last train home** (the end of the night).
2. **Take one action:** **Visit the Local Market**, **Convenience Store**, **Travel**, **Promote**, or
   **Bribe a Vendor**.
3. **Sourcing is a gamble on the ladder, safe on the drinks side.** *Visit the Local Market* (your region)
   flips the top 3 of that region's deck: any **hazard** fires on the spot, then you keep up to **2** of the
   **ingredients** you turned up — the push-your-luck spine, the way you bulk-source **region signatures**.
   *Convenience Store* takes a single blind top card from **any** region (event → whiff, nothing fires) —
   the safe, no-travel way to source the **common** ingredient the drinks engine runs on. *Travel* takes a
   single blind top card on arrival.
4. **Buzz is a public fight — on the ladder.** *Promote* places Buzz onto vendor(s) you're with (ladder
   vendors: your current region; beverage vendors: anywhere — they're region-free). You can only **Bribe** a
   vendor when you hold **≥2 more Buzz on it than your rival** and can **pay its ingredients** (minus
   discounts). Winning clears all its Buzz to the supply and scores you Prestige + Rep + its perk.
5. **The two roads diverge on the clock.** A **ladder** Bribe (breakfast or night-market) **advances the
   day-clock +1** — it is *progress*, and it hurries the end. A **beverage** Bribe scores you easy points
   but **does NOT advance the clock** — it is *parallel*. When the day-clock reaches **dusk**, the Ladder
   sweeps and re-stocks from the **Night-Market deck**; at the **last-train** mark, **head office calls Code
   Red** → finish the round + one full round → reveal missions → score.

The **ladder** compounds legibly and with a brake: each ladder vendor makes a *class* of future vendors
cheaper in **ingredients** (the ramp) — but every one still demands you **win an undiscounted,
region-gated, contested Buzz majority**, on-site. The **drinks** road does *not* ramp — it's a flat,
reliable, region-free trickle of easy points. That asymmetry **is** the fork (see *The drinks fork*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** — 4 regions on a ring: **North 北 – Central 中 – South 南 – East 東**; an
  **HSR** spine links North↔South down the west coast. The board carries the **day-clock** (the Act track,
  with a **dusk** and a **last-train** mark), the **VP (Prestige) track**, the **Reputation track**, the
  **Vendor Board** (its two zones), and a face-down **market deck** zone per region.
- Build the **four region market decks**: each = its **one signature ingredient** (several copies), **the
  common ingredient** *(in the two regions that carry it — see Economy)*, **+ 3–4 event cards**
  (hazard-leaning), shuffled face-down.
- Build the **three vendor decks** from the 25 vendors (re-sorted by venue — see *Vendors*):
  - **Act I deck = the Breakfast Shops 早餐店** (~10), shuffled.
  - **Act II deck = the Night-Market Stalls 夜市攤** (~8–9), shuffled — set aside face-down until dusk.
  - **Beverage deck = the Beverage Shops 飲料店** (~6–7), shuffled — feeds the persistent Beverage Row.
- Deal the **Ladder** from the Act I (Breakfast) deck (2p: **4 slots**). Deal the **Beverage Row** from the
  Beverage deck (2p: **2 slots**). Set the **day-clock** marker to 0.
- Form the **Buzz** supply (open pool; **~24 at 2p** — see *Economy*).
- Each agent: choose/deal an **Agent Character** (ability + flaw, public); take a pawn (start on opposite
  regions — one North, one South); place **VP** and **Rep** markers at 0; take an empty tour + Larder area.
  The Larder (ingredient cards) sits **face-up** all game. Deal **3 Mission cards, secretly keep 1** (+7),
  return 2 unseen.

**A turn = choose ONE action:** **Visit the Local Market · Convenience Store · Travel · Promote · Bribe a
Vendor.** Then if your Larder exceeds **7** ingredients, discard down to 7 (to that region's market
discard). Play passes clockwise (the Influencer's flaw = goes last; see *Characters*).

**End-trigger (the last train home).** When the **day-clock reaches the last-train mark**, **the night
market winds down**: finish the current round (equal turns for all), play **one more full round**, then
**reveal signature missions** and score. A fair, unswingy wind-down; the extra full round guarantees the
trailing player answers the trigger. **Reputation-top scores its bonus but does not end the game** (carried
from v3.1's sim-fix).

Target length: **~25–30 min at 2p**, roughly **14–18 turns per player**, **~5–6 vendors won per player**
(a mix of ladder + drinks).

---

## Actions

A turn = ONE of five. Each is simple; the depth is in *when*, *where*, and *which road*.

| Action | Where | Effect | Notes |
|--------|-------|--------|-------|
| **Visit the Local Market** | your current region | Reveal the top **3** cards of this region's market deck. Resolve **any event** revealed immediately (**hazards fire**), discard them. Keep up to **2** of the revealed **ingredients** (to your Larder); discard the rest. | The ingredient workhorse **and** the push-your-luck spine — the way you bulk-source your **region signature**. More hazards = more risk. *大胃王 keeps all 3; 媽寶 keeps only 1.* |
| **Convenience Store** | anywhere | Reveal the **top 1** card of **any one** region's market deck. Ingredient → take it. Event → discard it, **nothing fires** ("shelf was picked clean"). | **The drinks engine's spine.** Safe, no travel, any region — the reliable way to grab the **common** ingredient beverages run on. Aim it at a common-bearing region. One blind card, can whiff. |
| **Travel** | to an adjacent region | Move your Agent to an **adjacent** region (HSR: North↔South counts adjacent); then reveal the **top 1** card of the **arriving** region's deck (ingredient → take it; event → whiff). | Never a dead turn — you (usually) arrive with something. *媽寶 draws the region she LEFT instead. 里長伯 cannot use HSR.* |
| **Promote** | ladder: your region · beverages: anywhere | Place **2 Buzz** from the supply onto **vendor(s) you're with** — a ladder vendor **in your current region**, and/or a **beverage** vendor (region-free, so from anywhere). Buzz stays on the card, public; the rival may also Buzz it. | The Buzz-placement action. Ladder Buzz is region-gated; beverage Buzz is not (drinks stands are everywhere). *網紅 places 3 (+1). 大哥's alternate flaw = places 1.* |
| **Bribe a Vendor** | ladder: in its region · beverages: anywhere | Choose a Board vendor you're with on which you hold **≥2 more Buzz than your rival**; **pay its ingredients** (− region discounts, floored at 0). Take it to your tour → gain **Prestige** (VP live), a **Rep** bump, and its **perk**. **All Buzz on it returns to the supply.** Refill the slot from the matching deck; **the vendor is locked from the rival.** **If the vendor is a breakfast or night-market (ladder) vendor, advance the day-clock +1. A beverage Bribe does NOT advance the clock.** | The scoring beat, gated by **majority + ingredients** (+ **position**, for ladder vendors). The clock-tick clause is the fork's spine. *大哥 wins at a tie (≥0), not ≥2; 大哥 pays +1 ingredient.* |

**Five actions, no conditional sixth.** (Poach and Extract are **cut**.) Every turn has multiple live
options with real trade-offs, including the top-level **which road** choice. No forced/obvious move.

**Two rules stated once, to keep the ruleset small:**
- **Hazards fire only when you Visit the Local Market.** A hazard revealed by *Travel* or the *Convenience
  Store* (single blind draws) is simply discarded — "that shelf was bare," nothing fires. (Protects the
  travel + drinks engines; makes *Visit* the true push-your-luck.)
- **Buzz lives only in the supply or ON a vendor.** No private Buzz pool. You never "hold" Buzz; you place
  it, and it is either won-and-cleared or fizzled-and-cleared.

---

## The market decks & events (the push-your-luck sourcing layer) — now a 5-ingredient palette

- **Palette = 5 ingredients** (cut from ~10; the wild "pantry" token is retired, folded into the common):
  **one signature per region** + **one common**. See *Economy* for the region map and re-cost.
- **Four face-down region decks.** Each = its **one signature** (several copies) + **the common** *(only in
  the two common-bearing regions)* + **3–4 event cards**, shuffled. You know each region's signature
  (printed on the board) and that hazards lurk — you don't know the order.
- **Visit the Local Market** is the risk/reward: 3 flips, hazards fire, keep 2. If two of three flips are
  events, you keep only 1 (or 0) **and** eat the hazards — the genuine push-your-luck. **Convenience Store /
  Travel** are the low-variance single blind draws (whiff, don't fire).
- **Does a smaller palette flatten the dig?** No — the push-your-luck tension comes from the **hazards**
  eating your keep-slots, not from ingredient variety; that's untouched. And the decision of *where* to dig
  is still driven by which **region signature** your target vendor needs. What the cut removes is
  collection *breadth* (fewer distinct things), which we replace with **texture variety across regions**:
  the two common-bearing region decks read "signature + common + events" (a diluted, safer dig with a
  consolation prize), the two pure regions read "signature + events" (an all-or-nothing, higher-tension
  dig). *(This is a real risk to watch — see Riskiest Assumptions; the fix if it flattens is more/spicier
  hazards and a higher cross-region rate on night-market recipes, NOT adding ingredients back.)*
- **Events lean hazard (~55–60% hazard / ~40–45% boon across the pooled decks).** Warm-comedic,
  **tax-not-destroy** (a hazard delays, reroutes, or taxes tempo; never removes an ingredient you hold or a
  whole turn). The boon minority keeps a Visit from being pure dread.
- **Where events sit:** hazards are **per-region cards in that region's deck** (typhoon in the coastal
  South/East decks, plum rains in Central, scooter gridlock in the North). A few **table-wide** events
  reach everyone but still live in a region deck and fire when that region is Visited.
- **Recycling:** ingredient cards flow deck → Larder → (spent on a Bribe) → that region's discard; when a
  deck runs dry, reshuffle its discard (fired hazards return too, so the pressure persists). **Deck
  exhaustion also backstops the day-clock** — see *Acts & end-game*.

**Event starter set (~14; secular, hazard-leaning, warm-comedic; wording via the consultant before lock).**
Hazards (majority): **颱風假 Typhoon Day**, **梅雨 Plum Rains** (your Visit this turn keeps 1 fewer), **完售
Sold Out** (discard the next ingredient in this deck), **機車陣 Scooter Gridlock** (your next Travel arrives
empty), **客滿 Fully Booked** (shuffle this region's deck), plus new per-region hazards so every deck carries
~2 hazards. Boons (minority): **芒果季 Mango Season**, **珍奶節 Bubble-Tea Festival**, **臭豆腐大挑戰
Stinky-Tofu Dare** (opt-in push-your-luck), **再吃一點啦 The Aunty Insists**, **網紅來了 Food Blogger**
(table-wide next-Promote +1 Buzz), and the CD's dynamic value-swing boon **摘星了！ Michelin Nod / 得獎了！
Competition Winner** (see below). *Reserve knob:* if blind decks feel too swingy, add a **"brewing"
telegraph** (top card of each region deck face-up before you Visit) — ~1 rule, restores preview agency.

**The "vendor gets hot" boon (★ Star — makes ladder vendor value DYNAMIC).** At least one boon event —
**摘星了！ Michelin Nod** (variants: **得獎了！ Just Won the Competition**, **爆紅 Went Viral**) — **places a ★
Star token on a LADDER vendor** (breakfast or night-market — **never a beverage**; see below), raising its
worth to **+2 Prestige / +1 Rep** for whoever wins it. **Targeting (proposed):** the Star lands on the
**lowest-Prestige unstarred Ladder vendor** (ties → the revealing agent chooses) — deterministically
turning *the most-ignored stall* into a live contested prize that **pulls both agents toward that region**
and starts a fresh Buzz fight. **Why ★ stays off the drinks side:** the ★ swing is what makes the *ladder*
high-variance-high-value; the drinks fork is deliberately the **steady, low-swing** road. A ★ on a
region-free beverage would create no travel pull and would blur the fork — so the token targets the Ladder
only. *(Design knobs → sim: the targeting rule; how many "gets hot" events sit in the boon slice — 1–2
proposed.)*

---

## The Buzz-majority system (the headline mechanic)

The core, unchanged from v4. Read it as the Arcs-Court "agents on a card" mechanic, re-skinned to **hype on
a vendor** and lightened for a 2p duel.

**The rules, plainly:**
1. **Buzz is committed, public, and gated by presence.** **Promote** places **2 Buzz** onto vendor(s)
   you're with. For a **ladder** vendor that means **in your current region**; a **beverage** vendor is
   region-free, so you can Buzz it from anywhere. Buzz sits on the card, face-up. **Both agents may pile on
   the same vendor.**
2. **Winning = ingredients + a ≥2 majority + presence.** To **Bribe** you must be with the vendor (in its
   region, for ladder vendors), hold **at least 2 more Buzz on it than your rival**, and **pay its ingredient
   cost** (− region discounts). Checked at the instant you pay. *(大哥 needs only a **tie or lead** — a ≥0
   margin.)*
3. **On a win, all Buzz on that vendor clears to the supply** — winner's and loser's alike. The winner's
   hype "paid off"; the loser's "fizzled" (the vendor chose the rival). No private pool. The loser lost
   **only tempo** — never ingredients or VP. **"Outraced, not robbed"** holds mechanically and thematically.
4. **Committing early is a risk *and* a weapon.** Every Buzz you place raises the bar a rival must clear to
   swoop. But Buzz placed is an action **not** spent sourcing — over-invest and you can't pay when the
   moment comes.
5. **No private hoarding, no windfalls.** Buzz recycles on every win; a modest supply (~24 at 2p) sustains
   the whole game and keeps every placement a real, scarce choice.

**Why this is the anti-runaway brake (on the ladder).** Every ladder vendor — however cheap its ingredients
become as your discount ramp grows — still demands you **win a contested, region-gated, undiscounted Buzz
majority, on-site.** The ramp cheapens only the *ingredient* half; the Buzz fight never ramps and can be
**actively raised by your rival.** So the ladder courting *rate* stays capped at roughly **1 vendor per
2–3 turns** even fully ramped.

**Beverages ride the same Bribe rule — but the fight rarely erupts.** Drinks use the identical ≥2-majority
rule (elegance: one winning rule, no special case). The **low conflict is emergent**, not a separate rule:
a beverage is worth so little (Prestige 2, no ramp) that spending contested Buzz on it is usually a bad
trade versus the ladder — so in practice both agents let each other take drinks, and the fork's
"low-conflict" character falls out of the economics. *(Probe: confirm drink-fights stay rare at the table;
if they erupt too often, the fix is lowering beverage value or narrowing the Beverage Row, not a new rule.)*

**The escalation question (a real risk to sim).** Two agents can keep piling Buzz on the same ladder vendor
— a bidding war. Caps: **(a)** the war ends the instant one agent can close (ingredients + on-site);
**(b)** the supply is finite; **(c)** every Buzz placed is an action stolen from sourcing. *Is the war fun or
a slap-fight?* is **Riskiest Assumption #1** — and the **大哥 tie-win** pokes at exactly this floor
(**Riskiest #1b**).

---

## Vendors — the engine cards (three venue types; two on the clock, one off)

A **Vendor** is a stall/cook who agrees to feature on your tour once you've wooed them (ingredients +
winning Buzz majority). The three v5 "Stall / Eatery / Marquee" bands are **renamed to real Taiwanese venue
types** (`identity.md` §Naming) — and v6 re-homes the middle one **off the clock**:

| Venue type | Role | ~Count | On the day-clock? | Region-gated? | Ingredient cost | Prestige (VP) | Rep | Perk | Where it lives |
|------|------|-------:|---|---|---|--------------:|----:|------|------|
| **Breakfast shop 早餐店** | the cheap opening band; the discount **ramp** starts here | ~10 | **Yes (Act I)** | Yes | **1–2** (its region **signature**, sometimes + common) | **1–2** | **+1** | its **region discount icon** (the base ramp) | Act I deck → the **Ladder** |
| **Night-market stall 夜市攤** | the apex; fiercely contested; the **★** lives here | ~8–9 | **Yes (Act II)** | Yes | **2–3** (signatures across 2–3 regions, sometimes + common) | **5–6** *(★ apex 7–8)* | **+2/+3** | a **strong** perk (wild region icon · Buzz-reach · counts as 2 icons · +2 Rep on Bribing) | Act II deck → the **Ladder** |
| **Beverage shop 飲料店** | the **easy-points fork**; low value, low conflict, low travel | ~6–7 | **No — off the clock** | **No — region-free** | **1–2** (the **common**, sometimes + Central tea for a "premium" drink) | **2** (flat) | **+1** | **none / minor** (deliberately **off the ramp** — no region discount icon) | Beverage deck → the persistent **Beverage Row** |

> **The value swing is preserved (v5, kept).** Night-market stalls are the apex both agents want — worth an
> HSR haul and several undiscounted Buzz — with **2–3 "Legendary" 夜市攤 at 7–8 carrying a printed ★** (a
> standing Michelin / Bib Gourmand / competition accolade). Breakfast shops are the humble opening (their
> value is the ramp, not the face number). Beverages are flat easy points. The dynamic **★ Star token**
> (above) makes ladder value *move* mid-game. The band is a **time-of-day / contest-intensity** curve, NOT
> a "which food is posher" ladder — a 手搖飲 isn't fancier than breakfast, and the ★ lets a humble stall hit
> apex (`identity.md` binds this).

### The drinks fork — making "easy points" a real choice, not a trap and not a solved line

The fork is the v6 headline. It must clear **two** bars at once: **viable** (a drinks lean genuinely
competes) and **not dominant** (you can't win on drinks alone against a good ladder player). Here's how each
lever is set to thread that:

**What makes drinks *viable* (not a trap):**
- **Region-free + common-fed + Convenience-Store-sourced = a genuinely low-travel engine.** You never have
  to move to source the common or to Promote/Bribe a drink. A drinks-leaning player can run almost the whole
  game from one spot.
- **Low conflict.** Because drinks are low-value, the rival rarely contests them — you usually clear the ≥2
  floor with a single Promote and close. No Buzz war, no fizzled tempo.
- **Cheap + reliable.** 1–2 common per drink, sourced safely (no hazard fire on Convenience Store). A
  steady trickle with almost no variance — the exact opposite of the ladder's high-variance dig + fight.
- **Flat value that *beats a breakfast shop's face number*** (2 vs 1) — so early, a drink is a legitimately
  attractive "bird in the hand" versus a cheap breakfast stall whose payoff is deferred into the ramp.
- **A mission line of its own** (e.g. *"3 beverage shops"*) so a drinks lean can also chase the +7.

**What keeps drinks from *dominating* (not a solved line):**
- **A hard-capped ceiling.** Beverage Prestige is flat (2), the deck is small (~6–7), and the Beverage Row
  is narrow (2 slots @2p) — so there is a low hard cap on total drink points. A ladder player's 2–3
  night-market stalls (5–8 each) + the ramp + missions out-scores a pure-drinks tour.
- **No ramp.** Drinks carry **no region discount icon** — they don't compound. The ladder's whole
  engine-building payoff (each vendor cheapening the next) is unavailable to the drinks road. Flat stays
  flat.
- **Off the clock — no tempo lever when ahead.** A drinks Bribe doesn't advance the day-clock, so a
  drinks-leaning leader can't *use* their easy wins to hurry the game to a close while ahead (the way a
  ladder leader can). Drinks pad the score but don't shorten the runway for the trailing player.
- **Weak on breadth.** Beverages are region-free, so they **don't count toward region-coverage mission
  patterns** (the grand tour) — the highest-value +7 lines stay ladder-flavoured.

The intended shape: **drinks are the reliable floor and the diversifier** (hedge a lost Buzz fight, pad
between ladder plays, feed one mission); **the ladder is the higher ceiling and the way you actually win a
contested game.** A strong line *mixes* — a few drinks, a strong ladder. **This balance is a knob-heavy
sim/table question (Riskiest #2)** — the live knobs are beverage Prestige value, beverage deck/row size,
whether drinks give any Rep, and the common's availability (below).

**The discount ramp (ladder only, unchanged in spirit).** Each secured **ladder** vendor carries a **region
icon** (N/C/S/E, or wild). Holding *k* vendors with the X-icon reduces the **X-region ingredient** portion
of any future vendor by *k* (floored at 0). Early ladder vendors are dear; each one signed makes a *class*
of future ladder vendors cheaper in ingredients. **Buzz is never reduced; beverages never carry an icon** —
the two brakes on the two roads.

> **Sensitivity (binds — `identity.md`):** East signatures draw on **Indigenous** cuisines — generic,
> respectful labels, consultant before art/print. Taiwan as itself; Traditional characters; Tâi-lô + 繁體,
> never mangled. The "Bribe" keyword must read as **warm comedy**, never corruption. ★ accolades stay real
> & secular, dish names intact, never a false star on a real named business.

---

## Acts & end-game — the day-clock (Day → Night; drinks are off it)

*(v6 flavour note: the end-game is the natural **Day → Night** arc — no named end-trigger. Was flavoured
"Code Red" in v5; the CD simplified it to "play through the day into the night, and when the night's over
the tour's done" — the *trigger mechanic below is unchanged in structure*, only the alarm label is dropped.)*

The game is **one escalating eating day** on a single **day-clock** — a marker that climbs **+1 every time
any agent Bribes a breakfast or night-market (ladder) vendor**. **A beverage Bribe never advances it.** The
clock has **two marks**:

**Act I · The Breakfast Run 早餐** *(day-clock 0 → dusk; renamed from v5's "Afternoon Crawl", which read too
late now that Act I opens on breakfast — bg-theme's rec; alts = "The Day Crawl" / "Daytime 白天").*
- The Ladder is stocked from the **Breakfast Shop deck** — cheap, low-contest at first. Where you **build
  your discount ramp** and stake early region positions. The **Beverage Row runs alongside all day**.

**Dusk (the day-clock reaches the dusk mark).**
- **Sweep** any unwon Ladder vendors (their Buzz returns to the supply — "the breakfast places are
  closing"), and re-stock the Ladder from the **Night-Market deck**. The Act track moves to **Act II**. *(The
  Beverage Row is NOT swept — drinks are all day.)*

**Act II · Night Market 夜市** *(dusk → the last train home).*
- The big **夜市攤** names — expensive, multi-region, fiercely contested, the ★ apex. Where the ladder game
  is won or lost. Only night-market vendors are on the Ladder now.

**The last train home (the day-clock reaches the last-train mark).**
- **Night falls, the night market winds down** — catch the last train home. Finish the current round + one
  more full round → reveal missions → score. (Warm and self-evident; no alarm, no named trigger.)

**The concrete condition (this doc's call — retuned for the fork; ≤30 min @2p):**

> **The day-clock is a single ascending marker, advanced +1 on every table-wide *ladder* Bribe (breakfast
> or night-market). Beverage Bribes do NOT advance it.**
> - **Dusk (Act I → Act II): the 4th table-wide ladder win (2p).**
> - **The last train (game ends): the 7th table-wide ladder win (2p)** — i.e. **3 wins into the Night
>   Market.**
> - **Backstops (prevent an all-drinks stall):** if the **Breakfast deck** empties, dusk fires immediately;
>   if the **Night-Market deck** empties, the last-train mark fires immediately.
>
> *(3p: dusk 5 / last train 9. 4p: dusk 6 / last train 11. All → sim.)*

**Why these numbers (retuned down from v5's 6/10).** In v5 the marks counted *every* Bribe; v6 counts
**ladder Bribes only**, a subset. A "balanced" line wins ~5–6 vendors/player, of which ~60–70% are ladder →
~7 ladder wins table-wide, plus ~4 drink wins in parallel → ~10–12 total wins, ~14–18 turns/player,
**~25–30 min** — the same length as v5, re-labelled so drinks don't push the clock. The 4/3 split (morning
ramp → short sharp night-market scramble) lands the finish on the night-market north star.

**Why "ladder Bribes only" (the CD's #6 call — implemented, and I concur).** This is the structural spine of
the fork. If beverage wins ticked the clock, grinding drinks would **race the game to the last train without
making progress**, and a drinks-rush could end the game before the ladder player cashes their night-market
plays — punishing the intended "main" road. Ticking on **ladder wins only** means a drinks-grinder **scores
in parallel without hastening the end**, exactly reinforcing "focus on progress OR bank easy points." **My
call: implement it.** The one pacing risk it introduces — *does the game drag if a player leans
drinks-heavy and stops feeding the clock?* — is contained by (a) the deck-exhaustion backstops and (b) the
fact that a pure-drinks line is sub-optimal, so a rational player always does *some* ladder. Flagged as a
pacing probe (Riskiest #2b), but I do not expect it to break — it's the cleaner of the two options by a
distance.

**Why a single day-clock (one marker, two marks).** The most elegant form of the escalation: one component,
one "it climbs on ladder wins" rule, two printed marks. It re-uses the removed Season-counter slot as a
*day*-clock tied to **ladder wins, not turns** — keeping the v3.1 catch-up co-brake (fast laddering hurries
the end; a slow/tall player leaves the mark far off and gets more turns to reach parity).

---

## Missions — the secret +7 (draw-3-keep-1), the sole breadth carrier

Deal **3**, secretly **keep 1**, discard 2 unseen. A mission is a **secret vendor pattern** worth **+7 at
scoring** (binary). With Region-Coverage cut as a track, the grand-tour "breadth" line lives here. Starter
pool (re-tuned for the shorter ~5–6-win game, and for the fork):
- *"a vendor in **all 4 regions**"* (**the grand tour — breadth**; ladder-only by nature, beverages are
  region-free)
- *"**3 vendors in the South**"* (region concentration)
- *"**3 breakfast shops**"* (go wide-and-cheap on the ramp)
- *"**3 beverage shops**"* (**the drinks-fork line** — lets an easy-points lean also chase the +7)
- *"**2 night-market stalls**"* (go tall/apex)
- *"a vendor of each of **3 named cuisines**"*
- *"vendors totalling **≥ 12 Prestige**"* (go tall — retuned for the shorter game)
- *"**5 vendors, any**"* (pure volume — near-max; drinks help here, a natural mix line)

Draw-3-keep-1 lets you steer your character/road synergy on purpose and launders the char×mission balance
(you *choose* the combo; the opponent sees your public character and contests). **Open number → sim/table:**
re-confirm each pattern is *achievable but not trivial* in a ~5–6-win game — especially the grand-tour, the
5-vendor, and the two "3 of a venue" lines given the venue counts.

---

## Economy & math

The Buzz-majority + push-your-luck market + the fork are the make-or-break. Numbers are first-pass — the
sim's job is to attack them.

### The 5-ingredient palette + the region map (v6 — the re-cost brief for `bg-developer`)

**Palette = 5** (cut from ~10; the wild "pantry" token is retired):
- **One signature per region.** Collapse the old per-region proteins/produce to a single signature each:
  - **North signature** — a North **protein** (propose **豬肉 pork**, the most broadly-used; beef/chicken/egg
    fold into it mechanically, or survive only as flavour on a couple of apex 夜市攤 — `bg-developer` keeps
    the dishes real).
  - **Central signature** — **茶 tea** (and note: "premium" beverages may want tea + common).
  - **South signature** — **海鮮 seafood** (oysters/milkfish family — the Tainan/Chiayi coast).
  - **East signature** — **米 rice** *(or 山蘇 greens — `bg-developer` picks the one that keeps the most East
    dishes real; the Indigenous-forward East set must stay authentic).* 
- **One common ingredient** — the **drinks + Convenience-Store staple** (the successor to "pantry", now a
  real, finite, named token). *Thematic proposal (bg-theme locks the name + 繁體/Tâi-lô):* **糖 sugar/syrup**
  or **鮮奶 milk** — the base every 手搖飲 shares and every convenience store stocks; it reads as both
  drink-base and light food-filler. It is what the drinks fork runs on.

**Common availability = HALF (2 of the 4 regions) — this doc's call (per the CD's lean), sim-tunable.**
- **Why half, not everywhere:** it **preserves travel value** (a common-everywhere resource makes *where you
  stand* matter less) and creates the **texture variety** the smaller palette needs — two "signature + common
  + events" regions (safer, diluted digs) and two "signature + events" regions (pure, high-tension digs).
- **Why it doesn't starve the drinks engine:** the drinks player sources the common via **Convenience
  Store**, which reaches **any** region's top card from anywhere — so they simply aim it at a common-bearing
  region. Concentrate the common in those two decks so the Convenience-Store yield stays reliable enough to
  make drinks viable. A drinks player standing in a common-bearing region can also **Visit** it (flip 3,
  keep 2) to bulk-source faster, trading the safety of Convenience Store for hazard risk.
- **Which two regions:** propose the **staple's real production home** (e.g. sugar → the historic
  South/Central refining belt) so it's thematically honest; keep the two *pure* regions among those most
  central to night-market cross-region recipes (so the apex-feeding digs stay high-tension). `bg-developer`
  picks; sim-tunable. **If the sim finds the drinks engine non-viable (too slow), widen the common to 3–4
  regions or raise its per-deck share** — this is the top fork knob.

**Re-cost principles for `bg-developer` (v6 — supersedes the v5 re-cost, keeps the geography spirit):**
- **Re-sort the 25 vendors by venue *identity*** (what the dish actually is), not the old tier: breakfast
  items → 早餐店 (~10); drinks → 飲料店 (~6–7); night-market foods → 夜市攤 (~8–9). Expect the night-market
  band to *grow* from v5's 6 (蚵仔煎/雞排/臭豆腐 etc. are night-market foods, not "eateries"). Add a few real
  dishes per band if a band comes up short; may need more per band at 3–4p.
- **Re-cost every recipe to the 5-palette.** Anchor each **ladder** vendor in its own region **signature**;
  keep **~40% of night-market vendors cross-region** (the load-bearing travel lever); breakfast = 1–2
  (mostly its signature, occasionally + common); night-market = 2–3 (signatures across 2–3 regions,
  occasionally + common); **beverage = 1–2 common** (region-free), a couple "premium" drinks + Central tea.
- **Keep the common generally useful** (appears as a minor filler in some ladder recipes) so the Convenience
  Store isn't a drinks-only action — but keep the **signatures** as the thing that gates the ladder.
- **Beverages carry NO region icon** (off the ramp) and no cross-region link.
- Re-home the two orphaned **wild_pantry** perks → **wild_specialty**. Cap any one signature so no single
  region's Visit is over-demanded (watch North, which absorbs the old 4 proteins).

**Income vs spend (per action):**

| Action | Yield (EV) |
|--------|-------|
| Visit the Local Market | +~1.3–1.7 ingredients (region-gated) − hazard exposure *(大胃王 +~0.5; 媽寶 −~0.6)* |
| Convenience Store | +~0.5–0.8 common (blind, aim at a common region, can whiff) — **the drinks engine's income** |
| Travel | +~0.7 ingredient + reposition |
| Promote | +2 Buzz onto the board (a positional investment) *(網紅 +3)* |
| Bribe (ladder) | − signatures (− discount); win vendor → +Prestige +Rep +perk; clears Buzz; **+1 day-clock** |
| Bribe (beverage) | − common; win → +2 Prestige +1 Rep; clears Buzz; **clock unchanged** |

**Cost of a vendor, in actions (the real currency).**
- **Ladder (uncontested):** source signatures (1–3 Visits/draws, fewer as the ramp grows) + ≥1 Promote + the
  Bribe → **~3–4 actions early, ~2–3 ramped**; contested, add a Promote or two. Courting rate **~1 ladder
  vendor / 2–3 turns**.
- **Beverage:** source 1–2 common (1–2 Convenience Stores) + 1 Promote (usually uncontested) + the Bribe →
  **~2–3 actions**, low-variance, from anywhere. A comparable *rate* to the ladder early — but flat, capped,
  and non-compounding, so it falls behind a ramped ladder late. **That crossover is the fork's whole
  balance** (sim it).

**Buzz supply sizing (2p ≈ 24).** Wins recycle it. Beverages consume little Buzz (uncontested) so the supply
mostly serves the ladder fight. First tuning knob; scales ≈ +8–10 per extra player.

**Balance assumptions (attack these):**
1. **The binding constraint alternates** — *early:* ingredients bind (dig the signature out of a hazard-y
   deck) or you take the safe drinks; *late:* the ramp trivialises ladder ingredients, so **the Buzz fight +
   position** bind, and drinks stop keeping pace with the ramped apex.
2. **Two viable roads, ladder ceiling > drinks ceiling** — a pure-drinks tour cannot out-score a good
   ladder tour, but a drinks *lean* (with some ladder) stays competitive. Neither road is >~55%.
3. **Larder cap 7** forces the source→spend rhythm.
4. **Target 2p winner ~22–32 total VP** (retuned for the shorter fork game): ladder Prestige ~14–22 (incl.
   any ★ swing) + a few beverage points ~2–6 + Reputation end-VP ~4–6 + signature mission 0/**7**.

---

## Scoring / win condition — "Top Agent"

Hybrid multi-track: **two live tracks + one hidden vector**. Tracks pay bonuses, **highest total VP wins**
(no sudden-death). At game end each agent totals:
1. **Tour Prestige (VP)** — sum of your vendors' values (breakfast 1–2 / beverage 2 / night-market 5–6 / ★
   apex or Star-token'd 7–8). *(Live on the VP track.)* The tall/prestige line, amplified by the ★ swing.
2. **Reputation** — end-VP by final marker position: **3→+2 · 6→+4 · 9→+6 · 12 (max)→+9.** Climbed by
   Bribing (each vendor's printed Rep; drinks give a small +1). *(Live on the Rep track.)*
3. **Secret signature mission** — **+7 if completed**, else 0. The one hidden vector; carrier of the
   breadth/grand-tour line (and now the drinks-fork *"3 beverage shops"* line).

Highest total is **Top Agent**. **Tiebreak:** highest Reputation, then most vendors, then most regions
covered *(beverages are region-free, so this last tiebreak still rewards the ladder's grand tour)*.

**Designing out a dominant line (they pull against each other).** Night-market Prestige rewards *few, big*
ladder vendors; the ramp rewards *many ladder vendors doubled-up in a couple of regions*; the grand-tour
mission rewards *one ladder vendor in each region*; the drinks line rewards *volume at the region-free
stands*; Rep rewards *steady Bribing on either road*. You cannot max ramp-concentration **and** the
grand-tour **and** an all-drinks volume line at once. The Buzz fight injects **opponent-dependence** — the
"best line" shifts with where your rival commits. (Sim probe #2.)

---

## Randomness

- **Input randomness (the bulk):** the Vendor Board reveal, the **face-down market decks**, the Mission draw
  (mitigated by draw-3-keep-1), the deck orders. The market is **blind** — deliberate variance for the
  push-your-luck.
- **Bounded output randomness (the spice):** the **Visit** flip resolves *after* you chose to dig; bounded
  (keep 2 of 3, hazards tax-not-destroy, composition known, Convenience Store + Travel are low-variance
  valves). The **drinks fork is the low-variance road by design** — a player who dislikes variance can lean
  into safe, blind-but-non-firing Convenience-Store sourcing.
- **The Buzz fight and the Bribe are pure open-information** — no dice, no post-Bribe luck.
- **One hidden-information hook only:** your secret signature mission. Larder, both tours, all Buzz, and both
  tracks are open.

---

## Interaction & tension

**Direct (the spine):**
- **The Buzz-majority tug-of-war** — on the **ladder**. The public, escalating, on-site fight over each
  prize vendor. **Anti-resentment:** a lost fight costs only tempo and reads as *the vendor chose them* —
  "outraced, not robbed."
- **Positional denial** — being on-site gates ladder Promote/Bribe; occupying a contested region and
  stacking Buzz pressures a vendor. *(The drinks road is the low-interaction escape hatch — a player who
  wants less conflict this game can lean there.)*
- **Market scarcity** — a region deck running dry (both agents digging the same market) is a natural reroute
  pressure.

**Catch-up vs runaway (designed):**
- **Against runaway:** the contested Buzz floor, diminishing returns on cheap vendors, finite Buzz supply,
  and the **day-clock co-brake** (fast *laddering* hurries the last train / the end). *(Watch: a drinks-leaning leader is off
  the clock — see Riskiest #2b; contained by the low drink ceiling + deck backstops.)*
- **For catch-up (gentle):** the day-clock co-brake, the multi-track + two-road structure (a trailing player
  always has a live second vector — including the safe drinks road to grind back points), one **table-wide
  hazard** with a leader-excluding sop (Typhoon Day gives Buzz to everyone *except* the Prestige leader), and
  the hidden **+7**.

**Fellowship** — the comedic shared fight over a prize ladder vendor + the market drama (a shared typhoon
groan) — matching `identity.md`'s warm rivalry.

---

## Characters — asymmetry that bends the engine (v5 re-cast, carried into v6)

Five warm, food-obsessed **agent** archetypes — affectionate **Taiwanese social types** (`identity.md`
§Sensitivity), each **public**, each **one ability + one flaw on an opposing lever**. Abilities are
**flat/bounded — no compounding engine powers**. Target EV ≈ 2–4 VP or ~1–2 turns of tempo.

Three KEPT kits are re-lored (numbers unchanged, no re-sim of the *kit*); **two NEW kits** (大胃王, 大哥)
carry proposed numbers the **gated sim must tune.** *(v6 note: none of the kits reference the ingredient
palette directly, so the 10→5 cut does not re-open them — but 網紅's Buzz edge and 大胃王's Visit haul both
interact with the new deck composition, so re-check at the sim.)*

| # | Character | Ability | Flaw | Lever / anti-lever | Status |
|---|-----------|---------|------|--------------------|--------|
| 1 | **里長伯 The Old Councillor** | *Old Favours* — the first vendor you Bribe in **each of your first two regions** costs **1 fewer ingredient**. | *Works Every Room* — **no HSR**. | ingredient discount / mobility | **KEPT** |
| 2 | **媽寶 The Live-At-Home Office Worker** | *Mum Packed You a 便當* — when you **Travel**, draw the top market card of the region you are **LEAVING**. | *Only Eats Mum's Cooking* — on a **Visit** keep only **1**. | travel-sourcing / market-sourcing | **KEPT** |
| 3 | **網紅 The Influencer** | *Going Viral* — your **Promote places +1 Buzz** (3 instead of 2). | *Chasing Clout* — go **last** and start **behind** (2 resources). | Buzz fight / tempo | **KEPT** |
| 4 | **大胃王 The Competitive Eater** | *Eyes Bigger Than the Table* — keep **all 3** on a **Visit** (not 2). | *Head Down, Chopsticks Up* (**proposed**) — **hazards fire twice** when they hit on your Visit. | market haul / market risk | **NEW → sim** |
| 5 | **大哥 The Neighbourhood Big Brother** | *Everybody Knows 大哥* — wins a Buzz fight at a **tie or lead (≥0)** (**proposed**). | *Always Picks Up the Tab* (**proposed**) — each vendor he Bribes costs **+1 ingredient**. *(Alt: Promote places 1.)* | Buzz threshold / Bribe cost | **NEW → sim** |

**Design notes.**
- **里長伯 & 媽寶 are pure re-lores** — mechanics unchanged, **no re-sim of the kit** (only the field-wide
  re-cast re-check). Bind the framing: 里長伯's discount is **earned goodwill, NOT graft** (⚑ politician +
  "Bribe" consultant flag). 媽寶 is warm — the gag is the grown spy who still calls mum at lunch.
- **網紅's +Buzz is load-bearing** (Buzz is the contested spine) — watch she doesn't over-perform on the
  ladder; her go-last/behind flaw is the counterweight.
- **大胃王 (NEW, sim-legible).** Keep-all-3 is a **+1 ingredient per Visit** edge whose value is
  **deck-hazard-density-dependent** — both ability worth *and* flaw magnitude must be tuned. **Proposed flaw
  = hazards fire twice.** May over-brake. **Lighter alternates for the sim:** *(a)* on a Visit where **any**
  hazard fires, keep only **2**; *(b)* the **next** hazard in the deck also fires. Flag: the flaw may need to
  be light.
- **大哥 (NEW, the make-or-break dominance probe).** At a ≥0 margin he wins any vendor he's *matched* the
  rival on. A **large** edge; the **+1-ingredient tab** is the proposed brake but may **under-brake**. **Two
  live knobs:** the **threshold** (≥0 vs ≥1) and the **flaw** (tab vs Promote-1). **Bind HARD
  (`identity.md`):** vendors *like & respect* 大哥, keep full dignity — the reduced threshold is
  **affection/reputation, never fear**; warm cinema bluster; **secular** (street/cinema 角頭, NOT 八家將).
  ⚑⚑ tied-#1 consultant flag with "Bribe."

*(6th, held as expansion:* **The Homesick Local**, +/− tied to a self-picked home region.)*

**No dominant character×mission combo (verify in the gated sim).** Each ability sits on a *different* lever;
draw-3-keep-1 launders the rest; the two NEW kits are sim-legible by construction — **大哥 is the one to
watch.**

---

## Player counts & scaling

Base = **2p** (the design home). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Ladder slots** | 4 | 5 | 6 |
| **Beverage Row slots** | 2 | 2 | 3 |
| **Buzz supply** | ~24 | ~32 | ~40 |
| **Dusk mark (ladder wins)** | 4 | 5 | 6 |
| **Last-train mark (ladder wins)** | 7 | 9 | 11 |
| **Market deck size** | base | +1–2 each | +2–3 each |
| **Buzz majority rule** | ≥2 over the rival | **≥2 over the *highest* rival** | ≥2 over the highest rival |
| **Start positions** | opposite (N & S) | spread on the ring | spread |

At 3–4p the Buzz majority is **≥2 over the highest single rival**; 大哥's tie-win becomes **≥0 over the
highest rival** — flag its 3–4p balance to `bg-architect` + sim. The **drinks fork gets relatively stronger
at higher counts** (the ladder is more contested, so the low-conflict escape hatch is more valuable) — watch
that drinks don't over-perform at 4p (knob: hold the Beverage Row narrow). **Best-at: 2p.** 25 vendors is
comfortable at 2p; 3–4p may want a few more per venue type (→ `bg-architect`).

## Solo mode / Automa

**Medium priority.** Sketch — a **"Rival Agency" Automa**: a small **Route deck**; on its turn it
**Promotes** (drops Buzz on the highest-Prestige contested **Ladder** vendor in a rotating focus region),
**Bribes** (if it holds a ≥2 majority + can pay — locks it, advances the clock), **sources**, or **rotates**
its focus. It **ignores the Beverage Row** (the drinks fork is the human's escape hatch; the Automa applies
ladder pressure). Its Buzz is real and contests *your* ladder majority. Pressure = the Buzz race + the
day-clock. **Defer to `bg-architect`; not in the base MVP.**

## Complexity budget

Target **~2.4–2.5, ceiling 2.5** — **still holdable, now with more headroom** (the 10→5 palette cut is a
real bank). `complexity-budget.json` caps (rulebook 1650 words, keywords 15, component types 8, aid 22
lines); `bg-elegance` guards.

**The weight call (honest).** v6 **banks** the palette cut (fewer ingredient token types, fewer card icons,
a shorter aid, a smaller BOM) and **spends** one new concept (the all-day Beverage Row) + one rule clause
(drinks don't tick the clock). Net **~2.4–2.5** — the same band v5 held, with the component/cost gauges
reading materially lighter (fewer ingredient types → the `type`-column artifact that inflated
`component_types` shrinks too).

**Keywords ≈ 12** (under 15): Larder · Vendor · **Bribe** · **Buzz** · **Promote** · region **discount
icon** · **Prestige** · **Reputation** · **★ Star** · **market deck** · signature **Mission** · **day-clock
/ Act**. (Visit / Convenience Store / Travel / Ladder / Beverage Row / the three venue types / common /
signature / last train home stay plain-language — the venue types and the two board zones are *named board areas*,
not new rules keywords.)

## Keywords / glossary

- **Larder** — your sourced ingredient cards, **face-up**. Cap **7**.
- **Vendor** — a Board card you **Bribe** to secure. One of three **venue types**: **breakfast shop 早餐店**
  (Act I Ladder), **night-market stall 夜市攤** (Act II Ladder), **beverage shop 飲料店** (persistent,
  region-free Beverage Row). Carries an ingredient cost, a region **icon** *(ladder only)*, **Prestige**,
  **Reputation**, a **perk**, and the **Buzz piled on it**.
- **the Ladder** — the contested, region-gated, clock-driving zone of the Vendor Board; cycles from
  breakfast shops (Act I) to night-market stalls (Act II) at dusk.
- **the Beverage Row** — the small persistent, region-free, off-the-clock zone; drinks, always available.
- **Bribe a Vendor** *(LOCKED keyword)* — the core action: with the vendor, holding a ≥2 Buzz majority (≥0
  for 大哥), pay its ingredients (− discount) to win it. **A ladder Bribe advances the day-clock +1; a
  beverage Bribe does not.** Carries the binding warm reframe (*"a marketing opportunity, not a bribe"*).
- **Buzz** — the committed, public, contested resource; **Promote** to place it on a vendor you're with;
  never discounted; clears to supply on a win. The interactive anti-runaway brake.
- **Promote** — the action that places 2 Buzz (3 for 網紅) on vendor(s) you're with.
- **discount icon** — a **ladder** vendor's region badge; each held reduces that region's ingredient cost on
  future vendors by 1 (floored at 0). The compounding engine (ingredients only; **beverages carry none**).
- **Prestige (VP)** — a vendor's value; the headline VP vector; live on the track.
- **★ Star** — a value hook on a standout **ladder** vendor: **printed** on an apex "Legendary" 夜市攤 (a
  standing Michelin/Bib-Gourmand/competition accolade, 7–8), or a **Star token** dropped mid-game by a
  "vendor gets hot" boon (+2 Prestige / +1 Rep; token returns on the win). The deliberate value swing on the
  ladder road.
- **signature ingredient** — a region's one specialty (N/C/S/E). **common ingredient** — the fifth, shared
  ingredient the drinks fork + Convenience Store run on (in two of the four regions).
- **market deck** — a region's face-down deck of its signature (+ common, in two regions) + events; **Visit**
  draws 3 keeps 2 (hazards fire); **Convenience Store**/**Travel** draw 1 (whiff, no fire).
- **signature Mission** — your secret **+7** vendor pattern (draw-3-keep-1); the only hidden info; carries
  the grand-tour breadth line and the *"3 beverage shops"* drinks line.
- **day-clock (the Act track)** — the marker that climbs +1 on every table-wide **ladder** Bribe (never a
  beverage one); at **dusk** the Ladder flips to the Night-Market deck (Act I → II); at the **last-train**
  mark **night falls, the night market winds down** and the game ends.
- **the last train home** — the end-game: when the day-clock hits the last-train mark, finish the round +
  one full round → reveal missions → score. (Day → Night arc; no named alarm — was "Code Red" in v5.)

---

## Riskiest assumptions & the top-3 open questions for playtesting

**The single riskiest cluster:** **the Buzz-majority tug-of-war is fun/tense (not a slap-fight or
snipe-degenerate, and 大哥 doesn't dominate it) AND the new drinks fork is viable-but-not-dominant.** The
first is carried from v5; the second is v6's headline new risk.

**Top 3 open questions (in priority order):**

1. **Is the Buzz fight fun/tense and non-degenerate — including under 大哥? (Carried make-or-break.)**
   *Attack:* Buzz-war frequency/depth; "snipe-only" win-rate (≤~55%); loser's-tempo cost; supply pressure
   (~24?); 大哥's win-rate at ≥0 vs ≥1 with the tab vs Promote-1. *Fixes:* the ≥2 margin (→≥1/≥3),
   Buzz-per-Promote, supply size, a partial loser-refund; for 大哥, threshold + flaw.
2. **Is the drinks fork a real choice — viable but not solved? (THE v6 make-or-break.)** *Attack (sim +
   table):* **drinks-lean vs ladder-lean win-rate** (each ≤~55%; neither a trap nor a solved line);
   **pure-drinks win-rate** (should clearly *lose* to a good ladder line — confirming the ceiling gap);
   **the crossover turn** (when does a ramped ladder pull ahead of flat drinks?); **drink-fight frequency**
   (should stay low — confirm the emergent low-conflict). **(2b) Pacing:** does a drinks-heavy line make the
   game **drag** (clock starved)? Check turns-to-Code-Red across ladder-heavy vs drinks-heavy fields; the
   deck backstops should cap it. *Fixes:* beverage Prestige value, beverage deck/row size, whether drinks
   give Rep, the common's availability (every-vs-half), the day-clock marks.
3. **Does the 5-ingredient dig stay a real decision, and does movement still spread?** *Attack:* **the
   market-dig "flatten" check** — is *where to Visit* still driven by need, or does everyone dig anywhere?;
   **hazard-hit rate per Visit**; **per-region sourcing share** (each ≥~18%; the two pure-signature regions
   not starved); **inter-region moves/game**; **Convenience-Store vs Visit usage** (drinks players lean
   Convenience Store). *Fixes:* hazard density, the cross-region rate on night-market recipes, the common's
   spread, the "brewing" telegraph knob — **not** adding ingredients back.

*(Secondary: per-character 45–55% with the two NEW kits (大哥 the one to watch); the two-Act day-clock
pacing landing ~5–6 wins/player in ≤30 min; mission patterns achievable in the shorter game, incl. the two
"3 of a venue" lines given the venue counts.)*

---

## → Open numbers for the gated sim to tune (once the CD approves — DO NOT run yet)

**Palette & the fork (the v6 additions):**
- **Ingredient count: 5 vs 4** — recommended **5** (one signature per region + one common); a 4-palette (3
  signatures + common) is the fallback only if 5's dig proves too heavy (unlikely). *Which region loses its
  signature at 4 is the awkward part — hence the 5 rec.*
- **Common availability: HALF (2 regions) vs EVERY region** — recommended **half** (travel value + texture);
  the top fork knob — **widen if the drinks engine proves non-viable.** Also: the common's **per-deck share**
  in the two carrying regions (Convenience-Store yield reliability).
- **Beverage point value (proposed 2 flat)** — the master fork knob; too high = drinks dominate, too low =
  drinks are a trap.
- **Beverage deck size (~6–7) + Beverage Row width (2 @2p)** — the drink-points hard cap.
- **Do beverages give Rep? (proposed +1)** — and do they carry any perk (proposed none). Either lever, if
  raised, can tip drinks toward dominance.
- **Does the ladder still reward travel over the drinks grind?** — confirm ladder-lean and drinks-lean both
  land ≤~55% and a *mix* is the strongest line; confirm pure-drinks clearly loses.

**Pacing & clock:**
- **Day-clock marks: dusk 4 / last train 7 (ladder wins @2p)** — do we land ≤30 min / ~5–6 vendors/player?
- **Does beverages-off-the-clock make the game drag** with a drinks-heavy field? (Backstops sufficient?)

**Carried from v5 (still live):**
- **Buzz supply size** (~24 @2p): too tight vs too loose?
- **大胃王 flaw magnitude:** hazards-fire-twice vs the lighter alternates.
- **大哥 threshold** (≥0 vs ≥1) and **flaw** (tab vs Promote-1) — the dominance probe.
- **Ladder slot count** (4 @2p): fewer = sharper head-to-head fights.
- **Vendor value spread:** apex 夜市攤 value (7–8), ★-printed count (2–3), Star-token bonus (+2/+1), the
  "gets hot" event count (1–2) + targeting. Do agents cross the island + burn Buzz for the ★ vendors? Does
  the swing stay fun, not luck-decides?
- **Character win-rate targets:** each **45–55%**, no dominant char×mission combo.
- **Mission thresholds** for the shorter game (grand-tour, 5-vendor, ≥12-Prestige, and the two "3 of a
  venue" lines).

---

## Decision for the Creative Director (the live design calls)

Everything structural is locked by the CD's v6 brief and this doc's implementation. The genuine A/B/C calls
the CD may want before the sim (all also sim-tunable — the CD can defer any to "let the sim pick"):

**H1 — 大胃王's flaw** *(carried from v5).* **A.** Hazards fire *twice* (proposed; simplest; may over-brake).
**B.** On a Visit where any hazard fires, keep only 2 (elegant, self-scaling). **C.** The next hazard also
fires (lightest). *Rec: ship **A**, keep **B** as the go-to if A over-brakes.*

**H2 — 大哥's threshold + flaw** *(carried from v5).* **A.** Tie-win (≥0) + the +1-ingredient tab (biggest,
funniest, highest-risk). **B.** Tie-win (≥0) + Promote-places-1 (harder brake). **C.** Must-lead-by-1 (≥1) +
the tab (smaller edge). *Rec: ship **A**; fall to **B** then **C** if 大哥 dominates.*

**H3 — the common's availability (the one NEW v6 call).**
- **A. Common in HALF the regions (2 of 4), concentrated.** *(this doc's rec.)* Protects travel value + gives
  the smaller palette texture variety; the drinks player targets those two decks via the Convenience Store.
- **B. Common in EVERY region.** Maximises the drinks engine's reliability (Convenience Store never picks a
  common-less deck) at the cost of some travel value and some signature-dig dilution everywhere.
- **C. Common in half, but at a HIGHER per-deck share.** A middle option if half-at-normal-share proves too
  slow for the drinks engine but every-region flattens travel too much.
> *Recommendation: ship **A** into the sim; it's the cleanest fork + travel balance. Fall to **C**, then
> **B**, only if the sim finds the drinks engine non-viable (too slow to source the common).*

---

## Handoff notes (guardian sweep — where to look)

**v6 — what moved (run `bg-theme` coherence + `bg-elegance` budget on the change):**
- **The signature twist is UNCHANGED in shape** (public on-site Buzz-majority fight for engine-piece ladder
  vendors) — but the **economy layer around it restructured**, so `bg-theme` should check: **(1)** the
  **drinks fork** — does the all-day, region-free 飲料店 "easy points" road read as warm and native (the
  very-Taiwan 手搖飲 stand on every corner), and does keeping the ★/contest off it feel right, not like a
  demoted second-class food? **(2)** the **venue-type rename is now fully mechanical** (breakfast = Act I
  ladder; night-market = Act II ladder; **beverage = off-clock persistent row**) — confirm the identity's
  "value band = time of day, not a food-class ladder" binding still holds when beverages are literally
  pulled *off* the day-clock (they're "all day", which reads correctly — but sanity-check). **(3)** the
  **common ingredient** needs a locked name (繁體/Tâi-lô) — bg-theme's call; propose 糖 sugar/syrup or 鮮奶
  milk, the drinks-and-convenience staple; confirm it's real, secular, not tied to a sacred motif, and that
  putting it in only two regions reads honestly (propose its real production home). **(4)** the **Act I
  rename** "Afternoon Crawl" → **"The Breakfast Run 早餐"** (bg-theme's rec; alts "The Day Crawl" / "Daytime
  白天") — applied here; confirm the label. **(5)** the **"Code Red" end-trigger flavour is DROPPED** (CD
  directive) → the plain **Day → Night** arc ("night winds down → last train home"); identity.md still says
  "Code Red" — **bg-theme to strip it in the guardian re-check** (I did not touch identity.md).
- **`bg-elegance` check:** the **10→5 palette cut** should read materially lighter on the component/cost
  gauges (fewer ingredient token types; the `type`-column artifact shrinks). Net weight ~2.4–2.5; keyword
  count ~12. The two NEW ideas to weigh: the **Beverage Row** (one board zone) and the **"drinks don't tick
  the clock"** clause. Guard the rulebook word count — and note the editorial fix below is now done.
- **Editorial fix (DONE this pass, per the v5 elegance flag):** the **"Still to specify → bg-developer" TODO
  block** and the **provenance/version blockquote** have been **moved OUT of `rules-draft.md`** into this
  design-doc (the dev-TODO is folded into `bg-developer` below; provenance lives in this doc's header) so the
  laid-out rulebook's word count reads true.
- **`bg-access` / `bg-infodesign`:** the vendor card now shows a **venue-type badge** and the board has **two
  labelled zones** (Ladder / Beverage Row) — a new at-a-glance read to dual-code. Fewer ingredient icons (5
  not 10) *helps* legibility. Keep dual-coding on region colours + emblems.

**`bg-developer` (AFTER CD sign-off — not yet) — the v6 build TODO (moved here from rules-draft):**
- **Re-cost to the 5-ingredient palette** (4 region signatures + 1 common; retire the wild "pantry" token) —
  see *Economy → the re-cost brief* for the region map, the common-in-two-regions rule, and the per-venue
  cost principles (breakfast 1–2 signature; night-market 2–3 cross-region; beverage 1–2 common, region-free,
  no icon; ~40% night-market cross-region; keep the common a minor filler in some ladder recipes; cap North's
  signature demand).
- **Re-sort the 25 vendors by venue *identity*** into the **three decks**: **Breakfast Shops 早餐店** (~10, Act
  I) · **Night-Market Stalls 夜市攤** (~8–9, Act II; build the value curve — ordinary 5–6 + **2–3 apex
  "Legendary" at 7–8 with a printed ★**) · **Beverage Shops 飲料店** (~6–7, the persistent Beverage Row,
  Prestige 2 flat, +1 Rep, no ramp icon). Add real dishes per band if short; more per band at 3–4p.
- **Board printing:** the **day-clock** (dusk + last-train marks), Prestige + Reputation tracks, and the
  **two-zone Vendor Board** — a **Ladder** (Act-cycling, region-gated, with Buzz zones) + a persistent,
  **region-free Beverage Row**. Four market-deck spaces. No Coverage scoring key (cut in v5).
- **Rebuild `events.csv`** (~14; hazard-leaning; in-deck; ~2 hazards/deck + table-wide ones). Include the
  **"vendor gets hot" boon** (摘星了／得獎了／爆紅) targeting a **Ladder** vendor + **~4 ★ Star tokens** (+2
  Prestige / +1 Rep, recyclable). Re-home orphaned perks: **wild_pantry → wild_specialty**; add the
  **Buzz-reach** night-market perk.
- **Bake the five v5 characters** (unchanged by v6): **里長伯 / 媽寶** (KEPT kits re-lored) · **網紅**
  (Promote 3; go last + behind) · **大胃王** (Visit keeps all 3; flaw = the CD's H1 pick) · **大哥** (wins at
  the CD's H2 threshold; flaw = the CD's H2 pick).
- Size the **Buzz supply** (~24 @2p; +8–10/player). Set the **day-clock marks** (2p: dusk **4** / last
  train **7**) — sim-tunable. Re-tune **mission thresholds** for the shorter game (incl. the new *"3
  beverage shops"* line; ≥12-Prestige).
- **Player-aid** (≤22 lines): the five actions + the Bribe requirements + **the ladder/beverage split (the
  clock-tick clause)** + the two scoring vectors + the mission +7 + the day-clock (dusk / last train home)
  rule.
- **Iconography:** 5 ingredients + 4 regions + a **venue-type badge** + the vendor-card layout (cost / region
  icon *(ladder)* / Prestige / Rep / perk / Buzz count / venue type), dual-coded (`bg-access` /
  `bg-infodesign`).

**`bg-playtest` (GATED — DO NOT run until the CD signs off):** rework `sim/travel_agents.py` to model the
**5-ingredient palette**, the **two-zone board** (Ladder + region-free Beverage Row), the **ladder-only
clock**, and the **drinks fork**; then run the three probes, **leading with Riskiest #1 (the Buzz fight,
incl. 大哥) and #2 (the drinks-fork viability/dominance + pacing).**

**Cut mechanics to sweep for stranded names/rules:** **Extract**, **Poach**, the **wild "pantry" token** (now
retired into the common), **the Season counter**, **the three value-bands-on-two-decks framing**, **the
Region-Coverage scoring track**, **event tiles / the face-up Market**, the **v4 character cast**, and the
**"Code Red" end-trigger label** (now the plain Day → Night arc). Also sweep for any lingering **"Stall /
Eatery / Marquee"** or **"~10 ingredients / pantry"** references — v6 renames the bands to venue types and
cuts the palette to 5.

> **Sweep tracker for the coordinator (design-side is clean; data-side is pending bg-developer, gated):**
> the **design-doc + rules-draft now carry ZERO live "Poach" and ZERO live "Code Red" references** (both
> appear only in cut/provenance notes). Still outstanding when `bg-developer` rebuilds data (sim gated):
> **`components/*.csv` and `sim/travel_agents.py` still need a Poach sweep** (and the same v6 sweep for
> Stall/Eatery/Marquee, the ~10-ingredient/pantry palette, and any "Code Red" strings). identity.md's
> "Code Red" is bg-theme's to strip in the guardian re-check.
