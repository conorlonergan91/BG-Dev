# Travel Agents: Taiwan — Design Doc (v5 · the two-Act "one glorious eating day" tightening)

Deeper design detail than the game bible. Owned by `bg-design`; keep the bible's summary in sync.

**Provenance (read this first).** The mechanical spine is the **v4 Buzz-majority / push-your-luck
rework** (committed public Buzz on vendors, face-down market decks, escalating tiers; Extract + Poach
cut). **v5 folds in the CD's LOCKED tightening**, from `decision-log.md` (top entries) + the CD's
direct brief:
- **Two Acts, not three** — a **≤30-minute** "single glorious eating day": **Act I · Afternoon Crawl 下午
  → Act II · Night Market 夜市**, ending on the **"Code Red"** last-train climax (this doc owns the exact
  firing condition; `bg-theme` owns the name/flavour).
- **Region-Coverage is CUT as a scoring track** — breadth is now carried **only by a Mission** (the
  grand-tour pattern). Scoring is **two live tracks (Prestige, Reputation) + the hidden +7 Mission.**
- **The vendor keyword is LOCKED = "Bribe a Vendor"** (no longer a working name; the warm reframe is
  binding — `identity.md`).
- **The five characters are re-cast to Taiwanese social types** — three KEPT kits re-lored, **two NEW
  kits** (大胃王, 大哥) whose numbers are **sim-tunable**.

This supersedes the v3/v4 fragments. Where an older label survives (Stalls / Eateries / Marquee) it is
now a **vendor *type*** printed on the card (used by Missions + Prestige value), no longer a separate
Act. The v4 change-ledger and the v3.1 movement rebalance are unchanged and still bind `bg-developer`.

> **One-line frame:** two rival travel agents race across Taiwan through **one escalating eating day** —
> source real regional ingredients from face-down region **markets** (push-your-luck: a typhoon may be
> the next card), and pile **Buzz** onto the island's vendors to **win them over** (you must be on-site,
> and you must out-hype your rival). Each vendor won is an engine piece (a compounding ingredient
> discount) climbing **Prestige** and **Reputation** toward a hidden **signature tour**. When head office
> calls **Code Red**, catch the last train home — best tour is **Top Agent**.

Sensitivity rails bind throughout (`identity.md` §Sensitivity): winning a vendor reads as **the vendor
choosing the agent who hyped them best** — never an agent seizing, cornering, or corrupting a place.
"Bribe" is the **warm-comedic** *"this isn't a bribe, it's a marketing opportunity"* caper — the smarm
lands on the over-the-top agent, never the vendor. Two characters (大哥 gangster-adjacent, 里長伯
politician) sit next to that keyword and carry the **#1 consultant flags** — bind the warmth hard.

---

## What changed in v5 (the honest ledger for `bg-elegance`)

v5 is a **tightening**, not a new system — it *removes* weight the v4 rework had added.

| Cut / banked (−) | Added / spent (+) |
|---|---|
| **Three Acts** (three tiers as separate phases) | **Two Acts** on one **day-clock** (a single marker, two marks) — fewer phases to teach |
| **Region-Coverage scoring track** (its own 2/5/9 bonus + a Coverage tick on every Bribe) | (folded into **one Mission pattern** — the grand tour; the region-gating already forces breadth) |
| **"Bribe" as a working name** pending `bg-theme` | **"Bribe a Vendor" LOCKED** (the warm reframe now carries every line) |
| Old cast's **event-coupled kits** (Rookie hazard-cancel, Gourmand reveal-4) | **Two sim-legible NEW kits** (大胃王 keep-all-3 + a hazard tax; 大哥 tie-wins + a tab) |
| ~40–45 min / 3-act pacing | **≤30 min** / 2-act pacing (~5–6 wins per player) |

**Honest weight call.** v4 pre-trim was **~2.5–2.6** (the Buzz-majority is the spend). v5 **spends the two
recommended trims for real** — Coverage → mission-only (≈ −0.1) and three Acts → two (≈ −0.05 teach) —
landing back at **~2.4–2.5, at/under the ceiling.** Depth still lives in the Buzz fight under a
push-your-luck market; we cut *around* it. `bg-elegance` guards; the honest budget is now **holdable
without a ceiling raise.**

---

## Design goals

- **A tight two-player engine with a real *fight* at its centre.** The Buzz-majority makes each prize
  vendor a **public, escalating, on-site tug-of-war** — the Arcs-Court tension the CD asked for, in a
  lighter frame, now inside a **half-hour** box.
- **Target weight ~2.4–2.5, ceiling 2.5.** Depth from the Buzz contest + push-your-luck market + the
  two-act escalation; complexity banked by cutting Extract/Poach/pantry/Coverage-track and 3→2 Acts.
- **2-player first.** The duel is the design home; the Buzz-majority is sharpest as a two-person
  tug-of-war. 3–4p is a scaling delta (majority = ≥2 over the *highest* rival).
- **Aesthetics (locked, `identity.md`):** **Discovery (lead)** — face-down markets and the dusk→night
  escalation keep revealing the island; **Fellowship** — the shared, comedic fight over a prize vendor;
  **Challenge** — the routing + two-input + when-do-I-commit puzzle, kept light.
- **The meaningful decision every turn:** *dig the market for the specialty I need (risk a typhoon), grab
  a safe blind card, travel on, pile more Buzz onto the vendor I'm fighting for — or close the Bribe now
  before my rival out-hypes me?* No forced move.
- **Taiwan does real work** (unchanged): the region↔ingredient web is real food geography — rename the
  setting and the recipes break. Dishes named Tâi-lô + 繁體, never mangled. The two Acts **are the real
  Taiwan food day** (afternoon crawl → night market).
- **Design the make-or-break risks out:** **(a)** the Buzz contest is fun/tense, not a swingy slap-fight
  or a "never commit, always snipe" degenerate; **(b)** no economy runaway inside a short game;
  **(c)** the push-your-luck market is spicy, not punishing; **(d)** movement still spreads across regions;
  **(e)** the 大哥 tie-win doesn't dominate the central Buzz fight.

---

## Core loop (detailed)

A turn is **one action**; short turns, low downtime. Each cycle you weigh three questions: *which input am
I short — the region-specific ingredients a vendor needs, or the Buzz majority on it? am I on-site to act
on it? and is now the moment to close before my rival swoops?*

