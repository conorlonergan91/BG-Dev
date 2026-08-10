#!/usr/bin/env python3
"""Throwaway re-smoke driver for the §17 vendor-depletion clock + Closing-Time die (bg-playtest,
2026-08-10). NOT the CD-gated full sweep — small instrumented batches to answer the make-or-break
questions before the gate. Run: python3 resmoke_vendor_clock.py [games_per_cell]."""
import os
import sys
import statistics

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "..", "..", "sim")))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", "tools", "sim")))


def _reload():
    """Re-import the sim so env-var knobs (TA_TRACK_L / TA_DIE_FORCE) are re-read for each cell."""
    import importlib
    if "travel_agents" in sys.modules:
        del sys.modules["travel_agents"]
    import travel_agents as TA
    importlib.reload(TA)
    return TA


def cell(c, L, N, seed=1, strat="balanced", chars=None, force=None):
    if L:
        os.environ["TA_TRACK_L"] = str(L)
    else:
        os.environ.pop("TA_TRACK_L", None)
    if force:
        os.environ["TA_DIE_FORCE"] = force
    else:
        os.environ.pop("TA_DIE_FORCE", None)
    TA = _reload()
    from engine import run_match
    g = TA._Seeded(c, chars)
    agents = {p: TA.STRATEGIES[strat] for p in range(c)}
    tpp, dierem, diecont, norem, blank, cf, back, ncl = [], [], [], [], [], [], [], []
    stall = lt = 0
    for i in range(N):
        sc, mt = run_match(g, agents, seed + i)
        tpp.append(mt["turns_per_player"])
        dierem.append(mt["die_removals_per_game"])
        diecont.append(mt["die_removals_contested_per_game"])
        norem.append(mt["die_noremovable_per_game"])
        blank.append(mt["die_blank_frac"])
        cf.append(mt["contested_frac"])
        back.append(mt["backstop_fires_per_game"])
        ncl.append(mt["claims_per_game"])
        stall += mt["end_by_stall"]
        lt += mt["end_by_lasttrain"]
    m = statistics.mean
    return {
        "tpp": m(tpp), "tpp_sd": statistics.pstdev(tpp), "tpp_min": min(tpp), "tpp_max": max(tpp),
        "die_rem": m(dierem), "die_cont": m(diecont), "norem": m(norem), "blank": m(blank),
        "cf": m(cf), "claims": m(ncl), "back": m(back),
        "stall": stall / N, "lt": lt / N,
    }


