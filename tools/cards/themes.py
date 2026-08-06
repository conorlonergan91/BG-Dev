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
            "signal":    {"color": "#c68a2b", "emblem": "beam"},      # brass lamp/beam — the keeper's light
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
    "night-market": {  # Travel Agents: Taiwan — a warm Taiwan night market at dusk.
        # FIRST-PASS palette from identity.md; NOT locked — pending the bg-access colour-blind check.
        # The identity flags a real red/green (deutan/protan) risk on the region colours (vermilion N
        # vs jade-teal C, amber S between), so EVERY suit is dual-coded: colour + a distinct emblem,
        # and the component data also carries a 繁體 + text label. Fonts include a CJK face so the
        # Traditional-character dish/ingredient labels render (Taiwan uses 繁體, never Simplified).
        "page": ("#F7F1E3", "#E9DCC2"),          # bao-paper cream, dusk-warmed toward the foot
        "ink": "#26324D",                         # dusk-indigo night sky — card borders + backs
        "text": "#2B2B2B",                        # soft ink body text
        "muted": "#7A6E58",                       # warm taupe for type lines / captions
        "accent": "#D64545",                      # lantern vermilion — flourishes, back rings
        # CJK-capable face FIRST: cairosvg's toy text API resolves the first family and does NOT fall
        # through the comma list, and dish/token text mixes Latin + 繁體 in one element — so the lead
        # font must carry BOTH scripts or the 繁體 renders as tofu boxes. WenQuanYi Zen Hei (installed
        # here) covers both; the mac/win faces follow for real-fallback renderers (e.g. browsers).
        "title_font": "'WenQuanYi Zen Hei', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif",
        "body_font": "'WenQuanYi Zen Hei', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif",
        "radius": 40,
        "suits": {
            # --- dish deck: suit = REGION (colour) + a distinct emblem (the dual-code) ---
            "north":      {"color": "#D64545", "emblem": "triangle"},  # Lantern vermilion — beef / pork
            "central":    {"color": "#1F8A7A", "emblem": "diamond"},   # Jade teal — tea / tapioca pearls
            "south":      {"color": "#E6A930", "emblem": "circle"},    # Golden amber — oysters / milkfish
            "east":       {"color": "#26324D", "emblem": "square"},    # Dusk indigo — rice / wild greens
            "signature":  {"color": "#C9A227", "emblem": "spark"},     # Gold — the cross-region feasts
            # --- assignment deck: the secret "Operation" dossier cards ---
            "assignment": {"color": "#26324D", "emblem": "stamp"},     # Dusk indigo + a passport stamp
            # --- ingredient tokens: colour = region, emblem distinct per specialty within its region ---
            "beef":       {"color": "#D64545", "emblem": "triangle"},
            "pork":       {"color": "#D64545", "emblem": "hex"},
            "tea":        {"color": "#1F8A7A", "emblem": "diamond"},
            "pearls":     {"color": "#1F8A7A", "emblem": "circle"},
            "oysters":    {"color": "#E6A930", "emblem": "hex"},
            "milkfish":   {"color": "#E6A930", "emblem": "diamond"},
            "rice":       {"color": "#26324D", "emblem": "square"},
            "greens":     {"color": "#26324D", "emblem": "triangle"},
            "pantry":     {"color": "#8A8F98", "emblem": "beam"},      # slate — convenience store, anywhere
            "_default":   {"color": "#26324D", "emblem": "circle"},
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
    if kind == "beam":  # a lamp with a glow halo — the lighthouse light (for Signals)
        return (f'<circle cx="{cx}" cy="{cy}" r="{r*0.95}" fill="none" stroke="{color}" '
                f'stroke-width="{max(2, r*0.16)}" opacity="0.5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r*0.5}" fill="{color}"/>')
    if kind == "stamp":  # an inked passport/dossier seal — a ring around a filled block (for Missions)
        o, inner = r * 0.95, r * 0.46
        return (f'<rect x="{cx-o}" y="{cy-o}" width="{2*o}" height="{2*o}" rx="{o*0.28}" fill="none" '
                f'stroke="{color}" stroke-width="{max(2, r*0.16)}" opacity="0.6"/>'
                f'<rect x="{cx-inner}" y="{cy-inner}" width="{2*inner}" height="{2*inner}" '
                f'rx="{inner*0.28}" fill="{color}"/>')
    # fallback
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" {sw}/>'
