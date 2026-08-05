# Beacon — Simulation findings (interpretation)

Hand-written reading of the auto-generated `sim-results.md` (3000 games/matchup, first-pass rules).
*Regenerate the raw report with:* `python tools/sim/simulate.py --module games/beacon/sim/beacon.py --n 3000 --out games/beacon/playtests/sim-results.md`

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
