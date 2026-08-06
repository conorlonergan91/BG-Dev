# 🎨 Travel Agents: Taiwan — Creative Identity

> The living source of truth for this game's **felt identity**: concept, theme, tone/vibe, story/lore,
> look & feel, and naming. Owned by `bg-theme`; read alongside `game-bible.md`. Keep it current — and
> keep it **coherent** while letting it **evolve** with the design.
> Slug: `travel-agents` · Started: 2026-08-06 · Last framed: 2026-08-06 (bg-theme)

> **Restraint first.** Match identity depth to what the game *earns*. Leaving story/lore light on purpose
> is a correct answer, not a gap. Never invent lore to fill a section.

## North star
**Image:** *A Taiwan night market at dusk — steam rising, neon and paper lanterns everywhere, two
friends grinning at each other: "we HAVE to try that one next."*
**Phrase:** the joy of discovering the next great bite, together.

Every choice serves this picture. When a decision is unclear, ask: *does it make the table feel like
that night market?*

## Concept & premise
A lighthearted travel-and-food game set in **Taiwan**. You're a food-obsessed "travel agent" on a
gleefully low-stakes "mission" — really just: eat the best things, ride the island, out-adventure your
friends. The comedy is **warm and celebratory** of Taiwanese food culture — done *with*, never *at*. The
secret-agent framing is a **wink** (mission-dossier flavour, code-name gags), not a spy thriller — and
in the base game it is **flavour only** (the load-bearing hidden-mission version is a held expansion).

## Target aesthetics (the kinds of fun) — **locked: 3**
1. **Discovery** *(lead)* — uncovering the island: which stall, which region, what's around the next
   corner. The map/menu *reveals*. This is the engine of delight.
2. **Fellowship** — the shared-table joy. Even in the competitive duel it's *warm rivalry* ("look what I
   found!"), and at 3–4 it's table talk. Matches the studio's co-op-adjacent warmth.
3. **Challenge** *(kept light, ~1.8)* — optimise your trip (the *Ticket to Ride* / *Let's Go! To Japan*
   satisfaction), but never so tight it stops feeling like a holiday.

*Sensation* (lovely food art, tactile bits) is a **supporting texture**, not a core pick — we get it for
free from good illustration without chasing it. Chasing all eight = chasing none.

## Tone & vibe — **one tone, held everywhere**
**"An over-enthusiastic travel buddy on a 'top-secret' snack mission — warm, funny, never at anyone's
expense."** Sunny, generous, gently comedic travel-guide enthusiasm — the delight of a friend who is
genuinely, ridiculously obsessed with Taiwan showing you around.

- **Where the comedy comes from (the *with* register):** the players' own gluttony and indecision; the
  absurd stakes of the "mission" gag; and *affectionate specifics a local would high-five* — the scooter
  swarm, 24-hour everything, convenience-store culture, "臭豆腐 smells wild, tastes incredible — the
  locals are right." Punch at yourself and the gag; never at the place.
- **The one test:** *would a Taiwanese player laugh **with** this, or feel it laughs **at** their home?*
  If a joke only works because you find Taiwan itself strange/foreign, cut it.
- **Keeping the wink a wink:** the spy layer lives in *register only* — a trench coat over a Hawaiian
  shirt, "Operation: Beef Noodle," a mission-dossier rulebook voice. No grit, no real espionage, no
  cataloguing/extracting gaze (see sensitivity pass).

## Restraint rung — **Evocative theme** (studio sweet spot)
A felt world you could describe in a sentence; **light-to-no narrative**. The *setting* does the heavy
lifting, humour is the seasoning, the agent gag is dressing. We are deliberately **not** climbing to
"light narrative / deep lore" — that's the held expansion's job, not the base game's.

## Story / world / lore
**Light by design — and staying that way.** There is no plot to keep straight. The "mission" is comedic
scaffolding; the real story is the trip *you* take and the log you fill. Leaving this near-empty is the
correct answer for this rung.

## Theme ↔ mechanic resonance
*(Spine not yet locked — revisit each iteration. Aim: a player could half-guess the rules from the
fiction.)*
- **collect dishes = eating** · **build routes / ride the rail = travelling** · **the "log" = your trip**
  — these read as inevitable, good.
