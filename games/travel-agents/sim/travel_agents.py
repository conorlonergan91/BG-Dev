"""
travel_agents.py — Travel Agents: Taiwan (v6 · THE ECONOMY FORK) encoded for the simulation harness
(see tools/sim/engine.py). Stdlib-only.

This is a FULL REWRITE to the v6 design (design/design-doc.md · "v6 — the economy fork"). Everything from
the v3.1 sim (Poach, Extract, the Season counter, T1/T2/T3 tiers, the Region-Coverage scoring track, the
~10-ingredient + wild-pantry palette) has been SWEPT OUT — none of it survives into v6.

What v6 is (the spine the sim must model):
  * ONE action per turn from five: VISIT THE LOCAL MARKET / CONVENIENCE STORE / TRAVEL / PROMOTE / BRIBE.
  * A TWO-ZONE Vendor Board:
      - THE LADDER — contested, region-gated, drives the day-clock. Breakfast shops (Act I) sweep to
        night-market stalls (Act II) at dusk. The ★ apex vendors live here.
      - THE BEVERAGE ROW — persistent, region-free, never swept, OFF the day-clock. The "easy points" fork.
  * FIVE ingredients: one signature per region (N pork / C tea / S seafood / E rice) + one COMMON (K, 糖
    sugar) that lives in HALF the regions (H3=A → C & S). Common feeds beverages + the Convenience Store.
  * BUZZ-MAJORITY fight: Promote places Buzz on a vendor you're with; to Bribe you must be with it, hold a
    ≥2 Buzz lead over the rival (≥0 for 大哥), and pay ingredients (− region-icon discounts). On a win, ALL
    Buzz on it clears to the supply; you gain Prestige + Rep + a perk (+ a region discount icon, ladder
    only). A LADDER Bribe advances the day-clock +1; a BEVERAGE Bribe does NOT.
  * DAY-CLOCK: dusk (Act I→II) at the 4th table-wide LADDER win @2p; last train (game end) at the 7th.
    Backstops: breakfast-deck exhaustion → dusk; night-market-deck exhaustion → last train; plus a hard
    turn-cap "stall" backstop (surfaces the drinks-drag pacing risk — see metric end_by_stall).
  * END scoring = Σ Prestige + Reputation end-VP (3-5→+2 / 6-8→+4 / 9-11→+6 / 12→+9) + hidden +7 mission.
  * ★ SWING: apex night-market vendors carry a printed ★ (7-8 Prestige); a dynamic "vendor gets hot" boon
    drops a ★ token (+2 Prestige/+1 Rep) on the lowest-Prestige unstarred LADDER vendor.
  * 5 CHARACTERS (start config = the CD's sign-off; H1/H2/H3 are env-knob tunable — see below).

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (bots are a FLOOR on depth, not a ceiling)
------------------------------------------------------------------------------------------------------
Faithfully modelled: the 4-region ring + HSR(N↔S); the five actions with their exact where/effect; the
5-ingredient palette + common-in-two-regions; per-region face-down market decks (reshuffle-on-empty, which
preserves per-draw hazard density — the push-your-luck spine); Visit-flips-3-keep-2 with hazards firing
(tax-not-destroy, modelled as keep-slot reduction), Convenience/Travel single blind draw (no fire); the
Buzz-majority Bribe (≥2 lead, presence, pay ingredients − discounts), Buzz clearing to a finite supply on
a win; the ladder-only day-clock (dusk 4 / last train 7 @2p) + dusk sweep + deck backstops; the discount
ramp (region icons cheapen that region's future ingredient cost; beverages carry none); the two-zone board
(4 ladder slots / 2 beverage slots @2p); Prestige + Rep-end-VP + the +7 mission (draw-3-keep-1, aligned
pick); the ★ printed apex + the dynamic ★ boon; the five characters (ability + flaw, H1/H2/H3 knobs).

Simplifications (the sim's blind spots — hand these to the table):
  * SHARED "engine brain": every strategy scores the legal actions with ONE greedy planner; strategies
    differ ONLY in their ROAD WEIGHTS (ladder vs beverage) + a pure-drinks flag. This isolates the v6 #1
    question — "is the drinks fork viable but not dominant?" — exactly as beacon.py isolates signal policy.
  * Ingredients are tracked per-token (N/C/S/E/K). A region's market yields its signature (+ common in the
    two carrying regions); hazards are modelled by their MECHANICAL payload (a keep-slot tempo tax), boons
    by theirs (a free ingredient / the dynamic ★). Exact tile text is the feel-test's job.
  * The Buzz war is resolved by a CONCESSION heuristic: a bot's appetite for a contested vendor falls as
    the rival's committed Buzz rises (anticipating a re-match), so the player who values it less switches
    to an uncontested target — the design's "outraced, not robbed". Deterministic mirrors will deadlock/tie
    on identical top targets (the mirror caveat); read depth from cross-strategy play.
  * Missions: the bot keeps the dealt mission best aligned to its road weights (draw-3-keep-1); it does not
    read the opponent's mission.
  * ASSUMPTIONS where the doc left a value open are tagged `# ASSUMPTION:` and gathered in sim-notes.md.

Run:
    python tools/sim/simulate.py --module games/travel-agents/sim/travel_agents.py --n 3000 \
        --out games/travel-agents/playtests/sim-results.md
    python games/travel-agents/sim/travel_agents.py            # runs the character + H1/H2/H3 probes
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
BEV_SLOTS      = int(os.environ.get("TA_BEV_SLOTS", "2"))       # 2p beverage-row width
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
STAR_BOON_CHANCE  = float(os.environ.get("TA_STARBOON", "0.35"))# of boons flipped on a Visit, this frac drop a ★

# ==================================================================================================
#  MAP
# ==================================================================================================
REGIONS = ("N", "C", "S", "E")
# ring N-C-S-E + HSR(N↔S). ring neighbours: N-C, C-S, S-E, E-N.
RING = {"N": ["C", "E"], "C": ["N", "S"], "S": ["C", "E"], "E": ["S", "N"]}
HSR = ("N", "S")
COMMON = "K"                                        # the common ingredient (糖 sugar)


def neighbours(pos, char=None):
    ns = list(RING[pos])
    if char != "councillor" and pos in HSR:         # 里長伯 cannot use HSR
        other = HSR[1] if pos == HSR[0] else HSR[0]
        if other not in ns:
            ns.append(other)
    return ns


def common_regions():
    if H3 == "every":
        return set(REGIONS)
    return {"C", "S"}                               # A / C: half (the South/Central refining belt)


def _next_hop(pos, dest, char=None):
    """BFS one step from pos toward dest over the character's legal adjacency."""
    if pos == dest:
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


