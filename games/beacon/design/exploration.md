# Beacon — Exploration (design directions considered)

*Output of the `bg-explore` stage. Divergent options, then the direction we committed to.*

## Idea dump (by axis)

**Core-loop candidates**
- (A) Simultaneous **blind Signal** commit → higher wins Tide + pick. ✅ chosen
- (B) **Trick-taking** with a lighthouse "lead suit" each round. ✗ crowded core (Fox in the Forest).
- (C) **Drafting** ships from a shared row with action cards. ✗ weaker direct tension for 2p.
- (D) **Real-time** "guide the ship before the fog rolls in" sand-timer. ✗ hard to test remotely / not cozy.

**Blend logic** — blind commit is exciting but shallow alone; pairing it with the **Tide tug-of-war**
gives a persistent stake (the blind bid affects more than one ship) and **set collection** gives a
long-game reason to sometimes throw a bid. Each mechanism covers another's weakness.

**Signature-twist options**
- Tide **reclaim** for the loser (catch-up). ✅ chosen — great 2p tension valve.
- **Fog** push-your-luck: grab a face-down ship. → kept as an optional module, not core.
- **Sabotage** signals that cancel the opponent. ✗ too swingy / feel-bad in a filler.

**Theme integration** — the lighthouse *beam* = your Signal; the *Tide* literally pulls ships to a
harbour; *fog* = hidden information. Mechanism and theme reinforce cleanly (not pasted-on).

## Directions (converged)

1. **Beacon (chosen)** — blind Signal commit + Tide tug-of-war + suit set-collection; cozy nautical;
   ~1.8 weight, 20 min. Strongest fun-to-complexity; all input randomness.
2. **Fogbank** — same theme but push-your-luck-first (Fog as the core). Riskier, swingier; parked as a
   possible variant/expansion.
3. **Harbourmaster** — heavier engine/economy version (build harbour upgrades). Rejected for now: breaks
   the "20-minute filler" brief.

## Recommendation
Commit to **Direction 1 (Beacon)**; hold Fog as an optional advanced module to test later.
