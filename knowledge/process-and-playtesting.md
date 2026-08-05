# The Design & Publishing Process + Playtesting & Rules Writing

## The indie design pipeline

1. **Idea / concept.** A mechanism seed, a theme, or a "what if." Define the core loop and target
   (weight, player count, length, audience) early.
2. **Paper prototype.** Cheap, ugly, fast — index cards, cubes, printouts. Make it **playable in a
   day**, not pretty. Digital prototyping (Tabletop Simulator, Tabletopia, Screentop, Google Sheets)
   is now standard for rapid remote iteration.
3. **Self-play / solo testing.** Break your own game; find dominant strategies and dead turns before
   spending testers' time.
4. **Playtesting — iterate (the heart of the process), in expanding circles:**
   - *Internal / friends* — rough, forgiving.
   - *Local groups & designer meetups.*
   - **Blind playtesting** — strangers play **from the written rules only, no designer present**. The
     single most important test; it exposes rulebook failures, unclear iconography, and false
     assumptions. Do it before you think you're done.
5. **Iteration loop.** Change **one variable at a time**, log results, kill your darlings, watch for
   AP, downtime, runaway leaders, dominant strategies. Expect dozens to hundreds of plays.
6. **Balancing & math.** Tune economy/costs, curve difficulty, verify counts scale, spreadsheet
   resource flows.
7. **Art & graphic design.** Theme integration, language-independent iconography, component list,
   information design. Often the largest cost.
8. **Rulebook.** Written and re-written continuously (not last) — see below.
9. **Path to market — choose:**
   - **Pitch to a publisher:** royalties (~5–10% of wholesale typical; sometimes 3–7%), publisher
     funds art/manufacturing/marketing; you cede control. Sell-sheet + clean prototype are the tools.
   - **Self-publish via crowdfunding:** keep control and margin, assume all risk/capital/logistics.
   - **Hybrid:** prove demand with a small crowdfunded run, then licence for wider distribution.
10. **Crowdfunding (if self-publishing).** Kickstarter, **Gamefound**, or **BackerKit**; build an
    audience/mailing list first, ship a compelling page + demo (often a free TTS/Tabletopia module),
    set stretch goals carefully, plan a **pledge manager** for add-ons/shipping.
11. **Manufacturing & fulfillment.** Choose a manufacturer, order a pre-production copy, run QC, plan
    freight + regional fulfillment (VAT, tariffs, shipping are major 2024–2026 cost/risk factors).
12. **Post-launch.** Errata, FAQ, community, expansions, reprints.

## Rules-writing best practices

**Structure:** theme/overview → components list → **goal / win condition (state it early)** → setup →
turn structure / flow of play → detailed action reference → end-game & scoring → appendix/FAQ/glossary.

- **Teach in order of play.** Big picture and objective before fine detail; players anchor rules to
  *why* they matter.
- **One concept per section; short sentences; consistent, defined terms.** Capitalize game-specific
  Keywords and use them consistently.
- **Show, don't just tell:** worked examples, diagrams, callouts for every non-obvious rule; annotate a
  sample turn.
- **Iconography key** + a **quick-reference / player-aid** card. Heavy games live or die by player aids.
- **Anticipate edge cases** in a FAQ: deck runs out, ties, simultaneous effects.
- **Blind-test the rulebook itself.** If new players can't set up and play correctly without you, the
  rulebook — not the players — failed.
- Modern aids: rules video, solo-mode section, errata hub.

## A lightweight playtest loop (what the `bg-playtest` agent runs)

1. State the **hypothesis / question** for this session ("does the economy stall at 4 players?").
2. Define **what to observe** (dead turns, AP moments, runaway leader, confusion points, fun spikes).
3. Run it; **log** with the `templates/playtest-log.md` template (counts, durations, quotes,
   scores, what broke).
4. **Synthesize** — one insight per finding, ranked by severity.
5. Propose **one change at a time**; record it in `decision-log.md`; re-test.

Cross-reference: [`design-fundamentals.md`](./design-fundamentals.md) for the levers you'll be tuning,
[`trends-2026.md`](./trends-2026.md) for platform/crowdfunding context.
