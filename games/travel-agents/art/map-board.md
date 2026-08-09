# The Shared Table Map — illustration brief

> **Briefs only. NO AI final art** (studio rail — `designer-profile.md`). Direction for a **human
> illustrator**; the board renders as a functional, labelled layout (`build_board.py --type regionmap`,
> two states via `--phase day|night`) until real art lands. This brief names the figure codes the board's
> composition RESERVES art space for, so the illustrated centrepiece drops onto the *same* functional
> skeleton (zones, clock rails, HSR spine, supply corners) without moving a single play position.
>
> **What this board is (read first):** the shared 2-player TABLE, oriented **across the table** — two
> agents seated on the long edges (top & bottom). The layout is symmetric about the horizontal mid-line;
> the day→night **vendor-claims clock is built into BOTH long edges** (mirror-rotated so each seat reads it
> upright); the 4-region **diamond** (北 top · 中 left · 東 right · 南 bottom) is the neutral shared map in
> the middle, with the **HSR spine** + Scheduled-Maintenance 停 slot down the centre; the four **corners**
> carry shared supplies (Tour-Ticket decks, ingredient wells, Buzz + ★, a read-me legend). Per-player
> instruments (Reach 及, Tours-Completed 好評, 成團/取消 piles) are NOT here — they live on the character
> boards.
>
> **Shared direction:** the warm night-market palette (lantern vermilion `#D64545` / jade teal `#1F8A7A` /
> golden amber `#E6A930` / dusk indigo `#26324D` on bao-paper cream `#F7F1E3`); the day state = warm
> dawn/gold chrome, the night state = festive lantern-**neon** (lavender/magenta) — *neon glow, never a
> cold or red alarm register*. **Region identity colours stay warm in BOTH states** (only the chrome flips)
> — hold that. Secular only (no temple/deity/ghost-month motifs). Taiwan is the **beloved**, celebrated
> *with* not laughed *at*; the island is a living subject that pushes the agents around, never passive
> exotica to be catalogued.
>
> **Binding legibility rails (bg-infodesign — do NOT let art break these):** every region stays
> dual-coded **colour + emblem + 繁體** (▲北 / ◆中 / ■東 / ●南); the clock's day→night must stay readable as
> **sun→moon + position** (not colour alone); illustration is a **backdrop/vignette behind** the functional
> zones — vendor card slots, token wells, deck backs, clock cells and their numerals must stay high-contrast
> on top of any art (drop a translucent scrim under text if a painted area would eat contrast). Art serves
> the at-a-glance read, never buries it.

---

## [FIG-MAP-ISLAND] — the Taiwan-island backdrop (behind the diamond)
- **Where:** the central diamond area behind the four region panels + the HSR spine (roughly the middle
  third of the board). A soft, stylised **island of Taiwan** motif tying the four regions into one place —
  a gentle relief map (Central mountains, the western plain, the east coast), not a literal atlas.
- **Tone:** a warm travel-poster / vintage-tourism-stamp feel (the passport/boarding-pass identity). Dusk
  light in the day state; lantern-neon shimmer at night.
- **Keep clear:** the HSR spine (a drawn double-rail runs N↔S), the 停 HSR-CLOSED reminder slot, and the
  ring adjacency lines must read on top — treat the island as a low-contrast underlay.

## [FIG-MAP-NORTH] · [FIG-MAP-CENTRAL] · [FIG-MAP-EAST] · [FIG-MAP-SOUTH] — the four region vignettes
- **Where:** a small illustrated vignette in each region panel's header/ground, behind its signature
  ingredient chips + its face-up vendor slots.
- **Direction (one signature scene each, dish-typed & generic — NEVER a real named business):**
  - **北 NORTH (Taipei / pork · vermilion ▲):** a capital night-market lane, steam off a pork-bun cart; this
    panel is the **common start (台北 Taipei)** — carry a subtle "head-office / departure" cue.
  - **中 CENTRAL (tea · jade ◆):** tea terraces + a 手搖飲 stand; the region that *exports* tea (胡椒餅, 麻糬).
  - **東 EAST (rice · indigo ■):** the Hualien–Taitung coast/valley, rice + bamboo-tube fare. **Indigenous-
    forward — the paid Taiwanese/Indigenous-consultant sign-off binds here** (dish, naming, framing) BEFORE
    art; warm, specific, dignified, never exotic-punchline.
  - **南 SOUTH (seafood · amber ●):** a Tainan/Kaohsiung quayside, oyster omelette on the griddle.
- **Keep clear:** the region header banner (emblem + name + 繁體), the START·台北 pill on North, and the
  card/token footprints.

