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
  * SOURCING is STRUCTURALLY UNTOUCHED (ingredients come from region MARKET decks, not vendors) — the
    §6b sourcing-by-type shares must read INVARIANT vs the old closed values (probe #2 anchor). The pool
    model, event fractions, Visit keep-2/3, Convenience Store, and per-count market depth are ported
    verbatim so the shares hold.

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

# --- sourcing model (PORTED VERBATIM from the old sim so the §6b shares stay INVARIANT) -----------
SIG_SUPPLY = int(os.environ.get("TA_SIG_SUPPLY", "10"))       # per-region-phase signature pool (2p base)
K_SUPPLY   = int(os.environ.get("TA_K_SUPPLY", "6"))          # 糖 Sugar common pool in C & S
VEG_SUPPLY = int(os.environ.get("TA_VEG_SUPPLY", "3"))        # 菜 Veg common pool in N & E
DAY_EVENT_FRAC   = float(os.environ.get("TA_DAY_EVENT", "0.25"))
NIGHT_EVENT_FRAC = float(os.environ.get("TA_NIGHT_EVENT", "0.42"))
EVENT_HAZARD_FRAC = float(os.environ.get("TA_HAZARD", "0.55"))
STALL_CAP  = int(os.environ.get("TA_STALL_CAP", "60"))       # safety net (deck-clock is guaranteed to fire)

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
                "icon": row["icon"].strip() or None,
                "trending": row.get("trending", "").strip() == "yes",
                "apex": tier >= 3,
                "cross": len(sig_regions) >= 2,   # a cross-region (→X) dish spans >1 signature region
            })
    return out


VENDORS = _load_vendors()
VID_BY_KEY = {v["vid"]: v["id"] for v in VENDORS}


def _region_deck(region, phase):
    return [v["id"] for v in VENDORS if v["region"] == region and v["phase"] == phase]


