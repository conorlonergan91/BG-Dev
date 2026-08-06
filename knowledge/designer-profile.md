# Designer & Studio Context

> **This is context, NOT a design-style bias.** The studio has **no default house style**. It is
> **genre- and style-agnostic** and approaches every game *generically*, on that game's own terms.
> Nothing here tells an agent to prefer a player count, weight, genre, mechanism family, or mood.

## Where design taste actually comes from

- **Per game** → the game's own **`identity.md`** + **`game-bible.md`** (set at kickoff from the brief,
  guarded by `bg-theme`). This is the *only* place a single game's taste/genre/weight/player-count lives.
- **Per group** → a **series/collection** may share a taste, but **only when the human explicitly asks
  for a group of games with a shared style**. Capture that shared taste in the series manifest
  (`series/<name>.md`), and it applies to that group only — never repo-wide.
- **Absent an explicit steer** → stay neutral. Ideate broadly, don't privilege any family, and let the
  brief for *this* game (or the human's answers) set the direction. Never import taste from another game.

**Every dispatched agent should be pointed at the specific game's `identity.md` + `game-bible.md`, not
at this file, for design direction.** This file exists only for the practical, game-independent facts
below.

## Practical facts (game-independent)

These are logistics about the human and how the studio runs — they are constraints/resources, not a
design aesthetic:

- **Location / markets:** based in **Ireland**; publishing interest in **Ireland, UK, USA** (drives
  `bg-publishing` compliance scope — see `publishing-ip.md`).
- **Playtest platform default:** **Screentop.gg** first — free, browser, join-by-link, works remote or
  in person. This is a *tooling* default (how prototypes get to a table quickly), **not** a statement
  about what kind of game to make. TTS / Tabletopia / print-and-play are alternates.
- **Testing resource:** the human has a regular **2-player playtest partner** available. This makes 2p
  testing convenient — it is **not** an instruction to design 2-player games. Design for whatever player
  count the specific game calls for.
- **Process:** wants a **fast, fun, collaborative human+AI** loop — playable early, tight iterations,
  decisions logged. (This is *how* the studio works, applies to any game.)
- **Release preference (soft):** the human has indicated a general preference for **low upfront cost and
  financial risk** where a game's own goals allow it (owned by `bg-funding`; see
  `funding-and-route-to-market.md`). Treat as a default to *offer*, not a constraint to force onto a
  design.

## Reference only — games the human has mentioned enjoying

Listed purely as **context**, so a conversation about a comparable can be grounded. **These are NOT a
lens the studio applies by default** and must not bias ideation, exploration, or design unless the
specific game's brief deliberately heads that way:

- *Hanabi*, *Sky Team*, *SAIL*, *Slay the Spire: The Board Game*, *Splendor Duel*,
  *The Lord of the Rings: Duel for Middle-earth*, *Patchwork*.

If a new game's brief points somewhere completely different (heavy, multiplayer, party, ameritrash,
sandbox, real-time, whatever), follow the brief — this list is irrelevant to it.

## How to keep this honest

- If you catch yourself defaulting to "2p", "co-op", "elegant/low-weight", "tug-of-war", or any other
  flavour **without the current game's brief asking for it**, stop — that's the old baked-in bias, and
  it's gone. Re-derive the direction from *this* game's `identity.md` / `game-bible.md` or ask the human.
- Update this file only for genuinely game-independent facts. **Never** add a design-style default here.
