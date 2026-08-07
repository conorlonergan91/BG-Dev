# Character mats — design notes (v6.2)

Companion to `characters.csv`. The CSV carries the **locked default kits**; this note records the
**reserve dials** and one **build-scope flag** for the Director. Data is the source of truth — change
the kit in `characters.csv`, not in a rendered mat.

## What was built — the FIVE locked v6.2 mats
All **five** mats from the locked v6.2 spec (`design/v6.2-content-draft.md` §Character kits) are built.
(大哥 was added after the CD corrected the brief — the original bg-developer task said "four" in error.)

| Mat | Ability | Flaw (default) | Sim |
|---|---|---|---:|
| 里長伯 Lí-tiúⁿ-peh | Regular's Discount (first Bribe in each of first 2 regions −1 ingredient) | No HSR | 51.8% |
| 媽寶 Ma-pó | Mum's Packed Lunch (Travel draws the region you LEFT) | none (Visit keep-2 normal) | 45.6% |
| 大胃王 Tuā-uī-ông | Bottomless (Visit keep all 3) | hazards fire TWICE on his Visit | 52.6% |
| 網紅 Bāng-âng | Going Viral (Promote places 3 Buzz) | Late to the Party (misses first NIGHT-phase turn) | 55.0%* |
| 大哥 Tuā-ko | Everybody Knows 大哥 (win a Buzz fight at a ≥1 lead, not the usual ≥2) | **none** (Option D) | 51.7% |

## 大哥 — the Buzz-margin override (no vendor data changes)
- ability `bribe_margin1` — *Everybody Knows 大哥* — you win a Buzz fight at a lead of just **≥1** over
  your rival (everyone else needs the ≥2 majority).
- flaw `none` — the tie-win and the +1-ingredient "tab" are both DROPPED; the slim ≥1 edge alone tested
  balanced at 51.7% (Option D).
- **NB the vendor data prints the ≥2 majority for everyone** (`buzz_cost` = 2 is the printed majority
  reminder on every vendor). 大哥's ≥1 is a **mat-level override**, not per-vendor data — no vendor rows
  change.
- **Sensitivity (bound in identity.md):** warm cinema lovable-rogue; vendors respect and *like* him
  (never intimidated), fully secular (NOT 八家將 / gang imagery). Mat text stays warm.

## 網紅 — the KEY table balance-check + the lost-turn DIAL (carry in reserve)
Built to the **default dial** (`late_to_night`). The sim seated 網紅 at 55.0% modelling the flaw only as
"goes last"; the sim flagged that a go-last disadvantage is *under-counted* in sim, so the concrete
lost-turn flaw the CD locked here may **over-correct below 45%**. This is **not sim-equivalent** and is a
KEY balance-check in the Screentop plan. If it tests too weak/strong, swap `flaw_code` in
`characters.csv` to one of:
- **Default / locked:** `late_to_night` — misses its first turn of the **night** phase (one lost turn).
- **Heavier** (`late_both_phases`): misses its first turn of **BOTH** phases (day + night — two lost turns).
- **Alt** (`forfeit_final_move`): forfeits its **final move** at the last-train trigger ("still posing
  while everyone catches the train").
- **Lighter / revert** (`goes_last_only`): drop the lost turn — keep just goes-last + the ability (the
  sim's 55.0% config) and instead **trim the ability** (e.g. +1 Buzz on your **first** Promote only, or a
  small bribe tab). Pick the dial from the session result.

## 媽寶 — near the floor
45.6% is just above the 45% band edge and its flaw is effectively dropped (Visit keep-2 = normal). Flagged
`table-watch`. If it seats too weak, the reserve is a **light non-Visit flaw** for silhouette (a
table/design call, not sim-load-bearing) — e.g. cannot claim a Tour Ticket on the same turn it Travels.
Do not re-add a Visit-crippling flaw (that was the 29.4% trap that was fixed).

## Rendering note (→ bg-prototyper / bg-infodesign)
Mats are rendered as **cards** by the current pipeline (a bespoke landscape mat template is an
infodesign task). Each mat should read: name (Tâi-lô primary + 繁體), one **ability** line, one **flaw**
line, both public. `table_watch=yes` mats want a small "playtest-watch" corner marker in the real layout.