# --------------------------------------------------------------------------------------------------
#  BOOKINGS — load bookings.csv and parse each `target` string into a monotonic (done, needed) fn.
# --------------------------------------------------------------------------------------------------
def _wstat(won):
    """A stat block over the vendors a player has WON (the pattern a Booking target reads)."""
    by = Counter(v["region"] for v in won)
    return {
        "n": len(won),
        "regions": set(by), "by": by,
        "max_region": max(by.values()) if by else 0,
        "food": sum(1 for v in won if not v["is_drink"]),
        "drinks": sum(1 for v in won if v["is_drink"]),
        "day_food": sum(1 for v in won if v["phase"] == 1 and not v["is_drink"]),
        "night_food": sum(1 for v in won if v["phase"] == 2 and not v["is_drink"]),
        "early": sum(1 for v in won if v["act_won"] == 1),                 # won before dusk
        "cheap": sum(1 for v in won if v["total_cost"] <= 2),
        "expensive": sum(1 for v in won if v["total_cost"] >= 3),
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
            out[key] = {
                "value": int(row["value"]),
                "phase": 1 if row["phase"].strip() == "day" else 2,
                "target": row["target"].strip(),
                "progress": _parse_target(row["target"].strip()),
                "is_general": key.startswith("g_"),
                "is_prestige": "value" in row.get("tags", "") and "prestige" in key,
            }
            order.append(key)
    return out, order


BOOKINGS, BOOKING_ORDER = _load_bookings()
PRESTIGE_KEYS = {"d_prestige8", "n_prestige14", "g_prestige12"}
# DAY / NIGHT booking pools (the deck-clock draws from these). A general (g_) booking rides the phase
# its CSV row is tagged with (g_travel3d = day; g_*n / g_collect5 / g_prestige12 / g_cross1 = night).
DAY_POOL = [k for k, b in BOOKINGS.items() if b["phase"] == 1]
NIGHT_POOL = [k for k, b in BOOKINGS.items() if b["phase"] == 2]


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
    tab = MAP["vendor_slots"].get(str(n)) or MAP["vendor_slots"].get(str(min(max(n, 3), 6)))
    return {r: tab[r] for r in ("N", "C", "S", "E")}


def _booking_deck_sizes(n):
    t = MAP["booking_deck_sizes"].get(str(n)) or MAP["booking_deck_sizes"].get(str(min(max(n, 3), 6)))
    return t["day"], t["night"]


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
        # per-count market depth (ported): more agents sourcing shouldn't starve the market
        ing_factor = 1.0 + 0.4 * (n - 2)
        sig = int(round(SIG_SUPPLY * ing_factor))
        ksup = int(round(K_SUPPLY * ing_factor))
        vsup = int(round(VEG_SUPPLY * ing_factor))
        mrow_w = 3 if n < 4 else 4

        # deal the day face-up vendor slots + build region decks
        vdeck, faceup = {}, {}
        for r in REGIONS:
            d = _region_deck(r, 1); rng.shuffle(d)
            up = [d.pop() for _ in range(min(slots[r], len(d)))]
            vdeck[r] = d; faceup[r] = up

        ing_pool, ing_discard = {}, {}
        for r in REGIONS:
            pool = Counter({SIG_TYPE[r]: sig})
            if r in COMMONS["sugar"]:
                pool["sugar"] += ksup
            if r in COMMONS["veg"]:
                pool["veg"] += vsup
            ing_pool[r] = pool
            ing_discard[r] = Counter()

        # the DAY booking deck IS the clock (deck-driven)
        day_deck = self._build_booking_deck(DAY_POOL, day_size, rng)
        mrow = [day_deck.pop() for _ in range(min(mrow_w, len(day_deck)))]

        players = []
        for p in range(n):
            ch = chars[p]
            mx = _char_max(ch)
            home = self._pick_home(faceup, ch)
            players.append({
                "char": ch, "pos": "N",                       # common Taipei start hub (map.start_hub)
                "max": mx, "board": START_MEEPLES, "supply_f": mx - START_MEEPLES,
                "larder": Counter(), "icons": Counter(), "won": [],
                "home_region": home,
                "tickets": [], "counted_done": set(),
                "day_book_score": 0, "night_book_score": 0, "cancel_penalty": 0,
                "next_bribe_disc": 0, "tempo_tax": 0,
                "ms1_done": False, "ms2_done": False,
                # per-lane fingerprint accumulators
                "fp_contest_entries": 0, "fp_wins": 0, "fp_fol_per_win": 0,
                "fp_src_visit": 0, "fp_src_travel": 0, "fp_src_cstore": 0, "fp_src_draw": 0,
                "fp_first_tier23_turn": None,
                "fp_free_draws": 0,
                "win_streak": 0, "best_win_streak": 0,
            })

        return {
            "_rng": rng, "n": n, "slots": slots,
            "vdeck": vdeck, "faceup": faceup,
            "ing_pool": ing_pool, "ing_discard": ing_discard,
            "sig": sig, "ksup": ksup, "vsup": vsup,
            "fol": {vid: [0] * n for r in REGIONS for vid in faceup[r]},   # committed followers per stall
            "commit_turn": {},                                             # (vid,p) -> first-commit turn
            "star": set(),                                                  # Trending markers on stalls
            "mrow": mrow, "mreserve": day_deck, "mrow_w": mrow_w,
            "day_size": day_size, "night_size": night_size,
            "players": players, "act": 1, "turn": 0, "cur": 0, "round": 0,
            "end_turn": None, "end_cause": None, "done": False, "_finalized": False,
            "dusk_turn": None, "last_turn": None, "first_night_win_turn": None,
            # ---- diagnostics / §9 probes ----
            "claims": 0, "contested_claims": 0, "claim_by_region": {r: 0 for r in REGIONS},
            "night_claims": 0, "prestige_completions": 0, "cancels": 0,
            "food_wins": 0, "drink_wins": 0,
            "src_by_type": Counter(), "empty_draws": 0,
            "travels": 0, "visits": 0, "cstores": 0, "promotes": 0, "passes": 0,
            "grow_total": 0, "grow_homebody_tick": 0, "return_to_supply": 0,
            "legal_counts": [], "forced_turns": 0,
            "tie_blocks": 0, "resolver_fires": 0, "frozen_at_boundary": 0,
            "max_committed_on_stall": 0, "max_committed_by_player": 0,
            "dage_edge_fires": 0, "dage_claims": 0,
            "ama_claims": 0, "ama_snipes": 0, "ama_travel_cost_paid": 0,
            "events_fired": 0, "trending_grows": 0,
            "commit_hist": [],   # (turn, vid, p) for fingerprints / earliest committer
        }

    def _build_booking_deck(self, pool, size, rng):
        deck = []
        while len(deck) < size:
            chunk = list(pool); rng.shuffle(chunk); deck.extend(chunk)
        deck = deck[:size]; rng.shuffle(deck)
        return deck

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
        return True   # V7-M sim: the Scheduled-Maintenance HSR outage is not modelled here (event-light)

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
        # need at least 1 of your own on the stall
        if mine + need_more < 1:
            need_more = 1 - mine
        return need_more

    def _can_claim_margin(self, s, p, vid):
        return self._needed_to_win(s, p, vid) == 0 and s["fol"][vid][p] >= 1

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
        return all(pl["larder"].get(t, 0) >= c for t, c in self._pay_plan(s, p, vid).items())

    def _can_bribe(self, s, p, vid):
        return self._present(s, p, vid) and self._can_claim_margin(s, p, vid) and self._can_afford(s, p, vid)

    def _promote_ok(self, s, p, vid):
        return s["players"][p]["board"] > 0 and self._present(s, p, vid)

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
        legal = self.legal_actions(s, p)
        s["legal_counts"].append(len(legal))
        if len(legal) <= 1:
            s["forced_turns"] += 1

        # 里長伯 HOME-GATED FAVOURS DRAW: while in home region, start of turn draw 1 ingredient (no action)
        if pl["char"] == "councillor" and pl["pos"] == pl["home_region"]:
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
        else:
            s["passes"] += 1
        self._discard_to_cap(s, pl)
        self._track_committed(s, p)

        s["turn"] += 1
        # END OF ROUND (every player has taken one turn) → SLOW REFILL of empty face-up slots
        if s["turn"] % s["n"] == 0:
            s["round"] += 1
            if SLOW_REFILL:
                self._refill_round(s)
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
        n_place = min(2, pl["board"])
        if n_place <= 0:
            return
        s["promotes"] += 1
        first = 1 if (spread_vid is not None and n_place >= 2) else n_place
        self._place(s, p, vid, first)
        if spread_vid is not None and n_place >= 2:
            self._place(s, p, spread_vid, 1)

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
        # pay ingredients
        for t, c in self._pay_plan(s, p, vid).items():
            pl["larder"][t] -= c
        pl["larder"] = +pl["larder"]
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
            "contested": contested, "act_won": s["act"], "final_round": s["end_turn"] is not None,
        })
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
        """End-of-round SLOW REFILL: top every region back up to its face-up count from its deck."""
        for r in REGIONS:
            while len(s["faceup"][r]) < s["slots"][r] and s["vdeck"][r]:
                nv = s["vdeck"][r].pop()
                if APEX_NOREFILL and VENDORS[nv]["apex"]:
                    continue   # reserve d: apex stalls, once gone, do not come back (drop, try next)
                s["faceup"][r].append(nv)
                s["fol"].setdefault(nv, [0] * s["n"])

    # -------- councillor home-gated draw --------
    def _councillor_draw(self, s, p):
        """Old Favours (home-gated): draw 1 ingredient card from ANY region's market into hand, no action.
        Bot heuristic: draw the ingredient TYPE it is most short of for a face-up food stall it can reach."""
        pl = s["players"][p]
        if sum(pl["larder"].values()) >= self._larder_cap(pl):
            return
        need = Counter()
        for vid in self._board(s):
            v = VENDORS[vid]
            if v["is_drink"]:
                continue
            for t, c in self._pay_plan(s, p, vid).items():
                short = c - pl["larder"].get(t, 0)
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
            pl["cancel_penalty"] += BOOKINGS[victim]["value"] // 2
            s["cancels"] += 1
        key = max(s["mrow"], key=lambda k: self._booking_want(s, p, k))
        s["mrow"].remove(key)
        pl["tickets"].append(key)
        if s["mreserve"]:
            s["mrow"].append(s["mreserve"].pop())
        else:
            self._booking_deck_out(s)   # the deck ran out → the boundary card → phase transition

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
                short = c - pl["larder"].get(t, 0)
                if short > 0:
                    need[t] += short
        return need.most_common(1)[0][0] if need else SIG_TYPE[pl["pos"]]

    # -------- the deck clock --------
    def _booking_deck_out(self, s):
        if s["act"] == 1:
            self._dusk(s)
        elif s["end_turn"] is None:
            self._trigger_end(s, "lasttrain")

    def _dusk(self, s):
        if s["act"] != 1:
            return
        s["act"] = 2
        s["dusk_turn"] = s["turn"]
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
                    pl["day_book_score"] += _judge_booking(key, pl["won"])
                else:
                    keep.append(key)
            pl["tickets"] = keep
        # sweep the day layer: uncommitted followers on cleared UNCLAIMED day stalls → owners' BOARDS
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                for q in range(s["n"]):
                    if s["fol"].get(vid, [0] * s["n"])[q] > 0:
                        s["players"][q]["board"] += s["fol"][vid][q]
                s["fol"][vid] = [0] * s["n"]
                s["star"].discard(vid)
            nd = _region_deck(r, 2); rng.shuffle(nd)
            up = [nd.pop() for _ in range(min(s["slots"][r], len(nd)))]
            s["vdeck"][r] = nd; s["faceup"][r] = up
            for vid in up:
                s["fol"].setdefault(vid, [0] * s["n"])
            pool = Counter({SIG_TYPE[r]: s["sig"]})
            if r in COMMONS["sugar"]:
                pool["sugar"] += s["ksup"]
            if r in COMMONS["veg"]:
                pool["veg"] += s["vsup"]
            s["ing_pool"][r] = pool; s["ing_discard"][r] = Counter()
        s["commit_turn"] = {}
        # deal the NIGHT booking deck (its exhaustion = LAST TRAIN)
        nd = self._build_booking_deck(NIGHT_POOL, s["night_size"], rng)
        s["mrow"] = [nd.pop() for _ in range(min(s["mrow_w"], len(nd)))]
        s["mreserve"] = nd

    def _resolve_all_ties(self, s, boundary, rng):
        """§2.6 baseline resolver: every still-tied contested stall force-resolves to most-followers →
        earliest committer; that agent claims (paying if able), losers → own supply. If the winner cannot
        pay, the frozen stall just clears (followers home) so nothing stays barricaded."""
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                fol = s["fol"].get(vid, [0] * s["n"])
                committers = [q for q in range(s["n"]) if fol[q] > 0]
                if len(committers) < 2:
                    continue
                s["frozen_at_boundary"] += 1
                # is it actually tied (no one has a plain claiming plurality)? if someone could already
                # claim they'd have done so; treat all multi-committer boundary stalls via the resolver.
                top = max(fol)
                top_players = [q for q in committers if fol[q] == top]
                winner = min(top_players, key=lambda q: s["commit_turn"].get((vid, q), 10 ** 9))
                s["resolver_fires"] += 1
                if self._can_afford(s, winner, vid):
                    for t, c in self._pay_plan(s, winner, vid).items():
                        s["players"][winner]["larder"][t] -= c
                    s["players"][winner]["larder"] = +s["players"][winner]["larder"]
                    self._award(s, winner, vid, contested=True, rng=rng)
                else:
                    # cannot pay → clear the frozen stall; followers go home (board at dusk / stay at end)
                    for q in committers:
                        if boundary == "dusk":
                            s["players"][q]["board"] += fol[q]
                        else:
                            s["players"][q]["supply_f"] += fol[q]
                    s["fol"][vid] = [0] * s["n"]

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
            night = sum(_judge_booking(key, pl["won"]) for key in pl["tickets"]
                        if BOOKINGS[key]["phase"] == 2)
            pl["night_book_score"] = night

    # -------- sourcing (PORTED so §6b shares stay invariant) --------
    def _larder_cap(self, pl):
        return AMA_LARDER_CAP if pl["char"] == "globetrotter" else LARDER_CAP

    def _event_frac(self, s):
        return DAY_EVENT_FRAC if s["act"] == 1 else NIGHT_EVENT_FRAC

    def _draw_market(self, s, r, rng):
        """Draw one card from region r's market: an EVENT (by fraction) or an ingredient TOKEN (a type)."""
        if rng.random() < self._event_frac(s):
            kind = "hazard" if rng.random() < EVENT_HAZARD_FRAC else "boon"
            return ("ev", kind)
        pool = s["ing_pool"][r]
        if sum(pool.values()) == 0:
            pool += s["ing_discard"][r]; s["ing_discard"][r] = Counter()
        if sum(pool.values()) == 0:
            s["empty_draws"] += 1
            return None
        toks = list(pool.elements())
        tok = rng.choice(toks)
        pool[tok] -= 1; s["ing_pool"][r] = +pool
        return tok

    def _return_token(self, s, tok):
        home = COMMON_HOME[tok] if _is_common(tok) else TYPE_SIG_REGION[tok]
        s["ing_pool"][home][tok] += 1
        s["ing_pool"][home] = +s["ing_pool"][home]

    def _fire_event(self, s, p, ev, during_visit):
        """Event payloads (abstracted, wired to the MEEPLE economy): a boon grows 1 follower or a free
        ingredient / Trending marker; a hazard returns 1 follower to supply or a tempo tax on keeps."""
        _, kind = ev
        s["events_fired"] += 1
        rng = s["_rng"]
        if kind == "boon":
            roll = rng.random()
            if roll < 0.34:
                self._grow(s, p, "event")               # "+1 follower" event (supply → board)
            elif roll < 0.56:
                self._place_star(s)                      # Trending marker onto a stall
            else:
                tok = SIG_TYPE[s["players"][p]["pos"]]   # ingredient windfall (the region signature)
                s["players"][p]["larder"][tok] += 1; s["src_by_type"][tok] += 1
            return 0
        # hazard
        if rng.random() < 0.40:
            self._return_one_to_supply(s, p)             # bad-review — return 1 follower to your supply
            return 0
        if during_visit:
            return 1                                     # a tempo tax on this Visit's keep
        s["players"][p]["tempo_tax"] += 1
        return 0

    def _place_star(self, s):
        cand = [vid for r in REGIONS for vid in s["faceup"][r] if vid not in s["star"]]
        if cand:
            s["star"].add(min(cand, key=lambda vid: VENDORS[vid]["total_cost"]))

    def _apply_tempo(self, pl, keep):
        if pl["tempo_tax"] > 0 and keep > 0:
            pl["tempo_tax"] -= 1
            return keep - 1
        return keep

    def _keep_cap(self, pl):
        return 3 if pl["char"] == "bigeater" else 2

    def _do_visit(self, s, p, rng):
        pl = s["players"][p]
        r = pl["pos"]
        s["visits"] += 1; pl["fp_src_visit"] += 1
        cards = [self._draw_market(s, r, rng) for _ in range(3)]
        toks = [c for c in cards if isinstance(c, str)]
        events = [c for c in cards if isinstance(c, tuple)]
        haz = 0
        for ev in events:
            haz += self._fire_event(s, p, ev, during_visit=True)
        if pl["char"] == "bigeater":
            haz *= 2                                     # 大胃王 flaw: hazards fire TWICE on his Visit
        keep = max(0, self._keep_cap(pl) - haz)
        keep = max(0, self._apply_tempo(pl, keep))
        # 大胃王 greedy 4th: keep one extra, then RETURN 1 follower to your supply (the greed sink)
        if pl["char"] == "bigeater" and len(toks) > keep and self._hungry(s, p):
            keep += 1
            for _ in range(BIGEATER_COST):
                self._return_one_to_supply(s, p)
        for c in toks[:keep]:
            pl["larder"][c] += 1; s["src_by_type"][c] += 1
        for c in toks[keep:]:
            self._return_token(s, c)

    def _hungry(self, s, p):
        pl = s["players"][p]
        for vid in self._board(s):
            if VENDORS[vid]["is_drink"]:
                continue
            if not self._can_afford(s, p, vid):
                return True
        return False

    def _do_cstore(self, s, p, r, rng):
        pl = s["players"][p]
        s["cstores"] += 1; pl["fp_src_cstore"] += 1
        c = self._draw_market(s, r, rng)
        if isinstance(c, str):
            if self._apply_tempo(pl, 1) > 0:
                pl["larder"][c] += 1; s["src_by_type"][c] += 1
            else:
                self._return_token(s, c)
        elif isinstance(c, tuple):
            self._fire_event(s, p, c, during_visit=False)

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        # grow your following (Travel +1: supply → board). Homebody grow-tick switchable (reserve g′).
        self._grow(s, p, "travel")
        # 阿嬤 Travel-anywhere COSTS 1 follower to supply (baseline ON: "the trip tires her crowd")
        if pl["char"] == "globetrotter" and AMA_TRAVEL_COST:
            if pl["board"] > 0:
                pl["board"] -= 1; pl["supply_f"] += 1; s["ama_travel_cost_paid"] += 1
        # 媽寶 is the SOLE Travel-sourcer: draw HOMEBODY_DRAW (2) cards of the region she LEFT, keep all
        if pl["char"] == "homebody":
            pl["fp_src_travel"] += 1
            for _ in range(HOMEBODY_DRAW):
                c = self._draw_market(s, src, rng)
                if isinstance(c, str):
                    if self._apply_tempo(pl, 1) > 0:
                        pl["larder"][c] += 1; s["src_by_type"][c] += 1
                    else:
                        self._return_token(s, c)
                # an event on a Travel fly-by whiffs (not fired)

    def _discard_to_cap(self, s, pl):
        cap = self._larder_cap(pl)
        total = sum(pl["larder"].values())
        if total <= cap:
            return
        for _ in range(total - cap):
            tok = max((k for k in pl["larder"] if pl["larder"][k] > 0), key=lambda k: pl["larder"][k])
            pl["larder"][tok] -= 1
            self._return_token(s, tok)
        pl["larder"] = +pl["larder"]

    # -------- scoring --------
    def scores(self, s):
        if not s["_finalized"]:
            self._finalize(s)
        out = {}
        for p in range(s["n"]):
            pl = s["players"][p]
            base = pl["day_book_score"] + pl["night_book_score"] - pl["cancel_penalty"]
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

        return {
            "margin": float(margin),
            "tie": 1.0 if len(winners) > 1 else 0.0,
            "turns": float(s["turn"]), "turns_per_player": float(s["turn"] / n),
            "dusk_turn": float(s["dusk_turn"]) if s["dusk_turn"] is not None else float(s["turn"]),
            "last_turn": float(s["last_turn"]) if s["last_turn"] is not None else float(s["turn"]),
            "end_by_lasttrain": 1.0 if s["end_cause"] == "lasttrain" else 0.0,
            "end_by_stall": 1.0 if s["end_cause"] == "stall" else 0.0,
            "first_night_win_turn": float(s["first_night_win_turn"]) if s["first_night_win_turn"] else float(s["turn"]),
            # ---- MAKE-OR-BREAK PROBE #1: does the battle happen more? (numerator + denominator) ----
            "claims_per_game": float(s["claims"]),
            "contested_claims_per_game": float(s["contested_claims"]),
            "contested_frac": float(s["contested_claims"] / claims),
            "night_claims_per_player": float(s["night_claims"] / n),
            "prestige_completions_per_game": float(s["prestige_completions"]),
            # ---- MAKE-OR-BREAK PROBE #2: sourcing/throughput health ----
            "src_share_meat_N": share("meat"), "src_share_tea_C": share("tea"),
            "src_share_seafood_S": share("seafood"), "src_share_pantry_E": share("pantry"),
            "src_share_sugar": share("sugar"), "src_share_veg": share("veg"),
            "empty_draws_per_game": float(s["empty_draws"]),
            "bookings_completed_field": float(held_or_done),
            "cancels_per_game": float(s["cancels"]),
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
            # ---- live-decision density ----
            "avg_legal_actions": float(statistics.mean(s["legal_counts"])) if s["legal_counts"] else 0.0,
            "forced_turn_frac": float(s["forced_turns"] / len(s["legal_counts"])) if s["legal_counts"] else 0.0,
            # ---- per-lane probes ----
            "dage_edge_fire_rate": float(s["dage_edge_fires"] / s["dage_claims"]) if s["dage_claims"] else 0.0,
            "dage_edge_fires_per_game": float(s["dage_edge_fires"]),
            "ama_snipe_rate": float(s["ama_snipes"] / s["ama_claims"]) if s["ama_claims"] else 0.0,
            "ama_travel_cost_paid_per_game": float(s["ama_travel_cost_paid"]),
            "councillor_free_draws_per_game": float(sum(pl["fp_free_draws"] for pl in s["players"])),
            # ---- claim geography ----
            "claim_share_N": s["claim_by_region"]["N"] / claims,
            "claim_share_C": s["claim_by_region"]["C"] / claims,
            "claim_share_S": s["claim_by_region"]["S"] / claims,
            "claim_share_E": s["claim_by_region"]["E"] / claims,
        }


