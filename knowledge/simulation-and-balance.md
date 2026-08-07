# Simulation & Balance Playbook

How to use `tools/sim/` to pressure-test a design *before* human playtests, and how to read the
results honestly. Distilled from the Beacon design→critic→simulate→tune loop (see
`games/beacon/playtests/sim-notes.md` for the worked example). Owned by `bg-playtest`; `bg-critic`
writes probes against it.

## The loop
**design → critic → simulate → tune → re-sim**, one change at a time. The critic names risks and a
*probe* for each; most probes are "simulate this and report metric X". Simulate, read the signals
below, apply the smallest fix, re-sim to confirm — then hand the questions the sim *can't* answer to a
human playtest.

> **The simulation gate — sim only on the CD's explicit go.** A full run is slow (many minutes) and is
> pure waste if the human still has design notes to fold in. So the sim stage is **gated by the Creative
> Director's explicit approval**: after a design pass + the cheap guardian sweep, the design is presented
> for sign-off with every queued note incorporated, and **only an explicit "sim it" starts the run**.
> Silence or a general "sounds good" is not sim approval. If the human then changes something, re-confirm
> before re-simming. (Cheap checks — the linter, complexity/access gauges, quick EV/probability
> sanity-scripts — are *not* gated; only the model-a-thousand-games runs are.) See the "simulation gate"
> in the `board-game-studio` skill for the full protocol.

## 1. Instrument the design's questions as metrics
Don't eyeball win rates — put each open question into the game's `metrics()` so the sim answers it
directly. On Beacon the open questions became:
- `tide_decisive` — how often the Tide bonus flips the winner (is the signature mechanic load-bearing?)
- `round_ties`, `nights_tide_centered` — does the mechanic go dormant under strong play?
- `margin`, `tie` — how swingy / how close are games?
Pattern: **every "we're not sure if X matters" → a metric.**

## 2. Build a strategy library (naive baselines + rule-aware lines)
Include, at minimum:
- **Naive baselines**: `random`, `always_min`, `always_max` (or `always_high`/`always_low`).
- **Rule-aware lines**: strategies that actually try to exploit the current rules.
A healthy game: **rule-aware lines beat the naive baselines, but no single line beats everything.**

## 3. Read the health signals (the sim prints these automatically now)
The round-robin report ends with a **Health read**:
- **⚠ dominant strategy** (a Condorcet winner that beats every other line by wide margins) → a degenerate
  optimum. This is the #1 thing to fix. *(Beacon v0.1: `always_high` at 66.7%.)*
- **⚠ a *naive* line tops the field** → the interesting decisions don't matter yet.
- **✓ intransitive (rock-paper-scissors)** among the good lines → real depth; no single answer.
- **✓ the field leader is a *rule-aware* line, not a baseline** → skill is being rewarded.
- **Watch for a memorizable one-liner**: even a non-dominant leader is a smell if the best line is a
  single sentence ("bid min on a 3/4, else max"). Depth should need *reading the opponent*, not a rote rule.

## 4. Don't trust field averages — probe targeted matchups
Field-wide metrics are inflated by weak bots. Use `simulate.py --matchup A:B` to inspect specific
pairings, especially:
- **Mirror matches** (`A:A`) of the strongest line — this is where a design collapses if it's going to.
  *(Beacon: `grabber` vs `grabber` showed the Tide never moved — `tide_points_total = 0`, all 12 rounds
  tied — invisible in the field average.)*
- **The interesting fork** (e.g. grab-vs-contest) — confirm the signature mechanic is active and decisive
  there.

