#!/usr/bin/env python3
"""
make_figures.py — build ANNOTATED TEACHING FIGURES for the Travel Agents rulebook.

Takes the game's real committed renders (vendor card, tour card, ingredient card, the day map board)
and overlays clean callout lines + short English-first labels — "how to read this component" diagrams.
PRESENTATION ONLY: nothing here changes a rule; it only points at what the render already shows.

Output: games/travel-agents/build/figures/FIG-*.png  (build/ = gitignored playtest props, because the
base renders embed AI-mockup food art — the studio no-AI-final-art rail keeps those out of committed dirs).

Renders SVG -> PNG via cairosvg (WenQuanYi Zen Hei carries the 繁體 labels, matching the cards).
"""
from __future__ import annotations
import base64, html, io, textwrap
from pathlib import Path
from PIL import Image
import cairosvg

ROOT = Path("/home/user/BG-Dev/games/travel-agents")
OUT = ROOT / "build" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# --- night-market palette (themes.py: "night-market") -------------------------------------------
CREAM   = "#FBF7EE"
PANEL   = "#F7F1E3"
INK     = "#26324D"   # dusk indigo
ACCENT  = "#D64545"   # lantern vermilion
MUTED   = "#7A6E58"   # warm taupe
GOLD    = "#C9A227"
FONT    = "WenQuanYi Zen Hei"


def _datauri(path: Path) -> str:
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    buf = io.BytesIO(); im.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _wrap(text: str, max_chars: int):
    return textwrap.wrap(text, width=max_chars) or [""]


# =================================================================================================
# CARD anatomy: card centred, labelled chips down the left & right with leader lines to the target.
# =================================================================================================
def card_figure(base: Path, out: Path, title: str, left: list, right: list):
    """left / right: lists of dicts {fx, fy, term, gloss}. fx,fy = target point as fraction of card."""
    im = Image.open(base); cw, ch = im.size
    COL, GAP, TITLE_H, PAD_TB = 640, 70, 120, 70
    card_x = COL + GAP
    W = COL + GAP + cw + GAP + COL
    H = TITLE_H + PAD_TB + ch + PAD_TB
    card_y = TITLE_H + PAD_TB

    CHIP_W = COL - 40
    term_fs, gloss_fs, lh = 34, 26, 32
    inner = CHIP_W - 44

    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CREAM}"/>']
    # title band
    parts.append(f'<rect x="0" y="0" width="{W}" height="{TITLE_H}" fill="{INK}"/>')
    parts.append(f'<rect x="0" y="{TITLE_H-8}" width="{W}" height="8" fill="{ACCENT}"/>')
    parts.append(f'<text x="{W/2:.0f}" y="{TITLE_H*0.63:.0f}" font-family="{FONT}" font-size="52" '
                 f'font-weight="bold" fill="#ffffff" text-anchor="middle">{_esc(title)}</text>')
    # soft shadow + card
    parts.append(f'<rect x="{card_x+10}" y="{card_y+12}" width="{cw}" height="{ch}" rx="34" '
                 f'fill="#000000" opacity="0.16"/>')
    parts.append(f'<image x="{card_x}" y="{card_y}" width="{cw}" height="{ch}" '
                 f'xlink:href="{_datauri(base)}"/>')

    TOP_PAD, BOT_PAD, GAP_TG = 24, 26, 12
    term_adv, gloss_adv = int(term_fs * 1.22), int(gloss_fs * 1.28)

    def emit(items, side):
        n = len(items)
        for i, a in enumerate(items):
            tx = card_x + a["fx"] * cw
            ty = card_y + a["fy"] * ch
            term_lines = _wrap(a["term"], max(8, int(inner / (term_fs * 0.62))))
            gloss_lines = _wrap(a["gloss"], max(8, int(inner / (gloss_fs * 0.52))))
            text_h = len(term_lines) * term_adv + GAP_TG + len(gloss_lines) * gloss_adv
            chip_h = TOP_PAD + text_h + BOT_PAD
            slot_top = card_y + 2
            slot_span = ch - 4 - chip_h
            cy = slot_top + (slot_span * (i / max(1, n - 1)) if n > 1 else slot_span / 2)
            chip_x = 20 if side == "left" else card_x + cw + GAP + 20
            anchor_x = chip_x + CHIP_W if side == "left" else chip_x
            anchor_y = cy + chip_h / 2
            bend_x = card_x - 26 if side == "left" else card_x + cw + 26
            parts.append(
                f'<polyline points="{anchor_x:.0f},{anchor_y:.0f} {bend_x:.0f},{anchor_y:.0f} '
                f'{tx:.0f},{ty:.0f}" fill="none" stroke="{INK}" stroke-width="3.5" '
                f'stroke-linejoin="round" opacity="0.9"/>')
            parts.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="13" fill="{ACCENT}" '
                         f'stroke="#ffffff" stroke-width="4"/>')
            parts.append(f'<rect x="{chip_x}" y="{cy:.0f}" width="{CHIP_W}" height="{chip_h}" rx="18" '
                         f'fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
            parts.append(f'<rect x="{chip_x}" y="{cy:.0f}" width="10" height="{chip_h}" rx="5" fill="{ACCENT}"/>')
            y = cy + TOP_PAD
            for ln in term_lines:
                parts.append(f'<text x="{chip_x+28}" y="{y+term_fs*0.80:.0f}" font-family="{FONT}" '
                             f'font-size="{term_fs}" font-weight="bold" fill="{INK}">{_esc(ln)}</text>')
                y += term_adv
            y += GAP_TG
            for ln in gloss_lines:
                parts.append(f'<text x="{chip_x+28}" y="{y+gloss_fs*0.80:.0f}" font-family="{FONT}" '
                             f'font-size="{gloss_fs}" fill="{MUTED}">{_esc(ln)}</text>')
                y += gloss_adv

    emit(left, "left")
    emit(right, "right")

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + '</svg>')
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(out), output_width=W, output_height=H)
    print(f"[fig] {out.name}  ({W}x{H})")


