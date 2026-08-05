# Beacon — Design Doc

*Output of the `bg-design` stage. First-pass numbers — the point of playtesting is to tune these.*

## Design goals
A 20-minute 2-player duel whose single meaningful decision each round is **"which Signal do I commit,
blind?"** — with a visible Tide that makes each commit matter beyond one ship. Depth from simple rules;
all **input** randomness (which ships appear), **no output** randomness.

## Core loop (detailed)
Reveal ships to the Channel → both players simultaneously commit one Signal face-down → reveal →
higher Signal wins the **beam** (move the Tide 1 step toward them + first pick of a Channel ship);
loser takes the other → refill the Channel → repeat.

## Structure of play — 3 Nights
- The game is **3 Nights**. Each Night uses an **8-card Night deck** (deal the 24-card Ship deck into
  three face-down stacks of 8).
- Each Night: reveal a **Channel of 2** ships. Play **4 rounds**; refill the Channel to 2 after each.
- Each Night both players hold their **full hand of 6 Signals** (0–5) and will commit **4** of them —
  so you **hold back 2**. *Which 4 you commit, and in what order, is the game.*

## A round
1. Both players secretly choose 1 Signal and reveal simultaneously.
2. **Higher Signal wins the beam:** move the Tide marker **1 space toward the winner**; the winner
   **picks either Channel ship** into their Harbour; the loser takes the remaining one.
3. **Tie:** Tide does not move; the current **first keeper** picks first, then the other.
4. Spent Signals are set aside for this Night. Refill the Channel to 2.

## End of a Night
- **Tide bonus:** whichever side the Tide marker is on scores **+3 VP** (dead centre = no one).
- **Reset:** Tide returns to centre; both players take all Signals back to hand.
- **The tide turns (catch-up):** the player who **lost the Tide** (or, if centred, the player with fewer
  ships) becomes **first keeper** for the next Night — initiative as a comeback lever.

## Components
| Component | Qty | Notes |
|-----------|-----|-------|
| Ship cards | 24 | 3 suits (Cargo/Passenger/Naval) × values 1–4, two of each value per suit |
| Signal cards | 12 | two identical sets of 6 (values 0–5), one set per player |
| Tide track + marker | 1 + 1 | 7 spaces (−3…+3), marker starts centre |
| Harbour zones | 2 | one per player (scoring area) |
| First-keeper token | 1 | initiative marker |

## Economy & math (first pass)
- Ship value in deck: each suit = 1,1,2,2,3,3,4,4 (sum 20) → **deck total 60 VP** of ships.
- Per Night 8 ships (~20 VP) are claimed; over 3 Nights all 24 ships go to a Harbour (none lost in the
  base game). So ~**30 VP of ships each** on average — the *skill* is grabbing the 3s/4s and completing
  sets while stealing the Tide.
- Signals 0–5: committing your **5** wins a beam but burns your best card; the **0** is a deliberate
  "sacrifice this ship to bait/save big Signals" play. Holding 2 of 6 each Night = the bluff space.
- Tide: 4 rounds/Night, so the Tide can reach at most ±4 but track caps ±3; +3 VP/Night × 3 = up to
  9 VP swing from Tide — deliberately large enough to fight over, small enough not to dominate ships.

## Scoring / win condition
Total VP = **ship values** + **set bonuses** + **Tide bonuses**.
- **Convoy bonus:** each complete set of {1 Cargo + 1 Passenger + 1 Naval} = **+2 VP**.
- **Run bonus:** each 3 consecutive values in one suit (e.g. Cargo 2-3-4) = **+2 VP**.
Highest total wins; tie → most **Naval** ships; still tied → shared win.

## Randomness
Input only: ship reveal order + your opponent's hidden choice. No dice, no post-decision luck.

## Interaction & tension
Direct and constant (every round is a head-to-head commit). Catch-up via the Tide bonus + initiative
handoff prevents a runaway leader — key for 2p.

## Player counts & scaling
Strictly 2. (A 3–4p "harbour rush" variant is possible later but out of scope.)

## Solo mode / Automa
Not for v1 (it's a duel). A simple "Lighthouse automa" that commits a Signal by a face-up rule could
come later.

## Complexity budget
Target weight ~1.8. Everything above fits on a 1-page rules sheet + a player-aid card. If the set
bonuses feel like too much, the first cut is the **run bonus** (keep convoys).

## Keywords / glossary
**Channel** (face-up ship row) · **Beam** (winning the higher Signal) · **Tide** (the tug-of-war track)
· **Harbour** (your claimed ships) · **Keeper** (player) · **First Keeper** (initiative).

## Open questions for playtesting
1. **Depth of blind commit:** does reading your opponent reward skill over 3 Nights, or feel random?
2. **Signal economy:** is "commit 4, hold 2 of 6" the right ratio? Try 5-of-7 or reclaim rules.
3. **Set bonuses:** do convoy/run bonuses add meaningful direction, or just scoring overhead? Test
   without them.
4. **Denial:** is "loser still takes a ship" too gentle? Test the optional **Rocks** variant (Channel
   of 3, winner + loser take one, third is lost).
