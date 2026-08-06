# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Ideation**

## One-liner
<!-- The hook a stranger would repeat. -->
You're a globe-trotting "travel agent" on a delicious undercover mission across Taiwan — chase night-market
eats, ride the rails, and out-adventure your rivals. *(working hook — to be sharpened)*

## Core fantasy / player role
<!-- Who you are, what you're doing, the feeling (the "kind of fun"). -->
The spirit of **adventure and discovery** with a **lighthearted, quirky** edge. You're part food-obsessed
traveller, part secret agent on a "mission" that's really just: eat the best stuff, see the island, one-up
your friends. Big emphasis on **food** and **Taiwanese humour**. (Kinds of fun to lock with `bg-theme`:
likely **Discovery + Fellowship + Challenge**.)

## Creative identity (concept · theme · tone · look & feel)
- **North star:** *(to be set with `bg-theme`)* — a warm, funny "eat your way across Taiwan" adventure.
- **Tone/vibe:** lighthearted, playful, adventurous; quirky secret-agent wink optional (not mandatory).
- **Details:** see `identity.md`.

## Positioning
- **Weight (BGG 1–5):** target ~1.8 (light-to-mid; family+ / gateway+)
- **Players:** 2–4 (**2-player duel mode** a first-class possibility — studio focus is 2p)
- **Playtime:** ~30–45 min (TBD)
- **Tone:** silly / warm / adventurous
- **Comparable:** *Let's Go! To Japan* meets *Ticket to Ride*, with a dash of *Couture* and *Agent Avenue*.
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight:** ~1.8 (BGG 1–5)
- **Caps:** see `complexity-budget.json`. Check drift with
  `python tools/complexity/check_complexity.py --game games/travel-agents` and run **`bg-elegance`** each
  iteration. Over budget → simplify, or consciously log a raise. Never silent creep.

## Modes & scope (see knowledge/modes-and-expansions.md)
- **Player modes:** 2–4. Explore a dedicated **2-player duel** (head-to-head "who has the better trip")
  alongside a 3–4p multiplayer race. Owned by `bg-architect`.
- **Campaign?** None planned (fine!). Possible light "trip journal" replay hook later.
- **Expansion ambition:** base = clean travel-food optimiser (agent framing is flavour only). Two held
  hooks (not baggage): a **"Secret Missions" expansion / campaign mode** that makes the secret-agent
  framing load-bearing (hidden objectives / bluff-deduction), and a **destination series** (other
  regions/countries) if the base sings. Owned by `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- 1–3 mechanism families and the blend; why each part needs the others (see knowledge/archetypes.md). -->
*(To be committed in Exploration/Design.)* Candidate blend from the inspirations: **set collection**
(food/dishes), **route/network building or push-your-luck travel** (Ticket to Ride DNA), and **open-drafting
/ card-play** (Let's Go! To Japan, Couture). Agent Avenue suggests a **bluff/deduction** micro-hook.

## Core loop
<!-- The repeated cycle of decisions and rewards, step by step. -->
*(To be designed.)*

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
*(To be found — likely where the "food" and "adventure/agent" fictions fuse into one rule.)*

## Components (summary)
*(To be defined; detailed manifest in components/manifest.md.)*

## Win condition & scoring
*(To be designed — likely "best trip": most/most-varied delicious adventures.)*

## Rules summary
*(To be drafted in design/rules-draft.md.)*

## Open questions & risks
- Which single mechanism spine? (route vs draft vs set-collection lead)
- ~~Is the "secret agent" wink load-bearing?~~ **Decided:** flavour in the base; load-bearing version held as a "Secret Missions" expansion/campaign candidate (2026-08-06).
- 2p duel vs 3–4p race: one core with a mode toggle, or is 2p the true home?
- **Sensitivity:** the game depicts a **real place & culture (Taiwan)** — flag for `bg-theme` +
  `bg-publishing` (respectful, well-researched, avoid caricature; "Taiwanese humour" done *with* not *at*).

## Status by stage
- [ ] Ideation
- [ ] Research
- [ ] Exploration
- [ ] Design
- [ ] Development
- [ ] Prototype (Screentop.gg / PnP)
- [ ] Playtesting
- [ ] Marketing
- [ ] Publishing / IP

## Links
<!-- design/, components/, playtests/, marketing/ artifacts as they appear. -->
- Identity: `identity.md`
- Decisions: `decision-log.md`
