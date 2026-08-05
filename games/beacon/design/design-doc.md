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

## A round  *(v0.2 — see "Design history" below)*
1. Both players secretly choose 1 Signal and reveal simultaneously.
2. **Higher Signal wins the beam:** move the Tide marker **1 space toward the winner**. **But the keeper
   who held back (the *lower* Signal) picks a Channel ship first**; the beam winner takes the other. You
   can't grab position *and* cargo in the same round — bright light steers the Tide, a dim light snatches
   the ship in front of you.
3. **Tie:** Tide does not move; the current **first keeper** picks first, then the other.
4. Spent Signals are set aside for this Night. Refill the Channel to 2.

## End of a Night
- **Tide bonus (v0.3):** whichever side the Tide marker is on scores **2 VP per space from centre**
  (so a decisive Tide is worth up to 6; dead centre = no one). Scaling it (vs a flat +3) is what makes
  a voluntary high bid a live choice rather than a wasted turn — see the design history.
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
1. **Depth of blind commit:** ~~does reading your opponent reward skill?~~ *Simulation (v0.2) supports
   "yes": a rule-aware line beats naive ones ~59% vs ~42–54%, no dominance. Confirm the feel with humans.*
2. **Signal economy:** is "commit 4, hold 2 of 6" the right ratio? Try 5-of-7 or reclaim rules.
3. **Set bonuses:** do convoy/run bonuses add meaningful direction, or just scoring overhead? Test
   without them.
4. **Does anyone ever want the Tide?** *Addressed in v0.3 (scaled Tide bonus) — contesting the Tide is
   now a co-viable line in the sim.* New watch-item from v0.3: the **draw rate** rose (~21% in
   grab-vs-contest); if humans see too many ties, add a tie-breaker or nudge scoring.
5. **Is the blind read actually fun?** The sim can't answer this — it's the whole point of human
   session 1. Do players feel a live "grab or contest?" read each commit, or settle into a shrug?

## Design history
- **v0.1** — beam winner picked the ship *and* moved the Tide toward themselves. Sim: `always_high`
  dominant (66.7%), spread ~55 pts, avg margin ~10.
- **v0.2** — *loser of the beam picks the ship first* (winner still steers the Tide). Sim: no dominant
  line (spread ~13–16 pts), avg margin ~6, Tide decides ~26% of games, and a rule-aware `grabber`
  strategy leads at ~59% (skill rewarded). Big improvement on the #1 critique. *(Loop iteration 1.)*
- **v0.2 diagnostic** — the critic re-checked and the sim confirmed a *successor* problem: `grabber`
  is a one-liner no cleverer line beats, and in skilled mirror play the **Tide is 100% dormant**
  (every round ties, Tide never moves, token/luck decides). *(Loop iteration 2.)*
- **v0.3** — *Tide bonus scales with how far you push it* (`2 × |position|`). Sim: the top four lines
  land within ~3 pts across *different* approaches (contest-Tide, selective-grab, grab, adapt), pure
  grabbing drops to ~45%, and the Tide is decisive in ~56% of grab-vs-contest games — a real
  grab-or-contest fork. Watch-item: draw rate rose (~21%). Next step: **human playtest** (is the read
  fun?). *(Loop iteration 3.)*