# ==================================================================================================
#  VENDOR TABLE (baked v6 set — a representative value curve per the design's Economy section)
# ==================================================================================================
# A vendor: id, kind ("breakfast"|"nm"|"bev"), region (icon region; None for bev), cost (Counter over
# N/C/S/E/K), prestige, rep, perk, star (printed apex ★). Perks: "icon"(base ramp), "double_icon",
# "wild", "buzz_reach"(Promote +1), "rep_plus2".
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

    # --- Beverage shops 飲料店 (~7, persistent region-free row): flat easy points, no icon.
    for c in ({"K": 1}, {"K": 2}, {"K": 1}, {"K": 2}, {"K": 1, "C": 1}, {"K": 1}, {"K": 2}):
        add("bev", None, c, BEV_VALUE, BEV_REP, None)
    return vends


VENDORS = _build_vendors()
BREAKFAST = [v["id"] for v in VENDORS if v["kind"] == "breakfast"]
NM        = [v["id"] for v in VENDORS if v["kind"] == "nm"]
BEV       = [v["id"] for v in VENDORS if v["kind"] == "bev"]


# ==================================================================================================
#  MISSIONS (secret +7; draw-3-keep-1 → bot keeps the one aligned to its road weights)
# ==================================================================================================
MISSIONS = ("grand_tour", "south_3", "breakfast_3", "beverage_3", "nm_2",
            "three_regions", "prestige_12", "volume_5")


