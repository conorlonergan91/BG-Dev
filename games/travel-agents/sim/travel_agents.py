"""
travel_agents.py — Travel Agents: Taiwan (v6.1 · THE ECONOMY FORK, region-anchored + scoped events)
encoded for the simulation harness (see tools/sim/engine.py). Stdlib-only.

This reworks the checkpointed v6 first-pass to the LOCKED v6.1 design (design/design-doc.md · header
"v6.1 · the economy fork"). v6.1 folds TWO CD corrections into the v6 economy fork; the spine (the
Buzz-majority fight, the five actions, the ladder-only day-clock, the ★ swing, the five characters) is
UNCHANGED. What v6.1 moved — and what this rework implements:

  (A) BEVERAGES ARE REGION-ANCHORED, not a region-free central "Beverage Row".
      * v6 (first pass): one flat "Beverage Row" of 2 slots, region=None, present-everywhere.
      * v6.1: a persistent beverage slot in EVERY region (4 @2p, one per region on the map). A beverage
        card is region-AGNOSTIC but takes the region of the slot it fills; you must be ON-SITE (standing
        in that region) to Promote/Bribe it — the SAME unified Bribe rule as any vendor (on-site + ≥2
        majority + pay). The low-travel identity now comes from UBIQUITY (a stand where you already stand)
        + easy sourcing (common off the Convenience Store from anywhere), NOT from acting at a distance.
      * The Beverage DECK (not the slot count) is still the hard cap: ~7-8 winnable all game; once it
        empties, region beverage slots go empty and stay empty.

  (B) THE CONVENIENCE STORE FIRES EVENTS BY SCOPE (was a silent whiff in v6).
      * Every event card carries a dual-coded SCOPE tag: ⦿ self / ⬢ region / ➤ neighbour, resolved
        RELATIVE TO THE REGION THE CARD WAS DRAWN FROM.
      * Events fire when you WORK a market — VISIT (your region) or CONVENIENCE STORE (any region, often
        remote). TRAVEL's arrival flip still WHIFFS (you're passing through).
      * self ⦿ → the acting player; region ⬢ → whoever is STANDING in the drawn region (the take-that
        lever: flip a rival's region and a region-hazard lands on THEM); neighbour ➤ → whoever stands
        adjacent to the drawn region.
      * The drinks player usually CS-flips a REMOTE common-bearing region where no rival stands, so they
        mostly only eat SELF-scoped events — a mild, bounded personal tax (tax-not-destroy) that is the
        deliberate v6.1 nerf on the drinks engine's spine, while region/neighbour events become a poke
        they can aim.
      Proposed scope ratio (sim knob): ~40% self / ~40% region / ~20% neighbour, hazards leaning
      region/neighbour, boons leaning self (keep some region boons — a festival boons everyone present).

Everything else stands from v6: the 5-ingredient palette (N pork / C tea / S seafood / E rice + one
COMMON K 糖 sugar in HALF the regions), the ladder-only day-clock (dusk 4 / last train 7 @2p) + dusk
sweep + deck backstops, the discount ramp (ladder icons only; beverages carry none), Prestige + Rep-end-VP
+ the hidden +7 mission, the ★ printed apex + the dynamic ★ "gets hot" boon, and the five characters.

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (bots are a FLOOR on depth, not a ceiling)
------------------------------------------------------------------------------------------------------
Faithfully modelled: the 4-region ring + HSR(N↔S); the five actions with their exact where/effect; the
5-ingredient palette + common-in-two-regions; per-region face-down market decks (reshuffle-on-empty,
preserving per-draw hazard density — the push-your-luck spine); Visit-flips-3-keep-2 with events firing
BY SCOPE (a self/region hazard hitting the actor eats a keep-slot; a region/neighbour hazard hitting a
rival applies a bounded tempo tax); Convenience Store single blind draw that ALSO fires by scope; Travel
single blind draw that WHIFFS on an event; the region-anchored beverage slots (one per region, on-site
Bribe, deck-capped, never swept); the Buzz-majority Bribe (≥2 lead, presence, pay ingredients −discounts),
Buzz clearing to a finite supply on a win; the ladder-only day-clock + dusk sweep + deck backstops; the
discount ramp; the ★ printed apex + dynamic ★ boon; the five characters (ability + flaw, H1/H2/H3 knobs).

Simplifications (the sim's blind spots — hand these to the table):
  * SHARED "engine brain": every strategy scores the legal actions with ONE greedy planner; strategies
    differ ONLY in their ROAD WEIGHTS (ladder vs beverage) + a pure-drinks flag. This isolates the v6/v6.1
    #2 question — "is the drinks fork viable but not dominant?" — exactly as beacon.py isolates policy.
  * Event PAYLOADS are abstracted to their mechanical shape: a HAZARD = a bounded, tax-not-destroy tempo
    tax (one fewer sourced ingredient on the target's current/next sourcing — never removes a held card,
    never a whole turn); a BOON = a free ingredient windfall to the targets present, OR (a fraction) the
    dynamic ★ "vendor gets hot" placement. Buzz-boons/festival-Buzz are folded into the ingredient
    windfall. Exact tile text + the warmth of the rival-facing beats are the feel-test's job (bg-theme).
  * The CS "take-that" is exercised two ways: (1) emergently — a drinks player CS-flipping a common region
    a rival happens to occupy; (2) a light deliberate POKE fallback — a bot with nothing productive to do
    (larder near cap, no live target) may CS-flip a rival's region. It's BLIND (you don't know the top
    card) so it can backfire — a cheeky low-stakes poke, never a reliable strike (knob TA_POKE).
  * The Buzz war is resolved by a CONCESSION heuristic (appetite falls as the rival's committed Buzz
    rises). Deterministic mirrors deadlock/tie on identical top targets (the mirror caveat); read depth
    from cross-strategy play.
  * Missions: the bot keeps the dealt mission best aligned to its road weights (draw-3-keep-1).
  * ASSUMPTIONS where the doc left a value open are tagged `# ASSUMPTION:` and gathered in sim-notes.md.

Run:
    python tools/sim/simulate.py --module games/travel-agents/sim/travel_agents.py --n 3000 \
        --out games/travel-agents/playtests/sim-results.md
    python games/travel-agents/sim/travel_agents.py            # runs the character + H1/H2/H3/H4 probes
"""
from __future__ import annotations

import os
import sys
import statistics
from collections import Counter, deque

# ==================================================================================================
#  SIM KNOBS (env vars; the design's open numbers — do NOT alter the printed rules)
# ==================================================================================================
BUZZ_SUPPLY    = int(os.environ.get("TA_BUZZ_SUPPLY", "24"))    # 2p Buzz supply (design ~24)
BUZZ_MARGIN    = int(os.environ.get("TA_BUZZ_MARGIN", "2"))     # ≥N Buzz lead to Bribe (design 2)
LADDER_SLOTS   = int(os.environ.get("TA_LADDER_SLOTS", "4"))    # 2p ladder width
DUSK_MARK      = int(os.environ.get("TA_DUSK", "4"))            # ladder wins → dusk (Act I→II) @2p
LASTTRAIN_MARK = int(os.environ.get("TA_LASTTRAIN", "7"))       # ladder wins → last train (end) @2p
LARDER_CAP     = int(os.environ.get("TA_LARDER_CAP", "7"))
BEV_VALUE      = int(os.environ.get("TA_BEV_VALUE", "2"))       # beverage Prestige (flat) — master fork knob
BEV_REP        = int(os.environ.get("TA_BEV_REP", "1"))         # beverage Rep bump
STAR_BONUS_P   = int(os.environ.get("TA_STAR_P", "2"))          # dynamic ★ token +Prestige
STAR_BONUS_R   = int(os.environ.get("TA_STAR_R", "1"))          # dynamic ★ token +Rep
STALL_CAP      = int(os.environ.get("TA_STALL_CAP", "26"))      # hard per-player turn cap (drinks-drag backstop)

# H3 — common availability. "half" (A: C & S) | "every" (B) | "half_rich" (C: half, higher per-deck share).
H3 = os.environ.get("TA_H3", "half")
# H1 — 大胃王 flaw. "twice" (A) | "keep2" (B) | "next" (C).
H1 = os.environ.get("TA_H1", "twice")
# H2 — 大哥 threshold+flaw. TA_H2_THRESH 0 (tie ≥0, A/B) | 1 (lead ≥1, C); TA_H2_FLAW "tab"(+1 ing, A/C) |
# "promote1"(Promote places 1, B).
DAGE_THRESH = int(os.environ.get("TA_H2_THRESH", "0"))
DAGE_FLAW   = os.environ.get("TA_H2_FLAW", "tab")

