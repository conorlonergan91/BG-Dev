#!/usr/bin/env python3
"""
build_snapshot.py — freeze / list / restore whole-product "builds" (snapshot folders).

A **build** is a self-contained frozen copy of a game's source (and, by default, its committed exports)
at a point in time, stored in `games/<slug>/builds/build-N/`, with a human ledger in
`games/<slug>/builds/BUILDS.md`. When a design goes somewhere that's no longer fun, you can revert to
"build 3" and branch off it.

    python tools/version/build_snapshot.py cut     --game games/beacon --note "v0.3 tide-scaled, fun"
    python tools/version/build_snapshot.py cut     --game games/beacon --note "..." --source-only
    python tools/version/build_snapshot.py list     --game games/beacon
    python tools/version/build_snapshot.py restore  --game games/beacon --build 3        # dry-run
    python tools/version/build_snapshot.py restore  --game games/beacon --build 3 --yes  # overwrite working source

Snapshots exclude `build/` (regenerable scratch) and `builds/` (the snapshots themselves).
`--source-only` also excludes `exports/` (regenerate them from the snapshot's data with `make.sh`).
Reverting is safest on a fresh git branch: `git checkout -b beacon-from-build-3 && restore --yes`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

LEDGER = "BUILDS.md"


def _git(game: Path, *args) -> str:
    try:
        return subprocess.run(["git", "-C", str(game), *args], capture_output=True, text=True,
                              timeout=15).stdout.strip()
    except Exception:
        return ""


def _next_n(builds: Path) -> int:
    if not builds.exists():
        return 1
    ns = [int(m.group(1)) for p in builds.glob("build-*") if (m := re.match(r"build-(\d+)$", p.name))]
    return (max(ns) + 1) if ns else 1


def _weight(game: Path):
    bp = game / "complexity-budget.json"
    if bp.exists():
        try:
            return json.loads(bp.read_text()).get("target_weight")
        except Exception:
            return None
    return None


def cut(game: Path, note: str, source_only: bool) -> int:
    builds = game / "builds"
    builds.mkdir(exist_ok=True)
    n = _next_n(builds)
    dst = builds / f"build-{n}"
    ignore_names = ["build", "builds", ".DS_Store", "__pycache__"]
    if source_only:
        ignore_names.append("exports")
    shutil.copytree(game, dst, ignore=shutil.ignore_patterns(*ignore_names))
    sha = _git(game, "rev-parse", "--short", "HEAD") or "-"
    date = _git(game, "show", "-s", "--format=%cs", "HEAD") or "-"
    weight = _weight(game)
    ledger = builds / LEDGER
    if not ledger.exists():
        ledger.write_text(
            f"# Build ledger — {game.name}\n\n"
            "Each build is a frozen snapshot in `build-N/` (revert with `build_snapshot.py restore`).\n"
            "Newest at bottom.\n\n"
            "| build | date | commit | weight | note |\n|---|---|---|---|---|\n", encoding="utf-8")
    with ledger.open("a", encoding="utf-8") as f:
        f.write(f"| build-{n} | {date} | {sha} | {weight if weight is not None else '-'} | "
                f"{note or '(no note)'} |\n")
    kind = "source-only" if source_only else "source + exports"
    print(f"✓ cut build-{n} ({kind}) → {dst}")
    print(f"  ledger: {ledger}")
    print(f"  commit these so the snapshot is preserved. Revert later with: "
          f"restore --game {game} --build {n} --yes (on a fresh branch).")
    return 0


def list_builds(game: Path) -> int:
    ledger = game / "builds" / LEDGER
    if ledger.exists():
        print(ledger.read_text(encoding="utf-8"))
    else:
        print(f"No builds yet for {game.name}. Cut one with: cut --game {game} --note \"...\"")
    return 0


def restore(game: Path, n: int, yes: bool) -> int:
    src = game / "builds" / f"build-{n}"
    if not src.exists():
        print(f"build-{n} not found in {game/'builds'}"); return 1
    files = [p for p in src.rglob("*") if p.is_file()]
    if not yes:
        print(f"[dry-run] would overlay {len(files)} files from {src} onto {game} "
              f"(build/ and builds/ untouched).")
        print("Re-run with --yes to apply. Do it on a fresh branch: "
              f"git checkout -b {game.name}-from-build-{n}")
        return 0
    shutil.copytree(src, game, dirs_exist_ok=True)
    print(f"✓ restored build-{n} over {game} ({len(files)} files). "
          "Note: this overlays; files added after the build are not removed. Review `git status`.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze / list / restore whole-product builds.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("cut", "list", "restore"):
        s = sub.add_parser(name)
        s.add_argument("--game", required=True, type=Path)
        if name == "cut":
            s.add_argument("--note", default="")
            s.add_argument("--source-only", action="store_true",
                           help="exclude exports/ (regenerate renders from the snapshot's data)")
        if name == "restore":
            s.add_argument("--build", required=True, type=int)
            s.add_argument("--yes", action="store_true", help="actually overwrite working source")
    args = ap.parse_args()

    if args.cmd == "cut":
        return cut(args.game, args.note, args.source_only)
    if args.cmd == "list":
        return list_builds(args.game)
    if args.cmd == "restore":
        return restore(args.game, args.build, args.yes)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
