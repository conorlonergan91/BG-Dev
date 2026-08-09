# Travel Agents: Taiwan — V7 → V7-M: Follower MEEPLES + VENDOR SCARCITY (LOCKED — CD-SIGNED)

> **Status: LOCKED — CD-SIGNED (2026-08-09).** Spec-only; no data/rules/code touched yet, no sim run. The CD
> has signed off; this is the FINAL model. §10 is the file-by-file data-change list `bg-developer` executes
> next; `bg-playtest` then runs the scoped re-sim (§9). Folds the guardian sweep (bg-theme + bg-elegance +
> bg-critic) AND the final-lock corrections: the Old Councillor is **locked as the home-gated favours
> engine** (§6.6), the Big Brother's edge is a **margin dial N** (§6.7), and two former reserves are **baked
> into baseline** — the DUSK/LAST-TRAIN tie-resolver (§2.6) and the Globetrotter's Travel-cost (§6.5b).
>
> **Two coupled changes:**
> 1. **MEEPLES (CD mandate):** replace the abstract Followers-max DIAL with physical, collectable,
>    colour-coded **Follower meeples**. The dial "didn't feel natural"; meeples make the area-majority
>    fight legible and turn *losing* into a real tempo cost. (Guardians GREEN-LIT this — feel/elegance/
>    theme all improve. Locked parameters below.)
> 2. **SCARCITY (CD decision):** the V7 sim proved the contested crowd-fight — the signature twist — fires
>    in only **~5% of vendor claims** (`contested_frac` 3.3/5.3/4.6/4.9% at 3–6p). The CD wants a **"race
>    AND battle"** game, not a 5%-of-the-time sideshow. The critic located the lever: **vendor scarcity**
>    (a map/setup knob, NOT a meeple rule). §1 designs it.
> 3. **CHARACTER LANES (CD steers, this pass):** the Big Brother's tie-win becomes a tunable **margin dial
>    N (0/1/2)** (§6.7), and each of the six characters is expressed as a **distinct strategic lane** in the
>    new economy (§6.5) — including a **real rework of the Old Councillor** into a resource-engine rush
>    (REPLACE-vs-BLEND for the CD, §6.6).
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
mitigation is the now-BASELINE DUSK / LAST-TRAIN tie-resolver** (§2.6) — scarcity makes that resolver
load-bearing, so it ships as a baseline rule, not a switchable reserve. It guarantees every frozen stall
clears at each phase boundary.

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
   (an outright plurality). *A tie claims nothing.* **Big Brother 大哥** wins by the **margin dial N** (§6.7;
   baseline N=1 = wins ties).
2. **Pay ingredients** — its recipe minus your region-icon discounts. *(The Old Councillor no longer has a
   home Bribe discount — his edge is the home-gated draw, §6.6.)* **There is no follower threshold** — the
   ingredient cost is the only gate (§5).
3. **Take the stall** onto your tour; complete any held Booking it satisfies.
4. **Your followers on it → your board** — kept, redeploy free later.
5. **Each losing agent's followers on that stall → their OWN colour's supply** — they must re-grow them.
   This is the entire lost-contest penalty (replaces the −1/−2 dial-drop). *Losers go home to their own
   supply — they never join the winner.*
6. **Do NOT refill the slot now** — it stays empty until the end-of-round refill (§1.2).

- **A tie just blocks.** Level for the biggest crowd (no Big Brother present to break it)? No one claims;
  every agent's followers **ride** (stay on the stall). Promote again to take the lead, or walk away and
  leave them committed. *(At DUSK / LAST-TRAIN a tie is force-resolved — the **baseline** endgame-tie
  resolver, §2.6.)*
- **Uncontested** = you have a majority with even a single follower (1 > 0); claim it if you can pay the
  ingredients.

### 2.5 Spread, re-commit, and the clock

- **Spread** = placing a Promote's followers on different co-located stalls. Spreading *across regions*
  still needs travelling, so the per-region face-up count (§1.3) bounds how thin you can spread.
