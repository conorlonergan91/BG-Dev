# The Shared Table Map — illustration brief (V7 · board render v3)

> **Briefs only. NO AI final art** (studio rail — `designer-profile.md`). Direction for a **human
> illustrator**; the board renders as a functional, **textless icon-only** layout
> (`build_board.py --type regionmap`, two faces via `--phase day|night`) until real art lands. This brief
> names the figure codes the board's composition RESERVES art space for, so an illustrated centrepiece
> drops onto the *same* functional skeleton (region diamond, HSR spine, Booking deck + row, per-region
> vendor deck + slot + market deck + discard, the Closing-Time counter) without moving a single play position.
>
> **What this board is (read first — V7 · v3):** the **neutral shared table** for **3–6 players**, read
> **upright from any seat** (one orientation, no across-the-table mirror). The board is **DOUBLE-SIDED and
> flips at dusk** — so **each face shows ONLY that phase's components**; the other phase's decks are in the
> box, not on the table. The 4-region **diamond** is the neutral shared map: **北 NORTH top · 南 SOUTH
> bottom** sit on the vertical **HSR spine** (a drawn N↔S double-rail); **中 CENTRAL · 東 EAST** flank left
> and right. Each region carries its own **face-up vendor slots** + a **MARKET deck**. The clock is
> **DECK-DRIVEN**: a central **開團 Booking** deck feeds a shared **face-up Booking row** (the sole prize
> row). **Per-player instruments are NOT on this board** — the **Followers dial** and the **成團 / 取消**
> piles live on each **character board**.

## The v3 redesign (CD steer 2026-08) — what changed from the first functional render

1. **SINGLE-PHASE PER FACE.** The DAY face carries ONE **DAY 開團 Booking deck** + the shared face-up
   Booking row, the day vendor slots per region, and the day MARKET deck per region — **nothing night**.
   The NIGHT face carries the night equivalents only. The old "DAY deck + NIGHT deck both shown on one
   face" is gone. The day/night STATE reads from the **whole-board chrome** (warm gold ↔ lantern-neon) +
   the phase badge (sun ☀日 / moon ☾夜), never from a clock position.
