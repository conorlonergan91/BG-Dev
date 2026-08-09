# V7+ — Generic Ingredient Categories (CD direction, 2026-08-09)

**The move (CD):** replace the 5 *specific* ingredients (pork · tea · seafood · rice · sugar) with a small
set of **generic categories** — e.g. **Meat · Vegetables · Fish · Tea · Sugar · Pantry** (final set TBD) —
whose **card illustration shows a MIX** (the "Meat" card depicts chicken, pork belly, beef, etc.). Reference:
a game the CD named that uses generic ingredient categories (confirm which — noted as "Yes Ginseng?"; the
mechanic, not the title, is the point).

**Why:** trading ingredient *specificity* for dish *breadth* opens the deck to **far more Taiwan dishes**
(deepening the culture-sharing theme), and it **elegantly solves the Chiayi turkey-rice problem** — turkey
rice becomes a **Meat** dish, no bespoke poultry ingredient needed (this supersedes the S04 A/B/C call:
turkey rice is now essentially free, so a Chiayi 火雞肉飯 vendor can exist without reopening the ingredient
system for it specifically).

## Design requirements (for the bg-design taxonomy pass — do AFTER the current bg-infodesign render lands)
1. **Define the generic set** (~6 categories). Candidate: Meat / Vegetables / Fish / Tea / Sugar / Pantry
   (Pantry = rice/noodles/flour/dry-goods staples). Confirm count + names with the CD if it drifts from this.
2. **PRESERVE the validated economy skeleton.** The current design's balance rests on a
   **regional-signature + common** structure (pork=North · tea=Central · seafood=South · rice=East ·
   sugar=common C&S) that makes **travel + cross-region dishes** matter, plus the CD-4 soft night-cost curve.
   The generic set MUST keep that skeleton — each region a signature category, one or two commons — so
   sourcing/travel/night-cost still behave. Map old→new (e.g. pork→Meat[N] · tea→Tea[C] · seafood→Fish[S] ·
   rice→Pantry[E] · sugar→Sugar[common] · + Vegetables as the new common/second axis) — bg-design fixes the
   exact mapping to hold the economy.
3. **Re-express the vendor recipes** (`vendors.csv`) in the generic categories, **preserving each dish's
   difficulty** (ingredient count + cross-region shape) so the tickets/sourcing balance is unchanged in
   structure; then diversify dishes for variety WITHIN that difficulty envelope.
4. **Ingredient cards** = one per generic category, illustration a **mix** of real Taiwan examples
   (art-brief per category, citing `art/art-style.md`; distinguishable by picture + shape, not colour — loop
   bg-access). Update `recipe-glyphs.csv` to the generic set.
5. **Balance assessment → likely a GATED re-sim.** Changing the ingredient taxonomy + diversifying dishes
   touches the economy the sim validates. bg-design assesses the magnitude: a near-structural mirror = small
   delta (maybe a light confirm); genuine dish diversification = **flag a CD-gated re-sim** before locking.
6. **Unlocks (list for the CD):** turkey rice (Chiayi, Meat), plus broad new dishes across meat/veg/fish/
   pantry — a much wider tour of Taiwan's food. Enumerate example new vendor dishes when re-expressing.

## Sequencing
The current bg-infodesign structural pass renders the **5-specific** ingredient cards + recipe-chips as
**interim** — superseded by this taxonomy redesign. Order: (a) bg-infodesign structural pass lands → (b)
bg-design taxonomy + recipe remap (+ balance assess) → (c) CD-gated re-sim if flagged → (d) re-render the
generic ingredient cards + vendor recipe-chips + art-briefs.
