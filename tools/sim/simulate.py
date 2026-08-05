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

from engine import round_robin, format_round_robin


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
    args = ap.parse_args()

    mod = load_module(args.module)
    game = getattr(mod, "GAME")
    strategies = getattr(mod, "STRATEGIES")
    title = getattr(mod, "TITLE", args.module.stem)

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
