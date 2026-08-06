# 🎲 Travel Agents: Taiwan — Game Bible

> The single living source of truth for this game. Every agent reads and updates this. Keep it current.
> Slug: `travel-agents` · Started: 2026-08-06 · Status: **Design** (spine A locked)

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
- **Tone/vibe:** lighthearted, playful, adventurous; the quirky **secret-agent wink is now first-class**
  — a present, rule-earning layer (kept warm/comedic), not optional flavour (Creative Director, 2026-08-06).
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
- **Expansion ambition:** base = travel-food optimiser **with the secret-agent layer load-bearing**
  (hidden Assignments + a shared Dossier — CD call 2026-08-06, so the hidden-mission content is IN the
  base, no longer a held expansion). Remaining held hooks (not baggage): explicit **co-op / duel mode
  split** (spine B — cheap to graft later since it shares this core), a deeper **campaign / "trip
  journal"** arc, and a **destination series** (other regions/countries) if the base sings. Owned by
  `bg-architect`.
- **Guardrail:** base must be complete & great on its own.

## Mechanism spine
<!-- 1–3 mechanism families and the blend; why each part needs the others (see knowledge/archetypes.md). -->
**LOCKED — spine A "Rival Agents, Shared Beat"** (CD, 2026-08-06; see `design/explore-agent-layer.md`).
A **competitive + co-op blend in one box**, built on:
- **Set collection with a twist — recipes by region.** A dish = a tiny recipe of 2–3 named ingredients;
  ingredients are sourced from the Taiwan **regions that actually supply them** (oysters coastal, Hakka
  mountain towns, east-coast Indigenous cuisines…). This is the generic-defeater — the map is shaped by
  real food geography, not "food + map." (from the Yes! Ginseng / Taiwan Snackbar inspirations)
- **Region routing / travel** — you move *because* the ingredient you need lives *there*.
- **The load-bearing agent layer:** a **hidden Assignment** (secret objective you race to plate) + a
  face-up **Grand Dossier** the whole table advances together + **tip-off / dead-drop** hand-offs that
  help a rival yet bank *you* a reward. This is what makes "I'm a food spy on a mission" a thing you *do*.

## Core loop
<!-- The repeated cycle of decisions and rewards, step by step. -->
*(→ `bg-design` to specify.)* Sketch: travel to a region → source ingredients there → plate dishes
(toward your **hidden Assignment** and the shared **Grand Dossier**) → optionally **tip off** a rival for
a personal reward → score. The tension every turn: advance my secret mission, or feed the shared Dossier
for the Discovery bonus everyone shares?

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
**The shared Dossier + tip-offs** — a genuinely cooperative spine running *inside* a competitive race, so
helping a rival can be the selfish play. Fused with **recipes-by-region**, so the spy-mission fiction and
the food-geography fiction drive the *same* decisions.

## Components (summary)
*(→ `bg-design` / `bg-developer`; detailed manifest in `components/manifest.md`.)* Likely: ingredient
cards (by region), dish/recipe cards, hidden Assignment cards, the shared Grand Dossier track/board, a
Taiwan region map, player itinerary/log, tip-off/dead-drop tokens.

## Win condition & scoring
*(→ `bg-design`.)* Sketch: most points from your completed **hidden Assignment** + plated dishes + your
share of **Grand Dossier** Discovery bonuses + tip-off rewards. "Best trip" wins.

## Rules summary
*(To be drafted in `design/rules-draft.md`.)*

## Open questions & risks
- ✅ **Mechanism spine — DECIDED:** A "Rival Agents, Shared Beat" (2026-08-06).
- ✅ **Is the "secret agent" wink load-bearing? — DECIDED:** yes, in the base (hidden Assignments +
  shared Dossier). Reverses the earlier "flavour-only / held expansion" call (2026-08-06).
- ⚠️ **TOP RISK (attack first with `tools/sim` + a Screentop session):** is the co-op layer *individually
  rational* often enough that players actually cooperate — or does it collapse into a dominant
  "hoard, never tip" line (killing the promised Fellowship) or **kingmaking**? Semi-co-op's knife-edge.
  Fallback: spine B's explicit co-op mode (cooperation as win condition, not temptation) on the same core.
- Hold weight at **~1.8** — one clean hidden-info hook, not a deduction engine (`bg-elegance` guards).
- 2p-first, but confirm it scales cleanly to 3–4 (`bg-architect`).
- **Sensitivity:** the game depicts a **real place & culture (Taiwan)** — flag for `bg-theme` +
  `bg-publishing` (respectful, well-researched, avoid caricature; "Taiwanese humour" done *with* not *at*;
  paid Taiwanese cultural + language consultant before art/print).

## Status by stage
- [x] Ideation
- [x] Research
- [x] Exploration
- [ ] Design ← **in progress** (`bg-design` specifying spine A)
- [ ] Development
- [ ] Prototype (Screentop.gg / PnP)
- [ ] Playtesting
- [ ] Marketing
- [ ] Publishing / IP

## Links
<!-- design/, components/, playtests/, marketing/ artifacts as they appear. -->
- Identity: `identity.md`
- Decisions: `decision-log.md`
