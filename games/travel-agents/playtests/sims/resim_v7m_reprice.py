"""
resim_v7m_reprice.py — CD-GATED N=400 re-sim driver for the V7-M vendor RE-PRICE + event redesign.
Throwaway analysis driver (bg-playtest). Emits exactly the probes the re-sim charter asks for:
  HEADLINE  vendor-VP share of winner + vendor-only HOARDER winrate (the CD's balance concern)
  FREE-CLAIM  free-claims/game by engine depth + net-cost-at-claim per apex (engine vs casual)
  REACHABILITY  apex claim-rate, below-floor blocks, prestige/last-train completion (Failure-Mode-B)
  ENGINE→PAYOFF  time-to-first-marquee proxy; day-cheap-grab hoarding loses
  WASH/CLOCK  game length + washes/game under EV-N29
  HEALTH  dominant-line / naive-winner / mirror check
Run:  python games/travel-agents/playtests/sims/resim_v7m_reprice.py [N]
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tools", "sim"))
sys.path.insert(0, os.path.join(_ROOT, "games", "travel-agents", "sim"))
import travel_agents as t          # noqa: E402
from engine import run_match       # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 400
S = t.STRATEGIES
COUNTS = (3, 4, 5, 6)


def winrate(agents, n_players, n_games, seed):
    """Seat-0 winrate for `agents` (dict seat->fn) at n_players, plus averaged metrics."""
    w, mt = t._run(agents, n_games, seed=seed, n_players=n_players)
    return w, mt


def seat0_vs_field(name, n_players, n_games, seed):
    ef = {0: S[name], **{p: S["balanced"] for p in range(1, n_players)}}
    w, mt = t._run(ef, n_games, seed=seed, n_players=n_players)
    return w[0], mt


print(f"# Travel Agents V7-M — vendor RE-PRICE + event redesign · CD-GATED RE-SIM  (N={N}/cell)")
print(f"# config: CANCEL_COST={t._cancel_cost()}  VISIT_MODE={t.VISIT_MODE}  VARIETY={t.VISIT_VARIETY}\n")

# ============================================================ HEADLINE + core field per count
print("=" * 92)
print("HEADLINE — vendor-VP share of winner (target 25-35%, ceiling 40%)  +  field reachability")
print("=" * 92)
seed = 1
field_mt = {}
for c in COUNTS:
    _, mt = winrate({p: S["balanced"] for p in range(c)}, c, N, seed); seed += N
    field_mt[c] = mt
    share = mt["vendor_vp_share_of_winner"] * 100
    flag = "  <<< BREACH" if share > 40 else ("  (over target)" if share > 35 else "")
    print(f"\n## {c}p")
    print(f"  vendor-VP {mt['winner_vendor_vp']:.1f} + booking-VP {mt['winner_booking_vp']:.1f}"
          f"  -> vendor-share {share:.0f}% / booking-share {100-share:.0f}%{flag}")
    print(f"  apex claims/game {mt['apex_claims_per_game']:.2f}  (per plyr {mt['apex_claims_per_player']:.3f})"
          f"  below-floor blocks/gm {mt['below_floor_blocks_per_game']:.2f}")
    print(f"  free-claims/gm {mt['free_claims_per_game']:.2f}  (deep>=7icons {mt['free_claims_deep_per_game']:.2f} /"
          f" shallow {mt['free_claims_shallow_per_game']:.2f} / apex {mt['free_apex_claims_per_game']:.2f})")
    print(f"  mean net-cost/claim {mt['mean_net_cost_per_claim']:.2f}  | mean APEX net-cost "
          f"{mt['mean_apex_net_cost']:.2f} (n={mt['apex_netcost_n']:.2f})")
    print(f"  prestige-done/gm {mt['prestige_completions_per_game']:.2f}  bookings-done/gm "
          f"{mt['bookings_completed_field']:.1f}  LAST-TRAIN end {mt['end_by_lasttrain']*100:.0f}% /"
          f" STALL {mt['end_by_stall']*100:.0f}%")
    print(f"  turns/plyr {mt['turns_per_player']:.1f}  washes/gm {mt['washes_per_game']:.2f}  "
          f"restocks/gm {mt['restocks_per_game']:.2f}  cancels/gm {mt['cancels_per_game']:.2f}")

# ============================================================ HOARDER (make-or-break) + exploit panel
print("\n" + "=" * 92)
print("HOARDER (vendor-only) winrate — MUST be < ~10% (tours must dominate) + exploit panel")
print("=" * 92)
for c in COUNTS:
    fair = 100.0 / c
    print(f"\n## {c}p  (fair share {fair:.0f}%)")
    for name in ("hoarder", "no_tickets", "marquee", "dodger", "denier", "sniper", "late_battler"):
        wr, mt = seat0_vs_field(name, c, N, seed); seed += N
        tag = ""
        if name == "hoarder":
            tag = "  <<< MAKE-OR-BREAK" + ("  FAIL" if wr * 100 > 10 else "  ok")
        print(f"    {name:13} {wr*100:5.1f}%  (idx {wr/(fair/100):.2f}){tag}")

# ============================================================ FREE-CLAIM PATH — deep engine bots
print("\n" + "=" * 92)
print("FREE-CLAIM PATH — do DEEP-ENGINE lines reach the discounted/free apex? (engine, marquee)")
print("=" * 92)
for c in (3, 4):
    print(f"\n## {c}p  engine/marquee in seat0 vs balanced field")
    for name in ("engine", "marquee"):
        wr, mt = seat0_vs_field(name, c, N, seed); seed += N
        print(f"    {name:8} wr {wr*100:4.0f}%  apex/gm {mt['apex_claims_per_game']:.2f}  "
              f"free/gm {mt['free_claims_per_game']:.2f} (deep {mt['free_claims_deep_per_game']:.2f})  "
              f"mean-apex-net {mt['mean_apex_net_cost']:.2f} (n {mt['apex_netcost_n']:.2f})  "
              f"vendor-share {mt['vendor_vp_share_of_winner']*100:.0f}%")
    # all-engine mirror: a table full of committed engines — does the free-claim path open then?
    _, mt = winrate({p: S["engine"] for p in range(c)}, c, N, seed); seed += N
    print(f"    [MIRROR all-engine] apex/gm {mt['apex_claims_per_game']:.2f}  free/gm "
          f"{mt['free_claims_per_game']:.2f} (deep {mt['free_claims_deep_per_game']:.2f} / apex "
          f"{mt['free_apex_claims_per_game']:.2f})  mean-apex-net {mt['mean_apex_net_cost']:.2f} "
          f"(n {mt['apex_netcost_n']:.2f})  vendor-share {mt['vendor_vp_share_of_winner']*100:.0f}%")
    _, mt = winrate({p: S["marquee"] for p in range(c)}, c, N, seed); seed += N
    print(f"    [MIRROR all-marquee] apex/gm {mt['apex_claims_per_game']:.2f}  free/gm "
          f"{mt['free_claims_per_game']:.2f} (deep {mt['free_claims_deep_per_game']:.2f} / apex "
          f"{mt['free_apex_claims_per_game']:.2f})  mean-apex-net {mt['mean_apex_net_cost']:.2f} "
          f"(n {mt['apex_netcost_n']:.2f})")

# ============================================================ HEALTH READ — dominant line across roster
print("\n" + "=" * 92)
print("HEALTH READ — each line in seat0 vs balanced field @4p (naive baselines + rule-aware)")
print("=" * 92)
c = 4
fair = 100.0 / c
roster = ["random", "no_tickets", "hoarder", "dodger", "avoider", "contester", "collector",
          "concentrate", "rush", "engine", "marquee", "sniper", "human", "human_contest",
          "human_spread", "balanced"]
rows = []
for name in roster:
    wr, _ = seat0_vs_field(name, c, N, seed); seed += N
    rows.append((name, wr * 100))
rows.sort(key=lambda kv: -kv[1])
for name, wr in rows:
    print(f"    {name:14} {wr:5.1f}%  (idx {wr/fair:.2f})")
print(f"\n  fair share @4p = {fair:.0f}%.  Healthy = rule-aware beats naive (random/no_tickets),"
      f" no single line runs away, hoarder < ~10%.")
