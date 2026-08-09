# Travel Agents: Taiwan — V7 → V7-M: Follower MEEPLES redesign (DESIGN PROPOSAL)

> **Status: PROPOSAL ONLY.** No data, rules, or code touched. No sim run (CD-gated). This spec is for
> the CD to sign off the new model before `bg-developer` executes the data and `bg-playtest` re-sims.
> Canon it will amend on approval: `design/rules-draft.md` §§3–5, `components/*.csv`, `map.json`.
>
> **The change (CD mandate, 2026-08-09):** replace the abstract **Followers-max DIAL** with physical,
> collectable, colour-coded **Follower MEEPLES**. The dial "didn't feel natural"; meeples make the
> area-majority fight legible and turn *losing* into a real tempo cost.
>
> **This reopens the economy the V7 sim CLOSED.** Said plainly: the taxonomy/pacing/character bands in
> `playtests/sim-results.md` were validated against the *dial*. This proposal changes the win-a-vendor
> economy (win now KEEPS your meeples; loss now sends them to supply to re-collect), so those bands are
> provisional until a fresh per-count 3–6 re-sim (scoped in §8) and the CD's flagged human 6p session.

---

## 0. Executive read (the model in a paragraph)

Every player owns a fixed pool of **Follower meeples in their own colour** — `max` of them, and that
count *is* the old Followers-max ceiling, now physical (no dial, no tracked number). At any instant each
meeple is in exactly one of three places: your character's **central supply** (uncollected), your
**player board** (collected, idle, ready to deploy), or **on a vendor** (committed, contesting). You
**COLLECT** meeples from your supply onto your board — chiefly on **Travel** (+1), the heir of the old
"+1 Followers-max" ramp; this is the **pace** lever. You **DEPLOY** (the old *Promote*) by placing up to
**2** meeples from your board onto vendor(s) you stand with — and you may **spread** them across several
co-located vendors, not all onto one. A vendor goes to whoever has the **most meeples on it** (pure
plurality; a tie blocks; the Big Brother 大哥 wins ties by matching — lever iii). **Win → your meeples
come home to your board** (kept, redeploy for free next round). **Lose a contested vendor → your meeples
on it go back to the central supply** (you must re-collect them) — this single rule *replaces the
day/night dial-drop penalty*. Nothing else about the game (regions, ingredients, bookings, the
deck-driven clock, tickets-only scoring) changes. The three CD-named balance levers are: **(i) `max`
per character**, **(ii) collection pace**, **(iii) the tie-break** — and only two characters carry a
meeple-native edge (Influencer = higher `max`; Big Brother = wins ties); the other four kits are
ingredient/mobility-side and untouched.

---

## 1. The full ruleset for the new mechanic

### 1.1 The supply model — `max` = **how many you OWN in total**, enforced physically

**`max` is the number of meeples that exist in your colour**, full stop. `(in supply) + (on board) + (on
vendors) = max`, always. There is **no separate "board hold limit"** and **no tracked ceiling number** —
the cap is the component count, so it needs zero bookkeeping. At setup you take exactly your character's
`max` meeples (printed on your board) in your colour; the rest of that colour stays in the box.

*Why own-total, not board-capacity:* it is the faithful, physical heir of the old **Followers-max
ceiling** ("your total committed can never pass your dial"). Board-capacity would let a player deploy an
unbounded number over the game (only limiting the buffer); own-total keeps the exact old invariant —
**you can never have more Followers working than your `max`** — while erasing the abstract number.

The three locations, and how meeples move between them:

| From → To | Trigger |
|---|---|
| **Supply → Board** (COLLECT) | Travel (+1); Trending win (+1); 2nd-tour Rave Review (+1); the "+1 Followers-max" events (+1) |
| **Board → Vendor** (DEPLOY) | Promote (place up to 2, may spread); certain events |
| **Vendor → Board** (WIN / keep) | you win the vendor it sits on; or the day layer clears it unclaimed at dusk |
| **Vendor → Supply** (LOSE / re-collect) | a *rival* wins a vendor you had meeples on; a bad-review event; Greedy Grab |

