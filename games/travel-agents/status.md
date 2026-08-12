# 📋 Travel Agents: Taiwan Food Tour — Status (current state of play)

> **The live dashboard.** Owned by `bg-producer`. Always reflects the CURRENT version — readable in under a
> minute. If you want the *why* behind a decision, see `decision-log.md`; the *history* lives in `archive/`;
> the CD's own steers live in `director-brief.md`. This doc answers only: **where are we right now?**
> _Last updated: 2026-08-11 · by bg-producer (presentation rebuild done + player-aid card landed)_

## Version
- **Current:** `V7-M` — *the 3–6-player Taiwan street-food area-majority race: pile follower meeples on
  vendors to win the biggest crowd, race a vendor-depletion clock (+ a Closing-Time die) through one eating
  day, and score on two tracks — completed tours + won vendors.*
- **Shipped / frozen builds:** V7-M merged to `main` in **PR #13** (2026-08-10). The **2026-08-11
  vendor-economy reshape + per-phase die fix** (re-sim-validated N=400), the **presentation rebuild** to the
  reshaped 30-vendor deck (commit `2313f40`), and the **per-player double-sided player-aid card** (commit
  `111c916`) are all landed on-branch — ready to PR + merge to `main`. No `builds/build-N/` snapshot cut yet.
- **Theme (pivot COMPLETE 2026-08-11):** the secret-agent wrapper is **scrapped** → **"Wacky Races,
  Taiwan-food edition"** (over-the-top, battle-hungry rival agents), title **Travel Agents: Taiwan Food
  Tour** applied everywhere (docs, rulebook, `make.sh`, art briefs). Felt identity, voice, names, rulebook,
  and all 8 art briefs re-founded + de-spied; 12 spy-era design notes archived to `archive/design-history/`.
  **Mechanics unchanged** — presentation/prose only.

## Pipeline stage
**Prototype-ready.** Design + development are CLOSED for V7-M at a clean, sim-validated state (N=400) —
including the day-engine / night-payoff **vendor-economy reshape** and the **per-phase Closing-Time die**
fix. The prototype kit is fully rebuilt to the reshaped 30-vendor deck, and the player aids are now
per-player, card-sized, double-sided. The next real work is a **blind human playtest at 4p + 6p** — that
table is the next arbiter, not more sim.

