# Information Design — graphic design that serves play

The functional visual layer: the **icon language, information hierarchy, and at-a-glance readability** of
every component. This is **graphic design, not illustration** — it's about whether a player can *parse*
the card/board/token in a glance and stay in flow, not whether it's pretty. A gorgeously illustrated game
with bad information design is unplayable; iconography that "boils a rule into one piece of art" is one of
the strongest quiet quality multipliers in tabletop, and bad iconography — sending players back to the
rulebook every turn — is one of the top silent killers of otherwise-good games. (Daniel Solis, *Graphic
Design for Board Games*, 2024.) Owned by **`bg-infodesign`**.

## The three neighbours (keep the lanes clear)
- **`bg-theme`** owns the *felt identity* — art direction, mood, palette, naming (the "aesthetics" leg).
- **`bg-infodesign`** (this) owns *functional legibility* — can you read and act on it fast?
- **`bg-access`** owns *who can perceive it at all* — colour-blind/contrast/legibility floor.
- **`bg-2d-components`** (skill) owns *rendering* — turning data + template into the actual SVG/PNG/PDF.

They overlap (a clear icon system helps all four); coordinate rather than duplicate. Information design is
where "it looks nice" becomes "I know what to do without asking."

## What good information design does
1. **Visual hierarchy** — the eye lands on the most important thing first (cost? name? the effect?), then
   the next. Rank every element on a card by how often a player needs it mid-turn and size/place/contrast
   it accordingly. A flat card where everything shouts is a card where nothing is found.
2. **At-a-glance readability** — the critical info reads from **across the table** (or at Screentop zoom),
   not just in hand. Test by squinting: what survives? That should be the load-bearing info.
3. **An icon *system*, not one-off icons** — a small, consistent visual vocabulary where each symbol means
   exactly one thing everywhere it appears. Icons should **replace** text where they're unambiguous
   (numbers, resources, actions), and defer to text where they'd be cryptic. Every icon earns its place;
   a bloated icon set is its own crystallised-cognitive tax (cross-ref `accessibility.md`).
4. **Consistency & alignment** — same field in the same place on every card; grids, not eyeballed
   placement. Consistency is what lets players stop *reading* and start *scanning*.
5. **Text that's laid out to teach** — effect text short, one idea per line, defined keywords styled
   consistently, worked-example iconography where it beats a sentence.

## The tension with elegance and identity
- **Information density is a budget too.** Every icon, badge, and tracker on a component competes for the
  glance. `bg-elegance` cuts *rules*; `bg-infodesign` cuts *visual clutter* — often the same fight from a
  different angle. If the card needs a legend to read, the design or the layout is too busy.
- **Identity vs. legibility can pull apart.** A gorgeous distressed texture that eats contrast, an
  on-theme font that's hard to read at size, a moody palette that flattens hierarchy — these are where
  `bg-theme` and `bg-infodesign` negotiate. Legibility wins on game-critical info; identity gets the rest.

## The at-a-glance checklist (run on any component pass)
- [ ] **Squint test:** the most-needed info survives blur / distance / Screentop zoom.
- [ ] **Hierarchy:** clear first/second/third read; nothing critical is buried or same-weight-as-noise.
- [ ] **Icon system:** each symbol = one meaning everywhere; icons replace text only where unambiguous;
      a key/legend exists but isn't *needed* mid-play.
- [ ] **Consistency:** every card places the same field in the same spot; aligned to a grid.
- [ ] **Text:** effect lines short, one idea each; keywords styled consistently.
- [ ] **Redundant with colour, never dependent on it** (hand to `bg-access` — colour + shape/icon/label).
- [ ] **Reads without the rulebook:** a returning player can act on the component from memory + the aid.
- [ ] **Language-independence where cheap:** icons over words lowers reading-level *and* localisation cost
      (cross-ref `funding-and-route-to-market.md` — less text = cheaper to translate and to pitch).

## Reference
- Daniel Solis, *Graphic Design for Board Games* (Routledge, 2024) — the field textbook.
- Cross-refs: `theme-and-identity.md` (identity), `accessibility.md` (perceptual floor),
  `elegance-and-clarity.md` (rulebook/aid clarity), the `bg-2d-components` skill (rendering).
