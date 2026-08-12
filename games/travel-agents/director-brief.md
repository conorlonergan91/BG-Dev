# 🎬 Travel Agents: Taiwan — Director's Brief (the CD's steers, per version)

> **The Creative Director's own input, preserved.** A log of the substantive messages/steers the CD sent —
> captured verbatim-ish with the context around them — so a good idea sent mid-thread never gets lost.
> Distinct from `decision-log.md`: that records *decisions we reached + rationale*; THIS records *what the
> CD actually asked for and why*, in the CD's voice. Real-time capture is the orchestrator's reflex (the
> CD's messages reach main Claude); `bg-producer` curates, organises by version, and flags anything
> captured-but-not-yet-actioned.
>
> **Entry format:** each steer gets — **the ask** (what the CD wanted, close to their words) · **context**
> (the why / the situation around it) · **status** (`captured` → `implemented` / `parked` / `superseded`)
> with a pointer to where it landed (commit / doc / decision-log entry).

---

## V7-M — current version

<!-- Newest at top. Append each substantive CD steer as it arrives. -->

- **2026-08-11 — Drop the apex glyph; CD will AI-generate the icons in a cartoonish emoji style.**
  - **Ask:** *"We can probably get rid of the old point glyph on the top right of vendor cards as well (or if that's only for apex then there's no need for a glyph — it should just be reflected in the cost and points value). I'm going to use AI art to generate the icons for points, ingredients and followers, so update the zip and the prompts etc. I don't want these icons hyper-realistic like the food pictures — more like emojis, cartoonish style."*
  - **Context:** After the round-2 vendor polish. The top-right mark was the apex ★ — CD wants it gone (apex reads from the higher points + cost, no dedicated glyph). And the CD will generate the 8 functional icons (6 ingredients + followers + points/ticket) themselves via AI, in an **emoji / cartoonish** style — explicitly NOT the realistic look of the food-dish illustrations.
  - **Status:** `captured` → apex ★ removed from the vendor card (`build_cards.py`). Icon-generation prompts + refreshed `ta-art-context.zip` → `bg-ai-prompt` (emoji-style anchor, shapes/colours matched to the SVG placeholders so the AI outputs drop in as `FIG-ICON-<type>.png`). Wiring the generated PNGs into the renderer is a later step once the CD delivers the art; the SVG icons stand in until then.

- **2026-08-11 — Vendor card polish round 2: kill the cross-region badge, one cost row, booking-style ticket reward, illustrated icons.**
  - **Ask:** *"No need for cross region badge — get rid of it. Also all the 'cost' should be on the same row (ingredients + followers), and then for the rewards the points should look the same as how they're displayed on the bookings. The glyph for points should be a ticket rather than a star thing. We should have illustrated icons instead of glyphs for ingredients and followers."*
  - **Context:** Reaction to the round-1 vendor redesign. CD wants the card to read as **COST (ingredients + followers together) → REWARD (points)**, with the reward matching the Bookings' `+N value` pill and a **ticket** glyph replacing the gold star, and the abstract geometric type/follower glyphs upgraded to **illustrated** (little drawn) icons.
  - **Status:** `captured` → in flight to `bg-art-director` (illustrated icon set + card visual simplification; Beacon byte-identical; dual-coding/CVD floor preserved). Cross-region badge → removed (this also closes the earlier A/B/C badge-accuracy question: answer = C, drop it).

- **2026-08-11 — Beef Noodle is the apex; vendor cards are too busy; any-tours share the day/night back.**
  - **Ask (three steers, one message):** *(1)* *"Can we change beef noodle to be the apex dish instead of
    the sausage."* *(2)* *"I also think the vendor cards are very busy and have way too much going on — we
    could trim down everything unnecessary and leave space for the images (attached a few for reference)."*
    *(3)* *"The 'any' tours shouldn't have a different back as they'll be mixed in with the respective
    DAY / Night tour decks."*
  - **Context:** CD shared 5 finished food illustrations (beef noodle, gua bao, bubble tea, egg crepe,
    pepper bun) — clean hero-food-on-cream, the target look for a trimmed vendor card with room for art.
    Beef noodle (牛肉麵) is Taiwan's national dish → it, not a Big Sausage, should be the marquee ★ apex.
    Any-time tours physically shuffle into the day/night tour decks, so a distinct any-back would make them
    sortable — they need to share the tour back.
  - **Status:** `captured` → in flight. (1) → `bg-design` (vendors.csv, invariant-preserving swap). (2) →
    `bg-infodesign` (vendor front redesign + embed the 5 images). (3) → unify the tour back (one
    boarding-pass back for day/night/any bookings; market cards keep their morning/night-market backs).

- **2026-08-11 — Seriously strip down the player aids into a per-player, card-sized, double-sided aid.**
  - **Ask:** *"Seriously strip down the player aids… fit in a card the same size as the others… one for each
    player, on one side it lists the actions (save explanation for the rulebook), on the other side a very
    brief explanation of the ability and flaw of the character."*
  - **Context:** The old player aid was a single verbose sheet. The CD wanted the aid to become a real
    component in the box — the same card size as everything else, one per player, with the turn actions on a
    shared front and each agent's character-specific ability + flaw on the back, keeping the *teaching* in the
    rulebook rather than crammed onto the aid.
  - **Status:** `implemented` → the old verbose single sheet is **retired** and replaced by a **poker-card-
    sized (750×1050), per-player, double-sided** aid: a shared FRONT listing the six turn actions (labels +
    one-line reminder, full teach left to the rulebook) and one BACK per character with that agent's ability +
    flaw in brief, tinted in the character's colour (漢字 + Tâi-lô + catchphrase). New `--type aidcard`
    renderer in `tools/boards/build_board.py`; new schema `components/player-aid.json` pulling display fields
    from `characters.csv` so it can't drift; `make.sh` renders into `build/aid/` → `exports/aid/` +
    `exports/screentop/` + a true-size cut-out PnP `exports/print/pnp-player-aids.pdf`; `check_complexity.py`
    taught the new schema (player_aid_lines 8/22). Guardians green. Commit `111c916`. (status.md Done bullet)

- **2026-08-10 — SCRAP the secret-agent premise; pivot to "Wacky Races, Taiwan-food edition"; retitle.**
  - **Ask:** The secret-agent / spy backstory was scrapped a while back — kill it everywhere. The direction
    is **over-the-top, wacky-racer, *battle-hungry* rival travel agents** in a zany all-out dash to **craft
    the best tours and sell the most tickets.** Retitle to **"Travel Agents: Taiwan Food Tour."**
  - **Context:** The living docs (identity.md AND game-bible.md) still carried the covert-agent wordplay
    (trench-coat-over-Hawaiian-shirt, dossier, earpiece, "Operation: ___", mission-dossier voice) as the
    north star; the CD caught it mid-way through a doc-currency sweep and halted it to fix the *premise*.
    **Take-that BETWEEN agents is now welcome** (elbows-out competition; the old "warm rivalry, never
    take-that" rail relaxes agent-vs-agent). **Taiwan, the food, and the vendors stay beloved and every
    sensitivity rail holds.** This is a THEME / felt-identity pivot only — all V7-M mechanics are unchanged.
  - **Status:** `captured` → re-founding `identity.md` (bg-theme) + `prose-identity.md` voice (bg-copywriter);
    game-bible theme-framing + title corrected; retitle propagating. (this entry; decision-log 2026-08-10 pivot)

- **2026-08-10 — Close off V7 (commit, PR, merge).**
  - **Ask:** Make sure everything's committed, then open a PR and merge V7.
  - **Context:** Wrapping V7-M at a clean, sim-validated state before moving to the human-playtest phase.
  - **Status:** `implemented` → **PR #13 merged to `main`** (2026-08-10); `game-bible.md` header records the merge.

- **2026-08-10 — Stand up a project-management DEPARTMENT + a per-version log of the CD's own messages.**
  - **Ask:** Add agents that keep everything on track, up to date, simplified, and current-version — *plus a
    per-version log of the CD's own messages + context, because good messages were getting lost.*
  - **Context:** The living docs were accreting history and good mid-thread steers were slipping through.
  - **Status:** `implemented` → the Production pod: **`bg-producer` + `bg-archivist`**, the current-state doc
    model, and **`status.md` + `director-brief.md`** (this file). Landed in commit `9bc3430`; docs pruned to
    current-state in `f15cce1`. *(This very brief is the "good messages don't get lost" mechanism working.)*

- **2026-08-10 — Game-world intro at the rulebook front.**
  - **Ask:** Open the rulebook with a game-world introduction.
  - **Context:** Set the warm caper tone before teaching rules.
  - **Status:** `implemented` → the **"Operation: Beef Noodle"** world intro (rulebook `--rich` layout;
    decision-log 2026-08-10 stylish-rulebook entry, commit `e7099aa`).

- **2026-08-10 — Big Brother → Big Boss (老大 / Lāu-tuā), and make the rail a *playful* boss.**
  - **Ask:** Rename The Big Brother → **The Big Boss** in both languages (漢字 大哥 → **老大**); the CD is
    comfortable with the affectionate boss / gang-boss read — rewrite the sensitivity rail as a *warm,
    playful fixer*, not menacing.
  - **Context:** "The Big Boss" fits the roster's "The X" register; the CD explicitly signed off on the read.
  - **Status:** `implemented` → id C5 + all mechanics unchanged (margin dial N=1, wins ties); name + rail
    swept LIVE across every doc/render, board portrait re-embedded (`board-big-boss.png`), rail rewritten to
    "playful, affectionate boss … never a triad/gang caricature," **consultant-gated**. Decision-log
    2026-08-10 "CD RENAME" entry. *(Watch-item: still one of the two consultant-gated items — see status.md.)*

- **2026-08-10 — `prose-identity.md` as a canonical VOICE bible.**
  - **Ask:** Author a canonical voice bible alongside the felt-identity and art-identity files.
  - **Context:** So every player-facing word reads as one narrator; distilled from the CD's gold-standard
    ChatGPT backstories/mat quotes ("much better").
  - **Status:** `implemented` → `prose-identity.md` authored (decision-log 2026-08-10 voice-bible entry) **and
    promoted to a studio-wide standard** (template + CLAUDE.md convention + copy-agent wiring, commit `e715a25`).

- **2026-08-10 — Use ChatGPT's prose; make the rulebook stylish with art + layout.**
  - **Ask:** Use ChatGPT's backstories (rulebook) + mat quotes (boards); add character pictures to the
    rulebook; make the rulebook stylish with art + layout.
  - **Context:** The CD supplied prose they preferred and wanted it dressed properly.
  - **Status:** `implemented` → mat quotes on boards (`085d374`); "Meet the Agents" backstory gallery + FIG
    portraits + `--rich` layout in the rulebook (`e7099aa`); complexity gauge taught to exclude flavour so
    the added prose didn't false-flag the budget.

- **2026-08-10 — Art / presentation direction (incl. lifting the no-AI-art rail for the prototype).**
  - **Ask:** Put the character images on the boards + Screentop; kill the white space (portrait too tall —
    shrink to lane height); make the prose funnier and hint each character's strategy; colour-match each
    board to that player's meeples; and *"forget the no-AI-art rule — I need AI art for the prototyping."*
  - **Context:** Getting a presentable, portrait-bearing prototype kit onto the table fast.
  - **Status:** `implemented` → boards carry embedded mock-up portraits (`exports/board-*.png`),
    colour-matched, portrait sized to lane; character blurbs rewritten funnier with strategy winks
    (decision-log copy-pass entry). **No-AI-art rail LIFTED for the prototype only** — final art stays
    human-illustrated; the content-sensitivity rails still apply.

- **2026-08-10 — Confirmations (cap-raise, gauge scope, Tâi-lô form).**
  - **Ask:** Accept the rulebook cap-raise **1900 → 2280**; accept the complexity gauge being scoped past
    parked/flavour content; accept Tâi-lô **"Lāu-tuā"** for 老大 (option A).
  - **Context:** Honest pricing of the consciously meatier V7-M after bg-elegance's fat cut; roster-consistent
    romanisation.
  - **Status:** `implemented` → cap confirmed in `complexity-budget.json` (gauge now 0-over; rules-only
    2262/2280); gauge scoped past parked `*-split.csv` + flavour sections; "Lāu-tuā" recorded canonical
    (Mandarin-pinyin "Lao Ta" kept as a consultant-check variant in `names.md`).

- **2026-08-10 — Ship config = 1A: ship MONO 6-type; PARK the 8-type split.**
  - **Ask:** Ship the clean **mono 6-type** taxonomy; park the 8-type split as a flag-gated experimental branch.
  - **Context:** The split reintroduced a seed-robust 5–6p hoarder tilt for a one-region (East) payoff — and
    that tilt lived in keep-2, the *only* mode the split earns its payoff in.
  - **Status:** `implemented` → mono ships; split preserved non-destructively behind `SPLIT_TAXONOMY`
    (default OFF; `*-split.csv` stay in the tree). Decision-log 2026-08-10 "SHIP-CONFIG LOCKED (1A)" entry.

- **2026-08-10 — Orphan showcase tours = 2A: re-tune, don't delete the anchor.**
  - **Ask:** Re-tune Best Bubble Tea + Dihua Crawl to be demanding-but-doable (accept option A — keep the
    scarce theme anchor).
  - **Context:** Both were ~72–83% orphan — a two-of-a-scarce-kind assembly wall, not slot availability.
  - **Status:** `implemented` → each relaxed to `1 scarce anchor + 1 common second leg` (disjoint sets, no
    degenerate 1-card completes); re-smoked to ~24–27% pattern-achieved, ~56–62% orphan = parity with the
    healthy pair tours. Decision-log 2026-08-10 "CD decision 2A DONE" entry. *(Theme-honest ~57–62% orphan
    accepted; a premium crawl should be a ~40% gamble — status.md Showcase-tours watch.)*

- **2026-08-09/10 — Vendors are the CLOCK + a 3-round track + a custom Closing-Time die.**
  - **Ask:** Let vendors run out to force fights; add a 3-round track + a custom d6 (4 region faces + 2
    blanks); roll after round 3; a region face closes the oldest unclaimed face-up stall; no resource loss —
    committed followers come home.
  - **Context:** A forcing function so the depletion clock reliably lands contests.
  - **Status:** `implemented` → the **Closing-Time die 關門** (die L2@3–5p / L3@6p; blank = 1/3 reprieve;
    followers home, no penalty). In `game-bible.md` mechanism spine + `components/tokens.csv`.

- **2026-08-09/10 — Accept the ~40–48 turns/player band; fix 3p with a helper.**
  - **Ask:** Accept a meatier game (~40–48 turns/player); fix 3p with fewer-vendor tours + a general "wild
    booking" gamble when nothing face-up suits.
  - **Context:** Keep 3p viable without shrinking the game elsewhere.
  - **Status:** `implemented` → the `counts` on-ramp tag + **Pot-Luck / wild booking (隨緣開團)**; die L2@3p.

- **2026-08-09/10 — Scale stalls + vendor deck per player count, thematically.**
  - **Ask:** A Tainan/South slot @5p, a Taipei/North slot @6p, East thinnest; count-tag tours so subsetting
    never makes a tour unbookable.
  - **Context:** Thematic, count-aware scaling.
  - **Status:** `implemented` **with a correction** — thematic `vendor_slots` scaling landed, but the vendor
    **POOL stays full at all counts** (shrinking it backfired: `per_count_subset:false`). Count-tag tours
    added (HEAVY / ON-RAMP / CORE). Decision-log 2026-08-10 "FORMALIZED §14+§20+§21" entry.

- **2026-08-09/10 — Full points on vendors (Route B); tours score higher.**
  - **Ask:** Full points on vendors (Route B), but tours are the dominant win path; an easy tour can score
    below a premium vendor; more effort → more reward; 1–2 cheap low-VP day stalls OK.
  - **Context:** A steady-bonus second track that never overtakes the tour path.
  - **Status:** `implemented` → **two-track VP** (§14 invariant `vp = ingredient_cost + min_followers − 2`,
    range 1–6; bookings widened so the tour ceiling clears the vendor ceiling; winner vendor-VP share
    ~28–35%). `game-bible.md` §14 + `components/vendors.csv`. *(⚠ stale prose in `rules-draft.md` §1/§9 +
    `names.md` §3 still reads tickets-only — routed to bg-continuity/bg-rulebook/bg-design; see status.md.)*

- **2026-08-09/10 — Difficult vendors must be worth it.**
  - **Ask:** Make hard vendors worth it — via missions that include them OR reintroduced vendor points; the
    earlier flat/easy vendors were the problem, not vendor-points per se.
  - **Context:** Diagnosis that the old flat vendors, not the concept of vendor VP, were the issue.
  - **Status:** `implemented` → difficulty-scaled vendor VP (folds into the two-track VP above).

- **2026-08-09/10 — Vendors require MULTIPLE ingredients.**
  - **Ask:** Every vendor needs multiple ingredients, to force cross-region spread.
  - **Context:** Make ingredient sourcing a real cross-region engine.
  - **Status:** `implemented` → multi-ingredient, mostly cross-region recipes (`game-bible.md` mechanism spine).

- **2026-08-09/10 — Rich, creative, mechanic-spanning EVENTS.**
  - **Ask:** Events across every mechanic — follower gain/loss (going viral / bad reviews / cancelled),
    ingredients stolen or bottom-decked / spoiled (heat wave), travel restricted (scheduled maintenance /
    "boss wants to talk"), actions restricted (no draw in a typhoon; no follower-gain on travel = no
    internet); scope self / same-or-surrounding / whole board; some persist; the more and the more creative
    the better; tune the events-vs-ingredients draw ratio per player count.
  - **Context:** Wanted events to feel rich and thematic, not filler.
  - **Status:** `implemented` → the **VERB · SCOPE · DURATION** event framework (~52 events; `events.csv` +
    `design-doc.md` §15), per-count deck mix, island-wide Scheduled Maintenance beat. Also captured in
    `content-ideas.md`.

- **2026-08-09/10 — Per-region face-up discard piles + reshuffle.**
  - **Ask:** Spent ingredients / fired events / forced discards → a region discard; reshuffle when a deck
    empties; previous-phase cards → box.
  - **Context:** Keep the region decks self-contained and cycling.
  - **Status:** `implemented` → ingredient + event decks reshuffle per region+phase (`game-bible.md`).

- **2026-08-09/10 — Anti-kingmaking rules.**
  - **Ask:** If multiple tied kings, all affected (excluding the drawer); don't be *too* punishing (a
    hard-earned lead shouldn't be demotivated); cancelled-tour BOONS — CLEAR (shed your own) + SALVAGE (take
    the lowest scorer's, complete at half value).
  - **Context:** Manage swing/kingmaking without deflating a legitimate leader.
  - **Status:** `implemented` → rival-facing ✦ events auto-target the leader at magnitude 1 (a small
    minority); Rave Reviews milestone boons; cancel = flat −1.

- **2026-08-09/10 — Big Boss tie-win → tunable MARGIN dial; Big Eater greed = day-only.**
  - **Ask:** Big Boss (then "Big Brother") wins a contested stall unless beaten by >N followers, N∈{0,1,2},
    with a night-scope option; make Big Eater's greed day-only as a cooling knob.
  - **Context:** Levers so the playtester can tune the heat.
  - **Status:** `implemented` → margin dial (N=1 → wins ties); night-scope kept as a labelled option.
    *(The character later renamed Big Brother → Big Boss — see the rename entry above.)*

- **2026-08-09/10 — Six asymmetric character lanes.**
  - **Ask:** Influencer build-high (deep pool max 8), Old Councillor resource-rush REWORK, Homebody mobile
    forager who dodges fights, Big Eater greedy glut, Big Boss margin battler, Globetrotter ubiquity.
  - **Context:** A diverse, no-crusher roster.
  - **Status:** `implemented` → the six V7-M kits (`components/characters.csv` is canon). *(The Old Councillor
    landed as a home-gated ingredient DRAW; balance reopened → carried to re-sim / table. ⚠ `names.md` §1 +
    `v7-plan.md` still describe pre-V7-M kit shapes — routed to bg-continuity; see status.md.)*

- **2026-08-09/10 — Make the battle real: vendor scarcity.**
  - **Ask:** Contests were firing only ~5% under the old dial — add a map/setup scarcity knob so fights
    actually happen.
  - **Context:** The central fight wasn't triggering.
  - **Status:** `implemented` → deliberately fewer stalls than agents; contested_frac now ~24–27% at
    multiplayer.

- **2026-08-09/10 — Follower MEEPLES replace the abstract dial.**
  - **Ask:** Each player owns N coloured meeples up to a max; collect from a table supply onto the board;
    place your own colour on vendors to contest; spreading allowed. WIN → meeples come home to your board;
    LOSE → back to your OWN supply (re-collect). Balance levers = per-character max, collection pace,
    tie-break.
  - **Context:** The abstract dial "didn't feel natural" — the CD wanted a physical, legible contest.
  - **Status:** `implemented` → follower meeples are the V7-M core contested currency (pool 6; Influencer 8;
    Followers-max dial). `game-bible.md` mechanism spine + `design/followers-meeples-redesign.md`.

- **2026-08-09/10 — Draw-3-keep-2 is useless in mono regions → test the fix.**
  - **Ask:** Draw-3-keep-2 is pointless with mono regions — test straight-draw OR more ingredients; "more
    ingredients" means SPLIT the 4 into finer types, not spread the existing 4; test both in playtest.
  - **Context:** The keep-2 choice had no teeth once regions went mono.
  - **Status:** `superseded` → this seeded the taxonomy arc; resolved by the **ship-config 1A** decision
    (mono ships, 8-type split parked) — see the 1A entry above.

- **2026-08-09/10 — Taxonomy decision: "Go with B" → "B-full" → "B-hybrid is better, go with that."**
  - **Ask:** After iterating, land on the 8-type split (Rice/Noodles + Sugar/Pearls; drop Veg→Spices).
  - **Context:** The CD's evolving call on the taxonomy experiment.
  - **Status:** `superseded` → built as a non-destructive flag-gated branch, then **PARKED** by the later
    ship-config 1A decision (mono ships). The B-hybrid work is preserved behind `SPLIT_TAXONOMY`.

- **2026-08-09/10 — Drop the Draw vendor attribute.**
  - **Ask:** Remove the Draw vendor attribute.
  - **Context:** Data hygiene.
  - **Status:** `implemented`.

- **2026-08-09/10 — Meta / working-style steers.**
  - **Ask:** Keep continuing without gates (unless a big design decision); poll every ~10 min so tasks don't
    die; add a playtest-strategy-developer agent; switch the vanishing interactive popups to plain-text A/B/C.
  - **Context:** Keep momentum and stop losing questions to disappearing popups.
  - **Status:** `implemented` → **`bg-playstrat`** added; the simulation gate remains the one explicit
    sign-off; A/B/C plain-text decisions adopted.

### ⚑ Not yet actioned (watch — don't let these slip)
**All caught up** — every V7-M steer above is `implemented`, `parked`, or `superseded` with a landing
pointer, and the studio-infra steer below is `implemented`. Nothing captured is awaiting action. The only
open threads are *stale-prose reconciliations* the CD's steers already decided (two-track VP / flat −1 /
min-followers floor / character-kit drift) — those are drift, tracked in `status.md`'s risks and routed to
bg-continuity / bg-rulebook / bg-design, not un-actioned CD asks.

---

## Studio-infra steers (cross-cutting — not version-specific)

- **2026-08-10 — De-duplication / single source of truth (post-V7 close).**
  - **Ask:** *"There seem to be a lot of duplicate docs and files spread around covering the same things …
    we should have something that keeps an eye out for this so we have less bloat, less places to edit or for
    'truth' to get confused after a clear. Less cognitive overload for the user too."* (Archive true history,
    but stop the sprawl.)
  - **Context:** After building the PM pod, the CD found the same content restated across multiple files → an
    editing hazard + truth-drift risk after a context clear.
  - **Status:** `implemented` → landed in commit **`2458d6d`** across the pod contracts + `CLAUDE.md` +
    `SKILL.md`. Per the restraint principle, **no new agent** was added; instead: **`bg-archivist`** gained an
    explicit de-dup remit (one canonical home per topic; consolidate + archive redundant copies), and
    **`bg-producer`** gained a **duplication WATCH** on the keep-current sweep (flag same-truth-in-two-places,
    route consolidation to the Archivist). *(This brief's status.md duplication/drift watch is that remit's
    first live exercise.)*

---

## Archived versions
*Pre-V7 CD steers were not captured under this per-version brief (it post-dates V7-M); the pre-V7 design
history lives in `archive/game-bible-history.md` + `archive/decision-log-pre-v7.md`. When V7-M closes fully,
roll this section's V7-M block down and keep the next version's brief at the top.*
