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
SCOPE_SHAPE = {"self": "ring_dot", "region": "hex", "neighbour": "arrow"}
SCOPE_WORD = {"self": "YOU 自己", "region": "THIS REGION 全區", "neighbour": "NEXT DOOR 鄰區"}
_SCOPE_GLYPHS = "⦿⬢➤"

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
# A vendor row carries a two-input economy (ingredients + Buzz) and three reward
# vectors (Prestige / Reputation / perk). The generic template buries all of that
# in body text, so vendor-shaped rows get a dedicated cost-row / reward-row layout.
# Dispatch is guarded by `_is_vendor` (needs BOTH `tier` and `buzz_cost`), so decks
# without those columns — Beacon, missions, events, characters — are byte-unchanged.
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
    prestige = str(row.get("value", "")).strip()
    rep = str(row.get("rep", "")).strip()
    tier = str(row.get("tier", "")).strip()
    perk_text = (row.get("perk") or "").strip()
    perk_code = (row.get("perk_code") or "").strip()

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
        f'text-anchor="end" font-family="{bfont}" font-style="italic">discount + coverage</text>')
    eng = _english_name(row.get("effect", ""))
    eng_line = ""
    if eng:
        eng_line = (f'<text x="{MARGIN}" y="{strip_y + 40}" font-size="30" fill="{text}" '
                    f'font-family="{bfont}" font-style="italic">{esc(eng)}</text>')

    # --- PAY row: ingredient chips (emblem-shaped, region colour, 繁體) + Buzz ----
    pay_label_y = strip_y + 104
    chips_cy = pay_label_y + 66
    r = 34
    x = MARGIN + 6
    chips = ""
    for iid in recipe:
        isuit = resolve_suit(theme, iid) if iid in theme["suits"] else {"color": muted, "emblem": "circle"}
        icol = isuit["color"]
        lab = esc((glyph_map or {}).get(iid, {}).get("label", "")) if glyph_map else ""
        tcol = pick_text_color(icol, dark=ink, light="#ffffff")
        chips += emblem_svg(isuit["emblem"], x + r, chips_cy, r, icol, stroke=ink)
        chips += (f'<text x="{x + r}" y="{chips_cy + r * 0.34}" font-size="30" fill="{tcol}" '
                  f'text-anchor="middle" font-family="{bfont}" font-weight="bold">{lab}</text>')
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
    pay_block = (
        f'<text x="{MARGIN}" y="{pay_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">PAY 付</text>' + chips + buzz_badge)

    # --- GAIN row: Prestige star + number, Reputation chip ----------------------
    gain_label_y = chips_cy + 118
    gain_cy = gain_label_y + 62
    # Prestige
    px = MARGIN + 40
    prestige_block = (
        emblem_svg("spark", px, gain_cy, 38, gold) +
        f'<text x="{px + 66}" y="{gain_cy + 18}" font-size="56" fill="{gold}" '
        f'font-family="{tfont}" font-weight="bold">{esc(prestige)}</text>'
        f'<text x="{px - 4}" y="{gain_cy + 70}" font-size="24" fill="{muted}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="1">PRESTIGE</text>')
    # Reputation
    rx = MARGIN + 320
    rep_block = (
        f'<circle cx="{rx + 34}" cy="{gain_cy}" r="38" fill="{teal}" stroke="{ink}" stroke-width="3"/>'
        f'<text x="{rx + 34}" y="{gain_cy + 14}" font-size="40" fill="#ffffff" text-anchor="middle" '
        f'font-family="{tfont}" font-weight="bold">+{esc(rep)}</text>'
        f'<text x="{rx + 90}" y="{gain_cy + 18}" font-size="34" fill="{teal}" '
        f'font-family="{tfont}" font-weight="bold">譽</text>'
        f'<text x="{rx - 4}" y="{gain_cy + 70}" font-size="24" fill="{muted}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="1">REPUTATION</text>')
    gain_block = (
        f'<text x="{MARGIN}" y="{gain_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">GAIN 得</text>'
        + prestige_block + rep_block)

    # --- PERK box: icon + wrapped text ------------------------------------------
    perk_label_y = gain_cy + 108
    pemb, pcol = _perk_visual(perk_code, rsuit, theme)
    box_y = perk_label_y + 18
    box_h = CARD_H - MARGIN - box_y
    perk_lines = wrap(perk_text, max_chars=26)
    perk_tspans = "".join(f'<tspan x="{MARGIN + 96}" dy="{0 if i == 0 else 40}">{esc(l)}</tspan>'
                          for i, l in enumerate(perk_lines))
    perk_block = (
        f'<text x="{MARGIN}" y="{perk_label_y}" font-size="28" fill="{accent}" '
        f'font-family="{tfont}" font-weight="bold" letter-spacing="3">PERK 技</text>'
        f'<rect x="{MARGIN}" y="{box_y}" width="{CARD_W - 2*MARGIN}" height="{box_h}" rx="18" '
        f'fill="#ffffff" opacity="0.45" stroke="{pcol}" stroke-width="3"/>'
        + emblem_svg(pemb, MARGIN + 46, box_y + 52, 30, pcol) +
        f'<text x="{MARGIN + 96}" y="{box_y + 46}" font-size="30" fill="{text}" '
        f'font-family="{bfont}">{perk_tspans}</text>')

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
  {gain_block}
  {perk_block}
  {ribbon}
</svg>"""


def render_card_svg(row: dict, theme: dict, glyph_map: dict | None = None) -> str:
    if _is_vendor(row):
        return render_vendor_svg(row, theme, glyph_map)
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
            # +N VP footer chip (bottom-left), no top index, no pip row
            chw, chh = 168, 60
            cx0, cy0 = MARGIN, CARD_H - MARGIN - 60
            value_row = (
                f'<rect x="{cx0}" y="{cy0}" width="{chw}" height="{chh}" rx="{chh/2}" fill="{scol}"/>'
                f'<text x="{cx0 + chw/2}" y="{cy0 + chh*0.68}" font-size="40" fill="#ffffff" '
                f'text-anchor="middle" font-family="{tfont}" font-weight="bold">+{esc(value)} VP</text>')
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
    type_block = (
        emblem_svg(suit['emblem'], MARGIN + 16, type_emblem_cy, 15, scol) +
        f'<text x="{MARGIN+44}" y="{type_text_y}" font-size="{TYPE_SIZE}" fill="{muted}" '
        f'font-family="{tfont}" font-style="italic" letter-spacing="2">{esc(ctype).upper()}</text>')

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
