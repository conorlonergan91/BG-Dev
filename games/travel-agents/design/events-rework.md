# Market Events — Comedy + Fun Rework (bg-theme)

> **Job:** the CD found the 11 Market Event tiles *too boring — not fun or funny enough.* This reworks
> the **flavour + fun** of the set (I own event flavour & experiential coherence). `bg-design` is
> rebalancing vendors + a Steal action in parallel — I did **not** respec the core. Effects marked
> **[FLAG]** carry a juicier payload that needs `bg-design`/`bg-developer` to sanity-check; everything
> else reuses payloads the design doc already lists.
>
> **This is NOT the data file.** `bg-developer` implements the funny-but-mechanically-sound set into
> `components/events.csv`. Wording on all Chinese/Tâi-lô text → the paid Taiwanese consultant before lock.

## What was wrong (the diagnosis)
The old set is *flavourless boons/hazards* — "Add 2 tokens," "take 1 oyster," "take 2 Buzz." Correct
mechanically, zero personality, and **no decision**: nothing to grin at, nothing to gamble on, no
moment. The identity's whole comedy well (the 40-deep queue, the aunty who won't let you leave, 24-hour
convenience-store culture, the stinky-tofu dare, the HSR sprint, typhoon day = everyone stays in and
eats) was sitting unused. This rework mines that well and adds a **bit of decision or swing** to each —
a choice, a gamble, a race, or a catch-up — inside the design's existing rules.

## Rules I stayed inside (from design-doc v3 §Market & Events)
- **Fire on refill** (drawn on a Stock Up / Travel refill, resolves on the spot).
- **Tax-not-destroy** — hazards **delay / reroute / tempo-tax**; they never remove what you *hold* or
  cost a whole turn. The shelf resets, never your larder.
- **Region-thematic**, **boon-skewed ~60/40** (`bg-developer`: tune the final ratio; see tally below).
- **Payloads events may carry** (per doc): add/free specialty tokens · free/± Buzz · table-wide next-Promote
  buff · free move · +Prestige to a face-up vendor · wash/reroute a Market · Stock-Up tempo tax · clear+refill a row.

## HARD sensitivity rails I held (binding — I own these)
- **Secular.** Zero temple / deity / ghost-month / funerary content. All comedy is food fairs, fruit
  seasons, weather, roads, crowds, media, and warm locals. (I deliberately **avoided 尾牙/辦桌**-type
  banquets that can carry religious association, and **omitted betel-nut** entirely — cleanest call.)
- **Locals are warm, dignified people, never punchlines/obstacles-as-caricature.** The aunty is
  *generous*, not a doddering gag; the blogger genuinely loves the food; the queue-crowd is the joke
  *with* them, not at them.
- **The comedy is the players' own gluttony/indecision, the absurd "mission" gag, and affectionate
  specifics** — never mocking the place, the language, or "weird foreign food" (stinky tofu = *the
  locals are right*, never "ew"). **Dish/place names stay real** (蚵仔煎, 珍珠奶茶, 臭豆腐, 便當, 左營, HSR…).

---

## The reworked set (13 core + 2 optional swaps)

Voice = the over-enthusiastic travel-buddy / head-office earpiece. Each tile gets a **funny name +
one-line flavour + region/trigger + effect**.

### Boons — regional windfalls (now with a choice)

**1 · 芒果季 Mango Season** *(South · boon · +choice)*
> *"The whole coast smells like a smoothie. Head office is weeping with joy into the earpiece."*
- **Effect:** the drawer **chooses**: *gorge now* — take **1 free South specialty** — **or** *let it
  ride* — dump **2 extra South specialty tokens** into the South Market (a glut you both race for).
- *Adds a small decision to the blandest old tile (E01). Both payloads already exist — trivial for dev.*

**2 · 蚵仔盛產 Oyster Glut** *(South · boon)*
> *"The tidal flats delivered. Every 蚵仔煎 griddle on the coast is sizzling at once — follow the smell."*
- **Effect:** the drawer takes **1 free oyster token**. *(Old E02, funnier voice.)*

