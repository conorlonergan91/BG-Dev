# Travel Agents: Taiwan — Art Style Reference (the one look)

**Purpose:** the single, canonical art-direction anchor for the whole game. **Every art-prompt / illustrator
brief in this project — characters, map, vendor cards, ingredient/food cards, icons, tokens, cover, rulebook
figures — MUST open by citing this reference**, so the whole set reads as one cohesive illustrated hand and
nothing drifts.

> **No AI final art (binding rail).** These briefs are for a **human illustrator**. AI is only ever used for
> labelled, gitignored *mockups* to explore a brief — never for shipped art. A **paid Taiwanese cultural +
> language consultant** reviews the character/theme art before final/print.

---

## The touchstone
The CD's reference is the art style of **Agent Avenue** — specifically its **fun, lighthearted, cartoonish
but *stylised*** look. **Take the LOOK, not the lore:** Travel Agents has stripped the secret-agent theme
entirely. The world here is **rival travel agents building the island's best street-food tour** — warm,
characterful **Taiwanese street-food & neighbourhood personalities**, a bustling day-to-night-market vibe.

## The look (what "stylised cartoon" means here)
- **Fun, lighthearted, cartoonish — but polished and STYLISED**, not crude doodle. Clean, confident linework;
  bold, mostly-flat colour with simple stylised shading; strong silhouettes; expressive, characterful faces.