def _mission_progress(key, won):
    ladder = [v for v in won if v["kind"] != "bev"]
    if key == "grand_tour":
        return len(set(v["region"] for v in ladder)), 4
    if key == "south_3":
        return sum(1 for v in ladder if v["region"] == "S"), 3
    if key == "breakfast_3":
        return sum(1 for v in won if v["kind"] == "breakfast"), 3
    if key == "beverage_3":
        return sum(1 for v in won if v["kind"] == "bev"), 3
    if key == "nm_2":
        return sum(1 for v in won if v["kind"] == "nm"), 2
    if key == "three_regions":
        return len(set(v["region"] for v in ladder)), 3
    if key == "prestige_12":
        return sum(v["prestige"] for v in won), 12
    if key == "volume_5":
        return len(won), 5
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


def _pick_mission(rng, road):
    """draw-3-keep-1: deal 3, keep the one best aligned to road (drinks lean → beverage_3)."""
    deal = rng.sample(MISSIONS, 3)
    pref = {"beverage_3": 3.0, "volume_5": 1.6} if road == "drinks" else \
           {"grand_tour": 2.0, "nm_2": 2.0, "prestige_12": 1.8, "south_3": 1.4, "breakfast_3": 1.2}
    return max(deal, key=lambda m: pref.get(m, 1.0))


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
    def new_state(self, rng, n_players=2, characters=None, roads=None):
        chars = list(characters) if characters else ["neutral"] * n_players
        roads = list(roads) if roads else ["mixed"] * n_players
        ladder_w = {2: 4, 3: 5, 4: 6}.get(n_players, LADDER_SLOTS)
        bev_w = {2: 2, 3: 2, 4: 3}.get(n_players, BEV_SLOTS)
        dusk = {2: DUSK_MARK, 3: 5, 4: 6}.get(n_players, DUSK_MARK)
        last = {2: LASTTRAIN_MARK, 3: 9, 4: 11}.get(n_players, LASTTRAIN_MARK)
        supply = int(round(BUZZ_SUPPLY * (1 + 0.35 * (n_players - 2))))

        rdecks = {r: self._fresh_region_deck(r, rng) for r in REGIONS}
        bdeck = list(BREAKFAST); rng.shuffle(bdeck)
        ndeck = list(NM);        rng.shuffle(ndeck)
        vdeck = list(BEV);       rng.shuffle(vdeck)
        ladder = [bdeck.pop() for _ in range(min(ladder_w, len(bdeck)))]
        bevrow = [vdeck.pop() for _ in range(min(bev_w, len(vdeck)))]
        starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "C", "S", "E"]}.get(
            n_players, ["N", "S"])

        players = []
        for p in range(n_players):
            ch = chars[p]
            players.append({
                "char": ch, "road": roads[p], "pos": starts[p % len(starts)],
                "larder": Counter(), "won": [], "icons": Counter(), "wild": 0,
                "prestige": 0, "rep": 0, "promote_bonus": (1 if ch == "influencer" else 0),
                "rep_per_court_bonus": 0, "councillor_regions": set(),
                "mission": _pick_mission(rng, "drinks" if roads[p] == "drinks" else "ladder"),
                "next_visit_extra_hazard": 0,        # 大胃王 H1=C carryover
            })
        if "influencer" in chars:                    # 網紅 flaw: opponents get a 2-ingredient head start
            infl = chars.index("influencer")
            for p in range(n_players):
                if p != infl:
                    players[p]["larder"][COMMON] += 2

        return {
            "n": n_players, "rdecks": rdecks,
            "bdeck": bdeck, "ndeck": ndeck, "vdeck": vdeck,
            "ladder": ladder, "bevrow": bevrow, "ladder_w": ladder_w, "bev_w": bev_w,
            "buzz": {vid: [0] * n_players for vid in set(ladder + bevrow)},
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
        deck += ["hazard"] * n_haz + ["boon"] * (events - n_haz)
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
            else:
                pay[COMMON] = pay.get(COMMON, 0) + 1
        return pay

    def _margin_for(self, pl):
        return DAGE_THRESH if pl["char"] == "dage" else BUZZ_MARGIN

    def _buzz_lead(self, s, p, vid):
        b = s["buzz"][vid]
        rival = max((b[q] for q in range(s["n"]) if q != p), default=0)
        return b[p] - rival, rival

    def _present(self, s, p, vid):
        v = VENDORS[vid]
        if v["region"] is None:
            return True
        return s["players"][p]["pos"] == v["region"]

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

    # -------- legal actions --------
    def legal_actions(self, s, p):
        pl = s["players"][p]
        acts = []
        board = list(s["ladder"]) + list(s["bevrow"])
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
        self._discard_to_cap(pl)
        if s["supply"] < s["supply_min"]:
            s["supply_min"] = s["supply"]

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
        if VENDORS[vid]["region"] is None:
            if any(s["buzz"][vid][q] > 0 for q in range(s["n"]) if q != p):
                s["drink_fights"] += 1

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
        pl["won"].append({"id": vid, "kind": v["kind"], "region": v["region"], "prestige": prestige})
        if v["region"] is not None:
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
        self._remove_and_refill(s, vid, ladder)
        if ladder:
            s["ladder_wins"] += 1
            if contested:
                s["contested_ladder_wins"] += 1
            if v["kind"] == "nm" and s["first_nm_win_turn"] is None:
                s["first_nm_win_turn"] = s["turn"]
            self._advance_clock(s)
        else:
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

    def _remove_and_refill(self, s, vid, ladder):
        if ladder:
            row, deck = s["ladder"], (s["bdeck"] if s["act"] == 1 else s["ndeck"])
        else:
            row, deck = s["bevrow"], s["vdeck"]
        if vid in row:
            row.remove(vid)
        if deck:
            nv = deck.pop()
            row.append(nv)
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
        s["ladder"] = []
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
        hazards = sum(1 for c in cards if c == "hazard")
        boons = sum(1 for c in cards if c == "boon")
        ings = [c for c in cards if c in ("sig", COMMON)]
        haz_hits = hazards
        if pl["char"] == "dagushi" and H1 == "twice":
            haz_hits = hazards * 2
        haz_hits += pl.get("next_visit_extra_hazard", 0)
        pl["next_visit_extra_hazard"] = 0
        keep = self._keep_cap(pl)
        if pl["char"] == "dagushi" and H1 == "keep2" and hazards > 0:
            keep = 2
        if pl["char"] == "dagushi" and H1 == "next" and hazards > 0:
            pl["next_visit_extra_hazard"] += hazards
        keep = max(0, keep - haz_hits)
        for c in ings[:keep]:
            tok = r if c == "sig" else COMMON
            pl["larder"][tok] += 1
            if tok == COMMON:
                s["src_common"] += 1
            else:
                s["src_by_region"][r] += 1
        for _ in range(boons):
            if rng.random() < STAR_BOON_CHANCE:
                self._place_star(s)
            else:
                pl["larder"][r] += 1                   # "the aunty insists" — a bonus signature
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
            tok = r if c == "sig" else COMMON
            pl["larder"][tok] += 1
            if tok == COMMON:
                s["src_common"] += 1
            else:
                s["src_by_region"][r] += 1

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        draw_region = src if pl["char"] == "office" else dest   # 媽寶: draw the region you LEFT
        c = self._draw(s, draw_region, rng)
        if c in ("sig", COMMON):
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
            mission = 7 if _mission_done(pl["mission"], pl["won"]) else 0
            out[p] = pl["prestige"] + _rep_end_vp(pl["rep"]) + mission
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
            "win_prestige": float(wp["prestige"]),
            "win_rep_vp": float(_rep_end_vp(wp["rep"])),
            "win_mission": 1.0 if _mission_done(wp["mission"], wp["won"]) else 0.0,
            "win_total": float(best),
        }


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan (v6 — the economy fork)"