**3 · 珍奶節 Bubble-Tea Festival** *(Central · boon · +choice)*
> *"They're handing out pearls like confetti. Somebody's already on their fourth cup. It's you."*
- **Effect:** the drawer **chooses** — take **2 Buzz** (the town's buzzing) **or 1 free Central
  specialty** (a fistful of pearls). *(Old E03 + a clean two-currency choice.)*

**4 · 豐收 Bumper Harvest** *(East · boon)*
> *"The terraces came in heavy this year. The farmer insists you take a bag. Then another bag."*
- **Effect:** the drawer takes **2 free East specialty tokens**. *(Old E04, warm dignified framing —
  the East grower is a proud host, not scenery.)*

### Boons — warm locals & 24-hour culture (the heart of the comedy)

**5 · 再吃一點啦！The Aunty Insists** *(any · boon)*
> *"You said you were full three plates ago. She has already reached for the ladle. You do not get a vote."*
- **Effect:** the drawer takes **2 free ingredients** from their **current region's** Market ("seconds").
- *New tile — the identity's flagship warm-local gag, made mechanical. She's generous, never a punchline.*

**6 · 深夜的便利商店 The 4 a.m. Convenience Store** *(any · boon)*
> *"You weren't hungry. You bought a 茶葉蛋 anyway. The whole island runs on this exact decision."*
- **Effect:** the drawer takes **1 free ingredient** (current specialty **or** pantry) **+ 1 Buzz**.
- *New tile — 24-hour convenience-store culture, the identity's own well. Small mixed windfall.*

**7 · 臭豆腐大挑戰 The Stinky-Tofu Dare** *(any · boon · GAMBLE)* **[FLAG bg-design/dev]**
> *"Smells wild. Tastes incredible. The locals are right — the only question is whether you're brave."*
- **Effect:** the drawer **MAY take the dare** — reveal the **top tile of their current region's
  supply**. **Specialty?** Take it **free + 1 Buzz** (brave; it paid off). **Another Event?** You queued
  into chaos — **resolve it now too** (you asked for it). **Decline** = play it safe, take **1 Buzz**.
- **[FLAG]** push-your-luck that **chains a reveal/resolution** — needs dev to confirm the extra flip is
  clean (worst case is just another boon-skewed event; still tax-not-destroy). The set's one real gamble.

### Boons — hype, crowds & the HSR (movement + swing)

**8 · 高鐵衝刺 The 3:47 to Zuoying** *(any · boon · movement)*
> *"Doors closing. 便當 in one hand, dossier in the other. This is the most secret-agent you will ever feel."*
- **Effect:** the drawer may **immediately move 1 region for free** (HSR counts North↔South adjacent).
- *Old E06's payload, re-skinned to the HSR-sprint gag the identity begs for (左營 = the real Kaohsiung terminus).*

**9 · 快閃排隊 The Queue That Ate the Block** *(any · boon)*
> *"Forty people deep and growing. Nobody's sure what it's for. Everybody's certain they need it."*
- **Effect:** the **cheapest face-up T1 vendor gains +1 Prestige** (the queue makes it a must-book —
  a race: whoever courts it first cashes the hype). *(Old E07, funnier — and the +Prestige is a live
  race between the two agents.)*

**10 · 網紅來了 The Food Blogger's Big Break** *(table-wide · boon)*
> *"Someone's reel just hit a million views. The whole town is buzzing — and mildly performing for the camera."*
- **Effect:** **every agent's next Promote gives +1 Buzz.** *(Old E05's payload; the food-blogger skin is
  warmer and funnier than "tour bus." The blogger loves the food — affectionate, self-aware, never contempt.)*

### The catch-up beat (everyone-but-the-leader)

