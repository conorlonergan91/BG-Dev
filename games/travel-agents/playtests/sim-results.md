# Travel Agents: Taiwan (v3 vendor-courting engine) — simulation report

500 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **ingredient_heavy**  62.4%  ███████████████████
- **buzz_heavy      **  61.1%  ██████████████████
- **reputation_climb**  60.6%  ██████████████████
- **mission_focus   **  59.9%  ██████████████████
- **balanced        **  59.3%  ██████████████████
- **prestige_rush   **  59.0%  ██████████████████
- **coverage_spread **  56.2%  █████████████████
- **random          **  19.6%  ██████
- **greedy_cheap    **  11.9%  ████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_che | balanced | prestige_r | reputation | coverage_s | buzz_heavy | ingredient | mission_fo |
|---|---|---|---|---|---|---|---|---|---|
| random |   49% |   42% |   11% |   11% |   12% |   11% |   17% |   10% |   11% |
| greedy_che |   55% |   48% |    0% |    0% |    0% |    0% |    0% |    0% |    0% |
| balanced |   88% |  100% |   50% |   49% |   51% |   56% |   46% |   48% |   49% |
| prestige_r |   90% |  100% |   49% |   47% |   53% |   52% |   47% |   48% |   47% |
| reputation |   89% |  100% |   53% |   56% |   52% |   54% |   48% |   49% |   53% |
| coverage_s |   89% |  100% |   44% |   48% |   46% |   54% |   40% |   44% |   44% |
| buzz_heavy |   82% |  100% |   52% |   54% |   50% |   56% |   54% |   47% |   55% |
| ingredient |   89% |  100% |   59% |   57% |   53% |   60% |   49% |   50% |   53% |
| mission_fo |   89% |  100% |   53% |   50% |   48% |   55% |   47% |   49% |   53% |

## Averaged game metrics
- margin: 21.071
- tie: 0.083
- turns: 105.794
- total_courts: 14.089
- courts_per_player: 7.044
- court_interval: 23.177
- court_interval_late: 2.630
- min_court_gap: 1.941
- mid_leader_won: 0.728
- stuck_turns: 0.000
- overflow_discards: 128.413
- buzz_spent: 33.612
- region_ing_spent: 11.613
- win_prestige: 33.512
- win_rep_vp: 7.603
- win_cov_vp: 7.460
- win_mission: 0.792
- end_by_rep: 0.000
- end_by_season: 0.786
- end_by_extract: 0.198

## Health read
- ~ mild edge to `ingredient_heavy` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
