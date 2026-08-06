# Beacon — Information Design Review (guardian parse-check)

*Owner: `bg-infodesign`. Theme: `nautical`. Reviewed against real renders in `build/png/*` and
`build/player-aid.png`, the data in `components/*`, and the layout in `tools/cards/{themes.py,build_cards.py}`.
Guardian sweep pass — review only, no edits made.*

**Verdict: near-pass.** The dual-coding foundation is genuinely good (every suit carries colour +
shape + word; every value carries numeral + pip-count). Three things flag: one is a hard render bug
(the value-0 Signal prints blank), one is a cross-component icon mismatch (rulebook emblems ≠ card
emblems), and one is a hierarchy inversion (flavour name is the hero; the load-bearing *value* is a
small corner number). None block playtesting; all three are cheap upstream fixes.

---

## 1. Icon system (symbol → meaning)

Suits are keyed off the card's `type` column by the `nautical` theme; value is drawn as a pip-row +
numeral by `build_cards.py`.

| Symbol (as rendered) | Colour | Means | Where | Status |
|---|---|---|---|---|
| **Hexagon** ⬡ | copper `#b5651d` | Cargo suit | header dot, type line, value pips | OK — distinct |
| **Diamond** ◆ | teal `#2a7f8f` | Passenger suit | header dot, type line, value pips | OK — distinct |
| **Triangle** ▲ | deep red `#7a2e3b` | Naval suit | header dot, type line, value pips | OK — distinct |
| **Beam** ◉ (lamp glyph) | brass `#c68a2b` | Signal card | header dot, type line, value pips | OK — distinct from the 3 ship shapes |
| **Numeral** (bottom-right) | suit colour | card value (ship worth / signal strength) | bottom band | OK *except value 0 (see F1)* |
| **Pip row** (bottom-left) | suit colour | value, redundantly, as N suit-shapes | bottom band | OK *except value 0 (see F1)* |

**Dual-coding is solid.** Suit = colour **and** shape **and** the word (`CARGO`/`PASSENGER`/`NAVAL`/`SIGNAL`),
so it survives colour-blindness and greyscale — hand the perceptual floor to `bg-access`, but the
shape/label channel it needs is already present and consistent. Value = numeral **and** pip-count, so
it's readable even if one channel is missed. No un-iconed keyword; no unused icon. Good restraint —
the vocabulary is exactly four suit marks + a number, nothing bloated.

### Gaps / overloads

- **F1 — the value-0 Signal renders BLANK (hard bug).** `build_cards.py` guards the value row with
  `if vn > 0:`, so **Dark Lantern (G0)** prints no numeral and no pips — a blank bottom edge where
  every other card shows a bold number. This is the one card whose *whole point* is "value 0 = pick a
  ship first but hand the Tide to your rival." Under the squint test a blank-bottomed card reads as
  *faceless* — cut-off, a card back, or an error — not as "zero." The lowest card in a blind-commit
  game must announce itself the loudest, not the least. **Fix: draw the `0` (and ideally a distinct
  "empty lantern" pip) explicitly.**
- **F2 — rulebook emblems ≠ card emblems (cross-component mismatch).** `design/rules-draft.md` names
  the suits `⚓ Cargo, ☺ Passenger, ⚔ Naval`, but the cards render hexagon / diamond / triangle. A
  player who learns "anchor = Cargo" from the rules then hunts for an anchor that isn't on any card.
  "One symbol, one meaning, *everywhere*" is broken across components. **Fix: pick one language.**
  Either update the rulebook/aid glyphs to the geometric shapes (cheap, keeps the clean abstract
  look), or — better for the felt theme — swap the theme's `emblem` values to nautical marks
  (anchor / figure / crossed-oars-or-cannon) and use those glyphs everywhere. Coordinate with
  `bg-theme`: right now the "nautical" suits are abstract geometry, which reads clean but leaves felt
  identity on the table.
- **No overloads.** No symbol is doing two jobs; the four marks stay in their lanes.

---

## 2. Hierarchy & layout (per component type)

Current template order of visual weight: **① Name** (50px, white on saturated colour band, top) →
**② Suit** (28px, muted grey italic caps) → **③ Value** (46px numeral, suit-colour, one bottom corner
+ small pips in the other).

