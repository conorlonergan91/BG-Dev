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

# ---- Card geometry (poker, trimmed, 300 DPI) --------------------------------
CARD_W, CARD_H = 750, 1050          # px @ 300 DPI
MARGIN = 54                         # ~4.5 mm safe margin
TITLE_SIZE, TYPE_SIZE, BODY_SIZE = 52, 30, 36
LINE_H = 46

# A calm default palette per card "type" (edit freely).
TYPE_COLORS = {
    "Building":  ("#2f4b3f", "#eaf3ee"),
    "Transport": ("#33475b", "#e9f0f6"),
    "Action":    ("#5b3a2e", "#f6efe9"),
    "Event":     ("#4a3a5b", "#f0ecf6"),
    "_default":  ("#333333", "#f4f4f2"),
}


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


def render_card_svg(row: dict) -> str:
    ctype = (row.get("type") or "").strip()
    ink, paper = TYPE_COLORS.get(ctype, TYPE_COLORS["_default"])
    name = esc(row.get("name", ""))
    cost = esc(row.get("cost", ""))
    value = esc(row.get("value", ""))
    body_lines = wrap(row.get("effect", ""), max_chars=30)
    body_tspans = "".join(
        f'<tspan x="{MARGIN}" dy="{0 if i == 0 else LINE_H}">{esc(l)}</tspan>'
        for i, l in enumerate(body_lines)
    )
    cost_badge = ""
    if str(cost).strip():
        cx, cy, r = CARD_W - MARGIN - 40, MARGIN + 40, 52
        cost_badge = (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ink}"/>'
            f'<text x="{cx}" y="{cy + 18}" font-size="52" fill="{paper}" '
            f'text-anchor="middle" font-family="Georgia, serif" font-weight="bold">{cost}</text>'
        )
    value_badge = ""
    if str(value).strip() and str(value).strip() != "0":
        value_badge = (
            f'<text x="{CARD_W - MARGIN}" y="{CARD_H - MARGIN}" font-size="44" fill="{ink}" '
            f'text-anchor="end" font-family="Georgia, serif" font-weight="bold">★ {value}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <rect x="0" y="0" width="{CARD_W}" height="{CARD_H}" rx="36" fill="{paper}" stroke="{ink}" stroke-width="8"/>
  <rect x="{MARGIN - 18}" y="{MARGIN - 18}" width="{CARD_W - 2*(MARGIN - 18)}" height="96" rx="16" fill="{ink}"/>
  <text x="{MARGIN}" y="{MARGIN + 46}" font-size="{TITLE_SIZE}" fill="{paper}" font-family="Georgia, serif" font-weight="bold">{name}</text>
  <text x="{MARGIN}" y="{MARGIN + 150}" font-size="{TYPE_SIZE}" fill="{ink}" font-family="Georgia, serif" font-style="italic" letter-spacing="2">{esc(ctype).upper()}</text>
  <text x="{MARGIN}" y="{MARGIN + 260}" font-size="{BODY_SIZE}" fill="#222" font-family="Georgia, serif">{body_tspans}</text>
  {cost_badge}
  {value_badge}
</svg>"""


def render_back_svg(slug: str) -> str:
    ink, paper = TYPE_COLORS["_default"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">
  <rect width="{CARD_W}" height="{CARD_H}" rx="36" fill="{ink}"/>
  <rect x="40" y="40" width="{CARD_W-80}" height="{CARD_H-80}" rx="24" fill="none" stroke="{paper}" stroke-width="6"/>
  <text x="{CARD_W/2}" y="{CARD_H/2}" font-size="60" fill="{paper}" text-anchor="middle" font-family="Georgia, serif" font-style="italic">{esc(slug)}</text>
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
    args = ap.parse_args()

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
        p.write_text(render_card_svg(row), encoding="utf-8")
        svg_paths.append((cid, p, int(row.get("quantity") or 1)))
    back_svg = render_back_svg(slug)
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
