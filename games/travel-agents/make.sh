#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan — v3 (the vendor-courting engine).
# Regenerates build/ (scratch) from data and snapshots the shareable deliverables into exports/ (committed).
# Run: ./make.sh   (from games/travel-agents/)  — needs the 2D pipeline deps (see tools/cards/requirements.txt).
#
# DATA IS THE SOURCE OF TRUTH (components/*.csv|json). Never hand-edit anything in build/ — regenerate.
set -euo pipefail
cd "$(dirname "$0")"
T=../../tools
theme=night-market
title="Travel Agents: Taiwan"

echo "→ regenerating into build/ (scratch)"
# Decks (data → cards). The tokens.csv feeds the ingredient chip-row on vendor cards (recipe glyphs).
python3 $T/cards/build_cards.py --csv components/vendors.csv    --out build --theme "$theme" --formats png screentop --tokens-csv components/tokens.csv
python3 $T/cards/build_cards.py --csv components/missions.csv   --out build --theme "$theme" --formats png screentop
# Event tiles + Character mats are NEW component types — rendered as cards here for the prototype
# (a bespoke tile / mat template is a bg-prototyper / bg-infodesign task; see the handoff notes).
python3 $T/cards/build_cards.py --csv components/events.csv     --out build --theme "$theme" --formats png screentop
python3 $T/cards/build_cards.py --csv components/characters.csv --out build --theme "$theme" --formats png screentop

# Board + tracks + token keys + aid
python3 $T/boards/build_board.py --type mat    --spec components/map.json --theme "$theme" --out build/map.png
python3 $T/boards/build_board.py --type track  --spaces 16 --title "Season end-timer" \
    --labels ",,,,,,,,,,,,,,,final" --left-label "start" --right-label "wind-down (~16 courts, 2p)" \
    --theme "$theme" --out build/season-track.png
python3 $T/boards/build_board.py --type track  --spaces 12 --title "Reputation track" \
    --labels ",,3,,,6,,,9,,,top" --left-label "0" --right-label "+9 & endgame" \
    --theme "$theme" --out build/reputation-track.png
python3 $T/boards/build_board.py --type tokens --from-csv components/tokens.csv --shape circle --cols 6 \
    --theme "$theme" --out build/token-key.png
python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png

# Cover + rulebook
python3 $T/cards/build_cover.py --title "$title" --subtitle "Court the island's vendors — a warm Taiwan food-tour duel" \
    --theme "$theme" --players 2 --time "40–50 min" --weight 2.3 --out build/cover.png
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
cp build/cover.png                        exports/cover.png 2>/dev/null || true
cp build/sheets/vendors_sheet_*.png       exports/ 2>/dev/null || true
cp build/sheets/vendors_back.png          exports/ 2>/dev/null || true
cp build/sheets/missions_sheet_*.png      exports/ 2>/dev/null || true
cp build/sheets/missions_back.png         exports/ 2>/dev/null || true
cp build/sheets/events_sheet_*.png        exports/ 2>/dev/null || true
cp build/sheets/characters_sheet_*.png    exports/ 2>/dev/null || true
cp build/map.png                          exports/map.png 2>/dev/null || true
cp build/season-track.png                 exports/season-track.png 2>/dev/null || true
cp build/reputation-track.png             exports/reputation-track.png 2>/dev/null || true
cp build/token-key.png                    exports/token-key.png 2>/dev/null || true
cp build/player-aid.png                   exports/player-aid.png 2>/dev/null || true
cp build/rulebook.pdf                     exports/rulebook.pdf 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."
