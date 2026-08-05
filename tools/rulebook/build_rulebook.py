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
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cards"))
from themes import get_theme  # noqa: E402


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
    body = md_to_html(args.md.read_text(encoding="utf-8"))
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
