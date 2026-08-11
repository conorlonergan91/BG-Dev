"""
sweep_die_L.py — CD-GATED targeted sweep: CLOSING-TIME DIE close-probability x track-length L x count.
(bg-playtest, 2026-08-11). Resolves the double-duty die tension flagged on the V7-M reshape
(commit 4e85ae3): the die eats DAY engine-seeds (gentler = deeper engine) AND drains the NIGHT pool to
END the game (gentler = more STALL). Sweeps faces x L together to find a config that kills the 4-5p
STALL (<~20%) AND lifts claims/player (~4) without breaching vendor-VP share (25-35%).

The die faces (t.DIE_FACES) and L (t.TRACK_L_OVERRIDE) are module globals resolved at call-time in the
LOCKED engine (_closing_time_die / _track_length), so this driver sweeps them by REASSIGNMENT — no rule
or map.json value is edited. Winner config is reported for the CD to apply after sign-off.

Faces swept (close-probability = 4 region faces / total):
  d6  = [N,C,S,E,BLANK,BLANK]                 -> 4/6 = 67%  (CURRENT / baseline)
  d8  = [N,C,S,E,BLANK*4]                     -> 4/8 = 50%  (CD's proposed lever)
  d10 = [N,C,S,E,BLANK*6]                     -> 4/10 = 40% (gentler third point)
L swept: {2, 3}.   Counts: {3,4,5,6}.

Run:  python games/travel-agents/playtests/sims/sweep_die_L.py [N]     (default N=300)
      python games/travel-agents/playtests/sims/sweep_die_L.py 300 --guard  (also hoarder/no_tickets)
"""
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tools", "sim"))
sys.path.insert(0, os.path.join(_ROOT, "games", "travel-agents", "sim"))
import travel_agents as t          # noqa: E402

N = 300
GUARD = "--guard" in sys.argv
for a in sys.argv[1:]:
    if a.isdigit():
        N = int(a)

S = t.STRATEGIES
COUNTS = (3, 4, 5, 6)
FACES = {
    "d6/67%": ("N", "C", "S", "E", "BLANK", "BLANK"),
    "d8/50%": ("N", "C", "S", "E", "BLANK", "BLANK", "BLANK", "BLANK"),
    "d10/40%": ("N", "C", "S", "E", "BLANK", "BLANK", "BLANK", "BLANK", "BLANK", "BLANK"),
}
LS = (2, 3)


def set_die(faces_key, L):
    t.DIE_FACES = FACES[faces_key]
    t.TRACK_L_OVERRIDE = L


def field(c, seed):
    _, mt = t._run({p: S["balanced"] for p in range(c)}, N, seed=seed, n_players=c)
    return mt


def seat0(name, c, seed):
    ef = {0: S[name], **{p: S["balanced"] for p in range(1, c)}}
    w, _ = t._run(ef, N, seed=seed, n_players=c)
    return w[0]


seed = 1
t0 = time.time()
print(f"# Travel Agents V7-M — CLOSING-TIME DIE x L SWEEP  (N={N}/cell, balanced field)")
print(f"# baseline (map.json) = d6/67% ; L per-count {{3:2,4:3,5:3,6:3}}. Guard runs: {GUARD}")
print(f"# TARGETS: STALL<~20% (must-fix) · claims/plyr up toward ~4 · vendor-share 25-35% (no breach)\n")

# columns
hdr = (f"{'faces':8} {'L':>2} {'cnt':>3} | {'STALL%':>6} {'turns/p':>7} | "
       f"{'claim/p':>7} {'day':>5} {'nt':>5} | {'wLane':>5} {'wN+E':>5} | "
       f"{'vshr%':>5} {'apex/gm':>7} {'die-rm':>6} {'blank':>5} {'wash':>5}")

results = {}   # (faces,L,count) -> mt
for faces_key in FACES:
    print("=" * len(hdr))
    print(hdr)
    print("-" * len(hdr))
    for L in LS:
        for c in COUNTS:
            set_die(faces_key, L)
            mt = field(c, seed); seed += N
            results[(faces_key, L, c)] = mt
            stall = mt["end_by_stall"] * 100
            vshr = mt["vendor_vp_share_of_winner"] * 100
            flag = ""
            if stall < 20:
                flag += " S"      # stall OK
            if 25 <= vshr <= 35:
                flag += "V"       # vendor-share in band
            print(f"{faces_key:8} {L:>2} {c:>3} | {stall:6.0f} {mt['turns_per_player']:7.1f} | "
                  f"{mt['claims_per_player']:7.2f} {mt['day_claims_per_player']:5.2f} "
                  f"{mt['night_claims_per_player']:5.2f} | {mt['winner_lane_depth']:5.2f} "
                  f"{mt['winner_NE_icons']:5.2f} | {vshr:5.0f} {mt['apex_claims_per_game']:7.3f} "
                  f"{mt['die_removals_per_game']:6.2f} {mt['die_blank_frac']:5.2f} "
                  f"{mt['washes_per_game']:5.2f}{flag}")
        print()

print(f"# balanced sweep done in {time.time()-t0:.0f}s\n")

# ---- GUARD: hoarder + no_tickets seat0 winrate on candidate configs (must be < ~fair share) ----
if GUARD:
    print("=" * 96)
    print("GUARDRAIL — hoarder (vendor-only) + no_tickets (objectives-blind) seat0 winrate vs fair share")
    print("MUST be < fair (tours must lead). Run on the shortlist + baseline.")
    print("=" * 96)
    # shortlist: baseline d6 per-count-L is handled separately; here sweep the promising gentle configs
    CANDIDATES = [("d6/67%", 2), ("d8/50%", 2), ("d8/50%", 3), ("d10/40%", 2)]
    for faces_key, L in CANDIDATES:
        print(f"\n## {faces_key}  L={L}")
        for c in COUNTS:
            fair = 100.0 / c
            set_die(faces_key, L)
            h = seat0("hoarder", c, seed); seed += N
            nt = seat0("no_tickets", c, seed); seed += N
            hf = "FAIL" if h * 100 > fair else "ok"
            ntf = "FAIL" if nt * 100 > fair else "ok"
            print(f"  {c}p (fair {fair:.0f}%): hoarder {h*100:5.1f}% {hf:4}   "
                  f"no_tickets {nt*100:5.1f}% {ntf}")
    print(f"\n# total sweep+guard {time.time()-t0:.0f}s")
