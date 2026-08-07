"""
travel_agents.py — Travel Agents: Taiwan (v6.2 · REGION VENDOR MARKETS + a MISSION CLOCK)
encoded for the simulation harness (see tools/sim/engine.py). Stdlib-only.

This reworks the v6.1 sim (central Ladder + region-anchored beverage slots + a ladder-only clock) to the
v6.2 PROPOSAL in design/v6.2-content-draft.md. v6.2 tears out the central Ladder and the beverage-slot
special-case; the board is now FOUR REGION VENDOR MARKETS, drinks are just the low-value vendors in each
deck, the day turns over to night at a single DUSK FLIP, and the day is paced by a MISSION CLOCK (with an
all-vendor-claims clock behind a knob for the A/B). What the spine keeps from v6.1: the Buzz-majority
public hype-fight, the 5-ingredient palette (4 signatures + 1 common in C&S), the push-your-luck market
dig with scoped events, the discount ramp on food vendors, Prestige + Rep-end-VP scoring, the dynamic ★,
and the five characters.

WHAT v6.2 MOVED — and what this rework implements:

  (1) REGION VENDOR MARKETS (no central Ladder). Each of the 4 regions has its OWN face-down vendor deck
      — a DAY deck in Act I, a NIGHT deck in Act II — with drinks mixed in as the low-value vendors. Each
      region shows 1-2 face-up (North 2, others 1), refilled in place from that region's current deck. You
      court whatever is face-up in the region you STAND in (one unified Bribe rule for everything).

  (2) THE DUSK FLIP. At dusk the ENTIRE day layer is cleared island-wide — BOTH the day vendor decks AND
      the day ingredient market decks are removed (unclaimed day vendors gone) — and the NIGHT decks are
      swapped in. Players KEEP their Larder; only the board/supply resets. The night ingredient decks use
      the SAME 5 palette but are EVENT-HEAVIER (the bustling night market).

  (3) RENEWABLE DISCARD (the anti-lockout rule). Larder cap 7; excess → that region's market discard,
      which reshuffles back into the deck when it runs dry — ingredients recycle, never removed from the
      game. Modelled as a CONSERVED per-region token pool (+ a discard that folds back in), so the hoarder
      probe + per-region signature supply size are faithful. Day discards clear at dusk.

  (4) THE VALUE SPREAD that PULLS travel: one ★ apex per region (E highest), a cross-region recipe cycle
      N→S→E→N with C feeding S, North dense-not-rich (2 slots), drinks cheap (locally sourceable K) only
      in C & S. Baked from the content draft.

  (5) TOUR TICKETS as the spine: a face-up shared ROW OF 3, claimed as a full action, scored RETROACTIVELY
      (+value / −floor(value/2) if unfinished — the penalty is a knob for the A/B), drawn from day/night/
      general pools (12 per phase in the box, 5 drawn per phase per game).

  (6) BOTH CLOCK MODES behind a knob. MISSION clock (a completed claimed mission advances the day; ~3 →
      dusk, ~3 more → last train @2p) vs the all-VENDOR-CLAIMS clock. Recommend one from the sim.

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (bots are a FLOOR on depth, not a ceiling)
------------------------------------------------------------------------------------------------------
Faithfully modelled: the 4-region ring + HSR(N↔S); the five actions; the 5-ingredient palette + common in
C&S; per-region day/night vendor decks with 2/1/1/1 face-up + refill-in-place + the dusk sweep; the
conserved per-region ingredient token pool with renewable over-cap discard; Visit-3-keep-2 with events
firing by scope; Convenience Store single blind draw firing by scope; Travel drawing the arriving region
(whiffs on an event); the Buzz-majority Bribe (≥margin lead, presence, pay ingredients −discounts) clearing
to a finite supply; the discount ramp (food only; drinks carry none); the ★ apex + dynamic ★ boon; Tour
Tickets from a shared row with retroactive ±scoring; both clock modes; the five characters.

Simplifications (the sim's blind spots — hand these to the table):
  * SHARED "engine brain": every strategy scores legal actions with ONE greedy planner; strategies differ
    only in PREFS (value/ticket/ramp/speed weights + disrupt/opportunistic/hoard flags + drink/ticket
    controls). Isolates the playstyle questions exactly as beacon.py isolates policy.
  * Event PAYLOADS abstracted: a HAZARD = a bounded, tax-not-destroy tempo tax (one fewer sourced
    ingredient); a BOON = a free ingredient windfall or (a fraction) the dynamic ★ placement. Warmth of
    rival-facing beats is the feel-test's job (bg-theme).
  * The Buzz war is resolved by a concession heuristic (appetite falls as the rival's committed Buzz
    rises); the fight's fun/tension is a table question, not a sim one.
  * ASSUMPTIONS where the draft left a value open are tagged `# ASSUMPTION:` and gathered in sim-notes.md.

Run:
    python tools/sim/simulate.py --module games/travel-agents/sim/travel_agents.py --n 2000 \
        --out games/travel-agents/playtests/sim-results.md
    python games/travel-agents/sim/travel_agents.py            # the full v6.2 probe suite
    python games/travel-agents/sim/travel_agents.py --counts 2,3,4   # the MP seat-balance smoke
"""
from __future__ import annotations

import os
import sys
import statistics
from collections import Counter, deque

# ==================================================================================================
#  SIM KNOBS (env vars; the design's open numbers — do NOT alter the printed rules)
# ==================================================================================================
BUZZ_SUPPLY  = int(os.environ.get("TA_BUZZ_SUPPLY", "24"))     # 2p Buzz supply (+~9/extra player)
BUZZ_MARGIN  = int(os.environ.get("TA_BUZZ_MARGIN", "2"))      # ≥N Buzz lead to Bribe (design 2)
LARDER_CAP   = int(os.environ.get("TA_LARDER_CAP", "7"))
STAR_BONUS_P = int(os.environ.get("TA_STAR_P", "2"))           # dynamic ★ token +Prestige
STAR_BONUS_R = int(os.environ.get("TA_STAR_R", "1"))           # dynamic ★ token +Rep
STALL_CAP    = int(os.environ.get("TA_STALL_CAP", "30"))       # hard per-player turn cap (drag backstop)

# The per-region signature SUPPLY (the hoarder / anti-lockout knob) — conserved tokens per region PER
# PHASE. Larger = denial is weaker. Common (K) supply in C&S is K_SUPPLY.
SIG_SUPPLY = int(os.environ.get("TA_SIG_SUPPLY", "10"))
K_SUPPLY   = int(os.environ.get("TA_K_SUPPLY", "6"))

# Event density (the "hotter night" knob): fraction of market draws that are events, day vs night.
DAY_EVENT_FRAC   = float(os.environ.get("TA_DAY_EVENT", "0.25"))
NIGHT_EVENT_FRAC = float(os.environ.get("TA_NIGHT_EVENT", "0.42"))
EVENT_HAZARD_FRAC = float(os.environ.get("TA_HAZARD", "0.58"))  # of events, this frac are hazards
STAR_BOON_CHANCE  = float(os.environ.get("TA_STARBOON", "0.30"))# of boons, this frac drop a dynamic ★

# Scope ratio (⦿ self / ⬢ region / ➤ neighbour); hazards skew region/neigh, boons skew self.
SCOPE_SELF   = float(os.environ.get("TA_SCOPE_SELF", "0.40"))
SCOPE_REGION = float(os.environ.get("TA_SCOPE_REGION", "0.40"))
SCOPE_NEIGH  = float(os.environ.get("TA_SCOPE_NEIGH", "0.20"))

# --- THE CLOCK (probe #5 A/B) --------------------------------------------------------------------
CLOCK_MODE = os.environ.get("TA_CLOCK", "mission")             # "mission" | "vendor"
# mission clock: completed claimed missions → dusk / last train (table-wide @2p; scale with count)
M_DUSK = int(os.environ.get("TA_M_DUSK", "3"))
M_END  = int(os.environ.get("TA_M_END",  "5"))
# vendor-claim clock: total vendor claims → dusk / last train (@2p)
V_DUSK = int(os.environ.get("TA_V_DUSK", "5"))
V_END  = int(os.environ.get("TA_V_END",  "10"))
NIGHT_SPRINT = int(os.environ.get("TA_NIGHT_SPRINT", "0"))     # >0: shorten the night half by this many

MISSION_DRAW = int(os.environ.get("TA_MISSION_DRAW", "5"))     # tickets drawn per phase (2p)
MROW = int(os.environ.get("TA_MROW", "3"))                     # face-up ticket row width

# --- THE −½ PENALTY (probe #6 A/B) ----------------------------------------------------------------
PENALTY = os.environ.get("TA_PENALTY", "half")                 # "half" (−floor(v/2)) | "zero" (score 0)