EVENT_HAZARD_FRAC = float(os.environ.get("TA_HAZARD", "0.58"))  # of a region deck's event cards, this frac hazards
STAR_BOON_CHANCE  = float(os.environ.get("TA_STARBOON", "0.30"))# of boons that fire, this frac drop a dynamic ★

# H4 (v6.1) — the event-scope ratio. Base weights; hazards skew region/neighbour, boons skew self (below).
SCOPE_SELF   = float(os.environ.get("TA_SCOPE_SELF", "0.40"))
SCOPE_REGION = float(os.environ.get("TA_SCOPE_REGION", "0.40"))
SCOPE_NEIGH  = float(os.environ.get("TA_SCOPE_NEIGH", "0.20"))
POKE_ENABLED = os.environ.get("TA_POKE", "1") != "0"           # the light deliberate CS "poke" fallback

# ==================================================================================================
#  MAP
# ==================================================================================================
REGIONS = ("N", "C", "S", "E")
# ring N-C-S-E + HSR(N↔S). ring neighbours: N-C, C-S, S-E, E-N.
RING = {"N": ["C", "E"], "C": ["N", "S"], "S": ["C", "E"], "E": ["S", "N"]}
HSR = ("N", "S")
COMMON = "K"                                        # the common ingredient (糖 sugar)


def neighbours(pos, char=None):
    """A pawn's LEGAL travel destinations (character-aware: 里長伯 cannot use HSR)."""
    ns = list(RING[pos])
    if char != "councillor" and pos in HSR:         # 里長伯 cannot use HSR
        other = HSR[1] if pos == HSR[0] else HSR[0]
        if other not in ns:
            ns.append(other)
    return ns


def region_neighbours(r):
    """GEOGRAPHIC adjacency (ring + HSR), character-agnostic — used to resolve a ➤ neighbour-scoped
    event's spill. The island pushes people around regardless of anyone's HSR restriction."""
    ns = set(RING[r])
    if r in HSR:
        ns.add(HSR[1] if r == HSR[0] else HSR[0])
    return ns


def common_regions():
    if H3 == "every":
        return set(REGIONS)
    return {"C", "S"}                               # A / C: half (the South/Central refining belt)


def _dist(pos, dest, char=None):
    """BFS hop-distance from pos to dest over the character's legal adjacency."""
    if pos == dest:
        return 0
    q = deque([(pos, 0)])
    seen = {pos}
    while q:
        cur, d = q.popleft()
        for nb in neighbours(cur, char):
            if nb in seen:
                continue
            if nb == dest:
                return d + 1
            seen.add(nb)
            q.append((nb, d + 1))
    return 99


def _next_hop(pos, dest, char=None):
    """BFS one step from pos toward dest over the character's legal adjacency."""
    if pos == dest or dest is None:
        return pos
    q = deque([(pos, None)])
    seen = {pos}
    while q:
        cur, first = q.popleft()
        for nb in neighbours(cur, char):
            if nb in seen:
                continue
            fh = nb if first is None else first
            if nb == dest:
                return fh
            seen.add(nb)
            q.append((nb, fh))
    return neighbours(pos, char)[0]


def _nearest_common(pos, char):
    """Closest common-bearing region — where a drinks-leaning bot wants to camp (Visit the common at
    3× the Convenience-Store throughput AND court that region's persistent stand)."""
    cr = common_regions()
    if not cr:
        return None
    return min(cr, key=lambda r: _dist(pos, r, char))


# ==================================================================================================
#  EVENT CARDS — a scoped event is the tuple  ("ev", kind, scope, sub)
#    kind  in {"hazard","boon"};  scope in {"self","region","neigh"}
#    sub   "tempo" (hazard) | "ingredient" | "star" (boon)
# ==================================================================================================
def _sample_scope(kind, rng):
    """Assign a scope, skewed by kind (hazards lean region/neighbour, boons lean self, keep some region
    boons). Base weights come from the H4 knobs; realized aggregate is reported in metrics()."""
    if kind == "hazard":
        w = {"self": SCOPE_SELF * 0.50, "region": SCOPE_REGION * 1.25, "neigh": SCOPE_NEIGH * 1.75}
    else:  # boon
        w = {"self": SCOPE_SELF * 1.55, "region": SCOPE_REGION * 0.95, "neigh": SCOPE_NEIGH * 0.45}
    tot = sum(w.values()) or 1.0
    x = rng.random() * tot
    acc = 0.0
    for s in ("self", "region", "neigh"):
        acc += w[s]
        if x <= acc:
            return s
    return "self"


def _make_event(kind, rng):
    scope = _sample_scope(kind, rng)
    if kind == "boon":
        if rng.random() < STAR_BOON_CHANCE:
            return ("ev", "boon", "region", "star")   # a "vendor gets hot" ★ is a place/region beat
        return ("ev", "boon", scope, "ingredient")
    return ("ev", "hazard", scope, "tempo")


# ==================================================================================================
#  VENDOR TABLE (baked v6.1 set — a representative value curve per the design's Economy section)
# ==================================================================================================
# A vendor: id, kind ("breakfast"|"nm"|"bev"), region (icon region; None for bev — region-AGNOSTIC card,
# it takes the region of the slot it fills), cost (Counter over N/C/S/E/K), prestige, rep, perk, star.
# Perks: "icon"(base ramp), "double_icon", "wild", "buzz_reach"(Promote +1), "rep_plus2".
def _build_vendors():
    vends = []

    def add(kind, region, cost, prestige, rep, perk, star=False):
        vends.append({"id": len(vends), "kind": kind, "region": region,
                      "cost": Counter(cost), "prestige": prestige, "rep": rep,
                      "perk": perk, "star": star})

    # --- Breakfast shops 早餐店 (~10, Act I ladder): cheap opening, the discount RAMP starts here.
    #     cost 1-2 (mostly its signature, some + common), Prestige 1-2, Rep +1, perk = region icon.
    add("breakfast", "N", {"N": 1},          1, 1, "icon")
    add("breakfast", "N", {"N": 2},          2, 1, "icon")
    add("breakfast", "N", {"N": 1},          1, 1, "icon")
    add("breakfast", "C", {"C": 1},          1, 1, "icon")
    add("breakfast", "C", {"C": 1, "K": 1},  2, 1, "icon")      # + common filler (C carries common)
    add("breakfast", "S", {"S": 1},          1, 1, "icon")
    add("breakfast", "S", {"S": 1, "K": 1},  2, 1, "icon")      # S carries common
    add("breakfast", "E", {"E": 1},          1, 1, "icon")
    add("breakfast", "E", {"E": 2},          2, 1, "icon")
    add("breakfast", "E", {"E": 1},          1, 1, "icon")

    # --- Night-market stalls 夜市攤 (~9, Act II ladder): the apex; ~44% cross-region; ★ apex 7-8.
    add("nm", "S", {"S": 2},                 5, 2, "double_icon")
    add("nm", "N", {"N": 3},                 5, 2, "double_icon")
    add("nm", "C", {"C": 2},                 5, 2, "rep_plus2")
    add("nm", "E", {"E": 2},                 5, 2, "buzz_reach")
    add("nm", "S", {"S": 2, "E": 1},         6, 2, "wild")        # cross
    add("nm", "N", {"N": 2, "C": 1},         6, 2, "wild")        # cross
    add("nm", "S", {"S": 3},                 8, 3, "double_icon", star=True)   # apex ★
    add("nm", "C", {"C": 2, "S": 1},         7, 3, "wild",        star=True)   # apex ★ cross
    add("nm", "N", {"N": 2, "S": 1},         8, 3, "rep_plus2",   star=True)   # apex ★ cross

    # --- Beverage shops 飲料店 (10 baked; region-AGNOSTIC, no icon): flat easy points. The DECK is the
    #     hard cap on drink wins; sliced to size {2p:7, 3p:9, 4p:10} in new_state.
    for c in ({"K": 1}, {"K": 2}, {"K": 1}, {"K": 2}, {"K": 1, "C": 1},
              {"K": 1}, {"K": 2}, {"K": 1}, {"K": 2}, {"K": 1, "C": 1}):
        add("bev", None, c, BEV_VALUE, BEV_REP, None)
    return vends


VENDORS = _build_vendors()
BREAKFAST = [v["id"] for v in VENDORS if v["kind"] == "breakfast"]
NM        = [v["id"] for v in VENDORS if v["kind"] == "nm"]
BEV       = [v["id"] for v in VENDORS if v["kind"] == "bev"]


