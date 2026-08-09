# V7+ — Named real-Taiwan TOURS (Bookings re-theme) — CD direction, 2026-08-09

**The move (CD):** re-theme the **Bookings** (the tour objectives / scoring cards) from abstract patterns
into **named, specific real-Taiwan tours** that tie in **landmarks / routes / festivals** around the vendor
locations. Makes the "you're a travel agent building tours" fantasy literal and stacks on the real-place
vendor grounding (`design/vendor-places.md`).

## The three tour flavours (all map onto existing booking patterns where possible)
1. **Landmark-cluster tours** — a sightseeing hook + eat nearby. *e.g.* "**Liberty Square & Dadaocheng**":
   see the National Theater & Concert Hall, then grab breakfast on **Dihua Street** + tea at the **wharf**
   (nearby). → maps to a **2–3 vendor set in an area/region** pattern.
2. **Route tours** — a journey across the island. *e.g.* "**環島 Round-Taiwan (Cycling Route No.1)**": one
   vendor in **every region** → this IS the existing **cross-region coverage** pattern (遍地開花 "Blossoming"),
   re-skinned. Also city-hop variants.
3. **Festival tours** — a seasonal Taiwanese occasion, framed on FOOD/MARKET/ACTIVITY. *e.g.* "**Lunar New
   Year Market**" (年貨大街 at Dihua St), "**Mid-Autumn BBQ**" (烤肉 + mooncakes/pomelo), "**Dragon-Boat
   Festival**" (races + zongzi/BBQ), "**Lantern Festival**" (元宵 lanterns + tangyuan). → map onto count/value/
   pairing patterns.

## Mechanical note (preserve balance)
- **Default = thematic RE-SKIN**: map each named tour onto an EXISTING booking pattern, preserving its
  difficulty (count / cross-region shape / value) so the sim-validated tickets economy is unchanged. Most of
  the CD's ideas fit an existing pattern (coverage, pairs, value, region-count).
- **Flag for bg-design**: any tour that wants a genuinely NEW pattern type — e.g. "collect these **specific
  named** vendors" or "one per **city**" (finer than region) — since that could touch balance. Decide re-skin
  vs new-pattern per tour; new patterns → assess re-sim need.
- Works hand-in-glove with the **generic-ingredient taxonomy** (`ingredient-taxonomy.md`): more dish variety
  → richer, more specific tours.

## ⚠ Sensitivity (BINDING — consultant verifies before print)
- **Festivals framed SECULAR**, on the food/market/activity: Lunar New Year *market*, Mid-Autumn *BBQ*,
  Dragon-Boat *races/food*, Lantern Festival. **EXCLUDE** Ghost Month (中元/盂蘭盆), tomb-sweeping/Qingming
  (funerary), temple pilgrimages (e.g. Mazu 遶境) and any deity/temple rite. When in doubt, it's about the
  eating and the outing, not the worship.
- **CKS Memorial (中正紀念堂) is politically sensitive** (Chiang Kai-shek / authoritarian-era + transitional-
  justice debate) — the CD floated it; **flag to the consultant** and PREFER less-charged landmarks:
  National Theater & Concert Hall (the "opera house"), Taipei 101, Dadaocheng/Dihua St, Ximending, Sun Moon
  Lake, Taroko Gorge, Alishan, Jiufen, Kaohsiung Pier-2, the cycling route. Use CKS only if the consultant
  okays the framing.
- Real landmark/route/festival names accurate + Traditional characters; dignified, celebratory, anti-tourist
  -gaze (a local's day out, not a postcard).

## Sequencing
Part of the **Bookings re-theme**, alongside the vendor real-place layer. Order: (a) bg-infodesign structural
render lands → (b) ingredient-taxonomy redesign (`ingredient-taxonomy.md`) → (c) apply vendor real-places to
the data → (d) **this: bg-theme names the tours + maps each to a pattern (bg-design flags any new pattern
type + re-sim)** → (e) render the Bookings with tour names + art-briefs (citing `art/art-style.md`) → rulebook.
Owned by bg-theme (naming/flavour) + bg-design (pattern integrity) + bg-infodesign (card layout).
