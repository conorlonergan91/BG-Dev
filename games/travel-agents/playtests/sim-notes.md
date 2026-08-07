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
