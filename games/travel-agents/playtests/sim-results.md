# Travel Agents: Taiwan (v3 vendor-courting engine) — simulation report

600 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **buzz_heavy      **  62.1%  ███████████████████
- **ingredient_heavy**  62.0%  ███████████████████
- **reputation_climb**  60.7%  ██████████████████
- **mission_focus   **  60.3%  ██████████████████
- **balanced        **  59.0%  ██████████████████
- **prestige_rush   **  58.6%  ██████████████████
- **coverage_spread **  55.7%  █████████████████
- **random          **  19.4%  ██████
- **greedy_cheap    **  12.3%  ████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_che | balanced | prestige_r | reputation | coverage_s | buzz_heavy | ingredient | mission_fo |
|---|---|---|---|---|---|---|---|---|---|
| random |   48% |   41% |   11% |   12% |   11% |   11% |   18% |   11% |    9% |
| greedy_che |   58% |   48% |    0% |    0% |    0% |    1% |    0% |    0% |    0% |
| balanced |   89% |  100% |   48% |   51% |   46% |   53% |   44% |   46% |   50% |
| prestige_r |   91% |   99% |   46% |   51% |   48% |   52% |   46% |   44% |   53% |
| reputation |   91% |  100% |   49% |   51% |   49% |   56% |   43% |   46% |   52% |
| coverage_s |   89% |   99% |   49% |   49% |   41% |   48% |   38% |   41% |   41% |
| buzz_heavy |   80% |  100% |   51% |   54% |   52% |   56% |   52% |   50% |   54% |
| ingredient |   88% |  100% |   55% |   52% |   51% |   59% |   48% |   50% |   52% |
| mission_fo |   88% |  100% |   54% |   57% |   47% |   56% |   44% |   50% |   50% |

## Averaged game metrics
- margin: 14.958
- tie: 0.082
- turns: 84.351
- total_courts: 8.489
- courts_per_player: 4.244
- court_interval: 23.112
- court_interval_late: 2.994
- min_court_gap: 2.128
- mid_leader_won: 0.703
- stuck_turns: 0.000
- overflow_discards: 110.514
- buzz_spent: 18.497
- region_ing_spent: 10.313
- win_prestige: 17.492
- win_rep_vp: 7.315
- win_cov_vp: 6.343
- win_mission: 0.666
- end_by_rep: 0.814
- end_by_season: 0.000
- end_by_extract: 0.172

## Health read
- ~ mild edge to `buzz_heavy` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