### 1.2 Setup

- Each player takes their character's `max` meeples in their colour, placing **`start` of them on their
  board** (baseline **2**; Influencer **2** — see §3) and the rest in their colour's **central supply**
  (a labelled tray/zone by the board — six small colour bins, or one shared tray sorted by colour).
- Everything else in setup is unchanged (§2 of the rules-draft): map, markets, vendor slots, DAY/NIGHT
  Booking decks with their boundary cards, characters, Larders.
- The board's per-count SETUP chart's "Followers supply" line becomes **"meeples per colour" = your
  character's `max`** (it is per-player, not a shared scaled pool — so the chart entry simplifies).

### 1.3 The turn (one action; unchanged list, two re-expressed)

- **VISIT / CONVENIENCE STORE / BOOK a tour** — unchanged.
- **TRAVEL** — move + reveal, then **COLLECT 1 meeple** from your supply to your board (was: raise dial
  +1). If your supply is empty you're at full pool; you still move.
- **PROMOTE (DEPLOY)** — place **up to 2** of your meeples **from your board** onto vendor(s) you stand
  with. You may split the 2 across two co-located face-up vendors (**spread**) or stack both on one. If
  your board holds fewer than 2, place what you have. **You cannot deploy meeples you have not
  collected** — an empty board means Promote does nothing, exactly as an under-raised dial once blocked
  further commitment. (This Travel→collect / Promote→deploy coupling is the faithful heir of the old
  Travel-raises-dial / Promote-commits coupling.)
- **BRIBE a vendor** — resolve the crowd (§1.4).

### 1.4 Win / lose resolution flow (colours visible, plurality)

To **Bribe** a vendor you stand with:

1. **Majority check** — you must have **strictly more of your meeples on it than any single other agent
   has** (an outright plurality). *A tie claims nothing* (see below). **Big Brother 大哥** needs only to
   **match** the highest present (lever iii).
2. **Pay ingredients** — its recipe minus your region-icon discounts (and the Councillor's home
   discount / away tax), exactly as today. (There is **no meeple threshold** — see §5.)
3. **Take the vendor** onto your tour; complete any held Booking it satisfies.
4. **Your meeples on it → your board** — kept, redeploy for free later. (Was: return to supply.)
5. **Each losing agent's meeples on that vendor → the central supply** — they must re-collect them.
   This is the **entire lost-war penalty** (replaces the −1/−2 dial-drop).
6. **Refill** the vendor slot.

- **A tie just blocks.** Level for the biggest crowd (and no Big Brother present to break it)? No one
  claims it; every agent's meeples **ride** (stay on the vendor). Promote again to take the lead, or
  walk away and leave them committed.
- **Uncontested** = you have majority with even a single meeple (1 > 0); you may claim if you can pay
  the ingredients. (Same as the old model; the ingredient cost is the real gate — see §5.)

### 1.5 Spread & re-commit across rounds

- **Spread** is placing your Promote's meeples on different co-located vendors. Spreading *across
  regions* still requires travelling — so the per-region face-up count (North 2, others 1–2 by player
  count) naturally bounds how thin you can spread. This continues the existing rule (old Promote already
  read "onto vendor(s)") — meeples just make it legible.
- **Re-commit:** meeples on an unresolved vendor stay put between your turns; you add to them with
  further Promotes. You never *move* a committed meeple sideways — it stays until the vendor is claimed
  (→ winner's board / losers' supply) or the layer clears at dusk.

### 1.6 Interaction with the DUSK / LAST TRAIN clock and the day→night flip

