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
                    boost_contrast, resolve_suit)

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
    spec: {title, subtitle?, sections:[{heading, lines:[...]}], width?}"""
    W = spec.get("width", 1600)
    pad = 56
    ink, accent, text, muted = theme["ink"], theme["accent"], theme["text"], theme["muted"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    wrap_at = max(24, int((W - 2 * pad) / 15))     # ~char width at the body size
    head_h = 150
    body = []
    y = head_h + 40
    for sec in spec.get("sections", []):
        heading = sec.get("heading", "")
        if any(g in heading for g in SCOPE_GLYPH_SHAPE):
            # drop a parenthetical that carries the tofu scope glyphs, then any stray glyphs
            heading = re.sub(r'\s*\([^)]*[⦿⬢➤][^)]*\)', '', heading)
            heading = re.sub(r'[⦿⬢➤]', '', heading)
        body.append((f'<text x="{pad}" y="{y}" font-size="34" fill="{accent}" font-family="{tfont}" '
                     f'font-weight="bold" letter-spacing="1">{esc(heading.upper())}</text>'))
        y += 20
        for line in sec.get("lines", []):
            if not any(g in line for g in SCOPE_GLYPH_SHAPE):
                for i, seg in enumerate(textwrap.wrap(line, wrap_at) or [""]):
                    y += 40
                    # Drawn bullet (not the "•" glyph — WenQuanYi Zen Hei lacks it and renders tofu □).
                    if i == 0:
                        body.append(f'<circle cx="{pad+8}" cy="{y-9}" r="6" fill="{accent}"/>')
                    body.append(f'<text x="{pad+30}" y="{y}" font-size="28" fill="{text}" '
                                f'font-family="{bfont}">{esc(seg)}</text>')
            else:
                # scope-glyph line: char-budget wrap treating each glyph as a ~2-char token, then emit
                # text runs interleaved with DRAWN scope shapes (no tofu). (bg-access FIX A)
                plines, cur, ln = [], [], 0
                for tok in line.split(" "):
                    w = 2 if tok in SCOPE_GLYPH_SHAPE else len(tok)
                    if cur and ln + 1 + w > wrap_at:
                        plines.append(cur); cur, ln = [], 0
                    cur.append(tok); ln += (1 if len(cur) > 1 else 0) + w
                if cur:
                    plines.append(cur)
                for i, toks in enumerate(plines):
                    y += 40
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
        y += 34
    H = y + pad
    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="28" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>',
             f'<rect x="0" y="0" width="{W}" height="{head_h}" fill="{ink}"/>',
             f'<rect x="0" y="{head_h}" width="{W}" height="6" fill="{accent}"/>',
             f'<text x="{pad}" y="76" font-size="56" fill="#fff" font-family="{tfont}" '
             f'font-weight="bold" letter-spacing="1">{esc(spec.get("title",""))}</text>']
    if spec.get("subtitle"):
        # subtitle sits on the dark `ink` header band — ensure ≥4.5:1 (lightens the accent only if needed,
        # so themes that already pass are untouched).
        sub_col = boost_contrast(accent, ink, 4.5)
        parts.append(f'<text x="{pad}" y="120" font-size="30" fill="{sub_col}" font-family="{tfont}" '
                     f'font-style="italic">{esc(spec["subtitle"])}</text>')
    parts += body
    return _svg(W, H, parts), W, H


# ---- region-ring map --------------------------------------------------------
def render_regionmap(theme, spec):
    """A clean region-ring board: region cards laid on a diamond, ring edges + an
    HSR spine drawn as real connectors, each region showing its specialty chips
    (colour + emblem + 繁體 + English). Purpose-built to replace the overlapping
    free-text mat. Spec: {title, width, height, regions[], ring[], hsr[], notes[]}."""
    W = spec.get("width", 1600)
    H = spec.get("height", 1200)
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    regions = {r["key"]: r for r in spec.get("regions", [])}
    RW, RH = spec.get("region_w", 330), spec.get("region_h", 214)

    parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
             f'<rect width="{W}" height="{H}" rx="30" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']

    # title — a slim top band with generous clearance below (the diamond starts well under it)
    title = spec.get("title", "")
    if title:
        parts.append(f'<rect x="0" y="0" width="{W}" height="84" fill="{ink}"/>')
        parts.append(f'<rect x="0" y="84" width="{W}" height="5" fill="{accent}"/>')
        parts.append(f'<text x="{W/2}" y="56" font-size="42" fill="#fff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(title)}</text>')

    def center(r):
        return (r["x"] + RW / 2, r["y"] + RH / 2)

    # edges drawn BEFORE the cards, so cards sit on top and the connector shows in the gap
    for a, b in spec.get("ring", []):
        if a in regions and b in regions:
            (x1, y1), (x2, y2) = center(regions[a]), center(regions[b])
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{muted}" '
                         f'stroke-width="12" stroke-linecap="round" opacity="0.55"/>')
    # HSR spine — a distinct double-rail with ties, drawn between its two regions
    hsr = spec.get("hsr", [])
    if len(hsr) == 2 and all(k in regions for k in hsr):
        (x1, y1), (x2, y2) = center(regions[hsr[0]]), center(regions[hsr[1]])
        # shorten the rail so it starts/ends at the card edges, not the centres
        ln = math.hypot(x2 - x1, y2 - y1) or 1
        ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
        sx, sy = x1 + ux * (RH / 2 + 6), y1 + uy * (RH / 2 + 6)
        ex, ey = x2 - ux * (RH / 2 + 6), y2 - uy * (RH / 2 + 6)
        px, py = -uy, ux                      # perpendicular for the two rails
        off = 9
        steel = "#4A5A72"
        for s in (off, -off):
            parts.append(f'<line x1="{sx + px*s}" y1="{sy + py*s}" x2="{ex + px*s}" y2="{ey + py*s}" '
                         f'stroke="{steel}" stroke-width="6" stroke-linecap="round"/>')
        ties = 14
        for i in range(1, ties):
            t = i / ties
            mx, my = sx + (ex - sx) * t, sy + (ey - sy) * t
            parts.append(f'<line x1="{mx + px*(off+5)}" y1="{my + py*(off+5)}" '
                         f'x2="{mx - px*(off+5)}" y2="{my - py*(off+5)}" stroke="{steel}" stroke-width="4"/>')
        # HSR label pill at the midpoint
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        lbl = "HSR 高鐵 · 北–南"
        lw = 300
        parts.append(f'<rect x="{mx - lw/2}" y="{my - 26}" width="{lw}" height="52" rx="26" '
                     f'fill="{steel}" stroke="#fff" stroke-width="2"/>')
        parts.append(f'<text x="{mx}" y="{my + 10}" font-size="28" fill="#fff" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">{esc(lbl)}</text>')

    # region cards
    for r in spec.get("regions", []):
        X, Y = r["x"], r["y"]
        rcol = r.get("color", accent)
        emb = r.get("emblem", "circle")
        rad = 20
        parts.append(f'<rect x="{X}" y="{Y}" width="{RW}" height="{RH}" rx="{rad}" '
                     f'fill="#ffffff" stroke="{rcol}" stroke-width="5"/>')
        # header strip in the region colour
        parts.append(f'<path d="M{X} {Y+rad} a {rad} {rad} 0 0 1 {rad} -{rad} h {RW-2*rad} '
                     f'a {rad} {rad} 0 0 1 {rad} {rad} v {60-rad} h -{RW} z" fill="{rcol}"/>')
        parts.append(emblem_svg(emb, X + 32, Y + 30, 15, "#ffffff"))
        parts.append(f'<text x="{X+58}" y="{Y+40}" font-size="34" fill="#fff" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(r.get("name",""))}</text>')
        # specialty chips (emblem-shaped, region colour, 繁體) with an English label under each
        specs = r.get("specialties", [])
        n = len(specs)
        chip_r = 30
        span = n * (2 * chip_r) + (n - 1) * 22
        x0 = X + (RW - span) / 2 + chip_r
        cy = Y + 118
        for i, sp in enumerate(specs):
            suit = resolve_suit(theme, sp.get("id", "")) if sp.get("id") in theme["suits"] else {}
            scol = suit.get("color", rcol)
            semb = suit.get("emblem", "circle")
            cx = x0 + i * (2 * chip_r + 22)
            tcol = pick_text_color(scol, dark=ink, light="#ffffff")
            parts.append(emblem_svg(semb, cx, cy, chip_r, scol, stroke=ink))
            parts.append(f'<text x="{cx}" y="{cy + chip_r*0.34}" font-size="30" fill="{tcol}" '
                         f'text-anchor="middle" font-family="{bfont}" font-weight="bold">{esc(sp.get("label",""))}</text>')
            parts.append(f'<text x="{cx}" y="{cy + chip_r + 34}" font-size="21" fill="{text}" '
                         f'text-anchor="middle" font-family="{bfont}">{esc(sp.get("en",""))}</text>')
        # Market-slots line, centred at the foot of the region card (clear of the header)
        slots = r.get("slots")
        if slots:
            parts.append(f'<text x="{X+RW/2}" y="{Y+RH-16}" font-size="23" fill="{rcol}" '
                         f'text-anchor="middle" font-family="{tfont}" font-weight="bold" '
                         f'letter-spacing="1">Market: {esc(slots)}</text>')

    # footer legend band — adjacency + pantry + start (no overlap with the diamond)
    notes = spec.get("notes", [])
    if notes:
        fy = H - 40 - len(notes) * 34
        parts.append(f'<rect x="0" y="{fy-30}" width="{W}" height="{H-(fy-30)}" fill="{ink}" opacity="0.06"/>')
        parts.append(f'<line x1="40" y1="{fy-30}" x2="{W-40}" y2="{fy-30}" stroke="{muted}" stroke-width="2" opacity="0.4"/>')
        for i, nt in enumerate(notes):
            parts.append(f'<circle cx="52" cy="{fy + i*34 - 8}" r="6" fill="{accent}"/>')
            parts.append(f'<text x="72" y="{fy + i*34}" font-size="26" fill="{text}" '
                         f'font-family="{bfont}">{esc(nt)}</text>')
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
        svg, W, H = render_regionmap(theme, spec)
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
