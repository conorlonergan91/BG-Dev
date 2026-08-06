# tools/sim — playtest simulator

Encode a game's rules once, then play it thousands of times to expose dominant strategies, balance
problems, score spreads, and how often a subsystem decides the game — **before** human playtesting.
Stdlib-only (no dependencies).

## Use it
```bash
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --n 3000 \
    --out games/<slug>/playtests/sim-results.md
```

## Write a game module
Create `games/<slug>/sim/<slug>.py` exposing:
- `GAME` — an object implementing the **Game protocol** (see `engine.py` docstring):
  `new_state · players · actors · legal_actions · step · is_over · scores` (+ optional `view`, `metrics`).
- `STRATEGIES` — `{name: agent}` where an agent is `agent(view, player, legal_actions, rng) -> action`.
- `TITLE` — optional.

`games/beacon/sim/beacon.py` is a complete worked example. `metrics()` is where you answer design
questions (e.g. Beacon reports `tide_decisive` — how often the Tide bonus flips the winner).

## What you get
- **Overall win rate** per strategy (both seatings averaged; ties = 0.5).
- A **matchup grid** (rock-paper-scissors among strategies is a good sign; one strategy at ~100% is a
  red flag).
- **Averaged metrics** you define (margins, decisive-subsystem rates, …).

## Read it right (limits)
Fixed/scripted strategies are a **floor on depth, not a ceiling** — they catch degenerate lines and
gross imbalance but can't model human reads/bluffing. Use the sim to *rule things out* and target
human playtests, not to declare a game "balanced". `bg-playtest` owns this loop.

- The round-robin report ends with an auto **Health read** (dominant line? naive winner? intransitive
  = depth?). Don't stop at raw win rates.
- **Probe targeted matchups** with `--matchup A:B`, especially the strongest line's **mirror** — field
  averages are inflated by weak bots.
- **Seat balance per player count** with `--counts "2,3,4" --agent <line>` — flags any count where a
  seat/turn-order wins far more than its fair share. No offered count should be garbage; if one is
  unfixable, cap the range (see `knowledge/simulation-and-balance.md`).
- **Full method + how to read every signal:** `knowledge/simulation-and-balance.md`.
