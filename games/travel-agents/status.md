# 📋 Travel Agents: Taiwan Food Tour — Status (current state of play)

> **The live dashboard.** Owned by `bg-producer`. Always reflects the CURRENT version — readable in under a
> minute. If you want the *why* behind a decision, see `decision-log.md`; the *history* lives in `archive/`;
> the CD's own steers live in `director-brief.md`. This doc answers only: **where are we right now?**
> _Last updated: 2026-08-10 · by bg-producer_

## Version
- **Current:** `V7-M` — *the 3–6-player Taiwan street-food area-majority race: pile follower meeples on
  vendors to win the biggest crowd, race a vendor-depletion clock (+ a Closing-Time die) through one eating
  day, and score on two tracks — completed tours + won vendors.*
- **Shipped / frozen builds:** V7-M merged to `main` in **PR #13** (2026-08-10). No `builds/build-N/`
  snapshot cut yet — the merge + `exports/` are the known-good state.
- **Theme (2026-08-10 pivot):** the secret-agent wrapper is **scrapped** → **"Wacky Races, Taiwan-food
  edition"** (over-the-top, battle-hungry rival agents); retitled **Travel Agents: Taiwan Food Tour**.
  Felt identity + voice re-founded (`identity.md`, `prose-identity.md`, `game-bible.md` framing, `names.md`).
  **Mechanics unchanged.** *Living docs + the rulebook world-intro are now re-voiced (2026-08-10); the retitle is only half-applied and art is still to come — see In-flight.*

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
  - **Rulebook** — "Meet the Agents" gallery + character portraits + stylish `--rich` layout. The
    front-of-book world intro is **re-voiced to the Wacky-Races premise** ("The Job", 2026-08-10); the
    backstories were already on-premise. `exports/rulebook.{html,pdf}` regenerated.
  - **Voice bible** — `prose-identity.md` authored and promoted to a studio standard.
  - **Art prep** — art prompts + `art/ta-art-context.zip` (2.7 MB) ready for the CD's ChatGPT art generation.
- **⏳ In-flight (theme-pivot follow-through, 2026-08-10):** the re-founded docs **and the rulebook world
  intro** are done (`identity.md`, `game-bible.md` framing, `prose-identity.md`, `names.md`,
  `rules-draft.md` intro, regenerated `exports/rulebook.{html,pdf}`, logs). **Remaining:** (1) **retitle
  decision — CD's call:** the pivot renamed the living docs to *Travel Agents: Taiwan Food Tour*, but
  `make.sh` + `rules-draft.md`'s H1 still read *Travel Agents: Taiwan* — pick one and align both. (2)
  Propagate the new frame into `art/` + `marketing/` (the art is the CD's ChatGPT pass). (3) Reconcile the
  character-kit drift in `names.md`/`v7-plan.md` to `characters.csv`. (4) Old `design/` exploration notes
  still hold the retired spy voice — **archive** (history), don't rewrite.
- **➡️ Next:** CD generates the remaining art (map + vendor cards) in ChatGPT from the prepared
  zip/prompts, then runs a **3–4-player human playtest**.

## Open decisions (waiting on the Creative Director)
*Nothing blocking.* All V7-M design decisions are made and logged (mono ship config, orphan-tour ceiling,
cap-raises, the Big Boss rename). The only thing awaiting the CD is **doing** the next step (art + table),
not a decision.

## Guardrail health
| Gauge | State |
|---|---|
| Lint (`check_game.py --theme night-market`) | ✅ **0 errors / 12 warnings** (warnings are the baseline "missing recommended column value/quantity" advisories — expected) |
| Complexity (`check_complexity.py`) | ✅ **in budget** — rules-only 2262 / cap **2280**; keywords 9/15; component types 8/8 (mono ship config) |
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
- ⚠️ **Drift watch (open currency reconciles):**
  - **Two-track scoring / flat −1 / the clock:** authority is `game-bible.md` + sim N=400 +
    `components/vendors.csv` (two-track VP · flat −1 cancel · vendor-depletion + Closing-Time-die clock).
    **`names.md` is now reconciled to this (2026-08-10).** Still lagging: **`design/rules-draft.md` §1/§9**
    (reads tickets-only / deck-driven clock) — the rules-teach reconcile → **bg-rulebook** / **bg-design**.
  - **`min_followers` crowd-floor:** in the component data but **untaught in `rules-draft.md` §5** (which
    teaches only biggest-crowd plurality). → **bg-design** / **bg-rulebook**.
  - **Character kits:** `components/characters.csv` is canon for the six V7-M kits, but **`names.md` §1/§3
    and `v7-plan.md` still describe pre-V7-M shapes** (Old Councillor / Big Eater / Influencer / Globetrotter);
    `bg-continuity` flagged them in `names.md` §5, not yet reconciled. → **bg-continuity**.

## Next real step
**The Creative Director's call:** generate the remaining art (map + vendor cards) in ChatGPT from
`art/ta-art-context.zip` + the art prompts, then run a **3–4-player human playtest** to answer RISK #1 (is
the fight fun?) and RISK #2 (do the six kits band, is the Old Councillor rework balanced?). No studio work is
blocking it.
