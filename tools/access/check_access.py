#!/usr/bin/env python3
"""
check_access.py — an accessibility linter for a game's component data + render theme.

Accessibility is cheapest to fix at the data/theme stage, before art. This catches the two most common,
most *computable* failures deterministically (stdlib-only):

  1. Colour-blind suit collisions — simulates protanopia / deuteranopia / tritanopia (Machado et al.
     2009 matrices) on the theme's suit palette and measures perceptual distance (CIELAB ΔE76). A pair
     of suits that is distinct in normal vision but collapses under a colour-vision-deficiency (CVD) is
     flagged. Because the theme gives each suit an EMBLEM as well as a colour, a collision is only an
     ERROR when the colliding suits *also* share an emblem (i.e. colour is the only channel). If the
     emblems differ, the game is dual-coded and it's downgraded to INFO.
  2. Text contrast — WCAG contrast ratio of ink/text vs the page background; flags < 4.5:1.

Everything else in accessibility (font size at physical scale, text-independence, motor load,
communication channel, emotive load) is judgement — see knowledge/accessibility.md and the bg-access
agent. This tool covers the part a machine can settle.

Usage:
    python tools/access/check_access.py --game games/beacon --theme nautical

Exit code is non-zero if any ERRORs are found (WARN/INFO don't fail). Owned by bg-access.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import get_theme  # noqa: E402

# ΔE76 thresholds (perceptual distance in CIELAB).
DISTINCT = 20.0     # ≥ this in normal vision → the two suits are *meant* to read as different colours
CONFUSABLE = 15.0   # < this under a CVD → a player with that CVD likely can't tell them apart
CONTRAST_MIN = 4.5  # WCAG AA for normal-size body text

# Machado et al. (2009) CVD simulation matrices, severity 1.0, applied to LINEAR RGB.
CVD = {
    "protanopia": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
    "deuteranopia": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "tritanopia": (
        (1.255528, -0.076749, -0.178779),
        (-0.078411, 0.930809, 0.147602),
        (0.004733, 0.691367, 0.303900),
    ),
}


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0
    def error(self, msg): self.errors += 1; print(f"  \033[31m[ERROR]\033[0m {msg}")
    def warn(self, msg): self.warns += 1; print(f"  \033[33m[WARN ]\033[0m {msg}")
    def info(self, msg): print(f"  [info ] {msg}")
    def ok(self, msg): print(f"  \033[32m[ ok  ]\033[0m {msg}")


# --- colour maths (stdlib only) ------------------------------------------------
def hex_to_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def simulate_cvd(rgb: tuple[float, float, float], matrix) -> tuple[float, float, float]:
    lin = [srgb_to_linear(c) for c in rgb]
    out = [sum(matrix[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return tuple(linear_to_srgb(c) for c in out)  # type: ignore


def rgb_to_lab(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (srgb_to_linear(c) for c in rgb)
    # linear sRGB -> XYZ (D65)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    # normalise by D65 white
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883
    def f(t): return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e76(a, b) -> float:
    la, lb = rgb_to_lab(a), rgb_to_lab(b)
    return sum((la[i] - lb[i]) ** 2 for i in range(3)) ** 0.5


def relative_luminance(rgb) -> float:
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# --- checks --------------------------------------------------------------------
def suits_used(game_dir: Path) -> set[str]:
    """The distinct lowercased card `type`s that actually appear in component data."""
    used: set[str] = set()
    comp = game_dir / "components"
    for cpath in sorted(comp.glob("*.csv")) if comp.is_dir() else []:
        for r in csv.DictReader(cpath.open(newline="", encoding="utf-8")):
            t = (r.get("type") or "").strip().lower()
            if t:
                used.add(t)
    return used


def check_colourblind(theme: dict, used: set[str], rep: Report):
    print("\n• colour-blind suit separability")
    suit_map = theme["suits"]
    # only named suits the game actually uses (skip the _default fallback)
    suits = [(s, suit_map[s]) for s in sorted(used) if s in suit_map and s != "_default"]
    if len(suits) < 2:
        rep.info(f"{len(suits)} named theme suit(s) in use — nothing to disambiguate")
        return
    rep.info("suits: " + ", ".join(f"{s} ({d['color']}/{d['emblem']})" for s, d in suits))
    flagged = False
    for i in range(len(suits)):
        for j in range(i + 1, len(suits)):
            (sa, da), (sb, db) = suits[i], suits[j]
            ca, cb = hex_to_rgb(da["color"]), hex_to_rgb(db["color"])
            normal = delta_e76(ca, cb)
            if normal < DISTINCT:
                rep.warn(f"'{sa}' & '{sb}' are close even in normal vision (ΔE {normal:.0f}) — "
                         f"consider more contrasting colours")
            worst_type, worst = None, normal
            for name, m in CVD.items():
                d = delta_e76(simulate_cvd(ca, m), simulate_cvd(cb, m))
                if d < worst:
                    worst, worst_type = d, name
            if worst < CONFUSABLE:
                same_emblem = da["emblem"] == db["emblem"]
                where = f"under {worst_type} ΔE drops to {worst:.0f} (normal {normal:.0f})"
                if same_emblem:
                    rep.error(f"'{sa}' & '{sb}' collide {where} AND share emblem '{da['emblem']}' — "
                              f"colour is the ONLY channel. Give them distinct emblems or colours.")
                    flagged = True
                else:
                    rep.info(f"'{sa}' & '{sb}' collide on colour {where}, but differ by emblem "
                             f"('{da['emblem']}' vs '{db['emblem']}') — dual-coded, OK. Keep emblems prominent.")
            # else: safely distinct under all CVD types
    if not flagged:
        rep.ok("no colour-only suit collisions (every confusable pair is dual-coded by emblem)")


def check_contrast(theme: dict, rep: Report):
    print("\n• text contrast (WCAG)")
    stops = theme.get("page", ("#ffffff", "#ffffff"))
    for label in ("ink", "text"):
        col = theme.get(label)
        if not col:
            continue
        worst = min(contrast_ratio(hex_to_rgb(col), hex_to_rgb(bg)) for bg in stops)
        if worst < CONTRAST_MIN:
            rep.error(f"'{label}' {col} on page {stops}: contrast {worst:.1f}:1 < {CONTRAST_MIN}:1 (WCAG AA)")
        else:
            rep.ok(f"'{label}' {col} on page: {worst:.1f}:1")


def main():
    ap = argparse.ArgumentParser(description="Lint a game's data + theme for accessibility (colour-blind + contrast).")
    ap.add_argument("--game", required=True, type=Path, help="path to games/<slug>")
    ap.add_argument("--theme", required=True, help="render theme name (see tools/cards/themes.py)")
    args = ap.parse_args()

    theme = get_theme(args.theme)
    theme["_name"] = args.theme
    used = suits_used(args.game)

    print(f"Accessibility check — {args.game} (theme: {args.theme})")
    rep = Report()
    check_colourblind(theme, used, rep)
    check_contrast(theme, rep)

    print(f"\n{'=' * 48}\nResult: {rep.errors} error(s), {rep.warns} warning(s)")
    print("Judgement items (font size, text-independence, motor, communication, emotive) → "
          "see knowledge/accessibility.md + bg-access.")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
