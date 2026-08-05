# 🎲 Beacon — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `beacon` · Started: 2026-08-05 · Status: **Prototype-ready (demo build)**
>
> ⚠️ **This is the studio's worked example / kitchen-sink demo** — a complete 2-player game taken
> through every pipeline stage to show each agent's output. First-pass numbers, unplaytested.

## One-liner
Two rival lighthouse keepers read the fog and fight the tide to guide the richest ships into their own
harbour — a 20-minute duel of blind signals and shifting advantage.

## Core fantasy / player role
You're a lighthouse keeper on a treacherous stretch of coast. Each night, ships come through the
Channel; your beam can only guide so many. Outread your rival — commit your signal before you know
theirs — and claim the fat cargo runs while the tide is with you.

## Positioning
- **Weight (BGG 1–5):** ~1.8 (light-medium)
- **Players:** 2 (strictly two-player)
- **Playtime:** ~20 min
- **Tone:** cozy-competitive, nautical, tense but warm
- **Comparable:** *The Fox in the Forest* meets *Air, Land & Sea* (blind commit + tug-of-war), with a
  dash of *Jaipur* set-collection.
- **Audience:** couples/friends who want a quick, thinky 2-player filler; café/travel play.
- **Target platform:** Screentop.gg first (playtest); print-and-play + card POD later.
- **Visual theme:** `nautical` (deep sea + brass + sea-foam; see `tools/cards/themes.py`). Shareable
  renders (decks, cover, rulebook, track, tokens) are committed in `exports/` — regenerate with
  `./make.sh`. Cover is a rough placeholder — real art TBD (human-illustrated, no AI).

## Mechanism spine
**Simultaneous blind selection** (the core tension) + **tug-of-war track** (the Tide, area-majority in
miniature) + **set collection** (ship suits for scoring). The blind commit *needs* the Tide: the Tide
is the payoff and catch-up valve that makes each blind bid matter beyond the single ship. (See
`knowledge/archetypes.md`.)

## Core loop
Reveal 2 ships to the Channel → both commit a Signal face-down → reveal → higher Signal wins the beam
(the Tide steps toward you) **but the lower Signal picks a ship first** → refill → 4 rounds/Night,
committing 4 of your 6 Signals (hold 2 back) → score at each Night's end. *(v0.2 — the "can't grab
position and cargo at once" tension came out of the design→sim→tune loop; see design-doc history.)*

## Signature twist
**The tide turns.** At each Night's end the Tide side scores 2 VP per space from centre (v0.3), resets to centre, and the keeper who
**lost** the Tide takes the First-Keeper token (initiative) for the next Night — a built-in catch-up
lever so the trailing player stays live. Winning the Tide scores now but hands your rival the edge next
Night. (The "commit 4 of 6, hold 2" hand also creates a constant bluff space.)

## Components (summary)
24 Ship cards (3 suits × values 1–4), 2 identical sets of 6 Signal cards (0–5), a 7-space Tide track +
1 marker, 2 Harbour zones, a first-keeper token. Full list in `components/manifest.md`.

## Win condition & scoring
After 3 Nights, score: sum of claimed ship **values** + **set bonuses** (runs/sets of suits) + **Tide
majority bonus** each Night. Highest total wins; tie → most Naval ships.

## Rules summary
See `design/rules-draft.md`. Light rules, one meaningful decision per round (which Signal to burn,
blind), with the Tide creating a second layer of pressure.

## Open questions & risks
1. Is blind simultaneous selection deep enough over 3 Nights, or does it get swingy/random?
2. Signal economy: is "commit 4, hold 2 of 6" the right ratio (vs 5-of-7)?
3. Denial: is "loser still takes a ship" too gentle? Test the optional **Rocks** variant (Channel of 3,
   third ship lost).

## Status by stage
- [x] Ideation
- [x] Research
- [x] Exploration
- [x] Design
- [x] Development (component data + rules draft + build)
- [x] Prototype (Screentop.gg deck sheets generated)
- [~] Playtesting (simulated — `playtests/sim-notes.md`; human session 1 planned — `playtests/session-01-plan.md`)
- [x] Marketing (sell sheet drafted)
- [x] Publishing / IP (IE/UK/US quick plan drafted)

## Links
- Design: `design/research.md`, `design/exploration.md`, `design/design-doc.md`, `design/rules-draft.md`
- Components: `components/ships.csv`, `components/signals.csv`, `components/manifest.md`
- Playtest: `playtests/session-01-plan.md`
- Marketing: `marketing/sell-sheet.md`, `marketing/ip-and-compliance.md`
