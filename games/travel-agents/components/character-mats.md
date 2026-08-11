# Character mats — design notes (v6.3.1)

Companion to `characters.csv`. The CSV carries the **locked v6.3.1 kits** (re-sim-validated, band
43.5–55.2%); this note records the **reserve dials**, the **infodesign icon asks**, and the FTUE
watch-flags for the Director. Data is the source of truth — change the kit in `characters.csv`, not in a
rendered mat.

## The FIVE locked v6.3.1 mats
| Mat | Ability | Flaw | Re-sim |
|---|---|---|---:|
| 里長伯 Lí-tiúⁿ-peh | **Old Favours (home turf)** — name ONE home region at setup; −1 ingredient discount there only | **The Away Tax** — +1 of any one ingredient to Sign Up anywhere else | 55.2% |
| 媽寶 Ma-pó | Mum's Packed Lunch (Travel draws the region you LEFT) | none (Market Run keep-2 normal) | 43.5% |
| 大胃王 Tuā-uī-ông | Bottomless (Market Run keep all 3) | hazards fire TWICE on his Market Run | 54.8% |
| 網紅 Bāng-âng | Going Viral (Promote places 3 Buzz, still Reach-capped) | **goes last** (turn order only — lost-turn flaw RETIRED) | 51.2% |
| 老大 Lāu-tuā | Everybody Knows 老大 (win a Buzz fight at a ≥1 lead, not the usual ≥2) | none (Option D) | 50.7% |

Everyone **starts Reach 2** and **starts in Taipei** (the North hub, CD-3). No kit changes those.

## 里長伯 — REWORKED (v6.3.1 CD-1, LOCKED −1 home / +1 away, start-Reach 2)
The old island-wide/first-two-region Old Favours **+ the no-HSR flaw** are both **RETIRED** (the no-HSR
concept is re-homed as the table-wide *Scheduled Maintenance* event). The new silhouette is **home-turf
advantage / away-from-home cost:**
- **Setup:** picks **ONE home region** (open, after mats are dealt). He still starts his pawn in Taipei
  like everyone — home is a strategic *build* declaration, not a start position.
- **Ability `discount_home`:** his **−1 ingredient** discount applies **only in his home region** (stacks
  with the region-icon ramp; floors at 0).
- **Flaw `away_tax`:** Signing up in any region other than home costs **+1 of any one ingredient** (his choice
  of type). On a cross-region →X night dish it is still just +1 of one chosen type.
- **⚠ CANON vs sim:** the committed sim module defaults to `TA_COUNCILLOR_REACH=1` (a start-Reach-1 variant
  the CD did **NOT** take). **Canon = start-Reach 2** (built here). The −1/+1 kit lands 55.2% (top-of-band)
  and the CD accepted it as-is.
- **Two mat icons → bg-infodesign:** a **home-region discount marker** + an **away-tax reminder**.
- **FTUE watch:** with the common Taipei start he picks North home ~60% and signs up home ~75% — a thematic
  "borough boss," watch it doesn't read as a *stuck* camp. **Reserve levers (only if the table confirms a
  problem):** `+2 away-tax` → ~50% but deepens the camp; **start-Reach 1** → ~45.5% (a clean second flaw
  that does NOT worsen the camp) — the preferred brake if one is ever wanted, but **not adopted now.**

## 網紅 — the lost-turn flaw RETIRED
Built to `goes_last` only. The v6.2 "Late to the Party" **lost-turn** flaw is **RETIRED**: the re-sim
landed the influencer at **51.2% with the flaw retired** vs **~41% with it** — the lost turn over-taxed a
Buzz-heavy kit now that the Buzz fight matters *less* to the score (points come from tickets). *(This is a
character-kit recommendation the re-sim surfaced, carried into the build — not part of the CD's three-call
balance lock, which was CD-1/CD-2/CD-4.)* **Reserve dial** if it tests too strong at the table: re-add a
light lost-turn (`late_to_night` — miss the first night-phase turn) or trim the ability (+1 Buzz on the
first Promote only).

## 老大 — the Buzz-margin override (no vendor data changes)
- ability `bribe_margin1` — win a Buzz fight at a lead of just **≥1** (everyone else needs ≥2).
- The vendor data prints `buzz_cost = 2` as the ≥2-majority reminder for everyone; 老大's ≥1 is a
  **mat-level override**, not per-vendor data — no vendor rows change.
- **Sensitivity (bound in identity.md):** warm cinema lovable-rogue; vendors respect and *like* him (never
  intimidated), fully secular (NOT 八家將 / gang imagery). Mat text stays warm.

## 媽寶 — the floor-watch
43.5% is the field floor; its flaw is effectively dropped (Market Run keep-2 = normal). Its routing-flexibility
ability is a documented greedy-bot blind spot (a floor, not a real break). Flagged `table-watch` — carry
the win-rate + fun to the table; **do not shotgun a kit change on the number.** If it seats too weak, the
reserve is a **light non-Market Run flaw** for silhouette (e.g. cannot claim a Tour Ticket on the same turn it
Travels). Do NOT re-add a Market Run-crippling flaw (the old 29% trap).

## 大胃王 — unchanged
Ability `visit_keep3` + flaw `hazard_twice_visit` hold (54.8%). Note his Greedy Grab (§4a) starts from
keep-3, so a greedy 4th keep costs −1 Reach from a base of 3.

## Rendering note (→ bg-prototyper / bg-infodesign)
Mats are rendered as **cards** by the current pipeline (a bespoke landscape mat template is an infodesign
task). Each mat should read: name (Tâi-lô primary + 繁體), one **ability** line, one **flaw** line, both
public. 里長伯 needs the two home/away icons; `table_watch=yes` mats (里長伯, 媽寶) want a small
"playtest-watch" corner marker in the real layout.