### Ship cards
- **Intended reads for play:** value (compared every round, and the thing you're collecting) and suit
  (sets/runs/convoy) are load-bearing; the name (`The Deepkeel`, `Ferry Wren`) is pure flavour and
  **never** matters mechanically.
- **Actual hierarchy is inverted.** The mechanically-irrelevant *name* is the single largest,
  highest-contrast element (reverse-out white on the colour band, top of card). The *value* — the hero
  of every comparison — is the smallest top-level element, tucked in a bottom corner. The colour band
  does carry the suit strongly, which rescues suit-reading; but value is under-weighted for how often
  it's needed.

### Signal cards
- **Same layout, and the inversion bites harder here.** The entire game is "which *value* do I commit,
  blind?" On a Signal the value *is* the decision — yet `Blinding Flare` (name) is the hero and `5` is
  a corner number. A fanned hand of six Signals should let you read the six values instantly; right now
  you read six flavour names first.
- Signals correctly share the ship frame/pip system (learn-once), and the brass band + beam glyph keep
  them from being mistaken for ships. Good. The 0-blank (F1) is the exception that breaks the set.

### Player aid
- **Strong.** Sectioned by cadence (Each round / Each night / Scoring / The question every round),
  short lines, keywords (HIGHER / LOWER / Tide / First Keeper) styled by caps, and it closes on the
  single core decision. A returning player can run a full round off this without the rulebook — which
  is the whole job. Only nit: it leans on the words `Cargo/Passenger/Naval` and never shows their
  suit glyphs, so it can't help a player map a word to the mark on the card (compounds F2). Adding the
  three suit glyphs next to the Convoy line would close the loop.

### Tide track / tokens
- Not deeply auditable from data here, but the track is the most-watched shared object; ensure the two
  harbour ends are labelled *and* colour/shape-anchored to each keeper, and the centre space is
  unmistakable (the "nobody scores" state). Flag for a look once rendered at table distance.

---

## 3. At-a-glance / squint test

- **Suit — PASS.** The saturated header band is the biggest thing on the card and each hue is far
  apart; even blurred, copper/teal/deep-red/brass separate cleanly, and the shape backs it up.
- **Value — MARGINAL.** The numeral is bold but small and lives in a single bottom corner at lower
  contrast (suit-colour on pale) than the name (white on saturated). Pips help at close range but are
  16px. Across a table or at Screentop zoom, value is legible-if-you-look, not announced.
- **Value 0 — FAIL (F1).** Blank bottom; does not read as a number at all.
- **Name — dominates but is noise.** The one element the eye lands on first is the one that never
  affects a decision.

**Edits to make it pass (all upstream in `build_cards.py` / `themes.py`, regenerate via `make.sh`):**
1. **F1:** remove the `if vn > 0` gate — always render the value; give `0` an explicit numeral and a
   distinct "unlit" pip so Dark Lantern reads as *deliberately zero*.
2. **Promote value:** add a **top-corner value index** (playing-card style) — a large numeral in the
   header band, opposite the name, in white for max contrast. This makes a fanned hand of Signals and
   a row of Channel ships readable by value at a glance without touching the flavour layout.
3. **F2:** unify suit glyphs across rulebook/aid and cards (one decision — see below).

---

## 4. Decision for the human — the one change to make now

The value-0 blank (F1) is an unambiguous bug: just fix it, no decision needed. The judgment call is
**how far to promote value / how to unify the suit marks.** Pick one:

- **A — Value index + keep abstract suits (fastest, recommended).** Add a big white value numeral in
  the top corner of every card, fix the 0-render, and change the *rulebook/aid* glyphs to match the
  existing hexagon/diamond/triangle. Ships and Signals become value-first; icon language becomes
  consistent everywhere. Pure template/text edits, no art, no `bg-theme` round-trip. Best serves the
  squint test for the least effort.
- **B — Value index + nautical emblems (best felt identity).** As A, but instead of documenting the
  geometric shapes, swap the theme's `emblem` values to true nautical marks (anchor / passenger /
  naval) and use them everywhere — cards, pips, rulebook, aid. Strongest theme payoff; costs a small
  `bg-theme` coordination and glyph-drawing pass, and you must re-verify the new marks stay distinct
  at pip size and in greyscale.
- **C — Minimal (fix the bug only).** Just render the `0`; leave hierarchy and the rulebook mismatch
  as-is. Unblocks the demo but leaves value under-weighted and the icon key inconsistent — not
  recommended beyond a stopgap.

**Recommendation: A now** (cheap, closes the squint-test gap and the icon mismatch in one template
pass), with **B** as the follow-up when `bg-theme` next touches the felt identity — the abstract
geometry is legible but is leaving the nautical theme unspent on the suits.
