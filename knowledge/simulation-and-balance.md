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

## Quick commands
```bash
# full tournament + health read
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --n 3000 --out games/<slug>/playtests/sim-results.md
# probe a specific matchup (esp. the strongest line's mirror)
python tools/sim/simulate.py --module games/<slug>/sim/<slug>.py --n 2000 --matchup best:best
```
Write the *interpretation* (findings + the one change to test) in `playtests/sim-notes.md`, separate
from the auto-generated `sim-results.md`.
