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
   (an outright plurality). *A tie claims nothing.* **Big Brother 大哥** wins by the **margin dial N** (§6.7;
   baseline N=1 = wins ties).
2. **Pay ingredients** — its recipe minus your region-icon discounts (Councillor discount per §6.6 — pending
   the CD's REPLACE/BLEND choice). **There is no follower threshold** — the ingredient cost is the only gate (§5).
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
| 2 | **Old Councillor 里長伯** | **Resource-engine rush** — draw/favours → afford pricey dishes EARLY, before the Influencer's crowd builds; take stalls uncontested by getting there first | **DRAW engine** (see §6.6) — passive card trickle + a favour/event hook | REPLACE-A or BLEND-B (§6.6); draw knob **+1 card/turn from any region, no action** | Rewards **speed** — buying the pricey stall before the pack arrives beats fighting for it under scarcity. A REAL REWORK (reopens his closed balance). |
| 3 | **Homebody 媽寶** | **Mobile forager who picks his battles** — wide ingredient spread from moving → afford complex dishes → win stalls the pack isn't on | **FORAGE**: on TRAVEL, draw 2 from the region you LEFT (sole Travel-sourcer) | `travel_draw_left = 2` | **PRESSURED, not exempt** — scarcity thins the "quiet" stalls too (1 non-refilling slot/region), so he can dodge the *cheap* scrums but must still fight for the *pricey* marquees his spread unlocks (§6.5a). |
| 4 | **Big Eater 大胃王** | **Greedy sourcing glut** — raw ingredient volume from Visits → afford anything, paced by a follower cost | **GLUT**: Visit keep ALL 3 + greedy 4th; hazards fire twice on his Visit | keep-3; greedy-4th = **return 1 follower to your supply**; hazard×2 | The greedy-4th follower cost pulls followers off his board → he is a **weaker battler**, so he wants cheap-to-win / uncontested stalls; scarcity makes him pace his greed. |
| 5 | **Big Brother 大哥** | **Margin battler** — win contests on the MARGIN, not the mass; fewer followers per win | **MARGIN dial N** (§6.7) | `N = 1` (baseline; = current wins-ties) | **Edge scales UP** with contest frequency — the reason he gets a tunable dial (pull back to 0, or up to 2). |
| 6 | **Globetrotter 阿嬤** | **Ubiquity** — reach any region in one Travel; chase whichever scarce slot just opened | `travel_anywhere`; immune to the HSR Maintenance outage | unchanged | **BUFFED by scarcity** — when each region has 1 region-locked, non-refilling slot, best positioning = best snipe. **Flag (§6.5b): may over-perform.** |

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

**Re-sim must confirm** (§9): the "ignore-the-contest" line is a viable ~in-band alternative, **not** a
dominant winrate. If his dodge winrate reads dominant, the knob is `travel_draw_left = 2 → 1` (narrow the
spread), not a scarcity change.

### 6.5b Globetrotter — scarcity is a buff; watch and hold a reserve

Go-anywhere-in-one-Travel is worth *more* when stalls are scarce and region-locked: she can always be where
the one open slot is, and snipe a quiet-region single slot before a Homebody walks over. Positioning becomes
premium exactly as she has the best of it. She is currently flaw-free (the small-basket flaw was retired in
the V7 close). **Reserve (hold, §8):** if she reads hot under scarcity, re-introduce a mild cost —
Larder/basket cap 7→6, or her Travel-anywhere costs a follower to supply — chosen after the sim shows the
magnitude. Do NOT pre-bake; flag for the re-sim's per-lane idx read.

## 6.6 Old Councillor 里長伯 — the resource-engine REWORK (CD choice: REPLACE vs BLEND)

The CD wants him to become a **resource-engine rush**: pull strings and call in favours so he can afford the
high-value dishes *early* — getting to the pricey stalls before the Influencer's crowd builds, or taking
them uncontested. This is a genuinely different identity from his current home-discount / away-tax kit, and
**it reopens his balance** (his away-tax +2 was a balance-closed trim; removing or softening it must re-sim).

**The concrete DRAW knob (both options share it):** *"Old Favours"* — **at the start of your turn, draw 1
card from ANY region's market (your choice) into hand, no action spent.** A steady, timing-independent
trickle from anywhere → more ingredients, faster → early buying power for pricey dishes. Optional flavour
layer / secondary knob: a **favour/event hook** — once per round he may resolve a face-up event to his
benefit (a "favour" — a beneficial event stays beneficial; a harmful one he waves off). Draw is the primary,
sim-clean knob; the event hook is the thematic garnish to tune only if the draw alone reads flat.

| | **(A) REPLACE** *(recommended for a clean lane)* | **(B) BLEND** |
|---|---|---|
| Home discount | **Dropped** | **Kept, lighter** — −1 in one home region only (no ramp-stack) |
| Away tax (flaw) | **Dropped** | **Dropped** (the flaw that made him a home-camper) |
| Draw engine | **+1 card/turn from any region** (the full engine) | **+1 card/turn from any region** (same) |
| Identity | A pure **connections/favours** economy-rush — legible, distinct, no home-camping | A **well-connected local** — a little home edge *plus* connections |
| Trade-off | Cleanest distinct lane; furthest from the closed V7 kit (biggest re-balance) | Familiar + incremental; risks a *muddy* double-engine (home edge + draw) that blurs the lane and stacks two advantages |

**Recommendation: (A) REPLACE** — the CD's aim is a *distinct* lane, and a home discount muddies "resource
rush" (it pulls him back toward camping and stacks a second edge). REPLACE also removes the FTUE
North-home-camping watch entirely. **(B) BLEND** is the conservative fallback if the CD wants continuity
with the printed kit.

**bg-theme flag:** does "pulls strings, calls in favours (events), has the connections to secure the fancy
stalls first" still read as a *warm* local councillor? I think yes — a well-connected councillor who *gets
things done for people* is squarely on-brand. **Rail:** keep it **favours / connections / clout**, never
*bribery / corruption / intimidation* (dignified locals; secular). The current blurb ("real clout in his own
borough") already carries it.

## 6.7 Big Brother 大哥 — the MARGIN dial (replaces the night-scope reserve)

His edge is no longer on/off. It is a graduated **margin dial N**:

> **Rule.** In a contested stall, the Big Brother claims it if the highest rival's committed followers
> exceed his own by **fewer than N** (i.e. `max_rival − his ≤ N − 1`). N is the tuning knob.

| N | Effect | Where |
|:--:|---|---|
| **0** | He **loses ties** — needs a strict plurality like everyone (no edge) | WEAK end |
| **1** | He **wins ties** — a rival needs +1 to beat him | **BASELINE (= current "wins ties")** |
| **2** | He also **shrugs off a one-follower deficit** — a rival needs +2 | STRONG end |

- **Baseline N = 1** (reproduces today's behaviour exactly). Playtest dial: **0 / 1 / 2.**
- This **replaces reserve (a)** (the night-scope). It is cleaner — **no day/night exception to teach** — and
  keeps his identity ("the market yields to Big Brother") intact across the whole range; only the *degree*
  moves. The critic's concern (he runs hot; scarcity strengthens the match-edge as fights get frequent) is
  now a single knob the playtester can dial down to 0.
- *Secondary note (optional, only if N=0 guts his identity but N=1 still overshoots):* a night-scoped N
  (e.g. N=1 night / N=0 day) remains available as a fine-grain fallback — but it re-introduces the exception
  the dial was meant to delete, so hold it below the plain 0/1/2 dial.


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
| **a** | *(retired — folded into the §6.7 margin dial)* | The night-scope reserve is **replaced** by the Big Brother's first-class **margin dial N (0/1/2)** — no exception to teach; pull him down to N=0 rather than night-scoping. | — (dial N is the lever now; night-scope survives only as the §6.7 secondary fallback) |
| **b** | **Endgame-tie resolver** (closes the stranding/denial HOLE — **load-bearing under scarcity**) | At **DUSK** and at **LAST TRAIN**, any tied contested stall force-resolves to **most followers, then earliest committer**; that agent claims it (pays ingredients if able), losers → own supply | Always specified as the phase-boundary rule (one FAQ line). Fires whenever a contested stall is still tied when DUSK / LAST-TRAIN triggers. Prevents perpetual re-tie freezes and permanent stranding. |
| **c** | **Influencer 網紅 `max` 7** | Drop her pool 8 → 7 | Re-sim seat-delta / `idx` shows 網紅 above band (reads hot). |
| **d** | **Non-refilling apex marquees** (§1.6) | Tier-3 apex stalls (N06/C05/S06/E04) never refill once claimed | Overall contested_frac rises but the *apex* contested rate stays flat AND the CD wants the famous-stall brawl sharpened. |
| **e** | **`max` knob** | Field `max` 5 or 7 (sweep) | Re-sim: if the fight over-floods (too many followers per stall) → 5; if it under-fires / can't spread → 7. |
| **f** | **Globetrotter 阿嬤 scarcity cost** (§6.5b) | Larder cap 7→6, OR Travel-anywhere costs 1 follower to supply | Re-sim shows 阿嬤 `idx` above band under scarcity (go-anywhere is buffed when slots are region-locked). |
| **g** | **Homebody 媽寶 spread trim** (§6.5a) | `travel_draw_left` 2 → 1 | Re-sim shows the "ignore-the-contest" dodge line is a **dominant** winrate (not merely viable). |

### 8.1 CONSOLIDATED PLAYTEST-LEVER TABLE (all dials in one place)

Everything the playtester can turn, baseline → range, folding the scarcity, meeple, and character knobs:

| Dial | Baseline | Range / options | Owns |
|---|---|---|---|
| **Scarcity — refill cadence** | slow / per-round | immediate (off) · per-round · phase-boundary (harder) | §1.2 |
| **Scarcity — face-up counts** | §1.3 (4/5/5/6) | looser (old 6/7/8/9) ↔ tighter | §1.3 |
| **Field `max`** | 6 | 5 / 6 / 7 | §3, reserve e |
| **start-on-board** | 2 | 2 (raise if a lane reads cold) | §3 |
| **Influencer 網紅 `max`** | 8 | 7 / 8 | §4, reserve c |
| **Big Brother 大哥 margin N** | **1** | **0 / 1 / 2** (0 = no edge · 1 = wins ties · 2 = survives −1) | §6.7 |
| **Old Councillor 里長伯 kit** | *CD choice pending* | REPLACE-A / BLEND-B (+ draw knob: 0 / +1 / +1&event-hook) | §6.6 |
| **Homebody 媽寶 forage** | draw 2 | 2 / 1 | §6.5a, reserve g |
| **Big Eater 大胃王 greedy-4th cost** | −1 follower to supply | −1 / −2 (if he over-sources) | §6.5, §2.1 |
| **Globetrotter 阿嬤 cost** | none (flaw-free) | none / cap 6 / −1 follower per Travel | §6.5b, reserve f |
| **Endgame-tie resolver** | ON (load-bearing) | on / off | reserve b |
| **Non-refill apex marquees** | off | off / on | §1.6, reserve d |

---

## 9. Re-sim scope (NOT run — CD-gated ~50 min; CD signs off THIS spec first)

Two changes reopen the win-a-vendor economy (meeples + scarcity), so re-run the standard V7 rig **per-count
3–6, N≥250/seating**, with these probes.

**Encode:** followers as a per-player pool (own supply / board / on-stall); Travel = grow 1; Promote = place
up to 2 from board (spread allowed); win → board; lost contest → own supply; `max` 6 (網紅 8), start 2; 大哥
= **margin dial N** (baseline 1); **里長伯 = draw engine** (+1/turn from any region; run REPLACE-A and
BLEND-B); Greedy-Grab & bad-review = return 1 to own supply; Trending / 2nd-Rave / "+1" events = grow 1.
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
b clear it?); Influencer idx under `max` 7 (reserve c).

**★ NEW — the six LANES must be DISTINCT and BANDED (the Steer-2 goal):**
- **Distinctness (not just balance):** per-character behavioural fingerprints should *diverge*, not just
  their winrates match. Report per character: contest-entry rate (Influencer/Big Brother high; Homebody
  low), followers-per-win (Big Brother lowest — margin; Influencer highest — mass), sourcing method mix
  (Councillor draw-share vs Homebody Travel-share vs Big Eater Visit-share), and **time-to-first tier-2/3
  claim** (the Councillor rush must land *earlier* than the field — the whole point of his rework). If two
  lanes fingerprint the same, they've blurred (esp. the three resource engines).
- **No dominant lane** — band idx 3–6p as before, with two sharp watches: **(i) Homebody dodge** — an
  "ignore-the-contest" bot line must be viable but NOT dominant (→ reserve g); **(ii) Globetrotter ubiquity
  under scarcity** — go-anywhere is buffed when slots are region-locked (→ reserve f). Report both idx
  explicitly.
- **Big Brother margin sweep N = 0 / 1 / 2** (the primary dial) — which N lands him in band *under scarcity*
  (fights are now frequent, so his edge is worth more than at the sim's old 5%).
- **Old Councillor REPLACE-A vs BLEND-B** — run both: does the draw-rush read in-band, does it actually hit
  pricey stalls earlier (the time-to-tier-2/3 probe), and does BLEND's double-engine (home + draw) overshoot
  or blur the fingerprint vs REPLACE's clean lane?

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
  "Follower / your pool" in all strings.
  - **大哥 (Steer 1):** recode `win_ties` → a **`margin_win` dial with parameter N (baseline 1)**; rewrite
    the ability to the §6.7 rule ("wins unless a rival exceeds his committed followers by N or more"; N=1 =
    wins ties). *Reopens his balance — sweep N in the re-sim.*
  - **里長伯 (Steer 2 — pending CD REPLACE/BLEND choice, §6.6):** REPLACE-A = drop `discount_home` +
    `away_tax`, add the **`draw_any` engine** (+1 card/turn from any region, no action) and rewrite ability
    + flaw + blurb to the connections/favours voice (rail: favours/clout, never bribery). BLEND-B = keep a
    lighter home −1 (no ramp-stack), drop `away_tax`, add `draw_any`. *Reopens his balance (away-tax +2 was
    closed) — do NOT execute until the CD picks A or B.*
  - No kit *values* change for 媽寶 / 大胃王(ingredient) / 阿嬤 (baseline; reserves f/g held).
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

**Steer-1/2 re-sweep (this pass):**
- **`bg-theme`** — **(i) Old Councillor rework fit (§6.6):** does "pulls strings, calls in favours, has the
  connections to secure the fancy stalls first" still read as a *warm, secular* local councillor? Guard the
  rail (favours/clout, **never** bribery/corruption/intimidation; dignified locals). Confirm whichever of
  REPLACE-A / BLEND-B the CD picks. **(ii) Influencer identity:** keep her *reach/viral — biggest crowd,
  fashionably late*, not a slow grinder (§4).
- **`bg-critic`** — **roster distinctness / no dominant lane:** are the six lanes mechanically distinct (the
  three resource engines especially — DRAW vs FORAGE vs GLUT, §6.5), and is any lane dominant — the Homebody
  **dodge** under scarcity (§6.5a) and the Globetrotter **ubiquity** buff (§6.5b) are the two to hunt, plus
  the Big Brother margin at N=2. All flagged for the scoped re-sim (§9).
