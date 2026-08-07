# Travel Agents: Taiwan — Rules Draft (v6.2, first-pass outline)

> Skeleton for `bg-developer` / `bg-elegance` to flesh into the real rulebook. **Teach-in-play order.**
> Voice: warm travel-guide / cheerful field-guide (per `identity.md`). Keep it tight —
> `complexity-budget.json` caps the rulebook (1650 words). **Full spec, provenance, the dev-build TODO,
> and all open numbers live in `design/v6.2-content-draft.md` (the LOCKED v6.2 spec)** — this file stays
> lean so the laid-out rulebook's word count reads true. **v6.2 supersedes v6.1's central Ladder / drinks
> fork / off-clock beverages / mission clock / live-retroactive ticket scoring.**

---

## 0. The pitch (read aloud, 20 seconds)
"You're rival **travel agents** building the best Taiwan food **tour** — in one glorious eating day. Ride
the rails between four regions, dig real ingredients out of each region's market (mind the typhoon), and
pile up **Buzz** on the vendors you want. Win a vendor by **out-hyping your rival, on the spot** — each food
vendor you sign makes the next cheaper and climbs your **Prestige** and **Reputation**. Book **Tour
Tickets** — your itinerary — and race to finish them before the day turns over. Every vendor you win pushes
the day toward dusk, then the neon **night market**; when the last train's called, catch it home. Best tour
is **Top Agent**."

## 1. Goal
Score the most points — from your vendors' **Prestige**, your **Reputation** standing, and your **Tour
Tickets** (booked itineraries; win-pile − lose-pile). Most = **Top Agent**.

## 2. Setup (teach while you set up)
1. Unfold the **Taiwan map** — four regions in a ring: **North 北 · Central 中 · South 南 · East 東** (an HSR
   spine links North↔South). The board holds the **day-clock track** (a **dusk** mark and a **last-train**
   mark), the **Prestige track**, the **Reputation track**, and — **per region** — a face-down **vendor
   deck** space with **face-up vendor slots** (**North 2, the others 1**) *and* a face-down **ingredient
   market deck** space. Put each agent's markers at 0 and the day-clock marker at 0.
2. For each region, sort its vendors and ingredients into a **DAY deck** and a **NIGHT deck** (drinks are the
   low-value vendors mixed into each). Set the four **night** vendor decks and **night** ingredient decks
   aside — they arrive at dusk. Shuffle each region's **day vendor deck** and **day ingredient deck**
   face-down into its board space; the ingredient decks are the 5-palette (**N 豬肉 · C 茶 · S 海鮮 · E 米**
   + the common **K 糖** in **C & S** only) salted with **event cards** (mostly hazards, each with a **scope
   tag** — see §6). Fill each region's face-up vendor slot(s) from its day vendor deck. Set out the **Buzz**
   supply (~24 @2p).
3. **Tour Tickets:** shuffle the **daytime** ticket pool, **draw 5** for this game (return the rest to the
   box), and reveal **3** face-up as the shared **ticket row** (the other 2 form its draw pile; a few
   general-pool tickets are shuffled in). Do the same with the **nighttime** pool, set aside for dusk.
4. Each agent: take an **Agent Character** (ability + flaw — read aloud, public) and a **pawn** (start
   opposite at 2p — one North, one South). Your Larder starts empty and stays **face-up** all game.

## 3. How a turn works (the core loop — teach these six, then just play)
On your turn, do **ONE** action. Then if your Larder is over **7** ingredients, discard down to 7 (to that
region's market discard — it reshuffles back in when the deck runs dry; ingredients are never removed from
the game).

