#!/usr/bin/env python3
"""
split_decks.py — split (and optionally MERGE) component CSVs into per-deck CSVs.

The 2D pipeline renders one sheet per CSV. Many games want a card CSV carved into
several play-ready piles — e.g. Travel Agents' 8 region+phase ingredient decks (each
= that region+phase's ingredient cards PLUS its matching scoped-event cards, so each
becomes ONE Screentop deck upload). This helper does that split from the source data,
so the piles are always regenerated from the CSVs (never hand-assembled).

    data (CSV[s])  --key col[,col]-->  build/decks/<prefix>_<keyval>.csv  --> build_cards.py

Usage
-----
    # 8 combined ingredient+event decks, grouped by the shared `deck` column:
    python split_decks.py --out build/decks --prefix market --key deck \
        --csv components/ingredients.csv --csv components/events.csv

    # 8 vendor decks by region+phase (type=north.. + phase=day/night -> "north-day"):
    python split_decks.py --out build/decks --prefix vend --key type,phase \
        --csv components/vendors.csv

    # 3 ticket decks by phase (day / night / general):
    python split_decks.py --out build/decks --prefix ticket --key phase \
        --csv components/missions.csv

Notes
-----
* Multiple --csv inputs are concatenated; the output column set is the UNION of all
  inputs' headers (missing fields left blank), so an ingredient row and an event row
  coexist in one deck CSV and each still renders through its own template branch.
* Output filenames are lowercased and slugified. Prints the list of decks + card
  counts (quantity-summed) so a caller / make.sh can echo the grid to the human.
* Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").strip().lower()).strip("-") or "none"


def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ap = argparse.ArgumentParser(description="Split/merge component CSVs into per-deck CSVs.")
    ap.add_argument("--csv", action="append", required=True, type=Path,
                    help="input CSV (repeatable; inputs are concatenated)")
    ap.add_argument("--out", required=True, type=Path, help="output directory for per-deck CSVs")
    ap.add_argument("--key", required=True, help="grouping column(s), comma-separated (joined by '-')")
    ap.add_argument("--prefix", required=True, help="output filename prefix")
    args = ap.parse_args()

    keys = [k.strip() for k in args.key.split(",") if k.strip()]

    # concatenate inputs, union the headers
    rows: list[dict] = []
    fields: list[str] = []
    for p in args.csv:
        for r in load(p):
            rows.append(r)
            for k in r:
                if k not in fields:
                    fields.append(k)

    # group
    groups: dict[str, list[dict]] = {}
    for r in rows:
        gval = "-".join(slugify(r.get(k, "")) for k in keys)
        groups.setdefault(gval, []).append(r)

    args.out.mkdir(parents=True, exist_ok=True)
    made = []
    for gval, grows in sorted(groups.items()):
        out = args.out / f"{args.prefix}_{gval}.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in grows:
                w.writerow({k: r.get(k, "") for k in fields})
        qty = sum(int(r.get("quantity") or 1) for r in grows)
        made.append((out.name, len(grows), qty))
        print(f"[split] {out.name}: {len(grows)} rows, {qty} cards")

    print(f"[split] wrote {len(made)} deck CSV(s) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