GAME = TravelAgentsGame()
TITLE = ("Travel Agents: Taiwan — V7-M (Follower MEEPLES + VENDOR SCARCITY · six lanes · "
         "plurality [tie blocks] · 大哥 margin dial N · slow per-round refill · deck-driven clock)")


# ==================================================================================================
#  SHARED PLANNER — one greedy brain; strategies differ in PREFS. SPREAD- & MARGIN-AWARE.
# ==================================================================================================
TEMPO = 1.1


def _needs(s, p, vid):
    pay = GAME._pay_plan(s, p, vid)
    pl = s["players"][p]
    return Counter({t: c - pl["larder"].get(t, 0) for t, c in pay.items() if c - pl["larder"].get(t, 0) > 0})


def _booking_marginal(s, p, vid, prefs):
    pl = s["players"][p]
    v = VENDORS[vid]
    cand = {"id": v["id"], "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "total_cost": v["total_cost"], "tier": v["tier"], "apex": v["apex"], "cross": v["cross"],
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
        if score > bscore:
            bscore, best = score, vid
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


def _plan(s, p, legal, rng, prefs):
    pl = s["players"][p]
    if legal == [("pass",)]:
        return ("pass",)

    # 1) a Bribe that helps always progresses
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs.get("no_drinks") and VENDORS[a[1]]["is_drink"])]
    if bribes:
        return max(bribes, key=lambda a: _road_value(s, p, a[1], prefs))

    # 2) maintain a working hand of objectives (drawing Bookings drives the deck-clock). Under the
    #    hand-limit: claim. AT the hand-limit: CANCEL-TO-CLAIM only for a CLEARLY hotter Booking (the
    #    row offers something >1.3× the worst STALE held one) — a bounded valve that unsticks a hand of
    #    uncompletable Bookings (else the night deck never drains → the game runs to the stall) WITHOUT
    #    churning a good hand or crowding out vendor-winning.
    #    Bots maintain a working hand of WORK_HAND objectives (< HAND_LIMIT) so most turns go to
    #    vendor-work, not claiming; the deck-clock still drains because COMPLETING a Booking (a vendor
    #    win) frees its slot → a fresh claim. A bounded cancel-valve unsticks a fully-stale hand.
    WORK_HAND = HAND_LIMIT if prefs.get("collect") else 2
    if ("claim",) in legal and not prefs.get("no_tickets"):
        inprog = GAME._in_progress(pl)
        if len(inprog) < WORK_HAND:
            return ("claim",)
        stale = [k for k in inprog if GAME._prog_frac(pl, k) < 0.34]
        if len(inprog) >= WORK_HAND and stale:
            best_row = max(GAME._booking_want(s, p, k) for k in s["mrow"])
            worst_held = min(GAME._booking_want(s, p, k) for k in stale)
            if best_row > worst_held * 1.3:
                return ("claim",)

    tgt = _pick_target(s, p, prefs)
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
CONTESTER = {**BAL, "contest": True}
AVOIDER = {**BAL, "avoid_contest": True, "w_food": 1.2}
MARQUEE = {**BAL, "marquee": True, "w_val": 1.2}
# §9 probe lines
HOMEBODY_DODGE = {**BAL, "avoid_contest": True, "no_tickets": False, "w_food": 1.3}      # (i) ignore-the-contest
HOMEBODY_LATE = {**BAL, "late_battle": True, "w_food": 1.2}                              # (i) banked-board late-battler
NO_TICKETS = {**BAL, "no_tickets": True}                                                # objectives-blind control


