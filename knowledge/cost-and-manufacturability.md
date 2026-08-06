# Cost & Manufacturability

Designing so the game is **cheap to make and cheap to move** — which, for a designer minimising upfront
cost, decides more than almost anything else. Component footprint is a *budget*, like complexity: set it at
project start (`component-cost-budget.json`), guard it with `tools/cost/check_cost.py`, and don't let it
creep. **Worth knowing: if a game targets a small box and low weight, that's already the cheapest to
release by every route** — so when a game does head that way, this discipline is mostly about not *losing*
that advantage as scope grows. Owned by **`bg-architect`** (component scope) with **`bg-funding`** (route-to-market economics).

## The cost levers, in order of impact
1. **Number of *unique component types*** — the biggest lever by far. Each distinct type (cards, tokens,
   dice, meeples, board, insert…) is its own tooling, assembly step, and QC pass. **4 types is far cheaper
   than 8 even at equal piece count.** Merge and reuse before you add a new type. This is where
   `bg-architect`'s "every mode/expansion earns its component cost" and the cost budget meet.
2. **Box size / tier** — a small box is cheaper to print *and* drives freight and warehouse cost per unit,
   and it's the line **tariffs hit hardest** (you pay duty on landed value, and volume ships by the
   container-slot). Small, light, dense-value box = cheaper everywhere. It also fits the **sub-$20 small-box
   slots most publishers actually buy** (cross-ref `funding-and-route-to-market.md`).
3. **Standard sizes** — poker/standard **63×88 mm** cards have the lowest tooling cost and best sleeve
   support; custom sizes and bespoke dies cost extra. Prefer off-the-shelf.
4. **Piece count** — raw quantity matters less than type count, but still drives material + assembly.
   **Double-sided and multi-use components** cut piece count for free.

## The budget (`component-cost-budget.json`)
Mirror the complexity budget: caps on **component types, total pieces, unique cards, box tier**, plus a
**target retail price** and **`target_cogs_fraction`** (manufactured unit cost as a share of retail). Rough
anchors:
- **COGS fraction:** indie/POD lands near **~0.5** (thin margin — a proving ground, not income); a healthy
  **pitch/crowdfund** target is around **~0.20** (the publisher's/your margin lives in the rest).
- A **compact card game can cost as little as ~$2/unit at volume**; box size then dominates freight.
The gauge estimates COGS from the component data (or a precise `components/cost-manifest.json` BOM). Going
over budget has two honest outcomes: **cut/merge components back under, or consciously (logged) accept a
higher price tier / thinner margin.** Never silent creep. *(Unit costs are order-of-magnitude — re-verify
with a live manufacturer quote before pricing.)*

## The 2026 macro factor: tariffs & freight (re-verify live)
Most games are manufactured in **China**, and 2025–2026 US tariffs on Chinese goods swung violently (from
~10% up through 30–54%, with threats far higher, then partial truces) — a **$25 game can become a $40 game**,
and freight has added double-digit percentages to landed cost. Whoever **imports and ships inventory** bears
this: **you, if you self-crowdfund; the publisher, if you licence; the platform/buyer, if you POD.** For a
risk-minimising designer this tilts toward **licensing and POD**, and if you *do* crowdfund: **price with a
tariff buffer, favour manufacture-and-fulfil to regional (EU/UK) hubs, and keep the box small and light.**
As an Ireland/EU designer serving IE/UK/EU, fulfilling within Europe sidesteps the worst US–China crossfire
for those backers. *(All figures move fast — confirm current rates via `bg-research`/`bg-publishing`.)*

## Quick self-check (run as scope grows)
- [ ] `check_cost.py` within budget: component types, pieces, unique cards, COGS fraction.
- [ ] Any **new component type** justified — could an existing token/card do the job? (Reuse > add.)
- [ ] **Standard card size**; box in the intended tier; double-sided/multi-use where it cuts pieces.
- [ ] The design still fits a **small-box, sub-$20** profile (cheapest to POD, easiest to pitch).
- [ ] For a physical run: a **tariff/freight buffer** priced in; regional fulfilment considered.

Cross-refs: `funding-and-route-to-market.md` (which route bears which cost), `manufacturing-specs.md`
(sizes/bleed/DPI), `manufacturing-and-fulfillment.md` (making & shipping), `modes-and-expansions.md`
(component reuse), `accessibility.md` (small/low-text is also more accessible).
