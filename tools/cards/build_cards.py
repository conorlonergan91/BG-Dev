#!/usr/bin/env python3
"""
build_cards.py — the studio's code-native 2D card pipeline.

    data (CSV)  ->  SVG (per card)  ->  PNG / PDF  +  Tabletop Simulator deck sheet

Data is the single source of truth; renders are disposable (regenerate any time).
This is a deliberately small, dependency-light starter — copy/adapt it per game.

Usage
-----
    python build_cards.py --csv example_deck.csv --out out
    python build_cards.py --csv example_deck.csv --out out --formats svg png pdf tts
    python build_cards.py --csv ../../games/<slug>/components/cards.csv --out ../../games/<slug>/build

CSV columns used (extra columns are ignored, missing ones are blank):
    id, name, type, cost, value, effect, quantity, tags, art_note
`quantity` controls how many copies go onto the TTS deck sheet.

Outputs (under --out)
---------------------
    svg/<id>.svg              one vector card each (always produced; no deps needed)
    png/<id>.png              raster cards               (needs cairosvg)
    print/<slug>.pdf          one card face per page     (needs cairosvg)  -- PrintNinja-style
    sheets/<slug>_sheet_N.png deck sheet(s) for Screentop.gg / TTS (needs cairosvg + Pillow)
    sheets/<slug>_back.png    standalone shared card back (needs cairosvg + Pillow)

Formats: svg png pdf tts screentop  (default: svg png screentop)
`screentop` and `tts` produce the same grid sheet + standalone back, with platform import notes.

Specs (see knowledge/manufacturing-specs.md)
--------------------------------------------
    Poker card = 63.5 x 88.9 mm = 750 x 1050 px @ 300 DPI (trimmed).
    Deck sheet: grid up to 10 x 7, <= 4096 x 4096 px, last cell = shared card back.
"""
from __future__ import annotations

import argparse
import base64
import csv
import html
import math
import os
import re
import sys
from pathlib import Path

# Scoped-event icons: the ⦿/✦/⬢/➤/▦ glyphs are TOFU under cairosvg's toy text API (no fall-through to a
# glyph-bearing font), so we DRAW them as SVG shapes keyed off the event `scope` column and keep the
# word label alongside. (bg-access FIX A.) V7-M (bg-infodesign 2026-08): the five-scope framework
# (design-doc §15.2) adds ✦ rival (auto-targets the LEADER) and ▦ board (whole map) alongside the
# shipped self/region/neighbour — `rival`→a spark/spotlight, `board`→the concentric island ring.
SCOPE_SHAPE = {"self": "ring_dot", "region": "hex", "neighbour": "arrow", "island": "island_ring",
               "rival": "spark", "board": "island_ring"}
SCOPE_WORD = {"self": "YOU 自己", "region": "THIS REGION 全區", "neighbour": "NEXT DOOR 鄰區",
              "island": "ISLAND-WIDE 全島", "rival": "THE LEADER 領先者", "board": "EVERYONE 全體"}
_SCOPE_GLYPHS = "⦿✦⬢➤▦"
# The slate that ties the Scheduled-Maintenance island banner to its 停 board marker (bg-access §v6.3.1).
MAINT_SLATE = "#8A8F98"

from themes import (get_theme, resolve_suit, emblem_svg, page_gradient, pick_text_color,
                    phase_style, phase_ribbon_svg, back_style, PHASE_STYLES)

# ---- Card geometry (poker, trimmed, 300 DPI) --------------------------------
CARD_W, CARD_H = 750, 1050          # px @ 300 DPI
MARGIN = 54                         # ~4.5 mm safe margin
TITLE_SIZE, TYPE_SIZE, BODY_SIZE = 50, 28, 34
LINE_H = 44
TITLE_WRAP = 22                     # chars/line before the title wraps (header grows to fit)
TITLE_LINE_H = 56

# ---- V7-M EVENT ICONOGRAPHY (VERB · SCOPE · DURATION) ------------------------
# Every event card is written in three primitives (design-doc §15.2). The card TEXT stays authoritative;
# these icons are the at-a-glance memory anchor. English-only verb labels (the design's own verb names) —
# no unreviewed 繁體 is minted here; the effect text carries the flavour/繁體 the consultant gates. All
# glyphs are DRAWN (no font glyphs) so nothing renders tofu under cairosvg.
VERB_WORD = {
    "rally": "RALLY", "disperse": "DISPERSE", "gift": "GIFT", "pinch": "PINCH", "spoil": "SPOIL",
    "swipe": "SWIPE", "sink": "SINK", "wash": "WASH", "restock": "RESTOCK", "trend": "TREND",
    "block": "BLOCK", "detour": "DETOUR",
}
# family sign (+ grow/gain · − lose/tax · ~ neutral shuffle · × lock) — drawn as an ASCII chip (font-safe)
VERB_SIGN = {
    "rally": "+", "gift": "+", "restock": "+", "trend": "+",
    "disperse": "-", "pinch": "-", "spoil": "-", "swipe": "-",
    "sink": "~", "wash": "~", "block": "x", "detour": "x",
}
DURATION_WORD = {"turn": "TURN", "round": "ROUND", "phase": "PHASE"}


def _sign_chip(sx: float, sy: float, sr: float, s: str, col: str, tfont: str) -> str:
    """A small +/−/~/× sign badge (ASCII only — font-covered, never tofu)."""
    return (f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" stroke="{col}" stroke-width="3"/>'
            f'<text x="{sx}" y="{sy + sr*0.42:.0f}" font-size="{sr*1.35:.0f}" fill="{col}" '
            f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(s)}</text>')


def _hourglass(cx: float, cy: float, r: float, col: str) -> str:
    """A drawn ⏳ hourglass — the DURATION 'lingers until…' marker (never the tofu emoji)."""
    top = f'<path d="M{cx-r} {cy-r} L{cx+r} {cy-r} L{cx} {cy} Z" fill="{col}"/>'
    bot = f'<path d="M{cx} {cy} L{cx+r} {cy+r} L{cx-r} {cy+r} Z" fill="{col}"/>'
    caps = (f'<line x1="{cx-r*1.15}" y1="{cy-r}" x2="{cx+r*1.15}" y2="{cy-r}" stroke="{col}" '
            f'stroke-width="{max(2, r*0.28):.0f}" stroke-linecap="round"/>'
            f'<line x1="{cx-r*1.15}" y1="{cy+r}" x2="{cx+r*1.15}" y2="{cy+r}" stroke="{col}" '
            f'stroke-width="{max(2, r*0.28):.0f}" stroke-linecap="round"/>')
    return top + bot + caps


