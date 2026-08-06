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
- **Weight (BGG 1–5):** aim ~1.8, acceptable up to **~2.2** if gameplay needs it (lighter is better, but don't let the budget hamper the fun — CD 2026-08-06). Band: TtR Europe ~1.9, Let's Go! To Japan ~2.25.
- **Players:** 2–4 (this game leads with a first-class **2-player duel** by its own design choice, then scales to a 3–4p race)
- **Playtime:** ~30–45 min (TBD)
- **Tone:** silly / warm / adventurous
- **Comparable:** *Let's Go! To Japan* meets *Ticket to Ride*, with a dash of *Couture* and *Agent Avenue*.
- **Audience:** families, foodies, casual + gateway hobbyist; travel/Taiwan-culture fans.
- **Target platform:** Screentop.gg for playtest (studio default); route-to-market TBD (`bg-funding`).

## Complexity budget (set at the START — defend it as you iterate)
- **Target weight:** aim ~1.8; **acceptable ceiling ~2.2** (CD raise 2026-08-06 — gameplay wins over strictness; lighter still preferred)
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
Specified in `design/design-doc.md`. **A turn = ONE action:** **Stock Up** (take 2 ingredients where you
stand) · **Travel** (move one region, arrive with 1) · **Plate** (spend a recipe from your Larder to take
a Menu dish → VP + Grand Dossier +1) · **Dead-drop** (give a rival 1 ingredient → bank an Insider Tip +
Grand Dossier +1) · **Extract** (trigger the end-game). You can only take a region's **specialty** while
there (oysters South, tea/pearls Central, rice/greens East, beef/pork North); **pantry** staples are at
the convenience store anywhere — so you *travel because the ingredient lives there*. Your **Larder sits
face-up in the open** (no hidden hand — the secret Assignment is the game's *only* hidden info).
**Larder caps at 7**,
so surplus is common → dead-dropping surplus (for an Insider Tip) beats discarding it: that's what makes
cooperation individually rational. The tension every turn: advance my secret **Assignment**, race a dish
off the shared **Menu**, or convert surplus into leverage — all while the shared **Grand Dossier** rises.

## Signature twist
<!-- The one memorable rule/hook that makes it *this* game. -->
**The shared Dossier + tip-offs** — a genuinely cooperative spine running *inside* a competitive race, so
helping a rival can be the selfish play. Fused with **recipes-by-region**, so the spy-mission fiction and
the food-geography fiction drive the *same* decisions.

## Components (summary)
*(Full table + quantities in `design/design-doc.md`; detailed manifest → `bg-developer`.)* **6 component
types — exactly at the budget cap:** (1) **Map board** — Taiwan, 4 regions on a ring + HSR spine, with
the Grand Dossier track and score track printed along the edge; (2) **~24 Dish cards** (recipe + VP +
name romanised & 繁體); (3) **~14–16 Assignment cards** (secret objectives, +7 VP); (4) **~120 ingredient
tokens** — 9 types: 8 region specialties (2 per region) + 1 fungible **pantry** (the convenience store);
(5) **~30 Insider Tip tokens**; (6) **4 Agent pawns**. (Dossier/score markers ride the board — not a 7th
type.) No headroom for a new type — new content reuses these (flag: `bg-elegance`).

## Win condition & scoring
Highest **Traveller's Log** wins. Score = **plated dishes** (3 VP for 2-ingredient · 4 VP for 3-ingredient
· 5 VP for a 3-region Signature) + **Assignment** (+7 if completed, revealed at scoring) + your banked
**Grand Dossier** bonuses. Dossier payout = **Hybrid (C, CD call 2026-08-06):** each milestone pays a flat
Discovery bonus to *everyone* (+2/+3/+4/+5 — a warm rising tide) **and** the player who triggers it picks
a small reward — an **Insider Tip or +1 VP**. **Tiebreak:** most dishes, then most regions visited. The
contested margin is **dishes + Assignment + Insider-Tip/trigger efficiency** (the flat Dossier base is a
rising tide that doesn't decide ranking; only the ≤+4 VP of triggerer-picks touches it). Expected 2p total
~48–52 VP. Detail + balance model in `design/design-doc.md`.

## Rules summary
Drafted in `design/rules-draft.md` (teach-in-play order). Turn = one of **Stock Up / Travel / Plate /
Dead-drop / Extract**; Larder cap 7; Grand Dossier +1 per Plate or Dead-drop with milestone Discovery
bonuses; end-game triggers on **Extract** or the Dossier's final milestone → finish the round + one more
full round → score. **One hidden-info hook only:** the secret Assignment (no deduction engine).

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