# ==================================================================================================
#  SHARED ENGINE BRAIN — every strategy scores the legal actions with THIS planner; strategies differ
#  ONLY in road weights (w_ladder / w_bev) + a pure_drinks flag. Isolates the v6 fork question.
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


def _mission_marginal(pl, v):
    cand = {"id": v["id"], "kind": v["kind"], "region": v["region"], "prestige": v["prestige"]}
    if _mission_helps(pl["mission"], cand, pl["won"]):
        after = _mission_done(pl["mission"], pl["won"] + [cand])
        return 6.0 if after else 1.4
    return 0.0


def _road_value(view, p, vid, prefs):
    pl = view["players"][p]
    v = VENDORS[vid]
    prestige = v["prestige"] + (STAR_BONUS_P if vid in view["star"] else 0)
    base = prestige + _rep_marginal(pl, v) + _mission_marginal(pl, v)
    if v["region"] is not None:
        base += _ramp_value(pl, v, 1.0)
        base *= prefs["w_ladder"]
    else:
        base *= prefs["w_bev"]
    return base


def _est_actions(view, p, vid):
    pl = view["players"][p]
    need = _needs(view, p, vid)
    ing = sum(need.values())
    bz = _buzz_short_real(view, p, vid, pl)
    py = GAME._promote_yield(pl)
    v = VENDORS[vid]
    travel = 1 if (v["region"] is not None and pl["pos"] != v["region"]) else 0
    return 0.7 * ing + (bz / py) + travel + 1.0