# ==================================================================================================
#  TOUR TICKETS (v6.1 PROPOSAL under test — CD-locked shape, 2026-08-07)
#  ------------------------------------------------------------------------------------------------
#  Ticket-to-Ride-style objectives that REPLACE the single hidden +7 mission when MISSION_MODE
#  ="tickets": you may hold several; CLAIM a new one as a full action (Book, does NOT tick the
#  day-clock); score +value on completion and −floor(value/2) if UNFINISHED at scoring (the CD's
#  "−half its value" call). The deck LEANS on MIX tickets (drinks + ladder) so a well-timed drink pays
#  toward a bonus a value/action planner can actually SEE — the exact incentive the flat-2-VP drink
#  lacked. Tickets stay secret (the hidden vector); Booking is a public tell you claimed *something*.
#  MISSION_MODE="single" restores the committed v6.1 baseline (deal-3-keep-1, one +7 binary, NO penalty,
#  NO Book) for a clean A/B on "does the ticket system make a well-timed mix beat pure ladder?".
# ==================================================================================================
MISSION_MODE = os.environ.get("TA_MISSION_MODE", "tickets")   # "tickets" (proposal) | "single" (baseline)
BOOK_LATE_MARGIN = int(os.environ.get("TA_BOOK_LATE", "1"))    # stop booking within N ladder-wins of the end

# key: (value, needs_bev, needs_ladder) — value = +on completion; −(value//2) if unfinished
TICKETS = {
    # --- mix tickets (the tilt: reward drinks + ladder together — the CD's "mostly mix" call) ---
    "stand_and_nm":  (4, True,  True),    # a beverage stand + a night-market stall
    "sampler":       (5, True,  True),    # one of each venue: a breakfast + a night-market + a stand
    "two_stands_nm": (6, True,  True),    # 2 stands + a night-market
    "stands_3reg":   (6, True,  False),   # a stand in 3 different regions (drinks + light travel)
    # --- ladder tickets (the spine) ---
    "grand_tour":    (7, False, True),    # a ladder vendor in all 4 regions
    "south_3":       (5, False, True),    # 3 ladder vendors in the South
    "nm_2":          (5, False, True),    # 2 night-market stalls
    "prestige_12":   (6, False, True),    # vendors totalling >=12 Prestige
    "breakfast_3":   (4, False, True),    # 3 breakfast shops
    # --- one modest pure-drinks ticket (kept low per "mostly mix") ---
    "beverage_3":    (4, True,  False),   # 3 beverage stands
}
TICKET_KEYS = tuple(TICKETS)
SINGLE_MISSION_VALUE = 7
# rough completability in a ~5-6-win game (a keep-choice proxy — a player keeps tickets they can finish,
# not just high-value ones). Region-anchored stands make multi-region/multi-stand tickets a touch harder.
TICKET_EASE = {
    "stand_and_nm": 0.90, "sampler": 0.80, "two_stands_nm": 0.65, "stands_3reg": 0.50,
    "grand_tour": 0.35, "south_3": 0.55, "nm_2": 0.70, "prestige_12": 0.55,
    "breakfast_3": 0.70, "beverage_3": 0.60,
}


def _ticket_value(key):
    return TICKETS[key][0] if MISSION_MODE == "tickets" else SINGLE_MISSION_VALUE


def _bev_regions(won):
    return set(v["region"] for v in won if v["kind"] == "bev" and v["region"] is not None)


def _mission_progress(key, won):
    ladder = [v for v in won if v["kind"] != "bev"]
    nb = sum(1 for v in won if v["kind"] == "bev")
    nnm = sum(1 for v in won if v["kind"] == "nm")
    nbf = sum(1 for v in won if v["kind"] == "breakfast")
    if key == "grand_tour":
        return len(set(v["region"] for v in ladder)), 4
    if key == "south_3":
        return sum(1 for v in ladder if v["region"] == "S"), 3
    if key == "breakfast_3":
        return nbf, 3
    if key == "beverage_3":
        return nb, 3
    if key == "nm_2":
        return nnm, 2
    if key == "prestige_12":
        return sum(v["prestige"] for v in won), 12
    if key == "stand_and_nm":                          # partial-credit AND (monotonic for the planner)
        return min(nb, 1) + min(nnm, 1), 2
    if key == "sampler":
        return min(nbf, 1) + min(nnm, 1) + min(nb, 1), 3
    if key == "two_stands_nm":
        return min(nb, 2) + min(nnm, 1), 3
    if key == "stands_3reg":
        return min(len(_bev_regions(won)), 3), 3
    return 0, 1


def _mission_done(key, won):
    d, n = _mission_progress(key, won)
    return d >= n


def _mission_helps(key, cand, won):
    b, n = _mission_progress(key, won)
    if b >= n:
        return False
    a, _ = _mission_progress(key, won + [cand])
    return a > b


def _ticket_fit(prefs, key):
    """How completable this ticket is for a bot with these road prefs (a no-drinks bot can't finish the
    beverage half; a pure-drinks bot can't finish the ladder half)."""
    _, needs_bev, needs_ladder = TICKETS[key]
    if prefs.get("no_drinks") and needs_bev:
        return 0.1
    if prefs.get("pure_drinks") and needs_ladder:
        return 0.15
    road = prefs.get("road", "mixed")
    if road == "drinks":
        return 1.3 if needs_bev else 0.7
    if road == "ladder":
        return 0.6 if (needs_bev and not needs_ladder) else 1.1
    return 1.0


def _ticket_keep_score(won, key, prefs):
    d, n = _mission_progress(key, won)
    prog = (d / n) if n else 0.0
    # keep the best EXPECTED value: value * completability * road-fit, plus a bonus for progress already made
    return _ticket_value(key) * TICKET_EASE.get(key, 0.6) * _ticket_fit(prefs, key) + 2.0 * prog


def _deal_start_tickets(rng, prefs):
    """Deal 3, keep the 1 best aligned/most-completable (draw-3-keep-1 opening)."""
    deal = list(rng.sample(TICKET_KEYS, 3))
    return [max(deal, key=lambda k: _ticket_keep_score([], k, prefs))]


def _book_keep(rng, won, prefs):
    """The Book action: draw 2, keep the better one (TtR keep-≥1); avoid the un-finishable (penalty)."""
    deal = list(rng.sample(TICKET_KEYS, 2))
    return max(deal, key=lambda k: _ticket_keep_score(won, k, prefs))


