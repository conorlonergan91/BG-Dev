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
import sys
from pathlib import Path

# themes.py lives with the card pipeline; make it importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import get_theme, page_gradient, emblem_svg  # noqa: E402

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
        parts.append(f'<text x="{cx}" y="{cy+d*0.11}" font-size="{d*0.30}" fill="#ffffff" text-anchor="middle" '
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
                         f'font-family="{theme["body_font"]}" letter-spacing="1">{esc(z["label"]).upper()}</text>')
    for t in spec.get("texts", []):
        parts.append(f'<text x="{t["x"]}" y="{t["y"]}" font-size="{t.get("size",30)}" fill="{ink}" '
                     f'font-family="{theme["body_font"]}">{esc(t["text"])}</text>')
    return _svg(W, H, parts), W, H


def _svg(W, H, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            + "".join(parts) + "</svg>")


def main():
    ap = argparse.ArgumentParser(description="Render themed boards, tracks, and tokens.")
    ap.add_argument("--type", required=True, choices=["track", "tokens", "mat"])
    ap.add_argument("--theme", default="clean")
    ap.add_argument("--out", type=Path, default=Path("build/board.png"))
    # track
    ap.add_argument("--spaces", type=int, default=7)
    ap.add_argument("--title", default="")
    ap.add_argument("--labels", default="", help="comma-separated (per space, or per token)")
    ap.add_argument("--left-label", default="")
    ap.add_argument("--right-label", default="")
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
    else:  # mat
        if not args.spec:
            ap.error("--type mat requires --spec <file.json>")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        svg, W, H = render_mat(theme, spec)

    _save(svg, args.out, W, H)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