def s_random(s, p, legal, rng):
    return rng.choice(legal)


STRATEGIES = {
    "balanced": _make(BAL),
    "contester": _make(CONTESTER),
    "avoider": _make(AVOIDER),
    "marquee": _make(MARQUEE),
    "homebody_dodge": _make(HOMEBODY_DODGE),
    "homebody_late": _make(HOMEBODY_LATE),
    "no_tickets": _make(NO_TICKETS),
    "random": s_random,
}


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
        if pl["char"] == "councillor" and pl["pos"] == pl["home_region"]:
            self._councillor_draw(s, p)   # home-gated draw fires at the start of the turn, before the action
        self._do_promote(s, p, a[1], spread_vid=a[2])
        self._discard_to_cap(s, pl)
        self._track_committed(s, p)
        s["turn"] += 1
        if s["turn"] % s["n"] == 0:
            s["round"] += 1
            if SLOW_REFILL:
                self._refill_round(s)
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
        print(f"# {TITLE}")
        print(f"# V7-M SMOKE TEST — {N} games/count, balanced mirror (import + end-to-end + sane instruments)\n")
        for c in (3, 4, 5, 6):
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
                  f"frozen@boundary/gm {mt['frozen_at_boundary_per_game']:.2f}  runaway best_win_streak {mt['best_win_streak']:.1f}")
            print(f"  decision density: avg_legal {mt['avg_legal_actions']:.1f}  forced_turn_frac {mt['forced_turn_frac']:.3f}\n")

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
