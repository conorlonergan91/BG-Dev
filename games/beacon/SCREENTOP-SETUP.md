# Beacon — Screentop.gg setup

How to turn the generated sheets into a playable Screentop room for you + a friend.

## 1. The assets
The ready-to-upload assets are committed in **`games/beacon/exports/`** (viewable on GitHub):
- `ships_sheet_1.png` — **10 × 3 grid**, 24 ships + back  ·  `ships_back.png`
- `signals_sheet_1.png` — **10 × 2 grid**, 12 signals + back  ·  `signals_back.png`
- `cover.png` — themed box/title image (the game's cover/thumbnail in Screentop)
- `tide-track.png` — the 7-space Tide track  ·  `tokens.png` — Tide marker + First-Keeper token
- `rulebook.pdf` — the v0.3 rules, laid out (share it with your friend before you start)

To **regenerate** them after changing the data/rules, just run the game's build script:
```bash
cd games/beacon && ./make.sh      # rebuilds build/ from data, refreshes exports/
```

## 2. Build the room on Screentop.gg
1. Sign in (free) → **Create a Game** → name it *Beacon*.
2. **Add a Deck → "Ships"**: upload `ships_sheet_1.png` as the deck **face**, `ships_back.png` as the
   **back**; set the grid to **columns 10 × rows 3** (24 cards + 1 back cell).
3. **Add a Deck → "Signals"**: upload `signals_sheet_1.png` (face) + `signals_back.png` (back); grid
   **columns 10 × rows 2** (12 cards = two identical sets of 6, one per player).
4. Upload **`tide-track.png`** as a board/table image and drop a **token** (from `tokens.png`) on its
   centre space as the Tide marker; give each player a **Harbour** area (table space is fine).
5. **Share the room link** with your friend — they join in a browser, no install.

## 3. Play
Follow `design/rules-draft.md`. Quick loop: reveal 2 ships → both pick a Signal face-down → reveal →
higher wins the beam (Tide step + first pick) → refill → 4 rounds/Night → Night-end Tide bonus + the
tide turns → after Night 3, score.

> Tip: for the blind simultaneous reveal, each keeper drags their chosen Signal face-down to the table,
> then both flip together. Screentop's hidden-hand zones keep your hand secret from your friend.
