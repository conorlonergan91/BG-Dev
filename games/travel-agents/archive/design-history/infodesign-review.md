# Information Design review — Travel Agents: Taiwan

Guardian pass by `bg-infodesign` on the rendered `night-market` build. Question: can a player parse the
components at a glance and stay in flow without the rulebook? Verified against the actual exports
(`dishes_sheet_1.png`, `assignments_sheet_1.png`, `player-aid.png`, `token-key.png`, `map.png`,
`grand-dossier-track.png`, `cover.png`) traced back to `components/*`, `tools/cards/themes.py`
(`night-market`), and the three builders (`build_cards.py`, `build_cover.py`, `build_board.py`).

Every fix is tagged **[DATA]** (edit a CSV/JSON), **[TOOLING]** (edit a builder), or **[ART]** (deferred
layout/illustration). I made **no data edits** — the high-value fixes are all tooling/art, and the one
tempting data edit (assignment titles) is a flavour call that belongs to `bg-theme`/you. Details below.

---

## 1. The icon system (symbol → meaning)

### Region grammar — the through-line (GOOD, and consistent on the dish deck)
Every region is triple-coded: **colour + emblem shape + 繁體 label**. This is the game's strongest piece
of information design and it's colour-blind-safe.

| Region | Colour | Emblem | Specialties |
|---|---|---|---|
| North 北 | vermilion `#D64545` | ▲ triangle | beef / pork belly |
| Central 中 | jade teal `#1F8A7A` | ◆ diamond | tea / tapioca pearls |
| South 南 | amber `#E6A930` | ● circle | oysters / milkfish |
| East 東 | indigo `#26324D` | ■ square | mountain rice / wild greens |
| Signature | gold `#C9A227` | ✦ spark | cross-region feasts |
| Assignment | indigo `#26324D` | ▣ stamp | secret "Operation" |

### Ingredient tokens — colour = region, glyph = 繁體 specialty (GOOD, compact, language-appropriate)
| Glyph | Ingredient | Colour |
|---|---|---|
| 牛 | beef | red (N) |
| 豬 | pork | red (N) |
| 茶 | tea | teal (C) |
| 圓 | tapioca pearls | teal (C) |
| 蚵 | oysters | gold (S) |
| 魚 | milkfish | gold (S) |
| 米 | mountain rice | indigo (E) |
| 菜 | wild greens | indigo (E) |
| 補 | pantry (wild / anywhere) | slate |
| 情報 | Insider Tip / intel | olive |
| A/B/C/D | player-agent markers | — |

### Gaps & overloads found
- **GAP (load-bearing): dish recipes use NONE of the above.** The recipe is English prose inside the
  flavour line (`"…· Beef + pantry · …"`). There is **no visual bridge** between the token a player is
  holding (red circle 牛) and the dish that needs it (the word "Beef"). This is the #1 issue — see §2.
- **LATENT OVERLOAD: three competing ingredient vocabularies.** (a) `ingredients.csv` `emblem` column
  names pictograms (`ox-slice`, `pork-belly`, `fish`…) that **are not implemented** in `emblem_svg()` and
  render nowhere. (b) `themes.py` assigns ingredient **shape**-emblems (beef=triangle, pork=hex,
  tea=diamond, pearls=circle, oysters=hex, milkfish=diamond, rice=square, greens=triangle) that are also
  never rendered (tokens use hanzi) **and reuse the region pip shapes with different meanings** — a
  triangle currently means *North* (dish pip), *beef*, **and** *greens*. If those shapes are ever drawn
  on tokens, one symbol = three meanings, breaking the "one symbol, one meaning" rule.
  **Recommendation:** canonicalise **ingredient = region colour + 繁體 glyph** (exactly what the tokens
  already do). Do not render the ingredient shape-emblems. Treat the `ingredients.csv emblem` column as
  dead/aspirational — either implement it as real pictograms later, or drop it to kill the third
  vocabulary. **[DATA/TOOLING — recommend]**

---

## 2. Hierarchy & layout, per component

### Dish cards — the recipe must become the 2nd read
Intended reads: **1) VP → 2) recipe (what it costs to plate) → 3) region + flavour.**
- **1st read is right:** the white VP index top-right leads cleanly; the pip row + numeral reinforce.
- **Region is over-encoded (4×):** header colour + type emblem + type label + pip shape all say the same
  thing. VP is stated 3× (index, pip count, numeral).
- **The recipe — the one thing you check every turn — is stated 0× as an icon** and buried mid-sentence
  in 34px prose. It does **not** survive the squint.
- **Fix [TOOLING]:** add a **recipe chip-row** directly under the title — one chip per required
  ingredient, each = region-colour circle + 繁體 glyph (identical to the physical token), reading the
  already-structured `recipe` column (`beef;pantry`). Signatures show their 3 cross-region chips. Size
  ~40px so it survives table distance. This is the token↔card bridge; the data already exists, so it's a
  pure builder change (a `travel-agents` card template, or a "draw recipe row if a `recipe` column
  exists" branch in `build_cards.py`). If space is tight, drop one redundant region cue (keep header
  colour + type emblem; the pip row can stay as VP).

### Assignment cards — objective buried, constant "7" shouts, title clips
Confirmed the prototyper's flag: long "Operation:" titles collide with the top-right index on **A01, A05,
A06, A10 (One Grand Feast), A12, A13, A14** — the `name` is one un-wrapped 50px line and the white "7"
sits on top of its tail.
- **Root cause of the clip is also an elegance problem:** the index is **always 7** on all 15 cards, so
  the card's biggest element carries zero information while stealing the title's width.
