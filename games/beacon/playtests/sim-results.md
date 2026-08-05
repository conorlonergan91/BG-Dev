# Beacon — simulation report

1200 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **always_high     **  54.5%  ████████████████
- **hand_smart      **  53.9%  ████████████████
- **grabber         **  52.6%  ████████████████
- **tide_racer      **  50.7%  ███████████████
- **random          **  49.4%  ███████████████
- **hoarder         **  47.7%  ██████████████
- **reactive        **  46.1%  ██████████████
- **always_low      **  45.1%  ██████████████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | always_hig | always_low | hoarder | reactive | grabber | hand_smart | tide_racer |
|---|---|---|---|---|---|---|---|---|
| random |   46% |   42% |   60% |   49% |   57% |   45% |   41% |   52% |
| always_hig |   60% |   49% |   83% |   49% |   56% |   49% |   39% |   50% |
| always_low |   42% |   16% |   48% |   60% |   49% |   46% |   46% |   51% |
| hoarder |   50% |   50% |   41% |   48% |   64% |   33% |   44% |   49% |
| reactive |   42% |   46% |   49% |   38% |   52% |   67% |   37% |   39% |
| grabber |   55% |   49% |   51% |   67% |   34% |   52% |   63% |   48% |
| hand_smart |   56% |   63% |   53% |   54% |   64% |   38% |   51% |   53% |
| tide_racer |   52% |   50% |   50% |   51% |   56% |   48% |   47% |   49% |

## Averaged game metrics
- margin: 5.999
- tie: 0.129
- tide_points_total: 4.582
- tide_decisive: 0.296
- round_ties: 4.081
- nights_tide_centered: 1.551
