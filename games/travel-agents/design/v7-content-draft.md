# Travel Agents: Taiwan — V7 — the MULTIPLAYER RE-HOME (3–6 players, area-majority) — DRAFT

> **STATUS: V7 Phase-0 DRAFT (bg-architect + bg-design, 2026-08-08).** This is the build-ready
> **multiplayer** shape. It **supersedes the 2-player framing** of `v6.4-content-draft.md` /
> `v6.3-content-draft.md` (both stay as immutable history — read them for every mechanic V7 does not
> restate). The pivot is CD-signed (decision-log ★★ V7). **Numbers here are Phase-1 sim knobs** unless
> tagged LOCKED — the point of this pass is a coherent, encodable multiplayer *shape*, not final-balanced
> values. Everything the v6.4/v6.3.1 LOCKED block carries in is **re-scoped for N players, not re-opened.**
>
> **The pivot in one line:** Travel Agents is no longer a 1v1 duel. Design home = **MULTIPLAYER 3–6**
> (tune 3–5 solid, validate 6 as a stretch). The contested-vendor core is re-architected from a duel
> ("out-hype your ONE rival, lock them out") into a native **multiplayer AREA-MAJORITY** (pile Followers
> on a vendor; the highest committed present agent claims it; the losers' crowd disperses).

---

## 0. The load-bearing finding (why this re-home is low-risk)

The duel resolution the sim already encodes is **already an area-majority primitive.** `_buzz_lead`
computes `b[p] − max(committed by every other player)` — it measures your lead over the *strongest*
rival, not a named 1v1 opponent. And because **Promote always places a fixed 2** (v6.4 §Change 1),
every player's committed total moves in steps of 2, so committed *leads* are always even (0, 2, 4 …).
Consequently the duel's "**out-hype by ≥2**" and a clean multiplayer "**strict plurality — you must hold
MORE than every rival**" are **functionally the same rule.** The re-home is therefore mostly a
**re-framing** of the validated primitive to N players plus the scaling/economy consequences that a
crowded board forces — not a re-engineering of the fight. That is the good news that makes the
lost-war sink and per-count scaling (below) the real design work, not the majority rule itself.

---

## 1. Design-home count (recommend 4) + how 3 / 4 / 5 feel; 6 as a validated stretch

**Design home = 4 players.** Four seats is where the area-majority sings: enough agents that most
face-up vendors draw a genuine crowd, few enough that turns stay snappy and a single war rarely pulls
in everyone. Tune 3–5 to a solid finish; carry 6 as a *validated stretch* (ship it only if Phase-1
clears the length/downtime bar).

| Count | Feel | The dominant tension |
|---|---|---|
| **3** | **Tense triangles.** Every war is a live three-body problem — the third agent decides whether to enter (and pay in), sit out, or swoop the vendor a distracted pair ignored. Lowest downtime; the most *readable* politics. | "Do I join this fight or grab the quiet stall?" |
| **4 (HOME)** | **A proper crowded market.** ~1.5 face-up vendors per agent means you *cannot* all have your own stall — collisions are the default, not the exception. The lost-war sink fires most games, the dial does real work, and turns are still short. | "Which two wars can I actually afford, and which do I concede early?" |
| **5** | **Scrappy.** More agents than comfortable stalls; the night especially becomes a scramble. Downtime starts to matter — the one-action turn is doing heavy lifting. Watch 網紅's goes-last flaw (more claims land before her first turn). | "Concede fast, commit deep on one, and read the table." |
| **6 (STRETCH)** | **Chaotic street-market energy — and the risk zone.** Great theme fit, but **downtime and length are real**: a shared claim-clock of ~26 means ~26 turns/player, and five rivals act between your turns. Ship only if Phase-1's downtime proxy + length hold (see §8); otherwise cap the range at 5 and call it a great 3–5 game. | "Can the table keep the pace up?" |

**6p named risks:** (a) **downtime** — five opponents between your turns; the mitigation in §5 is
load-bearing here. (b) **length** — the shared vendor-claims clock scales with N; at 6p it is the #1
length knob (may need nudging *down* below the per-player-claims-constant target). (c) **turn-order
fairness** — a shared Taipei start + fixed order gives later seats (esp. 網紅) fewer early claims; a
Phase-1 seat-fairness probe gates 6p.

---

## 2. The contested-vendor CORE — re-architected to MULTIPLAYER AREA-MAJORITY

### 2a. The model (active-claim area-majority — recommended over end-of-round scoring)

A vendor is **not** scored by majority at a phase break. It is **actively claimed on a turn** by the
agent who holds the majority, exactly as the duel Bribe did — this keeps the game snappy and keeps
"win it *now*, lock everyone else out" as the beat. The alternative (place Followers all game, resolve
all vendors by majority at dusk/last-train) was **rejected**: it defers the payoff, kills the tempo of
the fight, and turns Promote into blind area-control instead of a live escalation you can act on. Keep
active-claim.

> **PROMOTE** *(you must be present, with the vendor(s))* — place **2 Followers** from your supply onto
> co-located vendor(s), any split, provided your **total committed Followers across all vendors ≤ your
> Followers-max (the dial)**. (Unchanged from v6.4 §Change 1 — the dial is a ceiling on your running
> total, not a per-action amount.)
>
> **BRIBE A VENDOR** *(you must be present)* — **you may claim a vendor only if you hold STRICTLY MORE
> committed Followers on it than every other agent** (see the tie rule, 2b) **and** you pay its
> ingredient cost (− your region discounts). On a Bribe: the vendor joins your tour as an engine piece
> (region-icon feeds the discount ramp; may complete a held Booking → tick your Tours-Completed counter,
> freeing a Booking slot); **your** Followers on it return to your supply (freeing your dial); the
> **losers' crowd disperses** (§3); refill the vendor slot; advance the vendor-claims clock +1. **A
> vendor never scores** — it is pure engine (tickets-only, §6).

**"Highest committed present agent wins" — stated for N players:** among all agents with Followers on
that vendor, the one with the most may claim it (by spending the Bribe action + paying). You must be
physically in the region to Bribe. Because Promote places a fixed 2, a lead is always ≥2 in practice, so
"strict plurality" and the duel's "out-hype by ≥2" are the same bar (§0).

### 2b. The tie rule — LOCKED recommendation: **a tie blocks the claim; break it or bail**

> **If two or more agents are tied for the most committed Followers on a vendor, NO tied agent may claim
> it.** To win it you must **out-commit** (Promote again next turn to take the lead) — or concede and let
> your Followers ride (or eventually disperse when someone else wins). The tie is the *engine of the
> promotion war*: escalate, or walk away.

- **Why this rule:** it makes the war self-fuelling and self-terminating. Tied agents keep Promoting
  (+2 each) to break the deadlock until one runs out of dial or Follower supply, or judges the vendor
  not worth it and bails — at which point the winner claims and the sink (§3) fires. This is exactly
  the CD's "the lost war must be the NORM, not a 5% edge case."
- **Rejected alternatives:** *first-to-that-count wins the tie* (needs a fiddly "who got there first"
  memory token per vendor — bad at 6p); *presence + turn-order breaks the tie* (hands a silent edge to
  early seats and lets you snipe a tie you didn't out-earn — reads unfair in MP). A tie that simply
  **blocks** needs zero extra state and pushes the drama the right way.
- **大哥 (The Big Brother) exception — re-scoped, all-game:** 大哥 **wins ties** (he needs only to
  *match* the lead, not exceed it — "the whole market yields to Big Brother"). This is his entire
  fight edge and it is stronger and more legible in MP than in the duel. *(This adopts the sim's
  win-on-a-tie edge but drops the unblessed "night-scoped only" restriction — a clean, always-on kit.
  Phase-1 confirms it does not tip him out of band.)*

### 2c. Icon-first / language-agnostic compatibility

Everything above reads off pieces, not text: **Followers = tokens stacked on a vendor card** (physical
majority is visible at a glance); the dial is a per-player readout; "present" = your pawn in the region.
No on-component CJK is required to teach or resolve the majority. The one rulebook sentence carries the
tie rule and the 大哥 exception (his mat gets a "wins ties" icon — bg-infodesign).

---

## 3. The lost-promotion-war consequence — now the NORM, a first-class economy lever

When an agent Bribes a contested vendor, the **losers** are every other agent with Followers committed
there. In the duel this fired ~5% of games; in MP it is the default, so its economy weight is central.

> **LOCKED recommendation — BURN the losers' committed Followers (the crowd disperses).** A loser's
> committed Followers on that vendor are **spent, not returned** — removed from play back to the general
> supply pool but **lost to that agent** for the campaign (they must re-earn dial headroom by Promoting
> again). The winner's own Followers return to *their* supply as normal.

- **Why burn (over a dial drop):** burn is a **contention-scaled sink** — the more agents pile in and
  the deeper they commit, the bigger the sink when the war resolves. It directly attacks the diagnosed
  imbalance (gains ≈17/gm ≫ sinks ≈6/gm; the ramped dial's top half is dead weight in the back half).
  It stings *proportionally to how hard you fought*, and it needs **no extra bookkeeping** (Followers
  just go back to the box/supply instead of to your reserve).
- **The dial-drop reserve lever:** a loser's **Followers-max −1** ("you overreached and lost face") is
  held as a **reserve escalation**, NOT the default. It adds a dial-tracking step and can *over*-punish
  (agents stop contesting, flattening the fight the game is built around). Recommend **burn alone**;
  let Phase-1 add the −1 dial drop only if the back half still isn't tense.
- **First-class lever framing (for Phase-1):** the sim already exposes `LOSTWAR ∈ {off, burn, dropmax,
  both}` + `LOSTWAR_DROP`. Phase-1 sweeps **burn / dropmax / both** *in the multiplayer context* and
  recommends the mix, alongside the two supporting levers (b) raise night/apex Follower demand + lift
  the ceiling, and (c) add Follower-sink events. **Do NOT force the fight rate as the primary knob** —
  in MP contention comes for free; the job is to land the economy **tense in the back half without
  starving/swinging**.

---

## 4. Per-count scaling (concrete numbers — Phase-1 knobs; fills the sim's n=5/6 fallback gap)

The current sim defines scaling dicts only for n=2/3/4 and `.get(n, <2p default>)` silently falls back
to **2p** for n=5 and n=6 — a real bug the encode step must fix. The table below extends the sim's own
arithmetic pattern cleanly up through 6.

| Per count | **3p** | **4p (HOME)** | **5p** | **6p (stretch)** |
|---|---|---|---|---|
| **Day vendor slots** N / C / S / E | 2 / 2 / 1 / 1 (**6**) | 2 / 2 / 2 / 1 (**7**) | 2 / 2 / 2 / 2 (**8**) | 3 / 2 / 2 / 2 (**9**) |
| **Face-up vendors ÷ players** | 2.0 | 1.75 | 1.6 | 1.5 | 
| **Followers supply** (table pool) | 33 | 42 | 51 | 60 |
| **Booking deck depth** (DAY / NIGHT) | 20 / 25 | 20 / 25 | +dup commons → ~26 / ~32 | +dup commons → ~28 / ~35 |
| **Booking face-up row** (shared) | 3 | 4 | 4 | 4 |
| **Booking hand-limit** (per player) | 3 | 3 | 3 | 3 |
| **Ingredient market depth** per region | ×1.4 | ×1.8 | ×2.2 | ×2.6 (vs 2p base) |
| **Vendor-claims clock — dusk** (table-wide claim #) | 7 | 9 | 11 | 13 |
| **Vendor-claims clock — last train** (table-wide claim #) | 14 | 18 | 22 | 26 |
| **Turn order** | fixed, clockwise from start player; **網紅 always last** | | | |

**How to read it (design intent, all sim knobs):**
- **Face-up vendor slots deliberately stay BELOW the player count** (1.5–2.0 stalls/agent). This is the
  area-majority engine: not everyone can have a private stall, so collisions are forced. Slots follow the
  sim's existing growth (N:2,C:1,S:1,E:1 → C:2 @3 → S:2 @4) and I extend it E:2 @5, N:3 @6.
- **Followers supply** follows the sim's `round(24 × (1 + 0.375·(n−2)))` → 33/42/51/60. The dial makes
  per-player commitment self-limiting, so the pool mainly needs to cover the **table's peak simultaneous
  commitment + in-flight burn** — Phase-1 confirms it never starves (watch `supply_min`).
- **Clock:** dusk = 5 + 2·(N−2), last train = 10 + 4·(N−2) — holds per-player claims roughly constant
  (~2 day + ~2 night each) while total claims scale with N. Night gets the larger per-player increment
  (the climax stays the longer act). **6p is the length watch:** last-train 26 ⇒ ~26 turns/player; if
  Phase-1 length runs long, the lever is to nudge the 6p last train *down* (e.g. 24) and accept ~fewer
  claims/player, NOT to add rules.
- **Bookings:** the 44-card set is fine to 4p; at 5–6p the shared face-up row empties fast, so **duplicate
  the common/easy patterns** to keep the row refilling (a data step, not a rules step — no new patterns).
  Widen the face-up row to 4 at 4p+ so choice survives the crowd. Hand-limit stays 3 (per player).
- **Start / first player:** all agents start in **Taipei (North hub)** (carried CD-3). First player is
  random (or "ate street food most recently" — flavour). 網紅 goes last every round (locked flaw).

---

## 5. Downtime mitigation (the key 5–6p risk)

**Primary mitigation — the one-action turn (already core; keep it, and lean on it).** A Travel Agents
turn is exactly **ONE action** — Visit, Convenience Store, Travel, Promote, Bribe, or Book a Tour. This
is the single biggest downtime lever a 5–6p game can have: even with five rivals between your turns, each
of their turns is one quick, legible move. **Recommendation: keep the one-action turn as the load-bearing
answer for 3/4/5, and make the board fully open** (all Followers, dials, and won-vendor tours public) so
players plan their single next action *during* others' turns — off-turn you are constantly re-reading
which war to join, so engagement stays high.

**Secondary — a soft analysis-paralysis cap.** With ~9 legal actions and a shared board, the AP risk is
"which war do I join?" The **Booking hand-limit (3)** already bounds your planning scope (you are chasing
at most 3 tours). Recommend the rulebook nudge "**plan your action while others take theirs**" plus an
optional friendly turn-timer for 5–6p groups — a suggestion, not a rule.

**6p-only stretch lever — simultaneous action selection.** *Only if* Phase-1's downtime proxy flags 6p:
each agent secretly picks their one action, all reveal, resolve in **turn order** (turn order breaks
conflicts — e.g. two agents Bribing the same vendor: the earlier seat resolves first, the later one's
majority may have evaporated). **Recommend NOT baking this** into 3–5p (it adds a reveal step and an
ordering rule for little gain at low counts, and it weakens the live read-and-react of the open board).
Hold it as a **6p variant** the sim/table decides on. Rejected as a base rule for that reason.

---

## 6. The carried v6.4 rules, re-scoped for N players

All of the v6.4 LOCKED block carries in; the area-majority re-home only *sharpens* the Promote/dial/
lost-war layer (it now fires constantly). Each stated in multiplayer terms:

- **Bookings hand-limit N=3** — per player, unchanged. Shared DAY/NIGHT slots along your play area;
  cancel-to-claim at the cap (→ Cancelled pile, −floor(v/2)); completing frees a slot. The **shared
  face-up Booking row** widens to 4 at 4p+ (§4) so the crowd doesn't strip it bare.
- **Followers dial + Promote-places-2 ≤ dial** — per player, unchanged. The dial is your ceiling on
  *total committed across all vendors*; in MP you will more often be forced to choose **which** war to
  fund because a rival is escalating a second one. The dial doing real work is now the norm.
- **網紅 (The Influencer) Followers-max starts at 4** — carried CANON. (The sim's committed default of
  3 is **unblessed exploration**, superseded by the pivot; Phase-1 re-bands her in MP — see §8 and the
  discrepancy note.) Flaw = **goes last** — flag: goes-last is **more punishing as N rises** (more
  claims land before her first turn), a Phase-1 seat-fairness watch at 5–6p; reserve fix is a small
  first-turn compensation (an extra starting ingredient or +1 dial), decided after the sim.
- **Base Travel = move + +1 Followers-max only, NO ingredient** — unchanged. **媽寶 (The Homebody) is
  the SOLE Travel-sourcer** (draws the region she LEFT and keeps it; event on that draw whiffs). In MP
  her sourcing edge is *relatively* larger (everyone else sources only via Visit / Convenience Store),
  the expected organic fix to her ~43% floor — Phase-1 confirms she lifts toward band without
  overshooting.
- **Trending (event-dropped "Gone Viral" marker) → winning a Trending-marked vendor grants +1
  Followers-max** — unchanged; in MP the marked vendor is a hotter contested prize (whoever wins the war
  also jumps their dial), which slightly worsens the gain-heavy economy → folded into the Phase-1 sweep.
  The printed ★ Michelin/Bib-Gourmand **apex** vendors remain a separate permanent thing (naming = Phase-2
  bg-theme).
- **Rave Reviews = per-player boons** at your 2nd (+1 Followers-max) & 4th (+1 ingredient / next Bribe −1)
  completed tour — unchanged, `perplayer` by construction (cannot pump a leader), which is exactly what a
  5–6p table needs (no runaway-fuel to the front-runner). Tours-Completed stays per-player on the
  character board.
- **Scoring = tickets-only** — Σ Complete-pile value − Σ floor(v/2) Cancelled-pile, per player,
  independent piles. Vendors and Followers-max never score. Tiebreak: most vendors → most regions →
  fewest Cancelled. **In MP this is a strong anti-kingmaking property**: since you only ever score your
  own tickets and never touch a rival's pile, there is no direct way to hand points to an ally — the only
  political lever is *which war you fund/concede*, which Phase-1 measures (§8).
- **Carried spine unchanged:** the CD-4 soft night-cost curve + full vendor table, the 44-Booking pattern
  set, 里長伯 home-region kit (−1 home / +1 away), Scheduled Maintenance ×2 (table-wide HSR outage —
  already a *multiplayer-native* beat, it closes the HSR for everyone), common Taipei start, 大胃王 keep-
  extra kit, the Greedy-Grab sinks, scoped events (⦿/⬢/➤), the sensitivity rails. Read v6.3/v6.4 for
  detail.

---

## 7. Hand-offs (describe only — do NOT build in this pass)

- **MAP (→ bg-infodesign / bg-developer, a light `regionmap` edit):** remove the **across-the-table
  orientation only.** Strip the two-sided mirror + the per-edge duplicated clocks; collapse to **one
  neutral shared board readable from any seat**. The **region diamond, ONE central day→night clock, and
  the realistic component scaling all stay.** No re-conception — an orientation edit. Add per-count
  start marker(s) in Taipei and enough face-up vendor slots for the 6p slot table (§4). This is the CD's
  confirmed "light edit, not a casualty."
- **THEME (→ bg-theme):** re-frame the identity opener "*two rival travel agents race…*" into a
  **crowded market of rival agencies** all chasing the same stalls. Naming/voice/lore stay; it is a
  framing shift from a duel to a scrum. Also still owed: the **Bookings 繁體** blessing and the printed
  ★ apex naming call (Phase-2). **Sensitivity rails remain BINDING** (Traditional characters only, real
  dishes never mangled, secular events, dignified local characters, anti-extraction framing; paid
  Taiwanese cultural + language consultant before art/print).

**Cost-budget note (bg-architect owns; flag for bg-funding):** the game has **no
`component-cost-budget.json` yet** — set one at this pivot. The 2p→3–6p move raises the bill (more
Followers tokens ~60 @6p, up to a 6th character board + dial, a larger neutral board, deeper market/
Booking decks). None of it adds a **component *type*** beyond the existing set (tokens / character boards
/ vendor cards / Booking cards / dials / one board / pawns / clock) — the cost driver is *quantity*, the
cheap kind that scales at print, not tooling. Recommend a soft COGS budget set alongside the (unchanged)
complexity budget (target weight 2.2, ceiling 2.5 — the area-majority adds **no new keyword**, it
re-frames the existing contested-vendor rule, so bg-elegance stays in band). Do not gate the design on
cost now; revisit at Phase-4 / with bg-funding.

---

## 8. SIM SCOPE for Phase 1 (CD-gated; kicking off the plan IS the go)

**Counts to run:** **focus 3 / 4 / 5** (solid), **validate 6** (stretch — a length/downtime gate, not a
balance target). Fix the n=5/6 scaling fallback (§4) in `new_state` before running, and encode: the
multiplayer majority (strict plurality via the existing `_buzz_lead` max; margin 1 for all, 0 for 大哥
all-game; tie blocks); the lost-war **burn** default (sweep dropmax/both); the carried v6.4 changes
(hand-limit 3; 網紅 start-max **4** — re-band from canon, not the sim's stale 3; base Travel de-sourced
with 媽寶 sole sourcer + the `_bump_src` fix; Trending +1 Followers-max on win).

**Probes Phase-1 must report, per count:**
1. **Character band** — all **SIX locked chars** (incl. 阿嬤, adopted as canon §9): **no crusher**; 媽寶
   lifts off its ~43% floor as sole Travel-sourcer without overshooting ~55%; 網紅 lands **≥45% / ≤~55%**
   at start-max 4 (reserve dial to 3 only if hot in MP); 大哥's win-on-a-tie edge stays in band; 阿嬤's
   mobility kit bands in 45–55% too (she's LOCKED in — if out of band, **tune her kit, don't drop her**).
2. **Seat / turn-order fairness** — per count; specifically whether the shared Taipei start + fixed
   order + **網紅 goes-last** creates a first/last-seat skew that worsens as N rises (the 5–6p gate).
3. **Downtime proxy** — legal actions / decision load per turn (`avg_legal_actions`, `forced_turn_frac`)
   **and** turns/player + wall-clock estimate; the 6p ship/no-ship signal for §5.
4. **Game length vs the clock** — does the last train reliably fire per count (vs stall backstop)? Is 6p
   length acceptable, or does the 6p last-train need nudging down?
5. **Multiplayer contested-vendor health** — how often vendors are **genuinely contested** now
   (`contested_frac`, `night_contested_wins`, `lost_wars_per_game`, `followers_per_lost_war`); and
   whether the **lost-war burn sink** lands the economy **tense in the back half** (gain-vs-sink per
   game, cap-bind day vs night, back-half committed-to-cap slack) **without starving/swinging**. Sweep
   **LOSTWAR burn / dropmax / both** + levers **b** (night/apex demand + ceiling) and **c** (sink events)
   *in the multiplayer context* and **recommend the mix**. Do NOT force the fight rate — contention now
   comes for free with more players.
6. **Night-sourcing health with base Travel de-sourced** — re-confirm the CD-4 target (~60–100% of the
   day rate) holds **per count**; flag, don't change, the night curve if it drops.
7. **Tickets-only health** — `ignore_obj` stays dead per count (a zero-ticket line still loses); the
   expanded deck's collection lanes aren't pinched by the hand-limit.
8. **Kingmaking / leader-pump at 5–6** — does targeting Promotes or concede-decisions swing *who wins*
   more than a threshold? (Tickets-only + burn-your-own-fight should keep this low, but 5–6p politics is
   the new worry that replaces the 2p fight-rate worry — measure it.) Include a take-that/griefing read.

---

## 9. CD RULING — roster = SIX characters (阿嬤 / A-má adopted as the canonical 6th)

**CD decision (2026-08-08): adopt 阿嬤 (A-má) as the canonical 6th character NOW** — Travel Agents V7 is
a **six-character** game, one unique face per seat up to a full 6-player table. This resolves the roster
fork by *committing* rather than *validating-then-blessing*: the CD chose six unique characters over the
"5 + duplicates at 6p" fallback, so the identical-twin problem in the area-majority fight never arises.

The canonical roster is now: **里長伯 (The Old Councillor) · 媽寶 (The Homebody) · 大胃王 (The Big Eater) ·
網紅 (The Influencer) · 大哥 (The Big Brother) · 阿嬤 (A-má)** — 阿嬤's kit: a gentle "reach any region in
one Travel" mobility ability (she already exists in the sim from v6.4d exploration).

**What adoption-now changes for the pipeline (vs the validate-first path):**
- **Phase 1 bands all six as LOCKED members** — if 阿嬤 (or any of the six) reads out of band, the lever
  is to **TUNE her kit to fit, not to drop her**. She is in the game; the sim tunes the numbers.
- **Phase 2 owes 阿嬤 a bg-theme identity + dignity bless** under the Taiwan sensitivity rails (a granny
  character must read warm and dignified, never a caricature). bg-theme framed her in v6.4d exploration
  (commit `0b46eef`); that framing must be re-confirmed as canon in the guardian sweep, alongside her
  naming (English name + 繁體) coherence with the other five.
- **Phase 4 builds a 6th character board** + her icon-only ability/flaw; component counts scale to six
  characters (a *quantity* bump, not a new component type — cheap for the cost budget).

**Other forks I hit and CALLED (noted so the CD can veto, not left open):**
- **Active-claim vs end-of-round majority** → chose **active-claim** (keeps tempo; §2a).
- **Tie rule** → chose **tie blocks the claim** (self-fuelling war, zero extra state; §2b).
- **大哥 edge** → chose **wins ties all-game** (dropped the unblessed night-scoping; §2b).
- **Lost-war sink** → chose **burn** as default, dropmax as reserve (§3).
- **6p downtime** → chose **one-action turns** as primary; simultaneous-select held as a 6p-only variant
  (§5).

**Other forks I hit and CALLED (noted so the CD can veto, not left open):**
- **Active-claim vs end-of-round majority** → chose **active-claim** (keeps tempo; §2a).
- **Tie rule** → chose **tie blocks the claim** (self-fuelling war, zero extra state; §2b).
- **大哥 edge** → chose **wins ties all-game** (dropped the unblessed night-scoping; §2b).
- **Lost-war sink** → chose **burn** as default, dropmax as reserve (§3).
- **6p downtime** → chose **one-action turns** as primary; simultaneous-select held as a 6p-only variant
  (§5).

---

## 10. Provenance & status

Folds the CD-signed V7 pivot (decision-log ★★) onto the v6.4 CD-LOCKED spec and the v6.3.1 spine.
The v6.4/v6.3 LOCKED block is **re-scoped for N players, not re-opened**. This is Phase-0 of the V7
plan; **Phase 1 = the CD-gated multi-count re-sim** (kicking off the plan is the go). No sim run, no
CSV/module rebuild, no game-bible/decision-log rewrite in this pass — those are the encode + review
phases. Numbers here are Phase-1 sim knobs unless tagged LOCKED.
