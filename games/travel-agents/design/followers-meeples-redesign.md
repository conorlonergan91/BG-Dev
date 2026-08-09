# Travel Agents: Taiwan — V7 → V7-M: Follower MEEPLES + VENDOR SCARCITY (SIGN-OFF-READY SPEC)

> **Status: SIGN-OFF-READY SPEC.** No data, rules, or code touched. No sim run (CD-gated). This folds the
> guardian sweep (bg-theme + bg-elegance + bg-critic, 2026-08-09) into a single locked model AND adds the
> new **vendor-scarcity** lever the CD called for. On the CD's "go" it amends `design/rules-draft.md`
> §§3–5, `components/*.csv`, and `map.json`, then `bg-playtest` re-sims.
>
> **Two coupled changes:**
> 1. **MEEPLES (CD mandate):** replace the abstract Followers-max DIAL with physical, collectable,
>    colour-coded **Follower meeples**. The dial "didn't feel natural"; meeples make the area-majority
>    fight legible and turn *losing* into a real tempo cost. (Guardians GREEN-LIT this — feel/elegance/
>    theme all improve. Locked parameters below.)
> 2. **SCARCITY (CD decision, this pass):** the V7 sim proved the contested crowd-fight — the signature
>    twist — fires in only **~5% of vendor claims** (`contested_frac` 3.3/5.3/4.6/4.9% at 3–6p). The CD
>    wants a **"race AND battle"** game, not a 5%-of-the-time sideshow. The critic located the lever:
>    **vendor scarcity** (a map/setup knob, NOT a meeple rule). §1 designs it.
>
> **This reopens the economy the V7 sim CLOSED.** The taxonomy/pacing/character bands in
> `playtests/sim-results.md` were validated against the *dial* at the *old* vendor availability. Both
> changes here move the win-a-vendor economy, so those bands are provisional until the fresh per-count
> 3–6 re-sim scoped in §9.

---

## 0. Executive read (the whole model in two paragraphs)

**Scarcity (the new work).** The reason the crowd-fight is rare is not the meeples and not the tie-rule —
it is that **claiming a stall instantly conjures a substitute.** With ~1.5–2.0 face-up stalls per agent
and *immediate* refill, a rival who wants "your" stall just takes the fresh one that pops up: opening a
contest is −EV, so nobody does. The fix is two coordinated knobs. **(A) Slow refill — the load-bearing
lever:** a claimed or cleared slot stays **empty** and all empty slots refill **once per round** (after
every player has taken a turn), not instantly. This turns every stall into a non-substitutable prize for
the rest of the round — walk away and you pay a whole Travel to reach a region that may itself be barren.
**(B) Tighter face-up counts — the amplifier:** cut slots to ~1.0–1.33 per agent, floor **1 per region**,
so most regions hold a single contestable stall and two co-located agents must fight or leave. Crucially,
**sourcing is untouched** — ingredients come from the region MARKET decks, not from vendors — so the §6b
sourcing shares should be invariant; the only economy risk is on the *sink/throughput* side (fewer/slower
stalls → fewer total claims → Bookings harder to finish). The design keeps that risk small (per-round
restock, not per-phase; floor 1/region) and the re-sim's dual make-or-break probe verifies it (§9).

**Meeples (locked).** Every player owns a fixed pool of Follower meeples in their colour — `max` of them,
the physical heir of the old ceiling (component count enforces it; zero tracking). A follower is always
in one of two named zones — your **supply** (un-rallied) or **your board** (rallied, ready) — or placed
**on a stall** (committing to a contest). **Travel** now also grows your following (take 1 follower from
supply to your board); **Promote** sends up to 2 followers from your board onto stall(s) you stand with
(may spread). A stall goes to whoever has the **most followers on it** (pure plurality; a tie blocks; the
Big Brother 大哥 wins ties by matching). **Win → your followers come home to your board** (kept, redeploy
free). **Lose a contested stall → your followers go back to YOUR OWN supply** to be re-rallied — this one
rule replaces the day/night dial-drop. Locked parameters: field `max` **6**, Influencer 網紅 **8** / start
**2** (no head-start), pace = Travel +1, tie-break = 大哥 matches; vendor cost = **pure most-meeples-wins,
no threshold, `buzz_cost` dropped**; prestige Bookings retargeted to total `ingredient_cost`.

