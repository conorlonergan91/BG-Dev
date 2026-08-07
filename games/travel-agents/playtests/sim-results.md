# Travel Agents: Taiwan (v6.1 — the economy fork, region-anchored + scoped events) — simulation report

1000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **greedy_prest    **  66.7%  ████████████████████
- **mixed           **  66.0%  ████████████████████
- **ladder_only     **  63.8%  ███████████████████
- **ladder_lean     **  63.7%  ███████████████████
- **smart_mix       **  59.8%  ██████████████████
- **drinks_lean     **  52.4%  ████████████████
- **pure_drinks     **  21.1%  ██████
- **random          **   6.5%  ██

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | greedy_pre | ladder_onl | ladder_lea | drinks_lea | pure_drink | mixed | smart_mix |
|---|---|---|---|---|---|---|---|---|
| random |   50% |    0% |    0% |    0% |    0% |    1% |    0% |    0% |
| greedy_pre |  100% |   38% |   43% |   42% |   57% |   97% |   37% |   48% |
| ladder_onl |  100% |   34% |   38% |   40% |   54% |   99% |   32% |   48% |
| ladder_lea |  100% |   33% |   36% |   39% |   58% |   99% |   35% |   47% |
| drinks_lea |  100% |   25% |   31% |   30% |   46% |   86% |   26% |   32% |
| pure_drink |   99% |    1% |    1% |    1% |   11% |   49% |    1% |    1% |
| mixed |  100% |   34% |   40% |   41% |   57% |   97% |   37% |   49% |
| smart_mix |  100% |   28% |   33% |   35% |   54% |  100% |   32% |   44% |

## Averaged game metrics
- margin: 17.599
- tie: 0.025
- turns: 46.356
- turns_per_player: 23.178
- ladder_wins: 6.128
- bev_wins: 2.372
- bev_win_share: 0.271
- wins_per_player: 4.250
- drink_fights: 0.161
- contested_ladder_wins: 0.383
- contested_ladder_frac: 0.056
- max_buzz_on_vendor: 4.214
- buzz_supply_min: 15.629
- star_placed: 1.659
- star_wins_total: 0.987
- winner_star_wins: 0.757
- dusk_turn: 28.017
- last_turn: 42.710
- first_nm_win_turn: 34.607
- end_by_lasttrain: 0.688
- end_by_nm_deck: 0.000
- end_by_stall: 0.312
- travels_per_game: 9.267
- visits_per_game: 10.293
- cstores_per_game: 6.073
- src_share_N: 0.173
- src_share_C: 0.169
- src_share_S: 0.333
- src_share_E: 0.097
- src_share_common: 0.228
- avg_legal_actions: 9.934
- forced_turn_frac: 0.000
- events_fired_per_game: 11.650
- scope_self_frac: 0.290
- scope_region_frac: 0.508
- scope_neigh_frac: 0.202
- cs_self_events_per_game: 0.556
- cs_rival_hits_per_game: 0.370
- takethat_hits_per_game: 2.236
- pokes_per_game: 0.357
- win_prestige: 19.710
- win_rep_vp: 5.794
- win_mission: 0.643
- win_total: 30.005

## Health read
- ~ mild edge to `greedy_prest` (beats all, but by ≤1pt margins) — no crushing dominance.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
