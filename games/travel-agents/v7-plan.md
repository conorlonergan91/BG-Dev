# Travel Agents: Taiwan — V7 Work Plan (the multiplayer re-home)

**This is the authoritative job checklist for the V7 arc.** Work top to bottom, tick each box as you
finish it, and **commit + push after each meaningful item** so progress is never stranded. Do NOT skip
the sign-off gate (Phase 3). Full rationale for every decision below lives in `decision-log.md` (newest at
top) — this file is the *do-list*; the log is the *why*.

**★ The pivot:** Travel Agents is no longer a 2-player duel. **Design home = MULTIPLAYER 3–6** (tune 3–5
solid, 6 as a validated stretch). 2p is dropped as a design target.

---

## Decisions carried in — LOCKED, do NOT re-litigate (re-scope them for N players)

These are signed off by the CD. Re-validate/re-scale them for multiplayer; do not reopen the decision.

- **Scoring = tickets-only:** Σ Complete-pile Booking value − Σ floor(v/2) Cancelled-pile. No other scoring vector.
- **Bookings** (renamed from missions/tickets): **hand-limit N=3**, **cancel-to-claim**, **shared Day/Night slots**; 3 card-scale slots along the board top.
- **Followers** (renamed Buzz) + **Followers-max = a growing DIAL** (renamed Reach). **Promote places 2 Followers**, total committed across all vendors **≤ your dial**.
- **Influencer (網紅):** Followers-max **starts at 4** (Promote-3 dropped; goes-last flaw kept).
- **Base Travel = move + +1 Follower-max only, NO ingredient.** **Homebody (媽寶) = the SOLE Travel-sourcer** (draws the region LEFT; event on that draw whiffs).
- **Trending** (renamed ★ star *token*): dynamic, event-dropped ("Gone Viral"); **winning a Trending-marked vendor → +1 Follower-max**. The *printed* ★ Michelin/Bib-Gourmand **apex** vendors are a SEPARATE permanent thing (top Draw) — naming TBD (Phase 2, bg-theme).
- **Rave Reviews = per-player boons kept** (at the 2nd & 4th completed tour); **Tours-Completed stays per-player on the character board** (no VP race, no map track).
- **Lost promotion-war must STING the dial** (burn the loser's committed Followers and/or drop their Followers-max) — a first-class economy lever; at multiplayer this is the NORM, not an edge case.
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
