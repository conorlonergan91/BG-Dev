#!/usr/bin/env python3
"""
check_game.py — a consistency linter for a game's single source of truth.

As data + rules + manifest drift apart, small breaks creep in (a duplicate card id, a bad quantity, a
card `type` no theme colours, a sim module that no longer imports). This catches them cheaply so the
"data is the source of truth" promise stays honest.

Usage:
    python tools/lint/check_game.py --game games/beacon
    python tools/lint/check_game.py --game games/beacon --theme nautical   # also check suit coverage

Exit code is non-zero if any ERRORs are found (WARN/INFO don't fail).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import get_theme  # noqa: E402

RECOMMENDED = ["id", "name", "type", "value", "quantity"]


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0
    def error(self, msg): self.errors += 1; print(f"  \033[31m[ERROR]\033[0m {msg}")
    def warn(self, msg): self.warns += 1; print(f"  \033[33m[WARN ]\033[0m {msg}")
    def info(self, msg): print(f"  [info ] {msg}")
    def ok(self, msg): print(f"  \033[32m[ ok  ]\033[0m {msg}")


def check_csv(path: Path, theme, rep: Report):
    print(f"\n• {path}")
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    if not rows:
        rep.error("no rows"); return
    cols = rows[0].keys()
    for c in RECOMMENDED:
        if c not in cols:
            rep.warn(f"missing recommended column '{c}'")

    ids, dup = set(), set()
    total = 0
    types = {}
    for i, r in enumerate(rows, 1):
        cid = (r.get("id") or "").strip()
        if cid:
            (dup.add(cid) if cid in ids else ids.add(cid))
        else:
            rep.warn(f"row {i}: empty id")
        if not (r.get("name") or "").strip():
            rep.warn(f"row {i} ({cid}): empty name")
        # quantity
        q = (r.get("quantity") or "1").strip()
        try:
            qn = int(q)
            if qn < 1:
                rep.error(f"row {i} ({cid}): quantity {qn} < 1")
            total += max(qn, 0)
        except ValueError:
            rep.error(f"row {i} ({cid}): quantity '{q}' is not an integer")
        # numeric value/cost when present
        for numf in ("value", "cost"):
            val = (r.get(numf) or "").strip()
            if val:
                try:
                    float(val)
                except ValueError:
                    rep.error(f"row {i} ({cid}): {numf} '{val}' is not numeric")
        t = (r.get("type") or "").strip()
        types[t] = types.get(t, 0) + 1

    if dup:
        rep.error(f"duplicate ids: {sorted(dup)}")
    else:
        rep.ok(f"{len(rows)} rows, {total} cards, unique ids")
    rep.info(f"types: " + ", ".join(f"{t or '(blank)'}×{n}" for t, n in sorted(types.items())))

    if theme is not None:
        known = set(theme["suits"].keys())
        for t in types:
            if t and t.strip().lower() not in known:
                rep.warn(f"type '{t}' has no suit entry in theme '{theme.get('_name','?')}' "
                         f"→ will render with the default colour/emblem")


def check_sim(game_dir: Path, rep: Report):
    sim_dir = game_dir / "sim"
    mods = list(sim_dir.glob("*.py")) if sim_dir.is_dir() else []
    if not mods:
        return
    import importlib.util
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sim"))
    for m in mods:
        print(f"\n• {m}")
        try:
            spec = importlib.util.spec_from_file_location(m.stem, m)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            missing = [a for a in ("GAME", "STRATEGIES") if not hasattr(mod, a)]
            if missing:
                rep.error(f"sim module missing: {', '.join(missing)}")
            else:
                rep.ok(f"imports; exposes GAME + {len(mod.STRATEGIES)} strategies")
        except Exception as e:
            rep.error(f"sim module failed to import: {e}")


def main():
    ap = argparse.ArgumentParser(description="Lint a game's data + sim for consistency.")
    ap.add_argument("--game", required=True, type=Path, help="path to games/<slug>")
    ap.add_argument("--theme", default=None, help="if set, check card 'type' has suit colours in this theme")
    args = ap.parse_args()

    rep = Report()
    theme = None
    if args.theme:
        theme = get_theme(args.theme); theme["_name"] = args.theme

    comp = args.game / "components"
    csvs = sorted(comp.glob("*.csv")) if comp.is_dir() else []
    if not csvs:
        rep.warn(f"no component CSVs found in {comp}")
    for c in csvs:
        check_csv(c, theme, rep)

    check_sim(args.game, rep)

    print(f"\n{'='*48}\nResult: {rep.errors} error(s), {rep.warns} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
