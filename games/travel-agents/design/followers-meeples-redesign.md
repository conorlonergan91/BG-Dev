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

---

# 12. VENDOR ECONOMY REWORK — two coupled cost axes (CD steer, 2026-08-09)

> **Status: SPEC, appended after the LOCKED §§0–11.** A fresh CD steer reworks the vendor economy on
> top of the locked meeple + scarcity model. **This REOPENS the win-a-vendor economy a second time** —
> §§9–10's re-sim scope and data list are extended here (§12.7). Nothing in §§0–11 is deleted; this
> section *amends* three earlier decisions and says so explicitly:
> - **Amends §5 ("no threshold").** §5 dropped the flat vestigial `buzz_cost=2` and locked "pure
>   most-followers-wins, no threshold." The CD now REINTRODUCES a threshold — but a **tier-scaled
>   `min_followers` floor (1/2/3)**, NOT a flat constant. This is not a revival of `buzz_cost`; it is a
>   new, varied *second axis* (§12.2). §5's reserve ("hold a threshold only if the 1-follower sweep is
>   dominant") is now **promoted to baseline**, tier-scaled.
> - **Amends §6 (prestige Bookings).** The cost thresholds there assumed the OLD flat day cost (all
>   cost-1). Day stalls are no longer cost-1, so those targets are retuned (§12.6).
> - **Amends §1.5 / §9 probe #2 (sourcing "invariant").** Multi-ingredient recipes deliberately shift
>   per-category demand and raise aggregate demand ~30%. Sourcing shares are **no longer expected to be
>   invariant** — they should track the NEW demand vector (§12.5). Probe #2's targets are updated.

## 12.0 The two CD steers, folded into one lever

1. **Costs are too flat / boring.** Day was uniformly single-ingredient cost-1. Spread the whole curve
   so ingredient cost is a real decision.
2. **Add a tier-scaled `min_followers` floor** to CLAIM a stall — the plurality leader must ALSO hold at
   least the stall's floor, or nobody claims (stays contested).
3. **(Follow-on steer) No single-ingredient stalls.** Every recipe needs **≥2 ingredients, ideally
   spanning ≥2 of the 6 categories**, with a meaningful share spanning **≥2 regions** — a single-
   ingredient dish gives no reason to spread across the board; a multi-type/multi-region dish is what
   forces the sourcing-travel game.

**Steers 1 and 3 are the SAME lever.** Requiring ≥2 ingredients per recipe is *what* raises and varies
the cost (cost = recipe token count), and choosing ingredient *types* that aren't all local is what
forces cross-region sourcing. So the redesign is a single pass over all 24 recipes, producing two
numbers per card: **(a) `ingredient_cost`** (now 2–5, from the multi-token recipes) and **(b)
`min_followers`** (the tier floor). The floor (steer 2) stacks on top: a marquee now demands **both a
varied ingredient spread AND a real crowd.**

## 12.1 Axis A — the ingredient-cost curve (multi-ingredient, cross-region)

**Design rules applied to every recipe:**
- **≥2 ingredient tokens** (so `ingredient_cost ≥ 2` everywhere — the old cost-1 single-ingredient day
  stall is gone).
- **≥2 distinct categories** wherever the dish plausibly allows (24/24 achieve ≥2 types).
- **Gradient by tier:** day ≈ 2 (a couple of hearty day foods at 3), night mains = 3, apex = 4, top
  apex = 5. Full deck spans **cost 2–5**.
- **Cross-region by construction:** each stall keeps its home-region signature where the real dish has
  it, and picks up cross-region tokens for the second/third type. **20 of 24 recipes now require an
  ingredient not local to the stall's region → they force travel.** The 4 fully-local stalls are simple
  day items (a deliberate handful of no-travel quick grabs).
- **Keyword/taxonomy discipline:** unchanged 6-category taxonomy (Meat 肉 / Tea 茶 / Seafood 海鮮 /
  Pantry 糧 / Sugar 糖 / Veg 菜) and the region-local map (North = Meat+Veg, Central = Tea+Sugar,
  South = Seafood+Sugar, East = Pantry+Veg). Recipes are thematically faithful — **flag `bg-theme` to
  sanity-check the reflavoured recipes** (a few dishes gained an authentic second ingredient).

**Within-tier variety, not just a shifted-flat curve.** Two day foods (S02 Rice Bowl Cake, C02 Misua)
are **cost 3**, the rest of day cost 2 — so day itself spans 2–3, and the deck shows the payoff of the
second axis cleanly: **S02/C02 cost 3 with floor 1** sit right next to the **night mains at cost 3 with
floor 2** — same ingredient cost, different crowd demand. That contrast is exactly "the meaningful
second number" the CD asked for.

## 12.2 Axis B — the `min_followers` floor (tier-scaled)

> **Rule.** To CLAIM a stall you must be the follower leader (strict plurality; **Big Brother 大哥** by
> his margin dial N, §6.7) **AND** have at least the stall's `min_followers` of **your own** followers on
> it. If the plurality leader is below the floor, **nobody claims** — the stall stays contested/empty
> until someone meets it.

**Floor = tier** (the mnemonic: crowd floor = star tier):

| Tier | Stalls | `min_followers` |
|---|---|:--:|
| **1** (all 13 day + N07 night drink) | 14 | **1** |
| **2** (6 night mains) | 6 | **2** |
| **3** (4 night apex) | 4 | **3** |

**Floor range chosen: 1 → 3** (with a held 4th step on the top trophy — §12.7 reserve). Rationale, tuned
against the pool (field `max` **6**, Influencer **8**, start **2**, Travel grows **+1/turn**, slow refill):
- **Floor 1 = a near-no-op that PRESERVES the closed day economy.** Leading a stall already needs ≥1
  follower (1 > 0), so a floor of 1 changes nothing on day stalls — they stay frictionless single-
  follower quick grabs. This is the CD's "cheap day stalls a low floor," and it protects the day
  throughput the V7 sim closed.
- **Floor 2 (night mains) = a third of a 6-pool.** Ties up 2 followers until the contest resolves — a
  real tempo cost, and it lets a 6-pool spread **2+2+2** across three simultaneous night-main fights.
- **Floor 3 (apex) = half a 6-pool.** A serious "big crowd." A 6-pool can only fund **two** apex
  commitments (3+3), so spreading vs concentrating genuinely trades off — the whole point of the floor.
  Reachable (Travel +1/turn builds you there; wins return followers to redeploy) but a heavy commitment.
- **Why not the CD's example ceiling of 4?** With field `max` 6 and three stacking throttles (scarcity +
  floors + higher costs, §12.4), a floor-4 on the single hardest, region-locked apex risks a permanent
  below-floor block that strands its Booking value. Baseline apex floor = **3** (uniform, teachable);
  **E04 floor 3→4 is held as the "crown the top trophy" reserve** (§12.7), to be pulled only if the
  re-sim shows apex fights resolve too cheaply.