def _ticket_final_score(pl):
    if MISSION_MODE != "tickets":
        return SINGLE_MISSION_VALUE if _mission_done(pl["tickets"][0], pl["won"]) else 0
    tot = 0
    for key in pl["tickets"]:
        v = TICKETS[key][0]
        tot += v if _mission_done(key, pl["won"]) else -(v // 2)   # −half (floored) if unfinished
    return tot


# ==================================================================================================
#  SCORING helpers
# ==================================================================================================
def _rep_end_vp(rep):
    if rep >= 12:
        return 9
    if rep >= 9:
        return 6
    if rep >= 6:
        return 4
    if rep >= 3:
        return 2
    return 0


CHARACTERS = ("neutral", "councillor", "office", "influencer", "dagushi", "dage")


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:
    # -------- setup --------
    def new_state(self, rng, n_players=2, characters=None, roads=None, caps=None):
        chars = list(characters) if characters else ["neutral"] * n_players
        roads = list(roads) if roads else ["mixed"] * n_players
        caps = list(caps) if caps else [{} for _ in range(n_players)]
        ladder_w = {2: 4, 3: 5, 4: 6}.get(n_players, LADDER_SLOTS)
        bev_deck_size = {2: 7, 3: 9, 4: 10}.get(n_players, 7)
        dusk = {2: DUSK_MARK, 3: 5, 4: 6}.get(n_players, DUSK_MARK)
        last = {2: LASTTRAIN_MARK, 3: 9, 4: 11}.get(n_players, LASTTRAIN_MARK)
        supply = int(round(BUZZ_SUPPLY * (1 + 0.35 * (n_players - 2))))

        rdecks = {r: self._fresh_region_deck(r, rng) for r in REGIONS}
        bdeck = list(BREAKFAST); rng.shuffle(bdeck)
        ndeck = list(NM);        rng.shuffle(ndeck)
        vdeck = list(BEV);       rng.shuffle(vdeck)
        vdeck = vdeck[:bev_deck_size]                # the DECK is the hard cap on drink wins
        ladder = [bdeck.pop() for _ in range(min(ladder_w, len(bdeck)))]
        # v6.1: one persistent beverage slot in EVERY region (a drinks stand everywhere), seeded from
        # the (finite) Beverage deck. When the deck empties, refilled slots go None and stay empty.
        bevslots = {}
        for r in REGIONS:
            bevslots[r] = vdeck.pop() if vdeck else None
        starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "C", "S", "E"]}.get(
            n_players, ["N", "S"])

        players = []
        for p in range(n_players):
            ch = chars[p]
            deal_prefs = {"road": roads[p], **caps[p]}
            players.append({
                "char": ch, "road": roads[p], "caps": dict(caps[p]),
                "pos": starts[p % len(starts)],
                "larder": Counter(), "won": [], "icons": Counter(), "wild": 0,
                "prestige": 0, "rep": 0, "promote_bonus": (1 if ch == "influencer" else 0),
                "rep_per_court_bonus": 0, "councillor_regions": set(),
                "tickets": _deal_start_tickets(rng, deal_prefs),   # Tour Tickets (or the single mission)
                "booked": 0,
                "next_visit_extra_hazard": 0,        # 大胃王 H1=C carryover
                "tempo_tax": 0,                      # v6.1: pending bounded tax from a scoped hazard
            })
        if "influencer" in chars:                    # 網紅 flaw: opponents get a 2-ingredient head start
            infl = chars.index("influencer")
            for p in range(n_players):
                if p != infl:
                    players[p]["larder"][COMMON] += 2

        buzz_ids = set(ladder) | {v for v in bevslots.values() if v is not None}
        return {
            "n": n_players, "rdecks": rdecks,
            "bdeck": bdeck, "ndeck": ndeck, "vdeck": vdeck,
            "ladder": ladder, "bevslots": bevslots, "ladder_w": ladder_w,
            "buzz": {vid: [0] * n_players for vid in buzz_ids},
            "star": set(), "supply": supply, "supply_min": supply,
            "act": 1, "day_clock": 0, "dusk_mark": dusk, "last_mark": last,
            "players": players, "turn": 0, "cur": 0,
            "end_turn": None, "end_cause": None, "done": False,
            # diagnostics
            "ladder_wins": 0, "bev_wins": 0,
            "contested_ladder_wins": 0, "drink_fights": 0,
            "star_placed": 0, "star_wins": {p: 0 for p in range(n_players)},
            "max_buzz_on_vendor": 0,
            "src_by_region": {r: 0 for r in REGIONS}, "src_common": 0,
            "travels": 0, "visits": 0, "cstores": 0, "promotes": 0,
            "dusk_turn": None, "last_turn": None, "first_nm_win_turn": None,
            "legal_counts": [], "forced_turns": 0,
            # v6.1 event-scope diagnostics
            "events_fired": 0, "scope_fired": {"self": 0, "region": 0, "neigh": 0},
            "cs_self_events": 0, "cs_rival_hits": 0, "takethat_hits": 0,
            "pokes": 0, "bev_deck_empty_turn": None,
            # Tour Ticket diagnostics
            "books": 0,
        }

    def _fresh_region_deck(self, r, rng):
        cr = common_regions()
        deck = []
        if r in cr:
            share = 4 if H3 == "half_rich" else 3
            deck += ["sig"] * 5 + [COMMON] * share
            events = 4
        else:
            deck += ["sig"] * 8
            events = 3
        n_haz = max(1, round(events * EVENT_HAZARD_FRAC))
        deck += [_make_event("hazard", rng) for _ in range(n_haz)]
        deck += [_make_event("boon", rng) for _ in range(events - n_haz)]
        rng.shuffle(deck)
        return deck

    def _draw(self, s, r, rng):
        d = s["rdecks"][r]
        if not d:
            s["rdecks"][r] = self._fresh_region_deck(r, rng)
            d = s["rdecks"][r]
        return d.pop()

    def players(self, state):
        return list(range(state["n"]))

    def actors(self, state):
        return [state["cur"]]

    def view(self, state, player):
        return state

    # -------- vendor location (v6.1: a beverage's region is the slot it sits in) --------
    def _bev_region(self, s, vid):
        for r, v in s["bevslots"].items():
            if v == vid:
                return r
        return None

    def _vendor_region(self, s, vid):
        v = VENDORS[vid]
        if v["kind"] == "bev":
            return self._bev_region(s, vid)
        return v["region"]

    # -------- cost / affordability --------
    def _pay_plan(self, s, p, vid):
        pl = s["players"][p]
        v = VENDORS[vid]
        pay = {}
        for r, c in v["cost"].items():
            if r == COMMON:
                pay[COMMON] = c                        # common carries no region icon → never discounted
            else:
                pay[r] = max(0, c - pl["icons"].get(r, 0))
        w = pl["wild"]                                 # wild icons shave the largest region requirement
        regs = [r for r in pay if r != COMMON]
        while w > 0 and any(pay[r] > 0 for r in regs):
            r = max(regs, key=lambda k: pay[k])
            if pay[r] <= 0:
                break
            pay[r] -= 1
            w -= 1
        if pl["char"] == "councillor" and v["region"] is not None \
                and v["region"] not in pl["councillor_regions"] and len(pl["councillor_regions"]) < 2:
            for r in sorted(pay, key=lambda k: -pay[k]):
                if pay[r] > 0:
                    pay[r] -= 1
                    break
        if pl["char"] == "dage" and DAGE_FLAW == "tab":
            if v["region"] is not None:
                pay[v["region"]] = pay.get(v["region"], 0) + 1
            else:                                      # beverage (region-agnostic card) → tab hits common
                pay[COMMON] = pay.get(COMMON, 0) + 1
        return pay

    def _margin_for(self, pl):
        return DAGE_THRESH if pl["char"] == "dage" else BUZZ_MARGIN

    def _buzz_lead(self, s, p, vid):
        b = s["buzz"][vid]
        rival = max((b[q] for q in range(s["n"]) if q != p), default=0)
        return b[p] - rival, rival

    def _present(self, s, p, vid):
        """v6.1: presence is required for EVERY vendor type — a beverage's region is its slot."""
        vr = self._vendor_region(s, vid)
        if vr is None:
            return False
        return s["players"][p]["pos"] == vr

    def _can_bribe(self, s, p, vid):
        if not self._present(s, p, vid):
            return False
        pl = s["players"][p]
        lead, _ = self._buzz_lead(s, p, vid)
        if lead < self._margin_for(pl):
            return False
        for r, c in self._pay_plan(s, p, vid).items():
            if pl["larder"].get(r, 0) < c:
                return False
        return True

    def _promote_yield(self, pl):
        y = 2 + pl["promote_bonus"]
        if pl["char"] == "dage" and DAGE_FLAW == "promote1":
            y = 1
        return y

    def _board(self, s):
        return list(s["ladder"]) + [v for v in s["bevslots"].values() if v is not None]

    # -------- legal actions --------
    def legal_actions(self, s, p):
        pl = s["players"][p]
        acts = []
        board = self._board(s)
        for vid in board:
            if self._can_bribe(s, p, vid):
                acts.append(("bribe", vid))
        if s["supply"] > 0:
            for vid in board:
                if self._present(s, p, vid):
                    acts.append(("promote", vid))
        acts.append(("visit",))
        for r in REGIONS:
            acts.append(("cstore", r))
        for d in neighbours(pl["pos"], pl["char"]):
            acts.append(("travel", d))
        if MISSION_MODE == "tickets" and s["day_clock"] < s["last_mark"] - BOOK_LATE_MARGIN \
                and len(pl["tickets"]) < 4:
            acts.append(("book",))                     # claim a Tour Ticket (a full action; no clock tick)
        return acts

    # -------- transition --------
    def step(self, s, actions, rng):
        p = s["cur"]
        pl = s["players"][p]
        act = actions[p]
        legal = self.legal_actions(s, p)
        s["legal_counts"].append(len(legal))
        if len(legal) <= 1:
            s["forced_turns"] += 1
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
        elif kind == "book":
            self._do_book(s, p, rng)
        self._discard_to_cap(pl)
        if s["supply"] < s["supply_min"]:
            s["supply_min"] = s["supply"]
        if s["bev_deck_empty_turn"] is None and not s["vdeck"] \
                and all(v is None for v in s["bevslots"].values()):
            s["bev_deck_empty_turn"] = s["turn"]

        s["turn"] += 1
        s["cur"] = s["turn"] % s["n"]
        if s["end_turn"] is None and s["turn"] >= STALL_CAP * s["n"]:
            self._trigger_end(s, "stall")
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            s["done"] = True
        if s["turn"] > 6000:
            s["done"] = True
        return s

    def _do_promote(self, s, p, vid):
        pl = s["players"][p]
        y = min(self._promote_yield(pl), s["supply"])
        s["supply"] -= y
        s["buzz"][vid][p] += y
        s["promotes"] += 1
        s["max_buzz_on_vendor"] = max(s["max_buzz_on_vendor"], max(s["buzz"][vid]))
        if VENDORS[vid]["kind"] == "bev":
            if any(s["buzz"][vid][q] > 0 for q in range(s["n"]) if q != p):
                s["drink_fights"] += 1

    def _do_book(self, s, p, rng):
        pl = s["players"][p]
        prefs = {"road": pl["road"], **pl["caps"]}
        pl["tickets"].append(_book_keep(rng, pl["won"], prefs))   # draw 2, keep the better (a full turn)
        pl["booked"] += 1
        s["books"] += 1

    def _do_bribe(self, s, p, vid, rng):
        pl = s["players"][p]
        v = VENDORS[vid]
        for r, c in self._pay_plan(s, p, vid).items():
            pl["larder"][r] -= c
        pl["larder"] = +pl["larder"]
        _, rival_buzz = self._buzz_lead(s, p, vid)
        contested = rival_buzz > 0
        starred = vid in s["star"]
        prestige = v["prestige"] + (STAR_BONUS_P if starred else 0)
        rep = v["rep"] + (STAR_BONUS_R if starred else 0) + pl["rep_per_court_bonus"]
        pl["prestige"] += prestige
        pl["rep"] = min(12, pl["rep"] + rep)
        # v6.1: beverage cards are region-agnostic — record the SLOT region on the win so drinks-region
        # Tour Tickets ("a stand in 3 regions") can read it. Ladder patterns still filter kind != "bev".
        won_region = v["region"] if v["kind"] != "bev" else self._bev_region(s, vid)
        pl["won"].append({"id": vid, "kind": v["kind"], "region": won_region, "prestige": prestige})
        if v["region"] is not None:                    # ladder vendor → discount icon + perk
            pl["icons"][v["region"]] += 1
            self._apply_perk(pl, v)
            if pl["char"] == "councillor" and v["region"] not in pl["councillor_regions"] \
                    and len(pl["councillor_regions"]) < 2:
                pl["councillor_regions"].add(v["region"])
        if starred:
            s["star"].discard(vid)
            s["star_wins"][p] += 1
        s["supply"] += sum(s["buzz"][vid])             # clear ALL buzz → supply
        s["buzz"][vid] = [0] * s["n"]
        ladder = v["kind"] != "bev"
        if ladder:
            self._remove_and_refill_ladder(s, vid)
            s["ladder_wins"] += 1
            if contested:
                s["contested_ladder_wins"] += 1
            if v["kind"] == "nm" and s["first_nm_win_turn"] is None:
                s["first_nm_win_turn"] = s["turn"]
            self._advance_clock(s)
        else:
            self._refill_beverage(s, vid)              # refill THAT region's slot from the finite deck
            s["bev_wins"] += 1
            if contested:
                s["drink_fights"] += 1

    def _apply_perk(self, pl, v):
        perk = v["perk"]
        if perk == "double_icon":
            pl["icons"][v["region"]] += 1
        elif perk == "wild":
            pl["wild"] += 1
        elif perk == "buzz_reach":
            pl["promote_bonus"] += 1
        elif perk == "rep_plus2":
            pl["rep_per_court_bonus"] += 2

    def _remove_and_refill_ladder(self, s, vid):
        row = s["ladder"]
        deck = s["bdeck"] if s["act"] == 1 else s["ndeck"]
        if vid in row:
            row.remove(vid)
        if deck:
            nv = deck.pop()
            row.append(nv)
            s["buzz"].setdefault(nv, [0] * s["n"])

    def _refill_beverage(self, s, vid):
        r = self._bev_region(s, vid)
        if r is None:
            return
        s["bevslots"][r] = s["vdeck"].pop() if s["vdeck"] else None   # None → empty and stays empty
        nv = s["bevslots"][r]
        if nv is not None:
            s["buzz"].setdefault(nv, [0] * s["n"])

    def _advance_clock(self, s):
        s["day_clock"] += 1
        if s["act"] == 1 and s["day_clock"] >= s["dusk_mark"]:
            self._dusk(s)
        if s["day_clock"] >= s["last_mark"]:
            self._trigger_end(s, "lasttrain")
        if s["act"] == 1 and not s["bdeck"] and s["end_turn"] is None:
            self._dusk(s)                              # backstop: breakfast deck empty → dusk
        if s["act"] == 2 and not s["ndeck"] and s["end_turn"] is None:
            self._trigger_end(s, "nm_deck")            # backstop: nm deck empty → last train

    def _dusk(self, s):
        if s["act"] != 1:
            return
        s["act"] = 2
        s["dusk_turn"] = s["turn"]
        for vid in list(s["ladder"]):                  # sweep unwon ladder vendors: Buzz → supply
            s["supply"] += sum(s["buzz"].get(vid, [0] * s["n"]))
            s["buzz"][vid] = [0] * s["n"]
            s["star"].discard(vid)
        s["ladder"] = []                               # region beverage slots are NOT swept (all day)
        for _ in range(s["ladder_w"]):
            if s["ndeck"]:
                nv = s["ndeck"].pop()
                s["ladder"].append(nv)
                s["buzz"].setdefault(nv, [0] * s["n"])

    def _trigger_end(self, s, cause):
        if s["end_turn"] is not None:
            return
        s["end_cause"] = cause
        s["last_turn"] = s["turn"]
        n = s["n"]
        done = s["turn"] + 1
        s["end_turn"] = ((done + n - 1) // n) * n + n  # finish this round + one more full round

    # -------- events (v6.1: fire by scope, resolved relative to the drawn region) --------
    def _event_targets(self, s, actor, drawn_region, scope):
        if scope == "self":
            return [actor]
        if scope == "region":
            return [q for q in range(s["n"]) if s["players"][q]["pos"] == drawn_region]
        nbrs = region_neighbours(drawn_region)          # neigh
        return [q for q in range(s["n"]) if s["players"][q]["pos"] in nbrs]

    def _fire_event(self, s, actor, drawn_region, ev, rng, during_visit, origin):
        """Resolve one scoped event. Returns the keep-slot penalty to apply to the ACTOR's current Visit
        (0 for non-Visit or when the actor isn't a hazard target). Everything else (rival tempo taxes,
        boon windfalls, the dynamic ★) is applied here as a side effect."""
        _, kind, scope, sub = ev
        s["events_fired"] += 1
        s["scope_fired"][scope] += 1
        if origin == "cstore" and scope == "self":
            s["cs_self_events"] += 1
        targets = self._event_targets(s, actor, drawn_region, scope)
        penalty = 0
        if kind == "boon" and sub == "star":
            self._place_star(s)                         # place-once; targets irrelevant
            return 0
        for t in targets:
            if kind == "hazard":
                if during_visit and t == actor:
                    penalty += 1                        # eats a keep-slot on this Visit (tax-not-destroy)
                else:
                    s["players"][t]["tempo_tax"] += 1   # bounded: one fewer on their next sourcing
                if t != actor:
                    s["takethat_hits"] += 1
                    if origin == "cstore":
                        s["cs_rival_hits"] += 1
            else:                                       # boon "ingredient": a free signature windfall
                s["players"][t]["larder"][drawn_region] += 1
                s["src_by_region"][drawn_region] += 1
        return penalty

    def _apply_tempo_tax(self, pl, natural_keep):
        """Consume at most ONE pending tempo tax per sourcing action (never a whole turn)."""
        if pl["tempo_tax"] > 0 and natural_keep > 0:
            pl["tempo_tax"] -= 1
            return natural_keep - 1
        return natural_keep

    # -------- sourcing --------
    def _keep_cap(self, pl):
        if pl["char"] == "dagushi":
            return 3
        if pl["char"] == "office":
            return 1
        return 2

    def _do_visit(self, s, p, rng):
        pl = s["players"][p]
        r = pl["pos"]
        s["visits"] += 1
        cards = [self._draw(s, r, rng) for _ in range(3)]
        ings = [c for c in cards if c in ("sig", COMMON)]
        events = [c for c in cards if isinstance(c, tuple)]
        actor_haz = 0
        for ev in events:                               # fire each by scope (drawn region = your region)
            actor_haz += self._fire_event(s, p, r, ev, rng, during_visit=True, origin="visit")
        # 大胃王 H1 flaw modifies the ACTOR-targeting hazards this Visit
        haz_hits = actor_haz
        if pl["char"] == "dagushi" and H1 == "twice":
            haz_hits = actor_haz * 2
        haz_hits += pl.get("next_visit_extra_hazard", 0)
        pl["next_visit_extra_hazard"] = 0
        keep = self._keep_cap(pl)
        if pl["char"] == "dagushi" and H1 == "keep2" and actor_haz > 0:
            keep = 2
        if pl["char"] == "dagushi" and H1 == "next" and actor_haz > 0:
            pl["next_visit_extra_hazard"] += actor_haz
        keep = max(0, keep - haz_hits)
        keep = self._apply_tempo_tax(pl, keep)          # a pending tax from an earlier scoped hazard
        keep = max(0, keep)
        for c in ings[:keep]:
            tok = r if c == "sig" else COMMON
            pl["larder"][tok] += 1
            if tok == COMMON:
                s["src_common"] += 1
            else:
                s["src_by_region"][r] += 1

    def _place_star(self, s):
        cand = [vid for vid in s["ladder"] if vid not in s["star"]]
        if not cand:
            return
        tgt = min(cand, key=lambda vid: VENDORS[vid]["prestige"])
        s["star"].add(tgt)
        s["star_placed"] += 1

    def _do_cstore(self, s, p, r, rng):
        pl = s["players"][p]
        s["cstores"] += 1
        c = self._draw(s, r, rng)
        if c in ("sig", COMMON):
            got = self._apply_tempo_tax(pl, 1)          # a pending tax can eat this blind grab
            if got > 0:
                tok = r if c == "sig" else COMMON
                pl["larder"][tok] += 1
                if tok == COMMON:
                    s["src_common"] += 1
                else:
                    s["src_by_region"][r] += 1
        else:                                           # v6.1: the CS now FIRES the event by scope
            self._fire_event(s, p, r, c, rng, during_visit=False, origin="cstore")

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        draw_region = src if pl["char"] == "office" else dest   # 媽寶: draw the region you LEFT
        c = self._draw(s, draw_region, rng)
        if c in ("sig", COMMON):                        # an event on a Travel fly-by WHIFFS (no fire)
            got = self._apply_tempo_tax(pl, 1)
            if got > 0:
                tok = draw_region if c == "sig" else COMMON
                pl["larder"][tok] += 1
                if tok == COMMON:
                    s["src_common"] += 1
                else:
                    s["src_by_region"][draw_region] += 1

    def _discard_to_cap(self, pl):
        total = sum(pl["larder"].values())
        if total <= LARDER_CAP:
            return
        for _ in range(total - LARDER_CAP):
            tok = max((k for k in pl["larder"] if pl["larder"][k] > 0),
                      key=lambda k: pl["larder"][k])
            pl["larder"][tok] -= 1
        pl["larder"] = +pl["larder"]

    def is_over(self, s):
        return s["done"]

    # -------- scoring --------
    def scores(self, s):
        out = {}
        for p in range(s["n"]):
            pl = s["players"][p]
            out[p] = pl["prestige"] + _rep_end_vp(pl["rep"]) + _ticket_final_score(pl)
        return out

    def metrics(self, s):
        sc = self.scores(s)
        vals = sorted(sc.values(), reverse=True)
        margin = vals[0] - vals[1] if len(vals) > 1 else 0.0
        best = max(sc.values())
        winners = [p for p, v in sc.items() if v == best]
        tie = 1.0 if len(winners) > 1 else 0.0
        winner = winners[0]
        wp = s["players"][winner]
        total_wins = s["ladder_wins"] + s["bev_wins"]
        src = s["src_by_region"]
        src_tot = sum(src.values()) + s["src_common"]
        ev = s["events_fired"] or 1

        def share(x):
            return (x / src_tot) if src_tot else 0.0
        return {
            "margin": float(margin),
            "tie": tie,
            "turns": float(s["turn"]),
            "turns_per_player": float(s["turn"] / s["n"]),
            "ladder_wins": float(s["ladder_wins"]),
            "bev_wins": float(s["bev_wins"]),
            "bev_win_share": float(s["bev_wins"] / total_wins) if total_wins else 0.0,
            "wins_per_player": float(total_wins / s["n"]),
            "drink_fights": float(s["drink_fights"]),
            "contested_ladder_wins": float(s["contested_ladder_wins"]),
            "contested_ladder_frac": float(s["contested_ladder_wins"] / s["ladder_wins"]) if s["ladder_wins"] else 0.0,
            "max_buzz_on_vendor": float(s["max_buzz_on_vendor"]),
            "buzz_supply_min": float(s["supply_min"]),
            "star_placed": float(s["star_placed"]),
            "star_wins_total": float(sum(s["star_wins"].values())),
            "winner_star_wins": float(s["star_wins"][winner]),
            "dusk_turn": float(s["dusk_turn"]) if s["dusk_turn"] is not None else float(s["turn"]),
            "last_turn": float(s["last_turn"]) if s["last_turn"] is not None else float(s["turn"]),
            "first_nm_win_turn": float(s["first_nm_win_turn"]) if s["first_nm_win_turn"] is not None else float(s["turn"]),
            "end_by_lasttrain": 1.0 if s["end_cause"] == "lasttrain" else 0.0,
            "end_by_nm_deck": 1.0 if s["end_cause"] == "nm_deck" else 0.0,
            "end_by_stall": 1.0 if s["end_cause"] == "stall" else 0.0,
            "travels_per_game": float(s["travels"]),
            "visits_per_game": float(s["visits"]),
            "cstores_per_game": float(s["cstores"]),
            "src_share_N": share(src["N"]), "src_share_C": share(src["C"]),
            "src_share_S": share(src["S"]), "src_share_E": share(src["E"]),
            "src_share_common": float(s["src_common"] / src_tot) if src_tot else 0.0,
            "avg_legal_actions": float(statistics.mean(s["legal_counts"])) if s["legal_counts"] else 0.0,
            "forced_turn_frac": float(s["forced_turns"] / len(s["legal_counts"])) if s["legal_counts"] else 0.0,
            # v6.1 event-scope diagnostics
            "events_fired_per_game": float(s["events_fired"]),
            "scope_self_frac": float(s["scope_fired"]["self"] / ev),
            "scope_region_frac": float(s["scope_fired"]["region"] / ev),
            "scope_neigh_frac": float(s["scope_fired"]["neigh"] / ev),
            "cs_self_events_per_game": float(s["cs_self_events"]),
            "cs_rival_hits_per_game": float(s["cs_rival_hits"]),
            "takethat_hits_per_game": float(s["takethat_hits"]),
            "pokes_per_game": float(s["pokes"]),
            # Tour Ticket diagnostics
            "books_per_game": float(s["books"]),
            "tickets_held_winner": float(len(wp["tickets"])),
            "tickets_done_winner": float(sum(1 for k in wp["tickets"] if _mission_done(k, wp["won"]))),
            "ticket_net_winner": float(_ticket_final_score(wp)),
            "win_prestige": float(wp["prestige"]),
            "win_rep_vp": float(_rep_end_vp(wp["rep"])),
            "win_ticket_score": float(_ticket_final_score(wp)),
            "win_total": float(best),
        }


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan (v6.1 — the economy fork, region-anchored + scoped events)"


# ==================================================================================================
#  SHARED ENGINE BRAIN — every strategy scores the legal actions with THIS planner; strategies differ
#  ONLY in road weights (w_ladder / w_bev) + a pure_drinks flag. Isolates the v6/v6.1 fork question.
# ==================================================================================================
TEMPO = 1.1


def _needs(view, p, vid):
    pay = GAME._pay_plan(view, p, vid)
    pl = view["players"][p]
    need = Counter()
    for r, c in pay.items():
        short = c - pl["larder"].get(r, 0)
        if short > 0:
            need[r] = short
    return need


def _buzz_short_real(view, p, vid, pl):
    """Buzz shortfall to reach the margin, inflated by the rival's committed Buzz (anticipating a
    re-match). This is what makes a heavily-contested vendor progressively unattractive → concession."""
    _, rival = GAME._buzz_lead(view, p, vid)
    margin = GAME._margin_for(pl)
    raw = max(0, rival + margin - view["buzz"][vid][p])
    return raw + 0.6 * rival


def _ramp_value(pl, v, w):
    if v["perk"] in ("wild", "double_icon"):
        return w * 1.3
    if v["perk"] == "icon":
        held = pl["icons"].get(v["region"], 0)
        return w * (0.5 + 0.4 * held)
    return 0.0


def _rep_marginal(pl, v):
    now = _rep_end_vp(pl["rep"])
    then = _rep_end_vp(min(12, pl["rep"] + v["rep"] + pl["rep_per_court_bonus"]))
    return 0.5 * (v["rep"] + pl["rep_per_court_bonus"]) + (then - now)


def _tickets_marginal(view, p, vid):
    """Value of winning this vendor toward the bot's held (incomplete) Tour Tickets — completing one is
    worth ~its value (banks the +value AND dodges the −half penalty); progressing one is a fraction. This
    is what a ticket buys that a flat 2-VP drink never could: a payoff the greedy planner can see."""
    pl = view["players"][p]
    v = VENDORS[vid]
    reg = GAME._vendor_region(view, vid) if v["kind"] == "bev" else v["region"]
    cand = {"id": v["id"], "kind": v["kind"], "region": reg, "prestige": v["prestige"]}
    total = 0.0
    for key in pl["tickets"]:
        if _mission_done(key, pl["won"]):
            continue
        if _mission_helps(key, cand, pl["won"]):
            after = _mission_done(key, pl["won"] + [cand])
            val = _ticket_value(key)
            total += (val * 0.85) if after else (val * 0.2)
    return total


def _road_value(view, p, vid, prefs):
    pl = view["players"][p]
    v = VENDORS[vid]
    prestige = v["prestige"] + (STAR_BONUS_P if vid in view["star"] else 0)
    core = prestige + _rep_marginal(pl, v)             # the road-flavoured value (prestige/rep/ramp)
    if v["region"] is not None:                        # ladder (beverage cards are region-agnostic)
        core += _ramp_value(pl, v, 1.0)
        core *= prefs["w_ladder"]
    else:
        core *= prefs["w_bev"]
    # a Tour Ticket payoff is worth its points REGARDLESS of road preference — it must NOT be scaled down
    # by w_bev, or a ladder/mix bot would never pursue the drink its own mix ticket needs.
    return core + _tickets_marginal(view, p, vid)


def _est_actions(view, p, vid):
    pl = view["players"][p]
    need = _needs(view, p, vid)
    ing = sum(need.values())
    bz = _buzz_short_real(view, p, vid, pl)
    py = GAME._promote_yield(pl)
    eff_region = GAME._vendor_region(view, vid)        # v6.1: beverages are region-anchored too
    travel = 1 if (eff_region is not None and pl["pos"] != eff_region) else 0
    return 0.7 * ing + (bz / py) + travel + 1.0


def _pick_target(view, p, prefs):
    board = GAME._board(view)
    best, bscore = None, -1e9
    for vid in board:
        if prefs["pure_drinks"] and VENDORS[vid]["region"] is not None:
            continue
        if prefs.get("no_drinks") and VENDORS[vid]["region"] is None:
            continue
        val = _road_value(view, p, vid, prefs)
        score = val - TEMPO * (_est_actions(view, p, vid) - 1.0)
        if score > bscore:
            bscore, best = score, vid
    return best


def _get_common(view, p, legal, prefs):
    """Best way to source the COMMON for this bot. In a common region → VISIT (flip 3, you're at the
    stand). A drinks-leaning bot not at the supply RELOCATES to the nearest common region (co-locate with
    the common AND a courtable stand) rather than blindly remote-CS'ing at ~25% yield. Everyone else grabs
    it remotely from the Convenience Store (from anywhere)."""
    pl = view["players"][p]
    if pl["pos"] in common_regions() and ("visit",) in legal:
        return ("visit",)
    if prefs["road"] == "drinks":
        dest = _nearest_common(pl["pos"], pl["char"])
        if dest is not None:
            hop = _next_hop(pl["pos"], dest, pl["char"])
            if ("travel", hop) in legal:
                return ("travel", hop)
    for r in common_regions():
        if ("cstore", r) in legal:
            return ("cstore", r)
    return None


def _poke(view, p, legal):
    """v6.1 light deliberate poke: when there's nothing productive to do, CS-flip a rival's region
    (a blind, low-stakes scope poke). Returns an action or None."""
    if not POKE_ENABLED:
        return None
    rival_regions = {view["players"][q]["pos"] for q in range(view["n"]) if q != p}
    for r in rival_regions:
        if ("cstore", r) in legal:
            return ("cstore", r)
    return None


def _should_book(view, p, legal):
    """Claim a fresh Tour Ticket once you've DELIVERED everything you hold (pure upside) and there's still
    time — the TtR 'do I book another?' beat. Un-finishable held tickets never clear, so a bot that kept a
    bad ticket simply won't re-book (and eats that penalty) — the discipline is in the keep, not here."""
    if ("book",) not in legal:
        return False
    pl = view["players"][p]
    incomplete = [k for k in pl["tickets"] if not _mission_done(k, pl["won"])]
    # hold up to 2 live tickets at once (stack a cheap drinks/mix ticket alongside a ladder one — the
    # "complete more than one objective" idea); book early enough that a fresh one is still finishable
    return len(incomplete) < 2 and view["day_clock"] < view["last_mark"] - 2


def _plan(view, p, legal, rng, prefs):
    pl = view["players"][p]
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs["pure_drinks"] and VENDORS[a[1]]["region"] is not None)
              and not (prefs.get("no_drinks") and VENDORS[a[1]]["region"] is None)]
    if bribes:
        return max(bribes, key=lambda a: _road_value(view, p, a[1], prefs))

    if _should_book(view, p, legal):
        return ("book",)

    tgt = _pick_target(view, p, prefs)
    if tgt is None:
        # nothing worth chasing → source the common for our own use, else poke, else visit
        act = _get_common(view, p, legal, prefs)
        if act is not None:
            return act
        pk = _poke(view, p, legal)
        if pk is not None:
            view["pokes"] += 1
            return pk
        return ("visit",) if ("visit",) in legal else legal[0]

    v = VENDORS[tgt]
    eff = GAME._vendor_region(view, tgt)               # where the target physically sits
    need = _needs(view, p, tgt)
    lead, _rival = GAME._buzz_lead(view, p, tgt)
    margin = GAME._margin_for(pl)
    present = GAME._present(view, p, tgt)

    if not present:
        pos = pl["pos"]
        if need.get(pos, 0) > 0 and ("visit",) in legal:
            return ("visit",)
        if need.get(COMMON, 0) > 0 and pos in common_regions() and ("cstore", pos) in legal:
            return ("cstore", pos)
        hop = _next_hop(pos, eff, pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    if sum(need.values()) > 0:
        if need.get(COMMON, 0) > 0:
            act = _get_common(view, p, legal, prefs)
            if act is not None:
                return act
        if present and need.get(pl["pos"], 0) > 0 and ("visit",) in legal:
            return ("visit",)
        for r in REGIONS:
            if need.get(r, 0) > 0 and r != pl["pos"]:
                hop = _next_hop(pl["pos"], r, pl["char"])
                if ("travel", hop) in legal:
                    return ("travel", hop)
        if ("visit",) in legal:
            return ("visit",)

    if lead < margin and present and ("promote", tgt) in legal:
        return ("promote", tgt)
    if lead < margin and not present:
        hop = _next_hop(pl["pos"], eff, pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    if prefs["road"] == "drinks":
        act = _get_common(view, p, legal, prefs)
        if act is not None:
            return act
    # last resort: if our larder is fullish (sourcing pointless), a cheeky poke; else just Visit
    if sum(pl["larder"].values()) >= LARDER_CAP - 1:
        pk = _poke(view, p, legal)
        if pk is not None:
            view["pokes"] += 1
            return pk
    if ("visit",) in legal:
        return ("visit",)
    return legal[0]


def _make(prefs):
    def agent(view, p, legal, rng):
        return _plan(view, p, legal, rng, prefs)
    return agent


def s_random(view, p, legal, rng):
    return rng.choice(legal)


def s_greedy_prestige(view, p, legal, rng):
    prefs = {"w_ladder": 1.0, "w_bev": 1.0, "pure_drinks": False, "road": "mixed"}
    bribes = [a for a in legal if a[0] == "bribe"]
    if bribes:
        return max(bribes, key=lambda a: VENDORS[a[1]]["prestige"])
    return _plan(view, p, legal, rng, prefs)


# The "clever mix" the DESIGN INTENDS: ladder is the main game, and you bank an easy drink AT THE RIGHT
# TIME — a stand you're already standing next to, that you can already pay for, on a turn your ladder plan
# would otherwise be a non-progress dig. A one-step greedy value/action planner is blind to this timing
# value (a drink always scores worse per-action than a night-market vendor), so this wraps the ladder
# planner with the explicit opportunistic-close rule. This tests the CD's actual bar:
# "a clever mix of drinks at the right time + night markets should be a good strategy."
_SMART_PREFS = {"w_ladder": 1.25, "w_bev": 0.4, "pure_drinks": False, "road": "ladder"}


def _opportunistic_drink(view, p, legal):
    """A guaranteed-2-VP local stand to bank on a dead beat: present, affordable now, and either already
    at the majority (bribe) or one Promote from it. Returns an action or None."""
    pl = view["players"][p]
    bev = view["bevslots"].get(pl["pos"])
    if bev is None:
        return None
    if not all(pl["larder"].get(k, 0) >= c for k, c in GAME._pay_plan(view, p, bev).items()):
        return None                                    # can't pay without diverting sourcing → not free
    lead, _ = GAME._buzz_lead(view, p, bev)
    if lead >= GAME._margin_for(pl) and ("bribe", bev) in legal:
        return ("bribe", bev)
    if ("promote", bev) in legal:
        return ("promote", bev)                        # set up the close; next beat banks it
    return None


def s_smart_mix(view, p, legal, rng):
    # a real ladder bribe always wins the turn (progress > an easy drink)
    ladder_bribes = [a for a in legal if a[0] == "bribe" and VENDORS[a[1]]["region"] is not None]
    if ladder_bribes:
        return max(ladder_bribes, key=lambda a: _road_value(view, p, a[1], _SMART_PREFS))
    base = _plan(view, p, legal, rng, _SMART_PREFS)
    # only when the ladder plan is a non-progress dig/idle do we bank an easy local drink
    if base in (("visit",),) or (isinstance(base, tuple) and base[0] == "cstore"):
        opp = _opportunistic_drink(view, p, legal)
        if opp is not None:
            return opp
    return base


STRATEGIES = {
    "random":       s_random,
    "greedy_prest": s_greedy_prestige,
    "ladder_only":  _make({"w_ladder": 1.25, "w_bev": 0.0,  "pure_drinks": False, "no_drinks": True, "road": "ladder"}),
    "ladder_lean":  _make({"w_ladder": 1.25, "w_bev": 0.35, "pure_drinks": False, "road": "ladder"}),
    "drinks_lean":  _make({"w_ladder": 0.7,  "w_bev": 1.6,  "pure_drinks": False, "road": "drinks"}),
    "pure_drinks":  _make({"w_ladder": 0.0,  "w_bev": 1.0,  "pure_drinks": True,  "road": "drinks"}),
    "mixed":        _make({"w_ladder": 1.0,  "w_bev": 1.0,  "pure_drinks": False, "road": "mixed"}),
    "smart_mix":    s_smart_mix,
}


# ==================================================================================================
#  __main__ — character balance + H1/H2/H3/H4 probes (uses the harness directly, like beacon.py)
# ==================================================================================================
def _run(chars, roads, n=1500, seed=1):
    from engine import run_match

    class _G:
        def new_state(_self, rng):
            return GAME.new_state(rng, 2, characters=chars, roads=roads)

        def __getattr__(_self, k):
            return getattr(GAME, k)
    g = _G()
    w = [0, 0]; t = 0; sums = [0.0, 0.0]
    for i in range(n):
        sc, _mt = run_match(g, {0: _agent_for(roads[0]), 1: _agent_for(roads[1])}, seed + i)
        sums[0] += sc[0]; sums[1] += sc[1]
        if sc[0] == sc[1]:
            t += 1
        else:
            w[0 if sc[0] > sc[1] else 1] += 1
    return w[0] / n, w[1] / n, t / n, sums[0] / n, sums[1] / n


def _agent_for(road):
    return {"ladder": STRATEGIES["ladder_lean"], "drinks": STRATEGIES["drinks_lean"]}.get(
        road, STRATEGIES["mixed"])


# capability/road labels so ticket dealing+booking align with each named strategy's real intent
STRAT_CAPS = {"ladder_only": {"no_drinks": True}, "pure_drinks": {"pure_drinks": True}}
STRAT_ROAD = {"ladder_only": "ladder", "ladder_lean": "ladder", "drinks_lean": "drinks",
              "pure_drinks": "drinks", "mixed": "mixed", "smart_mix": "ladder",
              "greedy_prest": "mixed", "random": "mixed"}


def _versus(sa, sb, n=1500, seed=1):
    """A's win rate vs B, both seatings averaged, with each side's ticket capability/road wired in."""
    from engine import run_match
    ca, cb = STRAT_CAPS.get(sa, {}), STRAT_CAPS.get(sb, {})
    ra, rb = STRAT_ROAD.get(sa, "mixed"), STRAT_ROAD.get(sb, "mixed")

    def series(x, y, cx, cy, rx, ry, seed0):
        class _G:
            def new_state(_s, rng):
                return GAME.new_state(rng, 2, characters=["neutral", "neutral"],
                                      roads=[rx, ry], caps=[cx, cy])

            def __getattr__(_s, k):
                return getattr(GAME, k)
        gg = _G(); w = 0; t = 0
        for i in range(n):
            sc, _ = run_match(gg, {0: STRATEGIES[x], 1: STRATEGIES[y]}, seed0 + i)
            if sc[0] == sc[1]:
                t += 1
            elif sc[0] > sc[1]:
                w += 1
        return w, t
    wA, tA = series(sa, sb, ca, cb, ra, rb, seed)
    wB, tB = series(sb, sa, cb, ca, rb, ra, seed + n)
    return ((wA + 0.5 * tA) + ((n - wB - tB) + 0.5 * tB)) / (2 * n)


def _char_winrate(ch, n=1200, seed=1):
    a0, b0, t0, _, _ = _run([ch, "neutral"], ["mixed", "mixed"], n=n, seed=seed)
    a1, b1, t1, _, _ = _run(["neutral", ch], ["mixed", "mixed"], n=n, seed=seed + n)
    return ((a0 + 0.5 * t0) + (b1 + 0.5 * t1)) / 2


def _drinks_winrate(n=1500, seed=1):
    a0, _, t0, _, _ = _run(["neutral", "neutral"], ["drinks", "ladder"], n=n, seed=seed)
    _, b1, t1, _, _ = _run(["neutral", "neutral"], ["ladder", "drinks"], n=n, seed=seed + n)
    return ((a0 + 0.5 * t0) + (b1 + 0.5 * t1)) / 2


if __name__ == "__main__":
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _SIM = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "tools", "sim"))
    if _SIM not in sys.path:
        sys.path.insert(0, _SIM)

    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    print(f"# {TITLE} — character & knob probes ({N} games/cell)\n")

    print("## Character balance (char vs neutral, mixed road, both seatings) — target 45-55%")
    for ch in ("councillor", "office", "influencer", "dagushi", "dage"):
        wr = _char_winrate(ch, n=N)
        flag = "OK" if 0.45 <= wr <= 0.55 else "<-- OUT OF BAND"
        print(f"  {ch:12} {wr*100:5.1f}%  {flag}")

    print("\n## H2 — 大哥 threshold+flaw (大哥 vs neutral, both seatings)")
    for label, thr, flaw in (("A tie(>=0)+tab", 0, "tab"), ("B tie(>=0)+promote1", 0, "promote1"),
                             ("C lead(>=1)+tab", 1, "tab")):
        globals()["DAGE_THRESH"] = thr; globals()["DAGE_FLAW"] = flaw
        print(f"  {label:22} 大哥 {_char_winrate('dage', n=N)*100:5.1f}%")
    globals()["DAGE_THRESH"] = 0; globals()["DAGE_FLAW"] = "tab"

    print("\n## H1 — 大胃王 flaw (大胃王 vs neutral, both seatings)")
    for label, mode in (("A hazards-twice", "twice"), ("B keep-only-2", "keep2"), ("C next-fires", "next")):
        globals()["H1"] = mode
        print(f"  {label:16} 大胃王 {_char_winrate('dagushi', n=N)*100:5.1f}%")
    globals()["H1"] = "twice"

    print("\n## H3 — common availability (drinks_lean vs ladder_lean, both seatings) — target both <=~55%")
    for label, mode in (("A half (C&S)", "half"), ("B every region", "every"), ("C half-rich", "half_rich")):
        globals()["H3"] = mode
        dw = _drinks_winrate(n=N)
        print(f"  {label:16} drinks_lean {dw*100:5.1f}%  (ladder_lean {100-dw*100:5.1f}%)")
    globals()["H3"] = "half"

    print("\n## H4 — event-scope ratio (drinks_lean vs ladder_lean; the v6.1 CS-tax knob)")
    for label, sf, sr, sn in (("A proposal 40/40/20", 0.40, 0.40, 0.20),
                              ("B lighter 55/30/15", 0.55, 0.30, 0.15),
                              ("C spicier 25/50/25", 0.25, 0.50, 0.25)):
        globals()["SCOPE_SELF"] = sf; globals()["SCOPE_REGION"] = sr; globals()["SCOPE_NEIGH"] = sn
        dw = _drinks_winrate(n=N)
        print(f"  {label:22} drinks_lean {dw*100:5.1f}%  (ladder_lean {100-dw*100:5.1f}%)")
    globals()["SCOPE_SELF"] = 0.40; globals()["SCOPE_REGION"] = 0.40; globals()["SCOPE_NEIGH"] = 0.20

    print("\n## H5 — TOUR TICKETS A/B: does a well-timed mix now BEAT pure ladder? (>50% = yes)")
    print("   (a ticket payoff is greedy-visible, unlike a flat drink — so this is testable)")
    for mode in ("single", "tickets"):
        globals()["MISSION_MODE"] = mode
        sm = _versus("smart_mix", "ladder_only", n=N)
        mx = _versus("mixed", "ladder_only", n=N)
        dl = _versus("drinks_lean", "ladder_only", n=N)
        print(f"  MISSION_MODE={mode:8}  smart_mix {sm*100:5.1f}%  |  mixed {mx*100:5.1f}%  |  "
              f"drinks_lean {dl*100:5.1f}%   (vs ladder_only)")
    globals()["MISSION_MODE"] = "tickets"