- **At 黃昏 DUSK** (day Booking deck exhausted): unclaimed day vendors are cleared as today. **Meeples
  sitting on those cleared, unclaimed vendors return to their owners' BOARDS** — the stall simply closed
  un-won; no contest was lost, so no one is sent to supply. (Kept, non-punishing; redeploy at night.)
- **At 末班車 LAST TRAIN** (game end): meeples score nothing and are irrelevant; leave them where they
  lie.
- The clock, decks, and boundary cards are entirely unchanged (meeples don't touch pacing).

---

## 2. Re-expressing everything the dial did — before → after

Nothing silently vanishes. Every dial function maps to a meeple function:

| # | Old (dial) | New (meeples) | Note |
|---|---|---|---|
| **(a)** | Base **Travel = +1 Followers-max** (raise the ceiling) | **Travel = COLLECT 1** meeple (supply→board) | 1:1. The ramp is now the physical accumulation of your pool. Ceiling-growth and collect merge into one act. |
| **(b)** | **Promote = place a fixed 2** Followers from supply onto vendor(s), capped by dial | **Promote = DEPLOY up to 2** meeples from your **board** onto co-located vendor(s); may spread | Same rate; the new precondition is that they must already be collected (board buffer). |
| **(c)** | **Influencer 網紅 start-dial 4** (+ floor-4 sink-immunity) | **Influencer `max` = 8** (owns 2 more than the field); start-on-board **2** like everyone | Re-expressed as the CD named: a higher cap. The deeper pool is the soft heir of floor-4 (losses sting proportionally less). Head-start deliberately dropped — see §3. |
| **(d)** | **Trending win → +1 Followers-max** | **Trending win → COLLECT 1** meeple | 1:1 (EV-N09 reword). |
| **(e)** | **Big Eater 大胃王 Greedy Grab → keep a 4th ingredient, dial −1** | Greedy Grab → keep the extra, **return 1 of your meeples (board or vendor, your choice) to supply**; if you have none out, you may not Greedy-Grab | Mirrors the −1 tempo cost as a re-collect cost. |
| **(f)** | **Lost-war dial-drop −1 day / −2 night** (floor = start) | **Lose a contested vendor → your meeples on it → supply** (re-collect) | The day/night severity is **dropped as an explicit rule** — night losses hurt more *emergently* (you commit more meeples at night, so more return to supply). Bad-review events (EV-N15/16) become "return 1 meeple to supply." Net elegance trim. |
| **(g1)** | **Rave Review, 2nd tour → +1 Followers-max** | 2nd tour → **COLLECT 1** meeple | 1:1. 4th-tour boon (ingredient + next Bribe −1) unchanged. |
| **(g2)** | Kits: **里長伯** home −1 / away +2 · **媽寶** Travel-draw-2 · **大胃王** keep-3 · **大哥** wins ties · **阿嬤** go-anywhere + Maintenance-immune | Ingredient- and mobility-side kits are **untouched** (never referenced the dial). Only Influencer (c) and Big Brother tie-break carry meeple-native edges. | 大哥's tie-win now reads "match the most meeples"; 阿嬤/媽寶/里長伯/大胃王 as today, plus (e) for the Big Eater's greed sink. |

**Watch surfaced by (g2):** Travel now *collects a meeple*, and the **Homebody 媽寶** is the
travel-heaviest kit (her whole engine) — she incidentally ramps her Follower pool faster than the field.
She already ran warm (idx 1.30→1.45 at 4–6p). Flagged in §7 and §8.

---

## 3. First-pass REBALANCE MODEL (the three CD levers)

**Field baseline:** `max` **6**, **start-on-board 2**, collection pace = **Travel +1** (plus Trending /
2nd-Rave / the three dial-gain events, each +1), tie-break = **tie blocks**.

*Why `max` 6:* the old ceiling ended ~7.5 (`reach_end`) but peak commitment was only ~3–4.5
(`max_committed`) and the cap rarely bound. Meeples are now **kept on wins** (more efficient than the old
"return to supply, re-Promote"), so an equal ceiling would loosen the fight. **6** is deliberately tighter
than the old effective ~7.5 — enough to spread 2+2+2 or stack 3+3 across a real fight, tight enough that
you cannot flood every vendor. `max` is the **#1 re-sim knob** (sweep 5 / 6 / 7).

*Why start-on-board 2:* the old start-dial 2 let you commit 2 on turn one; 2 pre-collected meeples give
the same immediate Deploy. Empty-board-can't-Promote ≈ old low-dial-can't-commit.

| Character | `max` (i) | start on board | collection pace (ii) | tie-break (iii) | meeple-native edge? |
|---|:--:|:--:|---|---|---|
| **Old Councillor 里長伯** | 6 | 2 | baseline | tie blocks | No — home-discount/away-tax is ingredient-side |
| **Homebody 媽寶** | 6 | 2 | baseline *(travels most → de-facto faster collect — **WATCH**)* | tie blocks | No — Travel-draw sourcer |
| **Big Eater 大胃王** | 6 | 2 | baseline; **Greedy Grab returns 1 meeple to supply** | tie blocks | No — the greed sink is the only touchpoint |
| **Influencer 網紅** | **8** | 2 | baseline | tie blocks | **Yes — higher `max`** (the start-4 edge, re-expressed) |
| **Big Brother 大哥** | 6 | 2 | baseline | **WINS ties (match the most)** | **Yes — the tie-break** |
| **Globetrotter 阿嬤** | 6 | 2 | baseline | tie blocks | No — go-anywhere/Maintenance-immune is mobility-side |

**Influencer reasoning (the one genuine judgement call):** the CD said re-express start-4 as a *higher
cap*. Her old edge was two-part — start-dial-4 (early tempo) **and** floor-4 (sink-immunity, which the
critic flagged as *possibly too strong*). I propose **`max` 8, start 2**: her edge becomes a **deeper
late-game pool** (she can keep 8 meeples working once collected; the field caps at 6), which is the soft
heir of floor-4 *without* the exception, and I **drop the early head-start** so she isn't double-buffed
onto an already top-of-band kit whose "goes last" flaw is secretly a perk on an open board. Net: she
becomes a coherent **late-game** character (goes-last + deep pool both bite late). Trim/buff levers held
in reserve: if COLD, add start 3–4; if HOT, `max` 7.

**What the re-sim should check:**
- Six-character band re-closes across 3–6p (esp. 4p and 6p stress), idx spread comparable to the closed
  0.20–0.26.
- **Influencer** (`max` 8) does not overshoot; **Big Brother** (match-under-spread, §7) does not
  overshoot; **Homebody** (Travel-collect compounding) does not overheat.
- **Runaway brake:** does *win-keeps-meeples* snowball the leader? (score margin, leader-change count,
  lost-war frequency vs the old 0.32→1.00/gm).
- **Contested frac** under spreading — does spread raise collisions (the goal) or scatter them below the
  old ~5%?
- Sourcing/pacing bands (§6/§6b) should be **stable** — meeple-independent — and serve as the anchor
  that the non-meeple economy is untouched.

---

## 4. Vendor cost translation — the crux

**Recommendation: pure MOST-MEEPLES-WINS, no fixed threshold. Retire `buzz_cost`.**

The V7 rules already resolve a vendor by **plurality** ("strictly more committed Followers than any
rival"), *not* by clearing a per-vendor number. Confirming this in the data: **`buzz_cost` = 2 for all
24 vendors and is referenced nowhere in `rules-draft.md`.** It is vestigial (a fossil of the pre-V7
"≥2-more-than-rival margin"). So the honest translation of "the closed economy" is: **the follower fight
is purely relative — out-commit your rivals — and a vendor's real cost is its INGREDIENTS
(`ingredient_cost`, unchanged).**

Keeping it pure-plurality:
- **preserves the exact economy the sim closed** (which never used a threshold);
- keeps the fight **legible at a glance** — count coloured meeples, no hidden number to clear;
- adds **no per-vendor number** for players to parse against their pool.

→ **Drop `buzz_cost`** alongside `draw` (§5). The meeple count needed to win is emergent (rival + 1;
Big Brother = rival).

*Considered and rejected:* a **minimum-N-to-claim threshold** (e.g. "≥2 meeples to win even
uncontested"). It would change the closed economy (uncontested vendors currently fall to a single
Follower) and add a number to track. Hold it **in reserve** only if the re-sim shows the 1-meeple
uncontested sweep (§7) is dominant — but the ingredient cost is expected to be the true throttle (you
cannot win vendors faster than you can source their recipes), so I do not recommend it up front.

---

## 5. Draw retirement + prestige-booking re-target

**Drop the `draw` column** from `vendors.csv` (and the DRAW references in the art docs, per the mandate).

`draw` (人氣 popularity) was a per-vendor prestige number that tracked tier/cost almost exactly (day
foods 1–2 & cost 1; night "both" 5–6 & cost 3; apex 6–8 & cost 4–5). The three prestige Bookings ask you
to **accumulate high-prestige (pricey, marquee) vendors** as a summed-value axis, distinct from the
count / coverage / pair Bookings.

**Recommended surviving metric: total `ingredient_cost` of your won vendors** — the tightest structural
heir (both rise with tier), a metric that *survives* on every vendor, and it reflavours cleanly from
"popularity 人氣" to **"the priciest, most-sought tables"** (expensive marquee dishes *are* the
prestigious ones). This keeps the three as the game's **"go tall on value"** axis.

| Booking | Old target | New target | Difficulty check |
|---|---|---|---|
| `d_prestige8` (day, val 4) | `draw_total_day >= 8` | **`ingredient_cost_day >= 4`** | day vendors are all cost 1, so ≈ 4 daytime vendors — faithful to draw≥8 (≈4–5 day stalls). Reflavour "the daytime spots worth queueing for." |
| `n_prestige14` (night, val 6) | `draw_total >= 14` | **`ingredient_cost_total >= 9`** | night draw ≈ cost+2/vendor, so draw14 ≈ ~3 marquees ≈ cost ~8–9 → **9** forces leaning into pricey night stalls. |
| `g_prestige12` (night, val 6) | `draw_total >= 12` | **`ingredient_cost_total >= 7`** | draw12 < draw14 → set 7 < 9, preserving the relative easier target (≈2 marquees). |

*Flavour note:* to hit ≥9 you effectively must include night marquees (there aren't enough day slots to
reach 9 on cost-1 stalls), so cheap-vendor-spam can't satisfy the tall targets — the "揮金如土 money no
object / marquee" flavour holds.

*Alternatives considered:* **vendor count** (too blunt — loses the prestige/tall flavour, collides with
the collection Bookings); **regions spanned** (a different axis, already the coverage Bookings);
**most-Followers-committed** (a live meeple-native idea, but transient and unscoreable at game end —
rejected). If the CD prefers maximum simplicity over flavour, **vendor-count** thresholds (day ≥4 / total
≥5 / total ≥4) are the fallback.

---

## 6. Self red-team (hand these to `bg-critic`)

Degenerate-play risks I am introducing by reopening a closed economy **and** adding spread + kept-on-win:

1. **★ Weakened runaway brake (biggest economy shift).** The old brake was "win → Followers to supply →
   you must re-Promote each time." Now **win keeps your meeples on your board → redeploy for free.** A
   serial winner cycles their whole pool at no re-cost while a loser keeps dumping to supply and
   re-collecting. This can **snowball the leader** — the exact brake the V7 close relied on (the fight
   being undiscounted and re-paid) is softened. *Top re-sim watch.*
2. **★ Tie-block deadlock-vacuum with visible colours.** Ties block (Big Brother aside). Open meeple
   counts make it cheap and deliberate to **match a rival to freeze a key vendor nobody can take** —
   spite/denial. At a Big-Brother table others can't freeze *him*, but everyone can freeze everyone
   else; end-game key vendors may never resolve.
3. **★ Big Brother match-to-win under spreading.** He needs only to *match*. With spread + open info he
   can drop **1 meeple onto many vendors** and win each tied-or-uncontested one — cheap omnipresent
   contesting that is stronger under spreading than in the old single-pile model. (He was already
   top-of-band.)
4. **1-meeple uncontested sweep.** No threshold + kept-on-win means winning uncontested vendors costs a
   single meeple each, redeployed free. Could trivialise vendor accumulation — throttled *only* by
   ingredient cost (the intended gate; confirm in sim).
5. **Last-committer / minimum-overcommit snipe.** Open counts + spread let the last player in a round
   place exactly rival+1 to steal a contested vendor for minimal meeples. The **Influencer's "goes last"
   flaw becomes a sniping perk** on the open board (prior critic flag, now sharper with meeples).
6. **Kingmaking-by-denial at 5–6p.** An out-of-contention player tie-blocks or out-commits to deny the
   leader a booking-critical vendor, choosing the winner. Colours make targeted denial legible and easy;
   the meeple-to-supply cost is small if they merely tie-block (1 meeple to match).
7. **Homebody collection-compounding** (from §2): Travel-collect rewards her travel-heavy engine twice.
8. **Idle-board-eats-cap feel-bad / spread scatters the fight below the old ~5% contested** — either
   direction is possible; sim + table only.

**Top 3 to feature:** #1 (weakened runaway brake), #2 (tie-block deadlock with visible colours), #3
(Big Brother match-under-spread) — plus #4/#5 as the sniping cluster.

---

## 7. Precise "what changes in DATA" list (for `bg-developer` LATER — do NOT execute now)

- **`characters.csv`**
  - Add columns **`max`** and **`start_meeples`**. Field: `max=6, start_meeples=2`. **Influencer 網紅:
    `max=8, start_meeples=2`.**
  - Recode `ability_code` **`start_max_4` → `max_8`** (or a generic `max`/`start` pair the render reads);
    rewrite the Influencer ability text: dial-starts-4 → **owns 8 meeples (field owns 6)**, drop the
    floor-4 wording.
  - **Big Eater 大胃王** effect: greed sink "dial −1" → **"return 1 of your meeples to supply."**
  - Scrub "Followers-max / dial" from every `ability`/`blurb`/`effect` string → "Follower meeples / your
    pool." No kit *values* change for 里長伯 / 媽寶 / 大胃王(ingredient) / 大哥 / 阿嬤.
- **`vendors.csv`** — **DROP `draw`**; **DROP `buzz_cost`** (both vestigial under the new model). Keep
  `ingredient_cost`, `icon`, `trending`, `recipe`, tier, phase, etc. unchanged.
- **`bookings.csv`** — retarget the 3 prestige rows (§5): `d_prestige8` → `ingredient_cost_day>=4`;
  `n_prestige14` → `ingredient_cost_total>=9`; `g_prestige12` → `ingredient_cost_total>=7`. Reword each
  `effect` from "Draw (人氣)" to the cost/marquee flavour; keep `value`, ids, art_note.
- **`tokens.csv`**
  - **Replace** the single grey `followers` row (qty 60, one colour) with **six per-colour Follower
    meeple entries** matching the pawn colours (pawnA–F): provide **8 per colour = 48 meeples** (so any
    colour can play the Influencer's `max` 8; other characters simply use 6).
  - **DROP the `dial` row** (no more dial).
  - Keep `trending`, `mkTours`, `hsrClosed`, `pileWin`, `pileLose`, pawns.
- **`events.csv`**
  - `EV-D09 / EV-N13 / EV-N14` (+1 Followers-max) → **collect 1 meeple (supply→board).**
  - `EV-N09` Gone Viral / Trending win → **collect 1 meeple.**
  - `EV-N15 / EV-N16` bad-review / mix-up (dial-drop) → **return 1 of your meeples (board or vendor) to
    supply** (keep the "crowd drifts to a rival" wording rail — binding).
  - `EV-N08` (place 2 Followers on co-located vendor) → **deploy 2 meeples from your board** (place what
    you have if short). `EV-N11` (next Promote places +1) → **your next Promote deploys +1 meeple (3).**
  - Scrub "Followers-max / dial" everywhere → meeple/pool wording.
- **`map.json`** — replace the shared scaled "Followers supply" with a **per-colour meeple supply zone**
  (six bins); the per-count SETUP chart line becomes "meeples per colour = your character's `max`";
  remove any dial-track element.

**Not data (separate passes, flag on hand-off):** `rules-draft.md` §§3–5 rewrite (dial → meeple pool;
collect/deploy; win-keeps/lose-to-supply; FAQ dial questions) is an **editorial pass** (`bg-elegance` /
`bg-rulebook`). The player-board **dial zone → collected-meeple pool zone** and the supply tray are
**`bg-infodesign`**. Neither touches values.

---

## 8. Scope of the re-sim I would want (NOT run — CD-gated)

This reopens the win-a-vendor economy, so re-run the standard V7 rig **per-count 3–6, N≥250/seating**,
plus meeple-specific probes:

- **Encode:** meeples as a per-player pool (supply/board/vendor); Travel = collect 1; Promote = deploy 2
  from board (spread allowed); win → board; lost-contest → supply; `max` 6 (Influencer 8), start 2; Big
  Brother match; Greedy-Grab & bad-review = return 1 to supply; Trending / 2nd-Rave / dial-events =
  collect 1. Retire `buzz_cost` / `draw` (plurality + cost-based prestige Bookings).
- **Anchor probes (must stay stable — meeple-independent):** sourcing-by-type vs demand (§6b),
  night:day ratio, Last-Train completion %, turns/player, tickets-only stays dead.
- **New / reopened probes:** six-character band 3–6p (Influencer/Big-Brother/Homebody watch);
  **contested_frac** under spread; **runaway** (leader margin, leader-change frequency, lost-war/gm);
  **1-meeple uncontested-sweep rate**; **`max` knob sweep 5/6/7**; deadlock/tie-block frequency proxy.

---

## 9. Decisions for the CD (A/B/C)

1. **Influencer's edge** — **(A, rec)** `max` 8 / start 2 (deeper late pool; no head-start double-buff) ·
   (B) `max` 8 / start 4 (pool + early tempo, faithful to both old halves but risks overshoot) · (C)
   `max` 7 / start 3 (split the difference).
2. **Vendor cost** — **(A, rec)** pure most-meeples-wins, drop `buzz_cost` · (B) keep a minimum-2
   threshold to claim.
3. **Prestige metric** — **(A, rec)** total `ingredient_cost` (keeps the tall/marquee flavour) · (B)
   vendor-count (simplest, blunter).

---

## 10. Handoff — trigger the coherence check

This is a mechanic swap: the **signature twist moved** — the contested Follower majority is now a
physical, colour-coded meeple fight; **winning keeps your meeples, losing sends them home to re-collect**
(replacing the dial-drop). Flag the Director to run **`bg-theme`** (does the fiction still explain "your
crowd comes home when you win, scatters when you lose"? the "dial" is gone from identity/lore) and
**`bg-elegance`** (net *trim* expected — deletes the dial keyword, the day/night drop asymmetry, and two
vestigial columns; adds the meeple lifecycle) on the change. Mechanics that moved: **Promote→Deploy,
Travel-ramp→collect, the lost-war penalty, Trending/Rave/Greedy sinks, and the win-return direction.**
