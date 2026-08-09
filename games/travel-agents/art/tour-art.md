# Tour (Booking) art + flavour — named real-Taiwan tours (V7+)

> The Bookings deck re-themed from abstract patterns into **named real-Taiwan TOURS** (landmark-clusters /
> routes / festivals). Every brief reads against [`art/art-style.md`](art-style.md) (the one look) and
> [`design/tour-themes.md`](../design/tour-themes.md). **Human-illustrated; no AI final art.** These are the
> boarding-pass tickets — the sole scoring vector — so **at-a-glance readability wins**: the tour name + a
> single clear icon-motif, the mechanical requirement stays legible.

**The style line to open every brief:**
> *Style: per `art/art-style.md` — stylised cartoon, boarding-pass / ticket shape language, night-market
> palette (warm day → neon night); one clear icon-motif, readable at card size. 繁體字. Human-illustrated; no AI final art.*

## ⚠ Sensitivity rails (BINDING — consultant verifies before print)
- **DEFAULT = pure thematic re-skin.** Every shipped tour maps onto an **existing, sim-validated booking
  pattern** — only the name / hanzi / flavour / art changed; count / cross-region shape / value are
  untouched. (Flagged new-pattern ideas are listed at the bottom — **not implemented**.)
- **Festivals framed SECULAR** — on the food / market / activity, never the worship: Lunar New Year
  *market* (年貨大街), Mid-Autumn *BBQ* (烤肉 + 月餅/柚子), Dragon-Boat *races + food* (划龍舟 + 粽), Lantern
  Festival *lights + food* (元宵燈會). **EXCLUDE** Ghost Month (中元/盂蘭盆), tomb-sweeping/Qingming, temple
  pilgrimages (Mazu 遶境) and any deity/temple rite.
- **CKS Memorial (中正紀念堂) is NOT shipped** (politically sensitive — authoritarian-era + transitional-
  justice debate). `d_north2` uses the **National Theater & Concert Hall (兩廳院)** + Dadaocheng instead, and
  its art brief explicitly says *avoid Liberty Square / CKS framing*. CKS is noted **for the consultant
  only**, never on a card.
- **`跨海` avoided** on `g_cross1` (renamed **Fusion Plate 融合料理**) — "across the sea" can read as
  cross-Strait/political; the fusion framing is cleaner and stays on-theme.
- Real landmark / route / festival names accurate + 繁體字; **dignified, celebratory, anti-tourist-gaze** — a
  local's day out, not a postcard.

---

## The named tour set (which pattern each re-skins)

### DAY deck
| Card id | Tour name (EN · 繁體) | Flavour category | Re-skins pattern (unchanged) |
|---|---|---|---|
| d_breakfast3 | Morning Market Breakfast · 晨市早點 | activity | 3 day-food (`day_food_vendors>=3`) |
| d_food3 | **Dragon-Boat Food Run · 端午美食** | **festival** | 3 food (`food_vendors>=3`) |
| d_travel3 | HSR Three-City Hop · 高鐵三城 | route | 3 regions (`regions>=3`) |
| d_collect4 | Full-Day Itinerary · 一日遊 | activity | 4 vendors (`vendors_total>=4`) |
| d_early3 | Beat the Crowds · 早起的鳥兒 | activity | 3 before dusk (`early_vendors>=3`) |
| d_cheap3 | Coin-Snack Tour · 銅板美食 | activity | 3 cheap (`cheap_vendors>=3`) |
| d_cheap2 | Budget Bites · 小資美食 | activity | 2 cheap (`cheap_vendors>=2`) |
| d_north2 | **Concert Hall & Dadaocheng · 兩廳院 & 大稻埕** | **landmark-cluster** | 2 North (`vendors_region:N>=2`) |
| d_south2 | Tainan Old-Capital Walk · 府城巡禮 | landmark-cluster | 2 South (`vendors_region:S>=2`) |
| d_central2 | Taichung City & Tea · 臺中舊城 | landmark-cluster | 2 Central (`vendors_region:C>=2`) |
| d_east1 | Taroko Day Trip · 太魯閣一日 | landmark-cluster | 1 East (`vendors_region:E>=1`) |
| d_deep2 | Become a Regular · 在地常客 | activity | depth 2 (`region_depth>=2`) |
| d_pairNC | Taipei–Taichung Line · 北中線 | route | pair N+C (`pair:N+C`) |
| d_pairSE | South-Link Coast Run · 南迴線 | route | pair S+E (`pair:S+E`) |
| d_drinks2 | Hand-Shaken Run · 手搖控 | activity | 2 drinks (`drinks>=2`) |
| d_mix1 | A Bite & a Sip · 一口一杯 | activity | food+drink (`food>=1;drink>=1`) |
| d_daymix | The Breakfast Set · 早餐配一杯 | activity | day-food+drink (`day_food>=1;drink>=1`) |
| d_prestige8 | Check-in Trail · 打卡美食 | activity | day Draw ≥8 (`draw_total_day>=8`) |
| d_contest1 | Out-Hype the Rival · 擠進去 | activity | 1 contested (`contested_wins>=1`) |
| g_travel3d | Round-Island Rail · 臺鐵環島 | route | 3 regions (`regions>=3`) |

