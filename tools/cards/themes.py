"""
themes.py — shared visual themes for the 2D pipeline (cards + covers).

A theme is just a palette + type styling + a per-suit map of {colour, emblem}. Everything renders as
plain SVG shapes (no external fonts or image assets), so it's cheap, deterministic, and works headless.

Used by build_cards.py (--theme) and build_cover.py (--theme).
Add a theme by copying an entry in THEMES. Suit keys are matched against a card's lowercased `type`
column (e.g. "Cargo" -> "cargo"); "signal" covers Signal cards; "_default" is the fallback.
"""
from __future__ import annotations

import html
import math


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)

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
        # --- CARD BACK identity (Travel-Agents-native — NOT the shared generic ring back) -------------
        # A theme that carries a "back" dict opts in to a bespoke back renderer (see build_cards.py
        # render_back_svg). Themes WITHOUT a "back" key (Beacon's `nautical`, clean, ember, …) fall
        # through to the unchanged generic ring back, so nothing else regresses. The look derives from
        # identity.md: a night-market boarding-pass / passport-stamp — dusk-indigo ground, a lantern-
        # vermilion stamp roundel, ticket-stub perforation, warm bao-paper panel. The day/night VARIANTS
        # layer the PHASE_STYLES treatment on top (warm sun 日 vs neon moon 夜) so a face-down pile sorts
        # into day/night by MOTIF + palette, never colour alone (bg-access: drawn sun/moon, CJK 日/夜).
        "back": {
            "ground": "#1B2338",        # deep dusk indigo — the constant TA border on every back
            "panel": ("#F7F1E3", "#E4D4B4"),  # bao-paper panel for the NEUTRAL (unphased/mixed) back
            "stamp": "#D64545",         # lantern-vermilion stamp roundel (neutral)
            "wordmark": "TRAVEL AGENTS",
            "sub": "台灣 · TAIWAN",
            "emblem": "stamp",          # neutral central motif = a passport/dossier stamp
        },
        "suits": {
            # --- dish deck: suit = REGION (colour) + a distinct emblem (the dual-code) ---
            "north":      {"color": "#D64545", "emblem": "triangle"},  # Lantern vermilion — beef / pork
            "central":    {"color": "#1F8A7A", "emblem": "diamond"},   # Jade teal — tea / tapioca pearls
            "south":      {"color": "#E6A930", "emblem": "circle"},    # Golden amber — oysters / milkfish
            "east":       {"color": "#26324D", "emblem": "square"},    # Dusk indigo — rice / wild greens
            "signature":  {"color": "#C9A227", "emblem": "spark"},     # Gold — the cross-region feasts
            # --- assignment deck: the secret "Operation" dossier cards (legacy v2, retained) ---
            "assignment": {"color": "#26324D", "emblem": "stamp"},     # Dusk indigo + a passport stamp
            # --- v3 secret signature-tour Mission cards: the +7 prize (gold seal, distinct from the
            # indigo assignment stamp and the gold spark of `signature`) ---
            "mission":    {"color": "#C9A227", "emblem": "stamp"},     # Gold + a passport stamp — the prize
            # --- v7 Bookings (開團): the SOLE scoring deck. Its own suit so it never renders the grey
            # `_default` (clears the linter's default-colour warning) and reads as a boarding-pass ticket.
            # A UNIQUE `ticket` emblem => it can NEVER share an emblem with another suit, so the CVD
            # checker can only ever downgrade a colour-clash to INFO (never an ERROR); boarding-pass blue
            # is off the four region hues + the gold prize + the violet Followers. (bg-infodesign) ---
            "booking":    {"color": "#3A6EA5", "emblem": "ticket"},    # boarding-pass blue — the 開團 scoring deck
            # --- v7 LOCKED 6-category generic ingredient taxonomy (source of truth:
            # components/recipe-glyphs.csv). These are keyed off the `ingredient` column, so the big
            # ingredient-card glyph, the vendor recipe chip, and the token all render the SAME
            # colour+emblem for a category. Every category is dual-coded — a DISTINCT colour AND a
            # DISTINCT emblem — so no two share colour+emblem. Colours are EXACTLY recipe-glyphs.csv.
            # veg (green) is deliberately shape-distinct from meat (red): red/green is the classic
            # protan/deutan confusable, so the leaf-vs-hex SHAPE is the required redundant encoding
            # (accessibility.md). Each category's colour matches its home REGION suit hue but carries a
            # different emblem than that region's frame emblem, so a same-colour+same-emblem clash never
            # arises (meat/north, tea/central, seafood/south, pantry/east). ---
            "meat":       {"color": "#D64545", "emblem": "hex"},       # 肉 red   — North signature (region north = triangle)
            "tea":        {"color": "#1F8A7A", "emblem": "triangle"},  # 茶 teal  — Central signature (region central = diamond)
            "seafood":    {"color": "#E6A930", "emblem": "square"},    # 海鮮 amber — South signature (region south = circle)
            "pantry":     {"color": "#26324D", "emblem": "circle"},    # 糧 indigo — East signature (region east = square)
            "sugar":      {"color": "#B5835A", "emblem": "beam"},      # 糖 caramel — the COMMON (Central & South)
            "veg":        {"color": "#4C9A5A", "emblem": "leaf"},      # 菜 green  — the COMMON (North & East); leaf shape-distinct from meat-hex (CVD)
            # --- LEGACY per-specialty ingredient keys (pre-v7). NOT in any current component data — the
            # generic render keys off the 6 categories above — but retained (harmless dead keys) in case a
            # legacy render path or archived build still references them. Do not add new data on these. ---
            "beef":       {"color": "#D64545", "emblem": "square"},
            "pork":       {"color": "#D64545", "emblem": "hex"},
            "chicken":    {"color": "#D64545", "emblem": "diamond"},
            "egg":        {"color": "#D64545", "emblem": "circle"},
            "pearls":     {"color": "#1F8A7A", "emblem": "circle"},
            "oysters":    {"color": "#E6A930", "emblem": "hex"},
            "milkfish":   {"color": "#E6A930", "emblem": "diamond"},
            "rice":       {"color": "#26324D", "emblem": "circle"},
            "greens":     {"color": "#26324D", "emblem": "triangle"},
            # --- v3 second currency: Buzz (its own colour, off the four region hues + the CVD checker) ---
            "buzz":       {"color": "#6A4C93", "emblem": "spark"},     # violet — promotional Buzz
            "_default":   {"color": "#26324D", "emblem": "circle"},
        },
    },
}


