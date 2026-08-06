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
