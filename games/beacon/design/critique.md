# Beacon — Design Critique (red-team) — **v0.3 re-critique**

*Output of the `bg-critic` stage, iteration 3. Judged against the designer's goals (elegance,
tension-with-warmth, 2p-first). **This supersedes the v0.2 critique** — that version is preserved in git
history. This pass deliberately does NOT rerun v0.2's findings; it applies the studio's newer lenses
(social axis / synchronicity / playtime fit; per-count capping; modes-&-expansion restraint) and reports
only what is genuinely different. A short "still stands" list at the bottom carries forward the v0.2
points that remain live.*

**What v0.3 changed (don't re-litigate):** the scaled Tide bonus (`2×|position|`) fixed the v0.2
successor problem — pure grabbing fell to ~45–53%, four *different* approaches now sit within ~3 pts, and
the Tide is active in optimal play. That was the right fix. New risks below are the layer v0.3 exposes,
plus the social/scope lenses the earlier critique never applied.

---

## Top risks (ranked) — NEW this pass

### 1. Social-axis mismatch: Beacon is *sold* as a tense read of your rival, but its information structure may make it a quiet, near-deterministic deduction you could solve in silence.
The one-liner promises "outread your rival — commit before you know theirs." The intended aesthetic (MDA)
is **challenge + a psychological read** — the fun is *the other person across the table*. But three
mechanics quietly drain the read, and none of them is a balance problem the sim can see:
- **Hands are open.** Played Signals stay face-up, so both keepers always know the other's *remaining*
  set. The hidden layer is only ever "which one of your known-remaining cards this round."
- **The set is tiny and depletes.** You hold 6 and commit 4 per Night. By round 3–4 of a Night each
  player is choosing 1 of ~2–3 known cards, and the opponent knows it too. The bluff space is largest on
  round 1 and collapses toward arithmetic by round 4 — so **each Night front-loads the read and the tail
  is nearly forced.** The tension arc inside a Night is uneven.
- v0.3 gave you a real *grab-or-contest* fork (good, strategic depth), but a fork the sim rewards is not
  the same as a *read that feels social*. Choosing "grab this round or push the Tide" from a shrinking
  known hand can be pure private computation — the fundamentals warning applies verbatim: *"don't let a
  game that's meant to be social be solvable silently."*

*Why it matters for this designer:* the whole pitch is the blind read, and the taste signature is
**tension with warmth** — a live mind-game between two people. If the read is actually silent
card-counting over ~12 commits, Beacon is a competent little deduction filler but it isn't delivering the
*social* aesthetic it advertises, and the "warm, tense duel across a café table" feel doesn't land. This
is the single most important open question about the game.

**Probe (human, decisive — this is what session 1 must answer):** after players "get it," ask two things
directly — *(a)* "were you reading your **opponent**, or just counting cards?" and *(b)* the control test:
play one Night with **hands fully face-up** (open the current commit too, decide aloud) — if the outcome
and feel barely change, the hidden layer is cosmetic. Then play one Night with **played Signals kept
hidden** (only the reveal is public) and see if the read gets richer and more social. That A/B tells you
whether the bluff space is real or decorative.
**Probe (sim, cheap pre-check):** instrument a **late-round decision-triviality metric** — in rounds 3–4,
how often does open-hand info leave a single non-dominated Signal (a forced move)? And how often is the
Night's outcome determined *before* the reveal once both best-responses collapse? If rounds 3–4 are
mostly forced, the read only lives in rounds 1–2, and you'd want a longer/hidden hand to spread it.

### 2. v0.3 may have overcorrected the Tide from *dormant* → *over-decisive*, and the draw rate doubled.
The v0.2 problem was the Tide idling at high skill. The scaled bonus fixed that — but possibly too hard:
- A decisive Tide is now worth **up to 6 VP/Night** (was a flat 3) on ~30-point games, and the sim reports
  the Tide **decisive in ~56%** of grab-vs-contest games. A signature mechanic that flips *more than half*
  of games is as much a flag as one that never fires — it risks making the ship-grabbing and
  set-collection layers (a third of the rules) into decoration.
- The **draw rate rose to ~21%** in that matchup (field tie 13.1%, up from v0.2's ~5.7%). For a 20-minute
  cozy-competitive duel played by a couple, a **1-in-5 no-winner** result is a real feel-bad — you spend
  the whole session on a tense read and nobody wins — and the current tiebreak (most Naval → shared) is
  weak.

*Why it matters:* the fix that made the Tide load-bearing may have tipped it into being the game, and the
higher draw rate directly undercuts the competitive payoff. This is a v0.3-only risk the v0.2 critique
couldn't have seen.
**Probe (sim):** on the *strong cross-matchups* (`always_high:grabber`, `hand_smart:grabber`), report
`tide_decisive`, a "**Tide points alone predict the winner**" rate, and `tie`. If Tide-decisive stays
>~50% and ties >~15% in strong play, dial the scaling from `2×|pos|` toward `1.5×` **or cap the per-Night
Tide bonus at +4** (a middle setting between flat-3 dormancy and 2× dominance) and re-sim for
Tide-decisive ~30–40% and ties <10%. Cheapest independent fix: **add a real tiebreak** (Tide marker
position, or most 4-value ships) to kill the draw feel without touching the scaling.
**Probe (human):** do end-of-Night Tide scores feel *earned* or *swingy*? Does a draw land as
anticlimactic?

### 3. Scope is being pre-invented — hold the line on the focused 2p duel; build nothing modal until the base wins a human playtest.
`architecture.md` sketches a solo automa, a co-op "Storm" variant, a "Ports & Cargo" expansion, *and* a
Coastline campaign. To be fair, it's appropriately hedged (all "optional / later / hold back") — as a
*map of hooks* it's fine. The risk is treating it as a **roadmap**. Per the modes-&-expansions **restraint
principle**: scope must be *earned*, and Beacon's base has had **zero human playtests** — every finding to
date is simulated. Inventing four downstream products before session 1 is exactly the "don't build modes
to look ambitious" trap.
- The **co-op "Storm" variant is the specific temptation** — it hits the designer's constrained-comms-co-op
  love (the real north star), which makes it magnetic. But it is essentially a *different game* sharing
  components (two players vs a threat deck), not a mode of the blind duel. Building it now would split
  energy away from proving the actual current project — the competitive duel — is fun.
- Elegance also gates the expansion: `component_types` is **at its cap (4)**; "Ports & Cargo" adds new
  ship types → a budget breach that must be a conscious logged decision, not drift.

*Why it matters:* the studio's discipline is one focused thing done excellently; a strictly-2p duel done
well is a *complete, valid* product (see risk-4 note on the cap). The fix is a gate, not a cut.
**Probe (gate, not sim):** build nothing modal until the 2p duel has *won a human session and been called
fun*. When that gate passes, the honest test for the co-op variant is "is this a mode of Beacon, or a new
game wearing its art?" — if the latter, it deserves its own `bg-ideation` slot, not an "expansion" label.

---

## Smaller issues (new or newly sharpened)
- **The set-collection layer may now be noise, not just the run bonus.** v0.2 flagged runs; v0.3's scaled
  Tide sharpens it — if the Tide decides ~56% of games, do *convoys* even move the needle? Probe: A/B a
  sim with **all set bonuses off** and report win-rate/margin change. If negligible, the set layer is
  ceremony on top of a Tide-and-ships game.
- **Strictly-2p with no solo mode = the box only works when two people are present.** For this designer
  (regular 2p partner, café/couples audience) that's an acceptable, on-brand constraint — noted, not a
  flaw. Just don't let it become the *reason* a solo automa gets built prematurely (see risk 3).
- **The synchronous standoff could invite AP-lite.** A pure simultaneous-reveal read between two
  analytical players can stall ("you think, I think, we both hover"). Branching is tiny (1 of ~4 cards),
  so this is low-risk — but watch commit time in session 1; if each reveal takes >20–30s, the ~20-min
  clock slips.

## What's working (protect these — do not "fix" them away)
- **The synchronicity/clock/audience fit is genuinely good.** Simultaneous blind reveal = ~zero downtime,
  hard-caps playtime, and ~20 min for a 2p café/couples filler is a clean target-match. **Do not move to
  sequential turns** — it would add downtime and stretch the clock for no gain.
- **The strict 2p cap is a deliberate, correct decision — a strength, not a limitation.** It matches the
  designer's 2p-first taste, removes kingmaking entirely, and lets catch-up be built in. `architecture.md`
  is right that 3–4p would be a re-engineering, not a mode. A tight 2p done well beats a bolted-on wide
  range — the cap is the studio principle working as intended.
- **v0.3's scaled Tide restored a real grab-or-contest fork** (per sim). Don't revert to flat-3 — tune the
  *amount* (risk 2), not the *idea*.
- **Elegance is still green** and the budget is respected.

## Still stands from v0.2 (unchanged — see git history for full text)
- **Inverted core verb** (the *dim* light grabs the ship) — teachability tax; still a session-1 teach-test
  item (count rounds until players stop mis-predicting the ship winner).
- **First-keeper token quietly deciding tie-heavy rounds** — now *more* relevant given v0.3's higher draw
  rate; watch whether the token, not the read, does the work.
- **The sim can't see the ship-choice decision** (shared greedy picker) — still true; it makes both the
  set-bonus verdict *and* the new social-read verdict (risk 1) sim-blind. A strategy-dependent picker
  (`deny` vs `max-value`) would help.
- **Denial is gentle** (loser always gets a ship) — unchanged; the optional **Rocks** variant is the dial
  if duels feel frictionless.
- **Cut the run bonus, keep convoys** — still the cleanest elegance win (critic + elegance agree).

## Decision for the human — ONE next thing (A/B/C)
The sim has done its job: the math isn't broken and a real fork exists. The one thing that decides whether
Beacon is worth continuing is **risk 1 — is the blind read actually a social read, or silent arithmetic?**
Only humans can answer it.

- **(A) — recommended. Go to human session 1 now, instrumented for the read.** Include a **face-up control
  Night** (open the current commit) and a **hidden-hand variant Night** (played Signals stay secret) so you
  directly test whether the hidden layer earns its place and whether the read is social. **Freeze all
  mode/expansion work until this returns.**
- **(B).** First run the two cheap sim pre-checks — the **late-round forced-move rate** (risk 1) and
  **Tide-decisive + tie in strong cross-matchups** (risk 2) — to quantify how thin the late-Night decision
  is and whether the Tide overcorrected, *then* session 1. Best if the sim's already wired and you want
  numbers in hand first.
- **(C).** Dial the Tide (`2×` → `1.5×` or cap +4) and add a tiebreak now, re-sim, then session 1. Premature
  in my view — don't re-tune the Tide until a human confirms it *feels* swingy.

My call: **A**, with B's two metrics as a 30-minute pre-check if the sim is already set up. Hold C until
humans say the Tide feels off. And hold the whole mode/expansion roadmap (risk 3) behind the session-1 gate.