### NIGHT deck
| Card id | Tour name (EN · 繁體) | Flavour category | Re-skins pattern (unchanged) |
|---|---|---|---|
| n_nightfood3 | **Mid-Autumn BBQ · 中秋烤肉** | **festival** | 3 night-food (`night_food_vendors>=3`) |
| n_nmfood2 | Neon Bites · 霓虹小吃 | activity | 2 night-food (`night_food_vendors>=2`) |
| n_allfood5 | Big Eater's Feast · 大胃王 | activity | 5 food (`food_vendors>=5`) |
| n_four | Four-Stop Night Run · 四處奔波 | activity | 4 vendors (`vendors_total>=4`) |
| n_collect6 | The Grand Tour · 大滿貫 | activity | 6 vendors (`vendors_total>=6`) |
| n_all4 | **Round-Taiwan · Cycling Route No.1 · 環島** | **route (flagship)** | all 4 regions (`regions>=4`) |
| n_star1 | Chasing a Star · 摘星 | activity | 1 apex (`apex_wins>=1`) |
| n_expensive1 | Marquee Splurge · 名店大手筆 | activity | 1 expensive (`expensive_vendors>=1`) |
| n_expensive2 | Two-Marquee Feast · 名店雙響 | activity | 2 expensive (`expensive_vendors>=2`) |
| n_prestige14 | Top of the Charts · 打卡人氣王 | activity | Draw ≥14 (`draw_total>=14`) |
| n_east2 | Hualien–Taitung Line · 花東線 | route | 2 East (`vendors_region:E>=2`) |
| n_deep3 | True Local · 在地老饕 | activity | depth 3 (`region_depth>=3`) |
| n_surfturf | Surf & Turf · 南北雙拼 | route | pair S+N (`pair:S+N`) |
| n_eastnorth | Taroko–Taipei · 東北連線 | route | pair E+N (`pair:E+N`) |
| n_censouth | Taichung–Kaohsiung · 中南連線 | route | pair C+S (`pair:C+S`) |
| n_cross1 | Border Dish · 跨區料理 | activity | 1 cross-region (`cross_region>=1`) |
| n_cross2 | Two Borders · 雙跨區 | activity | 2 cross-region (`cross_region>=2`) |
| n_contest2 | Queue-for-it · 排隊名店 | activity | 2 contested (`contested_wins>=2`) |
| n_final2 | Closing-Time Sprint · 打烊前 | activity | 2 final-round (`final_round_wins>=2`) |
| n_drinks3 | One More Round · 續攤 | activity | 3 drinks (`drinks>=3`) |
| n_allvenue | Dawn-to-Dusk Full Day · 全席 | activity | one-of-each-venue (`day_food>=1;night_food>=1;drink>=1`) |
| g_travel3n | **Lantern-Festival Circuit · 元宵燈會** | **festival** | 3 regions (`regions>=3`) |
| g_collect5 | **New-Year Market Haul · 年貨大街** | **festival** | 5 vendors (`vendors_total>=5`) |
| g_prestige12 | Money No Object · 揮金如土 | activity | Draw ≥12 (`draw_total>=12`) |
| g_cross1 | Fusion Plate · 融合料理 | activity | 1 cross-region (`cross_region>=1`) |

**Boundary cards untouched:** 黃昏 DUSK (`boundary_dusk`) and 末班車 LAST TRAIN (`boundary_lasttrain`) — the
deck-driven clock — keep their names, flavour, and art.

---

## Hero art briefs (the tours that carry a real landmark / festival)
*(The generic activity tours keep concise ticket-motif notes in `components/bookings.csv` `art_note`; the
place/festival tours below get the fuller brief so the landmark reads correctly and safely.)*

