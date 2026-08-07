# Travel Agents: Taiwan (v6.1 — the economy fork, region-anchored + scoped events) — simulation report

1200 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **mixed           **  70.1%  █████████████████████
- **greedy_prest    **  69.9%  █████████████████████
- **ladder_lean     **  69.3%  █████████████████████
- **drinks_lean     **  54.6%  ████████████████
- **pure_drinks     **  27.5%  ████████
- **random          **   8.6%  ███

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_pre | ladder_lea | drinks_lea | pure_drink | mixed |
|---|---|---|---|---|---|---|
| random |   51% |    0% |    0% |    0% |    1% |    0% |
| greedy_pre |  100% |   33% |   37% |   53% |   97% |   32% |
| ladder_lea |  100% |   34% |   39% |   56% |   99% |   32% |
| drinks_lea |  100% |   12% |   16% |   46% |   91% |   13% |
| pure_drink |  100% |    1% |    1% |   11% |   58% |    1% |
| mixed |  100% |   33% |   36% |   55% |   96% |   31% |

## Averaged game metrics
- margin: 17.595
- tie: 0.027
- turns: 48.841
- turns_per_player: 24.420
- ladder_wins: 5.411
- bev_wins: 3.058
- bev_win_share: 0.365
- wins_per_player: 4.234
- drink_fights: 0.165
- contested_ladder_wins: 0.278
- contested_ladder_frac: 0.043
- max_buzz_on_vendor: 3.881
- buzz_supply_min: 16.019
- star_placed: 1.894
- star_wins_total: 1.053
- winner_star_wins: 0.837
- dusk_turn: 33.608
- last_turn: 45.140
- first_nm_win_turn: 39.185
- end_by_lasttrain: 0.563
- end_by_nm_deck: 0.000
- end_by_stall: 0.437
- travels_per_game: 9.181
- visits_per_game: 11.254
- cstores_per_game: 8.112
- src_share_N: 0.155
- src_share_C: 0.246
- src_share_S: 0.270
- src_share_E: 0.092
- src_share_common: 0.237
- avg_legal_actions: 9.778
- forced_turn_frac: 0.000
- events_fired_per_game: 13.302
- scope_self_frac: 0.290
- scope_region_frac: 0.509
- scope_neigh_frac: 0.201
- cs_self_events_per_game: 0.736
- cs_rival_hits_per_game: 0.463
- takethat_hits_per_game: 2.370
- pokes_per_game: 0.187
- win_prestige: 18.960
- win_rep_vp: 5.626
- win_mission: 0.570
- win_total: 28.576

## Health read
- ~ mild edge to `mixed` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
