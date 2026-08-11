# Travel Agents: Taiwan Food Tour — V7 Work Plan (the multiplayer re-home)

**This is the authoritative job checklist for the V7 arc.** Work top to bottom, tick each box as you
finish it, and **commit + push after each meaningful item** so progress is never stranded. Do NOT skip
the sign-off gate (Phase 3). Full rationale for every decision below lives in `decision-log.md` (newest at
top) — this file is the *do-list*; the log is the *why*.

**★ The pivot:** Travel Agents is no longer a 2-player duel. **Design home = MULTIPLAYER 3–6** (tune 3–5
solid, 6 as a validated stretch). 2p is dropped as a design target.

**★ CD DELEGATION (2026-08-09):** once the Granny confirm re-sim lands, **drive this plan autonomously as
far as it goes** — close V7 balance → Phase-2 lock + guardian sweep + the naming-bless → the Phase-4
component rebuild (character boards, the neutral N-player map, ingredients-as-pictorial-cards, the stripped
player aid, the icon-first / language-agnostic RA-clarity icon system with SVG placeholders + human
art-prompts). **Auto-accept sensible design recommendations** instead of pausing for each; keep committing +
pushing after every meaningful step; surface to the CD only a genuine blocker or a choice only they can make.

---

## Character roster — ALWAYS refer to these by the ENGLISH name (in chat + docs)

Never use the 繁體/Tâi-lô name alone — the human can't follow it. English first; original in parentheses only if precision needs it.

> **Canonical name/term table now lives in `games/travel-agents/names.md`** (`bg-continuity`, 2026-08-09).
> The roster below is kept current for convenience; `names.md` + `components/characters.csv` are the
> authority if they ever disagree.

| English name (USE THIS) | 繁體 (Tâi-lô) | Kit (V7-M — `characters.csv` is canon) |
|---|---|---|
| **The Old Councillor** | 里長伯 (Lí-tiúⁿ-peh) | *Old Favours* — name one home region; while home, start each turn drawing **1** ingredient from any market (no action); away, the engine is dark. Flaw-free. |
| **The Homebody** | 媽寶 (Ma-pó) | Sole Travel-sourcer — on a Travel, draw the top **2** of the region you LEFT and keep both (event whiffs). Flaw-free. |
| **The Big Eater** | 大胃王 (Tuā-uī-ông) | Keep all 3 on a Visit + a Greedy-Grab 4th (→ return 1 follower to supply); hazards fire twice on **her** Visit. |
| **The Influencer** | 網紅 (Bāng-âng) | Owns **8** follower meeples (the field owns 6) — a deeper pool; dial starts at **2** like everyone; goes last in turn order. |
| **The Big Boss** | 老大 (Lāu-tuā) | Margin dial N=1 — wins a contested stall unless a rival exceeds his committed followers by N or more (**wins ties**). Flaw-free. |
| **The Globetrotter** | 阿嬤 (A-má) | Reaches any region in one Travel + Scheduled-Maintenance-immune; each Travel-anywhere costs **1** follower to supply. Flaw-free. |

---

## Decisions carried in — LOCKED, do NOT re-litigate (re-scope them for N players)

> **Historical record (V7-arc, mostly executed).** The in-flight decisions below are a point-in-time
> record of the V7 arc and some were superseded during V7-M — e.g. **scoring is now two-track VP + flat −1
> cancel, not "tickets-only"**, and **the Influencer's edge is a deep pool of 8, not a dial that "starts at
> 4."** The current game is `game-bible.md` (V7-M); the current names/terms are `names.md` (see its §4
> retired table). Read this section as arc history, not current spec.

These are signed off by the CD. Re-validate/re-scale them for multiplayer; do not reopen the decision.