## Done · In-flight · Next
- **✅ Done (this version):**
  - **Vendor-economy reshape + die-cadence fix (2026-08-11) — CD-signed, sim-validated N=400.** The deck was
    reshaped into a **DAY engine / NIGHT payoff**: 18 cheap low-VP day **engine-seeds** (build the region-icon
    discount engine) → 12 scarce, expensive, **no-icon** night **trophies** (the payoff the built engine
    affords). Stripping night icons killed the old mid-vendor hoarder double-dip. The Closing-Time die moved to
    a **per-phase cadence** (day after L rounds L=2/3/3/3; night every round). Re-sim confirms **an engine
    forms, tours lead** (booking-share 67–75% / vendor-share 25–33%), **hoarder dead** (sub-fair 12–27% every
    count), and the 4–5p **stall killed** (3/10/7/3%). Vendors 25→30. Authority: `components/vendors.csv`,
    `components/map.json`, `playtests/sims/sim-reshape-N400-results.txt` + `sweep-two-dice-N400-confirm.txt`.
  - **Systems design** — area-majority follower-meeple fight, vendor-depletion Day→Night clock + Closing-Time
    die, two-track VP, agnostic tours + Pot-Luck, the 6-type mono ingredient taxonomy, the six V7-M character
    kits. Spine LOCKED.
  - **Sim validation (N=400)** — balanced at every count (vendor-only hoarder deeply sub-fair, tours dominate,
    battles scale); mono 6-type taxonomy shipped, the 8-type split **PARKED** behind flag `SPLIT_TAXONOMY`
    (default OFF).
  - **Presentation rebuild (2026-08-11) — COMPLETE (commit `2313f40`).** The rulebook was re-taught to the
    day-engine / night-payoff model + per-phase Closing-Time die and trimmed back under the complexity budget
    by bg-elegance (rulebook_words **2271 / 2280**). Exports fully rebuilt to the reshaped **30-vendor** deck:
    vendor Screentop + print deck sheets, A3/A4 card print-and-play, `rulebook.{html,pdf}`. `exports/` now
    matches the new economy end-to-end.
  - **Player-aid card (2026-08-11) — LANDED (commit `111c916`), CD steer delivered.** The old verbose
    single-sheet player aid is retired and replaced by a **poker-card-sized (750×1050), per-player,
    double-sided** aid — a shared FRONT listing the six turn actions (labels + one-line reminder; full teach
    left to the rulebook), and one BACK per character with that agent's ability + flaw in brief, tinted in the
    character's colour (漢字 + Tâi-lô + catchphrase). New `--type aidcard` renderer in
    `tools/boards/build_board.py`; new schema `components/player-aid.json` pulling display fields from
    `characters.csv` so it can't drift; `make.sh` renders into `build/aid/` → `exports/aid/` +
    `exports/screentop/` + a true-size cut-out PnP `exports/print/pnp-player-aids.pdf`. Guardians green.
  - **Prototype kit** — Screentop deck sheets, player/character boards with embedded AI mock-up portraits,
    per-player double-sided aid cards, A4/A3 print-and-play, map — all current in `exports/`.
  - **Rulebook** — fully current: de-spied to the Wacky-Races voice ("The Job" intro), scoring reconciled to
    **two-track VP + flat −1**, the **`min_followers` crowd-floor** taught, re-taught to the day-engine /
    night-payoff economy + per-phase die, trimmed back under the complexity budget (**2271/2280**), title A.
    `exports/rulebook.{html,pdf}` + `cover.png` regenerated.
  - **Voice bible** — `prose-identity.md` authored and promoted to a studio standard.
  - **Art prep** — art prompts + `art/ta-art-context.zip` (2.7 MB) ready for the CD's ChatGPT art generation.
  - **Events + tours currency/variety pass (2026-08-11)** — event deck de-monotonised (the "keep 1 fewer"
    pinch pile 10→6, the rest converted to spoil/sink/block/restock; weather now 5 distinct verbs; the triple
    "Sold Out" split into 3 cards; gifts split by scope), the "Fully Booked 客滿" logic bug fixed →
    **Sharing Tables 併桌**, funnier on-voice titles; tour flavour punched up + one hanzi fix. Counts held
    flat (map.json / pacing stable, no new keywords); **bg-critic: ship-to-table, no blockers, warmth rail
    holds**; guardians green; market + booking deck sheets regenerated.
  - **Vendor economy + die cadence — LANDED (2026-08-11).** The earlier Splendor-style steep re-price
    (checkpoint `3486f5e`) FAILED the sim (no engine formed, dead apex, tier-2 hoarding breaching 41–42%
    vendor-share). Fixed by **reshaping the DECK** (day-engine / night-payoff, night icons stripped) + a
    **per-phase die cadence**, not by re-pricing — CD-signed, re-sim-validated N=400 (see the reshape bullet
    above + `decision-log.md`).
- **⏳ In-flight: nothing.** The whole V7-M line (events/tours + economy reshape + die fix + presentation
  rebuild + player-aid card) is landed on-branch and ready to PR + merge to `main`.
- **➡️ Next (recommended): a blind human table at 4p + 6p.** The reshape + die fix are sim-clean, so the
  table is the arbiter. **#1 watch: does the NIGHT still *feel* like a payoff phase** — the one accepted sim
  trade-off is that the per-round night die can close trophies faster than players claim them, so a couple
  fewer trophies get bought. Also felt-only / unmeasurable in sim: is the area-majority fight fun/tense, do
  the six kits band, and the open event questions (forced-placement-as-tax, the SINK shrug, hazard:boon
  ratio). The CD also generates the remaining art (map + vendor cards) from `art/ta-art-context.zip`.
- **⏭ Deferred design follow-ups (surfaced by the sweep — not blocking; a later design pass):**
  **N06 Big Sausage recipe oddity — PROPOSAL READY, FLAGGED for CD + re-sim (not applied).** The recipe
  still carries seafood×2 in a pork sausage. A de-seafood is designed — `meat;meat;meat;meat;meat;veg;pantry`
  (5 meat + garlic-as-veg + pantry) — which holds the §14 invariant (cost 7 · min_followers 3 · vp 8) and
  keeps N06 cross-region. It is **held, not applied**, because it zeroes North's *entire* night-seafood
  demand (2→0) and cuts total night seafood 14→12 — a structural change to the North↔South seafood contest
  that wants a CD call + re-sim (→ `bg-design`). **`Draw`/人氣 data flag — CLEARED on the data side:** no
  `draw` column in `vendors.csv`, no draw-target rows in `bookings.csv`, and the sim never reads `draw`
  (retired in the vendor loader; not a scoring scalar) — component data already matches the rules. Residue
  now lives only in a DRAW art panel + a `design-doc.md` mention and the `打卡人氣王` booking *name* (whose
  mechanic is the real `ingredient_cost_total` target — fine) → `bg-art-director` / `bg-continuity`. Then:
  migrate `design-doc.md` §15/§17 (event framework + clock) into `game-bible.md`, then archive it + fix its
  stale header (→ `bg-design`); reconcile `art/rulebook-figures.md`'s stale 2p / Buzz / Reach mechanics to
  V7-M (→ `bg-continuity` / `bg-infodesign`); the portrait-slot size mismatch (604×286 vs 900×1380 →
  `bg-infodesign`); the board clock-band vs deck-driven vs Closing-Time-die description mismatch
  (→ `bg-architect`); and the remaining data flags (EV-D07 pork name, Indigenous romanisation →
  `bg-developer` / consultant).

