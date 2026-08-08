# Travel Agents: Taiwan — Design Doc

> ## 🔒 CURRENT DESIGN = v6.3 — **SHAPE LOCKED 2026-08-07** (CD sign-off on all nine items). See **`design/v6.3-content-draft.md`** for the authoritative current *shape*.
> **Balance is PENDING a gated re-sim.** v6.3 gives **Reputation teeth** (a live cap on committed Buzz;
> earned by Travel + events, **not** vendors; **it no longer scores**; and a small **Rep-sink** set —
> greed/corner-cutting cost Rep), adds **milestone boons** on the (renamed) **Bookings** track (marks 7/14,
> Set A "Tempo & Fuel", first-to-cross), **eliminates the perk field** (a vendor = Bookings + icon-or-not;
> table reissued), collapses **ticket pools 3→2 (DAY/NIGHT)**, and confirms **per-player win/lose piles**
> (COMPLETED 成團 / CANCELLED 取消). New tiebreak: **most vendors → most regions → fewest LOSE-pile tickets.**
> **⚠ Change 1 is NOT sim-equivalent — a combined re-sim (Changes 1+2+3) is REQUIRED and GATED on the CD's
> explicit "go."** **Until that run validates the numbers, `design/v6.2-content-draft.md` remains the last
> SIM-VALIDATED build.** Do not rebuild the CSVs or the sim module before the re-sim. Full v6.3 shape +
> the open sim knobs: `design/v6.3-content-draft.md`; the options + rationale: `design/v6.3-proposal.md`.

> ## ✅ PRIOR SIM-VALIDATED BUILD = v6.2 — **LOCKED 2026-08-07** (CD sign-off, sim-validated). See **`design/v6.2-content-draft.md`**. (Superseded in SHAPE by v6.3 above; remains the balance baseline until the v6.3 re-sim.)
> The detailed text below is **v6.1, retained as history/reference.** v6.2 (co-designed 2026-08-07; sim run +
> CD locks at the top of `decision-log.md`) **supersedes** several v6.1 structures and the sections below
> that describe them:
> - **Central Ladder → region vendor MARKETS.** No central Ladder. Each of the 4 regions has its own
>   face-down **vendor pile** (daytime stacked on nighttime), **1–2 face-up per region** (North 2, others 1),
>   refilled in place.
> - **The ladder-vs-drinks FORK is GONE, and beverages are no longer off-clock / region-free.** There is now
>   **one kind of vendor**; **drinks are simply the low-value vendors** mixed into each region's pile, courted
>   by the same one rule (on-site + ≥2 Buzz majority + pay).
> - **The single secret +7 mission → "Tour Tickets".** A **face-up row of 3**, claimed as an action, from
>   **daytime / nighttime / general** pools (12 per phase in the box, **5 drawn per phase per game**). **Scored
>   via a WIN-PILE / LOSE-PILE model (CD lock):** a ticket is judged **at the end of its phase** (daytime at
>   dusk, nighttime at the last train) — **completed → WIN pile, unfinished → LOSE pile** — and points are
>   tallied **once at game end**: **Σ(win-pile values) − Σ(floor(value/2) per lose-pile ticket)**. The −½
>   penalty is KEPT; its reading is locked as *half the ticket's own value, rounded down*. **This is
>   accounting-only and SIM-EQUIVALENT** — the same final scores the v6.2 sim's retroactive `+v / −floor(v/2)`
>   produced, so it changes **no** balance and needs **no** re-sim. *(Naming the two piles → bg-theme /
>   bg-infodesign, e.g. "published tours" vs "the ones that got away.")*
> - **The clock → the VENDOR-CLAIMS clock (CD lock; the mission-clock A/B is CLOSED).** The day advances
>   **as vendors are claimed** — **dusk = the 5th table-wide vendor claim, the last train = the 10th @2p**;
>   the marks GROW with player count (bg-architect finalizes with the MP pass); deck-exhaustion backstops end
>   a phase if decks dry island-wide. At **dusk the whole day layer flips** (both day vendor + day ingredient
>   decks cleared island-wide → night decks, event-heavier; Larder kept). Chosen over the mission clock
>   because it was tighter and more reliable (sim sd 3.9 vs 4.9, crisp mid-game dusk turn ~21 vs ~34, ~14% vs
>   26% stall).
> - **Character kits LOCKED (CD, from the sim):** **大哥 = lead-by-1 (≥1 Buzz margin, not ≥2), NO flaw**
>   (51.7%; tie-win dropped); **媽寶 = keep-2 on a Visit** (45.6%; the keep-1 flaw dropped); **大胃王 = H1-A,
>   hazards fire twice on his Visit** (52.6%); **網紅 = Going-Viral (+1 Buzz on Promote) + "misses its first
>   turn of the night phase"** (CD refinement — a concrete lost-turn flaw replacing "starts behind"; **a KEY
>   table balance-check, may over-correct**; dial in reserve); **里長伯 unchanged** (51.8%). Full kit table +
>   dials in `design/v6.2-content-draft.md`.
> - **Design target = the FIVE playstyles** (character-lean · opportunistic · disruptive · balanced ·
>   end-game-driver) all viable, none >~55% — **sim PASS** (43–53% band; a well-timed MIX crushes the
>   ignore-both control at 73%; pure-drinks is dead at ~0.5%).
> - **📦 FOR bg-developer (the v6.2 data rebuild — gated component work):** rebuild `components/*.csv` +
>   `player-aid.json` from the v6.2-content-draft (the CSVs are stale pre-v6 — do NOT render them). Build the
>   **per-region day/night vendor decks** (drinks marked low-value, ★ apex marked, cross-region costs marked),
>   the **Tour Tickets** (day/night/general; each carries its value; the win/lose-pile is a *scoring/handling*
>   rule, not per-card data), the **per-region day/night ingredient market decks** (5-palette, event-heavier
>   night, scoped events ⦿/⬢/➤), the **four character mats** to the locked kits above, the **Buzz supply**,
>   and the **vendor-claims clock track** (dusk + last-train marks). **DATA TWEAK (from the sim — not a rules
>   change): give Central tea an EXPORT.** Central is under-pulled (13% sourcing) because the cross-region
>   cycle makes it a pure importer (逢甲 needs S) — tea has no external demand, so nobody travels to *source*
>   it. Re-point one cross-region cost (an East or North night dish) to need **C tea**, closing the cycle into
>   a true four-region loop, mirroring how the other signatures export.
>
> **UNCHANGED from v6.1 (still binding, read below):** the **Buzz-majority public hype-fight**, the
> **5-ingredient palette** (N 豬肉 · C 茶 · S 海鮮 · E 米 + common 糖 in C & S), push-your-luck ingredient
> **market decks** with **scoped events** (⦿/⬢/➤, fire on Visit + Convenience Store, whiff on Travel), the
> **five characters** (里長伯/媽寶/網紅/大胃王/大哥), the **★ value swing**, the Prestige/Reputation vectors,
> the **Day→Night → last-train** arc, and **all sensitivity rails**. v6.2 is a board/objective restructure,
> not a new spine. This banner + `design/v6.2-content-draft.md` are the LOCKED v6.2 canon; the v6.1 body
> below is history where it conflicts.

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.
*(The v6.1 body follows — treat it as history where it conflicts with the v6.2 banner above.)*

**Provenance for v6.1 (read this first — two CD corrections folded into v6).** v6.1 folds in **two CD
corrections to the v6 economy fork** (design-only; no sim, no data/CSV edits):
1. **Convenience Store events now FIRE, resolved by a SCOPE.** v6 had a Convenience-Store draw *whiff*
   on an event ("shelf was picked clean"). It now **fires** the event, resolved by a small dual-coded
   **scope tag** (⦿ self / ⬢ region / ➤ next-door) that decides who it hits — so a Convenience-Store
   draw can now boon *or* hazard **other** players. This **unifies Visit and Convenience Store into one
   event system** (every event carries a scope and resolves per that scope, relative to the region it was
   drawn from) and injects the light interaction / vendor-contest an early sim read found missing.
2. **Beverages are REGION-ANCHORED, not a region-free central Row.** v6 wrongly modelled beverages as a
   persistent region-*free* "Beverage Row" you could Promote/Bribe from anywhere. Corrected: **one
   unified Bribe rule for all vendors** — you must be **in the region** to Promote/Bribe a beverage shop,
   same in-region + ≥2-Buzz-majority rule as any vendor. The central Beverage Row is dropped; **each
   region has its own persistent beverage slot** (a drinks stand in *every* region, all day). The
   low-travel fork identity now comes from **ubiquity + easy sourcing** (a stand where you already stand;
   糖 from the Convenience Store anywhere), **not** bribing-at-a-distance. Everything else about beverages
   is **unchanged**: cheap / low value / low conflict, **OFF the day-clock**, **no region-discount ramp**,
   fed by the common 糖.

**Provenance (the v6 base below this line).** The mechanical spine is the **v4 Buzz-majority / push-your-luck
rework** (committed public Buzz on vendors, face-down market decks, Extract + Poach cut). **v5** tightened
it to a **≤30-minute two-Act "one glorious eating day"** on a single **day-clock**, cut Region-Coverage to
a Mission, added the **★ Star value swing**, and re-cast the five characters as Taiwanese social types.
**v6 folds in the CD's LOCKED economy-fork direction** (this doc's brief) — it **supersedes v5's
"three value-bands dealt across two Act decks" + "~10-ingredient palette" framing**:

