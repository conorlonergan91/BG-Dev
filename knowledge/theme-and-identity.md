# Theme & Creative Identity — the studio playbook

The playbook for a game's **felt identity**: concept, theme, tone/vibe, story/lore, look & feel, and
naming — and, above all, keeping them **coherent** while letting them **evolve**. Owned by
`bg-theme` (the Creative Identity Keeper); every agent should bias toward it, the way they bias toward
`designer-profile.md`.

This is the studio's home for the **A** in **MDA** — *Aesthetics*, the experience the game creates.
`design-fundamentals.md` teaches MDA as a whole and the Mechanics/Dynamics legs; this file owns the
experience leg that the rest of the pipeline (mechanics, math, production) doesn't.

---

## 1. The identity stack

Six layers, top (most abstract) to bottom (most concrete). Each should support the one above it:

1. **Concept** — the seed. "Two lighthouse keepers reading the fog." Born in `bg-ideation`.
2. **Theme** — the subject the game is *about* (nautical rivalry; heist; growing a garden).
3. **Tone / vibe** — how it *feels*: cozy vs cutthroat, epic vs silly, warm vs bleak. One tone, held.
4. **Story / lore / world** — the fiction's depth. **Optional, scaled to the game** (see §4). Often a
   sentence; occasionally a world.
5. **Look & feel / art direction** — palette, type, iconography, silhouette, moodboard. What the eye
   meets first.
6. **Naming & voice** — the game's name, keyword/component names, and the rulebook's voice.

**Coherence = every layer points the same way.** The name matches the world, the palette matches the
tone, the signature rule matches the fiction. Incoherence anywhere reads as "muddled."

---

## 2. The kinds of fun (target aesthetics)

"Vibe" gets concrete when you name the **experience** you're going for. A useful vocabulary (the
MDA "8 kinds of fun"):

- **Sensation** — pleasure of the physical/visual (lovely bits, satisfying tactility).
- **Fantasy** — make-believe; being someone/somewhere else.
- **Narrative** — the drama of a story unfolding.
- **Challenge** — the obstacle course; mastery.
- **Fellowship** — the social fabric (co-op togetherness, table talk).
- **Discovery** — exploring an unknown (map, tech, mystery).
- **Expression** — making something yours (tableau, engine, style).
- **Submission** — the pleasant rhythm of a well-worn loop.

**Pick 2–3 as the target** and let them arbitrate. A constrained-comms co-op is chasing *fellowship +
challenge*; a tug-of-war duel is *challenge + a dash of fantasy*. Chasing all eight = chasing none.

---

## 3. Theme-first, mechanism-first, or abstract — all valid

- **Mechanism-first** (common here): the system exists; find the fiction that makes it *feel*
  inevitable. Most elegant duels start this way.
- **Theme-first**: the fiction is the pitch ("be a lighthouse keeper"); build systems that deliver it.
- **Pure abstract**: the game *is* its geometry (chess, *Azul*-adjacent). Then "identity" is tone +
  look, not story — and that's complete. **Don't apologise for it; don't bolt on lore.**

The studio's north star cuts across all three: **theme you can feel**, even when light. A great light
game has a *point of view*, not a paragraph of backstory.

---

## 4. The restraint ladder — how much identity does THIS game want?

Match identity depth to the game. Same discipline as modes/expansions: **pick the rung it earns and
stop.**

| Rung | What it means | Fits |
|------|----------------|------|
| **Pure abstract** | Tone + look only; no fiction | Deeply abstract elegance (*Patchwork*-adjacent) |
| **Light dressing** | A thin skin over the maths; evocative names | Quick fillers, most 20-min duels |
| **Evocative theme** | A felt world you could describe in a sentence; theme drives the twist | The studio sweet spot |
| **Light narrative** | Scenarios, a through-line, flavour that accrues | Campaigns, co-op arcs |
| **Deep world / lore** | A setting with its own logic, factions, history | Big-box, IP-led, expansion-heavy |

**An empty "story/lore" field on an elegant abstract is the right answer, not a gap to fill.** More
lore is not more theme.

---

## 5. Theme↔mechanic resonance (the integration test)

Theme is **integrated** when a player could half-guess the rules from the fiction, and the fiction
makes each rule feel inevitable. Theme is **pasted-on** when you could swap the setting and change
nothing.

- Interrogate the **signature twist** first: does the world *explain* it? (Beacon's "the tide turns —
  the loser takes initiative next Night" *is* the sea handing advantage back. The fiction earns the
  catch-up valve.)
