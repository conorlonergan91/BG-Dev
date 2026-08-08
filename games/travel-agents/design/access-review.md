# Accessibility Review — Travel Agents: Taiwan

> Guardian pass by `bg-access`. Theme: `night-market`. Date: 2026-08-06.
> Scope: colour-blind / contrast / legibility floor flagged as a real risk in `identity.md`, run once
> component data + the `night-market` render theme exist. Data source: `components/ingredients.csv`,
> `components/dishes.csv`, `components/player-aid.json`; theme `tools/cards/themes.py`; rendered sheets in
> `exports/`.

## 1. Checker output

`python tools/access/check_access.py --game games/travel-agents --theme night-market`

**Result: 3 error(s), 18 warning(s).**

**Text contrast (WCAG) — PASS.** `ink #26324D` on cream page = **9.4:1**; `text #2B2B2B` on page =
**10.4:1**. Both comfortably clear the 4.5:1 body floor. *(Note: the tool only checks ink/text vs page.
It does NOT check glyph-on-token contrast — see §3, where the real failure lives.)*

**Colour-blind separability — 3 ERRORS, all cross-family false positives.** The 3 hard errors are:

| Pair | Shared | Why the tool errors |
|------|--------|---------------------|
| `beef` & `north` | `#D64545` + `triangle` | ingredient reuses its own region's silhouette |
| `central` & `tea` | `#1F8A7A` + `diamond` | same |
| `east` & `rice` | `#26324D` + `square` | same |

The tool is **family-blind**: it treats the region suits (`north/central/south/east/signature` — used on
dish cards) and the ingredient suits (`beef/pork/tea/…` — the tokens) as peers and errors when any two
share **both** colour and emblem. In the actual renders these two families never compete in the same
"which of these is it?" decision, and **each is fully dual-coded on its own axis** (see §2). So these
land as **false positives** — but they are worth clearing so the checker stays a meaningful tripwire.

**The 18 warnings** are almost all "same colour in normal vision (ΔE 0)" between a region and its own
ingredients (e.g. `north`/`beef`/`pork` all vermilion) — that is *by design* (region colour is shared by
its specialties) and every such pair is emblem/label-separated. Acceptable, no action.

### Headline good news (contradicts the identity's feared risk)

`identity.md` flagged a **red/green (vermilion N vs jade-teal C)** confusion risk for protan/deutan
viewers. **The chosen first-pass hues clear it.** The checker reports **no CVD collision between any two
of the four region colours** under protanopia, deuteranopia, or tritanopia — vermilion `#D64545`, jade
`#1F8A7A`, amber `#E6A930`, and indigo `#26324D` all stay perceptually distinct (ΔE above threshold) in
every simulation. The only CVD *closenesses* reported are both **dual-coded and non-region**:
`south`-amber vs `signature`-gold (protan ΔE 11→4, separated by circle vs spark) and `central`-jade vs
`pantry`-slate (deutan ΔE 34→10, separated by diamond vs beam). **The region palette passes
separability — no hue nudge is required for colour-blind safety.**

## 2. How the game is actually dual-coded (why the errors are false positives)

- **Tokens** (`token-key.png`): render as a **coloured disc + a unique 繁體 glyph** — 牛 / 豬 / 茶 / 圓 /
  蚵 / 魚 / 米 / 菜 / 補. The geometric emblems in `themes.py` (`beef→triangle`, `tea→diamond`, …) are
  **never rendered on tokens.** Every ingredient carries a globally-unique character — the strongest
  possible label channel, independent of colour. Colour-blind identification is trivial.
- **Dish cards** (`dishes_sheet_1.png`): the suit = **region**, shown three ways at once — coloured header
  band + region **name in caps** (NORTH/CENTRAL/SOUTH/EAST/SIGNATURE) + a row of the region emblem as VP
  pips (▲ N / ◆ C / ● S / ■ E / + signature). The 5 region emblems are **all distinct**. Recipes are
  **text** (牛肉 + pantry), not ingredient emblems.

So the geometric ingredient emblems that trip the checker are **vestigial** — they don't render anywhere.
There is **no colour-only channel in the shipped renders.**

## 3. The real failure — token glyph contrast (checker doesn't see it)

The prototyper's white-on-amber flag is correct, and it's worse than "modest." Computed WCAG ratios for
the **white 繁體 glyph on the token ground**:

| Token | Ground | White glyph | Verdict |
|-------|--------|-------------|---------|
| 蚵 oysters, 魚 milkfish | amber `#E6A930` | **2.08:1** | **FAIL** |
| 情報 assignment / signature headers | gold `#C9A227` | **2.42:1** | **FAIL** |
| 補 pantry | slate `#8A8F98` | **3.25:1** | fails body, ok large |
| 牛 豬 beef/pork | vermilion `#D64545` | 4.38:1 | ok (borderline body) |
| 茶 圓 tea/pearls | jade `#1F8A7A` | 4.22:1 | ok (borderline body) |
| 米 菜 rice/greens | indigo `#26324D` | 12.8:1 | PASS |

**Fix — flip the glyph to dark ink on the light grounds (do NOT darken the palette).** Set the token/
header text colour by ground luminance: **dark ink `#26324D` on amber / gold / slate**, keep white on
vermilion / jade / indigo. Result:

- dark ink on amber = **6.1:1** (PASS, from 2.08)
- dark ink on gold = **5.3:1** (PASS, from 2.42)
- dark ink on slate = **3.9:1** (better than white's 3.25)

This is a **token-renderer change** (per-suit text colour keyed to background luminance in the token/aid
build path), **not** a palette change — it preserves the "golden fried-food" amber identity `bg-theme`
wants. Darkening amber itself to make white pass would need ~L 0.18 (a muddy brown) and is the wrong
lever.

## 4. Meeple-Centred Design — category grades

1. **Colour blindness — PASS (in render) / WATCH (theme-data hygiene).** No colour-only channel: tokens
   dual-coded by unique 繁體 glyph, dish cards by distinct region emblem + name. Region palette passes CVD
   separability (feared red/green does NOT collapse). *Smallest fix:* reassign the 3 vestigial ingredient
   emblems so the checker reports 0 errors (§6).
2. **Low-vision / contrast / legibility — FAIL → fixable.** Page/body contrast excellent (9.4–10.4:1).
   **But** white-on-amber/gold token glyphs fail (2.1–2.4:1) — the one real fail (§3). Token 繁體 glyphs
   are large/bold and legible at Screentop zoom; dish-card body 繁體 is small but non-load-bearing (the
   romanised name carries it). *Smallest fix:* dark ink on light grounds (§3).
3. **Cognitive — PASS (light).** One action per turn; player aid ≤18 lines; ~1.8 weight; gateway-scaled.
   Hidden Missions add a small hidden-info layer but resolve on reveal — low working-memory load.
   Coordinate cuts with `bg-elegance`; nothing to add.
4. **Emotive — PASS (defer depth to `bg-critic`).** Warm, no elimination; the only "take-that" is
   Dead-drop, which is *giving a gift*. Competitive mode is framed as warm rivalry. Low tilt. Flagged for
   `bg-critic` to confirm the hidden-Mission bluff doesn't create feel-bad.
5. **Physical / motor — PASS.** Screentop default = click-drag, no dexterity or real-time; Larder cap 7 =
   small hand. Appropriate for the intended gateway audience.
6. **Communication — PASS / N/A.** This is a race/duel (+ 3–4 table-talk), **not** a constrained-comms
   co-op — no enforced no-talking rule, so no non-verbal-signal requirement. Hidden Missions are private
   but need no verbal channel. *(If a future co-op mode restricts talk, re-open this.)*
7. **Socioeconomic — PASS (strong), one watch.** Small card+token count, free Screentop playtest, low
   footprint — cheap and inclusive (ties to `funding-and-route-to-market.md`). **Watch:** the game is
   **language-dependent** (繁體 + English). Bilingual is the *right, respectful* choice for a Taiwan
   subject and aids the colour-blind dual-code — but it raises localisation cost and mild ESL/crystallised
   load. Net positive; note for `bg-funding`.
8. **Intersectional — one conflict, already resolved; one to watch.** *Resolved:* fixing token contrast
   by **darkening amber** would fight `bg-theme`'s fried-gold identity — sidestepped by changing the
   **glyph** colour, not the ground. *Watch:* the 繁體-glyph-as-dual-code is superb for colour-blind +
   cultural authenticity but is **dense at low Screentop zoom** for low-vision players — keep the disc
   large and the glyph bold; don't shrink it to fit more on screen.

## 5. Other legibility bugs (hand to `bg-infodesign` / prototyper — not palette)

- **Player-aid bullet markers render as `□` tofu** (missing glyph in the bullet character) — a font-
  coverage bug, reads as broken. Use a covered bullet (·, —) or an SVG marker.
- **Assignment card titles collide with the corner "7"** (e.g. "Operation: Southern Comfort7") — long
  titles overrun the VP number. Reserve the corner or shrink/ellipsize the title.
- **Placeholder map:** amber `#E6A930` as a **thin dashed outline on cream = 1.85:1** (near invisible);
  title overlaps the score-track box; EAST label overflows. Placeholder only, but note: **amber needs a
  fill or a darker edge when used as a thin element on cream** — it disappears as a hairline.
- **Player-aid subtitle:** vermilion `#D64545` on the indigo header = **2.92:1** (fails). Use cream/white
  for that subtitle. (The vermilion section headers on cream are 3.9:1 — ok as large headers.)
- `muted #7A6E58` on cream = **~4.45:1** — right at the body floor; fine for the caps/labels it's used on,
  keep it off long body runs.

## 6. The colour-blind checker false-positive fix (optional but recommended)

The 3 vestigial ingredient emblems can be reassigned to make the checker report **0 errors** at **zero
visual cost** (they don't render). Choose shapes that are globally unique in (colour, emblem) and CVD-safe
against every same-shape suit:

| Suit | `themes.py` change | Why safe |
|------|--------------------|----------|
| `beef` | `triangle` → **`square`** | vermilion vs indigo (other squares) never collapses under CVD |
| `tea` | `diamond` → **`hex`** | jade vs vermilion/amber (other hexes) never collapses |
| `rice` | `square` → **`circle`** | indigo vs amber/jade (other circles) never collapses |

*(These are recommendations for the human to apply in `tools/cards/themes.py`; `bg-access` does not edit
the theme.)*

## 7. Optional palette comfort (NOT required)

Region separability passes, so **no region hue nudge is needed.** The single closest warm pair is
`south`-amber `#E6A930` vs `signature`-gold `#C9A227` (protan ΔE→4) — already emblem-separated (circle vs
spark) and `signature` is rare. If extra comfort is ever wanted, deepen signature gold toward bronze,
e.g. `#C9A227` → **`#A9781C`**, to open the amber gap. Cosmetic only; recommend **not** spending the
churn now.

## Verdict

**CONCERN — one real WCAG fail (token glyph contrast), everything else PASS/WATCH.** The colour-blind
floor the identity worried about is actually met: the region palette clears CVD separability and the game
is fully dual-coded (unique 繁體 per token, distinct region emblems + names on cards). The 3 checker
errors are family-blind false positives. Fix the token contrast now; optionally clean the checker.

### Decision for the human

**Do now (not optional):** switch token/header glyphs to **dark ink `#26324D` on amber / gold / slate**
grounds (keep white on vermilion / jade / indigo). Fixes 2.1:1 → 6.1:1. Renderer change, no palette edit.

**Then pick one for the colour-blind checker:**

- **A (recommended) — clean the checker.** Reassign the 3 vestigial emblems (`beef→square`, `tea→hex`,
  `rice→circle`). Checker goes green, zero visual cost, keeps the tripwire meaningful for future sweeps.
- **B — accept the 繁體 dual-code.** Leave the emblems; document that tokens carry unique glyphs.
  Correct in practice, but the checker stays red (3 errors) and future guardian sweeps will re-flag it.
- **C — also nudge the palette.** Not warranted — regions already pass CVD; adds churn for no
  colour-blind benefit. Skip unless you want the optional signature-gold comfort nudge (§7).
</content>
</invoke>

---

# v6.2 Re-check — Guardian Sweep (2026-08-07)

> Guardian pass by `bg-access` after the v6.2 component build. Theme: `night-market`. Report-and-flag
> only (bg-prototyper owns `themes.py` this cycle — fixes below are RECOMMENDED with exact values, to be
> routed). Data: `components/{events,ingredients,tokens}.csv`, `player-aid.json`; theme `tools/cards/themes.py`;
> renderers `tools/cards/build_cards.py`, `tools/boards/build_board.py`.

## Checker

`python tools/access/check_access.py --game games/travel-agents --theme night-market`
**Result: 0 error(s), 3 warning(s).** Text contrast PASS (`ink` 9.4:1, `text` 10.4:1). Colour-blind
separability: **no colour-only collisions** — every confusable pair is dual-coded by emblem. The 3 warnings
(`mission`/`signature` ΔE 0; `mission`/`south` and `signature`/`south` ΔE 11) are the pre-existing
gold-cluster pairs, all dual-coded (`stamp`/`spark`/`circle`) — **not new v6.2 regressions.** The new
`sugar` suit (caramel `#B5835A` / `beam`) resolves clean against every neighbour; `seafood` is not a card
`type` so it never renders as its own card suit (South ingredient cards render as the South region suit).

## Focus items

**1. New glyphs seafood 海鮮 / sugar 糖 — CVD.** `sugar` card suit is dual-coded (`beam`, distinct from all
region emblems) — PASS. Physical tokens carry unique 繁體 (`海` / `糖`) + colour, glyph contrast auto-dark
(seafood 6.1:1, sugar 3.9:1 large-text) — PASS. **BUT on vendor PAY-row ingredient chips** (`build_cards.py`
L193-199) `resolve_suit` gives **pork=`hex`, tea=`hex`, seafood=`hex`** — three ingredients share one
silhouette. They are told apart by **colour + the 繁體 label** (豬/茶/海), not by shape. The mandatory
redundant-encoding rule PASSES (colour + label = two channels), but under protan/deutan red-`pork` and
amber-`seafood` colours converge, leaving only the small CJK label. → **WATCH.**

**2. Event scope icons ⦿ / ⬢ / ➤.** Triple-coded: glyph + word ("YOU" / "THIS REGION" / "NEXT DOOR") +
the `scope` data field (`self`/`region`/`neighbour`). Redundant encoding PASSES with zero colour
dependence. **BUT the render font WenQuanYi Zen Hei (the only CJK face, resolved first — cairosvg's toy
text API does not fall through the family list) has NO glyph for U+29BF ⦿, U+2B22 ⬢, or U+27A4 ➤.** They
render as **tofu boxes** in the exports and in the player aid (aid text L25-27 uses them). Meaning survives
via the words, but the at-a-glance icon — the whole point — ships broken. → **FLAG (legibility).**

**3. Win/lose piles 成團 / 遺珠.** Distinct 繁體 (`成` vs `遺`) + colour (gold `#C9A227` vs taupe `#7A6E58`,
glyph contrast 5.3 / 5.0:1) + full names in the aid. Distinguishable without colour. → **PASS.**

**4. Day / night distinction.** `build_cards.py` has **zero** phase handling — phase lives only in data
(`phase`/`deck`/`tags`) and `art_note`. A day/night recolour is being added. If the recolour becomes the
only on-card phase signal, colour-blind / low-vision players cannot tell a day card from a night card — and
this is load-bearing (Dusk clears the whole day layer). Note: ☀ U+2600 / ☾ U+263E / 🌙 are **also missing**
from the render font (would tofu). → **FLAG (pre-emptive — fail-in-waiting).** The recolour MUST carry a
non-colour, font-covered phase marker.

**5. Standing floor.** Four region colours (north `#D64545` / central `#1F8A7A` / south `#E6A930` / east
`#26324D`) stay CVD-distinct + four distinct emblems (triangle/diamond/circle/square) — checker green. WCAG
text contrast holds (9.4 / 10.4:1). Redundant encoding holds across regions (colour+emblem+name), tokens
(colour+繁體), scope (glyph+word+field), piles (colour+繁體). → **PASS.**

## Recommended fixes (route to bg-prototyper — exact values)

**FIX A — scope icons (do now; legibility).** The font can't draw ⦿ ⬢ ➤. Draw them as SVG shapes (like
`emblem_svg`) instead of font glyphs, centred at the effect-line lead:
- `self` ⦿ → ring + centre dot: `<circle r=R fill=none stroke=ink sw=3/><circle r=R*0.42 fill=ink/>`
- `region` ⬢ → reuse `emblem_svg("hex", …)` outline.
- `neighbour` ➤ → right-pointing triangle: `<polygon points="cx-R,cy-R*0.7 cx+R,cy cx-R,cy+R*0.7" fill=ink/>`
(A fallback font will NOT fix this — cairosvg's toy API resolves only the first family. Drawing is the fix.)

**FIX B — day/night phase marker (before the recolour ships; fail-in-waiting).** Add a corner phase badge
redundant to any recolour, using font-covered glyphs: **`日` (day) / `夜` (night)** as a small ink label, OR
a drawn sun (`<circle/>` + short ray strokes) / crescent-moon (two offset circles) SVG. **Do NOT use
☀/☾/🌙** — missing from the render font, they tofu. Phase must never be colour-only.

**FIX C — ingredient-chip shape (hardening; WATCH).** Make the five v6.2 chips shape-distinct so shape is a
third discriminator, not just colour+label. In `themes.py` night-market suits, change (chosen to avoid any
same-colour + same-emblem clash with a live suit):
- `"tea": {"color": "#1F8A7A", "emblem": "triangle"}`  (was `hex`; teal triangle — north triangle is red)
- `"seafood": {"color": "#E6A930", "emblem": "square"}`  (was `hex`; amber square — east square is indigo)
- keep `pork=hex`, `rice=circle`, `sugar=beam` → five distinct silhouettes.
Also: the chip label is the load-bearing non-colour code, so `make.sh` MUST keep passing `--tokens-csv`
(else `glyph_map` is `None` and chips render with no 繁體 — colour-only). Confirm it does.

## Verdict

**NOT a clean pass — 2 flags + 1 watch, all renderer/theme edits, none touching game rules.** The mandatory
redundant-encoding floor is MET everywhere (no meaning is ever carried by colour alone). The flags are
**legibility/rendering**: FIX A ships a visibly broken glyph today; FIX B prevents a colour-only phase code
before the recolour lands.

### Decision for the human — one fix now

**FIX A (scope icons as SVG shapes).** Do this now — it's the only item that ships a broken artifact in the
current build. FIX B is required but only once the recolour actually lands (block that PR on it). FIX C is
optional hardening. All three are `themes.py` / renderer edits for bg-prototyper; no data or rules change.

---

## v6.2 — day/night backs + two-state board (comfort check, 2026-08-07)

Guardian comfort-check on the bg-infodesign visual change (distinct day/night card backs + a
day/night board). Scope: the NEW colour pairings only, not a floor re-audit. `check_access.py
--theme night-market` still reports **0 errors** (3 dual-coded ΔE warnings, all emblem-separated — unchanged).

**Prior FIX B (pre-emptive) is now DISCHARGED.** The recolour landed with the required non-colour phase
marker: backs carry a DRAWN sun (disc+rays) vs crescent-moon motif + font-covered 日/夜 char + a
high-contrast ink word ("DAY · 早" / "NIGHT · 夜市"). A face-down pile sorts by shape + word, never colour.

**PASS**
- Day-vs-night backs are shape/motif-distinct (sun vs crescent) + char (日/夜) + word. Colour-blind sort holds.
- Back bottom label uses `panel_txt` (dark ink): DAY 11.6:1, NIGHT ~9.9:1 — the word channel is strong on both.
- Night back wordmark/motif (violet #B14FD8 on lilac panel): 2.6–3.3:1 — soft but clears large-text on the
  top stop and the meaning is redundant; acceptable for a decorative wordmark + dual-coded motif.
- Board, both states: ink text on grounds — day #26324D/#FDF4DB 11.6:1; night on lilac 6.7–8.0:1. Region
  headers/zone labels and the 日/夜 MARKET tiles read cleanly on both warm-day and neon-night grounds.
- No collision with region/ingredient language: the back is a whole-card indigo-border + panel + stamp
  treatment (not a suit chip); night violet is the intentional Buzz/promo hue.

**WATCH → one cheap fix (day back only)**
- The day back draws its sun motif + 日 char + "TRAVEL AGENTS" wordmark in `stamp` = day frame amber
  **#E6A930 on the cream panel = 1.6–1.9:1** (below even the 3:1 large-text bar). The floor still holds
  (the ink WORD label is high-contrast + the shape is distinct), so this is comfort, not a break — but the
  day back's sort-motif is faint for low-vision players while the night back is crisp.
- **FIX (themes.py, regenerates):** give the day back a dedicated darker stamp hue, e.g.
  `PHASE_STYLES["day"]["back_stamp"] = "#A65E12"` (bronze) and have `back_style` prefer `back_stamp` over
  `frame` for `out["stamp"]`. Gives ~4.5:1 (top) / 3.8:1 (bot) — comfortably above large-text on the full
  gradient. Leave the day FACE frame + board frame at #E6A930 (those are frame lines, not text — unaffected).
  Night back needs no change.

**Verdict:** PASS on the floor + board; one WATCH (day-back amber motif contrast) with an exact-hex fix.

---

# v6.3.1 Re-check — Guardian Sweep (2026-08-08)

> Guardian pass by `bg-access` after the v6.3.1 component rebuild. Theme: `night-market`. REPORT-and-flag
> only (bg-infodesign owns the render this cycle — no edits to `themes.py`/templates; fixes below are
> RECOMMENDED with exact values, to be routed). Data: `components/{vendors,events,tokens,ingredients}.csv`,
> `player-aid.json`; theme `tools/cards/themes.py`; rendered faces in `exports/` + `exports/screentop/`.

## Checker

`python tools/access/check_access.py --game games/travel-agents --theme night-market`
**Result: 0 error(s), 3 warning(s).** Text contrast PASS (`ink #26324D` 9.4:1, `text #2B2B2B` 10.4:1).
Colour-blind separability: **no colour-only suit collisions** — every confusable pair is dual-coded by
emblem. The 3 warnings are the standing gold-cluster pairs (`mission`/`signature` ΔE 0 → stamp vs spark;
`mission`/`south` and `signature`/`south` ΔE 11 → stamp/spark vs circle). All dual-coded, **not new
v6.3.1 regressions.** Four region colours stay CVD-distinct; floor holds.

## What's new in v6.3.1 — focus items

**1. Simplified vendor face — PASS.** The day/night vendor faces now carry only region label → PAY row →
DRAW 人氣 → ICON. Confirmed on `vend_central-day` / `vend_east-night` / `vend_south-night`:
- **Draw legible + not-a-score-safe:** the Draw number renders as a large dark olive/gold numeral on
  cream (day) / pale lavender (night) — strong contrast, clear top-of-hierarchy after the title. The
  "crowd-pull · not a score" caption disambiguates it from VP. No hierarchy regression from dropping
  score/Rep/perk — the face is *cleaner*, DRAW reads as the dominant number.
- **Region dual-coded:** "◆ CENTRAL 中" / "◉ SOUTH 南" / "■ EAST 東" = emblem shape + English caps + 繁體 +
  header-band colour. Four channels; not colour-only.
- **Region-icon-or-none dual-coded:** discount vendors show the region emblem chip + text ("C discount
  icon — …"); drinks show a neutral disc + "Drink — NO discount icon"; trophies show ★ + "trophy — top
  Draw, NO discount icon". The discount region is carried by emblem + letter + text, never colour alone.

**2. Night-marquee cross-region costs — PASS.** The 5 ingredient chips are shape-distinct in `themes.py`
(v6.2 FIX C landed): **pork=hex, tea=triangle, seafood=square, rice=circle, sugar=beam** — plus a unique
繁體 label (豬/茶/海/米/糖) and region colour. Every cross-region cost that actually co-occurs on one card
is distinguishable by shape **and** glyph **and** colour:

| Card | Cost | Chips (shape / glyph) |
|------|------|------------------------|
| 石板烤肉 Stone-Slab BBQ | {E:3, N:2} | circle 米 vs hex 豬 |
| 蚵仔煎 Oyster Omelette | {S:2, N:1} | square 海 vs hex 豬 |
| 棺材板 Coffin Bread | {S:2, E:1} | square 海 vs circle 米 |
| 擔仔麵 Tan-tsú-mī | {S:3, E:1} | square 海 vs circle 米 |
| 麻糬 Mochi | {E:2, C:1} | circle 米 vs triangle 茶 |
| 胡椒餅 Pepper Bun | {N:2, C:1} | hex 豬 vs triangle 茶 |

Chips stay readable at card scale (glyph bold, disc large). *Minor note (not a flag):* rice (filled
circle) and sugar (beam = ring + centre dot) are the two roundest silhouettes, but they **never co-occur
on a cost** (sugar appears only on single-cost day drinks) and are colour- + glyph-distinct regardless.
The "5 shape-distinct chips" claim holds.

**3. New tokens/markers — PASS.** All render as coloured discs + a unique glyph (verified on
`token-key.png`), distinguishable without colour:
- Reach 及 (teal `#1F8A7A`), Tours-Completed 團 (gold `#C9A227`), HSR-closed 停 (slate `#8A8F98`),
  clock 鐘 (vermilion `#D64545`), ★ Star (gold disc + dark star pictogram, now +2 Draw).
- The gold cluster (★ / 團 / 成 win-pile, all `#C9A227`) is told apart by glyph (a pictogram vs two
  distinct 繁體) and sits in different board zones — glyph is a legitimate redundant channel. OK.

**4. Scheduled Maintenance banner — WATCH (the one real flag).** The island-wide event (`EV-M01/M02`,
`scope=island`) and its board marker split into two verdicts:
- **Board marker 停 — PASS.** Slate disc + 停 glyph, distinct from every other marker.
- **The card — WATCH.** On `events_sheet_1.png` the two Maintenance cards render with the **same purple
  night-event header band and the same layout as every scoped hazard**, and carry a region deck-tag
  (NORTH / SOUTH) but **no scope icon** in the slot where scoped cards show the drawn ⦿ / ⬢ / ➤. Its
  island-wide nature — game-critical (it changes *everyone's* Travel for a round) — is therefore carried
  by **body text alone** ("ISLAND-WIDE (not a scoped event…)"). For a low-vision / at-a-glance / ESL
  player it reads like a region hazard. The task's "clearly distinct from the ⦿/⬢/➤ scoped events" is
  **not yet met** by a non-text channel. (Also: the card body is dense — ~9 small lines — a secondary
  legibility/elegance watch; `bg-elegance` could trim, the effect is also on the aid.)

**5. Standing floor — PASS.** Scope icons ⦿/⬢/➤ render as drawn SVG shapes + bilingual words + `scope`
field (v6.2 FIX A holds — no tofu). Four region colours CVD-distinct; WCAG page/body contrast 9.4/10.4:1;
redundant encoding everywhere. *(Pre-existing, not a v6.3.1 item: the amber "SOUTH 南" region-label text
is low-contrast on cream — but it is heavily redundant (band colour + circle emblem + caps + 南); no new
regression, no action.)*

## Intersectional conflict worth a human call

The Maintenance fix (below) wants a distinct **colour band** to set the banner apart — but colour must not
be the *only* new channel (colour-blind players). Solution keeps it honest: lead with a **distinct scope
glyph** (shape channel) and use colour only as a bonus, tied to the 停 marker's slate so card and board
token read as one object.

## Recommended fix (route to bg-infodesign — exact values)

**FIX — give Scheduled Maintenance a non-text "island-wide" channel** (data/theme/renderer layer,
regenerates; no rules change):
- **Add an `island` scope glyph** in the slot where `self/region/neighbour` draw ⦿/⬢/➤. Draw it as an
  SVG shape (like `emblem_svg`, never a font glyph) that is **shape-distinct** from the other three — e.g.
  concentric double-ring "whole island": `<circle r=R fill=none stroke=ink sw=3/><circle r=R*0.6 fill=none
  stroke=ink sw=3/>` — paired with the word **"ISLAND-WIDE 全島"** (font-covered 全島).
- **Optional colour tie (bonus channel):** give the banner a top stripe / header accent in the
  HSR-maintenance slate **`#8A8F98`** (matches the 停 board marker), so the card visually links to its
  reminder token *and* stands apart from the region-coloured event bands. Colour is the bonus, the glyph +
  word carry the meaning.
- **Secondary (optional):** trim the Maintenance body to ~5 lines (hand to `bg-elegance`) — the full rule
  already lives on the player aid.

## Verdict

**NEAR-PASS — one WATCH (Scheduled Maintenance visual distinctness), everything else PASS.** The mandatory
redundant-encoding floor is MET across the new vendor faces, cross-region cost chips, and all new tokens.
The single gap: the island-wide event is distinguishable from scoped events only by reading its body text.

### Decision for the human — one fix now

**Add an `island` scope glyph (double-ring SVG) + the word "ISLAND-WIDE 全島" to the Scheduled Maintenance
card**, optionally with a slate `#8A8F98` header accent tying it to the 停 board marker. Cheap
renderer/theme edit, regenerates, no rules or data-content change. Route to `bg-infodesign`. Everything
else in v6.3.1 ships clean.