---

## 1. THE VENDOR-SCARCITY LEVER (the new work)

### 1.1 Why the fight is rare — and why it is a refill problem, not a count problem

The map's own note claimed the old counts (~1.5–2.0 stalls/agent) "force collisions — the area-majority
engine." **The sim falsified that:** `contested_frac` sat at 3.3/5.3/4.6/4.9%. The mechanism is subtle and
worth stating precisely, because it decides which knob is load-bearing:

- The fight is **local** (per-region, per-phase, among co-located agents), not global. A table-wide ratio
  of 1.75 stalls/agent still leaves any given region with an open stall for each of the 1–2 agents standing
  in it → they each take one → no contest.
- **Immediate refill defeats a pure count-cut.** Even at 1 slot per region, if claiming triggers an instant
  refill, a co-located rival simply takes the fresh card. A count-cut only bites when there is **no instant
  substitute**. So the load-bearing lever is the **refill timing**, and the count is the amplifier.
- Contests today only happen on **non-fungible** stalls (a specific vendor that completes a held Booking,
  or an apex trophy) where a fresh refill is *not* a substitute. That is the ~5%. To lift it, we must make
  **ordinary** stalls non-substitutable too — for a while.

### 1.2 Lever A (primary, load-bearing): SLOW / per-round refill

> **Rule.** When a stall is claimed, or cleared unclaimed at DUSK, its slot stays **empty**. At the **end of
> each round** — after every player has taken one turn — refill all empty face-up slots from their region
> decks. Refill is **never immediate.**

- **Why it works:** within a round the board only thins. The next agent into a region cannot count on a
  fresh substitute appearing — the stall in front of them is, for now, the only one. Walking away costs a
  full **Travel** into a region that may itself be barren this round. That flips the −EV that kept contests
  rare: out-committing a rival (one **Promote**, +1 follower) becomes the competitive line.
- **Night-weighting for free:** more followers are committed at night (bigger night deck, higher-value
  stalls) → the thinned board bites harder at night → night carries the bulk of the fights *emergently*.
  So we **keep ONE slot table for day and night** (no separate night table) — preserving the map's existing
  one-table elegance (bg-elegance-friendly) while still concentrating the brawl at night.
- **Elegance honesty:** this is a net rule-*add* on the scarcity side (~2 lines: "slots stay empty; refill
  all at end of round"). It is partially offset by the meeple swap's net *trim* (deletes the dial, the
  day/night drop asymmetry, two vestigial columns). Flag to bg-elegance for the combined re-gauge (§10).

### 1.3 Lever B (amplifier, pure data): tighter face-up counts, floor 1/region

With slow refill in place, tightening counts turns "most regions hold a single stall" into a genuine
squeeze. Concrete per-count face-up slots (DAY = NIGHT, one table):

| Players | N | C | S | E | Total | Stalls/agent | Was (total) |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **3p** | 1 | 1 | 1 | 1 | **4** | 1.33 | 6 |
| **4p** | 2 | 1 | 1 | 1 | **5** | 1.25 | 7 |
| **5p** | 2 | 1 | 1 | 1 | **5** | 1.00 | 8 |
| **6p** | 2 | 2 | 1 | 1 | **6** | 1.00 | 9 |

**Reasoning per knob-position:**
- **Floor 1 per region** (never 0): every region must stay alive for sourcing geography and for Bookings
  that require that region — a 0-slot region would strand its Bookings. One slot + slow refill is the
  tightest a region can go and still function.
- **North keeps 2 at 4p+:** North (台北) is the start hub, everyone's turn-1 position, and carries the
  highest-demand ingredient (Meat 22%). A single North slot at high counts would lock the hub instantly
  and could starve the meat line; 2 gives the hub breathing room while still forcing a squeeze when 3+
  agents cluster there.
- **Central gets the 6p 2nd slot:** Central is the other 2-vendor-demand region (Tea + Sugar) and the
  natural place to absorb the 6th agent without over-thinning.
- **Held at 5 total for 5p and 6→6:** I deliberately do **not** scale slots linearly with players — the
  whole point is demand > supply, so slots grow slower than the player count (1.33 → 1.0 stalls/agent as
  the table fills). 6p at 1.0/agent is the sharpest squeeze and the CD's stress count.

