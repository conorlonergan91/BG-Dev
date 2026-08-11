# Travel Agents — Card Backs (the market back)

> Owning brief for the **card back**. Cite `art/art-style.md` first (the one look), then this. Slug:
> `travel-agents`. Owned by `bg-art-director`.
>
> **CD steer (2026-08):** the back should feel like **Taiwan's traditional local market**, not a
> boarding-pass. **DAY back = the morning/wet market** (菜市場 / 傳統市場 / 早市) — a warm neighbourhood
> covered lane where dignified elders do their morning rounds choosing produce; baskets, stacked veg,
> hanging greens, steam. **NIGHT back = the 夜市 night market** — lanterns, neon glow, sizzling stalls,
> evening crowd. **The game name (wordmark) is GONE from the back** — everyone already knows what they're
> playing.

---

## The hard function (never lose this)
The back MUST stay **day-vs-night sortable face-down by MOTIF + palette, never colour alone** — setup and
storage rely on splitting a face-down pile into day and night at a glance. Beyond palette, the sort is
carried by **the central silhouette (produce basket by day vs hung lantern by night)**, the **大字 phase
glyph (早 vs 夜)**, and the **drawn sun vs moon** accent. A colour-blind player must still sort the pile.
Keep a **neutral / any-time** variant working (mixed or unphased decks, and the boarding-pass Bookings deck).

---

## The illustrated vision (for when real, human-illustrated art lands)
This is the direction final art follows. The back has **no game UI on it**, so it can carry a richer
painted scene than the card faces — a single centred market vignette or a quiet tiled market pattern, either
reads. Same house hand as everything else (per `art/art-style.md`): clean confident linework, bold mostly-
flat colour with soft cel-shading, the night-market palette, dignified locals, faithful real produce/dishes,
**secular** settings only.

- **DAY — the morning / wet market (菜市場 · 傳統市場 · 早市).** A warm covered neighbourhood lane at
  morning light. **Dignified elders — aunties and uncles — doing their morning rounds**, choosing produce
  with a discerning eye: hefting a melon, filling a woven basket, pointing out the good greens. Stacked veg
  and fruit crates, **hanging greens**, a **bamboo steamer** breathing steam, hand-painted **繁體** stall
  signs. Warm morning gold; the calm, unhurried, everyone-knows-everyone feeling of a real 菜市場. The elders
  are the warm heart of the scene — never frail, never a caricature; sharp, capable, at home in their patch
  (the same dignity rail as The Old Councillor / The Globetrotter).
- **NIGHT — the 夜市 night market.** The same lane after dark: **strings of lanterns**, neon glow, sizzling
  griddles, rising steam, an evening crowd threading between stalls. Warm-neon violet/teal over dusk-indigo —
  festive, never a cold/alarm register (identity.md's day/night grammar: warm, not alarm).
- **NEUTRAL / any-time.** A quieter any-time market read — a lone **bamboo-steamer** or a single stall
  vignette, or a simple tiled market pattern. Gold-neutral.

Even fully illustrated, keep the **basket-dominant (day) vs lantern-dominant (night)** silhouette so the
face-down sort survives at a glance.

**Rails (binding):** 繁體 (Traditional) never Simplified; secular (no temple/deity/ghost-month/funerary);
dignified locals, faithful produce; **English names first**; human-illustrated final art (AI = labelled,
gitignored mock-ups only). Elders and any real produce/signage are **consultant-gated** before final/print.

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
