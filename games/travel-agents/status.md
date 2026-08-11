# 📋 Travel Agents: Taiwan Food Tour — Status (current state of play)

> **The live dashboard.** Owned by `bg-producer`. Always reflects the CURRENT version — readable in under a
> minute. If you want the *why* behind a decision, see `decision-log.md`; the *history* lives in `archive/`;
> the CD's own steers live in `director-brief.md`. This doc answers only: **where are we right now?**
> _Last updated: 2026-08-11 · by bg-producer_

## Version
- **Current:** `V7-M` — *the 3–6-player Taiwan street-food area-majority race: pile follower meeples on
  vendors to win the biggest crowd, race a vendor-depletion clock (+ a Closing-Time die) through one eating
  day, and score on two tracks — completed tours + won vendors.*
- **Shipped / frozen builds:** V7-M merged to `main` in **PR #13** (2026-08-10). No `builds/build-N/`
  snapshot cut yet — the merge + `exports/` are the known-good state.
- **Theme (pivot COMPLETE 2026-08-11):** the secret-agent wrapper is **scrapped** → **"Wacky Races,
  Taiwan-food edition"** (over-the-top, battle-hungry rival agents), title **Travel Agents: Taiwan Food
  Tour** applied everywhere (docs, rulebook, `make.sh`, art briefs). Felt identity, voice, names, rulebook,
  and all 8 art briefs re-founded + de-spied; 12 spy-era design notes archived to `archive/design-history/`.
  **Mechanics unchanged** — presentation/prose only.

## Pipeline stage
**Prototype-ready.** Design + development are CLOSED for V7-M at a clean, sim-validated state (N=400). The
prototype kit is current in `exports/`. The next real work is a **human playtest** (CD testing mainly at
**3–4 players**) — that table is the next arbiter, not more sim.

## Done · In-flight · Next
- **✅ Done (this version):**
  - **Systems design** — area-majority follower-meeple fight, vendor-depletion Day→Night clock + Closing-Time
    die, two-track VP, agnostic tours + Pot-Luck, the 6-type mono ingredient taxonomy, the six V7-M character
    kits. Spine LOCKED.
  - **Sim validation (N=400)** — balanced at every count (vendor-only hoarder deeply sub-fair, tours dominate,
    battles scale); mono 6-type taxonomy shipped, the 8-type split **PARKED** behind flag `SPLIT_TAXONOMY`
    (default OFF).
  - **Prototype kit** — Screentop deck sheets, player/character boards with embedded AI mock-up portraits,
    A4/A3 print-and-play, map — all current in `exports/`.
  - **Rulebook** — fully current: de-spied to the Wacky-Races voice ("The Job" intro), scoring reconciled to
    **two-track VP + flat −1**, the **`min_followers` crowd-floor** now taught, trimmed back under the
    complexity budget (2277/2280), title A. `exports/rulebook.{html,pdf}` + `cover.png` regenerated.
  - **Voice bible** — `prose-identity.md` authored and promoted to a studio standard.
  - **Art prep** — art prompts + `art/ta-art-context.zip` (2.7 MB) ready for the CD's ChatGPT art generation.
  - **Events + tours currency/variety pass (2026-08-11)** — event deck de-monotonised (the "keep 1 fewer"
    pinch pile 10→6, the rest converted to spoil/sink/block/restock; weather now 5 distinct verbs; the triple
    "Sold Out" split into 3 cards; gifts split by scope), the "Fully Booked 客滿" logic bug fixed →
    **Sharing Tables 併桌**, funnier on-voice titles; tour flavour punched up + one hanzi fix. Counts held
    flat (map.json / pacing stable, no new keywords); **bg-critic: ship-to-table, no blockers, warmth rail
    holds**; guardians green; market + booking deck sheets regenerated.
- **⏳ In-flight:** none — the theme-currency sweep **and** the events/tours pass are complete and merged;
  no studio work is blocking.
- **➡️ Next (recommended): a 3–4-player human table** — bg-critic's steer, since the open event questions
  are *felt* (does forced-placement read as a tax to those behind? is the SINK card a shrug? the warmer
  hazard:boon ratio) and the sim can't answer them. The CD also generates the remaining art (map + vendor
  cards) from `art/ta-art-context.zip`.