# =================================================================================================
# BOARD at a glance: numbered passport-stamp roundels on the board + a legend strip below.
# =================================================================================================
def board_figure(base: Path, out: Path, title: str, marks: list, legend: list):
    """marks: {n, tx_f, ty_f, rx_f, ry_f} roundel at (rx,ry), leader to target (tx,ty), fractions of board.
       legend: {n, term, gloss} entries laid out in the bottom strip (2 columns)."""
    im = Image.open(base); bw, bh = im.size
    STRIP = int(bh * 0.40)
    W, H = bw, bh + STRIP

    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{INK}"/>']
    parts.append(f'<image x="0" y="0" width="{bw}" height="{bh}" xlink:href="{_datauri(base)}"/>')

    def roundel(cx, cy, n, r=46):
        return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{ACCENT}" stroke="#ffffff" '
                f'stroke-width="6"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="none" '
                f'stroke="{ACCENT}" stroke-width="2"/>'
                f'<text x="{cx:.0f}" y="{cy+r*0.36:.0f}" font-family="{FONT}" font-size="{r*1.1:.0f}" '
                f'font-weight="bold" fill="#ffffff" text-anchor="middle">{n}</text>')

    for m in marks:
        tx, ty = m["tx_f"] * bw, m["ty_f"] * bh
        rx, ry = m["rx_f"] * bw, m["ry_f"] * bh
        parts.append(f'<line x1="{rx:.0f}" y1="{ry:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" '
                     f'stroke="#ffffff" stroke-width="6" opacity="0.95"/>')
        parts.append(f'<line x1="{rx:.0f}" y1="{ry:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" '
                     f'stroke="{INK}" stroke-width="2.5"/>')
        parts.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="12" fill="#ffffff" stroke="{INK}" stroke-width="4"/>')
        parts.append(roundel(rx, ry, m["n"]))

    # legend strip
    sy = bh
    parts.append(f'<rect x="0" y="{sy}" width="{W}" height="{STRIP}" fill="{PANEL}"/>')
    parts.append(f'<rect x="0" y="{sy}" width="{W}" height="10" fill="{ACCENT}"/>')
    parts.append(f'<text x="60" y="{sy+96}" font-family="{FONT}" font-size="60" font-weight="bold" '
                 f'fill="{INK}">{_esc(title)}</text>')
    col_x = [60, W // 2 + 20]
    rows_per_col = (len(legend) + 1) // 2
    term_fs, gloss_fs = 42, 33
    for idx, e in enumerate(legend):
        col = idx // rows_per_col
        row = idx % rows_per_col
        x = col_x[col]
        y = sy + 190 + row * 168
        parts.append(roundel(x + 42, y - 12, e["n"], r=42))
        tx = x + 108
        parts.append(f'<text x="{tx}" y="{y}" font-family="{FONT}" font-size="{term_fs}" '
                     f'font-weight="bold" fill="{INK}">{_esc(e["term"])}</text>')
        gl = _wrap(e["gloss"], 50)
        gy = y + 48
        for ln in gl:
            parts.append(f'<text x="{tx}" y="{gy}" font-family="{FONT}" font-size="{gloss_fs}" '
                         f'fill="{MUTED}">{_esc(ln)}</text>')
            gy += 42

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + '</svg>')
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(out), output_width=W, output_height=H)
    print(f"[fig] {out.name}  ({W}x{H})")


