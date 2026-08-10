# Travel Agents: Taiwan — Content & Story Ideas (Events · Vendors · Bookings)

> **Purpose.** A living capture of the **Creative Director's creative-content ideas** for the three
> "content decks" — what the cards ARE (their story/flavour) and the mechanics the CD wanted them to
> express. This is a **backlog + record of intent**, not a spec: some ideas are fully realised in the
> component data (marked ✓), some partial (~), some still open for V8 / expansions (○). It exists so the
> creative vision has one home and nothing gets lost between iterations.
>
> **Cross-refs (the built content lives here):** `components/events.csv`, `components/vendors.csv`,
> `components/bookings.csv`; `design/design-doc.md` §15 (event system); `design/tour-themes.md`;
> `art/vendor-art.md`, `art/tour-art.md`. **Attribution:** the CD set the *direction* and the named
> mechanical hooks below; the specific dishes, places, and tour names were developed from that direction
> by the studio agents (bg-theme / bg-copywriter / bg-research).

---

## 1. EVENTS — "creative, and utilise as many mechanics as possible"

**The CD's vision (near-verbatim):** events should be *creative and touch as many mechanics as possible —
the more of them and the more creative, the better.* They should reach across every system (followers,
ingredients, travel, actions), hit different scopes (you / your area / the whole board), and some should
**persist** for a while.

### Mechanical hooks the CD named → what got built

