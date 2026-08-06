# Beacon — simulation report

1000 games per matchup; win rate averages both seatings (ties = 0.5).

## Overall win rate by strategy
- **always_high     **  54.7%  ████████████████
- **hand_smart      **  54.2%  ████████████████
- **grabber         **  52.4%  ████████████████
- **tide_racer      **  51.7%  ████████████████
- **random          **  48.9%  ███████████████
- **hoarder         **  47.8%  ██████████████
- **reactive        **  46.0%  ██████████████
- **always_low      **  44.3%  █████████████

## Matchup grid (row as P0 vs column as P1 — row's win rate)

| P0 \ P1 | random | always_hig | always_low | hoarder | reactive | grabber | hand_smart | tide_racer |
|---|---|---|---|---|---|---|---|---|
| random |   47% |   41% |   59% |   51% |   55% |   44% |   45% |   47% |
| always_hig |   60% |   50% |   84% |   50% |   55% |   51% |   38% |   52% |
| always_low |   41% |   18% |   50% |   58% |   52% |   50% |   44% |   47% |
| hoarder |   50% |   50% |   41% |   50% |   63% |   32% |   46% |   50% |
| reactive |   46% |   43% |   51% |   33% |   51% |   63% |   36% |   43% |
| grabber |   56% |   50% |   55% |   70% |   32% |   50% |   58% |   48% |
| hand_smart |   56% |   63% |   56% |   55% |   65% |   38% |   52% |   51% |
| tide_racer |   52% |   49% |   54% |   50% |   58% |   53% |   50% |   50% |

## Averaged game metrics
- margin: 6.007
- tie: 0.131
- tide_points_total: 4.593
- tide_decisive: 0.298
- round_ties: 4.077
- nights_tide_centered: 1.547

## Health read
- ✓ **no single dominant line** — strategies are intransitive (rock-paper-scissors). A good depth signal.
- Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and whether the optimal line actually uses the signature mechanic (probe with --matchup).