**11 · 颱風假 Typhoon Day** *(table-wide · catch-up + reroute)* **[FLAG bg-design/dev]**
> *"School's cancelled. Offices shut. The entire island orders 泡麵 and 鹹酥雞 and doom-scrolls 美食 pics.
> Head office groans down the phone. You, secretly, are thrilled."*
- **Effect:** the **coastal (S/E) Market's face-up specialties wash out and refill** (a reroute — you
  lose nothing you hold), **and** everyone's stuck indoors eating: **every agent *except* the current
  Prestige leader takes 2 Buzz** (word of mouth spreads while you snack).
- **[FLAG]** the catch-up half is a **new payload shape**: "leader = agent furthest along the **public,
  live VP/Prestige track**; if tied for the lead, **all** agents benefit." Gentle, on-identity (a comic
  inconvenience with a silver lining, never peril), and matches the doc's *"catch-up valve, not
  leader-bashing."* Reworks the old E09 typhoon into something with warmth **and** a swing.

### Hazards — comic inconveniences (tax-not-destroy, kept warm)

**12 · 梅雨 Plum Rains** *(Central · hazard)*
> *"Grey drizzle, damp everything, and a scooter seat you'll regret sitting on. A slow, soggy snack day."*
- **Effect:** the drawer's **Stock Up this turn yields 1 fewer** (tempo tax). *(Old E10, funnier voice.)*

**13 · 完售！Sold Out** *(any · hazard)*
> *"'完售' — the most heartbreaking word in the language. The last plate went to the person in front of you.
> They are not sorry."*
- **Effect:** **reroute** — discard **1 face-up specialty** from the current region's Market and refill
  it (the stall you were eyeing just sold out). **You lose nothing you hold.**
- *New tile — a warm, universal food-FOMO hazard. Tax-not-destroy; the shelf moves, your larder doesn't.*

### Optional swap-ins (so `bg-developer` can land on 11 or tune the boon/hazard ratio)

**14 · 機車陣 Scooter Gridlock** *(North/any · hazard)*
> *"Ten thousand scooters at one red light, all revving. Beautiful. Deafening. You are not going anywhere fast."*
- **Effect:** the drawer's **next Travel arrives with no ingredient** (the gridlock ate your time — a
  tempo tax, not a lost turn). *(Warm scooter-swarm gag; adds a hazard toward the 60/40 skew.)*

**15 · 客滿 Fully Booked** *(any · shakeup)*
> *"'客滿' hung across the door. Could be a disaster. Could be exactly the table you needed. Roll with it."*
- **Effect:** clear and refill an **entire Market row** (can help or hurt). *(Old E11 — the one true neutral shakeup.)*

---

## Boon/hazard tally & the 60/40 note (for `bg-developer`)
Core 13 as written skews **boon-heavy** (10 boons + 1 catch-up/reroute + 2 hazards) — deliberately warm.
The doc asks for **~60/40 boon/hazard**. To hit that, land **11** as: keep all boons that carry the
identity (Aunty, Convenience Store, Stinky-Tofu Dare, HSR, Queue, Blogger, + 2 regional windfalls) and
run **4 hazard-flavoured** tiles — **Plum Rains + Sold Out + Scooter Gridlock (#14) + Typhoon Day**
(Typhoon's reroute half is the hazard, its Buzz half the catch-up). That's ~7 boon / ~4 hazard-ish + the
occasional shakeup — the warm register **and** the 60/40 spice. Final ratio is `bg-design`'s call on feel.

## Effects needing `bg-design`/`bg-developer` sign-off (the only two)
- **#7 Stinky-Tofu Dare** — chains an extra reveal/resolution (push-your-luck). Confirm the flip is clean.
- **#11 Typhoon Day** — "everyone but the Prestige leader" is a new payload shape (needs a leader
  definition off the live/public VP track + a tie rule). Everything else reuses listed payloads.

## Coherence verdict (my lane)
All 13 land the **over-enthusiastic-travel-buddy** register, all are **secular**, all treat locals as
**dignified people**, and the comedy is **players' own gluttony/indecision + affectionate specifics**,
never at Taiwan. Dish/place names are real. This is the felt identity the tone section demands —
**still coherent**, now actually *fun*.
