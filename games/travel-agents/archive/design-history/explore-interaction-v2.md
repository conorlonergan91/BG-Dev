# Exploration v2 — Reworking the Player-Interaction / Experience Layer

> `bg-explore` divergent→convergent pass for **Travel Agents: Taiwan** (slug `travel-agents`).
> CD feedback after the first prototype (decision-log, top entry): **(1) not enough player
> interaction; (2) the dead-drop card-swap isn't fun or on-theme** — even though the sim proved it
> *mathematically* rational (+1 VP). By the studio's fun-first rule, "not fun / off-theme" beats
> "technically optimal," so this pass has license to **replace or heavily rework** the co-op/sharing
> interaction. **KEEP** spine A's genuine strengths: the **recipes-by-region food-sourcing engine**
> and the **Discovery** feel — those aren't the problem.
>
> **Compatible seed (parallel `bg-theme` pass):** a **"command centre"** that dispatches the agents +
> the island's **events/hazards** as fiction. This pass treats that as a given and designs the
> mechanics/interaction structure to hang on it; names get reconciled later.
>
> **Hard constraints honoured throughout:** decide the dead-drop's fate explicitly · **2-player
> first** · weight **~1.8–2.2** (recommend a *subset*, don't stack everything) · sensitivity binding
> (warm-comedic, affectionate rivalry — a bake-off, not a heist; never a colonial/extractive gaze or
> mean-spirited take-that).

---

## 0. Diagnosis — *why* the interaction is thin (design before ideas)

Before diverging, name the disease precisely, because it changes the cure.

**The current game is a parallel optimiser with one thin contested resource.**
- **Indirect interaction is weak.** Ingredient supply is open/unlimited (no scarcity contention), and
  Agents don't block each other on the map. The *only* real contested resource is the **4-card Menu**
  (you can plate a dish out from under a rival). One contested row is not enough interaction to carry a
  duel — everything else is two people doing solitaire near each other.
- **The dead-drop is a *paid one-way gift*, and that's why it isn't fun.** In a competitive game,
  voluntarily handing your only opponent an ingredient is counter-intuitive; the sim had to *bribe* it
  with +1 VP to make anyone do it. A gift you're paid to give reads as neither generosity **nor**
  competition — it's an **accounting trick**. And it isn't even interactive: *you* decide, the rival
  *passively receives*. It's a transfer, not an exchange. On top of that, "dead-drop" is the one piece
  of spy language the theme pass already flagged as leaning toward the forbidden extractive gaze.
- **The dead-drop was overloaded.** It was simultaneously (a) the interaction mechanic, (b) the
  Fellowship mechanic, and (c) the Larder-surplus sink. Three jobs, none done well.

### The unlock: Fellowship does **not** require mechanical co-op here

The design-doc over-committed Fellowship to *cooperation-as-mechanic* (the dead-drop + shared Dossier).
But **identity.md's own locked definition of Fellowship is softer** and already points the way:

> *"Fellowship — the shared-table joy. Even in the competitive duel it's **warm rivalry** ('look what I
> found!'), and at 3–4 it's **table talk**."* — identity.md, locked aesthetics

So by the game's *own* identity lock, Fellowship is carried by **shared drama + warm rivalry + table
talk**, not by a gift economy. The CD's brief says the same ("warm events / table-talk / affectionate
take-that can carry Fellowship"). **This is the linchpin of the whole rework:** we can cut the paid
dead-drop and *still* serve locked Fellowship — arguably better, because a table groaning at a typhoon
together or needling each other over a sniped bounty *feels* like fellowship in a way a bribed gift
never did.

**Design consequence:** stop asking "how do we make helping a rival rational?" (a trap the sim already
showed is a knife-edge) and instead ask "**what shared drama and clean rivalry make the table lean
in?**" That reframe is what the four seeded axes are actually for.

---

## 1. Fate of the dead-drop / Grand Dossier — decided up front

Because so much hangs on this, the recommendation across **all** models below is the same, stated once:

- **Dead-drop (paid one-way gift): CUT.** It's the unfun, off-theme, overloaded mechanic; its three
  jobs are reassigned: interaction → events + bounty race + light orders; Fellowship → shared event
  drama + warm rivalry; surplus-sink → *turn surplus in for leverage* (an Order / a light trade), which
  **preserves the "convert dead weight into leverage" decision the sim liked, minus the paid-gift
  weirdness.** Net keyword change is roughly zero (we retire **Dead-drop** *and* **Insider Tip** and add
  1–2 new terms), so this is a *swap*, not bloat — a strong `bg-elegance` argument.
- **Grand Dossier (shared rising-tide track): KEEP, but REPURPOSE as the event/clock engine** (rename
  toward *"the Season" / "the trip timeline" / the island's calendar*). The whole table still advances
  it (the shared beat / Fellowship feel and the end-clock survive), but its milestones now **fire
  events** instead of paying a flat non-interactive bonus. This gives events a trigger with **zero new
  machinery** (reuses the existing track), trims a non-interactive scoring line, and keeps the
  "we're on this trip together" warmth. (Model B trims the track hardest; A and C lean on it.)

> **Thematic bonus (sensitivity-positive):** cutting "dead-drop" removes the extractive spy word the
> theme pass flagged, and making the **island itself react** (it throws festivals, it rains out a
> region) turns Taiwan from *passive scenery to be catalogued* into *an active place with its own life*
> — the exact opposite of the colonial gaze the identity forbids. The rework is *more* on-theme, not
> less.

---

## 2. Idea dump — concrete mechanisms by axis (diverge; quantity first)

Each: *mechanism · one-line fun rationale · rough weight cost (Δ over base)*. Nothing killed silently.

### Axis 1 — Region-specific EVENTS

*Trigger options*
- **1a. Milestone-fired events (reuse the shared track).** Each Dossier/Season milestone flips the top
  event. *Fun:* shared drama at a shared beat; zero new trigger machinery. *Weight:* +0.10.
- **1b. Event-on-entering-a-region.** Arriving draws that region's event. *Fun:* personal discovery.
  *Weight:* +0.25 — per-move bookkeeping and can feel punitive/random on movement. *Weaker.*
- **1c. Face-up "season queue" (one active event + next previewed).** *Fun:* Discovery — you *see the
  storm coming* and route around it (preserves agency). *Weight:* +0.20. **Best of the three** —
  telegraphing is what keeps events from feeling like a stolen turn.
- **1d. One event per round off a small deck.** *Fun:* steady rhythm. *Weight:* +0.15. Fine but no
  preview, so weaker on agency than 1c.

*Scope + content (must CHANGE MAP STATE so games differ; must stay warm-comedic)*
- **Festival — boost a region** (a region's dishes +1 VP / its specialty stocks +1 this round). *Fun:*
  a hotspot both players suddenly want → **turns the dead map into live contention.** *Weight:* +0.05
  on top of the deck. **⚠ Sensitivity:** use **secular/food-season** festivals (mango season 芒果季,
  a night-market anniversary, 尾牙 year-end-banquet season) — **avoid religious/sacred events as
  mechanical gags** (鹽水蜂炮, 大甲媽祖 pilgrimage, ghost-month) per identity's "no sacred motifs for
  gags." Curate the list with the consultant.
- **Hazard — typhoon 颱風 / landslide 土石流 / 塞車 traffic** blocks or taxes a region (can't stock its
  specialty / travel in costs extra this round). *Fun:* forced reroute = shared "oh no" drama;
  environmental, so it's fair and warm (the *island*, not a rival, is the antagonist). *Weight:* +0.05.
  Frame lightly ("the scooter's not making the mountain today"), never disaster-porn.
- **Funny local-character NPC — one-off warm effect** ("the 阿姨 insists you take one more" → +1
  ingredient; "a lost tourist swaps you a tip"). *Fun:* the warm-comedic heart; people as generous
  hosts. *Weight:* +0.05. **⚠ Sensitivity:** vendors/aunties are *subjects with dignity*, warm and
  varied — never caricature or a punchline (identity's "people with dignity" rule).
- **Bumper harvest / market glut** — a region's specialty is abundant (+1 when stocking there). *Fun:*
  a positive pull that re-routes both players toward the same region → contention. *Weight:* +0.05.

> **Key event insight:** events are a **contention *amplifier*** for the interaction the game already
> has. When a festival makes the South hot, *both* players want to route South *now* — suddenly the
> Menu race, positioning, and timing all bite. Events buy a lot of interaction-per-rule **and** they
> are the strongest possible Discovery engine. Their risk is *swing/feel-bad* (a hazard robbing a
> planned plate), which **telegraphing (1c)** and **delay-not-destroy framing** defuse.

### Axis 2 — "Command-Centre ORDER" cards (direct interaction + light take-that)

*How you get/hold/play them*
- **2a. Orders REPLACE Insider Tips as the leverage currency** (earned by plating / milestones / turning
  in surplus). *Fun:* the leverage you already had, now with teeth and targets. *Weight:* +0.10 net
  (retires the Insider Tip keyword). **Cheapest way in.**
- **2b. Small hand of Orders, drawn as/among actions, hold-limit 1–2.** *Fun:* hand-management timing.
  *Weight:* +0.25 (a whole sub-economy: gain rate, hold limit, timing). *Heavier.*
- **2c. Face-up "orders board" you claim from.** *Fun:* Discovery + contention over which order.
  *Weight:* +0.20.

*Content (three flavours the CD named — all bounded to **delay-not-destroy**)*
- **Boost yourself** — "Priority clearance": +1 action / stock +2 / free travel this turn. *Fun:* clean
  tempo pop. *Weight:* +0.05.
- **Risky self-stifle for a bigger payoff** (the risk-reward the CD explicitly wants) — "Deep cover":
  skip your next Stock Up, but your next Plate scores +2; or "All-in": commit toward your Assignment
  for a bonus but lock a region out this round. *Fun:* push-your-luck texture **without dice**
  (input-random gamble; agency preserved). *Weight:* +0.10.
- **Stifle a rival (light, warm take-that)** — "Tip off the competition" / "steal the last parking" /
  "beat them to the bao": target rival skips their specialty this turn / pays +1 to travel / can't
  plate the *one* dish they're set for *this turn*. *Fun:* the direct "gotcha" the game lacks. *Weight:*
  +0.10. **Bounding (mandatory, esp. 2p):** one-turn **delay, never destroy** (never discard a rival's
  ingredients, steal VP, or skip a whole turn); **symmetric access** (both draw the same pool, so it
  nets out); **telegraphed/counterable**; **capped** (one Order/turn, no chain-stifling the same
  player). **⚠ Sensitivity:** the target is your fellow *travel agent* (a bake-off rival), **never** a
  vendor or the place; frame agent-vs-agent and affectionate.

### Axis 3 — SECRET MISSIONS (keep single, or refresh/multiple?)

- **3a. Keep single static hidden Assignment** (status quo). *Fun:* clean, but your mission is your
  own business → **near-zero interaction.** *Weight:* baseline.
- **3b. Public "bounty board" you RACE to claim + your one secret Assignment.** A face-up row of
  claimable missions (first to complete claims it; then it's gone and refills), alongside your still-
  secret personal one. *Fun:* converts the **most inert part of the game (a private objective) into a
  live, readable contest** — "she's going for the Southern crawl, I'll grab the variety tour first."
  *Weight:* +0.20, but **reuses the Assignment card type** (they *are* Operation cards, just some dealt
  face-up), so **no new component type** and it's **budget-safe on the hidden-info axis** (open info,
  not a second hidden layer). **⚠ Maps *perfectly* to the "command centre dispatches agents to claim
  assignments" fiction** the theme pass is building. **Standout interaction-per-rule of the whole
  exercise.**
- **3c. Refreshing personal hand of missions** (complete one → draw the next). *Fun:* a personal
  progression arc. *Weight:* +0.20. *Weaker* — more solitaire engine than contest.
- **3d. Escalating public mission tiers** unlocked by the Season track. *Fun:* rising stakes. *Weight:*
  +0.30. Probably too much this pass; note only.

### Axis 4 — VENUE layer (breakfast shop / market / night market / restaurant / dessert / drink)

*(Already creeping in: the North-dish lock tagged 蛋餅 + karaage burger as "breakfast-shop" items.)*
- **4a. Pure flavour tag** (dish names its venue, no rule). *Fun:* texture. *Weight:* 0 — but this is
  exactly the "demoted to paint" mistake the CD warned about.
- **4b. Venue-set bonus** (plate one of each venue = "a full day of eating" set). *Fun:* a satisfying
  "you did the whole day" combo. *Weight:* +0.15 — **but it's a second parallel scoring axis that
  competes with the region web for the player's attention and risks point-salad, and it adds almost no
  *interaction* (it's solitaire).**
- **4c. Venues as action locations / a time-of-day rhythm** (night market only "open" late in the
  Season; breakfast shop gives a morning bonus). *Fun:* thematic day-arc. *Weight:* +0.30 — a whole
  time system; heavy.
- **4d. Venues split source-vs-plate** (market = stock, restaurant/stall = plate). *Fun:* more routing.
  *Weight:* +0.20 — **fights the region engine** (a second spatial layer over the one that already
  works) and adds friction.

> **Venue verdict: do NOT make it a core mechanic this pass.** It buys the least interaction-per-rule
> of the four axes and is the most likely to bloat weight or fight the region web. **BUT it earns its
> keep for free as the *flavour vocabulary of events* (4a++):** "the **night market** throws its
> anniversary bash," "the **breakfast shop** runs a 蛋餅 special," "the **dessert** stall's 芒果冰 is
> the festival." Venues ride along on the event layer at ~0 weight and give events concrete, warm
> texture. Keep the venue-set bonus (4b) in reserve as a *later dial* if the game wants one more axis.

---

## 3. Three coherent interaction models (converge)

Cut by **personality of interaction**, so this is a real A/B/C, not small/medium/large of one idea.
All three **cut the paid dead-drop** and serve Fellowship via shared drama + warm rivalry (per §0–1).

### Model A — "The Island Reacts" (environment-led · warmest · lightest)

- **New layer:** a telegraphed **event/Season timeline** (1c) fired off the repurposed shared track —
  festivals (boost a region), hazards (block/tax a region), warm NPCs (one-off). Secret mission stays
  **single & hidden** (3a). No orders board.
- **Turn shape:** unchanged core (Stock Up / Travel / Plate), but *what's valuable where* keeps shifting
  under the players. Surplus discards freely (or a trivial trade).
- **Dead-drop/Dossier:** dead-drop cut; track becomes the event/clock engine.
- **Serves:** **Discovery ✓✓** (events reveal & remake the island — the strongest Discovery of the
  three), **Fellowship ✓** (shared "oh no, typhoon!" drama + table talk), **Challenge ✓** (adapt your
  route). Interaction is **indirect, amplified** — the map finally lives, but it stays mostly
  environmental.
- **2p story:** both agents react to the *same* shifting island; a festival opening the South is a land
  rush both feel; hazards force shared reroutes. Symmetric and environmental → **maximally fair and
  warm at 2p**, no slap-fight.
- **Weight:** **~1.9–2.0** (adds ~+0.2, but cutting the dead-drop/tip economy claws most of it back).
  Lightest. Keyword-neutral-ish.
- **Risk:** may **not add enough *direct* interaction** the CD asked for — it heats the indirect layer
  but two players still rarely act *on each other*. Warmest but least spicy.

### Model B — "Command Centre Duel" (player-vs-player · spiciest · heaviest)

- **New layer:** the command centre runs the show. **(a) Public bounty board** (3b) you race to claim +
  your secret Assignment; **(b) an Orders economy** (2a → replaces Insider Tips) with all three CD
  flavours: boost-self, risky self-stifle, light stifle-rival. Events minimal (a couple of Orders *are*
  mini-events).
- **Turn shape:** the duel gets teeth — race for public bounties, spend Orders for tempo / gentle
  needling, still source-and-plate underneath.
- **Dead-drop/Dossier:** dead-drop cut; shared track trimmed to a lean end-clock (Orders/bounties carry
  the drama, so the flat rising-tide is redundant).
- **Serves:** **Challenge ✓✓** (the race + tempo/take-that), **Fellowship ✓** (warm needling + banter —
  "you did *not* just close my region"), **Discovery ✓** (bounties + orders reveal). Most **direct**
  interaction of the three.
- **2p story:** **sharpest of all at 2p** — a public two-person bounty race is maximally tense and
  legible with exactly two, and Orders let you needle your single opponent (bounded delay-not-destroy so
  it stays a bake-off, not a brawl).
- **Weight:** **~2.1–2.2** (bounty board + a full Orders economy = two subsystems; likely 7–8 component
  types with an Orders deck). **At the ceiling — be honest with `bg-elegance`.**
- **Risk:** **(1)** Discovery slips from *lead* toward co-lead (identity locks Discovery as the lead
  aesthetic — a real tension); **(2)** take-that must be *tightly* bounded or a 2p duel curdles into a
  feel-bad slap-fight; **(3)** heaviest, nearest the weight ceiling.

### Model C — "Rivals on a Living Island" (the balanced blend) — **RECOMMENDED**

- **New layer:** the two **highest interaction-per-rule** pieces, and *only* those:
  1. **Public bounty board** (3b) — the standout, reusing the Assignment card type (no new component
     type), perfect command-centre fiction, budget-safe. This is the **direct, legible contest** the
     game lacks.
  2. **Light telegraphed event layer** (1c, lean deck) — keeps **Discovery leading** and supplies the
     shared environmental drama that carries Fellowship, with **venues as the events' flavour** (§4).
  - **Orders kept MINIMAL:** no full deck/economy. Just **spend surplus for a small tempo Order** (fills
    the dead-drop's surplus-sink role) plus **2–3 gentle order-effects folded into the event deck** (a
    single, bounded, telegraphed dash of self-stifle-risk and light take-that) — enough spice to answer
    "more direct interaction" **without** paying for a whole second subsystem.
- **Turn shape:** source-and-plate underneath (spine A's kept strength), now inside a **live two-front
  contest** — race the public bounties *and* the shifting island — with a light tempo/needle lever from
  surplus.
- **Dead-drop/Dossier:** dead-drop cut; shared track = the event/clock engine (as A).
- **Serves:** **Discovery ✓✓ (still lead** — events), **Fellowship ✓** (shared event drama + bounty-race
  banter + light warm needling), **Challenge ✓✓** (bounty race + routing + surplus-tempo). Hits all
  three locked aesthetics with **Discovery intact as lead** — the one place Model B strains.
- **2p story:** the **public bounty race is razor-sharp at 2p** (a two-person claim race is the most
  legible, tense form of it), events keep every game's map different, and the *light* order lever adds a
  gotcha or two **without** a slap-fight. Explicitly designed 2p-first.
- **Weight:** **~2.0–2.1** (bounty reuses the Assignment type; events = 1 lean deck; no Orders deck).
  Middle — comfortably inside the ~2.2 ceiling with headroom.
- **Risk:** see §4 — chiefly whether **bounty-sniping is fun-tense or resentment-inducing**, and the
  usual "did we actually keep Fellowship after cutting co-op" question.

---

## 4. Recommendation, riskiest assumption, and what to test

**Prototype Model C — "Rivals on a Living Island" — first.**

**Why C over A and B:**
- **vs A (The Island Reacts):** A is the warmest and lightest, but it **under-delivers the direct
  interaction the CD explicitly asked for** — it heats the indirect layer without ever making two
  players act *on each other*. C keeps A's whole event engine (so it loses none of A's Discovery/warmth)
  and **adds the one piece that creates a direct, legible contest** — the public bounty race — at the
  cost of only ~+0.1 weight (it reuses the Assignment card type). C strictly dominates A on
  interaction-per-rule while staying inside budget.
- **vs B (Command Centre Duel):** B is the spiciest and the most 2p-sharp, but it pays for a **full
  Orders economy** (a second subsystem, 7–8 component types, ~2.2 at the ceiling) **and it strains the
  locked "Discovery leads" aesthetic** by promoting player-vs-player take-that to co-lead. C takes B's
  *best* piece (the bounty board) and B's *risk-reward flavour* in a **minimal, bounded dose** (surplus-
  tempo + a few event-folded orders) — so it gets ~80% of B's spice for ~half the weight, and keeps
  Discovery leading. **Bridge:** C and B share the exact bounty board and card types, so if playtests
  crave more bite, C upgrades into B cheaply by adding the standalone Orders deck — B is C's natural
  growth path (hand to `bg-architect`), exactly as spine B was to spine A.

**The best interaction-per-rule subset (the explicit "what to cut" the brief demands):**
> **IN:** public bounty board (reuses Assignment type) · a lean telegraphed event deck (venues as its
> flavour) · surplus→small tempo Order + 2–3 event-folded gentle orders.
> **CUT/DEFER:** the paid dead-drop (cut) · Insider Tips (retired into the tempo Order) · a full Orders
> deck/economy (defer to the Model-B growth path) · the venue-set scoring axis (reserve dial) ·
> venue-as-location / time-of-day (cut — fights the region engine) · event-on-entering-region (cut —
> use the telegraphed queue instead).
This is a **swap, not a pile-on**: we retire two keywords (Dead-drop, Insider Tip) and one balance
knife-edge (rational-tipping) and add two (Event/Season, Bounty), landing near weight-neutral. Make that
argument to `bg-elegance`.

**The single riskiest assumption a sim / quick playtest must attack first:**
> *That the **public bounty race** creates exciting, warm interaction — a legible "claim it first"
> contest — rather than **(a)** curdling into resentment when a rival snipes a bounty you were set up
> for (a permanent claim stings more than losing a refillable Menu card), or **(b)** snowballing, where
> the leader plates faster, claims bounties faster, and runs away.*

Everything else in C is comparatively safe; this is the load-bearing bet. Secondary risk: **do shared
events + warm rivalry actually deliver the locked Fellowship** now that co-op is gone (the §0 wager)?

**What to test (cheap, in order):**
1. **Sim — bounty-claim share vs finish position (2p, then 3p).** *Pass:* claims spread; the eventual
   winner does **not** claim a disproportionate share (no runaway). *Fail:* leader sweeps bounties →
   add a claim cap, a catch-up (trailing player claims cheaper), or make bounties refresh faster.
   Re-use the existing `tools/sim` harness (it already tracked "milestone-trigger share vs finish").
2. **Sim — event variance.** Do events change optimal routing game-to-game (games differ) **without** a
   single hazard being able to erase a planned plate (agency)? *Fix if needed:* stronger telegraph
   (preview 1–2 ahead), hazards *tax* rather than *block*.
3. **2p Screentop feel-test (the part the sim can't judge, per the CD's fun-first rule):**
   - Does sniping a bounty feel *tense-fun* or *rage-inducing*? (If rage: telegraph intent, or make the
     sniped player get a small consolation.)
   - Does the table **groan/cheer together** at events → is Fellowship actually present without co-op?
   - Do the light orders read as **affectionate needling** or **mean**? (Bound harder if mean.)
   - Is the surplus→tempo Order a satisfying replacement for the dead-drop's "convert dead weight"
     decision?

**Sensitivity gate before any art/content lock (binding):** curate the festival list to
**secular/food-season** events only (no sacred/religious gags); NPCs are warm, varied, dignified hosts
(never caricature/punchline); take-that targets the **fellow agent**, never a vendor or the place;
route the event/order/mission wording through the paid Taiwanese cultural + language consultant. The
rework is net *more* on-theme (it drops the extractive "dead-drop" word and makes the island an active,
living subject rather than catalogued scenery) — keep it that way.

---

## Decision for the human (A / B / C)

Which interaction model do we commit to designing?

- **A — "The Island Reacts":** events-only; warmest, lightest (~1.9–2.0), keeps a single hidden mission.
  *Risk:* may not add enough **direct** interaction the CD wanted.
- **B — "Command Centre Duel":** public bounty race **+ a full Orders/take-that economy**; spiciest,
  sharpest 2p (~2.1–2.2, at the ceiling). *Risk:* strains "Discovery leads," take-that balance, weight.
- **C — "Rivals on a Living Island" (RECOMMENDED):** public **bounty race** + a lean **event** layer +
  a *minimal* dose of surplus-tempo/light orders; hits all three aesthetics with **Discovery still
  leading**, ~2.0–2.1, 2p-first, and **upgrades into B cheaply** if we want more bite. Dead-drop **cut**
  in all three; Fellowship carried by shared event drama + warm rivalry (consistent with identity.md's
  own Fellowship definition).