def _pick_target(view, p, prefs):
    board = list(view["ladder"]) + list(view["bevrow"])
    best, bscore = None, -1e9
    for vid in board:
        if prefs["pure_drinks"] and VENDORS[vid]["region"] is not None:
            continue
        val = _road_value(view, p, vid, prefs)
        score = val - TEMPO * (_est_actions(view, p, vid) - 1.0)
        if score > bscore:
            bscore, best = score, vid
    return best


def _plan(view, p, legal, rng, prefs):
    pl = view["players"][p]
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs["pure_drinks"] and VENDORS[a[1]]["region"] is not None)]
    if bribes:
        return max(bribes, key=lambda a: _road_value(view, p, a[1], prefs))

    tgt = _pick_target(view, p, prefs)
    if tgt is None:
        for a in legal:
            if a[0] == "cstore" and a[1] in common_regions():
                return a
        return ("visit",) if ("visit",) in legal else legal[0]

    v = VENDORS[tgt]
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
        hop = _next_hop(pos, v["region"], pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    if sum(need.values()) > 0:
        if need.get(COMMON, 0) > 0:
            for r in common_regions():
                if ("cstore", r) in legal:
                    return ("cstore", r)
        if v["region"] is not None and need.get(pl["pos"], 0) > 0 and ("visit",) in legal:
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
        hop = _next_hop(pl["pos"], v["region"], pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    if prefs["road"] == "drinks":
        for r in common_regions():
            if ("cstore", r) in legal:
                return ("cstore", r)
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


STRATEGIES = {
    "random":       s_random,
    "greedy_prest": s_greedy_prestige,
    "ladder_lean":  _make({"w_ladder": 1.25, "w_bev": 0.35, "pure_drinks": False, "road": "ladder"}),
    "drinks_lean":  _make({"w_ladder": 0.7,  "w_bev": 1.6,  "pure_drinks": False, "road": "drinks"}),
    "pure_drinks":  _make({"w_ladder": 0.0,  "w_bev": 1.0,  "pure_drinks": True,  "road": "drinks"}),
    "mixed":        _make({"w_ladder": 1.0,  "w_bev": 1.0,  "pure_drinks": False, "road": "mixed"}),
}


# ==================================================================================================
#  __main__ — character balance + H1/H2/H3 probes (uses the harness directly, like beacon.py)
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


def _char_winrate(ch, n=1200, seed=1):
    a0, b0, t0, _, _ = _run([ch, "neutral"], ["mixed", "mixed"], n=n, seed=seed)
    a1, b1, t1, _, _ = _run(["neutral", ch], ["mixed", "mixed"], n=n, seed=seed + n)
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

    print("\n## H3 — common availability (drinks_lean vs ladder_lean, both seatings)")
    for label, mode in (("A half (C&S)", "half"), ("B every region", "every"), ("C half-rich", "half_rich")):
        globals()["H3"] = mode
        a0, b0, t0, _, _ = _run(["neutral", "neutral"], ["drinks", "ladder"], n=N)
        a1, b1, t1, _, _ = _run(["neutral", "neutral"], ["ladder", "drinks"], n=N)
        drinks_wr = ((a0 + 0.5 * t0) + (b1 + 0.5 * t1)) / 2
        print(f"  {label:16} drinks_lean {drinks_wr*100:5.1f}%  (ladder_lean {100-drinks_wr*100:5.1f}%)")
    globals()["H3"] = "half"
