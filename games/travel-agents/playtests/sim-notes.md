# Travel Agents: Taiwan — simulation notes (interpretation)

Hand-authored read of the sim runs. Owner: `bg-playtest`. Sim module: `../sim/travel_agents.py`
(encodes spine A, the design-doc rules as-written). Auto-generated tournament report:
`sim-results.md`. This file is the interpretation + the one change to test. **Nothing here has been
logged to the design-doc / bible / decision-log — that's the CD's call after reading this.**

## §V7 Phase-1.5 — deck-driven clock + dial-drop sink — VERDICT: 6p FIXED · economy tighter · new balance target is 里長伯-hot/阿嬤-floor · buff-the-weak wins the band

**★ 6p is FIXED.** The deck-driven clock (DAY 3·(N+1) / NIGHT 4·(N+1)) + scaled decks make every count finish: **end LAST TRAIN 3p 99% · 4p 100% · 5p 100% · 6p 97%** (Phase-1 6p was 0% / **71% stall**). turns/player 27–29 (target 26–30); `empty_mkt_draws 0.00`; **supply_min recovered 7.5 → 26–47**. The deck-clock is stall-proof exactly as designed — the root fix landed.

**Economy tightened.** `slack_night` 4.0–4.4 (was ~5–6.5). Dial-drops/gm rise with count (0.48→0.92→0.92→1.20), overwhelmingly at **night** (6p day 0.28 / night 0.92 — as designed); `floor_hits` rare (0.02–0.11); the committed-over-max clause fired **0.000×** (dormant, as bg-design predicted). Sink sensitivity: −1/−2 vs −1/−1 vs off sit close on slack (~3.8–4.3) → most of the tighten comes from the shorter deck-paced game; the dial-drop is a mild, thematic sink. **Keep canon −1/−2.**

**Health holds all counts:** tickets-only DEAD (`ignore_obj` 1.2–4.6% ≪ fair); seat fairness ok; downtime fine (`avg_legal_actions` ~9.5–9.9, forced 0, ~27 t/p even at 6p); night sourcing 67–131% of day.

**★ The balance story CHANGED — the "battlers" are no longer the problem.** The dial-drop + deck-pacing cooled 大哥/網紅 into the mid-pack (idx ~1.1–1.3); the §11f reserve levers barely move them and are **not needed**. The real outliers now:
- **里長伯 (Old Councillor) = TOP at every count** — idx 1.39 / 1.12 / 1.38 / 1.40 (escalation-ladder default 6p 1.60). The new hot character.
- **阿嬤 = FLOOR at every count** — idx 0.97 / 0.92 / 0.93 / 0.91. Persistently just below fair.

**CD escalation ladder — band spread (hi−lo idx; lower = tighter):**

| approach | 4p spread | 6p spread |
|---|---|---|
| defaults (canon dial-drop) | 0.31 | 0.63 |
| (1) nerf-battlers (reserve levers) | 0.57 | 0.42 |
| (2) remove-ALL-flaws | 0.34 | **0.77 (worst)** |
| (3) **buff-the-weak (阿嬤+媽寶)** | **0.23** | **0.32 (best)** |

**buff-the-weak wins decisively** — tightest band at both counts, by lifting the floor (阿嬤 0.95–1.16, 媽寶 1.23–1.24) rather than dragging the top down. **remove-all-flaws BACKFIRES** (frees the already-strong 里長伯/大哥 → 0.77 @6p). nerf-battlers is mis-targeted (the battlers aren't the issue).

**→ ONE CHANGE TO TEST (for CD sign-off):** adopt **buff-the-weak** — lift **阿嬤** (persistent floor) + **媽寶**, and consider a small **里長伯** trim (now the top, esp. 6p at idx 1.4–1.6). Reject remove-all-flaws; drop the reserve battler-nerfs (unneeded). Exact buff/trim numbers → bg-design to spec → confirm re-sim. **6p ships (no cap at 5 needed).**

**Headline:** the design's single make-or-break assumption — *is the Dead-drop tuned so cooperation is
individually rational?* — **FAILS as the rules are written**, and the fix is clear and proven in sim:
**add +1 VP per Dead-drop.** Kingmaking and the payout-C pick-race both PASS untouched.

---

## What the sim covers (and what it deliberately doesn't)

- **Shared "productive brain":** sourcing / routing / plating / tip-use is ONE greedy heuristic used by
  every strategy. Strategies differ **only** in Dead-drop policy (never / rational-when-jammed /
  aggressive) + recipient choice + the milestone pick. This isolates the variable under test exactly as
  `beacon.py` isolates the signal policy. **Bots are a floor on depth, not a ceiling.**
- **Insider Tips are modelled through wild-substitute-at-Plate only.** The extra-stock (+1 ingredient)
  and +1-travel-hop uses exist in the action space but the bots don't exploit them. **So the sim
  UNDER-values tips** — the real tip is more flexible than modelled. This matters for reading Q1 (below):
  the as-written game is somewhat *less* broken than the baseline number looks, but the core problem (a
  Dead-drop costs a whole turn) survives even a generous tip valuation.
- **Draw-2-keep-1 ≈ one random Assignment** per player (all types ~equal difficulty by design).
- **Deck = 24** built from the 14 exemplar recipes (dupes of night-market staples, ~46% cross-region).
  At 3–4p the Menu can deplete late (bots then Extract); a real 3–4p deck may want more cards / a
  reshuffle — minor, flagged.
- **Can't judge:** whether the tip decision is *fun*, teachability, table-feel, the "should I arm my
  rival?" ache. Those are the human 2p Screentop session. Simulate to de-risk and target, not to bless.

Game arc produced: ~19–21 turns/player, ~5.6–7 plates/player, margins ~4–8 VP, ties ~10%. Turns are on
target (design 18–24); plates run a touch under the 8–9 target (bots Extract / the Dossier ends it a bit
early). Assignment completion ~66–84% (both competent players usually bank the +7 — see caveat under Q3+).

---

## TEST 1 — Hoarder (H) vs Generous-tipper (G), 2p  → **FAIL as-written; PASS with +1 VP/Dead-drop**

Criterion (design-doc): **PASS = G ≥ H** by a small margin. Fail-high (H ≥ G) ⇒ co-op is a trap.

| Config (2p, ~2500 games/seating) | H win | G win | tie | verdict |
|---|---:|---:|---:|---|
| **As-written** (no +VP, cap 7) | **66.8%** | **24.0%** | 9.1% | **FAIL — H dominates** |
| +1 VP per Dead-drop | 41.1% | **47.0%** | 11.9% | **PASS — G ≥ H, small margin** |
| +2 VP per Dead-drop | 24.9% | 65.6% | 9.5% | over-corrected (G dominant) |

Corroborated by the full round-robin (`sim-results.md`, as-written): **`hoarder` tops the field at
~68%**, beating `generous` ~72–28 and even the rational `balanced` line ~69–24. **The co-op layer is
currently a trap** — the exact failure mode the design set out to design out.

**Root cause (not a symptom):** a **Dead-drop costs a full turn** but yields **one Insider Tip**
(≈ one flexible ingredient ≈ ~½ a Stock-Up). So it's a losing tempo trade *unless* the turn would
otherwise be wasted (jammed at the cap with nothing to Plate) — and good play makes that state **rare**.
Every Dead-drop also (a) hands a rival material and (b) pushes the shared Dossier end-clock, shortening
the game and costing the giver future Plates. Net: the giver falls behind. Hoarding + free auto-discard
wins.

**The Larder cap is the WRONG knob for this.** Lowering it barely moves Q1 (cap 5, as-written:
H 65.4% vs G 26.2%) — it forces a few more jams but doesn't touch the turn-cost math.
+1 VP per Dead-drop is the lever that works because it **directly pays for the turn**.

---

## TEST 2 — Kingmaker probe, 3p  → **PASS (both configs)**

Setup: players 1 & 2 both `balanced`; player 0 is an aggressive tipper whose **only** varied knob is
*whom* it Dead-drops to. Metric = how far a rival's win-rate moves between "p0 always feeds the leader"
and "p0 always feeds the trailer".

| Config | swing in a rival's win-rate (feed-leader vs feed-trailer) | verdict |
|---|---:|---|
| As-written | **2.8 pt** | PASS |
| +1 VP per Dead-drop | **3.1 pt** | PASS |

One player's tip-targeting **barely moves who wins** (<10 pt threshold), and the +1-VP carrot does
**not** open a kingmaking lever — because the reward is the giver's own (a Tip / +VP, not a boost handed
to a chosen ally) and the **≤1-Dead-drop-received-per-round cap** bounds gang-feeding. The receive cap is
doing its job; keep it.

---

## TEST 3 — Payout-C trigger-share & decisiveness, 2p  → **PASS (both configs)**

| Config | winner's share of milestone picks | +1-VP pick solely decisive | picks/game |
|---|---:|---:|---:|
| As-written (`balanced` mirror) | 50.4% (fair ≈ 50%) | 2.6% | 3.85 |
| As-written (`balanced` vs `dossier_greedy`) | 43.1% | 2.8% | 3.89 |
| +1 VP per Dead-drop (field avg) | 54.9% | 2.6% | 3.14 |

Picks spread ~evenly (no leader-sweep runaway), and the **+1-VP option almost never decides a game on its
own** (~2–3%). Payout-C is a light "tip it over" flavour race, as intended — **no change needed.**

**One watch-point introduced by the fix:** under +1 VP/Dead-drop the milestone-hunting line
(`dossier_greedy`) rises to the top of the field (62.6%), but only by **≤2 pt head-to-head** — no
crushing dominance. If human play shows Dead-drop-*farming* for VP, the containment is already specced:
restrict the +1 VP to **surplus / at-or-over-cap** Dead-drops, and/or cap milestone picks at 2/player.
Do **not** go to +2 VP (sim shows it flips to a G-dominant, spammy optimum).

---

## Health read (field, as-written vs fixed)

| Strategy | as-written win% | +1 VP/Dead-drop win% |
|---|---:|---:|
| hoarder | **68.6** (dominant) | 57.6 |
| assignment | 64.3 | 57.3 |
| dossier_greedy | 51.7 | **62.6** |
| generous | 51.5 | 59.1 |
| balanced | 52.1 | 51.5 |
| random | 11.7 | 11.9 |

As-written: a **naive hoard line dominates** and the co-op strategies sit at coin-flip — the co-op
centrepiece is inert-to-negative. With **+1 VP/Dead-drop** the field compresses into a healthy pack
(tip-active lines lead, but everyone within ~11 pt and no Condorcet crusher by wide margins), and every
real line crushes `random` (~12%). **Seat balance 2p:** seat0 48% / seat1 42% / tie 10% — a mild
first-player edge, within tolerance (not flagged). *(3p/4p seat balance: the harness `--counts` path
needs `new_state(rng, n)`, which the module supports; per-count self-play mirrors tie by construction, so
read 3–4p health from the kingmaker probe + the 3p smoke, not a mirror win-rate.)*

---

## The ONE change to test next

**Add +1 VP to the Dead-drop** (giver banks +1 VP in addition to the Insider Tip + Dossier step).

- **Expected effect:** turns the Dead-drop from a losing tempo trade into a live, individually-rational
  option — G ≥ H by a small margin (sim: 47% vs 41%), hoarding drops from dominant to mid-pack, and the
  co-op lines lead the field without any single line running away.
- **How the next test confirms it:** it's already re-simmed and passes all three tests. The remaining
  question is one the sim *can't* answer — **does the Dead-drop now feel worth doing, and does "arm my
  rival or not?" feel like a live decision?** → a **2p Screentop session** watching Dead-drop frequency
  and whether players deliberate over it (the decision-language test), plus a check that nobody just
  farms Dead-drops for VP (the watch-point above).
- **Keep exactly +1** (not +2), and hold the ≤1-received-per-round cap. Leave the Larder cap alone for
  the co-op question (it's the wrong lever here; revisit it only for hand-management *feel*).

**Sim-pessimism caveat when you read the magnitude:** because the sim under-values Insider Tips (wild-at-
Plate only), the as-written FAIL is a touch overstated and the *needed* carrot may be slightly under +1 in
the real game. +1 VP is the clean, robust dose to prototype; a Screentop session will show whether it
wants to shade toward a stronger *Tip* instead (Alternative B).

> **NOTE (2026-08-06):** everything above is the **v2 "Rival Agents, Shared Beat" (Plate/Dead-drop/
> Hot-List)** model, kept as history. The game has since pivoted to the **v3 vendor-courting ENGINE**
> (design-doc v3). The sim module was reworked to model v3; the v2 model is gone. Read the v3 section
> below for the current findings.

---

# v3 — VENDOR-COURTING ENGINE — simulation notes (2026-08-06)

Sim module: `../sim/travel_agents.py` (reworked for v3: court-a-vendor + two inputs [ingredients + Buzz]
+ the discount ramp + Prestige/Reputation/Coverage/+7-Mission + Season timer + Market events + 5
Characters). Auto tournament report: `sim-results.md`. This file is the **interpretation**. Nothing here
is logged to the design-doc / bible / decision-log — that's the CD's call after reading this.

**Headline (4 probes):** **Probe 1 (no dominant track/opening) PASS · Probe 2 (no runaway) PASS ·
Probe 4 (anti-hoard/stuck) PASS · Probe 3 (character balance) FAIL.** Plus one structural finding that
overshadows all four: **the Reputation-top-at-12 end trigger ends 100% of games at ~5 courts/player —
the Season end-timer (16) never fires and the "engine" barely ramps** (design intended ~8 courts / 18–22
turns). Decoupling that one trigger fixes the game length *and* tightens track balance.

## What the sim covers (and its blind spots) — bots are a FLOOR on depth, not a ceiling
- **Shared "engine brain":** every strategy uses ONE greedy court/source/route engine; strategies differ
  ONLY in vendor-value **weights** (Prestige / Rep / Coverage / mission / ramp) + an **opening flag**
  (buzz-first vs ingredient/ramp-first). This isolates "is a track/opening dominant?" exactly as
  `beacon.py` isolates the signal policy.
- **Encoding simplifications (LISTED):**
  1. Ingredients tracked at **region granularity** (N/C/S/E + Pantry), not per-specialty — because
     courting discounts are per-region. Intra-region scarcity (oysters vs milkfish) collapses into one
     per-region supply pool (`REGION_SUPPLY=13` at 2p ≈ 2× solo demand — **ASSUMPTION**, a knob).
  2. **Market events** modelled by mechanical payload (free Buzz / free ingredient / tempo tax / supply
     wash), fired per-refill at `EVENT_PROB=0.24` (**ASSUMPTION**), boon 60 / hazard 40. Rookie = skips
     hazards; Gourmand = boons do nothing. **Events are the least-faithfully modelled system** — this
     matters for the Rookie/Gourmand reads (their kits are event-coupled; see Probe 3).
  3. **T3 marquee cost/reward spread** is a concrete guess inside the doc's "3–4 ingredients (2–3
     regions), 5–6 Prestige, 2–3 Rep" band (**ASSUMPTION** — see `t3` table in the module).
  4. **Vendor deck**: T1×20 (5/region), T2×16 (4/region), T3×10; icons **balanced across all 4 regions**
     (the design's North-richest guard) regardless of North's 4 specialties.
  5. Draw-3-keep-1 mission = bot keeps the dealt mission best aligned to its weights (no opponent read).
  6. Wild icons / pass-9 free icon / T2 pantry-wild / Gourmand pantry-sub are greedy, not optimal.
  7. Bots essentially never **Extract** early (they let Season/Rep-top end it) — matches the doc's
     "Extract is a tempo option; the timer usually ends the game." Extract's push-your-luck *feel* is a
     human question, not a sim one.
  8. Influencer's "goes last + starts 1 behind" = last seat + opponents start +1 Buzz. `no-HSR` (Auntie)
     is a real routing restriction, but on a 4-region ring the sim likely **under-penalises** it.
- **Cannot judge:** whether the ramp *feels* satisfying, teachability/FTUE, the "outraced not robbed"
  ache, event *feel*. Those are the 2p Screentop session.

Game arc (balanced mirror, **as-written**): ~33 turns (≈16.5/player), **5.3 courts/player**, winner VP
≈ 38 (Prestige ~20 · Rep-VP ~8.5 · Coverage-VP ~8 · Mission ~6), margins ~10 VP, ties ~8%. **Season-
timed** (the fix): ~46 turns (≈23/player), **8.6 courts/player** — squarely on the design's 18–22
turns / ~8 courts targets.

---

## STRUCTURAL FINDING (the big one) — the Season end-timer is DEAD; Rep-top truncates the engine
`end by: rep=100% season=0% extract=0%` in **every** balanced/track config. Reputation accrues ~2.2/court
(T1 +1, T2 +2, T3 +2/3, plus rep-perks), so the **top (12) is hit in ~5 courts** — long before the
Season timer's 16 courts. Consequences:
- The game ends at **~5 courts/player, not ~8** → the compounding discount **ramp barely develops** (the
  signature "engine" beat is muted; icons only reach ~5), and turns run **~16.5/player vs the 18–22
  target**.
- The **Season end-timer is inert** — one of three advertised end-triggers never fires. Dead rules.
- Cheap-rushing is a **trap**: `greedy_cheap` (court cheapest now) finishes **dead last at 12%**, below
  even `random` (19%) — it hits Rep-top fast with low Prestige and ends the game while behind.

**Fix (one clean knob, sim-proven):** decouple the end-clock from Rep — **raise/replace the Rep-top end
trigger so the Season timer (courts) paces the game** (Rep still *caps* at 12 for its +9 scoring; it just
no longer *ends* the game). Modelled as `TA_REP_TRIGGER=99`. Result: **8.6 courts/player, ~46 turns**
(on target), the ramp fully develops, and — bonus — **track balance tightens** (Probe 1 leader drops
54.7% → 51.9%; see below). *Alternative knobs:* lower rep-per-court, or raise the Rep top to ~18–20.

---

## PROBE 1 — No dominant track/opening (2p) → **PASS** (and better under the fix)
Criterion: no line >~55%, ≥3 viable in a tight band.

| Regime | field leader | spread (7 real lines) | viable ≥45% |
|---|---|---|---|
| **As-written** (rep-top 12) | buzz_heavy **54.7%** | 45.3 – 54.7% | **7 / 7** |
| **Season-timed** (the fix) | buzz_heavy **51.9%** | 46.9 – 51.9% | **7 / 7** |

All seven track/opening lines (prestige-rush · rep-climb · coverage-spread · buzz-heavy · ingredient-
heavy · mission-focus · balanced) sit inside a tight band; **no solved line, no solved opening**
(buzz-heavy ≈ ingredient-heavy). Every real line crushes the naive floor (`balanced` beats `greedy_cheap`
99.8%, `random` 89.5%), and the field shows **intransitivity** (a depth signal) with only a ≤3–6pt edge
to the leader — no Condorcet crusher. The design's "several paths" holds. *(Watch: mild, mixed seat
effects in mirrors — some first-, some second-player — all within tolerance, not flagged.)*

## PROBE 2 — No economy runaway (2p) → **PASS** (the Buzz floor holds)
The compounding ingredient-discount does **not** explode: the undiscountable **Buzz floor caps the court
rate**. Even fully ramped, the **minimum gap between one player's courts = 2.00 turns** and the late-game
**court-interval = 2.06–2.11 t/court** (season-timed) — i.e. **~1 vendor / 2 turns, never 1/turn**, exactly
the design's predicted ≈2× ramp ceiling (1 Promote + 1 Court). The **binding-constraint shift is real**:
Buzz : region-ingredient spend climbs from **1.75 (early/as-written) → 2.76–2.93 (late/season-timed)** —
late-game you're gated by Buzz, not ingredients, as designed. First-mover/leader edge exists but is **not
a runaway**: mid-game leader wins **71–73%** (not ~100%), avg margin **8–10 VP** on ~38 total. *(As-written
can't runaway simply because it ends at 5 courts before the ramp matures — the meaningful runaway test is
the season-timed 8-court game, which passes.)*

## PROBE 3 — Character balance (2p) → **FAIL**
Criterion: each of 5 in **45–55%**; no character × mission combo **>~60%**.

| Character | win% (as-written) | win% (season-timed) | verdict |
|---|---:|---:|---|
| **Auntie** (per-region −1 ingredient / no-HSR) | **74.8%** | **71.0%** | **OP — robust across regimes** |
| Conductor (Travel +1 / Stock −1) | 51.0% | 51.1% | ✓ in band |
| Influencer (Promote +1 / last + behind) | 49.8% | 54.5% | ✓ ~in band |
| **Gourmand** (pantry-wild / no boons) | **38.7%** | **38.8%** | **too weak** |
| **Rookie** (event luck / larder cap 6) | **35.6%** | **34.6%** | **too weak** |

Hot char × mission combos (all **>60%**): **Auntie × grand_tour 82%**, Influencer × 2-Marquee 70%,
Conductor × volume_5 65%, Gourmand × volume_5 63%, Rookie × cuisines_3 62%.

**Root causes:**
- **Auntie is over-tuned and her flaw doesn't self-balance.** Her "first vendor in each region −1
  ingredient" is a *recurring* discount on the cheap/contested axis, and the design's claimed counter —
  the **no-HSR flaw** — costs almost nothing on a 4-region ring (the sim likely **under-penalises** it).
  The design-doc's specific claim that no-HSR balances her breadth synergy is **contradicted**: Auntie ×
  grand_tour is the single hottest combo at **82%**.
- **Rookie & Gourmand look weak, but their kits ride on the event system the sim ABSTRACTS.** Rookie's
  ability (event draw-2-resolve-1) is worth little when events are a thin `EVENT_PROB` roll, while her
  flaw (larder cap 6) applies fully; same shape for the Gourmand (pantry-wild modest, "no boons" applies
  fully). So the *direction* (both under-powered) is trustworthy, but the *magnitude* is inflated by
  event under-modelling — **confirm the exact buff at a table / with a richer event model, don't over-
  correct on the sim number.**

## PROBE 4 — Anti-hoard / hard-stuck (2p) → **PASS**
`hard-stuck turns/game = 0.000` — the **unlimited pantry + always-available Promote** valves mean a
player can *never* be unable to act (confirmed by construction and in play). Larder-overflow discards are
near-zero under efficient play (~0.06/game) and rise only when a bot over-stocks — i.e. **hoarding is
taxed, not free**, exactly as intended.

---

## Health read (full round-robin incl. naive)
Real lines pack into **~55–64%** overall (inflated by beating naive), with a **≤3–6pt** edge to
buzz-heavy and **intransitivity** present → **no crushing dominant line**. `random` 19%, `greedy_cheap`
12% (a trap — see the structural finding). *(Caveat: the harness's "Averaged game metrics" block in
`sim-results.md` mixes in the degenerate naive games — e.g. `turns 84`, `win_mission 0.0`,
`end_by_extract 17%` — so read game-feel numbers from the probe runner, not that block. The **win-rate
grid + health read** are the trustworthy signal there.)*

---