2. **TEXTLESS · ICON-ONLY SPACES.** Every play position is a **space with one small drawn ICON** of the
   component that goes there — no sentences, no dev captions, no mm labels, no legend, no setup table. See
   the icon vocabulary below. The only characters on the board are the board **title** (identity) and the
   compact **繁體 region glyphs** (▲北 / ◆中 / ●南 / ■東). The region badges carry **NO signature-ingredient
   chips** (removed, CD steer — players **DISCOVER** each region's foods through play, via the market decks).
   **No English words** on play positions.
3. **Followers 粉 + Trending 爆紅 are OFF the board.** Those tokens sit loose on the table; the reclaimed
   space became open warmth.
4. **BARE HSR.** No **停** badge and no "played onto the HSR track" label. Just the double-rail spine with a
   **stop node at each end** (北 / 南) and a small **train icon** mid-spine. The Scheduled-Maintenance EVENT
   card is simply **placed on the track** — self-evident, no printed marker or slot. **(There is NO 停 slot
   — that language is retired everywhere in this doc.)**
5. **WARMTH underlay.** Soft **region colour-zones** (each panel tinted its region hue) over a stylised
   **island of Taiwan** underlay + a **gentle central glow** — warm gold by day, lantern-neon by night.
   Region identity colours stay warm in BOTH faces; only the chrome flips. Keeps the house hand (bold
   vector, night-market palette, the **inner gold hairline frame**) so it matches the character boards.

### The icon vocabulary (bg-infodesign owns this — one symbol, one meaning, everywhere)

| Play position | Icon (all DRAWN — no font glyphs, no tofu) | Dual-code |
|---|---|---|
| **Vendor deck** (face-down, feeds the slot) | a **face-down deck** (offset stack) badged with the **market-stall glyph** | region **colour** + stall shape; solid=deck |
| **Vendor slot** (face-up vendor to claim) | card-exact **dashed footprint** + a **market-stall glyph** (scalloped awning + counter) | region **colour** + region **emblem** carried by the panel; empty=dashed |
| **Booking deck** (開團, face-down) | a **face-down deck** (offset stack) badged with a **ticket** (boarding-pass stub) | booking **blue** + ticket shape; solid=deck |
| **Face-up Booking** (the shared row) | a **face-up card** (light card + folded corner) badged with a **ticket** | booking **blue** + ticket; light card + folded corner = face-up |
| **MARKET deck** (region ingredients + events, face-down) | a **face-down deck** badged with a **steaming bowl** | region **colour** + bowl shape (distinct from the ticket) |
| **Market discard** (spent ingredients/events) | a **dashed, greyed face-up footprint** (smaller) badged with a **bowl + ↻ cycle arrow** — reshuffles when the deck empties | region **colour** + bowl + cycle; the ONLY deck that recycles |
| **HSR line** | double-rail spine + **stop node** at each end + a **train glyph** mid-spine | steel colour + rail/train shape |
| **Region identity** | coloured header badge: **emblem + single 繁體 glyph** (▲北 ◆中 ●南 ■東) | **colour + emblem + 繁體** (triple-coded WHERE) |

Rationale: face-down **decks** (solid, coloured) vs empty **slots** (dashed, light) are told apart by
fill/outline; **ticket** (bookings) vs **bowl** (ingredients/market) tells the two deck TYPES apart by
shape, not colour; region **emblem + colour + 繁體** triple-codes every region so colour-blind players
never rely on hue. The board is legible at table distance and Screentop zoom with zero reading.

### Vendor-slot count on the board (RESOLVED, CD steer)

The board prints a **FLAT single face-up vendor slot per region.** The per-count slot scaling (5p adds a 2nd
South slot, 6p a 2nd North) is a **setup-rules thing and stays OFF the board** — the CD's call: no per-count
clutter, no gate chips. The face-up count data still lives in `components/map.json` (`vendor_slots`); it is
simply not painted. Each region shows one dashed stall slot, **fed by its own face-down vendor deck** (see
the icon table).

> **→ bg-rulebook:** the **setup-by-player-count table** (Booking-deck sizes, vendor slots N/C/S/E,
> Followers supply per count) and the **how-to-read legend** were REMOVED from the board and must live in
> the **rulebook / player aid** instead. The data is in `components/map.json`
> (`booking_deck_sizes`, `vendor_slots`, `followers_supply`).

> **→ Closing-Time cue (RESOLVED, CD steer):** the board now carries a small **bottom-right round-counter**
> — NOT a claims track. On the **DAY** face it's a 1→2→3 round track with the die roll-point flagged per
> player count (3人 at round 2, 4–6人 at round 3) and a reset loop ("advance each round → roll at your flag →
> reset"); on the **NIGHT** face it's a bare **die + ↻ cycle** icon (rolls every round). Icon-only, no
> descriptive text (the rulebook carries the how-to). Cadence is read data-driven from `map.json`
> `vendor_clock.track_length`. No clock/claims track (retired) — this small counter is the only Closing-Time
> mark on the board.

---

## Shared art direction (unchanged — for the future human-illustrated board)

> The warm night-market palette (lantern vermilion `#D64545` / jade teal `#1F8A7A` / golden amber
> `#E6A930` / dusk indigo `#26324D` on bao-paper cream `#F7F1E3`); the day face = warm dawn/gold chrome,
> the night face = festive lantern-**neon** (lavender/magenta) — *neon glow, never a cold or red alarm
> register*. **Region identity colours stay warm in BOTH faces** (only the chrome flips) — hold that.
> Secular only (no temple/deity/ghost-month motifs). Taiwan is the **beloved**, celebrated *with* not
> laughed *at*; the island is a living subject, never passive exotica.
>
> **Binding legibility rails (bg-infodesign — do NOT let art break these):** every region stays
> dual-coded **colour + emblem + 繁體** (▲北 / ◆中 / ●南 / ■東); the day↔night beat stays readable as
> **sun→moon + chrome flip**, never colour alone; illustration is a **backdrop/vignette behind** the
> functional zones — the icon spaces (vendor slots, region market decks, the Booking deck + face-up
> Booking row, the HSR spine + stop nodes) must stay high-contrast on top of any art (drop a translucent
> scrim under an icon if a painted area would eat contrast). Art serves the at-a-glance read, never
> buries it.

## [FIG-MAP-ISLAND] — the Taiwan-island backdrop (behind the diamond)
- **Where:** the central diamond area behind the four region panels + the HSR spine. A soft, stylised
  **island of Taiwan** motif tying the four regions into one place — a gentle relief map (Central
  mountains, western plain, east coast), not a literal atlas. The v3 code render already lays a faint
  island silhouette + a warm/neon glow here; the illustrated version replaces it at higher fidelity.
- **Tone:** a warm travel-poster / vintage-tourism feel. Dusk light on the day face; lantern-neon shimmer
  at night.
- **Neutral / any-seat:** compose so it reads **upright from every seat** — no top/bottom hero orientation.
- **Keep clear:** the HSR spine (a drawn double-rail N↔S) with its two **stop nodes**, and the region
  adjacency connectors must read on top — treat the island as a low-contrast underlay. **No 停 marker** and
  **no card slots/boxes/grid** in the art (the code draws the functional spaces on top).

## [FIG-MAP-NORTH] · [FIG-MAP-CENTRAL] · [FIG-MAP-SOUTH] · [FIG-MAP-EAST] — the four region vignettes
- **Where:** a small illustrated vignette in each region panel's ground, behind its face-up vendor slots
  and its market deck. North is **top**, South **bottom** (both on the HSR spine); Central and East flank.
- **Direction (one signature scene each, dish-typed & generic — NEVER a real named business):**
  - **北 NORTH (Taipei / Meat 肉 signature · vermilion ▲):** a capital night-market lane, steam off a
    pork-bun cart; this panel is the **common START (台北 Taipei)** for every agent — carry a subtle
    **home-base / departure** cue (every agency's tour sets off from here).
  - **中 CENTRAL (Tea 茶 signature · jade ◆):** tea terraces + a 手搖飲 hand-shaken-drink stand.
  - **南 SOUTH (Seafood 海鮮 signature · amber ●):** a Tainan/Kaohsiung quayside seafood counter (a generic
    **海鮮 Seafood** scene — not a single displaced dish; the old oyster-omelette scene was retired).
  - **東 EAST (Pantry 糧 signature · indigo ■):** the Hualien–Taitung coast/valley, rice + bamboo-tube fare.
    **Indigenous-forward — the paid Taiwanese/Indigenous consultant sign-off binds here** (dish, naming,
    framing) BEFORE art; warm, specific, dignified, never exotic-punchline; **no tribal iconography** in any
    interim placeholder.
- **Keep clear:** the region header badge (emblem + 繁體), the vendor deck + slot + market deck + discard
  footprints per region, the Booking deck + row, and the bottom-right Closing-Time counter.

## [FIG-MAP-FRAME] — the night-market border (carries the day/night chrome)
- **Where:** the outer frame / margins of the whole board.
- **Direction:** a string-of-lanterns / hand-painted stall-signage border that frames the table as a
  night-market street. This border is the **primary day/night STATE cue**: warm **gold bulbs + a rising
  sun** on the day face, glowing **lantern-neon + a moon** on the night face. Warm in both; only the chrome
  flips. This is the piece that makes the board a *stylish centrepiece* rather than a schematic.
- **Neutral / any-seat:** a continuous border with no single "front".
- **Keep clear:** the title band, the central Booking deck + face-up Booking row, and the region panels.

> **Retired figure codes:** the old **[FIG-MAP-CLOCK]** (numbered day→night clock rails on the long edges)
> is **GONE** — V7 has no printed claims-clock track (the beat is the two 開團 decks + the 黃昏 DUSK / 末班車
> LAST TRAIN boundary cards). The old **停 Scheduled-Maintenance slot/badge** is **GONE** too — the HSR
> spine is bare and the event card is simply placed on the track.

---

### Notes for the illustrator / bg-prototyper
- The functional render is the **ground truth for positions** — paint to the zones as laid out; do not move
  a vendor slot, market deck, the Booking deck/row, the HSR spine, or a stop node.
- Two **faces** ship, one per side (`map-day.png` / `map-night.png`) — the board is double-sided and flips
  at dusk. Deliver art that recolours cleanly for both, or two passes sharing one line-art base.
- **Read from any seat.** No orientation-specific hero framing.
- The board is **textless**: don't add printed labels, mm captions, legends, or a setup table (those live in
  the rulebook). Region identity is **colour + emblem + 繁體** only.

---

## AI mock-up prompts (playtest props — NOT final art)

> **Playtest prop only** — permitted so testers feel the island's warmth on the table during manual
> playtesting. **Final art stays human-illustrated; NO AI final art.** Each PNG is a **MOCKUP** → save to
> the **gitignored** `games/travel-agents/build/mockups/`, filename = the FIG code; **never committed,
> never moved to `exports/`, never shipped.**
>
> **SOFT & SIMPLE direction (CD steer 2026-08).** The board is a **backdrop underlay**: the functional
> icon spaces are rendered by code and sit **on top**, so the art stays **quiet and open** — mostly **soft
> colour + a gentle glow**, four regions as soft **colour-zones**, a **single clean HSR line** down the
> spine, a **clean open centre**, and only **ONE or TWO tiny accents.** Region identity colours stay
> **warm in BOTH faces** (only the light flips). **Double-sided:** a matched **DAY** and **NIGHT** face —
> generate the day face first, then reference it for the night face so they register back-to-back. Compose
> **upright from any seat.** **Secular only.** The paste-ready DAY + NIGHT prompts live in
> `art/mockup-kickoffs.md`.

- **`FIG-MAP-ISLAND-day` / `FIG-MAP-ISLAND-night` — the whole-table backdrop (the main warmth prop).**
  A softly stylised **island of Taiwan** with the four regions as **soft colour-zones** (北 top / 中 left /
  南 bottom / 東 right) and a single clean **HSR line** down the N↔S spine. **Add only ONE or TWO tiny
  accents** (e.g. one paper lantern + one little steaming bowl) — **no crowds, no people, no buildings, no
  dense stalls, no lantern strings, no card slots/boxes/grid, no 停 marker, no text.** Keep the whole
  **centre clean and open** (cards get placed on top). **DAY:** warm dawn glow, soft gold. **NIGHT:** soft
  lantern-neon glow + a moon, region colours stay warm — only the light flips.
  *Closing: one image, framed 2280×1680, ~1.36:1, full background, high-res PNG (not SVG); reads upright
  from every seat; save build/mockups/FIG-MAP-ISLAND-day.png (then the matched night as
  FIG-MAP-ISLAND-night.png).*
- **Per-region vignettes** (`FIG-MAP-NORTH` etc.) are **NOT part of the soft/simple mock-up** — the regions
  read as plain colour-zones. (The richer per-region briefs above remain options for a future
  human-illustrated board only, consultant-gated where East is concerned.)
