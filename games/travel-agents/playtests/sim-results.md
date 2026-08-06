# Travel Agents: Taiwan — simulation report

1000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **hoarder         **  67.9%  ████████████████████
- **assignment      **  64.8%  ███████████████████
- **dossier_greedy  **  52.1%  ████████████████
- **balanced        **  52.0%  ████████████████
- **generous        **  51.5%  ███████████████
- **random          **  11.8%  ████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | hoarder | generous | balanced | assignment | dossier_gr |
|---|---|---|---|---|---|---|
| random |   49% |    5% |    4% |    4% |    4% |    5% |
| hoarder |   96% |   48% |   73% |   73% |   51% |   70% |
| generous |   96% |   34% |   54% |   51% |   37% |   54% |
| balanced |   97% |   31% |   57% |   52% |   31% |   56% |
| assignment |   96% |   48% |   65% |   69% |   50% |   64% |
| dossier_gr |   96% |   30% |   55% |   51% |   41% |   53% |

## Averaged game metrics
- margin: 8.677
- tie: 0.111
- deaddrops_per_game: 2.683
- plates_per_player: 5.634
- turns: 36.803
- dossier_end: 13.951
- winner_pick_share: 0.501
- milestone_picks_total: 3.129
- vp_pick_decisive: 0.020
- assign_done_rate: 0.662

## Health read
- ~ mild edge to `hoarder` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