## 5. The deterministic-mirror caveat (important)
Two **identical, deterministic** strategies **always mirror-tie** every round in a simultaneous-reveal
game — the pure function returns the same move for both, so nothing separates them but luck. **This is
an artifact of scripted bots, not proof the game is shallow.** Read depth from:
- **cross-strategy** results (do different approaches trade wins?), and
- whether the **optimal line uses the signature mechanic** (if the best pure strategy ignores your
  centrepiece, that's the real smell — fix that, not the mirror).
Humans randomize and read; the sim can't model that. Which is why:

## 6. Know what the sim *can't* tell you → hand to humans
The sim rules out broken math, dominant lines, and dead mechanics. It **cannot** judge:
- whether the core decision is *fun* or just a shrug,
- teachability / whether a rule fights intuition,
- table feel, downtime, social dynamics, the "we almost made it" ache in co-op.
Those are the human session-1 questions. Simulate to *de-risk and target* playtests, never to replace them.

## 7. Beyond balance: instrument decision quality, randomness & the tension curve
Win-rates prove *fairness*; they say nothing about whether the decisions are *interesting*. A game can be
perfectly balanced and perfectly boring (flip a coin). Add these reads via `metrics()` so the sim answers
"is the fun there?", not just "is it fair?":

- **Live-decision density.** The single best proxy for Sid Meier's "a series of interesting decisions".
  For each turn, count the actions within X% (say 10%) of the best action's value by the agent's own
  heuristic. **>1 = a live decision; exactly 1 = a dead/obvious turn.** Report the fraction of turns that
  are live. A game where most turns have one clearly-best move is a solved puzzle wearing a game's clothes —
  it fails even at 50% win-rate. (Catches dead turns, false choices, and no-brainers that balance hides.)
- **Input vs. output randomness classification.** Tag each random subsystem: does the randomness resolve
  **before** the decision (input — you adapt; preserves agency) or **after** (output — swing, "I played
  perfectly and lost"). Measure output-luck's bite: correlation between a random draw/roll *after* commit
  and the game result. High output-luck decoupling outcome from decision quality is a design smell — and
  it's directly counter to the house value "input randomness, not output". Cheap, high-signal, rarely
  automated.
- **Tension curve / late-game decidedness.** Track the leader's win-probability (or score margin) over the
  course of a game. **Is the winner effectively decided before the final rounds?** For this studio's
  tug-of-war duels and the co-op "we almost made it" ache, the *most interesting decision should be near
  the end* and the winner in doubt late. If the sim shows games settled at 60% distance, the back half is
  dead air — a pacing failure no win-rate reveals. (Metric ideas: `lead_locked_round` = the round after
  which the eventual winner never trails; `final_margin` distribution; fraction of games decided in the
  last round.)

These are `bg-critic`'s probes made quantitative — the critic names the risk ("turn 3 is a no-brainer";
"the reveal is pure output swing"; "it's over by the midpoint") and points here for the metric that
confirms it. Bots are a **floor**: they can prove a turn is dead or a game is decided early; they can't
prove a live decision is *fun*. That last step is still the human session.

## Test every player count & variant (not just the sweet spot)
A game offered at 2–5 players is really several games. Test them all — in sim and with humans:
- **Seat balance per count:** `simulate.py --counts "2,3,4,5" --agent <line>` self-plays a strategy at
  each count and reports each **seat's win rate** vs its fair share (1/n). A seat winning ≥1.5× or ≤0.5×
  fair is flagged **⚠ suspect** — usually a turn-order/first-player problem. (Needs a game whose
  `new_state(rng, n_players)` parametrises count; fixed-count games report that cleanly.)
- **Variants/modes** get the same treatment — run the round-robin (and mirror probes) per active variant.
- **It needn't be perfect at every count — but never garbage at any offered count.** If a count is weak
  but fixable, fix it. **If it's irredeemable, cap the player range** ("2–3, not 2–5") or rework the
  offending part. A narrower range done well beats a wide one done badly — the goal is the *best game*,
  not the longest count list. `bg-playtest` owns this call; `bg-critic` flags the mismatch.
- The sim measures *balance*; **playtime, downtime, and the social feel per count** are human-session
  observations (see `design-fundamentals.md` → Social axis).

## Quick commands
```bash
# full tournament + health read
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --n 3000 --out games/<slug>/playtests/sim-results.md
# probe a specific matchup (esp. the strongest line's mirror)
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --n 2000 --matchup best:best
# seat balance across player counts (multi-count games)
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --counts "2,3,4" --agent <line>
```
Write the *interpretation* (findings + the one change to test) in `playtests/sim-notes.md`, separate
from the auto-generated `sim-results.md`.
