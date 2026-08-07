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
def render_tokens(theme, tokens, shape, diameter_px, cols):
    """tokens: list of dicts {label, color, qty}."""
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


# ---- region-ring map (TABLE-LAYOUT setup guide) -----------------------------
def render_regionmap(theme, spec, phase="day"):
    """A table-layout setup board: the 4-region ring (adjacency + HSR drawn as edges) with each region
    showing its signature chips, its FACE-UP vendor slots, and its DAY/NIGHT market-deck space — PLUS
    labelled placeholder zones for every other component (Tour-Ticket decks, Prestige / Reputation /
    clock tracks, the 成團/遺珠 piles, Buzz supply, ★ Star tokens, character mats). Renders in two states
    (--phase day|night) mirroring the dusk flip: warm ☀日 morning vs neon ☾夜 night (drawn sun/moon, never
    a font glyph). Region layout + all zone positions are computed here from spec content. TA-specific —
    only games/travel-agents/make.sh calls --type regionmap, so this does not affect other games."""
    W, H = 1840, 1540
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    regions = {r["key"]: r for r in spec.get("regions", [])}

    ps = PHASE_STYLES.get((phase or "day").lower(), PHASE_STYLES["day"])
    is_night = (phase or "day").lower() == "night"
    ground = ps["page"]                      # (top, bottom) phase gradient
    frame = ps["frame"]                      # phase accent (morning amber / neon violet)
    glow = ps.get("glow", frame)
    badge_emblem = ps.get("emblem", "sun")   # DRAWN sun / moon
    badge_char = "夜" if is_night else "日"
    badge_word = "NIGHT · 夜市" if is_night else "DAY · 早"
    steel = "#4A5A72"

    parts = [f'<defs>{page_gradient(theme, "pg", ground)}</defs>',
             f'<rect width="{W}" height="{H}" rx="30" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']

    # --- title band + day/night badge ---
    title = spec.get("title", "")
    parts.append(f'<rect x="0" y="0" width="{W}" height="92" fill="{ink}"/>')
    parts.append(f'<rect x="0" y="92" width="{W}" height="6" fill="{frame}"/>')
    parts.append(f'<text x="44" y="60" font-size="44" fill="#fff" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(title)}</text>')
    # phase badge, right of the title band
    bx = W - 300
    parts.append(f'<rect x="{bx}" y="20" width="256" height="54" rx="27" fill="{frame}"/>')
    parts.append(emblem_svg(badge_emblem, bx + 38, 47, 18, "#fff"))
    parts.append(f'<text x="{bx + 150}" y="58" font-size="30" fill="#fff" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(badge_char + "  " + badge_word)}</text>')

    # --- helpers -----------------------------------------------------------------
    def zone(x, y, w, h, label, glyph="", desc="", fill_op=0.42):
        z = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#ffffff" opacity="{fill_op}"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none" stroke="{frame}" '
             f'stroke-width="3" stroke-dasharray="11 8"/>',
             f'<text x="{x+18}" y="{y+34}" font-size="25" fill="{ink}" font-family="{tfont}" '
             f'font-weight="bold" letter-spacing="1">{esc(label.upper())}</text>']
        if desc:
            z.append(f'<text x="{x+18}" y="{y+62}" font-size="20" fill="{muted}" '
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
        d.append(f'<text x="{x+w/2}" y="{y+h/2-2}" font-size="24" fill="{tc}" text-anchor="middle" '
                 f'font-family="{tfont}" font-weight="bold">{esc(label)}</text>')
        if sub:
            d.append(f'<text x="{x+w/2}" y="{y+h/2+26}" font-size="17" fill="{tc}" text-anchor="middle" '
                     f'font-family="{bfont}" opacity="0.85">{esc(sub)}</text>')
        return "".join(d)

    # --- region ring geometry (computed) ---
    PW, PH = 404, 262
    centers = {"north": (626, 268), "central": (256, 590), "east": (996, 590), "south": (626, 912)}

    def tl(key):
        cx, cy = centers[key]
        return cx - PW / 2, cy - PH / 2

    # ring edges (under the panels)
    for a, b in spec.get("ring", []):
        if a in centers and b in centers:
            (x1, y1), (x2, y2) = centers[a], centers[b]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{muted}" '
                         f'stroke-width="12" stroke-linecap="round" opacity="0.5"/>')
    # HSR double-rail spine (North↔South)
    hsr = spec.get("hsr", [])
    if len(hsr) == 2 and all(k in centers for k in hsr):
        (x1, y1), (x2, y2) = centers[hsr[0]], centers[hsr[1]]
        sy, ey = y1 + PH / 2 + 6, y2 - PH / 2 - 6
        off = 9
        for s in (off, -off):
            parts.append(f'<line x1="{x1+s}" y1="{sy}" x2="{x2+s}" y2="{ey}" stroke="{steel}" '
                         f'stroke-width="6" stroke-linecap="round"/>')
        ties = 12
        for i in range(1, ties):
            my = sy + (ey - sy) * i / ties
            parts.append(f'<line x1="{x1-(off+5)}" y1="{my}" x2="{x1+(off+5)}" y2="{my}" '
                         f'stroke="{steel}" stroke-width="4"/>')
        my = (sy + ey) / 2
        parts.append(f'<rect x="{x1-150}" y="{my-26}" width="300" height="52" rx="26" '
                     f'fill="{steel}" stroke="#fff" stroke-width="2"/>')
        parts.append(f'<text x="{x1}" y="{my+10}" font-size="26" fill="#fff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">HSR 高鐵 · 北–南</text>')

    # --- region panels ---
    for r in spec.get("regions", []):
        key = r["key"]
        if key not in centers:
            continue
        X, Y = tl(key)
        rcol = r.get("color", accent)
        emb = r.get("emblem", "circle")
        rad = 18
        # phase frame accent (thin, outside) + white panel + region-colour border
        parts.append(f'<rect x="{X-4}" y="{Y-4}" width="{PW+8}" height="{PH+8}" rx="{rad+4}" '
                     f'fill="none" stroke="{frame}" stroke-width="3" opacity="0.7"/>')
        parts.append(f'<rect x="{X}" y="{Y}" width="{PW}" height="{PH}" rx="{rad}" '
                     f'fill="#ffffff" stroke="{rcol}" stroke-width="4"/>')
        # header
        hh = 54
        parts.append(f'<path d="M{X} {Y+rad} a {rad} {rad} 0 0 1 {rad} -{rad} h {PW-2*rad} '
                     f'a {rad} {rad} 0 0 1 {rad} {rad} v {hh-rad} h -{PW} z" fill="{rcol}"/>')
        parts.append(emblem_svg(emb, X + 32, Y + 27, 15, "#ffffff"))
        parts.append(f'<text x="{X+58}" y="{Y+37}" font-size="32" fill="#fff" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(r.get("name",""))}</text>')
        # signature chips (shape + 繁體 + short EN under) — short labels so nothing overflows
        chips = r.get("chips", [])
        n = len(chips)
        chip_r = 26
        cell = 108
        x0 = X + PW / 2 - (n * cell) / 2 + cell / 2
        ccy = Y + hh + 52
        for i, sp in enumerate(chips):
            suit = resolve_suit(theme, sp.get("id", "")) if sp.get("id") in theme["suits"] else {}
            scol = suit.get("color", rcol)
            semb = suit.get("emblem", "circle")
            cx = x0 + i * cell
            tcol = pick_text_color(scol, dark=ink, light="#ffffff")
            parts.append(emblem_svg(semb, cx, ccy, chip_r, scol, stroke=ink))
            parts.append(f'<text x="{cx}" y="{ccy + chip_r*0.34}" font-size="28" fill="{tcol}" '
                         f'text-anchor="middle" font-family="{bfont}" font-weight="bold">{esc(sp.get("label",""))}</text>')
            parts.append(f'<text x="{cx}" y="{ccy + chip_r + 26}" font-size="19" fill="{text}" '
                         f'text-anchor="middle" font-family="{bfont}">{esc(sp.get("en",""))}</text>')
        # bottom row: FACE-UP vendor slots (left) + the DAY/NIGHT market deck (right)
        slots_n = int(r.get("slots_n", 1))
        row_top = Y + PH - 112
        sw, sh = 60, 90
        parts.append(f'<text x="{X+26}" y="{row_top-8}" font-size="18" fill="{rcol}" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">FACE-UP ×{slots_n}</text>')
        for i in range(slots_n):
            sx = X + 26 + i * (sw + 12)
            parts.append(f'<rect x="{sx}" y="{row_top}" width="{sw}" height="{sh}" rx="8" '
                         f'fill="none" stroke="{rcol}" stroke-width="2" stroke-dasharray="7 6"/>')
            parts.append(emblem_svg(emb, sx + sw/2, row_top + 34, 12, rcol))
            parts.append(f'<text x="{sx+sw/2}" y="{row_top+sh-12}" font-size="15" fill="{muted}" '
                         f'text-anchor="middle" font-family="{bfont}">vendor</text>')
        # market deck (flips with phase)
        dw, dh = 92, 104
        dx = X + PW - 26 - dw
        deck_col = ground[1] if not is_night else "#3A2E52"
        parts.append(f'<text x="{dx+dw/2}" y="{row_top-8}" font-size="18" fill="{frame}" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold" letter-spacing="1">MARKET</text>')
        parts.append(facedown_deck(dx, row_top, dw, dh, frame,
                                   badge_char, "night" if is_night else "day"))

    # --- RIGHT column: track + pile + supply placeholder zones ---
    rc_x, rc_w = 1250, 550
    parts.append(zone(rc_x, 120, rc_w, 128, "Prestige (VP) track",
                      emblem_svg("spark", rc_x + rc_w - 44, 168, 26, theme["suits"].get("signature", {}).get("color", "#C9A227")),
                      "sum of your vendors' values — separate track"))
    parts.append(zone(rc_x, 268, rc_w, 128, "Reputation track",
                      f'<circle cx="{rc_x+rc_w-44}" cy="316" r="26" fill="{theme["suits"].get("central",{}).get("color","#1F8A7A")}"/>'
                      f'<text x="{rc_x+rc_w-44}" y="325" font-size="26" fill="#fff" text-anchor="middle" font-family="{tfont}" font-weight="bold">譽</text>',
                      "scores by FINAL position — separate track"))
    parts.append(zone(rc_x, 416, rc_w, 128, "Vendor-claims clock",
                      f'<circle cx="{rc_x+rc_w-44}" cy="464" r="26" fill="{accent}"/>'
                      f'<text x="{rc_x+rc_w-44}" y="473" font-size="24" fill="#fff" text-anchor="middle" font-family="{tfont}" font-weight="bold">鐘</text>',
                      "dusk @5 · last train @10 (2p)"))
    # piles
    pw = (rc_w - 16) / 2
    gold = theme["suits"].get("signature", {}).get("color", "#C9A227")
    taupe = muted
    parts.append(zone(rc_x, 564, pw, 150, "成團 · Win pile",
                      emblem_svg("stamp", rc_x + pw - 40, 636, 24, gold), "tours that ran → +value"))
    parts.append(zone(rc_x + pw + 16, 564, pw, 150, "遺珠 · Lose pile",
                      emblem_svg("stamp", rc_x + pw + 16 + pw - 40, 636, 24, taupe), "got away: lose half value"))
    # supply
    violet = theme["suits"].get("buzz", {}).get("color", "#6A4C93")
    parts.append(zone(rc_x, 730, pw, 150, "Buzz supply",
                      f'<circle cx="{rc_x+pw-40}" cy="802" r="24" fill="{violet}" stroke="{ink}" stroke-width="2"/>'
                      f'<text x="{rc_x+pw-40}" y="811" font-size="24" fill="#fff" text-anchor="middle" font-family="{tfont}" font-weight="bold">讚</text>',
                      "~24 tokens (2p)"))
    star_svg = ('<polygon points="' + " ".join(
        f'{rc_x+pw+16+pw-40 + (24 if i%2==0 else 24*0.42)*math.cos(-math.pi/2+i*math.pi/5):.1f},'
        f'{802 + (24 if i%2==0 else 24*0.42)*math.sin(-math.pi/2+i*math.pi/5):.1f}' for i in range(10))
        + f'" fill="{gold}"/>')
    parts.append(zone(rc_x + pw + 16, 730, pw, 150, "★ Star tokens", star_svg, "apex accolades (~4)"))

    # --- BOTTOM band: Tour-Ticket decks (left) + character mats (right) ---
    by = 1070
    # tickets
    parts.append(zone(60, by, 840, 400, "Tour-Ticket decks", desc="reveal a face-up ROW OF 3; refill when claimed"))
    tdw, tdh = 232, 250
    tspacing = (840 - 40 - 3 * tdw) / 2
    tlabels = [("day", "日 DAY", ground[1]), ("night", "夜 NIGHT", "#3A2E52"), ("general", "通 ANY", gold)]
    for i, (pk, lab, cc) in enumerate(tlabels):
        tx = 60 + 20 + i * (tdw + tspacing)
        parts.append(facedown_deck(tx, by + 90, tdw, tdh, cc if pk != "night" else "#6A4C93", lab, "draw 5 / phase"))
    # character mats
    parts.append(zone(940, by, 840, 400, "Character mats", desc="one per agent — ability + flaw, public"))
    mw = (840 - 40 - 20) / 2
    for i, lab in enumerate(("Agent A", "Agent B")):
        mx = 940 + 20 + i * (mw + 20)
        parts.append(f'<rect x="{mx}" y="{by+90}" width="{mw}" height="250" rx="14" fill="#ffffff" '
                     f'opacity="0.55" stroke="{ink}" stroke-width="2" stroke-dasharray="9 7"/>')
        parts.append(emblem_svg("stamp", mx + mw/2, by + 180, 30, frame))
        parts.append(f'<text x="{mx+mw/2}" y="{by+260}" font-size="24" fill="{ink}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">{esc(lab)}</text>')
        parts.append(f'<text x="{mx+mw/2}" y="{by+292}" font-size="18" fill="{muted}" text-anchor="middle" '
                     f'font-family="{bfont}">ability + flaw</text>')

    return _svg(W, H, parts), W, H


