# Beacon — Simulation findings (interpretation)

Hand-written reading of the auto-generated `sim-results.md` (3000 games/matchup, first-pass rules).
*Regenerate the raw report with:* `python tools/sim/simulate.py --module games/beacon/sim/beacon.py --n 3000 --out games/beacon/playtests/sim-results.md`

## Iteration log (design → critic → simulate → tune)

| Version | Rule change | Result |
|---------|-------------|--------|
| **v0.1** | beam winner takes the ship *and* the Tide | `always_high` **dominant 66.7%**; spread ~55 pts; margin ~10. Critic's #1: winning the beam is too cheap. |
| **v0.2** | **loser of the beam picks the ship first** (winner still steers the Tide) | **No dominant line** — field within ~13–16 pts of 50%; margin ↓ to ~6; Tide decides ~26%; a rule-aware **`grabber`** (bid low to grab ships) **leads at 58.7%**. Critic re-check found the *successor* issue: `grabber` is a one-liner and the **Tide goes dormant** in skilled mirror play (see below). |
| **v0.3** | **Tide bonus scales with how far you push it** (`2 × |position|`, was flat 3) | Top four lines now within **3 pts** across *different* approaches (contest-Tide `always_high` 54%, `hand_smart` 54%, `grabber` 53%, `tide_racer` 51%); pure grabbing (`always_low`) falls to 45%. In grab-vs-contest the **Tide is decisive in ~56%** of games, margins ~3 (very close). The Tide is finally part of optimal play. New watch-item: draw rate rose (~21% in that matchup). |

## Re-run A/B (post-system-upgrade) — runs, set-steering & the Tide
Re-ran the loop with the upgraded system + two sim-only knobs (`BEACON_RUN_BONUS`, `BEACON_PICK`),
n=1000/matchup. New, data-backed findings:
- **The Run bonus is input-luck noise that *compresses* skill.** Turning runs **off** widens the field
  from ~10pt spread to ~35pt (hand_smart 54→**68%**, grabber 52→**60%**, reactive 46→33). So runs were
  dragging good and bad lines toward the middle — random scoring masking skill. **Cut runs** (elegance's
  candidate) — but note it then nudges `hand_smart` toward dominance, so watch it after cutting.
- **Set-steering barely matters.** Picking for convoys vs pure value (`BEACON_PICK=value`) changes almost
  nothing (hand_smart 54.9 vs 54.2; margin 6.04 vs 6.0). So the set-collection layer is **largely
  decoration, not a decision** in the current model → supports simplifying it (cut runs; reconsider how
  much convoys should be worth / whether they're a real choice).
- **The Tide may have over-corrected.** v0.3 made it decisive in ~56% of grab-vs-contest games (up to
  6 VP/Night) — a signature flipping >half of games risks making ships/sets decoration; pairs with a
  high **draw rate** (~13% field-wide, ~21% in grab-vs-contest — a feel-bad for a filler with a weak
  tiebreak). Candidate: dial `TIDE_MULT` 2→~1.5 or cap the bonus, and add a cleaner tiebreak. *Test with
  humans before tuning further — the sim can't judge the feel.*

## What v0.2's diagnostic (iteration 2) proved
The critic asked us to measure before changing rules. It was right:
- **No cleverer line beat `grabber`** (57.7%); `hand_smart` 53.8%, `tide_racer` 48.8% — the optimum was a memorizable one-liner.
- **`grabber`-vs-`grabber` mirror:** `round_ties = 12/12`, `tide_points_total = 0`, `nights_tide_centered = 3/3` — the Tide never moved and the first-keeper token + deck luck decided everything (margin ~15.6). The signature mechanic was dead at equilibrium → drove the v0.3 fix.

**Verdict & honest caveats.** v0.3 makes the Tide load-bearing and restores a real *grab-or-contest*
fork (co-viable pure strategies → humans must read/mix). **Two caveats the sim itself flags:**
(1) the `grabber` mirror *still* ties every round — but that's inherent to two **identical deterministic**
bots in a simultaneous game, **not** proof of shallowness; the depth signal is that no pure line
dominates and opposite approaches tie at ~50%. (2) v0.3 raised the **draw rate** — the next thing to
tune (a tie-breaker or scoring nudge). **The honest next step is a human playtest** — the sim can rule
out broken math and dead mechanics, but only humans can tell us whether the blind read is *fun*.

---

## v0.1 baseline findings (historical)

## What the sim answered

**Q1 — Is a fixed signal policy dominant?** *Partly — and it's a yellow flag.*
- Top three policies cluster tight: `always_high` 66.7%, `hoarder` 65.0%, `reactive` 63.0%, and they
  beat each other in a **soft rock-paper-scissors** (e.g. hoarder > reactive, reactive ≥ always_high in
  one seating). `always_low` is a **trap** (11.7%). So there's *some* depth — no policy crushes all
  others — but **"just play your highest light" is tied for best**, which suggests the rules don't
  punish greedy high-play enough.

**Q2 — How swingy?** *Moderately lopsided.* Average win margin ≈ **10 points** (on ~30-point games) and
tie rate is only ~4%. Games aren't nail-biters on average — worth watching in real play.

**Q3 — Does the Tide bonus decide games?** *Yes, ~16% of the time* (`tide_decisive ≈ 0.157`), averaging
~5 Tide points/game. That's a **well-judged catch-up lever** — it matters without dominating.

## Design responses to test next (one at a time)
1. **Add a cost to winning the beam** so `always_high` isn't free — e.g. the beam winner discards/【burns】
   their played Signal for longer, or the Tide winner reclaims fewer signals. Re-sim to see if the top
   cluster tightens toward 50%.
2. **Tighten swinginess** — try the convoy/run bonuses doing more work, or reduce ship-value spread.
3. Keep the Tide bonus roughly as-is (it's pulling its weight).

## Honest caveat
The sim uses **fixed policies + a shared greedy ship-pick**, with **no bluffing or adaptation** — exactly
the human layer Beacon is built around (reading your opponent before you commit). So these numbers are a
**floor on depth, not a ceiling**: they catch degenerate lines and gross imbalance, but real 2-player
reads will add tension the bots can't model. Treat this as "the math isn't broken and here's the risk to
watch," then confirm with the session-1 human playtest.
