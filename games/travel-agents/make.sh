#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan — v6.2 (region vendor markets + the vendor-claims clock).
# Regenerates build/ (scratch) from data and snapshots the shareable deliverables into exports/ (committed).
# Run: ./make.sh   (from games/travel-agents/)  — needs the 2D pipeline deps (see tools/cards/requirements.txt).
#
# DATA IS THE SOURCE OF TRUTH (components/*.csv|json). Never hand-edit anything in build/ — regenerate.
# For the Screentop prototype the prototyper splits each deck by its `deck`/`phase` tag into per-region
# DAY and NIGHT piles; this script renders each CSV as one sheet (data is already tagged for the split).
set -euo pipefail
cd "$(dirname "$0")"
T=../../tools
theme=night-market
title="Travel Agents: Taiwan"

echo "→ regenerating into build/ (scratch)"
# Vendor decks (24 vendors, day+night, drinks mixed in). tokens.csv feeds the recipe chip glyphs.
python3 $T/cards/build_cards.py --csv components/vendors.csv     --out build --theme "$theme" --formats png screentop --tokens-csv components/tokens.csv
# Tour Tickets (12 day + 12 night + 3 general) — the objective spine (win-pile / lose-pile scored later).
python3 $T/cards/build_cards.py --csv components/missions.csv    --out build --theme "$theme" --formats png screentop
# Ingredient market decks (5-palette; K in C/S) — the Visit / CS / Travel draw.
python3 $T/cards/build_cards.py --csv components/ingredients.csv  --out build --theme "$theme" --formats png screentop --tokens-csv components/tokens.csv
# Scoped EVENT cards (⦿/⬢/➤) — shuffled into the matching region+phase ingredient deck (night event-heavier).
python3 $T/cards/build_cards.py --csv components/events.csv      --out build --theme "$theme" --formats png screentop
# Character mats — rendered as cards for the prototype (bespoke mat template is a bg-infodesign task).
python3 $T/cards/build_cards.py --csv components/characters.csv  --out build --theme "$theme" --formats png screentop

# --- PLAY-READY per-deck Screentop sheets (assembled from the data by split_decks.py) ----------
# Each pile below becomes ONE Screentop deck upload (one sheet + its back). The full-CSV sheets above
# stay as the PnP/overview set; these split sheets are what you stand the 2p module up from.
echo "→ assembling play-ready per-deck Screentop sheets"
rm -rf build/decks
# 8 ingredient decks = each region+phase's ingredient cards + its matching-`deck` scoped events, together.
python3 $T/cards/split_decks.py --out build/decks --prefix market --key deck \
    --csv components/ingredients.csv --csv components/events.csv
