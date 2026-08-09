#!/usr/bin/env python3
"""
build_pnp.py — tile a game's ALREADY-RENDERED component PNGs onto A4 / A3 pages at
TRUE physical size, with cut guides, for a home library print-and-play (print-and-cut).

Additive + standalone: this tool CONSUMES existing renders (individual card PNGs,
board/map/token/aid PNGs). It does NOT render components itself and does NOT import any
Beacon-shared render code (build_cards / build_board / themes). It only reads its palette
by name from a tiny local copy of the needed colours (below) so nothing shared can regress.

Engine: WeasyPrint — the same HTML/CSS -> PDF engine as tools/rulebook/build_rulebook.py.
Pages use `@page { size: A4 }` with **mm** units and images placed at exact mm, so a printer
set to 100% / Actual Size yields real-size cards (a 63.5x88.9 mm poker card measures exactly
that on paper). The cover page carries a 50 mm + 2-inch scale-check ruler to confirm the
printer did not shrink-to-fit.

Source renders are authored at 300 DPI, so an image's true size is px / 300 * 25.4 mm:
  card 750x1050 -> 63.5 x 88.9 mm (poker)   board 1680x1380 -> 142.2 x 116.8 mm
  map 2280x1680 -> 193.0 x 142.2 mm

Modes
  cards   tile card FRONT PNGs at 63.5x88.9 mm with a shared-line cut grid
          (9 per A4 = 3x3, 16 per A3 = 4x4). Produce one A4 set and one A3 set.
  images  place larger image assets (boards / map / tokens / aid) at native 300-DPI mm,
          N per page, each with a thin cut border + corner crop ticks.

Usage examples (see games/travel-agents/make.sh for the wired-up calls):
  python tools/print/build_pnp.py --mode cards  --page A4 --title "..." --blurb "..." \
      --out games/travel-agents/exports/print/pnp-cards-A4.pdf  build/pnp/cards/*/png
  python tools/print/build_pnp.py --mode images --page A4 --per-page 2 --title "..." \
      --out games/travel-agents/exports/print/pnp-boards.pdf   exports/board-*.png
"""
from __future__ import annotations
import argparse
import glob
import html as _html
from pathlib import Path

from PIL import Image

# ---- physical constants -----------------------------------------------------------------
DPI = 300.0
MM_PER_IN = 25.4
CARD_W_MM = 63.5   # poker 750px @300dpi
CARD_H_MM = 88.9   # poker 1050px @300dpi

PAGES_MM = {  # (width, height) portrait
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
}

# Cards-per-page grid per page size (task spec: 9 per A4, 16 per A3).
CARD_GRID = {"A4": (3, 3), "A3": (4, 4)}  # (cols, rows)

# ---- local palette (NOT imported from the shared themes.py — additive isolation) --------
# A tiny name->palette copy so this tool never touches Beacon-shared render code. Values
# mirror themes.py `night-market` for a consistent TA look; `clean` is a neutral fallback.
PALETTES = {
    "night-market": {
        "page": "#F7F1E3", "panel": "#EFE6D0", "ink": "#26324D",
        "text": "#2B2B2B", "muted": "#7A6E58", "accent": "#D64545",
        "font": "'WenQuanYi Zen Hei', 'Noto Sans TC', 'PingFang TC', sans-serif",
    },
    "clean": {
        "page": "#FFFFFF", "panel": "#F0F0F0", "ink": "#222222",
        "text": "#222222", "muted": "#777777", "accent": "#2266AA",
        "font": "'DejaVu Sans', Arial, sans-serif",
    },
}


def palette(name: str) -> dict:
    return PALETTES.get(name, PALETTES["clean"])


def page_dims(page: str, landscape: bool) -> tuple[float, float]:
    w, h = PAGES_MM[page]
    return (h, w) if landscape else (w, h)


def img_mm(path: str) -> tuple[float, float]:
    """True physical size of an image in mm, assuming it was authored at 300 DPI."""
    with Image.open(path) as im:
        w, h = im.size
    return (w / DPI * MM_PER_IN, h / DPI * MM_PER_IN)


def expand_inputs(patterns: list[str]) -> list[str]:
    out: list[str] = []
    for p in patterns:
        if any(ch in p for ch in "*?["):
            out.extend(sorted(glob.glob(p)))
        elif Path(p).is_dir():
            out.extend(sorted(str(x) for x in Path(p).glob("*.png")))
        else:
            out.append(p)
    # de-dup, preserve order
    seen: set[str] = set()
    uniq = []
    for f in out:
        if f not in seen and Path(f).exists():
            seen.add(f)
            uniq.append(f)
    return uniq


