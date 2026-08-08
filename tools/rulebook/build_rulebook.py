#!/usr/bin/env python3
"""
build_rulebook.py — turn a rules markdown file into a themed, laid-out rulebook.

Finishes the "producible" story: your rules live as markdown (diffable, the source of truth), and this
renders them to a styled A5 HTML/PDF that matches the game's theme. A clean rulebook is also the thing
blind-testers actually use, so it's worth generating early and often.

Usage:
    python tools/rulebook/build_rulebook.py --md games/beacon/design/rules-draft.md \
        --title "Beacon" --theme nautical --out games/beacon/build/rulebook.pdf

Output: always writes .html; writes .pdf too if WeasyPrint is installed
(pip install weasyprint markdown ; macOS also needs `brew install pango gdk-pixbuf`).
"""
from __future__ import annotations

import argparse
import html
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import get_theme, emblem_svg, pick_text_color, PHASE_STYLES  # noqa: E402


# ---------------------------------------------------------------------------
# Iconography legend page (the flip-to legend). Injected only where a markdown
# file contains the {{ICONOGRAPHY}} token, so rulebooks without it (Beacon) are
# byte-identical. Every glyph is DRAWN via the shared emblem_svg (no font glyphs
# → no ☀/☾/⦿ tofu), so the legend matches the cards/tokens exactly and stays
# colour-blind-safe (shape + 繁體 label, never colour alone).
# ---------------------------------------------------------------------------
ICON_TOKEN = "{{ICONOGRAPHY}}"

# Figure directive: a `> 🖼 **[FIG-CODE]** — brief…` blockquote becomes a RESERVED image box (a dashed
# placeholder sized for the illustrator's art) with the brief kept as a caption — instead of the plain
# bordered-callout fallback. Only fires on blockquotes carrying a [FIG-…] code, so rulebooks without them
# (Beacon) are byte-identical. Optionally, `[FIG-CODE|path.png]` embeds a real image if the file exists.
FIG_BLOCK_RE = re.compile(r'<blockquote>\s*(<p>.*?\[FIG-[A-Z0-9-]+.*?\].*?</p>)\s*</blockquote>', re.DOTALL)
FIG_CODE_RE = re.compile(r'\[FIG-([A-Z0-9-]+)(?:\|([^\]]+))?\]')


def insert_figure_boxes(body_html: str) -> str:
    """Turn [FIG-…] blockquotes into reserved figure boxes. Non-matching content is untouched."""
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        cm = FIG_CODE_RE.search(inner)
        code = cm.group(1) if cm else ""
        img = (cm.group(2).strip() if (cm and cm.group(2)) else "")
        if img and Path(img).exists():
            reserve = f'<img class="figimg" src="{html.escape(img)}" alt="{html.escape(code)}"/>'
        else:
            reserve = (f'<div class="figreserve"><span class="figcode">🖼 FIG · {html.escape(code)}</span>'
                       f'<span class="fignote">illustration reserved — see art brief</span></div>')
        return f'<figure class="figbox">{reserve}<figcaption>{inner}</figcaption></figure>'
    return FIG_BLOCK_RE.sub(repl, body_html)


