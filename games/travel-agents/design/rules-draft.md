# Travel Agents: Taiwan — Rules Draft (v6, first-pass outline)

> Skeleton for `bg-developer` / `bg-elegance` to flesh into the real rulebook. **Teach-in-play order.**
> Voice: warm travel-guide / cheerful field-guide (per `identity.md`). Keep it tight —
> `complexity-budget.json` caps the rulebook (1650 words). **Full spec, provenance, the dev-build TODO,
> and all open numbers live in `design-doc.md` (v6)** — this file stays lean so the laid-out rulebook's
> word count reads true.

---

## 0. The pitch (read aloud, 20 seconds)
"You're rival **travel agents** building the best Taiwan food **tour** — in one glorious eating day. Ride
the rails, dig real ingredients out of each region's market (mind the typhoon), and pile up **Buzz** on the
vendors you want. Win a vendor by **out-hyping your rival, on the spot** — each ladder stall you sign makes
the next cheaper and pushes you up your **Prestige** and your **Reputation**. Take the high road (the
contested **Breakfast Run → Night Market** ladder) or bank quick easy points at the **all-day drinks
stands**. Play the day into the night; when the night market winds down, catch the last train home. Chase
your **secret signature tour** (+7). Best tour is **Top Agent**."

## 1. Goal
Score the most points — from your vendors' **Prestige**, your **Reputation** standing, and your **secret
signature mission** (+7, revealed at the end). Most = **Top Agent**.

## 2. Setup (teach while you set up)
1. Unfold the **Taiwan map** — four regions in a ring: **North 北 · Central 中 · South 南 · East 東** (HSR
   links North↔South). The board holds the **day-clock** (with a **dusk** mark and a **last-train** mark),
   the **Prestige track**, the **Reputation track**, the central **Ladder** display, and — **per region** —
   a face-down **market deck** space *and* a persistent **beverage slot** (a drinks stand in every region).
   Put each agent's markers at 0 and the **day-clock** at 0.
2. Build the **four region market decks**: each region's **one signature ingredient** (several copies) +
   the **common ingredient** *(only in the two regions that carry it)* + its **event cards** (mostly
   hazards; each carries a **scope tag** — see §6), shuffled face-down. Set out the **Buzz** supply (~24 @2p).
3. Build the **three vendor decks** and stock the board:
   - **The Ladder** (the contested, clock-driving central display): deal from the **Act I · Breakfast Shop
     deck** to fill it (2p: **4 slots**). *(The **Night-Market deck** waits face-down for dusk.)*
   - **The region beverage slots** (persistent, all-day): seed **one beverage shop face-up into each
     region's slot** from the **Beverage Shop deck** (2p: 4 dealt, one per region). Never swept.
4. Each agent: take an **Agent Character** (ability + flaw — read aloud, public) and a **pawn** (start
   opposite at 2p — one North, one South). **Draw 3 Mission cards, secretly keep 1** (+7); return 2
   face-down. Your Larder starts empty and stays **face-up** — your mission is the only hidden thing.

## 3. How a turn works (the core loop — teach these five, then just play)
On your turn, do **ONE** action. Then if your Larder is over **7** ingredients, discard down to 7.

- **VISIT THE LOCAL MARKET** *(where you stand)* — flip the top **3** of this region's market deck. Any
  **event** flipped happens now (**it fires by its scope** — see §6), then is discarded. **Keep up to 2** of
  the **ingredients** you turned up (usually your region's **signature**); discard the rest. *(The gamble:
  more events = more swing. This is how you bulk-source signatures.)*
- **CONVENIENCE STORE** *(anywhere)* — flip the top **1** card of **any** region's market deck. An
  ingredient? Take it. **An event? It fires — by its scope** (⦿ you / ⬢ the region you flipped / ➤ a
  neighbour of it — see §6). *(One blind card, any region, no travel — the reliable way to grab the
  **common** ingredient your **drinks** run on. It's now **live**: flip a rival's region and a scoped island-
  hazard can land on **them** — but a self-scoped card taxes **you**, and you can't see the top card. Cheeky,
  not a sure thing.)*
- **TRAVEL** — move to a **neighbouring** region (HSR = North↔South), then flip the top **1** card of the
  region you **arrive** in (ingredient → take it; **event → nothing, keep moving** — you're passing through,
  not working the market).
- **PROMOTE** *(with the vendor, in this region)* — place **2 Buzz** from the supply onto **vendor(s) you're
  with in this region**: a **ladder** vendor here, and/or **this region's beverage slot**. Buzz stays on the
  card for all to see; your rival can pile on too. *(You Promote the drinks stand where you stand — like any
  vendor.)*
- **BRIBE A VENDOR** — win a vendor over by out-hyping your rival, **on the spot**. See §4–§5. *(Winning a
  **ladder** vendor moves the day-clock; winning a **beverage** does not.)*