| CD idea (story hook) | Mechanic | Status |
|---|---|---|
| **Going viral** (a reel blows up) | gain followers | ✓ Gone Viral · The Reel Blew Up · In the News · Blogger's Pick · A Featured Spot |
| **Bad reviews / getting cancelled** | lose / disperse followers | ✓ A Bad Review · A Mix-Up · The Comments Turned · The Hype Moves On |
| **Playing dirty** (poach a rival's ingredient) | steal an ingredient from a rival | ✓ Poached the Supplier · Cut in Line · Borrowed the Recipe |
| **Heat wave / broken fridge — food goes off** | spoil / discard held ingredients | ✓ Heat Wave · The Fridge Broke |
| **Return ingredients to the bottom of the deck** | sink held/deck ingredients | ✓ Picked Clean |
| **Forced Scheduled Maintenance** (HSR outage) | block/detour travel, island-wide | ✓ Scheduled Maintenance (its own banner) |
| **"The boss wants to talk"** | block an action next turn | ✓ The Boss Wants a Word (no Promote next turn) |
| **Typhoon shuts things down** | pinch draws / block a region | ✓ Typhoon Day · Night Typhoon · The Big Typhoon |
| **No internet connection out in the sticks** | no follower-gain on next Travel | ✓ No Signal |
| **Roads/passes closed** | detour / reroute travel | ✓ Roadworks · Landslide on the Pass · The 3:47 to Zuoying |

### Scope & persistence (CD's steer)
- **Scope — you / same area / surrounding areas / whole board.** ✓ Built as a five-scope framework:
  ⦿ **self** · ⬢ **region** · ➤ **neighbour** (next-door region) · ▦ **island/board** · ✦ **rival/leader**.
- **Persistence — some events last a period of time.** ✓ Built as a duration model:
  *now* / *turn* / *until end-of-round* (e.g. The Big Typhoon, Roadworks, Golden Week persist).
- **Tune the events-vs-ingredients draw ratio per region by player count.** ✓ `map.json` `event_deck_mix`.

### Cancelled-tour boons (the CD's catch-up idea)
- **CLEAR** — *shed one of your OWN cancelled tours* (a personal relief boon). ✓ **Back On the Itinerary** (`t_clear`).
- **SALVAGE** — *take the LOWEST-scoring rival's cancelled tour into your Completed pile at half value* — a
  double boon (helps you AND lifts that rival's cancellation penalty); the standings pick the target, so
  it's not kingmaking. ✓ **Someone Has to Run It** (`t_salvage`).

### Anti-kingmaking (the CD's steer)
- Leader-targeting (✦) event losses hit the leader; if several are **tied** for the lead, all of them
  **except the drawer**. Kept **not too punishing** so a hard-earned lead isn't demotivating. ✓ ✦ scope + the `NUDGE_CAP` rail.

### ○ Open / V8 event ideas
- More **named festivals** as board-wide flavour events (beyond Lantern / Mid-Autumn / Golden Week / Lunar
  New Year / Dragon-Boat already in).
- Weather/season chains that set up a later payoff (a persistent event that "resolves" into a boon).
- *(space for new ideas)*

---

## 2. VENDORS — "the dish is the hero"

**The CD's direction:**
- **Dish-is-the-hero.** Each vendor is a **famous real Taiwanese dish**; the art is the *dish alone* — no
  people, no stall, no market scene. ✓ 24 real dishes, each tied to a real place (Houlong pork bao,
  Yongkang beef noodle, Chun Shui Tang bubble tea, Tainan milkfish congee, Taimali roselle tea…).
- **Multi-ingredient recipes** — vendors need **several** ingredients so players must **spread across the
  board**, not camp one region. ✓ recipes of 2-5 ingredients with cross-region spans.
- **Difficult vendors must be worth it** — *"either missions that include them yield higher points, or
  reintroduce vendor points."* The CD's insight: vendor points weren't wrong before, the **flat, too-easy
  vendors** were. ✓ vendor VP scales with difficulty (`cost + min_followers − 2`), and apex/expensive
  vendors anchor high-value tours.
- **Scarcity + the battle** — limited vendor slots so **contests actually fire**; a **min-followers floor**
  to claim a stall (harder stalls demand a bigger crowd). ✓ `vendor_slots` scarcity + `min_followers`.
- **Regional identity** — North (meat) · Central (tea) · South (seafood) · East (rice/produce), each with a
  signature and a ★ apex. ✓

### ○ Open / V8 vendor ideas
- Expansion regions / offshore islands (Penghu, Kinmen) with their own signature dishes.
- Seasonal or limited-time vendor variants; a "michelin" premium tier.

---

## 3. BOOKINGS (Tours) — "named real-Taiwan tours"

**The CD's direction:**
- **Named real-Taiwan tours**, not abstract patterns — **landmark clusters, routes, and festivals**. ✓
  - **Crawls / clusters:** Dihua Street Food Crawl, Tainan Old-Capital Crawl, Taichung City Crawl.
  - **Routes:** Round-Taiwan Cycling Route (環島), South-Link Coast Run (南迴), Hualien–Taitung Line (花東),
    Taipei–Taichung Line, Surf & Turf, Taroko–Taipei.
  - **Festivals / occasions:** Mid-Autumn BBQ, Lunar New Year Haul, Dragon-Boat Food Run, Golden Week.
- **Tours OUT-SCORE vendors** — booking is the **dominant win path** (VP tuned so an *easy* tour can score
  below a *premium* vendor, but the effort ceiling is much higher: more effort → more reward). ✓ (Route B
  scoring; tour value ≈ 2× the vendor-equivalent − 3.)
- **Showcase "pilgrimage" tours** — the **bubble-tea Origin-&-Neon pilgrimage** and the **Dihua dawn-to-neon
  crawl**; premium, story-forward stretch goals. ✓ (re-tuned to demanding-but-doable, ~40% completion).
- **Agnostic tours** — most tours drawable from setup, judged at **Last Train** (day ☀ / night ☾ / any ⟳). ✓

### ○ Open / V8 booking ideas
- More festival/route tours (Pingxi sky-lantern run, a temple-pilgrimage route — *secular framing only*).
- Campaign / legacy tour chains (complete one to unlock the next).

---

## Standing sensitivity rails (apply to ALL content above)
Traditional 繁體 (never Simplified); secular only (no temple / deity / ghost-month / funerary framing);
dignified locals, faithfully-rendered real dishes; the two **Indigenous** dishes — **竹筒飯 bamboo rice
(E01)** and **石板烤肉 stone-slab BBQ (E04)** — stay **consultant-gated** (Paiwan/Rukai/Amis community
sign-off) before any real/print use; **English name first** in all human-facing text.
