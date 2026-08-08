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
import csv
import html
import math
import os
import re
import sys
from pathlib import Path

# Scoped-event icons: the ⦿/⬢/➤ glyphs are TOFU under cairosvg's toy text API (no fall-through to a
# glyph-bearing font), so we DRAW them as SVG shapes keyed off the event `scope` column and keep the
# word label alongside. (bg-access FIX A.)
SCOPE_SHAPE = {"self": "ring_dot", "region": "hex", "neighbour": "arrow", "island": "island_ring"}
SCOPE_WORD = {"self": "YOU 自己", "region": "THIS REGION 全區", "neighbour": "NEXT DOOR 鄰區",
              "island": "ISLAND-WIDE 全島"}
_SCOPE_GLYPHS = "⦿⬢➤"
# The slate that ties the Scheduled-Maintenance island banner to its 停 board marker (bg-access §v6.3.1).
MAINT_SLATE = "#8A8F98"

from themes import (get_theme, resolve_suit, emblem_svg, page_gradient, pick_text_color,
                    phase_style, phase_ribbon_svg, back_style)

# ---- Card geometry (poker, trimmed, 300 DPI) --------------------------------
CARD_W, CARD_H = 750, 1050          # px @ 300 DPI
MARGIN = 54                         # ~4.5 mm safe margin
TITLE_SIZE, TYPE_SIZE, BODY_SIZE = 50, 28, 34
LINE_H = 44
TITLE_WRAP = 22                     # chars/line before the title wraps (header grows to fit)
TITLE_LINE_H = 56


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
# guarded by `_is_vendor` (needs BOTH `tier` and `buzz_cost`), so decks without
# those columns — Beacon, missions, events, characters — are byte-unchanged.
TIER_FICTION = {"1": "攤 STALL", "2": "小吃 EATERY", "3": "名店 MARQUEE"}
REGION_LABEL = {"north": "NORTH 北", "central": "CENTRAL 中",
                "south": "SOUTH 南", "east": "EAST 東"}


