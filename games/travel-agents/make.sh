#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan.
# Regenerates build/ (scratch) from data and snapshots the shareable deliverables into exports/ (committed).
# Run: ./make.sh   (from games/travel-agents/)  — needs the 2D pipeline deps (see tools/cards/requirements.txt).
#
# DATA IS THE SOURCE OF TRUTH (components/*.csv|json). Never hand-edit anything in build/ — regenerate.
set -euo pipefail
cd "$(dirname "$0")"
T=../../tools
# NOTE: the `night-market` theme (palette + per-suit colour/emblem) is NOT yet in tools/cards/themes.py.
# Until a prototyper adds it, this falls back to the `clean` theme. Swap once it's in.
theme=night-market
title="Travel Agents: Taiwan"

echo "→ regenerating into build/ (scratch)"
# Decks (data → cards)
python3 $T/cards/build_cards.py --csv components/dishes.csv      --out build --theme "$theme" --formats png screentop
python3 $T/cards/build_cards.py --csv components/assignments.csv --out build --theme "$theme" --formats png screentop

# Board + tracks + tokens + aid
python3 $T/boards/build_board.py --type mat    --spec components/map.json        --theme "$theme" --out build/map.png
python3 $T/boards/build_board.py --type track  --spaces 16 --title "Grand Dossier" \
    --labels ",,,4,,,,8,,,,12,,,,16" --left-label "start" --right-label "final milestone" \
    --theme "$theme" --out build/grand-dossier-track.png
python3 $T/boards/build_board.py --type tokens --from-csv components/tokens.csv --shape circle --cols 7 \
    --theme "$theme" --out build/token-key.png
python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png

# Cover + rulebook
python3 $T/cards/build_cover.py --title "$title" --subtitle "A warm food-travel duel across Taiwan" \
    --theme "$theme" --players 2 --time "30–40 min" --weight 1.8 --out build/cover.png
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
cp build/cover.png                       exports/cover.png 2>/dev/null || true
cp build/sheets/dishes_sheet_*.png       exports/ 2>/dev/null || true
cp build/sheets/dishes_back.png          exports/ 2>/dev/null || true
cp build/sheets/assignments_sheet_*.png  exports/ 2>/dev/null || true
cp build/sheets/assignments_back.png     exports/ 2>/dev/null || true
cp build/map.png                         exports/map.png 2>/dev/null || true
cp build/grand-dossier-track.png         exports/grand-dossier-track.png 2>/dev/null || true
cp build/token-key.png                   exports/token-key.png 2>/dev/null || true
cp build/player-aid.png                  exports/player-aid.png 2>/dev/null || true
cp build/rulebook.pdf                    exports/rulebook.pdf 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."