# --- CHARACTER KNOBS ------------------------------------------------------------------------------
# H1 大胃王 flaw. "twice" (A) | "keep2" (B) | "next" (C).
H1 = os.environ.get("TA_H1", "twice")
# H2 大哥 threshold+flaw. THRESH 0 (tie-win) | 1 (must-lead-by-1). FLAW "tab"(+1 ing) | "promote1" |
# "none" (no flaw) | "nocontest" (tab + can't win a CONTESTED vendor — a real brake at the tie threshold).
DAGE_THRESH = int(os.environ.get("TA_H2_THRESH", "0"))
DAGE_FLAW   = os.environ.get("TA_H2_FLAW", "tab")
# 媽寶 buff (probe #8). "none" (keep-1, v6.1) | "keep2" (keep-2 on Visit) | "travel2" (keep-1 but Travel
# arrives with 2 from the region you left).
OFFICE_BUFF = os.environ.get("TA_OFFICE", "keep2")
# 網紅 flaw magnitude (opponents' head-start ingredients). v6.1 = 2 (was hot); try 3.
INFL_BEHIND = int(os.environ.get("TA_INFL_BEHIND", "3"))

# ==================================================================================================
#  MAP
# ==================================================================================================
REGIONS = ("N", "C", "S", "E")
RING = {"N": ["C", "E"], "C": ["N", "S"], "S": ["C", "E"], "E": ["S", "N"]}
HSR = ("N", "S")
COMMON = "K"
COMMON_REGIONS = {"C", "S"}                          # where the common 糖 lives (locally sourceable)


def neighbours(pos, char=None):
    """A pawn's LEGAL travel destinations (character-aware: 里長伯 cannot use HSR)."""
    ns = list(RING[pos])
    if char != "councillor" and pos in HSR:
        other = HSR[1] if pos == HSR[0] else HSR[0]
        if other not in ns:
            ns.append(other)
    return ns


def region_neighbours(r):
    """GEOGRAPHIC adjacency (ring + HSR) — resolves a ➤ neighbour-scoped event's spill."""
    ns = set(RING[r])
    if r in HSR:
        ns.add(HSR[1] if r == HSR[0] else HSR[0])
    return ns


def _dist(pos, dest, char=None):
    if pos == dest:
        return 0
    q = deque([(pos, 0)]); seen = {pos}
    while q:
        cur, d = q.popleft()
        for nb in neighbours(cur, char):
            if nb in seen:
                continue
            if nb == dest:
                return d + 1
            seen.add(nb); q.append((nb, d + 1))
    return 99


def _next_hop(pos, dest, char=None):
    if pos == dest or dest is None:
        return pos
    q = deque([(pos, None)]); seen = {pos}
    while q:
        cur, first = q.popleft()
        for nb in neighbours(cur, char):
            if nb in seen:
                continue
            fh = nb if first is None else first
            if nb == dest:
                return fh
            seen.add(nb); q.append((nb, fh))
    return neighbours(pos, char)[0]


# ==================================================================================================
#  EVENT CARDS — ("ev", kind, scope, sub); kind hazard|boon; scope self|region|neigh; sub tempo|ingredient|star
# ==================================================================================================
def _sample_scope(kind, rng):
    if kind == "hazard":
        w = {"self": SCOPE_SELF * 0.50, "region": SCOPE_REGION * 1.25, "neigh": SCOPE_NEIGH * 1.75}
    else:
        w = {"self": SCOPE_SELF * 1.55, "region": SCOPE_REGION * 0.95, "neigh": SCOPE_NEIGH * 0.45}
    tot = sum(w.values()) or 1.0
    x = rng.random() * tot; acc = 0.0
    for s in ("self", "region", "neigh"):
        acc += w[s]
        if x <= acc:
            return s
    return "self"


def _make_event(kind, rng):
    scope = _sample_scope(kind, rng)
    if kind == "boon":
        if rng.random() < STAR_BOON_CHANCE:
            return ("ev", "boon", "region", "star")
        return ("ev", "boon", scope, "ingredient")
    return ("ev", "hazard", scope, "tempo")


# ==================================================================================================
#  VENDOR TABLE (baked v6.2 content — the per-region day/night spread from the content draft)
# ==================================================================================================
# A vendor: id, region, phase (1 day | 2 night), is_drink, cost (Counter over N/C/S/E/K),
# prestige, rep, perk ("icon"|"double_icon"|"wild"|"rep_plus2"|None), star.
def _build_vendors():
    V = []

    def add(region, phase, is_drink, cost, prestige, rep, perk, star=False):
        V.append({"id": len(V), "region": region, "phase": phase, "is_drink": is_drink,
                  "cost": Counter(cost), "prestige": prestige, "rep": rep, "perk": perk,
                  "star": star, "total_cost": sum(cost.values())})

    # --- North 北 (pork · 2 slots · no local K) ---
    add("N", 1, False, {"N": 1}, 2, 1, "icon")            # 肉包 Pork Bao
    add("N", 1, False, {"N": 1}, 1, 1, "icon")            # 蛋餅 Egg Crepe
    add("N", 1, True,  {"K": 1}, 2, 1, None)              # 豆漿 Soy Milk (drink)
    add("N", 2, False, {"N": 2}, 4, 2, "double_icon")     # 胡椒餅 Pepper Bun
    add("N", 2, False, {"N": 2, "S": 1}, 5, 2, "wild")    # 牛肉麵 Beef Noodle →S
    add("N", 2, False, {"N": 3}, 7, 3, "rep_plus2", True) # ★ 大香腸 Big Sausage
    add("N", 2, True,  {"K": 1}, 2, 1, None)              # 珍奶 Bubble Tea (drink)
    # --- Central 中 (tea · 1 slot · local K) ---
    add("C", 1, False, {"C": 1}, 2, 1, "icon")            # 肉圓 Ba-wan
    add("C", 1, False, {"C": 1}, 1, 1, "icon")            # 麵線 Misua
    add("C", 1, True,  {"K": 1}, 2, 1, None)              # 珍珠奶茶 Bubble Tea (drink)
    add("C", 2, False, {"C": 2}, 4, 2, "double_icon")     # 大腸包小腸 Sausage-in-Sausage
    add("C", 2, False, {"C": 2, "S": 1}, 6, 3, "wild", True)  # ★ 逢甲名物 →S
    add("C", 2, True,  {"K": 1}, 2, 1, None)              # 冬瓜茶 Wintermelon Tea (drink)
    # --- South 南 (seafood · 1 slot · local K) ---
    add("S", 1, False, {"S": 1}, 2, 1, "icon")            # 虱目魚粥 Milkfish Congee
    add("S", 1, False, {"S": 1}, 1, 1, "icon")            # 碗粿 Rice Bowl Cake
    add("S", 1, True,  {"K": 1}, 2, 1, None)              # 木瓜牛奶 Papaya Milk (drink)
    add("S", 2, False, {"S": 2}, 4, 2, "double_icon")     # 蚵仔煎 Oyster Omelette
    add("S", 2, False, {"S": 2, "E": 1}, 5, 2, "wild")    # 棺材板 Coffin Bread →E
    add("S", 2, False, {"S": 3}, 7, 3, "rep_plus2", True) # ★ 擔仔麵 Tan-tsú-mī
    # --- East 東 (rice · 1 slot · no local K · Indigenous-forward) ---
    add("E", 1, False, {"E": 2}, 2, 1, "icon")            # 竹筒飯 Bamboo-Tube Rice
    add("E", 1, False, {"E": 1}, 2, 1, "icon")            # 米糕 Rice Cake
    add("E", 2, False, {"E": 2}, 4, 2, "double_icon")     # 麻糬 Mochi
    add("E", 2, False, {"E": 2, "N": 1}, 8, 3, "rep_plus2", True)  # ★ 部落風味 →N (apex, E highest)
    add("E", 2, True,  {"K": 1}, 2, 1, None)              # 洛神花茶 Roselle Tea (drink)
    return V


VENDORS = _build_vendors()


def _region_deck(region, phase):
    return [v["id"] for v in VENDORS if v["region"] == region and v["phase"] == phase]


# ==================================================================================================
#  TOUR TICKETS (v6.2 — 12 day + 12 night + 3 general; draw MISSION_DRAW per phase; face-up row of MROW)
# ==================================================================================================
# key -> (value, phase-tag "d"|"n"|"g"). Progress read from a won-vendor stat block below.
TICKETS = {
    # --- Daytime (the ramp / positioning phase) ---
    "d_breakfast3": (4, "d"), "d_travel3": (5, "d"), "d_south2": (4, "d"), "d_north2": (4, "d"),
    "d_drinks2": (3, "d"), "d_mix1": (3, "d"), "d_early3": (5, "d"), "d_cheap3": (4, "d"),
    "d_east1": (3, "d"), "d_prestige8": (4, "d"), "d_central2": (4, "d"), "d_contest1": (4, "d"),
    # --- Nighttime (the apex / contest phase) ---
    "n_nmfood2": (5, "n"), "n_star1": (5, "n"), "n_all4": (7, "n"), "n_surfturf": (4, "n"),
    "n_prestige14": (6, "n"), "n_four": (5, "n"), "n_expensive1": (4, "n"), "n_east2": (5, "n"),
    "n_contest2": (5, "n"), "n_final2": (5, "n"), "n_drinks3": (4, "n"), "n_allvenue": (6, "n"),
    # --- General (seeds both phases) ---
    "g_travel3": (5, "g"), "g_collect5": (5, "g"), "g_prestige12": (6, "g"),
}
DAY_TICKETS = [k for k, (_, ph) in TICKETS.items() if ph == "d"]
NIGHT_TICKETS = [k for k, (_, ph) in TICKETS.items() if ph == "n"]
GENERAL_TICKETS = [k for k, (_, ph) in TICKETS.items() if ph == "g"]


