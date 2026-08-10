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

# Scope icons ⦿/⬢/➤ AND the phase glyphs ☀/☾ are tofu under cairosvg's toy text API — draw them as SVG
# shapes inline in the player aid, matching the event-card badges + market-card phase badge (bg-access
# FIX A + §16.7). Keying ☀→sun / ☾→moon lets the aid's region/phase discard note draw the real glyphs.
SCOPE_GLYPH_SHAPE = {"⦿": "ring_dot", "⬢": "hex", "➤": "arrow", "☀": "sun", "☾": "moon"}


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
        ink, muted, accent = theme["ink"], theme["muted"], theme["accent"]
        tfont, bfont = theme["title_font"], theme["body_font"]
        default = theme["suits"].get("_default", {}).get("color", theme["accent"])
        d = min(diameter_px, 92)
        gap, pad = 22, 34
        row_h = d + gap
        name_x = pad + d + 28
        W = 1320
        # V7-M: the six per-colour Follower MEEPLE rows and the six Agent PAWN rows read as 12 near-identical
        # circles in a flat key. For Travel Agents ONLY (guarded by the theme's bespoke `back` wordmark),
        # collapse each into ONE grouped entry — a header + a strip of the six colour swatches — so the
        # follower POOLS (8 per colour) read as a family, clearly distinct from the one-per-player pawns.
        # Any other game (no TA wordmark) renders exactly as before — byte-identical.
        is_ta = theme.get("back", {}).get("wordmark") == "TRAVEL AGENTS"
        followers = [t for t in tokens if str(t.get("id", "")).lower().startswith("follower")]
        pawns = [t for t in tokens if str(t.get("id", "")).lower().startswith("pawn")]
        grouped = is_ta and (followers or pawns)
        ds = 66                                    # group-strip swatch size
        group_h = 44 + ds + gap                    # header + swatch strip
        if grouped:
            singles = [t for t in tokens
                       if not str(t.get("id", "")).lower().startswith(("follower", "pawn"))]
            H = (pad + len(singles) * row_h
                 + (group_h if followers else 0) + (group_h if pawns else 0) + pad)
        else:
            singles = tokens
            H = pad + len(tokens) * row_h + pad
        parts = [f'<defs>{page_gradient(theme, "pg")}</defs>',
                 f'<rect width="{W}" height="{H}" rx="26" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']

        def _swatch(cx, cy, dd, color, label):
            rad = dd / 2
            out = []
            if shape == "square":
                out.append(f'<rect x="{cx-rad}" y="{cy-rad}" width="{dd}" height="{dd}" rx="{dd*0.14}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            elif shape == "hex":
                pts = " ".join(f"{cx+rad*math.cos(math.radians(a))},{cy+rad*math.sin(math.radians(a))}" for a in range(0, 360, 60))
                out.append(f'<polygon points="{pts}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            else:
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{color}" stroke="{ink}" stroke-width="4"/>')
            tcol = pick_text_color(color, dark=ink, light="#ffffff")
            out.append(f'<text x="{cx}" y="{cy+dd*0.11}" font-size="{dd*0.34}" fill="{tcol}" text-anchor="middle" '
                       f'font-family="{tfont}" font-weight="bold">{esc(label)}</text>')
            return "".join(out)

        y = pad
        for t in singles:
            cy = y + d / 2
            cx = pad + d / 2
            color = t.get("color") or default
            parts.append(_swatch(cx, cy, d, color, t.get("label", "")))
            parts.append(f'<text x="{name_x}" y="{cy+10}" font-size="30" fill="{ink}" '
                         f'font-family="{bfont}">{esc(t.get("name","") or t.get("label",""))}</text>')
            parts.append(f'<text x="{W-pad}" y="{cy+10}" font-size="28" fill="{muted}" text-anchor="end" '
                         f'font-family="{tfont}" font-weight="bold">×{int(t.get("qty",1) or 1)}</text>')
            y += row_h

        def _group(members, title, subtitle, qty_label):
            nonlocal y
            parts.append(f'<text x="{pad}" y="{y+32}" font-size="30" fill="{accent}" '
                         f'font-family="{tfont}" font-weight="bold" letter-spacing="1">{esc(title)}</text>')
            parts.append(f'<text x="{W-pad}" y="{y+32}" font-size="26" fill="{muted}" text-anchor="end" '
                         f'font-family="{tfont}" font-weight="bold">{esc(qty_label)}</text>')
            scy = y + 44 + ds / 2
            for i, m in enumerate(members):
                scx = pad + ds / 2 + i * (ds + 16)
                parts.append(_swatch(scx, scy, ds, m.get("color") or default, m.get("label", "")))
            strip_right = pad + len(members) * (ds + 16) + 18
            parts.append(f'<text x="{strip_right}" y="{scy+9}" font-size="26" fill="{ink}" '
                         f'font-family="{bfont}">{esc(subtitle)}</text>')
            y += group_h

        if grouped and followers:
            _group(followers, "FOLLOWER MEEPLE POOLS · 粉",
                   "one pool per player colour (網紅 8; others 6)", "×8 per colour")
        if grouped and pawns:
            _group(pawns, "AGENT PAWNS", "one mover per player — NOT a follower", "×1 per colour")
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


# ---- region map (NEUTRAL shared N-player board, V7 · v3 CD REDESIGN) --------
def render_regionmap(theme, spec, phase="day"):
    """The shared TABLE board — V7 NEUTRAL board for 3-6 players, v3 (CD redesign 2026-08).

    SINGLE-PHASE PER FACE. The physical board is DOUBLE-SIDED and flips at dusk, so each `--phase`
    face shows ONLY that phase's components — the other phase's decks are in the box. So a face carries
    ONE 開團 Booking deck (face-down) + the shared face-up Booking row, and per region ONE phase MARKET
    deck + that region's face-up vendor slots. No day-and-night decks on one side.

    TEXTLESS · ICON-ONLY. Every play position is a SPACE with ONE small drawn ICON of the component
    that goes there — nothing more. The icon vocabulary (all DRAWN, no font glyphs → no tofu, legible
    at board scale, dual-coded by colour + emblem):
      • vendor slot  → a card-exact dashed footprint + a STALL glyph (awning + counter), region hue.
      • Booking deck → a face-down DECK glyph (offset stack) badged with a TICKET, booking-blue hue.
      • face-up Booking → a face-up CARD glyph (light card, folded corner) badged with a TICKET.
      • MARKET deck  → a face-down DECK glyph badged with a BOWL (ingredients), region hue.
      • Taipei start → a PAWN glyph in dashed pawn spaces (North hub).
      • regions      → colour + emblem + a single 繁體 glyph (▲北 / ◆中 / ●南 / ■東) — NO English words.
    Follower supplies + Trending 爆紅 are OFF the board (loose tokens beside each player's OWN board).
    NO off-board LEGEND band (CD steer 2026-08 — "get rid of the legend on the map"): the V7-M scarcity
    facts (SLOW / per-round refill timing, the per-count face-up slot totals, win→board / lose→own-supply,
    阿嬤 Travel-cost) + the region/phase discard cues live on the PLAYER AID and in the RULEBOOK, not here.
    The board stays a clean icon-only play surface; the freed bottom strip is margin under the warm glow.

    BARE HSR. A double-rail spine runs N↔S with a stop node at each end; the Scheduled-Maintenance
    EVENT card is simply placed on the track (self-evident — no 停 badge, no label). A tiny train ICON
    marks the line mid-spine.

    WARMTH. Soft region colour-zones (each panel tinted its region hue) sit over a stylised island
    underlay + a gentle central glow — warm gold by day, lantern-neon by night. Region identity colours
    stay warm in both states; only the chrome (frame / glow / phase badge) flips. Keeps the house hand
    (bold vector, night-market palette, inner gold hairline frame) so it matches the character boards.

    TA-specific — only games/travel-agents/make.sh calls --type regionmap."""
    W, H = 2280, 1680
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]

    ps = PHASE_STYLES.get((phase or "day").lower(), PHASE_STYLES["day"])
    is_night = (phase or "day").lower() == "night"
    ground = ps["page"]
    frame = ps["frame"]
    glow = ps.get("glow", frame)
    badge_emblem = ps.get("emblem", "sun")
    badge_char = "夜" if is_night else "日"
    steel = "#4A5A72"
    booking_col = theme["suits"].get("booking", {}).get("color", "#3A6EA5")

    # PER-REGION vendor footprints (V7-M SCARCITY, bg-infodesign 2026-08): the tightened single-slot model
    # draws each region's OWN slot count from map.json `regions[].slots_n` (the 4p HOME default: N 2, C/S/E
    # 1) instead of a flat 2 everywhere. This shows the scarce single-slot regions honestly — most regions
    # hold ONE contestable stall. The full per-count table (3p:4 / 4p:5 / 5p:5 / 6p:6, floor 1/region) and
    # the SLOW-refill timing live in the off-board LEGEND panel + the rulebook, not as per-space clutter.

    CARD_R = 0.714                 # 63.5 : 88.9 poker footprint ratio
    VW, VH = 120, 168             # a card-exact vendor / market / face-up footprint at board scale
    PAWN_R = 24

    # ------------------------------------------------------------------ ICON VOCABULARY (all drawn)
    def _pawn(cx, cy, r, col):
        head = f'<circle cx="{cx:.1f}" cy="{cy-r*0.5:.1f}" r="{r*0.42:.1f}" fill="{col}"/>'
        body = (f'<path d="M{cx-r*0.62:.1f} {cy+r*0.95:.1f} '
                f'C {cx-r*0.62:.1f} {cy+r*0.05:.1f} {cx-r*0.32:.1f} {cy-r*0.05:.1f} {cx:.1f} {cy-r*0.05:.1f} '
                f'C {cx+r*0.32:.1f} {cy-r*0.05:.1f} {cx+r*0.62:.1f} {cy+r*0.05:.1f} {cx+r*0.62:.1f} {cy+r*0.95:.1f} Z" '
                f'fill="{col}"/>')
        return head + body

    def _stall(cx, cy, r, col):
        # a market STALL: a scalloped awning over two posts + a counter — the vendor icon
        sw = max(2, r*0.14)
        roof = (f'<path d="M{cx-r:.1f} {cy-r*0.2:.1f} L{cx-r*0.78:.1f} {cy-r*0.64:.1f} '
                f'L{cx+r*0.78:.1f} {cy-r*0.64:.1f} L{cx+r:.1f} {cy-r*0.2:.1f} Z" fill="{col}"/>')
        scw = (2*r)/4.0
        scal = ""
        for i in range(4):
            sx = cx - r + i*scw
            scal += (f'<path d="M{sx:.1f} {cy-r*0.2:.1f} q {scw/2:.1f} {r*0.32:.1f} {scw:.1f} 0 Z" fill="{col}"/>')
        posts = (f'<line x1="{cx-r*0.72:.1f}" y1="{cy-r*0.2:.1f}" x2="{cx-r*0.72:.1f}" y2="{cy+r:.1f}" '
                 f'stroke="{col}" stroke-width="{sw:.1f}"/>'
                 f'<line x1="{cx+r*0.72:.1f}" y1="{cy-r*0.2:.1f}" x2="{cx+r*0.72:.1f}" y2="{cy+r:.1f}" '
                 f'stroke="{col}" stroke-width="{sw:.1f}"/>')
        counter = (f'<line x1="{cx-r*0.92:.1f}" y1="{cy+r:.1f}" x2="{cx+r*0.92:.1f}" y2="{cy+r:.1f}" '
                   f'stroke="{col}" stroke-width="{max(2,r*0.18):.1f}" stroke-linecap="round"/>')
        return roof + scal + posts + counter

    def _bowl(cx, cy, r, col):
        # a steaming BOWL — the ingredient / MARKET icon (distinct from the ticket)
        bowl = f'<path d="M{cx-r:.1f} {cy+r*0.05:.1f} A {r:.1f} {r:.1f} 0 0 0 {cx+r:.1f} {cy+r*0.05:.1f} Z" fill="{col}"/>'
        rim = (f'<ellipse cx="{cx:.1f}" cy="{cy+r*0.05:.1f}" rx="{r:.1f}" ry="{r*0.22:.1f}" '
               f'fill="none" stroke="{col}" stroke-width="{max(2,r*0.13):.1f}"/>')
        steam = ""
        for dx in (-r*0.42, r*0.42):
            sx = cx + dx
            steam += (f'<path d="M{sx:.1f} {cy-r*0.22:.1f} q {r*0.3:.1f} -{r*0.34:.1f} 0 -{r*0.68:.1f}" '
                      f'fill="none" stroke="{col}" stroke-width="{max(2,r*0.12):.1f}" '
                      f'stroke-linecap="round" opacity="0.85"/>')
        return steam + bowl + rim

    def _train(cx, cy, r, col):
        nose = (f'<path d="M{cx-r*0.82:.1f} {cy-r*0.4:.1f} q 0 -{r*0.72:.1f} {r*0.82:.1f} -{r*0.72:.1f} '
                f'q {r*0.82:.1f} 0 {r*0.82:.1f} {r*0.72:.1f} Z" fill="{col}"/>')
        body = f'<rect x="{cx-r*0.82:.1f}" y="{cy-r*0.5:.1f}" width="{r*1.64:.1f}" height="{r*1.5:.1f}" rx="{r*0.28:.1f}" fill="{col}"/>'
        win = f'<rect x="{cx-r*0.52:.1f}" y="{cy-r*0.5:.1f}" width="{r*1.04:.1f}" height="{r*0.5:.1f}" rx="{r*0.1:.1f}" fill="#ffffff" opacity="0.92"/>'
        wheels = (f'<circle cx="{cx-r*0.4:.1f}" cy="{cy+r*0.9:.1f}" r="{r*0.18:.1f}" fill="{col}"/>'
                  f'<circle cx="{cx+r*0.4:.1f}" cy="{cy+r*0.9:.1f}" r="{r*0.18:.1f}" fill="{col}"/>')
        return nose + body + win + wheels

    def _deck(x, y, w, h, col, emb):
        # a face-down DECK: an offset stack + a drawn emblem badge on the back (NO text)
        tc = pick_text_color(col, dark=ink, light="#ffffff")
        d = [f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" rx="12" fill="{ink}" opacity="0.16"/>',
             f'<rect x="{x+4}" y="{y+4}" width="{w}" height="{h}" rx="12" fill="{col}" opacity="0.55"/>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" stroke="{ink}" stroke-width="3"/>',
             f'<rect x="{x+9}" y="{y+9}" width="{w-18}" height="{h-18}" rx="8" fill="none" '
             f'stroke="#ffffff" stroke-width="2" opacity="0.55"/>',
             emb(x + w/2, y + h/2, min(w, h)*0.26, tc)]
        return "".join(d)

    def _faceup(x, y, w, h, col, emb):
        # a FACE-UP card space: light card, coloured border, a folded corner (reads as a card front)
        s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" opacity="0.85" '
             f'stroke="{col}" stroke-width="3"/>',
             f'<path d="M{x+w-24} {y} L{x+w} {y+24} L{x+w-24} {y+24} Z" fill="{col}" opacity="0.85"/>',
             emb(x + w/2, y + h/2, min(w, h)*0.26, col)]
        return "".join(s)

    def _vendor_space(x, y, w, h, rcol):
        # an empty card-exact vendor SLOT: dashed footprint + the stall glyph in the region hue
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" opacity="0.5" '
                f'stroke="{rcol}" stroke-width="2.5" stroke-dasharray="9 6"/>'
                + _stall(x + w/2, y + h/2, min(w, h)*0.24, rcol))

    # ------------------------------------------------------------------ DEFS + base
    defs = [page_gradient(theme, "pg", ground),
            f'<radialGradient id="glowA" cx="50%" cy="54%" r="60%">'
            f'<stop offset="0" stop-color="{glow}" stop-opacity="0.5"/>'
            f'<stop offset="0.55" stop-color="{glow}" stop-opacity="0.12"/>'
            f'<stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>',
            f'<radialGradient id="glowB" cx="50%" cy="50%" r="60%">'
            f'<stop offset="0" stop-color="{frame}" stop-opacity="0.20"/>'
            f'<stop offset="1" stop-color="{frame}" stop-opacity="0"/></radialGradient>']
    parts = [f'<defs>{"".join(defs)}</defs>',
             f'<rect width="{W}" height="{H}" rx="30" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>']

    # ------------------------------------------------------------------ WARMTH underlay (behind spaces)
    # a soft stylised island of Taiwan down the spine + a gentle central glow (warm day / neon night)
    parts.append(f'<path d="M1140 360 C 1376 512 1440 760 1308 1012 '
                 f'C 1226 1198 1170 1332 1120 1376 '
                 f'C 1072 1332 978 1198 944 1012 '
                 f'C 850 760 914 512 1140 360 Z" fill="{frame}" opacity="0.06"/>')
    parts.append(f'<ellipse cx="1140" cy="900" rx="1040" ry="720" fill="url(#glowA)"/>')
    parts.append(f'<ellipse cx="1140" cy="820" rx="640" ry="520" fill="url(#glowB)"/>')

    # inner hairline frame — the SAME house treatment as the character boards
    parts.append(f'<rect x="26" y="26" width="{W-52}" height="{H-52}" rx="22" fill="none" '
                 f'stroke="{frame}" stroke-width="2" opacity="0.5"/>')

    # ------------------------------------------------------------------ TITLE band REMOVED (CD steer):
    # no title band / phase badge on the map. Day vs night reads from the warm-gold vs lantern-neon
    # chrome (frame + central glow) that already flips per --phase. The freed top area is clean margin.

    # ------------------------------------------------------------------ BOOKING (single-phase clock)
    # ONE face-down Booking deck → the shared face-up Booking row. Icons only; no explainer text.
    strip_y = 152
    dw, dh = 120, 168
    fw, fh = 108, 150
    strip_w = dw + 44 + 4*fw + 3*14
    x0 = (W - strip_w) / 2
    parts.append(f'<rect x="{x0-30:.0f}" y="{strip_y-22}" width="{strip_w+60:.0f}" height="{dh+44}" '
                 f'rx="20" fill="#ffffff" opacity="0.20"/>')
    ticket = lambda cx, cy, r, c: emblem_svg("ticket", cx, cy, r, c)
    parts.append(_deck(x0, strip_y, dw, dh, booking_col, ticket))
    ax = x0 + dw + 8
    parts.append(f'<path d="M{ax:.0f} {strip_y+dh/2:.0f} h 30 m -11 -10 l 11 10 l -11 10" '
                 f'fill="none" stroke="{muted}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    fx0 = x0 + dw + 44
    fu_y = strip_y + (dh - fh) / 2
    for i in range(4):
        parts.append(_faceup(fx0 + i*(fw+14), fu_y, fw, fh, booking_col, ticket))

    # ------------------------------------------------------------------ REGION DIAMOND
    PW_NS, PW_CE, PH = 640, 560, 340
    centers = {"north": (1140, 560), "central": (520, 862), "east": (1760, 862), "south": (1140, 1164)}
    pwidth = {"north": PW_NS, "south": PW_NS, "central": PW_CE, "east": PW_CE}
    region_char = {"north": "北", "central": "中", "south": "南", "east": "東"}

    def tl(key):
        cx, cy = centers[key]
        return cx - pwidth[key] / 2, cy - PH / 2

    # adjacency ring — trimmed to span only the GAP between panel borders (so a connector never stabs
    # across a region's card content, which sits over the panel centre).
    def _edge(cx, cy, hw, hh, dx, dy):
        t = min(hw / abs(dx), hh / abs(dy)) if dx and dy else (hw / abs(dx) if dx else hh / abs(dy))
        return cx + t * dx, cy + t * dy
    for a, b in spec.get("ring", []):
        if a in centers and b in centers:
            (x1, y1), (x2, y2) = centers[a], centers[b]
            dx, dy = x2 - x1, y2 - y1
            ex1, ey1 = _edge(x1, y1, pwidth[a] / 2 + 4, PH / 2 + 4, dx, dy)
            ex2, ey2 = _edge(x2, y2, pwidth[b] / 2 + 4, PH / 2 + 4, -dx, -dy)
            parts.append(f'<line x1="{ex1:.0f}" y1="{ey1:.0f}" x2="{ex2:.0f}" y2="{ey2:.0f}" stroke="{muted}" '
                         f'stroke-width="13" stroke-linecap="round" opacity="0.45"/>')

    # BARE HSR double-rail spine (N↔S) + a stop node at each end + a small train ICON mid-spine
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
            parts.append(f'<line x1="{x1-(off+5)}" y1="{ty:.1f}" x2="{x1+(off+5)}" y2="{ty:.1f}" '
                         f'stroke="{steel}" stroke-width="4"/>')
        for sty in (sy, ey):
            parts.append(f'<circle cx="{x1}" cy="{sty}" r="12" fill="#ffffff" stroke="{steel}" stroke-width="5"/>')
        parts.append(_train(x1, (sy + ey) / 2, 26, steel))

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
        # soft region colour-ZONE (warmth, tinted the region hue) + a crisp coloured border
        parts.append(f'<rect x="{X}" y="{Y}" width="{PWc}" height="{PH}" rx="{rad}" fill="{rcol}" opacity="0.14"/>')
        parts.append(f'<rect x="{X}" y="{Y}" width="{PWc}" height="{PH}" rx="{rad}" fill="none" '
                     f'stroke="{rcol}" stroke-width="3.5"/>')
        # compact region BADGE — colour + emblem + a single 繁體 glyph (NO English word)
        bw, bh = 96, 52
        parts.append(f'<rect x="{X+16}" y="{Y+16}" width="{bw}" height="{bh}" rx="14" fill="{rcol}"/>')
        parts.append(emblem_svg(emb, X+16+30, Y+16+bh/2, 15, "#ffffff"))
        parts.append(f'<text x="{X+16+68}" y="{Y+16+bh*0.70:.0f}" font-size="34" fill="#fff" '
                     f'text-anchor="middle" font-family="{tfont}" font-weight="bold">{esc(region_char.get(key,""))}</text>')

        # signature-ingredient chips (emblem + 繁體 only; no English)
        chips = r.get("chips", [])
        ccx0 = X + 16 + bw + 30
        ccy = Y + 16 + bh/2
        for i, sp in enumerate(chips):
            suit = resolve_suit(theme, sp.get("id", "")) if sp.get("id") in theme["suits"] else {}
            scol = suit.get("color", rcol)
            semb = suit.get("emblem", "circle")
            cx = ccx0 + i*84
            tcol = pick_text_color(scol, dark=ink, light="#ffffff")
            parts.append(emblem_svg(semb, cx, ccy, 22, scol, stroke=ink))
            parts.append(f'<text x="{cx}" y="{ccy+8:.0f}" font-size="24" fill="{tcol}" text-anchor="middle" '
                         f'font-family="{bfont}" font-weight="bold">{esc(sp.get("label",""))}</text>')

        # bottom row: this region's OWN vendor slots (slots_n) + the region MARKET deck (single phase)
        gap = 16
        try:
            nslots = int(r.get("slots_n", 1) or 1)
        except (TypeError, ValueError):
            nslots = 1
        nslots = max(1, nslots)                    # floor 1 per region
        n_cells = nslots + 1
        block_w = n_cells * VW + (n_cells - 1) * gap
        x_start = X + PWc - 26 - block_w
        row_y = Y + PH - VH - 18
        for i in range(nslots):
            parts.append(_vendor_space(x_start + i*(VW+gap), row_y, VW, VH, rcol))
        parts.append(_deck(x_start + nslots*(VW+gap), row_y, VW, VH, rcol, _bowl))

        # North is the shared START (Taipei) — dashed PAWN spaces with the pawn glyph (no text)
        if r.get("start"):
            for i in range(3):
                px = X + 60 + i*58
                py = Y + PH - VH/2 - 6
                parts.append(f'<circle cx="{px}" cy="{py:.0f}" r="{PAWN_R}" fill="#ffffff" opacity="0.5" '
                             f'stroke="{rcol}" stroke-width="2" stroke-dasharray="6 5"/>')
                parts.append(_pawn(px, py-2, PAWN_R*0.9, rcol))

    # ------------------------------------------------------------------ NO OFF-BOARD LEGEND (CD steer 2026-08)
    # The off-board LEGEND band is REMOVED per the CD ("get rid of the legend on the map"). The scarcity /
    # slow-refill timing, the per-count face-up slot totals, and the win→board / lose→own-supply + 阿嬤
    # Travel-cost notes now live on the PLAYER AID (components/player-aid.json) and in the rulebook — NOT on
    # the shared table board, which stays a clean icon-only play surface. `vendor_slots` / `legend_notes`
    # stay in map.json (still valid data; the per-region slot count is read above via slots_n) — they are
    # simply no longer painted onto the map. The freed bottom strip is clean margin under the warm glow.

    return _svg(W, H, parts), W, H


# ---- Closing-Time die (關門) — a printable 6-FACE reference sheet ------------
def render_die(theme, spec):
    """The Closing-Time die 關門 as a 6-face reference sheet (a printable / Screentop d6 key).

    A custom d6: 4 REGION faces (North 北 / Central 中 / South 南 / East 東) + 2 BLANK faces (the 1/3
    reprieve). Every region face is dual-coded per bg-access — the region's established COLOUR *and* its
    emblem *and* its 繁體 character — so the die reads without relying on colour alone. Colours/emblems are
    reused straight from map.json's regions (the same hues the map + vendors use), never minted here.

    TA-specific — only games/travel-agents/make.sh calls --type die."""
    ink, accent, muted, text = theme["ink"], theme["accent"], theme["muted"], theme["text"]
    tfont, bfont = theme["title_font"], theme["body_font"]

    # Region colour + emblem come from the shared map spec; the 繁體 char + English name are fixed canon.
    region_char = {"north": "北", "central": "中", "south": "南", "east": "東"}
    region_en = {"north": "NORTH", "central": "CENTRAL", "south": "SOUTH", "east": "EAST"}
    by_key = {r.get("key"): r for r in spec.get("regions", [])}
    order = ["north", "central", "south", "east"]
    faces = []
    for key in order:
        r = by_key.get(key, {})
        faces.append({
            "kind": "region",
            "color": r.get("color", accent),
            "emblem": r.get("emblem", "circle"),
            "char": region_char.get(key, ""),
            "en": region_en.get(key, key.upper()),
        })
    # the two reprieve faces
    faces.append({"kind": "blank"})
    faces.append({"kind": "blank"})

    # layout: a 3×2 grid of die-face tiles under a title band
    TILE = 460
    GAP = 52
    PADX = 70
    title_h = 176
    foot_h = 74
    cols, rows_n = 3, 2
    W = PADX * 2 + cols * TILE + (cols - 1) * GAP
    H = title_h + rows_n * TILE + (rows_n - 1) * GAP + foot_h + 40

    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#pg)"/>']

    # --- title band -----------------------------------------------------------
    parts.append(f'<rect x="0" y="0" width="{W}" height="{title_h}" fill="{theme["ink"]}"/>')
    # a small die glyph (rounded square + 3 pips) left of the wordmark, so the band reads "a die"
    dx, dy, dr = 92, title_h / 2, 52
    parts.append(f'<rect x="{dx-dr}" y="{dy-dr}" width="{2*dr}" height="{2*dr}" rx="16" fill="#ffffff"/>')
    for (ox, oy) in [(-0.42, -0.42), (0, 0), (0.42, 0.42)]:
        parts.append(f'<circle cx="{dx+ox*dr:.0f}" cy="{dy+oy*dr:.0f}" r="{dr*0.13:.0f}" fill="{theme["ink"]}"/>')
    parts.append(f'<text x="{dx+dr+40}" y="{title_h*0.44:.0f}" font-size="58" fill="#ffffff" '
                 f'font-family="{tfont}" font-weight="bold">Closing-Time Die 關門</text>')
    parts.append(f'<text x="{dx+dr+40}" y="{title_h*0.78:.0f}" font-size="30" fill="#F7F1E3" '
                 f'font-family="{bfont}">A custom d6 · 4 region faces + 2 blank (1-in-3 reprieve)</text>')

    def _face_tile(x, y, f, idx):
        s = []
        # face-index numeral (top-left) so the sheet reads as the six faces of ONE die
        s.append(f'<text x="{x+18}" y="{y+42}" font-size="30" fill="{muted}" '
                 f'font-family="{tfont}" font-weight="bold" opacity="0.7">{idx}</text>')
        cx = x + TILE / 2
        if f["kind"] == "region":
            col = f["color"]
            # die-face tile: light region-tinted ground + a thick region-colour edge (a physical die face)
            s.append(f'<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="46" fill="{col}" opacity="0.12"/>')
            s.append(f'<rect x="{x+6}" y="{y+6}" width="{TILE-12}" height="{TILE-12}" rx="42" fill="none" '
                     f'stroke="{col}" stroke-width="10"/>')
            # emblem (the SHAPE channel) — upper; sits clear of the CJK char below
            s.append(emblem_svg(f["emblem"], cx, y + 132, 70, col, stroke=ink))
            # 繁體 character (the CJK channel) — big, centred
            s.append(f'<text x="{cx}" y="{y+322:.0f}" font-size="120" fill="{col}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">{esc(f["char"])}</text>')
            # English region name + a terse "what it does" caption (both clear of the char)
            s.append(f'<text x="{cx}" y="{y+392:.0f}" font-size="33" fill="{col}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="3">{esc(f["en"])}</text>')
            s.append(f'<text x="{cx}" y="{y+428:.0f}" font-size="20" fill="{muted}" text-anchor="middle" '
                     f'font-family="{bfont}" font-style="italic">closes this region\'s oldest face-up stall</text>')
        else:
            # BLANK face — neutral grey, empty; visibly a NON-region face (reprieve, nothing closes)
            grey = "#8A8F98"
            s.append(f'<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="46" fill="{grey}" opacity="0.08"/>')
            s.append(f'<rect x="{x+6}" y="{y+6}" width="{TILE-12}" height="{TILE-12}" rx="42" fill="none" '
                     f'stroke="{grey}" stroke-width="8" stroke-dasharray="20 16"/>')
            # a soft open ring with a dash (not a slash — nothing is forbidden; simply no region comes up)
            s.append(f'<circle cx="{cx}" cy="{y+180}" r="80" fill="none" stroke="{grey}" '
                     f'stroke-width="10" opacity="0.55"/>')
            s.append(f'<text x="{cx}" y="{y+198:.0f}" font-size="60" fill="{grey}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold">—</text>')
            s.append(f'<text x="{cx}" y="{y+340:.0f}" font-size="40" fill="{grey}" text-anchor="middle" '
                     f'font-family="{tfont}" font-weight="bold" letter-spacing="3">BLANK</text>')
            s.append(f'<text x="{cx}" y="{y+400:.0f}" font-size="23" fill="{muted}" text-anchor="middle" '
                     f'font-family="{bfont}" font-style="italic">reprieve — no stall closes</text>')
        return "".join(s)

    for i, f in enumerate(faces):
        c = i % cols
        rr = i // cols
        x = PADX + c * (TILE + GAP)
        y = title_h + 30 + rr * (TILE + GAP)
        parts.append(_face_tile(x, y, f, i + 1))

    # --- footer: the dual-coding note + when it rolls ---------------------------
    fy = H - foot_h + 34
    parts.append(f'<text x="{PADX}" y="{fy}" font-size="26" fill="{muted}" font-family="{bfont}">'
                 f'Roll after track round L (L=2 at 3p · L=3 at 4-6p). '
                 f'Dual-coded: colour + emblem + 繁體 — never colour alone.</text>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<defs>{page_gradient(theme, "pg")}</defs>' + "".join(parts) + "</svg>")
    return svg, W, H


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


def _pb_follower_cost(cx, cy, n, fcol, tfont):
    """A small SECONDARY sub-marker for a follower COST: one follower dot (the follower/crowd hue) badged
    with a '-N' chip. Used to hint the V7-M meeple costs baked into two abilities (阿嬤's Travel-anywhere,
    大胃王's greedy-4th) without crowding the primary read."""
    return (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{fcol}"/>'
            + _pb_chip(cx+18, cy+7, f"-{n}", fcol, tfont, r=14))


def _pb_kit_glyph(cx, cy, code, col, ink, tfont, follower_col="#6A4C93"):
    """The Travel-Agents CHARACTER icon vocabulary — ONE consistent drawn glyph per ability/flaw code,
    the same meaning everywhere. Icons are memory anchors; the block TEXT carries the precise rule.
    Every shape is DRAWN (no font glyphs) so nothing renders tofu (bg-infodesign / bg-access).

    V7-M meeple/scarcity recode: the dead dial/discount codes (discount_home / away_tax / start_max_4 /
    win_ties) are RETIRED; the new roster codes are favours_home_draw (里長伯), deep_pool (網紅) and
    margin_win:N (大哥, param-driven off the retired two-bars glyph), plus the follower-cost sub-markers on
    travel_anywhere (阿嬤) and visit_keep3 (大胃王)."""
    e = emblem_svg
    base = code.split(":")[0]         # strip a ':N' parameter (e.g. margin_win:1)
    if code == "favours_home_draw":   # 里長伯: a home + an INBOUND card → goodwill drawn to you AT HOME
        house = e("home", cx-16, cy, 26, col, stroke=ink)
        card = (f'<rect x="{cx+18}" y="{cy-17}" width="27" height="37" rx="5" '
                f'fill="#ffffff" stroke="{col}" stroke-width="3"/>')
        arrow = (f'<path d="M{cx+16} {cy+2} l -13 0 m 6 -6 l -6 6 l 6 6" fill="none" '
                 f'stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        return house + card + arrow
    if code == "travel_draw_left":    # ring + back-chevron → draw the region you LEFT
        return (f'<circle cx="{cx}" cy="{cy}" r="27" fill="none" stroke="{col}" stroke-width="4"/>'
                f'<polyline points="{cx+8},{cy-13} {cx-9},{cy} {cx+8},{cy+13}" fill="none" '
                f'stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    if code == "visit_keep3":         # 大胃王: three stacked cards + '3' → keep all 3 on a Visit;
        cards = "".join(f'<rect x="{cx-26+i*10:.0f}" y="{cy-22-i*6:.0f}" width="32" height="44" rx="6" '
                        f'fill="#ffffff" stroke="{col}" stroke-width="3"/>' for i in range(3))
        # + a secondary follower-cost marker: the greedy 4th returns 1 follower to your supply
        return (cards + _pb_chip(cx+40, cy-16, "3", col, tfont)
                + _pb_follower_cost(cx+22, cy+30, "1", follower_col, tfont))
    if code == "hazard_twice_visit":  # warning triangle + '×2' → hazards fire twice on his Visit
        return e("triangle", cx, cy, 25, col, stroke=ink) + _pb_chip(cx+34, cy+24, "×2", col, tfont)
    if code == "deep_pool":           # 網紅: a big crowd + '8' → she owns 8 followers (the field owns 6)
        return e("crowd", cx, cy, 30, col) + _pb_chip(cx+42, cy+22, "8", col, tfont)
    if code == "travel_anywhere":     # 阿嬤 elder pass: a hub linked to all FOUR regions → go anywhere in one Travel
        s = f'<circle cx="{cx}" cy="{cy}" r="9" fill="{col}"/>'
        for dx, dy in [(1, -1), (-1, -1), (1, 1), (-1, 1)]:
            ex, ey = cx + dx*27, cy + dy*22
            s += f'<line x1="{cx}" y1="{cy}" x2="{ex}" y2="{ey}" stroke="{col}" stroke-width="3.5" opacity="0.85"/>'
            s += e("diamond", ex, ey, 9, col, stroke=ink)
        # + a secondary follower-cost marker: each Travel-anywhere costs 1 follower to supply (baseline)
        return s + _pb_follower_cost(cx+40, cy+34, "1", follower_col, tfont)
    if code == "goes_last":           # a queue of 3 dots, last one ringed → take the last seat
        dots = "".join(f'<circle cx="{cx-26+i*26:.0f}" cy="{cy}" r="9" fill="{col}" '
                       f'opacity="{0.38 if i<2 else 1}"/>' for i in range(3))
        return dots + f'<circle cx="{cx+26}" cy="{cy}" r="15" fill="none" stroke="{col}" stroke-width="3"/>'
    if base in ("margin_win", "bribe_margin"):   # 大哥: two bars, yours taller + 'N' → win a contest by margin N
        m = re.search(r'(\d+)', code)
        n = m.group(1) if m else "1"
        return (f'<rect x="{cx-22}" y="{cy-4}" width="15" height="30" rx="3" fill="{col}" opacity="0.42"/>'
                f'<rect x="{cx+3}" y="{cy-20}" width="15" height="46" rx="3" fill="{col}"/>'
                + _pb_chip(cx+42, cy-2, n, col, tfont))
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
    full-height character image + the FOLLOWER POOL/SUPPLY lifecycle panel down the left column.

    Layout (v2 · V7-M meeples):
       • TITLE band — English name TOP-LEFT (e.g. "The Globetrotter"); 漢字 TOP-RIGHT with the Tâi-lô
         romanisation as a subtitle directly under it (阿嬤 / A-má); the ABILITY + FLAW ICON-ONLY medallions
         (drawn glyphs, NO keyword/explainer text) sit CENTRED in the band — ability teal LEFT, flaw
         vermilion RIGHT (fixed position + hue tells which-is-which without a label).
       • LEFT column, full height — the character IMAGE (embedded mock-up when present, else placeholder)
         at top, and UNDER it the FOLLOWER lifecycle panel: three bins showing the meeple states left→right
         — SUPPLY (un-rallied) → grow on a Travel → YOUR BOARD (rallied) → place on a Promote → ON A STALL
         (committed). The character's `max` (網紅 8, field 6) and `start_meeples` (2) are surfaced in a pill
         and by the drawn meeple counts. REPLACES the retired 0–8 Followers dial.
       • RIGHT column — a short funny PROSE one-liner (from `blurb`) under the banner, then the TWO
         card-EXACT-footprint drop zones CANCELLED 取消 · COMPLETE 成團 (a real Booking card stacks on each).

    REMOVED in this v2 (all moved to the rulebook): the bottom footer (scoring line + hand-limit-3 +
    Rave-Reviews), the "icons are reminders" caption, and the old FOLLOWERS card-zone.

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
    # V7-M meeples: surface each character's OWN pool from the data — `max` followers exist in your colour
    # (網紅 8, field 6), `start_meeples` of them start on your board (the rest in your supply).
    try:
        pool_max = int(float(row.get("max") or 6))
    except (TypeError, ValueError):
        pool_max = 6
    try:
        start_n = int(float(row.get("start_meeples") or 2))
    except (TypeError, ValueError):
        start_n = 2
    start_n = max(0, min(start_n, pool_max))
    supply_n = pool_max - start_n

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
            _pb_kit_glyph(cx, med_cy, code, col, ink, tfont, follower_col=violet)])
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

    # --- FOLLOWERS → ONE card slot in the right-column row (V7-M · CD steer 2026-08) --------------------
    # The three-bin SUPPLY→BOARD→STALL lifecycle panel is RETIRED. Followers now get ONE card-shaped slot
    # sitting in a row with the two scoring piles, so the board reads as three identical card sections:
    # Followers | Cancelled | Complete (each icon-in-the-middle, no text). The follower LIFECYCLE words
    # move to the player aid (the board stays icon-only). `_follower` (kept) draws the slot's centre icon.
    def _follower(cx, cy, s, filled):
        """A follower MEEPLE glyph (round head + flared body). filled → solid; hollow → violet outline."""
        fill = violet if filled else "#ffffff"
        head = (f'<circle cx="{cx:.0f}" cy="{cy-s*0.62:.0f}" r="{s*0.34:.0f}" '
                f'fill="{fill}" stroke="{violet}" stroke-width="{max(3, s*0.10):.0f}"/>')
        body = (f'<path d="M{cx-s*0.62:.0f} {cy+s:.0f} '
                f'C {cx-s*0.62:.0f} {cy-s*0.08:.0f} {cx-s*0.3:.0f} {cy-s*0.2:.0f} {cx:.0f} {cy-s*0.2:.0f} '
                f'C {cx+s*0.3:.0f} {cy-s*0.2:.0f} {cx+s*0.62:.0f} {cy-s*0.08:.0f} {cx+s*0.62:.0f} {cy+s:.0f} Z" '
                f'fill="{fill}" stroke="{violet}" stroke-width="{max(3, s*0.10):.0f}"/>')
        return head + body

    # ==================== RIGHT COLUMN: prose one-liner + THREE card sections in a row ===================
    # Prose banner and the pile tray share ONE centred width so they stack as a tidy module (rather than a
    # single vast tray floating in void); clean board-background margins sit either side.
    right_l = img_x + IMG_W + 60                    # 1030
    right_r = W - M                                 # 3438
    right_w = right_r - right_l                     # 2408
    zgap = 50
    inner_pad = 24
    col_w = 3*CARD_W + 2*zgap + 2*inner_pad          # 2398 — hugs the THREE poker footprints
    col_x = right_l + (right_w - col_w) / 2          # centred in the right column

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

    # --- THREE card-EXACT-footprint sections in a row: FOLLOWERS | CANCELLED | COMPLETE (CD steer 2026-08).
    # Each is exactly one poker footprint (750×1050) so real meeples / Booking cards sit on it, styled
    # identically, ICON-IN-THE-MIDDLE, NO TEXT (the board is icon-only; the player aid carries the words).
    # Distinguished by SHAPE + colour (CVD-safe): a follower meeple (violet) · a slashed stamp = cancelled
    # (taupe) · a checked stamp = complete (gold). The follower slot is where YOUR gained followers live.
    tray_pad_top, tray_pad_bot = 70, 40
    tray_h = tray_pad_top + CARD_H + tray_pad_bot
    tray_y = ps_y + ps_h + ((H - M) - (ps_y + ps_h) - tray_h) / 2   # centred below the prose
    tray_x, tray_w = col_x, col_w
    P.append(f'<rect x="{tray_x}" y="{tray_y}" width="{tray_w}" height="{tray_h}" rx="24" '
             f'fill="#ffffff" opacity="0.28" stroke="{gold}" stroke-width="3"/>')

    zx = [tray_x + inner_pad + i*(CARD_W + zgap) for i in range(3)]
    card_top = tray_y + tray_pad_top

    def _card_zone(x0, emcol):
        return (f'<rect x="{x0}" y="{card_top}" width="{CARD_W}" height="{CARD_H}" rx="16" fill="#ffffff" '
                f'opacity="0.5" stroke="{emcol}" stroke-width="4" stroke-dasharray="14 10"/>')
    icx = lambda i: zx[i] + CARD_W/2
    icy = card_top + CARD_H/2
    # FOLLOWERS — a single large follower meeple (your gained followers live here)
    P.append(_card_zone(zx[0], violet) + _follower(icx(0), icy - 40, 210, True))
    # CANCELLED — a passport stamp with a bold diagonal slash (void); taupe
    P.append(_card_zone(zx[1], taupe)
             + emblem_svg("stamp", icx(1), icy, 150, taupe, stroke=ink)
             + f'<line x1="{icx(1)-150}" y1="{icy+150}" x2="{icx(1)+150}" y2="{icy-150}" '
               f'stroke="{taupe}" stroke-width="22" stroke-linecap="round"/>')
    # COMPLETE — a passport stamp with a bold check (done); gold
    P.append(_card_zone(zx[2], gold_pile)
             + emblem_svg("stamp", icx(2), icy, 150, gold_pile, stroke=ink)
             + f'<path d="M{icx(2)-110} {icy+6} l 70 80 l 150 -170" fill="none" stroke="{gold_pile}" '
               f'stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>')

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
                    choices=["track", "tokens", "mat", "aid", "regionmap", "die", "scoretrack", "playerboard"])
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
                    tokens.append({"id": row.get("id", ""), "label": row.get("label", ""),
                                   "color": row.get("color") or None,
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
    elif args.type == "die":
        if not args.spec:
            ap.error("--type die requires --spec <map.json> (region colours/emblems)")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_die(theme, spec)
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
