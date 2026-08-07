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
    # 3) Event scope — DRAWN shapes (never the ⦿/⬢/➤ font glyphs)
    scope = "".join([
        _tile(emblem_svg("ring_dot", 42, 34, 24, ink), "⦿ You", "self — only the flipper"),
        _tile(emblem_svg("hex", 42, 34, 24, ink), "⬢ This region", "everyone standing in the drawn region"),
        _tile(emblem_svg("arrow", 42, 34, 24, ink), "➤ Next door", "spills into a neighbouring region"),
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
    # 5) Currencies & scoring
    scoring = "".join([
        _tile(emblem_svg("spark", 42, 34, 24, violet)
              + f'<text x="42" y="44" font-size="22" text-anchor="middle" fill="#fff" font-family="{bfont}" font-weight="bold">讚</text>',
              "Buzz 讚", "the hype you pile on a vendor"),
        _tile(_star_svg(42, 34, 26, gold), "★ Apex / Star", "top prize per region; a Star adds value"),
        _tile(emblem_svg("spark", 42, 34, 24, gold), "Prestige", "a vendor's point value (your score)"),
        _tile(f'<circle cx="42" cy="34" r="26" fill="{teal}" stroke="{ink}" stroke-width="2"/>'
              f'<text x="42" y="44" font-size="26" text-anchor="middle" fill="#fff" font-family="{bfont}" font-weight="bold">譽</text>',
              "Reputation 譽", "your standing — scores by final position"),
    ])
    # 6) The two ticket piles
    piles = "".join([
        _tile(emblem_svg("stamp", 42, 34, 24, gold)
              + f'<text x="42" y="44" font-size="24" text-anchor="middle" fill="{pick_text_color(gold, dark=ink, light="#fff")}" font-family="{bfont}" font-weight="bold">成</text>',
              "成團 · Win pile", "tours that ran: gain printed value"),
        _tile(emblem_svg("stamp", 42, 34, 24, taupe)
              + f'<text x="42" y="44" font-size="24" text-anchor="middle" fill="#fff" font-family="{bfont}" font-weight="bold">遺</text>',
              "遺珠 · Lose pile", "got away: lose half the value"),
    ])

    # 7) Vendor card — layout key (a labelled schematic mirroring build_cards' vendor template)
    north = col("north", "#D64545")
    vkey = f'''<svg viewBox="0 0 620 300" class="vkey">
      <rect x="8" y="8" width="220" height="284" rx="16" fill="#fff" stroke="{ink}" stroke-width="3"/>
      <path d="M8 24 a16 16 0 0 1 16 -16 h188 a16 16 0 0 1 16 16 v40 h-220 z" fill="{north}"/>
      <text x="24" y="40" font-size="18" fill="#fff" font-family="{bfont}" font-weight="bold">肉包 · Bao</text>
      <rect x="150" y="14" width="66" height="26" rx="13" fill="#fff" opacity="0.9"/>
      <text x="183" y="33" font-size="14" fill="{north}" text-anchor="middle" font-family="{bfont}" font-weight="bold">攤</text>
      <text x="24" y="92" font-size="15" fill="{theme['accent']}" font-family="{bfont}" font-weight="bold">PAY 付</text>
      {emblem_svg("hex", 44, 118, 16, north, stroke=ink)}<text x="44" y="124" font-size="16" fill="#fff" text-anchor="middle" font-family="{bfont}" font-weight="bold">豬</text>
      <circle cx="96" cy="118" r="16" fill="{violet}" stroke="{ink}" stroke-width="2"/><text x="96" y="124" font-size="15" fill="#fff" text-anchor="middle" font-family="{bfont}" font-weight="bold">2</text>
      <text x="24" y="164" font-size="15" fill="{theme['accent']}" font-family="{bfont}" font-weight="bold">GAIN 得</text>
      {_star_svg(40, 190, 15, gold)}<text x="64" y="196" font-size="20" fill="{gold}" font-family="{bfont}" font-weight="bold">2</text>
      <circle cx="120" cy="190" r="15" fill="{teal}" stroke="{ink}" stroke-width="2"/><text x="120" y="196" font-size="14" fill="#fff" text-anchor="middle" font-family="{bfont}" font-weight="bold">+1</text>
      <rect x="24" y="212" width="180" height="42" rx="8" fill="none" stroke="{gold}" stroke-width="2"/>
      <text x="34" y="238" font-size="13" fill="{ink}" font-family="{bfont}">PERK 技 — special effect</text>
      <rect x="30" y="266" width="176" height="18" rx="9" fill="{day['tag_fill']}"/>
      <text x="118" y="280" font-size="12" fill="{day['tag_ink']}" text-anchor="middle" font-family="{bfont}" font-weight="bold">日 DAY 早</text>
      <g font-family="{bfont}" font-size="15" fill="{ink}">
        <text x="250" y="34">① <tspan font-weight="bold">Header band</tspan> = region colour + emblem + dish name</text>
        <text x="250" y="70">② <tspan font-weight="bold">PAY 付</tspan> = ingredient chips (shape+繁體) + Buzz needed</text>
        <text x="250" y="106">③ <tspan font-weight="bold">GAIN 得</tspan> = Prestige (★) + Reputation (譽) + perk</text>
        <text x="250" y="142">④ <tspan font-weight="bold">PERK 技</tspan> = the vendor's special bonus</text>
        <text x="250" y="178">⑤ <tspan font-weight="bold">Phase ribbon</tspan> = day 日 / night 夜 (which layer)</text>
        <text x="250" y="214">Top-right pill = venue tier (攤 stall · 小吃 · 名店)</text>
        <text x="250" y="250">★ printed = an apex / Star vendor (top prize)</text>
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
            f'<h2>Currencies &amp; scoring</h2><div class="legend-grid">{scoring}</div>'
            f'<h2>The two ticket piles</h2><div class="legend-grid">{piles}</div>'
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