## 4. Buzz — the hype fight (the heart of it)
Every vendor wants to feel wanted. You show them with **Buzz** — you *promote* them, promising crowds and
hype (that's literally your job as a travel agent: you bring people *to* the food).
- Buzz only ever sits **in the supply** or **on a vendor** — you never keep it in hand.
- To Buzz **any** vendor you must be **standing in its region** — a ladder vendor here, or the beverage
  stand in this region. *(One rule, every vendor type.)*
- **Both agents can pile Buzz on the same vendor** — that's the fight (and on the ladder it's where the
  game is won; drinks are rarely worth fighting over, and since a stand sits in every region you two usually
  end up at different ones).

## 5. Bribing a vendor (winning it over)
To **Bribe** a Board vendor, you must, all at once (**one rule for every vendor type**):
1. be **with the vendor — in its region** (a ladder vendor here, or this region's beverage stand);
2. hold **at least 2 more Buzz on it than your rival** (the majority — checked right now);
3. **pay its ingredients**, *minus your region discounts* (see below).
Then take the vendor to your tour and gain, at once:
- its **Prestige** — move your score marker up now;
- its **Reputation** — move your Rep marker up;
- its **perk** — for ladder vendors, usually a permanent **region discount icon** (bigger vendors carry
  stronger perks); beverages carry little or none.
Now **clear ALL Buzz on that vendor** (yours *and* your rival's) back to the supply — the deal's done, the
hype's spent. **Refill** the slot from the matching deck. **If it was a breakfast or night-market (ladder)
vendor, move the day-clock +1** (see §7). **A beverage win does NOT move the day-clock.**

> **The two roads (the "aha").** The **ladder** — breakfast shops now, night-market stalls later — is the
> high road: contested, region-gated, and it *drives the day forward*. Its payoff is the **ramp**: each
> ladder vendor carries a **region icon**, and every matching icon you hold makes that region's ingredients
> **1 cheaper** on future vendors — sign a couple of Southern stalls and the next Southern vendor barely
> needs oysters. The **drinks stands** are the easy road: there's **one in every region**, cheap (just the
> common ingredient off the convenience store), low-conflict, always open — so you grab the stand **right
> where you already are** (you never travel *for* a drink) for a steady trickle of easy points that *doesn't*
> move the clock. Great for padding your score and hedging a lost fight — but they don't ramp and can't
> reach the big night-market names, so you can't win on drinks alone. **Buzz is never discounted** — so as
> the ladder ramps, the *hype fight* (not the ingredients) becomes the thing that gates your next big win.

> **大哥 wins at a tie.** The Neighbourhood Big Brother needs only to **match or lead** his rival's Buzz on
> a vendor (no +2 lead) — everyone already knows him — but each Bribe costs him **+1 ingredient** (he picks
> up the tab). *(These numbers are being tuned — see the design doc.)*

> **Outraced, not robbed.** If your rival out-hypes you and wins a vendor you wanted, your Buzz just
> fizzles back to the supply — you keep every ingredient you sourced, and a fresh vendor comes out. The
> vendor simply chose *them* this time. You out-plan each other; you never seize a place.

## 6. The market decks & events (the island doesn't sit still)
Each region's market is a **face-down deck** of its **signature ingredient** (+ the **common** ingredient,
in two of the four regions) + a few **event** cards (mostly hazards). **Whenever you work a market — a
VISIT or a CONVENIENCE STORE — a flipped event fires straight away, by its scope.** *(Only a card flipped
as you **arrive** on a Travel just means "shelf was bare" — nothing fires.)*
- **hazards** *(the majority)* — a typhoon shuts a road, plum rains slow your haul, a "完售 SOLD OUT" sign,
  scooter gridlock eats your next trip. They **tax or delay — never destroy** what you already hold, never
  cost a whole turn.
- **boons** *(the minority)* — a mango glut, a bubble-tea festival that hands out Buzz, a kind auntie who
  loads you up, or — the big one — a vendor **suddenly gets hot** (see ★ below).

> **The scope tag — who the event hits.** Every event carries a small icon that says who it lands on,
> **measured from the region the card came out of**:
> - **⦿ You** — just the player who flipped it (a personal boon or tempo tax).
> - **⬢ This region** — everyone **standing in the region you drew from** (and/or that region's market/road).
> - **➤ Next door** — someone standing in a **neighbouring** region.
>
> On a **Visit** you're standing in the region you flipped, so ⬢ tends to hit **you** (and any rival here).
> On a **Convenience Store** you're often somewhere else, so ⬢ hits **whoever's standing in the region you
> flipped** — flip your rival's region and a warm island-hazard can land on **them**. It's the island living
> its life and pushing everyone around — never a mean personal attack, always a typhoon/crowd/sold-out beat.

> **★ Star vendors — the hot targets (on the ladder).** Some standout **night-market** names carry a
> **printed ★** (a real Michelin / Bib-Gourmand / competition nod) and score **7–8 Prestige** — the apex
> prizes both agents fight over. And a boon event — **摘星了！ Michelin Nod / 得獎了！ Just Won the
> Competition** — drops a **★ Star token** on a **Ladder** vendor (usually the most-ignored one), making it
> worth **+2 Prestige and +1 Rep** to whoever wins it. Watch a quiet little stall suddenly become the thing
> everyone's racing to — pack your bags and out-hype your rival for it. *(The drinks stands stay steady —
> the ★ swing lives on the ladder.)*