- **Scoring = tickets-only:** Σ Complete-pile Booking value − Σ floor(v/2) Cancelled-pile. No other scoring vector.
- **Bookings** (renamed from missions/tickets): **hand-limit N=3**, **cancel-to-claim**, **shared Day/Night slots**; 3 card-scale slots along the board top.
- **Followers** (renamed Buzz) + **Followers-max = a growing DIAL** (renamed Reach). **Promote places 2 Followers**, total committed across all vendors **≤ your dial**.
- **Influencer (網紅):** Followers-max **starts at 4** (Promote-3 dropped; goes-last flaw kept).
- **Base Travel = move + +1 Follower-max only, NO ingredient.** **Homebody (媽寶) = the SOLE Travel-sourcer** (draws the region LEFT; event on that draw whiffs).
- **Trending** (renamed ★ star *token*): dynamic, event-dropped ("Gone Viral"); **winning a Trending-marked vendor → +1 Follower-max**. The *printed* ★ Michelin/Bib-Gourmand **apex** vendors are a SEPARATE permanent thing (top Draw) — naming TBD (Phase 2, bg-theme).
- **Rave Reviews = per-player boons kept** (at the 2nd & 4th completed tour); **Tours-Completed stays per-player on the character board** (no VP race, no map track).
- **Lost promotion-war = the Followers-max DIAL DROPS** — down **1 notch by day, 2 at night** (CD, post Phase-1; replaces the weak "burn"). The contention-scaled economy sink; at multiplayer this is the NORM. (Floor + committed-over-max interaction: bg-design specs in Phase 1.5.)
- **Pacing scales with player count** (CD, post Phase-1): day + night decks grow/shrink with N; **deck exhaustion drives the clock** — day-deck-out → dusk, night-deck-out → last train — with a possible different "shift gears" night trigger; the clock track also scales per count. (bg-design specs in Phase 1.5; this is the 6p fix.)
- **Ingredients are CARDS** in the regional market decks — **retire the ingredient tokens** (pork/tea/seafood/rice/sugar); food/ingredient cards become **pictorial** (language-agnostic).
- **Map:** **phase-split** day/night card slots (day-only slots on the day side, night-only on the night side; unused cards → box); **drop the Ingredient-Supply section**; **remove the across-the-table orientation** (one neutral shared board; region diamond + single central clock + realistic scaling stay).
- **Component direction:** **icon-first, language-agnostic** (no on-component CJK), **RA-clarity**; SVG icon placeholders + art-prompts; character boards = **icon-only** abilities/flaws (rulebook carries the words), the **Followers dial** (reach-track retired), **card-shaped Complete/Cancelled** zones, **booking slots**; player aid stripped to **"On your turn" only**.
- **Naming:** missions→**Bookings**, Buzz→**Followers**, Reach→**Followers-max**; keep **Promote / Complete 成團 / Cancelled 取消**; **Trending**. (Bookings 繁體 bless still owed — Phase 2, bg-theme.)

---

## PHASE 0 — bg-architect RE-HOME to multiplayer (with bg-design on concrete rules)

Output: a new `design/v7-content-draft.md` (the v6.3-content-draft stays as history).