# ---------------------------------------------------------------------------
# Phase treatments (day / night) — a data-driven recolour keyed off a card's
# `phase` column, layered ON TOP of the region/suit palette. The region colour
# still carries WHERE (header band + emblem); the phase treatment carries WHEN
# (warm morning vs neon night market) via three cheap, legible signals that never
# fight the body text: a tinted card ground, a recoloured outer frame, and a slim
# phase ribbon along the bottom margin. Card interiors stay light so all the CJK +
# body text keeps its contrast — the day/night read lives in the frame + ground.
# `phase_style` returns None for phase-less decks (e.g. characters) → unchanged.
# ---------------------------------------------------------------------------
PHASE_STYLES = {
    "day": {   # warm morning — sunrise cream, gold frame
        "page": ("#FDF4DB", "#F6DFAE"),
        "frame": "#E6A930",        # morning amber (FACE frame / board frame — a line, not text)
        "back_stamp": "#A65E12",   # darker bronze for the BACK stamp roundel + wordmark ink so the
                                   # day motif/日/wordmark clears large-text contrast on cream
                                   # (~4.5:1 vs amber's 1.6:1) — bg-access WATCH fix; night needs none
        "glow": "#F4CE7E",
        "tag_fill": "#E6A930",
        "tag_ink": "#3A2A0E",
        "label": "日 DAY 早",
        "emblem": "sun",           # drawn (not the ☀ glyph — cairosvg toy text renders it tofu)
    },
    "night": {  # neon night market — dusk ground drifting to lantern-lit lavender, neon frame
        "page": ("#EDE1CB", "#D7C6E6"),
        "frame": "#B14FD8",        # neon violet
        "glow": "#59D6D6",         # neon cyan counter-glow
        "tag_fill": "#6A4C93",     # deep promo violet (matches the Buzz currency)
        "tag_ink": "#FFFFFF",
        "label": "夜 NIGHT 市",
        "emblem": "moon",          # drawn crescent (not the ☾/🌙 glyph — tofu in this font)
    },
    "general": {  # seeds both phases — neutral gold
        "page": ("#F5EEDD", "#E9DCC2"),
        "frame": "#C9A227",
        "glow": "#E4CE8A",
        "tag_fill": "#C9A227",
        "tag_ink": "#3A2A0E",
        "label": "通用 ANY",
        "emblem": "spark",
    },
}


