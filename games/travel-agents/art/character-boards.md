# Character Boards — illustration briefs

> **Briefs only. NO AI final art** (studio rail — `designer-profile.md`). These are direction for a
> **human illustrator**; the boards render with a labelled placeholder box until real art lands. Each brief
> names the figure code the board reserves art space for, the portrait direction (from `characters.csv`'s
> `art_note`), and the binding tone/sensitivity rails from `identity.md`.
>
> **Shared direction (all five):** warm night-market palette (lantern vermilion / jade teal / golden amber
> / dusk indigo on bao-paper cream); a **half-body character portrait** framed like a passport / boarding-pass
> photo (ties the boards to the boarding-pass identity); expressive, affectionate, **dignified — never a
> gag at Taiwan's expense** (the comedy lands on the over-the-top travel-agent *act* — the elbows-out,
> Wacky-Races food-tour race — not the people or the food). Secular only — no temple/deity/ghost-month motifs. Portraits should read as
> **local Taiwanese promoters**, warm and specific; where relevant reflect Taiwan's multi-ethnic range.
> Art fills the reserved box on each landscape board (roughly 560×320 px at the current render scale,
> upper-left); keep the face/expression in the top 2/3 so it survives the passport-frame crop.

---

## [FIG-CHAR-old-councillor] — Lí-tiúⁿ-peh · The Old Councillor · 里長伯
- **Portrait:** a cheerful apron-clad neighbourhood councillor (里長) waving you over — dignified, warm,
  sharp-eyed; the pillar of his own borough. **Not** a gag figure.
- **Read at a glance:** *home-turf clout* — he belongs to one street and everyone there knows him.
- **Sensitivity (BINDING, standing 里長伯 line):** his favours are **neighbourly standing bounded to the
  one borough a real 里長 serves** — reads as local respect, never graft/corruption. Keep him
  courteous, well-liked, secular.

## [FIG-CHAR-homebody] — Ma-pó · The Homebody · 媽寶
- **Portrait:** an earnest young office worker clutching a mum-packed lunchbox, phone to ear (calling
  home). Sweet, a little sheepish, entirely likeable.
- **Read at a glance:** *ties to home* — he does best sourcing where he just came from.
- **Sensitivity:** affectionate, never mocking. 媽寶 is played as warm and endearing (a good son who
  loves home cooking), not as an insult. *(English name `The Homebody` is a proposal — see flag.)*

## [FIG-CHAR-big-eater] — Tuā-uī-ông · The Big Eater · 大胃王
- **Portrait:** a grinning competitive eater mid-bite, the table piled with empty bowls — all appetite,
  no brakes, delighted.
- **Read at a glance:** *bottomless haul* (keeps all 3 on a Market Run) balanced by *greed bites back*
  (hazards fire twice on his Market Run).
- **Sensitivity:** joyful gluttony, celebratory of the food; the joke is his appetite, never the cuisine.

## [FIG-CHAR-influencer] — Bāng-âng · The Influencer · 網紅
- **Portrait:** a stylish food blogger framing a bowl for the perfect shot, grinning — genuinely, happily
  obsessed with the island's food.
- **Read at a glance:** *hype engine* (Promote places 3 Buzz) who *goes last* in turn order.
- **Sensitivity:** an affectionate, self-aware wink at influencer culture — she really loves the food;
  never cynical or at Taiwan's expense.

## [FIG-CHAR-big-boss] — Lāu-tuā · The Big Boss · 老大
- **Portrait:** a beaming older man in a bomber jacket greeting a delighted stall-owner like an old
  friend — **warm cinema charm, never a threat.**
- **Read at a glance:** *everybody knows him* — he wins a Buzz fight at just a 1-lead; no drawback.
- **Sensitivity (LOAD-BEARING — `identity.md` 老大 binding; consultant-gated):** a warm, lovable fixer vendors
  **respect and like** (never intimidated); secular; the neighbourhood big boss, **not** a gangster/triad
  caricature. 老大 carries a boss/gang-leader connotation, so the paid consultant must sign off on the name +
  depiction before final art. If a rendering ever reads as menace, it is off-rail — dial back to the grin.

---

## Data / naming flags (for the CD + `bg-theme`)
- **English names are BLESSED & CANONICAL** (in `characters.csv` as `name_en`; CD "adopt as proposed"
  2026-08-08, dignity-passed by `bg-theme`): The Old Councillor · The Homebody · The Big Eater ·
  The Influencer · The Big Boss. `The Homebody` (the warmer, de-fanged read of literal 媽寶 "mama's
  boy") and `The Big Boss` (the warm, affectionate 老大, NOT a gangster/triad caricature; consultant-gated) both PASS the dignity
  bar **only while their warm portrayals stay load-bearing on every surface** — carry the blurb/art-note
  warmth (never a mocking or menacing read). These two + the 里長→"Councillor" gloss are the character-name
  watch-items for the paid Taiwanese consultant (still required before art/print).
- **`blurb` column** on `characters.csv` is the cleaned warm prose shown on each board (pulled from the
  `effect` flavour column with the `[re-sim …]` sim-metadata + the mechanical restatement STRIPPED).
- **Pile labels FINALISED (CD 2026-08-08): COMPLETED `成團` (win) / CANCELLED `取消` (lose)** — this is now
  the sole canonical pair everywhere. The old English "SOLD" label and the retired 繁體 `遺珠` "the Ones
  That Got Away" are GONE; the board now renders **COMPLETED 成團 / CANCELLED 取消**. (繁體 成團 · 取消 →
  native reviewer to bless.)

---

## AI mock-up prompts (playtest props — NOT final art)

> **Playtest props only** — permitted so testers feel each promoter's warmth during manual playtesting.
> **Final art stays human-illustrated; NO AI final art.** Each PNG is a **MOCKUP** → save to the
> **gitignored** `games/travel-agents/build/mockups/`, filename = the FIG code (e.g.
> `FIG-CHAR-big-boss.png`); **never committed, never moved to `exports/`, never shipped.**
>
> **The portrait prompts live in [`art/character-art.md`](character-art.md) — do NOT duplicate them here.**
> The six board portraits reserve the **same `FIG-CHAR-<slug>` slots**; generate them from the
> character-art.md prompts. This section only adds the **board-integration** notes so a mock-up drops onto
> the board's reserved passport frame at the right scale.

- **Scale (canonical — supersedes this file's older "~560×320 px" estimate):** the portrait slot is
  **604 × 286 px, ~2.11:1 wide letterbox** — a WIDE band sitting top-left (44,176) on the 1680×1380
  landscape board. Generate at **2×** and export at that exact aspect so it drops into the slot without a
  reflow. Keep the **face/expression in the upper-centre** so it survives the passport-frame crop.
- **Background:** **transparent** — the board's passport / boarding-pass frame, name plate, and the
  **COMPLETED 成團 / CANCELLED 取消** pile labels, Reach 及 / Tours-Completed 好評 tracks and 成團/取消 piles
  are all **rendered by code**, not by the mock-up. The mock-up supplies the cut-out character only; it
  must not paint any board chrome, labels, or track furniture.
- **Rails carry over unchanged:** the Big Boss's warmth (load-bearing — vendors *like* him, never
  intimidated) and the Old Councillor's neighbourly-not-graft standing are the same dignity watch-items as
  in the portrait briefs; secular throughout. English names on any label the mock-up hints at.
