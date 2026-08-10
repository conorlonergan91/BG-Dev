# 📋 <GAME NAME> — Status (current state of play)

> **The live dashboard.** Owned by `bg-producer`. Always reflects the CURRENT version — readable in under a
> minute. If you want the *why* behind a decision, see `decision-log.md`; the *history* lives in `archive/`;
> the CD's own steers live in `director-brief.md`. This doc answers only: **where are we right now?**
> _Last updated: <date> · by <who>_

## Version
- **Current:** `<vX.Y>` — *<one line: what this version IS>*
- **Shipped / frozen builds:** *<latest known-good build snapshot, if any>*

## Pipeline stage
*<Where in the arc: ideation · design · development · prototype · playtest · funding · marketing · publishing ·
production. One line on what stage the game is actually in.>*

## Done · In-flight · Next
- **✅ Done (this version):** *<the landed milestones>*
- **⏳ In-flight:** *<what's actively being worked, and by whom/what>*
- **➡️ Next:** *<the next real step>*

## Open decisions (waiting on the Creative Director)
*<Each a crisp question the CD can answer fast. Empty = nothing blocking.>*
- [ ] *<decision — options / recommendation>*

## Guardrail health
| Gauge | State |
|---|---|
| Lint (`check_game.py`) | *<0 errors / the flag>* |
| Complexity (`check_complexity.py`) | *<in-budget / over on X>* |
| Accessibility (`check_access.py`) | *<pass / flag>* |
| Cost (`check_cost.py`) | *<in-budget / n/a>* |
| Simulation | *<last read: balanced? / n/a>* |

## Risks · watch-items
*<Known risks, fragile assumptions, things to watch at the table. Include anything consultant-gated.>*

## Next real step
*<The single most important next action, and whose call/turn it is.>*
