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
# Clean-rebuild build/ every run so stale/renamed renders (e.g. a removed ticket_general
# sheet) can't linger in build/sheets and get re-snapshotted into exports/. build/ is
# disposable scratch (gitignored) — always regenerate from scratch.
rm -rf build
# The PHASED decks (vendors / tickets / ingredients / events) render as `png` only here — their
# play-ready sheets come from the day/night SPLITS below (top-level PnP + Screentop), so the mixed
# full-CSV screentop sheet (one NEUTRAL back) is deliberately NOT produced: it would hide the
# day/night back distinction the identity requires. `png` keeps per-card art + the PnP print PDF.
# Vendor decks (24 vendors, day+night, drinks mixed in). tokens.csv feeds the recipe chip glyphs.
python3 $T/cards/build_cards.py --csv components/vendors.csv     --out build --theme "$theme" --formats png --tokens-csv components/tokens.csv
# Tour Tickets (20 DAY + 25 NIGHT = 45 cards / 44 patterns — the SOLE scoring vector; win-pile / lose-pile).
python3 $T/cards/build_cards.py --csv components/missions.csv    --out build --theme "$theme" --formats png
# Ingredient market decks (5-palette; K in C/S) — the Visit / CS / Travel draw.
python3 $T/cards/build_cards.py --csv components/ingredients.csv  --out build --theme "$theme" --formats png --tokens-csv components/tokens.csv
# Scoped EVENT cards (⦿/⬢/➤) — shuffled into the matching region+phase ingredient deck (night event-heavier).
python3 $T/cards/build_cards.py --csv components/events.csv      --out build --theme "$theme" --formats png
# Character CARDS are RETIRED — replaced by per-player CHARACTER BOARDS (landscape player mats), rendered
# in the board section below via `build_board.py --type playerboard`. See art/character-boards.md.

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

# --- DAY/NIGHT-SPLIT top-level PnP / overview sheets (phased decks carry their DISTINCT phase back) --
# The top-level exports/ is the shareable / print-and-play set. Split the phased card types by `phase`
# so each exports as a DAY sheet and a NIGHT sheet, EACH stamped with its own boarding-pass back
# (warm-☀日 / neon-☾夜) — so anyone using the MAIN export (not just the Screentop module) can sort day
# vs night piles by the back at setup / storage. Coarser than the Screentop split on purpose: two piles
# per type here (a clean PnP overview), vs Screentop's per-region+phase play piles. Ingredients + scoped
# events combine into one MARKET deck per phase (mirrors the region markets: you draw them together).
# Rendered into build/top so build/top/sheets is ISOLATED from build/sheets — the screentop snapshot's
# market_*/vend_*/ticket_* globs can never pick these up, and vice-versa.
echo "→ assembling day/night-split top-level PnP sheets"
rm -rf build/top
python3 $T/cards/split_decks.py --out build/top/decks --prefix vendors --key phase --csv components/vendors.csv
python3 $T/cards/split_decks.py --out build/top/decks --prefix market  --key phase \
    --csv components/ingredients.csv --csv components/events.csv
