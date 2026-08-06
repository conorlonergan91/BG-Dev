# Modes & Expansions Playbook

How to architect a game across **scopes** (base ↔ expansion) and **modes** (solo / duel / multiplayer /
party / campaign) so it's great standalone *and* great combined, while reusing components. Owned by
`bg-architect`; cross-refs `design-fundamentals.md` (scaling, solo/Automa) and `elegance-and-clarity.md`
(the base's complexity budget). Reference facts verified 2024–2025 (cited); re-check specifics live with
`tools/bgg/bgg_lookup.py` when precision matters.

## Prime principles
1. **The base must be complete and excellent alone.** Expansions *extend*; they never *fix* a base that
   only sings once you buy more. Ship the canonical/complete core; hold back **variety**, not the
   finished experience.
2. **Leave hooks, not baggage.** Decide mode/campaign/expansion ambition at kickoff so the core loop can
   *accommodate* the future (clean seams, scalable loop, spare iconography) — without carrying its weight
   now.
3. **Every mode/expansion earns its component cost.** Reuse base components first; add new ones only when
   they buy real experience. This lives under the complexity budget.
4. **Judge each scope separately AND combined.** Base alone, each mode, and base+expansion must all play
   well and stay balanced (watch power creep + combined complexity).

## Player modes — what makes each good, and how to add it cheaply
- **Solo / Automa.** A rules/card-driven opponent: low upkeep, real pressure, scalable difficulty. Reuse
  the multiplayer components + a small **automa deck** (Heat's *Legends* = 10 cards run the non-player
  cars, unlocking solo *and* grid-filling; the expansion just makes the same automa smarter).
- **2-player / duel.** Tight, direct, catch-up built in (no gang-up). Two routes: a **scaled mode** of the
  base, or — when the multiplayer engine doesn't translate — a **standalone re-engineered duel** (see
  *The White Castle: Duel*: dice removed, replaced by deterministic lantern-token action selection;
  reuses theme/art, rebuilds the engine for constant 2p tension).
- **Multiplayer.** Scale via board sections, round count, neutral players, count-specific rules; protect
  turn length/downtime as the count rises.
- **Party.** Short rules, many players, social — almost always its *own* design, not a mode bolted onto a
  heavier game.
- **Don't add a mode that doesn't earn its keep.** More modes = more teaching, testing, and components.

### Component-reuse techniques (add modes without ballooning parts)
- **Dummy / exposed-hand scaling** — cover solo→4p from *one deck* by varying how many hands are
  face-up/controlled (the LOTR *Fellowship* trick-taker: solo = one player runs 4 face-up hands; 2p uses a
  partly-open dummy hand). Zero extra components per count.
