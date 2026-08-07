# Travel Agents: Taiwan (v6.1 — the economy fork, region-anchored + scoped events) — simulation report

1000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **mixed           **  67.3%  ████████████████████
- **greedy_prest    **  66.7%  ████████████████████
- **smart_mix       **  61.0%  ██████████████████
- **drinks_lean     **  59.0%  ██████████████████
- **ladder_lean     **  58.6%  ██████████████████
- **ladder_only     **  56.1%  █████████████████
- **pure_drinks     **  24.8%  ███████
- **random          **   6.5%  ██

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_pre | ladder_onl | ladder_lea | drinks_lea | pure_drink | mixed | smart_mix |
|---|---|---|---|---|---|---|---|---|
| random |   50% |    0% |    0% |    0% |    0% |    0% |    0% |    0% |
| greedy_pre |  100% |   33% |   54% |   45% |   51% |   82% |   31% |   42% |
| ladder_onl |  100% |   22% |   37% |   35% |   32% |   99% |   21% |   33% |
| ladder_lea |  100% |   24% |   40% |   40% |   37% |   97% |   21% |   36% |
| drinks_lea |   99% |   28% |   52% |   46% |   45% |   76% |   28% |   43% |
| pure_drink |   99% |    4% |    1% |    1% |   18% |   47% |    6% |    2% |
| mixed |   99% |   34% |   52% |   49% |   50% |   82% |   33% |   44% |
| smart_mix |  100% |   25% |   44% |   41% |   42% |   98% |   25% |   38% |

## Averaged game metrics
- margin: 17.691
- tie: 0.022
- turns: 49.563
- turns_per_player: 24.781
- ladder_wins: 5.690
- bev_wins: 2.812
- bev_win_share: 0.334
- wins_per_player: 4.251
- drink_fights: 0.157
- contested_ladder_wins: 0.339
- contested_ladder_frac: 0.052
- max_buzz_on_vendor: 4.109
- buzz_supply_min: 15.865
- star_placed: 1.703
- star_wins_total: 1.051
- winner_star_wins: 0.755
- dusk_turn: 33.707
- last_turn: 45.842
- first_nm_win_turn: 39.580
- end_by_lasttrain: 0.533
- end_by_nm_deck: 0.000
- end_by_stall: 0.467
- travels_per_game: 8.815
- visits_per_game: 9.831
- cstores_per_game: 7.925
- src_share_N: 0.161
- src_share_C: 0.164
- src_share_S: 0.351
- src_share_E: 0.087
- src_share_common: 0.237
- avg_legal_actions: 10.765
- forced_turn_frac: 0.000
- events_fired_per_game: 11.841
- scope_self_frac: 0.290
- scope_region_frac: 0.509
- scope_neigh_frac: 0.200
- cs_self_events_per_game: 0.738
- cs_rival_hits_per_game: 0.485
- takethat_hits_per_game: 2.253
- pokes_per_game: 0.262
- books_per_game: 2.444
- tickets_held_winner: 2.150
- tickets_done_winner: 1.034
- ticket_net_winner: 2.668
- win_prestige: 18.318
- win_rep_vp: 5.419
- win_ticket_score: 2.668
- win_total: 26.405

## Health read
- ~ mild edge to `mixed` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