- **The day-clock is TWO beats, not a three-band ladder.** **Act I · The Breakfast Run 早餐** (breakfast
  shops 早餐店, the morning opening) → **Act II · Night Market 夜市** (night-market stalls 夜市攤, the
  climax; the apex ★ vendors live here). **Beverage shops 飲料店 come OFF the clock** — persistent, "all
  day," with **one stand in every region** *(v6.1: region-anchored, not region-free)*.
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
| **Beverages as a mid-rung of the ladder** | **Beverages as a parallel FORK** — common-fed, off-clock, low-conflict (one new idea: a persistent beverage stand in every region — *v6.1 corrected this from the mistaken region-free central Row*) |
| **"day-clock climbs on every Bribe"** | **"day-clock climbs only on ladder Bribes"** (+1 rule clause — the fork's engine) |

**Honest weight call.** The palette cut (10→5, drop the wild pantry) is worth more than the fork costs:
fewer ingredient types = fewer icons on cards, a shorter player-aid, a smaller bill of materials, and a
dig that's easier to parse. The fork adds **one new concept** (the region beverage slots) and **one rule
clause** (drinks don't tick the clock). Net **~2.4–2.5, at/under the 2.5 ceiling** — the same band v5 held,
with more of it banked. `bg-elegance` re-reads (the component gauge should now read materially lighter).

### What v6.1 changed on top of v6 (the delta ledger for `bg-elegance`)

Two CD corrections. The net is **roughly weight-neutral** — one addition (the event scope) is paid for by
one removal (the region-free-beverage special case).

| Cut / banked (−) | Added / spent (+) |
|---|---|
| **The "beverage vendors are region-free — Promote/Bribe from anywhere" special case** → **ONE unified Bribe rule** (all vendors: on-site + ≥2 majority). A real simplification — the rulebook stops carrying a vendor-type exception on Promote and Bribe. | **The event scope tag** (⦿ self / ⬢ region / ➤ next-door) — **one small concept, three icons**, that lets a single event system resolve on both Visit and Convenience Store. |
| **The old carve-out "events fire only on Visit; a Convenience-Store draw whiffs"** (partial — CS now fires; only Travel still whiffs). | **Convenience Store now fires events by scope** — a live, slightly-risky sourcing action instead of a purely safe one; injects the vendor-contest / take-that an early sim read found near-zero. |
| **The single central "Beverage Row" component** (one board zone). | **A per-region beverage slot** on each of the four regions (fed by the same one Beverage deck) — no net new *deck*, just where the drinks stand physically sits (in every region, reinforcing "always open, everywhere"). |

**v6.1 weight call.** The unified Bribe rule is a genuine simplification (one fewer exception to teach);
the event scope is a bounded 3-icon concept that *replaces* the old "does it fire?" carve-out with a
richer "who does it hit?" read — and buys the missing interaction. Net **still ~2.4–2.5**. The one real
watch is the same one `bg-elegance` already flagged on v6: **rulebook prose is over its word cap** — the
scope block and the unified Bribe rule must be written *tight* (one compact scope block, one Bribe rule
that no longer forks by vendor type — the latter should *shorten* the Bribe/Promote prose). Flagged in the
guardian handoff.

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
  win the Buzz fight for a big night-market name) — or bank an easy drink at the stand right where I stand,
  fed by the common off the convenience store?* And within the ladder: *dig now (risk an event), aim a
  Convenience-Store draw at a common region (or at my rival's region, to drop a scoped hazard on them),
  travel on, pile more Buzz, or close the Bribe before my rival out-hypes me?* No forced move.
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

1. **Read the board.** Every vendor is **region-gated** — you must be **on-site** (standing in its region)
   to Promote or Bribe it. There are two kinds of vendor space:
   - **The Ladder** (the contested, clock-driving central display): breakfast-shop vendors in Act I,
     night-market vendors in Act II — each with its ingredient cost, its **region icon**, its
     **Prestige/Rep/perk**, and **the Buzz both agents have piled on it**.
   - **The region beverage slots** (the persistent, off-clock drinks stands): **each of the four regions
     has its own beverage slot** (a face-up beverage shop), fed by the common Beverage deck and **never
     swept** — a drinks stand open in every region, all day. You court the one **in the region you stand
     in**.
   Your secret **signature mission** points at a vendor pattern worth **+7**. The four **region market
   decks** are face-down (you know each region's signature + that hazards lurk). Your **Prestige** and
   **Reputation** markers show your two live vectors; the **day-clock** shows how close the day is to dusk
   (Act II) and to the **last train home** (the end of the night).
2. **Take one action:** **Visit the Local Market**, **Convenience Store**, **Travel**, **Promote**, or
   **Bribe a Vendor**.
3. **Sourcing digs the market; the island reacts.** *Visit the Local Market* (your region) flips the top 3
   of that region's deck: any **event** fires on the spot (**by its scope** — see below), then you keep up
   to **2** of the **ingredients** you turned up — the push-your-luck spine, the way you bulk-source
   **region signatures**. *Convenience Store* takes a single blind top card from **any** region — an
   ingredient you take, or **an event that fires by its scope** (v6.1: no longer a whiff — it can now boon
   *or* hazard whoever the scope points at, including a rival). The safe-ish, no-travel way to source the
   **common** ingredient the drinks engine runs on. *Travel* takes a single blind top card on arrival (an
   event there is still just a whiff — you're passing through, not working the market).
4. **Buzz is a public fight — you must be on-site.** *Promote* places Buzz onto vendor(s) you're with **in
   your current region** — a ladder vendor and/or your region's beverage slot. You can only **Bribe** a
   vendor when you are **with it (in its region)**, hold **≥2 more Buzz on it than your rival**, and can
   **pay its ingredients** (minus discounts). One unified Bribe rule for every vendor type. Winning clears
   all its Buzz to the supply and scores you Prestige + Rep + its perk.
5. **The two roads diverge on the clock.** A **ladder** Bribe (breakfast or night-market) **advances the
   day-clock +1** — it is *progress*, and it hurries the end. A **beverage** Bribe scores you easy points
   but **does NOT advance the clock** — it is *parallel*. When the day-clock reaches **dusk**, the Ladder
   sweeps and re-stocks from the **Night-Market deck** (the region beverage slots are **not** swept); at
   the **last-train** mark, **night falls / the night market winds down** → finish the round + one full
   round → reveal missions → score.

The **ladder** compounds legibly and with a brake: each ladder vendor makes a *class* of future vendors
cheaper in **ingredients** (the ramp) — but every one still demands you **win an undiscounted,
region-gated, contested Buzz majority**, on-site. The **drinks** road does *not* ramp — it's a flat,
reliable, **low-travel** trickle of easy points (low-travel because a stand is open in *every* region, so
you court the one where you already stand, and the common comes off the Convenience Store from anywhere).
That asymmetry **is** the fork (see *The drinks fork*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** — 4 regions on a ring: **North 北 – Central 中 – South 南 – East 東**; an
  **HSR** spine links North↔South down the west coast. The board carries the **day-clock** (the Act track,
  with a **dusk** and a **last-train** mark), the **VP (Prestige) track**, the **Reputation track**, the
  central **Ladder** display, and — **per region** — a face-down **market deck** zone **and a persistent
  beverage slot** (a drinks stand in every region).
- Build the **four region market decks**: each = its **one signature ingredient** (several copies), **the
  common ingredient** *(in the two regions that carry it — see Economy)*, **+ 3–4 event cards**
  (hazard-leaning, each carrying a **scope tag** — see *Events*), shuffled face-down.
- Build the **three vendor decks** from the 25 vendors (re-sorted by venue — see *Vendors*):
  - **Act I deck = the Breakfast Shops 早餐店** (~10), shuffled.
  - **Act II deck = the Night-Market Stalls 夜市攤** (~8–9), shuffled — set aside face-down until dusk.
  - **Beverage deck = the Beverage Shops 飲料店** (~7–8), shuffled — feeds the **four region beverage
    slots**.
- Deal the **Ladder** from the Act I (Breakfast) deck (2p: **4 slots**). Seed **one beverage shop face-up
  into each region's beverage slot** from the Beverage deck (4 dealt @2p, one per region). Set the
  **day-clock** marker to 0.
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
| **Visit the Local Market** | your current region | Reveal the top **3** cards of this region's market deck. Resolve **any event** revealed immediately (**it fires by its scope** — see *Events*), discard them. Keep up to **2** of the revealed **ingredients** (to your Larder); discard the rest. | The ingredient workhorse **and** the push-your-luck spine — the way you bulk-source your **region signature**. More events = more swing. *大胃王 keeps all 3; 媽寶 keeps only 1.* |
| **Convenience Store** | anywhere | Reveal the **top 1** card of **any one** region's market deck. Ingredient → take it. **Event → it fires by its scope** (⦿ self / ⬢ the drawn region / ➤ a neighbour of it — see *Events*). | **The drinks engine's spine** *and now a light interaction lever.* No travel, any region — the reliable way to grab the **common**; aim it at a common-bearing region. **v6.1: live-but-slightly-risky** — the drawn card can be an event, which now *fires*: a self-scoped one taxes **you**, but a region/neighbour-scoped one can drop a warm island-hazard (or boon) on **whoever is standing there** — including a rival whose region you flip. One blind card. |
| **Travel** | to an adjacent region | Move your Agent to an **adjacent** region (HSR: North↔South counts adjacent); then reveal the **top 1** card of the **arriving** region's deck (ingredient → take it; **event → whiff, nothing fires** — you're passing through, not working the market). | Never a dead turn — you (usually) arrive with something. *媽寶 draws the region she LEFT instead. (v6.3.1: 里長伯's no-HSR flaw is REMOVED — HSR closure is now the table-wide "Scheduled Maintenance" event.)* |
| **Promote** | your current region | Place **2 Buzz** from the supply onto **vendor(s) you're with in this region** — a ladder vendor here and/or **this region's beverage slot**. Buzz stays on the card, public; the rival may also Buzz it. | The Buzz-placement action, **on-site for every vendor type** (v6.1: no beverage exception — you Promote the drinks stand where you stand). *網紅 places 3 (+1). 大哥's alternate flaw = places 1.* |
| **Bribe a Vendor** | **in its region** (all vendor types) | Choose a Board vendor **you're with (in its region)** on which you hold **≥2 more Buzz than your rival**; **pay its ingredients** (− region discounts, floored at 0). Take it to your tour → gain **Prestige** (VP live), a **Rep** bump, and its **perk**. **All Buzz on it returns to the supply.** Refill the slot from the matching deck; **the vendor is locked from the rival.** **If the vendor is a breakfast or night-market (ladder) vendor, advance the day-clock +1. A beverage Bribe does NOT advance the clock.** | The scoring beat — **ONE unified rule for all vendors**: presence + majority + ingredients. The clock-tick clause is the fork's spine. *大哥 wins at a tie (≥0), not ≥2; 大哥 pays +1 ingredient.* |

**Five actions, no conditional sixth.** (Poach and Extract are **cut**.) Every turn has multiple live
options with real trade-offs, including the top-level **which road** choice. No forced/obvious move.

**Two rules stated once, to keep the ruleset small:**
- **Events fire when you work a market (Visit or Convenience Store), resolved by their scope; a card merely
  flipped on a Travel fly-by whiffs.** You deliberately reach into a market (Visit's 3 flips, or the
  Convenience Store's blind grab) → the island reacts and the event fires by its **scope tag** (⦿ self /
  ⬢ region / ➤ neighbour). A card that just happens to be on top when you *arrive* on a Travel is "shelf
  was bare" — discarded, no fire. (This keeps mobility clean and protects the *never-a-dead-turn* Travel;
  whether Travel should also fire is a listed sim knob.) *v6.1 note: this replaces v6's "events fire only
  on Visit" — the Convenience Store now fires too, which is the whole point of correction 1.*
- **Buzz lives only in the supply or ON a vendor.** No private Buzz pool. You never "hold" Buzz; you place
  it, and it is either won-and-cleared or fizzled-and-cleared.

---

## The market decks & events (the push-your-luck sourcing layer) — now a 5-ingredient palette

- **Palette = 5 ingredients** (cut from ~10; the wild "pantry" token is retired, folded into the common):
  **one signature per region** + **one common**. See *Economy* for the region map and re-cost.
- **Four face-down region decks.** Each = its **one signature** (several copies) + **the common** *(only in
  the two common-bearing regions)* + **3–4 event cards** (each with a **scope tag**), shuffled. You know each
  region's signature (printed on the board) and that events lurk — you don't know the order.
- **Visit the Local Market** is the risk/reward: 3 flips, events fire (by scope), keep 2. If two of three
  flips are events, you keep only 1 (or 0) **and** resolve them — the genuine push-your-luck. **The
  Convenience Store** is the single blind draw that **also fires** an event (by scope) — lower variance than
  a Visit (one card, not three), but no longer risk-free. **Travel's** arrival flip is the only reveal that
  **whiffs** on an event (you're passing through).
- **Does a smaller palette flatten the dig?** No — the push-your-luck tension comes from the **hazards**
  eating your keep-slots, not from ingredient variety; that's untouched. And the decision of *where* to dig
  is still driven by which **region signature** your target vendor needs. What the cut removes is
  collection *breadth* (fewer distinct things), which we replace with **texture variety across regions**:
  the two common-bearing region decks read "signature + common + events" (a diluted, safer dig with a
  consolation prize), the two pure regions read "signature + events" (an all-or-nothing, higher-tension
  dig). *(This is a real risk to watch — see Riskiest Assumptions; the fix if it flattens is more/spicier
  hazards and a higher cross-region rate on night-market recipes, NOT adding ingredients back.)*
- **Events lean hazard (~55–60% hazard / ~40–45% boon across the pooled decks).** Warm-comedic,
  **tax-not-destroy** (a hazard delays, reroutes, or taxes tempo; **never** removes an ingredient you hold
  or costs a whole turn). The boon minority keeps a market-dig from being pure dread.

**The event scope tag (v6.1 — the ONE event system for both Visit and Convenience Store).** Every event
card carries a small **dual-coded scope tag** that decides **who it hits**, resolved **relative to the
region the card was drawn from** (for a Visit, that's your current region; for a Convenience Store, it's
whichever region's deck you flipped — possibly remote). Three scopes, one tiny icon vocabulary:

| Scope | Icon (proposed) | Who / where it lands | Read |
|---|---|---|---|
| **Self** | ⦿ (a single figure) | the **acting player only**, wherever they stand | a personal boon/hazard — *"you got the last portion" / "you queued an hour"* |
| **Region** | ⬢ (the region glyph) | the **drawn region** — every agent **standing in it**, and/or that region's board (its market/road) | the island acting on a *place* — *"typhoon shuts this region's road" / "festival crowd here"* |
| **Neighbour** | ➤ (an arrow) | **agent(s) standing in a region adjacent to the drawn region** | it spills next door — *"the queue's so long it backs up into the next town"* |

- **How the two actions read differently through one system:**
  - **Visit** (you flip *your* region, you're standing there): **Self** → you; **Region** → your region, so it
    hits **you** (and any rival also here); **Neighbour** → a rival standing next door, not you. So a Visit
    mostly self-resolves, with an occasional splash next door.
  - **Convenience Store** (you flip *any* region, often one you're **not** in): **Self** → you; **Region** →
    **whoever is standing in that (possibly remote) region** — this is the take-that lever: flip your
    **rival's** region and a region-scoped hazard lands on **them**; **Neighbour** → whoever's beside it.
    Because you're usually *not* in the flipped region, the drinks player sourcing the common mostly only
    eats **Self**-scoped events — a mild, bounded personal tax that makes the Convenience Store
    *live-but-slightly-risky* rather than a free lunch, while region/neighbour events become a weapon they
    can aim.
- **Warm rail (binds — flag for `bg-theme`):** a rival-facing hazard stays a **warm, secular island-life
  beat** (a typhoon shuts a road, a festival crowd, a "完售 Sold Out" sign, scooter gridlock), never
  mean-spirited, never destroying what a player holds or costing a whole turn. The scope makes the island
  *push people around*, which is exactly the identity's "the island is a subject, not scenery" rail — but the
  new *aim-it-at-a-rival* capability of the Convenience Store must land as cheeky caper, not spite. `bg-theme`
  to sanity-check the rival-facing beats.
- **Proposed scope ratio (→ sim-tune):** across the ~14-event pool, **~40% Self ⦿ / ~40% Region ⬢ / ~20%
  Neighbour ➤.** Rationale: Region is the workhorse interaction scope (the reach-a-rival lever); Self keeps
  a floor so the Convenience Store isn't purely a weapon and a Visit isn't self-harm; Neighbour is the rarer
  spice. Skew **hazards** slightly toward Region/Neighbour (so rival-facing beats exist) and **boons**
  slightly toward Self (your personal windfalls) — but keep some **Region boons** (a festival that boons
  everyone present, rival included — warm, not pure take-that). The ratio + whether it rebalances the
  drinks-vs-ladder fork are listed sim knobs.
- **Where events sit:** events are **per-region cards in that region's deck** (typhoon in the coastal
  South/East decks, plum rains in Central, scooter gridlock in the North), each carrying its own scope. A
  few naturally **Region/Neighbour-scoped** ones reach players who are *there*; they still live in a region
  deck and fire when that deck is worked (Visit or Convenience Store).
- **Recycling:** ingredient cards flow deck → Larder → (spent on a Bribe) → that region's discard; when a
  deck runs dry, reshuffle its discard (fired hazards return too, so the pressure persists). **Deck
  exhaustion also backstops the day-clock** — see *Acts & end-game*.

**Event starter set (~14; secular, hazard-leaning, warm-comedic; each carries a scope; wording + scopes via
the consultant before lock).** Hazards (majority): **颱風假 Typhoon Day** *(⬢ region — shuts the drawn
region's road: agents there can't Travel out next turn, or that region's next market draw is skipped)*,
**梅雨 Plum Rains** *(⦿ self — your haul this turn keeps 1 fewer)*, **完售 Sold Out** *(⬢ region — discard
the next ingredient in this deck)*, **機車陣 Scooter Gridlock** *(⦿ self — your next Travel arrives empty)*,
**客滿 Fully Booked** *(➤ neighbour — the crowd spills next door: an agent in an adjacent region loses a
tempo beat)*, plus new per-region hazards so every deck carries ~2. Boons (minority): **芒果季 Mango Season**
*(⬢ region boon — a windfall for whoever's in the drawn region)*, **珍奶節 Bubble-Tea Festival** *(⬢ region —
Buzz to those present)*, **臭豆腐大挑戰 Stinky-Tofu Dare** *(⦿ self, opt-in push-your-luck)*, **再吃一點啦
The Aunty Insists** *(⦿ self boon)*, **網紅來了 Food Blogger** *(⦿ self — your next Promote +1 Buzz)*, and the
CD's dynamic value-swing boon **摘星了！ Michelin Nod / 得獎了！ Competition Winner** *(its own ★ targeting —
see below; treat as region-flavoured)*. *Note the table-wide catch-up beat* **颱風假** *can be built as the
leader-excluding variant (Buzz to everyone except the Prestige leader) — that variant reads as ⬢ region/table
rather than a rival-aimed strike.* *Reserve knob:* if blind decks feel too swingy, add a **"brewing"
telegraph** (top card of each region deck face-up before you work it) — ~1 rule, restores preview agency.

**The "vendor gets hot" boon (★ Star — makes ladder vendor value DYNAMIC).** At least one boon event —
**摘星了！ Michelin Nod** (variants: **得獎了！ Just Won the Competition**, **爆紅 Went Viral**) — **places a ★
Star token on a LADDER vendor** (breakfast or night-market — **never a beverage**; see below), raising its
worth to **+2 Prestige / +1 Rep** for whoever wins it. **Targeting (proposed):** the Star lands on the
**lowest-Prestige unstarred Ladder vendor** (ties → the revealing agent chooses) — deterministically
turning *the most-ignored stall* into a live contested prize that **pulls both agents toward that region**
and starts a fresh Buzz fight. **Why ★ stays off the drinks side:** the ★ swing is what makes the *ladder*
high-variance-high-value; the drinks fork is deliberately the **steady, low-swing** road. A ★ on a beverage
shop (which sits in every region and never ramps) would create no travel pull and would blur the fork — so
the token targets the Ladder only. *(Design knobs → sim: the targeting rule; how many "gets hot" events sit
in the boon slice — 1–2 proposed.)*

---

## The Buzz-majority system (the headline mechanic)

The core, unchanged from v4. Read it as the Arcs-Court "agents on a card" mechanic, re-skinned to **hype on
a vendor** and lightened for a 2p duel.

**The rules, plainly:**
1. **Buzz is committed, public, and gated by presence — for every vendor type.** **Promote** places **2
   Buzz** onto vendor(s) you're with **in your current region** — a ladder vendor here and/or **this
   region's beverage slot** (v6.1: beverages are no longer region-free; the drinks stand you can Buzz is the
   one where you stand). Buzz sits on the card, face-up. **Both agents may pile on the same vendor.**
2. **Winning = ingredients + a ≥2 majority + presence — one unified rule.** To **Bribe** you must be **with
   the vendor (in its region)** — ladder *or* beverage — hold **at least 2 more Buzz on it than your rival**,
   and **pay its ingredient cost** (− region discounts). Checked at the instant you pay. *(大哥 needs only a
   **tie or lead** — a ≥0 margin.)*
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

**Beverages ride the *exact* same Bribe rule (v6.1 — now genuinely one rule) — but the fight rarely erupts.**
Drinks use the identical **on-site + ≥2-majority** rule as any vendor — v6.1 removes the old region-free
special case, so there is now literally *one* Bribe rule and *one* Promote rule, no vendor-type fork. The
**low conflict stays emergent**, not a written exception: a beverage is worth so little (Prestige 2, no
ramp) that spending contested Buzz on it is usually a bad trade versus the ladder — so in practice both
agents let each other take drinks, and because a stand sits in *every* region the two agents usually court
*different* beverage slots (they tend to be in different regions), so the drinks fights rarely even collide.
*(Probe: confirm drink-fights stay rare at the table now that beverages are region-anchored; if they erupt
too often, the fix is lowering beverage value or thinning the Beverage deck, not a new rule.)*

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
| **Beverage shop 飲料店** | the **easy-points fork**; low value, low conflict, low travel | ~7–8 | **No — off the clock** | **Yes — in the region it sits in** *(v6.1: no longer region-free; same on-site Bribe rule as any vendor)* | **1–2** (the **common**, sometimes + Central tea for a "premium" drink) | **2** (flat) | **+1** | **none / minor** (deliberately **off the ramp** — no region discount icon) | Beverage deck → **one persistent beverage slot per region** (a stand in every region, all day) |

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

**What makes drinks *viable* (not a trap) — v6.1: low-travel via UBIQUITY + easy sourcing, not
bribing-at-a-distance:**
- **A stand in *every* region + common off the Convenience Store = a genuinely low-travel engine.** You
  court the beverage slot **in the region you already stand in** (there's always one), and you source the
  common 糖 via the Convenience Store **from anywhere** — so a drinks-leaning player still barely needs to
  move. The low-travel comes from *ubiquity*, not from acting at a distance.
- **Low conflict (emergent + spatial).** Drinks are low-value, so the rival rarely spends contested Buzz on
  them — you usually clear the ≥2 floor with a single Promote and close. And because each region has its
  *own* stand, the two agents (usually in different regions) tend to court *different* beverage slots, so
  drink-fights rarely even collide. No Buzz war, no fizzled tempo.
- **Cheap + reliable — now *slightly* risky (v6.1).** 1–2 common per drink, sourced off the Convenience
  Store — which now **fires events by scope**. But the drinks player usually flips a *remote* common-bearing
  region, so only **Self**-scoped events tax them — a mild, bounded personal tax (never destroys held cards,
  never a whole turn). Still the low-variance road versus the ladder's dig + fight, just no longer a free
  lunch — a good, intended nerf that helps contain a runaway drinks fork.
- **Flat value that *beats a breakfast shop's face number*** (2 vs 1) — so early, a drink is a legitimately
  attractive "bird in the hand" versus a cheap breakfast stall whose payoff is deferred into the ramp.
- **A mission line of its own** (e.g. *"3 beverage shops"*) so a drinks lean can also chase the +7.

**What keeps drinks from *dominating* (not a solved line):**
- **A hard-capped ceiling.** Beverage Prestige is flat (2) and the deck is small (**~7–8**) — so even with a
  stand showing in all four regions, **at most ~7–8 drinks are winnable all game** (the deck, not the slot
  count, is the cap; once it empties, region beverage slots go empty and stay empty). A ladder player's 2–3
  night-market stalls (5–8 each) + the ramp + missions out-scores a pure-drinks tour.
- **No ramp.** Drinks carry **no region discount icon** — they don't compound. The ladder's whole
  engine-building payoff (each vendor cheapening the next) is unavailable to the drinks road. Flat stays
  flat.
- **Off the clock — no tempo lever when ahead.** A drinks Bribe doesn't advance the day-clock, so a
  drinks-leaning leader can't *use* their easy wins to hurry the game to a close while ahead (the way a
  ladder leader can). Drinks pad the score but don't shorten the runway for the trailing player.
- **Weak on breadth.** A beverage shop *sits* in a region (for presence), but it is **not** a region-
  signature vendor, so it **does not count toward region-coverage mission patterns** (the grand tour) — the
  highest-value +7 lines stay ladder-flavoured.
- **Now carries a mild sourcing tax (v6.1).** The Convenience-Store event-fire adds a small, steady
  Self-scoped risk to the drinks engine's spine — a deliberate brake on a runaway drinks fork.

The intended shape: **drinks are the reliable floor and the diversifier** (hedge a lost Buzz fight, pad
between ladder plays, feed one mission); **the ladder is the higher ceiling and the way you actually win a
contested game.** A strong line *mixes* — a few drinks, a strong ladder. **This balance is a knob-heavy
sim/table question (Riskiest #2)** — the live knobs are beverage Prestige value, beverage deck size, the
per-region-slot supply, whether drinks give any Rep, the common's availability, **and now the
Convenience-Store event-scope ratio** (below).

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
  your discount ramp** and stake early region positions. The **region beverage slots run alongside all
  day** (a stand in every region).

**Dusk (the day-clock reaches the dusk mark).**
- **Sweep** any unwon Ladder vendors (their Buzz returns to the supply — "the breakfast places are
  closing"), and re-stock the Ladder from the **Night-Market deck**. The Act track moves to **Act II**. *(The
  region beverage slots are NOT swept — drinks are all day, in every region.)*

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
- *"a vendor in **all 4 regions**"* (**the grand tour — breadth**; ladder-only by nature — a beverage shop
  sits in a region but is **not** a region-signature vendor, so it doesn't count for coverage)
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
  items → 早餐店 (~10); drinks → 飲料店 (~7–8, feeding the four region beverage slots); night-market foods →
  夜市攤 (~8–9). Expect the night-market band to *grow* from v5's 6 (蚵仔煎/雞排/臭豆腐 etc. are night-market
  foods, not "eateries"). Add a few real dishes per band if a band comes up short; may need more per band at
  3–4p. **Beverage cards are region-agnostic** — a beverage shop takes the region of whatever **slot** it
  fills (so it needs **no** printed region tag; the slot supplies its region-for-presence). This keeps "a
  stand in every region" true without pinning specific drinks to specific regions.
- **Re-cost every recipe to the 5-palette.** Anchor each **ladder** vendor in its own region **signature**;
  keep **~40% of night-market vendors cross-region** (the load-bearing travel lever); breakfast = 1–2
  (mostly its signature, occasionally + common); night-market = 2–3 (signatures across 2–3 regions,
  occasionally + common); **beverage = 1–2 common** (region-agnostic card; no region icon), a couple
  "premium" drinks + Central tea.
- **Keep the common generally useful** (appears as a minor filler in some ladder recipes) so the Convenience
  Store isn't a drinks-only action — but keep the **signatures** as the thing that gates the ladder.
- **Beverages carry NO region icon** (off the ramp) and no cross-region link — but you must still be
  **on-site** (in the slot's region) to Promote/Bribe one (the unified Bribe rule).
- Re-home the two orphaned **wild_pantry** perks → **wild_specialty**. Cap any one signature so no single
  region's Visit is over-demanded (watch North, which absorbs the old 4 proteins).

**Income vs spend (per action):**

| Action | Yield (EV) |
|--------|-------|
| Visit the Local Market | +~1.3–1.7 ingredients (region-gated) − hazard exposure *(大胃王 +~0.5; 媽寶 −~0.6)* |
| Convenience Store | +~0.5–0.8 common (blind, aim at a common region) − a small event-scope exposure *(v6.1: an event now fires by scope; a remote flip usually only Self-scopes onto you)* — **the drinks engine's income, now slightly risky** |
| Travel | +~0.7 ingredient + reposition |
| Promote | +2 Buzz onto the board (a positional investment) *(網紅 +3)* |
| Bribe (ladder) | − signatures (− discount); win vendor → +Prestige +Rep +perk; clears Buzz; **+1 day-clock** |
| Bribe (beverage) | on-site in the slot's region; − common; win → +2 Prestige +1 Rep; clears Buzz; **clock unchanged** |

**Cost of a vendor, in actions (the real currency).**
- **Ladder (uncontested):** source signatures (1–3 Visits/draws, fewer as the ramp grows) + ≥1 Promote + the
  Bribe → **~3–4 actions early, ~2–3 ramped**; contested, add a Promote or two. Courting rate **~1 ladder
  vendor / 2–3 turns**.
- **Beverage:** source 1–2 common (1–2 Convenience Stores) + 1 Promote (usually uncontested) + the Bribe,
  **all at the stand in the region you already stand in** → **~2–3 actions**, low-variance. A comparable
  *rate* to the ladder early — but flat, capped, and non-compounding, so it falls behind a ramped ladder
  late. **That crossover is the fork's whole balance** (sim it). *(v6.1: the low-travel comes from a stand
  being in every region + common off the Convenience Store, not from acting at a distance.)*

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
covered *(beverage shops don't count toward region coverage, so this last tiebreak still rewards the
ladder's grand tour)*.

**Designing out a dominant line (they pull against each other).** Night-market Prestige rewards *few, big*
ladder vendors; the ramp rewards *many ladder vendors doubled-up in a couple of regions*; the grand-tour
mission rewards *one ladder vendor in each region*; the drinks line rewards *volume at the region beverage
stands*; Rep rewards *steady Bribing on either road*. You cannot max ramp-concentration **and** the
grand-tour **and** an all-drinks volume line at once. The Buzz fight injects **opponent-dependence** — the
"best line" shifts with where your rival commits. (Sim probe #2.)

---

## Randomness

- **Input randomness (the bulk):** the Vendor Board reveal, the **face-down market decks**, the Mission draw
  (mitigated by draw-3-keep-1), the deck orders. The market is **blind** — deliberate variance for the
  push-your-luck.
- **Bounded output randomness (the spice):** the **Visit** flip resolves *after* you chose to dig; bounded
  (keep 2 of 3, events tax-not-destroy, composition known; **Travel** is the low-variance valve — its arrival
  flip whiffs). The **drinks fork is still the lower-variance road** — but v6.1 gives the Convenience Store a
  **small, bounded event-scope exposure** (a remote flip mostly Self-scopes a mild tax onto you), so drinks
  are *low*-variance, not *zero*-variance. A player who dislikes variance still leans Convenience-Store
  sourcing; they just accept a light, tax-not-destroy risk.
- **The Buzz fight and the Bribe are pure open-information** — no dice, no post-Bribe luck.
- **One hidden-information hook only:** your secret signature mission. Larder, both tours, all Buzz, and both
  tracks are open.

---

## Interaction & tension

**Direct (the spine):**
- **The Buzz-majority tug-of-war** — on the **ladder**. The public, escalating, on-site fight over each
  prize vendor. **Anti-resentment:** a lost fight costs only tempo and reads as *the vendor chose them* —
  "outraced, not robbed."
- **The Convenience-Store scope reach (v6.1 — the new light take-that).** Flipping a region's deck now
  *fires* the event by scope, so a Convenience Store can drop a **region/neighbour-scoped** warm island-
  hazard (a typhoon shutting a road, a festival crowd, a sold-out sign) on **a rival standing there** — or
  hand them a boon you'd rather not. It's **blind** (you don't know the top card) and **can backfire**
  (a Self-scoped card taxes you), so it's a cheeky, low-stakes poke, not a reliable strike. This is the
  layer an early sim read found near-zero (vendor-contest/interaction) — the scope injects it without a new
  action.
- **Positional denial** — being on-site gates *all* Promote/Bribe (ladder *and* beverage); occupying a
  contested region and stacking Buzz pressures a vendor. *(The drinks road is still the lower-interaction
  lane — but v6.1 makes it slightly less of a pure escape hatch, since the Convenience Store the drinks
  player leans on now carries scope risk and doubles as a poke.)*
- **Market scarcity** — a region deck running dry (both agents digging the same market) is a natural reroute
  pressure.

**Catch-up vs runaway (designed):**
- **Against runaway:** the contested Buzz floor, diminishing returns on cheap vendors, finite Buzz supply,
  and the **day-clock co-brake** (fast *laddering* hurries the last train / the end). *(Watch: a drinks-leaning leader is off
  the clock — see Riskiest #2b; contained by the low drink ceiling + deck backstops.)*
- **For catch-up (gentle):** the day-clock co-brake, the multi-track + two-road structure (a trailing player
  always has a live second vector — including the reliable drinks road to grind back points), one **table-wide
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
| 1 | **里長伯 The Old Councillor** | *Old Favours* — picks a **home region** at setup; his Bribes there cost **1 fewer ingredient** (home only). *(v6.3.1 CD-1 rework — supersedes the first-two-region version.)* | *An Outsider Everywhere Else* — the **away-tax**: Bribing in any region other than home costs **+1 ingredient**. *(no-HSR flaw REMOVED → re-homed as the table-wide "Scheduled Maintenance" event.)* | home-region discount / away tax | **REWORKED (v6.3.1)** |
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
| **Region beverage slots** | 1 per region (**4** up) | 1 per region (4) | 1 per region (4) |
| **Beverage deck size** | ~7–8 | ~9 | ~10 |
| **Buzz supply** | ~24 | ~32 | ~40 |
| **Dusk mark (ladder wins)** | 4 | 5 | 6 |
| **Last-train mark (ladder wins)** | 7 | 9 | 11 |
| **Market deck size** | base | +1–2 each | +2–3 each |
| **Buzz majority rule** | ≥2 over the rival | **≥2 over the *highest* rival** | ≥2 over the highest rival |
| **Start positions** | opposite (N & S) | spread on the ring | spread |

At 3–4p the Buzz majority is **≥2 over the highest single rival**; 大哥's tie-win becomes **≥0 over the
highest rival** — flag its 3–4p balance to `bg-architect` + sim. The **drinks fork gets relatively stronger
at higher counts** (the ladder is more contested, so the low-conflict lane is more valuable) — watch that
drinks don't over-perform at 4p (knob: **keep the Beverage deck small** so the drink-points hard cap
holds; the four region slots stay, but the deck caps how many are winnable). **Best-at: 2p.** 25 vendors is
comfortable at 2p; 3–4p may want a few more per venue type (→ `bg-architect`).

## Solo mode / Automa

**Medium priority.** Sketch — a **"Rival Agency" Automa**: a small **Route deck**; on its turn it
**Promotes** (drops Buzz on the highest-Prestige contested **Ladder** vendor in a rotating focus region),
**Bribes** (if it holds a ≥2 majority + can pay — locks it, advances the clock), **sources**, or **rotates**
its focus. It **ignores the region beverage slots** (the drinks fork is the human's lower-conflict lane; the
Automa applies ladder pressure). Its Buzz is real and contests *your* ladder majority. Pressure = the Buzz
race + the day-clock. *(v6.1 note: the Automa never fires Convenience-Store scope events at the human — keep
its take-that off; it pressures via the ladder only.)* **Defer to `bg-architect`; not in the base MVP.**

## Complexity budget

Target **~2.4–2.5, ceiling 2.5** — **still holdable, now with more headroom** (the 10→5 palette cut is a
real bank). `complexity-budget.json` caps (rulebook 1850 words, keywords 15, component types 8, aid 22
lines); `bg-elegance` guards.

**The weight call (honest, v6.1).** v6 banks the palette cut (fewer ingredient token types, fewer card
icons, a shorter aid, a smaller BOM). v6.1 then **removes** a special case (region-free beverages → one
unified Bribe rule) and **adds** one small concept (the event **scope** tag) — roughly a wash. Net
**~2.4–2.5** — the same band v5 held, with the component/cost gauges reading materially lighter (fewer
ingredient types → the `type`-column artifact that inflated `component_types` shrinks too).

**Keywords ≈ 13** (under 15): Larder · Vendor · **Bribe** · **Buzz** · **Promote** · region **discount
icon** · **Prestige** · **Reputation** · **★ Star** · **market deck** · signature **Mission** · **day-clock
/ Act** · **event scope** *(⦿ self / ⬢ region / ➤ neighbour — v6.1, one small keyword)*. (Visit /
Convenience Store / Travel / Ladder / region beverage slot / the three venue types / common / signature /
last train home stay plain-language — the venue types and the board zones are *named board areas*, not new
rules keywords. The scope keyword *nets against* the removed region-free-beverage special case — see the
v6.1 delta ledger.)

## Keywords / glossary

> Re-curated for v6.3.1 (2026-08-08, bg-elegance) — the true player term set (15). Stale v6.1/v6.2 vocab
> dropped because it no longer exists in the game: Prestige, Bookings/VP track, perk, the central Ladder,
> region beverage slot, the three venue types (早餐店/夜市攤/飲料店), signature/common ingredient (now plain
> board terms), signature Mission (objectives are Tour Tickets), and Code Red. One bolded head-term per
> entry (definitions plain) so the count reads true.

- **Larder** — your sourced ingredient cards, kept face-up; cap 7.
- **Vendor** — a face-up card you Bribe to win; carries a Draw number and either one region icon or none.
  Once won it is a stop on your tours and an engine piece — it never scores directly.
- **Draw** (人氣) — a vendor's printed value attribute (crowd-pulling power). NOT a score; it only feeds the
  few Tour Tickets that reference vendor value and marks the ★ apex as the marquee get.
- **Bribe** — the one unified action to win a face-up vendor: be with it in its region, hold a ≥2 Buzz
  majority, and pay its ingredients minus your region discounts. Winning moves the day-clock +1.
- **Buzz** — the committed, public, contested resource placed by Promote; never discounted; sits only in the
  supply or on a vendor; clears back to supply when the vendor is won.
- **Promote** — the action that places 2 Buzz on vendor(s) you are with in your current region, so long as
  your total committed Buzz stays within your Reach.
- **Reach** — your live Buzz cap (committed Buzz ≤ Reach); a track marker starting at 2. Built by Travel
  (+1) and some events; dinged by greed (the Greedy Grab) and a couple of events. It does NOT score.
- **region discount icon** — a vendor's region badge; each one you hold makes that region's ingredients 1
  cheaper on future vendors (floored at 0). The compounding engine; drinks and the ★ apex carry none.
- **★ Star** — the apex night-market trophy: a printed ★, the top Draw, no region icon (one per region). A
  boon can also drop a ★ Star token on a vendor, worth +2 Draw to whoever wins it.
- **Tour Ticket** — the objective you book from the shared row (DAY / NIGHT pools); the sole scoring vector.
  Judged at its phase end into your win-pile or lose-pile.
- **成團 / 取消** — your two ticket piles: **COMPLETED 成團** (WIN, tours that ran, +value) and **CANCELLED 取消**
  (LOSE, tours that didn't run in time, −floor(value ÷ 2)); tallied once at game end.
- **Rave Reviews** (好評) — the two per-player milestone boons on the Tours Completed counter, earned the
  first time YOU reach your 2nd and 4th completed tour (never pumps the leader).
- **market deck** — a region's face-down deck of its signature ingredient (+ the common K, in two regions)
  and a few events. Events carry a scope (⦿ self / ⬢ region / ➤ next-door) and fire on a Visit or
  Convenience Store; a card flipped on Travel arrival does nothing.
- **day-clock** — the Day→Night track; climbs +1 on every vendor win. At dusk the day layer is swept for the
  night decks (and day tickets are judged); at the last-train mark the game ends.
- **Scheduled Maintenance** (排班保養) — a table-wide event (its own island-wide banner, not a scope glyph):
  the HSR is down for everyone until the drawer's next turn; North and South take the long way. Two copies,
  seeded in the North and South NIGHT ingredient decks.

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
2. **Is the drinks fork a real choice — viable but not solved, now that it's region-anchored AND the
   Convenience Store carries scope risk? (THE v6 make-or-break, re-pointed by v6.1.)** *Attack (sim +
   table):* **drinks-lean vs ladder-lean win-rate** (each ≤~55%; neither a trap nor a solved line);
   **pure-drinks win-rate** (should clearly *lose* to a good ladder line — confirming the ceiling gap);
   **the crossover turn** (when does a ramped ladder pull ahead of flat drinks?); **drink-fight frequency**
   (should stay low even though beverages are now in-region — confirm the emergent + spatial low-conflict);
   **does the new Convenience-Store event-risk over- or under-nerf drinks** (the self-scoped tax on the
   drinks engine's spine). **(2b) Pacing:** does a drinks-heavy line make the game **drag** (clock starved)?
   Check turns-to-last-train across ladder-heavy vs drinks-heavy fields; the deck backstops should cap it.
   *Fixes:* beverage Prestige value, beverage deck size, the per-region-slot supply, whether drinks give
   Rep, the common's availability (every-vs-half), the day-clock marks, **the CS event-scope ratio**.
3. **Does the 5-ingredient dig stay a real decision, does movement still spread, and does the new event
   scope inject the right amount of interaction?** *Attack:* **the market-dig "flatten" check** — is *where
   to Visit* still driven by need?; **event-fire rate per Visit / per Convenience Store**; **per-region
   sourcing share** (each ≥~18%; the two pure-signature regions not starved); **inter-region moves/game**;
   **Convenience-Store vs Visit usage** (drinks players lean Convenience Store); **v6.1: how often is a
   Convenience Store aimed at a rival's region as a scoped poke** (the interaction the early read found
   near-zero — should now be non-trivial but not oppressive), and **does any scope feel swingy or
   mean-spirited**. *Fixes:* event/scope density, the **scope ratio** (self/region/neighbour), whether
   Travel should also fire, the cross-region rate on night-market recipes, the common's spread, the
   "brewing" telegraph knob — **not** adding ingredients back.

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
- **Beverage deck size (~7–8) — the drink-points hard cap** (now feeds four region slots; the *deck*, not
  the slot count, is the cap). Once the deck empties, region beverage slots go empty.
- **Do beverages give Rep? (proposed +1)** — and do they carry any perk (proposed none). Either lever, if
  raised, can tip drinks toward dominance.
- **Does the ladder still reward travel over the drinks grind?** — confirm ladder-lean and drinks-lean both
  land ≤~55% and a *mix* is the strongest line; confirm pure-drinks clearly loses.

**The event scope + Convenience-Store fire (the v6.1 additions):**
- **Scope ratio (proposed ~40% self ⦿ / ~40% region ⬢ / ~20% neighbour ➤)** — the primary v6.1 knob. Too
  much region/neighbour = the Convenience Store becomes an oppressive take-that weapon and over-nerfs the
  drinks engine; too much self = no interaction (back to the near-zero the sim flagged). Also skew hazards
  vs boons across scopes (hazards lean region/neighbour, boons lean self, keep some region boons).
- **Does the Convenience-Store event-risk rebalance the drinks-vs-ladder fork?** — the drinks engine's spine
  now eats a self-scoped tax; confirm it contains a runaway drinks fork **without** tipping drinks into
  non-viability. (If it over-nerfs: lower the region/neighbour share or the hazard rate; if it under-nerfs:
  the reverse.)
- **Should events also fire on Travel?** — proposed **no** (protect mobility + never-a-dead-turn + 里長伯).
  Sim can test whether firing on Travel too is fun or over-taxes movement.
- **Region-scoped resolution:** does "hits every agent standing in the drawn region" create enough contest
  without being swingy? (Alt: hits only the acting player + the region's board.)

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

**H3 — the common's availability (carried from v6).**
- **A. Common in HALF the regions (2 of 4), concentrated.** *(this doc's rec.)* Protects travel value + gives
  the smaller palette texture variety; the drinks player targets those two decks via the Convenience Store.
- **B. Common in EVERY region.** Maximises the drinks engine's reliability (Convenience Store never picks a
  common-less deck) at the cost of some travel value and some signature-dig dilution everywhere.
- **C. Common in half, but at a HIGHER per-deck share.** A middle option if half-at-normal-share proves too
  slow for the drinks engine but every-region flattens travel too much.
> *Recommendation: ship **A** into the sim; it's the cleanest fork + travel balance. Fall to **C**, then
> **B**, only if the sim finds the drinks engine non-viable (too slow to source the common).* *(v6.1
> interaction: the new Convenience-Store event-risk taxes the drinks engine's spine, so H3 and the scope
> ratio (H4) must be tuned together — if drinks read non-viable, widen the common **or** soften the scope
> ratio, whichever the sim points at.)*

**H4 — the event-scope ratio + does Travel fire (the NEW v6.1 call; both fully sim-tunable — the CD can
defer).** The proposal is **~40% self ⦿ / ~40% region ⬢ / ~20% neighbour ➤**, hazards leaning
region/neighbour, boons leaning self, and **events fire on Visit + Convenience Store but NOT on Travel**.
- **A. Ship the proposal as-is** *(this doc's rec)* — a healthy interaction lever with a Self floor that
  keeps the Convenience Store from being pure take-that, and a protected Travel.
- **B. Lighter interaction** — more Self (~55/30/15) and/or events fire only when a *hazard* would land on a
  rival, if the table finds the Convenience-Store poke too spicy or the drinks engine over-nerfed.
- **C. Spicier** — more region/neighbour and/or Travel also fires, if the sim finds the interaction still
  near-zero.
> *Recommendation: ship **A**; the ratio is the primary v6.1 tuning knob and the sim will move it. This is
> genuinely the one-or-two live calls for the human this pass (with H3, which it interacts with).*

---

## Handoff notes (guardian sweep — where to look)

**v6.1 — what moved this pass (run `bg-theme` coherence + `bg-elegance` budget on the change):**
- **Signature twist UNCHANGED in shape** (public on-site Buzz-majority fight for engine-piece ladder
  vendors). v6.1 touched the **economy/interaction layer around it**, in two places:
- **(A) Event scope + Convenience Store fires — `bg-theme` warmth check (load-bearing).** The Convenience
  Store can now drop a **region/neighbour-scoped hazard on a rival**. The rail: every rival-facing hazard
  must stay a **warm, secular island-life beat** (typhoon shuts a road, festival crowd, 完售 Sold Out sign,
  scooter gridlock), **tax-not-destroy**, never mean-spirited, never a whole turn — and the *aim-it-at-a-
  rival* capability must land as **cheeky caper, not spite** (the identity's "island is a subject that
  pushes everyone around" rail helps here). `bg-theme` to (1) confirm the rival-facing beats read warm; (2)
  name/lock the three **scope icons** (⦿ self / ⬢ region / ➤ neighbour) in the icon vocabulary; (3) note
  the scope adds a *new game-term* — check it doesn't over-clutter the warm register.
- **(B) Beverages region-ANCHORED — `bg-theme` + identity.md fix.** Beverages are no longer region-free;
  there is now a drinks stand **in every region**, and you must be **on-site** to Promote/Bribe one.
  **identity.md is now STALE on this** — it repeatedly calls the drinks fork **"region-free"** and names a
  central **"Beverage Row"** (e.g. the Theme↔mechanic resonance "drinks fork" bullet, the Naming "飲料店"
  bullet). **bg-theme must update identity.md** so the fiction reads *"a 手搖飲 stand on every corner — you
  grab the one where you already are"* (which is, if anything, *more* authentic than region-free — the
  ubiquity is the real-Taiwan truth). The warm "off-clock / always-there / low-conflict / never-race-for-a-
  drink" identity is **fully intact** — only the "region-free / act-at-a-distance" plumbing changed. Confirm
  coherence.
- **`bg-elegance` (v6.1 net):** we **removed** a special case (region-free beverages → **one unified Bribe
  rule + one unified Promote rule**, a real teach-simplification) and **added** one small concept (the
  3-icon **event scope**). Roughly a wash on game-terms (~12 → ~13). See the *v6.1 delta ledger* up top. The
  standing v6 flag is unchanged and still live: **rulebook prose is over its word cap** — write the scope
  block tight (one compact table) and let the unified Bribe/Promote rules *shorten* the action prose (they
  no longer fork by vendor type). The scope must be taught as **ONE concept** ("every event has a scope =
  who it hits"), never three rule blocks.
- **`bg-access` / `bg-infodesign` (v6.1):** two new at-a-glance reads to dual-code — the **event scope tag**
  (⦿ / ⬢ / ➤ must be distinguishable beyond shape alone, e.g. + a label) and the **region beverage slot**
  on each region (a drinks stand marker per region). Otherwise unchanged.

**v6 — what moved (run `bg-theme` coherence + `bg-elegance` budget on the change).** *(v6.1 supersedes the
"region-free beverages / Beverage Row" parts of this block — read the v6.1 block above first; the items
below are the v6-base record, lightly patched.)*
- **The signature twist is UNCHANGED in shape** (public on-site Buzz-majority fight for engine-piece ladder
  vendors) — but the **economy layer around it restructured**, so `bg-theme` should check: **(1)** the
  **drinks fork** — does the all-day **all-region** 飲料店 "easy points" road *(v6.1: a stand in every
  region, not region-free)* read as warm and native (the very-Taiwan 手搖飲 stand on every corner), and does
  keeping the ★/contest off it feel right, not like a demoted second-class food? **(2)** the **venue-type rename is now fully mechanical** (breakfast = Act I
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
  gauges (fewer ingredient token types; the `type`-column artifact shrinks). Net weight ~2.4–2.5; game-term
  count ~12 *(v6.1: ~13 with the scope term, which nets against the removed region-free special case)*.
  The NEW ideas to weigh: the **region beverage slots** *(v6.1: per-region, superseding the v6 "Beverage
  Row")* and the **"drinks don't tick the clock"** clause. Guard the rulebook word count — and note the
  editorial fix below is now done.
- **Editorial fix (DONE this pass, per the v5 elegance flag):** the **"Still to specify → bg-developer" TODO
  block** and the **provenance/version blockquote** have been **moved OUT of `rules-draft.md`** into this
  design-doc (the dev-TODO is folded into `bg-developer` below; provenance lives in this doc's header) so the
  laid-out rulebook's word count reads true.
- **`bg-access` / `bg-infodesign`:** the vendor card shows a **venue-type badge**; the board has the central
  **Ladder** + a **per-region beverage slot** *(v6.1, superseding the v6 central "Beverage Row")* — a new
  at-a-glance read to dual-code. Fewer ingredient icons (5 not 10) *helps* legibility. Keep dual-coding on
  region colours + emblems. *(v6.1 also adds the event scope icons — see the v6.1 block above.)*

**`bg-developer` (AFTER CD sign-off — not yet) — the v6 build TODO (moved here from rules-draft):**
- **Re-cost to the 5-ingredient palette** (4 region signatures + 1 common; retire the wild "pantry" token) —
  see *Economy → the re-cost brief* for the region map, the common-in-two-regions rule, and the per-venue
  cost principles (breakfast 1–2 signature; night-market 2–3 cross-region; beverage 1–2 common, **region-
  agnostic card, no icon**; ~40% night-market cross-region; keep the common a minor filler in some ladder
  recipes; cap North's signature demand).
- **Re-sort the 25 vendors by venue *identity*** into the **three decks**: **Breakfast Shops 早餐店** (~10, Act
  I) · **Night-Market Stalls 夜市攤** (~8–9, Act II; build the value curve — ordinary 5–6 + **2–3 apex
  "Legendary" at 7–8 with a printed ★**) · **Beverage Shops 飲料店** (**~7–8**, feeding the **four region
  beverage slots**, Prestige 2 flat, +1 Rep, no ramp icon, **region-agnostic**). Add real dishes per band if
  short; more per band at 3–4p.
- **Board printing:** the **day-clock** (dusk + last-train marks), Prestige + Reputation tracks, the central
  **Ladder** display (Act-cycling, region-gated, with Buzz zones), and — **per region on the map** — a
  face-down **market-deck space** *and* a persistent **beverage slot** *(v6.1: replaces the single central
  region-free "Beverage Row" — a drinks stand in every region)*. No Coverage scoring key (cut in v5).
- **Rebuild `events.csv`** (~14; hazard-leaning; in-deck; ~2 hazards/deck + table-wide ones). **v6.1: add a
  `scope` column to every event** (⦿ self / ⬢ region / ➤ neighbour), targeting **~40 / ~40 / ~20** with
  hazards leaning region/neighbour and boons leaning self (see *Events* for the starter re-tag). Include the
  **"vendor gets hot" boon** (摘星了／得獎了／爆紅) targeting a **Ladder** vendor + **~4 ★ Star tokens** (+2
  Prestige / +1 Rep, recyclable). Re-home orphaned perks: **wild_pantry → wild_specialty**; add the
  **Buzz-reach** night-market perk. **Events now fire on Visit AND Convenience Store (by scope); Travel
  whiffs** — reflect in any sim/resolution code.
- **Bake the five v5 characters** (unchanged by v6): **里長伯 / 媽寶** (KEPT kits re-lored) · **網紅**
  (Promote 3; go last + behind) · **大胃王** (Visit keeps all 3; flaw = the CD's H1 pick) · **大哥** (wins at
  the CD's H2 threshold; flaw = the CD's H2 pick).
- Size the **Buzz supply** (~24 @2p; +8–10/player). Set the **day-clock marks** (2p: dusk **4** / last
  train **7**) — sim-tunable. Re-tune **mission thresholds** for the shorter game (incl. the new *"3
  beverage shops"* line; ≥12-Prestige).
- **Player-aid** (≤22 lines): the five actions + the **one unified Bribe/Promote rule (on-site for every
  vendor type)** + **the ladder/beverage clock-tick split** + **the event scope key (⦿/⬢/➤; fires on Visit
  & Convenience Store, not Travel)** + the two scoring vectors + the mission +7 + the day-clock (dusk / last
  train home) rule.
- **Iconography:** 5 ingredients + 4 regions + a **venue-type badge** + the **3 event scope icons** + the
  vendor-card layout (cost / region icon *(ladder)* / Prestige / Rep / perk / Buzz count / venue type),
  dual-coded (`bg-access` / `bg-infodesign`).

**`bg-playtest` (GATED — DO NOT run until the CD signs off):** rework `sim/travel_agents.py` to model the
**5-ingredient palette**, the **region-anchored beverages** (a stand in every region; on-site to
Promote/Bribe — the drinks_lean strategy must be *in* a region to bribe its stand, not bribe from
anywhere), the **Convenience-Store event-fire by scope** (⦿/⬢/➤; the drinks player's remote CS flips mostly
self-scope), the **ladder-only clock**, and the **drinks fork**; then run the three probes, **leading with
Riskiest #1 (the Buzz fight, incl. 大哥) and #2 (the drinks-fork viability/dominance + pacing, now with the
CS scope-tax + region-gating).**

**Cut mechanics to sweep for stranded names/rules:** **Extract**, **Poach**, the **wild "pantry" token** (now
retired into the common), **the Season counter**, **the three value-bands-on-two-decks framing**, **the
Region-Coverage scoring track**, **event tiles / the face-up Market**, the **v4 character cast**, the
**"Code Red" end-trigger label** (now the plain Day → Night arc), and — **v6.1 new** — **"region-free"
beverages / a central "Beverage Row"** (now a per-region beverage slot) and the **"hazards fire only on
Visit / Convenience-Store whiff"** rule (CS now fires by scope; only Travel whiffs). Also sweep for any
lingering **"Stall / Eatery / Marquee"** or **"~10 ingredients / pantry"** references.

> **Sweep tracker for the coordinator (design-side is clean; data-side is pending bg-developer, gated):**
> the **design-doc + rules-draft now carry ZERO live "Poach", ZERO live "Code Red", ZERO live "region-free
> Beverage Row", and ZERO live "Convenience-Store whiff" references** (all appear only in cut/provenance
> notes). **identity.md is the one design-side file still stale on v6.1** — it still says beverages are
> "region-free" and names a "Beverage Row" (and still carries "Code Red"); **bg-theme owns the identity.md
> fixes** in the guardian re-check. Still outstanding when `bg-developer` rebuilds data (sim gated):
> **`components/*.csv` and `sim/travel_agents.py`** need the full sweep — Poach, Stall/Eatery/Marquee, the
> ~10-ingredient/pantry palette, "Code Red" strings, the region-free-beverage model, and the addition of the
> **event `scope` column + CS-fires-events** logic.

---

## FTUE — Teaching sequence (relocated from `rules-draft.md`, 2026-08-07, bg-elegance)

> **Provenance:** moved out of the standing rulebook (`design/rules-draft.md`) to keep the laid-out
> word count true against the 1650-word cap — the same editorial relocation applied to earlier
> appendices. This is a *teaching order* handoff for the eventual FTUE / how-to-teach page, not a rules
> change: every rule referenced below is defined in `rules-draft.md`. Owned by bg-playtest for the
> blind-test / FTUE plan.

The order a first game should reveal the rules:

1. **Goal + one Vendor** — "here's a stall in the North; it wants 2 pork, and whoever hypes it most (by 2
   Buzz) while standing here wins it. Let's go get it."
2. **Visit / Convenience Store / Travel** — dig the North market for its signature; note that events fire
   *by their scope* (point at the ⦿/⬢/➤ tag) when you Visit or hit the Convenience Store; grab a card; move.
3. **Promote** — drop Buzz on the stall; "your rival can pile on too — this is the fight."
4. **Bribe** — in-region, ahead by 2 Buzz, pay the ingredients → win it: Prestige moves, Rep moves, point at
   its **region icon** ("your first North discount"). Its Buzz clears; **the day-clock ticks +1**.
5. **The ramp** — win a second North vendor and *watch the ingredients cost less* (Buzz still full).
6. **Drinks** — point at a cheap drink: "low value, no icon, no ramp — a quick grab to pad your score or feed
   a mix ticket, but you can't win on drinks alone. It still ticks the day-clock like any vendor."
7. **Tour Tickets** — "your itinerary. Book one from the row; finish it before its phase closes or it drops
   to your lose-pile at half value. Book bold, or play it safe."
8. **The hype fight** — the first time you both stack Buzz on one vendor: "out-commit, race to the
   ingredients, or concede and take another. Outraced, not robbed."
9. **Reach** — the Buzz cap you build by travelling; "it fuels the hype fight but never scores — the only
   score is your Tour Tickets, so book bold and finish them."
10. **Dusk → the Night Market** — introduce at the dusk flip: "the day judges your daytime tickets, the
    street turns over to neon, the big names arrive — and night's coming, so don't miss the last train."


---

## Rules-draft provenance (relocated)

> Relocated here 2026-08-08 (bg-elegance) from the scaffolding HTML comment at the top of `rules-draft.md`,
> to keep the rulebook's word count clean while losing no context. Voice for the rulebook: warm
> travel-guide, teach-in-play order (identity.md). CANON spec = `design/v6.3-content-draft.md`.
> Terminology now blessed/locked and used in the rulebook: a vendor's *value* attribute = **Draw** 人氣;
> *Reputation* = **Reach**. (The note below is the historical v6.3/v6.3.1 change record; it predates the
> Draw rename and still says "value" for the vendor attribute — read that as Draw.)

**v6.3 changes folded in:** TICKETS-ONLY scoring (vendors give NO points — Tour Tickets are the sole score;
expanded ~44-ticket deck); Reputation→Reach gates Buzz (a live cap) + Reach sinks; Reputation no longer
scores; perk field eliminated; ticket pools 3→2; milestones = perplayer, re-homed on a Tours-Completed
counter. A vendor keeps a printed value ATTRIBUTE (referenced by value-tickets; NOT a score) — now named
**Draw** 人氣. The former "Bookings" score track is retired as a score; its physical track is repurposed as
the Tours-Completed / Rave-Reviews counter.

**v6.3.1 (four CD changes — BALANCE-VALIDATED by the re-sim, `playtests/sim-notes.md §v6.3.1`; the CD's
three final calls LOCKED 2026-08-08):**
1. 里長伯 reworked — picks a HOME region at setup; −1 discount there only, +1 ingredient away-tax elsewhere;
   no-HSR flaw REMOVED. LOCKED −1/+1 AS-IS (lands 55%, top-of-band, CD-accepted); he starts Reach 2 like
   everyone (NO start-Reach change — the sim module's start-Reach-1 default is NOT canon).
2. New table-wide event "Scheduled Maintenance" (HSR down for everyone one round — re-homes the no-HSR
   concept); LOCKED at 2 copies (a felt ~12% beat; sim default 1 is NOT canon).
3. ALL agents start in Taipei (North hub) — replaces the split N/S 2p start.
4. NIGHT vendors cost meaningfully MORE than day vendors (LOTR:Duel-style curve); LOCKED SOFT curve — night
   "both" foods → 3, apex ★ → 4 (top apex 5), every night marquee cross-region biased; DAY held as printed;
   steep +2 and the min-1 floor both rejected.

bg-developer builds to CANON (v6.3-content-draft §CD-4 table), not the sim defaults.

---

## Sensitivity — production rail (RELOCATED from the player rulebook, 2026-08-08, bg-elegance)

> **Why this lives here, not in `rules-draft.md`:** these are **production constraints for the team**
> (art, naming, print, publishing), not rules a first-time player needs. The rulebook now carries only a
> short, warm player-facing line ("these are real Taiwanese dishes and night markets — celebrated with
> care"). The binding rail below is NOT lost — it is relocated intact and still binds `bg-developer`,
> `bg-theme`, `bg-publishing`, and the art pipeline. Full context: `identity.md` §Sensitivity + the
> theme↔mechanic resonance bullets; this is the consolidated at-a-glance rail.

**Binding production constraints (all must hold before art/print):**
- **Paid Taiwanese / Indigenous cultural + language consultant sign-off** before art — the **#1 pre-art
  item**, especially the East region (Indigenous-forward) and the top apex **石板烤肉 Stone-Slab BBQ**
  (dish + naming + framing must clear the consultant first).
- **Names are never mangled.** Dish, vendor, and place names stay real and intact — **Tâi-lô romanisation +
  繁體字**, never bent to fit a gag or a "starred" joke.
- **Traditional Chinese only (繁體), never Simplified** — Taiwan uses Traditional characters; this is
  non-negotiable in every printed and rendered string.
- **Secular only.** No mechanics, art, or gags built on temple festivals, deities, ghost-month, or funerary
  customs. Events lean modern/secular — food fairs, fruit seasons, weather, roads, crowds, warm local
  characters (people with dignity, never exotic punchlines).
- **"Bribe" reads as warm comedy, never corruption** — the smarm lands on the over-the-top agent; the
  vendor is the beloved, never a mark. 大哥 (gangster-adjacent) and 里長伯 (politician) sit next to that
  word and carry the tied-#1 consultant flags — bind the warmth hard.
- **★ accolades stay real and secular**, dishes stay dish-typed generic stalls — **never a false star on a
  real named business.**
- **Celebration, not extraction** — the agents are passionate local promoters showing off home; if a tour
  or event ever reads as outsiders packaging/harvesting the island, that's a re-theme flag.
