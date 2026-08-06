# Beacon — Elegance Review

*Output of the `bg-elegance` stage. Guards the complexity budget, hunts simplifications, reviews
rulebook/aid clarity, and manages FAQ discipline. Gauge: `python tools/complexity/check_complexity.py
--game games/beacon`.*

## Budget status — ✓ within budget
| proxy | value | cap |
|-------|-------|-----|
| rulebook_words | 524 | 900 |
| keywords (glossary) | 6 | 8 |
| exception_words | 0 | 8 |
| component_types | **4** | **4** ← at cap |
| player_aid_lines | 12 | 16 |

Beacon is comfortably at its ~1.8 target — no creep. **One thing to watch:** `component_types` is *at*
its cap (Cargo / Passenger / Naval / Signal). Adding a fourth ship suit or a new card type would breach
the budget → that would need a conscious, logged decision, not a drift.

## Simplification candidates (ranked)
1. **Cut the Run bonus (keep Convoy).** *Recommended.* The critic and the sim both flag it: runs (3
   consecutive values in a suit) aren't steerable — you only pick from the 2 ships in the Channel, so a
   run mostly *happens to you* (input luck), adding a scoring step and a little swing without a decision.
   Convoy ({Cargo+Passenger+Naval}) is steerable and thematically clean ("a balanced harbour"). *What's
   lost:* a bit of scoring variety. *Gain:* one fewer scoring rule, a shorter aid line, less end-game
   arithmetic — pure elegance. *Confirm:* one Night of the next playtest scored without runs; does anyone
   miss them?
2. **Keep the "commit 4 of 6, hold 2" economy.** Not a cut — flagging it as *protected*: it quietly
   forces at least one high bid per Night (so the Tide must move) and creates the bluff space. Don't
   "simplify" it to a smaller hand without re-checking.

## Rulebook & player-aid clarity — good, with one note
- Rulebook is 524 words (well under budget) and teaches in play order — keep it lean as it grows.
- Player aid is 12 short lines — one glance. Good.
- **Clarity risk (from the critic):** v0.3's rule inverts intuition (the *dim* light grabs the ship).
  Already reinforced on the Dark Lantern / Blinding Flare cards and the aid. Add one plain "why" line in
  the rulebook so the inversion lands on first read (done in the FAQ below).

## FAQ (added to the rulebook — kept minimal)
Genuine ambiguities only. If any of these recur in play, that's a signal to fix the rule, not grow the FAQ.
- **Are hands open?** Yes — played Signals are face-up, so both keepers' remaining Signals are known;
  only the current round's choice is hidden. (Non-obvious; worth stating.)
- **Both play the same Signal?** Tie: the Tide doesn't move; the First Keeper picks a ship first, then
  the other. Both still take one.
- **Who is First Keeper on Night 1?** Decided at setup (randomly, or "last to see the sea").
- **Can the Channel fail to refill?** No — each Night's 8 ships divide evenly into 4 rounds of 2, so the
  deck never strands a round in the base game.

## Decision for the human
**(A)** Cut the Run bonus next playtest (recommended — cleanest elegance win, low risk); **(B)** keep both
set bonuses and test whether runs actually get noticed; **(C)** defer — revisit after session 1. I'd take
(A). Either way the FAQ above is added and the budget is green.
