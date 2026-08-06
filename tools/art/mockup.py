#!/usr/bin/env python3
"""
mockup.py — build an AI-art *mockup* prompt from a game's identity, and (optionally) render it.

⚠️ MOCKUP-ONLY. The studio's stance is **human-illustrated final art, no AI** (see
`knowledge/designer-profile.md` and each game's `identity.md`). This tool is a MANUAL, opt-in way to
see a high-fidelity *vibe mockup* — it is NOT part of the build pipeline (`make.sh` never calls it),
its output lands in `games/<slug>/art/mockups/` (gitignored), and every file is labelled a mockup.
Never promote a mockup into `exports/` or ship it as final art.

It reads `identity.md` (the bg-theme source of truth) so the prompt reflects the *current* felt
identity — north star, tone, palette, look & feel.

Usage:
    # default: derive + write the prompt(s); paste into any image tool you like
    python tools/art/mockup.py --game games/beacon --subject cover
    python tools/art/mockup.py --game games/beacon --subject card --card "Blinding Flare"

    # optional: actually render via an image API on YOUR machine (needs a key + network egress)
    OPENAI_API_KEY=... python tools/art/mockup.py --game games/beacon --subject cover --backend openai

Subjects: cover | card | scene.  Backends: prompt (default) | openai.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
from pathlib import Path

BANNER = ("AI MOCKUP — exploration only. Studio stance: final art is HUMAN-ILLUSTRATED (no AI). "
          "Do not ship or move into exports/.")


def sections(md: str) -> dict:
    out, key, buf = {}, "_pre", []
    for line in md.splitlines():
        h = re.match(r"^#{1,6}\s+(.*)", line)
        if h:
            out[key.strip().lower()] = "\n".join(buf).strip()
            key, buf = h.group(1), []
        else:
            buf.append(line)
    out[key.strip().lower()] = "\n".join(buf).strip()
    return out


def _find(secs: dict, *needles: str) -> str:
    for k, v in secs.items():
        if any(n in k for n in needles):
            return v
    return ""


def _clean(text: str, limit: int = 400) -> str:
    text = re.sub(r"[*_`>#\-]", " ", text)           # strip md
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def build_prompt(identity_md: str, subject: str, card: str | None) -> dict:
    s = sections(identity_md)
    north = _clean(_find(s, "north star"), 300)
    tone = _clean(_find(s, "tone & vibe", "tone"), 200)
    concept = _clean(_find(s, "concept"), 250)
    look = _clean(_find(s, "look & feel", "look &"), 400)
    palette_m = re.search(r"palette[^:]*:\s*(.+)", look, re.I) or re.search(r"palette[^:]*:\s*(.+)", identity_md, re.I)
    palette = "as described in identity.md"
    if palette_m:
        # first sentence only (keeps the colour parentheticals, drops trailing "(Render ...)" notes)
        p = re.split(r"\.\s", palette_m.group(1))[0]
        palette = _clean(p, 160)

    framing = {
        "cover": "board-game box-cover composition, room for a title at the top, iconic and inviting",
        "card": f"single card illustration for '{card or 'a card'}', centred subject, space for a title bar and value",
        "scene": "an atmospheric key-art scene establishing the world",
    }[subject]

    positive = (f"{framing}. Illustration (painterly / storybook, not photorealistic). "
                f"Subject & mood: {north or concept}. Tone: {tone}. "
                f"Palette: {palette}. Cohesive, warm, readable at a glance. No lettering, no watermark.")
    negative = ("photorealistic, 3D render, dark/horror, grim, gory, zany/cartoonish-slapstick, garish "
                "neon, cluttered, low-contrast, text/letters/watermark/signature, extra fingers, UI frames")
    return {"subject": subject, "positive": positive, "negative": negative,
            "identity_north_star": north, "palette": palette}


def render_openai(prompt: dict, out_png: Path, size: str = "1024x1536") -> bool:
    import urllib.request
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("[mockup] --backend openai needs OPENAI_API_KEY. Wrote the prompt instead."); return False
    body = json.dumps({"model": "gpt-image-1", "prompt": prompt["positive"] + " Avoid: " + prompt["negative"],
                       "size": size, "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
        b64 = data["data"][0]["b64_json"]
        out_png.write_bytes(base64.b64decode(b64))
        print(f"[mockup] rendered {out_png}")
        return True
    except Exception as e:
        print(f"[mockup] image API call failed ({type(e).__name__}: {e}). Prompt was still written; "
              "run it in your own image tool, or check your key/egress.")
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Build (and optionally render) an AI-art mockup from identity.md.")
    ap.add_argument("--game", required=True, type=Path)
    ap.add_argument("--subject", default="cover", choices=["cover", "card", "scene"])
    ap.add_argument("--card", default=None, help="card name when --subject card")
    ap.add_argument("--backend", default="prompt", choices=["prompt", "openai"])
    ap.add_argument("--size", default="1024x1536")
    args = ap.parse_args()

    identity = args.game / "identity.md"
    if not identity.exists():
        print(f"No identity.md in {args.game} — run bg-theme first."); return 1
    prompt = build_prompt(identity.read_text(encoding="utf-8"), args.subject, args.card)

    out_dir = args.game / "art" / "mockups"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{args.subject}" + (f"-{re.sub(r'[^a-z0-9]+','-',(args.card or '').lower()).strip('-')}" if args.card else "")
    (out_dir / f"{stem}-prompt.txt").write_text(
        f"# {BANNER}\n\nPOSITIVE:\n{prompt['positive']}\n\nNEGATIVE:\n{prompt['negative']}\n", encoding="utf-8")
    print(f"# {BANNER}\n")
    print(f"[mockup] prompt → {out_dir / f'{stem}-prompt.txt'}\n")
    print("POSITIVE:\n" + prompt["positive"] + "\n\nNEGATIVE:\n" + prompt["negative"] + "\n")

    if args.backend == "openai":
        render_openai(prompt, out_dir / f"{stem}-mockup.png", args.size)
    else:
        print("[mockup] Paste the prompt into your image tool of choice, or re-run with "
              "--backend openai (needs OPENAI_API_KEY + egress). Mockups stay in art/mockups/ (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
