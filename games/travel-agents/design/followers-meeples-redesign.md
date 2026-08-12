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
— add: **tier-3 apex stalls (N05 牛肉麵, C05 逢甲名物, S06 擔仔麵, E04 石板烤肉) do not refill at all
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

## 5. Vendor cost: ingredients only — and the reserved claim-floor was ADOPTED

> **Currency note (2026-08-11):** the "no threshold" conclusion below was **superseded**. The reserve at the
> foot of this section — a minimum-N-to-claim threshold — was subsequently adopted: V7-M uses a tier-scaled
> **`min_followers` crowd-floor (1/2/3)** to claim a stall (canon: `components/vendors.csv` + the sim §12.2 +
> `game-bible.md`; `vp = cost + floor − 2`). The `buzz_cost`-drop below still holds; read the "pure plurality,
> no floor" wording as the original rationale, not the current rule.

### 5.0 (original rationale, kept as history) — pure most-followers-wins

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
| **d** | **Non-refilling apex marquees** (§1.6) | Tier-3 apex stalls (N05/C05/S06/E04) never refill once claimed | Overall contested_frac rises but the *apex* contested rate stays flat AND the CD wants the famous-stall brawl sharpened. |
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
| N05 | ★ Beef Noodle | 3 | night | meat;pantry;veg (3) | **M;P;V;V** | 4 | 3 | ✱ (P→E) |
| N06 | Big Sausage | 2 | night | meat;meat;meat;seafood (4) | **M;M;S** | 3 | 2 | ✱ (S→S) |
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
| N05 | ★ Beef Noodle | 3 | night | 4 | 3 | **5** |
| N06 | Big Sausage | 2 | night | 3 | 2 | **3** |
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
- **High-VP stalls are scarce board-wide:** exactly **4 apex** (N05/C05/S06/E04, one per region,
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

---

# 18. VISIT-SOURCING A/B — the keep-2 non-choice (SPEC-ONLY; CD to A/B in playtest)

> **Status: SPEC-ONLY — no data/rules/sim touched.** This section designs BOTH of the CD's candidate fixes
> for the Visit keep-choice, threads the ripples (Option A → the §16 discard feeder; Option B → the §12
> spread-forcing + the §12.5 sourcing balance), wires them as a **switchable playtest lever** (`VISIT_MODE`
> + a variety parameter) so the re-sim and the human table can compare head-to-head, and recommends one on
> design coherence. The re-sim/rulebook folds here are ADDITIONS to the in-flight §9/§12.9/§16.8 scope.

## 18.1 The diagnosis — CONFIRMED, with the region-by-region nuance

The CD's read is right: after §12 collapsed each region to **≈ one signature type + one thin common**, the
"flip 3, keep 2" choice is shallow-to-absent. Here is the actual per-region-phase deck composition (from
`ingredients.csv`, ingredient cards only — events thin it further, see below):

| Region-phase | Signature (depth) | Common (depth) | Deck (ingredients) | Signature share |
|---|---|---|:--:|:--:|
| North day | Meat 6 | Veg 2 | 8 | **75%** |
| North night | Meat 5 | Veg 1 | 6 | **83%** |
| Central day | Tea 6 | Sugar 3 | 9 | 67% |
| Central night | Tea 5 | Sugar 3 | 8 | 63% |
| South day | Seafood 6 | Sugar 3 | 9 | 67% |
| South night | Seafood 5 | Sugar 3 | 8 | 63% |
| East day | Pantry 6 | Veg 2 | 8 | **75%** |
| East night | Pantry 5 | Veg 1 | 6 | **83%** |

**P(a flip-3 shows >1 ingredient TYPE), ignoring events** (i.e. shows the common at all, so keep-2 is even a
nominal choice):

| Region-phase | P(mixed flip) | P(all one type = pure non-choice) |
|---|:--:|:--:|
| North day (6M,2V) | 0.64 | 0.36 |
| North night (5M,1V) | 0.50 | 0.50 |
| Central / South day (6·,3K) | 0.75 | 0.25 |
| Central / South night (5·,3K) | 0.80 | 0.20 |
| East day (6P,2V) | 0.64 | 0.36 |
| East night (5P,1V) | 0.50 | 0.50 |

**Reads (be precise — the diagnosis is *shallow-choice*, not always *no-choice*):**
- **The choice, when it exists, is signature-vs-thin-common — a near-forced keep of the signature.** You
  Visit a region *for its signature* (the mono-region redesign is why), and the common is the two
  lowest-demand/lowest-utility categories — **Veg 10.8%** (N/E) and **Sugar 10.8%, over-supplied** (C/S,
  §12.5). Keeping signature over common is right almost every time, so even a "mixed" flip is a rubber-stamp,
  not a decision.
- **North and East are the near-mono decks (75–83% signature; thin Veg common)** — keep-2 there is a
  non-choice ~half the time and a rubber-stamp the rest. **Central and South have the only real texture**
  (deeper Sugar common) — but it's signature-vs-idle-Sugar, still a weak pick.
- **Events make it worse than the table shows.** Each market deck also carries events; a flip-3 with 1–2
  events leaves you **1–2 ingredients**, so keep-2 collapses to "keep whatever you drew" — no discard
  decision at all. So the *effective* live-choice rate on a Visit is materially below the ingredient-only
  P(mixed) above.
- **Verdict:** keep-2 was designed for the OLD multi-type regions; §12 removed the variety it fed on. The CD
  is right that it is now largely a non-choice. The re-sim should confirm the effective live-choice rate
  (metric M1, §18.5) reads LOW under the current rule (Cell 2 control) — that is the number both fixes move.

**A finding the CD should hold onto:** keep-2 was doing **double duty** — a keep-*choice* AND the **primary
discard feeder** (§16.2 feeder 1, "the highest-volume feeder"). The choice is what's broken; the feeder is
load-bearing for the reshuffle loop. Any fix that removes keep-2 (Option A) removes *both* — hence the §16
ripple below is real and must be threaded, not hand-waved.

## 18.2 Option A — straight draw (drop the keep-choice)

> **Rule (A).** **VISIT the market** *(where you stand)*: **draw the top 2 ingredients** of this region's
> current-phase deck straight into your Larder. Any **event** you turn up while drawing **fires at once**
> (per §7) and is discarded — it does **not** count toward the 2; keep drawing until you hold 2 ingredients
> (or the deck + its discard are exhausted). No flip-3, no keep-choice, no passed-over card.
> Character deltas unchanged in spirit: **Big Eater 大胃王** draws to **3** (may grab a greedy 4th → return
> 1 follower to supply; hazards fire twice); **Homebody 媽寶** draws **1** on a Visit (his sourcing lane is
> Travel-forage, §6.5).

- **N = 2** (matches the current keep-2 target, so the sourcing *rate* the sim closed is preserved — you end
  a Visit with 2 ingredients either way). Blind draw (you don't pre-see the 3) **keeps the push-your-luck
  spine** — you dig through whatever events sit on top, exactly the "more events = more swing" texture the
  Visit was praised for — while honestly admitting there is no *keep* decision to make.
- **Where the decision goes:** onto the **map**. Because a region gives you its signature, *variety* is
  bought by **travelling** — which is precisely §12's cross-region intent (20/24 recipes force travel). A
  relocates the Visit's dead micro-choice to a live macro-choice (which region next), rather than faking an
  in-region choice the deck can't support.

### 18.2a Ripple to §16 — A removes the biggest discard feeder (the real cost of A)

Straight-draw keeps both drawn cards, so **there is no "passed-over" card** — §16.2 **feeder 1 (the
highest-volume feeder) is eliminated.** Trace the per-Visit deck accounting:

| | Deck loses / Visit | → Larder (out of cycle) | → discard (recycles) |
|---|:--:|:--:|:--:|
| **keep-2 (current)** | 3 cards | 2 | **1 (passed-over)** |
| **straight-draw-2 (A)** | 2 cards | 2 | **0** |

Two opposing effects, and the honest net:
- **Decks deplete *slower*** under A (2 cards pulled/Visit, not 3) → each live deck lasts longer before
  deck-out → **reshuffles happen *less often***. Good side: **fired events recur less** (a phase's hazards
  cycle back more slowly — mildly kinder, less punishing).
- **But the discard grows *slower*** (only feeders 2/3/4 remain: paid ingredients, fired events, forced) →
  when a deck *does* run out, its reshuffle pile is **thinner and more event-enriched** than under keep-2.
  This *sharpens* the §16.5 "reshuffle-thinning / event-enrichment" risk: with passed-over ingredients no
  longer padding the discard, the pile that cycles back is proportionally more events + paid cards.

**Is that fine, or does A need a compensating feeder?** My read: **probably fine, because the two effects
partly cancel** (slower depletion offsets the thinner discard), and A does not touch the *source* of any
category — Pantry is still 11 physical cards cycling to cover 16 demand (§16.5), and A pulls the East deck
down *slower*. **But it must be measured, not assumed** — the exact tight-category (Pantry) `supply_min` and
the reshuffle cadence are what decide it. **Do NOT bake a compensating feeder now.** IF the re-sim shows
Pantry `supply_min` → 0 or a region stalls under A, the compensating fix is the **already-specified §12.5
deck-rebalance** (swap idle Sugar depth → Pantry/Meat: Central/South sugar 12→7, East pantry 11→14, North
meat 11→13) — **not** re-introducing keep-2 as a feeder. Re-adding keep-2 to feed the discard would be
tail-wagging-dog: keeping a dead micro-choice alive purely for deck plumbing.

### 18.2b Is A "the more coherent fix"? — CONFIRMED

The CD's claim holds. §12 deliberately made regions mono-signature **to force travel for variety**; keep-2
was trying to manufacture *in-region* variety the deck no longer has. A stops pretending: a region gives its
signature, and every variety decision lives on the map (travel) — exactly §12's spread engine. A is also a
net **rules-trim** (bg-elegance): *"draw 2 of this region's ingredients"* replaces *"flip 3, fire events,
keep 2, discard the rest."* One fewer sub-step, one fewer thing to teach, and it retires the "keeps ≤2 /
passed-over" clause from both the turn rules and §16.2's feeder list. The only price is the discard-feeder
loss (18.2a) — bounded and measurable. **A is the coherence + elegance winner unless the sim says it
starves a deck.**

## 18.3 Option B — more variety per region (make keep-2 a real choice)

The trap the CD named is exactly right and worth stating as a hard constraint: **the only thing that makes
flip-3-keep-2 a genuine *type* choice is putting ≥2 *useful* types in each region — which is what §12 spent
a whole pass REMOVING to force travel.** So a naive B ("give every region several sourceable types")
**directly undoes §12's spread-forcing** — if North also carries Pantry, an East-Pantry recipe is sourced at
North and nobody travels. **I will not spec that version; it is incoherent with the locked design.** Two
non-destructive B variants exist; only one is worth testing:

- **B-naive (REJECTED):** add a full secondary signature to each region. Makes keep-2 a real choice, but
  dissolves cross-region sourcing → kills §12. Do not test.
- **B-quality (REJECTED as hollow):** add a value/quality axis to the *same* type (premium vs standard
  Meat). Preserves regional identity and travel, BUT the choice is empty unless recipes *consume* quality —
  and recipes count tokens by type only (`ingredient_cost` = token count; the `value` column is blank). So
  B-quality creates a fake choice unless we also rebuild the recipe economy — a large, off-scope change.
- **B-wild (the ONLY testable B):** inject a **shallow "wild" ingredient** into each region-phase deck — a
  card that counts as **any one category** when paying a recipe. Keep-2 becomes a real choice
  (signature-for-volume **vs** the flexible wild), regional identity is preserved (the deck stays
  mostly signature), and **it does not turn a region into a bulk cross-region source** *provided the wild is
  a genuine minority.*

> **Rule (B-wild).** Add **`VISIT_VARIETY` wilds** (baseline test value **2**) to each region-phase deck. A
> wild ingredient (百搭 / "market-choice") counts as **one ingredient of any category** when paying a
> recipe. On a keep-2 Visit you choose signature-vs-wild. Kept in the CD's requested `keep-2` VISIT_MODE
> (B needs the keep-choice to express).

**Quantify the sourcing rebalance B-wild forces:**
- **Depth:** +2 wild per region-phase deck = **+16 wilds** if added on top (decks go 8→10 / 6→8 / 9→11).
  Added-on-top (not replacing signature) avoids starving the signature and slightly deepens every deck →
  **slower reshuffle-thinning** (a small §16 *benefit*), at a slower cycle-rate.
- **Effective supply:** wilds inflate the *effective* supply of every category. Since **Pantry is the one
  tight category** (24.6% demand vs 17.7% deck-share, §12.5), wilds preferentially get spent on Pantry →
  they **ease the Pantry squeeze** — a real upside. But that same flexibility is a *travel-avoidance* tool:
  every wild spent cross-region is one avoided Travel.
- **The load-bearing constraint on B:** the wild must stay a **minority** (≈2/deck, ≤ ~18% of a day deck) or
  it becomes a self-service cross-region substitute and **erodes the spread game** — the exact §12 intent.
  Even at depth 2, B-wild trades *some* travel-forcing for the in-region choice. **This is B's honest cost,
  and the sim must prove travel/spread rate (M2) does NOT fall vs Option A.**

**Honest bottom line on B:** B-wild is the least-damaging way to restore a live Visit choice, but it still
pushes *against* the pass that just locked. It adds a component (a new ingredient card type + its rule),
nudges toward less travel, and only "works" if held to a strict minority. **B buys a local decision at the
cost of a little of the global one A leans into.**

## 18.4 The switchable playtest lever (a clean toggle for the re-sim + the table)

Two independent toggles, so the sim can isolate *variety* from *draw-mode*:

```
VISIT_MODE    ∈ { straight-draw , keep-2 }     # A vs the keep-choice family
VISIT_VARIETY ∈ { mono , wild:K }              # K wilds per region-phase deck; K=2 baseline for B
```

| Cell | VISIT_MODE | VISIT_VARIETY | = | Purpose |
|:--:|---|---|---|---|
| **1** | `straight-draw` | `mono` | **Option A** | The recommended fix. |
| **2** | `keep-2` | `mono` | **Control (status quo)** | The non-choice the CD diagnosed — the baseline both fixes must beat. |
| **3** | `keep-2` | `wild:2` | **Option B** | Variety injection under the keep-choice. |

- **Cell 1 vs 2** isolates the cost/benefit of *dropping the keep-choice* (does A lose anything vs status
  quo on sourcing/throughput/reshuffle?).
- **Cell 3 vs 2** isolates whether *variety alone* restores the choice (M1 up) and what it costs travel (M2).
- **Cell 1 vs 3** is the head-to-head the CD wants: A (relocate the choice to the map) vs B (rebuild the
  in-region choice). The human table plays **Cell 1 and Cell 3 back-to-back** and judges whether a Visit
  *feels* like a decision or a chore.
- Baseline for the main re-sim run = **Cell 1 (A)** (my recommendation); Cells 2/3 are delta runs.

## 18.5 What the sim / table must measure to pick a winner

| # | Metric | What it tells us | Expected: A / Control / B |
|:--:|---|---|---|
| **M1** | **Live-decision density on a Visit** — % of Visits offering a real keep-choice (≥2 *useful* distinct types available) | Whether a fix actually restores the local decision | A ~**0** *(by design — choice moved to map)* / Control **LOW** *(confirms diagnosis)* / B **HIGH** |
| **M2** | **Travel / spread rate** — travels/player/game + cross-region-sourcing share | §12's core intent; **B's danger metric** | A **hold/RISE** / Control base / B **must NOT fall** vs A |
| **M3** | **Sourcing health** — per-category share vs §12.5 vector (±2pt); **Pantry `supply_min`**; `capbind` | The economy survives the change; Pantry is the make-or-break | all modes: shares track §12.5; **Pantry supply_min > 0** in whichever ships |
| **M4** | **Reshuffle cycle-rate** — reshuffles/game per region-phase deck + reshuffled-deck-size (§16.5 thinning proxy) | A's discard-feeder ripple (18.2a); B's deck-deepening | A **slower cycle / thinner reshuffle** *(watch)* / B **slower cycle / fatter reshuffle** |
| **M5** | **Throughput guard** — claims/gm, Booking + prestige-Booking completion (≥~90%), turns/player (26–32) | Neither Visit change chokes the §12.4 three-throttle stack | all modes must hold |

**Decision rule (state it plainly for the CD):**
- **Ship A** if Cell 1 holds M3 (Pantry alive) + M4 (no deck stall) + M5 (throughput) and M2 stays high —
  i.e. A costs nothing the sim can see. This is the expected outcome.
- **Ship B (wild:2)** only if the human table at Cell 1 genuinely *misses* the in-region choice (M1=0 feels
  flat) **AND** Cell 3 keeps M2 (travel) within a whisker of Cell 1 **AND** M3/M5 hold. If B drops travel
  materially, B loses on coherence regardless of how nice the local choice feels.
- **If A starves a deck** (M3 Pantry supply_min → 0 or M4 stall), first apply the §12.5 deck-rebalance under
  A — do **not** fall back to keep-2-as-feeder.

## 18.6 Recommendation

**Lean Option A (straight-draw).** It is the coherent heir of the mono-region redesign: §12 made regions
mono-signature to force travel, so the variety decision *belongs on the map*, and A honestly puts it there
instead of faking an in-region choice the deck can't support. It is a net rules-trim (bg-elegance win), it
preserves the sourcing rate (draw 2 = keep 2) and the push-your-luck event spine, and its one real cost —
losing §16's biggest discard feeder — is bounded (A also depletes decks slower, partly self-correcting),
measurable (M4 + Pantry `supply_min`), and cheaply fixable if it bites (the §12.5 Sugar→Pantry rebalance,
not a keep-2 revival). **Option B, even in its least-damaging wild form, spends a little of §12's
spread-forcing to buy back a local choice, and adds a component.** Set both up honestly — Cell 1 (A) vs
Cell 3 (B), with Cell 2 as the diagnosed control — and let the sim (M1–M5) plus the human table's
"decision-or-chore" read decide. My money is on A.

## 18.7 Change lists (SPEC-ONLY — for the owning agents AFTER the A/B resolves)

**SIM (`bg-playtest`) — ADDITION to the in-flight §9/§12.9/§16.8 re-encode (not a new run):**
- Add the **`VISIT_MODE`** toggle (`straight-draw` | `keep-2`) and **`VISIT_VARIETY`** (`mono` | `wild:K`,
  K default 2). Baseline the main run at **Cell 1 (straight-draw, mono)**; run Cell 2 (control) and Cell 3
  (wild:2) as deltas.
- `straight-draw`: Visit draws **2** ingredients from the region current-phase deck, digging past events
  (fire → discard), **no passed-over feeder** (drop §16.2 feeder 1 from the discard model for this mode).
  Big Eater draws 3 (+greedy 4th); Homebody draws 1.
- `wild:K`: seed **K wild ingredients per region-phase deck**; a wild pays **any one category** at Bribe.
  Keep-2 keep-choice active.
- **Add compare-metrics M1–M5** (§18.5): M1 live-Visit-decision rate; M2 travels/player + cross-region
  source share; M3 per-category share + **Pantry `supply_min`** + `capbind`; M4 reshuffles/game +
  reshuffled-deck-size per region-phase; M5 claims/gm + Booking/prestige completion + turns/player. Report
  Cell 1 vs 2 vs 3 side-by-side.

**DATA (`bg-developer`) — Option B ONLY, and only as a switchable/branch, NOT a destructive edit:**
- **`ingredients.csv`** — IF B is chosen: add **wild ingredient rows** (e.g. `ING-<R>-<P>-W`, type `wild`,
  tag `wild;<region>;<phase>;v7-B`, **quantity 2** per region-phase deck), effect *"百搭 Market-choice —
  counts as one ingredient of any category when paying a recipe."* **Add behind a B branch / feature flag —
  do NOT edit the mono baseline in place** (A must remain runnable). Option A requires **no `ingredients.csv`
  change.**
- Run `tools/lint/check_game.py` after any B branch (new rows + new `wild` type).

**RULEBOOK (`bg-rulebook` / `bg-elegance`) — teach whichever WINS, AFTER the A/B (not now):**
- If **A:** replace the Visit line with *"VISIT — draw the top 2 ingredients of this region's market into
  your Larder; any event you turn up fires at once."* Retire "flip 3 / keep 2 / discard the rest" from the
  turn rules **and** the §16.2 discard-feeder list (feeder 1 goes away — a small §16 rewrite). Net trim.
- If **B:** keep the flip-3-keep-2 line; add one line teaching the **wild (百搭)** ingredient ("counts as
  any one ingredient when you pay a stall"); `bg-infodesign` gets a wild-card icon. Net add — flag
  `bg-elegance` for the budget.

## 18.8 Handoff / coherence flag (per the contract — extends §11)

**Mechanics that move in this pass (spec-only until the A/B resolves):** the **VISIT sourcing action** — the
game's primary ingredient intake, which sits directly upstream of the **signature crowd-fight** (it funds
every Bribe). Flag the Director to run the guardian sweep on whichever option the A/B selects:
- **`bg-theme`** — Option A reframes a Visit as *"you take what the stall-strip is selling today"* (accept
  the region's specialty) rather than *"pick the best of three"*; confirm that still reads as a lively
  market forage, not a vending machine. Option B introduces a **wild "market-choice" (百搭)** ingredient —
  confirm the fiction (a mixed/utility grab) and that it carries **no cultural-sensitivity load** (a generic
  market item; **secular, dignified** per the rails).
- **`bg-elegance`** — A is a net **trim** (fewer Visit sub-steps + one fewer §16 feeder) → re-gauge headroom
  *down*; B is a net **add** (a new ingredient type + rule) → confirm within the complexity budget.
- **`bg-critic` / `bg-playtest`** — the ripples to watch: **A → §16 discard-feeder loss** (reshuffle
  cadence + Pantry `supply_min`); **B → §12 spread-forcing erosion** (travel rate M2 must not fall) **and**
  the §12.5 Pantry rebalance the wild causes. Both are wired into the M1–M5 probes above.

---

# 19. OPTION B-SPLIT — the finer regional taxonomy (the CD's ACTUAL Option B)

> **Status: SPEC-ONLY — no data/rules/sim touched.** §18 mis-analysed the CD's Option B. §18 evaluated
> three *foreign-injection / value / wild* variants and rejected all but B-wild. The CD's actual Option B is
> a **fourth, structurally different thing**: SPLIT each existing category into **finer subtypes that stay
> REGION-LOCAL**. This section specs it honestly, wires it as a third value of the §18.4 `VISIT_VARIETY`
> toggle (non-destructive — Option A stays runnable), and re-judges **A vs B-split** (a stronger B than the
> B-wild §18 landed on). **Bottom line up front:** B-split *preserves* cross-region spread (it is NOT
> B-naive), the **Pantry→Rice+Noodles** split is an excellent idea, the **Veg→Spices** split is near-
> vestigial and should be dropped, and the **decisive question is accessibility** — 8–10 ingredient suits at
> chip scale. The finer taxonomy's real value (recipe specificity + theme) is **orthogonal to the keep-2
> question**, which reframes the whole A/B (§19.8).

## 19.1 Why this is NOT the rejected B-naive — the spread test

§18.3 rejected "B-naive = add a foreign secondary signature to each region" because it **dissolves
cross-region sourcing** (if North also carries Pantry, an East-Pantry recipe is sourced at North → nobody
travels). **B-split does the opposite of what B-naive does:**

| | B-naive (§18, REJECTED) | **B-split (this section)** |
|---|---|---|
| What changes | Adds a **foreign region's category** to a region | Splits a category into **finer subtypes that stay in their ORIGINAL region** |
| North gains… | Pantry (East's category) → sourceable off-region | Nothing foreign — its Veg just resolves finer |
| Rice/Noodles live in… | (n/a) | **East only** — exactly where Pantry lived |
| Cross-region span of a recipe | **DESTROYED** (source anything anywhere) | **PRESERVED** — same region required, now a *specific subtype* of it |
| Effect on §12 spread-forcing | Kills it | **Neutral-to-reinforcing** (§19.3) |

**The spread test, run on all 24 recipes (§19.3): every ✱ cross-region requirement is identical before and
after the split.** Because subtypes co-locate (Rice+Noodles both East; Sugar+Pearls both Central&South;
Veg+Spices both North&East), no recipe can now be sourced anywhere it couldn't before, and none loses a
travel it used to force. B-split is **cross-region-neutral by construction** — the exact property B-naive
lacked. This is the crux of the CD's correction, and it holds.

## 19.2 The finer taxonomy (6 → 9, and why 8 is the honest number)

The CD's splits, mapped to the mono-6 taxonomy (Meat 肉 / Tea 茶 / Seafood 海鮮 / Pantry 糧 / Sugar 糖 /
Veg 菜) and the region-local map (N={Meat,Veg}, C={Tea,Sugar}, S={Seafood,Sugar}, E={Pantry,Veg}):

| # | Subtype (EN) | 繁體 | From | Region(s) it lives in | Role | New demand (of old total) |
|---|---|---|---|---|---|:--:|
| 1 | Meat | 肉 | Meat (unsplit) | North | signature (deep) | **14** (was 14) |
| 2 | Seafood | 海鮮 | Seafood (unsplit) | South | signature (deep) | **11** (was 11) |
| 3 | Tea | 茶 | Tea (unsplit) | Central | signature (deep) | **10** (was 10) |
| 4 | **Rice** | **米** | Pantry split | **East** | signature (deep) | **10** ⎫ Pantry 16 |
| 5 | **Noodles** | **麵** | Pantry split | **East** | signature (deep) | **6** ⎭ |
| 6 | **Sugar** | **糖** | Sugar split | **Central & South** | common (thin) | **5** ⎫ Sugar 7 |
| 7 | **Pearls (tapioca)** | **珍珠** | Sugar split | **Central & South** | common (thin) | **2** ⎭ |
| 8 | **Vegetables** | **菜** | Veg split | **North & East** | common (thin) | **6** ⎫ Veg 7 |
| 9 | **Spices / Herbs** | **香料** | Veg split | **North & East** | common (thin) | **1** ⎭ |

**"Meat + Fish, already two — keep distinct":** these are already separate categories in separate regions
(Meat=North, Seafood=South); no split needed. **Tea stays.** So only three categories split (Pantry, Sugar,
Veg), yielding **9 types**. Region identity is preserved exactly: each region still owns its signature +
its thin common, now resolved one level finer.

**Honest quality read of the three splits — they are NOT equal:**

- **Pantry → Rice 米 + Noodles 麵 — EXCELLENT, the whole reason to consider B-split.** 10/6 demand split,
  both well-used and iconic, and it splits a **signature** (the thing you Visit East *for*) into two
  high-demand subtypes → this is the *only* split that makes keep-2 genuinely real (§19.4). It also fixes a
  real fiction gap: "beef noodle = meat + noodles" and "congee = fish + rice" are obviously different foods
  the mono-6 taxonomy flattened into "Pantry."
- **Sugar → Sugar 糖 + Pearls 珍珠 — GOOD theme, MARGINAL mechanics.** Pearls demand is only **2** (both
  bubble teas), but boba is the single most iconic Taiwanese street ingredient and it is thematically wrong
  to file tapioca pearls under "sugar." Cheap identity win; low mechanical load. Borderline-keep.
- **Veg → Veg 菜 + Spices 香料 — WEAK, recommend DROP.** Spices demand is **1** (garlic on the Big Sausage).
  A whole ingredient suit — colour, emblem, deck cards, chips, art — for one token of demand is exactly the
  point-salad / component bloat `bg-elegance` and `bg-architect` exist to kill. And it does not even fix
  North's keep-2 (§19.4: North's problem is a low-utility common, not a lack of variety — adding a *second*
  low-utility common is noise, not a decision). **The refined B-split drops the Veg split → 8 types**, not 9.

> **Recommended taxonomy for testing: 8 types** (Meat, Seafood, Tea, Rice, Noodles, Sugar, Pearls, Veg) —
> the Pantry split (load-bearing) + the Pearls split (cheap identity), **without** the Spices split
> (vestigial). The 9-type version is specced for completeness but is not recommended.

## 19.3 The 24 recipes re-expressed (cost + cross-region span PRESERVED)

Subtype codes: **M**=Meat, **T**=Tea, **S**=Seafood, **Ri**=Rice, **No**=Noodles, **Su**=Sugar,
**Pe**=Pearls, **Ve**=Veg, **Sp**=Spices. Split choices are made by **dish fidelity** (a bao is flour→
Noodles; congee is rice→Rice; bubble tea's defining ingredient is Pearls). Cost = token count (unchanged
per dish). ✱ = forces cross-region travel (needs a non-home-local subtype). Home-local family unchanged:
N={M,Ve/Sp}, C={T,Su/Pe}, S={S,Su/Pe}, E={Ri/No,Ve/Sp}.

| id | Dish | tier | §12.7 recipe (mono-6) | **B-split recipe** | cost | ✱ span (was → now) | specificity added? |
|---|---|:--:|---|---|:--:|---|---|
| N01 | Pork Bao | 1 | M;P | **M;No** | 2 | ✱ P→E → No→E | needs **Noodles** (flour bun) |
| N02 | Egg Crepe | 1 | M;V | **M;Ve** | 2 | — local | — |
| N03 | Soy Milk | 1 | P;K | **No;Su** | 2 | ✱ P→E,K→C/S → No→E,Su→C/S | you-tiao = **Noodles** |
| N04 | Pepper Bun | 2 | M;M;T | **M;M;T** | 3 | ✱ T→C (same) | — (no P/K/V) |
| N05 | ★ Beef Noodle | 3 | M;P;V;V | **M;No;Ve;Ve** | 4 | ✱ P→E → No→E | **the CD's marquee apex — Noodles, not "Pantry"** |
| N06 | Big Sausage | 2 | M;M;S | **M;M;S** | 3 | ✱ S→S (same) | grilled-meat trophy (demoted from apex) |
| N07 | Bubble Tea | 1 | T;K | **T;Pe** | 2 | ✱ T→C,K→C/S → T→C,Pe→C/S | **Pearls** (珍奶 = pearl tea) |
| C01 | Ba-wan | 1 | M;T | **M;T** | 2 | ✱ M→N (same) | — |
| C02 | Misua | 1 | T;S;P | **T;S;No** | 3 | ✱ S→S,P→E → S→S,No→E | thread **Noodles** (麵線) |
| C03 | Bubble Tea (orig) | 1 | T;K | **T;Pe** | 2 | — local | **Pearls** (珍珠奶茶) |
| C04 | Sausage-in-Sausage | 2 | M;P;T | **M;Ri;T** | 3 | ✱ M→N,P→E → M→N,Ri→E | 糯米腸 = glutinous **Rice** |
| C05 | ★ Fengjia Signature | 3 | T;S;S;P | **T;S;S;Ri** | 4 | ✱ S→S,P→E → same | **Rice** plate |
| C06 | Wintermelon Tea | 1 | T;K | **T;Su** | 2 | — local | **Sugar** (no pearls) |
| S01 | Milkfish Congee | 1 | S;P | **S;Ri** | 2 | ✱ P→E → Ri→E | congee = **Rice** (粥) |
| S02 | Rice Bowl Cake | 1 | S;S;P | **S;S;Ri** | 3 | ✱ P→E → Ri→E | 碗粿 = **Rice** batter |
| S03 | Papaya Milk | 1 | V;K | **Ve;Su** | 2 | ✱ V→N/E → Ve→N/E | **Sugar** |
| S04 | Turkey Rice | 2 | M;P;V | **M;Ri;Ve** | 3 | ✱ M→N,P→E → M→N,Ri→E | 火雞肉**飯** = **Rice** |
| S05 | Coffin Bread | 2 | S;S;P | **S;S;No** | 3 | ✱ P→E → No→E | fried bread = **Noodles**(flour) |
| S06 | ★ Tan-tsú-mī | 3 | S;S;M;P | **S;S;M;No** | 4 | ✱ M→N,P→E → same | 擔仔**麵** = **Noodles** |
| E01 | Bamboo Rice | 1 | P;V | **Ri;Ve** | 2 | — local | 竹筒**飯** = **Rice** |
| E02 | Rice Cake | 1 | P;M | **Ri;M** | 2 | ✱ M→N (same) | 米糕 = **Rice** |
| E03 | Mochi | 2 | P;K;T | **Ri;Su;T** | 3 | ✱ T→C,K→C/S → same | 糯米 = **Rice**; **Sugar** |
| E04 | ★ Stone-Slab BBQ | 3 | P;P;M;M;V | **Ri;Ri;M;M;Ve**² | 5 | ✱ M→N (same) | highland grain = **Rice**; ²**keep Ve, do NOT reinterpret as Spices** (Indigenous — consultant-gated framing untouched) |
| E05 | Roselle Tea | 1 | T;K | **T;Su** | 2 | ✱ T→C (same) | **Sugar** |

**Verification (the CD's core ask):**
- **Cost totals per dish: identical** (every re-expression is a within-category relabel; no token added or
  removed). Deck cost distribution stays 2×14 · 3×8 · 4×3 · 5×1, avg 2.71 (§12.7).
- **Cross-region span: identical on all 24.** Every ✱ before is ✱ after; the 4 local dishes (N02, C03, C06,
  E01) stay local; 20/24 still force travel. **No recipe gains OR loses a required region.**
- **Aggregate demand preserved and re-verified against §12.5:** Meat 14, Tea 10, Seafood 11 (unchanged);
  **Pantry 16 → Rice 10 + Noodles 6; Sugar 7 → Sugar 5 + Pearls 2; Veg 7 → Veg 6 + Spices 1.** Σ = 65. ✓

**Where specificity ADDS spread vs is NEUTRAL — the honest answer:** the split adds **zero cross-region
span** (subtypes co-locate, so it cannot force a *new* region). Its reinforcement of §12 is on a **different
axis**: (a) **within-region specificity** — you must now draw the *right* subtype at the region you already
had to travel to (Noodles, not just "Pantry"), and (b) **anti-hoard pressure** — a single-region hoarder of
East gets a Rice+Noodles *mix*, so stockpiling no longer satisfies an arbitrary Pantry need; you need the
specific subtype, whose sub-pool is thinner. So B-split does not *widen* the map game; it *deepens* the
sourcing game and makes single-region hoarding modestly weaker. That is a genuine, if narrower, reinforcement
— and it is the opposite of B-naive's erosion.

## 19.4 Does keep-2 become a genuine choice? — YES at East, marginal elsewhere (be precise)

keep-2 is real **iff a Visit flips ≥2 distinct subtypes you would actually want to keep differently.** That
happens only where a region's **signature** (the thing you Visit it *for*) splits into two high-demand
subtypes — which, under the CD's list, is **East alone.** Region-by-region:

| Region | Deck under B-split | Distinct types shown | keep-2 verdict |
|---|---|:--:|---|
| **East** | **Rice** + **Noodles** (both signature-deep) + Veg | **3, two of them high-demand** | **GENUINELY REAL** — recipe-driven Rice-vs-Noodles |
| Central | Tea (signature-deep) + Sugar + Pearls | 3, but the pair is the *thin common* | Marginal — real only when you specifically need Pearls (2 dishes) |
| South | Seafood (signature-deep) + Sugar + Pearls | 3, pair is thin common | Marginal — as Central |
| North | Meat (signature-deep) + Veg (+Spices, 9-type) | 2 (or 3) all-low-utility beyond Meat | **Still shallow** — you Visit North for Meat; the common(s) are low-demand; adding Spices adds noise not a decision |

**Worked demonstration (the payoff, at East).** You are building **Beef Noodle** (M;**No**;Ve) and
**Milkfish Congee** (S;**Ri**). You Visit East and flip three: **{Rice, Noodles, Veg}**.
- **Mono-6 (status quo):** the flip reads {Pantry, Pantry, Veg} — keep any 2 Pantry; the two Pantry cards
  are interchangeable → **no decision** (the §18.1 diagnosis).
- **B-split:** Rice ≠ Noodles, and your two target dishes need *different* ones → keep **Noodles** (beef
  noodle now) **+ Rice** (congee later)? or **Noodles + Veg** if congee is off-plan? → **a real, recipe-
  driven keep decision.** Contrast a North Visit flipping {Meat, Meat, Veg}: still a rubber-stamp keep of the
  two Meat.

So B-split **restores keep-2 exactly where a signature splits** (East), and only there under the CD's list.
Across all 24 dishes, **9 touch Rice** (C04, C05, S01, S02, S04, E01, E02, E03, E04) and **6 touch Noodles**
(N01, N03, N05, C02, S05, S06), so which you want genuinely depends on your current Booking — the choice has
real information. **If the CD wants keep-2 real in ALL regions**, the move is to also split the other three
signatures (Meat, Seafood, Tea) and leave the commons mono — a larger, more symmetric variant flagged in
§19.8, but it pushes the suit count and the accessibility problem harder.

## 19.5 Sourcing rebalance — thinner sub-pools are the real economy risk

Aggregate demand is preserved (§19.3), so the §12.5 per-*category* balance is untouched at the family level.
The new risk is **within a split family: the deck must split too, so each subtype's effective pool is
thinner.** Reasoning from the current decks (`ingredients.csv` depths):

- **East (Pantry) deck** currently ≈ Pantry 6(day)/5(night) + Veg 2/1. Under B-split this Pantry depth must
  divide into Rice + Noodles cards. Demand is Rice 10 / Noodles 6 (≈ 5:3), so a proportional split of an
  11-card East signature depth is roughly **Rice ~7, Noodles ~4** across day+night. **Noodles at ~4 physical
  cards covering 6 demand is now the tightest sub-pool in the game** (worse than mono-Pantry's 11-vs-16,
  because it can't borrow Rice cards). A Visit that flips {Rice, Rice, Veg} gives a Noodle-hungry player
  nothing → travel-back or wait. **This is the #1 re-sim probe for B-split** (per-subtype `supply_min`,
  Noodles especially).
- **Sugar 5 / Pearls 2:** Sugar was already over-supplied (§12.5, 19.4% deck-share vs 10.8% demand), so even
  after peeling 2 Pearls demand off, Sugar stays comfortable. Pearls at 2 demand needs only a **shallow
  seed** (≈2–3 cards across Central+South decks). Fine.
- **Veg 6 / Spices 1** (9-type only): Spices at 1 demand needs 1–2 cards — a near-dead suit, reinforcing the
  §19.2 recommendation to **drop the Veg split**.

**Deck-depth spec (do NOT pre-change data; this is the branch target for the re-sim):** split the East
signature depth **Rice ≈ 60% / Noodles ≈ 40%**, seed **Pearls 2–3** off the existing Sugar depth (Sugar
absorbs the loss — it was over-supplied), and (9-type only) seed **Spices 1–2** off Veg. Keep total deck
depth ≈ 62 (redistribute, don't add). **Same aggregate demand, more categories → the binding question is
whether the thinnest sub-pool (Noodles) starves.** Flag for the re-sim; conditional fix if Noodles starves
= shift 1–2 cards from Rice → Noodles (the §12.5-style rebalance, held not baked).

## 19.6 THE CRUX — accessibility (this decides B-split)

**The problem stated honestly: 8–10 ingredient suits, each a CVD-safe, squint-legible colour+emblem pair, at
BOTH card scale and chip scale.** Ten mutually-distinguishable colours is beyond what any CVD-safe
categorical palette delivers (Okabe-Ito tops out ~8, and that degrades on small shapes). **A naïve "10
distinct colours" B-split is NOT accessible — full stop.** But the split's own structure hands us the only
encoding that can work:

> **Colour = the 6 original category/region FAMILIES (reuse the already-CVD-validated mono-6 palette).
> Emblem = the specific subtype within a family.** We do NOT mint new colours for Rice-vs-Noodles,
> Sugar-vs-Pearls, Veg-vs-Spices — the split pair **shares its family colour** and is told apart by a
> strongly-contrasting **emblem silhouette.**

This keeps the colour count at **6** (safe) and moves the discrimination load onto **9–10 emblems**. The
split pairs are conceptual cousins that co-locate, so a shared family hue is coherent, not confusing. The
emblem set must give each split pair a **maximally different silhouette**:

| Family (colour) | Subtype | Proposed emblem (silhouette-first) | Within-pair contrast |
|---|---|---|---|
| Meat (family A) | Meat 肉 | meat-cut / drumstick | — (mono) |
| Seafood (family B) | Seafood 海鮮 | whole fish | — (mono) |
| Tea (family C) | Tea 茶 | single tea leaf | — (mono) |
| **Pantry (family D)** | **Rice 米** | **cluster of small grains (dots)** | **grains-cluster vs long-wavy — STRONG** |
| | **Noodles 麵** | **long wavy strands** | |
| **Sugar (family E)** | **Sugar 糖** | **diamond/cube crystal** | **hard-edged diamond vs 3 filled circles — STRONG** |
| | **Pearls 珍珠** | **three filled circles (boba)** | |
| **Veg (family F)** | **Veg 菜** | **leafy green** | **leaf vs 8-point star-anise — STRONG** (9-type only) |
| | **Spices 香料** | **star anise (radial star)** | |

**Verdict — feasible, but a real, measurable downgrade concentrated at chip scale:**
1. **Colour:** FEASIBLE — reuse the 6 validated family colours; do not attempt 9–10 hues.
2. **Emblem at CARD scale:** FEASIBLE — cards are large; the silhouettes above read cleanly and pass a squint
   test.
3. **Emblem at CHIP scale:** **MARGINAL — this is where it bites and where the decision lives.** Under a
   shared family colour, colour **no longer identifies the suit** — you *must* read the emblem every time, and
   a chip is small. Mono-6 had colour sufficient + emblem redundant; B-split **inverts** that to emblem-
   primary. The Rice/Noodles pair (both pale-starch family) is the worst case.
4. **Linter:** likely **PASSES** `tools/access/check_access.py` (it is dual-coding/emblem-aware and the 6
   colours are already safe) — **but a linter pass would understate the real cost**: at-a-glance,
   across-the-table chip reading degrades for *everyone*, most for CVD and low-vision players.

**This is the decisive argument.** B-split is not *inaccessible*, but it trades the mono-6's clean colour-
sufficient encoding for an emblem-primary one that is materially harder at chip scale — and Option A pays
none of that. **Every added suit worsens it, which is the strongest reason to (a) drop the Veg→Spices split
and (b) prefer the smallest split that delivers the value (Pantry only, or Pantry+Pearls).**

> **FLAG `bg-access` (BINDING before any B-split ships):** verify the 8-type (Rice/Noodles/Pearls) emblem set
> against the actual theme palette with `tools/access/check_access.py`, AND run a **chip-scale squint test**
> the linter can't (physical-size legibility of the split-pair emblems under a shared family colour). If the
> chip-scale test fails, B-split fails on its decisive axis regardless of the linter result.

## 19.7 Component cost (flag `bg-architect`)

- **Ingredient CARDS:** total deck depth stays ≈ 62 (redistributed, not added), so card *count* is roughly
  unchanged — but each new subtype needs its **own card face + art asset** (8–10 vs 6). More unique
  illustration/mock-up work; a real but one-time art cost.
- **Ingredient CHIPS/tokens:** **confirm the pay mechanism first.** If a Bribe is paid straight from the
  Larder (a hand of ingredient *cards*), there are **no typed ingredient chips** and chip cost is ~nil (the
  "ingredient-cost chips" in §12.10 are the *number* on the vendor card, not typed tokens). If the game uses
  typed ingredient tokens, 8–10 denominations vs 6 means more punchboard, more sort space, bigger insert.
- **Net:** B-split's marginal COGS is dominated by **art assets** (more unique faces) and, *if* typed chips
  exist, punchboard. Flag `bg-architect` to run `tools/cost/check_cost.py` on the 8-type branch and confirm
  the pay mechanism. Likely small, but non-zero, and it stacks on the accessibility cost.

## 19.8 Switchable branch — extend the §18.4 VISIT_VARIETY toggle (non-destructive)

B-split is a third value of the existing `VISIT_VARIETY` axis — it does not disturb `mono` (Option A) or
`wild:K` (§18's B-wild):

```
VISIT_MODE    ∈ { straight-draw , keep-2 }
VISIT_VARIETY ∈ { mono , wild:K , split[:8|:9] }   # NEW: split = finer region-local taxonomy
```

| Cell | VISIT_MODE | VISIT_VARIETY | = | Purpose |
|:--:|---|---|---|---|
| **1** | `straight-draw` | `mono` | **Option A** | §18 recommendation; baseline. |
| **2** | `keep-2` | `mono` | Control (status quo) | The diagnosed non-choice. |
| **3** | `keep-2` | `wild:2` | Option B-wild | §18's B (erodes spread). |
| **4** | `keep-2` | `split:8` | **Option B-split** | **This section — keep-2 on the finer taxonomy.** |
| **4a** | `straight-draw` | `split:8` | **A + finer taxonomy** | **The decoupled hybrid (§19.9) — theme/specificity WITHOUT reviving keep-2.** |

- **Cell 4 vs 3** isolates B-split vs B-wild: does the *region-local finer taxonomy* restore keep-2 (M1) with
  **no travel-rate loss** (M2), where wild traded travel away?
- **Cell 4a** is the key insight (§19.9): the finer taxonomy is orthogonal to the draw mode — you can have
  Rice/Noodles under straight-draw and get the theme + specificity win with none of the keep-2 fakery.
- **Non-destructive DATA:** the split taxonomy lives in a **branch** `ingredients-split.csv` (subtype rows +
  split deck depths, §19.5) + a **branch recipe re-expression** of `vendors.csv` (the §19.3 column), behind a
  `SPLIT_TAXONOMY` flag. The mono-6 `ingredients.csv` / `vendors.csv` are **untouched** — Option A and Cells
  1–3 stay runnable exactly as specced.
- **Metrics:** reuse §18.5 M1–M5, **plus** a new **M6 = per-subtype `supply_min` (Noodles watch, §19.5)** and
  **M1 refined** to require ≥2 *distinct high-utility* subtypes (so the East signature-split counts and the
  North common-noise does not).

## 19.9 A vs B-split — the re-judgement (and the reframe the CD should see)

§18 recommended **A over B-wild**. Re-judging **A vs B-split**, B-split is a **stronger B than wild** on the
one axis that mattered most in §18:

| Axis | Option A (straight-draw, mono-6) | B-wild (§18) | **B-split (§19)** |
|---|---|---|---|
| Restores keep-2 | No (moves choice to map) | Yes (signature-vs-wild) | **Yes at East (recipe-driven); marginal elsewhere** |
| §12 cross-region spread | Holds/rises | **Erodes** (wild = travel-avoidance) | **PRESERVED exactly** (the win over wild) |
| Theme / fidelity | neutral | neutral | **UP** (rice≠noodles, boba pearls — a real identity gain) |
| Elegance | **net trim** (fewer sub-steps) | net add (1 type+rule) | **net add** (+2–4 suits, keeps keep-2 sub-step) |
| Accessibility | **6 clean suits, colour-sufficient** | +1 suit | **8–10 suits, emblem-primary at chip scale (§19.6 — the crux)** |
| Component cost | none | small | small–moderate (art assets; maybe chips) |
| Sourcing risk | discard-feeder loss (§18.2a) | Pantry-ease | **thin Noodles sub-pool (§19.5)** |

**Recommendation — and the reframe:** the CD framed B-split as a way to *rescue keep-2*, but §19.4 shows keep-2
only genuinely revives at **one region (East)**, while §19.6 shows the accessibility cost lands on **every**
chip. Judged as "keep-2 rescue," **B-split does not beat A** — it buys one region's local choice at the price
of the whole game's chip-scale readability, and A already relocated that choice to the map coherently.

**But the finer taxonomy's real value — recipe specificity + theme (beef *noodle*, boba *pearls*) — is
ORTHOGONAL to the draw mode.** That unlocks a better answer than either §18 option:

1. **PRIMARY — Ship A (straight-draw), and seriously consider adopting the Pantry→Rice+Noodles split UNDER A
   (Cell 4a).** This is the **decoupled hybrid**: straight-draw kills the dead keep-choice (A's coherence +
   elegance win), while Rice/Noodles delivers B-split's genuine upside (theme + recipe specificity + anti-hoard
   pressure + preserved spread) with the accessibility cost held to **+1 suit** (7 total, or +2 with Pearls) —
   *not* the +3–4 of the full keep-2 B-split. You get the best of both and pay the smallest access bill.
2. **SECONDARY — full B-split (Cell 4)** only if the human table at A/Cell-4a genuinely misses an *in-region*
   keep decision AND `bg-access` clears the emblem set **at chip scale** (§19.6). B-split beats B-wild, so if
   any keep-2 B is tested, test this one — retire `wild:2` from the plan.
3. **DROP the Veg→Spices split in all cases** (demand 1; pure bloat) — test **8 types**, not 9.

**My money: A + Rice/Noodles (Cell 4a).** It is the honest synthesis of the CD's correct instinct (the finer
taxonomy is a real improvement) and §18's correct instinct (the keep-choice belongs on the map, not faked
in-region).

## 19.10 Data-change list (SPEC-ONLY — branch, non-destructive; for the owning agents AFTER the A/B)

- **`ingredients-split.csv` (NEW branch file — do NOT edit mono `ingredients.csv`):** subtype rows for the
  **8-type** taxonomy (Rice 米, Noodles 麵, Sugar 糖, Pearls 珍珠 + unchanged Meat/Seafood/Tea/Veg), region-
  locked per §19.2, deck depths split per §19.5 (East signature ≈ Rice 60% / Noodles 40%; Pearls 2–3 seeded
  off Sugar; total ≈ 62). 9-type variant adds Spices 香料 (1–2 cards) — specced, not recommended.
- **`vendors-split.csv` (NEW branch, or a `recipe_split` column):** the §19.3 re-expressed recipes for all 24
  rows. **Costs and cross-region span unchanged** — this is a pure within-category relabel.
- **`bookings.csv`:** **no change** — prestige targets read `ingredient_cost` totals, which are invariant
  under B-split.
- **Sim (`bg-playtest`):** add `VISIT_VARIETY = split[:8|:9]` behind `SPLIT_TAXONOMY`; encode subtype-specific
  recipe payment and per-subtype decks; add **M6 per-subtype `supply_min`** + refined M1 (§19.8). Baseline
  main run stays **Cell 1 (A, mono)**; run Cell 4 and Cell 4a as deltas.
- Run `tools/lint/check_game.py` on the branch (new subtype rows + new `recipe_split`).
- **Option A requires NO data change** (mono baseline). B-split is entirely additive/branchable.

## 19.11 Handoff / coherence flag (extends §18.8 / §11)

Mechanic that moves (spec-only until the A/B resolves): the **ingredient taxonomy granularity** — upstream
of both the VISIT sourcing action and every Bribe cost. Flag the Director to run:
- **`bg-access` (DECISIVE — §19.6):** verify the 8-type emblem set against the palette AND a **chip-scale
  squint test** the linter can't run. This is the make-or-break for any B-split/hybrid — a linter pass alone
  is NOT sufficient sign-off.
- **`bg-architect` (§19.7):** cost-gauge the 8-type branch; confirm the Bribe pay-mechanism (cards vs typed
  chips) that determines whether chip COGS applies.
- **`bg-theme`:** the re-expressed recipes are *more* faithful (beef noodle = noodles; congee = rice; boba =
  pearls) — a coherence GAIN; confirm. **Rail-critical:** E04 Stone-Slab BBQ keeps **Veg** (not Spices) — do
  NOT reinterpret an Indigenous dish's tokens; framing stays consultant-gated and untouched.
- **`bg-elegance`:** B-split is a net ADD (+2–4 suits, keeps the keep-2 sub-step); the decoupled hybrid
  (§19.9, A + Rice/Noodles) is the lower-complexity path — re-gauge against the budget. The Veg→Spices split
  is flagged as bloat to cut.
- **`bg-critic` / `bg-playtest`:** the ripple to watch is **thin sub-pools** (Noodles §19.5), not spread
  erosion (spread is preserved). B-split does NOT reopen the §12 spread game the way B-wild did.

---

# 20. AGNOSTIC TOURS — make booking SAFE by default (CD steer, 2026-08-10)

> **Status: SPEC (bg-design, 2026-08-10). SPEC-ONLY — no data/sim edited here;** the change lists are
> §20.6–20.9. **This re-opens the booking economy** (the deck's phase mix + a handful of §14.3 values move),
> so it must **land BEFORE the CD-gated full sim** — otherwise the run measures the *old* risky deck and the
> "tours dominate" VP intent (§14) can't be read honestly.

## 20.0 The problem, in one paragraph (the CD's diagnosis)

Too many tours judge at **DUSK** — every `phase=day` Booking (20 of 45) must be *completed before the day
vendor pool empties*, or it **cancels at −⌊V/2⌋** (design-doc §17.7). Under the vendor-depletion clock (§17)
the player does **not** control when DUSK fires (the Closing-Time die can slam it shut early), so holding a
day tour is a real gamble. Players respond rationally: **don't book, hoard vendors** — which starves
tour-completion and lets the vendor-only hoarder over-win, defeating the §14 "tours are the win engine"
intent (the diagnosis's downstream finding #1). The clock is now vendor-driven so booking-avoidance no
longer *freezes* the game (§17 fixed that) — but booking must still be made **attractive and safe** or the
VP economy never fires. **The fix: make the majority of tours completable ACROSS the day→night transition
(judged at LAST TRAIN, not DUSK), so a booked tour is safe by default; keep a spicy minority phase-specific
and pay them a premium for the cancel risk.**

## 20.1 The mechanism that creates the risk (and the one lever that removes it)

The cancel risk lives entirely in **when a tour JUDGES**, not in what it targets:

- **`phase=day` → judges at DUSK.** Held-and-unfinished → CANCELLED −⌊V/2⌋. **This is the only acute risk.**
- **`phase=night` → judges at LAST TRAIN** (game end). No mid-game cancel; you have the whole night.

So the load-bearing move is a **new third phase value, `phase=any` (AGNOSTIC)**: *available to draw and hold
from the start, judged at LAST TRAIN.* An agnostic tour can be booked early, worked on across the flip, and
completed any time before the game ends — **near-zero cancel risk** (it only cancels in the rare event it's
still unfinished at LAST TRAIN, exactly like a night tour). No new penalty rule, no new component — one new
enum value on the existing `phase` column.

> **Design rule (agnostic-by-construction).** A tour is **AGNOSTIC** iff (a) it judges at **LAST TRAIN**
> and (b) its target is satisfiable by vendors **won in either phase** (any-phase counts, or a target that
> deliberately spans a day+night pair). A tour is **PHASE-SPECIFIC** iff it judges at DUSK (day-cancel risk)
> **or** its target can only be met within one phase.

## 20.2 The recommended RATIO — majority agnostic (point 1)

45 scoring tours. Recommended mix — **~2/3 agnostic, ~1/3 phase-specific premium:**

| Bucket | Count | Share | Judges | Risk | Pay |
|---|:--:|:--:|---|---|---|
| **AGNOSTIC** (`phase=any`, any-phase / day+night-spanning) | **29** | **64%** | LAST TRAIN | low (safe default line) | base rung |
| **PHASE-SPECIFIC — DAY** (`phase=day`, DUSK cancel risk) | **8** | 18% | DUSK | high (cancel) | **+1 rung premium** |
| **PHASE-SPECIFIC — NIGHT-locked** (`phase=night`, single-phase target) | **8** | 18% | LAST TRAIN | mid (completion-difficulty) | difficulty-priced (§14) |

Rationale for ~2/3: a player should almost always be able to hold a **safe** tour, so **booking is the
default attractive line** (fixes hoard-don't-book). The ~1/3 phase-specific keeps the day/night texture of
the theme alive and gives a **high-reward gamble** for players who want it. The DAY bucket is deliberately
**small (8)** — those are the only tours carrying the acute cancel risk, and they now *pay for it*.

*(The 8 NIGHT-locked are the tours whose target only night vendors can satisfy — `night_food_vendors`,
`apex_wins`, `expensive_vendors ≥4-cost`, `cross_region`, `final_round_wins`. They judge at LAST TRAIN so
they carry **no DUSK cancel**; their "risk" is completion difficulty within the shorter night, already
premium-priced in §14. They are counted phase-specific because they are NOT freely any-phase.)*

## 20.3 The two new tour TYPES (point 2)

Both are **agnostic by construction** and both lean on real day+night vendor pairs (§20.4).

### A. STREET / MARKET CRAWL (place-based)
> **Target syntax:** `locale:<key>>=N` — win **N vendors whose `locale` = key**. Judges at LAST TRAIN.

Complete the stalls of one walkable food district that spans a **day stall + a night stall**. The flagship
is **Dihua Street / Dadaocheng** — `locale:dadaocheng>=2`, whose only two members are N02 Egg Crepe (day) +
N07 Bubble Tea (night), so `>=2` **forces the transition span** — the cleanest showcase of the whole idea.
Honest crawl locales (real contiguous food destinations) in §20.4: **Dadaocheng, Tainan 府城, Taichung,
Hualien.**

### B. DISH-TYPE tour (food-based)
> **Target syntax:** `dishtype:<type>>=N` — win **N vendors whose `dish_type` = type**. Judges at LAST TRAIN.

"Try the island's best ___." The showcase is **bubble tea** — `dishtype:bubble_tea>=2`, whose only two
members are C03 (春水堂, the *birthplace*, day) + N07 (大稻埕 riverside neon, night): again exactly 1 day +
1 night, so `>=2` **forces the span**. Broader dish tours (`dishtype:noodle>=2`, `dishtype:bun>=2`,
`dishtype:rice>=3`, the existing `drinks` tours re-expressed as `dishtype:drink>=N`) don't *force* a span but
are still agnostic (LAST-TRAIN, any-phase) — the safe accumulation line.

### Existing types — kept, rebalanced (not deleted)
`region-pattern` (regions / region_depth / vendors_region / pair), `collection` (vendors_total /
food_vendors any), `cost-threshold` (cheap / expensive / ingredient_cost), `contest-win`, `apex/star`,
`cross-region`, `speed` all remain. The rebalance is **not** "delete types" — it is **flip most of them from
`phase=day` to `phase=any`** so they stop judging at DUSK (§20.6). Only the genuinely single-phase targets
stay phase-locked.

## 20.4 The DAY+NIGHT-PAIR AUDIT + the two new vendor tags (point 3)

**Answer up front: the existing 24 vendors already contain enough day+night pairs — by locale AND by
dish-type — to build every agnostic tour above. NO phase re-slotting is needed** (which is the right
outcome: re-slotting a vendor day↔night would break the **13-day / 12-night die-clock pools** (§17.1) and
would have to be done in balanced pairs; it also risks the 24-unique-dishes identity and the recipe/sourcing
economy). **The only vendor-data change is adding two grouping tags** — `locale` and `dish_type` — which
touch **no** recipe, cost, floor, phase, region, or VP value. Zero economic ripple.

**`locale` audit (which districts already give a day+night pair):**

| locale (key · 繁體) | day members | night members | pair? | crawl anchor |
|---|---|---|:--:|---|
| **dadaocheng 大稻埕** | N02 Egg Crepe | N07 Bubble Tea | ✅ 1+1 | **FLAGSHIP** (Dihua crawl; `>=2` forces span) |
| **tainan 府城** | S01 Congee, S02 Rice Cake | S05 Coffin Bread, S06 Tan-tsú-mī | ✅ 2+2 | Old-Capital crawl |
| **taichung 臺中** | C02 Misua, C03 Bubble Tea, C06 Wintermelon | C04 Sausage-in-Sausage, C05 Fengjia | ✅ 3+2 | City crawl (looser) |
| **hualien 花蓮** | E01 Bamboo Rice | E03 Mochi | ✅ 1+1 | Hualien crawl |
| taitung 臺東 | E05 Roselle | E04 Stone-Slab BBQ | ⚠ 1+1 | **DO NOT anchor** — E04 is the consultant-gated Indigenous item; no light-tour naming on it |
| taipei-core 臺北 | N03 Soy Milk | N04 Pepper Bun, N05 Beef Noodle, N06 Big Sausage | (span, but spread across the city) | not a tight crawl — use Dadaocheng instead |
| houlong / changhua / kaohsiung / chiayi / luodong | (solo, day-only or night-only) | — | ❌ | cannot anchor a crawl (fine) |

→ **4 honest crawl locales** (Dadaocheng flagship + Tainan + Taichung + Hualien). Ample.

**`dish_type` audit (which food-forms already span day+night):**

| dish_type (繁體) | members (d=day, n=night) | span? | usable for agnostic tour |
|---|---|:--:|---|
| **bubble_tea 珍奶** | C03(d), N07(n) | ✅ 1+1 | **SHOWCASE** — `>=2` forces span |
| **drink 飲品** | N03(d),C03(d),C06(d),S03(d),E05(d), N07(n) | ✅ (via N07) | `drinks` tours → `dishtype:drink>=N` |
| **noodle 麵食** | C02(d), N05(n),S06(n) | ✅ | `dishtype:noodle>=2` |
| **bun 包餅** | N01(d),N02(d), N04(n),S05(n) | ✅ 2+2 | `dishtype:bun>=2` |
| **rice 米食** | C01(d),S01(d),S02(d),E01(d),E02(d), S04(n),E03(n) | ✅ | `dishtype:rice>=3` |
| grill 燒烤 | N06(n),C04(n),C05(n),E04(n) | ❌ night-only | backs no agnostic tour (fine — premium night dishes) |

`bubble_tea` is a granular sub-type of `drink` (a vendor carries both, or `bubble_tea` is the `dish_type` and
"drink" tours count it too — dev's call; recommend `dish_type=bubble_tea` for C03/N07 and a `drink` **tag**
so `dishtype:drink` still counts them). Every other vendor gets one `dish_type`. **Grill is night-only by
nature** — it correctly produces no agnostic tour and instead sits behind the premium night bucket.

**Verdict:** existing set + the 2 tags **suffice**. No re-slotting; 13/12 pools, 24 dishes, and the
recipe/sourcing economy all untouched.

## 20.5 VP on the effort curve — premium compensates risk (point 4)

Anchored to the **locked §14 ladder (3·5·7·9·11)**. Two rules:

1. **New agnostic tours slot at the base rung for their effort.** A 2-vendor patterned tour (a forced-span
   locale/dish pair, or a region-2 / dish-2) = **5**. A 3-vendor accumulation (rice-3, drink-3) = **7**.
2. **At EQUAL effort, a phase-specific tour pays ONE rung MORE than the agnostic** (the premium that
   compensates the DUSK cancel / single-phase difficulty). **Agnostic must never out-pay a riskier
   phase-specific tour for equal effort** (the CD's explicit constraint).

**New-tour values:**

| New tour | target | phase | effort | VP |
|---|---|:--:|---|:--:|
| Dihua St Food Crawl | `locale:dadaocheng>=2` | any | 2, forced-span | **5** |
| Tainan Old-Capital Crawl | `locale:tainan>=2` | any | 2 patterned | **5** |
| Taichung City Crawl | `locale:taichung>=2` | any | 2 patterned | **5** |
| Best Bubble Tea (Origin & Neon) | `dishtype:bubble_tea>=2` | any | 2, forced-span | **5** |
| Noodle Run | `dishtype:noodle>=2` | any | 2 patterned | **5** |
| Rice Tour | `dishtype:rice>=3` | any | 3 accumulation | **7** |

**Ordering checks (premium holds):** agnostic region/locale-2 (5) **<** phase-specific `night_food>=2`
n_nmfood2 (7) ✓; agnostic `food_vendors>=3` d_food3 (5) **<** phase-specific `night_food>=3` n_nightfood3 (9)
✓. **One §14 violation to fix:** `d_breakfast3` (3 **day** foods before DUSK — riskier AND harder than the
agnostic 3-any-food d_food3, yet both sit at 5). **Nudge d_breakfast3 → 7** to restore the premium (§20.7).
And **tours stay dominant over vendors** everywhere: agnostic VP 5–11 still clears the vendor ceiling 6, so
§14.5's "vendor-only is dominated" argument is untouched (the change only moves *when* tours judge and adds
two lower-rung entry tours — it does not lower the tour ceiling).

## 20.6 The risk/reward, confirmed (point 5)

| | Agnostic (`any`) | Phase-specific (day / night-locked) |
|---|---|---|
| Judges | LAST TRAIN | DUSK (day) / LAST TRAIN (night-locked) |
| Cancel risk | ~none (whole game to finish) | **real** (day: DUSK cancel −⌊V/2⌋) / completion-difficulty (night) |
| Variance | **low** | high |
| Pay for equal effort | base | **+1 rung premium** |
| Role | **the default, always-safe booking line** | the spicy high-reward gamble |

This is exactly the CD's target shape: **booking becomes safe and attractive by default** (a player can
always hold an agnostic tour and work it across the flip → the hoard-don't-book problem dissolves), while
**phase-specific tours remain a live, well-paid gamble** for players who want the swing. The §15.9
cancel/salvage catch-up boons still backstop the minority of tours that do cancel.

## 20.7 Change list — `bookings.csv` (DATA — spec only, `bg-developer` executes)

**Core move — flip the any-phase-satisfiable DAY tours to `phase=any` (value UNCHANGED — kills their DUSK
cancel):** `d_food3, d_travel3, d_collect4, d_cheap3, d_cheap2, d_deep2, d_east1, d_pairNC, d_pairSE, d_mix1,
d_daymix, d_contest1, g_travel3d, d_north2*, d_south2*, d_central2*, d_drinks2**` (~16 rows). *(\*retargeted
to the new locale type — see below; \*\*re-expressed as `dishtype:drink`.)*

**KEEP `phase=day` (premium DAY bucket, 8) — the genuinely day-locked / day-flavoured:** `d_breakfast3`
(`day_food_vendors>=3`), `d_early3` (`early_vendors>=3`, end-game driver), `d_prestige8`
(`ingredient_cost_day>=7`) — plus retain ~5 more day tours here if the sim wants the bucket at 8 (candidates
to keep day for flavour: one region-2, one pair). Dev/`bg-playtest` set the exact 8; the **rule** is: a tour
stays `phase=day` **only** if it is day-locked or deliberately kept as a premium gamble.

**Retheme to the new STREET-CRAWL type (`locale:...`), set `phase=any`:**
- `d_north2` (was `vendors_region:N>=2`) → **Dihua Street Food Crawl**, `locale:dadaocheng>=2`, value 5.
- `d_south2` (was `vendors_region:S>=2`, already "Tainan Old-Capital Walk") → **`locale:tainan>=2`**, value 5.
- `d_central2` (was `vendors_region:C>=2`) → **Taichung City Crawl**, `locale:taichung>=2`, value 5.

**Add / retheme the DISH-TYPE type (`dishtype:...`), `phase=any`:**
- `d_drinks2` / `n_drinks3` → `dishtype:drink>=2` / `>=3` (rename to "Hand-Shaken Trail" etc.), values
  unchanged (3 / 5).
- **New:** **Best Bubble Tea** `dishtype:bubble_tea>=2`, value 5 (repurpose a redundant coverage slot — e.g.
  one of the three `regions>=3` duplicates `d_travel3`/`g_travel3d`/`g_travel3n`).
- **New:** **Noodle Run** `dishtype:noodle>=2`, value 5 (repurpose a second redundant slot).
- **New:** **Rice Tour** `dishtype:rice>=3`, value 7 (repurpose a redundant collection slot).

**VALUE nudge (premium ordering, §20.5):** `d_breakfast3` **5 → 7**.

**Night bucket:** leave `n_nightfood3, n_nmfood2, n_final2` (and the difficulty-locked `n_star1,
n_expensive1/2, n_cross1/2, g_cross1`) as `phase=night`. Flip the any-phase night tours (`n_four`,
`n_collect6`, `n_all4`, `n_allfood5`, `n_deep3`, `n_east2`, `n_surfturf`, `n_eastnorth`, `n_censouth`,
`n_contest2`, `n_prestige14`, `n_allvenue`, `g_collect5`, `g_prestige12`, `g_travel3n`) to **`phase=any`**
too (they already judge at LAST TRAIN — the flip only makes them **drawable from the start**, so the safe
line exists in Act I as well as Act II). Net deck: keep 45 rows; **no deck-size change** (protects
`booking_deck_sizes` + complexity/cost budgets).

Run `tools/lint/check_game.py` after (new `phase` enum value `any`, retargeted `target` strings, 3 value
edits, tag adds). Add `booking;any;agnostic;v7` / `booking;street-crawl` / `booking;dish-type` tags to the
reworked rows for downstream filtering.

## 20.8 Change list — `vendors.csv` (DATA — spec only)

- **ADD column `locale`** — controlled key per §20.4 (`dadaocheng, huashan, raohe, yongkang, shilin,
  houlong` … recommend one key per district; the four crawl keys `dadaocheng / tainan / taichung / hualien`
  are load-bearing, the rest are cosmetic grouping). No other field changes.
- **ADD column `dish_type`** — one of `{bubble_tea, drink, noodle, bun, rice, grill}` per §20.4 (with C03/N07
  = `bubble_tea`; keep a `drink` **tag** on them so `dishtype:drink` still counts them if the dev models
  drink as a superset). No other field changes.
- **NO phase / recipe / cost / floor / region / vp / quantity changes.** 13-day / 12-night pools, 24 unique
  dishes, sourcing economy, and §14 vendor VP **all untouched.** Re-run `tools/lint` + `tools/access`
  (tags-only; no palette/economy impact expected).

## 20.9 Change list — `map.json` + SIM + RULEBOOK (spec only)

- **`map.json`** — register the **third `phase` value `any`** for Bookings: available to draw from setup,
  held across DUSK, **judged at LAST TRAIN** (never cancels at DUSK). Recommend a **single always-available
  agnostic tour market** (or: agnostic tours present in *both* phase rows); `phase=day` tours remain
  day-draw-only and DUSK-judged; `phase=night` remain night-draw. Note the deck-plumbing is a dev choice —
  the invariant is *availability throughout + LAST-TRAIN judging* for `any`.
- **SIM (`sim/travel_agents.py`, `bg-playtest` re-models) — the run must model the reworked deck or it
  measures the wrong game:** (1) parse the two new target ops — `locale:<key>>=N` and `dishtype:<type>>=N`
  (count a player's WON vendors matching the tag); (2) implement `phase=any` = drawable from setup, judged at
  LAST TRAIN, no DUSK cancel; (3) **metrics:** booking-rate (bookings held/completed per player — must rise
  vs the old risky deck), **DUSK-cancel rate** (must fall sharply — the whole point), agnostic vs
  phase-specific **completion split**, and re-confirm §14.5/§14.6 (vendor-only winrate < ~10%, vendor-VP
  share ~25–35%) on the **new** deck. Wire to the §14.6 tuning tripwires.
- **RULEBOOK (`bg-rulebook`/`bg-elegance`):** teach the three tour kinds in one line — *"Most tours (marked
  ⟳ **any-time**) can be finished any time before LAST TRAIN — book them freely. A few **day** tours must be
  finished before DUSK or they're cancelled — riskier, but they pay more."* Plus the two new named types
  (street crawl / dish trail). Presentation flag `bg-infodesign`: the tour card needs an **any-time ⟳ vs
  day-only ☀ glyph** (dual-coded, not colour-only — flag `bg-access`).

## 20.10 Open questions for playtest (top 3)

1. **Is 2/3 agnostic too safe?** If booking-rate spikes but the *phase-specific* premium tours go
   near-unbooked (nobody takes the gamble), widen the premium (day tours +2 rungs) or trim the DAY bucket to
   6. Conversely if DUSK-cancels are still frequent, the day bucket is still too big — trim toward 6.
2. **Does the forced-span showcase (Dadaocheng / bubble tea) actually get completed?** Both require the
   *night* half (N07), which is a single-slot night stall the Closing-Time die can close (§17.3). If N07's
   closure routinely orphans these signature tours, they read as traps — consider a 2nd cheap night drink
   copy (the §17.6 "duplicate commodity stalls" lever) so the span is reliably completable.
3. **Does `locale:taichung>=2` (a looser, city-spread crawl) feel like a real "crawl" or just a region-2 in
   disguise?** If it reads as reskinned coverage, drop it and keep the 3 tight crawls (Dadaocheng / Tainan /
   Hualien) only.

## 20.11 Decision for the human

**A/B on the DAY bucket size (the one dial the CD should set):**
- **(A · RECOMMENDED) 8 day / 29 agnostic / 8 night-locked** — a real, well-paid phase-specific minority;
  booking safe by default. Best balance of "safe default" + "spicy option survives."
- **(B) 6 day / 31 agnostic / 8 night-locked** — booking even safer, cancel-risk nearly designed out; risk
  the day/night texture thins and the premium gamble is a curio.
- **(C) 10 day / 27 agnostic / 8 night-locked** — keeps more day flavour and end-game DUSK races, but leaves
  more cancel-risk on the table (closer to today's problem).

## 20.12 Handoff / coherence flags (per the contract)

**Mechanics that moved this pass:** (1) a **third `phase` value `any` (agnostic)** — tours now split
safe-LAST-TRAIN vs risky-DUSK; (2) **two new tour TYPES** — street-crawl (`locale`) + dish-type
(`dishtype`); (3) two **vendor tags** (`locale`, `dish_type`); (4) a **value nudge** (`d_breakfast3` 5→7) +
the day/night→any flips. **The signature twist (the follower crowd-fight over scarce vendors) is untouched**
— this pass only changes *when tours judge* and *how they're described*, not the fight or the pools.

- **`bg-theme` (naming — please bless the voice):** the new tour names live in the night-market world and
  should sing — "Dihua Street Food Crawl 迪化街美食巡禮," "Tainan Old-Capital Crawl 府城巡禮," "Best Bubble
  Tea — the Origin & the Neon Cup 珍奶朝聖," "Noodle Run 麵食巡禮," "Rice Tour 米食之旅." Secular, 繁體,
  English-first. Confirm the ⟳ any-time / ☀ day-only framing reads warm ("finish it whenever" vs "before the
  breakfast stalls pack up"), not bureaucratic. **Do NOT name a tour on E04 (Stone-Slab BBQ)** — Taitung is
  excluded as a crawl anchor pending the paid Indigenous consultant (§20.4).
- **`bg-elegance` (budget):** net rules add = one new `phase` enum value + two target operators + one
  glyph; it **replaces** no prose but is small — confirm within the complexity budget (it *buys* the removal
  of the biggest source of feel-bad cancels, a fun/clarity gain).
- **`bg-access`:** the any-time vs day-only glyph must dual-code (⟳ / ☀ + text, never colour-only); the two
  new vendor tags are non-visual (no palette impact) — a tags-only `tools/access` pass.
- **`bg-developer` (data):** owns §20.7/20.8/20.9 execution.
- **`bg-playtest` (sim):** **this re-opens the booking economy → land it BEFORE the CD-gated full sim.** The
  run must model `locale`/`dishtype` completion, the `phase=any` availability/judging, and re-verify §14 on
  the new deck (§20.9). Running the sim on the *old* risky deck would misread the "tours dominate" intent.

---

# 21. THE WILD BOOKING + THE 3P CLAIM-THROUGHPUT HELPER (CD steer, 2026-08-10)

> **Status: SPEC (bg-design, 2026-08-10). SPEC-ONLY — no data/rules/sim edited here;** the change lists are
> §21.10. Builds on the CD's locked calls: **accept the ~40–48 turns/player band** (a meatier game), **4–6p
> validated healthy** (bg-playstrat scaling sweep, sim `1c22551`: pace ~40–45, tours dominate, contested
> 24–27%, stall 1–2%), and **fix 3p with a helper package — NOT by shortening the game.** Two deliverables:
> **(1) a WILD BOOKING** action option (general, all counts) and **(2) a 3p claim-throughput helper**
> (simpler tours count-tagged into the 3p deck). This layers on top of §20's agnostic tours — it does not
> change the fight, the pools, the scarcity levers, or the §14 VP ladder.

## 21.0 Executive read

The 3p failure is **not** a VP problem (§14 already makes tours out-score vendors) — it is a **completion**
problem. A 3p player gets only ~**6–9 total claims** in a whole game, and the healthy 4–6p tour deck is
full of tours that each need **4–6 vendor claims** to finish. So a 3p player completes **<1 tour** and the
vendor-only **HOARDER wins 46–55%**. The fix has to make tours **completable at low claim volume**, without
touching the validated 4–6p deck.

- **Wild booking** removes the *hoard-don't-book hesitation*: if none of the (thin, at 3p) face-up tours
  suit, you may **decline the row and draw the top booking blind** — so you are **never stuck with no tour
  worth booking**. Bounded downside (a whiff costs one action + the flat **−1** cancel), push-your-luck
  upside (a fresh tour when the row is barren). General benefit; **strongest at 3p** where the face-up row
  is thinnest.
- **The 3p subset** is the load-bearing lever: **pull the ~7 heaviest 4+-claim collection/coverage tours
  OUT of the 3p deck** (via a per-count `counts` tag), leaving a 3p deck of ~38 tours **all completable in
  ≤3 claims.** Now a 3p player's ~7 claims each *contribute to finishing a tour* — they complete **3–4 small
  tours** and out-earn the hoarder.
- **The simpler tours are FLEXIBLE at 4–6p (CD refinement).** The 8 easy "on-ramp" tours are **guaranteed
  in at 3p** (the fix), but at 4–6p they sit behind a **switch** (`onramp_high_count`, default **IN**):
  **IN** = the validated 45-tour deck (gentler on-ramp + variety, no regression); **OUT** = a meatier 4–6p.
  The sim A/Bs it. So the 4–6p deck is **untouched by default**, with a deliberate meatier variant on tap.

## 21.1 The WILD BOOKING — the mechanic (a variant of Book, not a new action)

**Recommendation: make it a variant of the existing Book action (§6), not a new always-on action.** This is
the cleanest — it mints **no new action keyword** (bg-elegance rail) and the "instead of the face-up row"
framing *structurally* makes it the fallback rather than a parallel default.

> **Rule (extends rules-draft §6 — the Book action).** When you **Book a tour**, you may **either** take one
> card from the **face-up Booking row** (as now, then refill the row) **or** decline the whole face-up row
> and **draw the top card of the current Booking deck blind** and take it into your hand. **One Book = one
> tour, one way or the other** — you never do both, and you never see the blind card before committing.
> A blind-drawn tour is **kept** (it does not go back); if it does not fit your plan you may **Cancel** it
> later for the flat cancel (**−1**). Normal Book limits apply: you still hold at most **3**, and if you are
> at the limit you must Cancel one first (−1) to make room. Because you took no face-up card, the face-up
> row is **not** refilled on a wild Book.

- **Which deck:** the top of whichever Booking deck currently feeds the face-up row — the **DAY** deck by
  day, the **NIGHT** deck at night. Under §20 the decks are ~2/3 **agnostic (`phase=any`)** tours, so a
  blind draw very often lands a *safe, holdable* tour anyway — the wild booking and the agnostic rework
  reinforce each other (the gamble is mild because the deck is mostly safe tours).
- **You keep it (no peek-and-discard).** Keeping the blind card *is* the gamble; letting a player look then
  decline would make it strictly better than a face-up Book and trivialise the row (§21.2).

## 21.2 The WILD BOOKING — the guard (why it stays the fallback, not a strictly-better default)

The design constraint is that the wild booking must **not** become the default line that trivialises the
face-up choice. It does not, for three structural reasons — **no extra token cost is needed** (a cost would
be bloat):

1. **Information asymmetry self-selects it as the fallback.** A face-up tour is a **known** value; the blind
   draw is **unknown**. A rational player takes a suitable face-up tour when one exists (known good) and
   only gambles blind **when none of the face-up tours suit** — which is exactly the intended trigger. The
   either/or gate (one Book = one tour) prevents cherry-picking both.
2. **The action cost limits "digging."** Each wild Book is a **whole turn**. In a claim-limited game
   (especially 3p, ~6–9 claims total) an action is worth far more than the **−1** flat cancel, so spamming
   wild Books to dig for a specific easy tour is self-punishing — you burn tempo you cannot spare. The flat
   **−1** cancel makes the downside *cheap enough to never be stuck*, while the action cost makes it *too
   expensive to abuse*. That is the exact bounded-downside / push-your-luck shape the CD asked for.
3. **The hand-limit + keep rule caps the whiff.** A whiffed blind draw occupies a hand slot until you cancel
   it (−1), so a bad gamble has a small, real, bounded cost — never zero, never catastrophic.

**Verdict:** the gate "**instead of** the face-up row, one tour per Book, kept blind" is sufficient. It is
the fallback/gamble by construction; the face-up row remains the primary, better-informed line.

## 21.3 The WILD BOOKING — effect (general benefit, strongest at low counts)

The behaviour it kills is **hoard-don't-book hesitation**: today, if the face-up row shows nothing a player
can realistically complete, the rational line is to *not book at all* and just hoard vendors — which starves
tour-completion and hands the game to the hoarder. Wild booking means **a bookable tour is always one action
away**, so:

- **more tours enter play → more tours complete → tours-dominate strengthens** (the §14 intent finally
  fires in practice, not just on paper);
- **general across all counts**, but **strongest at 3p**, where the face-up row is thinnest (fewest slots,
  fewest draws cycling) and therefore most often shows nothing suitable. At 4–6p the row is wider and a
  suitable face-up tour is usually present, so the wild booking fires **rarely** there — which is precisely
  why it does **not** regress the validated 4–6p economy (§21.9). It is a *floor under booking*, not a new
  dominant strategy.

## 21.4 The 3P PROBLEM restated — it is COMPLETABILITY, not VP

From the bg-playstrat scaling sweep (sim `1c22551`): 3p is **claim-throughput-limited**. The chain:

- deep-claiming design (multi-ingredient recipes + the follower fight) → ~**13 turns per claim** → in a
  ~40–48-turn 3p game a player lands only ~**6–9 claims** all game;
- the healthy 4–6p tour deck is thick with **4–6-claim collection/coverage tours** (`n_collect6` = 6,
  `g_collect5` = 5, `n_allfood5` = 5, `d_collect4`/`n_four` = 4, `n_all4` = 4 regions);
- a 3p player cannot finish those **and** complete anything else → **<1 tour completed/player** → the
  vendor-only **HOARDER wins 46–55%** (vendors score their §14 VP with none of the tour overhead).

**Key correction (from the locked steer): pacing 3p faster does NOT fix this.** The CD's "3p clock ticks on
fewer vendors" *shortens* the game → **fewer** claims → **fewer** completed tours → it makes tours-dominate
**worse**. The lever that bites is **making each tour completable within the low 3p claim budget** — i.e.
shrinking the *claims-per-tour* the 3p deck demands, not shrinking the game.

## 21.5 CORE LEVER — a FLEXIBLE per-count `counts` tag (three groups + one switch)

Extend §20's tour-tagging machinery with a **`counts:` tag** naming the player counts at which a tour is
dealt into the deck. At setup you **build the DAY and NIGHT Booking decks from only the rows whose `counts`
tag includes your player count.** This is a **pure setup filter** — zero in-play rules, no new components,
invisible once the game starts (bg-elegance-friendly). It reuses the exact `tags`-column mechanism §20
already added, so it costs nothing structurally.

Per the CD's refinement, the tag is **not** a hard 3p-exclusive lock. Tours fall into **three groups**, the
third of which is **switchable at 4–6p** (a tuning A/B), while its 3p inclusion is guaranteed:

| Group | `counts` tag | Rows | 3p? | 4–6p? | Role |
|---|---|:--:|:--:|:--:|---|
| **CORE** | `counts:3456` | ~30 | ✅ always | ✅ always | the backbone — in at every count |
| **HEAVY** | `counts:456` | **7** | ❌ out (unreachable) | ✅ always | 4+-claim collection/coverage — a 3p ~7-claim budget can't finish these |
| **ON-RAMP (simpler)** | `counts:3456` **+ `onramp` group** | **8** | ✅ **always (the fix)** | **switchable** (`onramp_high_count`, default **IN**) | the easy 1–2-vendor tours; guaranteed at 3p, optional at 4–6p |

**Group 2 — HEAVY (hard-out at 3p; not switchable — they simply can't be completed at 3p):**

| id | Tour | Target | min claims |
|---|---|---|:--:|
| `n_collect6` | The Grand Tour | `vendors_total>=6` | 6 |
| `g_collect5` | New-Year Market Haul | `vendors_total>=5` | 5 |
| `n_allfood5` | Big Eater's Feast | `food_vendors>=5` | 5 |
| `d_collect4` | Full-Day Itinerary | `vendors_total>=4` | 4 |
| `n_four` | Four-Stop Night Run | `vendors_total>=4` | 4 |
| `n_all4` | Round-Taiwan · Route No.1 | `regions>=4` | 4 |
| `n_prestige14` | Top of the Charts | `ingredient_cost_total>=9` | ~3–4 pricey |

**Group 3 — ON-RAMP simpler tours (the flexible set — the 8 value-3, 1–2-vendor easiest tours):**

| id | Tour | Target | VP | vendors |
|---|---|---|:--:|:--:|
| `d_cheap2` | Budget Bites | `cheap_vendors>=2` | 3 | 2 |
| `d_deep2` | Become a Regular | `region_depth>=2` | 3 | 2 |
| `d_east1` | Taroko Day Trip | `vendors_region:E>=1` | 3 | 1 |
| `d_pairNC` | Taipei–Taichung Line | `pair:N+C` | 3 | 2 |
| `d_pairSE` | South-Link Coast Run | `pair:S+E` | 3 | 2 |
| `d_drinks2` | Hand-Shaken Run → `dishtype:drink>=2` | `dishtype:drink>=2` | 3 | 2 |
| `d_mix1` | A Bite & a Sip | `food>=1;drink>=1` | 3 | 2 |
| `d_daymix` | The Breakfast Set | `day_food>=1;drink>=1` | 3 | 2 |

- **The switch:** a per-count setup flag **`onramp_high_count`** governs whether the ON-RAMP group is dealt
  at **4/5/6p** (it is **always** dealt at 3p — that is the throughput fix). Two settings:
  - **IN (RECOMMENDED DEFAULT):** on-ramp tours stay in the deck at 4–6p → a **gentler on-ramp + more deck
    variety.** This is the deck the 4–6p sweep (`1c22551`) already validated as healthy (it ran the
    near-full 44-tour deck), so **default IN is the no-regression, safe default.**
  - **OUT (the "meatier 4–6p" variant):** the 8 on-ramp tours drop at 4–6p → higher counts are forced onto
    the ambitious tours, preserving a meatier feel. This is the A/B the sim must judge (§21.12 Q4).
- **Why default IN:** it reproduces the validated 4–6p deck exactly — zero risk to the healthy balance —
  and the CD's "harmless variety/accessibility win vs meatier" question is then answered *empirically* by
  the OUT run, not guessed on paper.

**The 3p deck, net:** CORE (~30) + ON-RAMP (8) = **~38 completable tours** (HEAVY 7 excluded), skewed hard
toward 1–2-claim tours — exactly the low-claim-budget completability the fix needs. **At 4–6p:** CORE +
HEAVY (+ ON-RAMP if the switch is IN) = the full **45** by default.

*(The 3p Booking-deck **size** parameter already scales down at low counts in per-count setup, so a ~38-row
3p pool is consistent with the smaller 3p deck — no deck runs thin.)*

## 21.6 The 3P COMPLETABILITY MATH — how tours now out-earn hoarding

**Assumptions:** 3p player ~**7 claims** all game (mid of 6–9); vendor-only hoarder ceiling ≈ **~22 VP**
(§14.5, unchanged); tour VP on the §14 ladder (2-vendor patterned = **5**, 1-vendor premium = **5–7**,
3-vendor = **7**). Claims are **shared** — a vendor you claim scores its vendor VP **and** counts toward
every tour it satisfies (§14.5).

**A tour-focused 3p line with 7 claims and the simpler deck:**

| Source | detail | VP |
|---|---|:--:|
| completed tours | 3× 2-vendor tours (5+5+5) + 1× 1-vendor premium (5) — claims SHARED across them | **~20** |
| vendor VP | those same ~6–7 claims also score vendor VP (mix of 1–3 each) | **~10** |
| **total** | ~7 claims | **~30** |

- **~30 (tour line) > ~22 (hoarder ceiling)** — tours out-earn hoarding at 3p, the whole point.
- The hoarder's ceiling is *unchanged*; what changed is that the tour player can now **convert** their 7
  claims into **3–4 completed tours** instead of **<1**, because the 3p deck no longer demands 4–6-claim
  tours. Completability, not VP, was the missing piece.
- **Wild booking is the enabler underneath this:** it guarantees the 3p player can *always* have a simple,
  completable tour in hand to point those 7 claims at — no dead "nothing worth booking" turns.

**Target for the sim (§21.10):** 3p **tours-completed/player rises above ~1** (aim ~2.5–3.5), **hoarder
winrate falls from 46–55% → ≤ fair (~33%)**, **vendor-VP share ~22–25%** (matching the healthy 4–6p band),
**pace stays in ~40–48 tpp**, **stall ≤ ~2%.**

## 21.7 The CD's CLOCK idea — a PACE aid only, NOT the tours-dominate fix

"3p clock ticks on fewer vendors" is evaluated **strictly as a pace lever, held OFF by default.** It does
**not** fix tours-dominate — it makes it worse (fewer claims → fewer completions, §21.4). **Do not adopt it
to fix 3p.** Adopt it **only if**, after the completability fix + wild booking, the sim shows 3p **drags
long** (pace pushes past ~48 tpp). That is unlikely: the completability fix does **not** lengthen the game
(same claim count — it just makes more of those claims *finish* tours), so 3p pace should already sit in
band. If a pace trim is ever needed, it is the already-flagged **die-clock track length L=2 at 3p**
(`map.json`, the L-sweep from the Closing-Time-die decision), not a claim-volume change.

## 21.8 RESERVE (last resort) — a modest 3p claim speedup

If completability (§21.5) + wild booking (§21.1) still leave the 3p tour line short of the hoarder in the
sim, a **modest 3p-only claim speedup** is the reserve — but it is the **lever of last resort** because
cheapening claiming ripples into the 4–6p spread depth and the scarcity economy. **Prefer the tour-side fix.**
If forced, ranked least-invasive first:

| # | Reserve | Change | Why held |
|---|---|---|---|
| **3p-a** | **+1 face-up Booking slot at 3p** | 3p Booking row shows +1 tour | Pure tour-supply widening — helps completion without touching claiming; try FIRST. |
| **3p-b** | **1 more `counts:456` demotion** | pull 3-claim coverage tours (`d_travel3`/`g_travel3d`/`n_deep3`) from 3p too | Deepens the subset skew; still tour-side, no claim change. |
| **3p-c** | **modest 3p claim speedup** | e.g. −1 follower floor OR +1 face-up **vendor** slot at 3p | LAST — cheapening claiming ripples into 4–6p spread depth; adopt only if a/b insufficient. |

## 21.9 COUNT-SCOPING — 4–6p are UNTOUCHED (confirmed)

- The `counts` tag is a **per-count setup filter by construction.** With **`onramp_high_count = IN`
  (default)**, the **4p/5p/6p deck keeps all 45 tours** — the validated 4–6p config (sim `1c22551`) is
  **byte-for-byte the same deck**, so the default has **no regression path.** The **OUT** setting is the
  only thing that changes a 4–6p deck (drops the 8 on-ramp tours), and it is a deliberate, sim-judged A/B —
  never a silent side effect (§21.12 Q4). Only **3p** ever loses the 7 HEAVY tours.
- **Wild booking is general** (all counts) but is a **pure add** — an *option* on an existing action that a
  player only takes when the face-up row is barren. At 4–6p the wider row rarely leaves a player with
  nothing suitable, so it fires seldom there. The sim's job is to **confirm** it does not shift 4–6p
  hoarder-winrate / pace / contested_frac vs `1c22551` (expected: negligible).
- **Net:** the only count whose deck changes is **3p**; the only new *option* (wild booking) is a floor that
  bites at low counts and is near-silent at high counts. 4–6p stay as-is.

## 21.10 CHANGE LISTS (SPEC-ONLY — for the owning agents to execute)

**`design/rules-draft.md` §6 (the Book action) — the WILD BOOKING (bg-design/bg-developer):**
- Add the either/or option to **Book a tour**: *"…or decline the face-up row and draw the top card of the
  current Booking deck **blind**, taking it into your hand (you keep it; the row is not refilled). One Book =
  one tour. A blind tour that doesn't fit can be Cancelled later for the flat −1."* Keep the 3-hold limit and
  the at-limit-Cancel-first rule consistent.
- Add a one-line rationale in §6 or the FAQ: *"You are never stuck with no tour worth booking — if the row
  is barren, take a chance on the next one off the pile."*
- **Confirm the flat cancel value is −1** (rules-draft §9 currently reads "−half"; the healthy config uses
  **flat:1** per the CD's accepted band — align §9's cancel wording to flat −1 when this lands, coordinating
  with §20's cancel references). Flag to bg-developer to reconcile in one pass.

**`components/bookings.csv` — the 3P count-tags, three groups (bg-developer):**
- Add a **`counts:` tag** to every row's `tags` field (reusing the §20 tag mechanism):
  - **HEAVY → `counts:456`** on the **7** rows: `n_collect6`, `g_collect5`, `n_allfood5`, `d_collect4`,
    `n_four`, `n_all4`, `n_prestige14`. (Hard-out at 3p; not switchable.)
  - **ON-RAMP → `counts:3456` + `onramp`** on the **8** value-3 rows: `d_cheap2`, `d_deep2`, `d_east1`,
    `d_pairNC`, `d_pairSE`, `d_drinks2`, `d_mix1`, `d_daymix`. (Always in at 3p; the `onramp` group tag lets
    the `onramp_high_count` switch drop them at 4–6p.)
  - **CORE → `counts:3456`** on the **other ~30** rows.
- **No value / target / phase / quantity changes** here — this is a tag-only add. (§20's phase/type/value
  reworks are a separate, already-spec'd change list — §20.7; execute both together but keep them distinct.)
- Deck stays **45 rows** total (protects `booking_deck_sizes` + complexity/cost budgets); the **3p deck is a
  ~38-row subset** (CORE + ON-RAMP, HEAVY excluded); the **4–6p deck is 45** by default, or **37** if
  `onramp_high_count = OUT`.
- **Reserve rows (do NOT add yet):** if the sim needs reserve **3p-b**, demote `d_travel3`/`g_travel3d`/
  `n_deep3` from CORE to `counts:456`; no new rows are created in any reserve.
- Run `tools/lint/check_game.py` after (new `counts`/`onramp` tag values on existing rows).

**`map.json` — per-count setup + the on-ramp switch + (conditional) clock (bg-developer):**
- Register that per-count Booking-deck composition **filters by the `counts` tag** (3p deck = rows tagged
  with 3). This is the setup-side plumbing for §21.5.
- Register the **`onramp_high_count`** switch (default **IN**): at 4/5/6p, deal the `onramp` group iff IN;
  at 3p always deal it. Expose it as a first-class sim/setup toggle for the §21.12 Q4 A/B.
- **Only IF §21.7 pace-trim is adopted** (not by default): set the 3p Closing-Time-die **track length L=2**
  as the 3p clock param. **Do not adopt unless the sim shows 3p drags.**
- **Only IF reserve 3p-a is adopted:** +1 to the 3p face-up **Booking** row count. Held.

**`sim/travel_agents.py` — model both, then validate (bg-playstrat / bg-playtest):**
- **Wild booking:** model Book as **either** a face-up pick **or** a top-of-deck blind draw; a bot chooses
  blind when no face-up tour is completable given its held + reachable vendors; the blind tour enters hand
  and is Cancelled at flat **−1** if it whiffs. Meter the wild-book **fire-rate by count** (expect high at
  3p, low at 4–6p) and its **completion contribution**.
- **3p deck:** build the 3p Booking decks from CORE + ON-RAMP (exclude the 7 HEAVY `counts:456`); ~38 rows.
- **The on-ramp switch:** model **`onramp_high_count`** as a toggle. 4–6p **IN** run = full 45 (the
  regression baseline vs `1c22551`); 4–6p **OUT** run = drop the 8 `onramp` rows (37) — the "meatier 4–6p"
  A/B.
- **Make-or-break metrics (3p):** tours-completed/player **> ~1** (aim ~2.5–3.5); hoarder winrate **46–55%
  → ≤ ~33%**; vendor-VP share **~22–25%**; pace **~40–48 tpp**; stall **≤ ~2%**; contested_frac holds.
- **Regression guard (4–6p, switch IN):** with wild booking ON and `onramp_high_count = IN`, confirm
  hoarder-winrate / pace / contested_frac / vendor-share are **within noise of sim `1c22551`.**
- **On-ramp A/B (4–6p, switch OUT):** does dropping the 8 easy tours make 4–6p **meatier** (fewer trivial
  completions, longer tail) **without** breaking tours-dominate — or is it neutral (default IN wins on
  variety/accessibility)? Report the delta so the CD can set the default (§21.12 Q4).

## 21.11 HANDOFF / FLAGS (per the contract)

**Mechanics that moved this pass:** (1) the **Book action gains a blind-draw variant** (the wild booking) —
a general throughput floor; (2) a **per-count `counts` tag** on tours yielding a **~38-row 3p deck** (the 7
HEAVY tours drop at 3p only); (3) a **flexible `onramp` group + `onramp_high_count` switch** — 8 easy tours
guaranteed at 3p, switchable at 4–6p (default IN = the validated deck). **The signature twist (the follower
crowd-fight over scarce vendors) is untouched** — no change to the fight, the scarcity levers, the pools,
the recipes, or the §14 VP ladder. This pass only adds a booking *option* and a per-count deck *filter*.

- **`bg-elegance` (budget — please re-gauge):** the wild booking is **+1 option on an existing action**
  (Book), **not a new keyword** — the smallest possible add; the `counts` tag is a **setup-only filter,
  invisible in play** (no in-game rules text beyond one setup line). It *buys* the removal of the 3p
  hoard-don't-book dead-turn problem (a fun/clarity gain). Confirm both sit within the complexity budget;
  flag if the Book action's rules-text grows past a clean sentence.
- **`bg-playstrat` (sim — validates next):** engineer (a) a bot that uses the wild booking rationally
  (blind only when the row is barren) and (b) the 3p exploit probe — does the 3p subset + wild booking make
  a **tour line beat the vendor-only HOARDER**, with pace in band, **without** regressing 4–6p? This is the
  make-or-break read (§21.10).
- **`bg-theme` (naming — light):** the wild booking wants a warm night-market name — *"Pot-Luck Booking /
  隨緣開團"* (take what the pile gives you) or *"Chance a Tour."* English-first, secular, 繁體. Confirm it
  reads as *taking a chance on the next tour*, not a penalty.
- **`bg-developer` (data):** owns §21.10 execution; reconcile the **flat −1 cancel** wording across
  rules-draft §9 + §20 in the same pass.
- **`bg-playtest` (sim harness):** this rides with §20 (both re-open the booking economy) → land §20 + §21
  together, then ONE combined re-smoke, **before** the CD-gated full run.

## 21.12 Open questions (top 3) + decision for the human

**Top-3 balance/open questions for playtest & sim:**
1. **Does the 38-row 3p subset get tours ABOVE the hoarder without over-simplifying 3p?** If tours-completed
   overshoots and 3p turns into a shallow tour-rush, dial the subset back (demote fewer tours) or lift a few
   3-claim tours back in. (make-or-break §21.6.)
2. **How often does the wild booking actually fire — and only when it should?** If it fires *often at 4–6p*
   (not just 3p), the either/or gate isn't self-selecting as intended and we may need a small friction; if it
   never fires at 3p, the 3p row is already fine and the subset alone carries it.
3. **Is the flat −1 cancel the right downside for a wild whiff?** Too cheap → players dig with blind draws
   (watch the fire-rate); too dear → the "never stuck" promise weakens. Tune the cancel value on the sim's
   wild-book fire-rate + dig-rate.
4. **(CD's flexible-inclusion A/B) Should the 8 ON-RAMP tours stay in at 4–6p, or drop?** IN = gentler
   on-ramp + variety (and the validated deck); OUT = meatier higher counts. **Does leaving them in harm the
   already-healthy 4–6p balance, or is it a harmless variety/accessibility win?** The sim runs both and
   reports the delta — this sets the `onramp_high_count` default.

**Decision for the human (two calls):**

**Call 1 — how aggressive should the 3p HEAVY drop be?**
- **(A · RECOMMENDED) Drop the 7 heaviest (4+-claim) tours at 3p** — `counts:456` on `n_collect6`,
  `g_collect5`, `n_allfood5`, `d_collect4`, `n_four`, `n_all4`, `n_prestige14`; keep all ≤3-claim tours in.
  Minimal, surgical, keeps 3p feeling like the same game with completable goals.
- **(B) Drop 10 (also the 3-region coverage + `n_deep3`)** — deeper skew to 1–2-claim tours; safer for
  completability but risks 3p feeling shallow / same-y (reserve 3p-b from the start).
- **(C) Drop none; rely on wild booking + reserve 3p-a (+1 Booking slot) alone** — smallest data change,
  but likely under-fixes tours-dominate (the sweep says the heavy tours are the throughput sink); not
  recommended.

**Call 2 — the `onramp_high_count` default (the flexible 4–6p inclusion, from the CD's refinement):**
- **(IN · RECOMMENDED DEFAULT) Keep the 8 on-ramp tours in at 4–6p** — reproduces the validated `1c22551`
  deck (no regression), gentler on-ramp, more variety. Let the sim's OUT run prove whether the meatier
  variant is worth switching to.
- **(OUT) Drop them at 4–6p** — meatier higher counts, but changes the validated deck; adopt only if the
  sim's A/B (Q4) shows a clear meatier-without-harm win.
