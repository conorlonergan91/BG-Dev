# Beacon — Accessibility Review (bg-access guardian sweep)

> Reviewed: 2026-08-06 · Theme: `nautical` · Build: v0.3 (prototype-ready demo) · Reviewer: bg-access
> Framework: Meeple-Centred Design (Heron et al.) — see `knowledge/accessibility.md`.
> **Verdict: CLEAN PASS.** One soft watch item (dual-coded, functionally moot) + two forward-looking notes. No fix required now.

## 1. Objective checker output

`python tools/access/check_access.py --game games/beacon --theme nautical`

**Colour-blind suit separability — PASS (0 errors).**
- Suits: cargo `#b5651d`/hex · naval `#7a2e3b`/triangle · passenger `#2a7f8f`/diamond · signal `#c68a2b`/beam.
- One WARN: cargo & signal are close in normal vision (ΔE 17), and collapse under deuteranopia (ΔE 11) —
  **but they differ by emblem (hex vs beam), so they're dual-coded → no colour-only collision.**
- Functionally the warning barely bites: `cargo` (a ship suit on the shared Channel) and `signal` (each
  player's private 0–5 hand) live in **different decks and never sit side-by-side needing discrimination**.
  A keeper never has to tell a Cargo ship apart from a Signal card by colour.

**Text contrast — PASS.** ink `#123244` 9.8:1 · text `#16323f` 9.9:1 on the page — both well above WCAG
4.5:1 (body) and 3:1 (large).

Result: **0 errors, 1 warning.**

## 2. Category grades (Meeple-Centred Design)

| # | Category | Grade | Note |
|---|----------|-------|------|
| 1 | Colour blindness | **PASS** | 3 ship suits triple-encoded (distinct colour + distinct shape). Signal strength carried by the **number 0–5**, not brightness/colour. |
| 2 | Low-vision / legibility | **PASS** | Contrast excellent. Watch the numeric glyph at Screentop zoom (see below). |
| 3 | Cognitive | **PASS** | ~1.8 weight, one decision/round, **open hands** (spent Signals face-up = low memory load). |
| 4 | Emotive | **PASS** | Duel with built-in catch-up; blind-commit sting flagged to bg-critic, not an access fail. |
| 5 | Physical / motor | **PASS** | Card play only — no real-time, no dexterity, no precise placement. |
| 6 | Communication | **PASS (N/A)** | Beacon is a **duel**, not a constrained-comms co-op — no required signalling channel to make non-verbal. |
| 7 | Socioeconomic | **PASS** | 36 cards + track + 2 tokens; low-text, icon-driven — cheap, easy to localise. |
| 8 | Intersectional | **PASS** | No hard conflict in the base. One axis to watch (below). |

### Detail on the two that carry the most risk for this studio

**Colour blindness (the suit-coloured-card-game risk) — PASS.**
The three ship suits are the game-critical colour channel, and each is triple-encoded: copper/hex (Cargo),
teal/diamond (Passenger), deep-red/triangle (Naval). Checker confirms no colour-only collision. Crucially,
**Signal strength — the thing the whole blind-commit turns on — is carried by a printed number 0–5**, with
name and brightness metaphor as extra channels; brightness/colour is never the sole cue. Redundant-encoding
rule satisfied. Smallest upkeep: keep suit **emblems prominent** at Screentop zoom so the dual-code survives
zoom-out (see bg-infodesign).

**Communication — PASS / N/A for the base.**
Beacon sits on the **duel** side of the studio's taste, not the constrained-comms co-op side. There is no
"no table talk" rule and no required signal a hearing/speech-impaired player must convey — the hidden info
is *blind commitment*, which is fully accessible. The communication-accessibility check becomes live only
for the **future co-op "Storm" variant** (bible, Modes & scope) — flag it there when it's built.

## 3. Intersectional conflicts

None active in the base. **One latent axis to watch:** *socioeconomic ↔ low-vision.* If the box is ever
shrunk to shave cost (smaller cards / tighter layout), the **Signal number and suit emblem legibility** is
the first thing that suffers — and those two glyphs are load-bearing for colour-blind and low-vision players
alike. Hold the numeric glyph and emblem size when cost-cutting; don't trade them for a smaller card.

## 4. Forward-looking notes (not fixes — log only)

- **Signal glyph at zoom (WATCH, cosmetic):** confirm the `0–5` value renders as a large corner/centre glyph
  on Signal cards and `1–4` on ships — the number is the redundant channel that saves the colour-blind read.
  A rendering/layout item for bg-infodesign, not a data fix.
- **Emblem naming drift (trivial):** rules-draft uses ⚓/☺/⚔ for the suits while `themes.py` renders
  hex/diamond/triangle. Both are distinct-per-suit so it's harmless for access; just keep the teach diagram
  matching whatever the cards actually show.
- **Co-op "Storm" variant:** when built, re-run this review with the **Communication** category live — a
  constrained-comms co-op must give its required signalling a non-verbal form.

## Decision for the human

**None required — this is a clean guardian pass.** No data or theme edit is warranted. Logged for the
record. (The only items above are cosmetic/forward-looking and owned by bg-infodesign / future variants.)