## 7. The day-clock — Day → Night (the day escalates)
It's **one glorious eating day**. The **day-clock** climbs **+1 every time anyone Bribes a breakfast or
night-market (ladder) vendor** — a **beverage** win never moves it. It has two marks:
- **Act I — The Breakfast Run 早餐:** the morning food — cheap **breakfast shops** on the Ladder. Easy and
  low-contest; build your discount ramp here. *(The drinks stands run alongside, all day.)*
- **DUSK (the day-clock hits the dusk mark, 2p: the 4th ladder win):** the breakfast places are closing.
  **Sweep** any unwon Ladder vendors (their Buzz returns to the supply) and re-stock the Ladder from the
  **Night-Market** deck. Move to **Act II**. *(The region beverage slots are NOT swept — drinks are all
  day, in every region.)*
- **Act II — Night Market 夜市:** the big **night-market stalls** — expensive, neon, fought-over. This is
  where the ladder game is won.

*(The faster you all win ladder vendors, the faster the day moves — a built-in catch-up: a slow, tall
player leaves the last-train mark far off and gets more turns to reach parity. Grinding drinks doesn't
hurry the night along.)*

## 8. Ending the trip — the last train home
When the day-clock hits the **last-train mark** (2p: the **7th ladder win** — 3 into the Night Market),
**night falls and the night market winds down**: everyone catches the last train home. **Finish the current
round**, play **one more full round**, and stop. *(No end-game action and no alarm — the day-clock paces
the game, and when night's over the tour's done. If the Night-Market deck ever empties first, the last
train leaves then; if the Breakfast deck empties, dusk falls then. Reaching the top of Reputation scores
its reward but does not end the game.)*

## 9. Scoring (reveal signature missions now!)
Your markers already show your two live vectors. Total:
1. **Prestige** — the sum of your vendors' values (already on your track).
2. **Reputation** — score the VP for your **final** position **only** (not cumulative): 3–5 → **+2** · 6–8
   → **+4** · 9–11 → **+6** · 12 → **+9**.
3. **Signature mission** — flip it: **+7** if you pulled off its pattern, else 0. *(Some missions reward a
   grand tour across all four regions — the breadth reward; others reward a stack of drinks stands or a
   couple of big night-market names.)*
Most points wins → **Top Agent**. **Ties:** highest Reputation, then most vendors, then most regions
covered.

## 10. The warm-tone reminders (margin asides, not rules)
- You're a travel agent **promoting** Taiwan's food — winning a vendor means out-hyping your rival to earn
  their blessing, never taking from them or the place. "Bribe" is the cheeky word; the deed is a warm hard
  sell, not corruption.
- Events are the island living its life — festivals, weather, kind locals — never sacred customs for
  laughs; local characters are warm, real people. When a Convenience-Store event lands on your rival, it's
  the *island* doing it (a typhoon, a queue, a sold-out sign) — a shared groan, a cheeky "ooh, bad luck,"
  never a spiteful strike.
- Dish/vendor names stay real (Tâi-lô + 繁體). The comedy is the mission gag and your own gluttony.

---

## Teaching sequence (FTUE — the order a first game should reveal rules)
1. **Goal + one Vendor** — "here's a breakfast stall; it wants 2 North ingredients, and whoever hypes it
   most (by 2 Buzz) while standing here wins it. Let's go get it."
2. **Visit / Convenience Store / Travel** — dig the North market for its signature; note that events fire
   *by their scope* (point at the ⦿/⬢/➤ tag) when you Visit or hit the Convenience Store; grab a card; move.
3. **Promote** — drop Buzz on the stall; "your rival can pile on too — this is the fight."
4. **Bribe** — in-region, ahead by 2 Buzz, pay the ingredients → win it: Prestige moves, Rep moves, point
   at its **region icon** ("your first North discount"). Its Buzz clears; the day-clock ticks.
5. **The ramp** — win a second North vendor and *watch the ingredients cost less* (Buzz still full).
6. **The drinks fork** — point at the beverage stand in this region: "there's one in *every* region, so you
   grab the one where you already stand — cheap off the convenience store, low-fuss easy points that *don't*
   move the clock. Same on-site Bribe rule as any vendor. Great for padding, but they don't ramp and can't
   reach the big names."
7. **The hype fight** — the first time you both stack Buzz on one ladder vendor: "out-commit, race to the
   ingredients, or concede and take another. Outraced, not robbed."
8. **Reputation** — the second live track; "several ways to win — go tall, climb your Rep, or grind drinks."
9. **Signature mission** — "your secret +7 tour; keep it face-down."
10. **Dusk → the Night Market** — introduce when the Ladder first turns over: "the breakfast places are
    closing; the big neon names arrive — and night's coming, so don't miss the last train."
