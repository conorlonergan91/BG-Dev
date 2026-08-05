# Decision Log — Beacon

One line per decision. Newest at top. Format: **date — decision — why — (alternatives rejected)**.

- 2026-08-05 — **v0.2 rule (design→sim→tune loop, iter 1):** the *loser* of the beam picks a ship first; winner still steers the Tide. Why: the critic's #1 issue + sim showed "always play high" dominant (66.7%). After the change no line dominates (spread ~13 pts), games are closer (margin 10→6), and a rule-aware strategy leads at ~59% — depth confirmed. (playtests/sim-notes.md)
- 2026-08-05 — Simulated 3000 games/matchup. Finding: no dominant signal policy (top 3 within ~4%, soft rock-paper-scissors; always_low is a trap); Tide bonus decides ~16% of games (healthy) but avg margin ~10 and "always_high" is tied-for-best. Next test: add a cost to winning the beam so greedy high-play isn't free. (see playtests/sim-notes.md)
- 2026-08-05 — Tide bonus each Night + "the tide turns" (Night's Tide-loser becomes next First Keeper). Why: catch-up valve so a trailing player stays live in a 2p game, less bookkeeping than a signal-reclaim rule. Rejected: single end-game Tide bonus (too swingy); loser-reclaims-signals (fiddlier).
- 2026-08-05 — Core structure: 3 Nights × 4 rounds, Channel of 2, commit 4 of 6 Signals (hold 2). Why: 24 ships divide cleanly (8/Night) and holding 2 signals creates the bluff space. "Lost to the rocks" moved to an optional Rocks variant (playtest Q).
- 2026-08-05 — Core = simultaneous blind Signal selection + Tide tug-of-war + suit set-collection. Why: strongest fun-to-complexity for 2p; all input randomness, no output luck. Rejected: trick-taking core (crowded space), pure drafting (weaker direct tension).
- 2026-08-05 — Concept "Beacon" chosen from ideation shortlist. Why: cozy-competitive nautical hook, card-first (Screentop-friendly), tight 2p tension. Rejected: "Spore Bloom" (fungal engine, too fiddly for a filler), "Heist Clock" (real-time, hard to test remotely).
- 2026-08-05 — Studio demo game started (2-player, Screentop target).
