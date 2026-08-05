#!/usr/bin/env python3
"""
build_cover.py — a cheap, themed, procedural cover/box image for a prototype.

No AI art and no asset files: the cover is built from vector shapes tinted by the chosen theme, so it's
instant, deterministic, and gives a Screentop/TTS table (or a sell sheet) a basic sense of style. It is
a *placeholder vibe*, not final art — swap in real illustration later.

Usage
-----
    python build_cover.py --title "Beacon" --subtitle "Two keepers. One coast." \
        --theme nautical --players 2 --time "20 min" --weight 1.8 --out build/cover.png

Motifs: `nautical`, `ember`, and a `generic` fallback (works for any theme). Add more in MOTIFS.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from themes import get_theme, emblem_svg


# ---- colour helpers ---------------------------------------------------------
def _rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _hex(t): return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in t)
def blend(c1, c2, t): a, b = _rgb(c1), _rgb(c2); return _hex(tuple(a[i] + (b[i]-a[i])*t for i in range(3)))
def darken(c, t=0.25): return blend(c, "#000000", t)
def lighten(c, t=0.25): return blend(c, "#ffffff", t)


# ---- motifs (return an SVG fragment sized to WxH) ---------------------------
def motif_nautical(W, H, theme):
    ink, accent = theme["ink"], theme["accent"]
    sea = darken(ink, 0.1)
    y_sea = H * 0.70
    cx = W * 0.5
    lx, lw = cx, W * 0.085
    top = H * 0.34
    # beams from the lantern
    beams = (f'<polygon points="{cx},{top} {W*0.02},{H*0.10} {W*0.10},{top*0.6}" fill="{accent}" opacity="0.12"/>'
             f'<polygon points="{cx},{top} {W*0.98},{H*0.10} {W*0.90},{top*0.6}" fill="{accent}" opacity="0.12"/>')
    # moon + stars
    sky = (f'<circle cx="{W*0.80}" cy="{H*0.16}" r="{W*0.055}" fill="{lighten(accent,0.5)}" opacity="0.9"/>'
           + "".join(emblem_svg("spark", W*x, H*y, W*0.012, lighten(ink, 0.6))
                     for x, y in [(0.15, 0.12), (0.30, 0.20), (0.62, 0.10), (0.88, 0.30)]))
    # tower with stripes
    stripes = ""
    seg = (y_sea - top) / 5
    for i in range(5):
        stripes += (f'<rect x="{lx-lw/2}" y="{top + i*seg}" width="{lw}" height="{seg}" '
                    f'fill="{"#f4f4f2" if i % 2 == 0 else accent}"/>')
    tower = (f'<polygon points="{lx-lw/2},{y_sea} {lx-lw*0.35},{top} {lx+lw*0.35},{top} {lx+lw/2},{y_sea}" fill="#f4f4f2"/>'
             + stripes
             + f'<rect x="{lx-lw*0.6}" y="{top-lw*0.5}" width="{lw*1.2}" height="{lw*0.5}" fill="{darken(accent,0.2)}"/>'  # gallery
             + f'<rect x="{lx-lw*0.4}" y="{top-lw*1.3}" width="{lw*0.8}" height="{lw*0.8}" fill="{accent}"/>'            # lantern room
             + f'<circle cx="{lx}" cy="{top-lw*0.9}" r="{lw*0.22}" fill="#fff7d6"/>'                                     # light
             + f'<polygon points="{lx-lw*0.5},{top-lw*1.3} {lx+lw*0.5},{top-lw*1.3} {lx},{top-lw*2.0}" fill="{darken(ink,0.1)}"/>')  # roof
    # sea
    wave = (f'<path d="M0,{y_sea} Q{W*0.25},{y_sea-18} {W*0.5},{y_sea} T{W},{y_sea} V{H} H0 Z" fill="{sea}"/>'
            f'<path d="M0,{y_sea+30} Q{W*0.25},{y_sea+12} {W*0.5},{y_sea+30} T{W},{y_sea+30} V{H} H0 Z" fill="{darken(ink,0.2)}" opacity="0.6"/>')
    return beams + sky + tower + wave


def motif_ember(W, H, theme):
    accent = theme["accent"]
    flames = ""
    for i, (dx, sc, col) in enumerate([(0.0, 1.0, darken(accent, 0.15)), (0.06, 0.7, accent),
                                        (-0.05, 0.55, lighten(accent, 0.25)), (0.0, 0.32, "#ffe9b0")]):
        cx = W * (0.5 + dx); base = H * 0.82; h = H * 0.42 * sc; w = W * 0.14 * sc
        flames += (f'<path d="M{cx},{base-h} C{cx-w},{base-h*0.4} {cx-w*0.6},{base} {cx},{base} '
                   f'C{cx+w*0.6},{base} {cx+w},{base-h*0.4} {cx},{base-h} Z" fill="{col}"/>')
    embers = "".join(emblem_svg("circle", W*x, H*y, W*0.006, lighten(accent, 0.3))
                     for x, y in [(0.35, 0.35), (0.6, 0.28), (0.5, 0.2), (0.42, 0.5), (0.62, 0.5)])
    return flames + embers


def motif_generic(W, H, theme):
    accent = theme["accent"]
    suit = theme["suits"].get("_default", {"color": accent, "emblem": "circle"})
    rings = "".join(f'<circle cx="{W*0.5}" cy="{H*0.42}" r="{W*(0.12+0.09*i)}" fill="none" '
                    f'stroke="{accent}" stroke-width="3" opacity="0.25"/>' for i in range(4))
    scatter = "".join(emblem_svg(suit["emblem"], W*x, H*y, W*0.02, blend(suit["color"], accent, 0.3))
                      for x, y in [(0.2, 0.25), (0.8, 0.22), (0.28, 0.6), (0.74, 0.62), (0.5, 0.42)])
    return rings + scatter


MOTIFS = {"nautical": motif_nautical, "ember": motif_ember}


def build_cover_svg(title, subtitle, theme_name, players, time, weight, W, H):
    theme = get_theme(theme_name)
    ink, accent = theme["ink"], theme["accent"]
    top_bg, bot_bg = theme["page"]
    motif = MOTIFS.get(theme_name.lower(), motif_generic)(W, H, theme)

    # badges
    pills, items = "", [(f"{players}p" if players else None), time or None,
                        (f"weight {weight}" if weight else None)]
    items = [i for i in items if i]
    if items:
        pw, ph, gap = W * 0.26, H * 0.055, W * 0.02
        total = len(items) * pw + (len(items) - 1) * gap
        x = (W - total) / 2
        for label in items:
            pills += (f'<rect x="{x}" y="{H*0.90}" width="{pw}" height="{ph}" rx="{ph/2}" '
                      f'fill="{ink}" opacity="0.85"/>'
                      f'<text x="{x+pw/2}" y="{H*0.90+ph*0.68}" font-size="{H*0.026}" fill="#fff" '
                      f'text-anchor="middle" font-family="{theme["body_font"]}">{label}</text>')
            x += pw + gap

    banner_y = H * 0.30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{darken(top_bg,0.12)}"/><stop offset="1" stop-color="{bot_bg}"/>
    </linearGradient>
    <radialGradient id="vig" cx="0.5" cy="0.42" r="0.75">
      <stop offset="0.6" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.28"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {motif}
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <!-- title banner -->
  <rect x="0" y="{banner_y}" width="{W}" height="{H*0.14}" fill="{ink}" opacity="0.82"/>
  <rect x="0" y="{banner_y-4}" width="{W}" height="6" fill="{accent}"/>
  <rect x="0" y="{banner_y+H*0.14-2}" width="{W}" height="6" fill="{accent}"/>
  <text x="{W/2}" y="{banner_y+H*0.092}" font-size="{W*0.11}" fill="#ffffff" text-anchor="middle"
        font-family="{theme['title_font']}" font-weight="bold" letter-spacing="2">{_esc(title)}</text>
  <text x="{W/2}" y="{banner_y+H*0.135}" font-size="{W*0.032}" fill="{lighten(accent,0.2)}"
        text-anchor="middle" font-family="{theme['title_font']}" font-style="italic">{_esc(subtitle or '')}</text>
  {pills}
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="18" fill="none" stroke="{accent}" stroke-width="4" opacity="0.6"/>
</svg>"""


def _esc(s):
    import html
    return html.escape(str(s or ""), quote=True)


def main():
    ap = argparse.ArgumentParser(description="Generate a themed procedural cover image.")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--theme", default="clean")
    ap.add_argument("--players", default="")
    ap.add_argument("--time", default="")
    ap.add_argument("--weight", default="")
    ap.add_argument("--out", default=Path("build/cover.png"), type=Path)
    ap.add_argument("--size", default="1024x1280", help="WxH, e.g. 1024x1280")
    args = ap.parse_args()

    W, H = (int(x) for x in args.size.lower().split("x"))
    svg = build_cover_svg(args.title, args.subtitle, args.theme, args.players, args.time,
                          args.weight, W, H)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    svg_path = args.out.with_suffix(".svg")
    svg_path.write_text(svg, encoding="utf-8")
    print(f"[cover] wrote {svg_path}")
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_path), write_to=str(args.out), output_width=W, output_height=H)
        print(f"[cover] wrote {args.out}  ({W}x{H})")
    except Exception:
        print("[cover] cairosvg not installed — SVG only. pip install cairosvg (+ brew install cairo).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