- **VISIT THE LOCAL MARKET** *(where you stand)* — flip the top **3** of this region's ingredient deck. Any
  **event** flipped happens now (**by its scope** — see §6), then is discarded. **Keep up to 2** of the
  **ingredients** you turned up; discard the rest. *(The gamble: more events = more swing. This is how you
  bulk-source a region's signature. 大胃王 keeps all 3, but hazards fire twice for him.)*
- **CONVENIENCE STORE** *(anywhere)* — flip the top **1** card of **any** region's ingredient deck. An
  ingredient? Take it. **An event? It fires — by its scope** (⦿ you / ⬢ the region you flipped / ➤ a
  neighbour of it — see §6). *(One blind card, any region, no travel — the reliable way to grab the **common
  K**. It's live: flip a rival's region and a scoped island-hazard can land on **them**; a self-scoped card
  taxes **you**. Cheeky, not a sure thing.)*
- **TRAVEL** — move to a **neighbouring** region (HSR = North↔South), then flip the top **1** card of the
  region you **arrive** in (ingredient → take it; **event → nothing, keep moving** — you're passing through).
  *(媽寶 draws the region she LEFT instead. 里長伯 can't use the HSR.)*
- **PROMOTE** *(with the vendor, in this region)* — place **2 Buzz** from the supply onto **vendor(s) you're
  with in this region**. Buzz stays on the card for all to see; your rival can pile on too. *(網紅 places 3.)*
- **BRIBE A VENDOR** — win a face-up vendor over by out-hyping your rival, **on the spot**. See §4–§5.
  *(Winning any vendor moves the day-clock +1.)*
- **CLAIM A TOUR TICKET** — take one ticket from the face-up **row of 3** (the current phase's pool) and set
  it in front of you as an open commitment; refill the row. You may only claim a ticket you **haven't yet
  completed**. It's scored later into your win-pile / lose-pile (§8–§9).

## 4. Buzz — the hype fight (the heart of it)
Every vendor wants to feel wanted. You show them with **Buzz** — you *promote* them, promising crowds and
hype (that's literally your job as a travel agent: you bring people *to* the food).
- Buzz only ever sits **in the supply** or **on a vendor** — you never keep it in hand.
- To Buzz a vendor you must be **standing in its region**.
- **Both agents can pile Buzz on the same vendor** — that's the fight, and it's where the game is won. (A
  cheap drink is rarely worth fighting over; and because vendors are spread across four regions, you two
  often end up courting different ones.)

## 5. Bribing a vendor (winning it over) — ONE rule for every vendor
To **Bribe** a face-up vendor, you must, all at once:
1. be **with the vendor — in its region**;
2. hold **at least 2 more Buzz on it than your rival** (the majority — checked right now);
3. **pay its ingredients**, *minus your region discounts* (see below).
Then take the vendor to your tour and gain, at once:
- its **Prestige** — move your score marker up now;
- its **Reputation** — move your Rep marker up;
- its **perk** — food vendors carry a **region discount icon** (the ramp); bigger vendors carry stronger
  perks; drinks carry little or none.
Now **clear ALL Buzz on that vendor** (yours *and* your rival's) back to the supply, **refill** the slot from
that region's current deck, and **move the day-clock +1** (§7). The vendor is locked from your rival.

> **The engine (the "aha").** Each **food** vendor carries a **region icon**; every matching icon you hold
> makes that region's ingredients **1 cheaper** on future vendors — sign a couple of Southern stalls and the
> next Southern vendor barely needs oysters. **Drinks** are the cheap, low-conflict grab: worth little (2
> Prestige), no icon, no ramp — great to pad a score or feed a mix ticket, but you can't win on drinks alone.
> **Buzz is never discounted** — so the *hype fight*, not the ingredients, is what gates your next big win.

> **大哥 wins with a slim lead.** The Neighbourhood Big Brother needs only **≥1 more Buzz** than his rival
> (everyone else needs ≥2) — everyone already knows him. He has no offsetting flaw. *(Kits are locked — see
> the design doc.)*

> **Outraced, not robbed.** If your rival out-hypes you and wins a vendor you wanted, your Buzz just fizzles
> back to the supply — you keep every ingredient you sourced, and a fresh vendor comes out. The vendor simply
> chose *them* this time. You out-plan each other; you never seize a place.

## 6. The market decks & events (the island doesn't sit still)
Each region's market is a **face-down deck** of its **signature** ingredient (+ the **common K**, in two of
the four regions) + a few **event** cards (mostly hazards). **Whenever you work a market — a VISIT or a
CONVENIENCE STORE — a flipped event fires straight away, by its scope.** *(A card flipped as you **arrive**
on a Travel is "shelf was bare" — nothing fires.)*
- **hazards** *(the majority)* — a typhoon shuts a road, plum rains slow your haul, a "完售 SOLD OUT" sign,
  scooter gridlock eats your next trip. They **tax or delay — never destroy** what you hold, never cost a
  whole turn.
- **boons** *(the minority)* — a mango glut, a bubble-tea festival that hands out Buzz, a kind auntie who
  loads you up, or — the big one — a vendor **suddenly gets hot** (★ below).

> **The scope tag — who the event hits**, measured from the region the card came out of:
> - **⦿ You** — just the player who flipped it. · **⬢ This region** — everyone standing in the drawn region
>   (and/or its market/road). · **➤ Next door** — someone standing in a neighbouring region.
>
> On a **Visit** you're standing in the region you flipped, so ⬢ tends to hit **you**. On a **Convenience
> Store** you're often elsewhere, so ⬢ hits **whoever's standing in the region you flipped** — flip your
> rival's region and a warm island-hazard can land on **them**. It's the island living its life, never a mean
> personal attack.

> **★ Star vendors — the hot targets.** Some standout night-market names carry a **printed ★** (a real
> Michelin / Bib-Gourmand / competition nod) and score top Prestige — one apex per region, the rotating prize
> both agents chase. And a boon event can drop a **★ Star token** on a vendor, making it worth **+2 Prestige
> / +1 Rep** to whoever wins it — watch a quiet stall suddenly become the thing everyone's racing for.

## 7. The day-clock — Day → Night (every vendor you win moves it)
It's **one glorious eating day**. The **day-clock** climbs **+1 every time anyone Bribes a vendor** — food or
drink, it all counts. It has two marks (2p: **dusk = the 5th table-wide vendor win · last train = the 10th**;
the marks grow with more players):
- **Act I — Daytime 白天:** the morning food + the day's drinks in each region. Cheap, low-contest at first;
  build your discount ramp and stake early positions here. **Daytime Tour Tickets** are on offer.
- **DUSK (the day-clock hits the dusk mark) — the street turns over.** In one thematic flip: **judge every
  claimed DAYTIME ticket** (completed → your win-pile · unfinished → your lose-pile — §9); then **clear the
  entire day layer island-wide** — every face-up **and** face-down **day vendor deck AND day ingredient
  deck** is removed — and replace it with each region's **night decks** (neon recolour; the night ingredient
  decks run **event-heavier** — the bustling night market). Swap the ticket row to the **nighttime** pool.
  **You keep your Larder** — day sourcing still pays into the night. *(Any unclaimed day vendor is gone —
  real Act-I urgency.)*
- **Act II — Night Market 夜市:** the big **night-market stalls** — expensive, neon, fought-over, the ★ apex
  per region. This is where the tour is won.

*(The faster you all win vendors, the faster the day moves — a built-in catch-up: a slow, tall player leaves
the last-train mark further off and gets more turns to reach parity.)*

## 8. Ending the trip — the last train home
When the day-clock hits the **last-train mark** (2p: the **10th vendor win**), **night falls and the night
market winds down**: everyone catches the last train. **Finish the current round**, play **one more full
round**, and stop. *(If a region's deck empties, its face-up slot simply isn't refilled until the next flip;
if all decks dry island-wide, the phase ends then — the deck-exhaustion backstop. Reaching the top of
Reputation scores its reward but does not end the game. Order of operations: if one win trips **dusk and**
the last train at once, resolve **dusk first**, then the end check.)*

## 9. Scoring — reveal your piles and tally once
Your markers already show your two live vectors; Tour Tickets are settled into two piles (daytime at dusk,
nighttime + general at the last train). Total:
1. **Prestige** — the sum of your vendors' values (already on your track).
2. **Reputation** — score the VP for your **final** position **only** (not cumulative): 3–5 → **+2** · 6–8 →
   **+4** · 9–11 → **+6** · 12 → **+9**.
3. **Tour Tickets** — **+the printed value of each ticket in your WIN pile**, then **−floor(value ÷ 2) for
   each ticket in your LOSE pile** (half its own value, rounded down). *(This is the whole ticket score,
   tallied once — nothing was added or subtracted during play.)*
Most points wins → **Top Agent**. **Ties:** highest Reputation, then most vendors, then most regions covered.

## 10. The warm-tone reminders (margin asides, not rules)
- You're a travel agent **promoting** Taiwan's food — winning a vendor means out-hyping your rival to earn
  their blessing, never taking from them or the place. "Bribe" is the cheeky word; the deed is a warm hard
  sell, not corruption.
- Events are the island living its life — festivals, weather, kind locals — never sacred customs for laughs.
  When a Convenience-Store event lands on your rival, it's the *island* doing it (a typhoon, a queue, a
  sold-out sign) — a shared groan, a cheeky "ooh, bad luck," never a spiteful strike.
- Dish/vendor names stay real (Tâi-lô + 繁體). The comedy is the caper gag and your own gluttony.

---

## Teaching sequence (FTUE — the order a first game should reveal rules)
1. **Goal + one Vendor** — "here's a stall in the North; it wants 2 pork, and whoever hypes it most (by 2
   Buzz) while standing here wins it. Let's go get it."
2. **Visit / Convenience Store / Travel** — dig the North market for its signature; note that events fire *by
   their scope* (point at the ⦿/⬢/➤ tag) when you Visit or hit the Convenience Store; grab a card; move.
3. **Promote** — drop Buzz on the stall; "your rival can pile on too — this is the fight."
4. **Bribe** — in-region, ahead by 2 Buzz, pay the ingredients → win it: Prestige moves, Rep moves, point at
   its **region icon** ("your first North discount"). Its Buzz clears; **the day-clock ticks +1**.
5. **The ramp** — win a second North vendor and *watch the ingredients cost less* (Buzz still full).
6. **Drinks** — point at a cheap drink: "low value, no icon, no ramp — a quick grab to pad your score or feed
   a mix ticket, but you can't win on drinks alone. It still ticks the day-clock like any vendor."
7. **Tour Tickets** — "your itinerary. Book one from the row; finish it before its phase closes or it drops
   to your lose-pile at half value. Book bold, or play it safe."
8. **The hype fight** — the first time you both stack Buzz on one vendor: "out-commit, race to the
   ingredients, or concede and take another. Outraced, not robbed."
9. **Reputation** — the second live track; "several ways to win — go tall, climb your Rep, chase tickets."
10. **Dusk → the Night Market** — introduce at the dusk flip: "the day judges your daytime tickets, the
    street turns over to neon, the big names arrive — and night's coming, so don't miss the last train."