`map.json` also carries a per-region `slots_n` (the 4p HOME default the render draws). Update it to the 4p
column: **N 2, C 1, S 1, E 1** (was N 2, C 2, S 2, E 1).

### 1.4 The exact `map.json` change

Replace the `vendor_slots` block (per hard constraint, this is the SPEC of the change — `bg-developer`
executes it after CD sign-off):

```json
"vendor_slots": {
    "_note": "face-up vendor slots per region (N/C/S/E); DAY = NIGHT (one table). V7-M SCARCITY (2026-08): counts tightened to ~1.0-1.33 stalls/agent AND refill is now SLOW (see `refill`). The V7 sim proved the old ~1.5-2.0/agent with IMMEDIATE refill left contested_frac at only 3-5%: claiming a stall instantly conjured a substitute, so opening a contest was -EV. Tighter counts + per-round (not instant) refill remove the cheap substitute and force the crowd-fight. `slots_n` on each region is the 4p HOME default for the render.",
    "refill": "SLOW / per-round: a claimed or cleared slot stays EMPTY; refill ALL empty slots from the region decks at the END of each round (after every player has taken one turn). NEVER immediate. This is the load-bearing scarcity lever - it makes each stall a non-substitutable prize for the rest of the round.",
    "3": {"N": 1, "C": 1, "S": 1, "E": 1},
    "4": {"N": 2, "C": 1, "S": 1, "E": 1},
    "5": {"N": 2, "C": 1, "S": 1, "E": 1},
    "6": {"N": 2, "C": 2, "S": 1, "E": 1}
},
```

And in `regions[]`: `north.slots_n` stays **2**, `central.slots_n` **2 → 1**, `south.slots_n` **2 → 1**,
`east.slots_n` stays **1**. The bottom-band setup table on the rendered board picks these up automatically.

### 1.5 The collision with the closed sourcing economy — what breaks, what holds

This is the crux the CD demanded. Reasoning from the sim's closed numbers:

**HOLDS — sourcing rate (gain).** Ingredients are drawn from the region **MARKET decks**, not from
vendors. Vendor scarcity does not touch the source at all. So the §6b sourcing-by-type shares (Meat
22–27%, Pantry 24–26%, Tea 12–15%, Seafood 14–16%, Sugar 11–13%, Veg 10–11% — all tracking demand) should
be **invariant**. This is the anchor: if a sourcing share moves materially in the re-sim, the encoding is
wrong, not the design.

**HOLDS (with a watch) — the ingredient SINK.** Fewer/slower stalls could reduce total claims (the sink),
but the sim shows `gain` ≫ `sink` (2–2.4×) and the binding constraint on claims was **one-action-per-turn
+ ingredient availability**, never the face-up slot *count*. Slow refill still refills (once per round),
so total throughput is only mildly reduced (the board is thinner on average, not starved). Expected effect:
a small dip in claims/gm, ingredients pile up a little more (supply_min rises, hand-limit `capbind` binds
slightly more often — mild wasted sourcing, not a break).

**THE REAL RISK — tie-block freezes throttling throughput.** Under scarcity, more contests → more
tie-blocks → more **frozen** slots (a tied slot does not refill until resolved). At single-slot regions a
frozen stall can barricade a whole region for a round or more, and a trailing kingmaker can perpetually
re-tie a leader's Booking-critical stall to freeze it *and* strand the leader's followers (the critic's
endgame-denial HOLE). Left unchecked this could drop Booking completion below the sim's 95–98% floor. **The
mitigation is the pre-specified DUSK / LAST-TRAIN tie-resolver** (§8 reserve b) — scarcity makes that
resolver load-bearing, not optional. It guarantees every frozen stall clears at each phase boundary.

**WATCH — the prestige Bookings.** The retargeted prestige Bookings (§6) need enough high-cost night-marquee
claims. Those marquees are exactly the stalls that will be fought hardest under scarcity. If apex fights
deadlock, prestige Bookings could become hard — the re-sim tracks prestige-Booking completion specifically.

**Net:** sourcing (source side) is structurally untouched and should read invariant; all risk is on the
sink/throughput side and is bounded by (a) per-round (not per-phase) restock, (b) floor 1/region, and (c)
the DUSK/LAST-TRAIN tie-resolver. The re-sim's job (§9) is to confirm **contested_frac goes UP for real**
while **Booking completion and claim throughput HOLD**.