# ---- page CSS ---------------------------------------------------------------------------

def base_css(page: str, landscape: bool, pal: dict) -> str:
    size = f"{page} landscape" if landscape else page
    return f"""
    @page {{ size: {size}; margin: 0; }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{ font-family: {pal['font']}; color: {pal['text']}; background: #fff; }}
    .page {{ position: relative; width: {page_dims(page, landscape)[0]}mm;
             height: {page_dims(page, landscape)[1]}mm; overflow: hidden;
             page-break-after: always; }}
    .page:last-child {{ page-break-after: auto; }}
    .card-img, .asset-img {{ position: absolute; display: block; }}
    svg.overlay {{ position: absolute; left: 0; top: 0; }}
    """


# ---- SVG cut-guide helpers --------------------------------------------------------------

def _line(x1, y1, x2, y2, w=0.2, color="#555"):
    return (f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" '
            f'stroke="{color}" stroke-width="{w}"/>')


def card_grid_svg(pw, ph, mx, my, cols, cw, ch, n, accent: str) -> str:
    """A shared-line cut grid bounding exactly the n placed cards, + corner crop ticks."""
    full_rows = n // cols
    rem = n % cols
    total_rows = full_rows + (1 if rem else 0)
    parts = [f'<svg class="overlay" width="{pw}mm" height="{ph}mm" viewBox="0 0 {pw} {ph}">']

    # horizontal cut lines (row boundaries) — full width for full rows, partial for last
    for r in range(full_rows + 1):
        parts.append(_line(mx, my + r * ch, mx + cols * cw, my + r * ch))
    if rem:
        y = my + (full_rows + 1) * ch
        parts.append(_line(mx, y, mx + rem * cw, y))

    # vertical cut lines (column boundaries) — extend one more row where the last row is filled
    for c in range(cols + 1):
        y_end = my + full_rows * ch
        if rem and c <= rem:
            y_end = my + (full_rows + 1) * ch
        parts.append(_line(mx + c * cw, my, mx + c * cw, y_end))

    # corner crop ticks (extend outward into the margin) at the block's outer corners
    tick = 5.0
    right = mx + cols * cw
    bottom = my + total_rows * ch
    for (cx, cy, dx, dy) in [
        (mx, my, -1, -1), (right, my, 1, -1),
        (mx, bottom, -1, 1), (right, bottom, 1, 1),
    ]:
        parts.append(_line(cx, cy, cx + dx * tick, cy, w=0.35, color=accent))
        parts.append(_line(cx, cy, cx, cy + dy * tick, w=0.35, color=accent))
    parts.append("</svg>")
    return "".join(parts)


def asset_cut_svg(pw, ph, boxes, accent: str) -> str:
    """A thin cut rectangle + outward corner ticks around each placed asset image."""
    parts = [f'<svg class="overlay" width="{pw}mm" height="{ph}mm" viewBox="0 0 {pw} {ph}">']
    tick = 5.0
    for (x, y, w, h) in boxes:
        parts.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" '
                     f'fill="none" stroke="#555" stroke-width="0.2"/>')
        for (cx, cy, dx, dy) in [
            (x, y, -1, -1), (x + w, y, 1, -1), (x, y + h, -1, 1), (x + w, y + h, 1, 1),
        ]:
            parts.append(_line(cx, cy, cx + dx * tick, cy, w=0.35, color=accent))
            parts.append(_line(cx, cy, cx, cy + dy * tick, w=0.35, color=accent))
    parts.append("</svg>")
    return "".join(parts)


# ---- cover page -------------------------------------------------------------------------

