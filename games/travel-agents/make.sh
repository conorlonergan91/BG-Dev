#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan — v6.3.1 (TICKETS-ONLY scoring; soft night-cost curve).
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
# Tour Tickets (20 DAY + 25 NIGHT = 45 cards / 44 patterns — the SOLE scoring vector; win-pile / lose-pile).
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
# 2 Tour-Ticket decks by phase (DAY / NIGHT — draw 5/phase, reveal a row of 3).
python3 $T/cards/split_decks.py --out build/decks --prefix ticket --key phase --csv components/missions.csv
for d in build/decks/*.csv; do
    tok=""
    case "$d" in *market_*|*vend_*) tok="--tokens-csv components/tokens.csv";; esac
    python3 $T/cards/build_cards.py --csv "$d" --out build --theme "$theme" --formats screentop --tight-grid $tok
done

# Board (the region-ring table-layout) — ring + HSR + vendor slots + per-region day/night market decks +
# placeholder zones for every component. Rendered in BOTH states (mirrors the dusk flip): day / night.
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase day   --out build/map-day.png
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase night --out build/map-night.png

# Live in-game tracks (v6.3.1 — TICKETS-ONLY scoring: there is NO score/VP track; your score is your Tour-Ticket tally).
# Reach track — your Buzz CAP (start at 2). +1 per Travel + some events. NOT a score.
# Violet accent (the Buzz hue Reach caps) so the three tracks read as DIFFERENT instruments, not clones.
python3 $T/boards/build_board.py --type scoretrack --max 12 --per-row 13 \
    --title "Reach track (Buzz cap)" --start-label "START at 2" --accent-hex "#6A4C93" \
    --kicker "YOUR BUZZ CAP — committed Buzz ≤ Reach · NOT a score" \
    --note "One marker per player, START AT 2. Your total committed Buzz may never exceed your Reach. +1 each Travel; a few events +/-. Winning a vendor clears its Buzz, freeing your cap. Reach does NOT score." \
    --theme "$theme" --out build/reach-track.png
# Tours-Completed counter — the repurposed former Bookings/VP track. Hosts the per-player Rave Reviews.
# Teal accent (off the 成團 win-pile score-gold) + a "NOT your score" kicker so the completions METER is
# never mistaken for the ticket score (bg-theme coherence flag / bg-infodesign item 2).
python3 $T/boards/build_board.py --type scoretrack --max 8 --per-row 9 \
    --title "Tours Completed (Rave Reviews)" --start-label "0" --accent-hex "#1F8A7A" \
    --kicker "A COMPLETIONS METER — NOT your score (成團 win pile is your score)" \
    --milestones "2:RAVE REVIEW 1: +1 Reach;4:RAVE REVIEW 2: +1 ingredient, next Bribe -1" \
    --note "One marker per player, starts at 0 and never goes down. +1 the instant a held Tour Ticket's pattern is met. Each agent earns their OWN Rave Review the first time THEY reach the 2nd / 4th mark (no leader pump). A COMPLETIONS counter, NOT the 成團 win pile." \
    --theme "$theme" --out build/tours-track.png
# The VENDOR-CLAIMS day-clock. +1 each time ANY agent Bribes a vendor.
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
# Wipe the top-level deliverables first so orphans from older/renamed builds can't linger
# (mirrors the `rm -rf exports/screentop` below). exports/ is fully regenerated from data —
# nothing at the top level is hand-curated, so a clean-then-copy keeps it exactly in sync.
rm -f exports/*.png exports/*.pdf
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
cp build/map-day.png                      exports/map-day.png 2>/dev/null || true
cp build/map-night.png                    exports/map-night.png 2>/dev/null || true
cp build/reach-track.png                  exports/reach-track.png 2>/dev/null || true
cp build/tours-track.png                  exports/tours-track.png 2>/dev/null || true
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
