# Manufacturing & Fulfillment

Turning a finished design into a **well-made physical object and getting it into hands** — the cluster the
studio's prototype-first, Screentop-first house style **legitimately defers** until a specific game commits
to a physical run (a crowdfunder or a self-published POD/retail push). If the game is **licensed to a
publisher, this whole file is the publisher's job** — you keep the sell sheet and the prototype. Owned by
**`bg-production`**; costs the design against this belong to `bg-funding` + `cost-and-manufacturability.md`;
print specs are in `manufacturing-specs.md`. *(2025–2026 figures move fast — re-verify live.)*

## When to switch this on
- **Licensing/pitch** → skip; the publisher manufactures and fulfils. (Most likely path for this studio.)
- **POD** → light: the platform manufactures/ships; you just prep good print files + order proofs.
- **Self-run crowdfunding / self-publish** → the full file applies. This is where the risk lives.

## The disciplines (each a real role a publisher has staff for)
- **Production management** — factory selection, quotes, a **pre-production copy** (order one, check it in
  hand before the run), and **QC** on the run (punchboard alignment, warping, colour fidelity, miscuts,
  missing components — a single missing token per box is a mass-refund event).
- **Component engineering** — die-lines, **insert/tray** design (does everything repack; sleeved-card
  clearance), **box** structure, material choices, packing tolerance. Assembly cost scales with component
  *type* count (cross-ref `cost-and-manufacturability.md`).
- **Sourcing / procurement** — **OEM vs ODM**, minimum order quantities (**OEM often needs ~3,000 units**
  but ~15–20% cheaper per unit), and where to print. The wrong MOQ ruins small-run economics.
- **Sustainability** (a rising 2025–2026 buyer/retailer expectation, a deliberate trade — recycled stock
  costs ~10–30% more) — FSC/recycled paper, plastic reduction (paper trays/shrink), soy inks, **right-sized
  boxes** (air = wasted freight).
- **Freight / import / customs / tariffs** — ocean/air freight, duties, and the **volatile 2026 tariff
  environment** (China-made games have swung through 30–54%+; a $25 game can land like $40). **Whoever
  imports inventory bears it.** Mitigations: **manufacture-and-fulfil** partners, **regional (EU/UK) hubs**
  (the designer is IE/EU-based — fulfilling in Europe sidesteps the worst US–China crossfire for EU
  backers), and pricing a buffer.
- **Fulfillment / 3PL** — warehousing, kitting, pick-pack-ship, returns. The last mile of crowdfunding;
  bad fulfilment (damaged, late, wrong SKUs) becomes the customer's whole memory of the game. Firms handle
  freight-in → warehouse → global ship.
- **Pledge-manager operations** — post-campaign: lock addresses, tiers, add-ons, VAT (BackerKit/Gamefound/
  PledgeBox), then feed clean data to the 3PL. Errors here = missing/duplicate shipments at scale.

## Localization readiness (light, but design for it early)
The studio is English-first (IE/UK/US), but reach and pitchability improve when the game is
**low-text and icon-driven** — text expansion breaks layouts and mistranslated rules cause returns, so
**language-independent iconography** (owned by `bg-infodesign`) is the cheap insurance. Note text-heavy
components early as a localisation/cost risk; a publisher who licenses will value a low-text design.

## The pre-flight gate (before any print run)
Run `python tools/preflight/check_print.py --game games/<slug>` on the print specs before committing to a
manufacturer: **bleed (≥3 mm), safe margin (≥3 mm), 300 DPI, CMYK intent, standard card size (63×88 mm),
min body-text legibility.** Deterministic checks that catch the expensive, permanent mistakes (RGB→CMYK
shift, clipped art, unreadable text) at the file stage, not the proof stage. See `manufacturing-specs.md`.

Cross-refs: `cost-and-manufacturability.md` (design for cheap), `funding-and-route-to-market.md` (which
route bears which cost), `manufacturing-specs.md` (print specs), `publishing-ip.md` (safety compliance:
CE/UKCA, EN 71, ASTM F963/CPSIA, choking warnings, barcodes).