- Pasted-on isn't automatically bad for a filler — but integrated theme is free depth and free
  teaching. Push for it.
- **The re-skin test:** if you can rename everything with no loss, the theme is doing no work. Either
  make it do work, or accept it as light dressing (a valid choice — just be honest about the rung).

---

## 6. Evolve, don't restrict — theme as a living hypothesis

The single most important discipline. Mechanics change during development; the fiction must be free to
follow.

- **Mechanics win ties with fiction.** If a great new rule contradicts the current story, **re-skin the
  story** — don't hobble the rule. The identity doc is a hypothesis, not a contract.
- **Re-theme freely, early, cheaply.** A theme swap costs nothing on paper and everything after art is
  commissioned. Do it now if the resonance is off.
- Log every re-theme in the identity doc + `decision-log.md`: *what changed in the design → how the
  fiction moved to match.* That trail is how theme stays coherent *through* change.

---

## 7. Avoiding muddle — coherence checks

Drift is the opposite failure. Guard it with concrete checks:

- **One tone.** No cozy art on a cutthroat game (unless the clash is the deliberate joke — then it's a
  *held* choice, logged).
- **One world-logic.** Names, flavour, and icons obey the same fiction. No mixed metaphors (space
  pirates *and* wizards *and* corporations, unless that's the premise).
- **A north-star image.** One picture the whole game points at. When a choice is unclear, ask "does this
  serve the north-star image?"
- **Naming convention.** Component/keyword names share a register (all nautical verbs; all
  garden nouns). List them together and read them aloud — dissonance is audible.
- **A palette + type + icon system**, not one-off choices (see §8).

---

## 8. Look & feel / art direction basics

- **Palette** — 2–4 core colours + neutrals, tied to tone (deep sea + brass + sea-foam = cozy
  nautical). Suit/faction colours must stay **colour-blind-safe** and distinct at a glance. This is
  the render `theme` in `tools/cards/themes.py` — name it and reuse it everywhere.
- **Typography** — one display face (title/headers), one clean body face (rules/values). No zoo.
- **Iconography** — language-independent icons beat words on components; keep a consistent icon grammar
  (see `bg-2d-components`). Icons carry theme *and* teachability.
- **Silhouette / shape language** — card frames, token shapes, board motifs. Recognisable at arm's
  length.
- **Moodboard / references** — collect references in `art/`; write an **art brief** the artist (or
  `bg-prototyper`) executes.
- **Human-illustrated by default** — the designer's stance is real art, **no AI art** (see
  `designer-profile.md`). Renders that ship placeholders label them clearly as placeholder.

---

## 9. Naming & voice

- **Game name** — evocative, sayable, ownable. Coherent with the world. Run **trademark/clearance**
  through `bg-publishing` *before* falling in love with it.
- **Keyword & component names** — theme + function together ("Signal", "Tide", "Night"). A good name
  teaches the rule.
- **Voice** — the rulebook and player aid have a tone too (warm, confident, playful — never a legal
  document). `bg-elegance` keeps it *tight*; `bg-theme` keeps it *in character*.

---

## 10. Coherence checklist (run each iteration)

- [ ] Target aesthetics (2–3 kinds of fun) named — and the game still delivers them.
- [ ] Restraint rung still fits (haven't drifted up into unearned lore, or down out of a felt theme).
- [ ] Signature twist passes the resonance / re-skin test.
- [ ] One tone, one world-logic across names, art, and rule-flavour.
- [ ] Palette / type / icon system is a *system*, not one-offs; suits colour-blind-safe.
- [ ] Any mechanic change since last pass has a matching fiction move (or a logged re-theme).
- [ ] Names cleared with `bg-publishing` before commissioning art.

---

### Who owns what (so identity doesn't collide with other agents)

| Concern | Owner |
|---|---|
| Concept birth | `bg-ideation` (hands off to `bg-theme`) |
| **Identity coherence & evolution, art direction, naming/voice** | **`bg-theme`** |
| Complexity, rulebook/aid clarity | `bg-elegance` |
| Degenerate/broken play | `bg-critic` |
| Executing the look (renders/PnP/3D) | `bg-prototyper` / `bg-2d-components` / `bg-3d-components` |
| Selling copy & positioning | `bg-marketing` (consumes identity) |
| Name clearance & IP | `bg-publishing` |