# ---- score / reputation track (serpentine, numbered) ------------------------
def render_scoretrack(theme, max_v, per_row, title, milestones, note, start_label):
    """A compact numbered 0..max track that snakes across rows — a real running
    tracker you advance a per-player marker along. Milestones (pos->label) are
    highlighted with a call-out above the cell."""
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    cell = 108
    gap = 12
    pad = 44
    n = max_v + 1
    per_row = min(per_row, n)
    rows = math.ceil(n / per_row)
    title_h = 92
    call_h = 46                                   # room above each row for milestone call-outs
    row_h = cell + call_h + gap
    W = pad * 2 + per_row * (cell + gap) - gap
    H = title_h + rows * row_h + 70

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
            for j, seg in enumerate(textwrap.wrap(milestones[v], 16)[:2]):
                parts.append(f'<text x="{x+cell/2}" y="{y-16+j*22}" font-size="21" fill="{accent}" '
                             f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(seg)}</text>')
    if note:
        parts.append(f'<text x="{pad}" y="{H-28}" font-size="26" fill="{muted}" '
                     f'font-family="{bfont}" font-style="italic">{esc(note)}</text>')
    return _svg(W, H, parts), W, H


def _svg(W, H, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + "".join(parts) + "</svg>")


def main():
    ap = argparse.ArgumentParser(description="Render themed boards, tracks, and tokens.")
    ap.add_argument("--type", required=True,
                    choices=["track", "tokens", "mat", "aid", "regionmap", "scoretrack"])
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
    # tokens
    ap.add_argument("--shape", default="circle", choices=["circle", "square", "hex"])
    ap.add_argument("--diameter-mm", type=float, default=22.0)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--from-csv", type=Path, default=None, help="tokens: columns label[,color][,qty]")
    # mat
    ap.add_argument("--spec", type=Path, default=None)
    # regionmap day/night state (mirrors the dusk flip)
    ap.add_argument("--phase", default="day", choices=["day", "night"],
                    help="regionmap: render the day (warm) or night (neon) state of the board")
    args = ap.parse_args()

    theme = get_theme(args.theme)
    labels = [s.strip() for s in args.labels.split(",")] if args.labels else []

    if args.type == "track":
        svg, W, H = render_track(theme, args.spaces, args.title, labels, args.left_label, args.right_label)
    elif args.type == "tokens":
        tokens = []
        if args.from_csv:
            import csv
            with args.from_csv.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    tokens.append({"label": row.get("label", ""), "color": row.get("color") or None,
                                   "qty": row.get("qty", 1)})
        else:
            tokens = [{"label": l, "qty": 1} for l in labels] or [{"label": "?", "qty": 1}]
        svg, W, H = render_tokens(theme, tokens, args.shape, mm(args.diameter_mm), args.cols)
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
                                      milestones, args.note, args.start_label)
    else:  # aid
        if not args.spec:
            ap.error("--type aid requires --spec <file.json>")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_aid(theme, spec)

    _save(svg, args.out, W, H)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
