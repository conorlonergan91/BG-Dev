# Beacon — simulation report

3000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **grabber         **  58.7%  ██████████████████
- **always_low      **  54.0%  ████████████████
- **always_high     **  51.3%  ███████████████
- **random          **  50.2%  ███████████████
- **hoarder         **  43.7%  █████████████
- **reactive        **  42.1%  █████████████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | always_hig | always_low | hoarder | reactive | grabber |
|---|---|---|---|---|---|---|
| random |   49% |   54% |   46% |   51% |   61% |   39% |
| always_hig |   46% |   49% |   62% |   51% |   56% |   44% |
| always_low |   54% |   41% |   51% |   80% |   56% |   45% |
| hoarder |   49% |   49% |   20% |   51% |   64% |   30% |
| reactive |   39% |   44% |   43% |   36% |   50% |   41% |
| grabber |   61% |   56% |   56% |   71% |   60% |   51% |

## Averaged game metrics
- margin: 5.835
- tie: 0.057
- tide_points_total: 5.215
- tide_decisive: 0.266