def _wstat(won):
    by = Counter(v["region"] for v in won)
    return {
        "n": len(won),
        "regions": set(by),
        "by": by,
        "day_food": sum(1 for v in won if v["phase"] == 1 and not v["is_drink"]),
        "night_food": sum(1 for v in won if v["phase"] == 2 and not v["is_drink"]),
        "food": sum(1 for v in won if not v["is_drink"]),
        "drinks": sum(1 for v in won if v["is_drink"]),
        "prestige": sum(v["prestige"] for v in won),
        "prestige_day": sum(v["prestige"] for v in won if v["act_won"] == 1),
        "contested": sum(1 for v in won if v["contested"]),
        "stars": sum(1 for v in won if v["starred"]),
        "cost_le2": sum(1 for v in won if v["total_cost"] <= 2),
        "cost_ge3": sum(1 for v in won if v["total_cost"] >= 3),
        "before_dusk": sum(1 for v in won if v["act_won"] == 1),
        "final_round": sum(1 for v in won if v["final_round"]),
    }


def _mprog(key, st):
    """(done, needed) — monotonic partial credit for the planner."""
    by = st["by"]
    if key == "d_breakfast3":  return min(st["day_food"], 3), 3
    if key == "d_travel3":     return min(len(st["regions"]), 3), 3
    if key == "d_south2":      return min(by["S"], 2), 2
    if key == "d_north2":      return min(by["N"], 2), 2
    if key == "d_drinks2":     return min(st["drinks"], 2), 2
    if key == "d_mix1":        return min(st["food"], 1) + min(st["drinks"], 1), 2
    if key == "d_early3":      return min(st["before_dusk"], 3), 3
    if key == "d_cheap3":      return min(st["cost_le2"], 3), 3
    if key == "d_east1":       return min(by["E"], 1), 1
    if key == "d_prestige8":   return min(st["prestige_day"], 8), 8
    if key == "d_central2":    return min(by["C"], 2), 2
    if key == "d_contest1":    return min(st["contested"], 1), 1
    if key == "n_nmfood2":     return min(st["night_food"], 2), 2
    if key == "n_star1":       return min(st["stars"], 1), 1
    if key == "n_all4":        return min(len(st["regions"]), 4), 4
    if key == "n_surfturf":    return min(by["S"], 1) + min(by["N"], 1), 2
    if key == "n_prestige14":  return min(st["prestige"], 14), 14
    if key == "n_four":        return min(st["n"], 4), 4
    if key == "n_expensive1":  return min(st["cost_ge3"], 1), 1
    if key == "n_east2":       return min(by["E"], 2), 2
    if key == "n_contest2":    return min(st["contested"], 2), 2
    if key == "n_final2":      return min(st["final_round"], 2), 2
    if key == "n_drinks3":     return min(st["drinks"], 3), 3
    if key == "n_allvenue":    return min(st["day_food"], 1) + min(st["night_food"], 1) + min(st["drinks"], 1), 3
    if key == "g_travel3":     return min(len(st["regions"]), 3), 3
    if key == "g_collect5":    return min(st["n"], 5), 5
    if key == "g_prestige12":  return min(st["prestige"], 12), 12
    return 0, 1


def _mdone(key, won):
    d, n = _mprog(key, _wstat(won))
    return d >= n


def _mhelps(key, cand, won):
    st = _wstat(won)
    b, n = _mprog(key, st)
    if b >= n:
        return False
    a, _ = _mprog(key, _wstat(won + [cand]))
    return a > b


def _ticket_value(key):
    return TICKETS[key][0]


