# Accessibility & Inclusive Design

Making the game **perceivable, learnable, manipulable, and affordable by more people** — without diluting
the design. Accessibility is a *quality* lever, not a charity add-on: the same fixes that let a
colour-blind player read the suits make the table clearer for everyone, and a game that's legible at a
glance teaches faster and plays smoother. Owned by **`bg-access`** (a guardian, like `bg-theme` and
`bg-elegance`); the objective checks live in `tools/access/check_access.py`.

Why it matters here specifically: this studio ships **suit-coloured card games on Screentop.gg**, and its
signature is **constrained-communication co-op** — both sit directly on accessibility axes (colour +
communication). Getting this right costs almost nothing at the data stage and is expensive to retrofit
after art.

## The framework — Meeple-Centred Design (Heron et al.)

The recognised tabletop standard (the *Meeple Like Us* teardowns; Heron, Belford, Reid & Crabb, *The
Computer Games Journal*, 2018; expanded in *Tabletop Game Accessibility: Meeple-Centred Design*, Routledge
2024). It grades a game across **eight impairment categories**, then adds an **intersectional** overlay.
Use it as the checklist; grade each category **pass / watch / fail** for the current build.

1. **Colour blindness** — is any information carried by **colour alone**? Suits, player colours, score
   tokens, faction identity. ~8% of men are colour-blind. *The single most common failure — and the most
   computable.* Fix = **redundant encoding**: colour **+** shape/emblem **+** (where it fits) position or
   label. Never colour as the sole channel.
2. **Visual / low-vision & blindness** — text-independence, tactile differentiation, contrast, font size
   at arm's length, board "presence" readable by touch. On Screentop, contrast and font size dominate;
   for physical, tactile tokens.
3. **Cognitive** — split into **fluid** (in-the-moment working memory, simultaneous constraints, tracked
   state) and **crystallised** (learned rules, iconography recall). This is where *elegance and
   accessibility converge* — every rule/keyword/exception `bg-elegance` cuts also lowers cognitive load.
4. **Emotive / emotional** — theme distress, take-that, elimination, loss-of-agency, tilt. (Cross-ref
   `bg-critic`'s feel-bad hunt.)
5. **Physical / motor** — gross and fine motor: fiddly components, card-holding, precise placement,
   real-time manipulation, reach. *Real-time and dexterity mechanics trade fun for motor load — a
   deliberate choice, not an accident.*
6. **Communication** — reliance on speech/hearing (verbal negotiation, sound cues, "no-talking" rules).
   **This overlaps the studio's constrained-comms co-op directly** — a "no table talk" rule is a design
   feature *and* a communication-accessibility consideration; make sure the required signalling channel
   has a non-verbal form.
7. **Socioeconomic** — price, language dependence, replacement-part cost, cultural inclusion. Ties to the
   **minimal-cost / route-to-market** goal: a cheap, small-box, low-text game is also the more accessible
   and more inclusive one. (Cross-ref `funding-and-route-to-market.md`, `representation-and-sensitivity.md`.)
8. **Intersectional** — where two needs **conflict**. The toolkit's key insight: fixes aren't free.
   "Read it aloud" helps low-vision but fails a communication-impaired player; "symbols not text" helps
   low-vision/low-literacy but can raise crystallised-cognitive load (another icon to memorise). Flag the
   conflicts; don't pretend one fix serves all.

## What's computable (and already wired) vs. what's judgement

**Objective — `tools/access/check_access.py` checks these from data + theme:**
- **Colour-blind suit separability.** Simulates protanopia / deuteranopia / tritanopia (Machado 2009
  matrices) on the theme's suit palette and measures perceptual distance (CIELAB ΔE). Flags any two
  **suits used by the game** that are distinct in normal vision but **collapse** under a CVD type.
- **Dual-coding.** Because the theme gives each suit a colour **and** an emblem, the tool passes a
  colour-collision *only if the colliding suits still differ by emblem* (redundant channel). Two suits
  that share an emblem **and** collide on colour = a hard fail.
- **Text contrast.** WCAG contrast ratio of ink/text vs page background; flags < 4.5:1 (body) / < 3:1
  (large).

**Judgement — `bg-access` reviews these against the checklist (not auto-checkable):**
- Font size at physical/on-screen size (aim ~**2–3 mm** glyph height at arm's length; never 1 mm).
- Text-independence & reading level (can a non-reader / ESL player play from icons + aid?).
- Motor load (fiddliness, real-time, precise placement) vs. the intended audience.
- Communication channel has a non-verbal option where the design restricts talk.
- Emotive load (elimination, take-that) — cross-ref `bg-critic`.

## The redundant-encoding rule (the one to internalise)

> **Colour is a bonus channel, never the only channel.** Every piece of game-critical information must be
> distinguishable **without** relying on colour — via shape, emblem, icon, pattern, position, or text.

This is now an industry expectation, not a nicety (Mattel committed 80% of its portfolio to
colour-blind-accessible by end of 2024 — re-verify live). It's cheap at the data stage: the render theme
already carries a per-suit **emblem**, so keep emblems **distinct per suit** and you've dual-coded for free.

## Quick self-check (run every design/data pass)
- [ ] No information is carried by colour alone (suits/players/tokens all have a shape/icon/label too).
- [ ] `check_access.py` passes: no CVD suit collision without a distinct emblem; text contrast ≥ 4.5:1.
- [ ] Body text ≥ ~2–3 mm (physical) / legible at Screentop zoom; player aid readable at a glance.
- [ ] A non-reading / ESL player could play from icons + aid (text-independence).
- [ ] Motor/real-time demands match the intended audience (or are a deliberate, flagged trade).
- [ ] If the design restricts talking, the required signalling has a non-verbal form.
- [ ] Price/component footprint keeps it affordable (socioeconomic ↔ elegance ↔ cost).

**References to re-verify live:** *Meeple Like Us* masterlist and teardown methodology; the Machado et al.
(2009) CVD matrices (used by the tool); WCAG 2.x contrast thresholds.