- **⏸ Sim re-run — CD-GATED, with two hard watches when it runs** (owner: `bg-playtest` / `bg-playstrat`):
  (1) **teach the encoder** The Long Queue (EV-D05)'s new `rally 1` rider first, or the balance read is
  wrong; (2) **instrument the clock** — the `wash` card **New Management (EV-N29)** closes a vendor
  *without a claim* and pulls a refill, so confirm it doesn't **drain the vendor deck too fast and end the
  day early** (CD flag, 2026-08-11): measure game length + vendors-closed-without-claim vs the N=400
  baseline. Changing event effects invalidated N=400 — a re-sim is required before any new balance claim.
- **⏭ Deferred design follow-ups (surfaced by the sweep — not blocking; a later design pass):** migrate
  `design-doc.md` §15/§17 (event framework + clock) into `game-bible.md`, then archive it + fix its stale
  header (→ `bg-design`); reconcile `art/rulebook-figures.md`'s stale 2p / Buzz / Reach mechanics to V7-M
  (→ `bg-continuity` / `bg-infodesign`); the portrait-slot size mismatch (604×286 vs 900×1380 →
  `bg-infodesign`); the board clock-band vs deck-driven vs Closing-Time-die description mismatch
  (→ `bg-architect`); and the pre-existing data flags (`Draw`/人氣, EV-D07 pork name, Indigenous
  romanisation → `bg-design` / `bg-developer` / consultant).

## Open decisions (waiting on the Creative Director)
*Nothing blocking.* All V7-M design decisions are made and logged (mono ship config, orphan-tour ceiling,
cap-raises, the Big Boss rename). The only thing awaiting the CD is **doing** the next step (art + table),
not a decision.

## Guardrail health
| Gauge | State |
|---|---|
| Lint (`check_game.py --theme night-market`) | ✅ **0 errors / 12 warnings** (warnings are the baseline "missing recommended column value/quantity" advisories — expected) |
| Complexity (`check_complexity.py`) | ✅ **in budget** — rulebook_words **2277 / 2280** (trimmed by bg-elegance after the two-track + crowd-floor teaching landed); keywords 9/15; component types 8/8 (mono ship config) |
| Accessibility (`check_access.py`) | ✅ **pass** on the shipping mono config; MARGINAL flag exists **only** on the PARKED 8-type split (Rice/Noodles share the indigo hue) — not in play |
| Cost (`check_cost.py`) | **n/a** — Screentop-first prototype; physical COGS deferred until a physical run |
| Simulation | ✅ **last read balanced** (N=400): hoarder sub-fair all counts, tours dominate, contested_frac ~24–27% at multiplayer, paced (die L2@3–5p / L3@6p) |

## Risks · watch-items
- ⚠️ **The human playtest is the real arbiter — sim ≠ table.** The make-or-break question (is the
  area-majority fight *fun/tense*, not degenerate?) and whether the six kits band with no crusher are
  *unmeasurable* in sim. 3–4p is the focus; 5–6p downtime is the high-count watch.
- ⚠️ **Two consultant-gated content items — must clear a paid Taiwanese cultural + language consultant
  before any physical/public release:** (1) the character **The Big Boss (老大)** affectionate-fixer framing
  (warm, never a triad/gang caricature), and (2) the **2 Indigenous East-region dishes** (E01 竹筒飯,
  E04 石板烤肉). Screentop playtesting can proceed; art/print cannot without sign-off.
- ✅ **Drift watch — RESOLVED (2026-08-11 sweep).** The two-track scoring / flat −1 reconcile
  (`rules-draft.md` §1/§9, `components/manifest.md`), the `min_followers` crowd-floor teaching
  (`rules-draft.md` §5), and the character-kit reconcile (`names.md` / `v7-plan.md` → `characters.csv`) all
  landed and are guardian-verified. Remaining doc-consistency items are the non-blocking **deferred design
  follow-ups** listed under *Next* above.

## Next real step
**The Creative Director's call:** generate the remaining art (map + vendor cards) in ChatGPT from
`art/ta-art-context.zip` + the art prompts, then run a **3–4-player human playtest** to answer RISK #1 (is
the fight fun?) and RISK #2 (do the six kits band, is the Old Councillor rework balanced?). No studio work is
blocking it.
