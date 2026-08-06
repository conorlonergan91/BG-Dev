#!/usr/bin/env python3
"""
check_cost.py — a cost-of-goods (COGS) & component-footprint gauge.

The COST analog of tools/complexity/check_complexity.py. Complexity creep makes a game harder to learn;
component creep makes it more expensive to make, heavier to ship, and harder to pitch or crowdfund-fulfil
— and for a designer minimising upfront cost, that's decisive. This tracks the footprint against a
`component-cost-budget.json` set at project start.

The biggest lever is the number of *unique component types* (each type = its own tooling, assembly step,
and QC pass), then box size (freight + tariff exposure), then raw piece count. See
knowledge/cost-and-manufacturability.md and the bg-architect agent.

Data sources (best available wins):
  - components/*.csv           → counted as card decks (rows × quantity), the common case.
  - components/cost-manifest.json (optional) → a precise bill of materials for exact costing:
        [ {"type": "cards", "quantity": 54}, {"type": "tokens", "quantity": 30},
          {"type": "board", "quantity": 1} ]
    When present it's authoritative; otherwise the tool estimates from the CSVs and says so.
A box + rulebook are always assumed. Unit costs are ROUGH at-volume figures from the budget — re-verify
with a live manufacturer quote before pricing.

Usage:
    python tools/cost/check_cost.py --game games/beacon
    python tools/cost/check_cost.py --game games/beacon --strict   # exit 1 if over budget

Owned by bg-architect (component scope) with bg-funding (route-to-market economics).
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ALWAYS = ["box", "rulebook"]  # every boxed game has these


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0
    def error(self, msg): self.errors += 1; print(f"  \033[31m[OVER ]\033[0m {msg}")
    def warn(self, msg): self.warns += 1; print(f"  \033[33m[WATCH]\033[0m {msg}")
    def info(self, msg): print(f"  [info ] {msg}")
    def ok(self, msg): print(f"  \033[32m[ ok  ]\033[0m {msg}")


def load_budget(game_dir: Path) -> dict:
    p = game_dir / "component-cost-budget.json"
    if not p.is_file():
        raise SystemExit(f"no component-cost-budget.json in {game_dir} — copy templates/component-cost-budget.json "
                         f"and set it at project start (see knowledge/cost-and-manufacturability.md).")
    return json.loads(p.read_text())


def gather(game_dir: Path):
    """Return (bom: list[{type, quantity}], unique_cards, source_note)."""
    comp = game_dir / "components"
    manifest = comp / "cost-manifest.json"
    if manifest.is_file():
        bom = json.loads(manifest.read_text())
        return bom, None, "cost-manifest.json (authoritative BOM)"
    # estimate from CSVs: each CSV is a card deck
    total_cards, unique_cards = 0, 0
    for cpath in sorted(comp.glob("*.csv")) if comp.is_dir() else []:
        rows = list(csv.DictReader(cpath.open(newline="", encoding="utf-8")))
        unique_cards += len(rows)
        for r in rows:
            try:
                total_cards += max(int((r.get("quantity") or "1").strip()), 0)
            except ValueError:
                total_cards += 1
    bom = [{"type": "cards", "quantity": total_cards}] if total_cards else []
    return bom, unique_cards, "estimated from components/*.csv (add cost-manifest.json for a precise BOM)"


def main():
    ap = argparse.ArgumentParser(description="Gauge component footprint & COGS vs the game's cost budget.")
    ap.add_argument("--game", required=True, type=Path)
    ap.add_argument("--strict", action="store_true", help="exit 1 if over any budget cap")
    args = ap.parse_args()

    budget = load_budget(args.game)
    bom, unique_cards, source = gather(args.game)
    rep = Report()

    print(f"Cost gauge — {args.game}")
    print(f"• source: {source}")

    # fold in the always-present components
    full = list(bom) + [{"type": t, "quantity": 1} for t in ALWAYS]
    types = sorted({b["type"] for b in full})
    total_pieces = sum(int(b.get("quantity", 0)) for b in bom)  # game pieces (exclude box/rulebook from "pieces")

    unit = budget.get("unit_cost_per_type", {})
    default_unit = 0.05
    cogs = 0.0
    print("\n• bill of materials")
    for b in full:
        t, q = b["type"], int(b.get("quantity", 0))
        u = unit.get(t, default_unit)
        line = q * u
        cogs += line
        flag = "" if t in unit else "  (no unit cost in budget → default $%.2f)" % default_unit
        rep.info(f"{t:10} ×{q:<5} @ ${u:.2f} = ${line:6.2f}{flag}")

    retail = budget.get("target_retail_price", 0) or 0
    cogs_target = budget.get("target_cogs_fraction", 0.25) * retail if retail else 0

    print("\n• verdict vs budget")
    # component types
    cap = budget.get("max_component_types")
    if cap is not None:
        (rep.error if len(types) > cap else rep.ok)(f"component types: {len(types)} vs cap {cap}  ({', '.join(types)})")
    # total pieces
    cap = budget.get("max_total_pieces")
    if cap is not None:
        (rep.error if total_pieces > cap else rep.ok)(f"total game pieces: {total_pieces} vs cap {cap}")
    # unique cards
    cap = budget.get("max_unique_cards")
    if cap is not None and unique_cards is not None:
        (rep.error if unique_cards > cap else rep.ok)(f"unique cards: {unique_cards} vs cap {cap}")
    # COGS vs target
    if retail:
        frac = cogs / retail if retail else 0
        msg = (f"est. unit COGS ${cogs:.2f} = {frac*100:.0f}% of ${retail:.0f} retail "
               f"(target ≤ {budget.get('target_cogs_fraction',0.25)*100:.0f}% = ${cogs_target:.2f})")
        (rep.error if cogs > cogs_target else rep.ok)(msg)
    else:
        rep.info(f"est. unit COGS ${cogs:.2f} (no target_retail_price set to compare against)")

    print(f"\n{'=' * 48}\nResult: {rep.errors} over-budget, {rep.warns} watch")
    print("Rough at-volume estimate, pre-freight/pre-tariff — re-verify with a live quote. "
          "Fewer unique TYPES is the biggest lever (see knowledge/cost-and-manufacturability.md).")
    return 1 if (args.strict and rep.errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())
