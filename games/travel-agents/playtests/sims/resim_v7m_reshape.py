"""
resim_v7m_reshape.py — CD-GATED N=400 re-sim driver for the V7-M DAY/NIGHT-ROLE DECK RESHAPE
(commit 4e85ae3: 18 cheap icon-granting DAY engine-seeds / 12 no-icon NIGHT trophies).

Throwaway analysis driver (bg-playtest). Led by THE THESIS: claim many cheap DAY seeds → build a real
icon engine → the engine affords the scarce expensive NIGHT trophies + completes Bookings (the main VP).

Probes, thesis-first:
  HEADLINE       per count: vendor-VP share, bookings, DAY vs NIGHT claim split, day-claims/player,
                 END-OF-GAME icon depth (mean/winner lane depth + winner N+E), apex reachability,
                 pace (turns/plyr), LAST-TRAIN vs STALL %.
  ENGINE FORM    engine_h (the COMPETENT engine-builder, added 2026-08-11) vs balanced field, plus the
                 all-engine_h MIRROR — does building the engine deepen lanes and win?
  HOARDER        vendor-only hoarder + objectives-blind (no_tickets) winrate — MUST be < ~fair (tours lead).
  HEALTH @4p     roster winrate incl. naive baselines (random / no_tickets) vs rule-aware.
Run:  python games/travel-agents/playtests/sims/resim_v7m_reshape.py [N]
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tools", "sim"))
sys.path.insert(0, os.path.join(_ROOT, "games", "travel-agents", "sim"))
import travel_agents as t          # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 400
S = t.STRATEGIES
COUNTS = (3, 4, 5, 6)


def field(name_field, c, n_games, seed):
    return t._run(name_field, n_games, seed=seed, n_players=c)


def seat0(name, c, n_games, seed):
    ef = {0: S[name], **{p: S["balanced"] for p in range(1, c)}}
    w, mt = t._run(ef, n_games, seed=seed, n_players=c)
    return w[0], mt


print(f"# Travel Agents V7-M — DAY/NIGHT DECK RESHAPE · CD-GATED RE-SIM  (N={N}/cell)")
print(f"# config: CANCEL_COST={t._cancel_cost()}  VISIT_MODE={t.VISIT_MODE}  VARIETY={t.VISIT_VARIETY}")
print(f"# night-engine demand by region (icon worth): {dict(t.NIGHT_SIG_DEMAND)}\n")

seed = 1
# ============================================================ HEADLINE — thesis instruments per count
print("=" * 96)
print("HEADLINE (balanced field) — DOES THE ENGINE FORM + DO TOURS LEAD?  per player count")
print("=" * 96)
for c in COUNTS:
    _, mt = field({p: S["balanced"] for p in range(c)}, c, N, seed); seed += N
    share = mt["vendor_vp_share_of_winner"] * 100
    flag = "  <<< BREACH" if share > 40 else ("  (over)" if share > 35 else "")
    print(f"\n## {c}p")
    print(f"  vendor-VP {mt['winner_vendor_vp']:.1f} + booking-VP {mt['winner_booking_vp']:.1f}"
          f"  -> vendor-share {share:.0f}% / booking-share {100-share:.0f}%{flag}   (target 25-35%)")
    print(f"  claims/plyr {mt['claims_per_player']:.2f}  = DAY {mt['day_claims_per_player']:.2f}"
          f" + NIGHT {mt['night_claims_per_player']:.2f}   (thesis wants DAY up toward ~4-6)")
    print(f"  ENGINE DEPTH: mean lane {mt['mean_lane_depth']:.2f}  winner lane {mt['winner_lane_depth']:.2f}"
          f"  winner N+E icons {mt['winner_NE_icons']:.2f}  mean icons {mt['mean_icons_end']:.2f}")
    print(f"  apex claims/gm {mt['apex_claims_per_game']:.3f}  mean APEX net-cost {mt['mean_apex_net_cost']:.2f}"
          f" (n {mt['apex_netcost_n']:.2f})  below-floor blocks/gm {mt['below_floor_blocks_per_game']:.2f}")
    print(f"  free-claims/gm {mt['free_claims_per_game']:.2f} (deep>=7 {mt['free_claims_deep_per_game']:.2f}"
          f" / shallow {mt['free_claims_shallow_per_game']:.2f})  mean net-cost/claim {mt['mean_net_cost_per_claim']:.2f}")
    print(f"  bookings-done/gm {mt['bookings_completed_field']:.1f}  prestige/gm {mt['prestige_completions_per_game']:.2f}"
          f"  turns/plyr {mt['turns_per_player']:.1f}  LAST-TRAIN {mt['end_by_lasttrain']*100:.0f}% / STALL {mt['end_by_stall']*100:.0f}%")
    print(f"  die: removals/gm {mt['die_removals_per_game']:.2f} (contested {mt['die_removals_contested_per_game']:.2f})"
          f"  washes/gm {mt['washes_per_game']:.2f}  cancels/gm {mt['cancels_per_game']:.2f}")

# ============================================================ ENGINE FORMATION — the competent builder
print("\n" + "=" * 96)
print("ENGINE FORMATION — engine_h (COMPETENT builder) vs field + all-engine_h MIRROR")
print("=" * 96)
for c in COUNTS:
    fair = 100.0 / c
    print(f"\n## {c}p  (fair {fair:.0f}%)")
    for name in ("balanced", "human", "engine", "engine_h", "marquee"):
        wr, mt = seat0(name, c, N, seed); seed += N
        print(f"  {name:9} wr {wr*100:4.0f}% (idx {wr/(fair/100):.2f})  winnerLane {mt['winner_lane_depth']:.2f}"
              f"  winnerN+E {mt['winner_NE_icons']:.2f}  apex/gm {mt['apex_claims_per_game']:.3f}"
              f"  apexNet {mt['mean_apex_net_cost']:.2f}(n{mt['apex_netcost_n']:.2f})  DAYclaims/plyr {mt['day_claims_per_player']:.2f}")
    _, mt = field({p: S["engine_h"] for p in range(c)}, c, N, seed); seed += N
    print(f"  [MIRROR all-engine_h] mean lane {mt['mean_lane_depth']:.2f}  winner lane {mt['winner_lane_depth']:.2f}"
          f"  winner N+E {mt['winner_NE_icons']:.2f}  apex/gm {mt['apex_claims_per_game']:.3f}"
          f"  free-deep/gm {mt['free_claims_deep_per_game']:.2f}  DAYclaims/plyr {mt['day_claims_per_player']:.2f}"
          f"  vshare {mt['vendor_vp_share_of_winner']*100:.0f}%")

# ============================================================ HOARDER make-or-break per count
print("\n" + "=" * 96)
print("HOARDER (vendor-only) + no_tickets (objectives-blind) — MUST be < ~fair share (tours must lead)")
print("=" * 96)
for c in COUNTS:
    fair = 100.0 / c
    print(f"\n## {c}p  (fair {fair:.0f}%)")
    for name in ("hoarder", "no_tickets", "marquee", "dodger", "sniper"):
        wr, mt = seat0(name, c, N, seed); seed += N
        tag = ""
        if name == "hoarder":
            tag = "  <<< MAKE-OR-BREAK" + ("  FAIL" if wr * 100 > fair else "  ok")
        print(f"  {name:11} {wr*100:5.1f}%  (idx {wr/(fair/100):.2f}){tag}")

# ============================================================ HEALTH READ @4p
print("\n" + "=" * 96)
print("HEALTH READ @4p — each line in seat0 vs balanced field (naive baselines + rule-aware)")
print("=" * 96)
c = 4
fair = 100.0 / c
roster = ["random", "no_tickets", "hoarder", "dodger", "sniper", "marquee",
          "human", "human_spread", "balanced", "engine", "engine_h", "collector"]
rows = []
for name in roster:
    wr, _ = seat0(name, c, N, seed); seed += N
    rows.append((name, wr * 100))
rows.sort(key=lambda kv: -kv[1])
for name, wr in rows:
    print(f"  {name:14} {wr:5.1f}%  (idx {wr/fair:.2f})")
print(f"\n  fair share @4p = {fair:.0f}%.  Healthy = rule-aware beats naive (random/no_tickets),"
      f" no single line runs away, hoarder < fair.")