# =================================================================================================
if __name__ == "__main__":
    P = ROOT / "build" / "png"

    # 1) VENDOR (N10 Gua Bao — a day engine stall)
    card_figure(
        P / "N10.png", OUT / "FIG-VENDOR.png", "How to read a Vendor",
        left=[
            {"fx": 0.30, "fy": 0.09, "term": "Dish name",
             "gloss": "English first, then 繁體 (割包 · Kuah-pau)."},
            {"fx": 0.13, "fy": 0.21, "term": "Engine bonus",
             "gloss": "Win this day stall and its region's ingredients cost you 1 less — icons stack."},
            {"fx": 0.37, "fy": 0.78, "term": "Recipe",
             "gloss": "Ingredients you pay to Sign Up (minus your region discounts)."},
            {"fx": 0.50, "fy": 0.945, "term": "Phase footer",
             "gloss": "A day 日 stall or a night 夜 trophy."},
        ],
        right=[
            {"fx": 0.86, "fy": 0.07, "term": "Region",
             "gloss": "Which region it sits in (▲ North 北)."},
            {"fx": 0.845, "fy": 0.20, "term": "Points",
             "gloss": "VP you score for winning it. Small on day stalls, big on night trophies."},
            {"fx": 0.73, "fy": 0.82, "term": "Crowd floor",
             "gloss": "Followers you must have on it to claim it (1 day · 2–3 night · 4 ★ apex)."},
        ],
    )

    # 2) TOUR / Booking (d_south2 Tainan Old-Capital Crawl)
    card_figure(
        P / "d_south2.png", OUT / "FIG-TOUR.png", "How to read a Tour",
        left=[
            {"fx": 0.30, "fy": 0.11, "term": "Tour name",
             "gloss": "English first, then 繁體 (府城巡禮)."},
            {"fx": 0.50, "fy": 0.60, "term": "Illustration",
             "gloss": "The place and its signature dish — flavour, not a rule."},
        ],
        right=[
            {"fx": 0.905, "fy": 0.075, "term": "Ticket",
             "gloss": "The boarding-pass mark: this is a Tour (Booking) card."},
            {"fx": 0.77, "fy": 0.255, "term": "Value",
             "gloss": "VP scored when you complete the tour (+5)."},
            {"fx": 0.50, "fy": 0.925, "term": "Requirement",
             "gloss": "The vendors you must win to complete it (here: ≥ 2 Tainan / South stalls)."},
        ],
    )

    # 3) INGREDIENT / market card (ING-N-D Meat)
    card_figure(
        P / "ING-N-D.png", OUT / "FIG-INGREDIENT.png", "How to read an Ingredient",
        left=[
            {"fx": 0.14, "fy": 0.075, "term": "Pay chip",
             "gloss": "Colour + emblem match a vendor's recipe — spend this to pay (肉 Meat)."},
            {"fx": 0.20, "fy": 0.83, "term": "Name",
             "gloss": "The plain-language ingredient category."},
        ],
        right=[
            {"fx": 0.55, "fy": 0.46, "term": "Illustration",
             "gloss": "The food itself. Keep it in your Larder until you pay a recipe."},
        ],
    )

    # 4) BOARD at a glance (map-day)
    board_figure(
        ROOT / "exports" / "map-day.png", OUT / "FIG-BOARD.png", "The table at a glance",
        marks=[
            {"n": 1, "tx_f": 0.40, "ty_f": 0.135, "rx_f": 0.315, "ry_f": 0.055},
            {"n": 2, "tx_f": 0.125, "ty_f": 0.435, "rx_f": 0.055, "ry_f": 0.34},
            {"n": 3, "tx_f": 0.53, "ty_f": 0.375, "rx_f": 0.53, "ry_f": 0.30},
            {"n": 4, "tx_f": 0.50, "ty_f": 0.515, "rx_f": 0.635, "ry_f": 0.60},
            {"n": 5, "tx_f": 0.875, "ty_f": 0.90, "rx_f": 0.905, "ry_f": 0.775},
        ],
        legend=[
            {"n": 1, "term": "Tours (Booking) row",
             "gloss": "The face-down Booking deck feeds 4 face-up tours to pick from."},
            {"n": 2, "term": "Four regions in a ring",
             "gloss": "North 北 · Central 中 · South 南 · East 東 — colour + emblem."},
            {"n": 3, "term": "A region's stall row",
             "gloss": "L→R: vendor deck · face-up stall (followers pile here) · market deck · discard."},
            {"n": 4, "term": "The HSR line",
             "gloss": "Links North 北 ↔ South 南 directly, on top of the ring."},
            {"n": 5, "term": "Closing-Time track",
             "gloss": "Roll the die when it fills — a stall closes (faster after dark)."},
        ],
    )