### d_north2 — Concert Hall & Dadaocheng 兩廳院 & 大稻埕 (landmark-cluster)
*Style line as above.* **Motif:** the twin swoop-roofs of the **National Theater & Concert Hall (兩廳院)**
beside a red-brick **Dihua Street** shophouse arcade; a boarding-pass frame. **Rail:** render the
Concert-Hall roofs — **do NOT** depict Liberty Square / the CKS Memorial hall. (CKS for consultant note only.)

### d_south2 — Tainan Old-Capital Walk 府城巡禮
*Style line.* **Motif:** an **Anping fort** silhouette over a Tainan oyster-flat, SOUTH stamp. Warm day.

### d_central2 — Taichung City & Tea 臺中舊城
*Style line.* **Motif:** the **Taichung station clock-tower** over rolling **tea terraces**, CENTRAL stamp.

### d_east1 — Taroko Day Trip 太魯閣一日
*Style line.* **Motif:** **Taroko gorge** marble cliffs over a rice-terrace coastline, EAST stamp.

### d_pairSE — South-Link Coast Run 南迴線 · d_pairNC — Taipei–Taichung Line 北中線
*Style line.* **Motif:** the two region emblems stamped together with a **rail/coast line** running between —
南迴 for S+E (winding south coast), a straight inter-city rail for N+C.

### n_all4 — Round-Taiwan · Cycling Route No.1 環島 (flagship route)
*Style line.* **Motif:** a **bicycle** over **four regional stamps forming a ring** around a stylised Taiwan —
the full 環島 lap. This is the deck's signature tour; give it the fullest, most joyful ticket art.

### n_east2 — Hualien–Taitung Line 花東線
*Style line.* **Motif:** two EAST stamps down the **花東 rift-valley** line — a gorge road + the roselle coast.

### Festival tours (SECULAR — food/market/activity only)
- **d_food3 — Dragon-Boat Food Run 端午美食:** a **dragon-boat prow** on a river (the wharf races) + festival
  **zongzi (粽)** food parcels along the bank. No rites.
- **n_nightfood3 — Mid-Autumn BBQ 中秋烤肉:** a **night grill** under a **full moon**, a **pomelo (柚子)**
  beside it. Secular cook-out. No rites.
- **g_travel3n — Lantern-Festival Circuit 元宵燈會:** lantern-lit stalls strung across a **night map**,
  **sky-lanterns** (Pingxi 平溪) rising — frame as *lights + food*, a night out, not a wishing rite.
- **g_collect5 — New-Year Market Haul 年貨大街:** the **Dihua-Street New-Year market** — red lanterns, dried-
  goods stalls, arms full of parcels. Secular shopping street.

---

## FLAGGED for `bg-design` — tours that would need a genuinely NEW pattern type (NOT implemented)
> These were tempting richer tours the CD's direction gestures at, but each needs a **new target-predicate
> type** the sim hasn't validated. **All shipped cards above are pure re-skins** onto existing patterns; the
> ideas below are parked for a bg-design pattern add + **balance/re-sim** decision.

1. **Specific-named-vendor set** — e.g. a *true* Dadaocheng cluster requiring **N02 Dihua + N07 Wharf
   specifically** (not "any 2 North"). Needs a `has_vendors:N02,N07`-style **set-match predicate**.
   Currently shipped as the looser `vendors_region:N>=2` (d_north2). *Highest-value add if a
   landmark-cluster tour should feel truly place-specific.*
2. **City-level granularity ("one per city")** — finer than the four regions (e.g. "a bite in 3 different
   *cities*"). No city field exists on vendors (region only); needs a `place`/city taxonomy on the pattern
   side + a `cities>=N` predicate. City-hop flavour is currently carried at **region** level
   (d_travel3 / g_travel3d / g_travel3n).
3. **Ingredient/recipe-typed collection** — e.g. Mid-Autumn BBQ as "collect **3 肉/grilled** dishes", or
   Dragon-Boat as "collect **糧/zongzi** dishes". Needs a `recipe_contains:<ingredient>>=N` predicate keyed
   on the vendor recipe. Currently shipped as generic **night-food-count** (n_nightfood3) and **food-count**
   (d_food3) — the festival is flavour only, the count is ingredient-agnostic.

Each of the three would change what patterns are reachable and how the tickets economy scores → **re-sim
required** before shipping. Until then the set stays as validated re-skins.