## [FIG-MAP-CLOCK] — the day→night clock rails (both edges)
- **Where:** the two full-width rails hugging the top & bottom edges (the bottom one 180°-mirrored).
- **Direction:** a horizon that reads **dawn → dusk → night market** left-to-right — warm sunrise gold at
  START (0), the sun sinking to the **黃昏 DUSK** gate (5), lantern-neon night to the **末班車 LAST TRAIN**
  gate (10). A drawn **sun** anchors the day end, a **moon/lanterns** the night end.
- **Keep clear:** the 11 numbered clock cells, the DUSK / LAST TRAIN / START call-outs, and the marker flag
  must stay legible on top — art is a thin ribbon behind the cells, not over them.

## [FIG-MAP-FRAME] — the night-market border
- **Where:** the outer frame / margins of the whole board.
- **Direction:** a string-of-lanterns / hand-painted stall-signage border that frames the table as a
  night-market street. Warm in both states (gold bulbs by day, glowing neon by night). This is the piece
  that makes the board a *stylish centrepiece* rather than a schematic.
- **Keep clear:** the title band and the corner supply zones.

---

### Notes for the illustrator / bg-prototyper
- The functional render is the **ground truth for positions** — paint to the zones as laid out; do not move
  a slot, well, deck, clock cell, or the HSR spine.
- Two states ship (`map-day.png` / `map-night.png`). Deliver art that recolours cleanly for both, or two
  passes sharing one line-art base.
- Real component footprints are labelled in mm on the render (card 63×89mm, Ø20mm tokens, Ø12mm Buzz, 18mm
  ★, 15mm pawns); the final board is intended at **≈ 570 × 400 mm**. Keep painted detail from crowding the
  physical piece footprints.

---

## AI mock-up prompts (playtest props — NOT final art)

> **Playtest prop only** — permitted so testers feel the island's warmth on the table during manual
> playtesting. **Final art stays human-illustrated; NO AI final art.** Each PNG is a **MOCKUP** → save to
> the **gitignored** `games/travel-agents/build/mockups/`, filename = the FIG code (e.g.
> `FIG-MAP-ISLAND.png`); **never committed, never moved to `exports/`, never shipped.**
>
> **Each prompt = STYLE ANCHOR (paste verbatim from `art/art-style.md`) + the subject below + the closing
> line.** The board is a **backdrop underlay**: the functional zones (region panels, HSR spine, clock
> cells, supply corners, token wells) are rendered by code and sit **on top** — so keep the mock-up
> **low-contrast / calm where the play furniture lands** and save the warmth for the frame, the island
> relief, and the region vignettes. Region identity colours stay **warm in BOTH states** (only the chrome
> flips). **Secular only.**

- **`FIG-MAP-ISLAND` — the whole-table backdrop (the main warmth prop).** A warm travel-poster view of a
  stylised **island of Taiwan** tying four regions into one place — a gentle relief map (Central mountains,
  the western plain, the east coast), a drawn **HSR double-rail** running N↔S down the spine, a
  **string-of-lanterns night-market border** framing the table like a night-market street. Four soft
  region vignettes glowing at the diamond points: **北 NORTH** a Taipei night-market lane with a pork-bun
  cart (the START·台北 hub — a subtle "head-office / departure" cue); **中 CENTRAL** tea terraces + a
  hand-shaken-drink stand; **東 EAST** the Hualien–Taitung coast/valley with rice + bamboo-tube fare;
  **南 SOUTH** a Tainan/Kaohsiung quayside with an oyster omelette on the griddle. Warm dusk-gold light,
  the whole thing glowing and inviting. **Generate a warm-DAY pass and a lantern-NEON-NIGHT pass sharing
  one composition** (only the chrome flips). *Closing: framed for a 2280×1680 board, ~1.36:1 aspect, full
  background, keep the centre + edges calm for the play furniture, save as build/mockups/FIG-MAP-ISLAND.png
  (night pass: FIG-MAP-ISLAND-night.png).*
- **Optional per-region vignettes** (`FIG-MAP-NORTH` / `FIG-MAP-CENTRAL` / `FIG-MAP-EAST` / `FIG-MAP-SOUTH`)
  — if a tighter mock-up of one region's warmth helps, generate the single signature scene above for that
  region, **dish-typed and generic, NEVER a real named business.** East is Indigenous-forward — keep it
  **generic and respectful, no tribal iconography, consultant-gated** (placeholder only). *Closing: framed
  as a soft region vignette, transparent or simple background, save as build/mockups/FIG-MAP-<region>.png.*
