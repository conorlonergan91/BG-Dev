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