### 1.6 Reserve amplifier (hold, do NOT bake): non-refilling apex marquees

If the re-sim shows the **marquee/apex** fights specifically are not materialising (top-apex contested
rate stays flat) even as overall contested_frac rises — or the CD wants the *famous-stall* drama sharpened
— add: **tier-3 apex stalls (N06 士林大香腸, C05 逢甲名物, S06 擔仔麵, E04 石板烤肉) do not refill at all
once claimed — gone for the game.** This makes the four trophies true one-shot prizes (a pure race-and-
battle) while leaving the tier-1 sink stalls fungible so throughput is unaffected. Held in reserve because
it is an extra rule and narrows the top-tier sink; trigger = flat apex-contest rate AND CD wants marquee
drama.

---

## 2. THE MEEPLE RULESET (locked — keyword discipline enforced)

**Keyword discipline (bg-elegance, BINDING).** The only action keywords are the existing **Travel** and
**Promote** — we do **not** mint COLLECT or DEPLOY. There are exactly **two zone-words**, *supply* and
*your board*; a committed follower is *on the stall* (a placed state, not a third named zone). Below,
"grow/take/send/place" are plain-language verbs, never capitalised keywords.

### 2.1 The pool model — `max` = how many you OWN, enforced physically

**`max` is the number of followers that exist in your colour.** `(in supply) + (on your board) + (on
stalls) = max`, always. There is no separate board-hold limit and no tracked ceiling — the cap *is* the
component count, so it needs zero bookkeeping. At setup you take exactly your character's `max` followers
in your colour; the rest of that colour stays in the box. This is the faithful physical heir of the old
Followers-max ceiling ("your total committed can never pass your dial") with the abstract number erased.

The two zones and the placed state, and how followers move:

| From → To | Trigger |
|---|---|
| **supply → your board** (grow) | **Travel** (+1); Trending win (+1); 2nd-tour Rave Review (+1); the "+1" events (+1) |
| **your board → on the stall** (commit) | **Promote** (place up to 2, may spread); certain events |
| **on the stall → your board** (win / keep) | you win the stall it sits on; or DUSK clears it unclaimed |
| **on the stall → your OWN supply** (lose / re-rally) | a *rival* wins a stall you had followers on; a bad-review event; Greedy Grab |

> **Wording-rail honesty guard (bg-theme, BINDING).** On a loss your followers disperse back to **your own
> colour's supply** to be re-rallied — they do **NOT** defect *to* the rival. The flavour line "the crowd
> drifts to the rival's stall" describes the **stall's new allegiance**, not a transfer of your meeples.
> Keep the word "meeple" out of all flavour voice — always "followers / your crowd."

### 2.2 Setup

- Each player takes their character's `max` followers in their colour, placing **`start` of them on their
  board** (baseline **2**; Influencer 網紅 also **2** — no head-start, §4) and the rest in their colour's
  **own supply** (a labelled per-colour bin/zone by their board — six colour bins, or one shared tray
  sorted by colour). *There is no shared/central follower pool — supply is per player.*
- Everything else in setup is unchanged (rules-draft §2): map, market decks, the **tightened** vendor
  slots (§1.3), DAY/NIGHT Booking decks with their boundary cards, characters, Larders.
- The per-count setup line on the board becomes **"followers per colour = your character's `max`"** (per
  player, not a shared scaled pool — the old shared-supply line is retired).

### 2.3 The turn (one action; unchanged list, two re-expressed)

- **VISIT / CONVENIENCE STORE / BOOK a tour** — unchanged.
- **TRAVEL** — move + reveal, then **grow your following: take 1 follower from your supply to your board**
  (was: raise dial +1). If your supply is empty you are at full pool; you still move.
- **PROMOTE** — place **up to 2** of your followers **from your board** onto stall(s) you stand with. You
  may split the 2 across two co-located face-up stalls (spread) or stack both on one. If your board holds
  fewer than 2, place what you have. **You cannot place followers you have not yet grown** — an empty board
  means Promote does nothing, exactly as an under-raised dial once blocked commitment.
- **BRIBE a stall** — resolve the crowd (§2.4).

### 2.4 Win / lose resolution (colours visible, plurality)

To **Bribe** a stall you stand with:

