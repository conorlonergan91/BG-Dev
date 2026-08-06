# {{TITLE}} — Product Overview

> The **whole-product** view: the base game plus every expansion and distinct mode, seen together.
> Create this (from `templates/product.md`) once a game grows beyond a single base — `bg-architect`
> owns it. A focused single game doesn't need it; `game-bible.md` is enough. Don't add scope to fill
> this in (restraint) — list only what genuinely exists or is committed to.

## What it is
<!-- One-liner for the whole line. -->

## Series
<!-- If part of a series of standalone products: the series slug + link to series/<name>.md. Else "standalone". -->

## Modules
| Module | Kind | Status | Folder | Own bible |
|--------|------|--------|--------|-----------|
| Base | base game | <!-- e.g. shipping / in design --> | `./` | `game-bible.md` |
| <!-- e.g. Ports & Cargo --> | expansion | | `expansions/<slug>/` | `expansions/<slug>/expansion-bible.md` |
| <!-- e.g. Solo --> | mode | | `modes/<slug>/` | `modes/<slug>/…` |

## Combined view (base + everything)
- **Total components / new-per-module:** <!-- reuse map; keep new components minimal -->
- **Combined complexity:** <!-- base budget + each module's combined-with-base budget; watch creep -->
- **Plays well SEPARATELY:** <!-- base alone, each mode alone — status + last check -->
- **Plays well COMBINED:** <!-- base + expansion(s) together — status, power-creep watch, last sim/playtest -->

## Build history
<!-- Snapshots live in builds/ ; see builds/BUILDS.md. Cut a build at each known-good state. -->

## Open architecture decisions
<!-- e.g. "campaign in base or expansion 2?"; keep in sync with decision-log.md -->