## Open decisions (waiting on the Creative Director)
*Nothing blocking.* All V7-M design decisions are made and logged (mono ship config, orphan-tour ceiling,
cap-raises, the Big Boss rename). The only thing awaiting the CD is **doing** the next step (art + table),
not a decision.

## Guardrail health
| Gauge | State |
|---|---|
| Lint (`check_game.py --theme night-market`) | ✅ **0 errors / 12 warnings** (warnings are the baseline "missing recommended column value/quantity" advisories — expected) |
| Complexity (`check_complexity.py`) | ✅ **in budget** — rulebook_words **2271 / 2280** (trimmed by bg-elegance after the day-engine/night-payoff re-teach); **player_aid_lines 8 / 22** (new per-player card schema); keywords 9/15; component types 8/8 (mono ship config) |
| Accessibility (`check_access.py`) | ✅ **pass** on the shipping mono config; MARGINAL flag exists **only** on the PARKED 8-type split (Rice/Noodles share the indigo hue) — not in play |
| Cost (`check_cost.py`) | **n/a** — Screentop-first prototype; physical COGS deferred until a physical run |
| Simulation | ✅ **last read balanced** (N=400, post-reshape): engine forms, tours lead (booking-share 67–75% / vendor-share 25–33%), hoarder dead (sub-fair 12–27% all counts), 4–5p stall killed (3/10/7/3%); paced by the per-phase die (day L2@3p / L3@4–6p, night every round) |

## Risks · watch-items
- ⚠️ **The human playtest is the real arbiter — sim ≠ table.** The make-or-break question (is the
  area-majority fight *fun/tense*, not degenerate?) and whether the six kits band with no crusher are
  *unmeasurable* in sim. **4p + 6p is the focus** (6p is the downtime watch).
- ⚠️ **Does the NIGHT still feel like a payoff phase? (the reshape's one accepted trade-off).** The
  per-round night die can close trophies faster than players claim them → a couple fewer trophies bought.
  Sim-clean, but whether the night reads as a *satisfying payoff* (not a rushed scramble) is table-only — the
  #1 thing to watch at the blind table.
- ⚠️ **Consultant-gated content — must clear a paid Taiwanese cultural + language consultant before any
  physical/public release:** (1) the character **The Big Boss (老大)** affectionate-fixer framing (warm,
  never a triad/gang caricature); (2) the **2 Indigenous East-region dishes** (E01 竹筒飯, E04 石板烤肉);
  and (3) the **5 new day dishes** added in the reshape — **N09 飯糰, N10 割包, C07 大麵羹, S07 蚵仔煎,
  E06 蔥油餅** — still need consultant + Tâi-lô vetting before print (specific watches: **N10 割包** secular
  check re 龍山寺 / temple association; **C07** English name currently "Thick Noodle Soup" to confirm).
  Screentop playtesting can proceed; art/print cannot without sign-off.
- ✅ **Drift watch — RESOLVED (2026-08-11 sweep).** The two-track scoring / flat −1 reconcile
  (`rules-draft.md` §1/§9, `components/manifest.md`), the `min_followers` crowd-floor teaching
  (`rules-draft.md` §5), and the character-kit reconcile (`names.md` / `v7-plan.md` → `characters.csv`) all
  landed and are guardian-verified. Remaining doc-consistency items are the non-blocking **deferred design
  follow-ups** listed under *Next* above.

## Next real step
**The Creative Director's call:** the prototype kit (reshaped 30-vendor deck, rulebook, per-player aid
cards) is complete — generate the remaining art (map + vendor cards) from `art/ta-art-context.zip`, then run
a **blind 4p + 6p human playtest** to answer RISK #1 (is the fight fun?), RISK #2 (do the six kits band, is
the Old Councillor rework balanced?), and the reshape's one accepted trade-off (**does the night still feel
like a payoff phase?**).
