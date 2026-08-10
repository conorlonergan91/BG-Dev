#!/usr/bin/env bash
# Per-game build script for Travel Agents: Taiwan — V7 (multiplayer 3–6; area-majority; TICKETS-ONLY scoring).
# V7 DATA NOTE: missions.csv→bookings.csv (the 開團 Bookings deck); ingredient TOKENS dropped (ingredients are
# CARDS now — components/ingredients.csv); the vendor recipe-chip glyph key moved to components/recipe-glyphs.csv
# (tokens.csv is now the pure physical-token list: Followers / the Followers-max dial / Trending / pile+Rave
# markers / 停 / pawns). The vendor-claims clock is RETIRED (the Booking deck is the deck-driven clock now).
# RENDER REBUILD OWED → bg-infodesign: the icon system (6 character-board ability/flaw glyphs incl. new
# start_max_4 / win_ties / travel_anywhere codes), the neutral N-player regionmap (render_regionmap still draws
# the stale 2p across-the-table layout), and the pictorial ingredient/food cards. Those renders are STUBS here.
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
# Vendor decks (24 vendors, day+night, drinks mixed in). recipe-glyphs.csv feeds the recipe chip glyphs
# (the 5 ingredient ids → 繁體 label; decoupled from tokens.csv now that ingredient tokens are dropped).
python3 $T/cards/build_cards.py --csv components/vendors.csv     --out build --theme "$theme" --formats png --tokens-csv components/recipe-glyphs.csv
# Bookings (開團) — 6 DAY + 8 NIGHT + 31 ANY-time (§20/§21) = 45 cards — the SOLE scoring vector (成團 / 取消).
python3 $T/cards/build_cards.py --csv components/bookings.csv    --out build --theme "$theme" --formats png
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
# 3 Bookings decks by phase (DAY / NIGHT / ANY-time — §20 agnostic tours; reveal a face-up row).
python3 $T/cards/split_decks.py --out build/decks --prefix booking --key phase --csv components/bookings.csv
for d in build/decks/*.csv; do
    tok=""
    case "$d" in *market_*|*vend_*) tok="--tokens-csv components/recipe-glyphs.csv";; esac
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
python3 $T/cards/split_decks.py --out build/top/decks --prefix bookings --key phase --csv components/bookings.csv
for d in build/top/decks/*.csv; do
    tok=""
    case "$d" in *vendors_*|*market_*) tok="--tokens-csv components/recipe-glyphs.csv";; esac
    python3 $T/cards/build_cards.py --csv "$d" --out build/top --theme "$theme" --formats screentop --tight-grid $tok
done

# Board (the region-ring table-layout) — ring + HSR + vendor slots + per-region day/night market decks +
# placeholder zones for every component. Rendered in BOTH states (mirrors the dusk flip): day / night.
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase day   --out build/map-day.png
python3 $T/boards/build_board.py --type regionmap --spec components/map.json --theme "$theme" --phase night --out build/map-night.png

# Per-player CHARACTER BOARDS (6 A4-LANDSCAPE mats, one per characters.csv row) — CD REDESIGN 2026-08 v2.
# Each board carries: English name TOP-LEFT + 漢字 TOP-RIGHT with the Tâi-lô romanisation beneath it, and
# the ICON-ONLY ability/flaw medallions CENTRED in the gold title band (no keyword text — the rulebook
# carries the words); a full-height character IMAGE on the LEFT with the Followers DIAL (an actual 0–8
# notched dial face, start 2 / 4 for the Influencer, ready for a 3D-printed rotating knob) beneath it; a
# short funny PROSE one-liner; and the TWO card-EXACT-footprint scoring zones (63.5×88.9 mm) on the RIGHT
# — CANCELLED 取消 · COMPLETE 成團. The bottom footer (scoring/hand-limit/Rave/dial-rule text) was REMOVED
# from the board (it lives in the rulebook now). TA-only: --type playerboard renders only rows with
# ability_code+flaw_code, so Beacon et al. are untouched.
#
# ART EMBED: prep the six approved playtest illustrations from art/mockups/ into the gitignored
# build/mockups/ at the board's image-slot size (900×1330 px — the v3 LEFT-column portrait slot), keyed to
# transparent + fit. render_playerboard auto-embeds build/mockups/FIG-CHAR-<slug>.png (base64 data-URI)
# when present, else the dashed placeholder. NOTE (CD 2026-08): the "no AI art in committed deliverables"
# rail is LIFTED FOR THIS PROTOTYPE — the art-embedded boards below are what ships into exports/.
mkdir -p build/mockups
for slug in old-councillor homebody big-eater influencer big-boss globetrotter; do
    python3 $T/mockup/prep_mockup.py --image art/mockups/FIG-CHAR-$slug.png --key-bg \
        --fit 900x1330 --pad --outdir build/mockups --out FIG-CHAR-$slug.png
done
# WARM boards (playtest art embedded) → build/boards/. These ARE the committed set now (snapshotted into
# exports/ + exports/screentop/ below). Default --mockups-dir is build/mockups, so these embed the art.
python3 $T/boards/build_board.py --type playerboard --csv components/characters.csv --theme "$theme" --out build/boards/
# PLACEHOLDER boards (dashed [FIG-CHAR-<slug>] slot, NO art) → kept as the art-absent fallback reference
# only (no longer snapshotted). Point --mockups-dir at an empty dir so the embed falls back to placeholder.
mkdir -p build/nomockups
python3 $T/boards/build_board.py --type playerboard --csv components/characters.csv --theme "$theme" \
    --mockups-dir build/nomockups --out build/boards-placeholder/

# Live in-game tracks: V7 has NO shared clock track — the clock is DECK-DRIVEN (the Booking deck IS the
# clock: DAY-deck-out → 黃昏 DUSK, NIGHT-deck-out → 末班車 LAST TRAIN, via seeded boundary cards). The old
# vendor-claims clock-track render is RETIRED. The per-player Followers-max DIAL + the 好評 Rave-Reviews /
# Tours-Completed counter live ON the character boards (rendered above). So there is NO scoretrack render.

# Token key + player aid.
python3 $T/boards/build_board.py --type tokens --from-csv components/tokens.csv --shape circle --legend \
    --theme "$theme" --out build/token-key.png
# Closing-Time die (關門) — the custom d6 rendered as a 6-FACE reference sheet (a printable / Screentop
# key), replacing the single text-legend token: 4 region faces (北/中/南/東, each in that region's
# established colour + emblem + 繁體) + 2 BLANK faces (the 1/3 reprieve). Dual-coded colour + emblem +
# CJK (bg-access), region hues/emblems reused straight from map.json — none minted here.
python3 $T/boards/build_board.py --type die --spec components/map.json --theme "$theme" --out build/die-closing-time.png
python3 $T/boards/build_board.py --type aid    --spec components/player-aid.json --theme "$theme" --out build/player-aid.png

# Cover + rulebook.
python3 $T/cards/build_cover.py --title "$title" --subtitle "A crowded market of rival agencies — a warm Taiwan food-tour scrum" \
    --theme "$theme" --players "3–6" --time "30–45 min" --weight 2.2 --out build/cover.png
# --rich = the stylish layout (full-page cover, embedded board/die art, the "Meet the Agents" portrait
# cards); --portraits-dir feeds the six approved FIG-CHAR playtest illustrations (AI-art rail lifted for
# this prototype). All of this is opt-in — Beacon renders through the SAME script WITHOUT --rich, so its
# rulebook is byte-identical. --cover-image points at FIG-COVER.png: it auto-embeds a dedicated cover
# illustration WHEN the illustrator delivers one, and until then falls back to a tasteful themed title
# page (the CD's stated fallback). Swap to build/cover.png here if you prefer the auto box-cover render.
python3 $T/rulebook/build_rulebook.py --md design/rules-draft.md --title "$title" --theme "$theme" \
    --rich --cover-image art/mockups/FIG-COVER.png --portraits-dir art/mockups \
    --subtitle "A crowded market of rival agencies — a warm Taiwan food-tour scrum" \
    --out build/rulebook.pdf

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
cp build/top/sheets/bookings_day_sheet_*.png    exports/ 2>/dev/null || true
cp build/top/sheets/bookings_day_back.png       exports/ 2>/dev/null || true
cp build/top/sheets/bookings_night_sheet_*.png  exports/ 2>/dev/null || true
cp build/top/sheets/bookings_night_back.png     exports/ 2>/dev/null || true
# §20 ANY-time (agnostic) tour pile — 31 tours drawable throughout; its own sheet + neutral back.
cp build/top/sheets/bookings_any_sheet_*.png    exports/ 2>/dev/null || true
cp build/top/sheets/bookings_any_back.png       exports/ 2>/dev/null || true
# Character BOARDS — 6 A4-landscape player mats. Snapshot the WARM ART-EMBEDDED renders (build/boards/):
# the CD lifted the "no AI art in committed deliverables" rail for the PROTOTYPE, so the committed +
# Screentop boards SHOW the six approved playtest illustrations (art/mockups/FIG-CHAR-<slug>.png, prepped
# into build/mockups/ above and embedded by render_playerboard). The placeholder set (build/boards-
# placeholder/) is kept as the art-absent fallback only; it is no longer what ships.
cp build/boards/board-*.png               exports/ 2>/dev/null || true
cp build/map-day.png                      exports/map-day.png 2>/dev/null || true
cp build/map-night.png                    exports/map-night.png 2>/dev/null || true
cp build/token-key.png                    exports/token-key.png 2>/dev/null || true
cp build/die-closing-time.png             exports/die-closing-time.png 2>/dev/null || true
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
cp build/sheets/booking_*_sheet_*.png     exports/screentop/ 2>/dev/null || true
cp build/sheets/booking_*_back.png        exports/screentop/ 2>/dev/null || true
# Character BOARDS go into the Screentop set too — each uploads as a per-player board image (the WARM
# art-embedded renders; AI playtest art is wanted in the prototype per the CD).
cp build/boards/board-*.png               exports/screentop/ 2>/dev/null || true
# The shared TABLE map (both day/night states) — the Screentop module stands the play area up from these.
cp build/map-day.png                      exports/screentop/map-day.png 2>/dev/null || true
cp build/map-night.png                    exports/screentop/map-night.png 2>/dev/null || true
# The Closing-Time die reference sheet — the Screentop module stands the custom d6 up from this key too.
cp build/die-closing-time.png             exports/screentop/die-closing-time.png 2>/dev/null || true
echo "✓ exports/ refreshed — commit these."

# --- HOME PRINT-AND-PLAY (library A4 / A3, print-at-100%-and-cut) --------------------------------
# TA-LOCAL. Tiles the ALREADY-RENDERED component PNGs at TRUE physical size onto A4/A3 pages with cut
# guides + a scale-check cover, via tools/print/build_pnp.py (weasyprint, mm units — the same engine as
# the rulebook). This CONSUMES renders; it never re-renders shared code. The CD wanted a set they can
# print at a library and cut out. Regenerates into exports/print/ (committed). Cards get BOTH an A4 and
# an A3 version (the CD picks per the library's paper). build/pnp is disposable scratch.
echo "→ tiling the home print-and-play PDFs into exports/print/"
rm -rf build/pnp
mkdir -p build/pnp exports/print
# Individual card FRONT PNGs (750×1050 = true 63.5×88.9 mm poker) for the four play decks.
python3 $T/cards/build_cards.py --csv components/vendors.csv     --out build/pnp/vendors     --theme "$theme" --formats png --tokens-csv components/recipe-glyphs.csv
python3 $T/cards/build_cards.py --csv components/bookings.csv    --out build/pnp/bookings    --theme "$theme" --formats png
python3 $T/cards/build_cards.py --csv components/ingredients.csv --out build/pnp/ingredients --theme "$theme" --formats png --tokens-csv components/tokens.csv
python3 $T/cards/build_cards.py --csv components/events.csv      --out build/pnp/events      --theme "$theme" --formats png
cardblurb="All play cards, in real deck quantities: 24 Vendors, 45 Bookings, 62 Ingredients (16 faces × copies), 54 Events (the V7-M pool — day + night; setup deals a per-count subset per region)."
carddecks="build/pnp/vendors/png build/pnp/bookings/png build/pnp/ingredients/png build/pnp/events/png"
# Repeat each card by its deck `quantity` (so e.g. the 16 ingredient faces print as the real 62-card
# deck). No-op for vendors/bookings/events (all quantity 1).
cardqty="components/vendors.csv components/bookings.csv components/ingredients.csv components/events.csv"
# Cards — A4 (9 per sheet, 3×3) AND A3 (16 per sheet, 4×4). Both required.
python3 $T/print/build_pnp.py --mode cards --page A4 --theme "$theme" \
    --title "$title — Cards (A4)" --blurb "$cardblurb" --quantities-csv $cardqty \
    --out exports/print/pnp-cards-A4.pdf $carddecks
python3 $T/print/build_pnp.py --mode cards --page A3 --theme "$theme" \
    --title "$title — Cards (A3)" --blurb "$cardblurb" --quantities-csv $cardqty \
    --out exports/print/pnp-cards-A3.pdf $carddecks
# Character / player boards — 1 per A4-LANDSCAPE at true 297×210 mm (each board now IS a full A4 sheet).
python3 $T/print/build_pnp.py --mode images --page A4 --landscape --per-page 1 --theme "$theme" \
    --title "$title — Character Boards" \
    --blurb "6 character / player boards at true 297×210 mm (one per A4-landscape sheet), with the playtest character art embedded." \
    --out exports/print/pnp-boards.pdf exports/board-*.png
# Region map — A3 (one per sheet) + an A4-landscape fallback (fits on one A4 landscape, no taping).
python3 $T/print/build_pnp.py --mode images --page A3 --per-page 1 --theme "$theme" \
    --title "$title — Region Map (A3)" \
    --blurb "The shared table map at true 193×142 mm, in both day and night states — one per A3 sheet." \
    --out exports/print/pnp-map-A3.pdf exports/map-day.png exports/map-night.png
python3 $T/print/build_pnp.py --mode images --page A4 --landscape --per-page 1 --theme "$theme" \
    --title "$title — Region Map (A4 fallback)" \
    --blurb "A4-landscape fallback if the library has no A3: the 193×142 mm map fits on one A4 landscape sheet at true size — no taping needed. Day + night." \
    --out exports/print/pnp-map-A4.pdf exports/map-day.png exports/map-night.png
# Tokens key + player aid — one asset per sheet.
python3 $T/print/build_pnp.py --mode images --page A4 --per-page 1 --theme "$theme" \
    --title "$title — Tokens & Player Aid" \
    --blurb "The token key (Followers / Trending / dials / markers) on sheet 1, and the player aid on sheet 2, at true 300-DPI size." \
    --out exports/print/pnp-tokens-aid.pdf exports/token-key.png exports/player-aid.png
echo "✓ exports/print/ refreshed — print at 100% / Actual Size and cut. Commit these."