- Intended reads: **1) the objective (what must I plate?) → 2) the reward.** Today it's inverted: a
  meaningless constant "7" dominates and the objective hides in HANDLER flavour prose.
- **Fix [TOOLING] (recommended, fixes clip + hierarchy in one move):**
  1. Remove the big header index for the assignment deck (or replace with a small `+7 VP` footer chip),
     freeing the full title width — this alone stops the collision.
  2. Wrap the title to 2 lines.
  3. Surface a bold one-line **requirement** at the top of the body, generated from the `target` column
     (e.g. `PLATE ● ●● — 3 dishes, each a South ingredient`), with the HANDLER flavour beneath it. Now
     the win-condition is the 1st read and flavour recedes.
- **Fix [DATA] (fallback, only if you don't want tooling work):** drop the `"Operation: "` prefix from
  each `name` (the `ASSIGNMENT` type line already carries that context) — "Southern Comfort",
  "Round the Island", etc. all fit one line. **I did NOT do this**: "Operation:" is deliberate
  spy-thriller identity flavour, so it's `bg-theme`'s call, not a safe mechanical shortening. Flagged as a
  decision below.

### Player aid — content GOOD, one glyph bug
Well-structured, within the 18-line budget, "one action = one line" reads cleanly. **Bug:** the bullet
`•` renders as a tofu box (□) — U+2022 is missing from *WenQuanYi Zen Hei*.
- **Fix [TOOLING]:** in `render_aid()` replace the `"•  "` bullet with a drawn dot (tiny SVG `<circle>`)
  or a CJK-safe glyph (`·` U+00B7 / `‧`), or add a Latin fallback face carrying U+2022. Cosmetic, cheap.

### Tokens & Grand Dossier track — GOOD
Token key is compact, legible, and language-appropriate (繁體 in region-coloured chips; region reads by
colour grouping). Grand Dossier track is clean — milestones 4/8/12/16 clear, current position obvious.
No changes needed.

---

## 3. The map — non-functional placeholder (deferred ART)

`map.json` self-declares as a schematic placeholder, and it shows: the fixed title bar overlaps the
"Shared score track" zone; long zone labels overflow their dashed boxes ("EAST 東 (MOUNTAIN RICE / WILD
GR…" clips off-card); the bottom Grand Dossier label overruns and overlaps its sub-line; and the
**adjacency — the actual load-bearing spatial info — is prose, not drawn.**

### Brief for a readable functional map [ART/LAYOUT — bg-infodesign owns]
A player must answer three things from the map at a glance: *where am I, where can I go, what's there.*
- **Draw the ring + HSR spine as EDGES**, not sentences: North–Central–South–East–back-to-North as a
  loop, plus the west-coast HSR line making North–Central–South mutually adjacent. Adjacency is the map's
  whole job; render it as lines/rails between nodes.
- **Four region nodes**, each carrying the full region grammar: colour + emblem + 繁體 + specialty chips
  (the same ingredient chips from the recipe row). "Pantry available everywhere" marked once, unobtrusively.
- **Start positions** (Agent North, Agent South) shown as pips on their nodes.
- **Fit text to nodes** — short labels ("北 North · 牛豬"), never overflowing.
- **Drop the two edge tracks from the map.** The Grand Dossier already has its own clean standalone
  component; the 0–60 score track is generic. Removing them clears the title overlap and the bottom
  overflow, and lets the map do one job well.
- Title must sit in its own band, clear of all zones.
This can stay schematic (no illustration required) and still be functional — a clean node-and-edge
diagram beats the current overlapping dashed boxes. Real coastline art is a later polish.

---

## 4. Cover — title overflow (cheap TOOLING)

`build_cover.py` sets the title at `font-size = W*0.11` (112px on a 1024-wide cover) with no
fit-to-width, so "Travel Agents: Taiwan" clips both ends ("ravel Agents: Taiwa").
- **Fix [TOOLING]:** compute the title size from `min(W*0.11, (W - 2*pad) / (0.6 * len(title)))`, or wrap
  to two lines when the title exceeds one line's width. Purely cosmetic (a placeholder cover), but it's a
  two-line change.

---

## At-a-glance verdict (squint test)

| Component | Verdict | What survives / what's lost |
|---|---|---|
| Dish cards | **FAIL on recipe** | Survives: region colour, VP number, region shape. Lost: **what it needs to plate.** |
| Assignment cards | **FAIL** | Only a meaningless constant "7" survives; the objective is invisible + the title clips. |
| Player aid | PASS (glyph bug) | Reads well; only the bullet is broken. |
| Tokens | PASS | Colour + 繁體 both survive. |
| Grand Dossier track | PASS | Milestones + position clear. |
| Map | FAIL | Overlap/overflow; adjacency not drawn. |
| Cover | FAIL (cosmetic) | Title clipped. |

---

## Decision for the human — pick one to do FIRST

- **A) Dish recipe chip-row [TOOLING].** Highest play impact: builds the missing token↔card bridge so
  players stop reading prose to know what a dish costs. Data already supports it. **← recommended.**
- **B) Assignment index + title fix [TOOLING].** Kills the visible clip and un-buries the objective;
  removing the constant "7" is also an elegance win.
- **C) Map redesign [ART].** Biggest visual improvement, but deferrable — playtests can lean on the
  text-described adjacency for now.

**Recommendation: A now, B next (both are small builder changes to the same file), C when art time frees
up.** The assignment-title *flavour* question ("Operation:" prefix — keep and fix in tooling, or drop in
data) is a separate call for `bg-theme`/you.