def _is_vendor(row: dict) -> bool:
    return bool(str(row.get("tier", "")).strip()) and bool(str(row.get("buzz_cost", "")).strip())


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
    teal = theme["suits"].get("central", {}).get("color", "#1F8A7A")
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")

    recipe = [s.strip() for s in (row.get("recipe") or "").split(";") if s.strip()]
    buzz = str(row.get("buzz_cost", "")).strip()
    draw = str(row.get("draw", "")).strip()          # v6.3: the vendor's Draw (人氣) ATTRIBUTE — not a score
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

    # --- PAY row: ingredient chips (emblem-shaped, region colour, 繁體) + Buzz ----
    # v6.3.1 CD-4: every NIGHT marquee is CROSS-REGION — a chip whose ingredient belongs to a DIFFERENT
    # signature region than this vendor is flagged with an out-of-region "→" badge (and a header
    # CROSS-REGION tag) so the two-region bill parses at a glance, not just as a differently-coloured chip.
    ING_REGION = {"pork": "N", "tea": "C", "seafood": "S", "rice": "E"}   # sugar = common (never foreign)
    card_letter = {"north": "N", "central": "C", "south": "S", "east": "E"}.get(region, "")
    pay_label_y = strip_y + 104
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
    # plus + Buzz badge
    plus_x = x + 6
    x2 = plus_x + 40
    buzz_badge = (
        f'<text x="{plus_x}" y="{chips_cy + 14}" font-size="46" fill="{muted}" '
        f'font-family="{tfont}" font-weight="bold">+</text>'
        f'<circle cx="{x2 + r}" cy="{chips_cy}" r="{r}" fill="{violet}" stroke="{ink}" stroke-width="3"/>'
        f'<text x="{x2 + r}" y="{chips_cy + 12}" font-size="40" fill="#ffffff" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">{esc(buzz)}</text>'
        f'<text x="{x2 + r}" y="{chips_cy + 62}" font-size="24" fill="{violet}" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">讚 BUZZ</text>')
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
        + cross_tag + chips + buzz_badge)

    # --- DRAW row: the vendor's Draw (人氣) ATTRIBUTE — a printed number, NOT a score --
    # v6.3 tickets-only: vendors give no points. Draw only feeds the value-referencing
    # tickets and marks the ★ apex the marquee get. So the old GAIN(Prestige+Rep) +
    # PERK blocks are gone — a vendor face is just Draw + (region icon | none).
    # The Draw number is deliberately DE-SCORED: a crowd/人氣 glyph (never the gold ★-spark, which reads
    # as VP) and the number set inside a rounded "meter" gauge so it parses as a crowd-pull ATTRIBUTE, not
    # a points value. Kept mid-card (not the bottom-right VP corner) with an explicit "not points" caption.
    draw_label_y = chips_cy + 118
    draw_cy = draw_label_y + 62
    dx = MARGIN + 42
    gauge_x, gauge_w, gauge_h = dx + 60, 108, 60
    draw_block = (
        f'<text x="{MARGIN}" y="{draw_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">DRAW 人氣</text>'
        + emblem_svg("crowd", dx, draw_cy, 34, gold) +
        f'<rect x="{gauge_x}" y="{draw_cy - gauge_h/2}" width="{gauge_w}" height="{gauge_h}" '
        f'rx="{gauge_h/2}" fill="#ffffff" opacity="0.55" stroke="{gold}" stroke-width="3"/>'
        f'<text x="{gauge_x + gauge_w/2}" y="{draw_cy + 16}" font-size="46" fill="{gold}" '
        f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(draw)}</text>'
        f'<text x="{gauge_x + gauge_w + 20}" y="{draw_cy + 14}" font-size="23" fill="{muted}" '
        f'font-family="{bfont}" font-style="italic">crowd-pull · engine value, not points</text>')

    # --- ICON box: region discount icon, or NONE (trophy / drink) ---------------
    icon_label_y = draw_cy + 108
    box_y = icon_label_y + 18
    box_h = CARD_H - MARGIN - box_y
    if icon:
        isuit = resolve_suit(theme, {"N": "north", "C": "central",
                                     "S": "south", "E": "east"}.get(icon, icon.lower()))
        iemb, icol = isuit["emblem"], isuit["color"]
        icon_txt = f"{icon} discount icon — each you hold makes this region's ingredients 1 cheaper."
    elif is_apex:
        iemb, icol = "spark", gold
        icon_txt = "★ trophy — top Draw, NO discount icon (a get, not an engine piece)."
    else:
        iemb, icol = "circle", muted
        icon_txt = "Drink — cheap filler, NO discount icon."
    icon_lines = wrap(icon_txt, max_chars=26)
    icon_tspans = "".join(f'<tspan x="{MARGIN + 96}" dy="{0 if i == 0 else 40}">{esc(l)}</tspan>'
                          for i, l in enumerate(icon_lines))
    icon_block = (
        f'<text x="{MARGIN}" y="{icon_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">ICON 圖示</text>'
        f'<rect x="{MARGIN}" y="{box_y}" width="{CARD_W - 2*MARGIN}" height="{box_h}" rx="18" '
        f'fill="#ffffff" opacity="0.45" stroke="{icol}" stroke-width="3"/>'
        + emblem_svg(iemb, MARGIN + 46, box_y + 52, 30, icol) +
        f'<text x="{MARGIN + 96}" y="{box_y + 46}" font-size="30" fill="{text}" '
        f'font-family="{bfont}">{icon_tspans}</text>')

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
  {pay_block}
  {draw_block}
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


def render_card_svg(row: dict, theme: dict, glyph_map: dict | None = None) -> str:
    if _is_vendor(row):
        return render_vendor_svg(row, theme, glyph_map)
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
    is_objective = bool(target)                          # assignment-style: value is a completion bonus

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
    if value:
        try:
            vn = int(float(value))
        except ValueError:
            vn = 0
        if is_objective:
            # value footer chip (bottom-left), no top index, no pip row. Travel Agents' Tour Tickets score
            # in the game's own "value" language (成團 win pile → +value); other games keep the generic VP.
            bonus_word = "value" if ctype.lower() == "mission" else "VP"
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

    # --- scoped-event badge (drawn shape + word) — replaces the tofu ⦿/⬢/➤ glyph (bg-access FIX A) ---
    scope = (row.get("scope") or "").strip().lower()
    scope_chip = ""
    eff_text = row.get("effect", "")
    if scope in SCOPE_SHAPE and not (recipe and glyph_map):
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