- **Re-commit:** followers on an unresolved stall stay put between your turns; add to them with further
  Promotes. You never move a committed follower sideways — it stays until the stall is claimed (→ winner's
  board / losers' own supply) or the layer clears at DUSK.
- **黃昏 DUSK:** the **endgame-tie resolver** (§2.6) fires on any still-tied contested day stall first; then
  unclaimed day stalls clear as today, and followers on those cleared, *unclaimed* stalls return to their
  owners' **boards** (the stall closed un-won; no contest was lost, so no one goes to supply).
- **末班車 LAST TRAIN:** the **endgame-tie resolver** (§2.6) fires on any still-tied contested stall; then
  followers score nothing and are left where they lie. The deck-driven clock, decks, and boundary cards are
  unchanged.

### 2.6 Endgame-tie resolver (BASELINE rule — shipped, not a reserve)

> **Rule.** At **DUSK** and at **LAST TRAIN**, any contested stall that is still **tied** force-resolves to
> **most followers, then earliest committer**; that agent claims it (paying ingredients if able), and each
> loser's followers → their own supply.

This is a **baseline, shipped rule**, not a switchable dial. Under scarcity it is **load-bearing**: single
non-refilling slots make it cheap for a trailing kingmaker to perpetually re-tie a leader's Booking-critical
stall — freezing the Booking *and* stranding ~half the leader's pool — with no counter at LAST TRAIN. The
resolver closes that HOLE and guarantees every frozen slot clears at each phase boundary. *(Sim note: run it
ON vs OFF **once** to prove it is load-bearing — expect frozen-slot/denial frequency to spike with it OFF —
then bake ON for all remaining runs.)*

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
| **Big Brother 大哥** | 6 | 2 | baseline | **MARGIN dial N (baseline 1 = wins ties)** — §6.7 | **Yes — the tie margin** |
| **Globetrotter 阿嬤** | 6 | 2 | baseline | tie blocks | No — go-anywhere / Maintenance-immune is mobility-side |

The Big Brother's tie-break is no longer on/off — it is a graduated **margin dial N** (§6.7) so the
playtester can pull him back (he runs hot, and scarcity strengthens his match-edge) or push him up,
without any day/night exception to teach.

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

## 6.5 The six strategic LANES (each character wants to play the new economy differently)

The meeple + scarcity economy should reward **six distinct plans**. The design goal is that a player picks
a character and immediately knows a *different* answer to "how do I win the scarce crowd-fight and finish
Bookings." Two lanes attack the contest head-on (build-high, margin), two are economy-rushes (draw, glut),
one forages *around* the fight, one owns *position*.

| # | Character | Lane (the plan) | Core mechanism | Starting knob | How scarcity touches it |
|---|---|---|---|---|---|
| 1 | **Influencer 網紅** | **Build-high battler** — out-mass the field, win the marquee stalls by raw crowd | `max` **8** (field 6); wins contests on sheer follower count | `max=8, start=2` | **THRIVES** — scarce contested stalls reward whoever commits most; deep pool is decisive. (Watch: too strong → reserve `max` 7.) |
| 2 | **Old Councillor 里長伯** | **Home-anchored resource rush** — front-load ingredients at home → afford pricey dishes EARLY, then range out to take them before the crowd builds | **HOME-GATED DRAW** (§6.6): *while in your home region*, start of turn draw 1 from any region, no action | home region (named at setup); draw = **+1/turn while home only** | The **gate IS the flaw** — camp home to run the engine vs range out to contest scarce stalls; buying a pricey stall before the pack arrives beats fighting under scarcity. REWORK (reopens his closed balance). |
| 3 | **Homebody 媽寶** | **Mobile forager who picks his battles** — wide ingredient spread from moving → afford complex dishes → win stalls the pack isn't on | **FORAGE**: on TRAVEL, draw 2 from the region you LEFT (sole Travel-sourcer) | `travel_draw_left = 2` | **PRESSURED, not exempt** — scarcity thins the "quiet" stalls too (1 non-refilling slot/region), so he can dodge the *cheap* scrums but must still fight for the *pricey* marquees his spread unlocks (§6.5a). |
| 4 | **Big Eater 大胃王** | **Greedy sourcing glut** — raw ingredient volume from Visits → afford anything, paced by a follower cost | **GLUT**: Visit keep ALL 3 + greedy 4th; hazards fire twice on his Visit | keep-3; greedy-4th = **return 1 follower to your supply**; hazard×2 | The greedy-4th follower cost pulls followers off his board → he is a **weaker battler**, so he wants cheap-to-win / uncontested stalls; scarcity makes him pace his greed. |
| 5 | **Big Brother 大哥** | **Margin battler** — win contests on the MARGIN, not the mass; fewer followers per win | **MARGIN dial N** (§6.7) | `N = 1` (baseline; = current wins-ties) | **Edge scales UP** with contest frequency — the reason he gets a tunable dial (pull back to 0, or up to 2). |
| 6 | **Globetrotter 阿嬤** | **Ubiquity** — reach any region in one Travel; chase whichever scarce slot just opened | `travel_anywhere`; immune to the HSR Maintenance outage | **Travel-anywhere costs 1 follower to supply** (baseline ON — "the trip tires her crowd") | **BUFFED by scarcity** — when each region has 1 region-locked, non-refilling slot, best positioning = best snipe → the cost is baked into baseline (§6.5b). |

### 6.5a Homebody — viable dodge, NOT a dominant "ignore the contest" exploit

The tension the CD flagged is real: we added scarcity to *force* fights, and the Homebody's whole lane is
*avoiding* them. Three structural reasons scarcity keeps him honest rather than handing him an exploit:

1. **Scarcity thins the quiet corners too.** His dodge relies on "stalls others aren't fighting over." Under
   slow-refill + floor-1 counts, even a quiet region holds a *single* non-refilling slot — so a second
   dodger, or the Globetrotter, contests it and he's in a fight anyway. The lever that forces the pack's
   fights also closes his free lane.
2. **His payoff dishes are the contested ones.** A wide ingredient spread's whole point is affording the
   **complex, multi-ingredient** dishes — which are the tier-2/3 **night marquees**, i.e. the *most*-fought
   stalls under scarcity. He can dodge the cost-1 scrums; he cannot dodge the marquee fight and still cash
   his spread. His lane is *pick your battles*, not *skip them*.
3. **He commits no follower cost to source**, so if he *does* enter a fight his board is full — meaning a
   pure-dodge Homebody who banks followers is actually a *latent* battler, not a non-participant.

**The REAL exploit to hunt (bg-critic) — the "banked-board late-battler."** Point 3 above is also the risk:
his **Travel does three jobs** (move + sole-sourcer draw-2 + grow a follower), and he **Travels most** — so
he can bank a full board *and* out-source, then arrive at the marquee as the deepest-pool battler after all.
**Re-sim must confirm** (§9) the "ignore-the-contest" line is viable but **not dominant**. The **preferred
hot-fix is reserve g′** — **Travel grows a follower for everyone EXCEPT the Homebody** (deny his triple-dip
on the correct axis); the old `travel_draw_left 2→1` (reserve g) trims his *sourcing spread*, the **wrong
axis**, and is only a fallback.

### 6.5b Globetrotter — scarcity is a buff; the cost is now BASELINE

Go-anywhere-in-one-Travel is worth *more* when stalls are scarce and region-locked: she can always be where
the one open slot is, and snipe a quiet-region single slot before a Homebody walks over. Positioning becomes
premium exactly as she has the best of it. She was already the **4p idx outlier**, and *both* headline
changes (meeples + scarcity) buff her go-anywhere — so bg-critic pre-loads the cost into the **baseline**
rather than holding it in reserve: **her Travel-anywhere costs 1 follower to supply** ("the trip tires her
crowd"). *The re-sim runs it ON (baseline) **and** OFF to measure the delta*; if she is still hot with the
cost ON, the fallback is Larder cap 7→6 (reserve f-alt). The small-basket flaw stays retired.

## 6.6 Old Councillor 里長伯 — the resource-engine REWORK (CD choice: REPLACE vs BLEND)

**LOCKED (CD sign-off): the HOME-GATED FAVOURS ENGINE.** The CD chose the home-gated synthesis over both
REPLACE and BLEND — it is the all-guardian-convergent answer: it gives bg-critic the *shaped* (non-free)
draw and bg-theme the borough cushion in one mechanic, and keeps him clearly home-anchored (no free
island-wide tick, no muddy double-engine).

> **FINAL KIT — 里長伯 The Old Councillor.**
> **Ability — *Old Favours* (home-gated draw engine):** at setup, name ONE **home region** (open). **While
> you are in your home region**, at the start of your turn **draw 1 ingredient card from any region's
> market** into hand (no action spent). Away from home, the engine is dark.
> **No home Bribe discount** (the draw is his *sole* home edge — bg-elegance: no double-engine).
> **No away-tax** (dropped).
> **The shaped flaw is emergent, not a printed penalty:** the engine only ticks at home, so he must choose
> between **camping home to run the engine** and **ranging out to contest scarce stalls** — a real
> positional tension (bg-critic's "shaped draw") that also re-earns his home identity (bg-theme's borough
> cushion). Nothing is bolted on; the gate *is* the flaw.

*Why home-gated (fork resolved):* a free island-wide +1/turn (the old REPLACE knob) was unshaped and
snowbally under the new economy; BLEND stacked two edges. Gating the draw to home makes it **conditional
buying power** — he front-loads ingredients *when he holds his ground*, then must spend a Travel (and go
dark) to cash them on the pricey stalls elsewhere. The tension is the balance.

**BINDING sensitivity rail (bg-theme + bg-publishing — the flagged #1 consultant item).** Re-theme the draw
as **inbound goodwill**: people look after a beloved lifelong local public servant — neighbours and
stall-owners bring him **the day's best** while he keeps his post in the borough (*gifts inbound*). It is
**NEVER** string-pulling / patronage / favour-trading / bribery. This must go to the **paid Taiwanese
cultural consultant BEFORE art/print** — a favours-politician theme sitting next to the game's own "Bribe"
verb is the single highest sensitivity risk in the roster; the consultant confirms the framing reads as
warm civic affection, secular and dignified, not machine-politics. **Copy edits flagged (do NOT edit here):**
`identity.md` + `names.md` + `characters.csv` blurb — retire "clout / pulls strings" language, adopt the
inbound-goodwill voice; the printed kit line changes from home-discount/away-tax to *Old Favours* (home-gated
draw).

## 6.7 Big Brother 大哥 — the MARGIN dial (replaces the night-scope reserve)

His edge is no longer on/off. It is a graduated **margin dial N**:

> **Rule.** In a contested stall, the Big Brother claims it if the highest rival's committed followers
> exceed his own by **fewer than N** (i.e. `max_rival − his ≤ N − 1`). N is the tuning knob.

| N | Effect | Where |
|:--:|---|---|
| **0** | He **loses ties** — needs a strict plurality like everyone (no edge) | WEAK end — **the real cool-down** |
| **1** | He **wins ties** — a rival needs +1 to beat him | **BASELINE (= current "wins ties")** |
| **2** | He also **shrugs off a one-follower deficit** — a rival needs +2 | **SWEEP CEILING — probe only, NOT a baseline candidate** |

- **Baseline N = 1** (reproduces today's behaviour exactly). Playtest sweep: **0 / 1 / 2.** **N=2 is the
  sweep ceiling, not a shipping candidate** — bg-critic: under *frequent* fights (the whole point of
  scarcity) surviving a one-follower deficit compounds into a degenerate omnipresent-contest edge. Ship at
  0 or 1; use 2 only to map the curve.
- **The real cool-down is N → 0**, not phase-scoping. This dial **replaces** the old night-scope reserve.
- **bg-critic finding — night-scope is INEFFECTIVE as a cool-down.** The old sim showed night-only ≈
  neutral-to-*worse* (idx **1.25 night-only vs 1.19 all-game**) precisely because fights **concentrate at
  night** — restricting his edge to the phase where almost all contests happen barely restricts it — and
  **slow-refill worsens this** (it pushes even more of the fight into the busy night board). So a night-scope
  is kept only as a **labelled harmless option**; **we do NOT rely on it** to cool him down. If N=1 still
  overshoots, drop to **N=0** — do not reach for night-scope.


## 7. Self red-team (for `bg-critic` — reconfirmed under scarcity)

The guardian critic already downgraded #1 (runaway) and reframed the goal (→ scarcity, now designed). The
live risks, sharpened by scarcity:

1. **Tie-block deadlock-vacuum — now MORE likely.** Scarcity + visible colours make it cheap to match a
   rival and freeze a single-slot region's stall. *Mitigation now BAKED IN:* the DUSK/LAST-TRAIN
   tie-resolver (§2.6) is a baseline rule, load-bearing under scarcity.
2. **Endgame denial + follower-stranding — the rules HOLE, worsened by scarcity.** A trailing kingmaker
   re-ties a leader's Booking-critical single stall to freeze the Booking and strand ~half the leader's
   pool. Same mitigation (baseline §2.6).
3. **Throughput throttle → Bookings uncompletable.** Fewer/slower stalls could drop Last-Train completion
   below the 95–98% floor. *The make-or-break sink guard in §9.*
4. **Big Brother 大哥 scales with contest frequency.** His margin edge gets stronger the more the fight
   happens — and scarcity makes it happen more. Cool-down = **margin N → 0** (§6.7); night-scope is
   ineffective (it restricts him to the phase where nearly all fights already are) and is NOT relied on.
5. **Influencer 網紅 goes-last + deep pool = a sniping double-buff** on exactly the axis scarcity amplifies.
   Reserve = `max` 7 (§8 reserve c).
6. **Homebody 媽寶 grow-compounding → the banked-board late-battler** — Travel now grows his following, does
   three jobs, and he travels most. Preferred fix = grow-tick OFF for him (reserve g′, §6.5a).

---

## 8. BASELINE-baked rules + pre-specified RESERVES

Two items that were reserves are now **baked into the baseline** (shipped rules, not switchable dials);
the rest remain specified-but-not-baked, each with its trigger.

**BAKED INTO BASELINE (no longer reserves):**
- **Endgame-tie resolver (§2.6)** — a shipped rule. Load-bearing under scarcity (closes the re-tie
  freeze / stranding HOLE). *Sim runs it ON vs OFF once to prove load-bearing, then bakes ON.*
- **Globetrotter 阿嬤 Travel-cost (§6.5b)** — her Travel-anywhere now **costs 1 follower to supply** in the
  **baseline sim config** ("the trip tires her crowd"). She was already the 4p outlier and *both* headline
  changes (meeples + scarcity) buff her go-anywhere, so the cost ships ON by default. *Sim runs it ON and
  OFF for the delta.*

| # | Reserve (NOT baked) | Exact change | Trigger condition |
|---|---|---|---|
| **c** | **Influencer 網紅 `max` 7** | Drop her pool 8 → 7 | Re-sim seat-delta / `idx` shows 網紅 above band (reads hot). |
| **d** | **Non-refilling apex marquees** (§1.6) | Tier-3 apex stalls (N06/C05/S06/E04) never refill once claimed | Overall contested_frac rises but the *apex* contested rate stays flat AND the CD wants the famous-stall brawl sharpened. |
| **e** | **`max` knob** | Field `max` 5 or 7 (sweep) | Re-sim: if the fight over-floods (too many followers per stall) → 5; if it under-fires / can't spread → 7. |
| **g′** | **Homebody 媽寶 triple-dip denial** (§6.5a — the *preferred* lever) | **Travel grows a follower for everyone EXCEPT the Homebody** (his Travel keeps its move + sole-sourcer draw, but no free follower-grow) | Re-sim shows the **banked-board late-battler** line reads hot — the real exploit: Travel does 3 jobs (move + source + grow) and he Travels most, so he banks a full board *and* out-sources. Denying his grow-tick targets the actual axis. |
| **g** | **Homebody 媽寶 spread trim** (secondary — **wrong axis**) | `travel_draw_left` 2 → 1 | Held only as a fallback. bg-critic: this trims his *sourcing spread*, not the banked-board exploit — reach for **g′** first. |
| **f-alt** | **Globetrotter 阿嬤 further cost** | If Travel-cost (now baseline) is insufficient: Larder cap 7 → 6 | Re-sim shows 阿嬤 still above band *with* the baseline Travel-cost ON. |
| **h** | **Big Eater 大胃王 greedy-4th cost** | −1 follower to supply → −2 | Re-sim shows she leans on greedy-4th too hard / over-sources. |
| — | **Big Brother 大哥 night-scope** | *(labelled harmless option, §6.7 — INEFFECTIVE as a cool-down; we do NOT rely on it. The real cool-down is margin **N → 0**.)* | Not a trigger — retained only as an available toggle for completeness. |

### 8.1 CONSOLIDATED PLAYTEST-LEVER TABLE (all dials in one place)

Everything the playtester can turn, baseline → range, folding the scarcity, meeple, and character knobs:

| Dial | Baseline | Range / options | Owns |
|---|---|---|---|
| **Scarcity — refill cadence** | slow / per-round | immediate (off) · per-round · phase-boundary (harder) | §1.2 |
| **Scarcity — face-up counts** | §1.3 (4/5/5/6) | looser (old 6/7/8/9) ↔ tighter | §1.3 |
| **Field `max`** | 6 | 5 / 6 / 7 | §3, reserve e |
| **start-on-board** | 2 | 2 (raise if a lane reads cold) | §3 |
| **Influencer 網紅 `max`** | 8 | 7 / 8 | §4, reserve c |
| **Big Brother 大哥 margin N** | **1** | 0 / 1 / **2 = sweep ceiling (not shippable)** — ship at 0 or 1 | §6.7 |
| **Big Brother 大哥 scope** | all-phases | night-only = **labelled harmless option; INEFFECTIVE cool-down, not relied on** | §6.7 |
| **Old Councillor 里長伯** | **home-gated draw** (LOCKED, §6.6) | draw fires while in home region only; no home Bribe discount, no away-tax | §6.6 |
| **Homebody 媽寶 grow-tick** | ON (grows on Travel like everyone) | **OFF for Homebody only** (triple-dip denial — the preferred hot-fix) | §6.5a, reserve g′ |
| **Homebody 媽寶 forage** | draw 2 | 2 / 1 (secondary, wrong axis) | §6.5a, reserve g |
| **Big Eater 大胃王 greedy-4th cost** | −1 follower to supply | −1 / −2 (if she over-sources) | §6.5, §2.1, reserve h |
| **Globetrotter 阿嬤 Travel-cost** | **1 follower to supply (baseline ON)** | ON (baseline) / OFF (delta run) / + cap 6 (f-alt) | §6.5b |
| **Endgame-tie resolver** | **ON — BASELINE rule (§2.6)** | on (baseline) / off (one delta run to prove load-bearing) | §2.6 |
| **Non-refill apex marquees** | off | off / on | §1.6, reserve d |

---

## 9. Re-sim scope (NOT run — CD-gated ~50 min; CD signs off THIS spec first)

Two changes reopen the win-a-vendor economy (meeples + scarcity), so re-run the standard V7 rig **per-count
3–6, N≥250/seating**, with these probes.

**Encode (BASELINE config):** followers as a per-player pool (own supply / board / on-stall); Travel = grow
1; Promote = place up to 2 from board (spread allowed); win → board; lost contest → own supply; `max` 6
(網紅 8), start 2; 大哥 = **margin dial N** (baseline 1); **里長伯 = HOME-GATED draw** (draw 1 from any
region only while in his home region; no home Bribe discount, no away-tax); **阿嬤 Travel-anywhere costs 1
follower to supply (baseline ON)**; **endgame-tie resolver ON (baseline §2.6)**; Greedy-Grab & bad-review =
return 1 to own supply; Trending / 2nd-Rave / "+1" events = grow 1. Retire `buzz_cost` / `draw` (plurality +
cost-based prestige Bookings). **Scarcity:** tightened slot counts (§1.3) + **slow refill (empty until
end-of-round restock)**. **Switchable for deltas:** tie-resolver ON/OFF (prove load-bearing, once); 阿嬤
Travel-cost ON/OFF; Big Brother N=0/1/2; 里長伯 home-gated vs the rejected island-wide & BLEND variants (for
reference); Homebody grow-tick ON/OFF (g′); reserves c/d/e.

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
**runaway sharpened to consecutive-WIN-STREAK length** (the win-keeps-followers brake removal — does a
serial winner cycle their pool for free?) alongside leader margin / leader-change frequency / lost-contest
/gm; 1-follower uncontested-sweep rate; `max` knob sweep 5/6/7; **tie-block / frozen-slot frequency with the
resolver ON vs OFF** (does the deadlock-vacuum bite with it OFF? confirm §2.6 clears it — then bake ON);
Influencer idx under `max` 7 (reserve c); **live-decision-density per lane** (each lane must keep meaningful
choices, not collapse to a script); **seat-fairness under slow-refill (NEW re-open)** — per-round refill
re-opens a *first-into-a-region-each-round* advantage the old immediate-refill board didn't have; re-check
the s0…sN spread (was ok at ±few %).

**★ NEW — the six LANES must be DISTINCT and BANDED (the Steer-2 goal):**
- **Distinctness (not just balance):** per-character behavioural fingerprints should *diverge*, not just
  their winrates match. Report per character: contest-entry rate (Influencer/Big Brother high; Homebody
  low), followers-per-win (Big Brother lowest — margin; Influencer highest — mass), sourcing method mix
  (Councillor draw-share vs Homebody Travel-share vs Big Eater Visit-share), and **time-to-first tier-2/3
  claim** (the Councillor rush must land *earlier* than the field — the whole point of his rework). If two
  lanes fingerprint the same, they've blurred (esp. the three resource engines).
- **No dominant lane** — band idx 3–6p, with three sharp per-lane probes:
  - **(i) Homebody 媽寶 — the BANKED-BOARD late-battler bot** (the real exploit, not the dodge): a bot that
    Travels most, banks a full board *and* out-sources, then arrives deepest at the marquee. Measure
    **Travel-grow contribution** (how much of his board comes from the free grow-tick vs everyone) and
    **followers-at-first-marquee**. If dominant → reserve **g′** (grow-tick OFF for him), not g.
  - **(ii) Globetrotter 阿嬤 — snipe-rate** (how often she takes a just-opened scarce slot before a rival
    reaches it) and the **reserve-f ON/OFF delta** (Travel-cost is baseline ON; the OFF run measures how
    much the two headline changes buffed her).
  - **(iii) Big Brother 大哥 — edge-fire-rate under frequent fights** (how often his margin actually decides
    a claim now that fights are common) across the **N = 0 / 1 / 2** sweep; confirm the **N=0 floor** cools
    him (night-scope is NOT relied on) and that N=2 is degenerate (ceiling only).
- **Old Councillor 里長伯 — the home-gated engine:** is his tier-2/3 buying **front-loaded vs flat** (does he
  actually reach pricey stalls *earlier* than the field — the whole point)? Report **free-cards/gm**, his
  **turn-shape / action-mix** (does the home-gate visibly split his game into camp-then-range?), and run
  **home-gated vs the rejected island-wide & BLEND variants** for reference (home-gated should be less
  snowbally than island-wide and cleaner-fingerprinted than BLEND).

**Sequencing (critic's rec B):** run this scoped re-sim FIRST, then the human 6p judges fun / denial-feel /
"did the scrum materialise."

---

## 10. FINAL "what changes in DATA" list (CD-SIGNED — for `bg-developer` to EXECUTE next)

The spec is **LOCKED**. Below is the file-by-file change set. Everything is a value/column/row change to
component data or `map.json`; the rulebook/board/FAQ rewrites are the separate presentation passes noted at
the end. Run `tools/lint/check_game.py` after.

- **`characters.csv`** — add columns **`max`** and **`start_meeples`**; recode `ability_code` `start_max_4`
  → the `max`/`start` pair; scrub "Followers-max / dial" → "Follower / your pool" in every string. Final six
  kits:
  1. **里長伯 The Old Councillor — HOME-GATED FAVOURS ENGINE (LOCKED, §6.6):** `max=6, start_meeples=2`.
     **DROP** `discount_home` **and** `away_tax`. New ability `favours_home_draw`: *"Old Favours — name one
     home region at setup; **while in your home region**, at the start of your turn draw 1 ingredient card
     from any region's market (no action)."* Rewrite `ability` / `flaw` / `blurb` / `effect` to the
     **inbound-goodwill** voice (neighbours bring a beloved local public servant the day's best) — **rail:
     never string-pulling / patronage / bribery; secular, dignified.** *(Reopens his closed balance — the
     away-tax +2 trim is gone; re-sim.)*
  2. **媽寶 The Homebody:** `max=6, start_meeples=2`. Kit unchanged (`travel_draw_left`=2, flaw-free). *(Hot-fix
     reserve g′ = grow-tick OFF for him — held, not baked.)*
  3. **大胃王 The Big Eater:** `max=6, start_meeples=2`. `visit_keep3` + `hazard_twice_visit` unchanged;
     **greedy-4th sink "dial −1" → "return 1 follower to your supply"**.
  4. **網紅 The Influencer:** **`max=8`**, `start_meeples=2`. Rewrite ability: dial-starts-4 / floor-4 →
     *"owns 8 followers (the field owns 6)"*; **drop floor-4**; **reach/viral** voice (biggest crowd,
     fashionably late), not slow grinder. Keeps `goes_last`.
  5. **大哥 The Big Brother — MARGIN DIAL (LOCKED, §6.7):** `max=6, start_meeples=2`. Recode `win_ties` →
     **`margin_win` with parameter `N`, baseline `N=1`**. Ability text: *"wins a contested stall unless a
     rival exceeds his committed followers by N or more (N=1 → wins ties)."* *(Ship at 0 or 1; N=2 is a
     sweep ceiling only.)*
  6. **阿嬤 The Globetrotter:** `max=6, start_meeples=2`. `travel_anywhere` + HSR-immune unchanged, **plus a
     BASELINE cost: Travel-anywhere costs 1 follower to your supply** ("the trip tires her crowd"). *(Sim
     also runs it OFF for the delta; further reserve f-alt = Larder cap 7→6, held.)*
- **`vendors.csv`** — **DROP the `draw` column**; **DROP the `buzz_cost` column** (both vestigial). Keep
  `ingredient_cost`, `icon`, `trending`, `recipe`, `tier`, `phase`, `region`, etc. unchanged.
- **`bookings.csv`** — retarget the 3 prestige rows to **total `ingredient_cost`**: `d_prestige8` →
  **`ingredient_cost_day >= 4`**; `n_prestige14` → **`ingredient_cost_total >= 9`**; `g_prestige12` →
  **`ingredient_cost_total >= 7`**. Reword each `effect` from "Draw (人氣)" to the priciest/marquee-tables
  flavour; keep `value`, ids, `art_note`.
- **`tokens.csv`** — **DROP the single grey `followers` row** and **DROP the `dial` row**. Add **six
  per-colour Follower meeple entries** (pawnA–F colours), **8 per colour = 48 total** (so any colour can play
  網紅's `max` 8; other characters use 6). Keep `trending`, `mkTours`, `hsrClosed`, `pileWin`, `pileLose`,
  pawns.
- **`map.json`** — replace `vendor_slots` per **§1.4** (tightened per-count counts **3:4 / 4:5 / 5:5 / 6:6**
  + new **`refill` = SLOW / per-round** field + updated `_note`); update `regions[].slots_n` (**central 2→1,
  south 2→1**; north stays 2, east stays 1). Replace the shared "followers_supply" scaled block with a
  **per-colour follower supply zone**; the per-count setup line becomes **"followers per colour = your
  `max`"**; remove any dial-track element. Add a **Globetrotter note** to the setup/legend text
  ("阿嬤's Travel-anywhere costs 1 follower to supply"). *(The DUSK/LAST-TRAIN tie-resolver and the
  per-round refill are rules text, carried in `rules-draft.md`, not `map.json` fields — but the `refill`
  field flags the timing for the render/legend.)*
- **`events.csv`** — "+1 Followers-max" events (EV-D09 / EV-N13 / EV-N14) → **"grow 1 follower (supply →
  board)"**; EV-N09 Trending win → **grow 1**; EV-N15 / EV-N16 bad-review → **"return 1 follower to your
  supply"** (keep the *crowd-drifts-to-a-rival* flavour — vendor allegiance, **not** a meeple transfer to the
  rival); EV-N08 (place 2 on a co-located stall) → **place 2 from your board**; EV-N11 (next Promote +1) →
  **next Promote places +1**; scrub all "Followers-max / dial" wording.

**Not data (separate presentation passes — flag on hand-off, do NOT do here):**
- **`rules-draft.md` §§3–5 rewrite** (`bg-elegance` / `bg-rulebook`): dial → follower pool; grow/place;
  win-keeps / lose-to-own-supply; **slow-refill scarcity (baseline)**; the **baseline DUSK/LAST-TRAIN
  tie-resolver (§2.6)**; the Councillor home-gate; the Globetrotter Travel-cost; FAQ dial questions. **Must
  keep only Travel/Promote as action keywords; two zone-words (supply / your board), "on the stall".**
- **⚠ RULEBOOK-HEADROOM §-NOTE (bg-elegance — for the rulebook pass, NOT now):** scarcity's two new
  *baseline* rules — slow / per-round refill + the now-baseline tie-resolver — are **≈40 words** and
  **exceed the 7-word headroom** (1843/1850). At the rewrite, either **recover ~40 words** elsewhere (the
  meeple swap's deletions — dial, day/night drop asymmetry — are the natural donor) **OR log a conscious cap
  raise 1850 → 1900**. Record the choice in the elegance gauge; do not silently overrun.
- **Board/player-board (`bg-infodesign`):** dial zone → collected-follower pool zone; per-colour supply
  tray; the scarce single-slot region footprints. Touches no values.

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

**Final-lock re-sweep (this pass — LOCKED kit, CD-signed):**
- **`bg-theme` — the #1 consultant item + identity guard.** The Old Councillor's **home-gated favours
  engine** must read as **inbound goodwill** — neighbours look after a beloved lifelong local public servant,
  bringing him the day's best — and **NEVER** string-pulling / patronage / bribery. A favours-politician
  theme next to the game's own **"Bribe"** verb is the single highest sensitivity risk in the roster → this
  goes to the **paid Taiwanese cultural consultant BEFORE art/print** (log as the #1 pre-art item). Also
  guard the **Influencer** as *reach/viral — biggest crowd, fashionably late*, not a slow grinder (§4). Copy
  edits to make (not here): `identity.md`, `names.md`, `characters.csv` blurb — retire clout/string-pulling
  language for the inbound-goodwill voice.
- **`bg-critic` — roster distinctness / no dominant lane:** are the six lanes mechanically distinct (the
  three resource engines especially — home-gated DRAW vs FORAGE vs GLUT, §6.5), and is any lane dominant?
  The three to hunt in the re-sim: the Homebody **banked-board late-battler** (§6.5a, fix g′), the
  Globetrotter **ubiquity** buff (§6.5b, cost now baseline), and the Big Brother **margin under frequent
  fights** (N=0 floor as the cool-down; N=2 degenerate). All wired into §9.
- **`bg-elegance` — the rulebook-headroom flag:** scarcity's two baseline rules (~40 words) exceed the
  7-word headroom → recover ~40 words at the rewrite OR log a conscious 1850→1900 cap raise (§10 note).
