# Exploration — Making the Agent Layer Earn Rules

> `bg-explore` divergent→convergent pass for **Travel Agents: Taiwan** (slug `travel-agents`).
> Brief (Creative Director, 2026-08-06, + corrections): the secret-"travel agent" pun is the game's
> personality but had been demoted to paint, which made the draft (draft-your-trip + collect-the-best-
> eats optimiser) feel **generic**. Lean into the agent layer so "I'm a food spy on a secret mission" is
> something you *do*, not read on the box.
>
> **Hard constraints:** weight **~1.8** (one clean hidden-info hook, **not** a deduction engine); the
> **warm-comedic wink** (trench-coat-over-Hawaiian-shirt, never menace, never an "outsider
> catalogues/extracts the exotic East" gaze — sensitivity pass); **Discovery leads**, then **Fellowship**,
> then **Challenge** (the game's own locked aesthetics); **Taiwan must do real work** — dish/region
> specifics shape sets and routes, never generic "food + map"; the agent layer must **earn real rules**.
>
> **CD corrections folded in (this pass):**
> 1. **No global "house style."** Judge this game **purely on its own terms** (identity.md / game-bible.md).
>    Do **not** privilege co-op, tug-of-war, or any mechanism family unless *this game's* brief points
>    there. (Earlier draft leaned on a studio-taste north star — removed.)
> 2. **CD wants a BLEND:** a fundamentally **competitive** game that carries a **genuine cooperative /
>    shared-table layer** (semi-co-op), *or* one core that cleanly runs **both** a duel and a co-op mode.
>    The recommendation must reflect that blend — not a pure-competitive or pure-co-op pick.
> 3. **Two new food inspirations — "Yes! Ginseng" and "Taiwan Snackbar"** — mined for how food/ingredients/
>    dishes are made *central and celebrated*, to push Taiwan-specificity (see box below).

---

## What the two food inspirations teach us (food-content presentation)

*(Presentation principles extracted; exact rules unverified — flag `bg-research` to confirm specifics
before Design locks the economy.)*

- **Taiwan Snackbar** — the food *is* the star: individually named, illustrated **real Taiwanese
  dishes**, each its own celebrated card. Take-away: dishes should be **specific and hero'd** (gua bao,
  beef noodle, oyster omelette, bubble tea, stinky tofu…), not abstract "food tokens." Every dish a
  little postcard.
- **Yes! Ginseng** — foregrounds **ingredients** and their **quality/grade** as the tradable unit.
  Take-away: a light **ingredient → dish** layer, where a dish is *composed* of a few named ingredients,
  and ingredients carry regional origin. This is the single biggest lever against "generic."

**→ Design driver for the spine.** Instead of "collect finished dish cards," a **dish = a tiny recipe of
2–3 ingredient icons**, and ingredients are **sourced from the regions that actually supply them**. So:
- **Beef noodle 牛肉麵** = beef + hand-pulled noodles + suan-cai broth. **Gua bao 刈包** = braised pork
  belly + pickled mustard greens + peanut powder. **Oyster omelette 蚵仔煎** = oysters (coastal) + sweet-
  potato starch + egg. **Bubble tea 珍珠奶茶** = tea + tapioca pearls + milk.
- Coastal regions supply oysters; the south supplies certain classics; mountain/Hakka towns and the
  east (Indigenous cuisines) supply others. **Now the *map* and the *routes* are Taiwan-shaped by real
  food geography** — you travel *because* the ingredient you need lives *there*. That's the
  re-skin-test defeater: rename the setting and the recipe/region web breaks, i.e. Taiwan is doing work.
- Weight guard: keep it a **2–3-icon set-collection refinement, not a crafting engine** — the elegance
  budget (~1.8) forbids a production chain. You gather icons and "plate" a dish; no intermediate steps.

The shared spine underneath every direction: a map of **Taiwan's regions** holding **ingredient
markets**; you **travel** (HSR / local rail / scooter / ferry — a small transport economy) to source
ingredients and **plate specific dishes** into your **Traveller's Log** (set collection), the trip
bounded by a shared clock (the last train). That spine is the "generic" part. The **agent hook** is what
makes the personality load-bearing.

---

## 1. Idea dump — how the agent/mission fantasy can earn rules

Quantity first. Each: *mechanism · why it feels like a food-spy · weight cost*.

1. **Hidden "Assignment" dossiers (secret objectives).** Hold 1–2 secret scoring targets ("Operation:
   Beef Noodle — plate three southern classics"). *Feels spy:* your classified mission dossier; nobody
   knows your real target. *Weight:* +0.1 — a Ticket-to-Ride destination ticket in a trench coat. **Fits
   trivially.** (Alone it *stays* a re-skinned ticket — needs a partner hook.)

2. **Covert simultaneous selection ("program your strike").** Each round players secretly choose their
   next destination/market face-down; reveal at once. *Feels spy:* covert ops — don't tip your hand.
   *Weight:* +0.2. Low downtime. **Fits.**

3. **Light bluff / cover-story read.** Play a face-down claim; an opponent may call it. *Feels spy:* a
   feint. *Weight:* +0.2–0.3 **and it pulls toward a gotcha register that fights the warm tone.** At most
   one gentle call — or cut.

4. **Hidden movement (Scotland-Yard-lite).** Your position is secret; rivals deduce it. *Weight:* **+0.5+,
   a deduction engine — REJECTED for base** (breaks the one-hook cap; hunting each other is menace, not a
   holiday). Note only.

5. **Handler / intel-sharing role.** A (rotating) **Handler** sees a slice of upcoming intel and passes
   *constrained* tips. *Feels spy:* handler briefing agents in the field. *Weight:* +0.2–0.3. Opens a
   **shared-table / semi-co-op** door.

6. **Secret-role / hidden-loyalty (3–4).** Some players are double agents for a rival agency. *Weight:*
   +0.4 **and an accusation layer that risks turning mean — tonally wrong.** Wild card only.

7. **Shared Table Dossier (collective objective).** Alongside private scoring, a **face-up island Grand
   Dossier** the whole table advances *together*; completing stretches pays **everyone** a Discovery
   bonus. *Feels spy:* the cell's overall mission runs under the personal ops. *Weight:* +0.2. **This is
   the semi-co-op blend the CD asked for** — cooperation and competition in one box.

8. **Tip-offs / dead drops (blind hand-off).** Secretly pass a face-down **recommendation** (an ingredient
   / a hot-stall tip / a transport ticket) to another player. *Feels spy:* the dead drop. *Weight:* +0.2.
   Warm — "look what I found!" — the literal **Fellowship** mechanic; can *help a rival yet bank you* a
   shared/personal reward. Works competitive, semi-co-op, or co-op.

9. **Cover identities (hidden asymmetric power).** Each holds a secret cover — food blogger / backpacker /
   night-owl — tweaking scoring or a small power, revealed at end. *Feels spy:* your cover. *Weight:*
   +0.2. Light and Taiwan-flavourable.

10. **Decrypting dossier (gradual reveal).** Your objective starts coded and **decrypts** as you visit
    regions and flip tiles. *Feels spy:* decode the dossier. *Weight:* +0.2 as a *reveal* (keep it a
    Discovery flip, not real codebreaking, or it balloons).

11. **Planted intel in the shared market (gentle read).** One face-down card in the shared draft each
    round is "planted"; you read which market a rival is circling. *Feels spy:* reading the field.
    *Weight:* +0.2. A softer, market-based cousin of #3 (no accusations).

12. **Covert commit for a contested stall (tug hook).** When two agents want the same hot ingredient/stall,
    both secretly commit transport/"cover budget"; higher secures it, loser gets a consolation tip-off.
    *Feels spy:* a covert op to secure the asset first. *Weight:* +0.2. Because Assignments (#1) are
    hidden, rivals can't read *why* you're fighting — **bluff/read emerges for free, no deduction engine.**

13. **The "extraction" call (push-your-luck-lite).** Choose when to declare your mission complete and
    **extract** (lock your Log). *Feels spy:* nail the extraction window. *Weight:* +0.1–0.2. A shared-
    clock tension valve (Jaipur's "sell now?").

**Taiwan woven through:** Assignments and the Grand Dossier are real regional food legs (a *Tainan
classics* run, a *full night-market crawl in one city*, a *Hakka mountain-town* leg, an *east-coast
Indigenous-cuisine* leg, a *24h convenience-store* dare); recipes tie ingredients to the regions that
supply them; dish names romanised **and** in 繁體; transport mixes HSR / rail / scooter / ferry the way a
real island trip does. Sensitivity: the traveller is a **guest and fan**, dead-drops are *sharing
recommendations*, not *extracting intel* — keep the fiction generous.

---

## 2. Three coherent spine directions

### Direction A — **"Rival Agents, Shared Beat"** (competitive core + genuine co-op layer = semi-co-op) — *lead*
**Blend:** ingredient→dish set collection + small transport economy + **hidden Assignments (#1)** +
**Shared Table Dossier (#7)** + **tip-offs / dead drops (#8)**; **extraction call (#13)** ends it.
**Core loop:** Travel to source the ingredients your secret **Assignment** needs, **plate specific dishes**
into your Log (you score these — competitive). But a face-up **island Grand Dossier** advances whenever
*anyone* plates the dishes it calls for, and each completed stretch pays **the whole table** a Discovery
bonus. You may **dead-drop a tip-off** to a rival (hand them an ingredient/hot-stall lead) — it helps
them, but banks *you* a Fellowship token and nudges the shared Dossier. You choose when to **extract**.
**How the agent layer is load-bearing (not paint):** hidden Assignments make every source-run a
*concealed intention* — rivals can't tell whether your beef-run completes a secret op or is a feint, and
the tip-off/dead-drop is a genuine spy-craft *choice* (cooperate-to-win-the-shared-beat vs hoard-for-your-
Log). Strip the hidden layer and it collapses into the "generic" optimiser we started with. *Load-bearing,
and it delivers all three locked aesthetics at once.*
**Taiwan-specificity hook:** the recipe→region web (from Yes! Ginseng / Taiwan Snackbar) forces real
island routing; the Grand Dossier is a real great-crawl of the island.
**Primary aesthetic:** **Discovery** (lead — the revealing markets + shared Dossier) + **Fellowship**
(the dead-drops and shared bonuses are *real* cooperation, not just "warm rivalry") + **Challenge** (your
own optimisation). Directly answers the CD's competitive-carrying-a-cooperative-layer preference in **one
box, no mode toggle**.
**Main risk:** semi-co-op's classic knife-edge — the tip-off must be *individually rational often enough*
that players actually cooperate, without opening **kingmaking** or an always-optimal "never help anyone"
line that kills the warmth. Plus three subsystems can drift over 1.8 (keep transport tiny, one Assignment).

### Direction B — **"One Core, Two Modes"** (same components run a duel *or* a co-op cell) — *runner-up*
**Blend:** the same ingredient→dish spine, where the **agent hook is the mode switch** — **Duel mode:**
hidden Assignments (#1) + covert contested-stall commits (#12), a head-to-head race. **Co-op mode:** the
table is one **cell** with a shared Dossier (#7) + a Handler (#5) passing constrained tips + dead-drops
(#8), racing the clock together.
**Core loop:** identical board, markets, recipes, and transport; you pick a mode at setup. The dish/
ingredient content and the "secret mission" framing carry both.
**How the agent layer is load-bearing:** in Duel the concealment drives the read; in Co-op the constrained
tip-passing *is* the coordination puzzle. Either way the spy fiction earns rules.
**Taiwan-specificity hook:** same recipe→region web; the co-op Dossier and duel Assignments are both real
island legs.
**Primary aesthetic:** Duel = Challenge + Discovery + warm rivalry; Co-op = Fellowship + Discovery. Serves
the CD's "cleanly supports both a duel and a co-op mode" option literally.
**Main risk:** **two designs to balance** — the agent hook must carry two contexts, doubling the tuning
and threatening the ~1.8 budget with mode-specific rules overhead. Higher total risk than A's single blend;
easy to ship one great mode and one flat one.

### Direction C — **"Cover Stories"** (pure-competitive bluff market grab) — *foil, not recommended*
**Blend:** shared market + covert simultaneous selection (#2) + cover-story bluff (#3/#9).
**Core loop:** each round secretly pick a stall AND play a face-down cover; reveal; feint rivals off your
real target.
**How the agent layer is load-bearing:** the bluff/feint *is* the engine.
**Taiwan-specificity hook:** covers are Taiwan personas (food blogger, backpacker, night-owl).
**Primary aesthetic:** Challenge + a spicier social read — but **Discovery is demoted and the register
tilts to gotcha**, and it has **no cooperative layer at all** — so it fails the CD's blend preference.
Kept only as a contrast case.

---

## 3. Recommendation

**Prototype Direction A — "Rival Agents, Shared Beat" — first.**

**Why:** It is the cleanest expression of the CD's blend brief — a fundamentally **competitive** game
(you race to plate your secret Assignment) that carries a **genuine cooperative layer** (the shared Grand
Dossier + tip-off dead-drops), in **one box with no second mode to tune**. It hits **all three of this
game's own locked aesthetics simultaneously**: Discovery leads via the revealing markets and shared
Dossier, Fellowship is a *real* mechanic (helping a rival can pay you), and Challenge is your own
optimisation. Crucially it is the strongest answer to the original "feels generic" complaint: the recipe→
region food engine (mined from Taiwan Snackbar's hero'd dishes + Yes! Ginseng's ingredient/grade focus)
makes the map Taiwan-shaped rather than "food + map," and the hidden Assignments + dead-drop make the
food-spy fantasy do mechanical work rather than sit on the box.

**Honest trade-off vs the runners-up:**
- **vs B (One Core, Two Modes):** B is *more flexible* — it gives a true stand-alone co-op for co-op
  nights and a sharp duel for duel nights — and reuses the same components. Its cost is **two designs to
  balance**: the agent hook has to carry both contexts, which roughly doubles the tuning burden and is the
  likeliest way to blow the ~1.8 budget or ship one flat mode. A gets the blend in a *single* elegant
  ruleset. **Bridge:** A and B share the exact spine (board, recipes, markets, Assignment deck), so if
  playtests love A's shared layer we can later split it into B's explicit modes cheaply — hand to
  `bg-architect`. Start with A; keep B as the growth path.
- **vs C (Cover Stories):** C carries the most bluff energy but demotes the Discovery lead, tilts warm→
  gotcha, and has **no cooperative layer** — it fails the blend preference outright. Foil only.

**The single riskiest assumption a sim / quick playtest must attack first:**
> *That the cooperative layer (shared Grand Dossier + tip-off dead-drops) creates **genuine, warm
> interaction** — where helping a rival is **individually rational often enough** that players actually
> cooperate — rather than collapsing into a dominant **"hoard, never tip"** line (killing the Fellowship
> the game promises) or **kingmaking** (where tips arbitrarily decide the leader).*

This is semi-co-op's classic failure mode and it decides whether A is a warm blend or a competitive game
with a dead co-op sticker. Attack it cheaply: a `tools/sim` pass pitting a "pure hoarder" strategy against
a "generous tipper" (does hoarding dominate?), then a 2p Screentop/paper session watching whether real
players *feel* like tipping. If the co-op layer can't be made rational, fall back to Direction B's explicit
co-op mode (where cooperation is the win condition, not a temptation) on the same spine.

---

**Decision for the human (A / B / C):** which spine do we commit to designing first?
- **A — Rival Agents, Shared Beat** (**recommended**): competitive core + genuine co-op layer in one box;
  hits all three aesthetics; single ruleset; semi-co-op tuning is the risk.
- **B — One Core, Two Modes**: same components run a duel *and* a co-op cell; maximally flexible; two
  designs to balance is the risk. Natural growth path from A.
- **C — Cover Stories**: pure-competitive bluff; no co-op layer, demotes Discovery — not recommended.