## The ONE change to test next
**Fix the end-clock first: decouple the Rep-top trigger so the Season timer paces the game** (Rep still
caps at 12 for its +9; it no longer *ends* the game). One clean structural knob.
- **Expected effect (sim-proven):** courts/player 5.3 → **8.6**, turns/player ~16.5 → **~23** (on the
  design's 18–22 target), the discount ramp fully develops (the signature engine actually builds), the
  dead Season timer comes alive, and track balance *tightens* (Probe-1 leader 54.7% → 51.9%).
- **Why first:** the engine-builder identity depends on the engine actually building; and character
  balance interacts with game length. Settle length, then re-sim, **then** do the character pass.
- **Next (a separate one-variable pass, post-fix):** **nerf Auntie** (e.g. cap Regular's Discount to the
  first 1–2 regions, or exclude marquee, or strengthen the flaw) and **buff Rookie + Gourmand** (e.g.
  drop/loosen the larder-cap-6 flaw; give the Gourmand 1 boon/game or soften "no boons") — but validate
  the buff magnitude at a table because their kits are event-coupled and the sim abstracts events.
- **What the sim CAN'T answer** → the 2p Screentop feel-test: does the ramp *feel* satisfying, does
  "court now vs race the rival for that icon" play as a live decision, and do the Market events feel
  *swingy-fun* not random?

**Knobs exposed for re-sim:** `TA_REP_TRIGGER` (end-clock), `TA_SUPPLY` (scarcity), `TA_EVENT_PROB`,
`TA_BUZZ_FLOOR` (+N Buzz on every vendor — raise the anti-runaway floor), `TA_DISC_CAP` (cap the ramp),
`TA_CAP` (larder).

---

# v3 — CHARACTER REBALANCE pass (2026-08-06, after the end-clock fix)

**End-clock fix is now the sim DEFAULT** (`REP_TRIGGER=999` → Rep-top no longer ends the game; the Season
timer paces it; Rep still caps at 12 for its +9). At the correct length (**~8.6 courts/player, ~46 turns**)
I re-tuned the five characters, **changing as little as possible**, to hit the 45–55% band with no
character×mission combo >~60%.

## Result — Probe 3 now **PASS** (was FAIL)
Per-character win-rate (balanced strategy, 5-way round-robin, both seatings; ±~2pt run-to-run):

| Character | before (as-written) | **after rebalance** | in band? |
|---|---:|---:|:--:|
| Auntie | 74.8% | **52 – 54%** | ✓ |
| Conductor | 51.0% | **53 – 55%** | ✓ |
| Rookie | 35.6% | **51 %** | ✓ |
| Influencer | 49.8% | **46 – 47%** | ✓ |
| Gourmand | 38.7% | **45 – 47%** | ✓ |

Worst char×mission (measured correctly — see note) = **rookie × t3_2 ≈ 57%** (<60). The old outlier
**Auntie × grand_tour (82%)** is gone (Auntie × any mission now ≤53%).

> **Methodology fix (important):** the first char×mission scans were artefacts. Pitting (char c + mission)
> vs a **neutral, abilityless** opponent inflated *every* combo to ~65% (you were measuring "having an
> ability at all," not a synergy). The correct probe is a **mirror**: (char c on forced mission m) vs the
> **same char c** on an aligned pick, both seatings — baseline ~50%, a spike = a real broken synergy. On
> that fair test all combos sit **53–57%**. The scan in `probe3_characters()` now uses the mirror.

## The changes (with the exact numbers) + confidence

**1. Auntie — NERF. CONFIDENT (sim-robust across regimes).** She was the clear outlier (71–75%).
- *Regular's Discount* now applies to the **first vendor courted in each of your FIRST TWO regions only**
  (was: every region), still −1 ingredient. Marquee (T3) **allowed** (excluding T3 as well over-nerfed her
  to ~43%). Flaw (*no HSR*) unchanged.
- Sim knobs: `AUNTIE_MAX_REGIONS=2`, `AUNTIE_EXCLUDE_T3=False`. → **52–54%**, and kills the 82% grand-tour
  synergy (her recurring per-region discount no longer scales with breadth).
- *Recommended design wording:* "**Regular's Discount** — the first vendor you court in **each of your
  first two regions** costs 1 fewer ingredient (she vouches for you around town)." Confident because the
  nerf holds whether the game is truncated or full-length; her flaw was doing almost no work on a
  4-region ring, so the fix is on the *ability*, not the flaw.

**2. Rookie — BUFF. SIM-PESSIMISTIC (event-coupled; confirm at a table).** She was worst (35.6%).
- Her whole kit rides on the **event system the sim abstracts** (`EVENT_PROB≈0.24`, tiny payloads), so the
  sim badly *under-values* "First-Timer's Luck." Relaxing her flaw (Larder cap 6→7) barely moved her; the
  lever that works in-sim is making her event ability actually pay. Modelled as `ROOKIE_EVENT_MULT=2.2`
  (events fire ~2× as often in her region and she keeps the boon of the two draws), **flaw kept at cap 6**.
  → **51%**.
- *Recommended design action:* **keep the printed kit as-is** (draw 2 / resolve 1, Larder cap 6) — do NOT
  hard-code a numeric buff off this pessimistic model. The sim only says "as printed she's too weak *if*
  events are as thin as modelled." **Confirm at the table with the real event tiles.** If she's still weak
  there, the cheapest real levers are: relax the cap to **7**, or make her ability **draw 3 / resolve 1**
  (more boon selection). Flagged, not locked.

**3. Gourmand — BUFF. SIM-PESSIMISTIC (his ability is structurally invisible to bots).** He was 38.7%.
- Diagnostic finding: giving him **2 or even 3** pantry-as-specialty substitutions per turn changed his
  win-rate by **0.0** — because the greedy sourcing engine *already* supplies the ingredients a vendor
  needs, so "courting flexibility" is redundant to a bot. **The pantry-wild ability only pays under
  tight-hand pressure a human feels and a bot never does.** The *only* in-sim lever that moved him was
  softening his "cannot benefit from boons" flaw.
- Sim knobs: `GOURMAND_BOONS="half"` (ignores ~half of boons instead of all) + `GOURMAND_WILD_USES=2`
  (kept, though it does nothing in-sim). → **45–47%** (he caps around there; the sim can't fairly seat him
  higher).
- *Recommended design action:* the honest read is **he is probably already close to balanced at a real
  table** (his ability is worth far more when hands are tight and boons matter). Minimal recommended change:
  **soften the flaw** from "cannot benefit from *any* boon" to something less absolute — e.g. "cannot gain
  **Buzz** from boon events" (he still enjoys ingredient/festival boons). Do NOT buff his ability off the
  sim — it's the most under-modelled thing here. Flagged, needs table confirmation.

**4. Influencer — light nudge. SIM-DRIVEN (watch).** Rose to the top edge (~55%) once Auntie was nerfed.
- His *Going Viral* (+1 Buzz on Promote) is genuinely **strong in this sim** because **Buzz is the binding
  late-game constraint** (Probe 2) — +1 Buzz income compounds against the ramp. Nudged his flaw from
  *starts 1 behind* → **starts 2 behind** (`INFLUENCER_BEHIND=2`) to settle him at **46–47%**.
- *Recommended design action:* keep *Going Viral* + *goes last*; **try "starts 2 resources behind"** (from
  1). Flagged as sim-driven: if the real event economy hands out more Buzz (Bubble-Tea Festival, Tourist
  Season, pass-6 perk), his +1 edge shrinks and **1-behind may suffice** — decide at the table.

**5. Conductor — UNCHANGED.** Stable at 51–55% before and after; leave as printed (*Travel arrives with 2 /
Stock Up takes 1*).

## Confidence summary (for the CD baking these into the design-doc)
- **Bake now (confident):** Auntie → *first two regions only*.
- **Provisional (sim-driven, low-risk to try):** Influencer → *starts 2 behind*.
- **Do NOT hard-tune off the sim — confirm at the FTUE/feel table (event-coupled):** Rookie and Gourmand.
  Recommend keeping their printed kits, watching their win-rate + fun in the 2p Screentop session, and
  applying the cheap levers above (Rookie cap 6→7 or draw-3; Gourmand "no Buzz-boons" instead of "no
  boons") **only if** the table confirms the weakness the abstracted-event sim is warning about.

## The ONE change to test next (this pass)
Lock **Auntie = first-two-regions** and **Influencer = starts-2-behind** into the design; carry Rookie &
Gourmand **as-printed with a table watch-flag**. Then the next real test is the **2p Screentop FTUE
session**, instrumented to record **per-character win/loss + whether Rookie's event-luck and the
Gourmand's pantry-wild actually earn their keep** (the two things the sim provably cannot judge).

**Sim knob defaults now baked (see the module header):** `TA_REP_TRIGGER=999` (end-clock decoupled),
`TA_AUNTIE_REGIONS=2`, `TA_AUNTIE_NO_T3=0`, `TA_ROOKIE_CAP=6`, `TA_ROOKIE_EVT=2.2`,
`TA_GOURMAND_BOONS=half`, `TA_GOURMAND_WILD=2`, `TA_INFL_BEHIND=2`.

---

# v3.1 — MOVEMENT REBALANCE + THE POACH — re-sim (2026-08-06)

Sim module reworked for v3.1. **Two changes under test; engine otherwise unchanged.** The biggest
fidelity gain over v3: the vendor deck is now **loaded from the real re-costed `components/vendors.csv`
(25 vendors)** at region granularity, so the sim finally sees the *anchor + cross-link* structure the
rebalance is entirely about — a vendor's **cost regions** (its named specialties = where you must stand
to source) are now **separate from its discount ICON region**, and they **differ on the 8 cross-link
vendors**. The old synthetic table collapsed cost≈icon and was blind to this. Plus **The Poach** is
modelled as a real conditional action + two strategies.

**Headline (6 probes):** the **two v3.1 changes PASS their make-or-break** — **Probe A (movement)
SOFT-PASS** (South fixed, camping dead; only East is slightly light) and **Probe B (Poach) PASS** (safe,
non-griefy, self-correcting). Of the re-confirms: **Probe 2 (runaway) PASS, Probe 4 (stuck) PASS,
Probe 1 (track) SOFT** (mild ramp skew from the re-cost), and **Probe 3 (characters) FAIL — a re-cost
knock-on** (the Conductor collapsed to 26.5% because the anchored deck made his Stock-Up-1 flaw brutal).

## Probe-by-probe (2p; n as noted; ±~2pt run-to-run)

### PROBE A — MOVEMENT SPREAD → **SOFT-PASS** (the make-or-break for this iteration)
Field-average per-region **sourcing share** (all 7 real lines, both seatings, n≈800):

| Region | v3 (lopsided) | **v3.1 sourcing share** | vs ~18% floor |
|---|---|---:|:--:|
| North  | ~20 tokens (dominant) | **38.6%** | (richest, as designed — 4 specialties) |
| Central| ~5  | **22.0%** | ✓ |
| South  | ~2 (**~6%** ghost town) | **23.8%** | ✓ **the headline fix** |
| East   | ~9  | **15.6%** | ✗ **just under the floor** |

- **Inter-region moves ≈ 7.5 / game** (~3.7 per player over ~23 turns) — real routing, not camping.
- **STAY-HOME control (`camp_home`, never-travels) wins 0.0%** vs balanced / coverage / ingredient
  lines (courts only ~4 of its 6 home-sourceable North vendors; scores ~18 VP vs ~55+). Camping is
  **thoroughly non-viable.**
- **CROSS-LINK-SUFFICIENCY VERDICT: 32% (6/8 North-bound) is ENOUGH — do NOT nudge the rate up.** The
  anchor+cross-link web makes every region a mandatory sourcing stop (a South-icon vendor like 蚵仔煎/
  火雞肉飯/牛肉湯 still needs a North token; coverage + regional-crawl missions punish concentration), and
  a pure stay-home line loses every game. The remaining gap is **not** a camping problem — it is
  **East-specific**.
- **Why SOFT not clean PASS: East sourcing is 15.6%, ~2.4pt under the ~18% floor.** Root cause: East
  T1s (竹筒飯/山蘇/麻糬) are cheap single-token + pantry, easily pantry-substituted, and only **2** of the 8
  cross-links import an East/South token (6 of 8 pull North), so nothing *drags* players into East the
  way North is pulled. **Knob (a data tweak for `bg-developer`, not a rules change):** add **~+1 East
  demand** — e.g. one more `greens`/`rice` naming, or **re-point one North-bound cross-link to East**
  (making it ~5/8 North + 1 East) — then re-run Probe A. Minor; the real East **boon events** (Bumper
  Harvest) that the sim abstracts may already lift East at a table, so this is a *watch*, not a blocker.

### PROBE B — THE POACH → **PASS** (a fun risk-reward, not degenerate/griefy)
| Test (n≈800) | Result | Read |
|---|---:|---|
| Situational-poacher win-rate vs balanced | **48.5%** | usable, **not** dominant |
| Situational Poach frequency | **0.11 / game** | low/situational (a **bot floor** — see caveat) |
| Aggressive poach-lean (griefer) win-rate | **33.5%** | **spamming Poach LOSES** |
| RATIONAL steal-war freq (situational mirror) | **0.03 / game** | **self-correcting — no griefy spiral** |
| Rep spent on Poach (griefer field) | ~2.3 / game | the **−1 Rep is a real, compounding tax** |

- The whole-turn cost + the undiscountable-Rep tax + the "no Rep, no Poach" floor make Poach a **losing
  staple** and a **non-spiralling** one: a rational mirror never wars (0.03/game), and forcing *both*
  bots to grief-max is a tautological arms race that still scores low and beats nothing (reported as an
  adversarial-stress note, not a verdict driver).
- **Caveat (bot-blindness, flag for the human table):** the greedy bots value Poach only as
  *self-sourcing when they can't take the token locally*, so they poach only **0.11/game** — they are
  **blind to the denial/tempo value** ("she's one oyster from the seafood marquee — swipe it") that is
  the human reason to Poach. So the **frequency is a floor**; the *fun* and the true rate are the
  Screentop question. The safety results (not dominant, no spiral, real cost) are robust regardless.

### PROBE 1 — No dominant track/opening → **SOFT** (mild ramp skew, new in v3.1)
7 real lines, both seatings, n≈350; naive excluded from the band:

| Line | v3.1 overall | | Line | v3.1 overall |
|---|---:|---|---|---:|
| ingredient_heavy | **58.2%** (leader) | | mission_focus | 47.3% |
| prestige_rush | 54.8% | | balanced | 43.6% |
| buzz_heavy | 52.6% | | coverage_spread | 42.8% |
| reputation_climb | 50.7% | | | |

- **5 of 7 in the 45%+ band**, every real line **crushes naive** (balanced beats greedy_cheap 99%,
  random 88%). No solved opening (buzz ≈ ingredient early). **But the band widened vs v3** (was
  46.9–51.9%): the **anchor-in-region re-cost genuinely buffed the ramp line** — each region's discount
  now saves on *that region's own* vendors, so `ingredient_heavy` (ramp-weighted) leads at 58.2% while
  spread/balanced lines sag to ~43%. Not a solved line (<60%, naive crushed), but a **real mild skew the
  re-cost introduced** — watch whether the ramp *feels* like the obvious line at the table.

### PROBE 2 — No economy runaway → **PASS** (Buzz floor holds)
Season-timed (the locked default): **8.6 courts/player, ~48 turns**; late court-interval **2.35–2.85
t/court** (≈1 vendor / 2+ turns even fully ramped — the Buzz floor caps the rate); B:I spend ratio
climbs **~2.5 → ~3.7–4.5** (binding constraint shifts to Buzz late, as designed); mid-game leader wins
**73–74%** (a real first-mover edge, **not** a ~100% runaway); avg margin ~6–8 VP.

### PROBE 3 — Character balance → **FAIL** (a re-cost knock-on; needs a fresh pass)
5×5 round-robin, balanced strategy, both seatings, n≈300:

| Character | v3 (synthetic deck) | **v3.1 (real deck)** | in band? |
|---|---:|---:|:--:|
| **Rookie** | 51% | **63.1%** | ✗ hot |
| **Influencer** | 46–47% | **61.3%** | ✗ hot |
| **Auntie** | 52–54% | **58.8%** | ✗ hot |
| **Gourmand** | 45–47% | **40.4%** | ✗ soft |
| **Conductor** | 53–55% | **26.5%** | ✗ **collapsed** |

Hottest char×mission (fair mirror): **Influencer × north_3 63.9%**, Gourmand × south_3 61.5% (both
>60%). **Root cause = the character knobs (`ROOKIE_EVT`, `INFL_BEHIND`, `AUNTIE_REGIONS`,
`GOURMAND_BOONS`) were tuned against the v3 *synthetic* deck and are now mis-calibrated to the real 25.**
The load-bearing new finding is the **Conductor**: on the anchored deck, single-region **2-of-one-region
costs are common → Stock-Up-2 is the core sourcing move**, so his **"Stock Up takes 1" flaw is now
crippling** (he courts ~7.6 vendors vs opponents' ~9.4). His **"Travel +2" ability can't compensate**
because you rarely need 2 *different* region tokens on one anchored vendor. This is **not** a bug and
**not** event-coupled — it is a direct, trustworthy consequence of the movement re-cost.

### PROBE 4 — Anti-hoard / hard-stuck → **PASS**
`hard-stuck = 0.000/game`, overflow discards `0.05/game` — pantry + Promote valves hold; hoarding taxed.

## The single biggest remaining issue + the knob
**Character balance regressed against the real deck — the Conductor at 26.5% is the largest single
deviation (23.5pt).** **Knob:** soften the Conductor's flaw (the anchored deck over-punishes "Stock Up
takes 1" — e.g. "Stock Up takes 1 *only on a turn he also Travelled*", or drop the flaw and re-tune the
ability), and re-seat the three hot chars (Rookie/Influencer/Auntie) — a **fresh character pass against
the v3.1 deck**. This is a *knock-on of the re-cost*, and it interacts with both the East fix and the
real event tiles (Rookie/Gourmand are event-coupled), so it should be one clean pass **after** the deck
settles — not stacked onto this change.

## The ONE recommended next action — decision for the CD (A/B/C)
- **A — Proceed to the instrumented 2p Screentop FTUE session (RECOMMENDED).** The two v3.1 changes
  **pass their make-or-break** (movement spreads, camping is dead → cross-links sufficient; Poach is
  safe, non-griefy, real-cost). The residuals — East slightly light, the mild ramp skew, and the
  character imbalance — are all **re-cost knock-ons best co-judged with humans + the real event tiles**
  (which the sim abstracts and which specifically feed East/Rookie/Gourmand), and the Poach's *fun/true
  frequency* is a human-only question. Instrument the session for per-region visit feel, whether the
  ramp *feels* solved, per-character results, and Poach frequency/feel. **Carry the Conductor
  imbalance as an explicit watch-flag** (or seat symmetric characters for the first teach).
- **B — One sim pass first: re-tune the characters to the real deck** (fix the Conductor flaw + re-seat
  the hot three), re-sim Probe 3, *then* the human session. Choose this if the CD wants a competitively
  fair 5-character lineup in the very session meant to judge characters. Risk: the deck may shift again
  after the East tweak / human feedback, so the tune may need redoing.
- **C — One data tweak first: lift East** (+1 East demand or re-point one North-bound cross-link to
  East), re-sim Probe A to clear the 18% floor, then the human session. Choose this only if the CD wants
  a clean movement PASS on paper before the table; otherwise East is a cheap watch-flag for the session.

**Recommendation: A.** Ship the changes to a human table — they work; the leftovers are exactly the
feel/event-coupled questions the FTUE exists to answer. Fold the Conductor fix + character re-tune (B)
and the East nudge (C) into a single follow-up re-cost-cleanup pass once the table has weighed in.

## Encoding simplifications (v3.1 — the sim's blind spots)
1. **Vendors loaded from the real CSV at REGION granularity** (a fidelity *gain*: cost regions vs icon
   region now distinct, cross-links faithful). Still collapses **intra-region** specialty scarcity
   (oysters vs milkfish both = "S"), because discounts are per-region. So Probe A measures **region**
   sourcing spread, not oyster-vs-milkfish spread.
2. **The Poach** models co-location (pawn position), a **random region-token** steal (not a specific
   oyster-vs-milkfish — fine at region granularity), Rep −1 floored, and no refill/event/Season.
   **Greedy bots under-value Poach's denial/tempo use** → the 0.11/game situational rate is a **floor**;
   the human rate/feel is unmodelled.
3. **`camp_home` control never travels at all** — a deliberate lower bound on camping. Its 0% win is
   partly inflated by a passive camper dragging the game long (letting the opponent run up score); the
   qualitative conclusion (camping non-viable) is robust, the exact 0% is not a precise VP claim.
4. **Character knobs carried over from the v3 synthetic-deck tuning** (`TA_ROOKIE_EVT=2.2`,
   `TA_INFL_BEHIND=2`, `TA_AUNTIE_REGIONS=2`, `TA_GOURMAND_BOONS=half`) — now **mis-calibrated to the
   real deck**; Probe 3 is the real-deck retest showing they need re-tuning (Conductor esp.).
5. **Market events** still modelled by mechanical payload at `EVENT_PROB≈0.24`, boon 60/40 — the
   least-faithful system; still matters most for Rookie/Gourmand and for the East boons (Bumper Harvest)
   that may lift East sourcing at a table.
6. **Absolute VP totals run high (~50–56 vs the design's 35–42 target)** on the real deck at region
   granularity (vendors slightly easier to afford; missions/coverage/rep all stack) — read **relative**
   balance as trustworthy, treat absolute totals as indicative only. (A supply/discount-tightness knob,
   or per-specialty scarcity, would pull totals down — a later tuning question, not a v3.1 blocker.)
7. Missions updated to the **real 9-mission deck** (adds north_3 / central_3 crawls; the v3 sim's
   invented `cuisines_3` is gone — no cuisine mission exists in `missions.csv`).

**Knobs exposed for re-sim:** `TA_POACH_REP` / `TA_POACH_FLOOR` (Poach cost/floor), plus the v3 set
(`TA_REP_TRIGGER`, `TA_SUPPLY`, `TA_EVENT_PROB`, `TA_BUZZ_FLOOR`, `TA_DISC_CAP`, `TA_CAP`, and the
character knobs). New strategies: `camp_home` (Probe A control), `poach_situational`, `poacher`.

---

# v3.1 — TWO SIM-CONFIDENT FIXES (Conductor + East), post-CD-decision (2026-08-06)

CD decision after the re-sim above: **fix the two sim-confident issues now, carry the event-coupled
characters (Rookie/Influencer/Auntie/Gourmand) to the human table untouched.** Both fixes are now the
**sim defaults** (`TA_CONDUCTOR_FLAW=stock1_if_double`, `TA_EAST_FIX=2`). Recommended values for
`bg-developer` to bake, with post-fix numbers, below.

## FIX 1 — The Conductor: **26.5% → 52.1%** (in band, no new dominant character)
**Root cause (restated):** the anchor-in-region re-cost made single-region **2-of-one-region** vendor
costs common → **Stock-Up-2 became the core sourcing move**, so the old flaw "Stock Up **always** takes
1" was crippling (he courted ~7.6 vendors vs ~9.4). Tuning showed the sim **under-values his Travel+2
mobility** (a routing blind spot), so *heavy* flaws over-punish him in-sim: start-2-behind → 37%,
Larder-cap-6 → 41%, even the milder "full only right after a Travel" → 30% (bots double-stock anchored
costs). The lever that lands him **in band without touching the core first Stock Up** is penalising only
**back-to-back** Stock Ups.

**RECOMMENDED FINAL CONDUCTOR (for `characters.csv` + design-doc):**
- **Ability (UNCHANGED):** *Off-Peak Pass* — your **Travel** action arrives with **2** ingredients
  (instead of 1). *(The proud retired railwayman sources as he rides.)*
- **Flaw (REVISED):** *Timetable-bound* — **you can't work the same stall twice in a row: if you took
  the Stock Up action on your previous turn, your Stock Up this turn yields only 1 (instead of 2).**
  *(He can't linger — the timetable moves on.)* A run of Stock Ups yields 2, 1, 1, …; a Travel (or any
  other action) between them resets it to a full 2.
- **Post-fix win-rate:** **52.1%** in the 5-way round-robin (48.7% in the heads-up-vs-field tuning) —
  **in band, mid-pack, did NOT become a new dominant character.** Keeps his travel-first identity and
  actively discourages camping one market.
- **Confidence:** the *direction* (the old flaw was over-harsh) is sim-solid; the *exact* seat is
  slightly sim-pessimistic because his mobility ability is under-valued in-sim, so if anything he may run
  a touch higher at a real table — fine, still in band. Flag alongside the event-coupled chars for the
  FTUE per-character tally.

**Bonus effect — the field de-inflated.** The old 26.5% Conductor was a punching bag every other char
farmed; fixing him pulled the others down toward band **without touching them**:

| Character | before Conductor fix | **after Conductor fix** | note |
|---|---:|---:|---|
| Conductor | 26.5% | **52.1%** | FIXED |
| Influencer | 61.3% | **52.7%** | now **in band** (untouched) |
| Auntie | 58.8% | **55.4%** | edge (untouched; carry to table) |
| Rookie | 63.1% | **56.0%** | edge (untouched; event-coupled → table) |
| Gourmand | 40.4% | **33.8%** | still low (event-coupled → table, per CD) |

So Probe 3 still prints **FAIL** on the strict all-5-in-45–55 rule, **but the residual is now driven
almost entirely by the Gourmand (33.8%) — the event-coupled character the CD is deliberately carrying to
the table** (his pantry-wild ability is invisible to greedy bots; the sim cannot seat him fairly), plus
Rookie/Auntie a hair over 55. Hottest char×mission = gourmand×south_3 60.4% (a weak-char mirror artifact,
not a real synergy). **No sim-confident character remains broken.**

## FIX 2 — Lift East: **15.6% → 17.9%** (≈ the ~18% floor; N/C/S spread held)
A single cross-link re-point was **insufficient** — East under-performs its *demand* not from lack of
demand but because its cheapest cards (the East T1 stalls) are **1 East + 1 pantry**, so bots
**pantry-substitute** the East token away, and East is a **leaf** on the ring (visited less). Level-by-
level (field-average sourcing share):

| East fix | East share | Probe-1 leader (ramp line) |
|---|---:|---:|
| none | 15.9% | ingredient_heavy 59.5% |
| **V12 swap only** | 16.5% | 59.6% |
| **V12 swap + de-pantry 3 East T1s (RECOMMENDED)** | **17.9%** | 59.1% |

Key control read: **the ramp-line dominance (~59%) is invariant across East levels — the East fix does
NOT feed it** (that skew is a separate pre-existing re-cost effect; see remaining issue).

**RECOMMENDED FINAL EAST RE-COST (for `vendors.csv` + design-doc), 4 vendor edits:**
1. **V12 蚵仔煎 (Oyster Omelette), icon S:** `oysters;egg;pantry` → **`oysters;greens;pantry`**
   (egg N → **greens** E). Keeps the South oyster anchor; turns a 6th North-bound cross into an East
   import. **Authentic** — oyster omelette carries 茼蒿 crown-daisy greens. *Floor knock-on:* egg drops
   3→2 vendors (still on 蛋餅/V15 + 卡拉雞腿堡/V16); accept egg@2 or restore a 3rd egg naming elsewhere.
2. **V21 竹筒飯 (Bamboo-Tube Rice), icon E:** `rice;pantry` → **`rice;rice`**.
3. **V22 山蘇/龍鬚菜 (Mountain Greens), icon E:** `greens;pantry` → **`greens;greens`**.
4. **V23 麻糬 (Mochi), icon E:** `rice;pantry` → **`rice;rice`**.
   *(De-pantrying the East T1 stalls to a pure 2-East cost — the lever that actually moves the needle;
   all three are honest single-ingredient dishes, and 2-of-one-region matches the T1 "cost 2 (1 region)"
   spec better than the current 1+pantry.)*
- **Post-fix sourcing share (field avg):** **N 37.2 · C 21.4–22.2 · S 23.5 · E 17.9%** — East clears
  ~18%, North eases from ~38.6 to ~37.2, C/S steady, **camp line still 0%**. South stays the headline
  fix (~24%, up from v3 ~6%).
- **Caveat to flag for bg-developer/consultant:** this leaves East T1s at **2-East** while N/C/S T1s stay
  **1-spec + pantry** — a mild asymmetry (East T1s slightly harder/worse-value). It did **not** hurt
  Probe 1 or the coverage line in sim, but it's a content call. **Lighter fallback = Level 1 (V12 swap
  only):** keeps T1 symmetry but East only reaches ~16.5% (meaningful, just under the floor).

## Post-fix probe matrix (defaults: `stock1_if_double` + East level 2)
| Probe | Verdict | Key numbers |
|---|---|---|
| A — Movement | **SOFT-PASS** | N37.2/C22.2/S23.5/**E17.9**; moves ~7.6/gm; **camp 0%** |
| B — The Poach | **PASS** | situational 47% / griefer 36% win; rational steal-wars 0.08/gm |
| 1 — Track/opening | **SOFT** | ingredient_heavy **~59%** (pre-existing re-cost skew — see below) |
| 2 — Runaway | **PASS** | late interval 2.23 t/court; mid-leader 68–76% (not runaway) |
| 3 — Characters | **Conductor FIXED (52.1%)** | residual FAIL = Gourmand 33.8% (event-coupled → table) |
| 4 — Anti-hoard | **PASS** | stuck 0.000/gm; overflow 0.05/gm |

**Confirmed: neither fix created a new dominant line or character.** The Conductor lands mid-pack; the
East fix is ramp-line-neutral.

## The one remaining sim-visible issue (NOT in this task's scope) + the knob
**Probe 1 mild ramp skew: `ingredient_heavy` sits at ~58–60%** (borderline SOFT/FAIL), **East-level-
invariant and independent of both fixes** — it is a **pre-existing v3.1 knock-on of the anchor-in-region
re-cost** (each region's discount now saves on *that region's own* vendors, so the ramp/ingredient line
is the strongest; balanced/coverage sag to ~43%). **Knob:** cap or soften the discount ramp
(`TA_DISC_CAP`, or reduce the per-icon discount / raise the Buzz floor), or trim the ingredient line's
edge — but **validate at the table first** (does the ramp *feel* like the obvious line, or is 58–60% a
comfortable "slight edge to the engine-builder"?). This is a **separate one-variable pass** to run
**after** the human session weighs in, not something to stack now.

## New encoding simplifications (this fix pass)
- **Conductor flaw** modelled as `n_take=1` when the previous action was Stock Up (`last_kind=="stock"`),
  full 2 otherwise. Faithful to the recommended "back-to-back" rule. His Travel+2 ability is still
  **under-valued by greedy bots** (routing blind spot) → his 52.1% is if anything a floor.
- **East fix** applied as a post-load patch to the real CSV (`TA_EAST_FIX` level 0/1/2) so the CSV itself
  is untouched (bg-developer bakes the recommended values). Level 2 = the recommended package.
- The **East T1 de-pantry asymmetry** (East T1s 2-East vs others 1+pantry) is modelled exactly; its
  human *feel* (are East stalls now slightly unrewarding?) is a table question the sim can't judge.

---

# v6.1 — THE ECONOMY FORK (region-anchored beverages + scoped events) — simulation notes (2026-08-07)

Sim module reworked from the checkpointed v6 first-pass to the LOCKED **v6.1** design
(`../design/design-doc.md`). The spine is unchanged; v6.1 folds in the two CD corrections the sim now
models: **(A)** beverages are **region-anchored** — one persistent stand in *every* region, on-site to
Promote/Bribe (no more region-free "Beverage Row"); the **Beverage deck (7 @2p)** is the hard cap. **(B)**
the **Convenience Store fires events by SCOPE** (⦿ self / ⬢ region / ➤ neighbour), resolved relative to
the flipped region against pawn positions; **Visit** also fires by scope; **Travel** still whiffs.
Auto tournament report: `sim-results.md`. This file is the **interpretation** — nothing here is logged to
the design-doc / bible / decision-log; that's the CD's call after reading this.

> **CORRECTION (2026-08-07, after CD steer).** The CD clarified the design bar: *nobody should win on
> drinks alone — but a clever mix of drinks at the right time + night markets should be a good strategy.*
> That is **not** "drinks-lean ≈ 50%"; it is "**ladder + well-timed drinks beats ignoring drinks.**" My
> first-pass headline ("drinks is a structural trap") measured the wrong bar. The corrected read is below;
> the short version: **the sim confirms the parts it can (pure-drinks correctly loses; no drinks runaway),
> but the CD's actual goal — opportunistic well-timed drinks — is a KNOWN sim blind spot** (greedy one-step
> bots never hit a genuinely dead beat), so it is a **table question**, not a sim verdict.

**Headline (the two make-or-break v6.1 questions):**
- **Riskiest #2 — the drinks fork:** what the sim CAN say **PASSES** — a **pure-drinks tour clearly loses**
  to a good ladder line (~1–10% h2h, the intended ceiling gap) and **drinks are not secretly dominant** (no
  runaway, no solved drinks line). What the sim CANNOT judge — **whether a well-timed drink at the right
  moment makes a ladder line better** — is a **greedy-bot blind spot** (same failure mode as the old Poach
  / Gourmand findings): the bots essentially never bank a drink when playing to win (0.0–0.7/game) because a
  productive ladder dig is *always* available and scores more per action, so they never experience the
  "right time." **→ hand to the 2p Screentop table.** (Detail + the value sweep below.)
- **Riskiest #1 — the Buzz fight (incl. 大哥): the 大哥 dominance probe FLAGS hard**, and the Buzz fight
  itself is **near-absent in bot play** (4.3% of ladder wins contested) — so its *fun/tension* is unresolved
  and is a table question, but 大哥's **tie-win is confirmed too strong** in sim.

Game arc (field, both seatings): winner ~**28.6 VP** (Prestige ~19 · Rep-VP ~5.6 · mission hit 57%) —
squarely in the design's 22–32 target. Turns run **~19–20/player in competent mixed/ladder play** (a touch
over the 14–18 target), mostly ending by last-train; see the pacing finding for the drinks-heavy drag.

---

## What the v6.1 sim covers (and its blind spots) — bots are a FLOOR on depth, not a ceiling
- **Shared "engine brain":** every strategy uses ONE greedy court/source/route planner; strategies differ
  ONLY in **road weights** (w_ladder / w_bev) + a pure-drinks flag. This isolates the fork question exactly
  as `beacon.py` isolates signal policy. A **competence fix** was made this pass (validated below): a
  drinks-leaning bot now sources the common by **Visiting a common region** (3× the CS throughput) and
  **relocates to camp the common supply** rather than blindly remote-CS'ing at ~25% yield.
- **Region-anchored beverages** modelled faithfully: one slot per region, on-site presence required to
  Promote/Bribe, refill from the finite shared deck into the won slot's region, slots go empty when the
  deck dries, dusk does NOT sweep them.
- **Scoped events** modelled by mechanical payload: a HAZARD = a bounded, **tax-not-destroy** tempo tax
  (one fewer sourced ingredient on the target's current Visit or next sourcing — never a held card, never a
  whole turn); a BOON = a free signature windfall to the targets present, or (a fraction) the dynamic **★**
  "vendor gets hot" placement. Buzz-boons/festival-Buzz are folded into the ingredient windfall.
  Scope resolves against real pawn positions, so the **take-that** (a rival standing in a flipped/adjacent
  region) is emergent; a light deliberate **poke** fallback (CS-flip a rival's region when idle) exercises
  it too. Exact tile text + the *warmth* of the rival-facing beats are bg-theme's / the table's job.
- **Buzz war** resolved by a concession heuristic (appetite falls as the rival's committed Buzz rises) →
  deterministic mirrors rarely fight; the fight's depth/feel is a table question, not a sim one.
- **Cannot judge:** whether the Buzz tug-of-war is *fun*, whether the scoped take-that lands as **cheeky
  caper vs spite**, teachability/FTUE, whether the low-travel drinks fantasy *feels* good. Those are the 2p
  Screentop session.

---

## RISKIEST #2 (the v6.1 make-or-break) — re-scoped to the CD's actual bar

**The bar (per the CD):** *nobody wins on drinks alone; but a clever mix — well-timed drinks + night
markets — should be a good strategy.* So the tests that matter are **(i)** does a pure-drinks tour lose to
good ladder play? and **(ii)** does adding well-timed drinks make a ladder line *better than ignoring
drinks*? — NOT "is a drinks-lean ≈ 50%."

**(i) PASSES.** Field (both seatings, naive-excluded h2h): `mixed` ≈ `ladder_lean` ≈ `greedy_prest` at the
top (~50–52% among themselves); **`pure_drinks` ~1–10%** vs every real line; a drinks-*lean* (an
over-commit to drinks) sits ~30% h2h. So a drinks-only tour **correctly loses** to a good ladder tour — the
ceiling gap the design wanted — and there is **no drinks runaway / solved drinks line**. Good.

**(ii) is a SIM BLIND SPOT — hand to the table.** To test the intended "well-timed mix," I added a
`ladder_only` bot (never touches a stand) and a `smart_mix` bot (ladder-primary, but banks an affordable
*local* stand on a beat its ladder plan would otherwise waste on a non-progress dig). Result:

| Matchup (both seatings, mixed field) | winner | drinks banked by the mixer |
|---|---:|---:|
| `mixed` vs `ladder_only` | mixed **53%** | **0.4/game** |
| `ladder_lean` vs `ladder_only` | **50.5%** (coin flip) | **0.0/game** |
| `smart_mix` vs `ladder_only` (value 2) | smart_mix **42%** | 0.6/game |
| `smart_mix` vs `ladder_only` @ **value 4 + Rep 2** | smart_mix **48%** | 0.7/game |

**The bots essentially never bank a drink when playing to win (0.0–0.7/game), even when explicitly told to
look for the moment, even at double beverage value.** Reason: a stand costs **an action + common the ladder
also wants**, and a *productive ladder dig is almost always available*, so a one-step greedy planner never
faces a genuinely dead beat where an easy 2 VP is the best use of the turn. Forcing the drink in (smart_mix)
just **spends tempo the ladder wanted → it loses (42–48%)**. This is the **same structural blind spot the
notes already flag for the Poach ("blind to denial/tempo value") and the Gourmand ("flexibility invisible to
greedy bots")** — the sim cannot model the human "right time" (larder full of the wrong tokens, waiting on a
specific ladder slot, having just lost a Buzz race, repositioning), which is exactly when a human banks a
cheap drink. **So the sim can neither bless nor condemn the intended well-timed mix.**

**What this means for the CD:**
- **Do NOT read "drinks is a trap" off the sim** (my first-pass headline was measuring the wrong bar). The
  correct sim read is narrower: *drinks-as-a-standalone-road correctly loses (as intended), and drinks aren't
  degenerate/dominant.* The value of an **opportunistic** drink is unmeasured, not disproven.
- **The one concrete, sim-visible lever, IF the table finds drinks feel worthless:** the opportunity cost
  (an action + contested common vs a flat 2 VP) is high, so **beverage value 2→3–4 and/or a lower common
  cost** shifts the "is this beat worth a drink?" math at the margin (smart_mix 42% → 48% as value rises
  2→4). But **don't pre-tune off the sim** — it can't see the payoff; the table can.
- **Structural note (still true, now correctly contextualised):** the 7-card deck seeded 4-per-region + 3
  reserve, with refills landing in the won slot's region, means a *low-travel camp* caps at ~4 beverages
  (the other 3 seeded slots need travel). That's **fine** for "drinks are a supplement, not a road" — it
  only becomes a lever to revisit *if* the CD ever wants a heavier drinks lean to be a genuine road (it
  doesn't, per this steer).

**→ The 2p Screentop session is the real test of Riskiest #2.** Instrument: how often a player banks a
drink, at *what moments* (waiting on ingredients / lost a Buzz fight / repositioning / a stand right where
they stand), and whether the drink-banker wins more than a drinks-abstainer. That is the exact decision the
sim's greedy bots cannot make.

**Pacing knock-on (Riskiest #2b) — CONFIRMED, but bounded to drinks-heavy fields.** Beverages-off-the-clock
means a drinks-leaning player doesn't feed the day-clock. In **competent mixed/ladder play the game paces
fine** (~19–20 turns/player, **85–92% end by last-train**, stall 8–15%). But a **drinks-mirror drags badly
(27.9 turns/player, 98% end only via the artificial STALL_CAP)** — the deck backstops never fire
(`end_by_nm_deck 0%`) because nobody works the night-market deck. So the drag risk is real *if* a drinks
lean were viable; since it isn't, a rational player always ladders enough to pace the game. If the drinks
fork is later made viable (above), **the last-train / deck backstops must be re-checked** so a viable drinks
lean can't stall the game.

---

## RISKIEST #1 — the Buzz fight + 大哥 (the carried make-or-break)

**大哥 (the dominance probe) FLAGS.** 大哥 vs neutral, both seatings, at the three H2 options:

| H2 option | 大哥 win% | verdict |
|---|---:|---|
| **A** tie-win (≥0) + the +1-ingredient tab *(the doc's rec)* | **64.0%** | **too strong** |
| **B** tie-win (≥0) + Promote-places-1 | **86.6%** | **much worse** (the weaker Promote can't offset a tie-win; he just needs to *match*) |
| **C** must-lead-by-1 (≥1) + the tab | **30.7%** | over-corrected (too weak) |

The **tie-win threshold (≥0) is the problem**, not the flaw: winning every *matched* vendor is a large,
compounding edge that neither proposed flaw contains (B is a trap — reducing his Buzz output barely matters
when he only needs to tie). C shows the ≥1 threshold over-nerfs him. **Neither A nor B nor C lands in
band → 大哥 needs a *middle* setting the current three options don't offer:** e.g. **≥1 threshold + a
*lighter* flaw** (drop the tab), or **≥0 but with a genuinely heavy brake** (e.g. +1 ingredient *and* he
can't win contested vendors). Recommend the CD treat H2 as **unresolved** and sim a 4th option; do NOT ship
A. This is exactly Riskiest #1b as flagged.

**Two other characters out of band** (char vs neutral, mixed road, both seatings; target 45–55%):

| Character | win% | read |
|---|---:|---|
| 里長伯 councillor | 48.5% | ✓ |
| 媽寶 office | **30.4%** | **too weak** — "keep only 1 on a Visit" is brutal now that the Visit is the ingredient workhorse; her "draw the region you left on Travel" ability doesn't compensate |
| 網紅 influencer | **60.4%** | **too strong** — +1 Buzz on Promote over-performs (as the design flagged "load-bearing"); the go-last/start-behind flaw under-counts in sim |
| 大胃王 dagushi | 50.6% | ✓ |
| 大哥 dage | **64.0%** | out (see H2) |

**大胃王's flaw (H1) is a non-issue** — all three options sit in band (A hazards-twice 50.6% / B keep-2
50.6% / C next-fires 51.9%). **Ship A** (simplest) as the doc recommends; it does not over-brake here.

**The Buzz fight is near-absent in bot play** — only **4.3% of ladder wins are contested** and
`max_buzz_on_vendor ~3.9`, `buzz_supply_min ~16` (the ~24 supply never gets tight). The concession
heuristic + asymmetric road targeting mean bots rarely pile onto the *same* vendor. So the sim **cannot
answer "is the tug-of-war fun/tense"** — that is squarely the 2p Screentop question. What the sim *can* say:
there is **no snipe-degenerate or supply-crunch failure**, and 大哥's tie-win is the one broken knob.

---

## RISKIEST #3 — the dig, movement spread, and the new interaction

- **Movement spread SKEWS to the common-bearing regions.** Field sourcing shares: **N 15.5% · C 24.6% ·
  S 27.0% · E 9.2%** (+ common 23.7%). Concentrating the common in C&S (H3=half) pulls sourcing there;
  **East is starved at 9.2%** (well under the ~18% floor) and North is light. A carry-over of the old v3.1
  "East light" issue, now driven by the *common's* placement rather than East recipe costs. **Knob:** the
  common's spread (put one of the two common regions in the E/N half of the ring), or lift East demand on
  night-market recipes — a data tuning for bg-developer, not a rules change.
- **The v6.1 interaction injection is REAL but LIGHT in sim.** ~**2.4 take-that hazard hits/game** land on a
  non-actor (mostly Visit region/neighbour scope catching a co-located/adjacent rival); only **~0.46 via the
  Convenience Store** + **~0.19 deliberate pokes/game**. So the "near-zero interaction" an early read flagged
  is now non-zero, but the **CS-as-weapon is rare** — bots are sourcing-driven and rarely flip a rival's
  region on purpose, and a rival is seldom standing in the common region a drinks player flips. Read this as
  a **floor** (the sim under-models deliberate poking); whether the aim-it-at-a-rival lever is *used and
  fun* is a table question.
- **Realized scope ratio skews REGION-heavy: ~29% self / 51% region / 20% neighbour** (vs the proposed
  40/40/20). The per-kind skew (hazards→region/neigh, boons→self) plus forcing ★-boons to region scope
  over-weights region and under-floors self. If the CD wants the proposed Self floor (so the CS isn't
  mostly a region weapon), **soften the hazard region-skew** — but note it barely affects balance (H4 flat),
  so this is a *feel/identity* tune, not a balance one.
- **The 5-ingredient dig did not flatten** — events fire ~13/game, Visits (11.3) > CS (8.1) > Travels (9.2)
  are all well-used, `forced_turn_frac 0.000` (never a dead turn), `avg_legal_actions ~9.8`. The push-your-
  luck tension survives the smaller palette. The dynamic **★** fires ~1.9/game, winner grabs ~0.84 — a
  modest, non-decisive swing.

---

## Health read (field round-robin)
The ladder-capable lines (`mixed` / `ladder_lean` / `ladder_only` / `greedy_prest` / `smart_mix`) pack
within ~1–3pt head-to-head — no crushing dominant single line. Every real line crushes `random`. As
designed, **the ladder is the game and a drinks-only tour loses** (`pure_drinks` a near-pure loss vs
anything real; `drinks_lean`, an over-commit, ~30% h2h). What the field does NOT resolve — because the
greedy bots won't bank an opportunistic drink (see Riskiest #2) — is whether *well-timed* drinks beat
ignoring drinks. `mixed`/`smart_mix` ≈ `ladder_only` here **only because the bots barely use drinks**, not
because well-timed drinks are proven worthless. Seat effects mild, not flagged.

---

## The ONE thing to test next (this pass)
**Riskiest #2 goes to the 2p Screentop table, not to a knob.** The sim has done its job on the extremes
(pure-drinks correctly loses; drinks aren't dominant; no runaway) and confirmed the parts it can. The CD's
actual goal — *well-timed drinks as a good tactical supplement* — is a **greedy-bot blind spot** (0.0–0.7
drinks banked/game even when instructed; a productive ladder dig is always the better per-action play), the
same limitation the notes flag for the Poach and Gourmand. **Instrument the session** for: drink-bank
frequency, the *moment* each drink is taken (waiting on ingredients / lost a Buzz fight / repositioning), and
whether a drink-user out-scores a drink-abstainer. **Carry as a cheap, sim-visible lever only if the table
finds drinks feel worthless:** beverage value 2→3–4 / a lower common cost (smart_mix 42%→48% as value 2→4).
Do not pre-tune off the sim. **Separately (sim-confident):** treat **H2 (大哥) as unresolved** — none of
A/B/C is in band; sim a 4th option (≥1 threshold + a lighter flaw, or ≥0 + a real brake). Nudge **網紅 down**
/ **媽寶 up**; **ship 大胃王 = H1-A**; fix **East** via the common's spread. The Buzz fight's *fun* and the
scoped take-that's *warmth* are table questions.

---

**Knobs exposed for re-sim:** `TA_BEV_VALUE` / `TA_BEV_REP` (beverage value — a marginal lever on the
opportunistic mix, 42%→48% as value 2→4; NOT a road-viability fix),
`TA_H3` (common availability half/every/half_rich), `TA_SCOPE_SELF|REGION|NEIGH` (H4 scope ratio),
`TA_H2_THRESH` / `TA_H2_FLAW` (大哥), `TA_H1` (大胃王), `TA_HAZARD` (event hazard frac), `TA_STARBOON`
(★-boon frac), `TA_BUZZ_SUPPLY` / `TA_BUZZ_MARGIN`, `TA_DUSK` / `TA_LASTTRAIN` (clock marks),
`TA_STALL_CAP` (the drinks-drag backstop), `TA_POKE` (the deliberate CS poke). **No structural
harvest-fix knob exists yet — that's the design call to make, then encode.**

## Encoding simplifications (v6.1 — the sim's blind spots)
1. **Beverages baked (10 templates, sliced to a 7/9/10 deck by count)** at region granularity; the
   region-anchored slot mechanics (seed 4 + reserve, refill-into-won-region, empty-and-stay-empty) are
   faithful. These cap a low-travel drinks *camp* at ~4 wins — fine given the CD's "drinks are a supplement,
   not a road" steer; a lever to revisit only if a heavier drinks lean should ever be a genuine road.
2. **Event payloads abstracted** to tempo-tax (hazard) / free-ingredient or ★ (boon); Buzz/festival boons
   folded into the ingredient windfall. The *warmth* of rival-facing beats is unmodelled (bg-theme/table).
3. **The Buzz war is concession-resolved** → contested-win rate (4.3%) is a floor; the fight's fun/tension
   is unmeasurable in sim by construction.
4. **The deliberate CS "poke"** fires only as an idle fallback (larder full / no target) → poke frequency
   (0.19/game) and CS-rival-hits (0.46/game) are floors; a human weaponises the blind flip more.
5. **STALL_CAP (26 turns/player)** is an artificial backstop to surface the drinks-drag pacing risk
   (`end_by_stall`); it is NOT a game rule — the real end-triggers are the last-train mark + deck exhaustion.
6. Component CSVs (`../components/*.csv`) are still on the pre-v6 data model; the sim bakes its own
   representative v6.1 vendor/event set (as prior passes did). The CSV rebuild is bg-developer's separate,
   still-gated data task — out of scope for this sim rework.
7. **The `ladder_only` (never-drinks) and `smart_mix` (ladder + opportunistic local-stand) bots** exist to
   test the CD's "well-timed mix" bar. `smart_mix` only banks a drink when its ladder plan would otherwise
   be a non-progress dig AND a local stand is already affordable. It still fires rarely (0.6/game) and loses
   to `ladder_only` (42–48%) — the greedy planner has almost no genuinely dead beats, so this UNDER-models
   the human "right time." Read (ii) in Riskiest #2 as *unmeasured by the sim*, not *disproven*.

---

## TOUR TICKETS — a proposed fix, GATED RUN COMPLETE (2026-08-07, CD-directed & CD-signed-off)

**The proposal (CD-locked shape).** Replace the single hidden +7 mission with **Ticket-to-Ride-style Tour
Tickets**: hold several; **claim a new one as a full action** (Book; doesn't tick the day-clock); score
**+value on completion, −floor(value/2) if unfinished**. The deck **leans on MIX tickets** (drinks +
ladder: "a stand + a night-market", "a stand in 3 regions", "one of each venue") so a *well-timed drink
pays toward a bonus the greedy planner can SEE* — the exact incentive the flat-2-VP drink lacked. Encoded
behind `TA_MISSION_MODE` (`tickets` = proposal; `single` = the committed v6.1 baseline, for a clean A/B).
New bot `ladder_only` (never drinks) is the "ignore drinks" control.

**Headline: Tour Tickets turn the drinks fork from a ~20% trap into a BALANCED, in-band alternative, and
make a mix a legitimately competitive line — while pure-drinks still correctly loses.** The intended
effect landed.

**Authoritative numbers — the caps-aware `_versus`/H5 probes (n=1200; each side's ticket dealing aligned
to its real road/capability):**

| Matchup (both seatings) | single | tickets | read |
|---|---:|---:|---|
| `drinks_lean` vs `ladder_lean` (the fork balance) | 45.3% | **49.2%** | tickets add ~4pt → **in-band both sides** (was a ~20% trap pre-competence-fix) |
| `mixed` vs `ladder_only` (mix vs pure-ladder expert) | 50.4% | **51.0%** | a mix is **not worse** than pure ladder; ~coin-flip |
| `drinks_lean` vs `ladder_only` | 37.1% | 36.8% | leaning drinks still **loses to a pure-ladder expert** (correct: don't punish clean laddering) |
| `pure_drinks` (field) | — | **~25%** | still a **clear loss** — nobody wins on drinks alone ✓ |

So the two make-or-break bars for Riskiest #2 now PASS: **(i)** pure-drinks clearly loses; **(ii)** the
drinks *lean* is viable and in-band (≈49/51 vs the ladder lean), no longer a trap. A mix is competitive
with pure ladder rather than strictly dominant — arguably correct (a clean ladder line shouldn't be
punished either). **Why it works:** a ticket payoff is greedy-visible where flat drink-value was not, so a
held mix/drinks ticket makes the bot (and a human) actually pursue a well-timed drink.

**⚠ Methodology caveat — the auto round-robin (`sim-results.md`) is caps-BLIND, do NOT read its field
ordering as truth.** `simulate.py` calls `new_state(rng)` generically, so it can't pass per-strategy caps;
`ladder_only`/`pure_drinks` there get *dealt drinks-requiring tickets they will never complete* and eat the
−half penalties, which **inflates the drinks-inclusive lines** (the RR shows `drinks_lean` 59% > `ladder_only`
56%, an artifact — the fair `_versus` head-to-head is `drinks_lean` **37%** vs `ladder_only`). Trust the
`_versus`/H5 table above; the RR is a rough field-shape check only. (Fix if ever needed: thread caps through
the round-robin harness, or drop the two pure controls from the RR.)

**Character balance under tickets (mildly better, same conclusions):** councillor 49.3 ✓ · 大胃王 52.1 ✓ ·
網紅 55.4 (borderline, was 60.4) · 大哥 **58.9 (still hot, was 64.0)** · 媽寶 **30.0 (still weak)**. Tickets
add a shared scoring vector that slightly dilutes ability edges, but **H2 (大哥) is still unresolved** (A
58.9 / B 84.6 / C 30.4 — none in band; needs a 4th option) and 媽寶 still needs a buff. H1 (大胃王) all ~52%,
ship A.

**Costs & watch-points (honest):**
- **Weight.** Tickets are a real subsystem add (claim action + penalty rule + multi-objective tracking) —
  teachable, but pushes toward the top of the 2.5 budget. `bg-elegance` must weigh it before lock.
- **The ticket swing is modest** in bot hands: winner nets only **~+2.7** from tickets (holds ~2.1, completes
  ~1.0, eats a −half penalty on the unfinished one). The penalty bites — which is the intended TtR tension.
- **Under-modelled upside.** The "stack a ladder ticket + a cheap drinks ticket and finish BOTH" juggling is
  a multi-objective planning layer the greedy bot executes poorly (completes ~1 of 2 held), so the sim likely
  **under-estimates** the system's value for a thinking player — a point *for* the design, to confirm at the table.
- **Pre-existing v6.1 items unchanged by tickets:** East under-sourced (S 35% / E 9%), the Buzz fight rare in
  bot play (~5% contested → table question), and the drinks-heavy pacing drag.

**Recommendation:** Tour Tickets are a **keeper** — they fix the fork's viability (the session's #1 problem)
in the exact way the CD intended, cheaply and thematically. Next: **(1)** `bg-elegance` weight check +
`bg-theme` to lore the tickets as a travel agent's *itinerary/booked stops*; **(2)** if the CD wants the mix
to more clearly *beat* pure ladder (not just match it), add the complementary **cheaper-drink** lever (lower
common cost or a lighter claim on the low-conflict stands); **(3)** the real proof is the **2p Screentop
table** — the multi-objective juggling and the "book another? / can I finish it?" press-your-luck are exactly
what the sim can't fully judge. Only lock into the design-doc/bible on the CD's word — Tour Tickets remain a
*proposal* until then.

---

# v6.2 — REGION VENDOR MARKETS + A MISSION CLOCK — simulation notes (2026-08-07)

Sim module reworked from the v6.1 economy fork to the **v6.2 proposal** (`../design/v6.2-content-draft.md`).
The board is now **four region vendor markets** (per-region day/night decks, 2/1/1/1 face-up, refill-in-
place, **drinks are the low-value cards in each deck**), the day turns over at a single **DUSK FLIP** (both
day vendor decks AND day ingredient pools cleared island-wide → night decks, event-heavier; **Larder
kept**), the day is paced by a **MISSION CLOCK** (with an all-vendor-claims clock behind a knob for the
A/B), sourcing runs on a **conserved per-region token pool with renewable over-cap discard** (the
anti-lockout rule), and **Tour Tickets** are a **shared face-up row of 3**, claimed as an action, scored
retroactively (+value / −floor(v/2)). **Nothing here is logged to the bible/decision-log as LOCKED — the
CD picks from the A/B/C forks below; this is the interpretation.** Authoritative n = **1000 games/cell**.

**Headline: v6.2 is a strong pass.** All five playstyles are live and none dominates; a well-timed mix
crushes the ignore-both control while pure-drinks is dead; **East is no longer starved (18% sourcing, up
from v6.1's 9%)** — the cross-region cycle works; **hoarding is a confirmed trap, not a lockout**; and the
two open character calls **resolve** (H2 大哥 has an in-band 4th option; 媽寶's buff lands). The residuals
are all familiar sim blind-spots (the Buzz-fight's *fun*, the disruptor's *teeth*, 網紅's under-counted
go-last flaw) plus one new data flag (**Central is now the under-pulled region** — tea has no export
demand) and a pacing caveat (the region markets deliberately add travel, so bot games run **~25 turns/
player**, over the design's 14–18 estimate).

> **Methodology note.** All win-rates below come from the **caps-aware** `_versus` / `_char_winrate`
> probes in `__main__` — each side's prefs/capability (no-drinks, no-tickets, hoard region, character kit)
> is wired into `new_state`. The auto round-robin in `simulate.py` (`sim-results.md`) is **caps-BLIND** (it
> calls `new_state(rng)` generically and would mis-deal drink/ticket-requiring tickets to the pure
> controls, inflating them — the same artifact flagged for v6.1); it was **not** used as a source of truth
> this pass. Trust the probe suite.

## What the v6.2 sim covers (and its blind spots) — bots are a FLOOR on depth
- **Shared engine brain:** one greedy value/action planner; strategies differ ONLY in prefs
  (value/ticket/ramp/speed weights + disrupt/opportunistic/hoard flags + drink/ticket controls).
- **Region markets, the dusk flip, and the conserved ingredient pool** are modelled faithfully (per-region
  day/night decks, 2/1/1/1 face-up + refill, the island-wide dusk sweep of both layers with the Larder
  kept, event-heavier night draws, and a conserved token pool whose over-cap discard folds back in when
  the region runs dry — so denial is temporary and self-taxing).
- **Blind spots (hand to the table):** the Buzz tug-of-war's *fun/tension* (concession heuristic → bots
  rarely pile on the same vendor, ~5% contested — a floor); the disruptor's scoped-CS *warmth/teeth* (bots
  poke rarely and blindly); 網紅's **goes-last** flaw (seat effects are mild for greedy bots); whether the
  dusk flip *feels* like a turnover; teachability/FTUE. And the −½ penalty's real job — disciplining a
  human's *speculative* over-claim — is invisible to a bot that only claims finishable tickets.

## Game arc (balanced mirror, mission clock)
~**25.7 turns/player**, **5.1 vendors/player**, winner ~**34.2 VP** (Prestige ~16.3 · Rep-VP ~5.2 ·
**Tickets ~12.7**). Dusk ~turn 34, last-train ~turn 48. `forced_turn_frac 0.000` (never a dead turn),
`avg_legal ~9.6`, `empty_draws ~0.10/game`. **Note the ticket share (~37% of the winner's score)** — Tour
Tickets are load-bearing for scoring (a point for `bg-elegance`/the table: the spine is doing a lot of the
scoring work; that's by design, but watch it doesn't eclipse the vendor engine's *felt* payoff).

---

## PROBE 1 — the five playstyles → **PASS (all five live, none dominant)**
Avg win% vs the field, both seatings, all crush `random` (100%):

| Playstyle | avg vs field | read |
|---|---:|---|
| balanced | **53.0%** | generalist, mild top edge (<55) |
| mix (well-timed drinks + tickets) | **52.3%** | live |
| opportunistic (★/premium/high-value tickets) | **50.7%** | live |
| endgame (rush completions) | **50.5%** | live |
| disruptive (scoped CS at a rival) | **46.7%** | live but the weakest lane (see Probe 9) |
| *no_drinks (ignore drinks control)* | *43.1%* | ignoring drinks is a real handicap |

Band **43–53%**, no line >~53% (no Condorcet crusher), every real line crushes naive. **The design's
"several viable ways, none >~55%, some rock-paper-scissors" bar is met.**

## PROBE 2 — is a well-timed MIX good? → **PASS**
| Matchup | win% | verdict |
|---|---:|---|
| `mix` vs `ignore_obj` (ignore objectives AND drinks) | **73.4%** | a mix crushes ignoring both ✓ |
| `balanced` vs `ignore_obj` | 74.1% | objectives+drinks clearly matter |
| `pure_drinks` vs `balanced` | **0.5%** | nobody wins on drinks alone ✓ |
| `pure_drinks` vs `no_drinks` | 0.3% | " |
**Tour Tickets + drinks-as-low-value-vendors deliver the CD's bar:** a mix is strongly positive, pure
drinks is dead. (The mix's edge is amplified because tickets are ~37% of score — see the arc note.)

## PROBE 3 — Buzz-fight frequency → **LOW (~5%), a table question — NOT hard-flagged**
`contested-win frac 5.4%`, `max_buzz_on_vendor ~5.5`. Spreading vendors across region markets did **not**
make the fight rarer than v6.1 (~4.3%) — it's about the same. It is **not near-zero** (no hard flag), but
bots rarely collide by construction (concession heuristic + asymmetric targeting), so the *fun/tension* of
the headline mechanic remains **unmeasurable in sim → the #1 table question** (unchanged from v6.1).

## PROBE 4 — travel spread → **PASS on East; NEW flag on Central**
Field sourcing / claim share (balanced mirror):

| Region | SRC share | CLAIM share | read |
|---|---:|---:|---|
| North | 24% | 36% | dense capital (2 slots), as designed |
| Central | **13%** | **15%** | ⚠ **the new under-pulled region** (see below) |
| South | 27% | 32% | the busy cross-hub (everyone imports seafood) |
| East | **18%** | 17% | ✓ **the headline fix — was 9% in v6.1** |
**East is no longer starved (18% sourcing, at the ~18% floor)** — the cross-region cycle (S's 棺材板 pulls
rice out) + the P8 apex + coverage tickets drag traffic east, exactly as the value spread intended.
`inter_moves ~8.7/game` (real routing, not camping). **NEW flag — Central is now the under-pulled region
(13% src):** the cycle makes C a pure *importer* (逢甲 needs S), so **tea (C's signature) has no external
demand** and nobody travels to *source* it. This is the v6.2 analog of v3.1's "East starved." **Fix (a
data tweak for `bg-developer`, not a rules change):** give tea one export — e.g. re-point one cross-region
cost to need **C** (make an East or North night dish need a tea/tisane note), so the cycle becomes a true
loop through all four. Minor; a watch, not a blocker (Central still sees play via K + its own vendors).

## PROBE 5 — CLOCK A/B → **recommend the VENDOR-CLAIMS clock**
| Clock | turns/player (sd) | vendors/pl | dusk turn | end: LT / stall |
|---|---:|---:|---:|---:|
| mission | 25.7 (**4.9**) | 5.1 | **33.8** (late) | 74% / **26%** |
| vendor-claims | 25.2 (**3.9**) | 5.0 | **21.3** (mid) | 86% / **14%** |
The **vendor clock is tighter and more reliable**: lower length variance (sd 3.9 vs 4.9), a **crisp
mid-game dusk** (turn 21 vs 34), **half the stall rate** (14% vs 26%), and it reaches the real last-train
trigger far more often. The **mission clock's dusk comes late** because completing 3 missions *lags* vendor
wins — so Act I runs long and Act II is a short tail (a lopsided arc). **Recommend the vendor-claims clock**
(dusk 5 / last-train 10 @2p). *Caveat:* **both** clocks run **~25 turns/player** — over the design's 14–18
estimate — because the region markets + cross-region cycle deliberately add travel (v6.1's central ladder
was ~20). Greedy bots also over-travel/over-promote, so a human table will be tighter; if it drags, lower
the marks (fewer claims to end). ~25 bot-turns/player ≈ **~30–40 min**; humans likely land nearer the
25–30 target.

## PROBE 6 — the −½ penalty A/B → **no behavioural difference in sim (lean: safe to cut, with a caveat)**
| Penalty | mix vs ignore_obj | claims/gm | tickets done/held (winner) | winner VP |
|---|---:|---:|---:|---:|
| −floor(v/2) | 73.4% | 6.7 | 3.0 / 3.5 | 34.2 |
| score-0 | 82.7% | 6.7 | 2.9 / 3.5 | 35.1 |
**Bots claim and complete identically with or without the penalty** — it changes only the *score* (it
compresses the gap to the control and shaves ~1 VP). So by the brief's bar ("if behaviour doesn't differ,
recommend cutting it"), the sim **supports the `bg-elegance` cut**. **BUT** the caveat is load-bearing: the
penalty's design job is to discipline **speculative** claiming, which the greedy bot never does (it only
claims finishable tickets), so **the sim can't see what the penalty is for.** This is a genuine A/B/C for
the CD (below).

## PROBE 7 — the dusk flip + hotter night → **paces cleanly; night-sprint is a feel call**
No dead reset beat: `forced_turn_frac 0.000` across the flip, no stall spike at dusk, and the night
ingredient decks are event-heavier (modelled `NIGHT_EVENT_FRAC 0.42` vs day 0.25). The **night-half-sprint**
question interacts with the clock: the **mission clock already front-loads Act I** (dusk late → a naturally
short night), while the **vendor clock gives a balanced two-act arc** (dusk mid-game). So if you take the
vendor clock and *want* a sharper night, a small night sprint (fewer claims to last-train after dusk) is
the lever — but whether the night should *feel* like a sprint is a table question, not a sim verdict. The
"event-heavier = hectic-fun not swingy-punishing" judgement is squarely the table's (payloads are
abstracted).

## PROBE 8 — character balance → **H2 & 媽寶 RESOLVED; 網紅 borderline (watch); ship 大胃王 A**
Char vs neutral, both seatings, target 45–55%:

| Character | win% | verdict |
|---|---:|---|
| 里長伯 councillor | 51.8% | ✓ |
| 媽寶 office (with keep-2) | **45.6%** | ✓ **fixed** (was 29.4% at keep-1) |
| 大胃王 dagushi (H1-A) | 52.6% | ✓ **ship A** |
| 網紅 influencer | 60.5% avg → **55.0% goes-last** | ⚠ borderline (see below) |
| 大哥 dage | see H2 | resolved via option D |

**H2 (大哥) — RESOLVED. Recommend option D.**
| Option | win% | |
|---|---:|---|
| A tie-win + tab *(doc rec)* | 62.7% | too strong |
| B tie-win + Promote-1 | 91.4% | far worse |
| C lead-by-1 + tab | 26.9% | over-nerfed |
| **D lead-by-1 + NO flaw** | **51.7%** | ✓ **in band** |
| E tie-win + can't-win-contested + tab | 57.4% | in band-ish, hotter |
The **tie-win threshold was the whole problem** (winning every *matched* vendor compounds). Option **D**
drops the tie-win to a **lead-by-1** (still an edge — everyone else needs +2 — and needs no flaw), landing
**51.7%**. Cleanest to teach ("大哥 only needs a *slim* edge, not a decisive one"). E keeps the tie-win but
bars contested wins — thematic but hotter (57.4%) and adds a rule.

**媽寶 (office) — FIXED by keep-2.** none/keep-1 **29.4%** → keep-2 **45.6%** → travel2 34.3%. The keep-1
flaw was simply crippling now that the Visit is the ingredient workhorse. keep-2 removes it and lands her
in band. *Design shape note:* keep-2 leaves her ability-only (Travel draws the region you left, no flaw);
if you want to preserve an ability+flaw silhouette, give her a **light thematic flaw that doesn't touch the
Visit** (a table/design call, not sim-load-bearing).

**大胃王 (dagushi) — ship H1-A.** All three flaws ~in band (A 52.6 / B 52.6 / C 53.5); A (hazards-twice) is
simplest.

**網紅 (influencer) — borderline, carry with a watch-flag (unchanged from v6.1).** The +1-Buzz-on-Promote
ability is genuinely strong (Buzz is the binding late constraint). The head-start flaw is **inert** (a flat
common head-start moves nothing: 60% at behind 1/2/3 — K is low-value). Modelled **honestly as "goes last"
(fixed second seat)** he lands **55.0%** — top of the band, just in. **The sim under-counts a go-last
disadvantage** (a greedy bot doesn't feel reacting-last the way a human does), the exact limitation the
v6.1 notes flagged. **Keep "Going Viral + goes last + starts behind"; carry to the table** with the cheap
trims in reserve if he's still hot: +1 Buzz only on your **first** Promote each turn, or a small bribe tab.

**Day/night kit lean (design open-Q10):** every kit reaches the band **without any day/night tweak**, so
**no kit *needs* an explicit day/night ability** for balance — which is the answer to "add one only where
needed": none needed. The full **two-mode day/night flip stays an expansion** (as reserved), not a base
requirement.

## PROBE 9 — disruptive viability → **a real but the WEAKEST lane; not a trap, not oppressive**
`disruptive` sits at **46.7%** avg vs field — clearly viable (crushes naive, in the band), but the softest
of the five. The scoped-CS take-that is **light in bot hands** (bots poke rarely and blindly — a known
floor), and the contest tickets (搶手貨 / 人氣王) give the lever a scoring home so it isn't just a spoiler.
**Read: leaning disruptive is a legitimate lane, neither a trap nor oppressive — but at current teeth it's
the marginal playstyle.** If the table finds it toothless, the lever with the least feel-bad is *more
contest-reward* (a slightly higher-value contest ticket, or a small Rep/Buzz kickback for winning a
contested vendor), NOT nastier CS events (which risk the take-that warmth). This is a table question.

## PROBE 10 — hoarder / ingredient-denial → **CONFIRMED a trap, not a lockout**
| Hoarder | win% vs balanced | empty_draws/gm (denial) |
|---|---:|---:|
| baseline (no hoarder) | — | 0.10 |
| hoard **East** (rice) | **8.6%** | 0.27 (2.7×) |
| hoard **South** (seafood) | **15.8%** | 0.61 (6×) |
A hoarder **loses decisively** (renewable discard + Larder cap + the dusk reset make it self-taxing), yet it
**does buy real *temporary* denial** — a rival's Visits find the region dry 3–6× more often. Denying
**South** bites harder (seafood is imported by S's own vendors + N's 牛肉麵 + C's 逢甲) but still loses at
15.8%. **The per-region signature supply size (SIM `SIG_SUPPLY=10`) keeps denial *spice*, not a
stranglehold** — the exact tuning the brief asked for. Denial is a flavour of the disruptive lane, correctly
non-degenerate.

## PROBE 11 — MP light seat-balance smoke → **no catastrophic seat; mild last-seat tax (deferred)**
| Count | seats | note |
|---|---|---|
| 2p | seat0 54% / seat1 43% (tie 3%) | mild first-player edge, within tolerance |
| 3p | 36 / 35 / **23** (tie 7%) | last seat ~10pt light — a watch |
| 4p | 29 / **19** / 24 / 24 (tie 5%) | seat1 light — a watch |
**No seat is broken and none trips the harness "suspect" flag.** There is a **mild last/late-seat
disadvantage at 3–4p** — flagged for the **deferred dedicated MP pass** (`bg-architect` + `bg-critic`), not
tuned here (the brief scoped MP to a catastrophic-only smoke; 2p is the design home). No kingmaking test was
run (deferred with the MP pass).

## PROBE 12 — pacing / anti-runaway → **no runaway**
The tight playstyle band (Probe 1, all 43–53%) and **`endgame` at 50.5%** (the rush line does not run away)
are the anti-runaway signal: no line snowballs, the end-game-driver can't slam the door while ahead, and
`forced_turn_frac 0.000` means a trailing player always has live actions. The vendor clock's crisp,
low-variance length (sd 3.9) is the cleaner pacing spine.

## PROBE 13 — FAQ ambiguities (NOTE, not simmed)
- **A region's deck runs out:** face-up slots simply aren't refilled (fewer courtable vendors there) until
  dusk swaps in the night deck; the day/night backstops end the phase if *all* decks dry island-wide.
  Rulebook: "if a region's deck is empty, its face-up slot(s) stay as they are — refill only when able."
- **A simultaneous clock trip** (one claim triggers dusk *and* the last train, or the last day vendor won
  at dusk): resolve **dusk first, then** the end check. Rulebook needs an explicit order-of-operations line.
- **Claiming an already-satisfied ticket:** allow it, but it's a *wasted* action (it scores retroactively
  either way) — OR simplest rule: **you may only claim a ticket you have not yet completed.** Recommend the
  latter (prevents a confusing free-points-for-an-action edge case).

---

## The decision forks for the CD (A/B/C)
1. **The clock → recommend the VENDOR-CLAIMS clock** (dusk 5 / last-train 10 @2p): tighter, lower variance,
   crisp mid-game dusk, half the stalls. (Alt: mission clock — thematic but a lopsided, late-dusk arc.)
2. **The −½ penalty → CD's call, genuinely.** Sim shows no behavioural difference (supports the elegance
   cut), but it can't see the human speculation the penalty disciplines. Lean: **keep it (it's the
   press-your-luck tension), and let the table decide** whether claims feel agonised-over.
3. **大哥 → recommend option D** (lead-by-1, no flaw; 51.7%).
4. **媽寶 → keep-2** (45.6%), optionally add a light non-Visit flaw for silhouette.
5. **網紅 → keep Going-Viral + goes-last** (55.0% honest); carry with a cheap-trim watch-flag.
6. **Central under-pull → a small data tweak** (give tea one export in the cross-region cycle) — for the
   `bg-developer` v6.2 rebuild, not a rules change.

## Encoding simplifications (v6.2 — the sim's blind spots)
1. **Vendors baked** from the content draft (24 vendors, day/night per region, ★ + cross + drinks marked);
   the CSVs are stale pre-v6 and were NOT used — the v6.2 data rebuild is `bg-developer`'s gated job.
2. **Ingredient pool** is conserved per region PER PHASE (over-cap discard folds back; spent-on-vendor
   tokens are consumed; dusk resets to a fresh night pool). Faithful to the renewable-discard rule; the
   hoarder probe reads it correctly.
3. **Event payloads abstracted** to tempo-tax (hazard) / free-ingredient or ★ (boon). Warmth/feel unmodelled.
4. **Buzz war concession-resolved** → the 5.4% contested rate is a floor; the fight's fun is unmeasurable.
5. **Tickets** claimed from a shared row by a keep-fit heuristic; the multi-objective "juggle two and finish
   both" is executed poorly by the greedy bot, so the sim likely **under-values** tickets for a thinking
   player (a point *for* the design).
6. **網紅's goes-last flaw** is under-counted (mild seat effects for greedy bots) → his 55.0% is if anything
   a ceiling; a human table feels the flaw more.
7. **STALL_CAP (30 turns/player)** is an artificial backstop to surface pacing risk, not a game rule.

**Knobs:** `TA_CLOCK` (mission|vendor), `TA_M_DUSK/M_END`, `TA_V_DUSK/V_END`, `TA_PENALTY` (half|zero),
`TA_H2_THRESH/H2_FLAW` (大哥), `TA_H1` (大胃王), `TA_OFFICE` (媽寶), `TA_INFL_BEHIND` (網紅), `TA_SIG_SUPPLY`
(the hoarder/denial supply knob), `TA_K_SUPPLY`, `TA_DAY_EVENT/NIGHT_EVENT` (dusk-flip event density),
`TA_NIGHT_SPRINT`, `TA_HAZARD`, `TA_STARBOON`, `TA_SCOPE_*`, `TA_BUZZ_SUPPLY/MARGIN`, `TA_STALL_CAP`.

---

# v6.3-FIX — killing the `ignore_obj` dominance (tickets-only vs raise-values) (2026-08-07)

The first v6.3 re-sim (`sim-results.md`) validated the Reach economy but the **shape did not pass**: a
naive line `ignore_obj` won **77–81%**, crushing every real line ~73% h2h. This pass diagnoses that and
tests fixes. **One variable at a time; Reach rules held fixed; character kits held locked (drift noted,
not tuned).** New sim knobs added and parameterised: `TA_SCORING` (both|tickets_only), `TA_TICKETS`
(base|expanded), `TA_TVAL` (ticket-value multiplier), `TA_BOOK_W` (planner Bookings weight under
tickets_only), `TA_MS_MODE` (first|perplayer|consolation), `TA_MS_ON` (bookings|tickets), `TA_SLOTS`
(face-up scarcity lever). Module defaults still run the **v6.3 shape-lock** (both/base/first); the
recommended fix is a three-flag change (documented in the module header).

## 1) ROOT CAUSE of the `ignore_obj` dominance — the ticket subsystem is net-negative EV

`ignore_obj` = `{no_tickets, no_drinks}`: it never claims a Tour Ticket and never courts a drink — it
just grinds the highest-**Bookings** food vendors. Diagnosis (matchup `ignore_obj:balanced`, n=1200):
the winner averages **26.5 Bookings but only 3.4 ticket-score** — the winning line is the pure-Bookings
grinder. **This IS the "memorizable one-liner" the health read warned about**: *"ignore the whole ticket
minigame."* Why it's optimal under the v6.3 "both" scoring (Bookings + Tickets):

- Claiming a ticket carries an **opportunity cost** (you steer claims toward a pattern instead of the
  fattest vendor) **and a downside risk** (a `−floor(v/2)` lose-pile ding if you don't finish it by the
  phase judging). Grinding Bookings has **neither** — it's pure, safe upside.
- With Reputation no longer scoring (v6.3 Change 1e), Bookings is a big, reliable, penalty-free vector,
  so the objective layer is strictly a *worse* way to spend the same claims. **Objective-chasing is
  under-rewarded relative to its risk — so a rational line skips it entirely.** Not a knob problem; a
  structural one.

## 2) The two candidate fixes, head-to-head (2p; n=120–260/pair; ±~3pt run-to-run)

Metric convention: "avg win% vs field" is each line vs the other 6 (5 playstyles + the two controls
`ignore_obj`/`pure_drinks`); it is inflated ~+8–12pt for everyone by beating `pure_drinks` (~2%), so read
the **inter-playstyle spread** + the **h2h vs `ignore_obj`**, not the absolute top number.

| Config | `ignore_obj` | h2h (mix v ign) | 5-playstyle band | margin | contested | verdict |
|---|---:|---:|---|---:|---:|---|
| **A baseline** (both, base) | **80.7% (DOMINANT)** | 26% | 36–60 (endgame 36) | 10.1 | 4.6% | **FAIL** |
| **B tickets-only, base** | 40.4% | 73% | 47–68 (endgame 47) | 6.3 | 1.8% | kills it; band loose |
| **C tickets-only, EXPANDED** | 44.7% | 68% | **54–66** | 6.6 | 2.7% | **kills it; tight band** |
| D both + values ×1.6 | **68.1% (still leads)** | 43% | 45–63 | 17.8 | 4.7% | FAIL (not enough) |
| E both + values ×2.2 | 61.0% (mid-pack) | 48% | 46–64 | **20.1** | 5.3% | weak — swingy |
| F both + ×1.6 + **no penalty** | 49.5% | 62% | 52–64 | 12.6 | 4.6% | works, but 2 knobs + swingy |
| G tickets-only exp, `BOOK_W=1.0` | 48.3% | 62% | 54–64 | 7.2 | 5.6% | **robustness ✓** (≈C) |

**Read:**
- **Tickets-only (B/C) structurally kills the exploit** — with vendors giving no points, a zero-ticket
  line scores ~0 and loses 68–73% h2h. **G confirms it's not an artifact of my planner down-weighting**:
  whether the bots chase Bookings fully (`BOOK_W=1.0`) or lightly (0.35), the band and the `ignore_obj`
  collapse are the same.
- **The EXPANDED deck (C) is materially healthier than the base deck (B)**: the base deck leaves
  `endgame` stranded at 47% (too few finishable speed/collection tickets); the richer deck (region PAIRS,
  cross-region →X dishes, single-region DEPTH, deeper collections, food-count ladders) pulls `endgame`
  into band (~54%) and tightens the 5-playstyle spread to **~10pt with no crusher** — real choice in
  *which* tours to chase. Winner ticket-score rises 10.8 → 12.8 (more objective value actually in play).
- **The "just raise values" fix is a trap.** Raising `TA_TVAL` scales the **reward and the −½ penalty
  together**, so ignoring tickets stays a *safe* line: at ×1.6 `ignore_obj` still LEADS (68%); at ×2.2 it
  only reaches mid-pack (61%, ~coin-flip h2h) while **margins balloon to 20** and the score becomes
  ticket-dominated (winner Tickets 31 vs Bookings 22) — i.e. it drifts toward tickets-only anyway, but
  swingier and messier. To make raise-values actually beat `ignore_obj` you must *also* drop the penalty
  (F: two coupled changes → `ignore_obj` 49.5%, still swingier than C).

## 3) Does claiming vendors stay worth it under tickets-only? (CD concern #2) — YES, in-sim

`claims/gm` **9.3** and `vendors/player` **5.2** are **unchanged** from baseline (9.4 / 5.1); `promotes/gm`
~12 and the greedy-grab/Reach engine still breathe (grab 2.5/gm, reach-end ~6.9). Mechanically, claiming
vendors is still the central activity — a vendor is now valued as *the ramp piece + the stop that
completes a tour* rather than as raw points, and the bots claim just as many. **The sim cannot judge
whether claiming *feels* like a joyless means-to-an-end** (the CD's real worry) — that is the FTUE table
question. But there is no in-sim sign of vendors becoming inert.

## 4) Bonus probe — does tickets-only LIFT the contested Buzz fight (#2)? — NO (honest)

`contested_frac` is **2.7%** under tickets-only-expanded vs **4.6%** at baseline — it went *down*, not up
(`max_committed` 3.5 → 2.8: chasing patterns spreads Buzz thinner than chasing the few fat vendors did).
**The CD's hypothesis that tickets-only would converge players onto shared prizes is not confirmed in-sim**
— most tickets are *pattern* objectives (regions/counts/types), not specific-vendor, so they don't force
collisions. The `TA_SLOTS=1,1,1,1` scarcity lever (4 face-up vendors) nudges it back to **4.7%** and (bonus)
rebalances regions (Central claim 15→21%, South up), but the fight stays ~3–5% either way. **This 3–5% is
the sim's known concession-heuristic FLOOR** (bots concede rather than pile on; §blind-spots). *Whether a
5%-frequency fight is FUN when it happens is a human-table question the sim cannot answer* — flag it there;
don't over-engineer the board to chase the number.

## 5) Milestone runaway (#3) — `perplayer` (or `consolation`) removes the leader-pump

Baseline: the **same player takes both Rave-Review marks ~67–80%** (`ms_both_same`), and under
`MS_MODE=first` that player is the *only* one who gets the fuel → it compounds a lead. Fixes tested under
tickets-only-expanded:
- **`perplayer`** (each player earns the boon the first time THEY cross): boon-earners rise from **1.0 →
  ~2.0** per mark — both players get the fuel, so it **cannot pump the leader** (zero runaway). Band
  unchanged (it's small engine-fuel). **Simplest to teach; recommended.**
- **`consolation`** (first crosser full boon, later crosser reduced): near-identical in-sim; keeps a
  faint first-mover carrot. A fine alternative if the CD wants the race to still "mean" something.
- The boon still fires (`ms_earn` ~2), so the *race feel* survives; whether it's *exciting* is a table
  question. **Note: whichever mode, the milestone now needs a home once Bookings stops scoring — see
  ASSUMPTION below.**

## 6) Recommended settings (confirmed, n=260) + verdict

**RECOMMENDED FIX = tickets-only scoring + expanded ticket deck + milestone `perplayer`:**
`TA_SCORING=tickets_only TA_TICKETS=expanded TA_MS_MODE=perplayer`. Confirmed band (n=260):

| line | avg vs field | | line | avg vs field |
|---|---:|---|---|---:|
| balanced | 64.5% | | endgame | 54.7% |
| mix | 63.3% | | **ignore_obj** | **43.8%** (beaten 68–69% h2h) |
| opportunistic | 62.3% | | **pure_drinks** | **2.2%** (dies) |
| disruptive | 59.2% | | | |

5 playstyles in a **~10pt pack, no Condorcet crusher, objective-aware lines on top**; both naive/degenerate
controls clearly beaten; every real line crushes `random` (~99–100%). margin ~7 (tighter than baseline 10
and far tighter than raise-values' 18–20). **The v6.3 shape HOLDS with this fix in** — but it is a
**DESIGN CHANGE, not a number tweak** (dropping Bookings-as-score), so it needs CD sign-off (§decision).

## Fixes: number-tweak vs design-change (for the CD)
- **#1 (ignore_obj):** **DESIGN CHANGE — needs sign-off.** Vendors stop scoring; Tour Tickets become the
  sole scoring vector; ticket deck expanded. (The lighter number-only "raise values" alternative was
  tested and is worse — §2.)
- **#2 (contested):** unresolved in-sim (sim floor). `TA_SLOTS` is a real but structural lever; recommend
  carrying it as a **human-table question**, not a locked change.
- **#3 (milestone runaway):** **small rules change** — `perplayer` eligibility. Cheap, near-number-tweak,
  robustly removes the leader-pump.

## ⚠ ASSUMPTIONS + knock-ons I could NOT resolve (flag to the CD — design/theme/elegance calls)
- **Milestone home under tickets-only.** With Bookings no longer scoring, the marks' current home
  ("Bookings 7/14") is now a threshold on an **engine meter**, not a score track. **My sim placeholder =
  keep the marks on the Bookings-track count** (`MS_ON=bookings`, still accrues) — it runs fine. A cleaner
  home once Bookings isn't a "score" is **tickets-completed count** (`MS_ON=tickets`, marks at
  `MS_T1=2 / MS_T2=4`), which I've parameterised but not defaulted. **CD/bg-theme decide the home + name;
  the "Bookings" track name itself likely changes** (it's no longer bookings-as-points; it's an
  engine/ramp meter — maybe "Buzz/Coverage/Ramp"). Not a sim question.
- **Character kits drift under the new scoring (NOT pre-tweaked, per instruction).** Directional read
  (char vs neutral, so magnitudes are inflated — read direction only): **里長伯 councillor drifts HOT
  (~61%)** (cheaper claiming is worth more when claiming = the whole game) and **網紅 influencer drifts
  COLD (~39%)** (its Buzz-heavy kit + full lost-turn flaw is over-taxed when the fight matters less); 大哥
  dage sits **in band (~50%)** — the v6.3 "大哥 drifts up" worry does **not** materialise here, and the
  "can we drop 網紅's flaw?" question flips to "网红's flaw now looks too harsh." **If the CD adopts
  tickets-only, a fresh character re-pass is needed** (exactly like the v3→v3.1 deck-re-cost knock-on) —
  flagged, not touched.
- **Bookings-band retune.** Vendor Bookings values were set to matter as points; as pure engine pieces
  their *relative* values (ramp vs trophy) may want a light retune so every vendor is a worthwhile engine
  buy. Not tested here (out of scope); a follow-on if tickets-only is locked.

## The ONE change to test next — decision for the CD (A / B / C)
- **A — ADOPT tickets-only + expanded deck + milestone `perplayer` (RECOMMENDED).** It's the only fix that
  *structurally* kills the `ignore_obj` exploit (can't ignore objectives when they're the only points),
  it's robust (§G), gives the tightest healthy band, keeps vendors mechanically central, and de-swings the
  game. Cost: it's a genuine design change with the three knock-ons above (milestone home + track name;
  character re-pass; Bookings-band retune) — all follow-on, none blocking. **Then run the instrumented 2p
  Screentop FTUE** to answer what the sim can't: does claiming vendors *feel* like a joyless chore, does
  the expanded ticket choice read as rich-not-fiddly, and is the ~5% Buzz fight *fun* when it fires.
- **B — Keep "both" scoring, apply raise-values+no-penalty (F).** Only if the CD wants to preserve
  Bookings-as-a-scoring-vector for thematic reasons. It works but is worse: two coupled knobs, swingier
  (margin ~13), `ignore_obj` only just beaten (49.5%), and it half-converts to tickets-only anyway.
- **C — Ship the milestone `perplayer` fix now (cheap, standalone) and defer the scoring decision.** The
  milestone fix is independent of A/B and safe to lock immediately; #1 is the one that needs the CD's call.

**Recommendation: A + C** — lock milestone `perplayer` now, and adopt tickets-only+expanded pending the CD's
sign-off on the scoring redesign, then take it to the FTUE table. Do **not** pursue raise-values (B).

**Knobs added this pass:** `TA_SCORING`, `TA_TICKETS`, `TA_TVAL`, `TA_BOOK_W`, `TA_MS_MODE`, `TA_MS_ON`,
`TA_MS_B1/B2`, `TA_MS_T1/T2`, `TA_SLOTS`. New `metrics()`: `ms7_earn_players`, `ms14_earn_players`. New
`_wstat` fields: `cross` (→X dishes), `max_region` (deepest single-region stack). Central tea-export fix
(`CENTRAL_TEA_FIX`, 牛肉麵 →C) **confirmed applied**; Central still the lightest region (claim ~20% under the
expanded deck, up from ~15% baseline — the expanded Central tickets pull it up) — residual is a
bg-developer data knob, not a sim blocker.

---

# v6.3 — CHARACTER RE-PASS (tickets-only baseline, 2026-08-07)

The CD-approved balance follow-on to the **tickets-only lock** (v6.3-FIX option A, CD-signed-off). This
pass makes the CD-locked shape the **run default** (`SCORING=tickets_only · TICKETS=expanded ·
MS_MODE=perplayer` — the three flags flipped in the module) and re-tunes the two character kits that
drifted under it. **The Reach economy, tickets-only scoring, and the expanded 44-ticket deck are held
FIXED (all sim-validated); this pass touches the KITS + a Draw-band check only.** One kit at a time,
re-simmed to confirm. Char win-rates are char-vs-**neutral**, both seatings (so kit changes don't
interact — each is isolated); the playstyle band is character-neutral (so kits don't move it).

## Baseline drift confirmed (n=800, tickets-only, kits at the old v6.3 lock)
| Character | win% | |
|---|---:|---|
| 里長伯 councillor | **62.5%** | HOT — cheaper claiming scales harder when claiming IS the game |
| 網紅 influencer | **39.0%** | COLD — Buzz-heavy kit + full lost-turn flaw over-taxed |
| 媽寶 office | 43.7% | mildly cold (a tickets-only drift; see below) |
| 大胃王 dagushi | 53.2% | ✓ |
| 大哥 dage | 50.1% | ✓ |
Exactly the drift the CD flagged: 里長伯 hot, 網紅 cold; 大哥/大胃王 hold; 媽寶 a hair light.

## Change 1 — 網紅 influencer: RETIRE "Late to the Party" (one variable)
The Reach cap already throttles Promote-3 early (you can't over-commit Buzz past your Reach), so the
lost-turn flaw was **redundant double-punishment**. Dropping it (`INFL_FLAW=none`), keeping Promote-3 +
the goes-last seat tiebreak:

| Kit | n=800 | n=1200 | n=2000 |
|---|---:|---:|---:|
| "Late to the Party" (old lock) | 39.0% | — | — |
| **flaw RETIRED (default)** | **51.4%** | 50.7% | **48.7%** |

**→ RECOMMENDED FINAL 網紅: drop "Late to the Party"; keep Going-Viral (Promote places 3) + goes-last.**
Lands **~49%**, dead in band. Note the sim under-counts goes-last (a greedy bot doesn't feel reacting
last), so ~49% is if anything a slight ceiling — a real table sits a touch lower, still comfortably in
band. Protects the fun: the kit keeps its whole Buzz-forward identity, just sheds a punitive tax.

## Change 2 — 里長伯 councillor: Old-Favours discount → your FIRST region only (one variable)
New knob `TA_COUNCILLOR_REGIONS` (was hard-coded 2). Each region of discount is worth ~7.5pt:

| Old-Favours covers | n=800 | n=1500 | n=2000 | read |
|---|---:|---:|---:|---|
| 2 regions (old lock) | 62.5% | — | — | HOT |
| **1 region (RE-PASS default)** | 56.0% | 56.5% | **56.3%** | top-of-band (see caveat) |
| 0 regions | 47.5% | — | — | **guts the hook — rejected** |

**→ RECOMMENDED FINAL 里長伯: Old-Favours applies in your FIRST region only** (still −1 ingredient on the
first vendor you court there). Lightest touch, one number, **preserves the "regular's discount in your
home patch" hook** (arguably *more* thematic — a 里長伯 has clout in his own borough, not island-wide).
Lands **56%** in-sim = ~top-of-band; the sim **under-counts his no-HSR flaw** (a 4-region ring barely
feels it — a documented blind spot since v3.1), so a real table sits lower. Do **NOT** go to 0 regions
(47.5% but guts the hook — exactly the over-nerf the brief warns against).

**CD option B (if you want it dead-centre in-sim + an explicit ability+flaw silhouette):** pair REGIONS=1
with a thin-island-name flaw — **start at Reach 1** (`TA_COUNCILLOR_REACH=1`). Deep *local* favours,
limited *island-wide* reach — one coherent "hyper-local" identity.

| 里長伯 config | n=1500 |
|---|---:|
| REGIONS=1 (option A, default) | 56.5% |
| REGIONS=2 + start Reach 1 | 56.7% (start-Reach alone barely bites — Travel refuels it fast) |
| **REGIONS=1 + start Reach 1 (option B)** | **50.7%** (dead centre) |
| REGIONS=2 + start Reach 0 | 54.1% |

Trade-off: **A** is lighter (pure number-shrink, elegance-first) but leans on the no-HSR under-count to
call 56% "in band"; **B** is demonstrably mid-band in-sim and gives a clean flaw, at the cost of one
extra rule (a per-character start-Reach). Recommend **A**; **B** is a fair alternative if the CD prefers a
provable in-sim seat.

## Holds — 大哥 / 大胃王 / 媽寶 (final config, n=2000)
| Character | win% | verdict |
|---|---:|---|
| 大胃王 dagushi | 52.9% | ✓ holds (kit UNCHANGED — H1 hazards-twice) |
| 大哥 dage | 48.8% | ✓ holds (kit UNCHANGED — lead-by-1, no flaw) |
| 媽寶 office | **42.2%** | mildly cold — a **tickets-only drift, NOT caused by this pass** |
Both 大哥 and 大胃王 stay in band as the other two were tuned (as expected — the changes are isolated).

**媽寶 (office) — a borderline-cold WATCH, not a blocker.** It was already 43.7% in the untouched
baseline, so this is a tickets-only scoring drift, independent of the two kit changes. Its ability
("Travel draws the region you *left*") is a **routing-flexibility tool the greedy one-step bot
under-uses** (the same blind-spot family as the Gourmand pantry-wild / Poach denial / no-HSR) — bots
often draw the "wrong" (already-sourced) token, so **42% is a floor**; a human who wields the flexibility
deliberately sits higher. **Carry to the FTUE table with a watch-flag.** Do not shotgun a third kit
change on the sim number — if the table confirms weakness, the cheapest lever is a light non-Visit buff
(office kit already carries keep-2; a small start-ingredient or +1 Reach would lift it without touching
the Visit). NOT changed this pass.

## Draw-band check — no dead vendors; bands left AS-IS
Per-vendor claim frequency over 1500 balanced-mirror games (2p). "Draw" = the vendor value attribute
(the sim's `bookings`), now an ENGINE attribute (ramp + ticket-enabler + referenced by the 3 Draw-sum
tickets), not points.

- **No dead buys.** The lowest any vendor sees is **0.08 claims/game** — occasional, not dead.
- **Every Draw tier sees play, and the cheap end is *heavily* claimed:** Draw-1 day stalls run
  **0.39–0.76/game** — they're courted as **ramp icons + cheap ticket-enablers**, exactly the tickets-only
  logic (a vendor's worth is its engine/enabler role, not its Draw number). So low Draw ≠ dead.
- **The ★ apex stays special:** the Draw-8 apex (石板烤肉, E night, cross+★) is the standout at
  **0.55/game** — the most-claimed night vendor; the Draw-7 ★ trophies sit 0.45–0.69.
- **The cold cards are explained, and are NOT Draw-value problems:** the coldest are the intentionally
  **cheap drinks** (冬瓜茶 0.11 / 洛神花茶 0.08 / 珍奶 0.17 — low-stakes opportunistic stalls the greedy
  bots under-use, a documented blind spot; warm by design per identity) and the **known East/Central
  under-pull** (e.g. 竹筒飯 0.12 — the pricier of two same-Draw East day foods). Both are the existing
  **bg-developer region-data question**, not a Draw miscalibration.

**→ No Draw-band change.** Every vendor is a worthwhile claim and the ★ apex is meaningfully special.

## Top-line health carried (playstyle band, n=700, tickets-only default, character-neutral)
| Line | avg vs 5-playstyle field |
|---|---:|
| mix | 53.4% |
| balanced | 53.1% |
| opportunistic | 51.8% |
| disruptive | 47.9% |
| endgame | 42.8% |
| *ignore_obj* (naive) | *33.4%* (beaten 66%+ h2h) |
| *pure_drinks* vs balanced | *1.1%* (dies) |

Inter-playstyle band **~10.6pt** (42.8–53.4), **objective-aware lines on top**, **no crusher**, both
naive/degenerate controls clearly beaten, every real line crushes random. `contested_frac` **3.0%**
(the known concession-heuristic floor — a human-table fun question, not chased here), margin **7.7**
(tighter than the "both" baseline's 10), ~24.7 turns/player, ~5.2 vendors/player. **endgame (~43%) is
the softest of the five** — a pre-existing property of the tickets-only/expanded config (not this pass's
scope: kits + Draw), still viable and not a trap; flagged for a watch, not a blocker.

## Final five-character band (RECOMMENDED FINAL kits)
| Character | recommended kit | win% (n=2000) | note |
|---|---|---:|---|
| 網紅 influencer | Promote-3 + goes-last, **flaw retired** | **48.7%** | ✓ (goes-last under-counted → real a touch lower) |
| 里長伯 councillor | **Old-Favours = first region only** (opt A) | **56.3%** | top-of-band; no-HSR under-counted → real lower · opt B → 50.7% |
| 大胃王 dagushi | UNCHANGED | 52.9% | ✓ |
| 大哥 dage | UNCHANGED | 48.8% | ✓ |
| 媽寶 office | UNCHANGED | 42.2% | watch (floor; flexibility ability under-counted) |

## Verdict + the decision for the CD
**v6.3 is balance-clean and ready for the data rebuild + FTUE** — with **one CD call** (an A/B, not a
blocker):

- **A/B — 里長伯's brake.** **A (recommended):** Old-Favours = your first region only — lightest, one
  number, keeps the hook; 56% in-sim ≈ top-of-band once the under-counted no-HSR flaw is credited.
  **B:** the same, *plus* "starts with Reach 1" — dead-centre in-sim (51%) and an explicit ability+flaw
  silhouette, at the cost of one extra rule.
- **Carry to FTUE as watch-flags (none blocking):** 媽寶 42% (flexibility ability the sim can't see →
  likely a floor); 網紅 / 里長伯 both a touch lower at a real table than in-sim (goes-last / no-HSR both
  under-counted); endgame the softest playstyle (~43%); the ~3% contested Buzz fight (whether it's *fun*
  when it fires is the table's question, not a knob).

**Surfaced for the bible/mats rebuild (recommendations only — design docs + CSVs NOT edited):** 網紅 loses
"Late to the Party" (keeps Going-Viral + goes-last); 里長伯's Old-Favours applies in one region (option A)
or one region + start-Reach-1 (option B). No Draw-value / vendor-data edits. The 媽寶 watch + the East/
Central region-data pull stay open bg-developer/table items from prior passes.

---

# v6.3.1 — RE-SIM of the four CD changes (2026-08-08)

The gated re-sim of the four v6.3.1 CD reworks (design/v6.3-content-draft.md "FOUR CD CHANGES"), folded
ON TOP of the tickets-only lock (SCORING=tickets_only · TICKETS=expanded · MS_MODE=perplayer) and the
whole Reach economy — **all held FIXED**. All four change the economy, so they were validated **together**
in one gated run, then each probe isolated **one variable at a time**. New sim knobs: `TA_NIGHT_CURVE`
(0/1/2), `TA_MIN1_FLOOR`, `TA_START_SPLIT`, `TA_COUNCILLOR_KIT`, `TA_COUNCILLOR_HOME_DISC`,
`TA_COUNCILLOR_AWAY_TAX`, `TA_MAINT_COUNT/REGION/PHASE`. New instrumentation: the day/night sourcing
split (★ probe #1), free-(night-)bribe counter, night claims/player, maint fire/closed-turns, councillor
home-pick + away-tax incidence. Authoritative cells run at N=1500 (characters) / N=500 (playstyle + arc).

## Isolation — which change drives what (N=600 each, one variable on at a time)
| config (on top of tickets-only) | turns/p | LT% | stall% | night:day-src | free-night-bribes/gm | contested |
|---|---:|---:|---:|---:|---:|---:|
| raw v6.3 (no curve / split start / no maint) | 24.7 | 98 | 2 | **96%** | **1.73** | 2.9% |
| + common Taipei start only (CD-3) | 25.4 | 98 | 2 | 90% | 1.57 | **3.9%** |
| + Scheduled Maintenance only (CD-2) | 24.7 | 98 | 2 | 96% | 1.73 | 2.8% |
| + SOFT night curve only (CD-4 lvl1) | 26.5 | 96 | 4 | 123% | 0.95 | 2.6% |
| + STEEP night curve only (CD-4 lvl2) | 28.7 | 83 | **17** | 150% | 0.60 | 2.4% |
| **ALL v6.3.1 defaults (soft)** | 27.0 | 94 | 6 | 113% | 0.95 | 4.2% |

Reads cleanly: **CD-3 lifts collisions** (contested 2.9→3.9% at 2p, exactly the design's want), **CD-2 is a
rare spice** (negligible on the arc), and **CD-4 is the only load-bearing lever** — and the SHAPE-SPEC's
steep curve **over-corrects** (17% stall).

## ★ PROBE #1 — night-half sourcing (the load-bearing call) + the CD-4 backstop
The headline surprise: **night sourcing was never collapsing.** Even in raw v6.3 (no curve) the greedy
field sources at **96% of its day rate** at night — the "discount zeroes night costs → sourcing dies"
failure mode the CD flagged **does not manifest for the bots.** BUT the free-bribe counter shows the
exploit is real: raw v6.3 leaves **1.73 fully-free (all-ingredient-discounted) night bribes/game.** So the
concern is legitimate; it just shows up as *free marquee claims*, not as *dead sourcing*.

**Curve-level A/B (2p, one variable):**
| NIGHT_CURVE | night:day-src | night-clm/p | free-night/gm | 1st-night turn | LT% | stall% | turns/p | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0 off (raw v6.3) | 96% | 2.73 | 1.73 | ~34 | 98 | 2 | 24.7 | free bribes too easy |
| **1 SOFT (+1, cross-biased) — DEFAULT** | **113%** | **2.64** | **0.95** | ~35 | 94 | 6 | 27.0 | **kept** |
| 1 SOFT + MIN1_FLOOR | 114% | 2.64 | **0.00** | ~35 | 93 | 7 | 28.0 | floor not needed |
| 2 STEEP (+2) | 141–150% | 2.45 | 0.60 | ~36 | 83 | **17** | 28.7 | **REJECTED (stall)** |

**Verdict — SOFT curve, curve-only (MIN1_FLOOR OFF):**
- **Night sourcing stays solidly alive** (113% of day — night is now the *more* sourcing-heavy half; the
  GOAL was ~60–100%, so this clears it with room). Night claims/player 2.64 (the climax still fires),
  first-night-Bribe ~turn 35, LT 94%.
- **The free-bribe exploit is cut 1.73 → 0.95**, and — this is the key point — **every night marquee is now
  cross-region biased**, so the ~0.95 residual free bribes require a genuine **dual-region ramp** (you had
  to build *two* icon stacks to zero a `{N:3,S:1}`-shaped cost). That converts the *cheap single-region
  zero-out* into a *legitimate deep-engine reward* — a healthier outcome than a blanket floor.
- **MIN1_FLOOR is NOT needed.** It drives free bribes to 0.00 but adds a rule + lifts stall 6→7% for
  little gain, and it also taxes the legitimate dual-region payoff. Keep it as a reserve knob only.
- **The STEEP curve is rejected:** it meets the shape-spec's "≥2 mandatory residual" principle to the
  letter, but pushes ~16–17% of games past the last-train into the stall backstop (failure mode B — the
  vendor-claims clock can't reach its 10th claim before the drag cap). turns/player 28.7.
- **One watch:** the soft curve lifts 2p stall from 2% → **6%** (turns/player 24.7 → 27.0). Modest and
  acceptable (94% still end cleanly on the last train), but flagged — if the FTUE table reads games as
  "dragging" at the back half, the lightest recovery is a one-notch clock nudge (`V_END` 10→9 @2p) or a
  higher `STALL_CAP`; **do not** reach for the steep curve. (Recommendation only — clock NOT touched here.)

## CD-3 — common Taipei start: seat balance + the collision bonus
No catastrophic seat skew at any count now everyone launches from N/Taipei (seat_balance all **ok**, none
suspect): **2p 52/48 · 3p 39/31/30 · 4p 25/29/23/23** (n≈500 each). The 3p first-seat edge (39% vs 33%
fair = 1.18× — under the 1.5× smell threshold) is mild and pre-existing, not a common-start artifact.
**Bonus, as the CD hoped:** co-locating both agents in North from turn 1 lifts the 2p contested-Buzz rate
**2.7% → 4.2%** (and it climbs with count: 3p 5.3%, 4p 7.0%) — earlier collisions, the thing the design
wants. It's still the sim's known concession-heuristic floor (whether a ~4–7% fight is *fun* when it fires
is the FTUE's question), but common-start moved it the right direction. **網紅 going last from a shared
start is NOT newly punishing** — influencer lands 51.2% (below), squarely in band.

## CD-2 — Scheduled Maintenance: symmetric, no dead stretch, but RARE as specced
Fires cleanly and **symmetrically** (table-wide HSR closure hits everyone; closed-turns/gm 0.07 = a brief
one-go-around, no dead early stretch, no seat skew). The finding is **frequency**: seeded as **1 copy in
the North night deck it fires in only ~7% of games** (after a fidelity fix so a Travel flyby doesn't waste
the card — a Visit/CStore must surface it; with the common Taipei start players pass through N constantly).
**2 copies → ~12%.** So as written it is a near-invisible spice event (≈13 of 14 games never see it).
**Surfaced to the CD (design rec, not made):** if Scheduled Maintenance should be a *felt* beat, seed **2
copies** or **both** HSR-endpoint night decks (N *and* S); if it's meant as a rare surprise, 1 copy is
fine. No fairness problem either way. *(Sim ASSUMPTION: the marker rides the region's night ingredient
deck and only fires on a Visit/CStore draw; a Travel flyby returns it unfired.)*

## CD-1 — 里長伯 home-region kit: lands top-of-band; the away-tax bites; watch the camp
The reworked HOME-REGION kit (−1 home / +1 away, HSR restored) lands **55.2%** char-vs-neutral (N=1500) —
**top edge of the 45–55 band, essentially tied with 大胃王's accepted 54.8%.** Unlike the retired kit,
there is **no under-count excuse now** (he uses HSR, and the away-tax is fully modelled — it's paid on
26–33% of his food bribes and is worth ~8.6pt: dropping it → 64.9%). So 55% is a genuine slightly-hot
reading. **Levers (N=1500, one at a time):**
| 里長伯 config | win% | note |
|---|---:|---|
| home −1 / +1 (CD-1 canon default) | **55.2%** | top-of-band; kept as sim default (= spec) |
| home −1 / **+2 away-tax** | 49.8% | dead-centre, single lever — but deepens home-camping |
| home −1 / +1 **+ start-Reach 1** | 45.5% | in-band, clean offsetting flaw, doesn't worsen camping |
| home **−2** / +1 (disc+2) | 59.7% | hotter — rejected |
| legacy first-region-only kit (KIT=regions) | 60.7% | the retired kit runs hotter still under v6.3.1 |

**The camp watch (CD-3 interaction):** with the common Taipei start he picks **North home 60%** of the time
(N's 2 day-slots + the shared start pull him there) and bribes **home 3.39 vs away 1.13** — a home-centric
"borough boss" who rarely leaves. Thematic, but the greedy bot *minimises* the tax so it may over-camp;
`+2 away-tax` would deepen this, `start-Reach 1` would not. **Recommendation:** keep the canon **−1 / +1**
default (55%, playable, ceiling of band); if the CD wants dead-centre, prefer **start-Reach 1** (→45.5%,
a clean second flaw that doesn't worsen the camp) over **+2 away-tax** (→50% but more camping). CD call.

## Carried characters (N=1500) + the final bands
| Character | recommended kit (v6.3.1) | win% | verdict |
|---|---|---:|---|
| 網紅 influencer | Going-Viral (Promote-3) + goes-last, flaw retired | **51.2%** | ✓ (goes-last still under-counted → real a touch lower) |
| 大胃王 dagushi | UNCHANGED (H1 hazards-twice) | 54.8% | ✓ top-of-band |
| 大哥 dage | UNCHANGED (lead-by-1, no flaw) | 50.7% | ✓ dead-centre |
| 里長伯 councillor | HOME-REGION kit −1/+1 (CD-1) | 55.2% | top-of-band (CD lever above) |
| 媽寶 office | UNCHANGED | **43.5%** | carried WATCH (floor; flexibility ability under-counted) |

**媽寶 43.5% is the pre-existing tickets-only drift, NOT caused by this pass** (43.7% untouched in the
re-pass baseline; 45.0% at N=500 here). Its Travel-flexibility ability is a documented greedy-bot blind
spot → 43.5% is a floor; carry to FTUE with the watch-flag, don't shotgun a third kit change on the number.

**Final FIVE-CHARACTER band (N=1500):** 43.5% (媽寶, floor/watch) – 55.2% (里長伯, ceiling/CD-lever).
Three dead-centre (influencer 51.2 · dage 50.7 · dagushi 54.8); the two edges are both **known,
under-counted** cases, not new breaks.

**Final FIVE-PLAYSTYLE band (N=500, character-neutral):** mix 53.1 · balanced 52.3 · opportunistic 51.3 ·
disruptive 48.8 · endgame 46.0 — a **~7pt pack, no Condorcet crusher, objective-aware lines on top**;
`mix`/`balanced` beat the `ignore_obj` naive line 65% h2h; `pure_drinks` dies (2.9%); every real line
crushes `random`. endgame ~46% stays the softest (a pre-existing tickets-only property, viable not a trap).
The `ignore_obj` exploit stays structurally dead — the tickets-only lock holds under all four reworks.

## VERDICT — v6.3.1 HOLDS; ready for the data rebuild + FTUE, with two CD calls (neither blocking)
All four reworks are balance-clean **as long as CD-4 ships the SOFT curve, not the steep one the shape-spec
sketched.** The tickets-only health (band, no crusher, `ignore_obj` dead) survives all four changes.

- **CD call 1 — CD-4 curve depth (the important one).** Adopt the **SOFT (+1, cross-region-biased) night
  curve, curve-only** (recommended): night sourcing alive, free bribes cut ~45% and converted to a
  dual-region reward, +4pt stall (2p). The **steep +2 curve is rejected** (17% stall) and **MIN1_FLOOR is
  not needed.** *(If the CD wants zero free bribes on principle, MIN1_FLOOR is the clean guarantee at
  +1pt stall — but the soft curve's cross-region residual is the better design.)*
- **CD call 2 — 里長伯 ceiling.** Canon −1/+1 lands 55% (top-of-band, tied with 大胃王). Accept as-is, or
  take it dead-centre with **start-Reach 1** (→45.5%, preferred — doesn't worsen his North-camping) or
  **+2 away-tax** (→50%, but more camping).
- **Carry to FTUE as watch-flags (none blocking):** the 6% 2p stall (does the back half *drag*?); 媽寶 43.5%
  (flexibility the bot can't wield); 里長伯 North-camping 60% + home-centric 75% of bribes (does he feel like
  a stuck "borough boss"?); Scheduled Maintenance rarity (~7% at 1 copy — felt beat or rare surprise?);
  the ~4–7% contested Buzz fight (fun when it fires?); endgame the softest playstyle (~46%).

**Surfaced for the CD / bible / mats rebuild (recommendations only — design docs + CSVs NOT edited this
pass):** (1) CD-4 = SOFT curve, not steep — NIGHT "both" foods → 3 and apex ★ → 4 (top apex 5), **every
night marquee cross-region biased** (the cross component, not the raw magnitude, is what kills the free
bribe); DAY costs held as printed; MIN1_FLOOR not adopted. (2) 里長伯 = −1 home / +1 away (+ optional
start-Reach 1 if a dead-centre seat is wanted). (3) Scheduled Maintenance = consider 2 copies or both
HSR-endpoint night decks if it should be *felt*. (4) The value-referencing tickets (`d_prestige8`,
`n_prestige14`, `g_prestige12`) held up under the pricier night — night claims/player 2.64 stayed healthy,
so **no threshold retune needed** at the soft curve (they would have needed one at the steep curve). The
媽寶 watch + the East/Central region-data pull remain open bg-developer/table items from prior passes.

## CD DECISIONS — LOCKED (2026-08-08, Creative Director sign-off on the re-sim report)

The CD read the re-sim verdict above and locked the two open calls + the one minor knob. The sim now
encodes these as its defaults (the data rebuild inherits them):

1. **CD-4 night cost → SOFT curve, curve-only.** `TA_NIGHT_CURVE=1` (soft, already default), `MIN1_FLOOR`
   stays OFF. Steep +2 rejected. The cross-region-biased soft curve's dual-region residual is the accepted
   guard against the free-marquee bribe; the ~4pt 2p-stall lift carries to FTUE as a watch, not a blocker.
2. **CD-4 → 里長伯 pulled DEAD-CENTRE via start-Reach 1.** Locked `TA_COUNCILLOR_REACH=1` as the sim
   default (was the -1 reserve brake). The home-region kit alone ran 55.2% (top edge); start-Reach 1 lands
   him 45.5% with a clean second flaw ("his name doesn't carry across the island") that does NOT deepen the
   North-home camping tendency. The +2-away-tax alternative was rejected (it worsens camping).
3. **CD-2 Scheduled Maintenance → 1 copy, rare surprise.** `TA_MAINT_COUNT=1` (already default). Kept as a
   ~7%-of-games occasional disruption — a texture beat, not a planned-around mechanic. Revisit only if FTUE
   says the outage should be felt.

**Still carried to the data rebuild + FTUE (unchanged by these locks):** the 6% 2p-stall drag watch; 媽寶
43.5% (bot under-count of routing flexibility); 里長伯 North-camping feel; the ~4–7% contested-Buzz-fight
fun question; no ticket-threshold retune needed at the soft curve. **Next gated step: bg-developer bakes the
soft curve + start-Reach-1 + 1-copy Maintenance into the component CSVs + design docs + a decision-log
entry, then the human FTUE.**

## RE-RUN VERIFICATION (2026-08-08, bg-playtest) — the gated run RE-EXECUTED; the locks REPRODUCE

The v6.3.1 sim + this §v6.3.1 write-up were authored in a prior session; this pass **actually re-ran the
gated probe suite** on the committed module (`python sim/travel_agents.py`, N=600/cell authoritative +
N=120 smoke) to confirm the locked defaults reproduce before the data rebuild. **They do — every
load-bearing number lands within run-to-run noise (±~2–3pt at N=600) of the table above.** Module knobs as
committed: `NIGHT_CURVE=1 MIN1_FLOOR=0 START_SPLIT=0 COUNCILLOR_KIT=home COUNCILLOR_REACH=1 MAINT=1@N/ph2`
(`SCORING=tickets_only TICKETS=expanded MS_MODE=perplayer`).

| Verified cell (N=600 re-run) | committed §v6.3.1 | re-run | verdict |
|---|---|---|---|
| ★ night:day sourcing (soft, default) | 113% | **113%** | HOLDS — night stays live |
| free night bribes/gm (soft) | 0.95 | **0.95** | HOLDS — cut ~45% vs raw 1.73 |
| curve A/B: raw / soft / +floor / steep (stall%) | 2 / 6 / 7 / 17 | **2 / 4 / 7 / 17** | HOLDS — steep still rejected (17% stall) |
| Scheduled Maintenance fire rate (1 copy N night) | ~7% | **7%** | HOLDS — rare spice as specced |
| 里長伯 home-pick North / away-tax incidence | 60% / 26–33% | **61% / 30%** | HOLDS — home-centric, tax bites |
| 里長伯 LOCKED (home −1/+1 + start-Reach 1) | 45.5% | **46.5%** | HOLDS — in band (dead-centre lever works) |
| 里長伯 levers (no-reach 55 / no-tax 65 / legacy 61) | 55.2 / 64.9 / 60.7 | **57.2 / 64.8 / 61.0** | HOLDS |
| 網紅 flaw retired / (old lateparty) | 51.2 / — | **50.1 / 41.2** | HOLDS — retiring the flaw is right (lateparty → 41%) |
| 大哥 lock D (lead-1, no flaw) | 50.7% | **47.6%** | HOLDS — in band; alts A/C/E out (64/28/60) |
| 5-char band (locked kits) | 43.5–55.2 | **44.9–50.5** | HOLDS — tighter under the start-Reach-1 lock |
| 5-playstyle band (mix top, no crusher) | 46.0–53.1 | **46.4–51.9** | HOLDS — mix/balanced top |
| ignore_obj beaten h2h / pure_drinks | 65% / 2.9% | **64.8% / 2.7%** | HOLDS — tickets-only exploit stays dead |
| CD-3 seat balance 2p / 3p / 4p (all ok) | 52·48 / 39·31·30 / 25·29·23·23 | **50·50 / 37·31·31 / 27·26·23·24** | HOLDS — no suspect seat at any count |
| hoarder E / S vs balanced (a trap) | — | **14.8% / 16.0%** | HOLDS — denial is self-taxing, not a lockout |
| arc: turns/p · LT% · contested · claims/gm | 27.0 · 94 · 4.2% · 9.3 | **27.0 · 96 · 3.6% · 9.4** | HOLDS |

**Only deltas worth noting (all noise / known):** 媽寶 office **44.9%** here (0.1pt under the strict 45 gate;
the documented ~43.5% floor — its routing-flexibility ability is a greedy-bot blind spot, a carried FTUE
watch, *not* a new break); 大哥 47.6% and 大胃王 50.5% read a touch lower than the N=1500 authoritative
cells but sit comfortably mid-band. The `no_drinks` control reads ~52% (higher than disruptive/endgame) —
expected, not a flag: it's "balanced minus the low-value drinks," a near-peer of balanced, **not** a
degenerate control (the degenerate controls `ignore_obj`/`pure_drinks` are both clearly beaten).

**VERIFIED VERDICT — v6.3.1 HOLDS on re-execution.** All four CD reworks are balance-clean with the
CD-locked defaults; the tickets-only health survives all four. **Ready for the bg-developer data rebuild +
the human FTUE.** No new CD decision surfaced by the re-run — the two prior CD calls (soft curve;
start-Reach-1 councillor) both confirm in-band, and the 1-copy Maintenance rarity is unchanged. Carry the
existing watch-flags (2p back-half drag ~4–6% stall; 媽寶 floor; 里長伯 North-camping feel; the ~3–7%
contested Buzz fight's *fun*; endgame the softest playstyle; Maintenance ~7% — felt beat or rare surprise?)
to the FTUE table, where the sim goes blind.

---

# v6.4 — GATED RE-SIM (2026-08-08) — FOLLOWERS vocab · Bookings hand-limit N=3 · 網紅 start-max · base Travel de-sourced · Trending · the FOLLOWERS-ECONOMY sweep

Sim module reworked for v6.4 (`sim/travel_agents.py`; run via `python sim/travel_agents.py --v64 600`
— one gated invocation: validation + economy diagnosis + full lever sweep; character band at N=1200/cell,
sweep cells at N=600). This is the **interpretation**; nothing here is logged to the design-doc / bible /
decision-log — that is the CD's call at sign-off. **Module defaults for this run** (the carried v6.3.1
divergence still applies): `NIGHT_CURVE=1 MAINT=1 COUNCILLOR_REACH=1` (⚠ CANON is Maintenance ×2 /
里長伯 start-max 2 — see the v6.3.1 §CANON-vs-SIM-DEFAULT flag; unchanged by v6.4, carried to bg-developer),
plus the new v6.4 defaults `HAND_LIMIT=3 INFL_MAX_START=4 TRAVEL_NO_SOURCE=1 TRENDING=max(+1)`.

**Headline (3 validation items + the economy):**
**(1) base-Travel-de-source → 媽寶 FLOOR-FIX PASSES cleanly · (2) hand-limit N=3 PASSES (invisible, no
breadth pinch) · (3) 網紅 start-max 4 reads HOT (~58%) → the sim recommends the start-3 reserve dial ·
(4) the Followers-economy imbalance is REAL but every tightening lever over-corrects into STALL — so the
sim recommends a LIGHT touch (lost-war −1 sting) and carries the back-half-tension question to the table.**

## STEP 2 — VALIDATION (baseline v6.4, all economy levers OFF, N=600 arc / N=1200 band)

Arc is v6.3.1-identical → the renames + the three structural touches are balance-neutral at baseline:
`turns/plyr 28.8 · vendors/plyr 5.1 · winner 14.4 · end LT 93%/stall 7% · contested_frac 3.7% ·
max_committed 3.09 · reach_end 7.40 · forced_turn_frac 0.000`.

### (a) FIVE-CHARACTER BAND — `網紅 58.1 · 大胃王 54.2 · 媽寶 50.9 · 大哥 49.9 · 里長伯 47.5` [47.5–58.1]
- ✅ **媽寶 (Homebody) FLOOR-FIX — the clean win.** 43.5% → **50.9%**, lifted into band **without overshoot**
  (target was "off the ~43.5 floor, not past ~55"). As the **sole Travel-sourcer** (base Travel now sources
  nothing for everyone else) its routing ability finally earns its keep — exactly the predicted organic
  floor-fix (§Change 5e-2). No reserve lever needed.
- ⚠ **網紅 (Influencer) start-max 4 reads HOT — 58.1%, the band top, +4pt clear of the pack.** The +2
  head-start is too strong on this measure. **Reserve dial (§Change 4c): start-max 3 lands ~54% (in band).**
  → **the sim recommends locking 網紅 at start-max 3, not 4** (see the reserve-dial read below).
- 大胃王 54.2 / 大哥 49.9 / 里長伯 47.5 — all in band. (里長伯 at start-max **1** here, the sim default;
  at CANON start-max **2** he reads ~+7pt = ~55, top-of-band, as the CD accepted in v6.3.1 — a **carried
  divergence**, not a v6.4 change; his kit is untouched.)
- **Caveat on absolute levels (important for reading 網紅):** char-vs-neutral runs the *whole roster* hotter
  in v6.4 because de-sourcing base Travel makes every *ingredient* ability (大胃王 keep-3, 媽寶 travel-source,
  里長伯 discount) worth more vs a plain neutral — the field mean sits ~52, not ~50. So absolute numbers are
  inflated vs the v6.3.1 43.5–55.2 band, and the true 5-way gap is smaller than "58 vs 50" looks. Two things
  the harness under-credits, both cooling 網紅 at a real table: (i) her **"goes last" flaw washes out** in a
  2p both-seatings mirror (zero balancing credit here; a real 3–4p tempo cost), and (ii) the inflation is
  uniform. Net: **start-3 is the prudent sim-driven lock; start-4 is a legitimate table-confirmable
  alternative** if the CD wants the bolder head-start — a clean A/B for sign-off.

### (b) NIGHT-HALF SOURCING with base Travel DE-SOURCED — ✅ HOLDS
`src/turn DAY 0.20 · NIGHT 0.20 → night 105% of day` (target ~60–100%; **cleared with room**). Night claims/
plyr 2.64, first-night bribe turn 36.5 — the night climax still fires. **The CD-4 soft curve does NOT need
touching**: removing base Travel from sourcing did **not** collapse night sourcing (Visit + Convenience
Store + 媽寶's travel-draw carry it), and `_bump_src` was fixed so a base Travel is no longer miscounted as
a sourcing action (else this metric would have been meaningless). No night-curve or clock change from this item.

### (c) HAND-LIMIT N=3 — ✅ NO PINCH (invisible to healthy play)
- `collector` breadth line (weights n_collect6/g_collect5/food-ladders, pushes right up to the cap) wins
  **44.7% vs the field** — viable, **not** crushed by the 3-slot cap.
- Field: **cancels/gm 0.00 · at-limit claims/gm 0.00 · tickets_held_winner 2.58** — the winner's working set
  sits one *below* the cap, so N=3 never binds in healthy play (matches the ~2.38 prediction). Cancel-to-claim
  is modelled + scored (−floor(v/2)) but essentially never triggers for a competent line.
- **tickets-only health holds:** balanced beats `ignore_obj` **65.7%** h2h — the grind-only exploit stays
  structurally dead. N=3 is safe to lock.

## STEP 3 — FOLLOWERS-ECONOMY diagnosis + lever SWEEP ("let the sim decide the fix")

### Diagnosis (baseline v6.4) — the imbalance is REAL and reproduces
`gain/gm 17.1` (Travel **13.0** · events 1.8 · Rave milestones 1.89 · **Trending 0.45**) **vs `sink/gm 6.3`**
(greedy-grab 4.3 · bad-review events 2.0). The cap ramps `2 → reach_end 7.40` while `max_committed 3.09`
and **cap-bind DAY 21% / NIGHT 2%** — the cap **bites early, is slack late**: back-half (night) **cap-FILL
just 9% of the dial**, mean night slack **4.99**. **The top half of the ramped cap is dead weight in the
back half** — exactly the CD's read. (The new Trending gain adds only +0.45/gm — the dynamic marker is rare,
so it barely worsens the imbalance.)

### ⚠ LOST-PROMOTION-WAR — the CD's first-class lever: what it does, and what the sim says
**CURRENT STATE (off):** when a contested vendor resolves, the **loser's committed Followers simply RETURN
to supply, the cap is freed, and there is NO sting** — the missing, contention-scaled sink the CD flagged.
Baseline: **lost wars/gm 0.38**, **Followers committed per lost war 0.97** (~1 follower per lost war).

Lever test (field mirror, N=600):

| mode | contest% | lost-wars/gm | cap-bind NIGHT | night fill | night slack | reach_end |
|---|---|---|---|---|---|---|
| off (v6.3) | 3.7% | 0.38 | 2% | 9% | 4.99 | 7.40 |
| burn (committed SPENT) | 3.7% | 0.38 | 2% | 9% | 4.99 | 7.40 |
| dropmax −1 | 3.7% | 0.37 | 2% | 9% | 4.89 | 7.25 |
| dropmax −2 | 3.7% | 0.38 | 2% | 9% | 4.80 | 7.09 |
| both (burn+drop1) | 3.7% | 0.37 | 2% | 9% | 4.89 | 7.25 |

- **The lost-war consequence is nearly INERT as an economy sink** — because lost wars are **rare (~0.38/gm)**
  and each involves ~1 committed Follower. `burn` is invisible (a spent follower vs a 24-pool supply);
  `dropmax` shaves reach_end only 7.40→7.25 (−1) / 7.09 (−2) and moves back-half fill 0pt. **It cannot be
  THE economy fix at the current ~5% fight rate.**
- **But it is SAFE and it is the right STING.** It does **not** collapse the fight rate in-sim (contested
  stays 3.7% — the greedy bots are *blind* to the downside, so whether a real human stops contesting when
  losing drops their dial is the **#1 human-playtest question**, unchanged from the standing "~5% fight fun"
  flag). Recommended: **adopt `dropmax −1`** — losing a war drops your Followers-max by 1 (a real bite + a
  small contention-scaled sink that gives the dial a job) at **near-zero stall cost**. Do NOT go −2 or add
  `burn` on top (no sim benefit, and the sting escalates for no measured gain).

### Lever (b) — raise NIGHT/APEX demand + lift the ceiling  [the only real back-half mover — but it STALLS]

| night/apex/top | contest% | cap-bind N | night fill | night claims | stall% | reach_end |
|---|---|---|---|---|---|---|
| +0/+0/12 (base) | 3.7% | 2% | 9% | 2.64 | **7%** | 7.40 |
| +1/+0/12 | 3.3% | 6% | **19%** | 2.48 | **23%** | 7.95 |
| +1/+1/14 | 3.9% | 7% | 19% | 2.47 | 26% | 8.14 |
| +2/+1/14 | 3.7% | 9% | 22% | 2.42 | 31% | 8.50 |
| +2/+2/16 | 4.3% | 9% | 22% | 2.40 | 35% | 8.63 |

- **This is the ONLY lever that meaningfully spends the ramped cap late** — night-demand +1 ≈ **doubles**
  back-half fill (9%→19%) and triples night cap-bind (2%→6%). The dial finally gets used at night.
- **But it OVER-CORRECTS into stall exactly like the rejected steep night curve:** +1 pushes 2p stall
  **7%→23%** (the steep curve was rejected at 18%). Higher follower-demand = more Promotes per night vendor
  = the vendor-claims clock reaches last-train later = more games hit the drag backstop. Night claims also
  thin (2.64→2.48). **+2 is worse (31–35% stall).** So night-demand is a real fix for the *slack* but it
  cannot stand alone — it needs a compensating **one-notch clock nudge (`V_END` 10→9 @2p)** to absorb the
  stall, and that pairing was NOT swept here (a cheap confirming micro-run, flagged below).

### Lever (c) — Follower-SINK events — modest; shaves the ceiling, doesn't raise fill
`+0.10`: sink 6.3→6.8, reach_end 7.40→7.22, fill 9%→9%. `+0.20`: sink 7.2, reach_end 7.00, fill 9%.
Lowering the cap does **not** raise commitment (commit is the bottleneck, not the dial) — so sinks make the
dial read lower but do **not** make the back half tense. Useful only as a gentle ceiling trim.

### Lever (a) — tighten AVAILABILITY (fewer face-up slots) — the ONLY fight-rate mover, but stalls too
`slots 1,1,1,1` (vs 2,1,1,1): contested **3.7%→6.9%**, fights/gm **0.38→0.65** (nearly doubles the fight),
but stall **7%→18%**. Per the CD this is **NOT** the primary knob — the fight's *fun* at ~5–7% is the #1
human question, and tightening it also drags the close.

## RECOMMENDATION (the sim's read for the design lock)

**The honest finding:** the Followers-economy imbalance is real, but **the back-half cap slack is functioning
as the game's closing-valve** — every lever that tightens it (night-demand, availability) trades the slack
for **stall**, tripping the CD's own "without over-correcting into a starved, swingy feel" guardrail. So the
sim recommends a **LIGHT touch**, not a heavy re-cost:

1. **網紅 → start-max 3** (the reserve dial). start-4 reads hot (~58%, band top); start-3 lands ~54% (in
   band). *A/B for the CD:* start-4 is table-confirmable because the harness under-credits her goes-last
   flaw — but **3 is the prudent lock.**
2. **Lost-war consequence → `dropmax −1`** (a lost promotion war drops your Followers-max by 1). The CD's
   first-class lever, adopted for the **STING + a contention-scaled sink** it asked for — near-zero stall
   cost, gives the dial a real downside. **Not** the economy's whole fix (fights too rare in-sim), and its
   fight-suppression risk is a human question (bots are blind). Reject `burn` and `−2` (no sim gain).
3. **The "dead-weight top of the dial" → treat as cosmetic + a gentle ceiling trim** (optionally print the
   dial ceiling lower, e.g. 12→9, since `max_committed` is ~3 and the top is never reached) rather than a
   balance break. It does not hurt play (stall 7%, band healthy, night fires).
4. **CARRY the back-half TENSION question to the 2p human table** — where the fight's fun already lives as
   the #1 FTUE flag. **Reserve tension lever = night-demand +1 PLUS a `V_END` 10→9 clock nudge** (adopt only
   if the table finds the back half slack/boring; night-demand alone over-corrects into ~23% stall).
   **Flag a cheap confirming micro-run** of {night+1, V_END 9} before ever baking it.

**Everything else validated:** 媽寶 floor-fix (clean), hand-limit N=3 (no pinch, tickets-only health holds),
night sourcing (105% of day — CD-4 curve untouched), the renames/Trending/dial (balance-neutral).
**No blocker to the design lock.** The one genuinely OUT-of-band item is 網紅 start-max (→ start-3);
everything else is a light-touch feel choice for the CD + the table.

---

# V7 — MULTIPLAYER RE-HOME (3–6 players, area-majority) — Phase-1 re-sim

Hand-authored read of the CD-gated V7 Phase-1 re-sim. Auto report: `sim-results.md` (regenerated for
the V7 multi-count config via `python games/travel-agents/sim/travel_agents.py --v7 250 --out …`).
Run config: `BUZZ_MARGIN=1` (strict plurality — a tie BLOCKS) · 大哥 threshold `0` (wins ties all-game,
night-scoping dropped) · `LOSTWAR=burn` · `HAND_LIMIT=3` · 網紅 `start-max=4` · base Travel de-sourced
(媽寶 sole sourcer, `_bump_src` excludes base Travel) · Trending `+1 Followers-max` · run-out-of-stock
night `OFF` · 里長伯 reset to canon (−1 home / +1 away / start-max 2). Six characters incl. 阿嬤.
N = 250 games/seating (character band = avg of the first + last seat; field/seat probes ≥ 400–500).

## Encode summary (what changed in `sim/travel_agents.py`)
- **Per-count scaling — fixed the n=5/6 fallback bug.** `new_state` now defines slots / supply / clock /
  Booking-row / market-depth **explicitly per count** to §4 (verified non-fallback): slots N/C/S/E
  3p 2/2/1/1 · 4p 2/2/2/1 · 5p 2/2/2/2 · 6p 3/2/2/2; Followers supply 33/42/51/60; dusk 7/9/11/13;
  last-train 14/18/22/26; face-up Booking row 3 (≤3p) → 4 (4p+); ingredient market depth ×1.4/1.8/2.2/2.6.
- **Multiplayer area-majority + tie rule.** `_buzz_lead` already generalised to N (lead over the *max*
  rival); set `BUZZ_MARGIN=1` so a claim needs **strictly more** than every other agent and a **tie
  blocks** (verified: 2-vs-2 → no claim; 3-vs-2 → claim). The `_can_bribe` ≥1-committed floor stays.
- **大哥 wins ties all-game.** `_margin_for` returns `0` for 大哥 at every phase (dropped the unblessed
  v6.4b night-scoping). Verified: on a 2-vs-2 tie 大哥 *can* claim, a neutral cannot.
- **Lost-war = BURN by default** (losers' committed Followers spent, not returned); dropmax/both kept for
  the sweep.
- **Canon confirmations:** 網紅 start-max 4 (was stale 3); Promote flat 2 for all; hand-limit 3; base
  Travel de-sourced + `_bump_src` fix (both already correct); 媽寶 sole Travel-sourcer; Trending +1.
- **Neutralised unblessed exploration:** run-out-of-stock / region-shutdown (`NIGHT_DECK_CAP`) → default
  **OFF**; night contention slots (`NIGHT_SLOTS`) → **OFF** (night = day slots); 里長伯 `−2 home` and
  `start-max 1` (v6.4d tunes contradicting v6.4 §303) → reset to canon **−1 / start-2**. (`fighter`
  test-bot left in place — it's a strategy, not a rule.)

## How to read the character band (methodology caveat)
Each character is banded **vs a field of kitless `neutral`s** (char in the first seat and the last seat,
averaged). Because a `neutral` in that seat would win exactly the fair share (1/N), **`idx×fair` = 1.0
means "the kit performs no better than no kit," and idx > 1 is the EXPECTED, healthy sign that a kit
helps.** So — unlike the 2p "45–55%" band (which was symmetric around a 50% char-vs-one-neutral fair
point) — the MP read is: **nobody should be a FLOOR (idx ≪ 1, a trap kit); watch the relative spread and
any runaway crusher.** These are greedy bots: a floor on depth, blind to mobility value and to human
contest/politics.

## Per-count verdict (PASS / SOFT / FAIL)

| Probe | 3p | 4p (HOME) | 5p | 6p (stretch) |
|---|---|---|---|---|
| (1) six-char band | SOFT | SOFT | SOFT | **FAIL** (crushers) |
| (2) seat fairness | PASS | PASS | PASS | PASS |
| (3) downtime proxy | PASS | PASS | PASS | SOFT |
| (4) length vs clock | PASS | PASS | PASS | **FAIL** |
| (5) contested/economy | SOFT | SOFT | PASS | SOFT |
| (6) night sourcing (CD-4) | PASS | PASS | PASS | PASS |
| (7) tickets-only dead | PASS | PASS | PASS | PASS |
| (8) kingmaking/take-that | PASS | PASS | SOFT | SOFT |
| **overall** | **SOLID** | **SOLID** | **SOLID** | **NO-SHIP (as configured)** |

### (1) Six-character band
- **No hard floor at any count.** 阿嬤 sits nearest neutral (idx 0.98 → 1.06 → 1.02 → 1.04) — her OAP
  "reach any region in one Travel" mobility is a **known greedy-bot blind spot** (bots don't route to
  exploit reach), so idx≈1 is a *sim artifact, not a weak kit*. **Do NOT drop or buff her on this number**
  — her value is a table question (tempo/positioning). FLAG for the human table + Phase-2 guardians.
- **媽寶 lifted off her floor.** As the **sole Travel-sourcer** she now bands **at/above** neutral every
  count (idx 1.01 / 1.22 / 1.16 / 1.07) — she was the sub-neutral 43.5% floor at 2p. The §Change-5 organic
  floor-fix **works and does not overshoot**. PASS.
- **網紅 start-max 4 reads HOT in MP** (idx 1.25 / 1.50 / 1.46 / 1.74). The persistent +2 ceiling lets her
  out-commit early in every fight, and the edge *grows* with player count. **Recommend testing the reserve
  start-3** (§4c) — start-4 is the top of the band and at 6p she's a co-crusher. Goes-last seat read: at
  3p being last costs her hard (seat0 48.8 vs last 34.4); at 4–6p the first/last gap is small — but note
  the sim only models "goes last" as turn order, not as a real structural penalty, so the *felt* goes-last
  flaw is under-credited (a table watch, worse as N rises per §1/§4c).
- **大哥 win-on-tie all-game scales too strong at high counts** (idx 1.18 / 1.37 / 1.41 / **1.79**). More
  players → more ties → more free claims for him. At 3–4p he's in the pack; by 6p he is the top crusher.
  **FLAG:** the all-game tie-win (adopted over the night-only edge) may need re-scoping for 5–6p (e.g.
  night-only after all, or a soft cost) — decide with the human table + bg-critic.
- **里長伯 at canon runs hot** (idx 1.31 / 1.46 / 1.44 / 1.31), consistently top-2/3. This is the
  canon-vs-exploration reset I made (−1 home / start-2, per v6.4 §303) — the v6.4d exploration had tried
  −2 home / start-1 to tame him. At 2p canon the CD accepted him "top-of-band 55%"; in MP he's similarly
  hot. **FLAG the discrepancy** (below) for a CD ruling on his canonical numbers.
- **The 6p band FAILS**: spread blows out to idx 1.04–1.79 with 大哥 + 網紅 pulling away as crushers —
  compounding the 6p length fail below.

### (2) Seat fairness — PASS at every count
No suspect seat at 3/4/5/6p (each seat within fair bounds; 6p has a benign 3% tie rate). The common Taipei
start + fixed order does **not** create a catastrophic first/last skew for the *field*. The one seat-order
effect is 網紅-specific (goes-last at 3p, above) — carry to the table, not a board-level fairness break.

### (3) Downtime — PASS 3–5p, SOFT 6p
`forced_turn_frac = 0.000` everywhere (the one-action turn: never a dead/forced move). avg_legal_actions
~8.8–9.3 (healthy decision load, not AP-inducing). turns/player 28–30 at 3–5p; **34.6 at 6p** (up against
the stall backstop — see length). The one-action turn is doing its load-bearing downtime job through 5p;
6p downtime is coupled to the length fail (five rivals between turns *and* the game overruns).

### (4) Length vs the clock — PASS 3–5p, **FAIL 6p**
3p/4p/5p end on the **last train 94% / 97% / 93%** of games (stall backstop only 3–7%) — the vendor-claims
clock fires cleanly and paces the game. **6p: the last train NEVER fires (0%)** — 71% of games hit the
hard stall backstop (34 turns/player) and 29% end on deck-dry, at ~33 turns/player. **The last-train = 26
clock is unreachable at 6p**: the per-player claim *rate* DROPS at 6p (crowded board + heavy contention +
near-empty supply, `supply_min 7.5` vs 24–29 lower), so §4's "per-player claims ≈ constant" assumption
**breaks** — 6 players do NOT sustain 26 table claims before the backstop. This is the 6p ship gate, and
it does not hold.

### (5) Contested / lost-war economy
- **Contention comes for free with players** (as the pivot predicted): contested_frac 5.1% → 6.3% → 9.6%
  → 14.1%; lost_wars/game 0.81 → 1.34 → 2.72 → 6.28; followers/lost-war 1.6 → 2.1 → 3.0 → 5.0. The lost
  promotion war becomes the **norm** at 5–6p, exactly the design goal — with **zero forcing of the fight
  rate**.
- **BUT the back half is not tense at 3–5p in-sim, and no sink lever changes that.** Gains still ≫ sinks
  (~2.6–2.7 : 1), capfill_night stays 0.10–0.13, night cap-bind ~0.03–0.06, slack_night ~5. The dial's
  top half remains dead weight in the back half — the *same* 2p diagnosis, persisting because the **bot
  concession heuristic keeps commitment far below the cap** (contested_frac is a documented FLOOR). At 6p
  the cap finally binds (capfill_day 0.34, max_committed 10.2) — but only because the board is gridlocked,
  which is the *bad* kind of tension (the length fail).
- **This is the load-bearing "bots can't judge it" caveat:** whether the back half FEELS tense is the #1
  human-table question. The sink is correctly structured; the sim just can't exercise it because bots
  won't pile in like people will.

### (6) Night sourcing (CD-4) — PASS every count
With base Travel de-sourced, night:day sourcing ratio = **105% / 97% / 98% / 99%** — comfortably in the
~60–100%+ target at every count. Removing base-Travel sourcing did **not** collapse night sourcing (媽寶's
lone Travel-draw + Visit/CStore carry it). **Do not touch the night curve.** Minor watch: free-night-bribes
crept 0.95 (v6.3.1) → ~1.2–1.4/game at 3–5p (0.6 at 6p) — a small rise, not a regression; flag, don't act.

### (7) Tickets-only — PASS every count
`ignore_obj` is crushed: 6.2% / 1.6% / 0.8% / 2.0% vs fair 33/25/20/17%. A zero-ticket line loses hard at
every count; the expanded/duplicated deck's collection lanes are not pinched by hand-limit 3.

### (8) Kingmaking / take-that
takethat_hits/game scales with player count (4.6 → 9.6 → 18.3 → 39.4) but these are **event spillover
pokes, not directed kingmaking** — the sim's greedy bots don't collude or target. The structural
anti-kingmaking property is intact (tickets-only, you only ever score your own pile, burn-your-own-fight).
**5–6p politics/griefing is the new worry that replaces the 2p fight-rate worry and is a genuine table
question** (hand to bg-critic + the human table).

## Lost-war sink recommendation → **BURN alone (canon), levers held in reserve**
The 4p + 5p sweep (off / burn / dropmax1 / both / burn+leverB[night-demand+ceiling] / burn+leverC[sink
events]) shows **all six configs are statistically indistinguishable** on the tension metrics (4p
capfill_night 0.11–0.12, slack 4.95–5.38, LT 94–98%; 5p capfill 0.12–0.14, slack 5.5–5.8, LT 88–92%).
Because bot contention is a floor, no sink lever can tighten a back half where commitment never approaches
the cap. Read:
- **Adopt `burn` as the default** — it is the correct **contention-scaled, zero-bookkeeping** sink; it does
  no harm in-sim and is the structurally right sting for when humans DO pile in (which they will, far more
  than bots). This matches the §3 LOCKED recommendation.
- **Reject `dropmax`/`both` as the default** — they add a dial-tracking step for **no measurable sim gain**
  and carry a real over-punish/fight-suppression risk. Hold as a reserve escalation only if the human table
  finds the back half slack even with humans fighting.
- **Levers b (night/apex demand + higher ceiling) and c (sink events) are also inert in-sim** — hold both
  as reserves; do not bake now.
- **The economy's back-half tension is explicitly deferred to the human table** (the #1 feel question),
  per the mandate "do not force the fight rate."

## 6p ship / no-ship read → **NO-SHIP as configured; fixable-or-cap is a CD call**
6p **fails the length bar** (0% last-train, 71% stall, ~34 turns/player) and shows a **crusher band**
(大哥/網紅 idx ~1.75) and near-supply-starvation (`supply_min 7.5`). Per the pivot's own gate ("ship 6
only if Phase-1's downtime + length hold"), **6p does not clear.** Two paths for the CD/Phase-2:
1. **Re-tune 6p and re-sim:** nudge the 6p last-train **down hard** (≈26 → ~18–20 so it fires before the
   backstop), and likely **raise 6p Follower supply** (60 → ~68–72) so the deep-pile + burn economy doesn't
   bottom out. Then re-run `--v7`. If it then ends on the clock at an acceptable length, 6p can ship as a
   validated stretch.
2. **Cap the range at 3–5** and call it a great 3–5 game (a smaller range done well beats a wide one done
   badly). **This is my leaning** unless a focused 6p re-tune clears both the length AND the 大哥/網紅
   crusher gap — two coupled problems, not one.

## FLAGS for the CD + Phase-2 guardians
1. **6p length + crushers (blocking for 6p).** See above — re-tune-and-re-sim or cap at 5.
2. **網紅 start-max 4 is HOT in MP** (idx 1.5 @4p, 1.74 @6p). **Recommend the reserve start-3** (§4c) — a
   one-line change; re-band confirms. Human table can confirm start-4 (goes-last under-credited in-sim).
3. **大哥 all-game tie-win over-scales at 5–6p** (idx 1.41 → 1.79). Re-scoping candidate (night-only edge,
   or a soft cost). bg-critic + table.
4. **里長伯 canon-vs-exploration DISCREPANCY (needs a CD ruling).** The committed sim carried v6.4d
   *unblessed* tunes (`−2 home`, `start-max 1`) that **contradict v6.4 CANON §303 (−1 home / +1 away /
   start-max 2 like everyone)** and decision-log CD-1. I **reset the sim to canon**; at canon he runs hot
   (idx 1.31–1.46). The CD must confirm his canonical numbers (canon-hot, or adopt an exploration brake).
5. **阿嬤 bands at ≈neutral (idx ~1.0) — a bot blind spot, NOT a weak kit.** Do not tune her on this number;
   her mobility value is a table read. Phase-2 still owes her the bg-theme dignity/identity bless (a granny
   must read warm, never a caricature) + naming coherence.
6. **Back-half economy tension is unresolved in-sim** (dead top-of-dial persists at 3–5p because bot
   contention is a floor). Carry as the #1 human-table feel question; burn is the right default sink.
7. **run-out-of-stock/region-shutdown OFF changed nothing material** vs the v6.4b exploration for the
   *balance* read (it was never V7 canon) — noted per the checklist; no economy/clock artifact from
   disabling it beyond the honest 6p clock behaviour above.
8. **Sim blind spots (bots = floor, not ceiling):** the FUN of the area-majority fight; real downtime FEEL
   at 5–6p; 阿嬤's mobility; directed kingmaking/take-that politics at 5–6p. All → the human table.

## The one change to test next
**網紅 start-max 4 → 3** (the single out-of-band, one-line, self-tapering fix) — re-band at 3–5p to confirm
she lands in the pack (expected idx toward ~1.2–1.3), then the human table decides 3-vs-4 (the goes-last
flaw is under-credited in-sim). Everything else at 3–5p is SOLID; 6p is a separate CD decision
(re-tune-and-re-sim vs cap at 5).

---

# V7 — PHASE 1.5 RE-SIM (2026-08-08) — the DECK-DRIVEN clock + the DIAL-DROP lost-war sink

CD-gated re-sim of the two §11 fixes (deck-driven clock replacing the vendor-claims clock; dial-drop
replacing burn), written against the Phase-1 verdict **3–5p healthy, 6p BROKEN** (0% last-train / 71%
stall / 34.6 t/p / supply_min 7.5 / 網紅 idx 1.74, 大哥 1.79). Auto report: `sim-results.md`. Config
run: `CLOCK=deck · DAY=3·(N+1)/NIGHT=4·(N+1) · LOSTWAR=dialdrop (−1 day/−2 night, floor=start) · strict
plurality tie-blocks · 大哥 wins ties all-game · hand-limit 3 · 網紅 start-max 4 · base-Travel de-sourced
· Trending +1`. N=250/seating.

## HEADLINE — 6p is FIXED; the economy tightened; the battlers COOLED (not hotter). Adopt both fixes.

Both §11 moves work, and they compound exactly as §11e predicted. **6p now completes on the clock and
bands honestly for the first time.** The dial-drop did the OPPOSITE of the feared §11e outcome — instead
of buffing the tie-winners it **cooled 網紅 and 大哥 hard** (the whole economy tightened, so the fight-edge
is worth less). **Neither reserve lever is needed.** The one persistent band outlier is now 里長伯 (the
carried canon-hot councillor), not the battlers.

## What changed in `sim/travel_agents.py` (the encode)

- **Deck-driven clock (§11a, `CLOCK_MODE="deck"` default).** The shared BOOKING deck IS the clock: the
  DAY booking deck exhausts → DUSK (flip to night); the NIGHT booking deck exhausts → LAST TRAIN (end).
  Exhaustion = a refill finding the reserve empty (the seeded boundary card). REMOVED as clock drivers:
  the vendor-claims counter, the dusk@/last-train@ thresholds, the +1-on-Bribe step, the vendor-deck-dry
  end. The old STALL backstop is retained ONLY as a safety net (raised 34→50 t/p) so a real deadlock
  shows as a stall% spike rather than being masked; under the deck-clock it fires 0–3%.
- **Deck sizes (§11b) — TUNED.** §11b specced DAY=3·(N+2)/NIGHT=4·(N+2) [15/20·18/24·21/28·24/32] as
  *starting* knobs, flagged "the #1 re-sim knob." **At +2 they ran long (t/p 32–36) and 6p still stalled
  8%.** Swept the offset → **DECK_OFFSET=1 (DAY=3·(N+1)/NIGHT=4·(N+1) = 3p 12/16 · 4p 15/20 · 5p 18/24 ·
  6p 21/28)** lands every count at t/p 26.4–29.0 with LT 97–100%. The flat +3 day/+4 night-per-player and
  the 3:4 day:night ratio are preserved; only the constant offset moved 2→1. (Equal decks, which put dusk
  at ~50%, re-broke 6p — LT 67% — so night stays the longer act, dusk ~24–41%.)
- **Dial-drop sink (§11d, `LOSTWAR="dialdrop"`).** Lost-vendor Followers RETURN to the loser's supply
  (nothing burned); the loser's Followers-max drops −1 day / −2 night, floored at the character's START
  value (2 base / 4 網紅), with the committed-over-max reconcile (instrumented — fires **0.000/gm** at
  every count, provably dormant as §11d showed).
- **MODELING CHANGE (load-bearing — flag for the CD).** Under the deck-clock the balanced bots now keep
  their booking hand FULL to the hand-limit (was: self-limit to 2). This models the CD's design premise
  ("you score only by completing Bookings, so you must keep drawing new ones"). **Without it the deck
  depletes at the fight-gated completion rate and 5–6p re-stall** (LT 48%/10%) — i.e. the booking-clock is
  NOT automatically fight-independent; it only decouples if players churn their booking hand. See the
  FLAGS section — this is a real rulebook/teaching implication, not just a sim knob.

## Per-count verdict — PASS at EVERY count (incl. 6p)

| | end LT% | stall% | t/p | dusk/last | supply_min | max_committed | slack_night | band idx |
|---|---|---|---|---|---|---|---|---|
| **3p** | 99 | 1 | 29.0 | 31/82 | 26.0 | 3.48 | 4.40 | 0.97–1.39 |
| **4p** | 100 | 0 | 26.8 | 24/101 | 33.3 | 4.00 | 3.77 | 0.92–1.26 |
| **5p** | 100 | 0 | 26.4 | 45/124 | 40.7 | 4.28 | 4.02 | 0.93–1.38 |
| **6p** | 97 | 3 | 27.6 | 63/156 | 47.4 | 4.70 | 4.25 | 0.91–1.40 |

## Probe read (the §11f probes)

**(A) 6p completes? — YES.** end LAST TRAIN **97%** (was 0%), STALL **3%** (was 71%), t/p **27.6** (was
34.6, target 26–30). dusk 63 ≈ 40% of last 156 (night the longer climax, on §11c intent). The deck-clock
is monotonic and drawn by the (now-eager) booking action → it fires reliably at every count.

**(B) Economy tightens? — YES.** slack_night off the ~5.0–6.5 Phase-1 range to **3.8–4.4** at every count.
supply_min **recovers off 7.5 → 47.4 at 6p** (no starvation anywhere; 26–47). max_committed **10.2 → 4.7**
at 6p — dials no longer ramp/commit unchecked. gain:sink narrows from ~3:1 to ~2:1 (6p 52.0 vs 25.7). The
dial-drop is a genuine capacity sink. (capbind_night stays low 0.05–0.10 — the dial still doesn't *hard*-
bind at night in-sim, because bot contention is a floor; carried as the human-table feel question.)

**(C) Six-character band on COMPLETED games —** now measured honestly (6p completes). **阿嬤 (the Phase-1
floor) HOLDS at idx 0.91–0.97** — just below fair share, in-band-ish, a documented bot blind spot, not a
weak kit (§11e prediction confirmed). **網紅 & 大哥 (the 6p-hot pair) COOLED HARD:** 網紅 idx **1.74 →
1.31** (6p), 大哥 **1.79 → 1.28** (6p). The dial-drop did NOT worsen their hotness — the whole-economy
tightening cut the value of their fight-edge. **The new band top at every count is 里長伯 (idx 1.39–1.60),
the carried canon-hot councillor** — now the #1 band outlier, in place of the battlers.

**(D) Fairness / health / diagnostics —** seat fairness OK at every count (ties 0%). ignore_obj 1.2–4.6%
(≪ fair) — tickets-only DEAD. contested_frac 4.4–8.0% — NOT cratered (dial-drop vs off barely moves it:
6p 5.1% vs 5.3%), so the sink does NOT over-suppress contention (probe 9 PASS). Dial-drops 0.48–1.20/gm,
mostly NIGHT (0.38–0.92 vs day 0.08–0.28 — the −2 night sink is where it bites, as designed); floor_hits
0.02–0.11/gm (rare); **committed-over-max fires 0.000/gm** (dormant, confirmed). empty_mkt_draws **0.00** —
the reshuffling ingredient markets never gate progress. No deck-clock deadlock; boundary card always drawn.

## The 大哥 / 網紅 CALL (CD: "let the sim decide") → **leave the reserve levers UNUSED**

Ran the DEFAULTS first: at 6p 網紅 idx ~1.31 and 大哥 ~1.28 (main band) — **top-of-band, marginally over
the 1.10 nominal ceiling but nowhere near the Phase-1 crusher (~1.75/1.79), and both sit BELOW 里長伯 (1.40)**.
The focused reserve-lever follow-up confirms neither lever earns its keep:

- **Cap 網紅's floor at 2:** 6p 網紅 1.45 → 1.43 — **~zero effect** (the floor bites only ~0.08/gm, so
  lowering it does nothing). Do NOT adopt — it adds a special-case rule for no measurable gain.
- **Night-scope 大哥's tie-win:** 6p 大哥 1.27 → 1.28 — **no effect on him** (most of his wins are already
  at night). It does incidentally cool 網紅 (1.45→1.28) via the shared economy, but that's a side effect,
  not a targeted fix. Do NOT adopt — it re-adds the unblessed night-scoping complexity for no on-target gain.

**Recommendation: keep the V7 canon kit — 網紅 floor = start-value 4, 大哥 tie-win all-game.** The dial-drop
already did the cooling the reserve levers were held for. Hold both levers as documented reserves only.

## The CD escalation ladder — nerf-battlers vs remove-flaws vs buff-the-weak (band SPREAD, 6p)

| approach | 6p spread (idx hi−lo) | read |
|---|---|---|
| defaults (canon dial-drop) | 0.63 (里長伯 1.60 the outlier) | battlers cooled; 里長伯 the lone top |
| (1) nerf-battlers (levers) | 0.42 | barely helps; levers do little (see above) |
| (2) remove-ALL-flaws | **0.77 — WORSE** | un-checks 里長伯 (1.73) & 大哥 (1.45): flaws are load-bearing |
| (3) buff-the-weak (阿嬤+媽寶) | **0.32 — tightest** | lifts 媽寶; 阿嬤 stays 0.95 (bot blind spot) |

**Ladder read:** "**remove all flaws**" is the WRONG lever — it WIDENS the band, proving the strong
characters' checks (里長伯's away-tax especially — removing it sends him to 1.73) are doing real work and
must stay. "**Buff-the-weak**" gives the tightest band but can't move 阿嬤 (her basket cap isn't her
in-sim bottleneck — bots under-value her mobility). "Nerf-battlers" is unnecessary. **None of the three
is the right primary move**; the targeted fix is a 里長伯 brake (below), not a blanket flaw/buff pass.

## The ONE change to test next → a **里長伯 (councillor) brake** (a CD canon ruling first)

With the battlers cooled, 里長伯 is the single out-of-band character (idx 1.39–1.60, top at 3p/5p/6p).
This is the **carried canon-vs-exploration discrepancy** (Phase-1 FLAG 4 / decision-log CD-1): at canon
(−1 home / +1 away / start-max 2) he runs hot. The escalation ladder shows his away-tax is load-bearing
(removing it → 1.73), so the brake is in the OTHER direction. Candidates, one at a time:
1. **Harsher away-tax (+2 away)** or **start-Followers-max 1** (the v6.4d exploration brake) — needs the
   CD to bless departing from canon §303.
2. Re-run `--v7` with the chosen brake; expected to pull him toward idx ~1.15–1.25 (into the pack behind
   大哥/網紅). Everything else at every count is SOLID.

**Decision for the CD (A/B/C):**
- **(A, recommended) ADOPT both §11 fixes as canon** — deck-driven clock at **DAY=3·(N+1)/NIGHT=4·(N+1)**
  (the tuned offset) + **dial-drop −1/−2 floor=start**, keep the battler kit as-is (no reserve levers).
  Then test the ONE 里長伯 brake. 6p SHIPS as a validated stretch (it now clears the length + band gates).
- **(B)** Adopt the fixes but ALSO pre-emptively night-scope 大哥 / cap 網紅's floor. *Not recommended —
  the sim shows both do ~nothing on-target and add rules.*
- **(C)** Adopt the clock but keep BURN instead of dial-drop. *Rejected — burn tested within noise in
  Phase-1; the dial-drop is what recovered supply_min (7.5→47) and cooled the battlers.*

## FLAGS for the CD + Phase-2 guardians

1. **Deck sizes are TUNED to DECK_OFFSET=1** (3·(N+1)/4·(N+1)), not the §11b starting 3·(N+2)/4·(N+2).
   Update §11b's canon numbers to **3p 12/16 · 4p 15/20 · 5p 18/24 · 6p 21/28** if the CD adopts.
2. **The deck-clock RELIES on players keeping their booking hand full** (the modeling change). This is a
   real teaching point: the rulebook/player-aid should nudge "keep drawing tours — an empty booking slot
   is wasted tempo." A table that hoards a small hand of un-completable tours would drag the clock. Hand
   this to `bg-elegance` (rulebook) + confirm at the human table / FTUE. NOT a blocker, but the one
   assumption the whole clock rests on.
3. **里長伯 is the new #1 band outlier** (canon-hot). The battler worry is resolved; the councillor canon
   ruling is now the open balance question. See "one change to test."
4. **阿嬤 bands at floor (idx ~0.91–0.97) — bot blind spot, NOT a weak kit** (unchanged read). Do not tune
   on this number; her mobility value is a human-table read. Still owes the Phase-2 bg-theme dignity bless.
5. **4p night-sourcing dipped to 67% of day** (day rate 0.10/turn) — within the CD-4 60–100% target but
   noisy: the 4p day is very short (dusk ~24% of the game) so few day-sourcing actions are sampled. Flag,
   don't change; re-confirm if the 4p day lengthens.
6. **Back-half cap-bind is still soft in-sim** (capbind_night 0.05–0.10) even though slack tightened — bot
   contention is a floor, so the dial "binding late" is still a human-table feel question, not a sim call.
7. **Sim blind spots (bots = floor):** the FUN of the area-majority fight, the *feel* of a dial-drop
   ("taken down a peg"), real 5–6p downtime, 阿嬤's mobility, directed politics/kingmaking. → the table.