1. **Read the board.** The **Vendor Board** shows the current field (each vendor with its ingredient cost,
   its **region icon**, its **Prestige/Rep/perk**, and **the Buzz both agents have piled on it**). Your
   secret **signature mission** points at a vendor pattern worth **+7**. The four **region market decks**
   are face-down (you know each region's two specialties + that hazards lurk). Your **Prestige** and
   **Reputation** markers show your two live vectors; the **day-clock** shows how close the day is to dusk
   (Act II) and to the **last train** (Code Red).
2. **Take one action** (see *Actions*): **Visit the Local Market**, **Convenience Store**, **Travel**,
   **Promote**, or **Bribe a Vendor**.
3. **Sourcing is a gamble now.** *Visit the Local Market* (in your region) flips the top 3 of that region's
   deck: any **hazard** fires on the spot (a typhoon, a sold-out sign), then you keep up to **2** of the
   **specialties** you turned up. *Convenience Store* and *Travel* each take a single blind top card
   (specialty → keep it; event → the shelf was bare, nothing fires).
4. **Buzz is a public fight.** *Promote* places Buzz from the supply **onto vendor(s) in your current
   region** — committed, visible, and your rival can pile onto the same vendor. You can only close a
   **Bribe** on a vendor when you're **in its region**, hold **≥2 more Buzz on it than your rival**, and
   can **pay its ingredients** (minus your discounts). Winning clears all its Buzz to the supply, scores
   you Prestige + Rep + its perk, and **advances the day-clock** one step.
5. **The day escalates and ends.** When the day-clock reaches **dusk**, the Board **sweeps and re-stocks
   from the Night Market (Marquee) deck** — the big names, fiercely contested. When it reaches the
   **last-train** mark, **head office calls Code Red** → finish the round + one full round → **reveal
   missions** → score. No Extract; the day-clock paces and ends the game.

The loop compounds **legibly and with a brake**: each vendor makes a *class* of future vendors cheaper in
**ingredients** (the ramp) — but every vendor still demands you **win an undiscounted, region-gated,
contested Buzz majority**, one Promote at a time, on-site. That Buzz fight is the primary anti-runaway
brake (see *The Buzz-majority system* and *Economy*).

---

## Turn / round / phase structure

**Setup (2p shown; deltas in *Player counts & scaling*):**
- Place the **Taiwan map board** — 4 regions on a ring: **North 北 – Central 中 – South 南 – East 東**; an
  **HSR** spine links North↔South down the west coast. The board carries the **day-clock** (the Act track),
  the **VP (Prestige) track**, the **Reputation track**, the **Vendor Board** slots, and a face-down
  **market deck** zone per region.
- Build the **four region market decks**: each = its **two specialty ingredient cards** (several copies
  each) **+ 3–4 event cards** (hazard-leaning), shuffled face-down. (No pantry pile — the Convenience Store
  replaces it.)
- Build the **two Act decks** from the 25 vendors:
  - **Act I · Afternoon Crawl** = the **Stalls** (~11) shuffled on **top**, the **Eateries** (~8) shuffled
    **beneath** them. *(This gives a cheap opening board for the discount ramp, and the eateries surface as
    the afternoon "warms up" — a real mid-Act escalation without a third Act.)*
  - **Act II · Night Market** = the **Marquee** vendors (~6), shuffled. Set aside face-down until dusk.
  - Deal the **Act I** deck to fill the Board (2p: **5 slots**). Set the **day-clock** marker to 0.
- Form the **Buzz** supply (open pool; **~24 at 2p** — see *Economy*).
- Each agent: choose/deal an **Agent Character** (ability + flaw, public); take a pawn (start on opposite
  regions — one North, one South); place **VP** and **Rep** markers at 0; take an empty tour + Larder area.
  The Larder (ingredient cards) sits **face-up** all game. Deal **3 Mission cards, secretly keep 1** (your
  signature mission, +7), return 2 unseen.

**A turn = choose ONE action:** **Visit the Local Market · Convenience Store · Travel · Promote · Bribe a
Vendor.** Then if your Larder exceeds **7** ingredients, discard down to 7 (to that region's market
discard). Play passes clockwise (the Influencer's flaw = goes last; see *Characters*).

**End-trigger (Code Red).** When the **day-clock reaches the last-train mark** (see *Acts & end-game*),
**head office calls Code Red**: finish the current round (equal turns for all), play **one more full
round**, then **reveal signature missions** and score. A fair, unswingy wind-down; the extra full round
guarantees the trailing player answers the trigger. **Reputation-top scores its bonus but does not end the
game** (carried from v3.1's sim-fix).

Target length: **~25–30 min at 2p**, roughly **14–18 turns per player**, **~5–6 vendors won per player.**

---

## Actions

A turn = ONE of five. Each is simple; the depth is in *when* and *where*.

| Action | Where | Effect | Notes |
|--------|-------|--------|-------|
| **Visit the Local Market** | your current region | Reveal the top **3** cards of this region's market deck. Resolve **any event** revealed immediately (**hazards fire**), discard them. Keep up to **2** of the revealed **specialty** cards (to your Larder); discard the rest. | The ingredient workhorse **and** the push-your-luck spine. More hazards in the deck = more chance a flip both hurts you and eats an ingredient slot. *大胃王 keeps all 3; 媽寶 keeps only 1.* |
| **Convenience Store** | anywhere | Reveal the **top 1** card of **any one** region's market deck. Specialty → take it. Event → discard it, **nothing fires** ("shelf was picked clean"). | The flexible, reliable-ish valve: sourcing from *any* region without travelling, but only 1 blind card and it can whiff. Replaces the old pantry. |
| **Travel** | to an adjacent region | Move your Agent to an **adjacent** region (HSR: North↔South counts adjacent); then reveal the **top 1** card of the **arriving** region's deck (specialty → take it; event → whiff, nothing fires). | Never a dead turn — you (usually) arrive with something. *媽寶 draws the region she LEFT instead. 里長伯 cannot use HSR.* |
| **Promote** | your current region | Place **2 Buzz** from the supply onto **vendor(s) in your current region** (2 on one, or 1 on each of two). Buzz stays on the card, public; the rival may also Buzz the same vendor. | The Buzz-placement action. Region-gated — you can only hype vendors you're standing with. *網紅 places 3 (+1). 大哥's alternate flaw = places 1.* |
| **Bribe a Vendor** | in the vendor's region | Choose a Board vendor **in your current region** on which you hold **≥2 more Buzz than your rival**; **pay its ingredients** (− your region discounts, floored at 0). Take it to your tour → gain **Prestige** (VP live), a **Rep** bump, and its **perk** (usually a region discount icon). **All Buzz on it (yours + rival's) returns to the supply.** Refill the Board slot from the current Act deck; **advance the day-clock +1**; the vendor is locked from the rival. | The scoring + engine beat, now gated by **position + majority + ingredients**. The only action that advances the day-clock. *大哥 wins at a tie (≥0 lead), not ≥2; 大哥 pays +1 ingredient (the tab).* |

**Five actions, no conditional sixth.** (Poach and Extract are **cut**.) Every turn has multiple live
options with real trade-offs: dig the market (risk), grab a safe blind card, reposition + draw, pile Buzz
onto a contested prize, or close a Bribe. No forced/obvious move.

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
  lurk — you don't know the order.
- **Visit the Local Market** is the risk/reward: 3 flips, hazards fire, keep 2 specialties. If two of your
  three flips are events, you keep only 1 (or 0) specialty **and** eat the hazard effects — the genuine
  push-your-luck. **Convenience Store / Travel** are the low-variance single blind draws (whiff, don't
  fire).
- **Events lean hazard (~55–60% hazard / ~40–45% boon across the pooled decks)** — the CD's "cut the boon
  skew." They stay **warm-comedic** and **tax-not-destroy** (a hazard delays, reroutes, or taxes tempo;
  it never removes an ingredient you already hold or a whole turn). The boon minority keeps a Visit from
  being pure dread and preserves the "living island" warmth.
- **Where events sit:** hazards are **per-region cards in that region's deck** (a typhoon in the coastal
  South/East decks, plum rains in Central, scooter gridlock in the North). A few **table-wide** events are
  cards whose *effect* reaches everyone but still live in a region deck and fire when that region is
  Visited. `bg-developer` builds `events.csv` to this composition.