The floor is a **per-contest COMMITMENT, not a permanent spend** (see §12.3, interaction 3): meeting it
ties up followers only until you win (→ they come home to your board, reusable) or lose (→ your own
supply, re-grow). Its cost is tempo/opportunity, never attrition.

**Note — this floor is the tier-scaled promotion of §5's reserve.** It directly answers §5's worry: the
1-follower uncontested sweep is now impossible on night/apex (need 2/3), while day (floor 1) is
untouched.

## 12.3 The three interactions the CD flagged — RESOLVED

1. **min_followers × Big Brother 大哥 margin dial (§6.7).** The floor is an **absolute personal minimum**;
   the margin dial governs the **relative** contest. **Big Brother must still MEET the floor** — his edge
   only wins the relative fight with fewer followers than a rival, it never waives the floor. Worked
   cases on an apex (floor 3): rivals A=3, BB=3 → tie, BB wins by margin, **BB has 3 ≥ floor → claims.**
   A=3, BB=2 → A leads and meets floor → **A claims.** A=2, BB=2 → tie, BB would win the margin **but BB=2
   < floor 3 → nobody claims**, stays contested. So the floor can block even the plurality/margin winner —
   exactly the CD's "leader below the floor ⇒ not claimed."
2. **min_followers × tie-block × the endgame tie-resolver (§2.6).** A tie among leaders still blocks; the
   floor adds "a below-floor leader also blocks." At **DUSK / LAST TRAIN**, the resolver force-resolves
   **ties among floor-MEETING leaders** (most followers, then earliest committer). **The floor still
   applies at the resolver:** a stall whose top committer is **below the floor** does NOT get force-
   claimed — it **clears UNCLAIMED** (followers → owners' boards at DUSK / lie unscored at LAST TRAIN),
   like any unclaimed stall. This closes the loop without reopening the deadlock/stranding HOLE (§2.6,
   §1.5): the only new case is "nobody invested enough," which is not a denied prize — it clears clean,
   no follower is stranded (DUSK sends them home to boards, not supply).
3. **min_followers × win-keeps-followers.** The floor is committed *per contest*: you place ≥floor over
   one or more Promotes, **win → your followers return to your board** (kept, redeploy free), **lose →
   your followers to your OWN supply** (re-grow). The floor never permanently drains the pool — it is a
   temporary tie-up, so the pool binds through **tempo** (those followers can't be elsewhere meanwhile),
   which is precisely what makes spreading vs concentrating a live decision.

## 12.4 ⚠ THREE THROTTLES NOW STACK — the load-bearing flag

The CD has now stacked **three** independent brakes on claiming a stall, all pointing the same way:
1. **Scarcity** (§1) — fewer face-up slots + slow per-round refill → fewer stalls available.
2. **Higher/varied ingredient cost** (§12.1) — avg vendor cost rises **2.08 → 2.71** (+30%); every claim
   costs more ingredients, so more sourcing turns per claim.
3. **Follower floors** (§12.2) — night/apex claims now require 2–3 committed followers, not 1.

Individually each is intended. **Together they compound and could over-throttle throughput** — Bookings
(esp. the cost-targeted prestige Bookings, §12.6) becoming hard to finish is the #1 risk of this rework.
The re-sim must measure the **combined** effect and be ready to **loosen the cheapest-to-loosen lever
first** — that is **the scarcity slot counts** (§1.3), which were always the "amplifier," not the load-
bearing lever. Do NOT loosen the floors or costs first (they are the CD's actual asks). Explicit re-sim
guard in §12.7.

## 12.5 Sourcing-coherence check — how demand shifts (state + flag, per the CD)

Cost = recipe token count, so the new recipes change per-category demand. Aggregate rises **50 → 65
(+30%)**; **proportions stay close to the validated old ones** (the multi-ingredient rework scaled the
economy up more than it re-weighted it):

| Category | Old demand (Σ50) | Old share | **New demand (Σ65)** | **New share** | Deck depth | Deck share |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Meat 肉 | 11 | 22% | **14** | **21.5%** | 11 | 17.7% |
| Tea 茶 | 8 | 16% | **10** | **15.4%** | 11 | 17.7% |
| Seafood 海鮮 | 10 | 20% | **11** | **16.9%** | 11 | 17.7% |
| Pantry 糧 | 13 | 26% | **16** | **24.6%** | 11 | 17.7% |
| Sugar 糖 | 4 | 8% | **7** | **10.8%** | 12 | 19.4% |
| Veg 菜 | 4 | 8% | **7** | **10.8%** | 6 | 9.7% |

**Reads:**
- **Proportions hold within a few points** — biggest moves are Seafood −3.1pts and Sugar/Veg +2.8pts;
  Meat/Tea/Pantry within ~1.5pts. So the sourcing character the V7 sim validated is preserved; only the
  *volume* scales up.
- **Pantry stays the tightest category** — 24.6% demand vs 17.7% deck-share. This is the **same risk
  profile as the old game** (pantry was 26% demand vs 17.7% supply and the sim handled it fine, because
  the market decks reshuffle — `supply_min` never hit 0). No new structural break; just watch it under
  the +30% aggregate.
- **Sugar remains over-supplied** (10.8% demand vs 19.4% deck-share) — harmless idle supply, same as
  before, now slightly less idle.

**Deck decision: do NOT pre-change `ingredients.csv`.** Because proportions hold and decks reshuffle, the
existing decks should absorb the higher volume. **Flag the re-sim to VERIFY** (probe #2 retargeted to the
NEW shares above, ±2pt). **Conditional fix, only if the re-sim shows Pantry/Meat starvation under the
+30% load:** swap idle Sugar depth toward Pantry/Meat — e.g. Central/South sugar 12→7 (−5), East pantry
11→14 (+3), North meat 11→13 (+2), keeping deck total ~62. Held, not baked.

## 12.6 Prestige-Booking retune (amends §6)

The §6 prestige targets assumed day = all cost-1. Day is now cost 2–3, so `ingredient_cost` totals are
reached with far fewer claims. Recommended retune (validate in re-sim):

| Booking | §6 target | Why it breaks | **Recommended** |
|---|---|---|---|
| `d_prestige8` (day) | `ingredient_cost_day ≥ 4` | day now cost 2–3 → 2 day claims hit 4 (was ≈4 claims) | **`≥ 7`** (≈3 day claims; day cost-total is now 28) |
| `n_prestige14` (night) | `ingredient_cost_total ≥ 9` | night cost-total barely moved (36→37) | **hold `≥ 9`**; drop to `≥ 8` only if floors throttle night claims |
| `g_prestige12` (night) | `ingredient_cost_total ≥ 7` | as above | **hold `≥ 7`**; drop to `≥ 6` if needed |

This is a recommendation flagged for the re-sim, not a silent change — `bg-developer` applies the day
retune (`≥7`) and the re-sim confirms all three against the new cost economy + the three-throttle stack.

## 12.7 The full 24-vendor table (authoritative spec)

`cost` = `ingredient_cost` (recipe token count). `floor` = `min_followers`. Categories: M=Meat, T=Tea,
S=Seafood, P=Pantry, K=Sugar, V=Veg. **✱ = forces cross-region travel** (needs a non-home-local
category). Home-local: N={M,V}, C={T,K}, S={S,K}, E={P,V}.

| id | Dish (EN) | tier | phase | OLD recipe (cost) | **NEW recipe** | **cost** | **floor** | ✱ cross-region |
|---|---|:--:|:--:|---|---|:--:|:--:|:--:|
| N01 | Pork Bao | 1 | day | meat (1) | **M;P** | 2 | 1 | ✱ (P→E) |
| N02 | Egg Crepe | 1 | day | meat (1) | **M;V** | 2 | 1 | — (local) |
| N03 | Soy Milk | 1 | day | sugar (1) | **P;K** | 2 | 1 | ✱ (P→E, K→C/S) |
| N04 | Pepper Bun | 2 | night | meat;meat;tea (3) | **M;M;T** | 3 | 2 | ✱ (T→C) |
| N05 | Beef Noodle | 2 | night | meat;pantry;veg (3) | **M;P;V** | 3 | 2 | ✱ (P→E) |
| N06 | ★ Big Sausage | 3 | night | meat;meat;meat;seafood (4) | **M;M;S;V** | 4 | 3 | ✱ (S→S) |
| N07 | Bubble Tea | 1 | night | sugar (1) | **T;K** | 2 | 1 | ✱ (T→C) |
| C01 | Ba-wan | 1 | day | tea (1) | **M;T** | 2 | 1 | ✱ (M→N) |
| C02 | Misua | 1 | day | tea (1) | **T;S;P** | 3 | 1 | ✱ (S→S, P→E) |
| C03 | Bubble Tea (orig) | 1 | day | sugar (1) | **T;K** | 2 | 1 | — (local) |
| C04 | Sausage-in-Sausage | 2 | night | tea;tea;pantry (3) | **M;P;T** | 3 | 2 | ✱ (M→N, P→E) |
| C05 | ★ Fengjia Signature | 3 | night | tea;tea;seafood;seafood (4) | **T;S;S;P** | 4 | 3 | ✱ (S→S, P→E) |
| C06 | Wintermelon Tea | 1 | day | veg (1) | **T;K** | 2 | 1 | — (local) |
| S01 | Milkfish Congee | 1 | day | seafood (1) | **S;P** | 2 | 1 | ✱ (P→E) |
| S02 | Rice Bowl Cake | 1 | day | seafood (1) | **S;S;P** | 3 | 1 | ✱ (P→E) |
| S03 | Papaya Milk | 1 | day | sugar (1) | **V;K** | 2 | 1 | ✱ (V→N/E) |
| S04 | Turkey Rice | 2 | night | meat;pantry;veg (3) | **M;P;V** | 3 | 2 | ✱ (M→N, P→E) |
| S05 | Coffin Bread | 2 | night | seafood;seafood;pantry (3) | **S;S;P** | 3 | 2 | ✱ (P→E) |
| S06 | ★ Tan-tsú-mī | 3 | night | seafood;seafood;seafood;pantry (4) | **S;S;M;P** | 4 | 3 | ✱ (M→N, P→E) |
| E01 | Bamboo Rice | 1 | day | pantry;pantry (2) | **P;V** | 2 | 1 | — (local) |
| E02 | Rice Cake | 1 | day | pantry (1) | **P;M** | 2 | 1 | ✱ (M→N) |
| E03 | Mochi | 2 | night | pantry;pantry;tea (3) | **P;K;T** | 3 | 2 | ✱ (T→C, K→C/S) |
| E04 | ★ Stone-Slab BBQ | 3 | night | pantry;pantry;pantry;meat;meat (5) | **P;P;M;M;V** | 5 | 3 | ✱ (M→N) |
| E05 | Roselle Tea | 1 | day | veg (1) | **T;K** | 2 | 1 | ✱ (T→C) |

**Cost distribution:** 2 ×14 · 3 ×6 · 4 ×3 · 5 ×1 → wait, day-3s (C02,S02) + mains-3 (6) = 8 at cost 3;
cost 2 ×12, cost 3 ×8, cost 4 ×3, cost 5 ×1. Range **2–5**, avg **2.71** (was 2.08).
**Floor distribution:** 1 ×14, 2 ×6, 3 ×4.
**The 2-D space (cost, floor):** (2,1) quick grabs · (3,1) pricey solo day (S02, C02) · (2,1) night drink
N07 · (3,2) night mains · (4,3) apex · (5,3) top apex — six profiles, and the (3,1) vs (3,2) pair proves
the two numbers carry independent information.
**Cross-region:** 20/24 force travel; the 4 local stalls (N02, C03, C06, E01) are the deliberate easy
day grabs.

## 12.8 DATA-change list (for `bg-developer` — extends §10)

**`vendors.csv`** (this supersedes the §10 line that kept `ingredient_cost`/`recipe` unchanged):
- **REVISE `recipe` + `ingredient_cost` for all 24 rows** to the "NEW recipe / cost" columns in §12.7.
  (Every day stall changes; several night rows reflavoured for ≥2 types.)
- **ADD a new column `min_followers`** to all 24 rows = the `floor` column in §12.7 (tier 1→1, 2→2, 3→3).
- The §10 drops still stand: **DROP `buzz_cost`** and **DROP `draw`**. `min_followers` is the NEW,
  tier-scaled second axis — it does NOT restore the flat vestigial `buzz_cost`.
- `icon`, `trending`, `tier`, `phase`, `region`, `quantity`, `tags`, `place` unchanged.
- **Flag `bg-theme`** to sanity-check the reflavoured recipes (a few dishes gained an authentic 2nd/3rd
  ingredient — e.g. Misua as oyster-tea-noodle, wintermelon/roselle "teas" carrying a Tea token).

**`bookings.csv`** — apply the §12.6 retune: `d_prestige8` → **`ingredient_cost_day ≥ 7`**; hold
`n_prestige14` (`≥ 9`) and `g_prestige12` (`≥ 7`) pending re-sim.

**`ingredients.csv`** — **NO change now.** Conditional deck-rebalance (§12.5) held for the re-sim.

**`map.json`** — no change from this steer (slots/refill are §1.4).

Run `tools/lint/check_game.py` after (new column + recipe edits). Cost gauge / complexity unaffected by
values.

## 12.9 SIM re-encode additions (the re-encode is IN FLIGHT — extend its scope)

The scarcity+meeple re-encode (§9) must additionally:
- **Add the min-follower GATE to contest resolution:** a stall claims only if the plurality/margin leader
  holds ≥ its `min_followers`; a below-floor leader = **no claim, stays contested**. Apply the floor at
  the endgame resolver too (§12.3 interaction 2): below-floor top crowd → clears **unclaimed**.
- **Re-read `ingredient_cost` from the new recipes** (avg 2.71) and the retargeted prestige Bookings.
- **Retarget probe #2** to the NEW demand shares (§12.5), ±2pt — sourcing shares are **no longer
  invariant**; they should track the new vector. Pantry is the tight category to watch.

## 12.10 RULEBOOK additions (the rewrite is IN FLIGHT — add these)

- Teach the claim rule in one line: **"To claim a stall you must be the follower leader (Big Brother by
  his margin) AND have at least the stall's minimum followers of your own on it — below the floor, no one
  claims; it stays contested."**
- Teach the two card numbers: **ingredient-cost chips** + the **crowd-floor** (min-followers) number, and
  the mnemonic **floor = star tier (1/2/3)**.
- Add the endgame-resolver floor clause (a below-floor tied stall clears unclaimed).
- **Presentation note (NOT design — for `bg-infodesign`):** the vendor card shows ingredient chips + a
  min-follower number/icon, **no prose**.

## 12.11 What the re-sim must NOW ALSO verify (this reopens the economy)

Fold into §9's scoped re-sim (already CD-gated):
- **Cost-curve variety is LIVE:** cost decisions actually bind — players don't grab indiscriminately;
  higher-cost stalls are meaningfully harder to afford, and the (3,1)-vs-(3,2) profiles play differently.
- **min_followers makes the fight BIND without making marquees UNCLAIMABLE:** track apex/night-main CLAIM
  rate (must stay > 0 — marquees still get won), **below-floor block frequency** (transient, not a
  permanent barricade), and **Booking + prestige-Booking completion** (must hold ≥ ~90%).
- **The three-throttle stack (§12.4) does not over-choke throughput:** claims/gm, Last-Train completion,
  turns/player. If it chokes, **loosen the scarcity slot counts first** (§1.3), not floors or costs.
- **Sourcing tracks the NEW demand (§12.5):** shares within ±2pt of the new vector; **Pantry** is the
  starvation watch — if it starves, apply the conditional deck-rebalance (§12.5).
- **The spread/travel game is real:** with 20/24 recipes cross-region, confirm travel/sourcing turns rise
  and single-region hoarding is no longer viable (the CD's core intent).

## 12.12 Handoff / coherence flag (extends §11)

Two mechanics moved this pass: **(1) every vendor is now a multi-ingredient, mostly cross-region dish**
(the signature twist's *spread* engine — sourcing-travel now matters far more), and **(2) claiming gained
a tier-scaled follower FLOOR** (the crowd-fight now has a minimum-crowd gate). Flag the Director to run:
- **`bg-theme`** — do the reflavoured recipes still read as faithful real dishes (the ≥2-type additions),
  and does the fiction explain "a stall won't sell to you until enough of your crowd is there" (the
  floor)? The Taiwan cultural rails are untouched (E04 Stone-Slab BBQ still the #1 consultant item;
  Indigenous dishes E01/E04 unchanged in framing).
- **`bg-elegance`** — the floor adds one printed number per card + one claim clause (~15 words); folds
  into the same rulebook-headroom re-gauge already flagged (§10). The `min_followers` = tier mnemonic
  keeps it cheap.
- **`bg-critic`** — the floor interacts with every character lane (§12.11): Influencer's deep pool meets
  floors easiest (watch hot → reserve `max` 7), Big Eater's follower-sink weakens her at floors (leans on
  floor-1 day), Globetrotter's Travel-cost + floors compound (watch over-nerf), Homebody's banked board
  is worth more when floors demand crowds (reserve g′ more likely), Councillor's ingredient-rush is now
  floor-gated on high tiers (can't buy-and-snipe an apex with 1 follower). All wired into the §9 probes.

---

# 13. DIFFICULTY → REWARD COUPLING — the payoff half (CD steer, 2026-08-09)

> **Status: SPEC + a clean A / B / hybrid RECOMMENDATION for the CD's final call** (scoring architecture
> is the CD's decision). This is the REWARD half of the difficulty added in §12: if hard vendors aren't
> worth more, players grab the easy day stalls and skip the marquees, and the whole §12 difficulty becomes
> pure friction. The reward must scale with the difficulty.

## 13.0 The critical finding — Route A is ALREADY BUILT and validated

Reading `bookings.csv`: the scoring is **tickets-only** (score ONLY from completed Bookings 開團; the sim
validated this — `ignore_obj` winrate 1–5%, DEAD), **and the Booking deck already channels difficulty →
reward through dedicated cards.** The slope exists today:

| Booking type | Examples | Value | What difficulty it rewards |
|---|---|:--:|---|
| Cheap / pair / mix | `d_cheap2`, `d_pairNC`, `d_mix1`, `d_deep2` | **3** | easy day grabs |
| Coverage / collection / single-region | `d_travel3`, `d_collect4`, `d_north2` | **4–5** | breadth |
| **Expensive-cost** | `n_expensive1` (cost≥3), `n_expensive2` (2×cost≥3) | **4 / 6** | pricey stalls |
| **Apex** | `n_star1` (win a ★) | **5** | the marquee |
| **Contested (the signature twist!)** | `d_contest1` (1 contested win), `n_contest2` (2) | **4 / 5** | winning the crowd-fight |
| **Cross-region** | `n_cross1`, `n_cross2` | **4 / 6** | the spread |
| **Cost-total prestige** | `d_prestige8`, `n_prestige14`, `g_prestige12` | **4 / 6 / 6** | leaning into pricey night names |
| Big collection / all-regions | `n_collect6` (6), `n_all4` (4 regions) | **7** | grand tour |

**So the marquee is ALREADY worth fighting for — via these Bookings.** The mechanism the CD floated as
"Route A" is the existing, sim-validated architecture. There are contested-win Bookings that reward the
signature twist *directly*. The residual gaps are only two: **(i) the value SLOPE is a bit flat** (an apex
Booking at 5 ≈ a 4-cheap-grab collection at 5, even though winning an apex is far harder now), and **(ii)
CONTINGENCY** — whether a marquee is "worth it" this game depends on your Booking draw (bounded, because
the deck is dense with difficulty-Bookings and players hold several).

## 13.1 ⚠ Coherence ripple — the new cost curve mis-calibrates the cost-referencing Bookings

Independent of the A/B/hybrid choice, §12's cost change **breaks the calibration of every Booking that
references `ingredient_cost`** (they were written for the old flat all-cost-1 day tier). Must retune:

| Booking | Target | Old behaviour | New behaviour under §12 | Fix |
|---|---|---|---|---|
| `d_cheap2` / `d_cheap3` | `cheap_vendors` = cost ≤2 | caught cost-1 day stalls | now catches the **12 cost-2 stalls** (not the cost-3 day S02/C02) | keep ≤2 (still "the cheap grabs"); note semantics shifted |
| `n_expensive1` | cost ≥3 | night mains + apex only (10) | now also catches **day S02/C02** (cost 3) | **raise to cost ≥4** to stay "marquee" (else 2 day stalls read as splurges) |
| `n_expensive2` | 2× cost ≥3 | as above | as above | **raise to cost ≥4** likewise |
| `d_prestige8` | `ingredient_cost_day ≥4` | ≈4 day claims | ≈2 day claims (day now 2–3) | **≥7** (§12.6) |
| `n_prestige14` / `g_prestige12` | ≥9 / ≥7 | — | night cost-total barely moved | hold (§12.6) |

This retune is mandatory regardless of route — flag to `bg-developer` + re-sim.

## 13.2 The three routes — crisp trade-off for the CD

**Route A — Booking-payout scaling (RECOMMENDED).** Keep tickets-only. Do two things: (1) the §13.1
retune, and (2) **widen the value slope** so the hard Bookings clearly out-score the easy ones now that
the difficulty rose — modest bumps, nothing new:
- `n_star1` (apex) **5 → 6**
- `n_contest2` (2 contested wins) **5 → 6**
- `n_expensive2` (2× cost≥4) **6 → 7**
- keep easy Bookings (pairs/mix/cheap) at **3–4**.
- *Optional density lever (hold):* add one `apex_wins≥2` Booking (value 7) if the re-sim shows a single
  apex incentive isn't enough to make the fight reliably fire.
- **Pros:** zero scoring-architecture change; the validated single axis is preserved; **`ignore_obj`
  stays dead by construction** (scoring is still 100% Bookings — a grab-only player scores 0); the
  contested/apex/expensive Bookings already reward the exact §12 difficulty; **no added complexity**
  (critical against the tight 1850-word budget). **Cons:** reward stays *indirect* — a marquee is worth
  it only if you hold a Booking that wants it (bounded by deck density, but real).

**Route B — full vendor points (ADVISE AGAINST).** Vendors score directly, scaled by difficulty (e.g. VP
= `ingredient_cost`, 2–5 each). **Cons dominate:** a player claiming 6–8 stalls banks 12–30 VP, *rivalling*
the Booking axis → revives the two-axis dilution the CD deliberately dropped, and directly threatens the
validated `ignore_obj`-dead result (grab-spam could win). It also adds a full second scoring pass. The
CD's hypothesis (vendor points failed only because vendors were flat) is plausible, but the fix for
"marquees aren't worth it" does **not** require making vendor-collection a co-equal win condition — that
is a bigger, riskier redesign than the problem needs. Reconsider only if the CD wants to *re-centre* the
game on vendor-collection scoring.

**Route H — hybrid: Route A backbone + a small capped prestige token (RECOMMENDED FALLBACK).** Keep
Bookings dominant (Route A), AND add a **small, tier-scaled, capped** direct vendor bonus so the marquee
carries intrinsic stakes *every* game (kills Route A's contingency gap and makes the signature apex-fight
fire unconditionally):

| Tier | Direct prestige points (`vp`) |
|---|:--:|
| 1 (day + N07) | **0** — the easy sink stays "grab for Bookings/ingredients only" |
| 2 (night main) | **1** |
| 3 (apex) | **2** |
| (E04 top apex) | **3** (optional) |

- **Difficulty → payoff mapping** (difficulty := `ingredient_cost + min_followers`): day (3) → 0 VP;
  night main (5) → 1 VP; apex (7) → 2 VP; top apex (8) → 3 VP — plus each still feeds the Bookings. So
  committing a wide spread + a 3-crowd to a marquee pays **2–3 intrinsic points AND** unlocks the value-6
  prestige/apex Bookings, versus 0 intrinsic for a cheap grab. The curve ties together.
- **Dominance guard (why `ignore_obj` stays dead):** realistic per-player VP under scarcity ≈ 1 apex + 2
  mains ≈ **4** (ceiling ~7 for an all-marquee hoarder, near-impossible under §12's three throttles),
  against a competitive Booking score of **~15–20** → VP is **~20–25%** of the total, Bookings
  clearly dominant. A grab-only player nets ~5–7 VP + 0 Bookings → loses to any ~15+ Booking score.
  **Bookings remain the win condition; VP is spice, not a second meal.**
- **Cost:** one printed number on night/apex cards + one end-scoring line. Small, but non-zero against the
  budget — hence *fallback*, not baseline.

## 13.3 RECOMMENDATION

**Ship Route A now; hold Route H as a re-sim-gated fallback.** Reasoning: the difficulty→reward mechanism
already exists and is validated, the only real work is the §13.1 retune (mandatory anyway) plus a modest
slope-widen, and it keeps the single scoring axis + the dead `ignore_obj` line the sim proved healthy —
at **zero architecture and near-zero complexity cost**. **Trigger for Route H:** if the re-sim (which is
already measuring apex/contested contested-rate) shows that **even with Route A's widened slope, the apex/
marquee fight does NOT fire** (players still skip marquees because no Booking happened to want them that
game) — then add the capped tier-scaled `vp` (H) to give the marquee unconditional stakes. Route B is not
recommended.

**Clean decision for the CD:**
- **A** (recommended): retune + slope-widen; no vendor points. Safest, simplest, preserves the validated
  architecture.
- **H** (recommended fallback): A + a capped `vp` {0/1/2/3} for reliable marquee stakes; small complexity
  add; needs the dominance guard confirmed in sim.
- **B** (advise against): full vendor scoring; reopens the two-axis dilution the CD already dropped.

## 13.4 Data / sim / rulebook changes each route implies

**Route A (`bookings.csv` only):**
- Retune (§13.1): `n_expensive1`/`n_expensive2` cost≥3 → **≥4**; `d_prestige8` → **≥7**; note `d_cheap*`
  semantics shift (no value change).
- Slope-widen: `n_star1` 5→**6**, `n_contest2` 5→**6**, `n_expensive2` 6→**7**.
- *(optional)* add one `apex_wins>=2` Booking (value 7).
- **Sim:** re-read Booking values/targets; confirm `ignore_obj` stays dead and **no single Booking becomes
  a forced must-chase**; confirm apex/contested claim-rate rises (the §12.11 marquee probe).
- **Rulebook:** no scoring rule change; just the retuned target text on the affected Booking cards.

**Route H (adds to A):**
- `vendors.csv`: add column **`vp`** = {tier1 0, tier2 1, tier3 2, E04 3}.
- Rulebook/player-aid: add an end-scoring line "score your Bookings, then +VP printed on each won night/
  apex stall"; player aid shows the VP pip.
- **Sim:** add VP to final score; **make-or-break guard — `ignore_obj` winrate must stay <~10% AND
  Bookings ≥ ~70% of the winning score** (else VP is over-weighted → drop tier values). Report VP-share of
  winning score per count.

**Route B (not recommended):** `vendors.csv` `vp` = `ingredient_cost`; full end-scoring; **sim must
re-prove the entire `ignore_obj`-dead result from scratch** (highest risk).

## 13.5 Handoff note
The scoring architecture is the CD's call — I've made it a clean A/H/B decision. Whichever route, the
§13.1 cost-Booking retune is **mandatory** (the §12 cost curve broke those targets). Flag `bg-elegance`
(Route H adds a scoring line — budget), `bg-critic` (no forced-chase Booking; VP dominance guard under H),
and `bg-theme` (VP reads as "winning the famous stall is its own prestige 人氣" — coherent with the twist).

---

# 14. VP SCORING — Route B, full vendor points (CD-LOCKED, 2026-08-09)

> **Status: SPEC. The CD LOCKED Route B (full vendor points), overriding §13's Route-A recommendation.**
> Every vendor scores VP. The two-axis dilution §13.2 warned about is mitigated **by TUNING, not by
> architecture** — the two levers are (a) a VENDOR VP curve whose top is deliberately held low (ceiling 6)
> and whose totals are structurally bounded by the §12 three-throttle scarcity, and (b) a BOOKING value
> curve widened so the tour ceiling clears the vendor ceiling and tour-per-game totals dominate. This
> section supersedes §13.4's Route-B sketch (`vp = ingredient_cost`): that ignored the crowd-floor effort
> axis and compressed VP to 2–5; the locked curve below uses **cost + floor** so reward tracks EFFORT and
> the cheapest day grabs sit exactly at the 1-VP floor.

## 14.1 The generating rules (two clean lines)

1. **Vendor VP = `ingredient_cost` + `min_followers` − 2.** Range **1–6**.
   - *Why this exact form:* the CD's difficulty = f(cost + floor + tier). But **floor = tier by
     construction** (§12.2: tier 1→floor 1, 2→2, 3→3), so cost + floor already carries the tier signal;
     adding tier as a third term would double-count it and steepen the apex to 8, pushing vendor VP into
     Booking territory and **worsening the dilution the CD wants tuned away.** I keep the flatter
     cost+floor curve and shift by −2 so the cheapest grab lands on **1** (the CD's "cheap day stalls
     score LOW VP" — the floor) and the top trophy on **6**.
   - *The two vendor numbers carry independent VP info:* a (cost 3, floor 1) day stall = **2 VP**; a
     (cost 3, floor 2) night main = **3 VP** — same ingredient cost, different crowd effort, different
     reward. That is the §12.1 "(3,1) vs (3,2)" contrast paying out on the scoreboard.
2. **Booking value = 2 × (old value) − 3.** Maps the validated slope 3→3, 4→5, 5→7, 6→9, 7→11.
   - *Why:* preserves the existing, sim-validated *relative* difficulty→reward ordering (§13.0) and simply
     **doubles the spread**, anchored at the easy floor **3** (so it OVERLAPS the vendor scale) with the
     ceiling lifted to **11** (clear of the vendor ceiling 6). This is the "tours score a LOT higher"
     tuning — no new Booking types, no architecture change.

## 14.2 The 24-vendor VP table (authoritative)

`cost` = `ingredient_cost` (§12.7). `floor` = `min_followers` (§12.2). `vp` = cost + floor − 2.

| id | Dish (EN) | tier | phase | cost | floor | **vp** |
|---|---|:--:|:--:|:--:|:--:|:--:|
| N01 | Pork Bao | 1 | day | 2 | 1 | **1** |
| N02 | Egg Crepe | 1 | day | 2 | 1 | **1** |
| N03 | Soy Milk | 1 | day | 2 | 1 | **1** |
| N04 | Pepper Bun | 2 | night | 3 | 2 | **3** |
| N05 | Beef Noodle | 2 | night | 3 | 2 | **3** |
| N06 | ★ Big Sausage | 3 | night | 4 | 3 | **5** |
| N07 | Bubble Tea | 1 | night | 2 | 1 | **1** |
| C01 | Ba-wan | 1 | day | 2 | 1 | **1** |
| C02 | Misua | 1 | day | 3 | 1 | **2** |
| C03 | Bubble Tea (orig) | 1 | day | 2 | 1 | **1** |
| C04 | Sausage-in-Sausage | 2 | night | 3 | 2 | **3** |
| C05 | ★ Fengjia Signature | 3 | night | 4 | 3 | **5** |
| C06 | Wintermelon Tea | 1 | day | 2 | 1 | **1** |
| S01 | Milkfish Congee | 1 | day | 2 | 1 | **1** |
| S02 | Rice Bowl Cake | 1 | day | 3 | 1 | **2** |
| S03 | Papaya Milk | 1 | day | 2 | 1 | **1** |
| S04 | Turkey Rice | 2 | night | 3 | 2 | **3** |
| S05 | Coffin Bread | 2 | night | 3 | 2 | **3** |
| S06 | ★ Tan-tsú-mī | 3 | night | 4 | 3 | **5** |
| E01 | Bamboo Rice | 1 | day | 2 | 1 | **1** |
| E02 | Rice Cake | 1 | day | 2 | 1 | **1** |
| E03 | Mochi | 2 | night | 3 | 2 | **3** |
| E04 | ★ Stone-Slab BBQ | 3 | night | 5 | 3 | **6** |
| E05 | Roselle Tea | 1 | day | 2 | 1 | **1** |

**VP distribution:** 1 VP ×12 (all cost-2 tier-1 — the cheap grabs, at the floor) · 2 VP ×2 (C02, S02, the
pricey day pair) · 3 VP ×6 (night mains) · 5 VP ×3 (apex) · 6 VP ×1 (E04 top apex).
**Total VP on the whole board if every stall were claimed = 55.** No player claims all 24 — this cap is
load-bearing for the dominance argument (§14.4).

## 14.3 The retuned Booking VP table (authoritative)

Rule: new = 2×old − 3. The **target retunes** from §12.6 / §13.1 (mandatory regardless of route) are folded
in here (marked †). Boundary cards carry no value.

| id | Booking (EN) | phase | old | **new** | target (if changed) |
|---|---|:--:|:--:|:--:|---|
| d_cheap2 | Budget Bites | day | 3 | **3** | — |
| d_east1 | Taroko Day Trip | day | 3 | **3** | — |
| d_deep2 | Become a Regular | day | 3 | **3** | — |
| d_pairNC | Taipei–Taichung Line | day | 3 | **3** | — |
| d_pairSE | South-Link Coast Run | day | 3 | **3** | — |
| d_drinks2 | Hand-Shaken Run | day | 3 | **3** | — |
| d_mix1 | A Bite & a Sip | day | 3 | **3** | — |
| d_daymix | The Breakfast Set | day | 3 | **3** | — |
| d_breakfast3 | Morning Market Breakfast | day | 4 | **5** | — |
| d_food3 | Dragon-Boat Food Run | day | 4 | **5** | — |
| d_cheap3 | Coin-Snack Tour | day | 4 | **5** | keep cost ≤2 (semantics shift, §13.1) |
| d_north2 | Concert Hall & Dadaocheng | day | 4 | **5** | — |
| d_south2 | Tainan Old-Capital Walk | day | 4 | **5** | — |
| d_central2 | Taichung City & Tea | day | 4 | **5** | — |
| d_prestige8 | Check-in Trail | day | 4 | **5** | † `ingredient_cost_day >= 7` |
| d_contest1 | Out-Hype the Rival | day | 4 | **5** | — |
| d_travel3 | HSR Three-City Hop | day | 5 | **7** | — |
| d_collect4 | Full-Day Itinerary | day | 5 | **7** | — |
| d_early3 | Beat the Crowds | day | 5 | **7** | — |
| g_travel3d | Round-Island Rail | day | 5 | **7** | — |
| n_surfturf | Surf & Turf | night | 4 | **5** | — |
| n_eastnorth | Taroko–Taipei | night | 4 | **5** | — |
| n_censouth | Taichung–Kaohsiung | night | 4 | **5** | — |
| n_cross1 | Border Dish | night | 4 | **5** | — |
| n_drinks3 | One More Round | night | 4 | **5** | — |
| n_expensive1 | Marquee Splurge | night | 4 | **5** | † cost `>= 4` (was ≥3, §13.1) |
| g_cross1 | Fusion Plate | night | 4 | **5** | — |
| n_nmfood2 | Neon Bites | night | 5 | **7** | — |
| n_four | Four-Stop Night Run | night | 5 | **7** | — |
| n_star1 | Chasing a Star | night | 5 | **7** | — |
| n_east2 | Hualien–Taitung Line | night | 5 | **7** | — |
| n_contest2 | Queue-for-it | night | 5 | **7** | — |
| n_final2 | Closing-Time Sprint | night | 5 | **7** | — |
| g_travel3n | Lantern-Festival Circuit | night | 5 | **7** | — |
| g_collect5 | New-Year Market Haul | night | 5 | **7** | — |
| n_nightfood3 | Mid-Autumn BBQ | night | 6 | **9** | — |
| n_allfood5 | Big Eater's Feast | night | 6 | **9** | — |
| n_expensive2 | Two-Marquee Feast | night | 6 | **9** | † 2× cost `>= 4` (was ≥3, §13.1) |
| n_prestige14 | Top of the Charts | night | 6 | **9** | hold `>= 9` (§12.6) |
| n_deep3 | True Local | night | 6 | **9** | — |
| n_cross2 | Two Borders | night | 6 | **9** | — |
| n_allvenue | Dawn-to-Dusk Full Day | night | 6 | **9** | — |
| g_prestige12 | Money No Object | night | 6 | **9** | hold `>= 7` (§12.6) |
| n_collect6 | The Grand Tour | night | 7 | **11** | — |
| n_all4 | Round-Taiwan · Route No.1 | night | 7 | **11** | — |

**Booking value distribution:** 3 ×8 · 5 ×13 · 7 ×14 · 9 ×8 · 11 ×2.

## 14.4 The effort→VP curve, and the OVERLAP (CD requirement)

Both tracks reward **effort**, on one shared VP scale, so the tracks OVERLAP — and the tour ceiling clears
the vendor ceiling both per-item and per-game.

| Effort band | Vendor (vp) | Tour / Booking (value) |
|---|:--:|:--:|
| easiest | cheap day grab = **1** | easy pair / mix / cheap-2 = **3** |
| low | pricey day (C02/S02) = **2** | 3-food / single-region-2 / expensive-1 = **5** |
| mid | night main = **3** | collection-4 / apex-Booking / contested-2 = **7** |
| high | apex = **5** | cross-2 / 2-marquee / prestige / depth-3 = **9** |
| highest | top apex E04 = **6** | grand tour / all-4-regions = **11** |

- **Overlap is real:** vendor VP spans **1–6**, Booking VP spans **3–11**; the shared band is **3–6**. An
  **easy tour (3) scores LOWER than a premium vendor (apex 5, top apex 6)** — exactly the CD's ask. A
  mid tour (5) ties an apex vendor (5). Effort, not track, sets the number in the overlap.
- **Ceilings separate:** the single best vendor is **6**; the single best tour is **11** — a **+5 per-item**
  gap at the top. And because a player completes *several* tours, the per-game gap is far larger (§14.5).

## 14.5 ★ THE MAKE-OR-BREAK ARGUMENT — vendor-only LOSES, tours DOMINATE

This is the guard `bg-design` flagged for Route B. The claim: **a vendor-only strategy is strictly
dominated** — it cannot win. The argument is numeric and rests on three structural facts.

**Balance assumptions (state them; the sim must verify — §14.6):**
- ~**28 turns/player** (mid of the §9 target 26–32), **one action/turn**.
- Under the §12.4 three-throttle stack (scarcity slots + higher costs + follower floors), a claim costs
  several actions (source 2–5 ingredients + Promote to floor + Travel + Bribe). **Realistic total claims/
  player/game ≈ 6–9.** Anchor: the game's OWN collection Bookings treat 4–6 claims as a full-game haul —
  `n_collect6` "The Grand Tour" = **6 vendors**; `g_collect5` = 5; `d_collect4`/`n_four` = 4.
- **High-VP stalls are scarce board-wide:** exactly **4 apex** (N06/C05/S06/E04, one per region,
  region-locked, single-slot, floor 3, most-contested) and **6 night mains** (3 VP). Realistically **1–2
  apex and 2–3 mains per player** across a whole game.

**Step 1 — the vendor-only CEILING is ~22 VP.** A vendor-only hoarder, freed of all Booking overhead,
pushes claims to ~9–10 and skews premium. Best realistic hoard:

| Claim | count | vp each | subtotal |
|---|:--:|:--:|:--:|
| apex / top apex | 1 | 5–6 | 5–6 |
| night mains | 3 | 3 | 9 |
| pricey day (C02/S02) | 2 | 2 | 4 |
| cheap day | 4 | 1 | 4 |
| **total (~10 claims)** | | | **~22** |

A *near-impossible* extreme (2 apex + 3 mains + 5 cheap, ~12 claims — unreachable under single-slot
scarcity) tops out **~27–29**. Call the vendor-only ceiling **~22, hard cap ~29.**

**Step 2 — the tour-focused WINNER is ~50+ VP.** A tour player claims **the same kind of premium stalls**
(they need apex/mains/cross to complete the high Bookings) — so those claims score their vendor VP **too**
— and then banks the Booking values on top:

| Source | detail | VP |
|---|---|:--:|
| vendor VP | 1 apex(5) + 2 mains(6) + 1 pricey-day(2) + 3 cheap(3), ~7 claims | **~16** |
| completed tours | e.g. n_star1(7)+n_contest2(7)+n_cross2(9)+d_collect4(7)+n_collect6(11) — claims SHARED | **~41** |
| **total** | | **~57** |

A *modest* tour winner (3 Bookings 5+7+7 = 19, + ~14 vendor) still scores **~33.**

**Step 3 — vendor-only is DOMINATED.** Line up the numbers:
- Vendor-only ceiling **~22** (hard cap ~29) **< even a modest tour score ~33 < a strong tour score ~57.**
- **Vendor share of a winning score ≈ 16 / 57 ≈ 28%** — vendors are a real, full-scoring **third** of your
  points (the CD's "full points"), but Bookings are the clear **majority** and the win engine.
- The clincher is structural, not just arithmetic: **every premium vendor a tour player claims ALSO scores
  its vendor VP AND completes a value-7-to-11 Booking.** There is no claim the vendor-only player makes
  that a tour player can't also make while additionally banking a tour. Vendor-only forgoes the larger
  axis for claims it is already making → strictly dominated. Ignoring Bookings stays **non-winning.**

**Why Route B's dilution is neutralised (the two tuning levers):**
1. **Vendor VP is capped low and structurally bounded.** Ceiling 6/item; the high-VP stalls are physically
   scarce (4 apex, 6 mains) and the three throttles cap claims at ~6–9 → a vendor total can't realistically
   clear ~22.
2. **Booking scale widened to 3–11.** The tour ceiling (11) clears the vendor ceiling (6) per-item, and
   several completions put the tour-per-game total (~35–45 from Bookings alone) far above the vendor
   total. `ignore_obj` stays dead by the same logic §13.0 validated, now with vendors merely *adding* a
   minority.

## 14.6 What breaks the argument — the SIM tripwires (tuning knobs, spec-only)

The argument rests on two assumptions the sim must confirm; if either fails, tune (do NOT touch
architecture):
- **IF realistic claims/player ≫ 9, or a single player routinely lands 3+ apexes** → the vendor-only
  ceiling rises. **Tuning fix, in order:** (a) compress the vendor top — change the rule to `min(cost +
  floor − 2, 4)` or `cost + floor − 3` (apex→4, top→5); then (b) widen Bookings further (e.g. 2×old − 2).
- **IF vendor VP share of the winning score creeps above ~40%** (vendors rivalling tours) → same fix.
- **Target band:** vendor-only winrate **< ~10%** (ideally ~0); vendor-VP share of winning score
  **~25–35%** (hard ceiling ~40%); Booking VP **≥ ~60%** of the winning score.

## 14.7 DATA change list (for `bg-developer` — extends §12.8)

**`vendors.csv`** — **ADD a new column `vp`**, 24 values per §14.2 (generating rule `vp = ingredient_cost
+ min_followers − 2`). This *supersedes* §13.4's Route-B sketch (`vp = ingredient_cost`). No other vendor
field changes (recipe/cost/floor already set by §12.8).

**`bookings.csv`** — **RETUNE `value` on all 45 Booking rows** per §14.3 (rule new = 2×old − 3), folding in
the mandatory target changes: `d_prestige8` → `ingredient_cost_day >= 7` (value 5); `n_expensive1` → cost
`>= 4` (value 5); `n_expensive2` → 2× cost `>= 4` (value 9); `n_prestige14` hold `>= 9` (value 9);
`g_prestige12` hold `>= 7` (value 9); `d_cheap2`/`d_cheap3` keep `<= 2` target (values 3 / 5). Boundary cards
unchanged. Run `tools/lint/check_game.py` after (new column + value edits); cost/complexity gauges
unaffected by these values.

## 14.8 FOLLOW-UP FLAGS

**SIM (`bg-playtest`) — the re-encode must now score BOTH tracks.** The §9/§12.9 re-encode already scores
Bookings; **ADD:** (1) sum vendor `vp` into each player's final score; (2) the **"vendor-only loses / tours
dominate" probe** — a bot that ignores Bookings and hoards stalls; report its winrate (target < ~10%),
plus the two assumption-checks that back §14.5: **realistic claims/player** and **apex-claims/player**, and
**vendor-VP share of the winning score** (target ~25–35%, hard ceiling ~40%). Wire the §14.6 tuning fixes
to those tripwires. *(Note: this is an ADDITION to the in-flight §12.9 re-encode, not a new run.)*

**RULEBOOK (`bg-rulebook` / `bg-elegance`) — scoring section.** Teach in two lines: *"At game end you score
**two ways**: the VP printed on **every stall you won**, plus the value of **every tour (Booking) you
completed**. Completed tours are worth far more — they are your main path to victory; won stalls are a
steady bonus on top."* Presentation note for `bg-infodesign`: the vendor card now shows a **third number,
the VP** (alongside ingredient chips + the crowd-floor) — the player aid needs a VP pip. Folds into the
§10 rulebook-headroom re-gauge (the scoring line is ~30 words — flag `bg-elegance`).

## 14.9 Coherence flag (extends §11 / §12.12)
One mechanic moved: **scoring is now two-track — every vendor scores VP, tours score higher.** Flag the
Director to run **`bg-theme`** (VP reads as "winning a famous stall is its own 人氣 prestige" — coherent
with the crowd-fight twist; the apex trophies now pay prestige directly) and **`bg-elegance`** (a third
printed number on vendor cards + a two-line scoring rule — confirm within the complexity budget; it is the
cost the CD accepted to lock Route B).
