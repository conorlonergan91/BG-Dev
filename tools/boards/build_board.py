#!/usr/bin/env python3
"""
build_board.py — render boards, tracks, and tokens (themed) for a prototype.

The card pipeline only does cards; but most games also need a **track** (a tug-of-war / score / round
track), **tokens** (markers, resources), and sometimes a **player mat / board**. This renders those as
themed vector SVG -> PNG/PDF, sharing the same themes as the card pipeline so everything matches.

Usage
-----
  # a 7-space tug-of-war track (e.g. Beacon's Tide) with a centred start:
  python build_board.py --type track --spaces 7 --title "Tide" \
      --left-label "Keeper A" --right-label "Keeper B" --theme nautical --out build/tide-track.png

  # a token sheet (markers/resources), tiled for cutting:
  python build_board.py --type tokens --labels "Tide,1st" --shape circle --theme nautical --out build/tokens.png

  # a player mat / board from a small JSON spec (see sample_mat.json):
  python build_board.py --type mat --spec sample_mat.json --theme nautical --out build/mat.png
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import math
import re
import sys
import textwrap
from pathlib import Path

# Scope icons ⦿/⬢/➤ are tofu under cairosvg's toy text API — draw them as SVG shapes inline in the
# player aid, matching the event-card badges (bg-access FIX A).
SCOPE_GLYPH_SHAPE = {"⦿": "ring_dot", "⬢": "hex", "➤": "arrow"}


def _text_w(s, fs):
    """Rough rendered width of a Latin+CJK string at font-size fs (CJK glyphs ~full-width)."""
    return sum((fs if ord(c) > 0x2E7F else fs * 0.52) for c in s)

# themes.py lives with the card pipeline; make it importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import (get_theme, page_gradient, emblem_svg, pick_text_color,  # noqa: E402
                    boost_contrast, resolve_suit, PHASE_STYLES)

DPI = 300


def esc(s):
    return html.escape(str(s or ""), quote=True)


def mm(v):
    return round(v / 25.4 * DPI)


def _save(svg, out: Path, W, H):
    out.parent.mkdir(parents=True, exist_ok=True)
    svg_path = out.with_suffix(".svg")
    svg_path.write_text(svg, encoding="utf-8")
    print(f"[board] wrote {svg_path}")
    try:
        import cairosvg
        if out.suffix.lower() == ".pdf":
            cairosvg.svg2pdf(url=str(svg_path), write_to=str(out))
        else:
            cairosvg.svg2png(url=str(svg_path), write_to=str(out), output_width=W, output_height=H)
        print(f"[board] wrote {out}  ({W}x{H})")
    except Exception:
        print("[board] cairosvg not installed — SVG only. pip install cairosvg (+ brew install cairo).")


# ---- track ------------------------------------------------------------------
def render_track(theme, spaces, title, labels, left_label, right_label):
    cell = 150
    pad = 40
    title_h = 96 if title else 24
    W = pad * 2 + spaces * cell
    H = title_h + cell + 70
    ink, accent, muted = theme["ink"], theme["accent"], theme["muted"]
    center = spaces // 2
    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="28" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']
    if title:
        parts.append(f'<text x="{W/2}" y="{title_h-28}" font-size="52" fill="{ink}" text-anchor="middle" '
                     f'font-family="{theme["title_font"]}" font-weight="bold" letter-spacing="2">{esc(title)}</text>')
    y0 = title_h
    # groove
    parts.append(f'<line x1="{pad}" y1="{y0+cell/2}" x2="{W-pad}" y2="{y0+cell/2}" stroke="{muted}" stroke-width="6" opacity="0.4"/>')
    for i in range(spaces):
        x = pad + i * cell
        is_center = (i == center)
        fill = accent if is_center else "#ffffff"
        op = "0.9" if is_center else "0.65"
        parts.append(f'<circle cx="{x+cell/2}" cy="{y0+cell/2}" r="{cell*0.32}" fill="{fill}" '
                     f'stroke="{ink}" stroke-width="4" opacity="{op}"/>')
        lab = ""
        if labels and i < len(labels):
            lab = labels[i]
        elif is_center:
            lab = "•"
        if lab:
            parts.append(f'<text x="{x+cell/2}" y="{y0+cell/2+14}" font-size="40" fill="{ink}" '
                         f'text-anchor="middle" font-family="{theme["title_font"]}" font-weight="bold">{esc(lab)}</text>')
    if left_label:
        parts.append(f'<text x="{pad}" y="{H-24}" font-size="34" fill="{muted}" '
                     f'font-family="{theme["body_font"]}">◀ {esc(left_label)}</text>')
    if right_label:
        parts.append(f'<text x="{W-pad}" y="{H-24}" font-size="34" fill="{muted}" text-anchor="end" '
                     f'font-family="{theme["body_font"]}">{esc(right_label)} ▶</text>')
    return _svg(W, H, parts), W, H


# ---- tokens -----------------------------------------------------------------
def render_tokens(theme, tokens, shape, diameter_px, cols, legend=False):
    """tokens: list of dicts {label, color, qty, name?}."""
    if legend:
        # A TRUE KEY (not a punch-grid): one row per token TYPE — swatch + glyph, its name (what it MEANS),
        # and the ×qty count — so a player can decode 及/團/成/遺/鐘/停 from this sheet alone (bg-infodesign).
        ink, muted = theme["ink"], theme["muted"]
        tfont, bfont = theme["title_font"], theme["body_font"]
        default = theme["suits"].get("_default", {}).get("color", theme["accent"])
        d = min(diameter_px, 92)
        gap, pad = 22, 34
        row_h = d + gap
        name_x = pad + d + 28
        W = 1320
        H = pad + len(tokens) * row_h + pad
        parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
                 f'<rect width="{W}" height="{H}" rx="26" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']
        for i, t in enumerate(tokens):
            cy = pad + i * row_h + d / 2
            cx = pad + d / 2
            color = t.get("color") or default
            rad = d / 2
            if shape == "square":
                parts.append(f'<rect x="{cx-rad}" y="{cy-rad}" width="{d}" height="{d}" rx="{d*0.14}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            elif shape == "hex":
                pts = " ".join(f"{cx+rad*math.cos(math.radians(a))},{cy+rad*math.sin(math.radians(a))}" for a in range(0, 360, 60))
                parts.append(f'<polygon points="{pts}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            else:
                parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            tcol = pick_text_color(color, dark=ink, light="#ffffff")
            parts.append(f'<text x="{cx}" y="{cy+d*0.11}" font-size="{d*0.34}" fill="{tcol}" text-anchor="middle" '
                         f'font-family="{tfont}" font-weight="bold">{esc(t.get("label",""))}</text>')
            parts.append(f'<text x="{name_x}" y="{cy+10}" font-size="30" fill="{ink}" '
                         f'font-family="{bfont}">{esc(t.get("name","") or t.get("label",""))}</text>')
            parts.append(f'<text x="{W-pad}" y="{cy+10}" font-size="28" fill="{muted}" text-anchor="end" '
                         f'font-family="{tfont}" font-weight="bold">×{int(t.get("qty",1) or 1)}</text>')
        return _svg(W, H, parts), W, H
    expanded = []
    for t in tokens:
        expanded.extend([t] * max(1, int(t.get("qty", 1))))
    gap = 24
    n = len(expanded)
    cols = min(cols, n) or 1
    rows = math.ceil(n / cols)
    d = diameter_px
    W = gap + cols * (d + gap)
    H = gap + rows * (d + gap)
    ink = theme["ink"]
    default = theme["suits"].get("_default", {}).get("color", theme["accent"])
    parts = [f'<rect width="{W}" height="{H}" fill="none"/>']
    for i, t in enumerate(expanded):
        r, c = divmod(i, cols)
        cx = gap + c * (d + gap) + d / 2
        cy = gap + r * (d + gap) + d / 2
        color = t.get("color") or default
        rad = d / 2
        if shape == "square":
            parts.append(f'<rect x="{cx-rad}" y="{cy-rad}" width="{d}" height="{d}" rx="{d*0.14}" fill="{color}" stroke="{ink}" stroke-width="5"/>')
        elif shape == "hex":
            pts = " ".join(f"{cx+rad*math.cos(math.radians(a))},{cy+rad*math.sin(math.radians(a))}" for a in range(0, 360, 60))
            parts.append(f'<polygon points="{pts}" fill="{color}" stroke="{ink}" stroke-width="5"/>')
        else:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{color}" stroke="{ink}" stroke-width="5"/>')
        # luminance-aware glyph colour: white on dark grounds, dark ink on light ones (WCAG) — so the
        # 繁體 labels stay legible on amber/gold/slate tokens instead of low-contrast white.
        tcol = pick_text_color(color, dark=ink, light="#ffffff")
        parts.append(f'<text x="{cx}" y="{cy+d*0.11}" font-size="{d*0.30}" fill="{tcol}" text-anchor="middle" '
                     f'font-family="{theme["title_font"]}" font-weight="bold">{esc(t.get("label",""))}</text>')
    return _svg(W, H, parts), W, H


# ---- mat / board ------------------------------------------------------------
def render_mat(theme, spec):
    W, H = spec.get("width", 1400), spec.get("height", 900)
    ink, accent, muted = theme["ink"], theme["accent"], theme["muted"]
    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="30" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']
    title = spec.get("title")
    if title:
        parts.append(f'<rect x="0" y="0" width="{W}" height="90" fill="{ink}"/>')
        parts.append(f'<text x="40" y="60" font-size="48" fill="#fff" font-family="{theme["title_font"]}" '
                     f'font-weight="bold">{esc(title)}</text>')
    for z in spec.get("zones", []):
        col = z.get("color") or accent
        parts.append(f'<rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="{z["h"]}" rx="18" '
                     f'fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="10 8"/>')
        if z.get("label"):
            parts.append(f'<text x="{z["x"]+16}" y="{z["y"]+40}" font-size="34" fill="{muted}" '
                         f'font-family="{theme["body_font"]}" letter-spacing="1">{esc(z["label"].upper())}</text>')
    for t in spec.get("texts", []):
        parts.append(f'<text x="{t["x"]}" y="{t["y"]}" font-size="{t.get("size",30)}" fill="{ink}" '
                     f'font-family="{theme["body_font"]}">{esc(t["text"])}</text>')
    return _svg(W, H, parts), W, H


def render_aid(theme, spec):
    """A themed player-aid / quick-reference sheet. Height auto-fits the content.
    spec: {title, subtitle?, sections:[{heading, lines:[...]}], width?}

    Layout rhythm (a quick-glance card, not a rulebook): a generous constant gap ABOVE each heading
    separates the blocks, a tight gap under the heading ties it to its lines, and a single line-step
    within a block. The header band GROWS to fit a wrapped subtitle, so a long subtitle wraps instead
    of clipping off the right edge."""
    W = spec.get("width", 1600)
    pad = 56
    ink, accent, text, muted = theme["ink"], theme["accent"], theme["text"], theme["muted"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    wrap_at = max(24, int((W - 2 * pad) / 15))     # ~char width at the body size

    # --- header band: title + a (wrapping) subtitle; the band height follows the subtitle -------------
    sub = spec.get("subtitle", "")
    sub_wrap = max(24, int((W - 2 * pad) / 16))     # subtitle sits at ~30px → a bit narrower budget
    sub_lines = textwrap.wrap(sub, sub_wrap) if sub else []
    title_y, sub_y0, sub_step = 78, 122, 40
    head_h = max(150, (sub_y0 + (len(sub_lines) - 1) * sub_step + 34) if sub_lines else 150)

    # rhythm constants
    GAP_ABOVE_HEAD = 58     # breathing room before each heading (block separation)
    HEAD_TO_LINE = 48       # heading baseline → first line baseline
    LINE_STEP = 40          # per wrapped row within a block

    body = []
    y = head_h + 30
    for si, sec in enumerate(spec.get("sections", [])):
        heading = sec.get("heading", "")
        if any(g in heading for g in SCOPE_GLYPH_SHAPE):
            heading = re.sub(r'\s*\([^)]*[⦿⬢➤][^)]*\)', '', heading)
            heading = re.sub(r'[⦿⬢➤]', '', heading)
        y += GAP_ABOVE_HEAD if si else 24
        body.append(f'<text x="{pad}" y="{y}" font-size="34" fill="{accent}" font-family="{tfont}" '
                    f'font-weight="bold" letter-spacing="1">{esc(heading.upper())}</text>')
        # a slim rule under the heading to anchor the block
        body.append(f'<line x1="{pad}" y1="{y+14}" x2="{W-pad}" y2="{y+14}" stroke="{accent}" '
                    f'stroke-width="2" opacity="0.28"/>')
        y += HEAD_TO_LINE
        first_line = True
        for line in sec.get("lines", []):
            if not any(g in line for g in SCOPE_GLYPH_SHAPE):
                for i, seg in enumerate(textwrap.wrap(line, wrap_at) or [""]):
                    if not first_line or i:
                        y += LINE_STEP
                    first_line = False
                    # Drawn bullet (not the "•" glyph — WenQuanYi Zen Hei lacks it and renders tofu □).
                    if i == 0:
                        body.append(f'<circle cx="{pad+8}" cy="{y-9}" r="6" fill="{accent}"/>')
                    body.append(f'<text x="{pad+30}" y="{y}" font-size="28" fill="{text}" '
                                f'font-family="{bfont}">{esc(seg)}</text>')
            else:
                # scope-glyph line: char-budget wrap treating each glyph as a ~2-char token, then emit
                # text runs interleaved with DRAWN scope shapes (no tofu). (bg-access FIX A)
                # Filter empty tokens so consecutive spaces don't inject wide phantom gaps.
                plines, cur, ln = [], [], 0
                for tok in (t for t in line.split(" ") if t != ""):
                    w = 2 if tok in SCOPE_GLYPH_SHAPE else len(tok)
                    if cur and ln + 1 + w > wrap_at:
                        plines.append(cur); cur, ln = [], 0
                    cur.append(tok); ln += (1 if len(cur) > 1 else 0) + w
                if cur:
                    plines.append(cur)
                for i, toks in enumerate(plines):
                    if not first_line or i:
                        y += LINE_STEP
                    first_line = False
                    if i == 0:
                        body.append(f'<circle cx="{pad+8}" cy="{y-9}" r="6" fill="{accent}"/>')
                    x = pad + 30
                    j = 0
                    while j < len(toks):
                        if toks[j] in SCOPE_GLYPH_SHAPE:
                            x += 6
                            body.append(emblem_svg(SCOPE_GLYPH_SHAPE[toks[j]], x + 12, y - 9, 12, accent, stroke=ink))
                            x += 34
                            j += 1
                        else:
                            run = []
                            while j < len(toks) and toks[j] not in SCOPE_GLYPH_SHAPE:
                                run.append(toks[j]); j += 1
                            seg = " ".join(run)
                            body.append(f'<text x="{x}" y="{y}" font-size="28" fill="{text}" '
                                        f'font-family="{bfont}">{esc(seg)}</text>')
                            x += _text_w(seg + " ", 28)
    H = y + pad
    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="28" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>',
             f'<rect x="0" y="0" width="{W}" height="{head_h}" fill="{ink}"/>',
             f'<rect x="0" y="{head_h}" width="{W}" height="6" fill="{accent}"/>',
             f'<text x="{pad}" y="{title_y}" font-size="52" fill="#fff" font-family="{tfont}" '
             f'font-weight="bold" letter-spacing="1">{esc(spec.get("title",""))}</text>']
    if sub_lines:
        # subtitle sits on the dark `ink` header band — ensure ≥4.5:1 (lightens the accent only if needed,
        # so themes that already pass are untouched).
        sub_col = boost_contrast(accent, ink, 4.5)
        for i, sl in enumerate(sub_lines):
            parts.append(f'<text x="{pad}" y="{sub_y0 + i*sub_step}" font-size="30" fill="{sub_col}" '
                         f'font-family="{tfont}" font-style="italic">{esc(sl)}</text>')
    parts += body
    return _svg(W, H, parts), W, H


# ---- region-ring map (NEUTRAL shared N-player board, V7) --------------------
def render_regionmap(theme, spec, phase="day"):
    """The shared TABLE board — V7 NEUTRAL board for 3-6 players (rebuilt from the 2p across-the-table
    centrepiece). ONE orientation, readable from any seat: no two-seat mirror, no per-edge clock rails.

      • THE CLOCK is DECK-DRIVEN — the 開團 Booking deck IS the clock. A full-width clock band carries the
        DAY deck (out → 黃昏 DUSK → flip to night) and the NIGHT deck (out → 末班車 LAST TRAIN → game ends),
        the seeded boundary cards, and the shared FACE-UP Booking row players draw from. There is NO
        numbered vendor-claims track (deleted).
      • THE 4-REGION DIAMOND (北 top · 中 left · 東 right · 南 bottom) is the shared map, each panel carrying
        colour + emblem + 繁體 (dual-coded WHERE), its ingredient chips, its PHASE-appropriate FACE-UP vendor
        slots, and a MARKET deck. The HSR spine + 停 Scheduled-Maintenance slot run down the centre; every
        agent starts in Taipei (北 hub).
      • NO Ingredient-Supply section (ingredients are CARDS in the market decks now).
      • Bottom band: the shared FOLLOWERS supply pool + Trending markers, a HOW-TO-READ legend, and the
        per-player-count setup table (Booking-deck sizes / vendor slots / Followers supply).
    Renders in two states (--phase day|night) mirroring the dusk flip: warm ☀日 vs neon ☾夜 chrome (drawn
    sun/moon, never a font glyph). TA-specific — only games/travel-agents/make.sh calls --type regionmap."""
    W, H = 2280, 1680
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]

    ps = PHASE_STYLES.get((phase or "day").lower(), PHASE_STYLES["day"])
    is_night = (phase or "day").lower() == "night"
    ground = ps["page"]
    frame = ps["frame"]
    badge_emblem = ps.get("emblem", "sun")
    badge_char = "夜" if is_night else "日"
    badge_word = "NIGHT · 夜市" if is_night else "DAY · 早"
    steel = "#4A5A72"
    day_amber = PHASE_STYLES["day"]["frame"]
    night_violet = PHASE_STYLES["night"]["tag_fill"]
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")       # Followers
    booking_col = theme["suits"].get("booking", {}).get("color", "#3A6EA5")
    gold = theme["suits"].get("signature", {}).get("color", "#C9A227")     # Trending / apex

    CARD_W, CARD_H = 138, 193      # 63.5 × 88.9 mm poker card
    FOL_R = 24                     # Ø12 mm Followers disc
    TREND_R = 30                   # 18 mm Trending marker
    PAWN_R = 26                    # 15 mm agent pawn

    parts = [f'<defs>{page_gradient(theme, "pg", ground)}</defs>',
             f'<rect width="{W}" height="{H}" rx="30" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>',
             # inner hairline frame — the SAME house treatment as the character boards (render_playerboard),
             # so the shared table reads as the same illustrated hand. Uses the phase `frame` colour so the
             # hairline is warm gold by day / neon by night; its top edge is hidden under the title band.
             f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="22" fill="none" stroke="{frame}" '
             f'stroke-width="2" opacity="0.5"/>']

    # ------------------------------------------------------------------ helpers
    def _star(cx, cy, r, fill, stroke="none"):
        pts = " ".join(
            f'{cx + (r if i % 2 == 0 else r*0.42)*math.cos(-math.pi/2 + i*math.pi/5):.1f},'
            f'{cy + (r if i % 2 == 0 else r*0.42)*math.sin(-math.pi/2 + i*math.pi/5):.1f}'
            for i in range(10))
        sw = f' stroke="{stroke}" stroke-width="2"' if stroke != "none" else ""
        return f'<polygon points="{pts}" fill="{fill}"{sw}/>'

    def zone(x, y, w, h, label, glyph="", desc="", fill_op=0.42, col=None):
        col = col or frame
        z = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#ffffff" opacity="{fill_op}"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none" stroke="{col}" '
             f'stroke-width="3" stroke-dasharray="11 8"/>',
             f'<text x="{x+20}" y="{y+38}" font-size="26" fill="{ink}" font-family="{tfont}" '
             f'font-weight="bold" letter-spacing="1">{esc(label.upper())}</text>']
        if desc:
            z.append(f'<text x="{x+20}" y="{y+66}" font-size="20" fill="{muted}" '
                     f'font-family="{bfont}">{esc(desc)}</text>')
        if glyph:
            z.append(glyph)
        return "".join(z)

    def facedown_deck(x, y, w, h, col, label, sub=""):
        d = [f'<rect x="{x+6}" y="{y+6}" width="{w}" height="{h}" rx="12" fill="{ink}" opacity="0.18"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" stroke="{ink}" stroke-width="3"/>',
             f'<rect x="{x+8}" y="{y+8}" width="{w-16}" height="{h-16}" rx="8" fill="none" '
             f'stroke="#ffffff" stroke-width="2" opacity="0.5"/>']
        tc = pick_text_color(col, dark=ink, light="#ffffff")
        d.append(f'<text x="{x+w/2}" y="{y+h/2-2}" font-size="26" fill="{tc}" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold">{esc(label)}</text>')
        if sub:
            d.append(f'<text x="{x+w/2}" y="{y+h/2+28}" font-size="18" fill="{tc}" text-anchor="middle" '
                     f'font-family="{bfont}" opacity="0.9">{esc(sub)}</text>')
        return "".join(d)

    def card_slot(x, y, emb, rcol, tag="vendor", mmlab="63×89mm", w=CARD_W, h=CARD_H):
        s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" '
             f'opacity="0.55" stroke="{rcol}" stroke-width="2" stroke-dasharray="8 6"/>',
             emblem_svg(emb, x + w/2, y + h/2 - 8, 26, rcol),
             f'<text x="{x+w/2}" y="{y+h-40}" font-size="20" fill="{muted}" text-anchor="middle" '
             f'font-family="{bfont}">{esc(tag)}</text>',
             f'<text x="{x+w/2}" y="{y+h-16}" font-size="16" fill="{muted}" text-anchor="middle" '
             f'font-family="{bfont}" font-style="italic">{esc(mmlab)}</text>']
        return "".join(s)

    # ================================================================== TITLE
    title = spec.get("title", "")
    parts.append(f'<rect x="0" y="0" width="{W}" height="74" fill="{ink}"/>')
    parts.append(f'<rect x="0" y="74" width="{W}" height="5" fill="{frame}"/>')
    parts.append(f'<text x="40" y="52" font-size="40" fill="#fff" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(title)}</text>')
    bx = W - 260
    parts.append(f'<rect x="{bx}" y="18" width="220" height="40" rx="20" fill="{frame}"/>')
    parts.append(emblem_svg(badge_emblem, bx + 32, 38, 14, "#fff"))
    parts.append(f'<text x="{bx + 128}" y="46" font-size="24" fill="#fff" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(badge_char + " " + badge_word)}</text>')
    parts.append(f'<text x="{bx-24}" y="46" font-size="22" fill="#fff" text-anchor="end" '
                 f'font-family="{bfont}" opacity="0.9">{esc(spec.get("players","3-6"))} players · read from any seat</text>')

    # ================================================================== CLOCK BAND (deck-driven)
    cbx, cby, cbw, cbh = 40, 92, W - 80, 300
    clk = spec.get("clock_model", {}) or {}
    parts.append(zone(cbx, cby, cbw, cbh, "The Clock — the 開團 Booking deck drives day → night",
                      desc="No numbered track: the deck IS the clock. Seed 黃昏 / 末班車 at each deck's bottom.",
                      col=frame, fill_op=0.5))
    ddw, ddh = 132, 178
    drow_y = cby + 96
    # DAY deck + its 黃昏 boundary
    dx1 = cbx + 34
    day_on = not is_night
    parts.append(facedown_deck(dx1, drow_y, ddw, ddh, day_amber, "DAY 開團", "draw a Booking"))
    # boundary caption UNDER the deck (compact, left-anchored so it never overflows a fixed box)
    parts.append(emblem_svg("sun", dx1+12, drow_y+ddh+30, 12, day_amber))
    parts.append(f'<text x="{dx1+30}" y="{drow_y+ddh+37}" font-size="17" '
                 f'fill="{ink}" font-family="{tfont}" font-weight="bold">out &#8594; 黃昏 DUSK</text>')
    parts.append(f'<text x="{dx1+30}" y="{drow_y+ddh+59}" font-size="15" fill="{muted}" '
                 f'font-family="{bfont}">flip to night</text>')
    # arrow
    ax1 = dx1 + ddw + 26
    parts.append(f'<text x="{ax1+22}" y="{drow_y+ddh/2+14}" font-size="52" fill="{muted}" '
                 f'font-family="{tfont}" font-weight="bold">&#8594;</text>')
    # NIGHT deck + its 末班車 boundary
    dx2 = ax1 + 70
    parts.append(facedown_deck(dx2, drow_y, ddw, ddh, night_violet, "NIGHT 開團", "draw a Booking"))
    parts.append(emblem_svg("moon", dx2+12, drow_y+ddh+30, 12, night_violet))
    parts.append(f'<text x="{dx2+30}" y="{drow_y+ddh+37}" font-size="17" '
                 f'fill="{ink}" font-family="{tfont}" font-weight="bold">out &#8594; 末班車 LAST TRAIN</text>')
    parts.append(f'<text x="{dx2+30}" y="{drow_y+ddh+59}" font-size="15" fill="{muted}" '
                 f'font-family="{bfont}">finish the round, then end</text>')
    # shared FACE-UP Booking row
    frx = dx2 + ddw + 80
    parts.append(f'<text x="{frx}" y="{drow_y-8}" font-size="22" fill="{booking_col}" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">FACE-UP BOOKINGS (shared) — draw 1, then refill</text>')
    fsw, fsh = 118, 165
    for i in range(4):
        parts.append(card_slot(frx + i*(fsw+14), drow_y+16, "ticket", booking_col,
                                tag="booking", mmlab="63×89", w=fsw, h=fsh))
    # active-phase call-out on the right
    aphase = "DAY deck depleting → DUSK next" if not is_night else "NIGHT deck depleting → LAST TRAIN next"
    parts.append(f'<text x="{cbx+cbw-22}" y="{cby+cbh-18}" font-size="21" fill="{frame}" text-anchor="end" '
                 f'font-family="{tfont}" font-weight="bold" font-style="italic">this side: {esc(aphase)}</text>')

    # ================================================================== REGION DIAMOND
    PW_NS, PW_CE, PH = 640, 560, 340
    centers = {"north": (1140, 560), "central": (520, 862), "east": (1760, 862), "south": (1140, 1164)}
    pwidth = {"north": PW_NS, "south": PW_NS, "central": PW_CE, "east": PW_CE}

    def tl(key):
        cx, cy = centers[key]
        return cx - pwidth[key] / 2, cy - PH / 2

    for a, b in spec.get("ring", []):
        if a in centers and b in centers:
            (x1, y1), (x2, y2) = centers[a], centers[b]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{muted}" '
                         f'stroke-width="13" stroke-linecap="round" opacity="0.5"/>')
    # HSR double-rail spine (North↔South)
    hsr = spec.get("hsr", [])
    if len(hsr) == 2 and all(k in centers for k in hsr):
        (x1, y1), (x2, y2) = centers[hsr[0]], centers[hsr[1]]
        sy, ey = y1 + PH / 2 + 6, y2 - PH / 2 - 6
        off = 9
        for s in (off, -off):
            parts.append(f'<line x1="{x1+s}" y1="{sy}" x2="{x2+s}" y2="{ey}" stroke="{steel}" '
                         f'stroke-width="6" stroke-linecap="round"/>')
        for i in range(1, 11):
            ty = sy + (ey - sy) * i / 11
            parts.append(f'<line x1="{x1-(off+5)}" y1="{ty}" x2="{x1+(off+5)}" y2="{ty}" '
                         f'stroke="{steel}" stroke-width="4"/>')
        # region STOPS — a stop node where the spine meets North (top) and South (bottom), so the HSR reads
        # as a track WITH stops, not just a decorative rail.
        for sty in (sy, ey):
            parts.append(f'<circle cx="{x1}" cy="{sty}" r="11" fill="#ffffff" stroke="{steel}" stroke-width="5"/>')
        my = (sy + ey) / 2
        parts.append(f'<rect x="{x1-150}" y="{my-104}" width="300" height="44" rx="22" '
                     f'fill="{steel}" stroke="#fff" stroke-width="2"/>')
        parts.append(f'<text x="{x1}" y="{my-74}" font-size="23" fill="#fff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">HSR 高鐵 · 北–南</text>')
        if spec.get("hsr_closed_marker"):
            slate = "#8A8F98"
            # NO separate drop-slot placeholder (CD steer): the Scheduled-Maintenance EVENT CARD is played
            # ONTO the track itself. Draw a small printed 停 badge ON the spine + a caption saying the event
            # sits here — a LABEL on the track, never an empty dashed slot that reads as "place a card box".
            mky = my - 2
            # translucent scrim under the caption so it stays high-contrast where it crosses the rails
            # (the map-board legibility rail: drop a scrim under text over busy track art).
            parts.append(f'<rect x="{x1-176}" y="{mky+34}" width="352" height="52" rx="12" '
                         f'fill="#ffffff" opacity="0.82"/>')
            parts.append(f'<circle cx="{x1}" cy="{mky}" r="23" fill="{slate}" stroke="#fff" stroke-width="3"/>')
            parts.append(f'<text x="{x1}" y="{mky+11}" font-size="27" fill="#fff" text-anchor="middle" '
                         f'font-family="{tfont}" font-weight="bold">停</text>')
            parts.append(f'<text x="{x1}" y="{mky+56}" font-size="17" fill="{ink}" text-anchor="middle" '
                         f'font-family="{tfont}" font-weight="bold">Scheduled-Maintenance event</text>')
            parts.append(f'<text x="{x1}" y="{mky+78}" font-size="15" fill="{muted}" text-anchor="middle" '
                         f'font-family="{bfont}" font-style="italic">played onto the HSR track</text>')

    hub_hanzi = spec.get("hub_hanzi", "台北")
    for r in spec.get("regions", []):
        key = r["key"]
        if key not in centers:
            continue
        PWc = pwidth[key]
        X, Y = tl(key)
        rcol = r.get("color", accent)
        emb = r.get("emblem", "circle")
        rad = 18
        parts.append(f'<rect x="{X-4}" y="{Y-4}" width="{PWc+8}" height="{PH+8}" rx="{rad+4}" '
                     f'fill="none" stroke="{frame}" stroke-width="3" opacity="0.7"/>')
        parts.append(f'<rect x="{X}" y="{Y}" width="{PWc}" height="{PH}" rx="{rad}" '
                     f'fill="#ffffff" stroke="{rcol}" stroke-width="4"/>')
        hh = 56
        parts.append(f'<path d="M{X} {Y+rad} a {rad} {rad} 0 0 1 {rad} -{rad} h {PWc-2*rad} '
                     f'a {rad} {rad} 0 0 1 {rad} {rad} v {hh-rad} h -{PWc} z" fill="{rcol}"/>')
        parts.append(emblem_svg(emb, X + 34, Y + 28, 16, "#ffffff"))
        parts.append(f'<text x="{X+62}" y="{Y+39}" font-size="34" fill="#fff" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(r.get("name",""))}</text>')
        if r.get("start"):
            sp_w = 176
            parts.append(f'<rect x="{X+PWc-sp_w-14}" y="{Y+12}" width="{sp_w}" height="32" rx="16" '
                         f'fill="#ffffff" opacity="0.95"/>')
            parts.append(f'<text x="{X+PWc-sp_w/2-14}" y="{Y+34}" font-size="19" fill="{rcol}" '
                         f'text-anchor="middle" font-family="{tfont}" font-weight="bold" '
                         f'letter-spacing="1">START · {esc(hub_hanzi)}</text>')

        # ingredient chips (shape + 繁體 + short EN) — a compact row high under the header, so the
        # vendor row (below) never collides with them even in the narrow CENTRAL/EAST panels.
        chips = r.get("chips", [])
        chip_r = 22
        ccy = Y + hh + 40
        for i, sp in enumerate(chips):
            suit = resolve_suit(theme, sp.get("id", "")) if sp.get("id") in theme["suits"] else {}
            scol = suit.get("color", rcol)
            semb = suit.get("emblem", "circle")
            cx = X + 44 + i * 96
            tcol = pick_text_color(scol, dark=ink, light="#ffffff")
            parts.append(emblem_svg(semb, cx, ccy, chip_r, scol, stroke=ink))
            parts.append(f'<text x="{cx}" y="{ccy + chip_r*0.34}" font-size="26" fill="{tcol}" '
                         f'text-anchor="middle" font-family="{bfont}" font-weight="bold">{esc(sp.get("label",""))}</text>')
            parts.append(f'<text x="{cx}" y="{ccy + chip_r + 24}" font-size="17" fill="{text}" '
                         f'text-anchor="middle" font-family="{bfont}">{esc(sp.get("en",""))}</text>')

        # agent-pawn spaces at the common start (Taipei)
        if r.get("start"):
            parts.append(f'<text x="{X+52}" y="{Y+176}" font-size="16" fill="{rcol}" text-anchor="middle" '
                         f'font-family="{tfont}" font-weight="bold" letter-spacing="1">PAWNS · 台北</text>')
            for i in range(3):
                px, py = X + 52 + (i % 2)*56, Y + 208 + (i // 2)*54
                parts.append(f'<circle cx="{px}" cy="{py}" r="{PAWN_R}" fill="#ffffff" opacity="0.6" '
                             f'stroke="{rcol}" stroke-width="2" stroke-dasharray="6 5"/>')
                parts.append(f'<circle cx="{px}" cy="{py-7}" r="9" fill="{rcol}" opacity="0.55"/>')
                parts.append(f'<rect x="{px-9}" y="{py+1}" width="18" height="15" rx="5" fill="{rcol}" opacity="0.55"/>')
            parts.append(f'<text x="{X+80}" y="{Y+322}" font-size="14" fill="{muted}" text-anchor="middle" '
                         f'font-family="{bfont}" font-style="italic">all agents · 15mm</text>')

        # functional row: PHASE-appropriate FACE-UP vendor slot(s) + the MARKET deck. Uses SMALLER map
        # placeholders (MW×MH) so the row sits well below the chip row (clears the CENTRAL crowding) while
        # the mm caption keeps the real 63×89 print intent.
        MW, MH = 112, 157
        slots_n = int(r.get("slots_n", 1))
        row_y = Y + PH - MH - 20
        gap = 14
        n_cells = slots_n + 1
        block_w = n_cells * MW + (n_cells - 1) * gap
        x_start = X + PWc - 26 - block_w
        parts.append(f'<text x="{x_start}" y="{row_y-10}" font-size="17" fill="{rcol}" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">FACE-UP ×{slots_n}</text>')
        for i in range(slots_n):
            sx = x_start + i * (MW + gap)
            parts.append(card_slot(sx, row_y, emb, rcol, tag="vendor", w=MW, h=MH))
        dxk = x_start + slots_n * (MW + gap)
        parts.append(f'<text x="{dxk+MW/2}" y="{row_y-10}" font-size="17" fill="{frame}" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="1">MARKET</text>')
        parts.append(facedown_deck(dxk, row_y, MW, MH, frame, badge_char, "night" if is_night else "day"))

    # ================================================================== BOTTOM BAND
    bb_y = 1360
    # --- LEFT: Followers supply + Trending markers ---
    fsx, fsw2, fsh2 = 40, 1080, 300
    parts.append(zone(fsx, bb_y, fsw2, fsh2, "Followers supply 粉 · Trending 爆紅",
                      desc="shared reserves — take Followers when you Promote; Trending drops on a Gone-Viral vendor",
                      col=frame, fill_op=0.5))
    # Followers cluster
    flx, fly = fsx + 40, bb_y + 150
    parts.append(f'<text x="{flx}" y="{fly-52}" font-size="20" fill="{violet}" font-family="{tfont}" '
                 f'font-weight="bold">FOLLOWERS 粉 · Ø12mm (see table →)</text>')
    for i in range(12):
        ox = flx + (i % 6) * 52
        oy = fly + (0 if i < 6 else 46)
        parts.append(f'<circle cx="{ox}" cy="{oy}" r="{FOL_R}" fill="{violet}" stroke="{ink}" stroke-width="2"/>')
    # Trending cluster
    ttx, tty = fsx + fsw2 - 360, bb_y + 150
    parts.append(f'<text x="{ttx}" y="{tty-52}" font-size="20" fill="{gold}" font-family="{tfont}" '
                 f'font-weight="bold">TRENDING 爆紅 · 18mm ×4</text>')
    for i in range(4):
        ox = ttx + (i % 2) * 96 + 24
        oy = tty + (0 if i < 2 else 62)
        parts.append(_star(ox, oy, TREND_R, gold, stroke=ink))
        parts.append(f'<text x="{ox}" y="{oy+8}" font-size="18" fill="#fff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">紅</text>')

    # --- RIGHT: how-to-read legend + per-count setup table ---
    hrx, hrw = 1160, 1080
    parts.append(zone(hrx, bb_y, hrw, fsh2, "How to read · setup by player count", col=frame, fill_op=0.5))
    legend = [
        "One neutral board — read from any seat. Your OWN pieces (the Followers dial,",
        "your 成團/取消 piles, your Rave-Reviews) live on YOUR character board, not here.",
        "Placeholders shown at real component size (mm labelled).",
    ]
    for i, ln in enumerate(legend):
        parts.append(f'<text x="{hrx+22}" y="{bb_y+92+i*26}" font-size="19" fill="{text}" '
                     f'font-family="{bfont}">{esc(ln)}</text>')
    # per-count table
    decks = spec.get("booking_deck_sizes", {}) or {}
    supply = spec.get("followers_supply", {}) or {}
    vslots = spec.get("vendor_slots", {}) or {}
    counts = ["3", "4", "5", "6"]
    tx0, ty0 = hrx + 24, bb_y + 190
    colw = (hrw - 48) / 5
    heads = ["players", "DAY deck", "NIGHT deck", "vendor slots N/C/S/E", "Followers"]
    for c, htxt in enumerate(heads):
        parts.append(f'<text x="{tx0 + colw*(c+0.5):.0f}" y="{ty0}" font-size="18" fill="{frame}" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(htxt)}</text>')
    for ri, n in enumerate(counts):
        ry = ty0 + 30 + ri*24
        d = decks.get(n, {})
        vs = vslots.get(n, {})
        vs_str = "/".join(str(vs.get(k, "-")) for k in ("N", "C", "S", "E")) if vs else "-"
        cells = [f"{n}p" + (" (home)" if n == "4" else ""), str(d.get("day", "-")),
                 str(d.get("night", "-")), vs_str, str(supply.get(n, "-"))]
        hot = (n == "4")
        weight = ' font-weight="bold"' if hot else ''
        for c, cell in enumerate(cells):
            parts.append(f'<text x="{tx0 + colw*(c+0.5):.0f}" y="{ry}" font-size="18" '
                         f'fill="{ink if not hot else frame}" text-anchor="middle" '
                         f'font-family="{bfont}"{weight}>{esc(cell)}</text>')

    return _svg(W, H, parts), W, H


# ---- per-player CHARACTER BOARD (landscape player mat) ----------------------
def _slugify(s: str) -> str:
    s = re.sub(r'^\s*the\s+', '', (s or "").strip(), flags=re.I)
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s or "char"


def _pb_chip(cx, cy, txt, col, tfont, r=19):
    """A small white numeric/keyword chip (a legit 'icon' when it's a number/keyword) — always ASCII
    digits + '+'/'-'/'×' (all font-covered; NO U+2212 or ≥ → no tofu)."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{col}" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy+r*0.36:.0f}" font-size="{r*1.15:.0f}" fill="{col}" text-anchor="middle" '
            f'font-family="{tfont}" font-weight="bold">{esc(txt)}</text>')


