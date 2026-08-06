# Travel Agents: Taiwan — Rules Draft (first-pass outline)

> A skeleton for `bg-developer` / `bg-elegance` to flesh into the real rulebook. **Teach-in-play order.**
> Voice: warm mission-dossier / over-caffeinated tour-guide (per identity.md). Keep it tight —
> `complexity-budget.json` caps the rulebook at **1100 words**. Detail lives in `design-doc.md`.

---

## 0. The pitch (read aloud, 20 seconds)
"You're a food-obsessed *travel agent* on a top-secret snack mission across Taiwan. Ride the rails,
source real ingredients from the regions that actually grow them, and plate the island's greatest
dishes into your Traveller's Log. You've got a **secret Assignment** — but sometimes the smart move is
to tip off a rival, because a good deed banks *you* a favour and pushes the whole table's Grand Tour
forward. Best trip wins."

## 1. Goal
Score the most points from **plated dishes**, your **secret Assignment**, and the shared **Grand
Dossier** bonuses everyone earns together. Highest **Traveller's Log** wins.

## 2. Setup (teach while you set up)
1. Unfold the **Taiwan map** — four regions in a ring: **North 北 · Central 中 · South 南 · East 東**
   (the HSR line links North–Central–South down the west coast). Put the **Grand Dossier** marker at 0
   and the **score** markers at 0.
2. Stock the ingredient supply: **each region's two specialties** by that region, plus the **pantry**
   pile (the convenience store — available anywhere). Put the **Insider Tip** tokens nearby.
3. Shuffle the **Dish deck**; deal a **Menu** of **4** face-up (5 at 3p, 6 at 4p).
4. Each agent: take a **pawn** (start on **opposite** regions at 2p — one North, one South), **draw 2
   Assignments, keep 1 secret**, return the other. Your Larder starts empty and stays **face-up in the
   open** — the Assignment is the only thing you keep hidden.

## 3. How a turn works (the core loop — teach these five, then just play)
Your **Larder** (the ingredients you're carrying) sits **face-up in the open** in front of you all game —
there's no hidden hand; the *only* secret in the game is your Assignment. On your turn, do **ONE** action.
Then if your Larder is over **7 ingredients**, discard down to 7.

- **STOCK UP** — take **2 ingredients** where you stand (this region's specialties and/or pantry).
- **TRAVEL** — move to a **neighbouring** region, then take **1 ingredient** there. (North↔South is a
  neighbour by HSR.)
- **PLATE** — pick a **Menu** dish you can pay for, spend its recipe from your Larder, and lay the Dish
  card in your **Traveller's Log**. Refill the Menu. **Advance the Grand Dossier +1.**
- **DEAD-DROP** *(the tip-off)* — hand **1 ingredient to a rival** ("you *have* to try this"). **Score +1
  VP**, take **1 Insider Tip** for yourself, and **advance the Grand Dossier +1**. *(3–4p: a player can
  receive only one Dead-drop per round.)*
- **EXTRACT** — belly full, wallet empty, you sprint to **catch the last HSR home** before it pulls out of
  the station: declare your trip done and trigger the end-game (see §6). *(The one "spy" word that sounds
  dramatic — it's really just "I'm stuffed, let's go home.")*

> **Insider Tips** (spend anytime, free): pick one — take **1 extra ingredient** here · treat **1 recipe
> ingredient as any type** when plating · **travel 1 extra** region.

## 4. Sourcing & recipes (the "aha": travel because the food lives there)
- You can only take a region's **specialty** while you're **in** that region — oysters in the South, tea
  in the Central hills, rice & mountain greens in the East, beef & pork in the North.
- **Pantry** supplies are at the convenience store in **every** region.
- A **Dish** is a little recipe of 2–3 named ingredients. To plate the Chishang bento you need East rice
  *and* Northern pork — so you travel. *(That's the whole game in one sentence.)*

## 5. The Grand Dossier (the shared beat)
Every **Plate** and every **Dead-drop** nudges the shared marker **+1**. When it crosses a **milestone**,
**every player** scores that **Discovery bonus** (a rising tide — we did the tour together!), **and** the
player who pushed it over picks a small reward: **an Insider Tip *or* +1 VP**. The **final milestone** can
end the game (§6).

*(Milestones at 4/8/12/16 for 2p; scale up at higher counts — see design-doc.)*

## 6. Ending the trip
The end-game begins the moment **either**: a player takes **EXTRACT** (catches the last HSR home), **or**
the **Grand Dossier** hits its **final milestone**. Then: **finish the current round**, play **one more
full round**, and stop.

## 7. Scoring (reveal Assignments now!)
Add up your **Traveller's Log**:
1. **Dishes** — 3 VP (2-ingredient) · 4 VP (3-ingredient) · 5 VP (Signature).
2. **Assignment** — **+7** if you pulled it off (flip it face-up), else 0.
3. **Dead-drops** — **+1 VP for each Dead-drop you made** (that's why sharing pays).
4. **Grand Dossier** — the flat Discovery bonuses you banked along the way, plus any **+1 VP** you took
   as a triggerer's pick (Insider Tips are leverage — they're worth 0 VP now).
Most points wins. **Ties:** most dishes, then most regions visited.

## 8. The warm-tone reminders (margin asides, not rules)
- Dead-drops are *recommendations*, not thefts — you're a fan sharing the good stuff.
- Dish names stay real (romanised + 繁體). The comedy is the mission gag and your own gluttony — never
  the food or the place.

---

## Teaching sequence (FTUE — the order a first game should reveal rules)
1. **Goal + one dish** — "here's beef noodle; it needs beef (North) + a pantry staple. Let's get it."
2. **Stock Up / Travel** — source the two ingredients; feel the "travel because the food's there" turn.
3. **Plate** — score it, nudge the Grand Dossier; point at the shared bonus track.
4. **Assignment** — "here's your secret mission; it shapes which dishes you chase."
5. **Dead-drop** — first time someone's Larder is full: "rather than discard, tip a rival — you get an
   Insider Tip and push the tour." (This is the teachable moment for the co-op layer.)
6. **Extract / end-game** — introduce once the Dossier is ~half full.

## Still to specify (→ `bg-developer`)
- Exact Dish deck (24 cards) + Assignment deck (14–16) as component data (CSV).
- Final ingredient supply counts; Insider Tip token count.
- Player-aid card (≤16 lines) — the five actions + Insider Tip uses + end-trigger.
- Iconography for 9 ingredients + 4 regions (dual-coded colour **and** emblem — `bg-access`).