def _star_svg(cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append(f"{cx + rr*math.cos(ang):.1f},{cy + rr*math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'


def _tile(inner, name, desc):
    return (f'<div class="li"><svg viewBox="0 0 84 80" class="g">{inner}</svg>'
            f'<div class="lb"><b>{html.escape(name)}</b><span>{html.escape(desc)}</span></div></div>')


def _chip(shape, color, char, ink, font):
    """A shape in its suit colour with a 繁體 glyph on top (matches the token/chip grammar). `font` must
    lead with a CJK-capable face so the 繁體 renders (never tofu) in both WeasyPrint and cairosvg."""
    s = emblem_svg(shape, 42, 34, 26, color, stroke=ink)
    tc = pick_text_color(color, dark=ink, light="#ffffff")
    return (s + f'<text x="42" y="44" font-size="28" text-anchor="middle" fill="{tc}" '
            f'font-family="{font}" font-weight="bold">{html.escape(char)}</text>')


def iconography_html(theme: dict) -> str:
    ink = theme["ink"]
    suits = theme["suits"]
    bfont = theme["body_font"]  # WenQuanYi-first — carries the 繁體 in the drawn glyphs (no tofu)
    def col(k, d="#888"): return suits.get(k, {}).get("color", d)
    day, night = PHASE_STYLES["day"], PHASE_STYLES["night"]
    gold = col("signature", "#C9A227")
    teal = col("central", "#1F8A7A")
    violet = col("buzz", "#6A4C93")
    taupe = theme.get("muted", "#7A6E58")
    muted = theme["muted"]
    north = col("north", "#D64545")
    slate = "#8A8F98"   # the Scheduled-Maintenance island slate (matches build_cards MAINT_SLATE)

    # 1) Ingredients (the 5-token palette) — shape + colour + 繁體
    ingredients = "".join([
        _tile(_chip("hex", col("pork", "#D64545"), "豬", ink, bfont), "Pork 豬肉", "North signature · hexagon"),
        _tile(_chip("triangle", col("tea", "#1F8A7A"), "茶", ink, bfont), "Tea 茶", "Central signature · triangle"),
        _tile(_chip("square", col("seafood", "#E6A930"), "海", ink, bfont), "Seafood 海鮮", "South signature · square"),
        _tile(_chip("circle", col("rice", "#26324D"), "米", ink, bfont), "Rice 米", "East signature · circle"),
        _tile(_chip("beam", col("sugar", "#B5835A"), "糖", ink, bfont), "Sugar 糖", "The common (C & S only) · beam"),
    ])
    # 2) Regions — colour + emblem
    regions = "".join([
        _tile(_chip("triangle", col("north", "#D64545"), "北", ink, bfont), "North 北", "vermilion · triangle · pork"),
        _tile(_chip("diamond", col("central", "#1F8A7A"), "中", ink, bfont), "Central 中", "jade · diamond · tea"),
        _tile(_chip("circle", col("south", "#E6A930"), "南", ink, bfont), "South 南", "amber · circle · seafood"),
        _tile(_chip("square", col("east", "#26324D"), "東", ink, bfont), "East 東", "indigo · square · rice"),
    ])
    # 3) Event scope — DRAWN shapes (never the ⦿/⬢/➤ font glyphs). The island-wide double-ring is the
    # Scheduled-Maintenance banner marker — deliberately NOT a 4th scope glyph: it's a table-wide event
    # with its own banner frame, listed here so a player who sees it knows it isn't a ⦿/⬢/➤ card.
    scope = "".join([
        _tile(emblem_svg("ring_dot", 42, 34, 24, ink), "⦿ You", "self — only the flipper"),
        _tile(emblem_svg("hex", 42, 34, 24, ink), "⬢ This region", "everyone standing in the drawn region"),
        _tile(emblem_svg("arrow", 42, 34, 24, ink), "➤ Next door", "spills into a neighbouring region"),
        _tile(emblem_svg("island_ring", 42, 34, 24, slate, stroke=ink), "◎ Island-wide",
              "Scheduled Maintenance (HSR down for all) — its OWN banner, not a ⦿/⬢/➤ card"),
    ])
    # 4) Phase — drawn sun/moon + 繁體 (never ☀/☾)
    phase = "".join([
        _tile(emblem_svg("sun", 42, 32, 22, day["frame"])
              + f'<text x="42" y="72" font-size="24" text-anchor="middle" fill="{day["frame"]}" font-family="{bfont}" font-weight="bold">日</text>',
              "Day 日 · 早", "warm morning layer — breakfast run"),
        _tile(emblem_svg("moon", 42, 32, 22, night["frame"])
              + f'<text x="42" y="72" font-size="24" text-anchor="middle" fill="{night["frame"]}" font-family="{bfont}" font-weight="bold">夜</text>',
              "Night 夜 · 市", "neon night-market layer (after dusk)"),
    ])
    # 5) The fight — Buzz · Reach · Draw. TICKETS-ONLY (v6.3.1): NONE of these score — the score is the
    # ticket piles (§ below). Draw uses the vendor face's crowd glyph in GOLD (never the gold ★-spark,
    # which reads as VP); Reach is the drawn violet Buzz-cap (no invented 繁體 — Reach carries no blessed
    # char anywhere in the game, so the tile shows the cap relationship, not a character); ★ apex is the
    # top-Draw trophy, not a prize that scores.
    fight = "".join([
        _tile(emblem_svg("spark", 42, 34, 24, violet)
              + f'<text x="42" y="44" font-size="22" text-anchor="middle" fill="#fff" font-family="{bfont}" font-weight="bold">讚</text>',
              "Buzz 讚", "the hype you pile on a vendor (the fight currency)"),
        _tile(f'<line x1="18" y1="22" x2="66" y2="22" stroke="{violet}" stroke-width="5" stroke-linecap="round"/>'
              f'<circle cx="34" cy="44" r="10" fill="{violet}"/><circle cx="54" cy="44" r="10" fill="{violet}"/>',
              "Reach", "your Buzz cap — committed Buzz ≤ Reach. NOT a score"),
        _tile(emblem_svg("crowd", 42, 34, 22, gold),
              "Draw 人氣", "a vendor's crowd-pull attribute — NOT a score"),
        _tile(_star_svg(42, 34, 26, gold), "★ Apex / Star",
              "top-Draw trophy vendor (no discount icon); scores nothing itself"),
    ])
    # 6) The two ticket piles — the ONLY thing that scores (tickets-only).
    piles = "".join([
        _tile(emblem_svg("stamp", 42, 34, 24, gold)
              + f'<text x="42" y="44" font-size="24" text-anchor="middle" fill="{pick_text_color(gold, dark=ink, light="#fff")}" font-family="{bfont}" font-weight="bold">成</text>',
              "成團 · Win pile", "tours that RAN: score +the ticket's printed value"),
        _tile(emblem_svg("stamp", 42, 34, 24, taupe)
              + f'<text x="42" y="44" font-size="24" text-anchor="middle" fill="#fff" font-family="{bfont}" font-weight="bold">遺</text>',
              "遺珠 · Lose pile", "the ones that got away: -½ the ticket's value"),
    ])
    # 7) Counters & character markers — the Tours-Completed METER (must NOT read as the 成團 score pile:
    # teal meter with the 2/4 Rave-Review ticks, no stamp) + 里長伯's home-discount / away-tax mat icons
    # (drawn exactly as build_cards' kit_icon: a teal home −1 and a vermilion away-arrow +1).
    counters = "".join([
        _tile(f'<rect x="14" y="30" width="56" height="16" rx="8" fill="{teal}" opacity="0.92"/>'
              f'<line x1="34" y1="24" x2="34" y2="52" stroke="{ink}" stroke-width="3"/>'
              f'<line x1="54" y1="24" x2="54" y2="52" stroke="{ink}" stroke-width="3"/>',
              "Tours Completed", "your completions meter (Rave Reviews at 2 & 4) — NOT the 成團 score"),
        _tile(emblem_svg("home", 30, 34, 18, teal, stroke=ink)
              + f'<circle cx="58" cy="46" r="13" fill="#fff" stroke="{teal}" stroke-width="3"/>'
              f'<text x="58" y="52" font-size="17" text-anchor="middle" fill="{teal}" font-family="{bfont}" font-weight="bold">-1</text>',
              "里長伯 · home -1", "cheaper to Bribe in his chosen home region"),
        _tile(emblem_svg("arrow", 28, 34, 16, north, stroke=ink)
              + f'<circle cx="58" cy="46" r="13" fill="#fff" stroke="{north}" stroke-width="3"/>'
              f'<text x="58" y="52" font-size="17" text-anchor="middle" fill="{north}" font-family="{bfont}" font-weight="bold">+1</text>',
              "里長伯 · away +1", "the away tax: +1 ingredient off his home patch"),
    ])

    # 8) Vendor card — layout key. Mirrors the v6.3.1 render_vendor_svg face EXACTLY: a de-scored two-input
    # PAY row (ingredient chips + the Buzz reminder) + a printed DRAW (人氣) crowd-pull ATTRIBUTE in a gauge
    # + a region-discount ICON (or none) — and NO GAIN, NO Prestige, NO Reputation, NO perk. The old
    # GAIN(★+譽)+PERK schematic is retired: vendors don't score.
    vkey = f'''<svg viewBox="0 0 760 392" class="vkey">
      <rect x="8" y="8" width="224" height="372" rx="16" fill="#fff" stroke="{ink}" stroke-width="3"/>
      <!-- ① header band: region colour + dish name + tier pill -->
      <path d="M8 24 a16 16 0 0 1 16 -16 h192 a16 16 0 0 1 16 16 v40 h-224 z" fill="{north}"/>
      <text x="22" y="42" font-size="19" fill="#fff" font-family="{bfont}" font-weight="bold">肉包 · Bao</text>
      <rect x="158" y="14" width="62" height="26" rx="13" fill="#fff" opacity="0.9"/>
      <text x="189" y="33" font-size="15" fill="{north}" text-anchor="middle" font-family="{bfont}" font-weight="bold">攤</text>
      <!-- region strip + English dish name -->
      {emblem_svg("triangle", 26, 90, 12, north)}<text x="46" y="96" font-size="16" fill="{north}" font-family="{bfont}" font-weight="bold">NORTH 北</text>
      <text x="216" y="96" font-size="13" fill="{muted}" text-anchor="end" font-family="{bfont}" font-style="italic">engine</text>
      <text x="22" y="122" font-size="16" fill="{ink}" font-family="{bfont}" font-style="italic">Pork Bao</text>
      <!-- ② PAY row: ingredient chip (shape+繁體) + Buzz reminder (讚) -->
      <text x="22" y="152" font-size="14" fill="{theme['accent']}" font-family="{bfont}" font-weight="bold">PAY 付</text>
      {emblem_svg("hex", 40, 184, 16, north, stroke=ink)}<text x="40" y="190" font-size="15" fill="#fff" text-anchor="middle" font-family="{bfont}" font-weight="bold">豬</text>
      <text x="66" y="190" font-size="24" fill="{muted}" font-family="{bfont}" font-weight="bold">+</text>
      <circle cx="108" cy="184" r="16" fill="{violet}" stroke="{ink}" stroke-width="2"/><text x="108" y="190" font-size="15" fill="#fff" text-anchor="middle" font-family="{bfont}" font-weight="bold">2</text>
      <text x="130" y="190" font-size="12" fill="{violet}" font-family="{bfont}" font-weight="bold">讚</text>
      <!-- ③ DRAW row: crowd glyph + gauge number (an attribute, NOT points) -->
      <text x="22" y="224" font-size="14" fill="{theme['accent']}" font-family="{bfont}" font-weight="bold">DRAW 人氣</text>
      {emblem_svg("crowd", 40, 256, 16, gold)}
      <rect x="66" y="240" width="46" height="30" rx="15" fill="none" stroke="{gold}" stroke-width="2.5"/>
      <text x="89" y="262" font-size="20" fill="{gold}" text-anchor="middle" font-family="{bfont}" font-weight="bold">2</text>
      <text x="120" y="262" font-size="11" fill="{muted}" font-family="{bfont}" font-style="italic">not points</text>
      <!-- ④ ICON box: region discount icon (or NONE) -->
      <text x="22" y="296" font-size="14" fill="{theme['accent']}" font-family="{bfont}" font-weight="bold">ICON 圖示</text>
      <rect x="22" y="304" width="196" height="34" rx="10" fill="none" stroke="{north}" stroke-width="2"/>
      {emblem_svg("triangle", 40, 322, 12, north)}<text x="58" y="326" font-size="12.5" fill="{ink}" font-family="{bfont}">N discount — its region -1</text>
      <!-- ⑤ phase ribbon -->
      <rect x="28" y="350" width="184" height="22" rx="11" fill="{day['tag_fill']}"/>
      <text x="120" y="366" font-size="12" fill="{day['tag_ink']}" text-anchor="middle" font-family="{bfont}" font-weight="bold">日 DAY 早</text>
      <g font-family="{bfont}" font-size="15" fill="{ink}">
        <text x="256" y="30">① <tspan font-weight="bold">Header band</tspan> = region colour + emblem + dish name</text>
        <text x="256" y="66">② <tspan font-weight="bold">PAY 付</tspan> = ingredient chips (shape+繁體) + Buzz needed (讚)</text>
        <text x="278" y="88" font-size="12.5" fill="{muted}">night marquees add a CROSS-REGION →X tag (a two-region bill)</text>
        <text x="256" y="124">③ <tspan font-weight="bold">DRAW 人氣</tspan> = the crowd-pull ATTRIBUTE — NOT points</text>
        <text x="256" y="160">④ <tspan font-weight="bold">ICON 圖示</tspan> = a region discount icon (N/C/S/E), or NONE</text>
        <text x="278" y="182" font-size="12.5" fill="{muted}">no icon = a ★ apex trophy, or a drink (filler)</text>
        <text x="256" y="218">⑤ <tspan font-weight="bold">Phase ribbon</tspan> = day 日 / night 夜 (which layer)</text>
        <text x="256" y="258">Top-right pill = venue tier (攤 stall · 小吃 eatery · 名店 marquee)</text>
        <text x="256" y="294">★ apex = top-Draw trophy: no discount icon, scores nothing itself</text>
        <text x="256" y="336" fill="{theme['accent']}" font-weight="bold">Vendors don't score: no GAIN, Prestige, Reputation or perk.</text>
      </g>
    </svg>'''

    css = f'''<style>
      .iconography {{ page-break-before: always; }}
      .iconography h1 {{ margin-bottom: 4pt; }}
      .iconography .lead {{ color: {theme['muted']}; font-style: italic; margin: 0 0 8pt; font-size: 9.5pt; }}
      .iconography h2 {{ font-size: 12.5pt; margin: 12pt 0 5pt; border-bottom: 1.5pt solid {theme['accent']}; }}
      .legend-grid {{ display: flex; flex-wrap: wrap; gap: 6pt 14pt; margin-bottom: 4pt; }}
      .li {{ display: flex; align-items: center; gap: 6pt; width: 46%; }}
      .li .g {{ width: 34pt; height: 32pt; flex: none; }}
      .li .lb {{ display: flex; flex-direction: column; line-height: 1.15; }}
      .li .lb b {{ font-size: 9.5pt; color: {ink}; }}
      .li .lb span {{ font-size: 8pt; color: {theme['muted']}; }}
      .vkey {{ width: 100%; height: auto; margin-top: 4pt; }}
    </style>'''

    return (f'{css}<section class="iconography"><h1>Iconography — the flip-to legend</h1>'
            f'<p class="lead">Every glyph on the cards, tokens, and board. Shapes are drawn, so they read '
            f'by shape + 繁體 label, never colour alone.</p>'
            f'<h2>Ingredients (the 5 tokens)</h2><div class="legend-grid">{ingredients}</div>'
            f'<h2>The four regions</h2><div class="legend-grid">{regions}</div>'
            f'<h2>Event scope — who it hits</h2><div class="legend-grid">{scope}</div>'
            f'<h2>Day / Night</h2><div class="legend-grid">{phase}</div>'
            f'<h2>The fight — Buzz · Reach · Draw <span style="font-weight:normal;font-size:9pt;">(none of these score)</span></h2>'
            f'<div class="legend-grid">{fight}</div>'
            f'<h2>Your ONLY score — the two ticket piles</h2><div class="legend-grid">{piles}</div>'
            f'<h2>Counters &amp; character markers</h2><div class="legend-grid">{counters}</div>'
            f'<h2>Vendor card — layout key</h2>{vkey}</section>')


def md_to_html(md: str) -> str:
    """Prefer the `markdown` package; fall back to a small converter for our subset."""
    try:
        import markdown as _md
        return _md.markdown(md, extensions=["extra", "sane_lists"])
    except Exception:
        return _fallback_md(md)


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def _fallback_md(md: str) -> str:
    out, i = [], 0
    lines = md.splitlines()
    list_type = None  # 'ul' | 'ol'
    para = []

    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>"); list_type = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para(); close_list(); continue
        h = re.match(r"^(#{1,4})\s+(.*)", line)
        if h:
            flush_para(); close_list()
            lvl = len(h.group(1)); out.append(f"<h{lvl}>{_inline(h.group(2))}</h{lvl}>"); continue
        if line.lstrip().startswith(">"):
            flush_para(); close_list()
            out.append("<blockquote>" + _inline(line.lstrip()[1:].strip()) + "</blockquote>"); continue
        ul = re.match(r"^\s*[-*]\s+(.*)", line)
        ol = re.match(r"^\s*\d+\.\s+(.*)", line)
        if ul or ol:
            flush_para()
            want = "ul" if ul else "ol"
            if list_type != want:
                close_list(); out.append(f"<{want}>"); list_type = want
            out.append("<li>" + _inline((ul or ol).group(1)) + "</li>"); continue
        para.append(line.strip())
    flush_para(); close_list()
    return "\n".join(out)


def css(theme: dict) -> str:
    ink, accent, text, muted = theme["ink"], theme["accent"], theme["text"], theme["muted"]
    tfont, bfont = theme["title_font"], theme["body_font"]
    top, _ = theme["page"]
    return f"""
    @page {{ size: A5; margin: 16mm 15mm 18mm 15mm;
             @bottom-center {{ content: counter(page); color: {muted}; font-family: {bfont}; font-size: 9pt; }} }}
    body {{ font-family: {bfont}; color: {text}; font-size: 10.5pt; line-height: 1.5; }}
    h1 {{ font-family: {tfont}; color: #fff; background: {ink}; padding: 10pt 12pt; border-radius: 6pt;
          font-size: 22pt; margin: 0 0 10pt; border-bottom: 4pt solid {accent}; }}
    h2 {{ font-family: {tfont}; color: {ink}; font-size: 15pt; margin: 16pt 0 4pt;
          border-bottom: 2pt solid {accent}; padding-bottom: 3pt; }}
    h3 {{ font-family: {tfont}; color: {accent}; font-size: 12pt; margin: 12pt 0 2pt; }}
    ul, ol {{ margin: 4pt 0 8pt 16pt; }} li {{ margin: 2pt 0; }}
    strong {{ color: {ink}; }}
    code {{ background: {top}; padding: 1pt 4pt; border-radius: 3pt; font-size: 9.5pt; }}
    blockquote {{ margin: 8pt 0; padding: 6pt 10pt; border-left: 4pt solid {accent};
                  background: {top}; color: {muted}; font-style: italic; }}
    .figbox {{ margin: 10pt 0; }}
    .figbox .figreserve {{ display: flex; flex-direction: column; align-items: center; justify-content: center;
                  gap: 3pt; height: 120pt; border: 2pt dashed {accent}; border-radius: 6pt; background: {top}; }}
    .figbox .figcode {{ font-family: {tfont}; color: {ink}; font-weight: bold; font-size: 11pt; letter-spacing: 1pt; }}
    .figbox .fignote {{ color: {muted}; font-size: 8.5pt; font-style: italic; }}
    .figbox .figimg {{ width: 100%; height: auto; border-radius: 6pt; }}
    .figbox figcaption {{ margin-top: 4pt; padding-left: 8pt; border-left: 3pt solid {accent};
                  color: {muted}; font-size: 9pt; }}
    .figbox figcaption p {{ margin: 0; }}
    """


def main():
    ap = argparse.ArgumentParser(description="Render a rules markdown file to a themed rulebook.")
    ap.add_argument("--md", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path("build/rulebook.pdf"))
    ap.add_argument("--theme", default="clean")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    theme = get_theme(args.theme)
    raw = args.md.read_text(encoding="utf-8")
    body = md_to_html(raw)
    # Reserve image boxes for any [FIG-…] directives (no-op for rulebooks without them, e.g. Beacon).
    body = insert_figure_boxes(body)
    # Inject the drawn-SVG iconography page wherever the {{ICONOGRAPHY}} token appears (as its own last
    # page). Absent → untouched, so rulebooks without the token (e.g. Beacon) are byte-identical.
    if ICON_TOKEN in raw:
        legend = iconography_html(theme)
        body = re.sub(r'<p>\s*' + re.escape(ICON_TOKEN) + r'\s*</p>', legend, body)
        body = body.replace(ICON_TOKEN, legend)
    title = args.title or args.md.stem
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
           f"<style>{css(theme)}</style></head><body>{body}</body></html>")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    html_path = args.out.with_suffix(".html")
    html_path.write_text(doc, encoding="utf-8")
    print(f"[rulebook] wrote {html_path}")
    try:
        from weasyprint import HTML
        HTML(string=doc).write_pdf(str(args.out.with_suffix(".pdf")))
        print(f"[rulebook] wrote {args.out.with_suffix('.pdf')}")
    except Exception as e:
        print(f"[rulebook] PDF skipped ({type(e).__name__}). Open the HTML, or install WeasyPrint: "
              f"pip install weasyprint markdown  (macOS: brew install pango gdk-pixbuf)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
