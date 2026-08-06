# Travel Agents: Taiwan — simulation notes (interpretation)

Hand-authored read of the sim runs. Owner: `bg-playtest`. Sim module: `../sim/travel_agents.py`
(encodes spine A, the design-doc rules as-written). Auto-generated tournament report:
`sim-results.md`. This file is the interpretation + the one change to test. **Nothing here has been
logged to the design-doc / bible / decision-log — that's the CD's call after reading this.**

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