- **A cohesive night-market palette** carried across every component: **warm daytime golds/ambers → neon-lit
  night-market violets/teals** (matches the game's day→night arc and the existing `night-market` theme).
- **At-a-glance clarity first** (this is a game, not an illustration gallery): the art serves readability —
  a character, a dish, a region must read instantly at component size.
- **One cohesive cast:** the six characters and the vendors all look like they belong to the same charming,
  slightly-exaggerated world — same linework weight, same colour language, same level of stylisation.
- **Dial the energy UP — over-the-top & wacky** (CD steer). Characters and **events** especially: big
  expressions, dynamic/comedic poses, exaggerated reactions, a bit of visual slapstick — lean into the fun.
  This amplifies the exaggeration; it does **NOT** loosen the dignity guardrail below (wacky ≠ mocking).

## The characters (the six)
Warm, affectionate, instantly-distinct **personalities** — lovable street-food/travel types, each exaggerated
for **charm and readability**:
- **The Old Councillor** (里長伯) — a cheerful apron-or-suit neighbourhood elder with real local clout.
- **The Homebody** (媽寶) — an earnest young office worker clutching a mum-packed lunchbox, phone to ear.
- **The Big Eater** (大胃王) — a joyful competitive eater, all appetite, mid-bite.
- **The Influencer** (網紅) — a stylish food blogger framing the perfect bowl for the feed.
- **The Big Brother** (大哥) — a **warm, lovable neighbourhood big-brother** in a bomber jacket, greeting a
  delighted stall-owner like an old friend — **cinema-charm, never a threat** (the #1 dignity watch-item).
- **The Globetrotter** (阿嬤 / A-má) — a spry, sharp-eyed granny with her elder travel-pass, already at the
  next market before everyone else — **age as her superpower, never frail**.

## Vendors — anchored to REAL Taiwan food places, and ALL distinct (CD steer)
Vendors are not generic stalls. Each references a **real, famous Taiwan night-market / street / food-area**
known for good eats, and its art **reflects that specific place** (its signature dish, stall look, and
neighbourhood character). **No two vendors look the same** — distinct dish, distinct stall, distinct place,
distinct composition; the vendor deck should feel like a tour across the island's real food scene.
- **`bg-research` curates the accurate real-place set** across the game's four regions (North / Central /
  South / East), with **correct place names + signature dishes** (rails: real dishes never mangled; secular;
  Traditional characters; consultant-verified before final art).
- **Anchor places the CD wants in (personal / family):** **Dadaocheng 大稻埕 + Dihua Street 迪化街 & the
  Dadaocheng Wharf 大稻埕碼頭** (Taipei — Datong); **Miaoli 苗栗** (near the place the CD wrote "Huolong" —
  **confirm the exact town + 繁體: likely 後龍 Houlong, possibly the 火炎山 Huoyanshan area — DO NOT guess the
  characters, verify**); and **Chiayi 嘉義** (famous for 火雞肉飯 turkey-rice). Weave these in respectfully as
  real, warm places — never a tourist-gaze postcard.

## ⚠ The sensitivity guardrail (BINDING — read before writing any character prompt)
"**Caricature**" here means **charming personality exaggeration** — the warm, expressive stylisation of a
great animated ensemble — **NOT ethnic caricature, racial stereotype, or mockery.** This is a real culture
(Taiwan), and the rails are binding: **dignified local characters**, real dishes rendered accurately and
respectfully, **secular** settings only (no temple/deity/ghost-month/funerary imagery), anti-extraction
framing (celebration, never a tourist's gaze). Every character reads **warm, likeable, and dignified** — we
are laughing *with* this world, never *at* it. When in doubt, dial toward affection. (Consultant reviews
before final art; native-review watch-items: the Big Brother's warmth, the granny's spryness, the food/place
names.)

## How to cite this in a prompt
Open every brief with one line, e.g.:
> *Style: per `art/art-style.md` — fun, lighthearted, **stylised** cartoon (Agent Avenue-style look, travel-agent
> not spy theme); clean linework, bold flat colour, night-market palette (warm day → neon night); warm,
> dignified Taiwanese characters, charming not caricatured. Human-illustrated; no AI final art.*
Then add the component-specific subject, composition, and the reserved size/figure code.

---

## AI mock-up prompts (playtest props — NOT final art)

> **What this section is.** A **permitted, opt-in** use of AI: quick **high-fidelity mock-ups** so the CD
> and playtesters can *feel* the game's warmth on the table during **manual playtesting**. These are
> **props for playtesting only.**
>
> **The binding rail does NOT change: final art is human-illustrated. NO AI final art, ever.** Nothing
> generated from these prompts is final, and none of it ships or is committed.
>
> **Where the PNGs go.** Every generated image is a **MOCKUP**: save it to the **gitignored** scratch dir
> **`games/travel-agents/build/mockups/`**, filename = the **FIG code** (e.g. `FIG-CHAR-globetrotter.png`,
> `FIG-VEND-N01.png`, `FIG-TOUR-d_north2.png`). Label it MOCKUP wherever it's shown. It is **never**
> committed, **never** moved to `exports/`, and **never** shipped as final art.
>
> **This file is the canonical scaffolding.** The other art files' mock-up sections all cite the **STYLE
> ANCHOR**, the **SCALE TABLE**, and the **sensitivity rails** below — they don't repeat them.

### STYLE ANCHOR (paste this verbatim at the start of EVERY mock-up prompt)

> A **bold, exaggerated, over-the-top CARTOON CARICATURE** — a lively modern animated-feature / comic
> character, **NOT a realistic or semi-realistic portrait**. Push the exaggeration hard: **slightly
> oversized head, big expressive eyes and hands, snappy stylised proportions, a wacky dynamic pose and a
> huge expression** — visible comic energy, a bit of playful slapstick. The fun, characterful *look* of
> Agent Avenue, with a **travel-agent, Taiwanese street-food theme (no spies)**. Clean, confident bold
> linework; bright, mostly-flat cartoon colour with simple stylised shading; a strong readable
> silhouette. **Wacky in the CHARMING, animated-ensemble sense — never ethnic caricature or mockery; still
> warm, likeable, and dignified.** Cohesive **night-market palette**: warm daytime golds and
> ambers glowing into neon-lit night-market violets and teals — lantern vermilion `#D64545`, jade teal
> `#1F8A7A`, golden amber `#E6A930`, dusk indigo `#26324D`, on bao-paper cream `#F7F1E3`. Cozy, inviting,
> celebratory. **The single most important goal: convey the WARMTH at the heart of this game** — the
> friendly, food-loving, celebratory spirit of Taiwan's night markets should be *felt at a glance*.
> Dignified Taiwanese locals and faithfully-rendered real dishes; **charming personality exaggeration,
> never ethnic caricature or mockery**; **secular settings only** — no temple, deity, ghost-month or
> funerary imagery.

### SCALE TABLE (px @ 300 DPI — the exact slot each mock-up must drop into)

Generate at **2× the pixel size below** for crispness, then **export at the exact aspect ratio** so the
image drops cleanly into its SVG slot. Background: **transparent** for cut-out character portraits;
**full/simple** for full-card faces and the map (noted per row). Save to
`build/mockups/<FIG-CODE>.png`.

| Slot | FIG code | Size (px) | Physical | Aspect | Background | Composition note |
|---|---|---|---|---|---|---|
| Character-board portrait | `FIG-CHAR-<slug>` | **490 × 600** | 41.5 × 50.8 mm | **~0.82:1 PORTRAIT (≈4:5)** | transparent | full-figure / waist-up hero standing tall; the slot is now a **large PORTRAIT** at top-left (44,176) on the 1680×1380 board (was a wide letterbox) — **compose TALL**. Auto-embedded when `build/mockups/FIG-CHAR-<slug>.png` exists (data-URI), else a dashed placeholder renders. `preserveAspectRatio=meet` letterboxes, so exact 490×600 is ideal but any ~4:5 crop drops in cleanly |
| Ingredient card art | `FIG-ING-<id>` | **642 × 560** | 54.4 × 47.4 mm | **~1.15:1** | simple | on a 750×1050 poker card at (54,168); shows a **MIX** of that generic category (e.g. Meat = pork belly + beef + sausage + poultry together) |
| Vendor card face | `FIG-VEND-<id>` | **750 × 1050** | 63.5 × 88.9 mm | **~0.71:1** | full-bleed | poker-card face, **54 px (4.5 mm) safe margin**; see drop-in note below |
| Tour / Booking card face | `FIG-TOUR-<id>` | **750 × 1050** | 63.5 × 88.9 mm | **~0.71:1** | full-bleed | poker-card face, **54 px safe margin**; see drop-in note below |
| Region map (full board) | `FIG-MAP-ISLAND` | **2280 × 1680** | 193 × 142.2 mm | **~1.36:1** | full | per-region vignettes optional |

**Vendor & Tour card drop-in (read `render_vendor_svg` in `tools/cards/build_cards.py`).** The vendor
face is **UI-dense**: a region-colour **header band** (Tâi-lô title + 繁體 subtitle) with a **tier pill**
top-right, then a **region strip + English dish name**, then the **PAY** row (ingredient chips + the
violet **Followers** badge), the **DRAW 人氣** crowd-gauge, and an **ICON 圖示** box filling the lower
card. Those UI elements are drawn as **translucent white boxes (opacity ~0.45–0.9) that sit on top** of
whatever art is behind them. So the cleanest mock-up is **(b) a full-bleed card face the UI overlays** —
paint the whole 750×1050 face, but **keep the hero dish/stall as the focal point in the upper ~55% of the
card** (under the header band, above the PAY/DRAW/ICON stack) and keep that lower region calmer/darker so
the translucent PAY/DRAW/ICON panels stay legible on top. Same approach for Tour tickets: full-bleed
boarding-pass face with the icon-motif read in a clear upper window, the name band and requirement text
overlaid. (Option (a) a boxed central hero-window that clears the UI is available if a face gets too busy —
but full-bleed reads warmer and is what these prompts assume.)

### Sensitivity rails for mock-ups (BINDING — same rails as final art)

A mock-up is still a picture of a real culture; the `art-style.md` guardrail above applies in full.

- **Dignified locals** — charming personality exaggeration only; **never** ethnic caricature, racial
  stereotype, or mockery. We laugh *with* this world, never *at* it. When in doubt, dial toward affection.
- **Secular only** — no temple, deity, ghost-month or funerary imagery, even where a real place sits near
  a temple.
- **Real dishes rendered faithfully** — the food is the beloved; get it right.
- **Indigenous items are consultant-gated even for mock-ups.** **E04 石板烤肉 (slate BBQ, Paiwan/Rukai)**
  and **E01 竹筒飯 (bamboo-tube rice)** — keep any mock-up **generic and respectful**, **no specific tribal
  iconography**, no AI-invented Indigenous-language terms. Treat these as placeholders and **flag for the
  paid community consultant**; do not treat a mock-up as any kind of sign-off.

### Generating & prepping the PNGs (the raster reality + the prep tool)

AI image tools (ChatGPT/DALL·E, Midjourney, …) return **raster PNGs, not SVG**, and won't reliably
loop over a cast or emit one file per item. **That's expected — and fine.** The component SVG *embeds*
a raster in its art slot; we never needed per-item SVGs. Ask the tool for a **raster PNG**, not vector.

**Generate for a clean cut-out** so prep is painless:
- **One subject per image.** Don't ask for a grid/sheet of the whole cast — the tool composes them at
  different scales and you then have to slice it. One character (or one vendor) per generation.
- **Flat or transparent background — NO baked backdrop.** Explicitly request *"on a plain flat
  background"* or *"transparent background, no scenery."* **Avoid the dark radial glow/vignette** some
  tools add by default: it is *not* a flat colour, so it can't be keyed cleanly and forces a re-gen.
  (This is exactly why the Councillor and the Globetrotter came back hard to cut out.)
- Keep the subject **fully inside the frame** with a little margin, so trimming doesn't clip a hand.

**Prep the export into a drop-in slot asset — `tools/mockup/prep_mockup.py` (stdlib + Pillow):**
It (1) splits a grid into individual cells, (2) keys a flat background to transparent via a
**corner-seeded flood fill** (lifts the backdrop without punching holes in a white shirt or bowl —
interior whites aren't border-connected, so they survive), and (3) trims + scales + pads each cutout
to a slot's **exact px size**, writing to the gitignored `build/mockups/<FIG-CODE>.png`.

```bash
# Split a 2×2 grid of four characters, key the white bg, fit each to the board portrait slot:
python tools/mockup/prep_mockup.py --grid ~/Downloads/cast.png --rows 2 --cols 2 \
    --names homebody,big-eater,influencer,big-brother \
    --key-bg --fit 490x600 --pad --game games/travel-agents --prefix FIG-CHAR-

# Clean one already-cropped portrait (e.g. the Globetrotter) to the same slot:
python tools/mockup/prep_mockup.py --image ~/Downloads/granny.png --key-bg \
    --fit 490x600 --pad --game games/travel-agents --out FIG-CHAR-globetrotter.png
```

Use the **SCALE TABLE** `--fit` value for the slot you're filling (char `490x600`, ingredient `642x560`,
card `750x1050`, map `2280x1680`). A heavy vignette will only *partly* key — regenerate those flat.

**Aspect note (portraits & the board slot).** The board portrait slot is now a **large ~4:5 PORTRAIT
(490×600)** — reshaped from the old wide letterbox precisely so **full-figure character art shows big**.
Compose TALL (full-figure or waist-up hero standing). `render_playerboard` embeds
`build/mockups/FIG-CHAR-<slug>.png` as a self-contained data-URI (`preserveAspectRatio=meet`, so it
letterboxes rather than crops — an exact 490×600 fills edge-to-edge); with no file present the dashed
placeholder renders. Ingredient cards (`FIG-ING-<id>`) auto-embed the same way. (Board layout owned by
`bg-infodesign`.)