- **Recycling:** ingredient cards flow deck → Larder → (spent on a Bribe) → that region's discard; when a
  deck runs dry, reshuffle its discard (fired hazards return too, so the pressure persists).

**Event starter set (~14; secular, hazard-leaning, warm-comedic; wording via the consultant before lock).**
Hazards (the majority): **颱風假 Typhoon Day**, **梅雨 Plum Rains** (your Visit this turn keeps 1 fewer),
**完售 Sold Out** (discard the next specialty in this deck), **機車陣 Scooter Gridlock** (your next Travel
arrives empty), **客滿 Fully Booked** (shuffle this region's deck — reset the run), plus new per-region
hazards so every deck carries ~2 hazards. Boons (the minority): **芒果季 Mango Season**, **珍奶節 Bubble-Tea
Festival**, **臭豆腐大挑戰 Stinky-Tofu Dare** (opt-in push-your-luck), **再吃一點啦 The Aunty Insists**,
**網紅來了 Food Blogger** (table-wide next-Promote +1 Buzz), and — **the CD's dynamic value-swing boon** —
**摘星了！ Michelin Nod / 得獎了！ Competition Winner** (see below). *Reserve knob:* if blind decks feel too
swingy at the table, add a **"brewing" telegraph** (the top card of each region deck is face-up before you
Visit) — ~1 rule, restores preview agency.

**The "vendor gets hot" boon (CD, 2026-08-06 — makes vendor value DYNAMIC).** At least one boon event —
**摘星了！ Michelin Nod** (variants: **得獎了！ Just Won the Competition**, **爆紅 Went Viral**) — **places a
★ Star token on a Board vendor**, raising its worth to **+2 Prestige / +1 Rep** for whoever wins it (see
*Vendor value curve*). **Targeting (proposed):** the Star lands on the **lowest-Prestige unstarred vendor
currently on the Board** (ties → the revealing agent chooses) — deterministically turning *the most-ignored
stall* into a live contested prize neither agent set up, which **pulls both toward that region** and starts
a fresh Buzz fight. Warm, secular, and real (a genuine Taiwan food accolade; dish names intact). *(Design
knob → sim: the targeting rule — lowest-value vs revealing-agent's-choice vs Visited-region — and how many
of these events sit in the ~40% boon slice; 1–2 is the proposed dose.)*

---

## The Buzz-majority system (the headline mechanic)

The core, unchanged from v4. Read it as the Arcs-Court "agents on a card" mechanic, re-skinned to **hype on
a vendor** and lightened for a 2p duel.

**The rules, plainly:**
1. **Buzz is committed, public, and region-gated.** **Promote** places **2 Buzz** from the supply onto one
   or two vendors **in your current region**. Buzz sits on the vendor card, face-up, for anyone to see.
   **Both agents may pile Buzz on the same vendor.**
2. **Winning = ingredients + a ≥2 majority + presence.** To **Bribe** a vendor you must be **in its
   region**, hold **at least 2 more Buzz on it than your rival**, and **pay its ingredient cost** (− region
   discounts). The majority is checked at the instant you pay. *(大哥 needs only a **tie or lead** — a ≥0
   margin — see Characters.)*
3. **On a win, all Buzz on that vendor clears to the supply** — winner's and loser's alike. The winner's
   hype "paid off" (spent); the loser's hype "fizzled" (the vendor chose the rival). Neither player gets
   Buzz back into a private pool (there isn't one). The loser lost **only tempo** — the actions they spent
   promoting — never ingredients or VP. **"Outraced, not robbed"** holds mechanically and thematically.
4. **Committing early is a risk *and* a weapon.** Every Buzz you place raises the bar a rival must clear to
   swoop (they need ≥2 over *your* current pile) — so early commitment can price a rival out. But Buzz
   placed is an action **not** spent sourcing the ingredients you also need — over-invest and you can't pay
   the Bribe when the moment comes.
5. **No private hoarding, no windfalls.** Because Buzz never enters a private pool and clears on every win,
   it **recycles** — a modest supply (~24 at 2p) sustains the whole game and keeps every placement a real,
   scarce choice.

**Why this is the anti-runaway brake.** Every vendor — however cheap its ingredients become as your
discount ramp grows — still demands you **win a contested, region-gated, undiscounted Buzz majority, one
Promote at a time, on-site.** The ramp cheapens only the *ingredient* half; the Buzz fight never ramps and
can be **actively raised by your rival.** So the courting *rate* stays capped at roughly **1 vendor per
2–3 turns** even fully ramped, and a fast/wide leader can't simply buy the board.

**The escalation question (a real risk to sim).** Two agents can keep piling Buzz on the same vendor, each
needing ≥2 over the other — a bidding war. Three things cap it: **(a)** you can only *win* with the
ingredients in hand and while on-site, so the war ends the instant one agent is ready to close;
**(b)** Buzz supply is finite (~24) — you physically can't over-stack every vendor; **(c)** every Buzz
placed is an action stolen from sourcing. Nonetheless — *is the war fun or a slap-fight?* is **Riskiest
Assumption #1** — and the **大哥 tie-win** pokes at exactly this floor (**Riskiest #1b**).

---

## Vendors — the engine cards (three types across two Acts)

A **Vendor** is a stall/cook who agrees to feature on your tour once you've wooed them (ingredients +
winning Buzz majority). **Three vendor *types*** (printed on the card — used for Missions and Prestige
value) are dealt across **two Acts**:

| Type | ~Count | Ingredient cost | Buzz to win (uncontested) | Prestige (VP) | Rep | Perk | Deck |
|------|-------:|-----------------|--------------:|--------------:|----:|------|------|
| **Stalls** | ~11 | **1–2** (in-region) | ≥2 | **1** | **+1** | its **region discount icon** (the base ramp) | Act I (top) |
| **Eateries** | ~8 | **2–3** (1 cross-region) | ≥2 | **3** | **+2** | region icon **+ one** of {Promote +1 Buzz · once/turn treat 1 specialty as any specialty when Bribing · +1 Rep on each future Bribe} | Act I (beneath) |
| **Marquee** | ~6 | **3–4** (2–3 regions) | ≥2 (but heavily contested) | **5–6** *(★ apex 7–8)* | **+2/+3** | a **strong** perk: a **wild region icon** · **or** Buzz-reach (place Buzz on adjacent-region vendors too) · **or** counts as **2** region icons · **or** +2 Rep on Bribing | Act II |

> **"Buzz to win ≥2" is the *floor* (uncontested).** The real cost of a Marquee is that your rival is
> fighting you for it — the ≥2 majority against *their* pile is what makes the night-market names hard, not
> a bigger printed number. The Act escalates on **contest intensity + ingredient/region breadth +
> Prestige**, not ever-larger Buzz numbers (which would just drain the supply).

### Vendor value curve & ★ Star vendors — the swing that makes the fight worth it (CD, 2026-08-06)

**The Buzz fight only fires if the best vendors are *clearly* worth fighting for and worth crossing the
island to reach.** A flat value field means nobody contests and nobody travels — everyone just takes the
nearest convenient stall. So v5 builds a **deliberate value curve**, humble stalls → standout stars, not a
flat one:

- **The printed curve (an ~8× top-to-bottom spread):** a humble **Stall = 1** Prestige · a solid
  **Eatery = 3** · an ordinary **Marquee = 5–6** · and **2–3 apex "Legendary" Marquee = 7–8** carrying a
  **printed ★** (a standing **Michelin star / Bib Gourmand / recent competition win** — a real, warm reason
  *that* stall is the one everyone's chasing). The apex names are the **guaranteed Act II prizes both agents
  want** — worth an HSR haul across the island and several undiscounted Buzz to out-hype a rival for.
- **★ Star tokens (the DYNAMIC swing — makes value move mid-game):** a small supply (~4) of **★ Star
  tokens**. A **"vendor gets hot" boon event** (below) drops a Star onto a Board vendor — **+2 Prestige /
  +1 Rep** to whoever wins it. This can land on an *ignored humble stall* (1 → 3 Prestige), instantly
  turning it into a live contested prize and **pulling both agents toward that region** — travel pull and a
  fresh hype fight, on the fly. On the win, the +2/+1 scores and the token returns to the supply
  (recyclable). *(A printed-★ apex Marquee is a **standing** star; a Star **token** is a **new/temporary**
  one — same ★ language, one is baked, one is dynamic.)*
- **Why this is anti-flat *and* anti-runaway.** The swing gives the Buzz fight a **reason to exist** (a
  clear apex to converge on) without breaking the brake: an apex/starred vendor still demands the same
  region-gated, undiscounted ≥2 Buzz majority — it's just *worth overpaying for*, which is exactly the
  tension we want. The star is a **value** hook, kept distinct from the engine **perk** (a starred marquee
  with a strong perk = the ultimate prize — the game's natural climax fight).
- **Reputation/perk can echo the swing too:** the apex names carry the **+2/+3 Rep** end of the band and
  the strongest perks, so a star vendor is a jump on *all three* of Prestige, Reputation and engine — a
  triple reason to fight for it.

> **Sensitivity (binds — `identity.md`):** accolades stay **real and warm** — Taiwan genuinely has the
> Michelin Guide + Bib Gourmand street-food nods; frame a star as **celebration** (this beloved stall got
> its due), dish names intact, never a fabricated grand claim about a specific real business. → light
> consultant note (confirm the accolade framing reads as pride, not marketing spin).

**The discount ramp (kept, unchanged in spirit).** Each secured vendor carries a **region icon** (N/C/S/E,
or wild). Holding *k* vendors with the X-icon reduces the **X-region ingredient** portion of any future
vendor by *k* (floored at 0). Early vendors are dear; each one signed makes a *class* of future vendors
cheaper in ingredients. **Buzz is never reduced** — the brake.

**Re-cost note for `bg-developer` (unchanged from v4, pantry removed).** Re-cost the 25 vendors to **named
specialties only**, preserving the v3.1 *movement rebalance* (anchor every vendor in its own icon-region;
~40% carry a cross-region link; cap pork ≤5 / rice ≤5; every specialty on ≥3 vendors). Re-home the two
orphaned **wild_pantry** perks → the **wild_specialty** perk. **New v5 deck build:** the old T1/T2/T3 split
becomes the **Stalls / Eateries / Marquee** *types*; build the **two Act decks** as above (Stalls-on-top +
Eateries-beneath = Act I; Marquee = Act II).

> **Sensitivity (binds — `identity.md`):** East specialties draw on **Indigenous** cuisines — generic,
> respectful labels, consultant before art/print. Taiwan as itself; Traditional characters; Tâi-lô + 繁體,
> never mangled. The "Bribe" keyword must read as **warm comedy** (hype + goodwill), never corruption.

---

## Acts & end-game — the day-clock (replaces the 3-Act structure and the Season counter)

The game is **one escalating eating day** on a single **day-clock** — a marker that climbs **+1 every time
any agent Bribes a vendor** (win-paced, so it doubles as the catch-up co-brake). It has **two marks:**

**Act I · Afternoon Crawl 下午** (day-clock 0 → dusk).
- The everyday food — snack **Stalls** first, then sit-down **Eateries** as the afternoon warms up (the
  deck build surfaces them in that order). Cheap, low contest at first. This is where you **build your
  discount ramp** and stake early region positions.

**Dusk (the day-clock reaches the dusk mark).**
- **Sweep** any unwon Act I vendors off the Board (their Buzz returns to the supply — "the stalls you never
  got to are closing"), and re-stock the Board from the **Night Market (Marquee)** deck. The Act track
  moves to **Act II**.

**Act II · Night Market 夜市** (dusk → last train).
- The big names — expensive, multi-region, fiercely contested. Where the game is won or lost. Only Marquee
  vendors are winnable now, so every win from here is a night-market win.

**Code Red (the day-clock reaches the last-train mark).**
- **Head office calls Code Red** — mission's wrapping, catch the last train home. Finish the current round
  + one more full round → reveal missions → score.

**The concrete condition (this doc's call — the CD asked for one, ≤30 min at 2p):**

> **The day-clock is a single ascending marker, advanced +1 on every table-wide Bribe.**
> - **Dusk (Act I → Act II): the 6th table-wide win (2p).**
> - **Code Red: the 10th table-wide win (2p)** — i.e. **4 wins into the Night Market.**
> - **Backstop:** if the Marquee deck empties before the 10th win, Code Red fires immediately.
>
> *(3p: dusk 8 / Code Red 13. 4p: dusk 9 / Code Red 15. All → sim.)*

**Why these numbers.** ~10 total wins ≈ **5–6 per player**, at the game's proven courting rate (~1 vendor /
2–3 turns/player) = ~14–18 turns/player = **~25–30 min at 2p** — the CD's target. The split (6 afternoon /
4 night-market) gives a satisfying **build-then-cash arc**: ~3 ramp vendors each in the afternoon, then a
short, sharp ~2-each Marquee scramble as the climax. It lands the finish **on the north-star image** (the
night market at neon-dusk).

**Why a single day-clock (one marker, two marks) over three Act conditions.** It is the **most elegant**
form of the escalation: one component, one "it climbs on wins" rule, two printed marks — cheaper to teach
than three per-act thresholds, and it **re-uses the removed Season counter's slot** as a *day*-clock tied
to **wins, not turns** (so it keeps the v3.1 catch-up co-brake: fast winning hurries the end; a tall/slow
player leaves the mark far off and gets more turns to reach parity).

---

## Missions — the secret +7 (draw-3-keep-1), now the sole breadth carrier

Deal **3**, secretly **keep 1**, discard 2 unseen. A mission is a **secret vendor pattern** worth **+7 at
scoring** (binary). **With Region-Coverage cut as a track, the grand-tour "breadth" line lives here.**
Starter pool (variety on purpose; re-tuned for the shorter ~5–6-win game):
- *"a vendor in **all 4 regions**"* (**the grand tour — the breadth carrier**)
- *"**3 vendors in the South**"* (region concentration)
- *"**3 Stalls**"* (go wide-and-cheap)
- *"**2 Marquee** vendors"* (go tall/night-market)
- *"a vendor of each of **3 named cuisines**"*
- *"vendors totalling **≥ 14 Prestige**"* (go tall — retuned down from 18 for the shorter game)
- *"**5 vendors, any**"* (pure volume — near-max for the shorter game; a stretch)
- *"a **Marquee + two Stalls** of its feeder regions"* (a themed combo)

Draw-3-keep-1 (not a random deal) lets you steer your character/track synergy on purpose and launders the
char×mission balance problem (you *choose* the combo; the opponent sees your public character and
contests). **Open number → sim/table:** re-confirm each pattern is *achievable but not trivial* in a
~5–6-win game (the grand-tour and 5-vendor patterns are the tight ones).

---

## Economy & math

The Buzz-majority + push-your-luck market are the make-or-break. Numbers below are first-pass — the sim's
job is to attack them (see *Riskiest assumptions*).

**Income vs spend (per action):**

| Action | Yield (EV) |
|--------|-------|
| Visit the Local Market | +~1.3–1.7 specialties (region-gated) − hazard exposure *(大胃王 +~0.5; 媽寶 −~0.6)* |
| Convenience Store | +~0.6–0.8 specialty (blind, any region, can whiff) |
| Travel | +~0.7 specialty + reposition |
| Promote | +2 Buzz **onto the board** (no private gain — a positional investment) *(網紅 +3)* |
| Bribe | − ingredients (− discount); win vendor → +Prestige +Rep +perk; clears the vendor's Buzz |

**Cost of a vendor, in actions (the real currency).** Uncontested, a vendor costs roughly: **source its
ingredients** (1–3 Visits/draws, fewer as the ramp grows) **+ ≥1 Promote** (to reach the ≥2 floor) **+ the
Bribe** — call it **~3–4 actions early, ~2–3 actions ramped.** Contested, add a Promote or two. So the
**courting rate** sits at **~1 vendor / 2–3 turns** and never approaches 1/turn.

**Buzz supply sizing (2p ≈ 24).** At any moment ~2–4 vendors carry 2–6 Buzz each (≈ 8–16 committed), the
rest in supply; wins recycle it. The supply size is the first Buzz-fight tuning knob. Scales with player
count (≈ +8–10 per extra player).

**Balance assumptions (attack these):**
1. **The binding constraint alternates** — a feature. *Early (afternoon):* ingredients bind (can I dig the
   specialty out of a hazard-y deck?). *Late (night market):* the ramp trivialises ingredients, so **the
   Buzz fight + position** bind. Keeps decisions fresh across the day.
2. **VP/turn stays flat-ish across types** (~1.1–1.9) so no type is an auto-win; Stalls pay **indirectly**
   (cheap icons make everything else cheaper), Marquee pay in Prestige + mission synergy, not raw rate.
3. **Larder cap 7** (ingredient cards) forces the source→spend rhythm.
4. **Target 2p winner ~24–34 total VP** (retuned for the shorter ~5–6-win game; the wider ★ value curve
   lifts the top end). Rough split: vendors' Prestige ~16–24 (incl. any ★ apex/Star swing) + Reputation
   end-VP ~4–6 + signature mission 0/**7**.

---

## Scoring / win condition — "Top Agent"

Hybrid multi-track, now **two live tracks + one hidden vector** (Coverage cut). Tracks pay bonuses,
**highest total VP wins** (no sudden-death — warm, and a trailing player always has a live second vector).
At game end each agent totals:
1. **Tour Prestige (VP)** — sum of your vendors' stars (Stalls 1 / Eateries 3 / Marquee 5–6 / **★ apex or
   Star-token'd 7–8**). *(Live on the VP track.)* — the **tall / prestige** line, and the axis the **★ Star**
   swing amplifies.
2. **Reputation** — end-VP by final marker position: **3→+2 · 6→+4 · 9→+6 · 12 (max)→+9.** Climbed by
   Bribing (each vendor's printed Rep). *(Live on the Rep track.)* — the **reputation-climb** line.
   *(Milestone perks passing 3/6/9 are cut — Rep is pure end-VP; a clean parallel scorer. Banked ≈0.15.)*
3. **Secret signature mission** — **+7 if completed** (revealed now), else 0. **The one hidden vector, and
   now the carrier of the breadth/grand-tour line** (the "all 4 regions" pattern).

Highest total is **Top Agent**. **Tiebreak:** highest Reputation, then most vendors, then most regions
covered. *(Regions are no longer scored, but remain a sensible final tiebreak — it rewards the grand tour
one last time.)*

**Designing out a dominant line (they pull against each other).** Prestige rewards *few, big* vendors; the
discount ramp rewards *many, doubled-up in a couple of regions*; the grand-tour mission rewards *one in each
region*; Rep rewards *steady Bribing*. You cannot max ramp-concentration **and** the grand-tour mission at
once. The Buzz fight injects **opponent-dependence** — the "best line" shifts with where your rival commits,
so no opening is statically solved. (Sim probe #2.)

---

## Randomness

- **Input randomness (the bulk):** the Vendor Board reveal, the **face-down market decks**, the Mission
  draw (mitigated by draw-3-keep-1), the deck orders. The market is **blind** — a deliberate increase in
  variance to feed the push-your-luck.
- **Bounded output randomness (the spice):** the **Visit** flip resolves *after* you chose to dig. Bounded
  to *spice, not decide*: you **keep 2 of 3**, hazards are **tax-not-destroy**, deck composition is known,
  and the **Convenience Store** + **Travel** are the low-variance valves. Digging is opted-into
  push-your-luck.
- **The Buzz fight and the Bribe are pure open-information** — no dice, no post-Bribe luck. The skill of
  the engine stays legible; the luck lives only in what the market decks hand you.
- **One hidden-information hook only:** your secret signature mission. Larder, both tours, all Buzz on the
  board, and both tracks are open. No deduction engine.

---

## Interaction & tension

**Direct (the spine):**
- **The Buzz-majority tug-of-war.** The public, escalating, on-site fight over each prize vendor. You *see*
  your rival's Buzz piling on the seafood marquee and must decide to out-commit, race them to the
  ingredients, or concede and take a different vendor. **Anti-resentment:** a lost fight costs only tempo
  (your Buzz fizzles, you keep every ingredient) and reads as *the vendor chose them* — **"outraced, not
  robbed."**
- **Positional denial.** Being *on-site* gates Promote and Bribe, so occupying a contested region and
  stacking Buzz is a way to pressure a vendor and read your rival's intentions.
- **Market scarcity.** A region deck running dry (both agents digging the same market) is a natural reroute
  pressure.

**Catch-up vs runaway (designed):**
- **Against runaway:** the **contested Buzz floor**, **diminishing returns** on cheap vendors, **finite
  Buzz supply**, and the **day-clock co-brake** (fast winning hurries Code Red).
- **For catch-up (gentle):** the **day-clock co-brake** (a tall/slow player gets more turns before the
  last train), the **multi-track structure** (a trailing player always has a live second vector), one
  **table-wide hazard** with a leader-excluding sop (Typhoon Day gives Buzz to everyone *except* the
  Prestige leader), and the hidden **+7**.

**Fellowship** is carried by the comedic shared fight over a prize vendor ("you did *not* just out-hype me
on my noodle guy") + the market drama (table groans at a shared typhoon) — matching `identity.md`'s warm
rivalry, not mechanical co-op.

---

## Characters — asymmetry that bends the engine (v5 re-cast)

Five warm, food-obsessed **agent** archetypes — affectionate **Taiwanese social types** (`identity.md`
§Sensitivity), each **public**, each **one ability + one flaw on an opposing lever**. Abilities are
**flat/bounded — no compounding engine powers**. Target EV ≈ 2–4 VP or ~1–2 turns of tempo.

**v5 re-cast:** three KEPT kits are re-lored (numbers unchanged, no re-sim of the *kit*); **two NEW kits**
(大胃王, 大哥) carry proposed numbers that the **gated sim must tune.**

| # | Character | Ability | Flaw | Lever / anti-lever | Status |
|---|-----------|---------|------|--------------------|--------|
| 1 | **里長伯 The Old Councillor** | *Old Favours* — the first vendor you Bribe in **each of your first two regions** costs **1 fewer ingredient** (an old contact who owes him one). | *Works Every Room* — **no HSR** (rings the map the long way, stopping to chat). | ingredient discount / mobility | **KEPT** (was Night-Market Auntie) |
| 2 | **媽寶 The Live-At-Home Office Worker** | *Mum Packed You a 便當* — when you **Travel**, draw the top market card of the region you are **LEAVING** (a lunch from home) instead of the arriving region. | *Only Eats Mum's Cooking* — on a **Visit** keep only **1** specialty (not 2). | travel-sourcing / market-sourcing | **KEPT** (was Lunch-Box Granny) |
| 3 | **網紅 The Influencer** | *Going Viral* — your **Promote places +1 Buzz** (3 instead of 2) — the camera loves them. | *Chasing Clout* — go **last** in turn order and start **behind** (2 resources). | Buzz fight / tempo | **KEPT** |
| 4 | **大胃王 The Competitive Eater** | *Eyes Bigger Than the Table* — keep **all 3** cards on a **Visit** (not 2) — hauls loads. | *Head Down, Chopsticks Up* (**proposed**) — too busy eating to watch the weather: **hazards fire twice** when they hit on your Visit. | market haul / market risk | **NEW → sim** |
| 5 | **大哥 The Neighbourhood Big Brother** | *Everybody Knows 大哥* — wins a vendor's Buzz fight **without the ≥2 lead**: a **tie or lead (≥0 margin)** suffices (**proposed ≥0**). | *Always Picks Up the Tab* (**proposed**) — each vendor he Bribes costs **+1 ingredient** (he buys extra for the whole street). *(Alt: Promote places only 1 Buzz.)* | Buzz threshold / Bribe cost | **NEW → sim** |

**Design notes.**
- **里長伯 & 媽寶 are pure re-lores** of the v4 Auntie / Lunch-Box Granny kits — the *mechanics are
  unchanged*, so **no re-sim of the kit itself** (only the field-wide re-cast re-check). Bind the framing:
  里長伯's discount is **earned goodwill after a lifetime of service, NOT graft** — the beloved fixer, not a
  power-broker (⚑ politician + "Bribe" compounding-risk consultant flag). 媽寶 is warm — living at home is
  normal; the gag is the grown spy who still calls mum at lunch.
- **網紅's +Buzz is load-bearing now** (Buzz is the contested spine) — watch she doesn't over-perform; her
  go-last/behind flaw is the counterweight (may need re-tuning at count).
- **大胃王 (NEW, sim-legible).** Keep-all-3 is a **+1 specialty per Visit** edge whose real value is
  **deck-hazard-density-dependent** — so both the ability's worth *and* the flaw magnitude must be tuned.
  **Proposed flaw = hazards fire twice on his Visit.** This may over-brake (it taxes the very action the
  ability supercharges, in a hazard-heavy deck). **Lighter alternates for the sim:** *(a)* on a Visit where
  **any** hazard fires, keep only **2** that turn (so keep-all-3 only pays on a *clean* dig); *(b)* the
  **next** hazard in the deck also fires (a smaller, single tax). Flag: **the flaw may need to be light.**
- **大哥 (NEW, the make-or-break dominance probe).** *Everybody Knows 大哥* pokes **hardest at the central
  Buzz fight** — at a ≥0 margin he wins any vendor he's *matched* the rival on, where the rival needs a full
  ≥2 lead to deny him. That is a **large** edge; the **+1-ingredient tab** is the proposed brake, but it may
  **under-brake** (it taxes the ingredient half, which the discount ramp erodes anyway). **The two live
  knobs for the sim:** the **threshold** (≥0 tie-win vs ≥1 "must lead by 1") and the **flaw** (tab
  +1 ingredient vs the harsher **Promote-places-1**). **Bind HARD (`identity.md`):** vendors *like &
  respect* 大哥 and keep full dignity — the reduced threshold is **affection/reputation, never fear**; warm
  cinema bluster, never a shakedown; **secular** (street/cinema 角頭, NOT 八家將). ⚑⚑ tied-#1 consultant
  flag with "Bribe."

*(6th, held as expansion:* **The Homesick Local**, +/− tied to a self-picked home region.)*

**No dominant character×mission combo (verify in the gated sim).** Each ability sits on a *different*
lever, each flaw pulls against the mission it most helps, and draw-3-keep-1 launders the rest. The two NEW
kits (大胃王, 大哥) are **sim-legible by construction** (keep-all-3 and a Buzz-threshold delta are both
measurable) — the re-sim should seat all five; **大哥 is the one to watch.**

---

## Player counts & scaling

Base = **2p** (the design home; the Buzz tug-of-war is sharpest as a two-person fight). Deltas:

| Element | 2p | 3p | 4p |
|---------|----|----|----|
| **Vendor Board slots** | 5 | 6 | 7 |
| **Buzz supply** | ~24 | ~32 | ~40 |
| **Dusk mark (day-clock)** | 6 | 8 | 9 |
| **Code Red mark (day-clock)** | 10 | 13 | 15 |
| **Market deck size** | base | +1–2 event & specialty each | +2–3 each |
| **Buzz majority rule** | ≥2 over the rival | **≥2 over the *highest* rival** | ≥2 over the highest rival |
| **Start positions** | opposite (N & S) | spread on the ring | spread |

At 3–4p the Buzz majority is **≥2 over the highest single rival** on that vendor (not the sum). 大哥's
tie-win becomes **≥0 over the highest rival** — flag its 3–4p balance to `bg-architect` + sim (it may need
a floor bump at count). Resentment is **lower** at 3–4p (a lost fight is diffuse); the sharp balance case
is **2p**. **Best-at: 2p**; 3–4p a warmer, louder race. 25 vendors is comfortable at 2p; 3–4p may want a
few more per type (→ `bg-architect`).

## Solo mode / Automa

**Medium priority** (near-expected on a mid-weight engine). Sketch — a **"Rival Agency" Automa**:
- A small **Route deck**. On its turn, flip the top card: it **Promotes** (drops Buzz on the highest-
  Prestige contested Board vendor in a rotating "focus region"), **Bribes** (if it holds a ≥2 majority on a
  vendor in its focus region and its running ingredient counter can pay — locks it from you and advances the
  day-clock), **sources** (bumps its ingredient counter), or **rotates** its focus region. Its Buzz on a
  vendor is real and contests *your* majority — so the fight still bites solo.
- Pressure = **the Buzz race + the day-clock**. Difficulty = Buzz-aggressiveness + a target score. Upkeep
  near-zero. **Defer to `bg-architect`; not in the base MVP.**

## Complexity budget

Target **~2.4–2.5, ceiling 2.5** — now **holdable without a ceiling raise** (v5 spent both v4 trims).
`complexity-budget.json` caps (rulebook 1650 words, keywords 15, component types 8, aid 22 lines);
`bg-elegance` guards.

**The weight call (honest).** v4 pre-trim was ~2.5–2.6 (the Buzz-majority is the spend). v5 **banks**:
**Coverage → mission-only** (one fewer scoring track + no Coverage tick on Bribe; ≈ −0.1), **three Acts →
two on one day-clock** (fewer phases; ≈ −0.05 teach), **Rep milestone perks → pure end-VP** (≈ −0.15). Net
**~2.4–2.5**. The Buzz-majority remains the deliberate spend and the CD's headline ask; depth lives there —
protect it, cut around it.

**Keywords ≈ 12** (under 15): Larder · Vendor · **Bribe** · **Buzz** · **Promote** · region **discount
icon** · **Prestige** · **Reputation** · **★ Star** · **market deck** · signature **Mission** · **day-clock
/ Act**. (Visit / Convenience Store / Travel / specialty / Code Red stay plain-language.) *(Coverage keyword
dropped; ★ Star added for the value swing.)*

**The ★ Star cost (honest, for `bg-elegance`).** The Star adds **one keyword + one small token type**
(~+0.05 weight) and one event line. It's the CD's fix for a real hole — a flat value field where nobody
contests or travels — so it **earns the Buzz fight's whole payoff**; net weight holds **~2.5**. The printed
★ apex costs nothing (it's Prestige on existing cards); only the dynamic Star *token* is new.

## Keywords / glossary

- **Larder** — your sourced ingredient cards, **face-up**. Cap **7**.
- **Vendor** — a Board card (Stall / Eatery / Marquee type) you **Bribe** to secure; carries ingredient
  cost, a region **icon** (discount), **Prestige**, **Reputation**, a **perk**, and the **Buzz piled on
  it**.
- **Bribe a Vendor** *(LOCKED keyword)* — the core action: in the vendor's region, holding a ≥2 Buzz
  majority (≥0 for 大哥), pay its ingredients (− discount) to win it (the vendor **chose you** — the rival
  was outraced, not robbed). Carries the binding warm reframe (*"a marketing opportunity, not a bribe"*).
- **Buzz** — the committed, public, contested resource; **Promote** to place it **on vendors in your
  region**; never discounted; clears to supply on a win. The interactive anti-runaway brake.
- **Promote** — the action that places 2 Buzz (3 for 網紅) on vendor(s) in your current region.
- **discount icon** — a vendor's region badge; each held reduces that region's ingredient cost on future
  vendors by 1 (floored at 0). The compounding engine (ingredients only).
- **Prestige (VP)** — a vendor's star value; the headline VP vector; live on the track.
- **★ Star** — a value hook marking a **standout** vendor: either **printed** on an apex "Legendary"
  Marquee (a standing Michelin/Bib-Gourmand/competition accolade, worth 7–8) or a **Star token** dropped
  mid-game by a "vendor gets hot" boon event (**+2 Prestige / +1 Rep** to whoever wins that vendor; token
  returns to supply on the win). The deliberate value swing that makes a specific vendor worth crossing the
  island and burning Buzz for.
- **Reputation** — the parallel track climbed by Bribing; end-VP by final position (pure, no milestone
  perks).
- **market deck** — a region's face-down deck of its 2 specialties + events; **Visit** draws 3 keeps 2
  (hazards fire); **Convenience Store**/**Travel** draw 1 (whiff, no fire).
- **hazard / event** — a warm-comedic secular event card inside a market deck; hazards tax-not-destroy;
  fire only on a Visit.
- **signature Mission** — your secret **+7** vendor pattern (draw-3-keep-1); the only hidden info; now the
  carrier of the grand-tour breadth line.
- **day-clock (the Act track)** — the marker that climbs +1 on every table-wide Bribe; at the **dusk** mark
  the Board flips to the **Night Market (Marquee)** deck (Act I → II); at the **last-train** mark head
  office calls **Code Red** and the game ends.
- **Code Red** — the flavoured end-trigger (the day-clock's last-train mark): finish the round + one full
  round → reveal missions → score.

---

## Riskiest assumptions & the top-3 open questions for playtesting

**The single riskiest assumption:** **the Buzz-majority tug-of-war is fun and tense, not a swingy
slap-fight or a degenerate "never commit, always snipe"** — and **the 大哥 tie-win does not dominate it.**
New, load-bearing. The re-sim (once the CD approves) must lead with it.

**Top 3 open questions (in priority order):**

1. **Is the Buzz fight fun/tense and non-degenerate — including under 大哥? (THE make-or-break.)** *Attack
   (sim + table):* **Buzz-war frequency & depth**; **"snipe-only" win-rate** (≤~55% — early commitment must
   be viable); **loser's-tempo cost** ("outraced not robbed" vs feels-bad); **supply pressure** (~24
   right?); and **大哥's win-rate** at ≥0 vs ≥1 threshold, with the tab vs Promote-1 flaw. *Fail fixes:* the
   ≥2 margin (→≥1/≥3), Buzz-per-Promote, supply size, a partial loser-refund; for 大哥, the threshold + flaw.
2. **No dominant track or opening?** Do **tall ≈ rep-climb ≈ the grand-tour mission** stay competitive, and
   does the Buzz fight keep openings from solving (opponent-dependence)? *Attack:* dominant-track/opening
   probe (no line >~55%, ≥3 viable). *Fail fixes:* rebalance costs / track rewards / mission thresholds.
3. **Is the push-your-luck market spicy, not punishing — and does movement still spread?** *Attack:*
   **hazard-hit rate per Visit**, **Visit vs Convenience-Store usage**, **per-region sourcing share** (each
   ≥~18%; South not starved), **inter-region moves/game**. *Fail fixes:* hazard density, reveal-count, the
   "brewing" telegraph knob, cross-link rate.

*(Secondary: per-character 45–55% with the two NEW kits (大胃王, 大哥) — 大哥 the one to watch; the two-Act
day-clock pacing landing ~5–6 wins/player in **≤30 min**; mission patterns achievable in the shorter game.)*

---

## → Open numbers for the gated sim to tune (once the CD approves — DO NOT run yet)

- **Day-clock marks:** dusk **6** / Code Red **10** at 2p — does the game land **≤30 min** / ~5–6 wins per
  player? (The single pacing knob; adjust both marks together.)
- **Buzz supply size** (~24 @2p): too tight (can't contest) vs too loose (no scarcity)?
- **大胃王 flaw magnitude:** hazards-fire-**twice** vs the lighter alternates (keep-2-on-a-hazardous-Visit /
  next-hazard-also-fires) — keep-all-3's value is deck-hazard-density-dependent; the flaw may need to be
  light.
- **大哥 threshold:** **≥0 (tie-win)** vs **≥1 (must lead by 1)** — the make-or-break dominance probe.
- **大哥 flaw:** the **+1-ingredient tab** vs the harsher **Promote-places-1** — does the tab under-brake?
- **Board slot count / contest density** (5 @2p): fewer slots = sharper head-to-head Buzz fights.
- **Vendor value spread (the swing that drives contest + travel):** the apex Marquee value (**7–8**), how
  many are ★-printed (**2–3**), the ★ Star-token bonus (**+2 Prestige / +1 Rep**), and how many "vendor
  gets hot" boon events (**1–2**) + their targeting rule. Probe: do agents actually **cross the island and
  burn Buzz** for the standout/★ vendors (contest rate on top-value vs bottom-value vendors; travel-to-a-hot
  region rate), and does the swing stay *fun*, not *swingy* (a single lucky Star shouldn't decide the game)?
- **Character win-rate targets:** each **45–55%**, no dominant char×mission combo (里長伯 / 媽寶 / 網紅
  unchanged-kit re-checks; 大胃王 + 大哥 the real tuning).
- **Mission thresholds** for the shorter game (the ≥14-Prestige, 5-vendor, and grand-tour patterns).

---

## Decision for the Creative Director (the two live design calls)

Everything structural is locked; **two character numbers are genuine A/B/C calls** the CD may want before
the sim. (Both are also sim-tunable — the CD can defer either to "let the sim pick.")

**H1 — 大胃王's flaw (the counterweight to keep-all-3).**
- **A. Hazards fire *twice* on his Visit.** *(proposed.)* Taxes the same action the ability supercharges;
  simplest to state; may **over-brake** in a hazard-heavy deck.
- **B. On a Visit where *any* hazard fires, keep only 2 that turn.** Keep-all-3 pays only on a *clean* dig —
  elegant, self-scaling, thematically "the weather catches him"; slightly wordier.
- **C. The *next* hazard in the deck also fires.** A single, smaller tax; probably the lightest.
> *Recommendation: ship **A** into the sim, keep **B** as the go-to if A over-brakes.*

**H2 — 大哥's threshold + flaw (the dominance probe).**
- **A. Tie-win (≥0) + the +1-ingredient tab.** *(proposed.)* Biggest, funniest edge; the tab is a soft
  brake the ramp erodes — highest-ceiling, highest-risk.
- **B. Tie-win (≥0) + Promote-places-1.** Same big edge, a **harder** brake on his hype tempo — likely the
  safer pairing if A dominates.
- **C. Must-lead-by-1 (≥1) + the +1-ingredient tab.** A **smaller** edge (still beats the ≥2 floor) with the
  soft brake — the conservative option if a tie-win proves oppressive.
> *Recommendation: ship **A** into the sim as the headline probe; fall to **B** then **C** if 大哥 dominates
> the Buzz fight.*

---

## Handoff notes (guardian sweep — where to look)

**v5 — what moved (run `bg-theme` coherence + `bg-elegance` budget on the change):**
- **The signature twist is UNCHANGED in shape** (public on-site Buzz-majority fight for engine-piece
  vendors) — but two things around it moved that `bg-theme` should check: **(1)** the **two-Act day-clock +
  Code Red** end-game (does the "afternoon crawl → night market → last train" arc read on the north star,
  and is "Code Red" warm-not-menacing?); **(2)** the **五-character re-cast** (do 里長伯 & 大哥 stay
  rail-safe next to the "Bribe" keyword — the tied-#1 consultant flags?); **(3)** the **★ Star / accolade**
  value swing — do Michelin/Bib-Gourmand/competition nods read as **warm celebration** (this beloved stall
  got its due), and stay real/secular with dish names intact? (light consultant note.)
- **`bg-elegance` check:** teach-weight **down** to ~2.4–2.5 (both v4 trims spent: Coverage→mission, 3→2
  Acts, Rep→pure end-VP). Keyword count down to ~11 (Coverage dropped). Guard the rulebook word count.
- **`bg-access` / `bg-infodesign`:** unchanged component reads from v4 (Buzz piled on vendor cards; the
  day-clock is a single track with two printed marks — simpler than three act thresholds). Keep dual-coding.
- **`bg-developer` (AFTER CD sign-off — not yet):** re-tier the 25 vendors into **Stall / Eatery / Marquee
  types** and build the **two Act decks** (Stalls-top + Eateries-beneath = Act I; Marquee = Act II); build
  the **value curve** — Stall 1 / Eatery 3 / Marquee 5–6 with **2–3 apex "Legendary" Marquee at 7–8 marked
  with a printed ★** (real Michelin/Bib-Gourmand/competition accolades, dish names intact); add **~4 ★ Star
  tokens** + the **"vendor gets hot" boon event(s)** (摘星了／得獎了／爆紅) to `events.csv`; **remove the
  Coverage scoring track** (board + player-aid) and the Coverage tick from Bribe; print the **day-clock with
  dusk + last-train marks** in place of the 3-act track; bake the **five v5 characters** (里長伯 / 媽寶 =
  KEPT kits re-lored; 網紅 unchanged; **大胃王** keep-all-3 + the chosen flaw; **大哥** the chosen threshold
  + flaw); size the **Buzz supply** (~24 @2p); rebuild `events.csv` (hazard-leaning, in-deck); re-tune
  mission thresholds for the shorter game.
- **`bg-playtest` (GATED — DO NOT run until the CD signs off):** rework `sim/travel_agents.py` to model the
  **two-Act day-clock**, the **v5 characters** (esp. 大哥's threshold + 大胃王's hazard flaw), and the
  **mission-only breadth**; then run the three probes, **leading with Riskiest #1 (the Buzz fight, incl.
  大哥)**.

**Cut mechanics to sweep for stranded names/rules:** **Extract**, **Poach**, **pantry**, **Stock Up**,
**the Season counter**, **the three-Act structure**, **the Region-Coverage scoring track**, **event tiles /
the face-up Market**, and the **v4 character cast** (Night-Market Auntie / Eager Rookie / Lunch-Box Granny /
Grizzled Gourmand as *named* characters — their KEPT kits survive under 里長伯 / 媽寶). Check nothing in
components/rulebook/sim still references them.
