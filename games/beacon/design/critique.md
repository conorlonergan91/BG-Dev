# Beacon — Design Critique (red-team) — **v0.2**

*Output of the `bg-critic` stage, iteration 2. Judged against the designer's goals (elegance,
tension-with-warmth, 2p duel). Uses the v0.2 sim in `playtests/sim-results.md` / `sim-notes.md`.
**This replaces the v0.1 critique.***

**What v0.2 fixed (don't re-litigate):** the v0.1 #1 problem — `always_high` dominant at 66.7% —
is gone. "Loser of the beam picks the ship first" taxed greedy high-play; no line crushes the field,
margins fell from ~10 to ~5.8, and a rule-aware `grabber` beats the naive field. Good loop. The
findings below are the *next* layer, not a rerun of the old one.

## Top risks (ranked)

### 1. The best line is a one-line rule, and skilled mirror play may hollow into a reverse-auction. *(the successor to the old dominance problem — read this one carefully)*
The v0.2 rule inverts the auction: to get the ship you want, you bid **low**; bidding high only
concedes the ship and banks a Tide step. The sim's winner, `grabber`, encodes this in a single
sentence — "bid `min` if a 3/4 is showing, else `max`" — and it leads at 58.7%. The corroborating
signal is `always_low` beating `hoarder` **80%**: grabbing ships massively outweighs winning the
Tide. So the "skill" here is a **one-time discovery** of an obvious heuristic, after which two players
who both know it are in mirror territory (`grabber` vs `grabber` ≈ 51%, i.e. a near coin-flip decided
by deck luck and the first-keeper token). Worse, in the *exact* mirror the good-ship round resolves as
`0 vs 0` → a **tie** → no Tide move and the first keeper simply takes the ship. The blind "read" the
whole design is built on can evaporate at equilibrium into "both bid rock-bottom and hope for the
token." *Why it matters for this designer:* depth-from-simplicity is the north star; a game whose
optimal play is a memorizable one-liner and whose duel collapses to a token flip is elegant but
**shallow**, not deep.
**Probe (sim, cheap):** add smarter strategies the current six miss — (a) `concede_for_tide`
(outbid-by-one to trade the ship for a Tide step), (b) a hand-counting line that exploits low-card
scarcity, (c) a Tide-first line. Re-sim. *If a cleverer line beats `grabber`, depth is real (good). If
`grabber` still wins by ~8pts and its mirror sits at ~50% with a high round-tie rate, the read is
cosmetic.* Also report **round-tie rate** and **fraction of games decided by the first-keeper token**.
**Probe (human):** session 1 — once both players "get it," do they still feel a live read each commit,
or does it settle into "we both bid low, shrug, flip"? That ache-or-shrug is the whole verdict.

### 2. The Tide — the signature twist and the 2p catch-up valve — may go dormant exactly when play gets good.
The Tide only moves when someone **voluntarily bids high**, but skilled play bids low on every
good-ship round. Under mirror `grabber`, good rounds tie (no Tide move) and trash rounds tie (no Tide
move) → the Tide can sit at centre all Night → **no +3 bonus and no initiative flip**. The
catch-up-via-Tide lever the designer is relying on for a gang-up-proof 2p arc stops firing precisely
under the strong symmetric play it's meant to govern. The field-wide `tide_decisive = 26%` is
reassuring only because the field contains *bad* players who bid high; it likely overstates Tide
activity between two good players. *Why it matters:* "the tide turns" is billed as the signature and
the comeback brake; a mechanic that idles at high skill isn't pulling its weight.
**Probe:** in the same re-sim, report `tide_points_total`, `tide_decisive`, and **% of Nights the Tide
ends dead-centre** *for `grabber`-vs-`grabber` and `always_low`-vs-`always_low` specifically* (not the
field average). Expect near-dormant → confirms the risk.

### 3. Inverted core verb: teachability and the cozy-quick-filler feel take a hit.
The fantasy and the box promise "your **bright** beam guides the richest ships in." v0.2 says the
**dim** light snatches the ship and the bright beam only nudges a track. The rules-draft flavour ("a
dim light snatches the cargo in front of it while your bright beam steers the Tide") is a well-written
*rationalization of a counterintuitive rule* — it doesn't make the rule intuitive. For a ~1.8-weight
20-minute filler meant to be taught in one pass to couples and café players, a core verb that fights
intuition is a real teachability tax and slightly cools the "warm" tone (every new player mis-predicts
who gets the ship for the first few rounds). *Why it matters:* elegance includes *legibility*; a rule
you must un-learn your instincts for is a hidden complexity cost.
**Probe (human):** teach test — count rounds until each player stops mis-predicting the ship winner,
and log "wait, what?" moments in the first Night. If it's more than ~2 rounds, consider a theme reskin
that makes low=grab intuitive (e.g. reframe the beam as "the ship you *warn off* vs the one you *let
pass to you*").

### 4. Two set-collection layers (convoy **and** run) — runs likely don't earn their keep.
Convoys ({C,P,N}) are steerable and thematically clean ("a balanced harbour"). Runs (3 consecutive
values in one suit) are **not steerable**: you claim ~half the deck across 3 Nights, you only ever
pick from the 2 ships in the Channel, and which values appear is input luck — so a run mostly
*happens to you*. That adds a scoring step and a little swing without a decision. The sim can't even
see this (it uses one shared greedy picker for both players), so runs are pure scoring noise in the
model today. This is the designer's own flagged first-cut.
**Probe:** A/B sim with runs off; and count how often a run actually completes and how often it flips
the winner. If runs rarely complete or complete by luck, cut them — keep convoys.

## Smaller issues
- **First-keeper token quietly becomes the decider.** Under skilled (tie-heavy) play it breaks every
  tie for first ship-pick, and it flips by Tide-loss / fewer-ships. That's a fine catch-up loop, but
  if the game's real fulcrum is "who holds the token on good-ship rounds," the per-round *decision* is
  thin. Watch whether the token, not the read, is doing the work.
- **The sim can't see the ship-choice decision.** Both players share one greedy picker, so the genuine
  v0.2 decision — *when you win first pick, take raw value vs deny the opponent a convoy/run* — is
  invisible to the model, which both **understates** real depth and makes the convoy/run verdict
  unreliable. Upgrade: make the picker strategy-dependent (a `deny` picker vs a `max-value` picker) and
  see if set bonuses create a real fork.
- **Denial is still gentle** (the loser always gets a ship). Low take-that is on-brand for "warm," but
  the optional **Rocks** variant (Channel of 3, third ship lost) is the right dial if duels feel
  frictionless.
- **`always_low` at 54% is a red herring, not a second dominance problem** — it's buoyed by crushing
  the weak field (80% vs hoarder) but *loses* head-to-head to both `always_high` (41%) and `grabber`.
  The real concern is `grabber`'s *simplicity* (risk #1), not `always_low` being unbeatable.

## What's working (protect these)
- **The v0.2 rule itself.** No crushing line, margin ~5.8 (much closer games), `grabber` > `reactive`
  (skill rewarded). Do not tune "loser picks first" away — it's the fix.
- **The 6-card ladder + hold-2 is doing quiet, elegant work.** Only three cards are ≤2 but you play
  four per Night, so **at least one high bid is forced every Night** — the economy rations your "grab"
  bids and guarantees the Tide *must* move at least once. That's a real constraint carrying its weight;
  don't drop to a ratio that removes the forced-high pressure without re-checking.
- **Closer games / low tie rate** (margin 5.8, ties 5.7%) — the swinginess flagged in v0.1 is resolved.
- **Elegant footprint** — 36 cards + a track still hits the 20-minute brief.

## Decision for the human — ONE next thing (A/B/C)
The top two risks (solved heuristic + dormant Tide) are *nearly free to diagnose in sim and the sim
literally cannot answer risk #3*, so run the loop in this order:

- **(A) — recommended.** Run the risk-1/2 **diagnostic sim** (add `concede_for_tide` + a hand-counting
  line; report mirror-`grabber` Tide activity, round-tie rate, token-decides rate). **If it confirms
  the Tide goes dormant and `grabber` still dominates,** apply the smallest fix — **raise the Tide's
  pull** so a voluntary high bid is a live choice on good rounds (Tide bonus +3 → +5, *or* a Tide step
  grants a tiny immediate reward) — and re-sim for the appearance of voluntary high-bids. Tightest
  design→sim loop; targets #1 and #2 together, adds no rules.
- **(B).** Skip straight to **human session 1** to feel whether the inverted verb (risk #3) is
  fun/teachable and whether players find the concede-for-Tide tension — the one thing sim can't model.
  Best if you'd rather protect fun before touching numbers.
- **(C).** Cut the **run bonus** (keep convoys) and A/B it — the cheapest elegance win, but it's a
  smaller-issue fix, not the core risk.

My call: **A**, and pre-commit to the Tide-pull bump if the diagnostic confirms dormancy — then spend
session 1 on the inverted-verb feel (B) with the numbers already de-risked.
