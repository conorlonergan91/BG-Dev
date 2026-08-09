# AI mock-up workflow — high-fidelity playtest art (proven loop)

How the studio turns art briefs into **warm, cohesive AI mock-ups** for **manual playtesting**, and drops
them straight into the rendered components. Proven on *Travel Agents: Taiwan* (the six character boards).

> **Binding rail (unchanged):** these are **MOCK-UPS / playtest props only**. Final art is
> **human-illustrated**; where a real culture is involved, a **paid cultural + language consultant**
> reviews before final/print. Mock-ups are labelled, never shipped as final, and **never copied into
> `exports/`**. See `art/art-style.md` and each game's `art/mockups/README.md`.

## The loop
1. **One look, cited everywhere.** Every brief opens by citing the game's `art/art-style.md` (the single
   style + palette + sensitivity anchor). Keeps the whole set cohesive.
2. **Upload context ONCE.** Zip the art `.md` files (`art-style.md` + the per-asset briefs + real-place /
   taxonomy grounding) and upload them to the image tool (ChatGPT/etc.) as knowledge — so per-item prompts
   can stay short.
3. **Thin per-asset "kickoff" prompts.** One block per asset: name the asset + its brief + only the
   make-or-break constraints (below). Paste one at a time. (See `art/mockup-kickoffs.md`.)
4. **Attach a STYLE REFERENCE image** (the biggest consistency win). Alongside the prompt, attach a liked
   earlier character and say *"match this art style."* Build the whole cast outward from your favourite.
5. **Prep** the raster export → drop-in slot asset with `tools/mockup/prep_mockup.py` (split grids,
   corner-seeded flood **key-to-transparent** that preserves interior whites, **fit to the slot** px).
6. **Persist + embed.** Commit CD-approved finals to `games/<slug>/art/mockups/` (labelled MOCKUP);
   `make.sh` preps them into gitignored `build/mockups/`; the board/card renderers **auto-embed**
   `build/mockups/<FIG-CODE>.png` (base64 data-URI) into the art slot, falling back to the placeholder when
   absent. **Committed `exports/` stay placeholder** (no AI final art); warm renders go to `build/` for
   playtest + print, delivered to the human via the chat (`SendUserFile`) — handy when they can't pull
   files from the GitHub app.

## What actually made the art good (craft notes)
- **Pose DRAMATIZES the character's game ABILITY** — not a generic "running" pose. This was the single
  biggest fix from "boring" to "perfect": the home-turf character rallies his borough from a soapbox, the
  sole-sourcer staggers under a tower of mum's supplies, the tie-winner swaggers in with the goods, etc.
- **Energy to match the game's verbs.** A race-and-battle game wants competitive, slightly **chaotic**,
  high-motion poses (mid-scramble, snatching the prize, speed lines) — warm, never mean.
- **Style: point at the game's established look; avoid over-caricature.** "Bold exaggerated big-head
  caricature" over-corrected and was rejected; the **polished original cartoon** (clean linework, bold flat
  colour, expressive face) was what the CD wanted. Dial energy via *pose*, not via changing the render style.
- **Generate for a clean cut-out:** ONE subject per image (no grids/sheets); **flat or transparent
  background, NO baked vignette/glow** (a gradient can't be keyed cleanly); subject fully in frame.
- **Local specificity reads.** Real, recognisable local props beat generic ones (e.g. the actual EasyCard,
  not a generic transit card).
- AI tools return **raster PNG, not SVG**, and won't batch a cast — that's expected and fine.

## Tools
- `tools/mockup/prep_mockup.py` — grid-split · corner-flood key-to-transparent · fit-to-slot.
- `tools/boards/build_board.py`, `tools/cards/build_cards.py` — auto-embed `build/mockups/<FIG>.png`.
- The SCALE TABLE in `art/art-style.md` gives each slot's exact px.

Owned by **bg-theme** (the look + briefs) with **bg-infodesign / bg-prototyper** (scale, prep, embed).
