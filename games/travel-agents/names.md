# Travel Agents: Taiwan — Canonical Names & Terms

> **The single source of truth for how every name and term is spelled, formed, and staged.** Owned by
> `bg-continuity` (the drift-catcher); read alongside `identity.md` (felt identity / `bg-theme`) and
> `design/rules-draft.md` (the current V7 rules). If a doc, component, or render disagrees with this
> table, this table wins — reconcile the doc, or (for a mechanics/value question) flag it.
>
> **House rule — English first.** In chat and in prose, use the **English name**; put the 繁體 / Tâi-lô in
> parentheses only where precision or the cultural-sensitivity context needs it.
>
> **Cultural rails (binding).** Traditional characters only — **never Simplified**. Tâi-lô romanisation is
> best-effort until a **paid Taiwanese cultural + language consultant** confirms it (binding before art/
> print — this table does not discharge that). Indigenous items (E01 竹筒飯, E04 石板烤肉) are consultant-
> gated even for mock-ups.
>
> Status: **V7 (multiplayer 3–6)** · Last swept 2026-08-09 (`bg-continuity`, first sweep).
> Supersedes the roster table in `v7-plan.md` as the canonical name reference.

---

## 1. Characters — the six-agent roster (source: `components/characters.csv`)

Always refer to a character by the **English name** in prose. Never use the 繁體 / Tâi-lô alone.

| # | English name (USE THIS) | 繁體 | Tâi-lô | One-line kit (see `characters.csv` / `rules-draft.md` for the exact rule) |
|---|---|---|---|---|
| C1 | **The Old Councillor** | 里長伯 | Lí-tiúⁿ-peh | Pick one **home region**: Bribing there costs 1 less; anywhere else the away-tax adds +2. |
| C2 | **The Homebody** | 媽寶 | Ma-pó | Sole on-the-move sourcer — on a **Travel**, draw 2 of the region left and keep both. Flaw-free. |
| C3 | **The Big Eater** | 大胃王 | Tuā-uī-ông | On a **Visit**, keep all 3 (may grab a 4th). Flaw: hazards fire **twice** on his Visit. |
| C4 | **The Influencer** | 網紅 | Bāng-âng | Followers-max **dial starts at 4** (floors at 4). Flaw: takes the **last** seat. |
| C5 | **The Big Brother** | 大哥 | Tuā-ko | **Wins ties** — needs only to *match* the biggest crowd. Flaw-free. |
| C6 | **The Globetrotter** | 阿嬤 | A-má | **Travel reaches any region** in one action; immune to Scheduled Maintenance. Flaw-free. |

**Name-form watch (dignity / sensitivity, binding portrayals):**
- **The Homebody (媽寶)** — an affectionate stays-close-to-home read; **never** a mocking "mama's boy".
- **The Big Brother (大哥)** — the warm community elder / lovable rogue; **never** a menacing gangster or an
  Orwellian "Big Brother". Blessed *only while the warm portrayal stays load-bearing* (#1 character-name
  consultant watch-item).
- **The Globetrotter (阿嬤)** — spry, sharp-eyed, unstoppable; age-as-superpower, **never** frail/forgetful.
  Names a *type*, not a demographic; guard against a foreign-tourist gaze (she is a restless *local*).
- **The Old Councillor (里長伯)** — neighbourly standing, not graft; favours bounded to his one borough.

> **Locked (do not re-litigate — `bg-theme` bless, logged in `decision-log.md`):** all six English names
> are canonical. "The Globetrotter" is **locked** over "The Free Rider" (freeloader read) and "A-má / The
> Globetrotter Granny" (off-register).

---

## 2. Ingredient categories — the SIX generic set (source: `components/ingredients.csv`, `recipe-glyphs.csv`)

The V7 taxonomy is **six generic categories**, each card illustrated as a **mix** of real examples. This
**retires the five specific ingredients** (see §4).

