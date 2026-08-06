#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan.
# Regenerates build/ (scratch) from data and snapshots the shareable deliverables into exports/ (committed).
# Run: ./make.sh   (from games/travel-agents/).
set -euo pipefail
cd "$(dirname "$0")"
T=../../tools
theme=clean            # placeholder — swap for the game's palette theme once bg-theme sets it (tools/cards/themes.py)
title="Travel Agents: Taiwan"

echo "→ regenerating into build/ (scratch)"
# One line per deck (repeat for each components/*.csv) — decks appear once component data exists:
# python3 $T/cards/build_cards.py --csv components/cards.csv --out build --theme "$theme" --formats png screentop
# Optional pieces — uncomment/adjust as the game needs them:
# python3 $T/boards/build_board.py --type track  --spaces 7 --title "Route" --theme "$theme" --out build/track.png
# python3 $T/boards/build_board.py --type tokens --labels "A,B" --shape circle --theme "$theme" --out build/tokens.png
# python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png
python3 $T/cards/build_cover.py --title "$title" --subtitle "Eat your way across the island" --theme "$theme" \
    --players 4 --time "30–45 min" --out build/cover.png
# python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
cp build/cover.png                exports/cover.png 2>/dev/null || true
cp build/sheets/*_sheet_*.png     exports/ 2>/dev/null || true
cp build/sheets/*_back.png        exports/ 2>/dev/null || true
# cp build/rulebook.pdf             exports/rulebook.pdf 2>/dev/null || true
# cp build/track.png build/tokens.png build/player-aid.png exports/ 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."
