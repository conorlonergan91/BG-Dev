# Travel Agents: Taiwan (v6.3.1 — four CD reworks: home-region 里長伯 · Maintenance · Taipei start · night curve) — simulation report

1200 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **mix             **  61.8%  ███████████████████
- **greedy_book     **  61.6%  ██████████████████
- **balanced        **  61.3%  ██████████████████
- **opportunistic   **  61.0%  ██████████████████
- **disruptive      **  61.0%  ██████████████████
- **ignore_obj      **  58.1%  █████████████████
- **no_drinks       **  57.0%  █████████████████
- **endgame         **  55.2%  █████████████████
- **pure_drinks     **  14.4%  ████
- **random          **   8.6%  ███

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_boo | balanced | opportunis | disruptive | endgame | mix | ignore_obj | pure_drink | no_drinks |
|---|---|---|---|---|---|---|---|---|---|---|
| random |   52% |    0% |    0% |    0% |    0% |    1% |    0% |    2% |   28% |    4% |
| greedy_boo |  100% |   51% |   49% |   53% |   50% |   59% |   49% |   58% |   98% |   53% |
| balanced |  100% |   49% |   52% |   49% |   50% |   58% |   49% |   57% |   97% |   48% |
| opportunis |  100% |   49% |   51% |   51% |   50% |   57% |   48% |   56% |   97% |   53% |
| disruptive |  100% |   49% |   49% |   51% |   50% |   57% |   46% |   57% |   97% |   50% |
| endgame |   99% |   45% |   42% |   44% |   43% |   48% |   43% |   45% |   96% |   49% |
| mix |  100% |   49% |   48% |   50% |   50% |   59% |   50% |   56% |   97% |   52% |
| ignore_obj |   99% |   44% |   40% |   44% |   41% |   51% |   42% |   57% |   98% |   68% |
| pure_drink |   72% |    3% |    3% |    3% |    3% |    4% |    2% |    2% |   33% |    3% |
| no_drinks |   97% |   50% |   47% |   46% |   46% |   56% |   47% |   33% |   97% |   44% |

## Averaged game metrics
- margin: 12.466
- tie: 0.005
- turns: 62.055
- turns_per_player: 31.028
- food_wins: 7.136
- drink_wins: 1.883
- wins_per_player: 4.509
- drink_win_share: 0.222
- contested_wins: 0.443
- contested_frac: 0.053
- max_buzz_on_vendor: 3.480
- max_committed: 3.722
- buzz_supply_min: 17.577
- star_placed: 1.138
- star_wins_total: 0.453
- dusk_turn: 29.866
- last_turn: 58.382
- first_night_win_turn: 41.294
- end_by_lasttrain: 0.644
- end_by_deck: 0.000
- end_by_stall: 0.356
- travels_per_game: 13.371
- inter_moves: 13.371
- visits_per_game: 14.826
- cstores_per_game: 4.781
- promotes_per_game: 11.805
- passes_per_game: 0.000
- claim_share_N: 0.490
- claim_share_C: 0.185
- claim_share_S: 0.184
- claim_share_E: 0.137
- src_share_N: 0.270
- src_share_C: 0.132
- src_share_S: 0.264
- src_share_E: 0.167
- src_share_common: 0.167
- avg_legal_actions: 9.606
- forced_turn_frac: 0.000
- events_fired_per_game: 17.567
- scope_self_frac: 0.516
- scope_region_frac: 0.327
- scope_neigh_frac: 0.145
- takethat_hits_per_game: 2.406
- cs_rival_hits_per_game: 0.232
- empty_draws_per_game: 0.336
- claims_per_game: 8.254
- reach_start: 2.000
- reach_blocked_per_game: 2.015
- reach_gain_travel: 13.059
- reach_gain_event: 2.592
- reach_gain_ms: 1.431
- reach_loss_grab: 3.349
- reach_loss_event: 2.815
- reach_forced_return: 0.045
- greedy_visit_per_game: 2.859
- greedy_cs_per_game: 0.490
- greedy_grab_per_game: 3.349
- reach_zero_turns: 0.397
- reach_mean_all: 4.496
- reach_at_dusk_mean: 3.861
- reach_end_mean: 7.459
- ms7_fired: 0.911
- ms14_fired: 0.835
- ms_both_fired: 0.835
- ms_both_same_player: 0.727
- ms_both_same_given_both: 0.727
- ms7_earn_players: 1.443
- ms14_earn_players: 1.145
- src_day_per_turn: 0.455
- src_night_per_turn: 0.497
- night_day_src_ratio: 1.207
- night_claims_per_player: 2.089
- night_food_wins_per_player: 1.732
- free_bribes_per_game: 1.759
- free_night_bribes_per_game: 0.712
- turns_night_frac: 0.510
- maint_seeded_per_game: 0.932
- maint_fired_per_game: 0.166
- maint_fired_rate: 0.166
- maint_closed_turns_per_game: 0.160
- councillor_home_bribes: 0.000
- councillor_away_bribes: 0.000
- councillor_away_frac: 0.000
- home_pick_N: 0.000
- home_pick_C: 0.000
- home_pick_S: 0.000
- home_pick_E: 0.000
- win_bookings: 21.781
- win_ticket_score: 11.943
- win_total: 11.943
- tickets_held_winner: 2.381

## Health read
- ✓ **no single dominant line** — strategies are intransitive (rock-paper-scissors). A good depth signal.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