| English | 繁體 | glyph | Role | Illustration = a mix of… |
|---|---|---|---|---|
| **Meat** | 肉 | 肉 | North signature | pork belly · beef shank · sausage · poultry (incl. turkey) |
| **Tea** | 茶 | 茶 | Central signature | high-mountain oolong · black tea · bubble-tea leaf base |
| **Seafood** | 海鮮 | 海 | South signature | oyster · milkfish · shrimp · clam · squid |
| **Pantry** | 糧 | 糧 | East signature | valley rice · glutinous rice · noodles · flour |
| **Sugar** | 糖 | 糖 | Common (Central & South) | cane sugar |
| **Vegetables** | 菜 | 菜 | Common (North & East) | greens · cabbage · radish · bamboo shoot · scallion · roselle |

---

## 3. Term glossary — CURRENT (V7)

The authoritative player term set. Canonical spellings and forms; use these everywhere.
(Source: `design/rules-draft.md`, `components/tokens.csv`, `components/events.csv`, `v7-plan.md` decisions.)

| Term | 繁體 | What it is |
|---|---|---|
| **Followers** | 粉 | The committed, public, contested hype you pile ON a vendor. A **Promote** places **2 Followers**; total committed ≤ your dial. *(renamed from Buzz)* |
| **Followers-max (the dial)** | 盤 | Your live per-player ceiling on committed Followers, shown by a **dial**. Start **2** (the Influencer 網紅 starts **4**); raised by Travel + events; the lost-war sink drops it. **Never scores.** *(renamed from Reach)* |
| **Promote** | — | The action that places 2 Followers on vendor(s) you stand with. |
| **Bribe** | — | The action to win a face-up vendor: hold the **biggest crowd** (outright Followers majority) + pay its ingredients − region discounts. |
| **Bookings** | 開團 *kāi-tuán* | The tour cards — the **sole scoring vector**. Hand-limit **3**, cancel-to-claim; the **Booking decks are the deck-driven clock**. *(renamed from Tour Tickets / missions)* |
| **COMPLETED** | 成團 | The WIN pile — a Booking whose tour ran; scores **+full value**. *(the win label, renamed from "SOLD" / "Published Tours")* |
| **CANCELLED** | 取消 | The LOSE pile — a Booking that didn't run in time; scores **−½ value** (rounded down). *(renamed from 遺珠 / "the Ones That Got Away")* |
| **Trending** | 爆紅 | The **dynamic**, event-dropped going-viral marker ("Gone Viral"); winning a Trending-marked vendor grants **+1 Followers-max**. *(renamed from the ★ Star token)* |
| **★ apex** | — | The **printed, permanent** marquee vendor (Michelin / Bib-Gourmand register), one per region's night set, carrying no region icon. A **separate thing** from Trending — held apart on purpose. |
| **area-majority / biggest crowd** | — | The contested-vendor rule: strict plurality of committed Followers wins; a **tie blocks** (none may claim) — the Big Brother 大哥 alone wins ties. |
| **lost-war dial-drop** | — | Lose a contested vendor → your dial drops **−1 by day / −2 at night** (floor = your start value); return any over-cap Followers to supply. Framed as *the crowd drifting to a rival's stall*. |
| **黃昏 DUSK** | 黃昏 | The seeded boundary card that flips day → night when the DAY Booking deck runs out. |
| **末班車 LAST TRAIN** | 末班車 | The seeded boundary card that ends the game when the NIGHT Booking deck runs out. |
| **the day-clock** | — | The day→night→end beat, carried **entirely by the two Booking decks + the two boundary cards** (§8 of the rules). *A concept/section name — there is **no printed clock track** (see §4).* |
| **Larder** | — | Your sourced ingredient cards, kept face-up; cap **7**. |
| **Visit / Convenience Store / Travel** | — | The three sourcing/movement turn actions. |
| **region icon / discount ramp** | — | Each region icon a won vendor carries makes that region's ingredients **1 cheaper** on future Bribes (floor 0). Drinks and ★ apex carry none. |
| **Rave Reviews** | 好評 | The two per-player milestone boons at your **2nd** and **4th** completed tour (never pumps the leader). |
| **Tours-Completed** | — | The per-player monotonic counter that hosts the Rave Reviews milestones. |
| **Scheduled Maintenance** | 排班保養 | An island-wide event: the HSR is down for everyone for a round (the Globetrotter 阿嬤 is immune). |

