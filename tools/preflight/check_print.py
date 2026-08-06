#!/usr/bin/env python3
"""
check_print.py — a print-readiness pre-flight gate for a physical run.

Before committing files to a manufacturer, the expensive, permanent mistakes are deterministic: too little
bleed, art in the safe margin, RGB instead of CMYK, sub-300-DPI, a non-standard card size, unreadable body
text. This validates a game's declared print intent (`print-spec.json`) against manufacturing norms so
those are caught at the FILE stage, not the proof stage (or worse, the printed run). See
knowledge/manufacturing-and-fulfillment.md and knowledge/manufacturing-specs.md.

This is a SPEC validator (stdlib-only). If Pillow is installed and build/ holds rendered PNGs, it also
spot-checks their pixel resolution against the declared size × DPI.

Declare intent in `games/<slug>/print-spec.json` (copy this shape):
  {
    "bleed_mm": 3, "safe_margin_mm": 3, "dpi": 300, "color_mode": "CMYK",
    "card_size": "63x88", "min_body_font_pt": 7, "check_pngs": true
  }

Usage:
    python tools/preflight/check_print.py --game games/beacon

Exit code is non-zero on any ERROR. Owned by bg-production (mostly deferred; skip if the game is licensed
or Screentop-only). Norms: bleed ≥3 mm, safe margin ≥3 mm, DPI ≥300, CMYK, standard card size, body text
≥ ~7 pt (~2.5 mm).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

STANDARD_CARD_SIZES = {"63x88", "63.5x88.9", "44x67", "56x87", "70x70", "57x89"}  # mm, common POD/offset
MIN_BLEED = 3.0
MIN_SAFE = 3.0
MIN_DPI = 300
MIN_FONT_PT = 7.0  # ~2.5 mm cap height — legible at arm's length


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0
    def error(self, msg): self.errors += 1; print(f"  \033[31m[ERROR]\033[0m {msg}")
    def warn(self, msg): self.warns += 1; print(f"  \033[33m[WARN ]\033[0m {msg}")
    def info(self, msg): print(f"  [info ] {msg}")
    def ok(self, msg): print(f"  \033[32m[ ok  ]\033[0m {msg}")


def validate_spec(spec: dict, rep: Report):
    print("\n• print spec vs manufacturing norms")
    b = float(spec.get("bleed_mm", 0))
    (rep.ok if b >= MIN_BLEED else rep.error)(f"bleed: {b} mm (norm ≥ {MIN_BLEED})")
    s = float(spec.get("safe_margin_mm", 0))
    (rep.ok if s >= MIN_SAFE else rep.error)(f"safe margin: {s} mm (norm ≥ {MIN_SAFE})")
    d = int(spec.get("dpi", 0))
    (rep.ok if d >= MIN_DPI else rep.error)(f"resolution: {d} DPI (norm ≥ {MIN_DPI})")
    cm = str(spec.get("color_mode", "")).upper()
    (rep.ok if cm == "CMYK" else rep.error)(f"colour mode: {cm or '(unset)'} (must be CMYK for print, not RGB)")
    cs = str(spec.get("card_size", "")).replace(" ", "").lower().replace("mm", "")
    if not cs:
        rep.warn("card_size unset")
    elif cs in {x.lower() for x in STANDARD_CARD_SIZES}:
        rep.ok(f"card size: {cs} mm (standard — lowest tooling cost)")
    else:
        rep.warn(f"card size: {cs} mm (non-standard → custom die cost; confirm with printer)")
    f = float(spec.get("min_body_font_pt", 0))
    if f:
        (rep.ok if f >= MIN_FONT_PT else rep.error)(f"min body font: {f} pt (norm ≥ {MIN_FONT_PT} ≈ 2.5 mm)")
    else:
        rep.warn("min_body_font_pt unset — verify body text is legible at arm's length (~2.5 mm)")


def check_pngs(game_dir: Path, spec: dict, rep: Report):
    if not spec.get("check_pngs"):
        return
    try:
        from PIL import Image  # noqa
    except ImportError:
        rep.info("check_pngs set but Pillow not installed — skipping pixel check (pip install Pillow)")
        return
    from PIL import Image
    cs = str(spec.get("card_size", "63x88")).replace("mm", "").lower()
    try:
        w_mm, h_mm = (float(x) for x in cs.split("x"))
    except ValueError:
        rep.warn(f"can't parse card_size '{cs}' for pixel check"); return
    dpi = int(spec.get("dpi", 300))
    exp_w = round(w_mm / 25.4 * dpi)
    build = game_dir / "build"
    pngs = list(build.rglob("*.png")) if build.is_dir() else []
    if not pngs:
        rep.info("check_pngs set but no PNGs in build/ — render first, then re-run"); return
    print(f"\n• PNG resolution spot-check (expect ~{exp_w}px wide for a card at {dpi} DPI)")
    for p in pngs[:8]:
        with Image.open(p) as im:
            w = im.width
        # only meaningful for single-card renders; sheets are wider — just report
        rep.info(f"{p.name}: {w}px wide")


def main():
    ap = argparse.ArgumentParser(description="Pre-flight a game's print spec against manufacturing norms.")
    ap.add_argument("--game", required=True, type=Path)
    args = ap.parse_args()

    rep = Report()
    print(f"Print pre-flight — {args.game}")
    spec_path = args.game / "print-spec.json"
    if not spec_path.is_file():
        print(f"\n  no print-spec.json found — declare print intent before a physical run:")
        print('  {"bleed_mm":3,"safe_margin_mm":3,"dpi":300,"color_mode":"CMYK",'
              '"card_size":"63x88","min_body_font_pt":7,"check_pngs":false}')
        print("\n  (Screentop-only / licensed games don't need this — see bg-production.)")
        return 0
    spec = json.loads(spec_path.read_text())
    validate_spec(spec, rep)
    check_pngs(args.game, spec, rep)

    print(f"\n{'=' * 48}\nResult: {rep.errors} error(s), {rep.warns} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
