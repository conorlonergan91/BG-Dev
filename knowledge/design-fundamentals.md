# Design Fundamentals

The levers that make a game *work*. Use these as a checklist when designing or diagnosing.

## Core loop
The repeated cycle of decisions and rewards each turn/round (e.g. *gather → build → produce → score*).
A strong core loop is intuitive, satisfying on its own, and compounds. **Design the loop first**, before
content.

## Player agency & meaningful decisions
Agency = players' *choices* drive outcomes, not luck. A **meaningful decision** has (a) multiple viable
options, (b) discernible trade-offs, (c) partly foreseeable consequences, (d) no single dominant move.
Strip away non-decisions.

## Tension & catch-up (rubber-banding)
Keep trailing players in contention and prevent runaway leaders: turn-order compensation, catch-up
bonuses, escalating end-triggers, letting the leader be targeted. Balance against fairness — overt
"bash the leader" or heavy rubber-banding feels arbitrary and punishes good play.

## Downtime
Time a player waits with nothing to do. Mitigate with simultaneous action (7 Wonders drafting), shorter
turns, parallel personal boards (roll-and-writes), interrupts/reactions, and reducing analysis paralysis
(AP) via clearer choices.

## Player interaction: direct vs indirect
- **Direct:** attacking, blocking, stealing, negotiation — targets specific opponents (thematic/wargame).
- **Indirect:** competing for shared but impersonal resources — markets, worker spaces, turn order, area
  majorities (classic Euro). Too little interaction of either kind → "multiplayer solitaire".

## Asymmetry
Players start with different powers/factions/positions — from mild (variable powers in Terraforming Mars)
to extreme (Root, Spirit Island, Vast). Boosts replayability and theme; multiplies balancing and
teaching cost.

## Randomness: input vs output
- **Input randomness** happens *before* your decision (dealt cards, revealed market, rolled dice you then
  assign) — you adapt; preserves agency (Wingspan feeder, Ark Nova card row).
- **Output randomness** happens *after* your decision (roll to hit) — drama and swings, but can negate
  skill (Risk combat). Choose deliberately; mitigate output luck (re-rolls, mitigation dice, EV tuning).

## Decision space
Breadth × depth of viable choices. Too small = solvable/boring; too large = AP. Good games **funnel** a
wide space into a few consequential decisions per turn.

## Elegance — depth vs complexity
- **Complexity** = rules/component overhead to learn (the barrier).
- **Depth** = strategic richness that emerges (the reward).
- **Elegance** = maximum depth from minimum complexity (Go, Azul, Chess, Splendor). "Emergent
  complexity" — deep play from simple rules — is the prize.

## Feedback loops
- **Positive:** success breeds success (leader accelerates) → runaway winners; needs a brake or hard
  end-trigger.
- **Negative:** success is taxed / trailing is aided → keeps races close but can feel unfair if heavy.
Balance both so the game stays tense to the end without punishing skill.

## MDA framework (Mechanics / Dynamics / Aesthetics)
Hunicke, LeBlanc & Zubek (2004):
- **Mechanics** — rules & components (what you write).
- **Dynamics** — run-time behaviour that emerges in play.
- **Aesthetics** — emotional responses evoked (the "8 kinds of fun": sensation, fantasy, narrative,
  challenge, fellowship, discovery, expression, submission).
Designers build left→right; players experience right→left. Great for diagnosing *why* a tweak changes
the feel.

## Player counts & scaling
The game must work across its stated range. Techniques: add/remove board sections or cards, adjust round
count, neutral/"dummy" players at low counts, count-specific rules. The "best at N" sweet spot is real
(see BGG best/recommended counts).

## Solo modes & Automa
A dedicated single-player mode, usually an **Automa** — a rules/card system simulating an opponent
without full AI (popularized by Automa Factory for Scythe, Viticulture, Wingspan, Terraforming Mars).
Now a near-mandatory feature and a major growth segment. Good Automa = low-upkeep, real pressure,
scalable difficulty.

## Table presence
The visual/tactile draw on the table — insert trays, 3-D pieces, art, component quality. Drives shelf
appeal and crowdfunding pledges; distinct from strategic quality.

## Weight / complexity (BGG scale 1.0–5.0)
Community estimate of rules complexity/effort — **complexity, not quality or depth**:
- ~1.0–1.9 light/gateway (Ticket to Ride ~1.8, Azul ~1.8)
- ~2.0–2.9 medium (Wingspan ~2.5, Catan ~2.3)
- ~3.0–3.9 medium-heavy (Terraforming Mars ~3.2, Ark Nova ~3.7, Brass ~3.9)
- ~4.0–5.0 heavy (Twilight Imperium ~4.3; most 18xx/heavy wargames)

## A quick design self-check
- Is the core loop satisfying on turn 1 *and* turn 10?
- Does every turn present a meaningful decision (not a forced/obvious move)?
- Where's the tension? What stops a runaway leader? What ends the game?
- Input vs output randomness — did I choose on purpose?
- Depth-to-complexity ratio: can I cut a rule without losing depth?
- Does it scale to all stated player counts? Is there a solo mode?
- What's the aesthetic (the fun) I'm actually delivering (MDA)?
