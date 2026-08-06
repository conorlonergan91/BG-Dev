#!/usr/bin/env python3
"""
bgg_lookup.py — deterministic reference lookups from BoardGameGeek's public XML API.

Use it in research/ideation to ground comparisons in real data — most usefully, to set a game's
complexity budget "like <game>": it reads the community **weight** (averageweight, 1–5) plus player
count, playtime, mechanisms, and rank straight from BGG, rather than the model recalling them.

    python tools/bgg/bgg_lookup.py --name "Arcs"
    python tools/bgg/bgg_lookup.py --name "The White Castle" --json
    python tools/bgg/bgg_lookup.py --name "Arcs" --suggest-budget          # print a complexity-budget.json seeded from BGG weight
    python tools/bgg/bgg_lookup.py --name "Arcs" --suggest-budget --out games/<slug>/complexity-budget.json

Offline / testing (no network):
    python tools/bgg/bgg_lookup.py --thing-xml tools/bgg/sample_thing.xml

NETWORK: needs outbound HTTPS to boardgamegeek.com. If your environment routes through a policy proxy,
that host must be on the allowlist (some managed sessions block it — you'll get a 403 from the proxy).
Runs fine on a normal machine. Stdlib-only; honours HTTPS_PROXY and the CA bundle env vars.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "https://boardgamegeek.com/xmlapi2"


def _ctx():
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not ca and os.path.exists("/root/.ccr/ca-bundle.crt"):
        ca = "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()


def _get(url: str, tries: int = 4) -> str:
    """GET with retry; BGG returns 202 while a request is queued."""
    ctx = _ctx()
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": "BG-Dev/1.0 (board game studio)"})
        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                if r.status == 202:
                    time.sleep(2 * (i + 1)); continue
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 202:
                time.sleep(2 * (i + 1)); continue
            raise
    raise RuntimeError(f"BGG did not return a result after {tries} tries: {url}")


def search(name: str):
    """Return candidate [(id, name, year)] — exact matches first, else fuzzy."""
    q = urllib.parse.quote(name)
    for exact in ("&exact=1", ""):
        root = ET.fromstring(_get(f"{API}/search?query={q}&type=boardgame{exact}"))
        items = root.findall("item")
        if items:
            out = []
            for it in items:
                nm = it.find("name")
                yr = it.find("yearpublished")
                out.append((it.get("id"), nm.get("value") if nm is not None else "?",
                            yr.get("value") if yr is not None else "?"))
            return out
    return []


def _stat(item, path, attr="value", cast=None):
    el = item.find(path)
    if el is None:
        return None
    v = el.get(attr)
    if cast and v is not None:
        try:
            return cast(v)
        except ValueError:
            return None
    return v


def parse_thing(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)
    item = root.find("item")
    if item is None:
        raise RuntimeError("no <item> in thing response")
    names = [n.get("value") for n in item.findall("name") if n.get("type") == "primary"]
    links = lambda t: [l.get("value") for l in item.findall("link") if l.get("type") == t]
    ranks = {}
    for r in item.findall("statistics/ratings/ranks/rank"):
        ranks[r.get("name")] = r.get("value")
    return {
        "id": item.get("id"),
        "name": names[0] if names else "?",
        "year": _stat(item, "yearpublished"),
        "weight": _stat(item, "statistics/ratings/averageweight", cast=float),
        "rating": _stat(item, "statistics/ratings/average", cast=float),
        "users_rated": _stat(item, "statistics/ratings/usersrated", cast=int),
        "rank_overall": ranks.get("boardgame"),
        "minplayers": _stat(item, "minplayers", cast=int),
        "maxplayers": _stat(item, "maxplayers", cast=int),
        "minplaytime": _stat(item, "minplaytime", cast=int),
        "maxplaytime": _stat(item, "maxplaytime", cast=int),
        "playingtime": _stat(item, "playingtime", cast=int),
        "minage": _stat(item, "minage", cast=int),
        "mechanics": links("boardgamemechanic"),
        "categories": links("boardgamecategory"),
        "designers": links("boardgamedesigner"),
    }


def thing(bgg_id: str) -> dict:
    return parse_thing(_get(f"{API}/thing?id={bgg_id}&stats=1"))


def resolve(name: str) -> dict:
    cands = search(name)
    if not cands:
        raise SystemExit(f"No BGG board game found for {name!r}.")
    # fetch details for up to 5 candidates; pick the most-rated (most likely "the" game). Deterministic.
    best, best_data = None, None
    for cid, _nm, _yr in cands[:5]:
        try:
            d = thing(cid)
        except Exception:
            continue
        if best is None or (d.get("users_rated") or 0) > (best_data.get("users_rated") or 0):
            best, best_data = cid, d
    if best_data is None:
        raise SystemExit(f"Found candidates for {name!r} but could not fetch details.")
    return best_data


def suggest_budget(d: dict) -> dict:
    """Seed a complexity-budget.json from BGG weight. Caps scale with weight and reproduce our
    Beacon (1.8) caps at that point; heavier reference games get roomier budgets."""
    w = d.get("weight") or 2.0
    r = lambda x: int(round(x))
    return {
        "target_weight": round(w, 2),
        "max_rulebook_words": r(300 + w * 330),
        "max_keywords": r(2 + w * 3.3),
        "max_exception_words": r(2 + w * 3.3),
        "max_component_types": r(1 + w * 1.7),
        "max_player_aid_lines": r(6 + w * 5.6),
        "_note": f"Seeded from BoardGameGeek: {d['name']} ({d.get('year')}) — weight {w}. "
                 f"Adjust to taste; this is a starting point, not a mandate.",
    }


def _fmt(d: dict) -> str:
    pl = f"{d['minplayers']}–{d['maxplayers']}" if d.get("minplayers") else "?"
    pt = (f"{d['minplaytime']}–{d['maxplaytime']} min" if d.get("minplaytime") != d.get("maxplaytime")
          else f"{d.get('playingtime')} min")
    return "\n".join([
        f"# {d['name']} ({d.get('year')})   BGG id {d['id']}",
        f"  weight (complexity):  {d.get('weight')}/5   ·   rating {d.get('rating')}   ·   "
        f"rank {d.get('rank_overall')}   ({d.get('users_rated')} ratings)",
        f"  players: {pl}    playtime: {pt}    min age: {d.get('minage')}",
        f"  mechanics:  {', '.join(d.get('mechanics') or []) or '—'}",
        f"  categories: {', '.join(d.get('categories') or []) or '—'}",
        f"  designers:  {', '.join(d.get('designers') or []) or '—'}",
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description="Look up a board game on BoardGameGeek (deterministic).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--name")
    g.add_argument("--id", dest="bgg_id")
    g.add_argument("--thing-xml", type=Path, help="parse a saved thing XML (offline / testing)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--suggest-budget", action="store_true",
                    help="emit a complexity-budget.json seeded from the game's BGG weight")
    ap.add_argument("--out", type=Path, help="with --suggest-budget: write the JSON here")
    args = ap.parse_args()

    if args.thing_xml:
        d = parse_thing(args.thing_xml.read_text(encoding="utf-8"))
    elif args.bgg_id:
        d = thing(args.bgg_id)
    else:
        d = resolve(args.name)

    if args.suggest_budget:
        budget = suggest_budget(d)
        text = json.dumps(budget, indent=2)
        if args.out:
            args.out.write_text(text + "\n", encoding="utf-8")
            print(f"[bgg] wrote {args.out}\n{text}")
        else:
            print(text)
        return 0

    print(json.dumps(d, indent=2) if args.json else _fmt(d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