1. **Majority check** — you must have **strictly more of your followers on it than any single other agent**
   (an outright plurality). *A tie claims nothing.* **Big Brother 大哥** needs only to **match** the highest
   present (lever iii).
2. **Pay ingredients** — its recipe minus your region-icon discounts (Councillor home discount / away tax
   as today). **There is no follower threshold** — the ingredient cost is the only gate (§5).
3. **Take the stall** onto your tour; complete any held Booking it satisfies.
4. **Your followers on it → your board** — kept, redeploy free later.
5. **Each losing agent's followers on that stall → their OWN colour's supply** — they must re-grow them.
   This is the entire lost-contest penalty (replaces the −1/−2 dial-drop). *Losers go home to their own
   supply — they never join the winner.*
6. **Do NOT refill the slot now** — it stays empty until the end-of-round refill (§1.2).

- **A tie just blocks.** Level for the biggest crowd (no Big Brother present to break it)? No one claims;
  every agent's followers **ride** (stay on the stall). Promote again to take the lead, or walk away and
  leave them committed. *(At DUSK / LAST-TRAIN a tie is force-resolved — §8 reserve b.)*
- **Uncontested** = you have a majority with even a single follower (1 > 0); claim it if you can pay the
  ingredients.

### 2.5 Spread, re-commit, and the clock

- **Spread** = placing a Promote's followers on different co-located stalls. Spreading *across regions*
  still needs travelling, so the per-region face-up count (§1.3) bounds how thin you can spread.
