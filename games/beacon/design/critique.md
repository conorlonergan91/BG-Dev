# Beacon — Design Critique (red-team)

*Output of the `bg-critic` stage. Judged against the designer's goals (elegance, tension-with-warmth,
2p). Uses the sim evidence in `playtests/sim-notes.md`.*

## Top risks (ranked)

1. **Winning the beam is too cheap → "always play high" is tied-for-best.** *Why it matters:* the whole
   game is the blind commit; if the greedy line (spend your highest light) is never punished, the
   read-your-opponent depth the design promises is undercut, and elegance turns into a solved reflex.
   *Evidence:* sim has `always_high` at 66.7%, tied top. *Probe:* add a cost to winning (beam winner's
   Signal stays spent longer, or Tide winner reclaims fewer) and re-sim — success = the top cluster
   compresses toward ~50% and `reactive`/`hoarder` overtake pure high-play.

2. **Swinginess / lopsided games.** *Why it matters:* a cozy-tense 2p filler should stay close to the
   end; avg margin ~10 on ~30-point games suggests it can feel decided early. *Probe:* watch margins in
   session 1; if lopsided, let the convoy/run bonuses (comeback-friendly, skill-based) carry more weight
   and compress ship-value spread.

3. **Is the fun actually there for a blind-commit core?** *Why it matters:* blind simultaneous selection
   can read as "we both shrug and flip" if players can't form reads. The Tide + 3-Night structure must
   make earlier commits *inform* later ones. *Probe:* the pre-registered session-1 question — do players
   have "I should have read that" moments, or does it feel like a coin flip? If the latter, add a small
   information lever (e.g. see one upcoming ship).

## Smaller issues
- **Set bonuses may be overhead.** Convoy + run bonuses add scoring steps; if players ignore them, they
  cost elegance for nothing. Test with them off (already question #3 in the design doc).
- **"Loser still takes a ship" is gentle** — denial tension is low; the optional Rocks variant exists to
  dial it up if games feel too friendly.
- **Ship-pick isn't a player decision in the sim** (shared heuristic). In the real game, *which* of the
  two ships the winner takes is a genuine decision — make sure the rulebook makes that choice feel
  meaningful (set-completion vs raw value).

## What's working (don't "fix" these away)
- **The Tide bonus is well-tuned** — decides ~16% of games: a real catch-up lever that doesn't dominate.
  Leave it roughly as-is.
- **`always_low` is correctly a trap**, and the top strategies form a soft rock-paper-scissors — there
  *is* a decision space; it just needs the greedy line taxed.
- **Elegant footprint** — 36 cards + a track hits the 20-minute-filler brief cleanly.

## Decision for the human
Pick the first change to test: **(A)** add a cost to winning the beam (addresses the #1 risk — my
recommendation), **(B)** run session 1 as-is to feel whether the blind commit is fun before tuning, or
**(C)** try the game without set bonuses to test for elegance. All are cheap; (A) then a re-sim is the
tightest loop.
