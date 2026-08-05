#!/usr/bin/env bash
# Regenerate Beacon's components from data, then snapshot the shareable deliverables.
#   build/    = scratch (gitignored, all intermediate renders)
#   exports/  = committed deliverables (deck sheets, cover, rulebook, track, tokens)
# Run: ./make.sh   (from games/beacon/)  — needs the 2D pipeline deps (see tools/cards/requirements.txt).
set -euo pipefail
cd "$(dirname "$0")"
T=../../tools
theme=nautical

echo "→ regenerating into build/ (scratch)"
python3 $T/cards/build_cards.py  --csv components/ships.csv   --out build --theme "$theme" --formats png screentop
python3 $T/cards/build_cards.py  --csv components/signals.csv --out build --theme "$theme" --formats png screentop
python3 $T/boards/build_board.py --type track --spaces 7 --title "The Tide" \
    --left-label "Keeper A harbour" --right-label "Keeper B harbour" --theme "$theme" --out build/tide-track.png
python3 $T/boards/build_board.py --type tokens --labels "Tide,1st" --shape circle --theme "$theme" --out build/tokens.png
python3 $T/cards/build_cover.py  --title "Beacon" --subtitle "Two keepers. One coast." \
    --theme "$theme" --players 2 --time "20 min" --weight 1.8 --out build/cover.png
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "Beacon" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
cp build/cover.png                  exports/cover.png
cp build/sheets/ships_sheet_1.png   exports/ships_sheet_1.png
cp build/sheets/ships_back.png      exports/ships_back.png
cp build/sheets/signals_sheet_1.png exports/signals_sheet_1.png
cp build/sheets/signals_back.png    exports/signals_back.png
cp build/tide-track.png             exports/tide-track.png
cp build/tokens.png                 exports/tokens.png
cp build/rulebook.pdf               exports/rulebook.pdf
echo "✓ exports/ refreshed — commit these."
