# Travel Agents — Card Backs (the market back)

> Owning brief for the **card back**. Cite `art/art-style.md` first (the one look), then this. Slug:
> `travel-agents`. Owned by `bg-art-director`.
>
> **CD steer (2026-08, updated — illustrated vendor backs, Ghibli hand, NO humans):** the vendor-deck backs
> become **illustrated shop scenes** (replacing the code-drawn market motif) — **NO humans in either, just
> the shop/stall.** **DAY back = a Taiwanese breakfast-shop (早餐店)** storefront — the soy-milk-and-egg-crepe
> morning feel (a hot griddle, a 豆漿 urn, stacks of 蛋餅 egg crepes and 燒餅油條, a 繁體 menu board, gentle
> steam, warm morning gold). **NIGHT back = the 夜市 night market** — a stall/lane of paper lanterns, neon
> glow, sizzling griddles and rising steam. **NO people in either scene.** Painted in the warm hand-painted
> **Studio-Ghibli-inspired** hand (per `art/art-style.md`). Embeddable filenames
> **`FIG-BACK-VEND-DAY.png` / `FIG-BACK-VEND-NIGHT.png`** (portrait card-back, 750×1050). **The game name
> (wordmark) stays GONE from the back** — everyone already knows what they're playing.
>
> *(This **supersedes** the earlier "morning/wet market 菜市場 with dignified elders doing their rounds" day
> vision: the CD now wants a **breakfast-shop** and **no humans**. The two Indigenous/consultant rails and
> the face-down sort function below are unchanged.)*
>
> **⚑ Wiring is a LATER step (orchestrator):** these two PNGs are **briefs only** for now. Dropping them in
> as the vendor-deck backs is a follow-up render step (embed behind the back layer in `build_cards.py`) the
> orchestrator does **once the CD delivers the art**; the deterministic code back below stays the shipping
> playtest back until then. Paste-ready generation prompts live in `art/mockup-kickoffs.md`
> (`FIG-BACK-VEND-DAY` / `FIG-BACK-VEND-NIGHT`).

---

## The hard function (never lose this)
The back MUST stay **day-vs-night sortable face-down by MOTIF + palette, never colour alone** — setup and
storage rely on splitting a face-down pile into day and night at a glance. A colour-blind player must still
sort the pile. Keep a **neutral / any-time** variant working (mixed or unphased decks, and the
boarding-pass Bookings deck).
- **On the shipping code back:** the sort is carried by **the central silhouette (produce basket by day vs
  hung lantern by night)**, the **大字 phase glyph (早 vs 夜)**, and the **drawn sun vs moon** accent.
- **On the illustrated vendor backs (`FIG-BACK-VEND-*`):** the sort is carried by the **whole scene** —
  **a breakfast-shop (早餐店) in warm morning gold (DAY)** vs **a lantern-lit 夜市 stall/lane in neon
  night (NIGHT)** — a distinct motif *and* a distinct palette, so the split survives without colour alone.

---

## The illustrated vision (for when real, human-illustrated art lands)
This is the direction final art follows. The back has **no game UI on it**, so it can carry a richer
painted scene than the card faces. Same house hand as everything else (per `art/art-style.md`, CD Ghibli
pivot 2026-08): **warm hand-painted Studio-Ghibli-inspired anime** — soft painterly light, gentle organic
outlines, luminous colour, delicious "Ghibli food" warmth, faithful real produce/dishes, **secular**
settings only. **NO humans in either scene — just the shop/stall.**

- **DAY — the breakfast-shop (早餐店).** A warm, cheerful Taiwanese morning breakfast-shop storefront seen
  head-on: a hot flat griddle, a big **豆漿 (soy-milk)** urn, stacks of rolled **蛋餅 (egg crepes)** and
  **燒餅油條**, a hanging **繁體** menu board, gentle rising steam, warm morning-gold light. The cozy,
  everyone's-neighbourhood-breakfast feeling — **but no people; the shop itself is the hero.**
- **NIGHT — the 夜市 night market.** A food stall/lane after dark: **strings of paper lanterns**, a little
  **neon** sign, sizzling griddles, hanging skewers and food, rising steam into a dusk-violet sky.
  Warm-neon violet/teal over dusk-indigo — festive, never a cold/alarm register (identity.md's day/night
  grammar: warm, not alarm). **No people — the stall/lane and its lights are the hero.**
- **NEUTRAL / any-time.** A quieter any-time market read — a lone **bamboo-steamer** or a single stall
  vignette, or a simple tiled market pattern. Gold-neutral.

Even fully illustrated, keep the **breakfast-shop-dominant (day) vs lantern-dominant (night)** read so the
face-down sort survives at a glance.

**Rails (binding):** 繁體 (Traditional) never Simplified; secular (no temple/deity/ghost-month/funerary);
dignified locals, faithful produce; **English names first**; human-illustrated final art (AI = labelled,
gitignored mock-ups only). Any real produce / stall signage / 繁體 menu text is **consultant-gated** before
final/print.

---

## The shipping code back (deterministic SVG — the playtest back until real art exists)
Full buildable spec for `tools/cards/build_cards.py` + `themes.py` lives in `decision-log.md` (dated
2026-08) and was handed to the CD to implement. In brief, the code back is:

- **A striped market-awning valance** across the top (scalloped candy-stripe canopy) — replaces the removed
  wordmark band and instantly says "market stall / covered lane".
- **A central market medallion:** a soft plate ring holding **a woven produce basket (DAY)**, **a hung
  lantern (NIGHT)**, or **a bamboo steamer (neutral / any-time)** — all DRAWN from SVG primitives, single-ink
  silhouettes matching the existing stamp aesthetic; plus a small **drawn sun / moon** accent and the **大字
  繁體 phase glyph (早 / 夜 / 通)**.
- **A receding stall-lane silhouette** low along the foot — little awning-topped booths with hanging bulbs,
  low-contrast, for the bustling-lane atmosphere.
- **Minimal text only:** the phase glyph + a small **繁體 market-name** label (早市 · MORNING MARKET / 夜市 ·
  NIGHT MARKET / 市場 · MARKET). **No game name anywhere.**
- Palette per phase from the existing `PHASE_STYLES`: day = warm sunrise cream + festive vermilion awning;
  night = dusk→lavender + neon-violet awning; neutral = gold. The constant dusk-indigo border stays (the TA
  edge on every back).

The 繁體 market-name labels (菜市場 / 早市 / 夜市 / 市場) are **provisional playtest text — consultant-gated**
before final/print (same status as the existing 全天 note).
</content>
</invoke>