def _ticket_final_score(pl):
    tot = 0
    for key in pl["tickets"]:
        v = TICKETS[key][0]
        if _mdone(key, pl["won"]):
            tot += v
        elif PENALTY == "half":
            tot -= (v // 2)
        # PENALTY == "zero": unfinished scores 0
    return tot


# --- ticket keep-fit (which ticket a bot wants to CLAIM off the face-up row) ---
# rough completability in a ~5-6-win game; harder ones (all-4, prestige, multi-region) lower.
TICKET_EASE = {
    "d_breakfast3": 0.7, "d_travel3": 0.5, "d_south2": 0.7, "d_north2": 0.8, "d_drinks2": 0.6,
    "d_mix1": 0.9, "d_early3": 0.5, "d_cheap3": 0.7, "d_east1": 0.7, "d_prestige8": 0.6,
    "d_central2": 0.7, "d_contest1": 0.45,
    "n_nmfood2": 0.7, "n_star1": 0.55, "n_all4": 0.3, "n_surfturf": 0.7, "n_prestige14": 0.5,
    "n_four": 0.65, "n_expensive1": 0.7, "n_east2": 0.55, "n_contest2": 0.4, "n_final2": 0.5,
    "n_drinks3": 0.55, "n_allvenue": 0.6,
    "g_travel3": 0.55, "g_collect5": 0.6, "g_prestige12": 0.55,
}


def _ticket_fit(prefs, key):
    """Can this bot realistically finish it, given its controls/leanings?"""
    needs_drink = key in ("d_drinks2", "n_drinks3", "d_mix1", "n_allvenue")
    hard_drink = key in ("d_drinks2", "n_drinks3")           # pure-drink counting tickets
    needs_food = key not in ("d_drinks2", "n_drinks3")
    if prefs.get("no_drinks") and hard_drink:
        return 0.05
    if prefs.get("pure_drinks") and needs_food and not needs_drink:
        return 0.1
    fit = 1.0
    if prefs.get("opportunistic") and key in ("n_star1", "n_prestige14", "g_prestige12", "d_prestige8", "n_expensive1"):
        fit *= 1.4
    if prefs.get("disrupt") and key in ("d_contest1", "n_contest2"):
        fit *= 1.6
    if prefs.get("speed") and key in ("d_early3", "n_final2", "d_breakfast3", "n_four"):
        fit *= 1.3
    return fit


def _ticket_keep_score(won, key, prefs):
    d, n = _mprog(key, _wstat(won))
    prog = (d / n) if n else 0.0
    return _ticket_value(key) * TICKET_EASE.get(key, 0.6) * _ticket_fit(prefs, key) + 2.0 * prog


# ==================================================================================================
#  SCORING helpers
# ==================================================================================================
def _rep_end_vp(rep):
    if rep >= 12: return 9
    if rep >= 9:  return 6
    if rep >= 6:  return 4
    if rep >= 3:  return 2
    return 0


CHARACTERS = ("neutral", "councillor", "office", "influencer", "dagushi", "dage")


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:
    # -------- setup --------
    def new_state(self, rng, n_players=2, characters=None, prefs=None):
        chars = list(characters) if characters else ["neutral"] * n_players
        prefs = list(prefs) if prefs else [dict(BAL) for _ in range(n_players)]
        # player-count scaling
        slots = {"N": 2, "C": 1, "S": 1, "E": 1}
        if n_players >= 3: slots["C"] = 2
        if n_players >= 4: slots["S"] = 2
        supply = int(round(BUZZ_SUPPLY * (1 + 0.375 * (n_players - 2))))
        mdraw = MISSION_DRAW + (1 if n_players == 3 else 2 if n_players >= 4 else 0)
        m_dusk = {2: M_DUSK, 3: M_DUSK + 1, 4: M_DUSK + 2}.get(n_players, M_DUSK)
        m_end  = {2: M_END,  3: M_END + 2,  4: M_END + 4}.get(n_players, M_END)
        v_dusk = {2: V_DUSK, 3: V_DUSK + 2, 4: V_DUSK + 4}.get(n_players, V_DUSK)
        v_end  = {2: V_END,  3: V_END + 4,  4: V_END + 8}.get(n_players, V_END)
        starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "C", "S", "E"]}.get(n_players, ["N", "S"])

        # region vendor decks (day now; night held) + face-up reveal
        vdeck, faceup, buzz_ids = {}, {}, set()
        for r in REGIONS:
            d = _region_deck(r, 1); rng.shuffle(d)
            up = [d.pop() for _ in range(min(slots[r], len(d)))]
            vdeck[r] = d; faceup[r] = up
            buzz_ids |= set(up)

        # per-region conserved ingredient pools (DAY) + empty discards
        ing_pool, ing_discard = {}, {}
        for r in REGIONS:
            pool = Counter({r: SIG_SUPPLY})
            if r in COMMON_REGIONS:
                pool[COMMON] += K_SUPPLY
            ing_pool[r] = pool
            ing_discard[r] = Counter()

        # tickets: draw MISSION_DRAW for the day phase from DAY + GENERAL; fill the face-up row
        day_pool = DAY_TICKETS + GENERAL_TICKETS
        drawn = rng.sample(day_pool, min(mdraw, len(day_pool)))
        mrow = drawn[:MROW]
        mreserve = drawn[MROW:]

        players = []
        for p in range(n_players):
            ch = chars[p]
            players.append({
                "char": ch, "prefs": prefs[p],
                "pos": starts[p % len(starts)],
                "larder": Counter(), "won": [], "icons": Counter(), "wild": 0,
                "prestige": 0, "rep": 0,
                "promote_bonus": (1 if ch == "influencer" else 0),
                "rep_per_court_bonus": 0, "councillor_regions": set(),
                "tickets": [], "counted_done": set(),
                "next_visit_extra_hazard": 0, "tempo_tax": 0,
            })
        if "influencer" in chars:
            infl = chars.index("influencer")
            for p in range(n_players):
                if p != infl:
                    players[p]["larder"][COMMON] += INFL_BEHIND

        return {
            "n": n_players, "slots": slots,
            "vdeck": vdeck, "faceup": faceup,
            "ing_pool": ing_pool, "ing_discard": ing_discard,
            "buzz": {vid: [0] * n_players for vid in buzz_ids},
            "star": set(), "supply": supply, "supply_min": supply,
            "act": 1,
            "clock_mode": CLOCK_MODE, "completions": 0, "vendor_claims": 0,
            "m_dusk": m_dusk, "m_end": m_end, "v_dusk": v_dusk, "v_end": v_end,
            "mrow": mrow, "mreserve": mreserve, "mdraw": mdraw,
            "players": players, "turn": 0, "cur": 0,
            "end_turn": None, "end_cause": None, "done": False,
            # diagnostics
            "food_wins": 0, "drink_wins": 0, "contested_wins": 0,
            "star_placed": 0, "star_wins": {p: 0 for p in range(n_players)},
            "max_buzz_on_vendor": 0,
            "claim_by_region": {r: 0 for r in REGIONS},
            "src_by_region": {r: 0 for r in REGIONS}, "src_common": 0,
            "travels": 0, "visits": 0, "cstores": 0, "promotes": 0, "inter_moves": 0,
            "dusk_turn": None, "last_turn": None, "first_night_win_turn": None,
            "legal_counts": [], "forced_turns": 0,
            "events_fired": 0, "scope_fired": {"self": 0, "region": 0, "neigh": 0},
            "cs_rival_hits": 0, "takethat_hits": 0, "pokes": 0,
            "claims": 0, "empty_draws": 0,
        }

    # -------- harness protocol --------
    def players(self, state):
        return list(range(state["n"]))

    def actors(self, state):
        return [state["cur"]]

    def view(self, state, player):
        return state

    def is_over(self, s):
        return s["done"]

    # -------- board helpers --------
    def _board(self, s):
        return [vid for r in REGIONS for vid in s["faceup"][r]]

    def _vendor_region(self, s, vid):
        return VENDORS[vid]["region"]

    def _present(self, s, p, vid):
        return s["players"][p]["pos"] == VENDORS[vid]["region"]

    # -------- cost / affordability --------
    def _pay_plan(self, s, p, vid):
        pl = s["players"][p]
        v = VENDORS[vid]
        pay = {}
        for r, c in v["cost"].items():
            if r == COMMON:
                pay[COMMON] = c                          # common carries no icon → never discounted
            else:
                pay[r] = max(0, c - pl["icons"].get(r, 0))
        w = pl["wild"]
        regs = [r for r in pay if r != COMMON]
        while w > 0 and any(pay[r] > 0 for r in regs):
            r = max(regs, key=lambda k: pay[k])
            if pay[r] <= 0:
                break
            pay[r] -= 1; w -= 1
        if pl["char"] == "councillor" and not v["is_drink"] \
                and v["region"] not in pl["councillor_regions"] and len(pl["councillor_regions"]) < 2:
            for r in sorted(pay, key=lambda k: -pay[k]):
                if pay[r] > 0:
                    pay[r] -= 1; break
        if pl["char"] == "dage" and DAGE_FLAW in ("tab", "nocontest"):
            tgt = COMMON if v["is_drink"] else v["region"]
            pay[tgt] = pay.get(tgt, 0) + 1
        return pay

    def _margin_for(self, pl):
        return DAGE_THRESH if pl["char"] == "dage" else BUZZ_MARGIN

    def _buzz_lead(self, s, p, vid):
        b = s["buzz"][vid]
        rival = max((b[q] for q in range(s["n"]) if q != p), default=0)
        return b[p] - rival, rival

    def _can_bribe(self, s, p, vid):
        if not self._present(s, p, vid):
            return False
        pl = s["players"][p]
        lead, rival = self._buzz_lead(s, p, vid)
        if lead < self._margin_for(pl):
            return False
        if pl["char"] == "dage" and DAGE_FLAW == "nocontest" and rival > 0:
            return False                                 # the "real brake": no contested wins at a tie
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
        if s["mrow"] and len(pl["tickets"]) < 4 and not pl["prefs"].get("no_tickets"):
            acts.append(("claim",))
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
        elif kind == "claim":
            self._do_claim(s, p)
        self._discard_to_cap(s, pl)
        if s["supply"] < s["supply_min"]:
            s["supply_min"] = s["supply"]

        s["turn"] += 1
        s["cur"] = s["turn"] % s["n"]
        if s["end_turn"] is None and s["turn"] >= STALL_CAP * s["n"]:
            self._trigger_end(s, "stall")
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            s["done"] = True
        if s["turn"] > 8000:
            s["done"] = True
        return s

    def _do_promote(self, s, p, vid):
        pl = s["players"][p]
        y = min(self._promote_yield(pl), s["supply"])
        s["supply"] -= y
        s["buzz"][vid][p] += y
        s["promotes"] += 1
        s["max_buzz_on_vendor"] = max(s["max_buzz_on_vendor"], max(s["buzz"][vid]))

    def _do_claim(self, s, p):
        pl = s["players"][p]
        if not s["mrow"]:
            return
        key = max(s["mrow"], key=lambda k: _ticket_keep_score(pl["won"], k, pl["prefs"]))
        s["mrow"].remove(key)
        pl["tickets"].append(key)
        s["claims"] += 1
        if s["mreserve"]:                                # refill the face-up row
            s["mrow"].append(s["mreserve"].pop(0))

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
        pl["won"].append({
            "id": vid, "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "prestige": prestige, "total_cost": v["total_cost"], "contested": contested,
            "starred": starred, "act_won": s["act"],
            "final_round": s["end_turn"] is not None,
        })
        if not v["is_drink"]:                            # food → discount icon + perk (drinks carry none)
            pl["icons"][v["region"]] += 1
            self._apply_perk(pl, v)
            if pl["char"] == "councillor" and v["region"] not in pl["councillor_regions"] \
                    and len(pl["councillor_regions"]) < 2:
                pl["councillor_regions"].add(v["region"])
        if starred:
            s["star"].discard(vid); s["star_wins"][p] += 1
        s["supply"] += sum(s["buzz"][vid]); s["buzz"][vid] = [0] * s["n"]
        s["claim_by_region"][v["region"]] += 1
        if v["is_drink"]:
            s["drink_wins"] += 1
        else:
            s["food_wins"] += 1
        if contested:
            s["contested_wins"] += 1
        if v["phase"] == 2 and s["first_night_win_turn"] is None:
            s["first_night_win_turn"] = s["turn"]
        self._remove_and_refill(s, v["region"], vid)
        self._on_claim_clock(s, p)

    def _apply_perk(self, pl, v):
        perk = v["perk"]
        if perk == "double_icon":
            pl["icons"][v["region"]] += 1
        elif perk == "wild":
            pl["wild"] += 1
        elif perk == "rep_plus2":
            pl["rep_per_court_bonus"] += 2

    def _remove_and_refill(self, s, region, vid):
        up = s["faceup"][region]
        if vid in up:
            up.remove(vid)
        deck = s["vdeck"][region]
        if deck:
            nv = deck.pop()
            up.append(nv)
            s["buzz"].setdefault(nv, [0] * s["n"])

    # -------- the clock (mission-driven or vendor-claims) --------
    def _on_claim_clock(self, s, p):
        # a vendor claim always counts the vendor-claim clock; and (re)checks mission completions
        s["vendor_claims"] += 1
        self._check_mission_completions(s, p)
        if s["clock_mode"] == "vendor":
            if s["act"] == 1 and s["vendor_claims"] >= s["v_dusk"]:
                self._dusk(s)
            if s["vendor_claims"] >= s["v_end"]:
                self._trigger_end(s, "lasttrain")
        # backstops (both modes): day decks island-wide empty → dusk; night decks empty → end
        if s["act"] == 1 and self._all_day_decks_dry(s) and s["end_turn"] is None:
            self._dusk(s)
        if s["act"] == 2 and self._all_night_decks_dry(s) and s["end_turn"] is None:
            self._trigger_end(s, "deck")

    def _check_mission_completions(self, s, p):
        pl = s["players"][p]
        for key in pl["tickets"]:
            if key in pl["counted_done"]:
                continue
            if _mdone(key, pl["won"]):
                pl["counted_done"].add(key)
                if s["clock_mode"] == "mission":
                    s["completions"] += 1
                    if s["act"] == 1 and s["completions"] >= s["m_dusk"]:
                        self._dusk(s)
                    if s["completions"] >= s["m_end"]:
                        self._trigger_end(s, "lasttrain")

    def _all_day_decks_dry(self, s):
        return all(not s["vdeck"][r] and not s["faceup"][r] for r in REGIONS)

    def _all_night_decks_dry(self, s):
        return all(not s["vdeck"][r] and not s["faceup"][r] for r in REGIONS)

    def _dusk(self, s):
        if s["act"] != 1:
            return
        s["act"] = 2
        s["dusk_turn"] = s["turn"]
        # sweep the day layer island-wide: unwon day vendors gone, day ingredient pools cleared
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                s["supply"] += sum(s["buzz"].get(vid, [0] * s["n"]))
                s["buzz"][vid] = [0] * s["n"]
                s["star"].discard(vid)
            # swap in the NIGHT vendor deck + reveal
            nd = _region_deck(r, 2); import_rng = None
            self._rng_shuffle(s, nd)
            up = [nd.pop() for _ in range(min(s["slots"][r], len(nd)))]
            s["vdeck"][r] = nd; s["faceup"][r] = up
            for vid in up:
                s["buzz"].setdefault(vid, [0] * s["n"])
            # swap in fresh NIGHT ingredient pools (day discards clear with the day layer)
            pool = Counter({r: SIG_SUPPLY})
            if r in COMMON_REGIONS:
                pool[COMMON] += K_SUPPLY
            s["ing_pool"][r] = pool
            s["ing_discard"][r] = Counter()
        # the ticket pool switches to NIGHT: discard the day supply, draw a fresh night row
        rng = s.get("_rng")
        night_pool = NIGHT_TICKETS + GENERAL_TICKETS
        if rng is not None:
            drawn = rng.sample(night_pool, min(s["mdraw"], len(night_pool)))
        else:
            drawn = night_pool[:s["mdraw"]]
        s["mrow"] = drawn[:MROW]
        s["mreserve"] = drawn[MROW:]
        # night sprint: shorten the night half (probe #7)
        if NIGHT_SPRINT > 0:
            if s["clock_mode"] == "mission":
                s["m_end"] = max(s["completions"] + 1, s["m_end"] - NIGHT_SPRINT)
            else:
                s["v_end"] = max(s["vendor_claims"] + 1, s["v_end"] - NIGHT_SPRINT)

    def _rng_shuffle(self, s, lst):
        # the harness rng is threaded via step(); dusk has no rng arg, so use a stashed one
        rng = s.get("_rng")
        if rng is not None:
            rng.shuffle(lst)

    def _trigger_end(self, s, cause):
        if s["end_turn"] is not None:
            return
        s["end_cause"] = cause
        s["last_turn"] = s["turn"]
        n = s["n"]
        done = s["turn"] + 1
        s["end_turn"] = ((done + n - 1) // n) * n + n    # finish this round + one more full round

    # -------- events (fire by scope, resolved relative to the drawn region) --------
    def _event_frac(self, s):
        return DAY_EVENT_FRAC if s["act"] == 1 else NIGHT_EVENT_FRAC

    def _draw_market(self, s, r, rng):
        """One market draw from region r: an event (regenerated) or a conserved token. Returns
        ("ev", ...) for an event, a token string ("N"/"C"/.../"K") for an ingredient, or None (dry)."""
        if rng.random() < self._event_frac(s):
            kind = "hazard" if rng.random() < EVENT_HAZARD_FRAC else "boon"
            return _make_event(kind, rng)
        pool = s["ing_pool"][r]
        if sum(pool.values()) == 0:                      # deck dry → reshuffle the discard back in
            pool += s["ing_discard"][r]; s["ing_discard"][r] = Counter()
        if sum(pool.values()) == 0:
            s["empty_draws"] += 1
            return None                                  # genuinely nothing here (temporary denial)
        toks = list(pool.elements())
        tok = rng.choice(toks)
        pool[tok] -= 1; pool = +pool; s["ing_pool"][r] = pool
        return tok

    def _return_token(self, s, tok):
        """A KEPT token is returned to circulation only via the over-cap discard (renewable). An UNKEPT
        card from a Visit flip goes back to its region pool immediately (you didn't take it)."""
        home = tok if tok != COMMON else "C"             # common recycles to a common region
        s["ing_pool"][home][tok] += 1
        s["ing_pool"][home] = +s["ing_pool"][home]

    def _event_targets(self, s, actor, drawn_region, scope):
        if scope == "self":
            return [actor]
        if scope == "region":
            return [q for q in range(s["n"]) if s["players"][q]["pos"] == drawn_region]
        nbrs = region_neighbours(drawn_region)
        return [q for q in range(s["n"]) if s["players"][q]["pos"] in nbrs]

    def _fire_event(self, s, actor, drawn_region, ev, rng, during_visit, origin):
        _, kind, scope, sub = ev
        s["events_fired"] += 1
        s["scope_fired"][scope] += 1
        targets = self._event_targets(s, actor, drawn_region, scope)
        penalty = 0
        if kind == "boon" and sub == "star":
            self._place_star(s)
            return 0
        for t in targets:
            if kind == "hazard":
                if during_visit and t == actor:
                    penalty += 1
                else:
                    s["players"][t]["tempo_tax"] += 1
                if t != actor:
                    s["takethat_hits"] += 1
                    if origin == "cstore":
                        s["cs_rival_hits"] += 1
            else:                                        # boon ingredient windfall (the region's signature)
                tok = drawn_region if drawn_region in REGIONS else COMMON
                s["players"][t]["larder"][tok] += 1
                s["src_by_region"][drawn_region] += 1
        return penalty

    def _apply_tempo_tax(self, pl, natural_keep):
        if pl["tempo_tax"] > 0 and natural_keep > 0:
            pl["tempo_tax"] -= 1
            return natural_keep - 1
        return natural_keep

    def _place_star(self, s):
        cand = [vid for r in REGIONS for vid in s["faceup"][r] if vid not in s["star"]]
        if not cand:
            return
        tgt = min(cand, key=lambda vid: VENDORS[vid]["prestige"])
        s["star"].add(tgt); s["star_placed"] += 1

    # -------- sourcing --------
    def _keep_cap(self, pl):
        if pl["char"] == "dagushi":
            return 3
        if pl["char"] == "office":
            return 2 if OFFICE_BUFF == "keep2" else 1
        return 2

    def _do_visit(self, s, p, rng):
        pl = s["players"][p]
        r = pl["pos"]
        s["visits"] += 1
        cards = [self._draw_market(s, r, rng) for _ in range(3)]
        toks = [c for c in cards if isinstance(c, str)]
        events = [c for c in cards if isinstance(c, tuple)]
        actor_haz = 0
        for ev in events:
            actor_haz += self._fire_event(s, p, r, ev, rng, during_visit=True, origin="visit")
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
        keep = max(0, self._apply_tempo_tax(pl, keep))
        kept = toks[:keep]
        for c in kept:
            pl["larder"][c] += 1
            if c == COMMON:
                s["src_common"] += 1
            else:
                s["src_by_region"][c] += 1
        for c in toks[keep:]:                            # unkept flips return to the region pool
            self._return_token(s, c)

    def _do_cstore(self, s, p, r, rng):
        pl = s["players"][p]
        s["cstores"] += 1
        c = self._draw_market(s, r, rng)
        if isinstance(c, str):
            got = self._apply_tempo_tax(pl, 1)
            if got > 0:
                pl["larder"][c] += 1
                if c == COMMON:
                    s["src_common"] += 1
                else:
                    s["src_by_region"][c] += 1
            else:
                self._return_token(s, c)
        elif isinstance(c, tuple):
            self._fire_event(s, p, r, c, rng, during_visit=False, origin="cstore")

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        s["inter_moves"] += 1
        draw_region = src if pl["char"] == "office" else dest
        n_draw = 2 if (pl["char"] == "office" and OFFICE_BUFF == "travel2") else 1
        for _ in range(n_draw):
            c = self._draw_market(s, draw_region, rng)
            if isinstance(c, str):                       # an event on a Travel fly-by whiffs (no fire)
                got = self._apply_tempo_tax(pl, 1)
                if got > 0:
                    pl["larder"][c] += 1
                    if c == COMMON:
                        s["src_common"] += 1
                    else:
                        s["src_by_region"][draw_region] += 1
                else:
                    self._return_token(s, c)

    def _discard_to_cap(self, s, pl):
        total = sum(pl["larder"].values())
        if total <= LARDER_CAP:
            return
        for _ in range(total - LARDER_CAP):
            tok = max((k for k in pl["larder"] if pl["larder"][k] > 0),
                      key=lambda k: pl["larder"][k])
            pl["larder"][tok] -= 1
            # renewable: the excess returns to that ingredient's region market discard
            home = tok if tok != COMMON else "C"
            s["ing_discard"][home][tok] += 1
        pl["larder"] = +pl["larder"]

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
        total_wins = s["food_wins"] + s["drink_wins"]
        src = s["src_by_region"]; src_tot = sum(src.values()) + s["src_common"]
        claim = s["claim_by_region"]; claim_tot = sum(claim.values()) or 1
        ev = s["events_fired"] or 1

        def csh(r): return claim[r] / claim_tot
        def ssh(x): return (x / src_tot) if src_tot else 0.0
        return {
            "margin": float(margin), "tie": tie,
            "turns": float(s["turn"]), "turns_per_player": float(s["turn"] / s["n"]),
            "food_wins": float(s["food_wins"]), "drink_wins": float(s["drink_wins"]),
            "wins_per_player": float(total_wins / s["n"]),
            "drink_win_share": float(s["drink_wins"] / total_wins) if total_wins else 0.0,
            "contested_wins": float(s["contested_wins"]),
            "contested_frac": float(s["contested_wins"] / total_wins) if total_wins else 0.0,
            "max_buzz_on_vendor": float(s["max_buzz_on_vendor"]),
            "buzz_supply_min": float(s["supply_min"]),
            "star_placed": float(s["star_placed"]),
            "star_wins_total": float(sum(s["star_wins"].values())),
            "dusk_turn": float(s["dusk_turn"]) if s["dusk_turn"] is not None else float(s["turn"]),
            "last_turn": float(s["last_turn"]) if s["last_turn"] is not None else float(s["turn"]),
            "first_night_win_turn": float(s["first_night_win_turn"]) if s["first_night_win_turn"] is not None else float(s["turn"]),
            "end_by_lasttrain": 1.0 if s["end_cause"] == "lasttrain" else 0.0,
            "end_by_deck": 1.0 if s["end_cause"] == "deck" else 0.0,
            "end_by_stall": 1.0 if s["end_cause"] == "stall" else 0.0,
            "travels_per_game": float(s["travels"]), "inter_moves": float(s["inter_moves"]),
            "visits_per_game": float(s["visits"]), "cstores_per_game": float(s["cstores"]),
            "claim_share_N": csh("N"), "claim_share_C": csh("C"),
            "claim_share_S": csh("S"), "claim_share_E": csh("E"),
            "src_share_N": ssh(src["N"]), "src_share_C": ssh(src["C"]),
            "src_share_S": ssh(src["S"]), "src_share_E": ssh(src["E"]),
            "src_share_common": float(s["src_common"] / src_tot) if src_tot else 0.0,
            "avg_legal_actions": float(statistics.mean(s["legal_counts"])) if s["legal_counts"] else 0.0,
            "forced_turn_frac": float(s["forced_turns"] / len(s["legal_counts"])) if s["legal_counts"] else 0.0,
            "events_fired_per_game": float(s["events_fired"]),
            "scope_self_frac": float(s["scope_fired"]["self"] / ev),
            "scope_region_frac": float(s["scope_fired"]["region"] / ev),
            "scope_neigh_frac": float(s["scope_fired"]["neigh"] / ev),
            "takethat_hits_per_game": float(s["takethat_hits"]),
            "cs_rival_hits_per_game": float(s["cs_rival_hits"]),
            "pokes_per_game": float(s["pokes"]),
            "empty_draws_per_game": float(s["empty_draws"]),
            "claims_per_game": float(s["claims"]),
            "completions_per_game": float(s["completions"]),
            "tickets_held_winner": float(len(wp["tickets"])),
            "tickets_done_winner": float(sum(1 for k in wp["tickets"] if _mdone(k, wp["won"]))),
            "ticket_net_winner": float(_ticket_final_score(wp)),
            "win_prestige": float(wp["prestige"]),
            "win_rep_vp": float(_rep_end_vp(wp["rep"])),
            "win_ticket_score": float(_ticket_final_score(wp)),
            "win_total": float(best),
        }


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan (v6.2 — region vendor markets + a mission clock)"


# ==================================================================================================
#  SHARED ENGINE BRAIN — one greedy planner; strategies differ ONLY in PREFS.
# ==================================================================================================
TEMPO = 1.1


def _needs(s, p, vid):
    pay = GAME._pay_plan(s, p, vid)
    pl = s["players"][p]
    need = Counter()
    for r, c in pay.items():
        short = c - pl["larder"].get(r, 0)
        if short > 0:
            need[r] = short
    return need


def _buzz_short_real(s, p, vid, pl):
    _, rival = GAME._buzz_lead(s, p, vid)
    margin = GAME._margin_for(pl)
    raw = max(0, rival + margin - s["buzz"][vid][p])
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


def _tickets_marginal(s, p, vid):
    pl = s["players"][p]
    v = VENDORS[vid]
    cand = {"id": v["id"], "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "prestige": v["prestige"], "total_cost": v["total_cost"],
            "contested": False, "starred": vid in s["star"], "act_won": s["act"],
            "final_round": s["end_turn"] is not None}
    total = 0.0
    for key in pl["tickets"]:
        if _mdone(key, pl["won"]):
            continue
        if _mhelps(key, cand, pl["won"]):
            after = _mdone(key, pl["won"] + [cand])
            val = _ticket_value(key)
            total += (val * 0.85) if after else (val * 0.22)
    return total * pl["prefs"].get("w_ticket", 1.0)


def _road_value(s, p, vid, prefs):
    pl = s["players"][p]
    v = VENDORS[vid]
    prestige = v["prestige"] + (STAR_BONUS_P if vid in s["star"] else 0)
    core = prestige + _rep_marginal(pl, v)
    if not v["is_drink"]:
        core += _ramp_value(pl, v, prefs.get("w_ramp", 1.0))
        core *= prefs.get("w_food", 1.0)
    else:
        core *= prefs.get("w_drink", 1.0)
    if prefs.get("opportunistic") and (vid in s["star"] or v["prestige"] >= 6):
        core *= 1.3
    return core * prefs.get("w_val", 1.0) + _tickets_marginal(s, p, vid)


def _est_actions(s, p, vid):
    pl = s["players"][p]
    need = _needs(s, p, vid)
    ing = sum(need.values())
    bz = _buzz_short_real(s, p, vid, pl)
    py = GAME._promote_yield(pl)
    reg = VENDORS[vid]["region"]
    travel = 1 if pl["pos"] != reg else 0
    return 0.7 * ing + (bz / py) + travel + 1.0


def _pick_target(s, p, prefs):
    board = GAME._board(s)
    best, bscore = None, -1e9
    for vid in board:
        v = VENDORS[vid]
        if prefs.get("pure_drinks") and not v["is_drink"]:
            continue
        if prefs.get("no_drinks") and v["is_drink"]:
            continue
        val = _road_value(s, p, vid, prefs)
        score = val - TEMPO * (_est_actions(s, p, vid) - 1.0)
        # mild stickiness: a small nudge to finish a vendor you've already committed Buzz to (cuts the
        # worst target-thrash) — kept light so it doesn't cause fixation on an unwinnable vendor.
        if s["buzz"][vid][p] > 0:
            score += 0.4
        if score > bscore:
            bscore, best = score, vid
    return best


def _token_source(s, p, tok, legal, prefs):
    """Best action to source token `tok`. Signatures: Visit/CS the region that holds it. Common: a
    common region."""
    pl = s["players"][p]
    if tok == COMMON:
        targets = list(COMMON_REGIONS)
    else:
        targets = [tok]
    if pl["pos"] in targets and ("visit",) in legal:
        return ("visit",)
    for r in targets:
        if ("cstore", r) in legal and (tok == COMMON or True):
            # prefer to travel to a signature region and Visit (3× throughput) if it's a signature we
            # need a lot of; but a single CS grab is fine for a top-up
            pass
    # relocate to a token region to Visit it (better yield than remote CS)
    dest = min(targets, key=lambda r: _dist(pl["pos"], r, pl["char"]))
    if pl["pos"] == dest and ("visit",) in legal:
        return ("visit",)
    hop = _next_hop(pl["pos"], dest, pl["char"])
    if ("travel", hop) in legal:
        return ("travel", hop)
    for r in targets:
        if ("cstore", r) in legal:
            return ("cstore", r)
    return None


def _poke(s, p, legal):
    rival_regions = {s["players"][q]["pos"] for q in range(s["n"]) if q != p}
    for r in rival_regions:
        if ("cstore", r) in legal:
            return ("cstore", r)
    return None


def _should_claim(s, p, legal, prefs):
    if ("claim",) not in legal or prefs.get("no_tickets"):
        return False
    pl = s["players"][p]
    incomplete = [k for k in pl["tickets"] if not _mdone(k, pl["won"])]
    limit = 3 if prefs.get("speed") else 2
    # don't claim so late that a fresh ticket can't be finished
    if s["clock_mode"] == "mission":
        room = s["completions"] < s["m_end"] - 1
    else:
        room = s["vendor_claims"] < s["v_end"] - 1
    return len(incomplete) < limit and room


def _plan(s, p, legal, rng, prefs):
    pl = s["players"][p]
    # 1) a bribe that fits the road always progresses
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs.get("pure_drinks") and not VENDORS[a[1]]["is_drink"])
              and not (prefs.get("no_drinks") and VENDORS[a[1]]["is_drink"])]
    if bribes:
        return max(bribes, key=lambda a: _road_value(s, p, a[1], prefs))

    # 2) hoarder overlay: over-source and SIT on a target region's signature to deny
    hr = prefs.get("hoard_region")
    if hr and sum(pl["larder"].values()) < LARDER_CAP:
        act = _token_source(s, p, hr, legal, prefs)
        if act is not None:
            return act

    # 3) claim a fresh ticket when it's pure upside
    if _should_claim(s, p, legal, prefs):
        return ("claim",)

    tgt = _pick_target(s, p, prefs)
    if tgt is None:
        pk = _poke(s, p, legal) if prefs.get("disrupt") else None
        if pk is not None:
            s["pokes"] += 1
            return pk
        return ("visit",) if ("visit",) in legal else legal[0]

    v = VENDORS[tgt]
    eff = v["region"]
    need = _needs(s, p, tgt)
    lead, _rival = GAME._buzz_lead(s, p, tgt)
    margin = GAME._margin_for(pl)
    present = GAME._present(s, p, tgt)

    # 4) get on-site if we're short the local ingredient, else route toward the target
    if not present:
        pos = pl["pos"]
        if need.get(pos, 0) > 0 and ("visit",) in legal:
            return ("visit",)
        if need.get(COMMON, 0) > 0 and pos in COMMON_REGIONS and ("cstore", pos) in legal:
            return ("cstore", pos)
        hop = _next_hop(pos, eff, pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    # 5) source what the target needs
    if sum(need.values()) > 0:
        for tok in list(need):
            act = _token_source(s, p, tok, legal, prefs)
            if act is not None:
                return act
        if ("visit",) in legal:
            return ("visit",)

    # 6) win the Buzz fight
    if lead < margin and present and ("promote", tgt) in legal:
        return ("promote", tgt)
    if lead < margin and not present:
        hop = _next_hop(pl["pos"], eff, pl["char"])
        if ("travel", hop) in legal:
            return ("travel", hop)

    # 7) disruptive fallback / idle
    if prefs.get("disrupt"):
        pk = _poke(s, p, legal)
        if pk is not None:
            s["pokes"] += 1
            return pk
    if ("visit",) in legal:
        return ("visit",)
    return legal[0]


def _make(prefs):
    def agent(s, p, legal, rng):
        return _plan(s, p, legal, rng, prefs)
    return agent


# --- PREFS per playstyle -------------------------------------------------------------------------
BAL = {"w_val": 1.0, "w_food": 1.0, "w_drink": 1.0, "w_ramp": 1.0, "w_ticket": 1.0}
OPPORTUNISTIC = {**BAL, "opportunistic": True, "w_ticket": 1.15}
DISRUPTIVE = {**BAL, "disrupt": True, "w_ticket": 1.1}
ENDGAME = {**BAL, "speed": True, "w_ticket": 1.2}
CHARLEAN = {**BAL}                                        # kit-driven; used with a character assigned
MIXPREFS = {**BAL, "w_drink": 1.1, "w_ticket": 1.15}      # the well-timed mix
IGNORE_OBJ = {**BAL, "no_tickets": True, "no_drinks": True}  # ignore objectives AND drinks (the control)
PURE_DRINKS = {"w_val": 1.0, "w_food": 0.0, "w_drink": 1.0, "w_ramp": 0.0, "pure_drinks": True, "w_ticket": 1.0}
NO_DRINKS = {**BAL, "no_drinks": True}


def s_random(s, p, legal, rng):
    return rng.choice(legal)


def s_greedy_prestige(s, p, legal, rng):
    bribes = [a for a in legal if a[0] == "bribe"]
    if bribes:
        return max(bribes, key=lambda a: VENDORS[a[1]]["prestige"])
    return _plan(s, p, legal, rng, BAL)


STRATEGIES = {
    "random":        s_random,
    "greedy_prest":  s_greedy_prestige,
    "balanced":      _make(BAL),
    "opportunistic": _make(OPPORTUNISTIC),
    "disruptive":    _make(DISRUPTIVE),
    "endgame":       _make(ENDGAME),
    "mix":           _make(MIXPREFS),
    "ignore_obj":    _make(IGNORE_OBJ),
    "pure_drinks":   _make(PURE_DRINKS),
    "no_drinks":     _make(NO_DRINKS),
}

STRAT_PREFS = {
    "random": BAL, "greedy_prest": BAL, "balanced": BAL, "opportunistic": OPPORTUNISTIC,
    "disruptive": DISRUPTIVE, "endgame": ENDGAME, "mix": MIXPREFS, "ignore_obj": IGNORE_OBJ,
    "pure_drinks": PURE_DRINKS, "no_drinks": NO_DRINKS,
}


# ==================================================================================================
#  A rng-threaded wrapper so dusk() can shuffle the night decks deterministically.
# ==================================================================================================
class _Seeded:
    """Wrap GAME so new_state stashes the match rng into state (dusk needs to shuffle without an rng
    arg). Also lets the probe runners pass n_players / characters / prefs."""
    def __init__(self, n=2, characters=None, prefs=None):
        self.n, self.characters, self.prefs = n, characters, prefs

    def new_state(self, rng):
        st = GAME.new_state(rng, self.n, characters=self.characters, prefs=self.prefs)
        st["_rng"] = rng
        return st

    def __getattr__(self, k):
        return getattr(GAME, k)


# ==================================================================================================
#  __main__ — the v6.2 probe suite (uses the harness directly, like beacon.py)
# ==================================================================================================
def _run(agents, n=1500, seed=1, n_players=2, characters=None, prefs=None):
    from engine import run_match
    g = _Seeded(n_players, characters, prefs)
    w = [0] * n_players; t = 0; sums = [0.0] * n_players
    accum = {}
    for i in range(n):
        sc, mt = run_match(g, {p: agents[p] for p in range(n_players)}, seed + i)
        for p in range(n_players):
            sums[p] += sc[p]
        best = max(sc.values()); winners = [p for p, v in sc.items() if v == best]
        if len(winners) > 1:
            t += 1
        else:
            w[winners[0]] += 1
        for k, v in mt.items():
            accum.setdefault(k, []).append(v)
    metrics = {k: statistics.mean(v) for k, v in accum.items()}
    return [x / n for x in w], t / n, [x / n for x in sums], metrics


def _versus(sa, sb, n=1500, seed=1):
    """A's win rate vs B, both seatings averaged, with each side's prefs/capability wired in (the
    caps-AWARE probe — authoritative over the caps-blind round-robin)."""
    pa, pb = STRAT_PREFS[sa], STRAT_PREFS[sb]
    w0, t0, _, _ = _run({0: STRATEGIES[sa], 1: STRATEGIES[sb]}, n=n, seed=seed, prefs=[pa, pb])
    w1, t1, _, _ = _run({0: STRATEGIES[sb], 1: STRATEGIES[sa]}, n=n, seed=seed + n, prefs=[pb, pa])
    a_as0 = w0[0] + 0.5 * t0
    a_as1 = w1[1] + 0.5 * t1
    return (a_as0 + a_as1) / 2


def _char_winrate(ch, n=1200, seed=1, prefs=None):
    pr = prefs or BAL
    w0, t0, _, _ = _run({0: STRATEGIES["balanced"], 1: STRATEGIES["balanced"]},
                        n=n, seed=seed, characters=[ch, "neutral"], prefs=[pr, BAL])
    w1, t1, _, _ = _run({0: STRATEGIES["balanced"], 1: STRATEGIES["balanced"]},
                        n=n, seed=seed + n, characters=["neutral", ch], prefs=[BAL, pr])
    return ((w0[0] + 0.5 * t0) + (w1[1] + 0.5 * t1)) / 2


def _field_metrics(n=1500, seed=1):
    """Balanced-mirror game arc + spread metrics (both seatings folded via mirror)."""
    _, _, _, mt = _run({0: STRATEGIES["balanced"], 1: STRATEGIES["balanced"]},
                       n=n, seed=seed, prefs=[BAL, BAL])
    return mt


if __name__ == "__main__":
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _SIM = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "tools", "sim"))
    if _SIM not in sys.path:
        sys.path.insert(0, _SIM)

    if "--counts" in sys.argv:
        from engine import per_count
        counts = [2, 3, 4]
        print(f"# {TITLE} — seat balance by player count (self-play: balanced)\n")
        for c in counts:
            g = _Seeded(c)
            from engine import seat_balance
            r = seat_balance(g, STRATEGIES["balanced"], c, n=800)
            flag = "⚠ suspect" if r["suspect"] else "✓ balanced"
            wr = "  ".join(f"seat{p}={v*100:.0f}%" for p, v in r["seat_win_rate"].items())
            print(f"  {c}p  {flag}  (fair {r['fair_share']*100:.0f}%)  {wr}  ties={r['tie_rate']*100:.0f}%")
        sys.exit(0)

    N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1200
    print(f"# {TITLE} — v6.2 probe suite ({N} games/cell)\n")

    print("## Game arc (balanced mirror)")
    mt = _field_metrics(n=N)
    print(f"  turns/player {mt['turns_per_player']:.1f}  vendors/player {mt['wins_per_player']:.1f}  "
          f"winner VP {mt['win_total']:.1f} (P {mt['win_prestige']:.1f}/Rep {mt['win_rep_vp']:.1f}/Tkt {mt['win_ticket_score']:.1f})")
    print(f"  dusk turn {mt['dusk_turn']:.1f}  last-train {mt['last_turn']:.1f}  "
          f"end: lasttrain {mt['end_by_lasttrain']*100:.0f}% deck {mt['end_by_deck']*100:.0f}% stall {mt['end_by_stall']*100:.0f}%")
    print(f"  contested-win frac {mt['contested_frac']*100:.1f}%  max_buzz {mt['max_buzz_on_vendor']:.1f}  "
          f"drink-win share {mt['drink_win_share']*100:.0f}%  claims/gm {mt['claims_per_game']:.1f} completions/gm {mt['completions_per_game']:.1f}")
    print(f"  CLAIM share  N {mt['claim_share_N']*100:.0f}% C {mt['claim_share_C']*100:.0f}% "
          f"S {mt['claim_share_S']*100:.0f}% E {mt['claim_share_E']*100:.0f}%")
    print(f"  SRC   share  N {mt['src_share_N']*100:.0f}% C {mt['src_share_C']*100:.0f}% "
          f"S {mt['src_share_S']*100:.0f}% E {mt['src_share_E']*100:.0f}% K {mt['src_share_common']*100:.0f}%")
    print(f"  moves/gm {mt['inter_moves']:.1f}  forced_turn_frac {mt['forced_turn_frac']:.3f}  "
          f"avg_legal {mt['avg_legal_actions']:.1f}  empty_draws/gm {mt['empty_draws_per_game']:.2f}")

    print("\n## PROBE 1 — the five playstyles vs each other + naive (win% vs the field)")
    field = ["balanced", "opportunistic", "disruptive", "endgame", "mix", "no_drinks"]
    for a in field:
        wr = statistics.mean([_versus(a, b, n=N // 2) for b in field if b != a])
        crush = _versus(a, "random", n=N // 2)
        print(f"  {a:14} avg vs field {wr*100:5.1f}%   vs random {crush*100:4.0f}%")

    print("\n## PROBE 2 — mix vs the ignore-objectives/ignore-drinks control; pure-drinks must lose")
    print(f"  mix        vs ignore_obj   {_versus('mix', 'ignore_obj', n=N)*100:5.1f}%  (want >=50: a mix beats ignoring objectives+drinks)")
    print(f"  balanced   vs ignore_obj   {_versus('balanced', 'ignore_obj', n=N)*100:5.1f}%")
    print(f"  pure_drinks vs balanced    {_versus('pure_drinks', 'balanced', n=N)*100:5.1f}%  (want clearly <50)")
    print(f"  pure_drinks vs no_drinks   {_versus('pure_drinks', 'no_drinks', n=N)*100:5.1f}%")

    print("\n## PROBE 8 — character balance (char vs neutral, both seatings) — target 45-55%")
    for ch in ("councillor", "office", "influencer", "dagushi", "dage"):
        wr = _char_winrate(ch, n=N)
        flag = "OK" if 0.45 <= wr <= 0.55 else "<-- OUT"
        print(f"  {ch:12} {wr*100:5.1f}%  {flag}")

    print("\n## H2 — 大哥 threshold+flaw (dage vs neutral) — resolve to 45-55%")
    for label, thr, flaw in (("A tie+tab", 0, "tab"), ("B tie+promote1", 0, "promote1"),
                             ("C lead1+tab", 1, "tab"), ("D lead1+none", 1, "none"),
                             ("E tie+nocontest", 0, "nocontest")):
        globals()["DAGE_THRESH"] = thr; globals()["DAGE_FLAW"] = flaw
        print(f"  {label:18} dage {_char_winrate('dage', n=N)*100:5.1f}%")
    globals()["DAGE_THRESH"] = 0; globals()["DAGE_FLAW"] = "tab"

    print("\n## H1 — 大胃王 flaw (should all be ~in band; ship A)")
    for label, mode in (("A hazards-twice", "twice"), ("B keep-only-2", "keep2"), ("C next-fires", "next")):
        globals()["H1"] = mode
        print(f"  {label:16} dagushi {_char_winrate('dagushi', n=N)*100:5.1f}%")
    globals()["H1"] = "twice"

    print("\n## 媽寶 buff options")
    for label, mode in (("none (keep-1)", "none"), ("keep2", "keep2"), ("travel2", "travel2")):
        globals()["OFFICE_BUFF"] = mode
        print(f"  {label:16} office {_char_winrate('office', n=N)*100:5.1f}%")
    globals()["OFFICE_BUFF"] = "keep2"

    print("\n## PROBE 5 — CLOCK A/B (mission vs vendor-claims): pacing")
    for mode in ("mission", "vendor"):
        globals()["CLOCK_MODE"] = mode
        mt = _field_metrics(n=N)
        print(f"  {mode:8}  turns/player {mt['turns_per_player']:.1f}  vendors/player {mt['wins_per_player']:.1f}  "
              f"dusk {mt['dusk_turn']:.1f} last {mt['last_turn']:.1f}  end(LT/deck/stall) "
              f"{mt['end_by_lasttrain']*100:.0f}/{mt['end_by_deck']*100:.0f}/{mt['end_by_stall']*100:.0f}%")
    globals()["CLOCK_MODE"] = "mission"

    print("\n## PROBE 6 — the −½ penalty A/B (does behaviour differ?)")
    for mode in ("half", "zero"):
        globals()["PENALTY"] = mode
        wr = _versus("mix", "ignore_obj", n=N)
        mt = _field_metrics(n=N)
        print(f"  penalty={mode:5}  mix vs ignore_obj {wr*100:5.1f}%  claims/gm {mt['claims_per_game']:.1f}  "
              f"tkt_done_winner {mt['tickets_done_winner']:.1f}/{mt['tickets_held_winner']:.1f}  winnerVP {mt['win_total']:.1f}")
    globals()["PENALTY"] = "half"

    print("\n## PROBE 10 — HOARDER (over-source a scarce signature to deny) — should LOSE")
    for hr in ("E", "S"):
        globals()["STRAT_PREFS"]  # no-op to keep linter calm
        hoard = {**BAL, "hoard_region": hr}
        # register a temp hoarder strategy
        STRATEGIES["_hoard"] = _make(hoard); STRAT_PREFS["_hoard"] = hoard
        wr = _versus("_hoard", "balanced", n=N)
        print(f"  hoard {hr}  vs balanced  {wr*100:5.1f}%   (want <50 = a trap, not a lockout)")
    del STRATEGIES["_hoard"]; del STRAT_PREFS["_hoard"]

    print("\n## PROBE 11 — MP light seat-balance smoke (per count)")
    from engine import seat_balance
    for c in (2, 3, 4):
        g = _Seeded(c)
        r = seat_balance(g, STRATEGIES["balanced"], c, n=600)
        flag = "⚠ suspect" if r["suspect"] else "✓ balanced"
        wr = "  ".join(f"seat{p}={v*100:.0f}%" for p, v in r["seat_win_rate"].items())
        print(f"  {c}p  {flag}  (fair {r['fair_share']*100:.0f}%)  {wr}  ties={r['tie_rate']*100:.0f}%")
