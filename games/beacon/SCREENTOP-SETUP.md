# Beacon — Screentop.gg setup

How to turn the generated sheets into a playable Screentop room for you + a friend.

## 1. Regenerate the decks + cover (if needed)
```bash
cd games/beacon
python3 ../../tools/cards/build_cards.py --csv components/ships.csv   --out build --theme nautical --formats screentop
python3 ../../tools/cards/build_cards.py --csv components/signals.csv --out build --theme nautical --formats screentop
python3 ../../tools/cards/build_cover.py --title "Beacon" --subtitle "Two keepers. One coast." \
    --theme nautical --players 2 --time "20 min" --weight 1.8 --out build/cover.png
```
Produces (under `build/`, gitignored — regenerated from the CSVs):
- `sheets/ships_sheet_1.png` — **10 × 3 grid**, 24 ships + back  ·  `sheets/ships_back.png`
- `sheets/signals_sheet_1.png` — **10 × 2 grid**, 12 signals + back  ·  `sheets/signals_back.png`
- `cover.png` — themed box/title image (use it as the game's cover/thumbnail in Screentop)

## 2. Build the room on Screentop.gg
1. Sign in (free) → **Create a Game** → name it *Beacon*.
2. **Add a Deck → "Ships"**: upload `ships_sheet_1.png` as the deck **face**, `ships_back.png` as the
   **back**; set the grid to **columns 10 × rows 3** (24 cards + 1 back cell).
3. **Add a Deck → "Signals"**: upload `signals_sheet_1.png` (face) + `signals_back.png` (back); grid
   **columns 10 × rows 2** (12 cards = two identical sets of 6, one per player).
4. Add two **Harbour** zones (image or just table areas) and a simple **Tide track** image (7 spaces)
   with a small token as the marker. (Placeholder art is fine for testing.)
5. **Share the room link** with your friend — they join in a browser, no install.

## 3. Play
Follow `design/rules-draft.md`. Quick loop: reveal 2 ships → both pick a Signal face-down → reveal →
higher wins the beam (Tide step + first pick) → refill → 4 rounds/Night → Night-end Tide bonus + the
tide turns → after Night 3, score.

> Tip: for the blind simultaneous reveal, each keeper drags their chosen Signal face-down to the table,
> then both flip together. Screentop's hidden-hand zones keep your hand secret from your friend.
