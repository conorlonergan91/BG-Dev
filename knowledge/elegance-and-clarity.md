# Elegance & Clarity Playbook

How the studio keeps games at their target weight and their rules a joy to read. Owned by
`bg-elegance`; every designer should internalise it. Cross-refs: `design-fundamentals.md`
(depth vs complexity), `process-and-playtesting.md` (rules-writing).

## The core principle
**Elegance = maximum depth from minimum complexity.** Complexity is the barrier (rules/components to
learn); depth is the reward (rich decisions that emerge). Prize the ratio, not fewer rules for their own
sake. Every rule must **buy depth commensurate with the complexity it adds** — otherwise cut it.

## Set the budget at the start
Define the game's **target weight** (BGG 1–5) and a `complexity-budget.json` at kickoff, with caps that
fit the target (an elegant ~1.8 filler ≠ a 3.5 hobbyist game). Example caps for a 20-min filler:
```json
{ "target_weight": 1.8, "max_rulebook_words": 900, "max_keywords": 8,
  "max_exception_words": 8, "max_component_types": 4, "max_player_aid_lines": 16 }
```
Then `python tools/complexity/check_complexity.py --game games/<slug>` tracks drift each iteration.
**The only honest responses to going over budget: simplify back under, or consciously (and log-ably)
raise the budget.** Never silent creep.

## The cut test (simplification review)
For every rule/component/scoring layer, ask:
- **Would the game play fine without it?** If yes → cut it.
- **Does it create a *decision*, or just bookkeeping / input luck?** Non-decisions are the first to go.
- **Do two rules overlap?** Merge them. **Is an exception single-use?** Fold it into the base rule or drop it.
- **Does a component earn its place**, or could a token/card already present do the job?
Always name **what is lost** by a cut (often: nothing, or a rarely-relevant edge). Confirm borderline
cuts with an **A/B simulation** (`bg-playtest`) or a targeted playtest question. Removing a rule is worth
more than adding one — but never cut a genuine **fun spike** or a real decision just to shrink the count.

## Rulebook: succinct, clear, fun
- **Teach in order of play**; goal/win condition stated early (see `process-and-playtesting.md`).
- **One concept per section; short sentences; consistent, defined Keywords** (keep the glossary small —
  every new capitalised term is complexity).
- **Show, don't tell**: a worked example beats a paragraph. **Iconography** beats words when it can be
  language-independent.
- **Fun to read**: warm and confident, with a light touch — not a legal document. A rulebook that's a
  pleasure to read gets taught correctly.
- **Blind-test the rulebook itself** — if new players can't set up and play from it alone, the rulebook
  failed, not the players.

## Player aid: ruthlessly short
One glance should recover the turn sequence + scoring. Bullet the flow; lead with the core decision.
If it doesn't fit on a card, the *game* (not the aid) is probably too complex — treat an overflowing
aid as a complexity alarm.

## FAQ discipline
A short FAQ appendix catches genuine ambiguities (deck runs out, ties, simultaneous effects) so the core
rules stay lean. But:
- **A recurring or obvious FAQ entry means the rule is unclear — fix the rule.** The FAQ is a safety net,
  not a patch pile.
- Keep it minimal; every entry is a small admission the core text could be clearer.

## Signals you're bloating (from the complexity gauge + judgment)
- Rulebook word count climbing each iteration; exception-words ("except/unless/instead") rising.
- New keywords/components added without removing any; the player aid spilling past one card.
- The critic's teachability probe finds players mis-predicting outcomes → a clarity/complexity cost.
When these move the wrong way, run `bg-elegance` before adding anything else.