- **Watch:** the **agent/mission** layer must earn a rule or it's just paint. In the base it is
  *honestly* light dressing (a themed name for objective cards) — that is fine, **as long as we're
  honest about it and don't pretend it's load-bearing.** The moment a mechanic makes the "mission" gag
  do real work (hidden info, bluff), that's the expansion — log the re-theme then.
- **Re-skin test:** if the whole game renames to any other food-travel setting with zero loss, the
  *place* (Taiwan) isn't doing work. It should: dish/region specifics should shape which sets and routes
  exist. Push design toward Taiwan-specific structure, not generic "food + map."

## Look & feel / art direction
**Render theme name:** `night-market` (to add to `tools/cards/themes.py` — palette + per-suit
colour+emblem). Suits carry **colour *and* an emblem/icon** always — never colour alone.

- **Palette (first pass — night-market at dusk):**
  | Role | Colour | Hex | Note |
  |------|--------|-----|------|
  | Core 1 | Lantern vermilion | `#D64545` | festival lanterns, warmth |
  | Core 2 | Jade teal | `#1F8A7A` | tea, mountains, Taiwan jade |
  | Core 3 | Golden amber | `#E6A930` | fried food, warm bulbs, gold |
  | Core 4 | Dusk indigo | `#26324D` | the night-sky backdrop (also dark neutral) |
  | Neutral light | Bao-paper cream | `#F5EFE2` | steamed-bun paper card ground |
  | Neutral dark | Soft ink | `#2B2B2B` | body text |
  - **Colour-blind flag (real, for `bg-access`):** vermilion vs jade-teal risk **red/green confusion**
    for deutan/protan viewers, with amber sitting between. **Redundant encoding is mandatory** — every
    suit/category dual-coded with a distinct emblem + label. Run
    `python tools/access/check_access.py --game games/travel-agents --theme night-market` **before
    locking**; expect to nudge hues/lightness apart. Palette is *first-pass*, not locked.
- **Typography feel:** one **friendly rounded display** face for titles (evokes hand-painted market
  signage), one **clean humanist sans** for body/values. Pair with a **Traditional Chinese** face — dish
  names appear romanised **and** in 繁體字 (Taiwan uses Traditional, *not* Simplified — see sensitivity).
- **Iconography grammar (three language-independent families):**
  1. **Food** — dish silhouettes (bowl of beef noodle, xiao long bao, bubble tea, gua bao, shaved ice…).
  2. **Transport** — HSR/train, local rail, scooter, bus, ferry, bike, foot.
  3. **Region/place** — a simple island-of-Taiwan motif + regional glyphs (N/C/S/E).
- **Silhouette / shape language:** cards frame as a **passport / boarding-pass / stall menu-board**;
  places visited recorded as **stamps** (passport-stamp motif doubles as the dossier gag and the
  Discovery feel). Rounded corners, warm.
- **Moodboard / references to gather in `art/`** (real photo refs for a human illustrator):
  Shilin / Raohe / Liuhe night markets at dusk; hand-painted stall signage & 繁體 hand-lettering; HSR
  and local trains; scooters; convenience-store culture; vintage travel stamps/stickers; and the iconic
  dishes above. **Note the multi-ethnic range** (Han, Hakka, and Indigenous cuisines — see sensitivity).
- **Art production:** **human-illustrated by default — no AI final art** (`designer-profile.md`).
  Placeholders clearly labelled. Opt-in AI *mockups* for vibe exploration only (`art/mockups/`, never
  shipped).

## Naming & voice
- **Working title:** "Travel Agents: Taiwan" — **flagged for a decision** (see the coherence note
  below). The travel/secret-agent pun is series-ready but **foregrounds the espionage layer we
  deliberately demoted to flavour** — a real tension.
- **Directions on the table** (all → `bg-publishing` for trademark/clearance before commissioning art):
  1. **Travel Agents: Taiwan** *(incumbent)* — max series-generality ("…: Japan", "…: Thailand"); but
     "Travel Agents" is generic/booking-site-ish and over-promises the agent gag.
  2. **Operation: Night Market** *(bg-theme lead)* — keeps the mission gag as an explicit *wink*
     ("Operation" = playful), while the title's real promise is the **market & food**; series-ready as
     "Operation: <place>". Threads the needle.
  3. **Night Market** *(warmest tonal fit)* — line-brand foregrounding the north-star image
     ("Night Market: Taiwan"); agent gag lives only inside the box. Weakest series-generality (not every
     country is night-market-centric) and a generic, crowded mark.