**Wording rail (binding).** Frame any loss of Followers or a dial-drop as *the crowd ebbing / drifting to a
rival's stall* — **never** a bare "−N Followers"; a real social-media feel-bad is the one way this warm beat
could curdle.

---

## 4. Term glossary — RETIRED (flag any live use)

If any of these appears as a **current** term in a doc, component, or render, it is drift — reconcile to the
CURRENT form (§3), or flag it if resolving it is a mechanics/value question.

| Retired term | Replaced by (V7) | Note |
|---|---|---|
| **Buzz** | Followers | Pure rename (CD v6.4 lock). |
| **Reach** (← Reputation / Prestige) | Followers-max (the dial) | Pure rename; the Reputation → Reach → Followers-max lineage. |
| **Tour Tickets / Tour-Ticket / missions** | Bookings 開團 | Pure rename. |
| **Draw** (人氣) — as a vendor *value* | *(retired as a scored/printed vendor value)* | ⚠ **Data-vs-rules contradiction — FLAG, do not fix.** Still a `draw` column in `vendors.csv`, 5 `draw`-target rows in `bookings.csv`, a DRAW card panel (`art/art-style.md`) and Draw-target Bookings (`art/tour-art.md`) — but `rules-draft.md` has no Draw. → `bg-design` / `bg-elegance` to resolve. |
| **★ Star token** | Trending marker (爆紅) | Rename of the *dynamic* token only. **The printed ★ apex is NOT retired** — do not conflate. |
| **vendor-claims clock-track / numbered day-clock track** | deck-driven 黃昏 DUSK / 末班車 LAST TRAIN | The *printed numbered track* is gone; the *concept* "day-clock" survives as a rules section name (§3). |
| **蚵仔煎 oyster omelette (as S04)** | 火雞肉飯 turkey rice (S04) | Oyster omelette is **displaced** from the 24 vendors (top candidate for a future South slot). |
| **the 2-player across-the-table map / the duel** | one neutral shared **3–6-player** board | V7 pivot — 2p dropped as a design target. |
| **SOLD** (win label) | COMPLETED 成團 | Also removes the clash with the 完售 "Sold Out" event. |
| **遺珠 / "the Ones That Got Away" / "Published Tours" / "Departures"** | CANCELLED 取消 | One canonical lose-pile name everywhere. |
| **"the Queue"** | *(retired)* | Old flavour-skin for the Buzz stack; Followers is self-flavouring. |
| **the 5 specific ingredients** — 豬肉 pork · 茶 tea · 海鮮 seafood · 米 rice · 糖 sugar | the SIX generic categories (§2) | pork→Meat 肉 · rice→Pantry 糧 · + Vegetables 菜 (new); tea/seafood/sugar 繁體 unchanged. |
| **早餐店 / 夜市攤 / 飲料店 venue types** | plain board terms | dropped as rules keywords. |
| **Beverage Row / the drinks fork** | drinks are just low-value vendors | mixed into every region's deck. |
| **Code Red** (end-trigger) | the plain last-train close | dropped. |
| **"Bookings" as an old score/VP track** *(v6.3 sense)* | *(that sense retired)* | ⚠ Note: **"Bookings" is REUSED in V7** as the tour-card name (開團). Same word, different referent — the V7 sense is current. |

---

## 5. Open flags (mechanics / ambiguous — for other agents, not fixed here)

- **Draw's V7 status** (see §4) → `bg-design` / `bg-elegance`. Presentation depends on it: the vendor card
  DRAW panel (`art/art-style.md`), Draw-target Bookings (`art/tour-art.md`, `bookings.csv`), and the
  `vendors.csv` `draw` column all live-reference it.
- **`components/events.csv` EV-D07** effect text names the granted ingredient "**(豬肉 Pork)**" — the
  retired specific term; the North signature is now **肉 Meat**. → text fix for `bg-developer` (a CSV/
  component-data file; not edited here per the presentation-only lane).
- **S04 turkey rice Tâi-lô** — *hóe-ke-bah-pn̄g* is best-effort → **consultant confirms** (binding). Same
  for all Indigenous terms (E01 竹筒飯, E04 石板烤肉) → consultant, never AI romanisation. → `bg-publishing`.