def _verb_glyph(verb: str, cx: float, cy: float, r: float, col: str, ink: str) -> str:
    """ONE consistent drawn icon per effect VERB (design-doc §15.2a). Grouped by family so a player
    reads them as three intuitions — CROWD (your crowd), PANTRY (your ingredients), STREET (the board).
    Every shape is drawn; the sign chip is added by the caller."""
    def bowl(bx, by, br):
        return (f'<path d="M{bx-br} {by-br*0.1} A {br} {br} 0 0 0 {bx+br} {by-br*0.1} Z" fill="{col}"/>'
                f'<ellipse cx="{bx}" cy="{by-br*0.1}" rx="{br}" ry="{br*0.24}" fill="none" '
                f'stroke="{col}" stroke-width="{max(2, br*0.16):.0f}"/>')
    def deck(dx, dy, dw, dh):
        return (f'<rect x="{dx-dw/2+5}" y="{dy-dh/2+5}" width="{dw}" height="{dh}" rx="5" fill="{col}" opacity="0.4"/>'
                f'<rect x="{dx-dw/2}" y="{dy-dh/2}" width="{dw}" height="{dh}" rx="5" fill="none" '
                f'stroke="{col}" stroke-width="4"/>')
    if verb in ("rally", "disperse"):        # CROWD — a cluster of people; a chevron grows (rally) / drops (disperse)
        s = emblem_svg("crowd", cx, cy, r*0.9, col)
        if verb == "rally":                   # chevron points UP, sitting above the crowd
            tip_y, base_y = cy - r*1.5, cy - r*1.05
        else:                                 # chevron points DOWN, below the crowd
            tip_y, base_y = cy + r*1.5, cy + r*1.05
        chev = (f'<path d="M{cx-r*0.5} {base_y} L{cx} {tip_y} L{cx+r*0.5} {base_y}" fill="none" '
                f'stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        return s + chev
    if verb == "gift":                        # PANTRY gain — a parcel (box + ribbon + bow)
        box = f'<rect x="{cx-r*0.8}" y="{cy-r*0.5}" width="{r*1.6}" height="{r*1.3}" rx="4" fill="{col}"/>'
        rib = (f'<line x1="{cx}" y1="{cy-r*0.5}" x2="{cx}" y2="{cy+r*0.8}" stroke="#ffffff" stroke-width="4"/>'
               f'<line x1="{cx-r*0.8}" y1="{cy-r*0.05}" x2="{cx+r*0.8}" y2="{cy-r*0.05}" stroke="#ffffff" stroke-width="4"/>')
        bow = (f'<circle cx="{cx-r*0.28}" cy="{cy-r*0.62}" r="{r*0.24}" fill="{col}"/>'
               f'<circle cx="{cx+r*0.28}" cy="{cy-r*0.62}" r="{r*0.24}" fill="{col}"/>')
        return box + rib + bow
    if verb in ("pinch", "spoil"):            # PANTRY loss — a bowl; spoil adds a rising 'off' wisp
        s = bowl(cx, cy, r*0.9)
        if verb == "spoil":
            s += (f'<path d="M{cx-r*0.3} {cy-r*0.6} q {r*0.3} -{r*0.4} 0 -{r*0.8}" fill="none" '
                  f'stroke="{col}" stroke-width="3" stroke-linecap="round" opacity="0.8"/>'
                  f'<path d="M{cx+r*0.3} {cy-r*0.6} q {r*0.3} -{r*0.4} 0 -{r*0.8}" fill="none" '
                  f'stroke="{col}" stroke-width="3" stroke-linecap="round" opacity="0.8"/>')
        return s
    if verb == "swipe":                       # PANTRY steal — a hand/arrow taking a chip
        dot = f'<circle cx="{cx+r*0.7}" cy="{cy}" r="{r*0.34}" fill="{col}"/>'
        arr = (f'<path d="M{cx+r*0.5} {cy} h -{r*1.3} m {r*0.5} -{r*0.42} l -{r*0.5} {r*0.42} l {r*0.5} {r*0.42}" '
               f'fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        return dot + arr
    if verb == "sink":                        # STREET — a card pushed to the BOTTOM of the deck
        return deck(cx, cy-r*0.15, r*1.3, r*1.5) + (
            f'<path d="M{cx} {cy-r*0.55} v {r*1.1} m -{r*0.36} -{r*0.36} l {r*0.36} {r*0.36} l {r*0.36} -{r*0.36}" '
            f'fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    if verb == "wash":                        # STREET — a refresh cycle (two curved arrows)
        return (f'<path d="M{cx-r*0.75} {cy} a {r*0.75} {r*0.75} 0 1 1 {r*0.22} {r*0.55}" fill="none" '
                f'stroke="{col}" stroke-width="4" stroke-linecap="round"/>'
                f'<path d="M{cx-r*0.95} {cy-r*0.3} l {r*0.2} {r*0.3} l {r*0.32} -{r*0.22}" fill="none" '
                f'stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    if verb == "restock":                     # STREET — an empty slot refilled (dashed box + up arrow)
        return (f'<rect x="{cx-r*0.7}" y="{cy-r*0.8}" width="{r*1.4}" height="{r*1.6}" rx="4" fill="none" '
                f'stroke="{col}" stroke-width="3" stroke-dasharray="6 4"/>'
                f'<path d="M{cx} {cy+r*0.55} v -{r*1.0} m -{r*0.34} {r*0.34} l {r*0.34} -{r*0.34} l {r*0.34} {r*0.34}" '
                f'fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    if verb == "trend":                       # STREET — going viral (a spark/star with motion ticks)
        return emblem_svg("spark", cx, cy, r*0.95, col) + (
            f'<line x1="{cx+r*0.9}" y1="{cy-r*0.6}" x2="{cx+r*1.25}" y2="{cy-r*0.85}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="{cx+r*0.95}" y1="{cy}" x2="{cx+r*1.35}" y2="{cy}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>')
    if verb == "block":                       # STREET — a prohibition ring (circle + diagonal slash)
        return (f'<circle cx="{cx}" cy="{cy}" r="{r*0.85}" fill="none" stroke="{col}" stroke-width="4"/>'
                f'<line x1="{cx-r*0.6}" y1="{cy+r*0.6}" x2="{cx+r*0.6}" y2="{cy-r*0.6}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
    if verb == "detour":                      # STREET — a bent/forked travel arrow
        return (f'<path d="M{cx-r*0.8} {cy+r*0.6} h {r*0.8} v -{r*0.9} h {r*0.7} m -{r*0.32} -{r*0.34} '
                f'l {r*0.32} {r*0.34} l -{r*0.32} {r*0.34}" fill="none" stroke="{col}" stroke-width="4" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    return emblem_svg("spark", cx, cy, r, col)


def _event_iconography(theme: dict, row: dict, verb: str, scope: str, duration: str,
                       value: str, type_text_y: float, scol: str) -> tuple[str, float]:
    """Build the VERB · SCOPE · DURATION icon strip for an event, plus a header ☀/☾ phase badge.
    Returns (svg, strip_height). Routed through the caller's existing `scope_chip` slot so the SHARED
    render_card_svg template gains NO new line — non-events pass "" and Beacon stays byte-identical.
    All coordinates are absolute, so the header badge lands top-right regardless of string placement."""
    ink, muted, accent = theme["ink"], theme["muted"], theme["accent"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    parts = []

    # --- header ☀/☾ phase badge (top-right) — the region+phase discard-sort cue (§16.7), DRAWN sun/moon
    ps = phase_style(row.get("phase"))
    if ps:
        pcol = ps["frame"]
        pchar = "夜" if ps.get("emblem") == "moon" else ("日" if ps.get("emblem") == "sun" else "通")
        bx, by, br = CARD_W - MARGIN - 34, MARGIN + 34, 42
        parts.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="#ffffff" stroke="{pcol}" stroke-width="4"/>')
        parts.append(emblem_svg(ps.get("emblem", "spark"), bx, by, br*0.42, pcol))
        parts.append(f'<text x="{bx}" y="{by + br*0.86:.0f}" font-size="22" fill="{pcol}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">{esc(pchar)}</text>')

    # --- VERB row: glyph + sign chip + word + magnitude ------------------------------------------------
    y0 = type_text_y + 44
    vx, vr = MARGIN + 30, 26
    parts.append(_verb_glyph(verb, vx, y0, vr, scol, ink))
    parts.append(_sign_chip(vx + vr + 4, y0 - vr, 15, VERB_SIGN.get(verb, "~"), scol, tfont))
    vw = VERB_WORD.get(verb, verb.upper())
    parts.append(f'<text x="{MARGIN + 78}" y="{y0 + 10}" font-size="34" fill="{scol}" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(vw)}</text>')
    # magnitude (show only when >1 — a '1' is the default and adds noise); a '×N' chip after the word
    try:
        mag = int(float(value)) if str(value).strip() else 1
    except ValueError:
        mag = 1
    if mag > 1:
        mtx = MARGIN + 78 + (len(vw) * 22) + 18
        parts.append(_sign_chip(mtx, y0 - 2, 18, f"×{mag}", accent, tfont))

    # --- SCOPE + DURATION row ---------------------------------------------------------------------------
    y1 = y0 + 64
    if scope in SCOPE_SHAPE:
        # 'rival' scope is overloaded: the anti-kingmaking hazards target THE LEADER, but the
        # 'auto-lowest' catch-up boon (t_salvage) targets the LOWEST-scoring rival — so the fixed
        # "THE LEADER 領先者" label contradicts that card's own effect text. Flip it for auto-lowest.
        # English-only here: no unreviewed 繁體 is minted in this renderer (see header note); a
        # reviewed 繁體 for "lowest rival" can be added once the consultant supplies it.
        sword = SCOPE_WORD.get(scope, "")
        if scope == "rival" and "auto-lowest" in (row.get("tags") or ""):
            sword = "THE LOWEST RIVAL"
        parts.append(emblem_svg(SCOPE_SHAPE[scope], MARGIN + 22, y1 - 8, 20, scol, stroke=ink))
        parts.append(f'<text x="{MARGIN + 58}" y="{y1}" font-size="28" fill="{scol}" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(sword)}</text>')
    if duration in DURATION_WORD:
        dx = CARD_W - MARGIN - 190
        _hourglass_r = 16
        parts.append(_hourglass(dx, y1 - 8, _hourglass_r, muted))
        parts.append(f'<text x="{dx + 26}" y="{y1}" font-size="24" fill="{muted}" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(DURATION_WORD[duration])}</text>')
    return "".join(parts), 130.0


def format_target(target: str) -> str:
    """Reformat a machine-readable `target` (e.g. 'region_src:S>=3') into a scannable requirement line.
    Cosmetic ONLY — punctuation/case, never changes meaning (the full prose stays in the effect text)."""
    t = str(target or "").strip()
    if not t:
        return ""
    for a, b in ((">=", " ≥ "), ("<=", " ≤ "), ("==", " = "), (">", " > "), ("<", " < ")):
        t = t.replace(a, b)
    t = t.replace(":", " · ").replace(";", ", ").replace("_", " ")
    return " ".join(t.split()).upper()


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def wrap(text: str, max_chars: int) -> list[str]:
    """Naive word-wrap good enough for a prototype card body."""
    out, line = [], ""
    for word in str(text or "").split():
        if len(line) + len(word) + 1 <= max_chars:
            line = f"{line} {word}".strip()
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


# ---- Vendor card (Travel Agents) --------------------------------------------
# v6.3 TICKETS-ONLY: a vendor gives NO points. Its face is just a two-input PAY row
# (ingredients + the Buzz majority reminder) + a printed DRAW (人氣) attribute + a
# region discount ICON or none. The old GAIN(Prestige/Reputation) + PERK reward
# vectors are RETIRED (vendors don't score; the perk field is gone). Dispatch is
# guarded by `_is_vendor` (needs BOTH `tier` and `recipe`), so decks without
# those columns — Beacon, missions, events, characters — are byte-unchanged.
# V7-M (2026-08): the vendor `buzz_cost` column was DROPPED from data (vestigial —
# the crowd-fight is pure plurality now, no threshold). Detection re-keyed off
# `recipe` (present on every vendor row, absent from Beacon/missions/events/
# characters) so vendors still dispatch to the vendor face. NOTE for the render/
# presentation pass: render_vendor_svg still draws a Buzz badge (from the dropped
# `buzz_cost`) and a DRAW gauge (from the dropped `draw`) — both now empty; that
# pass must remove those two widgets and rework the face for the meeple/plurality
# model. This is the ONLY shared-tool change in the data pass; it fires only for
# rows carrying both `tier` and `recipe` (Travel-Agents vendors), so Beacon renders
# byte-identical.
TIER_FICTION = {"1": "攤 STALL", "2": "小吃 EATERY", "3": "名店 MARQUEE"}
REGION_LABEL = {"north": "NORTH 北", "central": "CENTRAL 中",
                "south": "SOUTH 南", "east": "EAST 東"}


def _is_vendor(row: dict) -> bool:
    return bool(str(row.get("tier", "")).strip()) and bool(str(row.get("recipe", "")).strip())


def _english_name(effect: str) -> str:
    """Vendor `effect` is '繁體 · English Name · flavour…' — pull the English dish name."""
    parts = [p.strip() for p in str(effect or "").split("·")]
    return parts[1] if len(parts) >= 2 else ""


def _perk_visual(perk_code: str, region_suit: dict, theme: dict) -> tuple[str, str]:
    """(emblem, colour) for the perk icon, keyed off the machine perk_code."""
    code = str(perk_code or "").split(":")[0].strip().lower()
    gold = "#C9A227"
    teal = "#1F8A7A"
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")
    slate = "#8A8F98"
    if code in ("icon", "double_icon"):
        return (region_suit["emblem"], region_suit["color"])
    if code == "wild_icon":
        return ("spark", gold)
    if code in ("rep_engine", "rep_court"):
        return ("stamp", teal)
    if code == "buzz_income":
        return ("spark", violet)
    if code == "wild_pantry":
        return ("beam", slate)
    return ("circle", region_suit["color"])


def render_vendor_svg(row: dict, theme: dict, glyph_map: dict | None = None) -> str:
    ink, text, muted, accent = theme["ink"], theme["text"], theme["muted"], theme["accent"]
    radius = theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    region = (row.get("type") or "").strip().lower()
    rsuit = resolve_suit(theme, region)
    rcol, remb = rsuit["color"], rsuit["emblem"]
    # --- day/night treatment (data-driven off the `phase` column) ---
    pstyle = phase_style(row.get("phase"))
    frame_col = pstyle["frame"] if pstyle else ink
    page_cols = pstyle["page"] if pstyle else None
    ribbon = phase_ribbon_svg(pstyle, CARD_W, CARD_H, MARGIN, tfont)
    gold = theme["suits"].get("signature", {}).get("color", "#C9A227")

    # V7-M MEEPLE/SCARCITY MODEL (bg-infodesign render rebuild 2026-08): a vendor's cost is its INGREDIENTS
    # only (the recipe chips) and it is won by MOST FOLLOWERS on the stall (pure plurality — no printed
    # number). Both the old violet Buzz badge (from the dropped `buzz_cost`) and the gold DRAW 人氣 gauge
    # (from the dropped `draw`) are REMOVED — they now draw empty. The face carries: recipe chips + region +
    # tier/apex marker + place/flavour + a textless "won by the biggest crowd" reminder. buzz/draw are not
    # read at all now.
    recipe = [s.strip() for s in (row.get("recipe") or "").split(";") if s.strip()]
    tier = str(row.get("tier", "")).strip()
    icon = str(row.get("icon", "")).strip().upper()  # v6.3: N/C/S/E discount icon, or blank (trophy/drink)
    tags = str(row.get("tags", "")).lower()
    is_apex = ("apex" in tags) or ("trophy" in tags)
    is_drink = "drink" in tags
    strip_hint = ("★ trophy" if is_apex else ("drink" if is_drink else
                  ("discount engine" if icon else "no icon")))

    # --- header band (region colour): Tâi-lô title (wraps) + 繁體 subtitle -------
    # wrap at 16 so a long title breaks BEFORE the top-right tier pill instead of under it
    title_lines = wrap(row.get("name", ""), max_chars=16) or [""]
    han = esc(row.get("hanzi", ""))
    ty0 = MARGIN + 42
    title_tspans = "".join(
        f'<tspan x="{MARGIN}" y="{ty0 + i * TITLE_LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(title_lines))
    han_y = ty0 + (len(title_lines) - 1) * TITLE_LINE_H + 52
    header_h = (han_y + 22) - 26
    header_end = 26 + header_h

    # tier pill (top-right on the band) — CJK glyphs are ~full-width, so size for them
    tier_label = TIER_FICTION.get(tier, f"T{tier}")
    cjk = sum(1 for ch in tier_label if ord(ch) > 0x2E7F)
    pill_w = 34 + cjk * 26 + (len(tier_label) - cjk) * 14
    pill_x = CARD_W - MARGIN - pill_w
    tier_pill = (
        f'<rect x="{pill_x}" y="{MARGIN - 6}" width="{pill_w}" height="46" rx="23" '
        f'fill="#ffffff" opacity="0.9"/>'
        f'<text x="{pill_x + pill_w/2}" y="{MARGIN + 24}" font-size="24" fill="{rcol}" '
        f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(tier_label)}</text>')

    # --- region strip + English dish name (just under the header) ---------------
    strip_y = header_end + 46
    region_strip = (
        emblem_svg(remb, MARGIN + 16, strip_y - 10, 15, rcol) +
        f'<text x="{MARGIN + 44}" y="{strip_y}" font-size="30" fill="{rcol}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="1">'
        f'{esc(REGION_LABEL.get(region, region.upper()))}</text>'
        f'<text x="{CARD_W - MARGIN}" y="{strip_y}" font-size="24" fill="{muted}" '
        f'text-anchor="end" font-family="{bfont}" font-style="italic">{esc(strip_hint)}</text>')
    eng = _english_name(row.get("effect", ""))
    eng_line = ""
    if eng:
        eng_line = (f'<text x="{MARGIN}" y="{strip_y + 40}" font-size="30" fill="{text}" '
                    f'font-family="{bfont}" font-style="italic">{esc(eng)}</text>')
    # place / flavour — the real-world stall location (data `place`), small muted subtitle under the dish
    place = str(row.get("place", "")).strip()
    place_line = ""
    if place:
        for pl in wrap(place, max_chars=42)[:1]:
            place_line = (f'<text x="{MARGIN}" y="{strip_y + 76}" font-size="22" fill="{muted}" '
                          f'font-family="{bfont}" font-style="italic">{esc(pl)}</text>')

    # --- PAY row: ingredient chips only (V7-M: cost = ingredients; the Buzz badge is DROPPED) ---
    # v6.3.1 CD-4: every NIGHT marquee is CROSS-REGION — a chip whose ingredient belongs to a DIFFERENT
    # signature region than this vendor is flagged with an out-of-region "→" badge (and a header
    # CROSS-REGION tag) so the two-region bill parses at a glance, not just as a differently-coloured chip.
    ING_REGION = {"pork": "N", "tea": "C", "seafood": "S", "rice": "E"}   # sugar = common (never foreign)
    card_letter = {"north": "N", "central": "C", "south": "S", "east": "E"}.get(region, "")
    pay_label_y = strip_y + 132
    chips_cy = pay_label_y + 66
    r = 34
    x = MARGIN + 6
    chips = ""
    cross_letters: list[str] = []
    for iid in recipe:
        isuit = resolve_suit(theme, iid) if iid in theme["suits"] else {"color": muted, "emblem": "circle"}
        icol = isuit["color"]
        lab = esc((glyph_map or {}).get(iid, {}).get("label", "")) if glyph_map else ""
        tcol = pick_text_color(icol, dark=ink, light="#ffffff")
        chips += emblem_svg(isuit["emblem"], x + r, chips_cy, r, icol, stroke=ink)
        chips += (f'<text x="{x + r}" y="{chips_cy + r * 0.34}" font-size="30" fill="{tcol}" '
                  f'text-anchor="middle" font-family="{bfont}" font-weight="bold">{lab}</text>')
        foreign = ING_REGION.get(iid)
        if foreign and card_letter and foreign != card_letter:
            cross_letters.append(foreign)
            # a small out-of-region badge riding the chip's top-right: arrow + the region letter
            bx, by = x + 2 * r - 6, chips_cy - r - 4
            chips += (f'<circle cx="{bx}" cy="{by}" r="18" fill="#ffffff" stroke="{icol}" stroke-width="3"/>'
                      + emblem_svg("arrow", bx - 3, by, 7, icol) +
                      f'<text x="{bx + 8}" y="{by + 7}" font-size="20" fill="{icol}" text-anchor="middle" '
                      f'font-family="{tfont}" font-weight="bold">{esc(foreign)}</text>')
        x += 2 * r + 20
    # (V7-M: no "+" and no Buzz badge — the recipe chips ARE the whole cost.)
    # CROSS-REGION tag riding the PAY label — reads the two-region requirement without decoding chip colours
    cross_tag = ""
    if cross_letters:
        seen = "".join(dict.fromkeys(cross_letters))
        ctx = MARGIN + 170
        cross_tag = (
            f'<rect x="{ctx}" y="{pay_label_y - 30}" width="{150 + 22*len(seen)}" height="40" rx="20" '
            f'fill="#ffffff" opacity="0.85" stroke="{accent}" stroke-width="2"/>'
            + emblem_svg("arrow", ctx + 22, pay_label_y - 10, 11, accent) +
            f'<text x="{ctx + 44}" y="{pay_label_y - 2}" font-size="23" fill="{accent}" '
            f'font-family="{tfont}" font-weight="bold" letter-spacing="1">CROSS-REGION →{esc(seen)}</text>')
    pay_block = (
        f'<text x="{MARGIN}" y="{pay_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">PAY 付</text>'
        + cross_tag + chips)

    # --- STATS row (V7-M, ICONS + NUMBERS, no prose): the crowd FLOOR (min_followers) + the VP payoff (vp).
    # The old "WON BY 得標 · a plurality — no set number" line is REMOVED — it is now factually wrong (there
    # IS a min_followers floor). Two labelled stat cells replace it: a crowd-on-a-floor glyph + the floor
    # number (1/2/3 followers you must MEET to claim; a plurality still decides the winner), and a gold VP
    # pip + the payoff number (1–6, what the won stall scores). No sentences — the rulebook + icon sheet
    # carry the tie/大哥/plurality words.
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")
    min_f = str(row.get("min_followers", "")).strip()
    vp = str(row.get("vp", "")).strip()
    stats_label_y = chips_cy + 118
    stats_cy = stats_label_y + 74
    # left cell — CROWD FLOOR: a crowd glyph resting on a drawn floor bar + the number
    fx = MARGIN + 44
    crowd_stat = (
        f'<text x="{MARGIN}" y="{stats_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">CROWD 人潮</text>'
        + emblem_svg("crowd", fx, stats_cy - 4, 32, violet) +
        f'<line x1="{fx-42}" y1="{stats_cy+40}" x2="{fx+42}" y2="{stats_cy+40}" stroke="{violet}" '
        f'stroke-width="7" stroke-linecap="round"/>'
        f'<text x="{fx+96}" y="{stats_cy+24}" font-size="74" fill="{violet}" '
        f'font-family="{tfont}" font-weight="bold">{esc(min_f)}</text>')
    # right cell — VP payoff: a gold pip + the number
    vlx = CARD_W/2 + 40
    vx = vlx + 42
    vp_stat = (
        f'<text x="{vlx}" y="{stats_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">POINTS 分</text>'
        + emblem_svg("spark", vx, stats_cy - 4, 30, gold) +
        f'<text x="{vx+64}" y="{stats_cy+24}" font-size="74" fill="{gold}" '
        f'font-family="{tfont}" font-weight="bold">{esc(vp)}</text>')
    stats_block = crowd_stat + vp_stat

    # --- ICON box: region discount icon, ★ apex trophy, or drink — ICON + a terse tag (no sentence) ------
    icon_label_y = stats_cy + 108
    box_y = icon_label_y + 18
    box_h = CARD_H - MARGIN - box_y
    disc_chip = ""
    if icon:
        isuit = resolve_suit(theme, {"N": "north", "C": "central",
                                     "S": "south", "E": "east"}.get(icon, icon.lower()))
        iemb, icol = isuit["emblem"], isuit["color"]
        icon_tag = f"DISCOUNT 折 · {icon}"
        # a '-1' chip = each held makes this region's ingredients 1 cheaper (the number, not a sentence)
        disc_chip = (f'<circle cx="{MARGIN + 96 + 300}" cy="{box_y + 44}" r="26" fill="#ffffff" '
                     f'stroke="{icol}" stroke-width="4"/>'
                     f'<text x="{MARGIN + 96 + 300}" y="{box_y + 54}" font-size="34" fill="{icol}" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold">-1</text>')
    elif is_apex:
        iemb, icol = "spark", gold
        icon_tag = "★ APEX 名店"
    else:
        iemb, icol = "circle", muted
        icon_tag = "DRINK 飲"
    icon_block = (
        f'<text x="{MARGIN}" y="{icon_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">ICON 圖示</text>'
        f'<rect x="{MARGIN}" y="{box_y}" width="{CARD_W - 2*MARGIN}" height="{box_h}" rx="18" '
        f'fill="#ffffff" opacity="0.45" stroke="{icol}" stroke-width="3"/>'
        + emblem_svg(iemb, MARGIN + 46, box_y + 44, 30, icol) +
        f'<text x="{MARGIN + 96}" y="{box_y + 56}" font-size="34" fill="{text}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(icon_tag)}</text>'
        + disc_chip)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg', page_cols)}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{frame_col}" stroke-width="6"/>
  <rect x="14" y="14" width="{CARD_W-28}" height="{CARD_H-28}" rx="{radius-4}" fill="none" stroke="{frame_col}" stroke-width="2" opacity="0.45"/>
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{rcol}" stroke-width="2" opacity="0.5"/>
  <path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{rcol}"/>
  <text font-size="{TITLE_SIZE}" fill="#ffffff" font-family="{tfont}" font-weight="bold">{title_tspans}</text>
  <text x="{MARGIN}" y="{han_y}" font-size="40" fill="#ffffff" font-family="{tfont}" opacity="0.92">{han}</text>
  {tier_pill}
  {region_strip}
  {eng_line}
  {place_line}
  {pay_block}
  {stats_block}
  {icon_block}
  {ribbon}
</svg>"""


def _is_island_banner(row: dict) -> bool:
    """The Scheduled-Maintenance table-wide event: NOT a ⦿/⬢/➤ scoped card — its own island banner."""
    tags = str(row.get("tags", "")).lower()
    return (str(row.get("kind", "")).strip().lower() == "maintenance"
            or ("island-wide" in tags and "banner" in tags))


def _is_character(row: dict) -> bool:
    """A Travel-Agents character mat: carries ability_code + flaw_code (Beacon/others don't)."""
    return bool(str(row.get("ability_code", "")).strip()) and bool(str(row.get("flaw_code", "")).strip())


def _is_ingredient(row: dict) -> bool:
    """A Travel-Agents PICTORIAL ingredient/food card: carries an `ingredient` column (one of the 5
    palette types) and is tagged 'ingredient'. Beacon and every other game have no `ingredient` column,
    so this branch never fires for them — the change is byte-safe outside Travel Agents."""
    return (bool(str(row.get("ingredient", "")).strip())
            and "ingredient" in str(row.get("tags", "")).lower())


def _is_boundary(row: dict) -> bool:
    """A Travel-Agents deck-clock BOUNDARY card (黃昏 DUSK / 末班車 LAST TRAIN) seeded at the bottom of the
    Booking deck. Marked type=boundary. No other game uses that type → byte-safe elsewhere."""
    return str(row.get("type", "")).strip().lower() == "boundary"


def _hazard_stripes(x: float, y: float, w: float, h: float, a: str, b: str) -> str:
    """A hi-vis maintenance hazard band (diagonal a/b bars) — the 'roadworks' read, drawn (no pattern)."""
    step = 34
    clip = f'<clipPath id="hz"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></clipPath>'
    bars = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{a}"/>']
    i = -1
    while x + i * step < x + w + h:
        x0 = x + i * step
        bars.append(f'<polygon points="{x0},{y+h} {x0+step*0.5},{y+h} '
                    f'{x0+step*0.5+h},{y} {x0+h},{y}" fill="{b}"/>')
        i += 2
    return f'{clip}<g clip-path="url(#hz)">{"".join(bars)}</g>'


def _render_island_banner(row: dict, theme: dict) -> str:
    """Scheduled Maintenance — a distinctly-framed ISLAND-WIDE banner, visibly NOT a ⦿/⬢/➤ scoped card.
    Redundant channels (bg-access §v6.3.1): the island double-ring glyph + the words 'ISLAND-WIDE 全島'
    + a slate header that ties the card to its 停 board marker + a hi-vis works banner + an HSR-closed
    motif. Slate replaces the region suit colour so it never reads as a region-scoped event."""
    ink, text, muted = theme["ink"], theme["text"], theme["muted"]
    radius = theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    slate = MAINT_SLATE
    amber = theme["suits"].get("south", {}).get("color", "#E6A930")
    pstyle = phase_style(row.get("phase"))
    page_cols = pstyle["page"] if pstyle else None
    ribbon = phase_ribbon_svg(pstyle, CARD_W, CARD_H, MARGIN, tfont)

    title_lines = wrap(row.get("name", ""), max_chars=18) or [""]
    han = esc(row.get("hanzi", ""))
    header_h = 132

    # ISLAND-WIDE scope banner (top): the double-ring glyph + the words, on slate — the shape/label channel
    scope_y = 26 + header_h + 40
    scope_banner = (
        emblem_svg("island_ring", MARGIN + 30, scope_y - 8, 24, slate, stroke=ink) +
        f'<text x="{MARGIN + 74}" y="{scope_y}" font-size="34" fill="{slate}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="2">ISLAND-WIDE 全島</text>'
        f'<text x="{CARD_W - MARGIN}" y="{scope_y}" font-size="22" fill="{muted}" text-anchor="end" '
        f'font-family="{bfont}" font-style="italic">a whole-board event</text>')

    # hi-vis works banner
    hz_y = scope_y + 26
    hazard = _hazard_stripes(MARGIN, hz_y, CARD_W - 2 * MARGIN, 30, ink, amber)

    # HSR-closed motif: a short double rail with a red barrier + the 停 roundel (matches the board marker)
    m_cy = hz_y + 150
    rail_x0, rail_x1 = MARGIN + 60, CARD_W - MARGIN - 60
    rails = "".join(
        f'<line x1="{rail_x0}" y1="{m_cy + dy}" x2="{rail_x1}" y2="{m_cy + dy}" stroke="{slate}" '
        f'stroke-width="6" stroke-linecap="round"/>' for dy in (-14, 14))
    ties = "".join(
        f'<line x1="{rail_x0 + 30 + i*70}" y1="{m_cy - 22}" x2="{rail_x0 + 30 + i*70}" y2="{m_cy + 22}" '
        f'stroke="{slate}" stroke-width="4"/>' for i in range(int((rail_x1 - rail_x0 - 30) // 70)))
    barrier = (f'<line x1="{CARD_W/2 - 70}" y1="{m_cy - 46}" x2="{CARD_W/2 + 70}" y2="{m_cy + 46}" '
               f'stroke="{theme["accent"]}" stroke-width="12" stroke-linecap="round"/>')
    stop_roundel = (
        f'<circle cx="{CARD_W/2}" cy="{m_cy - 96}" r="40" fill="{slate}" stroke="{ink}" stroke-width="3"/>'
        f'<text x="{CARD_W/2}" y="{m_cy - 84}" font-size="42" fill="#ffffff" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">停</text>'
        f'<text x="{CARD_W/2}" y="{m_cy + 78}" font-size="26" fill="{slate}" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="1">HSR CLOSED · 高鐵停駛</text>')

    # body: drop the now-redundant "ISLAND-WIDE (not a scoped event — its own banner)." lead sentence
    eff = re.sub(r'^\s*ISLAND-WIDE[^.]*\.\s*', '', str(row.get("effect", "")))
    body_y = m_cy + 130
    body_tspans = "".join(f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
                          for i, l in enumerate(wrap(eff, max_chars=34)))
    title_tspans = "".join(
        f'<tspan x="{MARGIN}" y="{MARGIN + 46 + i * TITLE_LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(title_lines))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg', page_cols)}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{slate}" stroke-width="8"/>
  <rect x="18" y="18" width="{CARD_W-36}" height="{CARD_H-36}" rx="{radius-6}" fill="none" stroke="{slate}" stroke-width="2" opacity="0.5"/>
  <path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{slate}"/>
  <text font-size="{TITLE_SIZE}" fill="#ffffff" font-family="{tfont}" font-weight="bold">{title_tspans}</text>
  <text x="{CARD_W - MARGIN}" y="{MARGIN + 46}" font-size="40" fill="#ffffff" text-anchor="end" font-family="{tfont}" opacity="0.92">{han}</text>
  {scope_banner}
  {hazard}
  {rails}{ties}{barrier}{stop_roundel}
  <text x="{MARGIN}" y="{body_y}" font-size="{BODY_SIZE}" fill="{text}" font-family="{bfont}">{body_tspans}</text>
  {ribbon}
</svg>"""


def _render_character_svg(row: dict, theme: dict) -> str:
    """A Travel-Agents character mat rendered as a card: name (Tâi-lô + 繁體) + a public ABILITY block and
    FLAW block read off the clean `ability`/`flaw` columns (NOT the sim-annotated `effect`). 里長伯's
    home-region-discount + away-tax kit gets its two mat icons (bg-infodesign item 3)."""
    ink, text, muted, accent = theme["ink"], theme["text"], theme["muted"], theme["accent"]
    radius = theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    gold = theme["suits"].get("signature", {}).get("color", "#C9A227")
    teal = theme["suits"].get("central", {}).get("color", "#1F8A7A")
    vermilion = theme["suits"].get("north", {}).get("color", "#D64545")

    title_lines = wrap(row.get("name", ""), max_chars=20) or [""]
    han = esc(row.get("hanzi", ""))
    header_h = 104 + (len(title_lines) - 1) * TITLE_LINE_H
    header_end = 26 + header_h
    title_tspans = "".join(
        f'<tspan x="{MARGIN}" y="{MARGIN + 44 + i * TITLE_LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(title_lines))

    ability = str(row.get("ability", "")).strip()
    flaw = str(row.get("flaw", "")).strip()
    ability_code = str(row.get("ability_code", "")).strip().lower()
    flaw_code = str(row.get("flaw_code", "")).strip().lower()

    def kit_icon(cx: float, cy: float, code: str, side: str) -> str:
        """A drawn mat-icon for the kit's key codes; home/away get bespoke glyphs (item 3)."""
        if code == "discount_home":   # a house + a −1 chip → 'cheaper on home turf'
            return (emblem_svg("home", cx, cy, 30, teal, stroke=ink) +
                    f'<circle cx="{cx+30}" cy="{cy+26}" r="20" fill="#ffffff" stroke="{teal}" stroke-width="3"/>'
                    f'<text x="{cx+30}" y="{cy+33}" font-size="26" fill="{teal}" text-anchor="middle" '
                    f'font-family="{tfont}" font-weight="bold">-1</text>')
        if code == "away_tax":        # an out-of-home arrow + a +1 chip → 'pay more off your patch'
            return (emblem_svg("arrow", cx, cy, 28, vermilion, stroke=ink) +
                    f'<circle cx="{cx+30}" cy="{cy+26}" r="20" fill="#ffffff" stroke="{vermilion}" stroke-width="3"/>'
                    f'<text x="{cx+30}" y="{cy+33}" font-size="26" fill="{vermilion}" text-anchor="middle" '
                    f'font-family="{tfont}" font-weight="bold">+1</text>')
        emb = {"self": "ring_dot"}.get(code, "spark")
        return emblem_svg(emb, cx, cy, 28, gold if side == "ability" else muted, stroke=ink)

    def block(y0: float, label: str, code: str, txt: str, col: str, side: str) -> tuple[str, float]:
        lines = wrap(txt, max_chars=30)
        bh = 78 + len(lines) * 40
        icon = kit_icon(MARGIN + 52, y0 + 60, code, side)
        tspans = "".join(f'<tspan x="{MARGIN + 116}" dy="{0 if i == 0 else 40}">{esc(l)}</tspan>'
                         for i, l in enumerate(lines))
        s = (f'<rect x="{MARGIN}" y="{y0}" width="{CARD_W - 2*MARGIN}" height="{bh}" rx="18" '
             f'fill="#ffffff" opacity="0.5" stroke="{col}" stroke-width="3"/>'
             f'<text x="{MARGIN + 20}" y="{y0 + 34}" font-size="26" fill="{col}" '
             f'font-family="{tfont}" font-weight="bold" letter-spacing="2">{esc(label)}</text>'
             + icon +
             f'<text x="{MARGIN + 116}" y="{y0 + 70}" font-size="30" fill="{text}" '
             f'font-family="{bfont}">{tspans}</text>')
        return s, y0 + bh + 28

    y = header_end + 40
    ability_block, y = block(y, "ABILITY 能力", ability_code, ability, teal, "ability")
    flaw_block, y = block(y, "FLAW 弱點", flaw_code, flaw, vermilion, "flaw")
    setup_note = ""
    if ability_code == "discount_home":
        setup_note = (f'<text x="{MARGIN}" y="{y + 6}" font-size="24" fill="{muted}" '
                      f'font-family="{bfont}" font-style="italic">Setup: pick ONE home region (open).</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg')}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{gold}" stroke-width="2" opacity="0.5"/>
  <path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{gold}"/>
  <text font-size="{TITLE_SIZE}" fill="#ffffff" font-family="{tfont}" font-weight="bold">{title_tspans}</text>
  <text x="{CARD_W - MARGIN}" y="{MARGIN + 44}" font-size="40" fill="#ffffff" text-anchor="end" font-family="{tfont}" opacity="0.92">{han}</text>
  {ability_block}
  {flaw_block}
  {setup_note}
</svg>"""


# TA-only art-mock embed for ingredient cards. Set in main() from the CSV location; a module global so
# the Beacon-shared render_card_svg / _render_ingredient_svg signatures stay untouched (Beacon cards
# never hit _is_ingredient, so this path is dead for every non-TA deck → byte-identical output).
_ING_MOCKUPS_DIR = None


def _embed_fig_png(fig_id, x, y, w, h, rx=20):
    """If `<_ING_MOCKUPS_DIR>/<fig_id>.png` exists, return an SVG <image> for it — a base64 **data URI**
    (so the render stays self-contained through cairosvg→PNG; a file-path href would not survive
    rasterisation), clipped to a rounded rect and sized to the slot with preserveAspectRatio meet (never
    crops). Returns None when there is no mock-up on disk, so the caller keeps the byte-identical
    placeholder — a mock-up-free ingredient card renders exactly as before."""
    if not _ING_MOCKUPS_DIR:
        return None
    p = Path(_ING_MOCKUPS_DIR) / f"{fig_id}.png"
    if not p.is_file():
        return None
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    cid = "ingclip-" + re.sub(r'[^A-Za-z0-9]+', '-', fig_id).strip('-').lower()
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<image href="data:image/png;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid meet" clip-path="url(#{cid})"/>')


def _render_ingredient_svg(row: dict, theme: dict) -> str:
    """A PICTORIAL ingredient/food card (Travel Agents, V7 language-agnostic).

    The card is keyed off the `ingredient` column — NOT the region `type` — so its big picture-glyph is
    the SAME shape + colour a player sees in the vendor's recipe chip and on the token key (pork = red hex,
    tea = teal triangle, seafood = amber square, rice = indigo circle, sugar = caramel beam). That closes
    the match-your-hand-to-the-recipe loop at a glance. Distinguishable by PICTURE + SHAPE, never colour
    alone (bg-access): a large drawn ingredient emblem fills a framed art placeholder + a [FIG-ING-<id>]
    brief for the human illustrator. 繁體 + English name are the CULTURAL name (kept, per the sensitivity
    rails); nothing MECHANICAL relies on reading CJK."""
    ink, text, muted, accent, radius = (theme["ink"], theme["text"], theme["muted"],
                                        theme["accent"], theme["radius"])
    tfont, bfont = theme["title_font"], theme["body_font"]
    ing = str(row.get("ingredient", "")).strip().lower()
    isuit = resolve_suit(theme, ing) if ing in theme["suits"] else theme["suits"]["_default"]
    scol, semb = isuit["color"], isuit["emblem"]
    pstyle = phase_style(row.get("phase"))
    frame_col = pstyle["frame"] if pstyle else ink
    page_cols = pstyle["page"] if pstyle else None
    ribbon = phase_ribbon_svg(pstyle, CARD_W, CARD_H, MARGIN, tfont)

    han = str(row.get("hanzi", "")).strip() or str(row.get("name", "")).strip()
    name_full = str(row.get("name", "")).strip()
    # English part of "豬肉 Pork" → "Pork" (strip a leading CJK run + space)
    en = re.sub(r'^[^\x00-\x7f]+\s*', '', name_full).strip() or name_full
    region = str(row.get("region", "")).strip().lower()
    # map the deck-region LETTER (n/c/s/e) → the region suit (colour + emblem) + its 繁體 glyph, so REGION
    # is dual-coded on the card, not just a letter. A market card must sort to its region+phase discard
    # pile at a glance (§16.7) — region here, phase in the ☀/☾ badge below.
    region_key = {"n": "north", "c": "central", "s": "south", "e": "east"}.get(region, region)
    rsuit = resolve_suit(theme, region_key) if region_key in theme["suits"] else {"color": scol, "emblem": "circle"}
    rcol, remb = rsuit["color"], rsuit["emblem"]
    region_char = {"north": "北", "central": "中", "south": "南", "east": "東"}.get(region_key, "")
    tcol_head = pick_text_color(scol, dark=ink, light="#ffffff")

    # header band (grows nothing — single line): the ingredient's 繁體 name (region+phase live in the sort
    # tab below the band, so the band stays clean).
    header_h = 118
    header_end = 26 + header_h
    head = (f'<path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} '
            f'h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} '
            f'v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{scol}"/>'
            f'<text x="{MARGIN}" y="{MARGIN+60}" font-size="60" fill="{tcol_head}" '
            f'font-family="{tfont}" font-weight="bold">{esc(han)}</text>')

    # --- REGION + PHASE sort tab (top-right, straddling the header edge): two dual-coded roundels — REGION
    # (region colour + region emblem + 繁體 glyph) and PHASE (☀ day / ☾ night, DRAWN sun/moon — never a
    # font emoji → no tofu — + 日/夜). Together they say "this card's discard pile" at a glance (§16.7),
    # dual-coded by SHAPE (emblem + sun/moon), not colour alone (bg-access redundant-encoding). ---
    tab_cy = 26 + header_h/2
    tab_r = 40
    ph_cx = CARD_W - MARGIN - tab_r
    rg_cx = ph_cx - (2*tab_r + 14)
    phc = pstyle["frame"] if pstyle else ink
    phe = pstyle.get("emblem", "spark") if pstyle else "spark"
    phch = "夜" if phe == "moon" else ("日" if phe == "sun" else "通")
    sort_tab = (
        f'<circle cx="{rg_cx}" cy="{tab_cy}" r="{tab_r}" fill="#ffffff" stroke="{rcol}" stroke-width="4"/>'
        + emblem_svg(remb, rg_cx, tab_cy - 8, tab_r*0.42, rcol, stroke=ink) +
        f'<text x="{rg_cx}" y="{tab_cy + tab_r*0.82:.0f}" font-size="24" fill="{rcol}" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">{esc(region_char)}</text>'
        f'<circle cx="{ph_cx}" cy="{tab_cy}" r="{tab_r}" fill="#ffffff" stroke="{phc}" stroke-width="4"/>'
        + emblem_svg(phe, ph_cx, tab_cy - 8, tab_r*0.40, phc) +
        f'<text x="{ph_cx}" y="{tab_cy + tab_r*0.82:.0f}" font-size="24" fill="{phc}" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">{esc(phch)}</text>')
    head += sort_tab

    # PICTURE plate — a framed placeholder with the big ingredient emblem (the shape carries WHICH
    # ingredient) + the illustrator brief code. This is the pictorial payload of the card.
    px, py = MARGIN, header_end + 24
    pw, ph = CARD_W - 2*MARGIN, 560
    pcx, pcy = px + pw/2, py + ph/2 - 30
    corners = "".join(
        f'<path d="M{cxx} {cyy+dy*34} L{cxx} {cyy} L{cxx+dx*34} {cyy}" fill="none" '
        f'stroke="{scol}" stroke-width="4" opacity="0.75"/>'
        for (cxx, cyy, dx, dy) in [(px+18, py+18, 1, 1), (px+pw-18, py+18, -1, 1),
                                   (px+18, py+ph-18, 1, -1), (px+pw-18, py+ph-18, -1, -1)])
    fig = str(row.get("ingredient", "")).strip().lower()
    _mock = _embed_fig_png(f"FIG-ING-{fig}", px, py, pw, ph)
    if _mock:
        # a real illustration mock-up on disk → embed it (self-contained data URI) inside a solid frame
        plate = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="#ffffff" opacity="0.55"/>'
                 + _mock
                 + f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="none" '
                   f'stroke="{scol}" stroke-width="3"/>')
    else:
        plate = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="#ffffff" opacity="0.45" '
                 f'stroke="{scol}" stroke-width="3" stroke-dasharray="14 9"/>' + corners
                 + f'<circle cx="{pcx}" cy="{pcy}" r="150" fill="{scol}" opacity="0.14"/>'
                 + emblem_svg(semb, pcx, pcy, 118, scol, stroke=ink)
                 + f'<text x="{pcx}" y="{py+42}" font-size="22" fill="{muted}" text-anchor="middle" '
                   f'font-family="{bfont}" font-style="italic">illustration placeholder · human-illustrated (no AI final art)</text>'
                 + f'<rect x="{pcx-150}" y="{py+ph-64}" width="300" height="42" rx="21" fill="{ink}"/>'
                 + f'<text x="{pcx}" y="{py+ph-35}" font-size="24" fill="#ffffff" text-anchor="middle" '
                   f'font-family="{tfont}" font-weight="bold" letter-spacing="1">[FIG-ING-{esc(fig)}]</text>')

    # foot: big English name (the at-a-glance label) + a terse "into your Larder" line
    fy = py + ph + 64
    foot = (f'<text x="{MARGIN}" y="{fy}" font-size="52" fill="{scol}" '
            f'font-family="{tfont}" font-weight="bold">{esc(en)}</text>'
            f'<text x="{MARGIN}" y="{fy+44}" font-size="28" fill="{text}" '
            f'font-family="{bfont}">Take 1 into your Larder.</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg', page_cols)}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{frame_col}" stroke-width="6"/>
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{scol}" stroke-width="2" opacity="0.5"/>
  {head}
  {plate}
  {foot}
  {ribbon}
</svg>"""


def _render_boundary_svg(row: dict, theme: dict) -> str:
    """A self-announcing deck-clock BOUNDARY card: 黃昏 DUSK (bottom of the DAY Booking deck → flip to
    night) or 末班車 LAST TRAIN (bottom of the NIGHT deck → finish the round, end). When a refill turns it
    up, the clock announces itself — no one counts cards. Big drawn sun→moon (DUSK) / moon (LAST TRAIN)
    motif so it reads across the table and is dual-coded (shape + word + colour). Beacon has no boundary
    cards; TA-only."""
    ink, text, muted, radius = theme["ink"], theme["text"], theme["muted"], theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    day = PHASE_STYLES["day"]
    night = PHASE_STYLES["night"]
    phase = str(row.get("phase", "")).strip().lower()
    is_last = (phase == "night")
    ground = night["page"] if is_last else day["page"]
    band = night["tag_fill"] if is_last else day["tag_fill"]
    frame_col = night["frame"] if is_last else day["frame"]
    han = str(row.get("hanzi", "")).strip() or ("末班車" if is_last else "黃昏")
    en = "LAST TRAIN" if is_last else "DUSK"
    sub = ("The night's last tours are gone — finish the round, then the game ends."
           if is_last else "The day's tours have booked out — flip the board to night.")
    cx = CARD_W / 2
    # central motif: DUSK = sun handing to moon; LAST TRAIN = a lone moon over a rail
    if is_last:
        motif = (emblem_svg("moon", cx, 470, 120, frame_col)
                 + f'<line x1="{MARGIN+30}" y1="640" x2="{CARD_W-MARGIN-30}" y2="640" '
                   f'stroke="{ink}" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'
                 + f'<line x1="{MARGIN+30}" y1="662" x2="{CARD_W-MARGIN-30}" y2="662" '
                   f'stroke="{ink}" stroke-width="8" stroke-linecap="round" opacity="0.35" stroke-dasharray="30 26"/>')
    else:
        motif = (emblem_svg("sun", cx - 130, 470, 96, day["frame"])
                 + f'<path d="M{cx-30} 470 h 60" stroke="{muted}" stroke-width="7" '
                   f'stroke-linecap="round"/><path d="M{cx+18} 452 l 24 18 l -24 18" fill="none" '
                   f'stroke="{muted}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
                 + emblem_svg("moon", cx + 130, 470, 96, night["frame"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg', ground)}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{frame_col}" stroke-width="8"/>
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{frame_col}" stroke-width="3" stroke-dasharray="16 10" opacity="0.7"/>
  <rect x="26" y="120" width="{CARD_W-52}" height="150" fill="{band}"/>
  <text x="{cx}" y="228" font-size="120" fill="#ffffff" text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="4">{esc(han)}</text>
  {motif}
  <text x="{cx}" y="770" font-size="64" fill="{frame_col}" text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="6">{esc(en)}</text>
  <text x="{cx}" y="840" font-size="30" fill="{text}" text-anchor="middle" font-family="{bfont}">{esc("THE CLOCK · the Booking deck")}</text>
  <text x="{cx}" y="928" font-size="30" fill="{ink}" text-anchor="middle" font-family="{bfont}"><tspan x="{cx}" dy="0">{esc(sub.split(' — ')[0] if ' — ' in sub else sub)}</tspan></text>
  <text x="{cx}" y="966" font-size="30" fill="{ink}" text-anchor="middle" font-family="{bfont}">{esc(sub.split(' — ')[1] if ' — ' in sub else '')}</text>
</svg>"""


def render_card_svg(row: dict, theme: dict, glyph_map: dict | None = None) -> str:
    if _is_vendor(row):
        return render_vendor_svg(row, theme, glyph_map)
    if _is_boundary(row):
        return _render_boundary_svg(row, theme)
    if _is_ingredient(row):
        return _render_ingredient_svg(row, theme)
    if _is_island_banner(row):
        return _render_island_banner(row, theme)
    if _is_character(row):
        return _render_character_svg(row, theme)
    ctype = (row.get("type") or "").strip()
    suit = resolve_suit(theme, ctype)
    scol = suit["color"]
    ink, text, muted, accent, radius = theme["ink"], theme["text"], theme["muted"], theme["accent"], theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    # --- day/night treatment (data-driven off the `phase` column) ---
    pstyle = phase_style(row.get("phase"))
    frame_col = pstyle["frame"] if pstyle else ink
    page_cols = pstyle["page"] if pstyle else None
    ribbon = phase_ribbon_svg(pstyle, CARD_W, CARD_H, MARGIN, tfont)
    # inner phase-frame line only when there IS a phase → phase-less decks (characters, other games)
    # stay byte-identical to before this recolour.
    inner_frame = (f'<rect x="14" y="14" width="{CARD_W-28}" height="{CARD_H-28}" rx="{radius-4}" '
                   f'fill="none" stroke="{frame_col}" stroke-width="2" opacity="0.45"/>') if pstyle else ""
    cost = str(row.get("cost", "")).strip()
    value = str(row.get("value", "")).strip()
    recipe = (row.get("recipe") or "").strip()          # dishes: semicolon-separated ingredient ids
    target = (row.get("target") or "").strip()          # assignments: machine-readable win condition
    # TA-only V7-M event gate: events.csv gained a `verb` column (rally/pinch/gift/…) plus `target`
    # (a verb PARAMETER, e.g. block→draw) and a magnitude `value`. Those two columns collide with the
    # generic objective/value read (a `target` would render an event as an assignment card; a `value`
    # would stamp a stray VP numeral). An event is any row carrying a `verb` — a column NO other deck
    # (Beacon ships/signals, TA bookings/vendors/ingredients/characters) has — so this fires ONLY for
    # TA scoped events and leaves every other deck byte-identical. It keeps events rendering exactly as
    # they did before this data pass (plain effect card + scope chip); the verb/scope/duration/target
    # ICONOGRAPHY is a SEPARATE presentation pass (see the render-pass flags in the dev handoff).
    is_event = bool((row.get("verb") or "").strip())
    is_objective = bool(target) and not is_event        # assignment-style: value is a completion bonus
    # V7-M (bg-infodesign 2026-08): events now SHOW their magnitude on the VERB glyph (the icon strip
    # below), so the earlier blanket `value=""` suppression is GONE — we keep `value` readable for the
    # strip. The generic bottom VP-pip / top index is a SCORING widget, wrong for an event, so it is
    # guarded off with `not is_event` at its render site (below). Beacon has no `verb` → is_event False →
    # that guard is a no-op there → byte-identical.

    # --- title: wraps; the header band GROWS to fit, so single-line titles are pixel-unchanged ---
    title_lines = wrap(row.get("name", ""), max_chars=TITLE_WRAP) or [""]
    extra = (len(title_lines) - 1) * TITLE_LINE_H
    header_h = 104 + extra
    header_end = 26 + header_h
    title_tspans = "".join(
        f'<tspan x="{MARGIN}" y="{MARGIN + 44 + i * TITLE_LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(title_lines)
    )

    # cost badge (top-right, on the header band)
    cost_badge = ""
    if cost:
        cx, cy, r = CARD_W - MARGIN - 6, MARGIN + 24, 46
        cost_badge = (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{scol}" stroke-width="6"/>'
            f'<text x="{cx}" y="{cy + 16}" font-size="48" fill="{scol}" text-anchor="middle" '
            f'font-family="{tfont}" font-weight="bold">{esc(cost)}</text>'
        )
    # value: a large top-right "index" numeral (playing-card style — value leads the read), plus a pip
    # row + numeral at the bottom. Blank `value` => no value; value 0 is REAL and must render (a
    # zero-strength Signal is Beacon's Dark Lantern). OBJECTIVE cards (assignments) instead demote the
    # bonus to a "+N VP" footer chip so the win-condition — not a constant number — leads.
    value_index = ""
    value_row = ""
    if value and not is_event:
        try:
            vn = int(float(value))
        except ValueError:
            vn = 0
        if is_objective:
            # value footer chip (bottom-left), no top index, no pip row. Travel Agents' Tour Tickets score
            # in the game's own "value" language (成團 win pile → +value); other games keep the generic VP.
            bonus_word = "value" if ctype.lower() in ("mission", "booking") else "VP"
            chw, chh = (224 if bonus_word == "value" else 168), 60
            cx0, cy0 = MARGIN, CARD_H - MARGIN - 60
            value_row = (
                f'<rect x="{cx0}" y="{cy0}" width="{chw}" height="{chh}" rx="{chh/2}" fill="{scol}"/>'
                f'<text x="{cx0 + chw/2}" y="{cy0 + chh*0.68}" font-size="38" fill="#ffffff" '
                f'text-anchor="middle" font-family="{tfont}" font-weight="bold">+{esc(value)} {bonus_word}</text>')
        else:
            # top-right index — only when no cost badge and a single-line title share the corner cleanly
            if not cost and len(title_lines) == 1:
                vix, viy = CARD_W - MARGIN - 6, MARGIN + 54
                value_index = (f'<text x="{vix}" y="{viy}" font-size="62" fill="#ffffff" text-anchor="end" '
                               f'font-family="{tfont}" font-weight="bold">{esc(value)}</text>')
            if vn > 0:
                pips = "".join(emblem_svg(suit["emblem"], MARGIN + 22 + i * 46, CARD_H - MARGIN - 22, 16, scol)
                                for i in range(min(vn, 6)))
            else:
                pips = (f'<circle cx="{MARGIN + 22}" cy="{CARD_H - MARGIN - 22}" r="15" fill="none" '
                        f'stroke="{scol}" stroke-width="4" opacity="0.7"/>')
            value_row = (pips +
                f'<text x="{CARD_W - MARGIN}" y="{CARD_H - MARGIN - 6}" font-size="52" fill="{scol}" '
                f'text-anchor="end" font-family="{tfont}" font-weight="bold">{vn}</text>')

    # --- type line with emblem (rides just below the header band) ---
    type_emblem_cy = header_end + 20
    type_text_y = header_end + 30
    # Travel Agents renamed its objective spine "Tour Ticket" (canon); the CSV type stays "mission" so
    # sim/logic are unchanged — only the printed label is remapped. Other games print their type verbatim.
    type_label = "TOUR TICKET" if ctype.lower() == "mission" else ctype.upper()
    type_block = (
        emblem_svg(suit['emblem'], MARGIN + 16, type_emblem_cy, 15, scol) +
        f'<text x="{MARGIN+44}" y="{type_text_y}" font-size="{TYPE_SIZE}" fill="{muted}" '
        f'font-family="{tfont}" font-style="italic" letter-spacing="2">{esc(type_label)}</text>')

    # --- recipe chip-row (dishes only): one disc per ingredient = region colour + 繁體 glyph, matching
    # the tokens exactly. The bridge from a token in hand to the dish that needs it. Needs a `recipe`
    # column AND a glyph map (else skipped — so assignments and Beacon are unaffected). ---
    chips = ""
    chip_h = 0
    if recipe and glyph_map:
        ids = [s.strip() for s in recipe.split(";") if s.strip()]
        chip_cy = type_text_y + 54
        r = 26
        x = MARGIN
        for iid in ids:
            g = glyph_map.get(iid, {})
            gcol = resolve_suit(theme, iid)["color"] if iid in theme["suits"] else (g.get("color") or muted)
            gtxt = pick_text_color(gcol, dark=ink, light="#ffffff")
            chips += (
                f'<circle cx="{x + r}" cy="{chip_cy}" r="{r}" fill="{gcol}" stroke="{ink}" stroke-width="3"/>'
                f'<text x="{x + r}" y="{chip_cy + r*0.36}" font-size="30" fill="{gtxt}" text-anchor="middle" '
                f'font-family="{bfont}" font-weight="bold">{esc(g.get("label", ""))}</text>')
            x += 84
        chip_h = 84

    # --- scoped-event badge (drawn shape + word) — replaces the tofu ⦿/✦/⬢/➤/▦ glyph (bg-access FIX A) ---
    # V7-M events get the full VERB · SCOPE · DURATION iconography + magnitude + a ☀/☾ header phase badge,
    # all built by _event_iconography and routed through THIS existing `scope_chip` slot so the SHARED
    # template gains no new line (Beacon stays byte-identical). Non-events keep the plain scope chip.
    scope = (row.get("scope") or "").strip().lower()
    scope_chip = ""
    eff_text = row.get("effect", "")
    if is_event:
        verb = (row.get("verb") or "").strip().lower()
        duration = (row.get("duration") or "").strip().lower()
        scope_chip, ev_h = _event_iconography(theme, row, verb, scope, duration, value,
                                              type_text_y, scol)
        eff_text = re.sub(r'^\s*[' + _SCOPE_GLYPHS + r'][^·]*·\s*', '', eff_text)
        eff_text = re.sub(r'^\s*[' + _SCOPE_GLYPHS + r']\s*', '', eff_text)
        chip_h = max(chip_h, ev_h)
    elif scope in SCOPE_SHAPE and not (recipe and glyph_map):
        sy = type_text_y + 56
        scope_chip = (
            emblem_svg(SCOPE_SHAPE[scope], MARGIN + 24, sy - 8, 22, scol, stroke=ink) +
            f'<text x="{MARGIN + 64}" y="{sy}" font-size="30" fill="{scol}" '
            f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(SCOPE_WORD[scope])}</text>')
        # strip the leading "⬢ THIS REGION · " (glyph + its scope words + separator) so the body prose
        # keeps its meaning without the tofu glyph; fall back to stripping a bare leading glyph.
        eff_text = re.sub(r'^\s*[' + _SCOPE_GLYPHS + r'][^·]*·\s*', '', eff_text)
        eff_text = re.sub(r'^\s*[' + _SCOPE_GLYPHS + r']\s*', '', eff_text)
        chip_h = max(chip_h, 64)

    # --- body: for objectives a bold requirement line leads, then the flavour effect ---
    body_y = type_text_y + 104 + chip_h
    if is_objective:
        req_lines = wrap(format_target(target), max_chars=28)
        req_tspans = "".join(f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
                             for i, l in enumerate(req_lines))
        req_block = (f'<text x="{MARGIN}" y="{body_y}" font-size="{BODY_SIZE}" fill="{ink}" '
                     f'font-family="{bfont}" font-weight="bold">{req_tspans}</text>')
        eff_y = body_y + max(1, len(req_lines)) * LINE_H + 26
        eff_tspans = "".join(f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
                             for i, l in enumerate(wrap(row.get("effect", ""), max_chars=34)))
        body = (req_block +
                f'<text x="{MARGIN}" y="{eff_y}" font-size="{BODY_SIZE-4}" fill="{text}" '
                f'font-family="{bfont}">{eff_tspans}</text>')
    else:
        body_tspans = "".join(f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
                             for i, l in enumerate(wrap(eff_text, max_chars=32)))
        body = (f'<text x="{MARGIN}" y="{body_y}" font-size="{BODY_SIZE}" fill="{text}" '
                f'font-family="{bfont}">{body_tspans}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg', page_cols)}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{frame_col}" stroke-width="6"/>
  {inner_frame}
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{scol}" stroke-width="2" opacity="0.5"/>
  <!-- header band in the suit colour (grows with a wrapped title) -->
  <path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{scol}"/>
  <text font-size="{TITLE_SIZE}" fill="#ffffff" font-family="{tfont}" font-weight="bold">{title_tspans}</text>
  {cost_badge}
  {value_index}
  {type_block}
  {chips}
  {scope_chip}
  {body}
  <!-- footer flourish -->
  <line x1="{MARGIN}" y1="{CARD_H-MARGIN-70}" x2="{CARD_W-MARGIN}" y2="{CARD_H-MARGIN-70}" stroke="{accent}" stroke-width="2" opacity="0.5"/>
  {value_row}
  {ribbon}
</svg>"""


def render_back_svg(slug: str, theme: dict, phase: str | None = None) -> str:
    """Shared card back. Themes that declare a `back` config (Travel Agents' night-market) get a bespoke
    boarding-pass / passport-stamp back, with a day/night/general variant layered on from `phase`;
    every other theme (Beacon's nautical, …) falls through to the unchanged generic ring back."""
    bstyle = back_style(theme, phase)
    if bstyle is None:
        return _render_back_generic(slug, theme)
    return _render_back_travel_agents(slug, theme, bstyle)


def _render_back_generic(slug: str, theme: dict) -> str:
    """The original concentric-ring back — kept byte-for-byte for Beacon and every non-opted theme."""
    ink, accent, radius = theme["ink"], theme["accent"], theme["radius"]
    cx, cy = CARD_W / 2, CARD_H / 2
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{90 + i*46}" fill="none" stroke="{accent}" stroke-width="3" opacity="0.35"/>'
        for i in range(4)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pgb')}</defs>
  <rect width="{CARD_W}" height="{CARD_H}" rx="{radius}" fill="{ink}"/>
  <rect x="34" y="34" width="{CARD_W-68}" height="{CARD_H-68}" rx="{radius-8}" fill="url(#pgb)"/>
  {rings}
  {emblem_svg('spark', cx, cy, 60, accent)}
  <text x="{cx}" y="{CARD_H-90}" font-size="46" fill="{ink}" text-anchor="middle" font-family="{theme['title_font']}" font-style="italic">{esc(slug)}</text>
</svg>"""


# ---- card-back market motifs (CD steer 2026-08-11: local-market feel, NO game name) --------------
# Deterministic SVG silhouettes, arithmetic only (no math import). `ink` = the phase silhouette colour
# (b["stamp"]); `gap` = the light panel colour (ptop) used to carve weave/rib lines. A face-down pile
# sorts day vs night by MOTIF (basket vs lantern) + glyph (早 vs 夜) + drawn sun/moon — never colour alone.

def _awning_svg(x0, x1, y, h, colA, colB, n=9):
    """A candy-stripe market valance: n vertical stripes with a scalloped (half-disc) bottom edge."""
    w = (x1 - x0) / n
    p = []
    for i in range(n):
        x = x0 + i * w
        col = colA if i % 2 == 0 else colB
        p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{col}"/>')
        p.append(f'<path d="M {x:.1f} {y+h:.1f} A {w/2:.1f} {w/2:.1f} 0 0 0 {x+w:.1f} {y+h:.1f} Z" fill="{col}"/>')
    return "".join(p)


def _basket_svg(cx, cy, r, ink, gap):
    """A produce basket heaped with veg — the auntie's morning-market round (DAY motif)."""
    rimY, botY = cy + 0.10 * r, cy + 0.92 * r
    p = []
    for dx, dy, rr in ((-0.52, -0.10, 0.34), (0.0, -0.30, 0.40), (0.52, -0.10, 0.34)):
        p.append(f'<circle cx="{cx+dx*r:.1f}" cy="{cy+dy*r:.1f}" r="{rr*r:.1f}" fill="{ink}" opacity="0.85"/>')
    for dx in (-0.22, 0.22):
        x, topy = cx + dx * r, rimY - 0.62 * r
        p.append(f'<path d="M {x:.1f} {rimY:.1f} Q {x+0.06*r:.1f} {topy:.1f} {x:.1f} {topy-0.10*r:.1f} '
                 f'Q {x-0.06*r:.1f} {topy:.1f} {x:.1f} {rimY:.1f} Z" fill="{ink}" opacity="0.7"/>')
    p.append(f'<path d="M {cx-0.98*r:.1f} {rimY:.1f} L {cx+0.98*r:.1f} {rimY:.1f} '
             f'L {cx+0.66*r:.1f} {botY:.1f} L {cx-0.66*r:.1f} {botY:.1f} Z" fill="{ink}"/>')
    p.append(f'<ellipse cx="{cx:.1f}" cy="{rimY:.1f}" rx="{0.98*r:.1f}" ry="{0.15*r:.1f}" fill="{ink}"/>')
    for t in (0.34, 0.66):
        ytab = rimY + t * (botY - rimY)
        halfw = (0.98 - t * (0.98 - 0.66)) * r
        p.append(f'<line x1="{cx-halfw:.1f}" y1="{ytab:.1f}" x2="{cx+halfw:.1f}" y2="{ytab:.1f}" '
                 f'stroke="{gap}" stroke-width="3" opacity="0.6"/>')
    for dx in (-0.5, 0.0, 0.5):
        p.append(f'<line x1="{cx+dx*0.98*r:.1f}" y1="{rimY:.1f}" x2="{cx+dx*0.66*r:.1f}" y2="{botY:.1f}" '
                 f'stroke="{gap}" stroke-width="3" opacity="0.5"/>')
    return "".join(p)


def _lantern_svg(cx, cy, r, ink, gap):
    """A hung paper lantern — the night market (NIGHT motif)."""
    p = [f'<line x1="{cx:.1f}" y1="{cy-1.02*r:.1f}" x2="{cx:.1f}" y2="{cy-0.90*r:.1f}" stroke="{ink}" stroke-width="4"/>',
         f'<rect x="{cx-0.34*r:.1f}" y="{cy-0.90*r:.1f}" width="{0.68*r:.1f}" height="{0.16*r:.1f}" rx="3" fill="{ink}"/>',
         f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{0.62*r:.1f}" ry="{0.74*r:.1f}" fill="{ink}"/>']
    for dx in (-0.55, 0.0, 0.55):
        x = cx + dx * 0.62 * r
        p.append(f'<line x1="{x:.1f}" y1="{cy-0.72*0.74*r:.1f}" x2="{x:.1f}" y2="{cy+0.72*0.74*r:.1f}" '
                 f'stroke="{gap}" stroke-width="3" opacity="0.5"/>')
    p.append(f'<rect x="{cx-0.30*r:.1f}" y="{cy+0.72*r:.1f}" width="{0.60*r:.1f}" height="{0.14*r:.1f}" rx="3" fill="{ink}"/>')
    p.append(f'<line x1="{cx:.1f}" y1="{cy+0.86*r:.1f}" x2="{cx:.1f}" y2="{cy+1.08*r:.1f}" stroke="{ink}" stroke-width="4"/>')
    return "".join(p)


def _steamer_svg(cx, cy, r, ink, gap):
    """A stacked bamboo steamer with steam — the neutral / any-time motif (cooked-food read)."""
    w, h = 0.92 * r, 0.34 * r
    p = []
    for ty in (cy + 0.16 * r, cy + 0.54 * r):
        p.append(f'<rect x="{cx-w/2:.1f}" y="{ty-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{ink}"/>')
        for dx in (-0.28, 0.0, 0.28):
            x = cx + dx * w
            p.append(f'<line x1="{x:.1f}" y1="{ty-h/2+3:.1f}" x2="{x:.1f}" y2="{ty+h/2-3:.1f}" '
                     f'stroke="{gap}" stroke-width="2.5" opacity="0.5"/>')
    lidY = cy + 0.16 * r - h / 2
    p.append(f'<path d="M {cx-w/2:.1f} {lidY:.1f} Q {cx:.1f} {lidY-0.30*r:.1f} {cx+w/2:.1f} {lidY:.1f} Z" fill="{ink}"/>')
    p.append(f'<circle cx="{cx:.1f}" cy="{lidY-0.24*r:.1f}" r="{0.06*r:.1f}" fill="{ink}"/>')
    for dx in (-0.34, 0.0, 0.34):
        x, syy = cx + dx * r, lidY - 0.34 * r
        p.append(f'<path d="M {x:.1f} {syy:.1f} q {0.12*r:.1f} {-0.12*r:.1f} 0 {-0.24*r:.1f} '
                 f'q {-0.12*r:.1f} {-0.12*r:.1f} 0 {-0.24*r:.1f}" fill="none" stroke="{ink}" '
                 f'stroke-width="3" opacity="0.7" stroke-linecap="round"/>')
    return "".join(p)


_BACK_MOTIFS = {"basket": _basket_svg, "lantern": _lantern_svg, "steamer": _steamer_svg}


def _lane_svg(x0, x1, base_y, ink, bulb, n=5, opacity=0.42):
    """A faint receding row of awning-topped market booths with hanging bulbs (background texture)."""
    slot = (x1 - x0) / n
    p = [f'<g opacity="{opacity}">']
    for i in range(n):
        bx = x0 + i * slot + slot * 0.19
        bw = bh = slot * 0.62
        by = base_y - bh
        p.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{ink}"/>')
        p.append(f'<path d="M {bx-0.06*slot:.1f} {by:.1f} L {bx+bw+0.06*slot:.1f} {by:.1f} '
                 f'L {bx+bw/2:.1f} {by-0.22*slot:.1f} Z" fill="{ink}"/>')
        p.append(f'<circle cx="{bx+bw/2:.1f}" cy="{by-0.34*slot:.1f}" r="{0.06*slot:.1f}" fill="{bulb}"/>')
    p.append('</g>')
    return "".join(p)


def _render_back_travel_agents(slug: str, theme: dict, b: dict) -> str:
    """A LOCAL-MARKET back (CD steer): a striped market awning, a faint stall lane, and a central
    produce-basket (day) / lantern (night) / steamer (any) medallion under the 繁體 market glyph. A
    face-down pile still sorts day vs night by MOTIF + palette + 早/夜 glyph + drawn sun/moon — never
    colour alone. Carries NO game name. All shapes DRAWN (no ☀/☾ tofu)."""
    radius = theme["radius"]
    tfont = theme["title_font"]
    ground = b["ground"]
    ptop, pbot = b["panel"]
    ink = b["stamp"]                       # phase silhouette ink (contrast-safe per phase)
    glow = b.get("glow", ink)
    char = b.get("char", "")
    emblem = b.get("emblem", "stamp")
    awning = b.get("awning", ink)
    market = b.get("market", "")
    motif_fn = _BACK_MOTIFS.get(b.get("motif", "steamer"), _steamer_svg)
    cx = CARD_W / 2
    ix, iy, iw, ih = 40, 40, CARD_W - 80, CARD_H - 80
    panel_txt = pick_text_color(pbot, dark=theme["ink"], light="#ffffff")
    sy = 400
    awn = _awning_svg(ix + 12, ix + iw - 12, iy + 8, 88, awning, ptop, 9)
    lane = _lane_svg(90, CARD_W - 90, CARD_H - 120, ink, glow)
    plate = (f'<circle cx="{cx}" cy="{sy}" r="160" fill="none" stroke="{ink}" stroke-width="3" opacity="0.5"/>'
             f'<circle cx="{cx}" cy="{sy}" r="142" fill="none" stroke="{ink}" stroke-width="2" opacity="0.35"/>')
    motif = motif_fn(cx, sy, 118, ink, ptop)
    accent = emblem_svg(emblem, cx - 96, sy - 100, 26, ink)
    glyph = (f'<text x="{cx}" y="{sy + 250}" font-size="80" fill="{ink}" text-anchor="middle" '
             f'font-family="{tfont}" font-weight="bold">{esc(char)}</text>') if char else ""
    label = (f'<text x="{cx}" y="{sy + 320}" font-size="30" fill="{panel_txt}" text-anchor="middle" '
             f'font-family="{tfont}" letter-spacing="3" opacity="0.85">{esc(market)}</text>') if market else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>
    <linearGradient id="tab" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ptop}"/><stop offset="1" stop-color="{pbot}"/>
    </linearGradient>
    <radialGradient id="tag" cx="0.5" cy="0.38" r="0.75">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.28"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{CARD_W}" height="{CARD_H}" rx="{radius}" fill="{ground}"/>
  <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{radius-10}" fill="url(#tab)" stroke="{ink}" stroke-width="6"/>
  <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{radius-10}" fill="url(#tag)"/>
  {awn}
  {lane}
  {plate}
  {motif}
  {accent}
  {glyph}
  {label}
</svg>"""


def load_rows(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ap = argparse.ArgumentParser(description="Render board game cards from CSV.")
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--out", default=Path("out"), type=Path)
    ap.add_argument("--slug", default=None, help="name for combined outputs (default: csv stem)")
    ap.add_argument("--formats", nargs="+", default=["svg", "png", "screentop"],
                    choices=["svg", "png", "pdf", "tts", "screentop"])
    ap.add_argument("--theme", default="clean",
                    help="visual theme (see themes.py): clean, nautical, ember, parchment, cozy")
    ap.add_argument("--tokens-csv", type=Path, default=None,
                    help="optional token key (columns id,label[,color]) — enables the dish recipe "
                         "chip-row, mapping each recipe ingredient id to its 繁體 glyph + colour")
    ap.add_argument("--tight-grid", action="store_true",
                    help="pack each deck sheet into the tightest cols×rows grid (fewest blank cells) "
                         "instead of always maxing at 10 columns — cleaner Screentop imports for small "
                         "assembled decks. Card cell size is unchanged (409×585).")
    ap.add_argument("--ing-mockups-dir", type=Path, default=None,
                    help="override the dir searched for FIG-ING-<type>.png ingredient art. Default is "
                         "<game>/build/mockups (the CSV's parent's parent) — but a CARVED deck CSV (e.g. "
                         "build/decks/market_*.csv from split_decks) resolves that wrong, so pass this "
                         "explicitly when rendering carved market decks so the ingredient art still embeds.")
    args = ap.parse_args()

    theme = get_theme(args.theme)
    slug = args.slug or args.csv.stem
    # TA art-mock embed dir for ingredient cards: <game>/build/mockups next to the components CSV
    # (game dir = the CSV's parent's parent). Absent dir/file → the byte-identical placeholder path.
    global _ING_MOCKUPS_DIR
    _ING_MOCKUPS_DIR = (args.ing_mockups_dir if args.ing_mockups_dir
                        else args.csv.resolve().parent.parent / "build" / "mockups")
    rows = load_rows(args.csv)
    if not rows:
        print(f"No rows in {args.csv}", file=sys.stderr)
        return 1

    # Optional glyph map for recipe chips: id -> {label, color}. Absent => chips are simply not drawn,
    # so decks without a `recipe` column (assignments, Beacon) are unaffected.
    glyph_map = None
    if args.tokens_csv and args.tokens_csv.exists():
        glyph_map = {}
        for r in load_rows(args.tokens_csv):
            rid = (r.get("id") or "").strip()
            if rid:
                glyph_map[rid] = {"label": (r.get("label") or "").strip(),
                                  "color": (r.get("color") or "").strip()}
        print(f"[glyphs] loaded {len(glyph_map)} token glyphs from {args.tokens_csv}")

    (args.out / "svg").mkdir(parents=True, exist_ok=True)

    # 1) Always render per-card SVGs (no dependencies).
    svg_paths = []
    for row in rows:
        cid = (row.get("id") or row.get("name") or f"card{len(svg_paths)}").strip()
        p = args.out / "svg" / f"{cid}.svg"
        p.write_text(render_card_svg(row, theme, glyph_map), encoding="utf-8")
        svg_paths.append((cid, p, int(row.get("quantity") or 1)))
    # Distinct day/night/general backs, DATA-DRIVEN off the `phase` column: a deck whose cards all share
    # one phase gets that phase's back (so a split day/night pile sorts face-down at a glance); a mixed
    # or unphased deck (the full-CSV overview sheets, characters) gets the neutral Travel-Agents back.
    phases = {(r.get("phase") or "").strip().lower() for r in rows}
    phases.discard("")
    back_phase = next(iter(phases)) if len(phases) == 1 else None
    back_svg = render_back_svg(slug, theme, back_phase)
    (args.out / "svg" / "_back.svg").write_text(back_svg, encoding="utf-8")
    print(f"[svg]  wrote {len(svg_paths)} card SVGs -> {args.out/'svg'}  (back phase: {back_phase or 'neutral'})")

    # cairosvg is needed for anything raster/PDF.
    try:
        import cairosvg  # type: ignore
    except Exception:
        cairosvg = None
        if any(f in args.formats for f in ("png", "pdf", "tts")):
            print("[warn] cairosvg not installed — only SVGs produced. "
                  "Install: pip install -r requirements.txt (+ `brew install cairo` on macOS).")

    # 2) PNGs
    if "png" in args.formats and cairosvg:
        (args.out / "png").mkdir(parents=True, exist_ok=True)
        for cid, p, _ in svg_paths:
            cairosvg.svg2png(url=str(p), write_to=str(args.out / "png" / f"{cid}.png"),
                             output_width=CARD_W, output_height=CARD_H)
        print(f"[png]  wrote {len(svg_paths)} PNGs -> {args.out/'png'}")

    # 3) Print PDF — one card face per page (PrintNinja-style; add real bleed for manufacturing).
    if "pdf" in args.formats and cairosvg:
        (args.out / "print").mkdir(parents=True, exist_ok=True)
        try:
            from PyPDF2 import PdfMerger  # optional
            merger = PdfMerger()
            for cid, p, _ in svg_paths:
                tmp = args.out / "print" / f"{cid}.pdf"
                cairosvg.svg2pdf(url=str(p), write_to=str(tmp))
                merger.append(str(tmp))
            merger.write(str(args.out / "print" / f"{slug}.pdf"))
            merger.close()
            print(f"[pdf]  wrote combined {args.out/'print'/f'{slug}.pdf'}")
        except Exception:
            for cid, p, _ in svg_paths:
                cairosvg.svg2pdf(url=str(p), write_to=str(args.out / "print" / f"{cid}.pdf"))
            print(f"[pdf]  wrote per-card PDFs -> {args.out/'print'} (install PyPDF2 to combine)")

    # 4) Deck sheet(s) for Screentop.gg (default) / Tabletop Simulator — same grid-sheet format.
    want_sheet = "screentop" in args.formats or "tts" in args.formats
    if want_sheet and cairosvg:
        try:
            from PIL import Image  # type: ignore
        except Exception:
            print("[warn] Pillow not installed — skipping TTS sheet. pip install Pillow")
            return 0
        import io

        # Expand by quantity; TTS grid is capped so each card cell stays <= ~409x585 px.
        expanded = []
        for cid, p, qty in svg_paths:
            expanded.extend([(cid, p)] * max(1, qty))

        COLS, ROWS_MAX = 10, 7          # TTS max grid
        per_sheet = COLS * ROWS_MAX - 1  # reserve last cell for the back

        def pick_cols(n_cells: int) -> int:
            """Fewest-blanks grid within the 10×7 cap; tie-break toward fewer rows (wider)."""
            best = (10 ** 9, 10 ** 9, COLS)
            for c in range(1, COLS + 1):
                r = math.ceil(n_cells / c)
                if r > ROWS_MAX:
                    continue
                key = (c * r - n_cells, r)      # (blank cells, rows)
                if key < best[:2]:
                    best = (key[0], key[1], c)
            return best[2]
        # cell size respecting the 4096 px texture cap
        cell_w = min(CARD_W, 4096 // COLS)
        cell_h = min(CARD_H, 4096 // ROWS_MAX)

        def raster(svg_path):
            png_bytes = cairosvg.svg2png(url=str(svg_path), output_width=cell_w, output_height=cell_h)
            return Image.open(io.BytesIO(png_bytes)).convert("RGBA")

        back_png = cairosvg.svg2png(bytestring=back_svg.encode(), output_width=cell_w, output_height=cell_h)
        back_img = Image.open(io.BytesIO(back_png)).convert("RGBA")

        sheet_dir = args.out / "sheets"
        sheet_dir.mkdir(parents=True, exist_ok=True)
        # standalone back image (Screentop lets you set one shared back per deck)
        back_img.save(sheet_dir / f"{slug}_back.png")
        sheets = math.ceil(len(expanded) / per_sheet) or 1
        for s in range(sheets):
            chunk = expanded[s * per_sheet:(s + 1) * per_sheet]
            n = len(chunk) + 1                      # + back
            cols = pick_cols(n) if args.tight_grid else min(COLS, n)
            rows_n = math.ceil(n / cols)
            sheet = Image.new("RGBA", (cols * cell_w, rows_n * cell_h), (0, 0, 0, 0))
            for i, (_cid, p) in enumerate(chunk):
                r, c = divmod(i, cols)
                sheet.paste(raster(p), (c * cell_w, r * cell_h))
            # place the back in the final cell
            r, c = divmod(len(chunk), cols)
            sheet.paste(back_img, (c * cell_w, r * cell_h))
            out_png = sheet_dir / f"{slug}_sheet_{s+1}.png"
            sheet.save(out_png)
            print(f"[sheet] wrote {out_png}  ({cols}x{rows_n} grid, {len(chunk)} cards + back)")
        print(f"[sheet] standalone back -> {sheet_dir / f'{slug}_back.png'}")
        if "screentop" in args.formats:
            print("[screentop] New Game > add a Deck > upload the sheet as the deck face and "
                  f"'{slug}_back.png' as the back; set columns/rows to the grid above. "
                  "Share the room link to play with a friend.")
        if "tts" in args.formats:
            print("[tts] Objects > Components > Custom > Deck; set Width/Height to the grid, "
                  "point Face at the sheet and Back at the standalone back image.")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