- **Automa from a small deck** — solo + fill empty seats without a new engine (Heat *Legends*).
- **Toggleable overlay modules** — token/card add-ons on a fixed board (Heat's weather / events / garage;
  Sky Team's ice/wind/fuel hazards). Difficulty & variety come from *which modules you stack* → dozens of
  states from a few parts.
- **Difficulty from scenario selection, not new parts** (Sky Team: ~11 airports × 21 scenarios on one
  fixed cockpit engine).

## Campaigns — base mode vs expansion
Decide early which model fits (this changes the whole architecture):

| Model | Examples | When it fits |
|-------|----------|--------------|
| **Campaign IS the base game** | *Ticket to Ride Legacy: Legends of the West*; LOTR *Fellowship* trick-taker; (Slay the Spire's run progression) | When the journey *is* the product's identity — you buy the box for it. Drip rules in via sealed unlocks / ordered chapters (low teaching cost); leave a replayable game behind (TtR converts to a custom map) or lean on inherent replay (roguelike / trick-taker modes). |
| **Campaign is an EXPANSION on a complete base** | *Arcs* → *The Blighted Reach* | When the base must first stand alone (esp. competitive) for a broad audience; the campaign is a heavy, opt-in transformation for invested players — persistent board state + swappable narrative modules (Arcs' **Fates**) transform the game *without a new engine*. |

**Persistence spectrum** (pick the lightest that delivers the drama):
one-shot **legacy** w/ permanent unlocks (TtR Legacy — sealed "frontier boxes", then converts to a keeper)
→ **persistent-but-replayable** state across sessions (Arcs Blighted Reach, ~3 sessions)
→ **ordered non-destructive scenarios**, only "which chapter" persists (The Crew, LOTR trick-taker)
→ **run-based meta-unlock** that widens the pool, not the power (Slay the Spire).
Given the 2020s **legacy-fatigue** trend (shelf cost, one-and-done), lean reset-friendly / legacy-lite
unless one-shot destruction is genuinely the point. The elegant, low-component end (ordered scenario
cards + dummy-hand scaling, or toggleable overlays) suits the studio's 2p co-op/duel house style best.

## Expansions — what to hold back, and how
The natural hold-backs are remarkably consistent across good games — hold back one of:
- **More content of an existing type** (Sky Team destinations; Slay the Spire / *Downfall* characters;
  Heat cars & tracks) — the base ships the complete *kind*, the expansion adds *variety*.
- **A heavier optional layer the base doesn't need** (Arcs' campaign; Heat *Legends*' smarter automa).
- **A whole added subsystem/board** (*The White Castle: Matcha* — a tea-house board + geisha/matcha
  economy that extends length & depth on top of the complete base).
Rules: expansions **plug into the existing engine** (reuse board/decks/pieces); watch **power creep** and
**combined complexity** (base + every expansion must still respect a sane budget); and prefer **modular,
independently-toggleable** expansions over monolithic ones.

## Reference games — how they do it (the transferable lesson)
- **Slay the Spire: TBG** (co-op deckbuilder, 1–4, roguelike). Ships all 4 characters complete; meta-unlocks
  **widen the card pool, not the power**, so it grows without creep; each character = starter deck + pool +
  1 relic on shared enemy/map/economy scaffolding. *Downfall* adds 4 more characters. **Lesson: ship a
  complete roster, expand the pool not the power.**
- **Arcs** (competitive 4X-lite, 2–4; Leaders & Lore asymmetry ships in the base). Campaign is the
  **Blighted Reach expansion**: a 3-session, replayable, persistent-state trilogy driven by swappable
  **Fate** modules layered on the untouched action engine. **Lesson: complete competitive base → day-one
  campaign expansion that transforms via persistent state + player-chosen modules, no new engine.**
- **Sky Team** (strict 2p co-op, silent-comms). Longevity from a deep **scenario/hazard library** on a
  tiny fixed engine; *Turbulence* adds destinations + stackable hazard modules. **Lesson: small fixed
  engine + a big library of stackable overlays = huge variety at near-zero component growth.**
- **Heat: Pedal to the Metal** (racing, 1–6). The base *is* a stack of **independent opt-in modules**
  (weather, events, garage/upgrades, championship season, *Legends* automa); expansions add cars/tracks/a
  smarter automa to the same speed/heat engine. **Lesson: build the base as toggleable modules; dial
  complexity by how many you enable.**
- **Ticket to Ride Legacy: Legends of the West** (standalone, 2–5). A 12-game legacy campaign on the
  familiar TtR engine; rules **drip in via sealed unlocks** (low teaching), and it **converts to a
  replayable custom game** afterward. **Lesson: put a campaign on an engine players already know, feed
  complexity just-in-time, and leave a keeper behind.**
- **LOTR trick-taking games** — *The Fellowship of the Ring* / *The Two Towers* (co-op, 1–4; The
  Crew-family). One 4-suit deck covers solo→4p via **dummy/exposed hands**; an 18-chapter **ordered,
  non-destructive** campaign of quest cards; strong licensed story for pull. **Lesson: dummy-hand scaling
  + ordered scenario cards on one deck; mind that a licensed theme can stay skin-deep.**
  *(Not to be confused with **LOTR: Duel for Middle-earth** — a Knizia **2-player tug-of-war duel**, a
  different game entirely; both are useful references, for different things.)*
- **The White Castle** (dice-placement Euro, 1–4) + **Matcha** (base-required subsystem/board add-on) +
  **Duel** (standalone 2p; dice removed for deterministic lantern-token action selection). **Lesson: for a
  2p version of a multiplayer Euro, ship a standalone re-engineered duel — keep the theme/iconography,
  replace the randomizer/engine for constant two-player tension — rather than a bolted-on mode.**

## Sources (re-verify live for a real project)
Leder Games (Arcs / Blighted Reach); Days of Wonder (Heat universe & Legends; TtR Legacy); Le Scorpion
Masqué (Sky Team / Turbulence); Contention Games (Slay the Spire TBG); Office Dog (LOTR trick-takers);
Devir (The White Castle / Matcha / Duel); BoardGameGeek. Pull exact weights/counts with
`python tools/bgg/bgg_lookup.py --name "<game>"`.