def cover_page(page, landscape, pal, title, blurb, content_pages, per_page_desc) -> str:
    pw, ph = page_dims(page, landscape)
    # scale-check rulers: exact mm widths so 100%-scale print measures true.
    bar50 = 50.0
    bar2in = 2 * MM_PER_IN  # 50.8 mm
    def ruler(width_mm, label):
        # a bar with end caps + midpoint ticks, drawn in mm so it prints true-size
        ticks = "".join(
            _line(t, 6, t, 12, w=0.3, color=pal["ink"])
            for t in [i for i in range(0, int(width_mm) + 1, 10)]
        )
        return (
            f'<svg width="{width_mm + 4}mm" height="18mm" '
            f'viewBox="0 0 {width_mm + 4} 18" style="display:block;margin:2mm 0;">'
            f'<rect x="2" y="6" width="{width_mm}" height="6" fill="none" '
            f'stroke="{pal["accent"]}" stroke-width="0.5"/>'
            f'<line x1="2" y1="6" x2="2" y2="12" stroke="{pal["ink"]}" stroke-width="0.5"/>'
            f'<line x1="{width_mm + 2}" y1="6" x2="{width_mm + 2}" y2="12" '
            f'stroke="{pal["ink"]}" stroke-width="0.5"/>'
            f'<g transform="translate(2,0)">{ticks}</g>'
            f'<text x="{width_mm/2 + 2}" y="17" text-anchor="middle" '
            f'font-size="3.2" fill="{pal["muted"]}" '
            f'font-family="{pal["font"]}">{label}</text></svg>'
        )
    pages_line = (f"{content_pages} print sheet"
                  f"{'s' if content_pages != 1 else ''} follow this cover "
                  f"({content_pages + 1} pages total).")
    inner_w = pw - 24
    body = f"""
    <div class="page" style="padding:12mm; width:{pw}mm; height:{ph}mm;">
      <div style="width:{inner_w}mm;">
        <div style="background:{pal['ink']}; color:#fff; padding:6mm 7mm; border-radius:3mm;
                    border-bottom:2mm solid {pal['accent']};">
          <div style="font-size:20pt; font-weight:bold;">{_html.escape(title)}</div>
          <div style="font-size:10pt; opacity:.85; margin-top:2mm;">Home print-and-play — {page}{' landscape' if landscape else ''}</div>
        </div>

        <div style="margin-top:6mm; padding:5mm 6mm; border:0.6mm solid {pal['accent']};
                    border-radius:2mm; background:{pal['panel']};">
          <div style="font-size:14pt; font-weight:bold; color:{pal['accent']};">
            Print at 100% / Actual Size — do NOT "Fit to page" / "Shrink to fit".</div>
          <div style="font-size:9.5pt; color:{pal['text']}; margin-top:2mm;">
            In the print dialog set <b>Scale = 100%</b> (or "Actual size"). Then measure the two
            bars below with a ruler <b>before</b> cutting — the 50&nbsp;mm bar must read exactly
            50&nbsp;mm and the 2-inch bar exactly 2&nbsp;inches. If they are short, your printer
            shrank the page — turn scaling off and reprint.</div>
          <div style="margin-top:3mm;">
            {ruler(bar50, "50 mm — must measure exactly 50 mm")}
            {ruler(bar2in, "2 inches (50.8 mm) — must measure exactly 2 inches")}
          </div>
        </div>

        <div style="margin-top:6mm; font-size:9.5pt; color:{pal['text']};">
          <div style="font-size:12pt; font-weight:bold; color:{pal['ink']};">In this file</div>
          <div style="margin-top:1.5mm;">{_html.escape(blurb)}</div>
          <div style="margin-top:1.5mm; color:{pal['muted']};">{_html.escape(per_page_desc)} {pages_line}</div>
        </div>

        <div style="margin-top:5mm; font-size:9.5pt; color:{pal['text']};">
          <div style="font-size:12pt; font-weight:bold; color:{pal['ink']};">Cut &amp; mount</div>
          <ul style="margin:1.5mm 0 0 5mm; padding:0; line-height:1.5;">
            <li>Print onto (or glue onto) <b>~200–300&nbsp;gsm cardstock</b>; a glue stick or spray
                mount onto cereal-box card works for a first prototype.</li>
            <li>Cut along the shared grid lines — abutting cards share one cut, so a guillotine or
                a steel ruler + craft knife goes fastest. The <b>coloured corner
                ticks</b> mark the outer trim of each sheet.</li>
            <li>Round the corners if you like, and sleeve them (63.5×88.9&nbsp;mm = standard poker /
                "premium" sleeves) so they shuffle.</li>
          </ul>
        </div>

        <div style="margin-top:5mm; font-size:9pt; color:{pal['muted']};
                    border-top:0.3mm solid {pal['muted']}; padding-top:2mm;">
          <b style="color:{pal['ink']};">Colour is preferred, but this is fully B&amp;W-playable.</b>
          Every region and ingredient is <b>dual-coded</b> with a distinct shape / emblem (and a
          text + 繁體 label), not colour alone — so greyscale prints stay unambiguous.
          <br>Note: the character boards currently show the art <i>placeholder</i>; final mock-up
          art drops in later and re-tiles automatically.
        </div>
      </div>
    </div>"""
    return body