def exploit(c, name, L, N, seed=777):
    os.environ["TA_TRACK_L"] = str(L)
    os.environ.pop("TA_DIE_FORCE", None)
    TA = _reload()
    from engine import run_match
    g = TA._Seeded(c)
    agents = {0: TA.STRATEGIES[name], **{p: TA.STRATEGIES["balanced"] for p in range(1, c)}}
    won = 0.0
    for i in range(N):
        sc, mt = run_match(g, agents, seed + i)
        best = max(sc.values())
        winners = [q for q, v in sc.items() if v == best]
        if 0 in winners:
            won += 1.0 / len(winners)
    return won / N


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    COUNTS = (3, 4, 5, 6)
    LS = (1, 2, 3, 4)

    print(f"=== §17 VENDOR-CLOCK RE-SMOKE  (N={N}/cell, balanced self-play) ===\n")
    print("(1)+(3)+(5)  L-SWEEP per count  — target turns/player 26–32, STALL→0")
    print(f"{'cnt':>3} {'L':>2} | {'t/p':>5} {'sd':>4} {'min':>4} {'max':>4} | {'STALL':>5} {'LT':>4} | "
          f"{'claims':>6} {'die_rem':>7} {'contst':>6} {'no-rem':>6} {'blank%':>6} | {'cf%':>5} {'back':>4}")
    print("-" * 104)
    best_L = {}
    for c in COUNTS:
        rows = {}
        for L in LS:
            r = cell(c, L, N)
            rows[L] = r
            flag = "  <-- in band" if 26 <= r["tpp"] <= 32 and r["stall"] < 0.02 else ""
            print(f"{c:>3} {L:>2} | {r['tpp']:5.1f} {r['tpp_sd']:4.1f} {r['tpp_min']:4.0f} {r['tpp_max']:4.0f} | "
                  f"{r['stall']*100:4.0f}% {r['lt']*100:3.0f}% | {r['claims']:6.1f} {r['die_rem']:7.1f} "
                  f"{r['die_cont']:6.2f} {r['norem']:6.1f} {r['blank']*100:5.0f}% | {r['cf']*100:5.1f} {r['back']:4.2f}{flag}")
        # pick the L whose t/p is closest to 29 with stall<2%
        cand = [(abs(rows[L]["tpp"] - 29), L) for L in LS if rows[L]["stall"] < 0.02]
        best_L[c] = min(cand)[1] if cand else min((abs(rows[L]["tpp"] - 29), L) for L in LS)[1]
        print()

    print(f"Recommended L per count (closest to 29 t/p, STALL<2%): {best_L}\n")

    print("(2)  FREEZE-GUARANTEE — contrived stress at the recommended L")
    # 2a: all-BLANK die + NORMAL bots (claims drain the pool; deck-empty backstop clears lingering static)
    for c in COUNTS:
        r = cell(c, best_L[c], max(60, N // 2), force="BLANK")
        print(f"  2a {c}p all-BLANK die + balanced bots: t/p {r['tpp']:5.1f}  STALL {r['stall']*100:3.0f}%  "
              f"backstop/gm {r['back']:.2f}  (die_rem {r['die_rem']:.1f} must be 0)")
    # 2b: all-BLANK die + ZERO-CLAIM bots (never bribe/claim) — the pathological freeze probe
    os.environ["TA_TRACK_L"] = str(best_L[4])
    os.environ["TA_DIE_FORCE"] = "BLANK"
    TA = _reload()
    from engine import run_match

    def never_claim(s, p, legal, rng):
        # a bot that refuses to bribe/claim/promote — only travels/visits, so nothing drains the pool
        for a in legal:
            if a[0] == "visit":
                return a
        for a in legal:
            if a[0] in ("travel", "cstore"):
                return a
        return legal[0]

    g = TA._Seeded(4)
    outs = []
    for i in range(30):
        sc, mt = run_match(g, {p: never_claim for p in range(4)}, 5000 + i)
        outs.append((mt["turns_per_player"], mt["end_by_stall"], mt["backstop_fires_per_game"], mt["die_removals_per_game"]))
    tpp = statistics.mean(o[0] for o in outs)
    st = statistics.mean(o[1] for o in outs)
    bk = statistics.mean(o[2] for o in outs)
    print(f"  2b 4p all-BLANK die + ZERO-CLAIM bots (L={best_L[4]}): t/p {tpp:5.1f}  STALL {st*100:3.0f}%  "
          f"backstop/gm {bk:.2f}  die_rem {statistics.mean(o[3] for o in outs):.1f}  "
          f"-> terminates? {'YES' if tpp < TA.STALL_CAP else 'NO'}")
    print()

    print("(4)  DOWNSTREAM RE-JUDGE on the now-healthy end-state (at recommended L)")
    print("  HOARDER (vendor-only) seat0 win% vs balanced field  — MUST be <~10% (tours dominate):")
    for c in COUNTS:
        w = exploit(c, "hoarder", best_L[c], max(60, N))
        print(f"    {c}p (fair {100/c:.0f}%): hoarder {w*100:4.0f}%   {'OK' if w < 0.12 else 'FLAG'}")
    print("  contested_frac at recommended L (fights still happen?):")
    for c in COUNTS:
        r = cell(c, best_L[c], N)
        print(f"    {c}p: contested_frac {r['cf']*100:4.1f}%  (die-closed contests/gm {r['die_cont']:.2f} — "
              f"followers-home path)")
