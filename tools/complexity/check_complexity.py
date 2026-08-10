#!/usr/bin/env python3
"""
check_complexity.py — an objective complexity-drift gauge for a game.

Weight/complexity is ultimately a judgment call, but drift is easier to catch with proxies. This scans
a game's rules, components, and player aid and reports numbers that correlate with rules overhead, then
compares them to the game's complexity-budget.json (set at project start). It's an early-warning gauge
for the bg-elegance agent, not a verdict.

Usage:
    python tools/lint/../complexity/check_complexity.py --game games/beacon
    python tools/complexity/check_complexity.py --game games/beacon --strict   # exit 1 if over budget

Budget file (games/<slug>/complexity-budget.json), all keys optional:
    { "target_weight": 1.8, "max_rulebook_words": 900, "max_keywords": 8,
      "max_component_types": 4, "max_player_aid_lines": 16, "max_exception_words": 8 }
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

EXCEPTION_RE = re.compile(r"\b(except|unless|instead|however|special|exception|edge case|but if|"
                          r"cannot|may not|does not)\b", re.I)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
HEADING_RE = re.compile(r"^#{1,4}\s", re.M)
# Flavour sections are STORY, not rules-teaching load, so they must not count toward the rules
# proxies. A section is dropped if it is fenced by <!-- complexity:ignore-start/end --> markers, or if
# its heading matches this tight allowlist (a whole section = the heading + everything until the next
# heading of the same or higher level). Kept deliberately narrow so it never eats a real rules heading
# (e.g. "Setting up"). Games without such sections (e.g. Beacon) are unaffected — this is a no-op there.
FLAVOUR_HEADING_RE = re.compile(r"^\s*(meet the (agents|cast|crew)|backstor|character bios?|\blore\b)",
                                re.I)


def _strip_flavour(text: str) -> str:
    """Remove flavour sections from the rules text before counting the rules-complexity proxies."""
    out, skip_level, in_marker = [], None, False
    for ln in text.split("\n"):
        if "complexity:ignore-start" in ln:
            in_marker = True; continue
        if "complexity:ignore-end" in ln:
            in_marker = False; continue
        if in_marker:
            continue
        h = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if h:
            level, title = len(h.group(1)), h.group(2)
            if skip_level is not None and level <= skip_level:
                skip_level = None  # flavour section ended; re-evaluate this heading below
            if skip_level is None and FLAVOUR_HEADING_RE.match(title):
                skip_level = level; continue
        if skip_level is not None:
            continue
        out.append(ln)
    return "\n".join(out)


def measure(game: Path) -> dict:
    m = {}
    rules = game / "design" / "rules-draft.md"
    if rules.exists():
        text = _strip_flavour(rules.read_text(encoding="utf-8"))
        words = re.findall(r"\S+", text)
        m["rulebook_words"] = len(words)
        m["rule_sections"] = len(HEADING_RE.findall(text))
        m["exception_words"] = len(EXCEPTION_RE.findall(text))
    # keyword count: prefer the authoritative glossary in design-doc.md (the "## Keywords / glossary"
    # section) — rewards keeping one; count distinct bold terms there. This is the real game-term count,
    # not bolded emphasis.
    ddoc = game / "design" / "design-doc.md"
    if ddoc.exists():
        dtext = ddoc.read_text(encoding="utf-8")
        gm = re.search(r"^#{1,4}\s.*(keyword|glossary).*?$(.*?)(?=^#{1,4}\s|\Z)",
                       dtext, re.I | re.M | re.S)
        if gm:
            terms = {b.strip().lower() for b in BOLD_RE.findall(gm.group(2))}
            m["keywords"] = len(terms)
    comp = game / "components"
    if comp.is_dir():
        # Exclude parked, flag-gated experimental branches (e.g. *-split.csv): they live in
        # components/ but are not part of the ship config, so they must not inflate the budget
        # proxies (component_types / decks / card_count). Games without such files are unaffected.
        csvs = sorted(c for c in comp.glob("*.csv") if not c.name.endswith("-split.csv"))
        m["decks"] = len(csvs)
        types, total = set(), 0
        for c in csvs:
            for row in csv.DictReader(c.open(newline="", encoding="utf-8")):
                types.add((row.get("type") or "").strip().lower())
                try:
                    total += int(row.get("quantity") or 1)
                except ValueError:
                    pass
        m["component_types"] = len({t for t in types if t})
        m["card_count"] = total
    aid = comp / "player-aid.json"
    if aid.exists():
        spec = json.loads(aid.read_text(encoding="utf-8"))
        m["player_aid_lines"] = sum(len(s.get("lines", [])) for s in spec.get("sections", []))
    return m


def main() -> int:
    ap = argparse.ArgumentParser(description="Gauge a game's complexity against its budget.")
    ap.add_argument("--game", required=True, type=Path)
    ap.add_argument("--strict", action="store_true", help="exit 1 if any hard budget is exceeded")
    args = ap.parse_args()

    m = measure(args.game)
    budget_path = args.game / "complexity-budget.json"
    budget = json.loads(budget_path.read_text(encoding="utf-8")) if budget_path.exists() else {}

    print(f"# Complexity gauge — {args.game.name}")
    if budget.get("target_weight"):
        print(f"target weight: {budget['target_weight']} (BGG scale) — a judgment call; the proxies below track drift")
    print("\nproxy                over  value / budget")
    checks = [
        ("rulebook_words",   "max_rulebook_words"),
        ("keywords",         "max_keywords"),
        ("exception_words",  "max_exception_words"),
        ("component_types",  "max_component_types"),
        ("player_aid_lines", "max_player_aid_lines"),
    ]
    over = 0
    for key, bkey in checks:
        val = m.get(key)
        cap = budget.get(bkey)
        if val is None:
            continue
        flag = ""
        if cap is not None and val > cap:
            flag = "⚠"; over += 1
        cap_s = f"/ {cap}" if cap is not None else "(no cap)"
        print(f"  {key:18} {flag:>4}  {val} {cap_s}")
    # informational extras
    for k in ("rule_sections", "decks", "card_count"):
        if k in m:
            print(f"  {k:18}       {m[k]}")
    print()
    if not budget:
        print("No complexity-budget.json found — set one at project start (see templates/complexity-budget.json).")
    elif over:
        print(f"⚠ {over} proxy(ies) over budget — run bg-elegance to simplify or consciously raise the budget.")
    else:
        print("✓ within budget on all capped proxies.")
    return 1 if (args.strict and over) else 0


if __name__ == "__main__":
    raise SystemExit(main())
