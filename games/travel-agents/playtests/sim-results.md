# Travel Agents: Taiwan (v6.4b — FOLLOWERS vocab · Bookings hand-limit N=3 · 網紅 start-max 3 · base Travel de-sourced [媽寶 sole sourcer] · Trending +1 Followers-max · run-out-of-stock NIGHT [1/region, stock 2, region shutdown, last-train 9] · 大哥 night win-on-a-tie · +fighter) — simulation report

1000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **fighter         **  60.2%  ██████████████████
- **disruptive      **  60.0%  ██████████████████
- **greedy_book     **  59.9%  ██████████████████
- **balanced        **  59.8%  ██████████████████
- **mix             **  59.7%  ██████████████████
- **opportunistic   **  58.9%  ██████████████████
- **ignore_obj      **  57.5%  █████████████████
- **no_drinks       **  56.8%  █████████████████
- **endgame         **  54.2%  ████████████████
- **collector       **  53.9%  ████████████████
- **pure_drinks     **  12.2%  ████
- **random          **   6.9%  ██

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_boo | balanced | opportunis | disruptive | endgame | mix | ignore_obj | pure_drink | no_drinks | collector | fighter |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| random |   51% |    0% |    0% |    0% |    0% |    0% |    0% |    1% |   30% |    2% |    0% |    0% |
| greedy_boo |  100% |   51% |   54% |   53% |   51% |   59% |   54% |   60% |   98% |   55% |   58% |   50% |
| balanced |  100% |   55% |   52% |   55% |   51% |   59% |   52% |   58% |   98% |   52% |   59% |   49% |
| opportunis |  100% |   50% |   53% |   53% |   51% |   56% |   50% |   58% |   98% |   50% |   60% |   47% |
| disruptive |  100% |   54% |   53% |   51% |   52% |   59% |   54% |   61% |   98% |   53% |   58% |   51% |
| endgame |  100% |   48% |   45% |   48% |   45% |   46% |   45% |   47% |   98% |   48% |   49% |   43% |
| mix |  100% |   52% |   51% |   55% |   48% |   60% |   51% |   59% |   97% |   53% |   58% |   50% |
| ignore_obj |   99% |   43% |   46% |   47% |   49% |   50% |   45% |   53% |   97% |   74% |   51% |   55% |
| pure_drink |   73% |    2% |    1% |    2% |    3% |    2% |    3% |    3% |   32% |    2% |    2% |    2% |
| no_drinks |   98% |   52% |   51% |   52% |   52% |   60% |   53% |   30% |   97% |   48% |   59% |   48% |
| collector |  100% |   46% |   47% |   45% |   48% |   47% |   43% |   46% |   97% |   46% |   44% |   43% |
| fighter |  100% |   53% |   51% |   53% |   53% |   60% |   54% |   52% |   96% |   53% |   60% |   42% |

## Averaged game metrics
- margin: 12.951
- tie: 0.005
- turns: 61.100
- turns_per_player: 30.550
- food_wins: 6.847
- drink_wins: 1.528
- wins_per_player: 4.188
- drink_win_share: 0.191
- contested_wins: 0.509
- contested_frac: 0.066
- max_buzz_on_vendor: 3.770
- max_committed: 3.912
- buzz_supply_min: 17.143
- star_placed: 1.037
- star_wins_total: 0.505
- dusk_turn: 32.039
- last_turn: 57.449
- first_night_win_turn: 42.951
- end_by_lasttrain: 0.698
- end_by_deck: 0.000
- end_by_stall: 0.302
- travels_per_game: 14.785
- inter_moves: 14.785
- visits_per_game: 14.129
- cstores_per_game: 4.107
- promotes_per_game: 11.421
- passes_per_game: 0.000
- claim_share_N: 0.408
- claim_share_C: 0.247
- claim_share_S: 0.165
- claim_share_E: 0.174
- src_share_N: 0.234
- src_share_C: 0.180
- src_share_S: 0.208
- src_share_E: 0.203
- src_share_common: 0.175
- avg_legal_actions: 9.361
- forced_turn_frac: 0.000
- events_fired_per_game: 16.114
- scope_self_frac: 0.519
- scope_region_frac: 0.327
- scope_neigh_frac: 0.146
- takethat_hits_per_game: 2.170
- cs_rival_hits_per_game: 0.187
- empty_draws_per_game: 0.428
- claims_per_game: 8.283
- reach_start: 2.000
- reach_blocked_per_game: 2.553
- reach_gain_travel: 14.245
- reach_gain_event: 2.356
- reach_gain_ms: 1.442
- reach_loss_grab: 4.404
- reach_loss_event: 2.583
- reach_forced_return: 0.057
- greedy_visit_per_game: 3.814
- greedy_cs_per_game: 0.590
- greedy_grab_per_game: 4.404
- reach_zero_turns: 0.394
- reach_mean_all: 4.477
- reach_at_dusk_mean: 4.081
- reach_end_mean: 7.773
- reach_gain_trending: 0.490
- reach_loss_lostwar: 0.000
- followers_gain_total: 18.533
- followers_sink_total: 6.987
- capbind_day: 0.206
- capbind_night: 0.025
- reach_blocked_day: 2.282
- reach_blocked_night: 0.271
- slack_night_mean: 5.071
- capfill_night: 0.083
- capfill_day: 0.199
- lost_wars_per_game: 0.509
- followers_per_lost_war: 1.267
- cancels_per_game: 0.001
- book_capbind_per_game: 0.001
- ms7_fired: 0.922
- ms14_fired: 0.861
- ms_both_fired: 0.861
- ms_both_same_player: 0.717
- ms_both_same_given_both: 0.717
- ms7_earn_players: 1.475
- ms14_earn_players: 1.078
- src_day_per_turn: 0.253
- src_night_per_turn: 0.281
- night_day_src_ratio: 1.298
- night_claims_per_player: 1.765
- night_food_wins_per_player: 1.599
- night_contested_wins_per_game: 0.201
- night_contested_frac: 0.058
- free_bribes_per_game: 1.409
- free_night_bribes_per_game: 0.409
- turns_night_frac: 0.467
- maint_seeded_per_game: 0.938
- maint_fired_per_game: 0.124
- maint_fired_rate: 0.124
- maint_closed_turns_per_game: 0.119
- councillor_home_bribes: 0.000
- councillor_away_bribes: 0.000
- councillor_away_frac: 0.000
- home_pick_N: 0.000
- home_pick_C: 0.000
- home_pick_S: 0.000
- home_pick_E: 0.000
- win_bookings: 18.636
- win_ticket_score: 12.181
- win_total: 12.181
- tickets_held_winner: 2.373

## Health read
- ✓ **no single dominant line** — strategies are intransitive (rock-paper-scissors). A good depth signal.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