- **Component/keyword register (pick ONE, hold it):** playful travel-guide + light dossier garnish —
  objectives = **Missions/Assignments**, the trip = your **Itinerary**, scoring = the **Traveller's
  Log**, places visited = **Stamps**. Read them aloud together; kill any that clash.
- **Voice:** rulebook & aid as a warm **mission-dossier / field-guide** from an over-caffeinated
  handler-slash-tour-guide — second person, short, funny margin asides. `bg-elegance` keeps it tight.
  **Dish names stay authentic** (romanised + 繁體) — never invented or parodied; the comedy is in the
  flavour text and the gag, *never* in mangling real food.

## Sensitivity & representation pass — **REAL FLAG → `bg-publishing`**
Trigger: **yes** — a real place, culture, food, and people (Taiwan). Concept is warm and well-meant, but
the *subject* is real and politically sensitive, so this is a genuine flag, not a trivial pass.

- **Highest-consequence item — Taiwan's identity:** present Taiwan **as itself** — its places, food,
  culture — **without** wading into cross-strait politics **and without erasing it into "China."**
  Use **Traditional characters**, established English place-spellings (Taipei, Kaohsiung, Keelung,
  Tainan), Taiwan's own island form. **No PRC flag, no Simplified, never frame it as a province.** Equally
  don't turn the game into a political statement — keep it warm and on the island's own terms.
- **Guard the traveller-gaze:** the "agent/mission/outsider" framing must **not** tip into a
  colonial/orientalist "outsider extracts the exotic East" gaze. The traveller is a **guest and fan**,
  not a spy exploiting or a coloniser cataloguing. "Discovery" is discovery-*for-the-visitor*, framed
  with humility — people already live there.
- **People with dignity:** vendors, cooks, the aunties/uncles (阿姨/阿伯) are **subjects** — warm,
  specific, varied in age/look — not exotic scenery or obstacles. Let players see a range of faces.
- **Celebrate specifics locals recognise** and **acknowledge Taiwan is multi-ethnic** — Han majority
  *plus* Hakka, 16+ recognised **Indigenous peoples**, and newer immigrant communities all shape the
  food. Representing that range is itself a respect signal.
- **Don'ts:** no mocking accents / the sound of the language / "weird foreign food" gross-out (stinky
  tofu = "locals are right," not "ew"); no poverty or vendor punchlines; **no sacred/religious motifs as
  decoration** (temples, deities, ghost-month, funerary offerings) played for gags; no
  "ancient-mystical-China" tropes or caricature — lean **modern, neon, scooters, HSR**, which is both
  accurate and stereotype-proof. Handle betel-nut culture (and "betel-nut beauty" imagery) with great
  care or omit.
- **Consultation warranted (→ `bg-publishing`, before art & before print):** engage a **paid Taiwanese
  cultural consultant / sensitivity reader** (ideally across regions/ethnicities) and a **native
  reviewer for all Chinese text + romanisation**. This is cheap insurance against an
  unfixable-after-print, reputationally serious mistake. Ground food/geography research now via
  `bg-research` from Taiwanese sources.

## Locked vs fluid
- **Locked:** setting = Taiwan; **tone** = the over-enthusiastic-travel-buddy register above;
  **aesthetics** = Discovery + Fellowship + Challenge; **rung** = evocative theme; agent framing =
  flavour-only in base; human-illustrated art; the sensitivity guardrails above.
- **Fluid:** the exact **name** (decision below); the mechanism spine (→ resonance revisit); the suit
  set (food categories vs regions) and final palette hues; whether 2p duel or 3–4 race is the true home.

## Re-theme log
<!-- date — design change → identity move → why. -->
- 2026-08-06 — Project framed. Identity seeded from the brief (Taiwan food-travel adventure, quirky agent
  wink) — kept light pending the ideation direction.
- 2026-08-06 (bg-theme) — **Framed the identity.** North star = night-market-at-dusk; aesthetics locked
  to Discovery + Fellowship + Challenge; tone locked to the "over-enthusiastic travel buddy" register;
  rung = evocative theme. First-pass `night-market` palette + icon grammar + `stamp/passport` shape
  language. Ran the **sensitivity pass → REAL FLAG** (Taiwan is a real, politically-sensitive place):
  paid Taiwanese consultant warranted before art/print. Surfaced the **title tension** (the "Agents" pun
  foregrounds the demoted espionage layer) as a decision for the Creative Director.
