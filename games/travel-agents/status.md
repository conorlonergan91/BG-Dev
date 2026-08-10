# 📋 Travel Agents: Taiwan — Status (current state of play)

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
  - **Rulebook** — "Meet the Agents" gallery + world intro ("Operation Beef Noodle") + character portraits +
    stylish `--rich` layout.
  - **Voice bible** — `prose-identity.md` authored and promoted to a studio standard.
  - **Art prep** — art prompts + `art/ta-art-context.zip` (2.7 MB) ready for the CD's ChatGPT art generation.
- **⏳ In-flight:** none — V7-M development is being closed for now.
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
- ⚠️ **Duplication / drift watch (from the Archivist's currency flags → routed, NOT fixed here):** the same
  truths live in two places and one copy is stale —
  - **Two-track scoring:** current everywhere that matters (CD brief + sim N=400 + `components/vendors.csv`
    `vp` column + `game-bible.md` §14), **but `design/rules-draft.md` §1/§9 and `names.md` §3 still read
    "tickets-only / vendors never score," and `names.md` §3 says cancel = −½ value** where the live rule is
    **flat −1**. → routed to **bg-continuity** + **bg-rulebook** (prose), **bg-design** (says which is right —
    it's two-track / flat −1).
  - **`min_followers` crowd-floor:** in the component data but **untaught in `rules-draft.md` §5** (which
    teaches only biggest-crowd plurality). → **bg-design** / **bg-rulebook**.
  - **Character kits:** `components/characters.csv` is canon for the six V7-M kits, but **`names.md` §1 and
    `v7-plan.md` still describe the pre-V7-M shapes** (Old Councillor / Big Eater / Influencer / Big Boss).
    → **bg-continuity**.

## Next real step
**The Creative Director's call:** generate the remaining art (map + vendor cards) in ChatGPT from
`art/ta-art-context.zip` + the art prompts, then run a **3–4-player human playtest** to answer RISK #1 (is
the fight fun?) and RISK #2 (do the six kits band, is the Old Councillor rework balanced?). No studio work is
blocking it.
