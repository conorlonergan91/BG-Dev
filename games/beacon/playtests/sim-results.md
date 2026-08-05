# Beacon — simulation report

3000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **always_high     **  66.7%  ████████████████████
- **hoarder         **  65.0%  ████████████████████
- **reactive        **  63.0%  ███████████████████
- **random          **  43.5%  █████████████
- **always_low      **  11.7%  ████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | always_hig | always_low | hoarder | reactive |
|---|---|---|---|---|---|
| random |   51% |    7% |   93% |   50% |   17% |
| always_hig |   92% |   49% |  100% |   51% |   41% |
| always_low |    8% |    0% |   50% |    0% |    1% |
| hoarder |   50% |   50% |   99% |   50% |   76% |
| reactive |   83% |   59% |   99% |   24% |   50% |

## Averaged game metrics
- margin: 10.200
- tie: 0.038
- tide_points_total: 4.907
- tide_decisive: 0.157
