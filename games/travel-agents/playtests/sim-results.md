# Travel Agents: Taiwan (v6.3 — Reach gates Buzz + milestones) — simulation report

1500 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **ignore_obj      **  77.4%  ███████████████████████
- **balanced        **  59.9%  ██████████████████
- **disruptive      **  59.8%  ██████████████████
- **greedy_book     **  59.8%  ██████████████████
- **mix             **  59.3%  ██████████████████
- **opportunistic   **  58.6%  ██████████████████
- **no_drinks       **  58.2%  █████████████████
- **endgame         **  45.7%  ██████████████
- **pure_drinks     **  14.0%  ████
- **random          **   7.2%  ██

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_boo | balanced | opportunis | disruptive | endgame | mix | ignore_obj | pure_drink | no_drinks |
|---|---|---|---|---|---|---|---|---|---|---|
| random |   49% |    0% |    0% |    0% |    0% |    0% |    0% |    0% |   21% |    1% |
| greedy_boo |  100% |   51% |   53% |   51% |   52% |   72% |   53% |   31% |   98% |   53% |
| balanced |  100% |   53% |   53% |   57% |   50% |   70% |   51% |   28% |   98% |   52% |
| opportunis |  100% |   51% |   50% |   50% |   51% |   69% |   52% |   28% |   97% |   51% |
| disruptive |  100% |   51% |   52% |   54% |   51% |   72% |   53% |   30% |   98% |   50% |
| endgame |  100% |   32% |   34% |   35% |   34% |   39% |   33% |   20% |   98% |   32% |
| mix |  100% |   55% |   51% |   51% |   51% |   70% |   52% |   29% |   98% |   52% |
| ignore_obj |  100% |   72% |   72% |   76% |   73% |   81% |   75% |   60% |  100% |   87% |
| pure_drink |   79% |    1% |    1% |    1% |    1% |    1% |    1% |    0% |   49% |    1% |
| no_drinks |   99% |   52% |   50% |   52% |   51% |   68% |   52% |   21% |   97% |   48% |

## Averaged game metrics
- margin: 23.460
- tie: 0.005
- turns: 58.504
- turns_per_player: 29.252
- food_wins: 7.614
- drink_wins: 1.781
- wins_per_player: 4.697
- drink_win_share: 0.202
- contested_wins: 0.428
- contested_frac: 0.049
- max_buzz_on_vendor: 3.516
- max_committed: 3.743
- buzz_supply_min: 17.506
- star_placed: 0.840
- star_wins_total: 0.354
- dusk_turn: 29.169
- last_turn: 54.896
- first_night_win_turn: 38.459
- end_by_lasttrain: 0.751
- end_by_deck: 0.000
- end_by_stall: 0.249
- travels_per_game: 12.742
- inter_moves: 12.742
- visits_per_game: 11.259
- cstores_per_game: 4.542
- promotes_per_game: 12.156
- passes_per_game: 0.000
- claim_share_N: 0.411
- claim_share_C: 0.179
- claim_share_S: 0.223
- claim_share_E: 0.183
- src_share_N: 0.275
- src_share_C: 0.139
- src_share_S: 0.229
- src_share_E: 0.180
- src_share_common: 0.177
- avg_legal_actions: 9.518
- forced_turn_frac: 0.000
- events_fired_per_game: 12.934
- scope_self_frac: 0.523
- scope_region_frac: 0.330
- scope_neigh_frac: 0.146
- takethat_hits_per_game: 1.737
- cs_rival_hits_per_game: 0.205
- empty_draws_per_game: 0.284
- claims_per_game: 8.410
- reach_start: 2.000
- reach_blocked_per_game: 1.869
- reach_gain_travel: 12.479
- reach_gain_event: 1.928
- reach_gain_ms: 0.927
- reach_loss_grab: 3.164
- reach_loss_event: 2.092
- reach_forced_return: 0.038
- greedy_visit_per_game: 2.665
- greedy_cs_per_game: 0.499
- greedy_grab_per_game: 3.164
- reach_zero_turns: 0.376
- reach_mean_all: 4.217
- reach_at_dusk_mean: 3.822
- reach_end_mean: 7.039
- ms7_fired: 0.931
- ms14_fired: 0.897
- ms_both_fired: 0.897
- ms_both_same_player: 0.798
- ms_both_same_given_both: 0.798
- win_bookings: 24.732
- win_ticket_score: 11.518
- win_total: 36.250
- tickets_held_winner: 2.286

## Health read
- ⚠ **possible dominant strategy**: `ignore_obj` beats every other line (worst h2h 70%). Check it isn't a memorizable one-liner before shipping.
- • intransitivity present among some lines (a depth signal), alongside the note above.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
