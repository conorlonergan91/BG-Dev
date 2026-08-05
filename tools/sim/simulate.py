#!/usr/bin/env python3
"""
simulate.py — run a game module through the simulation harness.

A game module (e.g. games/<slug>/sim/<slug>.py) must expose:
    GAME        — an object implementing the engine's Game protocol (see engine.py)
    STRATEGIES  — {name: agent_callable}
    TITLE       — optional str

Usage:
    python tools/sim/simulate.py --module games/beacon/sim/beacon.py --n 3000
    python tools/sim/simulate.py --module games/beacon/sim/beacon.py --n 3000 --out games/beacon/playtests/sim-results.md
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from engine import round_robin, format_round_robin, play_series


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser(description="Simulate a game module.")
    ap.add_argument("--module", required=True, type=Path)
    ap.add_argument("--n", type=int, default=2000, help="games per matchup")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=Path, default=None, help="write the markdown report here")
    ap.add_argument("--matchup", default=None,
                    help="run a single matchup 'A:B' (P0:P1) and print its detailed metrics instead of a tournament")
    args = ap.parse_args()

    mod = load_module(args.module)
    game = getattr(mod, "GAME")
    strategies = getattr(mod, "STRATEGIES")
    title = getattr(mod, "TITLE", args.module.stem)

    if args.matchup:
        a, b = args.matchup.split(":")
        res = play_series(game, {0: strategies[a], 1: strategies[b]}, n=args.n, base_seed=args.seed)
        print(f"# {title} — matchup {a} (P0) vs {b} (P1), {res['n']} games\n")
        print(f"win rate: {a}={res['win_rate'][0]*100:.1f}%  {b}={res['win_rate'][1]*100:.1f}%  "
              f"ties={res['tie_rate']*100:.1f}%")
        print(f"score mean: {a}={res['score_mean'][0]:.1f}  {b}={res['score_mean'][1]:.1f}")
        print("metrics:")
        for k, v in res["metrics"].items():
            print(f"  {k}: {v:.3f}")
        return 0

    res = round_robin(game, strategies, n=args.n, base_seed=args.seed)
    report = format_round_robin(res, title=f"{title} — simulation report")
    print(report)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report + "\n", encoding="utf-8")
        print(f"\n[sim] wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
