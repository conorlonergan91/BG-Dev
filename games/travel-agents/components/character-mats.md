# Character mats — design notes (v6.2)

Companion to `characters.csv`. The CSV carries the **locked default kits**; this note records the
**reserve dials** and one **build-scope flag** for the Director. Data is the source of truth — change
the kit in `characters.csv`, not in a rendered mat.

## What was built (this pass)
Per the bg-developer task, **four** mats were built to the locked v6.2 kits:

| Mat | Ability | Flaw (default) | Sim |
|---|---|---|---:|
| 里長伯 Lí-tiúⁿ-peh | Regular's Discount (first Bribe in each of first 2 regions −1 ingredient) | No HSR | 51.8% |
| 媽寶 Ma-pó | Mum's Packed Lunch (Travel draws the region you LEFT) | none (Visit keep-2 normal) | 45.6% |
| 大胃王 Tuā-uī-ông | Bottomless (Visit keep all 3) | hazards fire TWICE on his Visit | 52.6% |
| 網紅 Bāng-âng | Going Viral (Promote places 3 Buzz) | Late to the Party (misses first NIGHT-phase turn) | 55.0%* |

## ⚠ BUILD-SCOPE FLAG for the Director — 大哥 (the 5th locked character) was NOT built
The v6.2 LOCKED spec (`design/v6.2-content-draft.md` §Character kits) lists **five** characters. The
bg-developer task explicitly said **"Four character mats"** and named only the four above, omitting
**大哥 (Everyone Knows 大哥 — Bribe with only a ≥1 Buzz margin; no flaw; sim 51.7%, Option D)**.
I followed the explicit instruction and built four. **Decision for the human:** include 大哥 as a fifth
mat? It's in-band and locked in the spec; adding it is a one-row CSV addition. If yes, its kit is:
- ability `bribe_margin1` — *Everyone Knows 大哥* — you may Bribe with only a **≥1** Buzz margin over
  your rival (everyone else needs ≥2).
- flaw `none` — the tie-win and the +1-ingredient "tab" are both DROPPED.
- **NB the vendor data assumes the ≥2 majority for everyone** (`buzz_cost` = 2 is the printed majority
  reminder on every vendor). 大哥's ≥1 is a **mat override**, not per-vendor data — no vendor rows change.

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
