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
import sys
from pathlib import Path

from themes import get_theme, resolve_suit, emblem_svg, page_gradient

# ---- Card geometry (poker, trimmed, 300 DPI) --------------------------------
CARD_W, CARD_H = 750, 1050          # px @ 300 DPI
MARGIN = 54                         # ~4.5 mm safe margin
TITLE_SIZE, TYPE_SIZE, BODY_SIZE = 50, 28, 34
LINE_H = 44


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


def render_card_svg(row: dict, theme: dict) -> str:
    ctype = (row.get("type") or "").strip()
    suit = resolve_suit(theme, ctype)
    scol = suit["color"]
    ink, text, muted, accent, radius = theme["ink"], theme["text"], theme["muted"], theme["accent"], theme["radius"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    name = esc(row.get("name", ""))
    cost = str(row.get("cost", "")).strip()
    value = str(row.get("value", "")).strip()

    body_lines = wrap(row.get("effect", ""), max_chars=32)
    body_tspans = "".join(
        f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(body_lines)
    )

    header_h = 104
    # cost badge (top-right, on the header band)
    cost_badge = ""
    if cost:
        cx, cy, r = CARD_W - MARGIN - 6, MARGIN + 24, 46
        cost_badge = (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{scol}" stroke-width="6"/>'
            f'<text x="{cx}" y="{cy + 16}" font-size="48" fill="{scol}" text-anchor="middle" '
            f'font-family="{tfont}" font-weight="bold">{esc(cost)}</text>'
        )
    # value as a row of suit emblems + numeral (bottom-left)
    value_row = ""
    try:
        vn = int(float(value)) if value else 0
    except ValueError:
        vn = 0
    if vn > 0:
        pips = "".join(emblem_svg(suit["emblem"], MARGIN + 22 + i * 46, CARD_H - MARGIN - 22, 16, scol)
                        for i in range(min(vn, 6)))
        value_row = (pips +
            f'<text x="{CARD_W - MARGIN}" y="{CARD_H - MARGIN - 6}" font-size="46" fill="{scol}" '
            f'text-anchor="end" font-family="{tfont}" font-weight="bold">{vn}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <defs>{page_gradient(theme, 'pg')}</defs>
  <rect x="4" y="4" width="{CARD_W-8}" height="{CARD_H-8}" rx="{radius}" fill="url(#pg)" stroke="{ink}" stroke-width="6"/>
  <rect x="26" y="26" width="{CARD_W-52}" height="{CARD_H-52}" rx="{radius-10}" fill="none" stroke="{scol}" stroke-width="2" opacity="0.5"/>
  <!-- header band in the suit colour -->
  <path d="M26 {26+radius-10} a {radius-10} {radius-10} 0 0 1 {radius-10} -{radius-10} h {CARD_W-52-2*(radius-10)} a {radius-10} {radius-10} 0 0 1 {radius-10} {radius-10} v {header_h-(radius-10)} h -{CARD_W-52} z" fill="{scol}"/>
  <text x="{MARGIN}" y="{MARGIN+44}" font-size="{TITLE_SIZE}" fill="#ffffff" font-family="{tfont}" font-weight="bold">{name}</text>
  {cost_badge}
  <!-- type line with emblem -->
  {emblem_svg(suit['emblem'], MARGIN+16, MARGIN+96, 15, scol)}
  <text x="{MARGIN+44}" y="{MARGIN+106}" font-size="{TYPE_SIZE}" fill="{muted}" font-family="{tfont}" font-style="italic" letter-spacing="2">{esc(ctype).upper()}</text>
  <!-- body -->
  <text x="{MARGIN}" y="{MARGIN+210}" font-size="{BODY_SIZE}" fill="{text}" font-family="{bfont}">{body_tspans}</text>
  <!-- footer flourish -->
  <line x1="{MARGIN}" y1="{CARD_H-MARGIN-70}" x2="{CARD_W-MARGIN}" y2="{CARD_H-MARGIN-70}" stroke="{accent}" stroke-width="2" opacity="0.5"/>
  {value_row}
</svg>"""


def render_back_svg(slug: str, theme: dict) -> str:
    ink, accent, radius = theme["ink"], theme["accent"], theme["radius"]
    scol = theme["suits"].get("_default", {}).get("color", accent)
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
    args = ap.parse_args()

    theme = get_theme(args.theme)
    slug = args.slug or args.csv.stem
    rows = load_rows(args.csv)
    if not rows:
        print(f"No rows in {args.csv}", file=sys.stderr)
        return 1

    (args.out / "svg").mkdir(parents=True, exist_ok=True)

    # 1) Always render per-card SVGs (no dependencies).
    svg_paths = []
    for row in rows:
        cid = (row.get("id") or row.get("name") or f"card{len(svg_paths)}").strip()
        p = args.out / "svg" / f"{cid}.svg"
        p.write_text(render_card_svg(row, theme), encoding="utf-8")
        svg_paths.append((cid, p, int(row.get("quantity") or 1)))
    back_svg = render_back_svg(slug, theme)
    (args.out / "svg" / "_back.svg").write_text(back_svg, encoding="utf-8")
    print(f"[svg]  wrote {len(svg_paths)} card SVGs -> {args.out/'svg'}")

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
            cols = min(COLS, n)
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
