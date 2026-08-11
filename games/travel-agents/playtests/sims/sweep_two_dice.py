"""
sweep_two_dice.py — CD-GATED sweep of the TWO-DICE / per-phase-cadence Closing-Time model
(bg-playtest, 2026-08-11). Supersedes the single-die sweep: the CD's steer is a GENTLE DAY die (spare
engine seeds → deep lanes) + a HARSH NIGHT die (drain the night pool → the game ENDS → kill the 4-5p
stall). The 1-D exploration showed the real driver is roll FREQUENCY (per-phase L / cadence), not face
harshness — so this sweep models BOTH: independent day/night die FACES *and* independent day/night L.

All four levers are LOCKED-engine module globals resolved at roll time (_die_faces_for / _track_length),
so the driver sweeps them by REASSIGNMENT — no rule or map.json value is edited. Winner reported for the
CD to apply on sign-off.

Die faces (close-prob = 4 region faces / total):
  d4  = [N,C,S,E]                 4/4  = 100%  (harshest — every roll closes; a clean physical d4)
  d6  = [N,C,S,E,B,B]             4/6  =  67%  (CURRENT die)
  d8  = [N,C,S,E,B,B,B,B]         4/8  =  50%
  d10 = [N,C,S,E,B*6]             4/10 =  40%
  d12 = [N,C,S,E,B*8]             4/12 =  33%  (gentlest)
Cadence L = rounds per track cycle before a roll (L=1 rolls every round).

Run:  python games/travel-agents/playtests/sims/sweep_two_dice.py [N] [--guard]
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
FACE = {
    "d4": ("N", "C", "S", "E"),
    "d6": ("N", "C", "S", "E", "BLANK", "BLANK"),
    "d8": ("N", "C", "S", "E") + ("BLANK",) * 4,
    "d10": ("N", "C", "S", "E") + ("BLANK",) * 6,
    "d12": ("N", "C", "S", "E") + ("BLANK",) * 8,
}


def set_dice(day_face, day_L, night_face, night_L):
    t.DIE_FACES_DAY = FACE[day_face]
    t.DIE_FACES_NIGHT = FACE[night_face]
    t.TRACK_L_DAY = day_L
    t.TRACK_L_NIGHT = night_L
    t.TRACK_L_OVERRIDE = 0


def field(c, seed):
    _, mt = t._run({p: S["balanced"] for p in range(c)}, N, seed=seed, n_players=c)
    return mt


def seat0(name, c, seed):
    ef = {0: S[name], **{p: S["balanced"] for p in range(1, c)}}
    w, _ = t._run(ef, N, seed=seed, n_players=c)
    return w[0]


# ---- the shortlisted configs (day_face, day_L, night_face, night_L, label) ----
# ordered cheapest-component-cost first. "1die" = reuse the current d6 in BOTH phases, only the CADENCE
# differs by phase (zero new dice). "2die" = a distinct gentle day die + harsh night die.
CONFIGS = [
    ("d6", 3, "d6", 1, "1die  d6 dayL3 / d6 nightL1  (ZERO new dice: cadence-only)"),
    ("d6", 3, "d6", 2, "1die  d6 dayL3 / d6 nightL2  (cadence-only, gentler night)"),
    ("d10", 3, "d6", 1, "2die  d10 dayL3 / d6 nightL1  (gentle day die + current night die)"),
    ("d10", 3, "d4", 1, "2die  d10 dayL3 / d4 nightL1  (gentle day + harsh night, CD full model)"),
    ("d8", 3, "d6", 1, "2die  d8 dayL3 / d6 nightL1"),
    ("d12", 4, "d6", 1, "2die  d12 dayL4 / d6 nightL1  (max-gentle day, push claims up)"),
]

seed = 1
t0 = time.time()
print(f"# Travel Agents V7-M — TWO-DICE / PER-PHASE-CADENCE SWEEP  (N={N}/cell, balanced field)")
print(f"# Baseline single-die (map): STALL ~30/73/62/36% at 3/4/5/6p — the finding this must fix.")
print(f"# TARGETS: STALL<~20% every count (must-fix) · claims/plyr up toward ~4 · vshare 25-35% · turns/p<~55\n")

hdr = (f"{'cnt':>3} | {'STALL%':>6} {'turns/p':>7} | {'claim/p':>7} {'day':>5} {'nt':>5} | "
       f"{'wLane':>5} {'wN+E':>5} {'apex/gm':>7} | {'vshr%':>5} {'wash':>5} {'gift':>5} {'die-rm':>6}")

store = {}
for day_face, day_L, night_face, night_L, label in CONFIGS:
    print("=" * 96)
    print(f"CONFIG: {label}")
    print(hdr)
    print("-" * 96)
    for c in COUNTS:
        set_dice(day_face, day_L, night_face, night_L)
        mt = field(c, seed); seed += N
        store[(label, c)] = mt
        stall = mt["end_by_stall"] * 100
        vshr = mt["vendor_vp_share_of_winner"] * 100
        flags = ""
        flags += "S" if stall < 20 else "."
        flags += "V" if 25 <= vshr <= 35 else "."
        flags += "T" if mt["turns_per_player"] < 55 else "."
        print(f"{c:>3} | {stall:6.0f} {mt['turns_per_player']:7.1f} | {mt['claims_per_player']:7.2f} "
              f"{mt['day_claims_per_player']:5.2f} {mt['night_claims_per_player']:5.2f} | "
              f"{mt['winner_lane_depth']:5.2f} {mt['winner_NE_icons']:5.2f} {mt['apex_claims_per_game']:7.3f} | "
              f"{vshr:5.0f} {mt['washes_per_game']:5.2f} {mt['gifts_per_game']:5.2f} "
              f"{mt['die_removals_per_game']:6.2f}  {flags}")
    print()

print(f"# balanced sweep done in {time.time()-t0:.0f}s   (flags: S=stall<20  V=vshare 25-35  T=turns<55)\n")

if GUARD:
    print("=" * 96)
    print("GUARDRAIL — hoarder (vendor-only) + no_tickets (blind) seat0 winrate — MUST be < fair share")
    print("=" * 96)
    for day_face, day_L, night_face, night_L, label in CONFIGS:
        set_dice(day_face, day_L, night_face, night_L)
        print(f"\n## {label}")
        for c in COUNTS:
            fair = 100.0 / c
            set_dice(day_face, day_L, night_face, night_L)
            h = seat0("hoarder", c, seed); seed += N
            nt = seat0("no_tickets", c, seed); seed += N
            print(f"  {c}p (fair {fair:.0f}%): hoarder {h*100:5.1f}% {'FAIL' if h*100>fair else 'ok':4}"
                  f"   no_tickets {nt*100:5.1f}% {'FAIL' if nt*100>fair else 'ok'}")
    print(f"\n# total {time.time()-t0:.0f}s")
