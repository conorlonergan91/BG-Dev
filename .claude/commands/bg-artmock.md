---
description: Generate an opt-in AI-art MOCKUP (exploration only) from a game's identity.
argument-hint: <game slug> [cover|card|scene] ["Card Name" if card]
---

Generate a high-fidelity **AI-art mockup** to explore a game's visual vibe. Parse `$ARGUMENTS` for the
game slug, an optional subject (`cover` default / `card` / `scene`), and — for `card` — a card name.

Run the manual mockup tool (owned by `bg-theme`):
```
python tools/art/mockup.py --game games/<slug> --subject <cover|card|scene> [--card "<Card Name>"]
```
It builds the prompt straight from `games/<slug>/identity.md` (so it matches the *current* felt
identity) and writes it to `games/<slug>/art/mockups/` (gitignored). To actually render, the human runs
it on their machine with `--backend openai` (needs `OPENAI_API_KEY` + egress); otherwise present the
prompt for them to paste into any image tool.

**Guardrails — state them, don't bypass them:** this is **mockup-only exploration**. The studio stance
is **human-illustrated final art (no AI)**. Mockups stay in `art/mockups/` (gitignored), are labelled
mockups, are never part of `make.sh`, and must **never** be moved into `exports/` or shipped as final
art. If `identity.md` doesn't exist yet, run `bg-theme` first.