python3 $T/cards/split_decks.py --out build/top/decks --prefix tickets --key phase --csv components/missions.csv
for d in build/top/decks/*.csv; do
    tok=""
    case "$d" in *vendors_*|*market_*) tok="--tokens-csv components/tokens.csv";; esac
    python3 $T/cards/build_cards.py --csv "$d" --out build/top --theme "$theme" --formats screentop --tight-grid $tok
done

# Board (the region-ring table-layout) — ring + HSR + vendor slots + per-region day/night market decks +
# placeholder zones for every component. Rendered in BOTH states (mirrors the dusk flip): day / night.
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase day   --out build/map-day.png
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase night --out build/map-night.png

# Per-player CHARACTER BOARDS (5 landscape mats, one per characters.csv row) — REPLACES the character
# cards. Each board carries: name in THREE scripts (Tâi-lô · English · 繁體), an art placeholder
# [FIG-CHAR-<slug>] + a warm blurb, the ABILITY/FLAW icon blocks, the BUZZ zone with a movable REACH cap
# marker (this FOLDS IN the old standalone reach-track — committed Buzz ≤ Reach enforced at a glance), the
# per-player SOLD 成團 / CANCELLED 取消 pile zones, and a per-player TOURS-COMPLETED (好評 Rave Reviews)
# mini-track. TA-only: --type playerboard renders only rows with ability_code+flaw_code, so Beacon et al.
# are untouched.
python3 $T/boards/build_board.py --type playerboard --csv components/characters.csv --theme "$theme" --out build/boards/

# Live in-game tracks (v6.3.1 — TICKETS-ONLY scoring: there is NO score/VP track; your score is your Tour-Ticket tally).
# NOTE: the standalone REACH track and TOURS-COMPLETED track are RETIRED — both are per-player instruments
# and now live ON the character boards above (Reach = the movable cap marker on the Buzz slot row 0→12;
# Tours-Completed = the 好評 Rave-Reviews mini-track). Only the TABLE-WIDE vendor-claims clock stays a
# shared track (it will move onto the MAP in the next map pass — a board↔map interface note).
# The VENDOR-CLAIMS day-clock. +1 each time ANY agent Bribes a vendor.
python3 $T/boards/build_board.py --type scoretrack --max 10 --per-row 11 \
    --title "Vendor-claims clock (2p)" --start-label "START" \
    --milestones "5:DUSK — flip to night;10:LAST TRAIN — end game" \
    --note "Advance +1 each time ANY agent Bribes a vendor (food or drink). 2p: DUSK = the 5th claim, LAST TRAIN = the 10th. Marks GROW with player count (~7-8/15 at 3p, ~10/20 at 4p)." \
    --theme "$theme" --out build/clock-track.png

# Token key + player aid.
python3 $T/boards/build_board.py --type tokens --from-csv components/tokens.csv --shape circle --legend \
    --theme "$theme" --out build/token-key.png
python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png

# Cover + rulebook.
python3 $T/cards/build_cover.py --title "$title" --subtitle "Court the island's vendors — a warm Taiwan food-tour duel" \
    --theme "$theme" --players "2–4" --time "25–30 min" --weight 2.2 --out build/cover.png
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" --out build/rulebook.pdf

echo "→ snapshotting deliverables into exports/ (committed)"
mkdir -p exports
# Wipe the top-level deliverables first so orphans from older/renamed builds can't linger
# (mirrors the `rm -rf exports/screentop` below). exports/ is fully regenerated from data —
# nothing at the top level is hand-curated, so a clean-then-copy keeps it exactly in sync.
rm -f exports/*.png exports/*.pdf exports/*.html
cp build/cover.png                        exports/cover.png 2>/dev/null || true
# PHASED decks — DAY + NIGHT sheet each, EACH with its DISTINCT phase back (sort day vs night by the
# back). This replaces the old single mixed sheet + one neutral back, so the day/night boarding-pass
# backs live in the MAIN export too, not only in exports/screentop/.
cp build/top/sheets/vendors_day_sheet_*.png    exports/ 2>/dev/null || true
cp build/top/sheets/vendors_day_back.png       exports/ 2>/dev/null || true
cp build/top/sheets/vendors_night_sheet_*.png  exports/ 2>/dev/null || true
cp build/top/sheets/vendors_night_back.png     exports/ 2>/dev/null || true
cp build/top/sheets/market_day_sheet_*.png     exports/ 2>/dev/null || true
cp build/top/sheets/market_day_back.png        exports/ 2>/dev/null || true
cp build/top/sheets/market_night_sheet_*.png   exports/ 2>/dev/null || true
cp build/top/sheets/market_night_back.png      exports/ 2>/dev/null || true
cp build/top/sheets/tickets_day_sheet_*.png    exports/ 2>/dev/null || true
cp build/top/sheets/tickets_day_back.png       exports/ 2>/dev/null || true
cp build/top/sheets/tickets_night_sheet_*.png  exports/ 2>/dev/null || true
cp build/top/sheets/tickets_night_back.png     exports/ 2>/dev/null || true
# Character BOARDS — 5 landscape player mats (replaces the old characters_sheet). Reach + Tours-Completed
# now live on these, so the standalone reach-track / tours-track exports are gone.
cp build/boards/board-*.png               exports/ 2>/dev/null || true
cp build/map-day.png                      exports/map-day.png 2>/dev/null || true
cp build/map-night.png                    exports/map-night.png 2>/dev/null || true
cp build/clock-track.png                  exports/clock-track.png 2>/dev/null || true
cp build/token-key.png                    exports/token-key.png 2>/dev/null || true
cp build/player-aid.png                   exports/player-aid.png 2>/dev/null || true
cp build/rulebook.pdf                     exports/rulebook.pdf 2>/dev/null || true
cp build/rulebook.html                    exports/rulebook.html 2>/dev/null || true   # keep the tracked HTML in sync (build always emits it) so it can't silently drift

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
# Character BOARDS go into the Screentop set too — each uploads as a per-player board image.
cp build/boards/board-*.png               exports/screentop/ 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."
