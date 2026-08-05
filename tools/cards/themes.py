"""
themes.py — shared visual themes for the 2D pipeline (cards + covers).

A theme is just a palette + type styling + a per-suit map of {colour, emblem}. Everything renders as
plain SVG shapes (no external fonts or image assets), so it's cheap, deterministic, and works headless.

Used by build_cards.py (--theme) and build_cover.py (--theme).
Add a theme by copying an entry in THEMES. Suit keys are matched against a card's lowercased `type`
column (e.g. "Cargo" -> "cargo"); "signal" covers Signal cards; "_default" is the fallback.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------
THEMES = {
    "clean": {
        "page": ("#fbfbf9", "#eef0ee"),
        "ink": "#2c2c2c", "text": "#232323", "muted": "#6b6b6b", "accent": "#c0392b",
        "title_font": "Georgia, 'Times New Roman', serif",
        "body_font": "'Helvetica Neue', Arial, sans-serif",
        "radius": 36,
        "suits": {
            "_default": {"color": "#444444", "emblem": "circle"},
            "signal":   {"color": "#b8860b", "emblem": "spark"},
        },
    },
    "nautical": {  # Beacon: deep sea + brass + sea-foam
        "page": ("#eaf2f2", "#cfe0e2"),
        "ink": "#123244", "text": "#16323f", "muted": "#5b7683", "accent": "#c68a2b",
        "title_font": "Georgia, 'Times New Roman', serif",
        "body_font": "'Helvetica Neue', Arial, sans-serif",
        "radius": 34,
        "suits": {
            "cargo":     {"color": "#b5651d", "emblem": "hex"},       # copper
            "passenger": {"color": "#2a7f8f", "emblem": "diamond"},   # teal
            "naval":     {"color": "#7a2e3b", "emblem": "triangle"},  # deep red
            "signal":    {"color": "#c68a2b", "emblem": "spark"},     # brass beam
            "_default":  {"color": "#123244", "emblem": "circle"},
        },
    },
    "ember": {  # dark, dungeon/deckbuilder (Slay the Spire vibe)
        "page": ("#241f23", "#15100f"),
        "ink": "#e8d9b5", "text": "#ece3d0", "muted": "#a9977d", "accent": "#e2622a",
        "title_font": "Georgia, 'Times New Roman', serif",
        "body_font": "'Helvetica Neue', Arial, sans-serif",
        "radius": 30,
        "suits": {
            "attack":  {"color": "#e2622a", "emblem": "triangle"},
            "skill":   {"color": "#3d8ea6", "emblem": "diamond"},
            "power":   {"color": "#9b59b6", "emblem": "spark"},
            "signal":  {"color": "#d9a441", "emblem": "spark"},
            "_default": {"color": "#c9a227", "emblem": "circle"},
        },
    },
    "parchment": {  # warm classic / cozy
        "page": ("#f6ecd6", "#e7d6b3"),
        "ink": "#5b4326", "text": "#3f3016", "muted": "#8a7550", "accent": "#9c3b2e",
        "title_font": "Georgia, 'Times New Roman', serif",
        "body_font": "Georgia, serif",
        "radius": 32,
        "suits": {
            "_default": {"color": "#5b4326", "emblem": "diamond"},
            "signal":   {"color": "#9c3b2e", "emblem": "spark"},
        },
    },
    "cozy": {  # soft pastels
        "page": ("#fef6f0", "#eef3ec"),
        "ink": "#4b5d52", "text": "#3a4a41", "muted": "#8aa093", "accent": "#e08a7b",
        "title_font": "'Trebuchet MS', Verdana, sans-serif",
        "body_font": "'Trebuchet MS', Verdana, sans-serif",
        "radius": 44,
        "suits": {
            "_default": {"color": "#6b8f7a", "emblem": "circle"},
            "signal":   {"color": "#e0a95b", "emblem": "spark"},
        },
    },
}


def get_theme(name: str) -> dict:
    return THEMES.get((name or "clean").lower(), THEMES["clean"])


def resolve_suit(theme: dict, type_str: str) -> dict:
    key = (type_str or "").strip().lower()
    return theme["suits"].get(key, theme["suits"]["_default"])


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------
def page_gradient(theme: dict, gid: str) -> str:
    top, bottom = theme["page"]
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/>'
            f'</linearGradient>')


def emblem_svg(kind: str, cx: float, cy: float, r: float, color: str, stroke: str = "none") -> str:
    """A small filled emblem centred at (cx, cy) with radius r."""
    sw = 'stroke="%s" stroke-width="3"' % stroke if stroke != "none" else ""
    if kind == "circle":
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" {sw}/>'
    if kind == "square":
        return f'<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" rx="{r*0.2}" fill="{color}" {sw}/>'
    if kind == "diamond":
        pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
        return f'<polygon points="{pts}" fill="{color}" {sw}/>'
    if kind == "triangle":
        h = r * 1.1
        pts = f"{cx},{cy-h} {cx+r},{cy+r*0.75} {cx-r},{cy+r*0.75}"
        return f'<polygon points="{pts}" fill="{color}" {sw}/>'
    if kind == "hex":
        pts = " ".join(
            f"{cx + r*math.cos(math.radians(a))},{cy + r*math.sin(math.radians(a))}"
            for a in range(0, 360, 60)
        )
        return f'<polygon points="{pts}" fill="{color}" {sw}/>'
    if kind == "spark":  # 4-point sparkle (two crossed diamonds)
        a = f"{cx},{cy-r} {cx+r*0.32},{cy} {cx},{cy+r} {cx-r*0.32},{cy}"
        b = f"{cx-r},{cy} {cx},{cy+r*0.32} {cx+r},{cy} {cx},{cy-r*0.32}"
        return f'<polygon points="{a}" fill="{color}"/><polygon points="{b}" fill="{color}"/>'
    # fallback
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" {sw}/>'