def phase_style(phase: str) -> dict | None:
    """Return the day/night treatment for a card's `phase` value, or None (neutral)."""
    return PHASE_STYLES.get((phase or "").strip().lower())


# Phase → the character + drawn motif a card back carries (font-covered 繁體 + a DRAWN sun/moon, so a
# face-down pile sorts by shape, never colour alone — bg-access). Neutral (mixed/unphased) decks get no
# phase mark, just the base TA passport identity.
BACK_PHASE = {
    "day":     {"char": "日", "label": "DAY · 早", "emblem": "sun"},
    "night":   {"char": "夜", "label": "NIGHT · 夜市", "emblem": "moon"},
    "general": {"char": "通", "label": "ANY · 通用", "emblem": "spark"},
}


def back_style(theme: dict, phase: str | None) -> dict | None:
    """Resolve a theme's card-back styling, merged with the day/night/general treatment.

    Returns None when the theme carries no `back` key → the caller renders the shared generic back
    (so Beacon and every non-opted-in theme are byte-unchanged). When a `back` key IS present, returns
    a dict of {ground, panel, stamp, wordmark, sub, emblem, char?, label?, glow?} with the phase layered
    on: day = warm sunrise + sun 日, night = neon night-market + moon 夜, general = gold + 通, and a bare
    phase (or None) = the neutral passport back."""
    back = theme.get("back")
    if not back:
        return None
    out = dict(back)  # base TA identity (neutral)
    ph = (phase or "").strip().lower()
    pstyle = PHASE_STYLES.get(ph)
    bp = BACK_PHASE.get(ph)
    if pstyle and bp:
        out["panel"] = pstyle["page"]      # warm/neon panel ground
        out["stamp"] = pstyle.get("back_stamp", pstyle["frame"])  # prefer a contrast-safe back stamp (day bronze); else the phase frame
        out["glow"] = pstyle.get("glow")
        out["emblem"] = bp["emblem"]       # drawn sun / moon / spark
        out["char"] = bp["char"]           # 日 / 夜 / 通  (font-covered, never ☀/☾ tofu)
        out["label"] = bp["label"]
    return out


def phase_ribbon_svg(style: dict, card_w: int, card_h: int, margin: int, tfont: str) -> str:
    """A slim phase ribbon in the bottom margin — the collision-free at-a-glance day/night signal.
    Sits below every template's content (perk box / +VP chip / value numeral all end by card_h-margin)."""
    if not style:
        return ""
    h = 36
    y = card_h - h - 10
    x0, x1 = 44, card_w - 44
    w = x1 - x0
    cy = y + h / 2
    # drawn day/night badge (a shape, never a glyph) so phase is dual-coded: colour + badge + word
    badge = emblem_svg(style.get("emblem", "spark"), x0 + 34, cy, 13, style["tag_ink"])
    return (
        f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" rx="{h/2}" '
        f'fill="{style["tag_fill"]}" opacity="0.96"/>'
        + badge +
        f'<text x="{card_w/2}" y="{y + h*0.68}" font-size="27" fill="{style["tag_ink"]}" '
        f'text-anchor="middle" font-family="{tfont}" font-weight="bold" '
        f'letter-spacing="4">{esc(style["label"])}</text>')


def get_theme(name: str) -> dict:
    return THEMES.get((name or "clean").lower(), THEMES["clean"])


def resolve_suit(theme: dict, type_str: str) -> dict:
    key = (type_str or "").strip().lower()
    return theme["suits"].get(key, theme["suits"]["_default"])