def _render_back_travel_agents(slug: str, theme: dict, b: dict) -> str:
    """A night-market boarding-pass back: dusk-indigo ground, a passport-stamp roundel, a ticket-stub
    perforation, and (when phased) a warm-sun 日 / neon-moon 夜 treatment so a face-down pile sorts into
    day vs night at a glance — by MOTIF + palette, never colour alone. All shapes DRAWN (no ☀/☾ tofu)."""
    radius = theme["radius"]
    tfont = theme["title_font"]
    ground = b["ground"]
    ptop, pbot = b["panel"]
    stamp = b["stamp"]
    glow = b.get("glow", stamp)
    char = b.get("char", "")
    label = b.get("label", b.get("sub", ""))
    emblem = b.get("emblem", "stamp")
    cx = CARD_W / 2
    # inner panel inset
    ix, iy, iw, ih = 40, 40, CARD_W - 80, CARD_H - 80
    # ground colour under the panel that shows through the border + notches
    panel_txt = pick_text_color(pbot, dark=theme["ink"], light="#ffffff")
    # ticket-stub perforation across the lower third, with edge notches punched out of the panel
    perf_y = CARD_H - 300
    dashes = "".join(
        f'<line x1="{ix + 44 + i*46}" y1="{perf_y}" x2="{ix + 44 + i*46 + 24}" y2="{perf_y}" '
        f'stroke="{stamp}" stroke-width="6" stroke-linecap="round" opacity="0.65"/>'
        for i in range(int((iw - 88) // 46)))
    notch_l = f'<circle cx="{ix}" cy="{perf_y}" r="22" fill="{ground}"/>'
    notch_r = f'<circle cx="{ix + iw}" cy="{perf_y}" r="22" fill="{ground}"/>'
    # central passport-stamp roundel: double ring + the drawn phase motif + the 繁體 phase char
    sy = 430
    roundel = (
        f'<circle cx="{cx}" cy="{sy}" r="150" fill="none" stroke="{stamp}" stroke-width="10" opacity="0.9"/>'
        f'<circle cx="{cx}" cy="{sy}" r="128" fill="none" stroke="{stamp}" stroke-width="3" opacity="0.6"/>'
        + emblem_svg(emblem, cx, sy - 18, 66, stamp))
    if char:
        roundel += (f'<text x="{cx}" y="{sy + 96}" font-size="72" fill="{stamp}" text-anchor="middle" '
                    f'font-family="{tfont}" font-weight="bold">{esc(char)}</text>')
    # corner stamp flecks for texture (low opacity), always the neutral stamp mark
    corners = "".join(
        emblem_svg("stamp", x, y, 22, stamp) for (x, y) in
        ((ix + 54, iy + 54), (ix + iw - 54, iy + 54),
         (ix + 54, iy + ih - 54), (ix + iw - 54, iy + ih - 54)))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>
    <linearGradient id="tab" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ptop}"/><stop offset="1" stop-color="{pbot}"/>
    </linearGradient>
    <radialGradient id="tag" cx="0.5" cy="0.42" r="0.75">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.28"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{CARD_W}" height="{CARD_H}" rx="{radius}" fill="{ground}"/>
  <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{radius-10}" fill="url(#tab)" stroke="{stamp}" stroke-width="6"/>
  <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{radius-10}" fill="url(#tag)"/>
  <g opacity="0.28">{corners}</g>
  <text x="{cx}" y="{iy + 108}" font-size="60" fill="{stamp}" text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="6">{esc(b.get('wordmark',''))}</text>
  <text x="{cx}" y="{iy + 162}" font-size="34" fill="{panel_txt}" text-anchor="middle" font-family="{tfont}" letter-spacing="4" opacity="0.8">{esc(b.get('sub',''))}</text>
  {roundel}
  {dashes}
  {notch_l}
  {notch_r}
  <text x="{cx}" y="{CARD_H - 190}" font-size="40" fill="{panel_txt}" text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="3">{esc(label)}</text>
  <text x="{cx}" y="{CARD_H - 100}" font-size="30" fill="{panel_txt}" text-anchor="middle" font-family="{tfont}" font-style="italic" opacity="0.7">{esc(slug)}</text>
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
    args = ap.parse_args()

    theme = get_theme(args.theme)
    slug = args.slug or args.csv.stem
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