def _pb_kit_glyph(cx, cy, code, col, ink, tfont):
    """The Travel-Agents CHARACTER icon vocabulary — ONE consistent drawn glyph per ability/flaw code,
    the same meaning everywhere. Icons are memory anchors; the block TEXT carries the precise rule.
    Every shape is DRAWN (no font glyphs) so nothing renders tofu (bg-infodesign / bg-access)."""
    e = emblem_svg
    if code == "discount_home":       # house + '-1' → cheaper on home turf
        return e("home", cx, cy, 27, col, stroke=ink) + _pb_chip(cx+32, cy+24, "-1", col, tfont)
    if code == "away_tax":            # out-of-home arrow + '+2' → costs +2 ingredients off your patch
        return e("arrow", cx, cy, 25, col, stroke=ink) + _pb_chip(cx+32, cy+24, "+2", col, tfont)
    if code == "travel_draw_left":    # ring + back-chevron → draw the region you LEFT
        return (f'<circle cx="{cx}" cy="{cy}" r="27" fill="none" stroke="{col}" stroke-width="4"/>'
                f'<polyline points="{cx+8},{cy-13} {cx-9},{cy} {cx+8},{cy+13}" fill="none" '
                f'stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    if code == "visit_keep3":         # three stacked cards + '3' → keep all 3 on a Visit
        cards = "".join(f'<rect x="{cx-26+i*10:.0f}" y="{cy-22-i*6:.0f}" width="32" height="44" rx="6" '
                        f'fill="#ffffff" stroke="{col}" stroke-width="3"/>' for i in range(3))
        return cards + _pb_chip(cx+40, cy+22, "3", col, tfont)
    if code == "hazard_twice_visit":  # warning triangle + '×2' → hazards fire twice on his Visit
        return e("triangle", cx, cy, 25, col, stroke=ink) + _pb_chip(cx+34, cy+24, "×2", col, tfont)
    if code == "promote3":            # (legacy v6.4) buzz sparkle + '3' → Promote places 3 Buzz
        return e("spark", cx, cy, 26, col) + _pb_chip(cx+34, cy+24, "3", col, tfont)
    if code == "start_max_4":         # 網紅: the Followers-max DIAL starts HIGH — a gauge reading '4'
        arc = (f'<path d="M{cx-26} {cy+10} A 26 26 0 0 1 {cx+26} {cy+10}" fill="none" '
               f'stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
        needle = f'<line x1="{cx}" y1="{cy+10}" x2="{cx+17}" y2="{cy-16}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
        hub = f'<circle cx="{cx}" cy="{cy+10}" r="5" fill="{col}"/>'
        return arc + needle + hub + _pb_chip(cx+38, cy+22, "4", col, tfont)
    if code == "win_ties":            # 大哥: two EQUAL committed stacks + '=' → a tie is enough to claim
        bars = (f'<rect x="{cx-24}" y="{cy-16}" width="17" height="44" rx="3" fill="{col}" opacity="0.5"/>'
                f'<rect x="{cx+7}" y="{cy-16}" width="17" height="44" rx="3" fill="{col}"/>')
        return bars + _pb_chip(cx+46, cy-2, "=", col, tfont)
    if code == "travel_anywhere":     # 阿嬤 elder pass: a hub linked to all FOUR regions → go anywhere in one Travel
        s = f'<circle cx="{cx}" cy="{cy}" r="9" fill="{col}"/>'
        for dx, dy in [(1, -1), (-1, -1), (1, 1), (-1, 1)]:
            ex, ey = cx + dx*27, cy + dy*22
            s += f'<line x1="{cx}" y1="{cy}" x2="{ex}" y2="{ey}" stroke="{col}" stroke-width="3.5" opacity="0.85"/>'
            s += e("diamond", ex, ey, 9, col, stroke=ink)
        return s
    if code == "goes_last":           # a queue of 3 dots, last one ringed → take the last seat
        dots = "".join(f'<circle cx="{cx-26+i*26:.0f}" cy="{cy}" r="9" fill="{col}" '
                       f'opacity="{0.38 if i<2 else 1}"/>' for i in range(3))
        return dots + f'<circle cx="{cx+26}" cy="{cy}" r="15" fill="none" stroke="{col}" stroke-width="3"/>'
    if code == "bribe_margin1":       # two bars, yours taller by one + '1' → win the fight at a 1 lead
        return (f'<rect x="{cx-22}" y="{cy-4}" width="15" height="30" rx="3" fill="{col}" opacity="0.42"/>'
                f'<rect x="{cx+3}" y="{cy-20}" width="15" height="46" rx="3" fill="{col}"/>'
                + _pb_chip(cx+42, cy-2, "1", col, tfont))
    if code == "none":                # a struck-through ring → no drawback
        return (f'<circle cx="{cx}" cy="{cy}" r="23" fill="none" stroke="{col}" stroke-width="3" opacity="0.6"/>'
                f'<line x1="{cx-13}" y1="{cy}" x2="{cx+13}" y2="{cy}" stroke="{col}" '
                f'stroke-width="5" stroke-linecap="round" opacity="0.7"/>')
    return e("spark", cx, cy, 24, col)


def _pb_headline(txt):
    """Split a CSV ability/flaw sentence into a short KEYWORD (before the em-dash) + one terse clause.
    Icon-first boards carry only these; the rulebook carries the full rule."""
    t = str(txt or "").strip()
    if "—" in t:
        head, rest = t.split("—", 1)
    elif " - " in t:
        head, rest = t.split(" - ", 1)
    else:
        head, rest = t, ""
    head = head.strip().rstrip(".")
    rest = rest.strip()
    if rest:
        rest = re.split(r'(?<=[.);])\s', rest)[0].strip()
    return head, rest


def _embed_fig_png(fig_id, x, y, w, h, mockups_dir, rx=16):
    """TA-only art-mock embed. If a mock-up PNG `<mockups_dir>/<fig_id>.png` exists, return an SVG
    <image> for it — base64 **data URI** (so the render stays self-contained through cairosvg→PNG; a
    file-path href would not survive rasterisation), clipped to a rounded rect and sized to the slot
    with preserveAspectRatio="xMidYMid meet" (letterboxes, never crops the character). Returns None
    when there is no mock-up on disk, so the caller falls back to the dashed placeholder — this keeps a
    mock-up-free board byte-for-byte the pre-existing behaviour (aside from the reshaped slot)."""
    if not mockups_dir:
        return None
    p = Path(mockups_dir) / f"{fig_id}.png"
    if not p.is_file():
        return None
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    cid = "figclip-" + re.sub(r'[^A-Za-z0-9]+', '-', fig_id).strip('-').lower()
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<image href="data:image/png;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid meet" clip-path="url(#{cid})"/>')


def render_playerboard(theme, row, mockups_dir=None):
    """One landscape CHARACTER BOARD per agent (V7 · CD REDESIGN 2026-08 v2 · icon-first, language-agnostic).

    A4-LANDSCAPE (297×210 mm @ 300 DPI = 3508×2480 px). Two TRUE poker-card footprints
    (63.5×88.9 mm = 750×1050 px each) sit on the right so real Booking cards stack on them, with a
    full-height character image + the Followers dial down the left column.

    Layout (v2):
       • TITLE band — English name TOP-LEFT (e.g. "The Globetrotter"); 漢字 TOP-RIGHT with the Tâi-lô
         romanisation as a subtitle directly under it (阿嬤 / A-má); the ABILITY + FLAW ICON-ONLY medallions
         (drawn glyphs, NO keyword/explainer text) sit CENTRED in the band — ability teal LEFT, flaw
         vermilion RIGHT (fixed position + hue tells which-is-which without a label).
       • LEFT column, full height — the character IMAGE (embedded mock-up when present, else placeholder)
         at top, and UNDER it the FOLLOWERS DIAL: an actual dial FACE (a 0–8 notched arc with a detent at
         each number, a centre pivot + dashed groove ring where a 3D-printed rotating knob seats, and a
         per-character MAX/START marker at the start value — 2, or 4 for 網紅 via start_max_4).
       • RIGHT column — a short funny PROSE one-liner (from `blurb`) under the banner, then the TWO
         card-EXACT-footprint drop zones CANCELLED 取消 · COMPLETE 成團 (a real Booking card stacks on each).

    REMOVED in this v2 (all moved to the rulebook): the bottom footer (scoring line + hand-limit-3 +
    Rave-Reviews + the dial +1/Travel & lost-war drop rule), the "icons are reminders" caption, and the
    old FOLLOWERS card-zone (Followers is no longer a card zone — it is the dial under the image).

    TA-specific: only games/travel-agents/make.sh calls --type playerboard, and it renders only rows that
    carry ability_code + flaw_code — so Beacon and every other game are untouched."""
    # A4 landscape at 300 DPI. mm() guarantees the card zones are EXACTLY one poker footprint.
    W, H = mm(297), mm(210)                       # 3508 × 2480
    CARD_W, CARD_H = mm(63.5), mm(88.9)           # 750 × 1050 — a real poker card sits on each zone
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    gold = theme["suits"].get("signature", {}).get("color", "#C9A227")
    teal = theme["suits"].get("central", {}).get("color", "#1F8A7A")      # ABILITY hue
    vermilion = theme["suits"].get("north", {}).get("color", "#D64545")   # FLAW hue
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")       # Followers hue
    booking_col = theme["suits"].get("booking", {}).get("color", "#3A6EA5")
    gold_pile, taupe = gold, muted

    name = row.get("name", "")                    # Tâi-lô
    hanzi = row.get("hanzi", "")                   # 漢字
    name_en = str(row.get("name_en", "")).strip()  # English
    blurb = str(row.get("blurb", "")).strip()
    acode = str(row.get("ability_code", "")).strip().lower()
    fcode = str(row.get("flaw_code", "")).strip().lower()
    slug = _slugify(name_en or row.get("id", ""))
    dial_start = 4 if acode == "start_max_4" else 2   # 網紅 starts at 4; the dial floors here too

    M = 70                                         # outer margin
    P = [f'<defs>{page_gradient(theme, "pg")}</defs>',
         f'<rect width="{W}" height="{H}" rx="34" fill="url(#pg)" stroke="{ink}" stroke-width="7"/>',
         f'<rect x="30" y="30" width="{W-60}" height="{H-60}" rx="24" fill="none" '
         f'stroke="{gold}" stroke-width="2" opacity="0.5"/>']

    # ==================== TITLE band: English TOP-LEFT · icons CENTRE · 漢字 + Tâi-lô TOP-RIGHT ==========
    ox, hr, hh = 18, 28, 250
    P.append(f'<path d="M{ox} {18+hr} a {hr} {hr} 0 0 1 {hr} -{hr} h {W-2*ox-2*hr} '
             f'a {hr} {hr} 0 0 1 {hr} {hr} v {hh-hr} h -{W-2*ox} z" fill="{gold}"/>')
    # English name — the hero, top-left
    P.append(f'<text x="52" y="152" font-size="86" fill="#ffffff" font-family="{tfont}" '
             f'font-weight="bold" letter-spacing="1">{esc(name_en)}</text>')
    P.append(f'<text x="54" y="210" font-size="30" fill="#ffffff" opacity="0.9" '
             f'font-family="{tfont}" font-style="italic" letter-spacing="3">CHARACTER BOARD · 角色板</text>')
    # 漢字 top-right, Tâi-lô romanisation directly underneath it
    P.append(f'<text x="{W-52}" y="140" font-size="100" fill="#ffffff" text-anchor="end" '
             f'font-family="{tfont}" font-weight="bold">{esc(hanzi)}</text>')
    P.append(f'<text x="{W-52}" y="212" font-size="50" fill="#ffffff" text-anchor="end" '
             f'font-family="{tfont}" font-style="italic" opacity="0.95">{esc(name)}</text>')
    # ICON-ONLY ability + flaw medallions, CENTRED in the gold band (drawn glyphs; NO keyword/explainer
    # text — the rulebook carries the words). Ability teal on the LEFT, flaw vermilion on the RIGHT: a
    # fixed position + hue pairing that tells which-is-which at a glance without a text label.
    med_r = 74
    med_cy = 138
    med_cx_a = W/2 - 92
    med_cx_f = W/2 + 92

    def icon_medallion(cx, code, col):
        return "".join([
            f'<circle cx="{cx}" cy="{med_cy}" r="{med_r}" fill="#ffffff" stroke="{col}" stroke-width="6"/>',
            _pb_kit_glyph(cx, med_cy, code, col, ink, tfont)])
    P.append(icon_medallion(med_cx_a, acode, teal))
    P.append(icon_medallion(med_cx_f, fcode, vermilion))

    content_top = 18 + hh + 40                     # = 308

    # ==================== LEFT COLUMN (full height): character IMAGE + the Followers DIAL ================
    img_x = M                                      # 70 — image now on the LEFT
    img_y = content_top                            # 308
    IMG_W = 900
    IMG_H = 1380                                    # portrait slot; the dial sits below in the same column
    fig_id = f"FIG-CHAR-{slug}"
    embedded = _embed_fig_png(fig_id, img_x, img_y, IMG_W, IMG_H, mockups_dir)
    if embedded:
        P.append(f'<rect x="{img_x}" y="{img_y}" width="{IMG_W}" height="{IMG_H}" rx="18" fill="#ffffff" opacity="0.6"/>')
        P.append(embedded)                          # clipPath + <image> data URI (self-contained)
        P.append(f'<rect x="{img_x}" y="{img_y}" width="{IMG_W}" height="{IMG_H}" rx="18" fill="none" '
                 f'stroke="{gold}" stroke-width="5"/>')
    else:
        # empty state: dashed placeholder frame + corner ticks + a portrait silhouette + caption + label
        P.append(f'<rect x="{img_x}" y="{img_y}" width="{IMG_W}" height="{IMG_H}" rx="18" fill="#ffffff" opacity="0.4" '
                 f'stroke="{gold}" stroke-width="4" stroke-dasharray="14 10"/>')
        for (tx, ty, dx, dy) in [(img_x+22, img_y+22, 1, 1), (img_x+IMG_W-22, img_y+22, -1, 1),
                                 (img_x+22, img_y+IMG_H-22, 1, -1), (img_x+IMG_W-22, img_y+IMG_H-22, -1, -1)]:
            P.append(f'<path d="M{tx} {ty+dy*34} L{tx} {ty} L{tx+dx*34} {ty}" fill="none" '
                     f'stroke="{muted}" stroke-width="4"/>')
        scx, scy = img_x+IMG_W/2, img_y+IMG_H/2 + 40
        P.append(f'<circle cx="{scx}" cy="{scy-190}" r="150" fill="{muted}" opacity="0.28"/>')
        P.append(f'<path d="M{scx-260} {scy+300} q260 -400 520 0 z" fill="{muted}" opacity="0.28"/>')
        P.append(f'<text x="{scx}" y="{img_y+44}" font-size="22" fill="{muted}" text-anchor="middle" '
                 f'font-family="{bfont}" font-style="italic">illustration placeholder · human-illustrated (no AI final art)</text>')
        P.append(f'<rect x="{scx-210}" y="{img_y+IMG_H-70}" width="420" height="46" rx="23" fill="{ink}"/>')
        P.append(f'<text x="{scx}" y="{img_y+IMG_H-38}" font-size="27" fill="#ffffff" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">[{esc(fig_id)}]</text>')

    # --- FOLLOWERS DIAL: an actual rotating-insert dial FACE (0–8 notched arc) UNDER the image -----------
    # Represents the BOARD FACE only; the physical knob is a separate 3D-printed component. A number arc
    # with a detent at each value, a centre pivot + dashed groove ring (where the knob seats), and the
    # per-character MAX/START marker (2, or 4 for 網紅) shown by a pointer + a highlighted notch.
    dial_top = img_y + IMG_H + 40                  # 1728
    P.append(emblem_svg("spark", img_x+52, dial_top+42, 24, violet))
    P.append(f'<text x="{img_x+92}" y="{dial_top+54}" font-size="34" fill="{violet}" '
             f'font-family="{tfont}" font-weight="bold" letter-spacing="1">FOLLOWERS 粉 · the dial</text>')
    P.append(f'<text x="{img_x+92}" y="{dial_top+92}" font-size="23" fill="{muted}" '
             f'font-family="{bfont}" font-style="italic">a 3D-printed knob clicks into the notches · points at Followers-max</text>')
    n_dial = 9
    dcx = img_x + IMG_W/2                           # 520 — centred under the image
    dcy = dial_top + 512                            # 2240 pivot
    R = 280                                         # number-arc radius
    # arc track (value 0 left → 8 right, sweeping over the top)
    P.append(f'<path d="M{dcx-R:.0f} {dcy:.0f} A {R} {R} 0 0 0 {dcx+R:.0f} {dcy:.0f}" '
             f'fill="none" stroke="{violet}" stroke-width="7" opacity="0.45"/>')
    # groove ring — where the rotating 3D insert seats — + centre pivot dot
    P.append(f'<circle cx="{dcx:.0f}" cy="{dcy:.0f}" r="104" fill="#ffffff" opacity="0.5" '
             f'stroke="{violet}" stroke-width="3" stroke-dasharray="10 8"/>')
    P.append(f'<circle cx="{dcx:.0f}" cy="{dcy:.0f}" r="12" fill="{violet}"/>')
    # the per-character START/MAX pointer FIRST (under the notches), from the pivot toward the start value
    a0 = math.pi * (1 - dial_start/(n_dial-1))
    px = dcx + (R-46)*math.cos(a0)
    py = dcy - (R-46)*math.sin(a0)
    P.append(f'<line x1="{dcx:.0f}" y1="{dcy:.0f}" x2="{px:.0f}" y2="{py:.0f}" stroke="{violet}" '
             f'stroke-width="9" stroke-linecap="round"/>')
    for i in range(n_dial):
        a = math.pi * (1 - i/(n_dial-1))
        nx = dcx + R*math.cos(a)
        ny = dcy - R*math.sin(a)
        # detent notch: a short radial tick across the arc at each value
        t1x, t1y = dcx + (R-16)*math.cos(a), dcy - (R-16)*math.sin(a)
        t2x, t2y = dcx + (R+16)*math.cos(a), dcy - (R+16)*math.sin(a)
        P.append(f'<line x1="{t1x:.0f}" y1="{t1y:.0f}" x2="{t2x:.0f}" y2="{t2y:.0f}" '
                 f'stroke="{violet}" stroke-width="3" opacity="0.6"/>')
        if i < dial_start:                          # inside the reachable range
            fill, stroke, ncol, sw, dash = "#ffffff", violet, ink, 4, ""
        elif i == dial_start:                       # the MAX / start notch
            fill, stroke, ncol, sw, dash = violet, violet, "#ffffff", 5, ""
        else:                                       # above the start ceiling
            fill, stroke, ncol, sw, dash = "#E7E1D4", muted, muted, 2, ' stroke-dasharray="6 5"'
        P.append(f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="33" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{sw}"{dash}/>')
        P.append(f'<text x="{nx:.0f}" y="{ny+11:.0f}" font-size="32" fill="{ncol}" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold">{i}</text>')
    # MAX tag just outside the arc at the start angle
    tgx = dcx + (R+78)*math.cos(a0)
    tgy = dcy - (R+78)*math.sin(a0)
    P.append(f'<rect x="{tgx-60:.0f}" y="{tgy-28:.0f}" width="120" height="56" rx="14" fill="{violet}"/>')
    P.append(f'<text x="{tgx:.0f}" y="{tgy-3:.0f}" font-size="24" fill="#ffffff" text-anchor="middle" '
             f'font-family="{tfont}" font-weight="bold" letter-spacing="1">MAX</text>')
    P.append(f'<text x="{tgx:.0f}" y="{tgy+20:.0f}" font-size="19" fill="#ffffff" text-anchor="middle" '
             f'font-family="{tfont}" font-weight="bold">start {dial_start}</text>')

    # ==================== RIGHT COLUMN: prose one-liner + the two SCORING-PILE card zones ================
    # Prose banner and the pile tray share ONE centred width so they stack as a tidy module (rather than a
    # single vast tray floating in void); clean board-background margins sit either side.
    right_l = img_x + IMG_W + 60                    # 1030
    right_r = W - M                                 # 3438
    right_w = right_r - right_l                     # 2408
    zgap = 170
    inner_pad = 90
    col_w = 2*CARD_W + zgap + 2*inner_pad           # 1850 — hugs the two poker footprints
    col_x = right_l + (right_w - col_w) / 2         # centred in the right column

    # --- PROSE strip: a short, funny one-liner (from the blurb), under the banner -----------------------
    ps_y, ps_h = content_top, 190
    P.append(f'<rect x="{col_x}" y="{ps_y}" width="{col_w}" height="{ps_h}" rx="20" fill="{gold}" opacity="0.16"/>')
    P.append(f'<rect x="{col_x}" y="{ps_y}" width="10" height="{ps_h}" rx="5" fill="{gold}"/>')
    P.append(f'<text x="{col_x+42}" y="{ps_y+66}" font-size="70" fill="{gold}" opacity="0.5" '
             f'font-family="{tfont}" font-weight="bold">&#8220;</text>')
    prose_wrap = max(36, int((col_w - 170) / 20))
    plines = textwrap.wrap(blurb, prose_wrap)[:2]
    pbase = ps_y + (ps_h - (len(plines)-1)*46) / 2 + 4
    for i, ln in enumerate(plines):
        P.append(f'<text x="{col_x+120}" y="{pbase + i*46:.0f}" font-size="38" fill="{ink}" '
                 f'font-family="{bfont}" font-style="italic">{esc(ln)}</text>')

    # --- SCORING-PILE tray: the TWO card-EXACT-footprint drop zones (CANCELLED 取消 · COMPLETE 成團) ------
    # Each zone is exactly one poker footprint (750×1050) so a real Booking card stacks on it. A compact
    # tray hugs the pair and is centred vertically in the space below the prose banner.
    tray_h = 200 + CARD_H + 56                      # header/label pad + card + bottom pad
    tray_y = ps_y + ps_h + ((H - M) - (ps_y + ps_h) - tray_h) / 2   # centred below the prose
    tray_x, tray_w = col_x, col_w
    P.append(f'<rect x="{tray_x}" y="{tray_y}" width="{tray_w}" height="{tray_h}" rx="24" '
             f'fill="#ffffff" opacity="0.32" stroke="{gold}" stroke-width="3"/>')
    P.append(f'<text x="{tray_x+40}" y="{tray_y+58}" font-size="32" fill="{ink}" '
             f'font-family="{tfont}" font-weight="bold" letter-spacing="1">SCORING PILES · 成團 / 取消</text>')
    P.append(f'<text x="{tray_x+40}" y="{tray_y+92}" font-size="24" fill="{muted}" '
             f'font-family="{bfont}" font-style="italic">stack each finished Booking card on its pile — these are your whole score</text>')

    zx = [tray_x + inner_pad + i*(CARD_W + zgap) for i in range(2)]
    card_top = tray_y + 200
    label_y = card_top - 22

    def pile_zone(x0, en, han, emcol, note, label):
        s = [f'<text x="{x0+CARD_W/2}" y="{label_y}" font-size="30" fill="{emcol}" text-anchor="middle" '
             f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(label)}</text>',
             f'<rect x="{x0}" y="{card_top}" width="{CARD_W}" height="{CARD_H}" rx="16" fill="#ffffff" '
             f'opacity="0.5" stroke="{emcol}" stroke-width="4" stroke-dasharray="14 10"/>',
             emblem_svg("stamp", x0+CARD_W/2, card_top+CARD_H*0.34, 54, emcol, stroke=ink),
             f'<text x="{x0+CARD_W/2}" y="{card_top+CARD_H*0.56:.0f}" font-size="72" fill="{emcol}" '
             f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(han)}</text>',
             f'<text x="{x0+CARD_W/2}" y="{card_top+CARD_H*0.66:.0f}" font-size="30" fill="{ink}" '
             f'text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="2">{esc(en)}</text>',
             f'<text x="{x0+CARD_W/2}" y="{card_top+CARD_H-40}" font-size="24" fill="{muted}" '
             f'text-anchor="middle" font-family="{bfont}" font-style="italic">{esc(note)}</text>']
        return "".join(s)
    P.append(pile_zone(zx[0], "CANCELLED", "取消", taupe, "didn't run → half value", "CANCELLED 取消"))
    P.append(pile_zone(zx[1], "COMPLETE", "成團", gold_pile, "ran → full value", "COMPLETE 成團"))

    return _svg(W, H, P), W, H


# ---- score / reputation track (serpentine, numbered) ------------------------
def render_scoretrack(theme, max_v, per_row, title, milestones, note, start_label,
                      accent_hex="", kicker=""):
    """A compact numbered 0..max track that snakes across rows — a real running
    tracker you advance a per-player marker along. Milestones (pos->label) are
    highlighted with a call-out above the cell.

    `accent_hex` overrides the milestone/highlight colour so sibling tracks (Reach cap, Tours-Completed
    counter, the day-clock) read as DIFFERENT instruments at a glance instead of three identical tracks —
    and, for the Tours-Completed counter, keeps it off the score-gold of the 成團 win pile (bg-infodesign
    item 2). `kicker` prints a bold sub-banner under the title (e.g. 'a progress meter — NOT your score')."""
    ink, muted, text = theme["ink"], theme["muted"], theme["text"]
    accent = accent_hex or theme["accent"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    cell = 108
    gap = 12
    pad = 44
    n = max_v + 1
    per_row = min(per_row, n)
    rows = math.ceil(n / per_row)
    title_h = 92 + (40 if kicker else 0)
    call_h = 78                                   # room above each row for (up to 2-line) milestone call-outs
    row_h = cell + call_h + gap
    W = pad * 2 + per_row * (cell + gap) - gap
    # Wrap the footer note to the panel width so a long --note never clips at the right edge
    # (bg-infodesign): grow the panel height to fit however many wrapped lines it needs.
    note_lines = textwrap.wrap(note, max(20, int((W - 2 * pad) / 14))) if note else []
    note_block_h = (len(note_lines) * 32 + 24) if note_lines else 40
    H = title_h + rows * row_h + 30 + note_block_h

    def cell_xy(v):
        row = v // per_row
        col = v % per_row
        if row % 2 == 1:                          # snake
            col = per_row - 1 - col
        x = pad + col * (cell + gap)
        y = title_h + row * row_h + call_h
        return x, y

    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="26" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']
    if title:
        parts.append(f'<text x="{W/2}" y="60" font-size="50" fill="{ink}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(title)}</text>')
    if kicker:
        parts.append(f'<rect x="{pad}" y="82" width="{W-2*pad}" height="40" rx="20" fill="{accent}"/>')
        parts.append(f'<text x="{W/2}" y="110" font-size="26" fill="#ffffff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(kicker)}</text>')
    # groove: a faint polyline through cell centres in snake order (shows one continuous track)
    pts = " ".join(f"{cell_xy(v)[0]+cell/2},{cell_xy(v)[1]+cell/2}" for v in range(n))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="{muted}" stroke-width="8" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.3"/>')
    for v in range(n):
        x, y = cell_xy(v)
        is_ms = v in milestones
        is_dec = (v % 10 == 0)
        if is_ms:
            fill, stroke, tcol, sw = accent, ink, "#ffffff", 5
        elif v == 0:
            fill, stroke, tcol, sw = ink, ink, "#ffffff", 4
        elif is_dec:
            fill, stroke, tcol, sw = "#ffffff", accent, ink, 4
        else:
            fill, stroke, tcol, sw = "#ffffff", muted, ink, 3
        op = "1" if is_ms else "0.92"
        parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="16" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
        parts.append(f'<text x="{x+cell/2}" y="{y+cell/2+16}" font-size="46" fill="{tcol}" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{v}</text>')
        if v == 0 and start_label:
            parts.append(f'<text x="{x+cell/2}" y="{y-14}" font-size="24" fill="{ink}" '
                         f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(start_label)}</text>')
        if is_ms:
            # stack the call-out ABOVE the cell top (y): the last line lands just over the cell so 2-line
            # labels no longer overlap the numeral. Tighter wrap keeps each line within ~one cell width.
            segs = textwrap.wrap(milestones[v], 13)[:2]
            base = y - 12 - (len(segs) - 1) * 24
            for j, seg in enumerate(segs):
                parts.append(f'<text x="{x+cell/2}" y="{base + j*24}" font-size="20" fill="{accent}" '
                             f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(seg)}</text>')
    if note_lines:
        ny = H - note_block_h + 30
        for i, ln in enumerate(note_lines):
            parts.append(f'<text x="{pad}" y="{ny + i*32}" font-size="26" fill="{muted}" '
                         f'font-family="{bfont}" font-style="italic">{esc(ln)}</text>')
    return _svg(W, H, parts), W, H


def _svg(W, H, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + "".join(parts) + "</svg>")


def main():
    ap = argparse.ArgumentParser(description="Render themed boards, tracks, and tokens.")
    ap.add_argument("--type", required=True,
                    choices=["track", "tokens", "mat", "aid", "regionmap", "scoretrack", "playerboard"])
    ap.add_argument("--theme", default="clean")
    ap.add_argument("--out", type=Path, default=Path("build/board.png"))
    # track
    ap.add_argument("--spaces", type=int, default=7)
    ap.add_argument("--title", default="")
    ap.add_argument("--labels", default="", help="comma-separated (per space, or per token)")
    ap.add_argument("--left-label", default="")
    ap.add_argument("--right-label", default="")
    # scoretrack
    ap.add_argument("--max", type=int, default=50, help="scoretrack: highest value (0..max)")
    ap.add_argument("--per-row", type=int, default=13, help="scoretrack: cells per row before snaking")
    ap.add_argument("--milestones", default="", help="scoretrack: 'pos:label;pos:label' call-outs")
    ap.add_argument("--note", default="", help="scoretrack: footer note")
    ap.add_argument("--start-label", default="", help="scoretrack: label above the 0 cell")
    ap.add_argument("--accent-hex", default="", help="scoretrack: override the milestone/highlight colour "
                    "(so sibling tracks read as different instruments; keeps Tours-Completed off score-gold)")
    ap.add_argument("--kicker", default="", help="scoretrack: bold sub-banner under the title")
    # tokens
    ap.add_argument("--shape", default="circle", choices=["circle", "square", "hex"])
    ap.add_argument("--diameter-mm", type=float, default=22.0)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--from-csv", type=Path, default=None, help="tokens: columns label[,color][,qty][,name]")
    ap.add_argument("--legend", action="store_true", help="tokens: render a true KEY (one row per type: "
                    "swatch + name + ×qty) instead of the qty-expanded punch-grid")
    # mat / regionmap
    ap.add_argument("--spec", type=Path, default=None)
    # playerboard: characters CSV → one landscape board per (character) row into --out (a DIRECTORY)
    ap.add_argument("--csv", type=Path, default=None,
                    help="playerboard: characters CSV (renders one board per row carrying ability+flaw)")
    ap.add_argument("--mockups-dir", type=Path, default=None,
                    help="playerboard: dir of art-mock PNGs (FIG-CHAR-<slug>.png) to embed in the portrait "
                    "slot; defaults to <game>/build/mockups next to the characters CSV. Absent → placeholder.")
    # regionmap day/night state (mirrors the dusk flip)
    ap.add_argument("--phase", default="day", choices=["day", "night"],
                    help="regionmap: render the day (warm) or night (neon) state of the board")
    args = ap.parse_args()

    theme = get_theme(args.theme)
    labels = [s.strip() for s in args.labels.split(",")] if args.labels else []

    if args.type == "playerboard":
        if not args.csv:
            ap.error("--type playerboard requires --csv <characters.csv>")
        import csv as _csv
        with args.csv.open(newline="", encoding="utf-8") as f:
            rows = list(_csv.DictReader(f))
        # Beacon-safe: render ONLY Travel-Agents character rows (carry ability_code + flaw_code).
        rows = [r for r in rows if str(r.get("ability_code", "")).strip()
                and str(r.get("flaw_code", "")).strip()]
        if not rows:
            print("[board] playerboard: no character rows (ability_code+flaw_code) — nothing rendered.")
            return 0
        # --out is a DIRECTORY for playerboard (one file per character).
        outdir = args.out if args.out.suffix == "" else args.out.parent
        # Art-mock embed dir: explicit --mockups-dir, else <game>/build/mockups (the characters CSV lives
        # in <game>/components/, so its parent's parent is the game dir). Absent dir → placeholder path.
        mockups_dir = args.mockups_dir
        if mockups_dir is None:
            mockups_dir = args.csv.resolve().parent.parent / "build" / "mockups"
        for r in rows:
            svg, W, H = render_playerboard(theme, r, mockups_dir=mockups_dir)
            slug = _slugify(str(r.get("name_en", "")).strip() or r.get("id", ""))
            _save(svg, outdir / f"board-{slug}.png", W, H)
        return 0

    if args.type == "track":
        svg, W, H = render_track(theme, args.spaces, args.title, labels, args.left_label, args.right_label)
    elif args.type == "tokens":
        tokens = []
        if args.from_csv:
            import csv
            with args.from_csv.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    tokens.append({"label": row.get("label", ""), "color": row.get("color") or None,
                                   "qty": row.get("qty", 1), "name": row.get("name", "")})
        else:
            tokens = [{"label": l, "qty": 1} for l in labels] or [{"label": "?", "qty": 1}]
        svg, W, H = render_tokens(theme, tokens, args.shape, mm(args.diameter_mm), args.cols, legend=args.legend)
    elif args.type == "mat":
        if not args.spec:
            ap.error("--type mat requires --spec <file.json>")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_mat(theme, spec)
    elif args.type == "regionmap":
        if not args.spec:
            ap.error("--type regionmap requires --spec <file.json>")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_regionmap(theme, spec, args.phase)
    elif args.type == "scoretrack":
        milestones = {}
        for chunk in args.milestones.split(";"):
            chunk = chunk.strip()
            if ":" in chunk:
                pos, _, lab = chunk.partition(":")
                try:
                    milestones[int(pos)] = lab.strip()
                except ValueError:
                    pass
        svg, W, H = render_scoretrack(theme, args.max, args.per_row, args.title,
                                      milestones, args.note, args.start_label,
                                      args.accent_hex, args.kicker)
    else:  # aid
        if not args.spec:
            ap.error("--type aid requires --spec <file.json>")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_aid(theme, spec)

    _save(svg, args.out, W, H)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