# ---------------------------------------------------------------------------
# Contrast helpers (WCAG) — shared so renderers can pick legible text colours.
# Pure/additive; safe for every existing caller.
# ---------------------------------------------------------------------------
def _rgb01(hex_color: str):
    h = (hex_color or "#000000").lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    r, g, b = (_lin(c) for c in _rgb01(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def pick_text_color(bg: str, dark: str = "#000000", light: str = "#ffffff") -> str:
    """Return whichever of `dark`/`light` has the higher WCAG contrast on `bg`."""
    return dark if contrast_ratio(dark, bg) >= contrast_ratio(light, bg) else light


def boost_contrast(fg: str, bg: str, target: float = 4.5) -> str:
    """Nudge `fg` toward white/black (away from `bg`) until it meets `target` on `bg`.
    Returns `fg` unchanged when it already passes — so callers that already comply are untouched."""
    if contrast_ratio(fg, bg) >= target:
        return fg
    toward = "#ffffff" if relative_luminance(bg) < 0.5 else "#000000"
    fr, tr = _rgb01(fg), _rgb01(toward)
    for step in range(1, 21):
        t = step / 20
        cand = "#%02x%02x%02x" % tuple(round((fr[i] + (tr[i] - fr[i]) * t) * 255) for i in range(3))
        if contrast_ratio(cand, bg) >= target:
            return cand
    return toward


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------
def page_gradient(theme: dict, gid: str, colors: tuple | None = None) -> str:
    top, bottom = colors if colors else theme["page"]
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
    if kind == "ring_dot":  # ⦿ scope=SELF — a ring with a filled centre dot
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
                f'stroke-width="{max(2, r*0.30)}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r*0.40}" fill="{color}"/>')
    if kind == "island_ring":  # ISLAND-WIDE scope — concentric double ring (shape-distinct from
        # ⦿ ring_dot / ⬢ hex / ➤ arrow); says "hits the whole board", not a drawn-region scope.
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
                f'stroke-width="{max(2, r*0.24)}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r*0.58}" fill="none" stroke="{color}" '
                f'stroke-width="{max(2, r*0.24)}"/>')
    if kind == "arrow":  # ➤ scope=NEXT DOOR — a right-pointing arrowhead
        pts = f"{cx-r},{cy-r*0.92} {cx+r},{cy} {cx-r},{cy+r*0.92} {cx-r*0.45},{cy}"
        return f'<polygon points="{pts}" fill="{color}" {sw}/>'
    if kind == "sun":  # ☀ phase=DAY — a disc with rays
        rays = "".join(
            f'<line x1="{cx + math.cos(math.radians(a))*r*0.78}" '
            f'y1="{cy + math.sin(math.radians(a))*r*0.78}" '
            f'x2="{cx + math.cos(math.radians(a))*r*1.20}" '
            f'y2="{cy + math.sin(math.radians(a))*r*1.20}" '
            f'stroke="{color}" stroke-width="{max(2, r*0.20)}" stroke-linecap="round"/>'
            for a in range(0, 360, 45))
        return rays + f'<circle cx="{cx}" cy="{cy}" r="{r*0.55}" fill="{color}"/>'
    if kind == "moon":  # ☾ phase=NIGHT — a crescent (outer disc minus an offset disc, evenodd)
        off = r * 0.52
        ri = r * 0.92
        return (f'<path fill-rule="evenodd" fill="{color}" d="'
                f'M {cx} {cy-r} a {r} {r} 0 1 0 0 {2*r} a {r} {r} 0 1 0 0 {-2*r} Z '
                f'M {cx+off} {cy-ri} a {ri} {ri} 0 1 0 0 {2*ri} a {ri} {ri} 0 1 0 0 {-2*ri} Z"/>')
    if kind == "crowd":  # 人氣 crowd-pull — a little cluster of people (NOT the gold VP spark);
        # keeps DRAW reading as an audience/popularity attribute, never a score numeral.
        s = ""
        for dx in (-r * 0.62, 0.0, r * 0.62):
            hx = cx + dx
            s += f'<circle cx="{hx}" cy="{cy-r*0.34}" r="{r*0.34}" fill="{color}"/>'
            s += (f'<path d="M {hx-r*0.44} {cy+r*0.74} q {r*0.44} -{r*0.62} {r*0.88} 0 Z" '
                  f'fill="{color}"/>')
        return s
    if kind == "home":  # a house — 里長伯's home-region marker
        return (f'<path d="M {cx} {cy-r} L {cx+r} {cy-r*0.12} L {cx+r*0.72} {cy-r*0.12} '
                f'L {cx+r*0.72} {cy+r} L {cx-r*0.72} {cy+r} L {cx-r*0.72} {cy-r*0.12} '
                f'L {cx-r} {cy-r*0.12} Z" fill="{color}" {sw}/>')
    if kind == "spark":  # 4-point sparkle (two crossed diamonds)
        a = f"{cx},{cy-r} {cx+r*0.32},{cy} {cx},{cy+r} {cx-r*0.32},{cy}"
        b = f"{cx-r},{cy} {cx},{cy+r*0.32} {cx+r},{cy} {cx},{cy-r*0.32}"
        return f'<polygon points="{a}" fill="{color}"/><polygon points="{b}" fill="{color}"/>'
    if kind == "beam":  # a lamp with a glow halo — the lighthouse light (for Signals)
        return (f'<circle cx="{cx}" cy="{cy}" r="{r*0.95}" fill="none" stroke="{color}" '
                f'stroke-width="{max(2, r*0.16)}" opacity="0.5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r*0.5}" fill="{color}"/>')
    if kind == "ticket":  # a boarding-pass / booking stub — rounded rect + a torn perforation edge
        w, h = r * 1.15, r * 0.82
        perf_x = cx + w * 0.34
        return (f'<rect x="{cx-w}" y="{cy-h}" width="{2*w}" height="{2*h}" rx="{h*0.3}" fill="{color}" {sw}/>'
                f'<line x1="{perf_x}" y1="{cy-h*0.72}" x2="{perf_x}" y2="{cy+h*0.72}" '
                f'stroke="#ffffff" stroke-width="{max(2, r*0.16)}" stroke-dasharray="{r*0.2} {r*0.15}" opacity="0.9"/>')
    if kind == "stamp":  # an inked passport/dossier seal — a ring around a filled block (for Missions)
        o, inner = r * 0.95, r * 0.46
        return (f'<rect x="{cx-o}" y="{cy-o}" width="{2*o}" height="{2*o}" rx="{o*0.28}" fill="none" '
                f'stroke="{color}" stroke-width="{max(2, r*0.16)}" opacity="0.6"/>'
                f'<rect x="{cx-inner}" y="{cy-inner}" width="{2*inner}" height="{2*inner}" '
                f'rx="{inner*0.28}" fill="{color}"/>')
    if kind == "leaf":  # 菜 Vegetables — a pointed leaf silhouette with a carved midrib vein
        # (fill-rule evenodd: the thin sliver becomes a hole showing the ground). Shape-distinct from
        # meat's hex so the veg-green / meat-red pair — the classic protan/deutan confusable — is
        # dual-coded by SHAPE, not colour alone (bg-access). New/additive: no existing theme references
        # 'leaf', so Beacon and every other theme render byte-identically. Degrades gracefully — at token
        # scale the hairline vein may close up, leaving a solid, still-leaf-shaped glyph.
        body = (f"M {cx} {cy-r} "
                f"C {cx+r*0.92} {cy-r*0.28}, {cx+r*0.58} {cy+r*0.82}, {cx} {cy+r} "
                f"C {cx-r*0.58} {cy+r*0.82}, {cx-r*0.92} {cy-r*0.28}, {cx} {cy-r} Z")
        vein = (f"M {cx-r*0.07} {cy-r*0.52} L {cx+r*0.07} {cy-r*0.52} "
                f"L {cx+r*0.07} {cy+r*0.70} L {cx-r*0.07} {cy+r*0.70} Z")
        return f'<path fill-rule="evenodd" fill="{color}" d="{body} {vein}" {sw}/>'
    # fallback
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" {sw}/>'
