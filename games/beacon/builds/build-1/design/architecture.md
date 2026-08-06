# Beacon — Modes & Expansion Architecture

*Output of the `bg-architect` stage. Beacon's base is a complete 2-player duel (weight ~1.8); this maps
what modes/expansions it could support later **without bloating that base**. See
`knowledge/modes-and-expansions.md`.*

## Mode plan
- **2-player duel — the base (done).** Complete and great on its own. Everything below is optional and
  reuses the base 36 cards + Tide track wherever possible.
- **Solo (automa) — strong fit, cheap.** A "Rival Keeper" automa: a small deck (~8 cards) that, each
  round, dictates the automa's Signal (high/low) by a face-up rule and its ship pick by a fixed priority.
  Reuses *all* base components + one new deck. Delivers the studio-standard solo mode at minimal cost.
- **Co-op variant — on-theme, low cost.** Both keepers vs an incoming "Storm": a shared threat track the
  ships advance; you cooperate (with Beacon's natural limited-info: blind Signals) to land enough ships
  before the storm. Reuses ships + Signals + Tide track; adds a storm track (reuse the Tide track art) +
  a small threat deck. Fits the designer's constrained-communication co-op love.
- **Multiplayer (3–4) — deprioritize.** Beacon's whole engine is the 2p blind duel + tug-of-war; scaling
  to 3–4 would need a new majority/turn structure and dilutes the head-to-head read. If ever wanted, it's
  a **standalone re-engineering**, not a mode — not worth it now.
- **Party — n/a.** Out of character for a 20-min elegant duel.

## Base ↔ expansion split
- **Base (complete):** 3 suits × 1–4 ships, 6 Signals/player, Tide track, tokens, the 3-Night duel.
- **Hold back for an expansion (variety, not the finished game):** a **"Ports & Cargo" module** — a few
  new ship types with light one-shot effects (e.g. a Lightship that shifts the Tide, a Smuggler worth
  more but risky), plus alternate **Signal sets** (asymmetric keeper powers, in the Arcs "Leaders" spirit).
  This adds *variety* on the existing engine; the base stays whole without it.
- **Campaign — as a small expansion, not the base.** Beacon's identity is the quick filler, so the
  campaign should be an **optional add-on**: an ordered, **non-destructive** ~6-scenario "Coastline"
  campaign (in the Sky Team / The Crew mold) where each scenario tweaks one rule (a rocky channel, a fog
  night, an asymmetric lighthouse). Persistence = "which scenario you've reached" only. Reuses the base
  deck + scenario cards; no legacy destruction (respects legacy-fatigue).
- **Hooks the base needs now (cheap to add):** keep a spare suit-colour/iconography slot on cards; keep
  the Tide track reusable as a generic track (storm/threat); don't hard-code "exactly 3 suits / 3 Nights"
  in the rulebook language so scenarios/modules can vary them.

## Component-reuse map
| Scope | Reuses | New components (keep minimal) |
|-------|--------|-------------------------------|
| Solo | all base | 1 automa deck (~8 cards) |
| Co-op "Storm" | ships, Signals, Tide track | storm/threat track (reuse Tide art) + small threat deck |
| "Ports & Cargo" expansion | base engine | a few ship cards + 1–2 alt Signal sets |
| "Coastline" campaign | base deck | ordered scenario cards only |

## Plays-well separately & combined — checks
- **Base alone:** already the focus of the design→sim→tune loop (v0.3). ✓
- **Solo automa:** must feel like a real read, not solitaire — sim the automa vs the `grabber`/`always_high`
  lines (reuse `tools/sim`); target a ~45–55% automa win rate at "standard".
- **Co-op:** watch the alpha-player leak — Beacon's blind Signals help; verify one player can't just
  dictate. Human playtest question.
- **Combined (base + expansion + module):** keep total within the complexity budget — new ship effects
  and alt powers are the main power-creep risk; A/B sim any effect that touches the Tide.

## Decision for the human
Which mode to build **first**, after the base playtests well? **(A)** Solo automa (cheapest, expected,
reuses everything — recommended); **(B)** the constrained-comms **co-op "Storm"** variant (most on-brand
for your taste); **(C)** none yet — keep polishing the duel. I'd do (A) to prove the automa pattern, then
(B) as the flagship. Campaign stays a later, optional expansion — not base baggage.