- [x] Set the **design-home count** (recommend **4**) and describe how **3 / 4 / 5** differ in feel; treat **6** as a validated stretch.
- [x] **Re-architect the contested-vendor core** from 1v1 duel → **multiplayer AREA-MAJORITY**: how 3–6 players pile Followers on a vendor, who wins (highest committed; define ties), and how it resolves.
- [x] Resolve the **lost-promotion-war** consequence as part of that core (losers' committed Followers **burned** = contention-scaled sink, and/or a **dial drop**) — now the norm.
- [x] **Re-scope scaling per count:** vendor slots per region, market + ticket supply, ticket draw, the **vendor-claims clock** (dusk / last-train per count), turn order / first-player.
- [x] Propose a **DOWNTIME mitigation** (the key 5–6p risk): simultaneous action selection, snappy turns, etc.
- [x] Fold the **carried-in v6.4 rules** (above) into the spec, re-scoped for N players.
- [x] Note the **hand-offs** (do NOT build yet): MAP = remove the across-the-table orientation only (light `regionmap` edit); THEME = re-frame "two rival agents" → a crowded market of agencies (bg-theme).
- [x] Define the **SIM scope**: which counts to run, and the probes Phase 1 must report.
- [x] Commit + push. Gut-check the CD **only** if a load-bearing fork appears; otherwise proceed.

## PHASE 1 — the CD-GATED multi-count re-sim  *(kicking off this plan IS the go)*

- [ ] **Encode** the multiplayer core + the carried-in v6.4 changes into `sim/travel_agents.py` (hand-limit N=3; Influencer Followers-max start 4, Promote 2; base Travel = move + Follower only, de-sourced, `_bump_src` fixed; Homebody sole Travel-sourcer; Trending +1 Follower-max on win; the lost-war sink lever).
- [ ] **Run across 3–6** (focus 3–5).
- [ ] Report per count: **character band** (no crusher; Homebody off its ~43% floor; Influencer ≥45/≤~55), **seat/turn-order fairness**, a **downtime proxy** (legal actions / decision load), **game length vs the clock**.
- [ ] **Multiplayer contested-vendor health:** how often vendors are genuinely contested now; whether the **lost-war Follower sink** lands the economy tense in the back half **without** starving/swinging. (This replaces the 2p economy sweep — contention now comes for free. Test the lost-war-burn / dial-drop lever + levers b [raise night/apex demand + ceiling] / c [more sink events], and **recommend the mix**. Do NOT force the fight rate as the primary knob.)
- [ ] Confirm **night sourcing** still healthy with base Travel de-sourced (flag, don't change, the CD-4 curve if it drops); **tickets-only health** holds (`ignore_obj` stays dead); **kingmaking / leader-pump** check at 5–6.
- [ ] Commit + push the sim module + refreshed `sim-results.md` / `sim-notes.md`.

## PHASE 1.5 — 6p PACING FIX + dial-drop sink (CD direction, post Phase-1)  *(fix 6p, don't cap)*

Phase-1 verdict: 3–5p healthy, **6p broken** (0% last-train / 71% stall — a scaling failure). Fix it via a pacing-model change + a real lost-war sink, then re-sim. bg-design (architect hat) specs into `design/v7-content-draft.md`; **gated re-sim only after the CD confirms the spec.**

- [ ] **Decks scale with player count** — set day + night market/booking deck sizes per count (3/4/5/6) so pacing self-adjusts and 6p stops exhausting supply.
- [ ] **Deck-exhaustion clock** — day-deck-out → **dusk** (flip to night); night-deck-out → **last train** (end). Propose the night "shift gears" trigger if it differs from a symmetric day-style deck-out.
- [ ] **Reconcile** the deck-clock with the existing vendor-claims clock (replace it, or keep a per-count-scaled claims-clock as a secondary end) — pick the cleanest single model; scale the clock track per count.
- [ ] **Lost-war dial-drop sink** — lose a promotion war → Followers-max dial down **1 (day) / 2 (night)**. Spec the **floor** (below start? at 1? at 0?) and the **committed-over-max** interaction (return Followers to supply, player's choice, until within cap).
- [ ] Flag the load-bearing **sub-forks** for a CD quick-confirm (deck sizes, night "shift gears", clock reconciliation, dial-drop floor); commit + push the spec.
- [ ] **Gated re-sim across 3–6** (CD go required): must show **6p now COMPLETES** (last-train, not stall), the **economy TIGHTENS** (slack_night down), and the **character band + tickets-only + seat fairness hold**. Re-read 阿嬤 (floor) + 網紅/老大 (6p-hot) post-fix. Commit results.

## PHASE 2 — design review + lock (bg-design + guardian sweep)

- [ ] **Lock the sim-resolved numbers:** the multiplayer majority rules + the lost-war sink, per-count scaling, the character/economy reads (confirm Influencer start-max 4 or a reserve dial).
- [ ] Fold in the pending **representation changes:** Trending; ingredients-as-cards (retire ingredient tokens; pictorial food cards); phase-split day/night map slots; Ingredient-Supply removed.
- [ ] **Guardian sweep — bg-theme:** the crowded-market re-frame + Followers/Promote/Trending/Bookings naming coherence + the printed **★ Michelin apex** naming call + the owed **Bookings 繁體** bless.
- [ ] **Guardian sweep — bg-critic:** multiplayer politics, kingmaking, downtime, take-that.
- [ ] **Guardian sweep — bg-elegance:** keyword count ≤ budget, rulebook word count ≤ cap.
- [ ] Update `game-bible.md` + `decision-log.md`; commit + push.
- [ ] Present the **FINAL locked V7 spec**.

## PHASE 3 — ⛔ STOP for CD sign-off

- [ ] Present the sim verdict + the locked V7 spec to the CD and **WAIT** — do not start the rebuild until the CD signs off.

## PHASE 4 — component rebuild  *(only after Phase 3 sign-off)*

Icon-first, language-agnostic. Data is the source; regenerate via `make.sh`; keep **lint + access at 0 errors**; **Beacon untouched**.

- [ ] **Icon system:** RA-clarity vocabulary; SVG placeholders + per-icon art-prompts (correct dimensions) into `art/`.
- [ ] **Character boards:** icon-only abilities/flaws (rulebook carries the words); the Followers **dial**; card-shaped **Complete/Cancelled** zones; **booking slots**; per-player Tours-Completed.
- [ ] **Map:** the neutral shared N-player board (across-the-table orientation removed); phase-split day/night slots; Ingredient-Supply removed.
- [ ] **Ingredient / food cards:** pictorial, in the market decks (no ingredient tokens).
- [ ] **Player aid:** stripped to "On your turn" only; the rest lives in the rulebook.
- [ ] **Rulebook:** the character section explains the abilities/flaws the boards only icon.
- [ ] Regenerate `exports/` + `exports/screentop/`; commit + push.

---

## Standing constraints (every phase)

- Branch **`claude/board-game-design-agents-81gkkl`** only. Commit + push as you go.
- **Taiwan sensitivity rails are BINDING:** Traditional characters only (never Simplified), real dishes never mangled, secular events only, dignified local characters, anti-extraction framing. A **paid Taiwanese cultural + language consultant** is required before art/print (not discharged by any pass).
- The **sim is slow + CD-gated** — run it once the module is encoded (Phase 1); don't re-run casually.
- **No AI final art** — AI only for labelled/gitignored mockups; art briefs are for human illustrators.
- Beacon (the other game) must stay untouched by TA render/tooling edits.