# 8 vendor decks split by region + phase (face-up: North 2, others 1 — see the setup note).
python3 $T/cards/split_decks.py --out build/decks --prefix vend --key type,phase --csv components/vendors.csv
# 3 Tour-Ticket decks by phase (day / night / general — draw 5/phase, reveal a row of 3).
python3 $T/cards/split_decks.py --out build/decks --prefix ticket --key phase --csv components/missions.csv
for d in build/decks/*.csv; do
    tok=""
    case "$d" in *market_*|*vend_*) tok="--tokens-csv components/tokens.csv";; esac
    python3 $T/cards/build_cards.py --csv "$d" --out build --theme "$theme" --formats screentop --tight-grid $tok
done

# Board (the region-ring map) — 4 regions on the ring + HSR spine + face-up slot counts.
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --out build/map.png

# Live in-game tracks.
# Prestige = the VP tracker (0->50, one marker per player, mark points as you Bribe vendors).
python3 $T/boards/build_board.py --type scoretrack --max 50 --per-row 13 \
    --title "Prestige (VP) track" --start-label "START" \
    --note "One marker per player. Advance it as you score — each vendor you Bribe adds its Prestige. Most points = Top Agent." \
    --theme "$theme" --out build/prestige-track.png
# Reputation track — end-VP by FINAL position only (not cumulative).
python3 $T/boards/build_board.py --type scoretrack --max 12 --per-row 13 \
    --title "Reputation track" --start-label "START" \
    --milestones "3:+2 VP;6:+4 VP;9:+6 VP;12:+9 VP" \
    --note "Climb by Bribing (each vendor's printed Rep). At GAME END score the VP bonus for your FINAL position only. Reputation does NOT end the game — the last train does." \
    --theme "$theme" --out build/reputation-track.png
# The VENDOR-CLAIMS clock — the v6.2 day-clock. +1 each time ANY agent Bribes a vendor.
python3 $T/boards/build_board.py --type scoretrack --max 10 --per-row 11 \
    --title "Vendor-claims clock (2p)" --start-label "START" \
    --milestones "5:DUSK — flip to night;10:LAST TRAIN — end game" \
    --note "Advance +1 each time ANY agent Bribes a vendor (food or drink). 2p: DUSK = the 5th claim, LAST TRAIN = the 10th. Marks GROW with player count (~7-8/15 at 3p, ~10/20 at 4p)." \
    --theme "$theme" --out build/clock-track.png

# Token key + player aid.
python3 $T/boards/build_board.py --type tokens --from-csv components/tokens.csv --shape circle --cols 6 \
    --theme "$theme" --out build/token-key.png
python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png

# Cover + rulebook.
python3 $T/cards/build_cover.py --title "$title" --subtitle "Court the island's vendors — a warm Taiwan food-tour duel" \
    --theme "$theme" --players 2 --time "40–50 min" --weight 2.2 --out build/cover.png
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
# stale orphan from a pre-v6 build (make.sh renders clock-track now, not season-track)
rm -f exports/season-track.png
cp build/cover.png                        exports/cover.png 2>/dev/null || true
cp build/sheets/vendors_sheet_*.png       exports/ 2>/dev/null || true
cp build/sheets/vendors_back.png          exports/ 2>/dev/null || true
cp build/sheets/missions_sheet_*.png      exports/ 2>/dev/null || true
cp build/sheets/missions_back.png         exports/ 2>/dev/null || true
cp build/sheets/ingredients_sheet_*.png   exports/ 2>/dev/null || true
cp build/sheets/ingredients_back.png      exports/ 2>/dev/null || true
cp build/sheets/events_sheet_*.png        exports/ 2>/dev/null || true
cp build/sheets/events_back.png           exports/ 2>/dev/null || true
cp build/sheets/characters_sheet_*.png    exports/ 2>/dev/null || true
cp build/map.png                          exports/map.png 2>/dev/null || true
cp build/prestige-track.png               exports/prestige-track.png 2>/dev/null || true
cp build/reputation-track.png             exports/reputation-track.png 2>/dev/null || true
cp build/clock-track.png                  exports/clock-track.png 2>/dev/null || true
cp build/token-key.png                    exports/token-key.png 2>/dev/null || true
cp build/player-aid.png                   exports/player-aid.png 2>/dev/null || true
cp build/rulebook.pdf                     exports/rulebook.pdf 2>/dev/null || true

# The PLAY-READY Screentop upload set — one sheet + back per pile (assembled per-deck sheets).
echo "→ snapshotting the play-ready Screentop deck set into exports/screentop/"
rm -rf exports/screentop
mkdir -p exports/screentop
cp build/sheets/market_*_sheet_*.png      exports/screentop/ 2>/dev/null || true
cp build/sheets/market_*_back.png         exports/screentop/ 2>/dev/null || true
cp build/sheets/vend_*_sheet_*.png        exports/screentop/ 2>/dev/null || true
cp build/sheets/vend_*_back.png           exports/screentop/ 2>/dev/null || true
cp build/sheets/ticket_*_sheet_*.png      exports/screentop/ 2>/dev/null || true
cp build/sheets/ticket_*_back.png         exports/screentop/ 2>/dev/null || true
cp build/sheets/characters_sheet_*.png    exports/screentop/ 2>/dev/null || true
cp build/sheets/characters_back.png       exports/screentop/ 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."
