# 🎨 Beacon — Creative Identity

> The living source of truth for this game's **felt identity**. Owned by `bg-theme`; read alongside
> `game-bible.md`. Keep it coherent while it evolves with the design.
> Slug: `beacon` · Started: 2026-08-05
>
> ⚠️ **Studio worked example.** Like the rest of beacon, this is a demonstration of the `bg-theme`
> output — first-pass, unplaytested.

> **Restraint rung: evocative theme.** Beacon is a ~1.8-weight, 20-minute duel. It wants a felt world
> and a clean nautical look — **not** lore. Story stays a sentence; the theme earns its keep through the
> *mechanics*, not backstory. That's deliberate.

## North star
Two lamps sweeping a foggy channel at night — warm brass light on cold water, each keeper willing the
richest ships toward their own harbour.

## Concept & premise
Two rival lighthouse keepers on a treacherous coast read the fog and fight the tide to guide the fattest
cargo runs into their own harbour. A quick, warm-but-tense duel of blind signalling and shifting
advantage.

## Target aesthetics (the kinds of fun)
- **Challenge** — the blind-commit read: outguess your rival before you know their signal.
- **Fantasy** — the cozy fiction of being *a keeper on the coast*, small and warm against the dark.
- *(a touch of **Sensation**)* — brass-and-sea-foam warmth; the satisfying "tide turns" swing.

## Tone & vibe
**Cozy-competitive, nautical, tense-but-warm.** A duel you play by a fire with a hot drink — sharp
decisions, no cruelty. Never grim, never zany.

## Restraint rung
**Evocative theme.** (Ladder: pure-abstract · light dressing · **evocative theme** · light narrative ·
deep world/lore.) Beacon sits here on purpose — a felt world with no need for scenarios or backstory.

## Story / world / lore
One sentence is enough: *a stretch of fog-blind coast where two keepers compete, night after night, to
land the richest ships.* No factions, no history, no named characters — the game is the rivalry, not a
saga. Blank-by-design below this line.

## Theme ↔ mechanic resonance
Beacon's theme is **integrated**, not pasted on — the fiction makes each core rule feel inevitable:
- **Blind commit = the fog.** You commit your signal before seeing your rival's *because neither keeper
  can see through the fog.* The information bottleneck *is* the weather.
- **Signature twist — "the tide turns."** At each Night's end the tide scores, resets to centre, and the
  keeper who **lost** the tide takes First-Keeper (initiative) next Night. This is the sea literally
  handing advantage back to the trailing keeper — the catch-up valve *is* the tide. Passes the re-skin
  test cleanly: rename it and you lose the reason it feels right.
- **Signal values (0–5), hold 2 of 6 = the beam's reach.** Your lamp can only guide so much; holding
  signals back is husbanding a limited light.

## Look & feel / art direction
- **Palette:** `nautical` — deep sea (navy/teal) + **brass** (warm accent) + **sea-foam** (light). Warm
  light against cold water. Suit colours kept distinct & colour-blind-safe. (Render `theme` in
  `tools/cards/themes.py`.)
- **Typography:** a lightly nautical display face for titles; clean, legible body face for rules & card
  values (values must read at arm's length).
- **Iconography:** ship-suit icons, a lamp/beam motif for Signals, a tide arrow for the track — language
  independent, teach-in-the-art.
- **Silhouette / shape language:** rounded "porthole" card frames; the Tide as a horizontal channel
  track; wooden-token feel for keepers.
- **Moodboard / references:** see `art/` (to populate) — foggy coastlines, brass lanterns, admiralty
  charts, *The Fox in the Forest*'s warmth.
- **Art production:** **human-illustrated — no AI art** (studio stance, `designer-profile.md`). Current
  `exports/cover` is a clearly-labelled placeholder; real art TBD. To *explore* a high-fidelity vibe you
  can generate an opt-in **AI mockup** (`python tools/art/mockup.py --game games/beacon --subject cover`)
  — mockups are exploration only, live in `art/mockups/` (gitignored), and never ship as final art.

## Naming & voice
- **Game name:** *Beacon* — evocative, sayable, ownable (clear via `bg-publishing` before committing).
- **Key names:** **Signal** · **Tide** · **Night** · **Channel** · **First-Keeper** — each names its
  function *and* fits the world; a player half-guesses the rule from the word.
- **Rulebook/aid voice:** warm and confident, a keeper's-log register — never a legal document
  (`bg-elegance` keeps it tight).

## Locked vs fluid
- **Locked:** nautical world, cozy-competitive tone, the `nautical` palette, the Signal/Tide/Night
  vocabulary, human-illustrated art.
- **Fluid:** final art direction & cover; whether a co-op "Storm" mode leans darker/more tense (its own
  identity note if it graduates from variant to product).

## Re-theme log
- *2026-08-05* — Set at evocative-theme rung from kickoff; fiction chosen mechanism-first (blind-commit
  duel needed a reason two players can't see each other's choice → fog/keepers). Resonance strong on
  first pass; no re-skin needed yet.
- *2026-08-06* — Regenerated assets to match this identity: Signal cards now render the **lamp/beam**
  emblem (brass lamp + glow halo, as value pips too) instead of the generic spark — the "keeper's light"
  motif. Palette/typography unchanged (nautical locked). Ship suit-emblems and cover remain placeholder;
  full ship/porthole iconography is still **human-illustrated, TBD** per the no-AI-art stance.
