# Travel Agents: Taiwan — V7 — the MULTIPLAYER RE-HOME (3–6 players, area-majority) — DRAFT

> **STATUS: V7 Phase-1.5 DRAFT (bg-design, 2026-08-08) — layered on the Phase-0 shape below.** The
> Phase-1 re-sim landed **3–5p healthy, 6p broken** (0% last-train / 71% stall / 34.6 turns/player /
> supply_min 7.5; economy loose: gain ≈2.5–3× sink, slack_night ~5). The CD's fix — a **self-scaling
> DECK-DRIVEN clock** + a **DIAL-DROP lost-war sink** — is specced in the new **§11**, which is now
> **canon for pacing and the lost-war consequence** and **supersedes** the fixed vendor-claims clock
> (§4 clock rows) and the BURN sink (§3). Everything else in §0–§10 stands. This is the build-ready
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
> **losers' crowd disperses** (§3 → **superseded by §11d: each loser returns their Followers to their own
> supply AND their Followers-max dial drops −1 by day / −2 at night**); refill the vendor slot.
> ~~advance the vendor-claims clock +1~~ **← REMOVED (§11a: the clock is now deck-driven, not
> claim-driven).** **A vendor never scores** — it is pure engine (tickets-only, §6).

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

> **⚠ SUPERSEDED by §11d (CD direction 2026-08-08).** The Phase-1 sweep showed burn / dropmax / both all
> within noise (slack_night stuck ~5 at every count), so the CD replaced burn with a **DIAL-DROP** sink
> (Followers-max −1 by day / −2 at night). Read §11d for the canon lost-war consequence; the burn
> recommendation below is kept as history (and as the reserve fallback if the dial-drop over-suppresses
> contention).
>
> **~~LOCKED recommendation — BURN the losers' committed Followers (the crowd disperses).~~** A loser's
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
| **Booking deck depth** (DAY / NIGHT) — **now the CLOCK, see §11b** | 15 / 20 | 18 / 24 | 21 / 28 | 24 / 32 |
| **Booking face-up row** (shared) | 3 | 4 | 4 | 4 |
| **Booking hand-limit** (per player) | 3 | 3 | 3 | 3 |
| **Ingredient market depth** per region | ×1.4 | ×1.8 | ×2.2 | ×2.6 (vs 2p base) |
| ~~**Vendor-claims clock — dusk** (table-wide claim #)~~ **REMOVED — §11a** | ~~7~~ | ~~9~~ | ~~11~~ | ~~13~~ |
| ~~**Vendor-claims clock — last train** (table-wide claim #)~~ **REMOVED — §11a** | ~~14~~ | ~~18~~ | ~~22~~ | ~~26~~ |
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

## 11. PHASE 1.5 — the DECK-DRIVEN CLOCK + the DIAL-DROP lost-war sink (CD direction 2026-08-08)

> **This section is canon for pacing and the lost-war consequence.** It supersedes the fixed
> vendor-claims clock (§4 clock rows, now struck through) and the BURN sink (§3, now flagged). Written
> against the Phase-1 verdict: **3–5p healthy, 6p broken** — 6p ran **0% last-train / 29% deck-out /
> 71% STALL**, dragged to **34.6 turns/player** (vs ~28–30 at 3–5p), and **exhausted Followers supply**
> (supply_min 7.5, max_committed 10.2). The economy stayed **loose at every count** (slack_night ~5.0–6.5;
> gain ≈2.5–3× sink). Two design moves fix both, and they reinforce each other.

### 11a. ONE clock, deck-driven — REPLACES the vendor-claims clock (recommend)

**The BOOKING (Tour-Ticket) deck is the clock.** The day/night booking deck depletes as players draw
Bookings, and its exhaustion drives the day→night→end transitions:

> **DUSK** fires when the **DAY booking deck** is exhausted (flip the board to night).
> **LAST TRAIN** fires when the **NIGHT booking deck** is exhausted (the game ends).

**Why the booking deck (and not the ingredient market or the vendor deck):**
- **It is stall-proof by construction.** The Phase-1 stall (71% at 6p) happened because the *claim*-clock
  only advanced on a Bribe — and when supply exhausted, bribes dried up, so the clock froze short of its
  26th claim. A booking-drawn clock advances on the action **tickets-only scoring structurally forces**:
  you score *only* by completing Bookings, so you *must* keep drawing new ones — the deck depletes no
  matter how the fight is going. **The clock can no longer get stuck behind a stalled fight.**
- **It is monotonic** — the booking deck never reshuffles, so it strictly decreases and is **guaranteed
  to reach zero.** No stall backstop is needed; the 71%-firing backstop is deleted.
- **It is already a single clean DAY deck + NIGHT deck** (no per-region fragmentation like the ingredient
  market), so it maps 1:1 onto a two-phase clock with zero new bookkeeping.
- **It is thematically exact:** the day's tours **book out** → dusk falls; the night's last tours are
  gone → the **last train** leaves. The clock *is* the fiction.

**Exhaustion = a self-announcing boundary card (recommend over "pile empty").** Seed a **黃昏 DUSK** card
at the bottom of the day booking deck and a **末班車 LAST TRAIN** card at the bottom of the night booking
deck. When a refill turns up the boundary card, the transition is called — **no one counts cards, the
clock announces itself**, and nothing is telegraphed early. (The boundary card *is* the "fixed reserve of
1" the CD asked about; a raw empty-pile trigger works too but needs a glance-count.)

**Trigger resolution (exactly what happens on the turn it fires):**
- **DUSK:** finish the triggering player's turn, then flip to night at the start of the next turn — return
  any remaining face-up DAY Bookings to the box, deal the NIGHT Booking row from the night deck, bring
  night vendors/markets online. Bookings already in players' hands are kept and can still be completed.
- **LAST TRAIN:** finish the **current round** so every player has taken an equal number of turns, then
  end. Final scoring: each player completes/cancels their remaining hand as normal, then tickets-only
  scoring (§6).

**Reconciliation (CD directive 4) — REPLACE, do not double up.** The deck-clock is the **sole**
end-mechanism. **Delete** the vendor-claims counter, the dusk@/last-train@ claim thresholds (§4), the
"+1 clock on Bribe" step (§2), and the stall backstop. One clock, self-scaling, guaranteed to fire —
elegance says do not keep a second competing clock when one provably suffices.

> **FORK 1 (recommend A):** **(A)** booking-deck clock, replace the claims-clock *(recommended — stall-proof,
> single, thematic)*. **(B)** keep a per-count-scaled claims-clock as a backstop alongside deck-out *(rejected:
> two clocks to teach; the deck-clock cannot stall, so a backstop is dead weight)*. **(C)** drive the clock off
> the ingredient MARKET deck instead *(rejected: 4 regional decks → a fragmented trigger, and it would force
> consolidating region-specific sourcing).* Reserve: if the re-sim finds booking-draw too lumpy a clock at some
> count, switch the clock deck to a consolidated phase market deck.

### 11b. Deck sizes per count — the self-scaling rule (CD directive 1)

The booking deck is a **single shared deck** drawn by all N players, so **more players deplete it faster**
— pacing self-adjusts. Sizes (clock cards; the boundary card sits below these):

| | 3p | 4p (HOME) | 5p | 6p |
|---|---|---|---|---|
| **DAY booking deck** = 3·(N+2) | **15** | **18** | **21** | **24** |
| **NIGHT booking deck** = 4·(N+2) | **20** | **24** | **28** | **32** |
| clock cards **÷ players** (day+night) | 11.7 | 10.5 | 9.8 | 9.3 |

**Rule: DAY = 3·(N+2), NIGHT = 4·(N+2)** — a flat **+3 day / +4 night per extra player**, a constant 3:4
day:night ratio. Design intent:
- **It self-scales the length.** Because the deck grows *roughly linearly* with N while it is drawn by N
  players, **clock-cards-per-player stays nearly flat and even ticks DOWN** (11.7 → 9.3). That is the
  direct fix for 6p's runaway length: instead of the fixed claims-clock forcing ~34.6 turns/player, the
  shared deck empties faster the more players draw it, pulling 6p back toward the ~28-turn band.
- **Night is the longer, tenser act** (4·(N+2) > 3·(N+2)) — the climax you build toward (carries §4 intent
  + CD-4's night-cost curve), while §11d makes the night sink twice the day's.
- These are grounded in the sim's own booking depths (Phase-1 listed 20/25 → dup-to-~28/~35) but are now
  **the #1 re-sim knob**, since the deck *is* the clock: the re-sim tunes the two constants to land
  turns/player ~26–30 and DUSK ≈ half the game at every count.

### 11c. The night "shift gears" (CD directive 3) — symmetric trigger, distinct FEEL (recommend)

**Recommend: symmetric deck-out for BOTH transitions** (day-deck-out → dusk, night-deck-out → last train),
and make the night *feel* different through **tuning, not a different end-mechanism**:
- a **longer** night deck (4·(N+2) vs 3·(N+2)) — the climax runs longer;
- a **tenser** night — the **−2 dial-drop** (double the day's, §11d) + the carried **CD-4 cross-region
  night-cost curve** (marquees cost more and demand a two-region engine).

That is four real gear-shifts (length, sink weight, cost, cross-region) with **no second mechanism to
teach**. Directive 4 asked for one clean model; a *different* night end-trigger would reintroduce exactly
the elegance cost we just removed.

> **FORK 2 (recommend A):** **(A)** symmetric deck-out, night distinguished by tuning *(recommended)*.
> **(B)** night ends on **night-deck-out OR all ★ apex/marquee night vendors claimed, whichever first** —
> a "the best stalls are gone, nothing left to stay up for" beat; thematic, but adds a second end-condition
> to track. **(C)** night ends purely when all night-apex vendors are claimed *(rejected: claim-driven →
> re-imports the stall risk we just designed out).*

### 11d. The lost-war sink: the FOLLOWERS-MAX DIAL DROPS (CD directive 5) — REPLACES burn

When a contested vendor is claimed (someone Bribes it), every **loser** is an agent who had Followers
committed there (Promote places a fixed 2, so a loser always had **≥2** committed). For each loser:

> **1. Return** — the loser's Followers on that vendor go back to **their own supply** (the vendor left
> the board into the winner's tour; nothing is burned — this is the change from §3). This frees that much
> dial headroom.
> **2. Dial drop** — the loser's **Followers-max dial drops by 1 if it is DAY, by 2 if it is NIGHT**
> (night = the higher-stakes climax).
> **3. Floor** — the dial never drops below the **character's START value** (base characters = 2; 網紅 = 4).
> **4. Reconcile** — if, after steps 1–3, the loser's total *committed* Followers still exceed their new
> dial, they return Followers to supply (**their choice which**) until committed ≤ dial.

**Where the dial floors — recommend the character's START value, and this is mechanically load-bearing:**
- **Below 2, Promote breaks.** Promote places a **fixed 2** within your dial. A dial of **1 or 0 makes
  Promote illegal** (you cannot place 2 within a max of 1) — a player floored that low is **locked out of
  the fight entirely** = a runaway-loser death spiral, the opposite of a catch-up valve. **The floor must
  be ≥ 2 for the game to keep working**, and every character's start value is already ≥ 2 (2 base, 4 網紅).
- Flooring at **start value** claws back **exactly the ramp you earned** (Travel +1, Trending +1, Rave +1
  — the gain-heavy top half of the dial the economy audit flagged as dead weight) while **never pushing
  you below where you began.** It punishes overreach, not existence.
- It also gives **網紅 a start-value floor of 4** — a deliberate protection of her kit (she is the
  goes-last flaw character). *This is itself a fork — see §11g #6, because a higher floor makes her
  more sink-immune and she is already 6p-hot.*
- **Reject** floor at 1 or 0 (both break Promote / death-spiral) and a flat floor of 2 for everyone (drops
  網紅 below her start).

**The committed-over-max clause is provably DORMANT under return-first (but spec it anyway).** With step 1
returning ≥2 and step 2 dropping ≤2, you can show it never fires from a lost war alone: let the loser hold
dial `D`, total committed `C ≤ D`, with `k ≥ 2` on the lost vendor. After return, committed = `C − k`;
after drop `d ∈ {1,2}`, dial = `D − d` (before floor). Since `k ≥ 2 ≥ d`, we have `C − k ≤ D − k ≤ D − d`
— committed is **already within the new dial**, and the floor only raises the dial further. So step 4 is a
**safety net, not a live rule** in normal play; it becomes live only if a *future* lever ever drops the
dial from a non-war source (e.g. a "bad review" event). It also directly answers the CD's "confirm it
stacks with area-majority": it does — cleanly, and without a mid-resolution cap violation.

**Full Bribe/claim sequence (stacks with §2 area-majority resolution):**
1. Claimant pays the ingredient cost, takes the vendor into their tour (engine), **their** Followers on it
   return to their supply; may complete a held Booking → tick Tours-Completed, free a Booking slot.
2. **Each loser:** return their Followers on that vendor to their supply → **dial −1 (day) / −2 (night)**
   → floor at start value → reconcile if needed.
3. Refill the vendor slot. **No clock advance** (the clock is the booking deck, §11a).

**Worked example (night):** You hold dial **8**, committed 4-on-A / 2-on-B / 2-on-C (total 8). A rival
out-commits you and Bribes **A**. It is night. → (1) your 4 on A return to supply (committed now 4). (2)
dial 8 → **6**. (3) 6 > start 2, no floor. (4) committed 4 ≤ 6, no reconcile. Net: you got 4 Followers back
but your ceiling fell to 6 — you can no longer re-escalate to 8 on a future war until you re-earn the ramp.
That is the sink: **it taxes your future capacity, scaled to how many wars you lose.**

**Why the dial-drop fixes what burn couldn't:** burn removed *tokens* (which recycle) and tested within
noise (slack_night stuck ~5). The dial-drop removes *capacity* — it lowers the ceiling itself, so in the
back half dials sit **below** the ~7–10 they ramped to, `slack_night` (dial − committed) is squeezed from
both ends, and — critically for 6p — **lower dials mean less simultaneous commitment, so Followers supply
stops exhausting** (the supply_min 7.5 collapse eases). It is a **contention-scaled capacity sink**: the
more you fight and lose, the lower your ceiling.

> **FORK 3 (recommend A):** the lost-vendor Followers **(A) return to the loser's supply**, dial-drop is
> the sole sink *(recommended — the CD said "replaces burn")*. **(B)** *also* burn them (dial-drop + burn)
> *(rejected as default: double sink risks over-suppressing the fight — held as the §3 reserve if
> contention craters).*

### 11e. Expected effect on the Phase-1 problems

- **6p COMPLETES.** The deck-clock is monotonic and drawn by the forced booking action → **LAST TRAIN
  fires reliably**; STALL 71% → ~0%. Shared-deck depletion self-scales length → 6p turns/player pulls from
  34.6 back toward ~26–30. And the dial-drop suppresses back-half dials → less simultaneous commitment →
  **supply_min recovers** off 7.5. The two fixes compound: shorter game *and* lower peak commitment.
- **Economy TIGHTENS.** The dial-drop is a real capacity sink scaling with the very contention that drives
  the gains → **slack_night should fall** (target: off ~5.0–6.5 toward ~2–4) and the gain-vs-sink gap
  narrows. `capbind night` should rise (dials bind more often once they stop ramping unchecked).
- **阿嬤 (the floor) re-read.** She sits ≈ fair share at every count (idx ~0.98–1.06), i.e. lowest of six
  but essentially in-band, not broken. Her "reach any region in one Travel" kit lets her **pick which wars
  to enter and grab quiet cross-region stalls** — under a punishing lost-war sink, *avoiding* bad wars is
  worth more, so expect her to **hold or tick up**. Watch she doesn't overshoot. If out of band, **tune her
  kit, don't drop her** (CD ruling §9).
- **網紅 / 大哥 (6p-hot) re-read — the key new watch.** A *punishing* lost-war sink **relatively buffs the
  characters who lose fewest wars**: **大哥 wins ties** (he rarely "loses" a contested vendor → eats fewer
  drops), and **網紅's start-value floor of 4** makes her more sink-immune than base characters. So the
  dial-drop could **worsen** their 6p hotness (Phase-1: 網紅 idx 1.74, 大哥 idx 1.79) rather than cool it.
  Because 6p now *completes*, Phase-1's 6p bands (measured on broken games) are re-measured honestly for
  the first time — treat 大哥's tie-immunity and 網紅's floor as the two most likely tuning targets (reserve
  levers in §11g #6–7).

### 11f. Re-sim knobs & probes (for the CD-gated Phase-1.5 re-sim)

**Knobs to encode (before the run):**
1. **Deck-clock:** DAY deck = 3·(N+2), NIGHT deck = 4·(N+2) [3p 15/20 · 4p 18/24 · 5p 21/28 · 6p 24/32] as
   the sole clock; DUSK on day-deck-out, LAST TRAIN on night-deck-out (boundary-card or empty-pile).
   **Remove** the vendor-claims counter, the dusk@/last-train@ thresholds, the +1-on-Bribe step, and the
   stall backstop.
2. **Dial-drop sink:** `LOSTWAR=dialdrop`, `DROP_DAY=1`, `DROP_NIGHT=2`, `FLOOR=start_value` (2 base / 4 網紅);
   lost-vendor Followers **return to the loser's supply** (not burned); committed-over-max reconcile coded
   (expected dormant).
3. **Market decks** sized as an ample per-N resource pool that **reshuffles on empty** (NOT the clock) —
   confirm they never gate progress.
4. Carry all Phase-1 config otherwise (strict plurality, 大哥 wins ties, hand-limit 3, 網紅 start-max 4,
   base-Travel de-sourced + 媽寶 sole sourcer, Trending +1).

**Probes to report, per count (focus 6p):**
1. **6p completes?** end-condition breakdown — LAST TRAIN % (target ~100), STALL % (target ~0), deck-out %.
2. **Length** — turns/player (6p off 34.6 toward ~26–30) and dusk_turn ≈ half of last_turn.
3. **Economy tightens?** `slack_night` per count (falls off ~5–6.5), gain-vs-sink gap, `capbind night`.
4. **Supply** — `supply_min` per count (6p recovers off 7.5, stays clear of 0).
5. **Six-character band** on *completed* games — all six idx 0.9–1.1: does 阿嬤 hold/rise, and do **網紅 &
   大哥 cool at 6p or stay hot** (the sink-buffs-tie-winners watch)?
6. **Seat / turn-order fairness** per count (deck-clock changes pacing; re-confirm no first/last skew;
   網紅 goes-last).
7. **Tickets-only health** — `ignore_obj` stays dead per count.
8. **Dial-drop diagnostics** — drops/game; avg dial in the back half (day vs night); how often the
   committed-over-max clause actually fires (expect ~0); how often a player hits the floor.
9. **Contention not over-suppressed** — `contested_frac` / `lost_wars/gm` don't crater vs Phase-1 (the
   §3 worry: a sink so harsh players stop contesting). If it craters, reserve = night drop −2 → −1.
10. **Deck-clock robustness / kingmaking** — does the boundary card always get drawn (no full-hand
    booking deadlock, no new stall path)? Does controlling *when* to trigger dusk/last-train (booking to
    end the game while ahead) swing who wins beyond a threshold?

### 11g. CD SIGN-OFF CHECKLIST — the forks/numbers to confirm before the gated re-sim

1. **Clock driver = the BOOKING deck** (§11a Fork 1-A). Confirm, or pick market/consolidated.
2. **Replace the vendor-claims clock** (drop the counter + stall backstop; single clock). Confirm A over
   keeping a backstop.
3. **Exhaustion trigger = a seeded 黃昏 DUSK / 末班車 LAST TRAIN boundary card** (self-announcing) vs raw
   empty-pile. Confirm.
4. **Deck-size constants — DAY 3·(N+2), NIGHT 4·(N+2)** [15/20 · 18/24 · 21/28 · 24/32]. Confirm as the
   re-sim starting knobs (the sim tunes to ~26–30 t/p).
5. **Night = symmetric deck-out, distinguished by tuning** (§11c Fork 2-A) vs a distinct night trigger.
6. **Dial-drop floor = each character's START value** (≥2 keeps Promote legal; anti-death-spiral) — and
   the sub-fork: **網紅's floor = 4 (protect her kit) or capped at base 2** (remove her sink-immunity,
   the lever if she reads 6p-hot). Confirm the default (floor = start value, i.e. 網紅 = 4) and hold the
   cap-to-2 as the reserve.
7. **Dial-drop magnitude −1 day / −2 night** (§11d) vs symmetric. Confirm; hold night −1 as the reserve
   if contention craters (probe 9). And hold **大哥's all-game tie-win** as canon but flag it as the other
   likely 6p tuning target (reserve: scope his tie-win / add a small drop on a tie-win).
8. **Lost-vendor Followers return to the loser's supply** (dial-drop is the sole sink) vs also-burn
   (§11d Fork 3-A). Confirm A.

---

## 10. Provenance & status

Folds the CD-signed V7 pivot (decision-log ★★) onto the v6.4 CD-LOCKED spec and the v6.3.1 spine.
The v6.4/v6.3 LOCKED block is **re-scoped for N players, not re-opened**. This is Phase-0 of the V7
plan; **Phase 1 = the CD-gated multi-count re-sim** (kicking off the plan is the go). No sim run, no
CSV/module rebuild, no game-bible/decision-log rewrite in this pass — those are the encode + review
phases. Numbers here are Phase-1 sim knobs unless tagged LOCKED.
