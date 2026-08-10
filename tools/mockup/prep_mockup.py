#!/usr/bin/env python3
"""prep_mockup.py — turn an AI-generated mock-up PNG into drop-in component art.

AI image tools (ChatGPT/DALL·E, Midjourney, …) hand back RASTER PNGs — often a
grid of several characters on a white or vignetted background — never per-item
SVGs. This little stdlib+Pillow utility does the three mechanical chores that
stand between that export and a component art slot, so a mock-up can be dropped
into the SVG renders for a playtest:

  1. SPLIT a grid image into its individual cells            (--grid, --rows, --cols, --names)
  2. KEY a flat background to transparent                    (--key-bg, corner-seeded flood fill)
  3. FIT each cutout to a component slot's exact px/aspect    (--fit WxH, trim + scale + pad)

It is a MOCK-UP helper only — the output is a labelled playtest prop, written to
the game's gitignored `build/mockups/` by default. It is NOT final art (final art
is human-illustrated; see art/art-style.md).

Background-keying is a CORNER-SEEDED FLOOD FILL, not a global threshold, so it
lifts a contiguous flat backdrop without punching holes in a white shirt, a bowl,
or a bao — the interior whites are not connected to the border, so they survive.
A heavy radial vignette/glow is NOT flat, so it keys poorly: regenerate those with
a flat/transparent background instead (the recipe in art/art-style.md says so).

Examples
--------
  # Split a 2x2 grid of four characters, key the white bg, fit each to the board slot:
  python tools/mockup/prep_mockup.py --grid ~/Downloads/cast.png --rows 2 --cols 2 \
      --names homebody,big-eater,influencer,big-brother \
      --key-bg --fit 604x286 --pad --game games/travel-agents --prefix FIG-CHAR-

  # Clean a single already-cropped portrait:
  python tools/mockup/prep_mockup.py --image ~/Downloads/granny.png \
      --key-bg --fit 604x286 --pad --game games/travel-agents --out FIG-CHAR-globetrotter.png
"""
from __future__ import annotations
import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is required: pip install pillow")


def _load_rgba(path: str) -> "Image.Image":
    return Image.open(os.path.expanduser(path)).convert("RGBA")


def split_grid(img: "Image.Image", rows: int, cols: int) -> list["Image.Image"]:
    """Cut an image into rows*cols equal cells, left-to-right, top-to-bottom."""
    w, h = img.size
    cw, ch = w // cols, h // rows
    cells = []
    for r in range(rows):
        for c in range(cols):
            box = (c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)
            cells.append(img.crop(box))
    return cells


def key_background(img: "Image.Image", thresh: int = 32) -> "Image.Image":
    """Make a flat, border-connected background transparent via corner-seeded flood fill.

    Seeds a flood fill from each of the four corners and the edge midpoints, keying
    every pixel within `thresh` colour-distance of the seed to fully transparent.
    Interior regions of the same colour (a white shirt, a bowl) are untouched because
    they are not connected to the image border. Runs on both a flat white and a flat
    dark backdrop; a gradient/vignette will only partially lift (regenerate those flat).
    """
    img = img.convert("RGBA")
    w, h = img.size
    # A scratch RGB copy for floodfill (Pillow floods on RGB), with an alpha sentinel.
    SENT = (255, 0, 255)  # magenta sentinel — flood target colour
    rgb = img.convert("RGB")
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for s in seeds:
        try:
            ImageDraw.floodfill(rgb, s, SENT, thresh=thresh)
        except Exception:
            pass
    # Any pixel the flood turned to the sentinel → transparent; keep original colour elsewhere.
    flooded = rgb.load()
    src = img.load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            if flooded[x, y] == SENT:
                dst[x, y] = (0, 0, 0, 0)
            else:
                dst[x, y] = src[x, y]
    return out


def _alpha_bbox(img: "Image.Image"):
    """Bounding box of non-transparent content (None if fully transparent)."""
    if img.mode != "RGBA":
        return img.getbbox()
    return img.split()[-1].getbbox()


def fit_slot(img: "Image.Image", w: int, h: int, pad: bool = True) -> "Image.Image":
    """Trim to content, scale to fit inside w×h preserving aspect, centre on a w×h canvas.

    With pad=True the result is EXACTLY w×h (transparent letterbox) — a true drop-in for
    the slot. With pad=False it is scaled-to-fit with no padding (may be smaller on one axis).
    """
    bbox = _alpha_bbox(img)
    if bbox:
        img = img.crop(bbox)
    iw, ih = img.size
    scale = min(w / iw, h / ih)
    new = img.resize((max(1, round(iw * scale)), max(1, round(ih * scale))), Image.LANCZOS)
    if not pad:
        return new
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.alpha_composite(new, ((w - new.size[0]) // 2, (h - new.size[1]) // 2))
    return canvas


def main() -> int:
    ap = argparse.ArgumentParser(description="Prep an AI mock-up PNG for a component art slot.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--grid", help="a grid image to split")
    src.add_argument("--image", help="a single already-cropped image")
    ap.add_argument("--rows", type=int, default=1)
    ap.add_argument("--cols", type=int, default=1)
    ap.add_argument("--names", help="comma-separated names for grid cells (row-major)")
    ap.add_argument("--key-bg", action="store_true", help="flood-key a flat background to transparent")
    ap.add_argument("--thresh", type=int, default=32, help="flood colour tolerance (default 32)")
    ap.add_argument("--fit", help="target slot WxH, e.g. 604x286 (char), 642x560 (ingredient), 750x1050 (card)")
    ap.add_argument("--pad", action="store_true", help="pad to EXACTLY the --fit size (transparent letterbox)")
    ap.add_argument("--game", help="game dir; output goes to <game>/build/mockups/ (gitignored)")
    ap.add_argument("--outdir", help="explicit output dir (overrides --game)")
    ap.add_argument("--prefix", default="", help="filename prefix for grid cells, e.g. FIG-CHAR-")
    ap.add_argument("--out", help="explicit output filename for --image mode")
    args = ap.parse_args()

    outdir = args.outdir or (os.path.join(args.game, "build", "mockups") if args.game else "mockups")
    os.makedirs(outdir, exist_ok=True)

    slot = None
    if args.fit:
        try:
            sw, sh = (int(v) for v in args.fit.lower().split("x"))
            slot = (sw, sh)
        except ValueError:
            return ap.error("--fit must look like 604x286")

    def process_and_save(im, name):
        if args.key_bg:
            im = key_background(im, thresh=args.thresh)
        if slot:
            im = fit_slot(im, slot[0], slot[1], pad=args.pad)
        path = os.path.join(outdir, name)
        im.save(path)
        print(f"[prep] wrote {path}  ({im.size[0]}x{im.size[1]})")

    if args.image:
        im = _load_rgba(args.image)
        name = args.out or (os.path.splitext(os.path.basename(args.image))[0] + ".png")
        process_and_save(im, name)
    else:
        grid = _load_rgba(args.grid)
        cells = split_grid(grid, args.rows, args.cols)
        names = (args.names.split(",") if args.names else [f"cell{i+1}" for i in range(len(cells))])
        if len(names) != len(cells):
            return ap.error(f"--names has {len(names)} entries but the grid has {len(cells)} cells")
        for im, nm in zip(cells, names):
            process_and_save(im, f"{args.prefix}{nm.strip()}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