- **Re-commit:** followers on an unresolved stall stay put between your turns; add to them with further
  Promotes. You never move a committed follower sideways — it stays until the stall is claimed (→ winner's
  board / losers' own supply) or the layer clears at DUSK.
- **黃昏 DUSK:** unclaimed day stalls clear as today; followers on those cleared, *unclaimed* stalls return
  to their owners' **boards** (the stall closed un-won; no contest was lost, so no one goes to supply). A
  tied contested stall at DUSK is force-resolved first (§8 reserve b).
- **末班車 LAST TRAIN:** a tied contested stall is force-resolved (§8 reserve b); then followers score
  nothing and are left where they lie. The deck-driven clock, decks, and boundary cards are unchanged.

---

## 3. The three CD-named balance levers (locked)

**Field baseline:** `max` **6**, start-on-board **2**, pace = Travel +1 (+ Trending / 2nd-Rave / the three
"+1" events, each +1), tie-break = tie blocks.

*Why `max` 6:* the old ceiling ended ~7.5 but peak commitment (`max_committed`) was only ~3–4.5 and the cap
rarely bound. Followers are now **kept on wins** (more efficient than the old return-and-re-Promote), so an
equal ceiling would loosen the fight; **6** is deliberately tighter than the old effective ~7.5 — enough to
spread 2+2+2 or stack 3+3 across a real fight, tight enough that you cannot flood every stall. `max` is the
#1 re-sim knob (sweep 5 / 6 / 7).

| Character | `max` (i) | start | pace (ii) | tie-break (iii) | meeple-native edge? |
|---|:--:|:--:|---|---|---|
| **Old Councillor 里長伯** | 6 | 2 | baseline | tie blocks | No — home-discount/away-tax is ingredient-side |
| **Homebody 媽寶** | 6 | 2 | baseline *(travels most → de-facto faster grow — **WATCH**)* | tie blocks | No — Travel-draw sourcer |
| **Big Eater 大胃王** | 6 | 2 | baseline; **Greedy Grab returns 1 follower to own supply** | tie blocks | No — the greed sink is the only touchpoint |
| **Influencer 網紅** | **8** | 2 | baseline | tie blocks | **Yes — higher `max`** (deeper pool; §4) |
| **Big Brother 大哥** | 6 | 2 | baseline | **WINS ties (match the most)** | **Yes — the tie-break** |
| **Globetrotter 阿嬤** | 6 | 2 | baseline | tie blocks | No — go-anywhere / Maintenance-immune is mobility-side |

---

## 4. Influencer 網紅 — the one judgement call (locked A), re-expressed as reach/viral

**Locked: `max` 8, start 2 (no head-start).** Her old edge was two parts — start-dial-4 (early tempo) and
floor-4 (sink-immunity, critic-flagged as possibly too strong). We re-express it as a single clean edge: a
**deeper pool** — she can keep **8** followers working once grown while the field caps at 6 — the soft heir
of floor-4 *without* the exception, and we drop the early head-start so she isn't double-buffed.

**Felt identity (bg-theme, re-expressed):** the Influencer is **reach / viral — she commands the biggest
crowd and arrives fashionably late**, not a slow grinder. Her deep pool is *the size of her following*;
"goes last" is *fashionably late* — she reads the room, then drops the largest crowd on the stall that
matters. Late-game character: goes-last + deep pool both bite at the end.

*Reserve:* if she reads **hot** in the re-sim, drop `max` **8 → 7** (§8 reserve c). If she reads **cold**,
add start 3.

---

## 5. Vendor cost (locked A): pure most-followers-wins, no threshold

The V7 rules already resolve a stall by **plurality** ("strictly more committed followers than any rival"),
not by clearing a per-vendor number. Confirmed in data: **`buzz_cost` = 2 for all 24 vendors and is
referenced nowhere in `rules-draft.md`** — vestigial. So:

- **DROP `buzz_cost`.** The follower fight is purely relative (out-commit your rivals); a stall's real cost
  is its **ingredients** (`ingredient_cost`, unchanged). The count needed to win is emergent (rival + 1; Big
  Brother = rival).
- Preserves the exact economy the sim closed (which never used a threshold), keeps the fight legible (count
  coloured followers, no hidden number), and adds no per-vendor number to parse.

*Reserve (hold):* a minimum-N-to-claim threshold. It would change the closed economy (uncontested stalls
currently fall to a single follower) and add a number to track. Hold **only** if the re-sim shows the
1-follower uncontested sweep is dominant — but the ingredient cost is expected to be the true throttle.

---

## 6. Draw retirement + prestige-Booking retarget (locked A)

**Drop the `draw` column** from `vendors.csv` (and DRAW references in the art docs). The three prestige
Bookings retarget to **total `ingredient_cost` of your won stalls** — the tightest structural heir (both
rise with tier), survives on every vendor, and reflavours cleanly from "popularity 人氣" to "the priciest,
most-sought tables."

| Booking | Old target | New target | Check |
|---|---|---|---|
| `d_prestige8` (day, val 4) | `draw_total_day >= 8` | **`ingredient_cost_day >= 4`** | day stalls all cost 1 → ≈ 4 day stalls (faithful to draw≥8). "The daytime spots worth queueing for." |
| `n_prestige14` (night, val 6) | `draw_total >= 14` | **`ingredient_cost_total >= 9`** | night draw ≈ cost+2/vendor → draw14 ≈ cost ~8–9 → **9** forces leaning into pricey night stalls. |
| `g_prestige12` (night, val 6) | `draw_total >= 12` | **`ingredient_cost_total >= 7`** | draw12 < draw14 → 7 < 9, preserving the relatively easier target (≈2 marquees). |

To hit ≥9 you must include night marquees (not enough day slots to reach 9 on cost-1 stalls), so
cheap-stall-spam can't satisfy the tall targets — the "揮金如土 money-no-object / marquee" flavour holds.
**Note the interaction with scarcity (§1.5 WATCH):** these targets require winning marquees, which are the
hardest-fought stalls under scarcity — re-sim tracks their completion.

---

## 7. Self red-team (for `bg-critic` — reconfirmed under scarcity)

The guardian critic already downgraded #1 (runaway) and reframed the goal (→ scarcity, now designed). The
live risks, sharpened by scarcity:

1. **Tie-block deadlock-vacuum — now MORE likely.** Scarcity + visible colours make it cheap to match a
   rival and freeze a single-slot region's stall. *Mitigation baked into the plan:* the DUSK/LAST-TRAIN
   tie-resolver (§8 reserve b) is now **load-bearing**, not optional.
2. **Endgame denial + follower-stranding — the rules HOLE, worsened by scarcity.** A trailing kingmaker
   re-ties a leader's Booking-critical single stall to freeze the Booking and strand ~half the leader's
   pool. Same mitigation (reserve b).
3. **Throughput throttle → Bookings uncompletable.** Fewer/slower stalls could drop Last-Train completion
   below the 95–98% floor. *The make-or-break sink guard in §9.*
4. **Big Brother 大哥 scales with contest frequency.** His match-to-win edge gets stronger the more the
   fight happens — and scarcity makes it happen more. Reserve = night-scope his tie-win (§8 reserve a).
5. **Influencer 網紅 goes-last + deep pool = a sniping double-buff** on exactly the axis scarcity amplifies.
   Reserve = `max` 7 (§8 reserve c).
6. **Homebody 媽寶 grow-compounding** — Travel now grows her following, and she travels most (mild).

---

## 8. Pre-specified RESERVES (do NOT bake — each with its trigger)

These are specified now so the re-sim can turn them on cleanly, but they are **not** in the baseline data.

| # | Reserve | Exact change | Trigger condition |
|---|---|---|---|
| **a** | **大哥 night-scope** | Big Brother wins ties **at night only** (day ties block for him too) | Re-sim shows 大哥 `idx` above band (> ~1.10 relative spread) — expected to worsen as contests get more frequent under scarcity (sim-proven 1.25 → in-band when night-scoped). |
| **b** | **Endgame-tie resolver** (closes the stranding/denial HOLE — **load-bearing under scarcity**) | At **DUSK** and at **LAST TRAIN**, any tied contested stall force-resolves to **most followers, then earliest committer**; that agent claims it (pays ingredients if able), losers → own supply | Always specified as the phase-boundary rule (one FAQ line). Fires whenever a contested stall is still tied when DUSK / LAST-TRAIN triggers. Prevents perpetual re-tie freezes and permanent stranding. |
| **c** | **Influencer 網紅 `max` 7** | Drop her pool 8 → 7 | Re-sim seat-delta / `idx` shows 網紅 above band (reads hot). |
| **d** | **Non-refilling apex marquees** (§1.6) | Tier-3 apex stalls (N06/C05/S06/E04) never refill once claimed | Overall contested_frac rises but the *apex* contested rate stays flat AND the CD wants the famous-stall brawl sharpened. |
| **e** | **`max` knob** | Field `max` 5 or 7 (sweep) | Re-sim: if the fight over-floods (too many followers per stall) → 5; if it under-fires / can't spread → 7. |

---

## 9. Re-sim scope (NOT run — CD-gated ~50 min; CD signs off THIS spec first)

Two changes reopen the win-a-vendor economy (meeples + scarcity), so re-run the standard V7 rig **per-count
3–6, N≥250/seating**, with these probes.

**Encode:** followers as a per-player pool (own supply / board / on-stall); Travel = grow 1; Promote = place
up to 2 from board (spread allowed); win → board; lost contest → own supply; `max` 6 (網紅 8), start 2; 大哥
matches; Greedy-Grab & bad-review = return 1 to own supply; Trending / 2nd-Rave / "+1" events = grow 1.
Retire `buzz_cost` / `draw` (plurality + cost-based prestige Bookings). **Scarcity:** tightened slot counts
(§1.3) + **slow refill (empty until end-of-round restock)**. Have reserves a–e switchable.

**★ MAKE-OR-BREAK PROBE #1 — does the battle actually happen more (the whole point):** `contested_frac`
must go **UP** toward roughly **2–3× the old 3–5%** (target ~10–15%). **Report the numerator and
denominator separately** — absolute contested-claims/gm AND total claims/gm — to prove the rise is **more
real fights** (numerator up), not a throughput artifact (denominator collapsing). If contested_frac rises
only because total claims fell, the scarcity failed and we escalate to reserve d / a tighter refill (phase-
boundary).

**★ MAKE-OR-BREAK PROBE #2 — sourcing/throughput health guard (the economy must survive the scarcity):**
- **Sourcing shares (§6b) stay INVARIANT** — Meat/Pantry/Tea/Seafood/Sugar/Veg within ~±2pts of the closed
  values (they are market-deck-driven; movement = encoding error).
- **Last-Train completion ≥ ~90%** and **turns/player ~26–32** (Bookings still finish; no grind).
- **claims/gm holds** (a mild dip is fine; a collapse means the sink is throttled → back off counts or
  soften refill).
- **Prestige-Booking completion** specifically (the marquee targets vs the marquee fights).
- **gain vs sink, supply_min, capbind** — confirm ingredients don't overflow into dead sourcing.

**New / reopened balance probes:** six-character band 3–6p (Influencer / Big Brother / Homebody watch);
runaway (leader margin, leader-change frequency, lost-contest/gm); 1-follower uncontested-sweep rate;
`max` knob sweep 5/6/7; **tie-block / frozen-slot frequency** (does the deadlock-vacuum bite? does reserve
b clear it?); Big Brother idx under night-scope (reserve a); Influencer idx under `max` 7 (reserve c).

**Sequencing (critic's rec B):** run this scoped re-sim FIRST, then the human 6p judges fun / denial-feel /
"did the scrum materialise."

---

## 10. Precise DATA changes (for `bg-developer` LATER — do NOT execute now)

- **`map.json`** — replace `vendor_slots` per §1.4 (tightened counts + `refill: SLOW/per-round` + updated
  `_note`); update `regions[].slots_n` (C 2→1, S 2→1). Replace the shared "Followers supply" line with a
  per-colour follower supply zone; the setup-chart line becomes "followers per colour = your `max`"; remove
  any dial-track element.
- **`characters.csv`** — add `max`, `start_meeples` (field 6/2; **網紅 8/2**); recode `start_max_4` → the
  `max`/`start` pair; rewrite 網紅 ability text (dial-starts-4 → owns 8 followers; drop floor-4; reach/viral
  voice); 大胃王 greed sink "dial −1" → "return 1 follower to your supply"; scrub "Followers-max / dial" →
  "Follower / your pool" in all strings. No kit *values* change for 里長伯 / 媽寶 / 大胃王(ingredient) / 大哥
  / 阿嬤.
- **`vendors.csv`** — DROP `draw`; DROP `buzz_cost`. Keep `ingredient_cost`, `icon`, `trending`, `recipe`,
  tier, phase, etc.
- **`bookings.csv`** — retarget the 3 prestige rows (§6): `d_prestige8` → `ingredient_cost_day>=4`;
  `n_prestige14` → `ingredient_cost_total>=9`; `g_prestige12` → `ingredient_cost_total>=7`; reword effects
  from "Draw (人氣)" to the cost/marquee flavour; keep `value`, ids, art_note.
- **`tokens.csv`** — replace the single grey `followers` row with six per-colour follower entries (8 per
  colour = 48, so any colour can play 網紅's `max` 8; others use 6); DROP the `dial` row. Keep `trending`,
  `mkTours`, `hsrClosed`, `pileWin`, `pileLose`, pawns.
- **`events.csv`** — the "+1 Followers-max" events (EV-D09 / EV-N13 / EV-N14) → "grow 1 follower (supply →
  board)"; EV-N09 Trending win → grow 1; EV-N15 / EV-N16 bad-review → "return 1 follower to your supply"
  (keep the crowd-drifts-to-a-rival flavour rail — describes allegiance, not transfer); EV-N08 (place 2 on
  a co-located stall) → place 2 from your board; EV-N11 (next Promote +1) → next Promote places +1; scrub
  dial wording throughout.

**Not data (separate passes, flag on hand-off):** `rules-draft.md` §§3–5 rewrite (dial → follower pool;
grow/place; win-keeps / lose-to-own-supply; slow-refill scarcity; DUSK/LAST-TRAIN tie-resolver; FAQ dial
questions) — an editorial pass (`bg-elegance` / `bg-rulebook`), **must land as a net cut** (7 words
headroom) and be re-gauged. The board's dial zone → follower-pool zone + per-colour supply tray →
`bg-infodesign`. Neither touches values.

---

## 11. Handoff — trigger the coherence check

Two mechanics moved: **(1) the signature twist got a scarcity engine** — slow-refill + tighter slots make
the contested crowd-fight frequent (the "race AND battle" the CD wants); **(2) the fight became physical
coloured followers** — win keeps them on your board, loss sends them home to your own supply. Flag the
Director to run **`bg-theme`** (does the fiction still explain "the market restocks between passes" and
"your crowd comes home on a win / disperses to your own supply on a loss"? the "dial" is gone from lore)
and **`bg-elegance`** (combined re-gauge: the meeple swap is a net *trim*, the slow-refill rule is a net
*add* — confirm the two net out within budget, and re-gauge the §§3–5 rulebook rewrite against the 7-word
headroom). Mechanics that moved for the guardian sweep to check: **the vendor slot counts + refill timing,
Promote (now spread onto scarce stalls), Travel-ramp → grow, the lost-contest penalty (→ own supply), the
DUSK/LAST-TRAIN tie-resolver, and the win-return direction.**
