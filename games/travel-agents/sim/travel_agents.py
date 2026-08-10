"""
travel_agents.py — Travel Agents: Taiwan · V7-M (Follower MEEPLES + VENDOR SCARCITY)
Encoded for the simulation harness (tools/sim/engine.py). Stdlib-only.

==================================================================================================
V7-M RE-ENCODE (2026-08-09) — spec: design/followers-meeples-redesign.md (LOCKED, CD-SIGNED)
==================================================================================================
The meeple + vendor-scarcity + six-lanes model is LOCKED and the component DATA is built. This module
re-encodes the STALE V7 sim (which modelled the retired dial / Followers-max / buzz_cost / dial-drop
economy) to the new model. The component CSVs + map.json are the SOURCE OF TRUTH and are LOADED here
(vendors, bookings, characters, per-count slot + booking-deck tables), so the sim can never drift from
the built data.

WHAT CHANGED FROM THE OLD SIM (the whole economy):
  * FOLLOWERS = a finite PER-PLAYER meeple pool of size `max` (field 6, Influencer 8). A follower is only
    ever in your SUPPLY (un-rallied), on YOUR BOARD (rallied), or ON A STALL (committed). Invariant:
    supply + board + Σ(committed) == max, always (component count enforces the old ceiling physically).
      - TRAVEL grows your following: take 1 from supply → your board (+ Trending win / Rave-Review / "+1"
        events each grow 1). The Homebody's grow-tick is switchable OFF (reserve g′).
      - PROMOTE places up to 2 from your board onto stall(s) you stand with — MAY SPREAD across two
        co-located face-up stalls.
      - WIN a contested stall → your committed followers come home to YOUR BOARD (kept, redeploy free).
      - LOSE a contested stall → your committed followers go back to YOUR OWN SUPPLY (re-rally them).
    The dial, the Followers-max number, the shared central supply, buzz_cost, and the day/night dial-drop
    are ALL DELETED.
  * CONTEST = pure most-followers PLURALITY. A tie BLOCKS (no claim). Big Brother 大哥 wins by a MARGIN
    dial N (baseline 1 = wins ties). BASELINE DUSK / LAST-TRAIN tie-resolver (most-followers → earliest
    committer) force-clears any still-tied contested stall at each phase boundary.
  * VENDOR SCARCITY: SLOW refill (a claimed/cleared slot stays EMPTY; refill ALL empty slots from the
    region decks at the END of each round) + the tighter per-count face-up counts (3p 4 / 4p 5 / 5p 5 /
    6p 6, floor 1/region). Vendor cost = ingredients only.
  * SIX LANES / kits: home-gated favours-draw Councillor, deep-pool Influencer, Homebody Travel-draw-2,
    Big Eater greedy-4th-returns-1-follower + hazard×2, Globetrotter Travel-anywhere-costs-1-follower +
    HSR-immune, Big Brother margin dial. Prestige Bookings target total ingredient_cost (day≥4 /
    total≥9 / g≥7).
  * SOURCING moved to an EXPLICIT DECK-FLOW (§16, folded in 2026-08): region MARKET decks are now REAL
    card lists (ingredients.csv fixed depths + a per-count slice of events.csv via map.event_deck_mix),
    recycling through a per-region face-up discard with reshuffle-on-empty. Sourcing shares are NO LONGER
    expected invariant (§12 amends this) — they track the NEW multi-ingredient demand vector; probe #2 is
    retargeted (§12.5).

FOLDED IN 2026-08 (on top of the LOCKED meeple+scarcity baseline — specs §12/§14/§15/§16, all CD-locked):
  * §12.2 MIN-FOLLOWER CLAIM GATE — a contested stall claims only if the plurality/margin leader ALSO
    holds ≥ the vendor's tier-scaled `min_followers` (1/2/3, read from vendors.csv); below-floor → no
    claim. At DUSK/LAST TRAIN a below-floor top crowd clears UNCLAIMED (§12.3 interaction 2).
  * §12.1 MULTI-INGREDIENT COSTS — `recipe`/`ingredient_cost` (avg 2.71, range 2–5) read from the CSV;
    the stale `expensive = cost>=3` predicate is fixed to `>=4` (§13.1/§14.3).
  * §14 VP TWO-TRACK SCORING — final score = completed-Booking VP + won-vendor `vp` (both from CSV). The
    vendor-only HOARDER probe + vendor-VP-share / claims-per-player / apex-per-player instruments verify
    "vendor-only loses / tours dominate."
  * §15 EVENT SYSTEM — events.csv modelled as VERB · SCOPE · DURATION: the 12 verbs wired to the real
    subsystems (RALLY/DISPERSE↔follower pool, GIFT/PINCH/SPOIL/SWIPE/SINK↔Larder/deck, TREND/RESTOCK/WASH↔
    vendor board, BLOCK/DETOUR↔action/travel), the 5 scopes (self/✦rival/⬢region/➤neighbour/▦board) with
    the CD tied-leader refinement (a ✦ loss hits all tied leaders EXCLUDING the drawer; fizzles if the
    drawer is the sole top), and ⏳ persistence (turn/round). Dealt per event_deck_mix.
  * §16 DISCARD/RESHUFFLE LOOP — four discard feeders + reshuffle-on-empty per region+phase; phase-to-box
    (day decks+discards → box at dusk; a carried concluded-phase Larder card spent in night → box) with a
    reshuffle-phase-purity ASSERTION (a night reshuffle contains only night cards). Metrics: cycle-rate,
    reshuffled-deck size, live-deck event-fraction, Pantry supply_min.

BOTS ARE SPREAD-AWARE (the critic's key point): the planner's follower-fight logic reads the true
`needed-to-win` accounting for co-located Big-Brother rivals (a rival BB needs +N to be beaten) and for
the bot itself being BB (it need only match at N=1), and can SPREAD a Promote across two co-located
stalls. A spread-naive bot under-credits Big Brother and mis-reads the contest. Probe bots wire the §9
lines: Homebody "ignore-the-contest" and "banked-board late-battler", plus per-lane fingerprints and the
Big-Brother edge-fire / Globetrotter snipe trackers in metrics().

BOTS ARE A FLOOR ON DEPTH, NOT A CEILING — they catch degenerate lines + gross imbalance; the fun /
denial-feel / "did the scrum materialise" is the human 6p judge's job (critic rec B: sim FIRST, then table).

Run:
    python games/travel-agents/sim/travel_agents.py --smoke            # tiny import+run smoke test
    python games/travel-agents/sim/travel_agents.py --resim [N] --out playtests/sim-results.md
        # the CD-GATED ~50-min per-count 3-6 re-sim (§9). DO NOT run without the CD's explicit "go".
"""
from __future__ import annotations

import csv
import json
import os
import random
import statistics
import sys
from collections import Counter, deque

# ==================================================================================================
#  SWITCHABLE RESERVES / DIALS (env vars — the §9 knobs; do NOT alter the printed rules by editing here)
# ==================================================================================================
FIELD_MAX      = int(os.environ.get("TA_MAX", "6"))            # field Follower pool max (reserve e: 5/6/7)
INFL_MAX       = int(os.environ.get("TA_INFL_MAX", "8"))       # 網紅 deep pool (reserve c: 7/8)
START_MEEPLES  = int(os.environ.get("TA_START", "2"))          # followers starting on your board
DAGE_N         = int(os.environ.get("TA_DAGE_N", "1"))         # 大哥 margin dial N (0 / 1 / 2=ceiling-only)
AMA_TRAVEL_COST = os.environ.get("TA_AMA_TRAVEL_COST", "1") == "1"  # 阿嬤 Travel-anywhere costs 1 follower (baseline ON)
HOMEBODY_GROW  = os.environ.get("TA_HOMEBODY_GROW", "1") == "1"     # 媽寶 grow-tick ON (reserve g′ = OFF for him)
HOMEBODY_DRAW  = int(os.environ.get("TA_HOMEBODY_DRAW", "2"))  # 媽寶 forage draw (reserve g: 2/1, wrong axis)
BIGEATER_COST  = int(os.environ.get("TA_BIGEATER_COST", "1"))  # 大胃王 greedy-4th sink (reserve h: 1/2)
TIE_RESOLVER   = os.environ.get("TA_TIE_RESOLVER", "1") == "1"  # baseline DUSK/LAST-TRAIN resolver ON (§2.6)
SLOW_REFILL    = os.environ.get("TA_SLOW_REFILL", "1") == "1"   # scarcity: slow per-round refill (A/B: OFF=immediate)
APEX_NOREFILL  = os.environ.get("TA_APEX_NOREFILL", "0") == "1" # reserve d: tier-3 apex stalls never refill
SLOTS_OVERRIDE = os.environ.get("TA_SLOTS", "")               # e.g. "1,1,1,1" (order N,C,S,E) — tighter/looser
LARDER_CAP     = int(os.environ.get("TA_LARDER_CAP", "7"))    # hand-limit on carried ingredients (阿嬤 f-alt: 6)
AMA_LARDER_CAP = int(os.environ.get("TA_AMA_LARDER_CAP", str(LARDER_CAP)))
HAND_LIMIT     = int(os.environ.get("TA_HAND_LIMIT", "3"))    # in-progress Bookings held at once

# --- sourcing / event model (V7-M+ EXPLICIT DECK-FLOW — §15 events, §16 discard/reshuffle) --------
# The old abstract-Counter sourcing pool (SIG/K/VEG_SUPPLY + a random event-fraction) is RETIRED. Region
# MARKET decks are now REAL card lists built from ingredients.csv (fixed depths) + a per-count slice of
# events.csv dealt via map.json.event_deck_mix (§15.4). Cards recycle through a per-region face-up discard
# and reshuffle on deck-out (§16); a concluded-phase card leaving a Larder goes to the BOX, never a
# current-phase discard (the phase-to-box guarantee the night-reshuffle assertion checks).
EVENT_SCALE   = float(os.environ.get("TA_EVENT_SCALE", "1.0"))   # switchable event-density multiplier (§15.7 knob)
EVENTS_OFF    = os.environ.get("TA_EVENTS_OFF", "0") == "1"       # deal ZERO events (A/B: event contribution delta)
STALL_CAP  = int(os.environ.get("TA_STALL_CAP", "60"))       # ultimate net (vendor clock is guaranteed to fire)

# --- §17 VENDOR-DEPLETION CLOCK + CLOSING-TIME DIE (2026-08-10, this re-model) ---------------------
# The clock is now the finite VENDOR pools (day 13 / night 11); a phase ends when its pool empties. The
# Closing-Time die (the game's FIRST randomness) is the forcing function that thins the board when claims
# stall. These knobs drive the re-smoke (L is the #1 pacing knob); the die is SEEDABLE for reproducibility.
TRACK_L_OVERRIDE = int(os.environ.get("TA_TRACK_L", "0"))    # 0 = per-count track_length from map.json; else force L
DIE_SEED_OVERRIDE = os.environ.get("TA_DIE_SEED", "")        # fixed die seed (all games) for exact replay
DIE_FORCE  = os.environ.get("TA_DIE_FORCE", "")              # force EVERY roll to this face (test hook: "BLANK"/"N"…)

# --- §17.6 PER-COUNT VENDOR-POOL SUBSET (2026-08-10, this tuning sweep) ----------------------------
# The CD structural fix: scale the phase pool (deck) IN LINE with player count. The 24 unique dishes
# (13 day / 11 night) are the SOURCE OF TRUTH; this lever models playing only a SUBSET of them in a given
# game — draw N-of-13 day / M-of-11 night — so a low-count game drains a SMALLER pool (doesn't run long on
# an oversized fixed pool) and a high-count game a bigger one. SUBSET (some dishes sit out; every dish stays
# unique) is preferred over duplication. Per-region SLOT-FLOORS are always kept so no region starts starved.
#   TA_POOL="" (default)   → full pool (13 day / 11 night) — the current fixed behaviour.
#   TA_POOL="D,M"          → D-of-13 day + M-of-11 night this game (subset if < full; DUPES if > full,
#                            see _phase_decks — dupes are FLAGGED, not the recommendation).
POOL_OVERRIDE = os.environ.get("TA_POOL", "")               # "" = full 13/11; "D,M" = subset (or dupe) sizes

# --- §18 VISIT_MODE toggle (the A/B the re-sim isolates) ------------------------------------------
# "straight" = Option A (BASELINE, §18.2/§18.6): draw straight to your keep-count, events fire+discard
#   and DO NOT count (§16.2 feeder-1 "passed-over card" is eliminated). "keep2" = status-quo control
#   (§18.4 cell 2): flip 3, fire events, keep up to the cap, discard the rest. A clean switch — no rule
#   is edited to pick one; both are faithful models and bg-playtest A/Bs them in one run.
VISIT_MODE    = os.environ.get("TA_VISIT_MODE", "straight")      # "straight" (A, baseline) | "keep2" (control)

# --- §15.9 the two cancelled-tour BOONS (CLEAR + SALVAGE) -----------------------------------------
# ⚠ DATA GAP (flag to bg-developer): §15.8 scheduled the verb count 13 → 15 IN DATA, but events.csv still
# holds only the 13 pre-boon verbs — the CLEAR (central-night, 1 copy) and SALVAGE (south-night, 1 copy)
# cards spec'd in §15.9 were never transcribed. So the SALVAGE-swing / catch-up probes the readiness
# charter requires cannot run off the CSV. Rather than edit component data (not this lane), the sim
# INJECTS the two §15.9-spec'd cards synthetically into the night C/S pools (see _inject_tours_boons),
# guarded by this flag so it is auditable + switchable. When bg-developer adds them to events.csv, set
# this OFF and they load from the CSV like every other event.
# §17 re-model: the real CLEAR (t_clear) + SALVAGE (t_salvage) rows now EXIST in events.csv, so the
# synthetic injection is RETIRED (default OFF) — they load from the CSV like every other event and are
# routed by VERB in _fire_event (the CSV's `rival` scope on salvage is ignored; verb dispatch wins).
TOURS_BOONS   = os.environ.get("TA_TOURS_BOONS", "0") == "1"    # LEGACY synthetic inject (now default OFF)
NUDGE_CAP     = int(os.environ.get("TA_NUDGE_CAP", "1"))        # §15.5 rail 6: max ✦ leader-hazard hits / leader / round

# --- CD PLAYTEST LEVER: CANCELLED-TOUR COST (2026-08-10, spec/sim-only A/B — NOT the shipped rule) ---
# A Cancelled tour's scoring penalty. BASELINE "half_value" = −⌊V/2⌋ (scales with the tour's ambition, so
# it punishes exactly the big tours the two-track intent wants people to book). The CD A/B is a gentler,
# predictable FLAT cost — "flat:N" charges a fixed −N per cancelled ticket regardless of V — lowering the
# risk of booking ambitious tours (the scoring-side companion to agnostic-tours safety). Sweep N∈{1,2}.
CANCEL_COST   = os.environ.get("TA_CANCEL_COST", "half_value")  # "half_value" (baseline) | "flat:1" | "flat:2"


def _cancel_cost():
    """Live-read of the CANCEL_COST lever (so a driver can sweep configs in one process)."""
    return os.environ.get("TA_CANCEL_COST", "half_value")


def _cancel_pen_one(v):
    """Penalty for ONE cancelled tour of value V under the active CANCEL_COST lever."""
    cc = _cancel_cost()
    if cc.startswith("flat:"):
        return int(cc.split(":", 1)[1])
    return v // 2                                               # baseline: −⌊V/2⌋


# ==================================================================================================
#  §20 + §21 LEVERS (SPEC-ONLY MODELS — live-read from env so a driver sweeps configs in one process).
#  These model the §21 wild booking + the 3p `counts`-tag helper and the recommended per-count scaling
#  from the 1c22551 sweep. NONE of these edit a shipped rule or the component CSVs — they are switchable
#  sim levers, exactly as bg-playstrat is meant to model spec proposals before the data build.
# ==================================================================================================
def _wild_book_on():
    """§21.1 WILD BOOKING modelled ON. A Book variant: decline the face-up row, draw the top of the deck
    blind, keep it (whiff → Cancel later at the flat cancel). Default ON for this validation."""
    return os.environ.get("TA_WILD_BOOK", "1") == "1"


def _counts_tag_on():
    """§21.5 the per-count `counts` tag filter (HEAVY out at 3p; ON-RAMP always in at 3p). Default ON."""
    return os.environ.get("TA_COUNTS_TAG", "1") == "1"


def _onramp_high_in():
    """§21.5 the `onramp_high_count` switch. IN (default) = the validated 45-tour deck at 4–6p (no
    regression); OUT = drop the 8 on-ramp tours at 4–6p (the meatier variant). Always IN at 3p."""
    return os.environ.get("TA_ONRAMP_HIGH", "IN").upper() != "OUT"


def _reserve_3pa():
    """§21.8 reserve 3p-a: +1 face-up Booking slot at 3p (pure tour-supply widening). Held OFF."""
    return os.environ.get("TA_RESERVE_3PA", "0") == "1"


def _reserve_3pb():
    """§21.8 reserve 3p-b: also demote the 3-claim coverage tours (d_travel3/g_travel3d/n_deep3) out of 3p."""
    return os.environ.get("TA_RESERVE_3PB", "0") == "1"


def _scaling_recommended():
    """Use the reconstructed 1c22551 recommended per-count scaling table (REC_SLOTS/REC_POOL/REC_TRACK).
    A global TA_SLOTS / TA_POOL / TA_TRACK_L env override still wins over the table where set."""
    return os.environ.get("TA_SCALING", "").lower() == "recommended"


# §21.5 tour groups. HEAVY_TOURS / ONRAMP_TOURS are now DERIVED FROM THE CSV `counts:`/`onramp` tags
# after BOOKINGS loads (see just below _load_bookings) — these are placeholders overwritten at load so
# the sim tracks the built data, never a hand-maintained id list. RESERVE_3PB_TOURS stays an explicit
# reserve set (a held-off sim lever, not a shipped tag).
HEAVY_TOURS = set()
ONRAMP_TOURS = set()
RESERVE_3PB_TOURS = {"d_travel3", "g_travel3d", "n_deep3"}

# Recommended per-count scaling from the 1c22551 sweep (thematic slots: base N1C1S1E1 → South +1 @5p →
# North +1 @6p, East kept thinnest; light SUBSET of the 24 unique dishes, 6p≈12/10; gentle die L=3;
# flat:1 cancel). REC_POOL is CALIBRATED here against the sweep's documented 4–6p health (hoarder ≤ fair,
# pace ~40–45 tpp) — the driver may nudge REC_POOL[3] to land 3p pace in the accepted ~40–48 band.
REC_SLOTS = {3: (1, 1, 1, 1), 4: (1, 1, 1, 1), 5: (1, 1, 2, 1), 6: (2, 1, 2, 1)}
REC_POOL = {3: (9, 7), 4: (10, 8), 5: (11, 9), 6: (12, 10)}
REC_TRACK = {3: 3, 4: 3, 5: 3, 6: 3}


def _counts_filter(keys, n):
    """§21.5 build a per-count tour pool from the `counts` groups. 3p drops the 7 HEAVY (4+-claim) tours
    (and the 3 reserve-3p-b tours if that reserve is on); 4–6p drop the 8 ON-RAMP tours only when the
    onramp switch is OUT. Everything else (CORE) is always in. A pure setup filter (no in-play rule)."""
    if not _counts_tag_on():
        return list(keys)
    heavy = set(HEAVY_TOURS)
    if n == 3 and _reserve_3pb():
        heavy |= RESERVE_3PB_TOURS
    out = []
    for k in keys:
        if n == 3:
            if k in heavy:
                continue                       # HEAVY (+reserve-b) unreachable at a ~7-claim 3p budget
        else:
            if (not _onramp_high_in()) and k in ONRAMP_TOURS:
                continue                       # 4–6p OUT variant: the meatier deck
        out.append(k)
    return out

# ==================================================================================================
#  DATA LOADING — the built component CSV/JSON are the SOURCE OF TRUTH
# ==================================================================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_COMP = os.path.abspath(os.path.join(_HERE, "..", "components"))

# canonical map: region letter -> signature ingredient TYPE, and the two commons and their source-regions
SIG_TYPE = {"N": "meat", "C": "tea", "S": "seafood", "E": "pantry"}
TYPE_SIG_REGION = {v: k for k, v in SIG_TYPE.items()}         # meat->N, tea->C, ...
COMMONS = {"sugar": {"C", "S"}, "veg": {"N", "E"}}            # common type -> regions it is sourceable in
COMMON_HOME = {"sugar": "C", "veg": "N"}                      # deterministic region a returned common goes to
REGIONS = ("N", "C", "S", "E")
RING = {"N": ["C", "E"], "C": ["N", "S"], "S": ["C", "E"], "E": ["S", "N"]}
HSR = ("N", "S")
REGION_KEY = {"north": "N", "central": "C", "south": "S", "east": "E"}


