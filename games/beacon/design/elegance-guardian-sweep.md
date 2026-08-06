# Beacon — Elegance Guardian Sweep

*Guardian pass by `bg-elegance` · 2026-08-06 · review only, no edits made.*

## 1. Budget status — WITHIN BUDGET (clean)

`python tools/complexity/check_complexity.py --game games/beacon`

| proxy | value / budget | status |
|---|---|---|
| rulebook_words | 655 / 900 | ✓ (73%) |
| keywords | 6 / 8 | ✓ |
| exception_words | 1 / 8 | ✓ |
| component_types | 4 / 4 | ✓ (at cap) |
| player_aid_lines | 12 / 16 | ✓ |

Target weight 1.8. **All capped proxies green.** Component types sits at the cap (4/4) but is not over —
worth noting so a future addition doesn't silently push it over. No creep this pass; the v0.3 changes
(scaled Tide bonus, initiative handoff) added depth without adding rulebook words or keywords. Healthy.

## 2. Simplification candidates

Nothing new to cut — the design has already been trimmed through three loop iterations and reads lean.
One standing lever, already flagged by the design itself, not a new find:

- **Run bonus (+2 per 3-consecutive-value run in a suit).** *Cut candidate if playtest says scoring
  feels heavy.* What's lost: a second set-collection axis (suit-completion pull) on top of the Convoy
  bonus. Confidence: medium — do NOT cut on my say-so; it's a live playtest question (design-doc open
  Q3: "do convoy/run bonuses add direction or just scoring overhead?"). How to confirm: A/B sim
  (convoy-only vs convoy+run) via `bg-playtest`, or ask session-1 testers whether they ever chased a
  run. The design doc already names run bonus as "the first cut" if set bonuses feel like too much —
  this just keeps it on the radar. **Do not pre-empt the playtest.**

No redundant rules, single-use exceptions, or components that don't earn their place. The optional Fog
module and Rocks variant are correctly held out of the base — not bloat.

## 3. Rulebook & player-aid clarity — good

Rulebook teaches in play order, goal stated early, warm voice ("whoever last saw the sea"), one worked
intuition per rule (bright = position, dim = cargo). Player aid is one glance, leads with the core
decision ("Grab the cargo… or push the Tide?"). Both are genuinely fun to read. No clarity edits needed.

## 4. Editorial pass — two minor nits, both internal-only (design-doc), zero player-facing errors

Player-facing numbers all cross-check against `components/*`: 24 ships (3 suits × values 1–4, two of
each value — confirmed in `ships.csv`), 12 signals (0–5 ×2 sets, confirmed in `signals.csv`), 36 cards
total, Tide 7 spaces, Convoy +2 / Run +2, Tide bonus 2×spaces (max 6). Rules-draft and player-aid agree.

The only inconsistencies are inside `design/design-doc.md` (internal notes, not a component or the
rulebook), where the v0.3 change didn't fully propagate:

- **Stale Tide economy number.** Economy section (line ~55) still describes the *pre-v0.3 flat* bonus:
  "+3 VP/Night × 3 = up to 9 VP swing." Under the current v0.3 rule (2×|position|, max 6/Night) it's
  **up to 6 VP/Night, up to 18 VP swing over 3 Nights.** This contradicts the same doc's scoring
  section (line ~33, correctly "up to 6"). Low severity — internal only; the rulebook/aid are correct.
- **Keyword casing.** Design-doc lowercases "first keeper" ("the current first keeper") while the
  Keyword elsewhere is capitalised "First Keeper." Trivial; align to the capitalised Keyword.

Neither reaches a physical component, so nothing is print-permanent. Fold both into the next design-doc
touch; no urgency.

## 5. FAQ — disciplined, no action

Four FAQ entries, all genuine ambiguities (open hands, tie resolution, the counter-intuitive dim-grabs
rule, first-keeper on Night 1). None is a recurring-question smell that should become a rule fix. The
dim-grabs entry earns its place because the rule is deliberately counter-intuitive. Keep as-is.

## Decision for the human

**Clean pass — no simplification or budget change needed now.** Nothing to action before session 1.
If you want one tidy-up:

- **A —** Do nothing; ship to playtest. *(Recommended — the game is at target and the nits are cosmetic
  internal notes.)*
- **B —** One-line editorial fix: correct the stale Tide-swing number and "first keeper" casing in
  `design-doc.md` next time it's open.
- **C —** Pre-register the run-bonus A/B as an explicit session-1 question so the standing simplification
  lever gets a real answer.