# ---- content builders -------------------------------------------------------------------

def build_card_pages(page, pal, cards: list[str]) -> tuple[str, int, int]:
    pw, ph = page_dims(page, False)
    cols, rows = CARD_GRID[page]
    per = cols * rows
    cw, ch = CARD_W_MM, CARD_H_MM
    block_w, block_h = cols * cw, rows * ch
    mx = (pw - block_w) / 2
    my = (ph - block_h) / 2
    pages_html = []
    for start in range(0, len(cards), per):
        chunk = cards[start:start + per]
        imgs = []
        for i, c in enumerate(chunk):
            r, col = divmod(i, cols)
            left = mx + col * cw
            top = my + r * ch
            uri = Path(c).resolve().as_uri()
            imgs.append(f'<img class="card-img" src="{uri}" '
                        f'style="left:{left:.3f}mm; top:{top:.3f}mm; '
                        f'width:{cw}mm; height:{ch}mm;"/>')
        overlay = card_grid_svg(pw, ph, mx, my, cols, cw, ch, len(chunk), pal["accent"])
        pages_html.append(f'<div class="page">{"".join(imgs)}{overlay}</div>')
    return "".join(pages_html), len(pages_html), per


def build_image_pages(page, landscape, pal, images: list[str], per_page: int) -> tuple[str, int]:
    pw, ph = page_dims(page, landscape)
    pages_html = []
    for start in range(0, len(images), per_page):
        chunk = images[start:start + per_page]
        sizes = [img_mm(p) for p in chunk]
        gap = 8.0
        total_h = sum(h for _, h in sizes) + gap * (len(chunk) - 1)
        y = (ph - total_h) / 2
        imgs, boxes = [], []
        for p, (w, h) in zip(chunk, sizes):
            x = (pw - w) / 2
            uri = Path(p).resolve().as_uri()
            imgs.append(f'<img class="asset-img" src="{uri}" '
                        f'style="left:{x:.3f}mm; top:{y:.3f}mm; width:{w:.3f}mm; height:{h:.3f}mm;"/>')
            boxes.append((x, y, w, h))
            y += h + gap
        overlay = asset_cut_svg(pw, ph, boxes, pal["accent"])
        pages_html.append(f'<div class="page">{"".join(imgs)}{overlay}</div>')
    return "".join(pages_html), len(pages_html)


# ---- main -------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Tile rendered component PNGs into a true-size PnP PDF.")
    ap.add_argument("inputs", nargs="+", help="card PNGs / dirs / globs (cards mode) or image files")
    ap.add_argument("--mode", choices=["cards", "images"], required=True)
    ap.add_argument("--page", choices=["A4", "A3"], default="A4")
    ap.add_argument("--landscape", action="store_true")
    ap.add_argument("--per-page", type=int, default=1, help="images mode: assets per page")
    ap.add_argument("--theme", default="night-market")
    ap.add_argument("--title", default="Print-and-Play")
    ap.add_argument("--blurb", default="", help="what components are in this file")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    pal = palette(args.theme)
    files = expand_inputs(args.inputs)
    if not files:
        raise SystemExit(f"[pnp] no input files matched: {args.inputs}")

    if args.mode == "cards":
        content, n_pages, per = build_card_pages(args.page, pal, files)
        per_desc = f"{len(files)} cards, {per} per sheet ({CARD_GRID[args.page][0]}×{CARD_GRID[args.page][1]}) at true 63.5×88.9 mm."
        cover = cover_page(args.page, False, pal, args.title, args.blurb, n_pages, per_desc)
        css = base_css(args.page, False, pal)
    else:
        content, n_pages = build_image_pages(args.page, args.landscape, pal, files, args.per_page)
        per_desc = f"{len(files)} asset(s), {args.per_page} per sheet at true (300-DPI) size."
        cover = cover_page(args.page, args.landscape, pal, args.title, args.blurb, n_pages, per_desc)
        css = base_css(args.page, args.landscape, pal)

    doc = (f"<!doctype html><html><head><meta charset='utf-8'>"
           f"<title>{_html.escape(args.title)}</title><style>{css}</style></head>"
           f"<body>{cover}{content}</body></html>")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    from weasyprint import HTML
    HTML(string=doc, base_url=str(args.out.parent)).write_pdf(str(args.out))
    print(f"[pnp] wrote {args.out}  ({n_pages + 1} pages: 1 cover + {n_pages} sheet(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