def _load_map():
    with open(os.path.join(_COMP, "map.json"), encoding="utf-8") as f:
        return json.load(f)


MAP = _load_map()


def _is_common(t):
    return t in COMMONS


def _load_vendors():
    """Load vendors.csv → the vendor table. recipe (a ';'-list of ingredient TYPES) is the cost; the
    `draw` and `buzz_cost` columns are RETIRED (dropped from the data). icon = region letter | ''."""
    out = []
    with open(os.path.join(_COMP, "vendors.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            recipe = [t.strip() for t in row["recipe"].split(";") if t.strip()]
            cost = Counter(recipe)
            region = row["region"].strip()
            tier = int(row["tier"])
            tags = set(row.get("tags", "").split(";"))
            is_drink = "drink" in tags
            sig_regions = {TYPE_SIG_REGION[t] for t in cost if not _is_common(t)}
            out.append({
                "id": len(out), "vid": row["id"], "region": region, "tier": tier,
                "phase": 1 if row["phase"].strip() == "day" else 2,
                "is_drink": is_drink,
                "cost": cost, "total_cost": int(row["ingredient_cost"]),
                # §12.2 min-follower FLOOR (tier-scaled 1/2/3) + §14 vendor VP — read from the CSV, never hardcoded
                "floor": int(row["min_followers"]),
                "vp": int(row["vp"]),
                "icon": row["icon"].strip() or None,
                "trending": row.get("trending", "").strip() == "yes",
                "apex": tier >= 3,
                "cross": len(sig_regions) >= 2,   # a cross-region (→X) dish spans >1 signature region
                # §21 tour targets `locale:<place>` / `dishtype:<kind>` match against these grouping columns
                # (read from the CSV — never hardcoded; a street-crawl / dish-type tour reads exactly them).
                "locale": row.get("locale", "").strip(),
                "dish_type": row.get("dish_type", "").strip(),
            })
    return out


VENDORS = _load_vendors()
VID_BY_KEY = {v["vid"]: v["id"] for v in VENDORS}


def _region_deck(region, phase):
    return [v["id"] for v in VENDORS if v["region"] == region and v["phase"] == phase]


# --------------------------------------------------------------------------------------------------
#  EVENTS (§15) — load events.csv into the framework model: VERB · SCOPE · DURATION. The card's `verb`
#  is the machine-readable hook; effects are wired to the MEEPLE / Larder / vendor / board subsystems.
#  EVENT_POOL[(region, phase)] is the POOL (quantity-expanded); the per-count event_deck_mix deals a
#  slice into each region+phase market deck at setup / at dusk (§15.4).
# --------------------------------------------------------------------------------------------------
def _load_events():
    out = []
    pool = {(r, ph): [] for r in REGIONS for ph in (1, 2)}
    with open(os.path.join(_COMP, "events.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            r = row["region"].strip()
            ph = 1 if row["phase"].strip() == "day" else 2
            tags = row.get("tags", "")
            kind = "hazard" if "hazard" in tags else ("boon" if "boon" in tags else "neutral")
            ev = {
                "idx": len(out), "id": row["id"], "region": r, "phase": ph,
                "scope": row["scope"].strip(),        # self | rival | region | neighbour | board
                "duration": row["duration"].strip(),  # now | turn | round | phase
                "verb": row["verb"].strip(),
                "target": row.get("target", "").strip(),
                "value": int(row["value"]) if row.get("value", "").strip() else 1,
                "qty": int(row["quantity"]) if row.get("quantity", "").strip() else 1,
                "kind": kind,
            }
            out.append(ev)
            if (r, ph) in pool:
                pool[(r, ph)].extend([ev["idx"]] * ev["qty"])
    return out, pool


EVENTS, EVENT_POOL = _load_events()


def _inject_tours_boons():
    """§15.9 CLEAR + SALVAGE — the two cancelled-tour boons, framework-native (VERB · SCOPE · DURATION),
    magnitude 1, rare (1 copy each). Not yet in events.csv (see the TOURS_BOONS flag note above), so the
    sim adds them here faithfully to the spec so the SALVAGE-swing / catch-up probes can run:
      * CLEAR  — *Back On the Itinerary* : VERB clear · SCOPE ⦿self · night / Central · qty 1. Shed ONE of
                 your OWN cancelled tours (highest-value → box); fizzle if you hold none.
      * SALVAGE — *Someone Has to Run It* : VERB salvage · SCOPE ✦(lowest-scoring rival) · night / South ·
                 qty 1. The trailer sheds one cancelled tour's −⌊V/2⌋; the salvaged tour enters the DRAWER's
                 Completed at HALF value ⌊V/2⌋. Graceful degrade → CLEAR own if no valid trailer.
    Scope on SALVAGE is stored 'salvage' (a bespoke lowest-scorer target, NOT the ✦ leader used by losses)
    so _scope_targets never mis-routes it up the standings."""
    if not TOURS_BOONS:
        return
    specs = [
        {"id": "EV-N31", "region": "C", "phase": 2, "scope": "self", "duration": "now",
         "verb": "clear", "target": "", "value": 1, "qty": 1, "kind": "boon"},
        {"id": "EV-N32", "region": "S", "phase": 2, "scope": "salvage", "duration": "now",
         "verb": "salvage", "target": "", "value": 1, "qty": 1, "kind": "boon"},
    ]
    for sp in specs:
        ev = {"idx": len(EVENTS), **sp}
        EVENTS.append(ev)
        EVENT_POOL[(sp["region"], sp["phase"])].extend([ev["idx"]] * sp["qty"])


_inject_tours_boons()


# --------------------------------------------------------------------------------------------------
#  INGREDIENTS (§16) — the FIXED per-region-phase market-deck depths (ingredients.csv is the source).
#  INGREDIENTS[(region, phase)] = list of (type, quantity). Cards are ("I", type, phase); events are
#  ("E", idx, phase). Every card carries its phase → the phase-to-box sort (§16.3) reads it directly.
# --------------------------------------------------------------------------------------------------
def _load_ingredients():
    out = {(r, ph): [] for r in REGIONS for ph in (1, 2)}
    with open(os.path.join(_COMP, "ingredients.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            r = row["region"].strip()
            ph = 1 if row["phase"].strip() == "day" else 2
            typ = row["ingredient"].strip()
            qty = int(row["quantity"]) if row.get("quantity", "").strip() else 1
            if (r, ph) in out:
                out[(r, ph)].append((typ, qty))
    return out


INGREDIENTS = _load_ingredients()


# --------------------------------------------------------------------------------------------------
#  BOOKINGS — load bookings.csv and parse each `target` string into a monotonic (done, needed) fn.
# --------------------------------------------------------------------------------------------------
def _wstat(won):
    """A stat block over the vendors a player has WON (the pattern a Booking target reads)."""
    by = Counter(v["region"] for v in won)
    return {
        "n": len(won),
        "regions": set(by), "by": by,
        # §21 street-crawl (locale:) + dish-type (dishtype:) tallies over the won pile
        "locale": Counter(v["locale"] for v in won if v.get("locale")),
        "dishtype": Counter(v["dish_type"] for v in won if v.get("dish_type")),
        "max_region": max(by.values()) if by else 0,
        "food": sum(1 for v in won if not v["is_drink"]),
        "drinks": sum(1 for v in won if v["is_drink"]),
        "day_food": sum(1 for v in won if v["phase"] == 1 and not v["is_drink"]),
        "night_food": sum(1 for v in won if v["phase"] == 2 and not v["is_drink"]),
        "early": sum(1 for v in won if v["act_won"] == 1),                 # won before dusk
        "cheap": sum(1 for v in won if v["total_cost"] <= 2),
        # §13.1 / §14.3: expensive is now cost >= 4 (was >= 3) — the §12 cost curve made day S02/C02 cost-3,
        # so "marquee" splurge Bookings (n_expensive1/2) retarget to >= 4 to stay night-marquee-only.
        "expensive": sum(1 for v in won if v["total_cost"] >= 4),
        "apex": sum(1 for v in won if v["apex"]),
        "cross": sum(1 for v in won if v["cross"]),
        "contested": sum(1 for v in won if v["contested"]),
        "final_round": sum(1 for v in won if v["final_round"]),
        "cost_day": sum(v["total_cost"] for v in won if v["phase"] == 1),
        "cost_total": sum(v["total_cost"] for v in won),
    }


# map a target token -> (fn(st)->current value, is_region_specific)
_SCALARS = {
    "day_food_vendors": lambda st: st["day_food"],
    "night_food_vendors": lambda st: st["night_food"],
    "food_vendors": lambda st: st["food"],
    "food": lambda st: st["food"],
    "day_food": lambda st: st["day_food"],
    "night_food": lambda st: st["night_food"],
    "drinks": lambda st: st["drinks"],
    "drink": lambda st: st["drinks"],
    "regions": lambda st: len(st["regions"]),
    "vendors_total": lambda st: st["n"],
    "early_vendors": lambda st: st["early"],
    "cheap_vendors": lambda st: st["cheap"],
    "expensive_vendors": lambda st: st["expensive"],
    "apex_wins": lambda st: st["apex"],
    "cross_region": lambda st: st["cross"],
    "contested_wins": lambda st: st["contested"],
    "final_round_wins": lambda st: st["final_round"],
    "region_depth": lambda st: st["max_region"],
    "ingredient_cost_day": lambda st: st["cost_day"],
    "ingredient_cost_total": lambda st: st["cost_total"],
}


def _parse_target(target):
    """Return a fn(st) -> (done, needed) giving monotonic partial credit for one booking target."""
    clauses = []  # list of (fn(st)->current, need)
    for part in target.split(";"):
        part = part.strip()
        if part.startswith("pair:"):
            a, b = part[len("pair:"):].split("+")
            clauses.append((lambda st, a=a: min(st["by"].get(a, 0), 1), 1))
            clauses.append((lambda st, b=b: min(st["by"].get(b, 0), 1), 1))
        elif part.startswith("vendors_region:"):
            body = part[len("vendors_region:"):]
            reg, need = body.split(">=")
            clauses.append((lambda st, r=reg: st["by"].get(r, 0), int(need)))
        elif part.startswith("locale:"):
            # §21 street-crawl: N won vendors sharing one `locale` (e.g. locale:dadaocheng>=2 = the Dihua crawl)
            loc, need = part[len("locale:"):].split(">=")
            clauses.append((lambda st, x=loc.strip(): st["locale"].get(x, 0), int(need)))
        elif part.startswith("dishtype:"):
            # §21 dish-type: N won vendors of one `dish_type` (e.g. dishtype:bubble_tea>=2, dishtype:rice>=3)
            kind, need = part[len("dishtype:"):].split(">=")
            clauses.append((lambda st, x=kind.strip(): st["dishtype"].get(x, 0), int(need)))
        else:
            key, need = part.split(">=")
            fn = _SCALARS[key.strip()]
            clauses.append((fn, int(need)))

    def progress(st):
        done = sum(min(fn(st), need) for fn, need in clauses)
        needed = sum(need for _, need in clauses)
        return done, needed
    return progress


def _load_bookings():
    out = {}
    order = []
    with open(os.path.join(_COMP, "bookings.csv"), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["type"].strip() == "boundary":
                continue
            key = row["id"].strip()
            ph_raw = row["phase"].strip()
            # §20/§21 THREE booking phases: day=1 (DUSK-judged), night=2 (LAST-TRAIN, night-locked),
            # any=3 (AGNOSTIC — drawable from setup, satisfiable across the whole game, judged at LAST
            # TRAIN, NOT coerced to night). The old model mapped "any"→night; the re-model gives it its
            # own value so it is (a) in the setup-available deck and (b) NOT frozen at dusk.
            phase = 1 if ph_raw == "day" else (3 if ph_raw == "any" else 2)
            tags = {t.strip() for t in row.get("tags", "").split(";") if t.strip()}
            counts = ""                                       # e.g. "3456" / "456" from the `counts:` tag
            for t in tags:
                if t.startswith("counts:"):
                    counts = t[len("counts:"):]
            out[key] = {
                "value": int(row["value"]),
                "phase": phase,
                "target": row["target"].strip(),
                "progress": _parse_target(row["target"].strip()),
                "is_general": key.startswith("g_"),
                "is_prestige": "value" in row.get("tags", "") and "prestige" in key,
                "tags": tags,
                "counts": counts,                             # player counts this tour is dealt at
                "onramp": "onramp" in tags,                   # §21.5 on-ramp (easy value-3) tour
            }
            order.append(key)
    return out, order


BOOKINGS, BOOKING_ORDER = _load_bookings()
PRESTIGE_KEYS = {"d_prestige8", "n_prestige14", "g_prestige12"}
# §20/§21 booking pools by phase. AGNOSTIC "any" (phase 3) tours are drawable from SETUP *and* stay
# drawable in night (they satisfy across the whole game), so they ride BOTH the setup-available pool and
# the night pool. day (1) = setup-only (DUSK-judged); night (2) = night-only. §20.9 sampling model: the
# setup-available deck = day + any; the night deck = night + any (both faithful to "drawable from setup /
# judged at last train"), landed here with the combined re-smoke.
DAY_POOL = [k for k, b in BOOKINGS.items() if b["phase"] in (1, 3)]      # setup-available (day + any)
NIGHT_POOL = [k for k, b in BOOKINGS.items() if b["phase"] in (2, 3)]    # night deck (night + any)

# §21.5 the `counts` tag + `onramp` flag, DERIVED FROM THE CSV (not hardcoded): HEAVY = the >=4-claim
# tours NOT dealt at 3p (their `counts` tag omits '3', i.e. counts:456); ON-RAMP = the easy value-3 tours
# governed by onramp_high_count at 4-6p. Overrides the earlier id-list placeholders now that the CSV
# carries the real tags (the sim can never drift from the built data).
HEAVY_TOURS = {k for k, b in BOOKINGS.items() if b["counts"] and "3" not in b["counts"]}
ONRAMP_TOURS = {k for k, b in BOOKINGS.items() if b["onramp"]}

# The two flagged-risk tours that BOTH hinge on the single-slot night stall N07 (珍奶 · Bubble Tea,
# Dadaocheng Wharf): g_travel3d = dishtype:bubble_tea>=2 (needs N07 + C03), d_north2 = locale:dadaocheng>=2
# (needs N07 + N02). If N07 rarely surfaces / is won, these two are orphaned in practice — we track their
# held-vs-completed rate (and N07's surface/win rate) so bg-playtest can size the orphan risk.
TRACKED_TOURS = {"g_travel3d", "d_north2"}
N07_ID = VID_BY_KEY.get("N07")


def _booking_done(key, won):
    d, n = BOOKINGS[key]["progress"](_wstat(won))
    return d >= n


def _booking_helps(key, cand, won):
    st = _wstat(won)
    d0, n = BOOKINGS[key]["progress"](st)
    if d0 >= n:
        return False
    d1, _ = BOOKINGS[key]["progress"](_wstat(won + [cand]))
    return d1 > d0


def _judge_booking(key, won):
    """Win-pile / lose-pile score: +value if the pattern is complete, else −floor(value/2)."""
    v = BOOKINGS[key]["value"]
    return v if _booking_done(key, won) else -(v // 2)


# --------------------------------------------------------------------------------------------------
#  CHARACTERS — load characters.csv → the six kits (ability_code drives the mechanics).
# --------------------------------------------------------------------------------------------------
# internal char keys mirror the ability lanes; map CSV id -> key
CHAR_KEY = {"C1": "councillor", "C2": "homebody", "C3": "bigeater",
            "C4": "influencer", "C5": "bigbrother", "C6": "globetrotter"}
ZH = {"councillor": "里長伯", "homebody": "媽寶", "bigeater": "大胃王",
      "influencer": "網紅", "bigbrother": "大哥", "globetrotter": "阿嬤", "neutral": "(neutral)"}
CHAR_MAX = {"influencer": INFL_MAX}   # everyone else = FIELD_MAX
CHAR_ORDER = ("councillor", "homebody", "bigeater", "influencer", "bigbrother", "globetrotter")


def _char_max(ch):
    return CHAR_MAX.get(ch, FIELD_MAX)


# ==================================================================================================
#  MAP HELPERS
# ==================================================================================================
def neighbours(pos, char=None, hsr_open=True):
    """Legal Travel destinations. 阿嬤 (globetrotter) reaches ANY region in one Travel (elder pass) and is
    immune to the HSR outage. Everyone else: ring + the HSR N↔S hop when it is open."""
    if char == "globetrotter":
        return [r for r in REGIONS if r != pos]
    ns = list(RING[pos])
    if hsr_open and pos in HSR:
        other = HSR[1] if pos == HSR[0] else HSR[0]
        if other not in ns:
            ns.append(other)
    return ns


def _dist(pos, dest, char=None, hsr_open=True):
    if pos == dest:
        return 0
    q = deque([(pos, 0)]); seen = {pos}
    while q:
        cur, d = q.popleft()
        for nb in neighbours(cur, char, hsr_open):
            if nb in seen:
                continue
            if nb == dest:
                return d + 1
            seen.add(nb); q.append((nb, d + 1))
    return 99


def _next_hop(pos, dest, char=None, hsr_open=True):
    if pos == dest or dest is None:
        return pos
    q = deque([(pos, None)]); seen = {pos}
    while q:
        cur, first = q.popleft()
        for nb in neighbours(cur, char, hsr_open):
            if nb in seen:
                continue
            fh = nb if first is None else first
            if nb == dest:
                return fh
            seen.add(nb); q.append((nb, fh))
    hops = neighbours(pos, char, hsr_open)
    return hops[0] if hops else pos


# ==================================================================================================
#  PER-COUNT SETUP TABLES (from map.json — data is the source of truth)
# ==================================================================================================
def _slots_for(n):
    if SLOTS_OVERRIDE:
        v = [int(x) for x in SLOTS_OVERRIDE.split(",")]
        return {"N": v[0], "C": v[1], "S": v[2], "E": v[3]}
    if _scaling_recommended() and n in REC_SLOTS:
        v = REC_SLOTS[n]
        return {"N": v[0], "C": v[1], "S": v[2], "E": v[3]}
    tab = MAP["vendor_slots"].get(str(n)) or MAP["vendor_slots"].get(str(min(max(n, 3), 6)))
    return {r: tab[r] for r in ("N", "C", "S", "E")}


def _booking_deck_sizes(n):
    t = MAP["booking_deck_sizes"].get(str(n)) or MAP["booking_deck_sizes"].get(str(min(max(n, 3), 6)))
    return t["day"], t["night"]


def _event_mix_for(n):
    """§15.4 per-count events-per-region-phase draw ratio (from map.json.event_deck_mix)."""
    t = MAP["event_deck_mix"].get(str(n)) or MAP["event_deck_mix"].get(str(min(max(n, 3), 6)))
    return t["day"], t["night"]


# §17 CLOSING-TIME DIE — faces are DATA (map.json.vendor_clock.die_faces); 4 region faces + 2 BLANK.
DIE_FACES = tuple(MAP["vendor_clock"]["die_faces"])


def _track_length(n):
    """Rounds per Closing-Time track cycle for this count. TA_TRACK_L overrides for the L-sweep; else the
    per-count value from map.json.vendor_clock.track_length (baseline 3 for all counts)."""
    if TRACK_L_OVERRIDE:
        return TRACK_L_OVERRIDE
    if _scaling_recommended() and n in REC_TRACK:
        return REC_TRACK[n]
    tab = MAP["vendor_clock"]["track_length"]
    return int(tab.get(str(n)) or tab.get(str(min(max(n, 3), 6))) or 3)


def _pool_target(phase, n):
    """§17.6 per-count subset size for a phase. A global TA_POOL ('D,M' = day,night) wins; else the
    recommended per-count table (REC_POOL); else None (full pool)."""
    if POOL_OVERRIDE:
        parts = [int(x) for x in POOL_OVERRIDE.split(",")]
        return parts[0] if phase == 1 else parts[1]
    if _scaling_recommended() and n in REC_POOL:
        return REC_POOL[n][0] if phase == 1 else REC_POOL[n][1]
    return None


def _phase_decks(phase, n, rng):
    """Build the per-region vendor decks for a phase as a per-count SUBSET of the full pool (§17.6).
    Returns {region: [vid, ...]} already shuffled. The full pool is the 13 day / 11 night unique dishes;
    TA_POOL trims (subset) or extends (dupe) the TOTAL toward its target while ALWAYS keeping each region's
    slot-floor face-able (no region starts starved). SUBSET is preferred; a target > full DUPLICATES cards
    (flagged — dupes share a vid, which the vid-keyed stall identity cannot cleanly distinguish, so dupes are
    a diagnostic only, not the shipped recommendation)."""
    slots = _slots_for(n)
    decks = {r: _region_deck(r, phase) for r in REGIONS}
    for r in REGIONS:
        rng.shuffle(decks[r])
    target = _pool_target(phase, n)
    full = sum(len(decks[r]) for r in REGIONS)
    if target is None or target == full:
        return decks
    if target < full:
        # keep at least each region's slot-floor; remove the surplus at random down to the target
        floors = {r: min(slots[r], len(decks[r])) for r in REGIONS}
        target = max(target, sum(floors.values()))      # cannot drop below what the slots demand
        removable = [(r, i) for r in REGIONS for i in range(floors[r], len(decks[r]))]
        rng.shuffle(removable)
        drop = set(removable[: full - target])
        for r in REGIONS:
            decks[r] = [decks[r][i] for i in range(len(decks[r])) if (r, i) not in drop]
    else:
        # DUPE (diagnostic): spread (target-full) duplicate cards across regions round-robin
        pool = [(r, vid) for r in REGIONS for vid in decks[r]]
        rng.shuffle(pool)
        for k in range(target - full):
            r, vid = pool[k % len(pool)]
            decks[r].append(vid)
    return decks


def _ing_cards(r, phase):
    """The fixed ingredient-card multiset for a region+phase market deck (ingredients.csv)."""
    cards = []
    for typ, qty in INGREDIENTS[(r, phase)]:
        cards.extend([("I", typ, phase)] * qty)
    return cards


def _deal_events(r, phase, n_players, rng):
    """Deal the per-count slice of the (r, phase) event POOL into this region's market deck (§15.4)."""
    if EVENTS_OFF:
        return []
    day_ct, night_ct = _event_mix_for(n_players)
    count = int(round((day_ct if phase == 1 else night_ct) * EVENT_SCALE))
    pool = list(EVENT_POOL[(r, phase)])
    rng.shuffle(pool)
    return [("E", idx, phase) for idx in pool[:min(count, len(pool))]]


def _build_market(s, r, phase, rng):
    """Build one region's live market deck (ingredient cards + dealt events), shuffled; fresh empty
    discard. This is the §16 physical model: one live face-down deck + one face-up discard per region."""
    deck = _ing_cards(r, phase) + _deal_events(r, phase, s["n"], rng)
    rng.shuffle(deck)
    s["deck"][r] = deck
    s["disc"][r] = []


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:

    # -------- setup --------
    def new_state(self, rng, n_players=4, characters=None):
        n = n_players
        chars = list(characters) if characters else ["neutral"] * n
        slots = _slots_for(n)
        day_size, night_size = _booking_deck_sizes(n)
        mrow_w = 3 if n < 4 else 4
        if n == 3 and _reserve_3pa():
            mrow_w += 1                                       # §21.8 reserve 3p-a: +1 face-up Booking slot

        # §17.6 decide the WHOLE-GAME vendor subset UP FRONT (day + night) so the Booking deck can co-scale
        # coherently: a tour is dealt only if the count's vendor pool can complete it (no orphaned tours).
        day_decks = _phase_decks(1, n, rng)
        night_decks = _phase_decks(2, n, rng)
        pool_vids = [vid for r in REGIONS for vid in day_decks[r]] + \
                    [vid for r in REGIONS for vid in night_decks[r]]

        # deal the day face-up vendor slots (pop from the day subset decks)
        vdeck, faceup = {}, {}
        for r in REGIONS:
            d = day_decks[r]
            up = [d.pop() for _ in range(min(slots[r], len(d)))]
            vdeck[r] = d; faceup[r] = up

        # §17.6 CO-SCALED Booking decks: filter DAY / NIGHT tour pools to those COMPLETABLE at this pool,
        # THEN apply the §21.5 per-count `counts`-tag filter (3p drops HEAVY; 4–6p onramp switch).
        day_keys = self._completable_keys(pool_vids, _counts_filter(DAY_POOL, n))
        night_keys = self._completable_keys(pool_vids, _counts_filter(NIGHT_POOL, n))
        day_deck = self._build_booking_deck(day_keys, day_size, rng)
        mrow = [day_deck.pop() for _ in range(min(mrow_w, len(day_deck)))] if day_deck else []

        players = []
        for p in range(n):
            ch = chars[p]
            mx = _char_max(ch)
            home = self._pick_home(faceup, ch)
            players.append({
                "char": ch, "pos": "N",                       # common Taipei start hub (map.start_hub)
                "max": mx, "board": START_MEEPLES, "supply_f": mx - START_MEEPLES,
                # §16 Larder split by PHASE-ORIGIN: `larder` = current-phase cards (recycle to region
                # discard when spent), `larder_prev` = carried concluded-phase cards (go to the BOX when
                # spent — the phase-to-box guarantee). At dusk, larder → larder_prev.
                "larder": Counter(), "larder_prev": Counter(), "icons": Counter(), "won": [],
                "home_region": home,
                "tickets": [], "counted_done": set(), "wild_tickets": set(),
                "day_book_score": 0, "night_book_score": 0, "cancel_penalty": 0,
                # §15.9 the CANCELLED-TOUR pile: full VALUES V of cancelled Bookings (mid-game hand-limit
                # cancels + phase-boundary unfinished). Scoring penalty = Σ⌊V/2⌋ over the pile, so CLEAR /
                # SALVAGE shedding a tour reduces the penalty naturally. `salvage_score` banks the drawer's
                # half-value Completed tours gained via SALVAGE (the sole Completed-at-half exception).
                "cancelled": [], "salvage_score": 0,
                "nudges_taken": 0, "nudge_impact": 0, "max_board": START_MEEPLES,
                "next_bribe_disc": 0, "tempo_tax": 0, "promote_bonus": 0, "visit_keep_bonus": 0,
                # §15 lingering BLOCK markers (⏳TURN): expiry = the turn at which they clear (this player's
                # next turn start). -1 = inactive.
                "block_promote": -1, "block_travel": -1, "block_travel_grow": -1, "block_draw": -1,
                "ms1_done": False, "ms2_done": False,
                # per-lane fingerprint accumulators
                "fp_contest_entries": 0, "fp_wins": 0, "fp_fol_per_win": 0,
                "fp_src_visit": 0, "fp_src_travel": 0, "fp_src_cstore": 0, "fp_src_draw": 0,
                "fp_first_tier23_turn": None,
                "fp_free_draws": 0,
                "win_streak": 0, "best_win_streak": 0,
            })

        s = {
            "_rng": rng, "n": n, "slots": slots,
            "vdeck": vdeck, "faceup": faceup,
            # §16 explicit market DECK-FLOW: one live deck + one face-up discard per region (current phase)
            "deck": {}, "disc": {},
            "fol": {vid: [0] * n for r in REGIONS for vid in faceup[r]},   # committed followers per stall
            "commit_turn": {},                                             # (vid,p) -> first-commit turn
            "star": set(),                                                  # Trending markers on stalls
            "linger": [],                                                   # §15 lingering (round/phase) effects
            "hsr_closed_until": {},                                         # p -> turn (detour hsr, ⏳TURN)
            "region_out_block": {},                                         # r -> round-end (detour link, ⏳ROUND)
            "mrow": mrow, "mreserve": day_deck, "mrow_w": mrow_w,
            # §17.6 pre-decided night vendor subset + the co-scaled completable NIGHT tour pool (used at dusk)
            "night_decks": night_decks, "night_keys": night_keys, "pool_vids": pool_vids,
            "day_size": day_size, "night_size": night_size,
            "players": players, "act": 1, "turn": 0, "cur": 0, "round": 0,
            "end_turn": None, "end_cause": None, "done": False, "_finalized": False,
            "dusk_turn": None, "last_turn": None, "first_night_win_turn": None,
            # §17 VENDOR-DEPLETION CLOCK + CLOSING-TIME DIE. The die is a SEPARATE seedable RNG so it is
            # reproducible independently of the shuffle stream (TA_DIE_SEED pins it; else it is derived
            # deterministically from this match's rng). `track` counts rounds 0→L-1; a roll fires at L.
            "track": 0,
            "die": random.Random(int(DIE_SEED_OVERRIDE)) if DIE_SEED_OVERRIDE else random.Random(rng.getrandbits(63)),
            "die_rolls": 0, "die_blanks": 0, "die_noremovable": 0,
            "die_removals": 0, "die_removals_contested": 0,
            # deadlock backstop tracker: rounds the face-up SET has been unchanged (a proxy for "no progress")
            "faceup_sig": None, "static_rounds": 0, "backstop_fires": 0,
            # ---- diagnostics / §9 probes ----
            "claims": 0, "contested_claims": 0, "claim_by_region": {r: 0 for r in REGIONS},
            "night_claims": 0, "prestige_completions": 0, "cancels": 0,
            # §21 WILD BOOKING probes: face-up Books vs blind (wild) Books, by phase; wild tours that
            # ended up COMPLETED (the wild-book completion contribution) vs whiffed-and-cancelled.
            "books_faceup": 0, "books_wild": 0, "books_wild_day": 0, "books_wild_night": 0,
            "wild_keys_taken": [], "wild_completed": 0, "wild_cancelled": 0,
            "food_wins": 0, "drink_wins": 0, "apex_claims": 0,
            "src_by_type": Counter(), "empty_draws": 0,
            "travels": 0, "visits": 0, "cstores": 0, "promotes": 0, "passes": 0,
            "grow_total": 0, "grow_homebody_tick": 0, "return_to_supply": 0,
            "legal_counts": [], "forced_turns": 0,
            "tie_blocks": 0, "resolver_fires": 0, "frozen_at_boundary": 0,
            "below_floor_blocks": 0,                                        # §12.2 min-follower gate blocks
            "max_committed_on_stall": 0, "max_committed_by_player": 0,
            "dage_edge_fires": 0, "dage_claims": 0,
            "ama_claims": 0, "ama_snipes": 0, "ama_travel_cost_paid": 0,
            "events_fired": 0, "trending_grows": 0,
            # ---- §15 event probes ----
            "ev_by_verb": Counter(), "ev_leader_fires": 0, "ev_leader_fizzles": 0,
            "swipes": 0, "spoils": 0, "gifts": 0, "restocks": 0, "washes": 0, "blocks": 0, "detours": 0,
            # §15.5 no-pile-on cap: leaders already ✦-nudged THIS round (cleared each end-of-round); cumulative
            # leader ✦-hazard impact across the game (the "mild nudge, not a beating" binding target).
            "nudged_this_round": Counter(), "nudge_pileon_blocked": 0, "leader_nudge_impact": 0,
            # §15.9 CLEAR / SALVAGE probes (the catch-up double-boons + the SALVAGE-swing guard)
            "clear_fires": 0, "clear_relief": 0, "salvage_fires": 0, "salvage_fizzles": 0,
            "salvage_gain_drawer": 0, "salvage_relief_trailer": 0,
            # §18 VISIT decision-density (M1): Visits offering a real keep-choice (≥2 distinct ingredient types)
            "visit_choice_offered": 0,
            # ---- §16 deck-flow probes ----
            "reshuffles": {(r, ph): 0 for r in REGIONS for ph in (1, 2)},
            "reshuffle_sizes": {(r, ph): [] for r in REGIONS for ph in (1, 2)},
            "evfrac_samples": {(r, ph): [] for r in REGIONS for ph in (1, 2)},
            "pantry_supply_min": 10 ** 9, "box_from_larder": 0,
            "commit_hist": [],   # (turn, vid, p) for fingerprints / earliest committer
            # N07-orphan probe: per-game held/completed for the two N07-dependent tours + N07 surface/win.
            "tour_held": Counter(), "tour_completed": Counter(),
            "n07_surfaced": False, "n07_won": False,
        }
        # build the four DAY live market decks (ingredient cards + dealt day events) + fresh discards
        for r in REGIONS:
            _build_market(s, r, 1, rng)
        self._sample_pantry_min(s)
        return s

    def _build_booking_deck(self, pool, size, rng):
        if not pool:
            return []
        deck = []
        while len(deck) < size:
            chunk = list(pool); rng.shuffle(chunk); deck.extend(chunk)
        deck = deck[:size]; rng.shuffle(deck)
        return deck

    def _completable_keys(self, pool_vids, keys):
        """§17.6 CO-SCALING coherence: return the subset of `keys` whose target is COMPLETABLE given the
        count's vendor pool — i.e. if ONE player could win EVERY vendor in the pool, the tour completes.
        A tour that even a whole-pool monopoly cannot finish (no apex left for apex_wins, pool total < the
        collection target, a region below its region-count, no cross/expensive dish, …) is ORPHANED and is
        NOT dealt at this count (the fix for the falsely-low completion / falsely-high hoarder read). Dynamic
        targets (contested/early/final wins) are treated as satisfiable — they depend on play, not the pool —
        by marking the upper-bound win pile contested + early + final."""
        upper = []
        for vid in pool_vids:
            v = VENDORS[vid]
            upper.append({"id": vid, "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
                          "total_cost": v["total_cost"], "tier": v["tier"], "apex": v["apex"],
                          "cross": v["cross"], "vp": v["vp"],
                          "locale": v["locale"], "dish_type": v["dish_type"],
                          "contested": True, "act_won": 1, "final_round": True})
        st = _wstat(upper)
        out = []
        for k in keys:
            d, need = BOOKINGS[k]["progress"](st)
            if d >= need:
                out.append(k)
        return out

    def _pick_home(self, faceup, ch):
        """里長伯 names one home region at setup (bot heuristic: the region with the most face-up food
        stalls — where his home-gated draw engine has the most to buy). Everyone else: None."""
        if ch != "councillor":
            return None
        score = {r: sum(1 for vid in faceup[r] if not VENDORS[vid]["is_drink"]) for r in REGIONS}
        return max(REGIONS, key=lambda r: (score[r], -REGIONS.index(r)))

    # -------- harness protocol --------
    def players(self, s):
        return list(range(s["n"]))

    def actors(self, s):
        return [s["cur"]]

    def view(self, s, p):
        return s

    def is_over(self, s):
        return s["done"]

    # -------- follower helpers --------
    def _committed(self, s, p):
        return sum(b[p] for b in s["fol"].values())

    def _hsr_open(self, s):
        """§15 DETOUR [hsr] event (⏳TURN): the HSR N↔S link is down for the acting player until their
        next turn. Globetrotter 阿嬤 is immune (handled in neighbours() by char)."""
        p = s["cur"]
        return s["hsr_closed_until"].get(p, -1) <= s["turn"]

    def _board(self, s):
        return [vid for r in REGIONS for vid in s["faceup"][r]]

    def _present(self, s, p, vid):
        return s["players"][p]["pos"] == VENDORS[vid]["region"]

    def _dage_n(self):
        return DAGE_N

    def _needed_to_win(self, s, p, vid):
        """SPREAD-AWARE / MARGIN-AWARE: how many MORE followers p must commit on vid to hold a claiming
        plurality RIGHT NOW — accounting for co-located Big-Brother rivals (a BB rival needs +N to beat)
        and for p itself being Big Brother (it need only match at N=1). Returns 0 if p can already claim
        (given ≥1 committed). Returns a large number if impossible this turn (no headroom)."""
        fol = s["fol"][vid]
        mine = fol[p]
        req = 0
        for q in range(s["n"]):
            if q == p:
                continue
            rq = fol[q]
            if rq == 0:
                continue
            if s["players"][q]["char"] == "bigbrother":
                need_here = rq + DAGE_N            # to BEAT a BB rival, exceed him by N
            else:
                need_here = rq + 1                 # strict plurality over a normal rival
            req = max(req, need_here)
        if s["players"][p]["char"] == "bigbrother":
            # BB claims if the top rival exceeds him by < N  →  he needs mine >= top_rival - (N-1)
            top = max((fol[q] for q in range(s["n"]) if q != p), default=0)
            req = max(0, top - (DAGE_N - 1))
        need_more = max(0, req - mine)
        # §12.2 MIN-FOLLOWER FLOOR (tier-scaled 1/2/3): you must also hold at least the stall's floor of
        # your OWN followers — the floor is an absolute personal minimum, stacked on the relative fight,
        # and Big Brother's margin never waives it (§12.3 interaction 1).
        floor = VENDORS[vid]["floor"]
        if mine + need_more < floor:
            need_more = floor - mine
        return need_more

    def _can_claim_margin(self, s, p, vid):
        # claim needs BOTH the plurality/margin (needed_to_win == 0) AND meeting the floor with own crowd
        return self._needed_to_win(s, p, vid) == 0 and s["fol"][vid][p] >= VENDORS[vid]["floor"]

    # -------- Larder (phase-origin split, §16) --------
    def _have(self, pl, t):
        return pl["larder"].get(t, 0) + pl["larder_prev"].get(t, 0)

    def _larder_total(self, pl):
        return sum(pl["larder"].values()) + sum(pl["larder_prev"].values())

    def _spend_one(self, s, pl, t):
        """Spend 1 ingredient of type t. A CURRENT-phase card recycles to its region's face-up discard
        (§16.2 feeder 2); a carried CONCLUDED-phase card goes to the BOX (§16.3) — never a current
        discard, which is what keeps a night reshuffle night-only. Current spent first (feeds the loop)."""
        if pl["larder"].get(t, 0) > 0:
            pl["larder"][t] -= 1
            self._discard_ingredient(s, t)
        elif pl["larder_prev"].get(t, 0) > 0:
            pl["larder_prev"][t] -= 1
            s["box_from_larder"] += 1        # stale card leaves the game

    def _discard_ingredient(self, s, t):
        """Route a current-phase ingredient token to its home region's face-up discard (§16.2)."""
        home = COMMON_HOME[t] if _is_common(t) else TYPE_SIG_REGION[t]
        s["disc"][home].append(("I", t, s["act"]))

    # -------- cost / affordability --------
    def _pay_plan(self, s, p, vid):
        pl = s["players"][p]
        v = VENDORS[vid]
        pay = {}
        for t, c in v["cost"].items():
            if _is_common(t):
                pay[t] = c                                     # commons carry no region icon → never discounted
            else:
                reg = TYPE_SIG_REGION[t]
                pay[t] = max(0, c - pl["icons"].get(reg, 0))
        if pl["next_bribe_disc"] > 0:                          # Rave-Review boon: next Bribe 1 cheaper
            for t in sorted(pay, key=lambda k: -pay[k]):
                if pay[t] > 0:
                    pay[t] -= 1; break
        return pay

    def _can_afford(self, s, p, vid):
        pl = s["players"][p]
        return all(self._have(pl, t) >= c for t, c in self._pay_plan(s, p, vid).items())

    def _can_bribe(self, s, p, vid):
        return self._present(s, p, vid) and self._can_claim_margin(s, p, vid) and self._can_afford(s, p, vid)

    def _promote_ok(self, s, p, vid):
        pl = s["players"][p]
        if pl["block_promote"] > s["turn"]:               # §15 BLOCK [promote] (⏳TURN)
            return False
        return pl["board"] > 0 and self._present(s, p, vid)

    # -------- legal actions --------
    def legal_actions(self, s, p):
        pl = s["players"][p]
        acts = []
        board = self._board(s)
        for vid in board:
            if self._can_bribe(s, p, vid):
                acts.append(("bribe", vid))
        for vid in board:
            if self._promote_ok(s, p, vid):
                acts.append(("promote", vid))
        acts.append(("visit",))
        for r in REGIONS:
            acts.append(("cstore", r))
        # §15 DETOUR [link] (⏳ROUND): can't Travel OUT of a region under an active roadworks/landslide lock
        if s["region_out_block"].get(pl["pos"], -1) < s["round"]:
            for d in neighbours(pl["pos"], pl["char"], self._hsr_open(s)):
                acts.append(("travel", d))
        if s["mrow"]:                                      # cancel-to-claim keeps the deck-clock draining
            acts.append(("claim",))
        return acts

    def _in_progress(self, pl):
        return [k for k in pl["tickets"] if k not in pl["counted_done"]]

    def _prog_frac(self, pl, key):
        d, need = BOOKINGS[key]["progress"](_wstat(pl["won"]))
        return (d / need) if need else 1.0

    # -------- transition --------
    def step(self, s, actions, rng):
        s["_rng"] = rng
        p = s["cur"]
        pl = s["players"][p]
        act = actions[p]
        # §15 lingering ⏳TURN blocks clear at the START of the affected player's next turn (their block_*
        # flags carry the turn they were set; if that is < now, they have lapsed — legal_actions/grow read
        # them live, so nothing more to clear here; the hsr closure likewise lapses by turn compare).
        legal = self.legal_actions(s, p)
        s["legal_counts"].append(len(legal))
        if len(legal) <= 1:
            s["forced_turns"] += 1

        # 里長伯 HOME-GATED FAVOURS DRAW: while in home region, start of turn draw 1 ingredient (no action).
        # §15 BLOCK [draw] suppresses it (⏳TURN).
        if pl["char"] == "councillor" and pl["pos"] == pl["home_region"] and pl["block_draw"] <= s["turn"]:
            self._councillor_draw(s, p)

        kind = act[0]
        if kind == "bribe":
            self._do_bribe(s, p, act[1], rng)
        elif kind == "promote":
            self._do_promote(s, p, act[1])
        elif kind == "visit":
            self._do_visit(s, p, rng)
        elif kind == "cstore":
            self._do_cstore(s, p, act[1], rng)
        elif kind == "travel":
            self._do_travel(s, p, act[1], rng)
        elif kind == "claim":
            self._do_claim(s, p)
        elif kind == "wild_book":
            self._do_wild_book(s, p)
        else:
            s["passes"] += 1
        self._discard_to_cap(s, pl)
        self._track_committed(s, p)

        s["turn"] += 1
        # END OF ROUND (every player has taken one turn) → SLOW REFILL of empty face-up slots + expire the
        # ⏳ROUND lingering boons (Golden Week visit-keep bonus) at the same beat slow-refill already uses.
        if s["turn"] % s["n"] == 0:
            s["round"] += 1
            if SLOW_REFILL:
                self._refill_round(s)       # rolls the Closing-Time die (§17) then slow-refills
            for q in range(s["n"]):
                s["players"][q]["visit_keep_bonus"] = 0
            s["nudged_this_round"].clear()     # §15.5: the no-pile-on ceiling resets each round
            self._check_pool_boundary(s)    # §17: DUSK / LAST-TRAIN off vendor-pool emptiness + backstop
        s["cur"] = s["turn"] % s["n"]

        if s["end_turn"] is None and s["turn"] >= STALL_CAP * s["n"]:
            self._trigger_end(s, "stall")
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            self._finalize(s); s["done"] = True
        if s["turn"] > 12000:
            self._finalize(s); s["done"] = True
        return s

    def _track_committed(self, s, p):
        s["max_committed_by_player"] = max(s["max_committed_by_player"], self._committed(s, p))
        pl = s["players"][p]
        pl["max_board"] = max(pl["max_board"], pl["board"])   # banked-board probe (late-battler fingerprint)
        for b in s["fol"].values():
            s["max_committed_on_stall"] = max(s["max_committed_on_stall"], max(b))

    # -------- follower lifecycle --------
    def _grow(self, s, p, kind="travel"):
        """supply → your board (+1). Homebody grow-tick switchable OFF (reserve g′)."""
        pl = s["players"][p]
        if kind == "travel" and pl["char"] == "homebody" and not HOMEBODY_GROW:
            return
        if pl["supply_f"] > 0:
            pl["supply_f"] -= 1; pl["board"] += 1
            s["grow_total"] += 1
            if pl["char"] == "homebody" and kind == "travel":
                s["grow_homebody_tick"] += 1

    def _return_one_to_supply(self, s, p):
        """A bad-review event: return 1 follower to your OWN supply (prefer pulling a committed one off
        the least-useful stall, else a rallied one off your board)."""
        pl = s["players"][p]
        cands = [vid for vid, b in s["fol"].items() if b[p] > 0]
        if cands:
            vid = min(cands, key=lambda v: (self._needed_to_win(s, p, v), s["fol"][v][p]))
            s["fol"][vid][p] -= 1; pl["supply_f"] += 1
            s["return_to_supply"] += 1
        elif pl["board"] > 0:
            pl["board"] -= 1; pl["supply_f"] += 1
            s["return_to_supply"] += 1

    def _do_promote(self, s, p, vid, spread_vid=None):
        """Place up to 2 from your board onto stall(s) you stand with. MAY SPREAD across two co-located
        face-up stalls (spread_vid = the 2nd stall to receive the 2nd follower)."""
        pl = s["players"][p]
        cap = 2 + pl["promote_bonus"]                     # §15 Blogger boon: next Promote places +1
        n_place = min(cap, pl["board"])
        if n_place <= 0:
            return
        s["promotes"] += 1
        if pl["promote_bonus"] > 0:
            pl["promote_bonus"] = 0                        # one-shot: consumed on this Promote
        # spread puts 1 on the partner stall and the rest on the primary (keeps the old split behaviour)
        if spread_vid is not None and n_place >= 2:
            self._place(s, p, vid, n_place - 1)
            self._place(s, p, spread_vid, 1)
        else:
            self._place(s, p, vid, n_place)

    def _place(self, s, p, vid, k):
        pl = s["players"][p]
        k = min(k, pl["board"])
        if k <= 0:
            return
        pl["board"] -= k
        s["fol"][vid][p] += k
        s["commit_turn"].setdefault((vid, p), s["turn"])
        s["commit_hist"].append((s["turn"], vid, p))

    def _do_bribe(self, s, p, vid, rng):
        pl = s["players"][p]
        v = VENDORS[vid]
        # pay ingredients — each spent card recycles to its region discard, or to the box if stale (§16)
        for t, c in self._pay_plan(s, p, vid).items():
            for _ in range(c):
                self._spend_one(s, pl, t)
        if pl["next_bribe_disc"] > 0:
            pl["next_bribe_disc"] -= 1
        contested = any(s["fol"][vid][q] > 0 for q in range(s["n"]) if q != p)
        self._award(s, p, vid, contested, rng)

    def _award(self, s, p, vid, contested, rng):
        """Resolve a claim: winner takes the stall; winner's committed → board; losers' committed → own
        supply; the slot stays EMPTY (slow refill). Records fingerprints + Big-Brother/Globetrotter probes."""
        pl = s["players"][p]
        v = VENDORS[vid]
        won_followers = s["fol"][vid][p]
        top_rival = max((s["fol"][vid][q] for q in range(s["n"]) if q != p), default=0)
        # WIN direction: your committed followers come home to YOUR BOARD (kept)
        pl["board"] += won_followers
        # LOSE direction: each rival's committed followers go back to THEIR OWN supply
        for q in range(s["n"]):
            if q != p and s["fol"][vid][q] > 0:
                s["players"][q]["supply_f"] += s["fol"][vid][q]
                s["return_to_supply"] += s["fol"][vid][q]
        s["fol"][vid] = [0] * s["n"]
        for q in range(s["n"]):
            s["commit_turn"].pop((vid, q), None)

        starred = vid in s["star"]
        pl["won"].append({
            "id": vid, "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "total_cost": v["total_cost"], "tier": v["tier"], "apex": v["apex"], "cross": v["cross"],
            "vp": v["vp"],                                  # §14 vendor VP (the second scoring track)
            "locale": v["locale"], "dish_type": v["dish_type"],   # §21 street-crawl / dish-type targets
            "contested": contested, "act_won": s["act"], "final_round": s["end_turn"] is not None,
        })
        if vid == N07_ID:
            s["n07_won"] = True
        if v["apex"]:
            s["apex_claims"] += 1
        if not v["is_drink"] and v["icon"]:
            pl["icons"][v["icon"]] += 1
        # Trending: winning a marked stall grows 1 follower
        if starred:
            s["star"].discard(vid); s["trending_grows"] += 1; self._grow(s, p, "trending")

        # counters
        s["claims"] += 1
        s["claim_by_region"][v["region"]] += 1
        pl["fp_wins"] += 1
        pl["fp_fol_per_win"] += won_followers
        pl["win_streak"] += 1
        pl["best_win_streak"] = max(pl["best_win_streak"], pl["win_streak"])
        for q in range(s["n"]):
            if q != p:
                s["players"][q]["win_streak"] = 0
        if v["is_drink"]:
            s["drink_wins"] += 1
        else:
            s["food_wins"] += 1
        if contested:
            s["contested_claims"] += 1
            pl["fp_contest_entries"] += 1
        if v["phase"] == 2:
            s["night_claims"] += 1
            if s["first_night_win_turn"] is None:
                s["first_night_win_turn"] = s["turn"]
        if v["tier"] >= 2 and pl["fp_first_tier23_turn"] is None:
            pl["fp_first_tier23_turn"] = s["turn"]
        # Big Brother edge-fire: did his MARGIN decide the claim? (he won without a strict plurality —
        # a rival matched or came within N of his committed followers). top_rival captured pre-clear.
        if pl["char"] == "bigbrother":
            s["dage_claims"] += 1
            if top_rival >= won_followers:               # tie or a rival ahead-but-inside-the-margin
                s["dage_edge_fires"] += 1
        # Globetrotter snipe: an uncontested grab in a non-start region she reached this round
        if pl["char"] == "globetrotter":
            s["ama_claims"] += 1
            if not contested and v["region"] != "N":
                s["ama_snipes"] += 1

        self._remove_and_refill(s, v["region"], vid)   # slow-refill: leaves the slot EMPTY (no immediate)
        self._check_completions(s, p)
        self._check_milestones(s, p)

    def _remove_and_refill(self, s, region, vid):
        up = s["faceup"][region]
        if vid in up:
            up.remove(vid)
        # V7-M SCARCITY: the slot stays EMPTY until the end-of-round refill (never immediate) when SLOW.
        if not SLOW_REFILL:
            self._fill_slot(s, region)

    def _fill_slot(self, s, region):
        if APEX_NOREFILL:
            pass  # reserve d handled in _refill_round (apex removed from deck once claimed)
        deck = s["vdeck"][region]
        if deck and len(s["faceup"][region]) < s["slots"][region]:
            nv = deck.pop()
            s["faceup"][region].append(nv)
            s["fol"].setdefault(nv, [0] * s["n"])

    def _refill_round(self, s):
        """End-of-round: (1) roll the §17 CLOSING-TIME DIE (BEFORE topping up — it thins the board even when
        claims stall), then (2) SLOW REFILL — top every region back up to its face-up count from its finite
        deck. The die removal + the claim both net-drain the finite pool by one (a removed slot refills from
        the deck), so the pool is monotone and the phase boundary is guaranteed."""
        self._closing_time_die(s)
        for r in REGIONS:
            while len(s["faceup"][r]) < s["slots"][r] and s["vdeck"][r]:
                nv = s["vdeck"][r].pop()
                if APEX_NOREFILL and VENDORS[nv]["apex"]:
                    continue   # reserve d: apex stalls, once gone, do not come back (drop, try next)
                s["faceup"][r].append(nv)
                s["fol"].setdefault(nv, [0] * s["n"])
                if nv == N07_ID:
                    s["n07_surfaced"] = True

    def _closing_time_die(self, s):
        """§17.3 the Closing-Time die forcing function. Every L rounds (L = track_length, baseline 3), roll a
        custom d6 [N,C,S,E,BLANK,BLANK] on the SEEDABLE die RNG. A region face → remove the OLDEST (leftmost,
        by insertion order) face-up stall in that region — CONTESTED OR NOT — it is GONE (never returned to
        the deck); every committed follower on it (INCLUDING a live contest) returns HOME to its owner's BOARD
        (kept, no re-grow, NO resource penalty). BLANK, or a rolled region with no removable face-up stall →
        nothing (no reroll). The die can only SPEED the close, never block it."""
        L = _track_length(s["n"])
        s["track"] += 1
        if s["track"] < L:
            return
        s["track"] = 0
        face = DIE_FORCE if DIE_FORCE else s["die"].choice(DIE_FACES)
        s["die_rolls"] += 1
        if face == "BLANK":
            s["die_blanks"] += 1
            return
        stalls = s["faceup"].get(face, [])
        if not stalls:
            s["die_noremovable"] += 1        # rolled region has no removable face-up stall → nothing
            return
        vid = stalls[0]                       # OLDEST / leftmost by insertion order
        stalls.remove(vid)
        fol = s["fol"].get(vid, [0] * s["n"])
        contested = sum(1 for q in range(s["n"]) if fol[q] > 0) >= 2
        for q in range(s["n"]):
            if fol[q] > 0:
                s["players"][q]["board"] += fol[q]   # HOME to board (no loss) — the DUSK-unclaimed treatment
        s["fol"].pop(vid, None)
        for q in range(s["n"]):
            s["commit_turn"].pop((vid, q), None)
        s["star"].discard(vid)
        s["die_removals"] += 1
        if contested:
            s["die_removals_contested"] += 1

    def _check_pool_boundary(self, s):
        """§17.1/§17.3 fire DUSK / LAST-TRAIN off VENDOR-POOL emptiness (NOT the Booking deck). Called once
        per end-of-round. DAY pool exhausted (all vdeck + all faceup empty) → DUSK; NIGHT pool exhausted →
        LAST TRAIN. The deadlock backstop covers the all-BLANK / zero-claim tail: the pool is monotone, so a
        static face-up set for a full track cycle with an empty deck (or, as an intent-faithful ultimate
        guard against a full-deck zero-progress freeze, static for 3 cycles) fires the boundary too."""
        if s["done"]:
            return
        L = _track_length(s["n"])
        decks_empty = all(not s["vdeck"][r] for r in REGIONS)
        faceup_empty = all(not s["faceup"][r] for r in REGIONS)
        sig = tuple(sorted(vid for r in REGIONS for vid in s["faceup"][r]))
        if sig == s["faceup_sig"]:
            s["static_rounds"] += 1
        else:
            s["faceup_sig"] = sig
            s["static_rounds"] = 0
        pool_gone = decks_empty and faceup_empty
        backstop = decks_empty and s["static_rounds"] >= L        # §17.3 spec backstop (realistic endgame)
        freeze_guard = s["static_rounds"] >= 3 * L                # intent-faithful net for the pathological case
        if not (pool_gone or backstop or freeze_guard):
            return
        if not pool_gone:
            s["backstop_fires"] += 1
        if s["act"] == 1:
            self._dusk(s)
        elif s["end_turn"] is None:
            self._trigger_end(s, "lasttrain")

    # -------- councillor home-gated draw --------
    def _councillor_draw(self, s, p):
        """Old Favours (home-gated): draw 1 ingredient card from ANY region's market into hand, no action.
        Bot heuristic: draw the ingredient TYPE it is most short of for a face-up food stall it can reach."""
        pl = s["players"][p]
        if self._larder_total(pl) >= self._larder_cap(pl):
            return
        need = Counter()
        for vid in self._board(s):
            v = VENDORS[vid]
            if v["is_drink"]:
                continue
            for t, c in self._pay_plan(s, p, vid).items():
                short = c - self._have(pl, t)
                if short > 0:
                    need[t] += short
        tok = need.most_common(1)[0][0] if need else SIG_TYPE[pl["pos"]]
        pl["larder"][tok] += 1
        s["src_by_type"][tok] += 1
        pl["fp_src_draw"] += 1; pl["fp_free_draws"] += 1

    # -------- claim a booking --------
    def _do_claim(self, s, p):
        pl = s["players"][p]
        if not s["mrow"]:
            return
        inprog = self._in_progress(pl)
        if len(inprog) >= HAND_LIMIT:
            # at the hand-limit → CANCEL the least-progressed in-progress Booking to make room (its
            # −floor(v/2) goes to the Cancelled pile). This keeps the deck-clock draining when Bookings
            # pile up incomplete — otherwise the night deck never exhausts and the game runs to the stall.
            victim = min(inprog, key=lambda k: self._prog_frac(pl, k))
            pl["tickets"].remove(victim)
            pl["cancelled"].append(BOOKINGS[victim]["value"])   # §15.9 pile (CLEAR/SALVAGE can shed it)
            s["cancels"] += 1
        key = max(s["mrow"], key=lambda k: self._booking_want(s, p, k))
        s["mrow"].remove(key)
        pl["tickets"].append(key)
        if key in TRACKED_TOURS:
            s["tour_held"][key] += 1
        s["books_faceup"] += 1
        if s["mreserve"]:
            s["mrow"].append(s["mreserve"].pop())
        # §17: the Booking deck is NO LONGER the clock — it is finite tour-supply and does NOT reshuffle.
        # If it runs dry the face-up row simply stops refilling; drawing a tour is optional supply, not a
        # boundary trigger. DUSK / LAST-TRAIN now fire off VENDOR-POOL emptiness (see _check_pool_boundary).

    def _do_wild_book(self, s, p):
        """§21.1 WILD BOOKING — the Book variant: decline the whole face-up row and draw the TOP of the
        current Booking deck BLIND, keep it. The face-up row is NOT refilled (you took no face-up card).
        A whiff is Cancelled later at the flat cancel; the hand-limit still caps the whiff (cancel one
        first to make room). Modelled here as: pop the top of s["mreserve"] (the current deck), keep it."""
        pl = s["players"][p]
        if not s["mreserve"]:
            return self._do_claim(s, p)               # deck dry → fall back to a face-up Book
        inprog = self._in_progress(pl)
        if len(inprog) >= HAND_LIMIT:
            victim = min(inprog, key=lambda k: self._prog_frac(pl, k))
            pl["tickets"].remove(victim)
            pl["cancelled"].append(BOOKINGS[victim]["value"])
            pl["wild_tickets"].discard(victim)
            s["cancels"] += 1
        key = s["mreserve"].pop()                     # BLIND top-of-deck draw (kept, no peek)
        pl["tickets"].append(key)
        pl["wild_tickets"].add(key)
        if key in TRACKED_TOURS:
            s["tour_held"][key] += 1
        s["books_wild"] += 1
        if BOOKINGS[key]["phase"] == 1:
            s["books_wild_day"] += 1
        else:
            s["books_wild_night"] += 1
        # the face-up row is deliberately NOT refilled on a wild Book (§21.1).

    def _booking_want(self, s, p, key):
        """How much a bot wants to hold/claim a Booking. Favours ACHIEVABLE + near-complete Bookings
        (value discounted by the remaining gap) so bots COMPLETE the ones they hold — completions free
        hand slots, which keeps the deck-clock draining and stops the game running to the stall."""
        pl = s["players"][p]
        d, need = BOOKINGS[key]["progress"](_wstat(pl["won"]))
        gap = max(0, need - d)
        val = BOOKINGS[key]["value"]
        return val / (1.0 + 0.3 * gap) + 2.0 * ((d / need) if need else 0.0)

    def _check_completions(self, s, p):
        pl = s["players"][p]
        for key in pl["tickets"]:
            if key in pl["counted_done"]:
                continue
            if _booking_done(key, pl["won"]):
                pl["counted_done"].add(key)
                if key in pl["wild_tickets"]:
                    s["wild_completed"] += 1        # §21 wild-book completion contribution
                if key in PRESTIGE_KEYS:
                    s["prestige_completions"] += 1

    def _check_milestones(self, s, p):
        """Rave Reviews (per-player, no runaway): at your 2nd completed tour grow 1 follower; at your 4th,
        take 1 useful ingredient + next Bribe 1 cheaper (tokens.csv 好評 boons)."""
        pl = s["players"][p]
        done = len(pl["counted_done"])
        if done >= 2 and not pl["ms1_done"]:
            pl["ms1_done"] = True; self._grow(s, p, "rave")
        if done >= 4 and not pl["ms2_done"]:
            pl["ms2_done"] = True
            pl["larder"][self._most_useful(s, p)] += 1
            pl["next_bribe_disc"] += 1

    def _most_useful(self, s, p):
        pl = s["players"][p]
        need = Counter()
        for vid in self._board(s):
            v = VENDORS[vid]
            if v["is_drink"]:
                continue
            for t, c in self._pay_plan(s, p, vid).items():
                short = c - self._have(pl, t)
                if short > 0:
                    need[t] += short
        return need.most_common(1)[0][0] if need else SIG_TYPE[pl["pos"]]

    # -------- DEPRECATED (§17): the old Booking-deck clock --------
    def _booking_deck_out(self, s):
        """RETIRED by §17 (the vendor-depletion clock). No longer called — DUSK / LAST-TRAIN fire off
        vendor-pool emptiness in _check_pool_boundary, not Booking-deck exhaustion. Kept only so any
        stale external reference resolves; do not re-wire the clock to this."""
        if s["act"] == 1:
            self._dusk(s)
        elif s["end_turn"] is None:
            self._trigger_end(s, "lasttrain")

    def _dusk(self, s):
        if s["act"] != 1:
            return
        s["act"] = 2
        s["dusk_turn"] = s["turn"]
        # §17: NIGHT starts on a fresh clock — reset the Closing-Time track + the deadlock tracker so the
        # night pool gets a full cycle before the first night roll and the day's static-count doesn't leak.
        s["track"] = 0
        s["faceup_sig"] = None
        s["static_rounds"] = 0
        rng = s["_rng"]
        # baseline endgame-tie resolver: force-clear any still-tied contested DAY stall
        if TIE_RESOLVER:
            self._resolve_all_ties(s, boundary="dusk", rng=rng)
        # judge held DAY bookings into the win/lose piles (frozen at dusk)
        for p in range(s["n"]):
            pl = s["players"][p]
            keep = []
            for key in pl["tickets"]:
                if BOOKINGS[key]["phase"] == 1:
                    # §15.9: completed DAY tour → full VP; unfinished at dusk → CANCELLED pile (its −⌊V/2⌋
                    # penalty, still sheddable by a night CLEAR/SALVAGE — the pile persists into night).
                    if _booking_done(key, pl["won"]):
                        pl["day_book_score"] += BOOKINGS[key]["value"]
                    else:
                        pl["cancelled"].append(BOOKINGS[key]["value"])
                else:
                    keep.append(key)
            pl["tickets"] = keep
        # sweep the day layer: uncommitted followers on cleared UNCLAIMED day stalls → owners' BOARDS
        night_decks = s["night_decks"]   # §17.6 per-count SUBSET night pool, pre-decided at setup
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                for q in range(s["n"]):
                    if s["fol"].get(vid, [0] * s["n"])[q] > 0:
                        s["players"][q]["board"] += s["fol"][vid][q]
                s["fol"][vid] = [0] * s["n"]
                s["star"].discard(vid)
            nd = night_decks[r]
            up = [nd.pop() for _ in range(min(s["slots"][r], len(nd)))]
            s["vdeck"][r] = nd; s["faceup"][r] = up
            for vid in up:
                s["fol"].setdefault(vid, [0] * s["n"])
                if vid == N07_ID:
                    s["n07_surfaced"] = True
            # §16.4 PHASE-TO-BOX: the day market deck + its face-up discard go to the BOX; build the fresh
            # NIGHT market deck (night ingredient cards + dealt night events) with an empty night discard.
            _build_market(s, r, 2, rng)
        # §16.4 Larder cards survive dusk (Option A) but become CONCLUDED-phase: carried day cards move to
        # `larder_prev` so a later spend routes them to the box, never the night discard.
        for q in range(s["n"]):
            plq = s["players"][q]
            plq["larder_prev"] += plq["larder"]
            plq["larder"] = Counter()
        s["commit_turn"] = {}
        self._sample_pantry_min(s)
        # deal the NIGHT booking deck (§17.6 CO-SCALED to the completable night tour pool decided at setup)
        nd = self._build_booking_deck(s["night_keys"], s["night_size"], rng)
        s["mrow"] = [nd.pop() for _ in range(min(s["mrow_w"], len(nd)))] if nd else []
        s["mreserve"] = nd

    def _resolve_all_ties(self, s, boundary, rng):
        """§2.6 baseline resolver: every still-tied contested stall force-resolves to most-followers →
        earliest committer; that agent claims (paying if able), losers → own supply. §12.3 interaction 2:
        the min-follower FLOOR still applies — a stall whose TOP crowd is BELOW the floor is NOT force-
        claimed; it clears UNCLAIMED (followers home). If the winner cannot pay, the stall likewise clears."""
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                fol = s["fol"].get(vid, [0] * s["n"])
                committers = [q for q in range(s["n"]) if fol[q] > 0]
                if len(committers) < 2:
                    continue
                s["frozen_at_boundary"] += 1
                top = max(fol)
                top_players = [q for q in committers if fol[q] == top]
                winner = min(top_players, key=lambda q: s["commit_turn"].get((vid, q), 10 ** 9))
                floor = VENDORS[vid]["floor"]
                # §12.2/§12.3: below-floor top crowd → clears UNCLAIMED (not a denied prize; no stranding)
                if top < floor or not self._can_afford(s, winner, vid):
                    if top < floor:
                        s["below_floor_blocks"] += 1
                    for q in committers:
                        if boundary == "dusk":
                            s["players"][q]["board"] += fol[q]
                        else:
                            s["players"][q]["supply_f"] += fol[q]
                    s["fol"][vid] = [0] * s["n"]
                    continue
                s["resolver_fires"] += 1
                for t, c in self._pay_plan(s, winner, vid).items():
                    for _ in range(c):
                        self._spend_one(s, s["players"][winner], t)
                self._award(s, winner, vid, contested=True, rng=rng)

    def _trigger_end(self, s, cause):
        if s["end_turn"] is not None:
            return
        s["end_cause"] = cause
        s["last_turn"] = s["turn"]
        n = s["n"]; done = s["turn"] + 1
        s["end_turn"] = ((done + n - 1) // n) * n + n   # finish the round so everyone gets equal turns

    def _finalize(self, s):
        if s["_finalized"]:
            return
        s["_finalized"] = True
        rng = s["_rng"]
        if TIE_RESOLVER:
            self._resolve_all_ties(s, boundary="lasttrain", rng=rng)
        for p in range(s["n"]):
            pl = s["players"][p]
            # §15.9: completed NIGHT tour → full VP; unfinished-at-last-train → CANCELLED pile (game over,
            # so its penalty stands). Scoring pulls the pile penalty in _booking_vp.
            night = 0
            for key in pl["tickets"]:
                # LAST TRAIN judges night (2) AND agnostic "any" (3) tours; day (1) tours were already
                # frozen at dusk (§20/§21: an "any" tour is satisfiable across the whole game).
                if BOOKINGS[key]["phase"] == 1:
                    continue
                if _booking_done(key, pl["won"]):
                    night += BOOKINGS[key]["value"]
                    if key in TRACKED_TOURS:
                        s["tour_completed"][key] += 1
                else:
                    pl["cancelled"].append(BOOKINGS[key]["value"])
            pl["night_book_score"] = night

    # -------- sourcing / Larder cap --------
    def _larder_cap(self, pl):
        return AMA_LARDER_CAP if pl["char"] == "globetrotter" else LARDER_CAP

    # -------- §16 explicit market deck-flow (draw / reshuffle / discard / phase-to-box) --------
    def _sample_pantry_min(self, s):
        """§16.5 guard: track the minimum recyclable Pantry (糧) card count in East's deck + discard."""
        cnt = sum(1 for c in s["deck"].get("E", []) if c[0] == "I" and c[1] == "pantry")
        cnt += sum(1 for c in s["disc"].get("E", []) if c[0] == "I" and c[1] == "pantry")
        s["pantry_supply_min"] = min(s["pantry_supply_min"], cnt)

    def _draw_card(self, s, r, rng):
        """Draw the top card of region r's live deck. On deck-out, RESHUFFLE the face-up current-phase
        discard into the deck (§16.2) — asserting phase-purity (the night-only guarantee, §16.4). Returns
        an ("I",type,phase) / ("E",idx,phase) card, or None if both deck and discard are empty."""
        if not s["deck"][r]:
            disc = s["disc"][r]
            if disc:
                for c in disc:                                   # PHASE-TO-BOX correctness check
                    assert c[2] == s["act"], f"phase leak: {c} in {r} discard during act {s['act']}"
                s["reshuffles"][(r, s["act"])] += 1
                s["reshuffle_sizes"][(r, s["act"])].append(len(disc))
                rng.shuffle(disc)
                s["deck"][r] = disc
                s["disc"][r] = []
        if not s["deck"][r]:
            s["empty_draws"] += 1
            return None
        dk = s["deck"][r]
        s["evfrac_samples"][(r, s["act"])].append(sum(1 for c in dk if c[0] == "E") / len(dk))
        card = dk.pop()
        if r == "E":
            self._sample_pantry_min(s)
        return card

    def _discard_card(self, s, r, card):
        """A spent / fired / forced / passed-over CURRENT-phase market card → region r's face-up discard."""
        s["disc"][r].append(card)

    def _keep_ing(self, s, p, r, card):
        """Keep an ingredient card into the current-phase Larder (records the sourcing-share probe)."""
        pl = s["players"][p]
        t = card[1]
        pl["larder"][t] += 1
        s["src_by_type"][t] += 1

    # -------- §15 EVENTS — VERB · SCOPE · DURATION, wired to the real subsystems --------
    def _leaders(self, s):
        """Leader set by the game's own tiebreak order (§15.5): most completed tours → most vendors →
        most board followers."""
        def key(q):
            pl = s["players"][q]
            return (len(pl["counted_done"]), len(pl["won"]), pl["board"])
        best = max(key(q) for q in range(s["n"]))
        return [q for q in range(s["n"]) if key(q) == best]

    def _standings_key(self, s, q):
        pl = s["players"][q]
        return (len(pl["counted_done"]), len(pl["won"]), pl["board"])

    def _lowest_scorers(self, s):
        """§15.9 SALVAGE targeting — the inverse of _leaders: fewest Completed → fewest vendors → fewest
        board followers. The standings pick the trailer; the drawer never free-picks (no kingmaking)."""
        worst = min(self._standings_key(s, q) for q in range(s["n"]))
        return [q for q in range(s["n"]) if self._standings_key(s, q) == worst]

    def _do_clear(self, s, p):
        """CLEAR: shed ONE of your own Cancelled tours (highest value = biggest −⌊V/2⌋ relief) to the box.
        Fizzle if you hold none. Returns the ⌊V/2⌋ relief (0 on fizzle)."""
        pile = s["players"][p]["cancelled"]
        if not pile:
            return 0
        v = max(pile)
        pile.remove(v)
        s["clear_fires"] += 1
        s["clear_relief"] += v // 2
        return v // 2

    def _do_salvage(self, s, p):
        """SALVAGE: auto-target the lowest-scoring rival holding a Cancelled tour; they shed its −⌊V/2⌋, the
        salvaged tour enters the DRAWER's Completed at HALF value ⌊V/2⌋. Graceful degrade → CLEAR own; else
        fizzle. (The only event that reaches a Completed pile, and never a leader's — cannot compound a lead.)"""
        trailers = [q for q in self._lowest_scorers(s) if q != p and s["players"][q]["cancelled"]]
        if not trailers:
            # widen to ANY rival with a cancelled tour, still standings-ordered (never the drawer's free pick)
            ranked = sorted((q for q in range(s["n"]) if q != p and s["players"][q]["cancelled"]),
                            key=lambda q: self._standings_key(s, q))
            trailers = ranked[:1]
        if not trailers:
            if self._do_clear(s, p) > 0:                 # graceful degrade to a self-CLEAR
                return
            s["salvage_fizzles"] += 1
            return
        q = trailers[0]
        v = max(s["players"][q]["cancelled"])            # the tour they'd most benefit shedding
        s["players"][q]["cancelled"].remove(v)
        s["players"][p]["salvage_score"] += v // 2       # drawer's half-value Completed (the bounded boon)
        s["salvage_fires"] += 1
        s["salvage_gain_drawer"] += v // 2
        s["salvage_relief_trailer"] += v // 2

    def _scope_targets(self, s, p, ev, r):
        """Who an event hits, from its scope icon, resolved relative to the drawn region r."""
        sc = ev["scope"]
        if sc == "self":
            return [p]
        if sc == "board":
            return list(range(s["n"]))
        if sc == "region":
            return [q for q in range(s["n"]) if s["players"][q]["pos"] == r]
        if sc == "neighbour":
            nb = set(neighbours(r, None, self._hsr_open(s)))
            return [q for q in range(s["n"]) if s["players"][q]["pos"] in nb]
        if sc == "rival":
            # ✦ loss auto-targets the LEADER; CD tied-leader refinement — hits ALL tied leaders EXCLUDING
            # the drawer; fizzles if the drawer is the sole/only-remaining top.
            leaders = [q for q in self._leaders(s) if q != p]
            if not leaders:
                s["ev_leader_fizzles"] += 1
                return None                                      # fizzle: drawer is sole leader
            if ev["kind"] == "hazard":
                # §15.5 rail 6 (the "light catch-up VALVE, not a beating" binding): NO PILE-ON. A leader
                # already ✦-nudged NUDGE_CAP times this round is not hit again — one nudge/leader/round is
                # the ceiling. If every tied leader is capped out, the whole ✦ hazard fizzles this round.
                eligible = [q for q in leaders if s["nudged_this_round"][q] < NUDGE_CAP]
                if not eligible:
                    s["nudge_pileon_blocked"] += 1
                    s["ev_leader_fizzles"] += 1
                    return None
                for q in eligible:
                    s["nudged_this_round"][q] += 1
                    s["players"][q]["nudges_taken"] += 1
                    # cumulative leader ✦-impact (magnitude is always 1 per rail 1): the DESIGN/SIM target
                    # that this stays MILD across a whole game (§15.5 binding, §15.7 probe 2).
                    s["players"][q]["nudge_impact"] += ev["value"]
                    s["leader_nudge_impact"] += ev["value"]
                s["ev_leader_fires"] += 1
                return eligible
            s["ev_leader_fires"] += 1
            return leaders
        return [p]

    def _steal_one(self, s, thief, victim, typ):
        """SWIPE: move 1 ingredient (named type or any) from victim → thief's current-phase Larder."""
        pv = s["players"][victim]
        cands = [typ] if typ and typ != "any" else \
            [t for t in list(pv["larder"]) + list(pv["larder_prev"]) if self._have(pv, t) > 0]
        for t in cands:
            if pv["larder"].get(t, 0) > 0:
                pv["larder"][t] -= 1
            elif pv["larder_prev"].get(t, 0) > 0:
                pv["larder_prev"][t] -= 1
            else:
                continue
            s["players"][thief]["larder"][t] += 1
            s["swipes"] += 1
            return

    def _spoil_one(self, s, q, typ, r):
        """SPOIL: a held ingredient of the named type(s) (or any) goes off → region discard (§16 feeder 4)."""
        pl = s["players"][q]
        types = [x for x in typ.split(";")] if (typ and typ != "any") else None
        cands = types if types else [t for t in list(pl["larder"]) + list(pl["larder_prev"])]
        for t in cands:
            if pl["larder"].get(t, 0) > 0:
                pl["larder"][t] -= 1
                self._discard_ingredient(s, t)          # current-phase card recycles
                s["spoils"] += 1
                return
            if pl["larder_prev"].get(t, 0) > 0:
                pl["larder_prev"][t] -= 1
                s["box_from_larder"] += 1               # stale card → box
                s["spoils"] += 1
                return

    def _fire_event(self, s, p, idx, r, during_visit):
        """Apply one event's VERB to its SCOPE with its DURATION persistence. Returns the PINCH amount to
        apply to THIS actor's current Visit keep (0 unless a pinch hit the visitor now)."""
        ev = EVENTS[idx]
        s["events_fired"] += 1
        s["ev_by_verb"][ev["verb"]] += 1
        # §15.9 TOURS boons have bespoke targeting (self / lowest-scorer), resolved before scope routing.
        if ev["verb"] == "clear":
            self._do_clear(s, p)
            return 0
        if ev["verb"] == "salvage":
            self._do_salvage(s, p)
            return 0
        aff = self._scope_targets(s, p, ev, r)
        if aff is None:
            return 0                                     # fizzled ✦
        verb, val, dur, tgt = ev["verb"], ev["value"], ev["duration"], ev["target"]
        pinch_here = 0
        turn_expiry = s["turn"] + s["n"]                 # ⏳TURN: covers exactly the affected player's next turn

        if verb == "rally":
            for q in aff:
                for _ in range(val):
                    self._grow(s, q, "event")
        elif verb == "disperse":
            for q in aff:
                for _ in range(val):
                    self._return_one_to_supply(s, q)
        elif verb == "gift":
            if tgt:                                      # a named ingredient windfall
                for q in aff:
                    s["players"][q]["larder"][tgt] += val
                    s["src_by_type"][tgt] += val
                    s["gifts"] += 1
            else:                                        # Golden Week — a ⏳ROUND "+val Visit keep" boon
                for q in aff:
                    s["players"][q]["visit_keep_bonus"] += val
        elif verb == "pinch":
            for q in aff:
                if q == p and during_visit:
                    pinch_here += val
                else:
                    s["players"][q]["tempo_tax"] += val
        elif verb == "spoil":
            for q in aff:
                self._spoil_one(s, q, tgt, r)
        elif verb == "swipe":
            for q in aff:
                self._steal_one(s, p, q, tgt)
        elif verb == "sink":
            if s["deck"][r]:
                s["deck"][r].insert(0, s["deck"][r].pop())   # top card → BOTTOM (stays live)
        elif verb == "trend":
            self._place_star(s, r)
        elif verb == "restock":
            self._fill_slot(s, r); s["restocks"] += 1
        elif verb == "wash":
            self._wash_region(s, r); s["washes"] += 1
        elif verb == "promote":
            if dur == "round":                           # Blogger — next Promote places +val
                for q in aff:
                    s["players"][q]["promote_bonus"] += val
            else:                                        # Anniversary — a free Promote now
                for q in aff:
                    self._free_promote(s, q)
        elif verb == "block":
            key = "block_" + (tgt.replace("-", "_") if tgt else "promote")
            for q in aff:
                if key in s["players"][q]:
                    s["players"][q][key] = turn_expiry
            s["blocks"] += 1
        elif verb == "detour":
            s["detours"] += 1
            if tgt == "hsr" and ev["kind"] == "boon":    # EV-N30 free HSR sprint (a self boon)
                pl = s["players"][p]
                if pl["pos"] in HSR:
                    pl["pos"] = HSR[1] if pl["pos"] == HSR[0] else HSR[0]
            elif tgt == "hsr":                           # HSR down (⏳TURN) for the affected agents
                for q in aff:
                    if s["players"][q]["char"] != "globetrotter":   # 阿嬤 immune
                        s["hsr_closed_until"][q] = turn_expiry
            else:                                        # link severed — approximate as a region travel-out lock
                s["region_out_block"][r] = s["round"]
        return pinch_here

    def _place_star(self, s, r=None):
        pool = ([vid for vid in s["faceup"].get(r, [])] if r else
                [vid for rr in REGIONS for vid in s["faceup"][rr]])
        cand = [vid for vid in pool if vid not in s["star"]]
        if cand:
            s["star"].add(min(cand, key=lambda vid: VENDORS[vid]["total_cost"]))

    def _wash_region(self, s, r):
        """WASH: clear the region's face-up vendor(s) (committed followers → owners' boards) and refill now."""
        for vid in list(s["faceup"][r]):
            for q in range(s["n"]):
                if s["fol"].get(vid, [0] * s["n"])[q] > 0:
                    s["players"][q]["board"] += s["fol"][vid][q]
            s["fol"][vid] = [0] * s["n"]
            s["star"].discard(vid)
            s["faceup"][r].remove(vid)
        while len(s["faceup"][r]) < s["slots"][r] and s["vdeck"][r]:
            nv = s["vdeck"][r].pop()
            s["faceup"][r].append(nv); s["fol"].setdefault(nv, [0] * s["n"])

    def _free_promote(self, s, q):
        """A free Promote (Market Anniversary): place up to 2 board followers on a co-located face-up stall."""
        pl = s["players"][q]
        if pl["board"] <= 0:
            return
        co = [vid for vid in s["faceup"].get(pl["pos"], [])]
        if co:
            self._place(s, q, co[0], min(2, pl["board"]))

    def _keep_cap(self, pl):
        base = 3 if pl["char"] == "bigeater" else 2
        return base + pl["visit_keep_bonus"]             # §15 Golden Week ⏳ROUND boon

    def _visit_target(self, pl):
        """§18 straight-draw keep-count: Big Eater 大胃王 → 3, Homebody 媽寶 → 1 (his lane is Travel-forage,
        §6.5), everyone else → 2; + the Golden Week ⏳ROUND boon."""
        if pl["char"] == "homebody":
            base = 1
        elif pl["char"] == "bigeater":
            base = 3
        else:
            base = 2
        return base + pl["visit_keep_bonus"]

    def _sample_visit_choice(self, s, types):
        """§18 M1 probe: a Visit offered a real keep-choice iff ≥2 distinct ingredient TYPES turned up.
        Under straight-draw (A) this reads ~0 by design (the choice moved to the map); under keep-2 it
        reads whatever the flip-3 window actually supported (the CD's 'is it a choice or a chore')."""
        if len(set(types)) >= 2:
            s["visit_choice_offered"] += 1

    def _do_visit(self, s, p, rng):
        pl = s["players"][p]
        r = pl["pos"]
        s["visits"] += 1; pl["fp_src_visit"] += 1
        # §15 BLOCK [draw] (⏳TURN): the market is shut for this agent — no cards this Visit
        if pl["block_draw"] >= s["turn"]:
            return
        if VISIT_MODE == "keep2":
            self._visit_keep2(s, p, r, rng)
        else:
            self._visit_straight(s, p, r, rng)

    def _ingredients_left(self, s, r):
        """§18.2 exhaustion clause: how many INGREDIENT cards are still obtainable from region r (live deck
        + its face-up discard). The straight-draw loop stops when this hits 0 — you cannot 'keep drawing
        until 2 ingredients' out of an all-event pile. This is the fix for the straight-draw × §16-recycling
        event-spin (fired events recycle, so the deck is never card-empty, but its INGREDIENTS can run out)."""
        n = sum(1 for c in s["deck"].get(r, []) if c[0] == "I")
        n += sum(1 for c in s["disc"].get(r, []) if c[0] == "I")
        return n

    def _visit_straight(self, s, p, r, rng):
        """§18.2 Option A (BASELINE): draw straight to the keep-count; an event fires at once and does NOT
        count (feeder-1 eliminated — no passed-over card). Fired events are held OUT until the Visit ends
        so they cannot reshuffle back and re-fire within the same Visit. Stop at the keep-count OR when no
        ingredients remain (the exhaustion clause). PINCH/tempo tax = keep 1 fewer; Big Eater digs a greedy
        4th (returns 1 follower); his hazards bite twice."""
        pl = s["players"][p]
        target = self._visit_target(pl)
        kept, seen, fired = [], [], []

        def _dig():
            """Pull the next INGREDIENT, firing (and holding) any events on the way; None if none remain."""
            while len(kept) < target or True:
                if self._ingredients_left(s, r) <= 0:
                    return None
                c = self._draw_card(s, r, rng)
                if c is None:
                    return None
                if c[0] == "E":
                    pn = self._fire_event(s, p, c[1], r, during_visit=True)
                    if pl["char"] == "bigeater":
                        pn *= 2                           # 大胃王 flaw: hazards bite TWICE
                    fired.append(c)                       # HELD — discarded only after the Visit (no mid-refire)
                    if pn:
                        return ("PINCH", pn)
                    continue
                return c

        while len(kept) < target:
            c = _dig()
            if c is None:
                break
            if isinstance(c, tuple) and c[0] == "PINCH":
                target = max(0, target - c[1])
                continue
            kept.append(c); seen.append(c[1])
        if pl["tempo_tax"] > 0 and target > 0:           # weather ⏳ tempo tax = one fewer kept
            pl["tempo_tax"] -= 1; target = max(0, target - 1)
        # 大胃王 greedy 4th: dig ONE more ingredient, keep it, return 1 follower to supply (the greed sink)
        if pl["char"] == "bigeater" and self._hungry(s, p):
            ex = _dig()
            while isinstance(ex, tuple) and ex[0] == "PINCH":   # a pinch surfaced — shrink target, dig again
                target = max(0, target - ex[1]); ex = _dig()
            if ex is not None:                               # a real ingredient card ("I", type, phase)
                kept.append(ex); seen.append(ex[1]); target += 1
                for _ in range(BIGEATER_COST):
                    self._return_one_to_supply(s, p)
        for c in kept[:target]:
            self._keep_ing(s, p, r, c)
        for c in kept[target:]:
            self._discard_card(s, r, c)                  # a pinch shrank the keep below what we drew
        for c in fired:
            self._discard_card(s, r, c)                  # §16 feeder 3: fired events recycle AFTER the Visit
        # §18.5 M1: straight-draw offers NO keep-choice by design (you keep all you draw) → leave at 0.

    def _visit_keep2(self, s, p, r, rng):
        """§18.4 cell 2 CONTROL (status-quo): flip 3, fire events, keep up to the cap, discard the rest
        (feeder-1 alive). The non-choice the CD diagnosed — kept switchable so bg-playtest A/Bs it vs A."""
        pl = s["players"][p]
        cards = [self._draw_card(s, r, rng) for _ in range(3)]
        ings = [c for c in cards if c is not None and c[0] == "I"]
        events = [c for c in cards if c is not None and c[0] == "E"]
        pinch = 0
        for c in events:
            pinch += self._fire_event(s, p, c[1], r, during_visit=True)
            self._discard_card(s, r, c)                  # §16 feeder 3: a fired event → discard (recurs)
        if pl["char"] == "bigeater":
            pinch *= 2                                   # 大胃王 flaw: hazards bite TWICE on his Visit
        keep = max(0, self._keep_cap(pl) - pinch)
        keep = max(0, self._apply_tempo(pl, keep))
        # 大胃王 greedy 4th: keep one extra, then RETURN 1 follower to your supply (the greed sink)
        if pl["char"] == "bigeater" and len(ings) > keep and self._hungry(s, p):
            keep += 1
            for _ in range(BIGEATER_COST):
                self._return_one_to_supply(s, p)
        for c in ings[:keep]:
            self._keep_ing(s, p, r, c)
        for c in ings[keep:]:
            self._discard_card(s, r, c)                  # §16 feeder 1: passed-over → discard
        # §18.5 M1: a real keep-choice existed iff you drew MORE ingredients than you kept AND ≥2 distinct
        # types were on offer (you actually chose which types to take, not a forced keep-everything).
        if len(ings) > keep:
            self._sample_visit_choice(s, [c[1] for c in ings])

    def _apply_tempo(self, pl, keep):
        if pl["tempo_tax"] > 0 and keep > 0:
            pl["tempo_tax"] -= 1
            return keep - 1
        return keep

    def _hungry(self, s, p):
        for vid in self._board(s):
            if VENDORS[vid]["is_drink"]:
                continue
            if not self._can_afford(s, p, vid):
                return True
        return False

    def _do_cstore(self, s, p, r, rng):
        pl = s["players"][p]
        s["cstores"] += 1; pl["fp_src_cstore"] += 1
        if pl["block_draw"] >= s["turn"]:
            return
        c = self._draw_card(s, r, rng)
        if c is None:
            return
        if c[0] == "I":
            if self._apply_tempo(pl, 1) > 0:
                self._keep_ing(s, p, r, c)
            else:
                self._discard_card(s, r, c)
        else:
            self._fire_event(s, p, c[1], r, during_visit=False)
            self._discard_card(s, r, c)

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        # grow your following (Travel +1: supply → board). Homebody grow-tick switchable (reserve g′);
        # §15 BLOCK [travel-grow] (⏳TURN) suppresses the grow this Travel.
        if pl["block_travel_grow"] < s["turn"]:
            self._grow(s, p, "travel")
        # 阿嬤 Travel-anywhere COSTS 1 follower to supply (baseline ON: "the trip tires her crowd")
        if pl["char"] == "globetrotter" and AMA_TRAVEL_COST:
            if pl["board"] > 0:
                pl["board"] -= 1; pl["supply_f"] += 1; s["ama_travel_cost_paid"] += 1
        # 媽寶 is the SOLE Travel-sourcer: draw HOMEBODY_DRAW (2) cards of the region she LEFT, keep all.
        # §15 BLOCK [travel] = "arrives with no ingredient" → suppress the travel-source this Travel.
        if pl["char"] == "homebody" and pl["block_travel"] < s["turn"]:
            pl["fp_src_travel"] += 1
            for _ in range(HOMEBODY_DRAW):
                c = self._draw_card(s, src, rng)
                if c is None:
                    continue
                if c[0] == "I":
                    if self._apply_tempo(pl, 1) > 0:
                        self._keep_ing(s, p, src, c)
                    else:
                        self._discard_card(s, src, c)
                else:
                    self._discard_card(s, src, c)        # an event on a Travel fly-by whiffs (not fired) → discard

    def _discard_to_cap(self, s, pl):
        """Larder over the hand-limit: dump the most-plentiful token(s). A current-phase card → region
        discard; a stale carried card → box (§16.2 feeder 1 / §16.3 box)."""
        cap = self._larder_cap(pl)
        while self._larder_total(pl) > cap:
            cur = [k for k in pl["larder"] if pl["larder"][k] > 0]
            if cur:
                tok = max(cur, key=lambda k: pl["larder"][k])
                pl["larder"][tok] -= 1
                self._discard_ingredient(s, tok)
            else:
                tok = max((k for k in pl["larder_prev"] if pl["larder_prev"][k] > 0),
                          key=lambda k: pl["larder_prev"][k])
                pl["larder_prev"][tok] -= 1
                s["box_from_larder"] += 1

    # -------- scoring (§14 TWO-TRACK: completed-Booking VP + won-vendor VP) --------
    def _vendor_vp(self, pl):
        return sum(w["vp"] for w in pl["won"])

    def _booking_vp(self, pl):
        # §14/§15.9: completed-tour VP (day+night) + SALVAGE half-value Completed tours − Σ⌊V/2⌋ over the
        # still-standing Cancelled pile (CLEAR/SALVAGE shed entries from the pile, lightening this penalty).
        cancel_pen = sum(_cancel_pen_one(v) for v in pl["cancelled"])   # CANCEL_COST lever (half_value | flat:N)
        return pl["day_book_score"] + pl["night_book_score"] + pl["salvage_score"] - cancel_pen

    def scores(self, s):
        if not s["_finalized"]:
            self._finalize(s)
        out = {}
        for p in range(s["n"]):
            pl = s["players"][p]
            base = self._booking_vp(pl) + self._vendor_vp(pl)   # §14 two-track final score
            st = _wstat(pl["won"])
            tie = 1e-3 * st["n"] + 1e-4 * len(st["regions"])   # tiebreak: most vendors → most regions
            out[p] = base + tie
        return out

    def metrics(self, s):
        sc = self.scores(s)
        vals = sorted(sc.values(), reverse=True)
        margin = vals[0] - vals[1] if len(vals) > 1 else 0.0
        best = max(sc.values())
        winners = [p for p, v in sc.items() if v == best]
        total_wins = s["food_wins"] + s["drink_wins"]
        n = s["n"]
        src = s["src_by_type"]; src_tot = sum(src.values()) or 1
        claims = s["claims"] or 1
        best_streak = max(pl["best_win_streak"] for pl in s["players"])
        # booking completion across the field
        held_or_done = sum(len(pl["counted_done"]) for pl in s["players"])

        def share(t):
            return src[t] / src_tot

        # §14 two-track scoring diagnostics: the WINNER's vendor-VP share of their winning score
        wp = winners[0]
        w_vendor = self._vendor_vp(s["players"][wp])
        w_book = self._booking_vp(s["players"][wp])
        w_total = w_vendor + w_book
        vendor_vp_share = (w_vendor / w_total) if w_total > 0 else 0.0

        # §16 deck-flow reads: reshuffles/game, reshuffled-deck size, live-deck event-fraction (enrichment)
        def _rs(r, ph):
            return float(s["reshuffles"][(r, ph)])

        def _rsz(r, ph):
            v = s["reshuffle_sizes"][(r, ph)]
            return float(statistics.mean(v)) if v else 0.0

        def _evf(r, ph):
            v = s["evfrac_samples"][(r, ph)]
            return float(statistics.mean(v)) if v else 0.0

        return {
            "margin": float(margin),
            "tie": 1.0 if len(winners) > 1 else 0.0,
            "turns": float(s["turn"]), "turns_per_player": float(s["turn"] / n),
            "dusk_turn": float(s["dusk_turn"]) if s["dusk_turn"] is not None else float(s["turn"]),
            "last_turn": float(s["last_turn"]) if s["last_turn"] is not None else float(s["turn"]),
            "end_by_lasttrain": 1.0 if s["end_cause"] == "lasttrain" else 0.0,
            "end_by_stall": 1.0 if s["end_cause"] == "stall" else 0.0,
            "rounds": float(s["round"]),
            # ---- §17 CLOSING-TIME DIE + vendor-depletion clock instruments ----
            "die_rolls_per_game": float(s["die_rolls"]),
            "die_removals_per_game": float(s["die_removals"]),
            "die_removals_contested_per_game": float(s["die_removals_contested"]),
            "die_blank_frac": float(s["die_blanks"] / s["die_rolls"]) if s["die_rolls"] else 0.0,
            "die_noremovable_per_game": float(s["die_noremovable"]),
            "backstop_fires_per_game": float(s["backstop_fires"]),
            "first_night_win_turn": float(s["first_night_win_turn"]) if s["first_night_win_turn"] else float(s["turn"]),
            # ---- MAKE-OR-BREAK PROBE #1: does the battle happen more? (numerator + denominator) ----
            "claims_per_game": float(s["claims"]),
            "contested_claims_per_game": float(s["contested_claims"]),
            "contested_frac": float(s["contested_claims"] / claims),
            "night_claims_per_player": float(s["night_claims"] / n),
            "prestige_completions_per_game": float(s["prestige_completions"]),
            # ---- §14 TWO-TRACK scoring probes (vendor-only loses / tours dominate) ----
            "claims_per_player": float(s["claims"] / n),
            "apex_claims_per_player": float(s["apex_claims"] / n),
            "winner_vendor_vp": float(w_vendor),
            "winner_booking_vp": float(w_book),
            "vendor_vp_share_of_winner": float(vendor_vp_share),
            "below_floor_blocks_per_game": float(s["below_floor_blocks"]),
            # ---- §15 EVENT probes ----
            "events_fired_per_game": float(s["events_fired"]),
            "events_fired_per_player": float(s["events_fired"] / n),
            "ev_leader_fires_per_game": float(s["ev_leader_fires"]),
            "ev_leader_fizzles_per_game": float(s["ev_leader_fizzles"]),
            "swipes_per_game": float(s["swipes"]), "spoils_per_game": float(s["spoils"]),
            "gifts_per_game": float(s["gifts"]), "blocks_per_game": float(s["blocks"]),
            "detours_per_game": float(s["detours"]), "restocks_per_game": float(s["restocks"]),
            "washes_per_game": float(s["washes"]),
            # §15.5 cumulative leader ✦-impact (BINDING: must stay MILD) + the no-pile-on cap effect. The
            # win-rate-delta from being nudged is read across runs by bg-playtest; per-game we expose the
            # total impact + the WINNER's own nudges-taken (a leader who won despite being nudged).
            "leader_nudge_impact_per_game": float(s["leader_nudge_impact"]),
            "nudge_pileon_blocked_per_game": float(s["nudge_pileon_blocked"]),
            "winner_nudges_taken": float(s["players"][wp]["nudges_taken"]),
            "max_nudges_on_one_leader": float(max((pl["nudges_taken"] for pl in s["players"]), default=0)),
            # §15.9 SALVAGE swing + CLEAR relief (the catch-up double-boons). SALVAGE swing = drawer gain +
            # trailer relief; the guard is that it NARROWS the gap without leapfrogging an earned leader.
            "salvage_fires_per_game": float(s["salvage_fires"]),
            "salvage_gain_drawer_per_game": float(s["salvage_gain_drawer"]),
            "salvage_relief_trailer_per_game": float(s["salvage_relief_trailer"]),
            "salvage_swing_per_game": float(s["salvage_gain_drawer"] + s["salvage_relief_trailer"]),
            "clear_fires_per_game": float(s["clear_fires"]),
            "clear_relief_per_game": float(s["clear_relief"]),
            "cancelled_pile_field": float(sum(len(pl["cancelled"]) for pl in s["players"])),
            # §18 M1 Visit decision-density (straight-draw should read ~0 by design; keep-2 shows what the
            # flip-3 window supported) + M4/M2 companions live in the deck-flow / travel probes below.
            "visit_choice_frac": float(s["visit_choice_offered"] / s["visits"]) if s["visits"] else 0.0,
            "visit_mode_straight": 1.0 if VISIT_MODE == "straight" else 0.0,
            # ---- §16 DECK-FLOW probes (cycle-rate, thinning, event-enrichment, pantry supply) ----
            "reshuffles_E_night": _rs("E", 2), "reshuffles_N_night": _rs("N", 2),
            "reshuffle_size_E_night": _rsz("E", 2), "reshuffle_size_N_night": _rsz("N", 2),
            "evfrac_E_night": _evf("E", 2), "evfrac_N_night": _evf("N", 2),
            "evfrac_E_day": _evf("E", 1), "evfrac_N_day": _evf("N", 1),
            "pantry_supply_min": float(s["pantry_supply_min"]),
            "box_from_larder_per_game": float(s["box_from_larder"]),
            # ---- MAKE-OR-BREAK PROBE #2: sourcing/throughput health ----
            "src_share_meat_N": share("meat"), "src_share_tea_C": share("tea"),
            "src_share_seafood_S": share("seafood"), "src_share_pantry_E": share("pantry"),
            "src_share_sugar": share("sugar"), "src_share_veg": share("veg"),
            "empty_draws_per_game": float(s["empty_draws"]),
            "bookings_completed_field": float(held_or_done),
            "tours_completed_per_player": float(held_or_done / n),
            "cancels_per_game": float(s["cancels"]),
            # ---- §21 WILD BOOKING + counts-tag probes ----
            "books_faceup_per_game": float(s["books_faceup"]),
            "books_wild_per_game": float(s["books_wild"]),
            "wild_book_frac": float(s["books_wild"] / (s["books_faceup"] + s["books_wild"]))
                              if (s["books_faceup"] + s["books_wild"]) else 0.0,
            "wild_books_day_per_game": float(s["books_wild_day"]),
            "wild_books_night_per_game": float(s["books_wild_night"]),
            "wild_completed_per_game": float(s["wild_completed"]),
            "tours_in_play_per_game": float(s["books_faceup"] + s["books_wild"]),
            # ---- meeple economy ----
            "grow_total_per_game": float(s["grow_total"]),
            "grow_homebody_tick_per_game": float(s["grow_homebody_tick"]),
            "return_to_supply_per_game": float(s["return_to_supply"]),
            "max_committed_on_stall": float(s["max_committed_on_stall"]),
            "max_committed_by_player": float(s["max_committed_by_player"]),
            "promotes_per_game": float(s["promotes"]),
            "travels_per_game": float(s["travels"]),
            "visits_per_game": float(s["visits"]),
            "trending_grows_per_game": float(s["trending_grows"]),
            # ---- scarcity / tie ----
            "tie_blocks_per_game": float(s["tie_blocks"]),
            "resolver_fires_per_game": float(s["resolver_fires"]),
            "frozen_at_boundary_per_game": float(s["frozen_at_boundary"]),
            # ---- runaway ----
            "best_win_streak": float(best_streak),
            # ---- banked-board fingerprint (late-battler / lowball) + per-player peak board ----
            "max_board_any_player": float(max((pl["max_board"] for pl in s["players"]), default=0)),
            "winner_max_board": float(s["players"][wp]["max_board"]),
            # ---- fingerprint aggregates (contest-entry rate + resource-per-win, for lane distinctness) ----
            "contest_entries_field": float(sum(pl["fp_contest_entries"] for pl in s["players"])),
            "fol_per_win_field": (float(sum(pl["fp_fol_per_win"] for pl in s["players"]))
                                  / float(sum(pl["fp_wins"] for pl in s["players"]))
                                  if sum(pl["fp_wins"] for pl in s["players"]) else 0.0),
            # ---- live-decision density ----
            "avg_legal_actions": float(statistics.mean(s["legal_counts"])) if s["legal_counts"] else 0.0,
            "forced_turn_frac": float(s["forced_turns"] / len(s["legal_counts"])) if s["legal_counts"] else 0.0,
            # ---- per-lane probes ----
            "dage_edge_fire_rate": float(s["dage_edge_fires"] / s["dage_claims"]) if s["dage_claims"] else 0.0,
            "dage_edge_fires_per_game": float(s["dage_edge_fires"]),
            "ama_snipe_rate": float(s["ama_snipes"] / s["ama_claims"]) if s["ama_claims"] else 0.0,
            "ama_travel_cost_paid_per_game": float(s["ama_travel_cost_paid"]),
            "councillor_free_draws_per_game": float(sum(pl["fp_free_draws"] for pl in s["players"])),
            # ---- N07-orphan probe (the two flagged N07-dependent tours) ----
            "n07_surfaced": 1.0 if s["n07_surfaced"] else 0.0,
            "n07_won": 1.0 if s["n07_won"] else 0.0,
            "g_travel3d_held_per_game": float(s["tour_held"].get("g_travel3d", 0)),
            "g_travel3d_completed_per_game": float(s["tour_completed"].get("g_travel3d", 0)),
            "d_north2_held_per_game": float(s["tour_held"].get("d_north2", 0)),
            "d_north2_completed_per_game": float(s["tour_completed"].get("d_north2", 0)),
            # ---- claim geography ----
            "claim_share_N": s["claim_by_region"]["N"] / claims,
            "claim_share_C": s["claim_by_region"]["C"] / claims,
            "claim_share_S": s["claim_by_region"]["S"] / claims,
            "claim_share_E": s["claim_by_region"]["E"] / claims,
        }


GAME = TravelAgentsGame()
TITLE = ("Travel Agents: Taiwan — V7-M (Follower MEEPLES + VENDOR SCARCITY · six lanes · "
         "plurality [tie blocks] · 大哥 margin dial N · slow per-round refill · §17 VENDOR-DEPLETION clock "
         "+ Closing-Time die)")


# ==================================================================================================
#  SHARED PLANNER — one greedy brain; strategies differ in PREFS. SPREAD- & MARGIN-AWARE.
# ==================================================================================================
TEMPO = 1.1


def _needs(s, p, vid):
    pay = GAME._pay_plan(s, p, vid)
    pl = s["players"][p]
    return Counter({t: c - GAME._have(pl, t) for t, c in pay.items() if c - GAME._have(pl, t) > 0})


def _booking_marginal(s, p, vid, prefs):
    pl = s["players"][p]
    v = VENDORS[vid]
    cand = {"id": v["id"], "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "total_cost": v["total_cost"], "tier": v["tier"], "apex": v["apex"], "cross": v["cross"],
            "vp": v["vp"], "locale": v["locale"], "dish_type": v["dish_type"],
            "contested": False, "act_won": s["act"], "final_round": s["end_turn"] is not None}
    total = 0.0
    for key in pl["tickets"]:
        if _booking_done(key, pl["won"]):
            continue
        if _booking_helps(key, cand, pl["won"]):
            after = _booking_done(key, pl["won"] + [cand])
            val = BOOKINGS[key]["value"]
            total += (val * 0.85) if after else (val * 0.22)
    return total * prefs.get("w_ticket", 1.0)


def _road_value(s, p, vid, prefs):
    pl = s["players"][p]
    v = VENDORS[vid]
    core = 1.0 + 0.35 * v["total_cost"]                         # engine-quality proxy (bigger dish = more ramp)
    if not v["is_drink"] and v["icon"]:
        core += prefs.get("w_ramp", 1.0) * (0.5 + 0.4 * pl["icons"].get(v["icon"], 0))
    core *= prefs.get("w_food", 1.0) if not v["is_drink"] else prefs.get("w_drink", 1.0)
    if prefs.get("marquee") and (v["apex"] or v["total_cost"] >= 3):
        core += 1.5
    return core * prefs.get("w_val", 1.0) + _booking_marginal(s, p, vid, prefs)


def _est_actions(s, p, vid):
    pl = s["players"][p]
    need = sum(_needs(s, p, vid).values())
    add = GAME._needed_to_win(s, p, vid)
    reg = VENDORS[vid]["region"]
    travel = 0 if pl["pos"] == reg else _dist(pl["pos"], reg, pl["char"], GAME._hsr_open(s))
    return 0.7 * need + 0.6 * add + travel + 1.0


def _pick_target(s, p, prefs):
    pl = s["players"][p]
    best, bscore = None, -1e9
    for vid in GAME._board(s):
        v = VENDORS[vid]
        if prefs.get("no_drinks") and v["is_drink"]:
            continue
        val = _road_value(s, p, vid, prefs)
        score = val - TEMPO * (_est_actions(s, p, vid) - 1.0)
        if s["fol"][vid][p] > 0:
            score += 0.4
        # FEASIBILITY: don't pile into a stall you cannot win even by emptying your whole pool (the
        # deadlock trap under scarcity) — gravitate to WINNABLE stalls so vendor claims actually close.
        add = GAME._needed_to_win(s, p, vid)
        reachable = pl["board"] + pl["supply_f"]
        if add > reachable:
            score -= 6.0
        else:
            score -= 0.5 * add
        rival = max((s["fol"][vid][q] for q in range(s["n"]) if q != p), default=0)
        if prefs.get("avoid_contest") and rival > 0:
            score -= 2.0 + 1.5 * rival                          # 媽寶 dodge: take the straight, quiet win
        if prefs.get("contest") and rival > 0:
            score += 2.0 + 1.0 * rival                          # brawler: hunt the rival's lock-in
        if prefs.get("late_battle") and s["act"] == 2 and v["tier"] >= 2:
            score += 2.5                                        # banked-board late-battler: crash the marquee
        # --- archetype tilts (each carves a DISTINCT behavioural fingerprint) ---
        if prefs.get("rush"):                                   # tempo: cheap, present, low-add wins fast
            if v["total_cost"] <= 2:
                score += 1.6
            score -= 0.4 * v["total_cost"]
            if GAME._present(s, p, vid):
                score += 0.8
        if prefs.get("engine") and not v["is_drink"] and v["icon"]:
            score += 1.2 * (1 + pl["icons"].get(v["icon"], 0))  # economy: stack same-region icons → discounts
        if prefs.get("concentrate") and v["region"] == pl["pos"]:
            score += 1.3                                        # pile in one region (deny spread)
        if prefs.get("spread") and v["region"] not in {w["region"] for w in pl["won"]}:
            score += 1.5                                        # breadth: a new region each time
        if prefs.get("snipe"):                                  # seat/open-info: grab uncontested + winnable NOW
            if rival == 0 and add <= pl["board"] and GAME._present(s, p, vid):
                score += 3.0
            elif rival > 0:
                score -= 1.5                                    # never brawl — snipe only the quiet, ready stalls
        if score > bscore:
            bscore, best = score, vid
    return best


def _pick_target_human(s, p, prefs):
    """CLAIM-HUNGRY realistic picker (the honest baseline the band is measured against). A sharp human
    chasing Bookings claims the vendors those Bookings need AND clears the stalls that pay off FASTEST —
    so this maximises VALUE-PER-TURN rather than raw value: vendor VP + the Bookings a stall advances +
    a little icon-ramp, all divided by the estimated turns to bring the claim home (travel + source +
    the follower fight). Two velocity levers a naive re-pick-every-turn brain lacks:
      * TARGET STICKINESS — a stall you already committed followers to (×1.5), or last turn's focus
        (×1.25), is favoured, so the bot FINISHES claims instead of thrashing and wasting sourced
        ingredients (the #1 cause of the 4-travel/4-visit-per-claim overhead the action-mix probe found);
      * a QUIET-WIN tempo bonus (×1.2) for an uncontested stall it already stands on and can win now.
    Feasibility-gated (never fixates on a stall it cannot win even by emptying its whole pool) and
    spread/margin-aware via _needed_to_win, exactly like the fair picker. Fidelity: this is a PREF flag on
    the one shared brain — every seat/character that carries `human` gets the identical policy (no seat is
    juiced), and the six character lanes inherit it uniformly (see LANE_H)."""
    pl = s["players"][p]
    reachable = pl["board"] + pl["supply_f"]
    focus = pl.get("_focus")
    best, bscore = None, -1e9
    for vid in GAME._board(s):
        v = VENDORS[vid]
        if prefs.get("no_drinks") and v["is_drink"]:
            continue
        add = GAME._needed_to_win(s, p, vid)
        if add > reachable:
            continue                                       # unwinnable this game → don't fixate (no deadlock)
        val = v["vp"] + _booking_marginal(s, p, vid, prefs)
        if not v["is_drink"] and v["icon"]:
            val += 0.3 * pl["icons"].get(v["icon"], 0)      # ramp: same-region icons discount future claims
        if prefs.get("marquee") and v["apex"]:
            val += 1.0
        est = _est_actions(s, p, vid)                       # ~turns to travel + source + win this stall
        score = val / max(1.0, est)                         # VALUE PER TURN — the claim-velocity brain
        if s["fol"][vid][p] > 0:
            score *= 1.5                                    # already invested here → finish it (anti-thrash)
        if vid == focus:
            score *= 1.25                                   # last turn's plan → stick unless clearly beaten
        rival = max((s["fol"][vid][q] for q in range(s["n"]) if q != p), default=0)
        if rival == 0 and GAME._present(s, p, vid):
            score *= 1.2                                    # a ready, quiet win → grab it, keep tempo
        if prefs.get("avoid_contest") and rival > 0:
            score *= 0.5
        if prefs.get("contest") and rival > 0:
            score *= 1.3
        if prefs.get("spread") and v["region"] not in {w["region"] for w in pl["won"]}:
            score *= 1.2
        if score > bscore:
            bscore, best = score, vid
    pl["_focus"] = best                                     # bot-only scratch (no game rule reads it)
    return best


def _token_source(s, p, tok, legal):
    pl = s["players"][p]
    targets = list(COMMONS[tok]) if _is_common(tok) else [TYPE_SIG_REGION[tok]]
    if pl["pos"] in targets and ("visit",) in legal:
        return ("visit",)
    dest = min(targets, key=lambda r: _dist(pl["pos"], r, pl["char"], GAME._hsr_open(s)))
    hop = _next_hop(pl["pos"], dest, pl["char"], GAME._hsr_open(s))
    if ("travel", hop) in legal:
        return ("travel", hop)
    for r in targets:
        if ("cstore", r) in legal:
            return ("cstore", r)
    return None


def _co_located_targets(s, p):
    """Face-up stalls in the player's current region (for spread decisions)."""
    r = s["players"][p]["pos"]
    return [vid for vid in s["faceup"].get(r, [])]


def _deny_target(s, p):
    """DENIER/KINGMAKER exploit line: find the highest-VP face-up stall a RIVAL currently out-commits the
    denier on AND the denier could MATCH (creating a top-tie → plurality tie BLOCKS the claim). Returns
    (vid, gap_to_tie) or None. Tests whether the tie-resolver + floor + 大哥 margin defeat perpetual denial
    (matching a Big-Brother rival does NOT deny — he wins ties at N=1, the design's built answer)."""
    pl = s["players"][p]
    best, bv = None, -1
    for r in REGIONS:
        for vid in s["faceup"].get(r, []):
            fol = s["fol"][vid]
            mine = fol[p]
            top_rival = max((fol[q] for q in range(s["n"]) if q != p), default=0)
            if top_rival <= mine or top_rival <= 0:
                continue                                   # no rival lock-in to deny here
            gap = top_rival - mine
            if gap > pl["board"] + pl["supply_f"]:
                continue                                   # cannot plausibly reach the tie
            v = VENDORS[vid]["vp"]
            if v > bv:
                bv, best = v, (vid, gap)
    return best


def _row_suitable(s, p):
    """§21 WILD-BOOK trigger (rational, spec-faithful): does the FACE-UP Booking row show a tour this
    player could realistically COMPLETE — a NEW, low-claim-gap objective? If yes, take the KNOWN face-up
    tour (never gamble blind when a suitable face-up exists). If no, the row is 'barren' and the rational
    line is a wild (blind) Book. Budget = plausible remaining claim headroom (thin at 3p, wider at 4–6p)."""
    pl = s["players"][p]
    budget = 3 if s["n"] == 3 else 4
    st = _wstat(pl["won"])
    for k in s["mrow"]:
        if k in pl["tickets"]:
            continue                                   # already held → not a reason to Book
        d, need = BOOKINGS[k]["progress"](st)
        if (need - d) <= budget:
            return True
    return False


def _book_action(s, p):
    """Choose the Book variant: a KNOWN face-up claim when the row is suitable; else a blind WILD book
    (only when barren, deck has cards, and the lever is on) — the §21.2 self-selecting fallback."""
    if _wild_book_on() and s["mreserve"] and not _row_suitable(s, p):
        return ("wild_book",)
    if s["mrow"]:
        return ("claim",)
    if _wild_book_on() and s["mreserve"]:
        return ("wild_book",)
    return None


def _plan(s, p, legal, rng, prefs):
    pl = s["players"][p]
    if legal == [("pass",)]:
        return ("pass",)

    # 1) a Bribe that helps always progresses
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs.get("no_drinks") and VENDORS[a[1]]["is_drink"])]
    if bribes:
        return max(bribes, key=lambda a: _road_value(s, p, a[1], prefs))

    # 1d) DENIER/KINGMAKER: before anything else, chase a top-tie on a stall a rival is locking (tie
    #     blocks the claim). Route to it, then Promote to MATCH the rival (never exceed → stay a tie).
    if prefs.get("deny"):
        dt = _deny_target(s, p)
        if dt is not None:
            vid = dt[0]
            if not GAME._present(s, p, vid):
                hop = _next_hop(pl["pos"], VENDORS[vid]["region"], pl["char"], GAME._hsr_open(s))
                if ("travel", hop) in legal:
                    return ("travel", hop)
            elif pl["board"] > 0 and GAME._promote_ok(s, p, vid):
                return ("promote", vid)                    # top up toward the tie (2/turn until matched)
            elif ("visit",) in legal:
                return ("visit",)                          # board empty → grow via sourcing, come back

    # 2) maintain a working hand of objectives (drawing Bookings drives the deck-clock). Under the
    #    hand-limit: claim. AT the hand-limit: CANCEL-TO-CLAIM only for a CLEARLY hotter Booking (the
    #    row offers something >1.3× the worst STALE held one) — a bounded valve that unsticks a hand of
    #    uncompletable Bookings (else the night deck never drains → the game runs to the stall) WITHOUT
    #    churning a good hand or crowding out vendor-winning.
    #    Bots maintain a working hand of WORK_HAND objectives (< HAND_LIMIT) so most turns go to
    #    vendor-work, not claiming; the deck-clock still drains because COMPLETING a Booking (a vendor
    #    win) frees its slot → a fresh claim. A bounded cancel-valve unsticks a fully-stale hand.
    # a claim-hungry human books MORE ambitiously when cancelling is cheap (flat:1) — the downside of
    # holding a big-but-incomplete tour is capped, so the working hand widens. Faithful incentive model of
    # the CANCEL_COST lever's intent; the load-bearing hoarder read is pure scoring (needs no bot change).
    _cc = _cancel_cost()
    _cheap_cancel = _cc.startswith("flat:") and int(_cc.split(":", 1)[1]) <= 1
    WORK_HAND = HAND_LIMIT if (prefs.get("collect") or (prefs.get("human") and _cheap_cancel)) else 2
    _can_book = (("claim",) in legal or ("wild_book",) in legal)
    if _can_book and not prefs.get("no_tickets"):
        inprog = GAME._in_progress(pl)
        if len(inprog) < WORK_HAND:
            a = _book_action(s, p)                     # §21: face-up if suitable, else wild (blind)
            if a is not None:
                return a
        stale = [k for k in inprog if GAME._prog_frac(pl, k) < 0.34]
        if len(inprog) >= WORK_HAND and stale and s["mrow"]:
            best_row = max(GAME._booking_want(s, p, k) for k in s["mrow"])
            worst_held = min(GAME._booking_want(s, p, k) for k in stale)
            if best_row > worst_held * 1.3:
                return ("claim",)

    tgt = _pick_target_human(s, p, prefs) if prefs.get("human") else _pick_target(s, p, prefs)
    if tgt is None:
        return ("visit",) if ("visit",) in legal else legal[0]

    v = VENDORS[tgt]
    reg = v["region"]
    need = _needs(s, p, tgt)
    present = GAME._present(s, p, tgt)

    # 3) route to the target region / source what it needs
    if not present:
        if need.get(SIG_TYPE.get(pl["pos"]), 0) > 0 and ("visit",) in legal:
            return ("visit",)
        hop = _next_hop(pl["pos"], reg, pl["char"], GAME._hsr_open(s))
        if ("travel", hop) in legal:
            return ("travel", hop)
    if sum(need.values()) > 0:
        for tok in list(need):
            act = _token_source(s, p, tok, legal)
            if act is not None:
                return act
        if ("visit",) in legal:
            return ("visit",)

    # 4) WIN THE FOLLOWER FIGHT — spread- & margin-aware. Return the action; step() applies it (the
    #    planner must NOT mutate state — the harness calls the agent, THEN step()).
    add = GAME._needed_to_win(s, p, tgt)
    # BANK the board (lowball / late-battler exploit): in the DAY, refuse to spend followers on stalls —
    # hoard board + source, then crash the night marquee with a full pool. Falls through to grow/source.
    if prefs.get("bank") and s["act"] == 1:
        if ("visit",) in legal:
            return ("visit",)
        return legal[0]
    if add > 0 and present:
        if GAME._promote_ok(s, p, tgt):
            # SPREAD decision: if this Promote already secures tgt (add ≤ 1) and the bot stands with a
            # 2nd co-located stall it also contests, SPLIT the 2 followers across both; else stack on tgt.
            if pl["board"] >= 2 and add <= 1:
                co = [w for w in _co_located_targets(s, p)
                      if w != tgt and _booking_marginal(s, p, w, prefs) > 0
                      and 0 < GAME._needed_to_win(s, p, w) <= 1]
                if co:
                    return ("promote_spread", tgt, co[0])
            return ("promote", tgt)
        # ingredients ready + present but board EMPTY → you can't commit here. Rather than travel away
        # (losing position), fall through: grow followers via a USEFUL travel toward a region that both
        # sources a future need and grows +1 — handled below. (A board-0 present bot mis-positioned;
        # good play keeps a board reserve, which sourcing-travels naturally build.)

    if ("visit",) in legal:
        return ("visit",)
    return legal[0]


def _make(prefs):
    def agent(s, p, legal, rng):
        return _plan(s, p, legal, rng, prefs)
    return agent


BAL = {"w_val": 1.0, "w_food": 1.0, "w_drink": 1.0, "w_ramp": 1.0, "w_ticket": 1.0}
# ---- DIVERSE PLAYSTYLE ROSTER (fair lines that explore the real strategy space) -----------------
CONTESTER   = {**BAL, "contest": True}                                # battler: hunt the follower-fight
AVOIDER     = {**BAL, "avoid_contest": True, "w_food": 1.2}           # dodger: take quiet, uncontested wins
MARQUEE     = {**BAL, "marquee": True, "w_val": 1.2}                  # trophy-hunter: chase high-VP apex stalls
RUSH        = {**BAL, "rush": True, "w_drink": 1.1}                   # tempo: many cheap early claims, fast
ENGINE      = {**BAL, "engine": True, "w_ramp": 1.4, "w_food": 1.15} # economy: stack region icons → discounts
COLLECTOR   = {**BAL, "collect": True, "spread": True, "w_ticket": 1.2}  # spread-thin: breadth Bookings + regions
CONCENTRATE = {**BAL, "concentrate": True, "contest": True}          # concentrate: dominate one region hard
# ---- THE CLAIM-HUNGRY REALISTIC BASELINE (2026-08-10) --------------------------------------------
# The honest human line: value-per-turn target choice + target stickiness → claims vendors its Bookings
# need at a realistic velocity, WHILE still playing tours (draws + completes Bookings, WORK_HAND=2).
# This is the baseline the L-band should be measured against (a claim-naive bot forces the die to clock
# the game and yields a false pacing read). Uniform pref → fair across seats/characters.
HUMAN       = {**BAL, "human": True}
HUMAN_CONTEST   = {**HUMAN, "contest": True}                          # human who also hunts the fight
HUMAN_SPREAD    = {**HUMAN, "spread": True, "collect": True, "w_ticket": 1.2}  # human breadth-Booking line
# ---- ADVERSARIAL EXPLOIT-HUNTERS (each from a bg-critic hypothesis — try to BREAK the design) ----
LATE_BATTLER = {**BAL, "bank": True, "late_battle": True, "w_food": 1.15}  # banked-board late-battler (媽寶 line)
DODGER       = {**BAL, "avoid_contest": True, "w_food": 1.3}              # ignore-the-contest dodger
DENIER       = {**BAL, "deny": True}                                      # perpetual re-tie denier / kingmaker
# §14.5 MAKE-OR-BREAK: the vendor-only HOARDER — ignores Bookings, hoards high-VP stalls. MUST win <~10%
# (proves tours dominate the two-track scoring; if it matches a fair line the design is NOT closed).
HOARDER      = {**BAL, "no_tickets": True, "marquee": True, "w_val": 1.2}
# "want-to-be-lowest" SALVAGE / leader-fizzle bait: bank low, hold a full hand (→ cancels = SALVAGE bait),
# never lead (dodge ✦ leader hazards), crash late. Tests the perverse "don't want to lead" incentive (§15.5).
LOWBALL      = {**BAL, "bank": True, "collect": True, "avoid_contest": True, "late_battle": True, "w_ticket": 0.6}
SNIPER       = {**BAL, "snipe": True, "avoid_contest": True}              # seat-order / open-info uncontested sniper
NO_TICKETS   = {**BAL, "no_tickets": True}                               # objectives-blind control
# ---- SIX CHARACTER-LANE lines (each kit's intended way to play the new economy, §6.5) -----------
LANE = {
    "councillor":   {**ENGINE},                       # home-gated draw engine → economy/ramp
    "homebody":     {**DODGER},                        # viable dodge (his lane, §6.5a)
    "bigeater":     {**RUSH, "w_food": 1.3},           # greedy 4th → many cheap food, fast
    "influencer":   {**CONCENTRATE},                   # deep pool → pile followers, win the brawl
    "bigbrother":   {**CONTESTER},                     # margin dial → the fight is his edge
    "globetrotter": {**SNIPER, "spread": True},        # travel-anywhere → snipe uncontested across regions
}
# six CHARACTER-LANE lines carrying the claim-hungry `human` brain (fair, uniform kit-appropriate tilts)
LANE_H = {
    "councillor":   {**HUMAN, "engine": True, "w_ramp": 1.4, "w_food": 1.15},
    "homebody":     {**HUMAN, "avoid_contest": True, "w_food": 1.3},
    "bigeater":     {**HUMAN, "rush": True, "w_food": 1.3},
    "influencer":   {**HUMAN, "concentrate": True, "contest": True},
    "bigbrother":   {**HUMAN, "contest": True},
    "globetrotter": {**HUMAN, "snipe": True, "spread": True},
}
# back-compat aliases (older run scripts referenced these names)
HOMEBODY_DODGE, HOMEBODY_LATE = DODGER, LATE_BATTLER


def s_random(s, p, legal, rng):
    return rng.choice(legal)


STRATEGIES = {
    "balanced": _make(BAL),
    "contester": _make(CONTESTER),
    "avoider": _make(AVOIDER),
    "marquee": _make(MARQUEE),
    "rush": _make(RUSH),
    "engine": _make(ENGINE),
    "collector": _make(COLLECTOR),
    "concentrate": _make(CONCENTRATE),
    # claim-hungry realistic baseline (the honest band-reference line)
    "human": _make(HUMAN),
    "human_contest": _make(HUMAN_CONTEST),
    "human_spread": _make(HUMAN_SPREAD),
    # adversarial exploit bots
    "late_battler": _make(LATE_BATTLER),
    "dodger": _make(DODGER),
    "denier": _make(DENIER),
    "hoarder": _make(HOARDER),
    "lowball": _make(LOWBALL),
    "sniper": _make(SNIPER),
    "no_tickets": _make(NO_TICKETS),
    # six character-lane lines
    "lane_councillor": _make(LANE["councillor"]),
    "lane_homebody": _make(LANE["homebody"]),
    "lane_bigeater": _make(LANE["bigeater"]),
    "lane_influencer": _make(LANE["influencer"]),
    "lane_bigbrother": _make(LANE["bigbrother"]),
    "lane_globetrotter": _make(LANE["globetrotter"]),
    # six character-lane lines carrying the claim-hungry human brain
    "laneh_councillor": _make(LANE_H["councillor"]),
    "laneh_homebody": _make(LANE_H["homebody"]),
    "laneh_bigeater": _make(LANE_H["bigeater"]),
    "laneh_influencer": _make(LANE_H["influencer"]),
    "laneh_bigbrother": _make(LANE_H["bigbrother"]),
    "laneh_globetrotter": _make(LANE_H["globetrotter"]),
    # controls
    "random": s_random,
}
# back-compat aliases so older run scripts keep resolving
STRATEGIES["homebody_dodge"] = STRATEGIES["dodger"]
STRATEGIES["homebody_late"] = STRATEGIES["late_battler"]


# ==================================================================================================
#  ACTION APPLICATION SHIM — the planner may return a ("promote_spread", tgt, other) meta-action; the
#  engine's step() only knows the printed actions, so we translate the spread meta-action into a plain
#  ("promote", tgt) that step() applies, and stash the spread partner so _do_promote can split. To keep
#  step() authoritative we override legal/step to understand the meta-action.
# ==================================================================================================
_ORIG_STEP = TravelAgentsGame.step


def _step_with_spread(self, s, actions, rng):
    p = s["cur"]
    a = actions[p]
    if isinstance(a, tuple) and a and a[0] == "promote_spread":
        # apply the spread promote directly, then run the normal end-of-turn bookkeeping
        s["_rng"] = rng
        pl = s["players"][p]
        if pl["char"] == "councillor" and pl["pos"] == pl["home_region"] and pl["block_draw"] <= s["turn"]:
            self._councillor_draw(s, p)   # home-gated draw fires at the start of the turn, before the action
        self._do_promote(s, p, a[1], spread_vid=a[2])
        self._discard_to_cap(s, pl)
        self._track_committed(s, p)
        s["turn"] += 1
        if s["turn"] % s["n"] == 0:
            s["round"] += 1
            if SLOW_REFILL:
                self._refill_round(s)       # rolls the Closing-Time die (§17) then slow-refills
            for q in range(s["n"]):
                s["players"][q]["visit_keep_bonus"] = 0
            s["nudged_this_round"].clear()     # §15.5: the no-pile-on ceiling resets each round
            self._check_pool_boundary(s)    # §17: DUSK / LAST-TRAIN off vendor-pool emptiness + backstop
        s["cur"] = s["turn"] % s["n"]
        if s["end_turn"] is None and s["turn"] >= STALL_CAP * s["n"]:
            self._trigger_end(s, "stall")
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            self._finalize(s); s["done"] = True
        return s
    return _ORIG_STEP(self, s, actions, rng)


TravelAgentsGame.step = _step_with_spread


# make legal_actions advertise the spread meta-action so the harness accepts it when returned
_ORIG_LEGAL = TravelAgentsGame.legal_actions


def _legal_with_spread(self, s, p):
    acts = _ORIG_LEGAL(self, s, p)
    pl = s["players"][p]
    if pl["board"] >= 2:
        co = _co_located_targets(s, p)
        for i, a in enumerate(co):
            for b in co[i + 1:]:
                acts.append(("promote_spread", a, b))
    # §21.1 WILD BOOKING: available whenever the current Booking deck (mreserve) still has cards — a
    # blind draw is an option even if the face-up row is empty (you decline the row, take from the pile).
    if _wild_book_on() and s["mreserve"]:
        acts.append(("wild_book",))
    return acts


TravelAgentsGame.legal_actions = _legal_with_spread


# ==================================================================================================
#  A seed-threaded wrapper so dusk() can shuffle deterministically, and a per-count runner.
# ==================================================================================================
class _Seeded:
    def __init__(self, n=4, characters=None):
        self.n, self.characters = n, characters

    def new_state(self, rng, n=None):
        return GAME.new_state(rng, n or self.n, characters=self.characters)

    def __getattr__(self, k):
        return getattr(GAME, k)


def _run(agents, n_games, seed, n_players, characters=None):
    """Play n_games self-play matches at a fixed count; aggregate win-rate per seat + averaged metrics."""
    from engine import run_match
    g = _Seeded(n_players, characters)
    wins = [0.0] * n_players
    accum = {}
    for i in range(n_games):
        sc, mt = run_match(g, {p: agents[p] for p in range(n_players)}, seed + i)
        best = max(sc.values())
        winners = [p for p, v in sc.items() if v == best]
        for w in winners:
            wins[w] += 1.0 / len(winners)
        for k, v in mt.items():
            accum.setdefault(k, []).append(v)
    return [w / n_games for w in wins], {k: statistics.mean(v) for k, v in accum.items()}


# ==================================================================================================
#  __main__ — SMOKE TEST (tiny) + the CD-GATED full re-sim scaffold (§9). DO NOT run the full sim
#  without the CD's explicit "go".
# ==================================================================================================
if __name__ == "__main__":
    _SIM = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "tools", "sim"))
    if _SIM not in sys.path:
        sys.path.insert(0, _SIM)

    # ---------------------------------------------------------------------------------------------
    #  --smoke  — prove the module imports, runs end-to-end across the offered counts, and the new
    #  instruments emit sane numbers. TINY batch (default 20 games/count at 3–6p) — NOT a tuning run.
    # ---------------------------------------------------------------------------------------------
    if "--smoke" in sys.argv or len(sys.argv) == 1:
        _args = [a for a in sys.argv[1:] if a.isdigit()]
        N = int(_args[0]) if _args else 20
        from engine import run_match
        # counts default to the full 3–6 offer; TA_SMOKE_COUNTS="4,6" runs a tiny 1–2-count batch instead
        _counts = os.environ.get("TA_SMOKE_COUNTS", "")
        SMOKE_COUNTS = tuple(int(x) for x in _counts.split(",")) if _counts else (3, 4, 5, 6)
        print(f"# {TITLE}")
        print(f"# V7-M SMOKE TEST — {N} games/count, counts {SMOKE_COUNTS}, VISIT_MODE={VISIT_MODE} "
              f"(import + end-to-end + sane instruments)\n")
        for c in SMOKE_COUNTS:
            bal = STRATEGIES["balanced"]
            wins, mt = _run({p: bal for p in range(c)}, N, seed=1, n_players=c)
            print(f"## {c}p  (fair share {100/c:.1f}%)")
            print(f"  seat win%: " + "  ".join(f"s{p}={w*100:.0f}%" for p, w in enumerate(wins)))
            print(f"  turns/player {mt['turns_per_player']:.1f}  end LASTTRAIN {mt['end_by_lasttrain']*100:.0f}% "
                  f"/ STALL {mt['end_by_stall']*100:.0f}%  dusk {mt['dusk_turn']:.0f}/last {mt['last_turn']:.0f}")
            print(f"  ★#1 contested_frac {mt['contested_frac']*100:.1f}%  "
                  f"(contested {mt['contested_claims_per_game']:.2f} / total {mt['claims_per_game']:.2f} claims/gm; "
                  f"{mt['claims_per_game']/c:.1f}/plyr)  night/plyr {mt['night_claims_per_player']:.2f}  "
                  f"prestige-done/gm {mt['prestige_completions_per_game']:.2f}  bookings-done/gm {mt['bookings_completed_field']:.1f}")
            print(f"  ★#2 src shares: Meat {mt['src_share_meat_N']*100:.0f}% Tea {mt['src_share_tea_C']*100:.0f}% "
                  f"Seafood {mt['src_share_seafood_S']*100:.0f}% Pantry {mt['src_share_pantry_E']*100:.0f}% "
                  f"Sugar {mt['src_share_sugar']*100:.0f}% Veg {mt['src_share_veg']*100:.0f}%  "
                  f"empty_draws/gm {mt['empty_draws_per_game']:.2f}")
            print(f"  meeples: grow/gm {mt['grow_total_per_game']:.1f}  return→supply/gm {mt['return_to_supply_per_game']:.1f}  "
                  f"max_committed(stall {mt['max_committed_on_stall']:.1f}/player {mt['max_committed_by_player']:.1f})  "
                  f"promotes/gm {mt['promotes_per_game']:.1f}  cancels/gm {mt['cancels_per_game']:.1f}")
            print(f"  scarcity/tie: resolver_fires/gm {mt['resolver_fires_per_game']:.2f}  "
                  f"frozen@boundary/gm {mt['frozen_at_boundary_per_game']:.2f}  below_floor_blocks/gm "
                  f"{mt['below_floor_blocks_per_game']:.2f}  runaway best_win_streak {mt['best_win_streak']:.1f}")
            print(f"  §14 VP two-track: winner vendor-VP {mt['winner_vendor_vp']:.1f} + booking-VP "
                  f"{mt['winner_booking_vp']:.1f}  → vendor-share {mt['vendor_vp_share_of_winner']*100:.0f}% "
                  f"(target 25–35%)  claims/plyr {mt['claims_per_player']:.1f}  apex/plyr {mt['apex_claims_per_player']:.2f}")
            print(f"  §15 events: fired/plyr {mt['events_fired_per_player']:.1f}  ✦leader fires/gm "
                  f"{mt['ev_leader_fires_per_game']:.2f} (fizzles {mt['ev_leader_fizzles_per_game']:.2f})  "
                  f"swipe/gm {mt['swipes_per_game']:.2f} spoil {mt['spoils_per_game']:.2f} gift {mt['gifts_per_game']:.1f} "
                  f"block {mt['blocks_per_game']:.2f} detour {mt['detours_per_game']:.2f} restock/wash "
                  f"{mt['restocks_per_game']:.2f}/{mt['washes_per_game']:.2f}")
            print(f"  §16 deck-flow: reshuffles(E-night {mt['reshuffles_E_night']:.1f}/N-night {mt['reshuffles_N_night']:.1f})  "
                  f"reshuffle-size(E {mt['reshuffle_size_E_night']:.1f})  live evfrac(E-night {mt['evfrac_E_night']*100:.0f}%/"
                  f"N-night {mt['evfrac_N_night']*100:.0f}%)  Pantry supply_min {mt['pantry_supply_min']:.0f}  "
                  f"→box/gm {mt['box_from_larder_per_game']:.1f}")
            print(f"  §15.9 tours-boons: SALVAGE fires/gm {mt['salvage_fires_per_game']:.2f} swing "
                  f"{mt['salvage_swing_per_game']:.2f} (drawer {mt['salvage_gain_drawer_per_game']:.2f}/trailer "
                  f"{mt['salvage_relief_trailer_per_game']:.2f})  CLEAR fires/gm {mt['clear_fires_per_game']:.2f} "
                  f"relief {mt['clear_relief_per_game']:.2f}  cancelled-pile/field {mt['cancelled_pile_field']:.1f}")
            print(f"  §15.5 leader-nudge (must stay MILD): impact/gm {mt['leader_nudge_impact_per_game']:.2f}  "
                  f"pileon-blocked/gm {mt['nudge_pileon_blocked_per_game']:.2f}  max-on-one-leader "
                  f"{mt['max_nudges_on_one_leader']:.1f}  winner-nudges {mt['winner_nudges_taken']:.2f}")
            print(f"  §18 VISIT_MODE={VISIT_MODE}: M1 visit-choice {mt['visit_choice_frac']*100:.0f}% "
                  f"(A→~0 by design)  banked-board(max any {mt['max_board_any_player']:.1f}/winner "
                  f"{mt['winner_max_board']:.1f})  fol/win-field {mt['fol_per_win_field']:.2f}")
            print(f"  decision density: avg_legal {mt['avg_legal_actions']:.1f}  forced_turn_frac {mt['forced_turn_frac']:.3f}")
            # ---- EXPLOIT-BOT PANEL: each adversarial line in seat0 vs a balanced field (must not beat it) ----
            # bg-critic hypotheses → concrete bots. HOARDER is the §14.5 make-or-break (must win <~10%).
            print("  exploit-bot seat0 win% vs balanced field (fair share {:.0f}%):".format(100 / c))
            for name, note in (("hoarder", "§14.5 vendor-only — MUST LOSE <10% (tours must dominate)"),
                               ("dodger", "ignore-the-contest"),
                               ("denier", "perpetual re-tie / kingmaker"),
                               ("lowball", "want-to-be-lowest / SALVAGE-bait"),
                               ("sniper", "seat-order / open-info snipe"),
                               ("late_battler", "banked-board late-battler")):
                ef = {0: STRATEGIES[name], **{p: STRATEGIES["balanced"] for p in range(1, c)}}
                ew, _ = _run(ef, N, seed=777, n_players=c)
                print(f"    {name:13} {ew[0]*100:4.0f}%   {note}")
            print()

        # per-lane probe spot-check at 4p: each character in seat0 vs 3 balanced-neutrals. Confirms the
        # six kits run AND the lane-specific instruments emit sane, non-trivial numbers with the real char.
        print("## per-lane probe spot-check (4p; char in seat0 vs 3 balanced-neutrals, N games each)")
        for ch in CHAR_ORDER:
            chars = ["neutral"] * 4; chars[0] = ch
            wins, mt = _run({p: STRATEGIES["balanced"] for p in range(4)}, N, seed=100, n_players=4, characters=chars)
            probe = ""
            if ch == "bigbrother":
                probe = f"edge-fire/gm {mt['dage_edge_fires_per_game']:.2f} (rate {mt['dage_edge_fire_rate']*100:.0f}%)"
            elif ch == "globetrotter":
                probe = f"snipe-rate {mt['ama_snipe_rate']*100:.0f}%  travel-cost paid/gm {mt['ama_travel_cost_paid_per_game']:.2f}"
            elif ch == "homebody":
                probe = f"grow-tick/gm {mt['grow_homebody_tick_per_game']:.2f}"
            elif ch == "councillor":
                probe = f"home free-draws/gm {mt['councillor_free_draws_per_game']:.2f}"
            elif ch == "influencer":
                probe = f"max_committed/player {mt['max_committed_by_player']:.1f} (pool {INFL_MAX})"
            elif ch == "bigeater":
                probe = f"return→supply/gm {mt['return_to_supply_per_game']:.1f} (greedy-4th sink)"
            print(f"  {ZH[ch]:6} ({ch:12}) seat0 win% {wins[0]*100:4.0f}% (fair 25%)  contested {mt['contested_frac']*100:3.0f}%  {probe}")

        print("\n[smoke] OK — module imported, ran end-to-end at 3/4/5/6p, and every new instrument emits sane numbers.")
        print("[smoke] READY for the CD-GATED per-count 3–6 re-sim (§9, ~50 min) — run `--resim` only on the CD's explicit 'go'.")
        sys.exit(0)

    # ---------------------------------------------------------------------------------------------
    #  --resim [N] [--out PATH]  — the CD-GATED ~50-min per-count 3–6 re-sim (§9). Runs the six-lane
    #  band, seat fairness, and the make-or-break probes per count, plus the reserve-lever deltas.
    #  ⚠ DO NOT run without the CD's explicit sign-off (the simulation gate). This scaffold is BUILT
    #  and smoke-tested; the full run is deferred to the CD's "go".
    # ---------------------------------------------------------------------------------------------
    if "--resim" in sys.argv:
        _args = [a for a in sys.argv[1:] if a.isdigit()]
        N = int(_args[0]) if _args else 250
        OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
        from engine import run_match, seat_balance
        L = []

        def out(line=""):
            print(line); L.append(line)

        def char_band(ch, c, n, seed):
            """Char in FIRST + LAST seat vs balanced-neutrals; avg win-rate (fair = 1/c)."""
            got = []
            for seat in (0, c - 1):
                chars = ["neutral"] * c; chars[seat] = ch
                g = _Seeded(c, chars)
                won = 0.0
                for i in range(n):
                    sc, _ = run_match(g, {p: STRATEGIES["balanced"] for p in range(c)}, seed + i)
                    best = max(sc.values()); winners = [q for q, v in sc.items() if v == best]
                    if seat in winners:
                        won += 1.0 / len(winners)
                got.append(won / n); seed += n
            return sum(got) / 2

        def field(c, n, seed):
            _, mt = _run({p: STRATEGIES["balanced"] for p in range(c)}, n, seed, c)
            return mt

        out(f"# {TITLE}")
        out(f"# CD-GATED V7-M RE-SIM (§9) — per-count 3–6, N={N}/seating\n")
        out(f"Config: MAX={FIELD_MAX}(網紅 {INFL_MAX}) · 大哥 N={DAGE_N} · 阿嬤 travel-cost={'ON' if AMA_TRAVEL_COST else 'OFF'} · "
            f"homebody-grow={'ON' if HOMEBODY_GROW else 'OFF'} · tie-resolver={'ON' if TIE_RESOLVER else 'OFF'} · "
            f"slow-refill={'ON' if SLOW_REFILL else 'OFF'} · HAND_LIMIT={HAND_LIMIT}\n")
        seed = 1
        for c in (3, 4, 5, 6):
            fair = 100.0 / c
            out(f"\n## {c}p  " + "=" * 70 + f"  (fair {fair:.1f}%)")
            band = {}
            for ch in CHAR_ORDER:
                band[ch] = char_band(ch, c, N, seed); seed += 2 * N
                out(f"    {ZH[ch]:6} {band[ch]*100:5.1f}%  idx {band[ch]/(fair/100):.2f}")
            lo, hi = min(band.values()), max(band.values())
            out(f"    band {lo*100:.1f}–{hi*100:.1f}%  spread(idx) {(hi-lo)/(fair/100):.2f}")
            g = _Seeded(c)
            r = seat_balance(g, STRATEGIES["balanced"], c, n=max(400, N)); seed += max(400, N)
            out(f"    seat fairness: {'SUSPECT' if r['suspect'] else 'ok'}  "
                + "  ".join(f"s{p}={v*100:.0f}%" for p, v in r["seat_win_rate"].items()))
            mt = field(c, max(400, N), seed); seed += max(400, N)
            out(f"    ★#1 contested_frac {mt['contested_frac']*100:.1f}%  (contested {mt['contested_claims_per_game']:.2f}"
                f"/total {mt['claims_per_game']:.2f} claims/gm)  night/plyr {mt['night_claims_per_player']:.2f}")
            out(f"    ★#2 src Meat {mt['src_share_meat_N']*100:.0f} Tea {mt['src_share_tea_C']*100:.0f} "
                f"Sea {mt['src_share_seafood_S']*100:.0f} Pan {mt['src_share_pantry_E']*100:.0f} "
                f"Sug {mt['src_share_sugar']*100:.0f} Veg {mt['src_share_veg']*100:.0f}  "
                f"LT {mt['end_by_lasttrain']*100:.0f}%  t/p {mt['turns_per_player']:.1f}  "
                f"prestige/gm {mt['prestige_completions_per_game']:.2f}")
            out(f"    runaway best_streak {mt['best_win_streak']:.1f}  resolver/gm {mt['resolver_fires_per_game']:.2f}  "
                f"大哥 edge/gm {mt['dage_edge_fires_per_game']:.2f}  阿嬤 snipe {mt['ama_snipe_rate']*100:.0f}%")
        if OUT:
            os.makedirs(os.path.dirname(OUT), exist_ok=True)
            with open(OUT, "w", encoding="utf-8") as f:
                f.write("\n".join(L) + "\n")
            print(f"\n[resim] wrote {OUT}")
        sys.exit(0)
