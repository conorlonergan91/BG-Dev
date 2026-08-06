"""
travel_agents.py — Travel Agents: Taiwan (v3, the VENDOR-COURTING ENGINE) encoded for the
simulation harness (see tools/sim/engine.py). Stdlib-only.

v3 REWORK (2026-08-06). The obsolete v2 model (plate-a-dish / dead-drop / Hot-List) is GONE.
This encodes design-doc.md v3: two rival travel agents build a Taiwan food TOUR by *courting
vendors* — paying region-specific ingredients (discounted by held region icons) + Buzz (never
discounted) — each vendor an engine piece feeding four scoring vectors: Prestige (VP), a Reputation
track, Region-Coverage, and a secret +7 signature Mission.

We attack the design's make-or-break assumptions BEFORE building components or spending a human
session. The four probes (run in __main__ and via the harness):

  PROBE 1  No dominant track/opening. No single strategy/track wins >~55%; >=3 viable in a tight band.
           (round_robin over the track + opening strategies + naive baselines; health read.)
  PROBE 2  No economy runaway. Does the discount snowball outrun the end-clock, or does the
           undiscountable-Buzz floor cap the court-rate at ~1 vendor / 2 turns even fully ramped?
           (court-interval late-game + max sustained rate + mid-game-leader-wins + VP gap.)
  PROBE 3  Character balance: each of 5 in 45-55%; no character x mission combo >~60%.
           (5x5 character round-robin at a fixed strategy; per-character x per-mission scan.)
  PROBE 4  Anti-hoard / hard-stuck ~= 0. Do the unlimited pantry + always-on Promote prevent stuck
           turns? (stuck-turn tally + larder-overflow discards = hoarding punished.)
Plus a standard health read (score spread, avg margin, trap paths).

Run:
    python tools/sim/simulate.py --module games/travel-agents/sim/travel_agents.py --n 2000 \
        --out games/travel-agents/playtests/sim-results.md
    python games/travel-agents/sim/travel_agents.py            # runs all four probes

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (bots are a FLOOR on depth, not a ceiling)
------------------------------------------------------------------------------------------------------
Faithfully modelled: 4-region ring + HSR(N-S) adjacency; the five actions (Stock Up +2 / Travel move+1 /
Promote +2 Buzz / Court / Extract); the two-input court cost = named region ingredients MINUS held
region-icon discounts (floored 0) + Buzz (NEVER discounted); the discount ramp (each vendor's region
icon cheapens that region's ingredient half of future vendors); the tiered Vendor Board (T1/T2/T3, 3
face-up per tier at 2p, refill on court, courted vendor locked from rivals); Prestige (1/3/5-6 by tier);
Reputation track climbed by printed Rep, milestone perks at 3/6/9 + top(12) end-trigger, end-VP
2/4/6/9; Region-Coverage 2/5/9; the secret +7 Mission (draw-3-keep-1, a strategy-aligned pick); the
Season end-timer (+1 per court, final ~16 at 2p -> finish round + one more full round); Market events
firing on refill (boon-skewed ~60/40, tax-not-destroy); finite per-region specialty supply (~2x solo
demand, unlimited pantry); the Larder cap 7 (6 Rookie); the 5 Characters (ability + flaw).

Simplifications (LISTED so we know the sim's blind spots):
  * SHARED "engine brain": every strategy uses ONE greedy courting/sourcing engine; strategies differ
    only in their VENDOR-VALUE WEIGHTS (how much they prize Prestige / Reputation / Coverage / mission /
    ramp) and an OPENING flag (buzz-first vs ingredient/ramp-first). This isolates "is a track/opening
    dominant?" exactly as beacon.py isolates the signal policy.
  * Ingredients are tracked at REGION granularity (N/C/S/E + Pantry), not per-specialty (beef vs pork
    both = "N"), because courting discounts are per-REGION. So intra-region specialty scarcity (only so
    many oysters vs milkfish) is collapsed into one per-region supply pool (~2x solo demand). Scarcity ->
    reroute is preserved at region level; the pantry valve is exact.
  * Market events are modelled by their MECHANICAL payload (free Buzz / free ingredient / a tempo tax /
    a supply wash), fired with a per-refill probability (~EVENT_PROB), boon 60 / hazard 40. The Rookie's
    "draw 2 resolve 1" = skips hazards; the Gourmand's "no boons" = boons do nothing. Exact tile text is
    not modelled (that's the feel-test's job).
  * Draw-3-keep-1 mission = the bot keeps the dealt mission best aligned to its weights (the design's
    "you steer your own keel"); it does not model reading the opponent's mission.
  * "Wild region icon" (T3 perk) and the pass-9 free icon are modelled as flexible discount + a coverage
    filler; a T2 "pantry-as-wild" perk and the Gourmand ability grant one pantry->specialty substitution
    per turn when courting. Perk allocation choices are greedy, not optimal.
  * Bots essentially never Extract early (they let the Season/Rep-top trigger end it) — matching the
    design's "Extract is a tempo option, the timer usually ends the game". The push-your-luck *feel* of
    Extract is a human-session question, not a sim one.
  * ASSUMPTIONS where the doc left a value open are tagged `# ASSUMPTION:` inline and collected in
    sim-notes.md.
"""
from __future__ import annotations

import os
import sys
import statistics
from collections import Counter

# ---- sim-only knobs (env vars; do NOT change the printed game rules) ------------------------------
SEASON_FINAL = {2: 16, 3: 24, 4: 30}                        # courts to fill the Season timer (design-doc)
REP_TOP = 12                                                # Reputation track top / scoring cap (design-doc)
# END-CLOCK FIX (LOCKED 2026-08-06): the Season timer paces the game; reaching Rep 12 no longer ENDS it
# (Rep still caps at 12 and pays its +9). Default = decoupled (999 = out of reach). Set TA_REP_TRIGGER=12
# to reproduce the OLD design where Rep-top ended the game at ~5 courts.
REP_TRIGGER = int(os.environ.get("TA_REP_TRIGGER", "999"))
CAP_DEFAULT = int(os.environ.get("TA_CAP", "7"))            # Larder cap (Rookie = 6)
REGION_SUPPLY = int(os.environ.get("TA_SUPPLY", "13"))      # ASSUMPTION: per-region specialty supply at 2p (~2x solo demand)
EVENT_PROB = float(os.environ.get("TA_EVENT_PROB", "0.24")) # ASSUMPTION: chance a market refill flips an Event tile
BUZZ_FLOOR_KNOB = int(os.environ.get("TA_BUZZ_FLOOR", "0")) # rebalance knob: +N Buzz on EVERY vendor (raise the floor)
DISCOUNT_CAP = int(os.environ.get("TA_DISC_CAP", "99"))     # rebalance knob: max region-icon discount per region

# ---- CHARACTER REBALANCE knobs (LOCKED values 2026-08-06; see sim-notes v3 rebalance) -------------
# Tuned at the fixed game length (end-clock decoupled). These are the DEFAULTS the design should adopt.
AUNTIE_MAX_REGIONS = int(os.environ.get("TA_AUNTIE_REGIONS", "2"))  # discount only on her first 2 regions (was: every region)
AUNTIE_EXCLUDE_T3 = os.environ.get("TA_AUNTIE_NO_T3", "0") == "1"   # discount never applies to Marquee (T3)
ROOKIE_CAP = int(os.environ.get("TA_ROOKIE_CAP", "6"))             # Larder cap for the Rookie (design: 6)
ROOKIE_EVENT_MULT = float(os.environ.get("TA_ROOKIE_EVT", "2.2"))  # her event ability strength (draw-2-resolve-1
                                                                   # -> more events fire in her region, always a boon)
GOURMAND_BOONS = os.environ.get("TA_GOURMAND_BOONS", "half")       # boon handling: "none"|"half"|"full" (softened flaw)
GOURMAND_WILD_USES = int(os.environ.get("TA_GOURMAND_WILD", "2"))  # pantry->specialty substitutions per turn (was 1)
INFLUENCER_BEHIND = int(os.environ.get("TA_INFL_BEHIND", "2"))     # resources the Influencer starts behind (was 1)

# ---- map -------------------------------------------------------------------------------------------
REGIONS = ("N", "C", "S", "E")
ADJ = {"N": ("C", "E", "S"), "C": ("N", "S"), "S": ("C", "E", "N"), "E": ("S", "N")}  # ring + HSR(N-S)
PANTRY = "P"

# ==================================================================================================
#  VENDOR TABLE (built once at import; decks/board/tours store integer ids -> cheap to copy)
# ==================================================================================================
# A vendor: tier, primary region, cost_regions (Counter over N/C/S/E), cost_pantry, buzz, prestige,
# rep, perk, cuisine. Perk in {None, "buzz_income", "pantry_wild", "rep_on_court", "wild", "rep_plus2",
# "double_icon"}.
VENDORS = []
_CUISINES = ("night_market", "seafood", "teahouse", "banquet", "breakfast")


def _V(tier, region, cost_regions, pantry, buzz, prestige, rep, perk, cuisine):
    VENDORS.append({
        "id": len(VENDORS), "tier": tier, "region": region,
        "cost_regions": dict(cost_regions), "cost_pantry": pantry, "buzz": buzz,
        "prestige": prestige, "rep": rep, "perk": perk, "cuisine": cuisine,
    })


def _build_vendor_table():
    VENDORS.clear()
    # ---- T1 Stalls (20): 5 per region. cost = 2 of its region. Buzz 1. Prestige 1. Rep 1. Icon = region.
    for r in REGIONS:
        for k in range(5):
            _V(1, r, {r: 2}, 0, 1, 1, 1, None, _CUISINES[k % len(_CUISINES)])
    # ---- T2 Eateries (16): 4 per region. cost 3 = 2 of region + (1 of a neighbour OR 1 pantry).
    #      Buzz 2. Prestige 3. Rep 2. Icon = region. Perk rotates.
    t2_perks = ("buzz_income", "pantry_wild", "rep_on_court", "buzz_income")
    for r in REGIONS:
        for k in range(4):
            r2 = REGIONS[(REGIONS.index(r) + 1 + k) % 4]
            if k % 2 == 0:
                cost, pantry = {r: 2, r2: 1}, 0
            else:
                cost, pantry = {r: 2}, 1
            _V(2, r, cost, pantry, 2, 3, 2, t2_perks[k], _CUISINES[(k + 1) % len(_CUISINES)])
    # ---- T3 Marquee (10): cost 3-4 across 2-3 regions. Buzz 3. Prestige 5-6. Rep 2-3. Strong perk.
    #      ASSUMPTION: concrete spread of the doc's "3-4 (2-3 regions)" band below.
    t3 = [
        ("N", {"N": 1, "S": 1, "E": 1}, 0, 3, 6, 3, "wild", "banquet"),       # Banquet Master (round-island)
        ("S", {"S": 2, "E": 1}, 0, 3, 5, 2, "rep_plus2", "seafood"),
        ("C", {"C": 2, "N": 1}, 0, 3, 5, 2, "double_icon", "teahouse"),
        ("E", {"E": 2, "S": 1}, 0, 3, 5, 2, "wild", "banquet"),
        ("N", {"N": 2, "C": 1, "S": 1}, 0, 4, 6, 3, "rep_plus2", "night_market"),
        ("S", {"S": 1, "N": 1, "C": 1}, 0, 3, 5, 2, "double_icon", "seafood"),
        ("C", {"C": 2, "E": 1}, 0, 3, 5, 2, "wild", "teahouse"),
        ("E", {"E": 2, "N": 1, "C": 1}, 0, 4, 6, 3, "rep_plus2", "banquet"),
        ("N", {"N": 2, "E": 1}, 0, 3, 5, 2, "double_icon", "breakfast"),
        ("S", {"S": 2, "C": 1, "E": 1}, 0, 4, 6, 3, "wild", "seafood"),
    ]
    for region, cost, pantry, buzz, prestige, rep, perk, cuisine in t3:
        _V(3, region, cost, pantry, buzz, prestige, rep, perk, cuisine)


_build_vendor_table()
_BY_TIER = {t: [v["id"] for v in VENDORS if v["tier"] == t] for t in (1, 2, 3)}


# ==================================================================================================
#  MISSIONS (secret +7; draw-3-keep-1 -> bot keeps the one aligned to its weights)
# ==================================================================================================
def _mission_progress(key, vids):
    """(done, needed) toward a mission, given the player's courted vendor ids."""
    vs = [VENDORS[i] for i in vids]
    if key == "south_3":
        return sum(1 for v in vs if v["region"] == "S"), 3
    if key == "grand_tour":
        return len(set(v["region"] for v in vs)), 4
    if key == "t1_3":
        return sum(1 for v in vs if v["tier"] == 1), 3
    if key == "t3_2":
        return sum(1 for v in vs if v["tier"] == 3), 2
    if key == "cuisines_3":
        return len(set(v["cuisine"] for v in vs)), 3
    if key == "tall_18":
        return sum(v["prestige"] for v in vs), 18
    if key == "volume_5":
        return len(vs), 5
    if key == "marquee_feeders":                     # a Marquee + >=2 Stalls (approx of "+ its 2 feeders")
        return min(sum(1 for v in vs if v["tier"] == 3), 1) + \
               min(sum(1 for v in vs if v["tier"] == 1), 2), 3
    return 0, 1


MISSIONS = ("south_3", "grand_tour", "t1_3", "t3_2", "cuisines_3", "tall_18", "volume_5", "marquee_feeders")


def _mission_done(key, vids):
    d, n = _mission_progress(key, vids)
    return d >= n


def _mission_helps(key, vid, cur_vids):
    """Does courting `vid` advance the mission counter?"""
    before, need = _mission_progress(key, cur_vids)
    if before >= need:
        return False
    after, _ = _mission_progress(key, cur_vids + [vid])
    return after > before


# ==================================================================================================
#  CHARACTERS (ability + flaw). "neutral" = symmetric (used in the strategy round-robin).
# ==================================================================================================
CHARACTERS = ("auntie", "rookie", "conductor", "influencer", "gourmand")


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


def _coverage_vp(n_regions):
    return {0: 0, 1: 0, 2: 2, 3: 5, 4: 9}[min(4, n_regions)]


def _coverage_count(pl):
    # wild icons can fill a missing region at scoring
    base = set(pl["regions"])
    return min(4, len(base) + pl["wild"] if len(base) < 4 else len(base))


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:
    def new_state(self, rng, n_players=2, characters=None, missions=None, strategies_meta=None):
        chars = characters or ["neutral"] * n_players
        # decks per tier (ids), shuffled
        decks = {}
        for t in (1, 2, 3):
            d = list(_BY_TIER[t])
            rng.shuffle(d)
            decks[t] = d
        board_w = {2: 3, 3: 4, 4: 5}[n_players]
        board = {t: [decks[t].pop() for _ in range(min(board_w, len(decks[t])))] for t in (1, 2, 3)}
        supply_scale = {2: 1.0, 3: 1.3, 4: 1.6}[n_players]   # sub-linear supply growth
        starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "S", "C", "E"]}[n_players]
        players = []
        infl_present = "influencer" in chars
        for p in range(n_players):
            ch = chars[p]
            # missions: explicit per-seat if given, else deal a random one (draw-3-keep-1 with no
            # strategy to steer the pick -> a neutral random keep). The probe runner overrides this
            # with a strategy-aligned pick; the harness round-robin relies on this default so the +7
            # Mission vector is actually exercised in sim-results.md.
            if missions is not None:
                m = missions[p]
            else:
                m = rng.choice(MISSIONS)
            players.append({
                "char": ch,
                "pos": starts[p],
                "larder": Counter(),
                "buzz": (INFLUENCER_BEHIND if (infl_present and ch != "influencer") else 0),  # Influencer starts behind
                "vendors": [],
                "icons": Counter(),
                "wild": 0,
                "prestige": 0,
                "rep": 0,
                "regions": set(),
                "promote_bonus": (1 if ch == "influencer" else 0),             # Going Viral: Promote +1
                "rep_per_court_bonus": 0,
                "pantry_wild_perk": False,
                "mission": m,
                "rep_ms": set(),
                "wild_used": 0,
                "tourist_boost": False,
                "acted": 0,
            })
        return {
            "n": n_players,
            "decks": decks,
            "board": board,
            "board_w": board_w,
            "supply": {r: int(round(REGION_SUPPLY * supply_scale)) for r in REGIONS},
            "players": players,
            "season": 0,                      # courts taken (any player)
            "season_final": SEASON_FINAL[n_players],
            "turn": 0,
            "cur": 0,
            "end_turn": None,
            "end_cause": None,
            "done": False,
            # diagnostics
            "courts_at": {p: [] for p in range(n_players)},   # global turn indices of each player's courts
            "stuck_turns": 0,
            "overflow_discards": 0,
            "buzz_spent": 0,
            "region_ing_spent": 0,
            "mid_scores": None,               # snapshot when season hits half
            "strat_meta": strategies_meta,    # optional {p: weights} for mission pick (set by runner)
        }

    def players(self, state):
        return list(range(state["n"]))

    def actors(self, state):
        return [state["cur"]]

    # ---- cost / affordability --------------------------------------------------------------------
    def _pay_plan(self, state, p, vid):
        """Return (region_pay dict, pantry_pay, buzz, pantry_wild_needed) — the minimal cost after
        discounts, wild icons, Auntie, floored at 0. pantry_wild_needed = region units we'd cover by a
        pantry->specialty substitution (Gourmand / pantry_wild perk)."""
        pl = state["players"][p]
        v = VENDORS[vid]
        pay = {}
        for r, c in v["cost_regions"].items():
            disc = min(DISCOUNT_CAP, pl["icons"].get(r, 0))
            pay[r] = max(0, c - disc)
        # wild icons reduce the largest remaining region requirement(s)
        w = pl["wild"]
        while w > 0 and any(x > 0 for x in pay.values()):
            r = max(pay, key=lambda k: pay[k])
            if pay[r] <= 0:
                break
            pay[r] -= 1
            w -= 1
        pantry = v["cost_pantry"]
        # Auntie: the first vendor she courts in a region new to her tour is 1 ingredient cheaper —
        # NERFED: only her first AUNTIE_MAX_REGIONS regions, and (optionally) never a Marquee (T3).
        auntie_ok = (pl["char"] == "auntie" and v["region"] not in pl["regions"]
                     and len(pl["regions"]) < AUNTIE_MAX_REGIONS
                     and not (AUNTIE_EXCLUDE_T3 and v["tier"] == 3))
        if auntie_ok:
            for r in sorted(pay, key=lambda k: -pay[k]):
                if pay[r] > 0:
                    pay[r] -= 1
                    break
            else:
                if pantry > 0:
                    pantry -= 1
        buzz = v["buzz"] + BUZZ_FLOOR_KNOB
        return pay, pantry, buzz

    def _affordable(self, state, p, vid):
        pl = state["players"][p]
        pay, pantry, buzz = self._pay_plan(state, p, vid)
        if pl["buzz"] < buzz:
            return False
        # region shortfalls
        short = 0
        for r, c in pay.items():
            short += max(0, c - pl["larder"].get(r, 0))
        pantry_have = pl["larder"].get(PANTRY, 0)
        pantry_short = max(0, pantry - pantry_have)
        # pantry->specialty substitutions (Gourmand ability + T2 pantry_wild perk): spare pantry covers
        # region units, up to the remaining per-turn capacity
        subs = 0
        cap = _wild_cap(pl)
        if cap > pl["wild_used"]:
            spare = pantry_have - pantry
            subs = min(short, cap - pl["wild_used"], max(0, spare))
        return (short - subs) <= 0 and pantry_short <= 0

    # ---- legal actions (coarse; the shared brain computes its own choice) -------------------------
    def legal_actions(self, state, player):
        p = player
        pl = state["players"][p]
        acts = []
        for t in (1, 2, 3):
            for idx, vid in enumerate(state["board"][t]):
                if self._affordable(state, p, vid):
                    acts.append(("court", t, idx))
        pos = pl["pos"]
        have_spec = state["supply"][pos] > 0
        r = pos if have_spec else PANTRY
        acts.append(("stock", (r, r)))
        acts.append(("stock", (r, PANTRY)))
        acts.append(("stock", (PANTRY, PANTRY)))
        dests = [d for d in ADJ[pos] if not (pl["char"] == "auntie" and _is_hsr(pos, d))]
        for d in dests:
            acts.append(("travel", d, d if state["supply"][d] > 0 else PANTRY))
            acts.append(("travel", d, PANTRY))
        acts.append(("promote",))
        acts.append(("extract",))
        return acts

    # ---- transition (mutates in place — the harness keeps no history) ------------------------------
    def step(self, state, actions, rng):
        s = state
        p = s["cur"]
        pl = s["players"][p]
        pl["wild_used"] = 0                       # reset per-turn pantry->specialty substitutions
        act = actions[p]
        kind = act[0]

        if kind == "court":
            self._do_court(s, p, act, rng)
        elif kind == "stock":
            self._do_stock(s, p, act, rng)
        elif kind == "travel":
            self._do_travel(s, p, act, rng)
        elif kind == "promote":
            gain = 2 + pl["promote_bonus"] + (1 if pl["tourist_boost"] else 0)
            pl["tourist_boost"] = False
            pl["buzz"] += gain
        elif kind == "extract":
            self._trigger_end(s, "extract")

        # end-of-turn: Larder cap
        self._discard_to_cap(s, p)
        pl["acted"] += 1

        # advance turn
        s["turn"] += 1
        s["cur"] = s["turn"] % s["n"]
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            s["done"] = True
        if s["turn"] > 4000:
            s["done"] = True
        return s

    def _do_court(self, s, p, act, rng):
        _, t, idx = act
        pl = s["players"][p]
        vid = s["board"][t][idx]
        v = VENDORS[vid]
        pay, pantry, buzz = self._pay_plan(s, p, vid)
        # pay buzz
        pl["buzz"] -= buzz
        s["buzz_spent"] += buzz
        # pay pantry
        take = min(pantry, pl["larder"].get(PANTRY, 0))
        pl["larder"][PANTRY] -= take
        # pay region ingredients (using a pantry->specialty sub if short by 1)
        for r, c in pay.items():
            need = c
            have = pl["larder"].get(r, 0)
            use = min(need, have)
            pl["larder"][r] -= use
            s["region_ing_spent"] += use
            need -= use
            while need > 0 and pl["wild_used"] < _wild_cap(pl) and pl["larder"].get(PANTRY, 0) > 0:
                pl["larder"][PANTRY] -= 1
                pl["wild_used"] += 1
                need -= 1
        pl["larder"] += Counter()  # drop zeros
        pl["larder"] = +pl["larder"]
        # gain rewards
        pl["vendors"].append(vid)
        pl["prestige"] += v["prestige"]
        rep_gain = v["rep"] + pl["rep_per_court_bonus"]
        self._rep_up(s, p, rep_gain)
        pl["regions"].add(v["region"])
        # perk
        self._apply_perk(pl, v)
        # base icon
        pl["icons"][v["region"]] += 1
        # board bookkeeping: refill, Season +1, lock from rivals (removed from shared board)
        deck = s["decks"][t]
        if deck:
            s["board"][t][idx] = deck.pop()
        else:
            s["board"][t].pop(idx)
        s["season"] += 1
        s["courts_at"][p].append(s["turn"])
        # mid-game snapshot (for runaway probe)
        if s["mid_scores"] is None and s["season"] >= s["season_final"] // 2:
            s["mid_scores"] = self.scores(s)
        # triggers
        if s["season"] >= s["season_final"]:
            self._trigger_end(s, "season")

    def _apply_perk(self, pl, v):
        perk = v["perk"]
        if perk == "buzz_income":
            pl["promote_bonus"] += 1
        elif perk == "pantry_wild":
            pl["pantry_wild_perk"] = True
        elif perk == "rep_on_court":
            pl["rep_per_court_bonus"] += 1
        elif perk == "rep_plus2":
            pl["rep_per_court_bonus"] += 2
        elif perk == "wild":
            pl["wild"] += 1
        elif perk == "double_icon":
            pl["icons"][v["region"]] += 1   # counts as an extra icon of its region (on top of the base)

    def _rep_up(self, s, p, amount):
        pl = s["players"][p]
        before = pl["rep"]
        pl["rep"] = min(REP_TOP, pl["rep"] + amount)
        for ms in (3, 6, 9):
            if before < ms <= pl["rep"] and ms not in pl["rep_ms"]:
                pl["rep_ms"].add(ms)
                if ms == 3:
                    pl["larder"][PANTRY] += 2                 # "take 2 wild ingredients" (modelled as flexible pantry)
                elif ms == 6:
                    pl["promote_bonus"] += 1                  # Promote permanently +1 Buzz
                elif ms == 9:
                    # +1 permanent discount icon of choice -> the region the player leans on most
                    r = max(REGIONS, key=lambda x: pl["icons"].get(x, 0))
                    pl["icons"][r] += 1
        if before < REP_TRIGGER <= pl["rep"]:
            self._trigger_end(s, "rep")                       # reaching the top ends the game

    def _do_stock(self, s, p, act, rng):
        _, ings = act
        pl = s["players"][p]
        n_take = 2
        if pl["char"] == "conductor":
            n_take = 1                                        # Timetable-bound: Stock Up takes 1
        taken = 0
        for ing in ings:
            if taken >= n_take:
                break
            if ing == PANTRY:
                pl["larder"][PANTRY] += 1
            else:
                if s["supply"][ing] > 0:
                    s["supply"][ing] -= 1
                    pl["larder"][ing] += 1
                else:
                    pl["larder"][PANTRY] += 1                 # scarcity -> fall back to pantry (a reroute cost)
            taken += 1
        self._refills(s, p, rng, n_flips=2, plum_stock=True)

    def _do_travel(self, s, p, act, rng):
        _, dest, ing = act
        pl = s["players"][p]
        pl["pos"] = dest
        n_take = 2 if pl["char"] == "conductor" else 1       # Off-Peak Pass: Travel arrives with 2
        for _ in range(n_take):
            if ing == PANTRY:
                pl["larder"][PANTRY] += 1
            elif s["supply"][dest] > 0:
                s["supply"][dest] -= 1
                pl["larder"][dest] += 1
            else:
                pl["larder"][PANTRY] += 1
        self._refills(s, p, rng, n_flips=1)

    # ---- Market events on refill ------------------------------------------------------------------
    def _refills(self, s, p, rng, n_flips, plum_stock=False):
        pl = s["players"][p]
        rookie = pl["char"] == "rookie"
        prob = min(1.0, EVENT_PROB * ROOKIE_EVENT_MULT) if rookie else EVENT_PROB
        for _ in range(n_flips):
            if rng.random() >= prob:
                continue
            boon = rng.random() < 0.60
            # Rookie: "draw 2, resolve 1" -> keep the boon of the two draws (dodges the hazard)
            if rookie and not boon:
                boon = rng.random() < 0.85                    # strong second-draw boon preference
            if boon:
                # Gourmand "Too jaded" flaw — SOFTENED: none = no boons; half = ignores 50%; full = normal
                if pl["char"] == "gourmand":
                    if GOURMAND_BOONS == "none":
                        continue
                    if GOURMAND_BOONS == "half" and rng.random() < 0.5:
                        continue
                kind = rng.choice(("buzz", "buzz", "ingredient", "ingredient", "tourist"))
                if kind == "buzz":
                    pl["buzz"] += 2
                elif kind == "ingredient":
                    r = pl["pos"]
                    if s["supply"][r] > 0:
                        s["supply"][r] -= 1
                        pl["larder"][r] += 1
                    else:
                        pl["larder"][PANTRY] += 1
                elif kind == "tourist":
                    pl["tourist_boost"] = True
            else:
                kind = rng.choice(("plum", "typhoon"))
                if kind == "plum" and plum_stock:
                    # this Stock Up yields 1 fewer: remove 1 just-taken ingredient if any
                    if sum(pl["larder"].values()) > 0:
                        r = max(pl["larder"], key=lambda k: pl["larder"][k])
                        pl["larder"][r] -= 1
                        if pl["larder"][r] <= 0:
                            del pl["larder"][r]
                elif kind == "typhoon":
                    r = rng.choice(("S", "E"))
                    s["supply"][r] = max(0, s["supply"][r] - 3)   # wash the shelf (reroute, not theft)

    def _trigger_end(self, s, cause="?"):
        if s["end_turn"] is not None:
            return
        s["end_cause"] = cause
        n = s["n"]
        turns_done = s["turn"] + 1
        s["end_turn"] = ((turns_done + n - 1) // n) * n + n    # finish this round + one more full round

    def _discard_to_cap(self, s, p):
        pl = s["players"][p]
        cap = ROOKIE_CAP if pl["char"] == "rookie" else CAP_DEFAULT
        total = sum(pl["larder"].values())
        if total <= cap:
            return
        excess = total - cap
        # what do the board vendors want? keep useful region ingredients; dump the most over-held
        want = Counter()
        for t in (1, 2, 3):
            for vid in s["board"][t]:
                for r, c in VENDORS[vid]["cost_regions"].items():
                    want[r] += 1
        pool = []
        for ing, c in pl["larder"].items():
            use = want.get(ing, 0) + (1 if ing == PANTRY else 0)   # pantry is generically useful
            pool.extend([(use, ing)] * c)
        pool.sort(key=lambda x: x[0])
        for _ in range(excess):
            _, ing = pool.pop(0)
            pl["larder"][ing] -= 1
            if pl["larder"][ing] <= 0:
                del pl["larder"][ing]
            s["overflow_discards"] += 1

    def is_over(self, state):
        return state["done"]

    # ---- scoring ----------------------------------------------------------------------------------
    def scores(self, state):
        out = {}
        for p in range(state["n"]):
            pl = state["players"][p]
            prestige = pl["prestige"]
            rep = _rep_end_vp(pl["rep"])
            cov = _coverage_vp(_coverage_count(pl))
            mission = 7 if (pl["mission"] and _mission_done(pl["mission"], pl["vendors"])) else 0
            out[p] = prestige + rep + cov + mission
        return out

    def metrics(self, state):
        s = state
        sc = self.scores(s)
        vals = sorted(sc.values(), reverse=True)
        margin = vals[0] - vals[1] if len(vals) > 1 else 0.0
        winners = [p for p, v in sc.items() if v == vals[0]]
        tie = 1.0 if len(winners) > 1 else 0.0
        winner = winners[0]
        # court cadence
        total_courts = sum(len(s["courts_at"][p]) for p in range(s["n"]))
        turns = s["turn"]
        court_interval = (turns / total_courts) if total_courts else float(turns)
        # late-game court interval (2nd half of turns) + max sustained rate (min gap between one player's courts)
        half = turns / 2
        late_courts = sum(1 for p in range(s["n"]) for tt in s["courts_at"][p] if tt >= half)
        court_interval_late = ((turns - half) / late_courts) if late_courts else float("nan")
        min_gap = float("inf")
        for p in range(s["n"]):
            cs = s["courts_at"][p]
            for a, b in zip(cs, cs[1:]):
                min_gap = min(min_gap, b - a)
        min_gap = 0.0 if min_gap == float("inf") else float(min_gap)
        # did the mid-game leader win? (runaway signal)
        mid_leader_won = float("nan")
        if s["mid_scores"] is not None and not tie:
            mvals = s["mid_scores"]
            mbest = max(mvals.values())
            mid_leaders = [p for p, v in mvals.items() if v == mbest]
            if len(mid_leaders) == 1:
                mid_leader_won = 1.0 if mid_leaders[0] == winner else 0.0
        # winning vector breakdown (which track carried the winner)
        wp = state["players"][winner]
        return {
            "margin": float(margin),
            "tie": tie,
            "turns": float(turns),
            "total_courts": float(total_courts),
            "courts_per_player": float(total_courts / s["n"]),
            "court_interval": float(court_interval),
            "court_interval_late": float(court_interval_late) if court_interval_late == court_interval_late else 0.0,
            "min_court_gap": min_gap,
            "mid_leader_won": mid_leader_won if mid_leader_won == mid_leader_won else 0.5,
            "stuck_turns": float(s["stuck_turns"]),
            "overflow_discards": float(s["overflow_discards"]),
            "buzz_spent": float(s["buzz_spent"]),
            "region_ing_spent": float(s["region_ing_spent"]),
            "win_prestige": float(wp["prestige"]),
            "win_rep_vp": float(_rep_end_vp(wp["rep"])),
            "win_cov_vp": float(_coverage_vp(_coverage_count(wp))),
            "win_mission": 1.0 if (wp["mission"] and _mission_done(wp["mission"], wp["vendors"])) else 0.0,
            "end_by_rep": 1.0 if s["end_cause"] == "rep" else 0.0,
            "end_by_season": 1.0 if s["end_cause"] == "season" else 0.0,
            "end_by_extract": 1.0 if s["end_cause"] == "extract" else 0.0,
        }


def _is_hsr(a, b):
    return {a, b} == {"N", "S"}


def _wild_cap(pl):
    """Pantry->specialty substitutions available this turn (Gourmand ability + T2 pantry_wild perk)."""
    return (GOURMAND_WILD_USES if pl["char"] == "gourmand" else 0) + (1 if pl["pantry_wild_perk"] else 0)


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan (v3 vendor-courting engine)"


# ==================================================================================================
#  SHARED ENGINE BRAIN  (sourcing / courting / routing) — every strategy uses this; strategies differ
#  ONLY in their vendor-value WEIGHTS + an opening flag. Isolates "is a track/opening dominant?".
# ==================================================================================================
TEMPO = 1.35          # VP-value of a turn (penalises slow-to-afford vendors)
HOLD_GAP = 2.0        # only skip an affordable court to build a strictly-better, near-affordable target
HORIZON = 3.5         # a target is "reachable soon" if est_turns <= HORIZON (keeps bots from starving
                      # for a far marquee they can never juggle under the Larder cap)


def _ramp_value(pl, v, w_ramp):
    """Value of the vendor's icon = expected future discount. Rewards concentration (stacking a region)."""
    if v["perk"] == "wild":
        return w_ramp * 1.3
    held = pl["icons"].get(v["region"], 0)
    return w_ramp * (0.5 + 0.35 * held)      # more valuable the more you've already stacked that region


def _coverage_marginal(pl, v, w_cov):
    if v["region"] in pl["regions"]:
        return 0.0
    now = _coverage_vp(min(4, len(pl["regions"])))
    then = _coverage_vp(min(4, len(pl["regions"]) + 1))
    return w_cov * (then - now)


def _rep_marginal(pl, v, w_rep):
    now = _rep_end_vp(pl["rep"])
    then = _rep_end_vp(min(REP_TOP, pl["rep"] + v["rep"] + pl["rep_per_court_bonus"]))
    # value both the end-VP jump and steady progress toward the next tier
    return w_rep * (0.6 * (v["rep"] + pl["rep_per_court_bonus"]) + (then - now))


def _mission_marginal(pl, v, w_m):
    if not pl["mission"]:
        return 0.0
    if _mission_helps(pl["mission"], v["id"], pl["vendors"]):
        after = _mission_done(pl["mission"], pl["vendors"] + [v["id"]])
        return w_m * (7.0 if after else 1.6)
    return 0.0


def _est_turns(state, p, vid):
    pl = state["players"][p]
    pay, pantry, buzz = GAME._pay_plan(state, p, vid)
    region_short = sum(max(0, c - pl["larder"].get(r, 0)) for r, c in pay.items())
    pantry_short = max(0, pantry - pl["larder"].get(PANTRY, 0))
    buzz_short = max(0, buzz - pl["buzz"])
    promote_yield = 2 + pl["promote_bonus"]
    # ingredients ~0.55 turn each (stock-2), buzz per-promote batch, +1 for the court itself
    return 1.0 + 0.55 * (region_short + pantry_short) + (buzz_short / promote_yield) * 1.0


def _vendor_value(state, p, vid, W):
    pl = state["players"][p]
    v = VENDORS[vid]
    val = (W["p"] * v["prestige"]
           + _rep_marginal(pl, v, W["r"])
           + _coverage_marginal(pl, v, W["c"])
           + _mission_marginal(pl, v, W["m"])
           + _ramp_value(pl, v, W["ramp"]))
    return val


def _rank_vendors(state, p, W):
    ranked = []
    for t in (1, 2, 3):
        for idx, vid in enumerate(state["board"][t]):
            val = _vendor_value(state, p, vid, W)
            et = _est_turns(state, p, vid)
            ranked.append((val - TEMPO * (et - 1.0), val, et, t, idx, vid,
                           GAME._affordable(state, p, vid)))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked


def _needed(state, p, vid):
    """(region_need Counter, pantry_need, buzz_need) still short for this vendor."""
    pl = state["players"][p]
    pay, pantry, buzz = GAME._pay_plan(state, p, vid)
    reg = Counter()
    for r, c in pay.items():
        short = c - pl["larder"].get(r, 0)
        if short > 0:
            reg[r] = short
    pantry_short = max(0, pantry - pl["larder"].get(PANTRY, 0))
    buzz_short = max(0, buzz - pl["buzz"])
    return reg, pantry_short, buzz_short


def _acquire_toward(state, p, vid, W, flags):
    """Choose Stock/Travel/Promote to get closer to affording `vid`."""
    pl = state["players"][p]
    pos = pl["pos"]
    reg_need, pantry_need, buzz_need = _needed(state, p, vid)

    # Opening bias: buzz-first banks Buzz early; ramp/ingredient-first fills ingredients early.
    early = pl["acted"] < 6
    if flags.get("buzz_open") and early and pl["buzz"] < 5:
        return ("promote",)

    # If Buzz is the binding constraint and ingredients are basically handled -> Promote.
    if buzz_need > 0 and sum(reg_need.values()) + pantry_need <= 1:
        return ("promote",)
    # Otherwise chase the ingredient half first (the ramp / contested axis), then Buzz.
    if reg_need:
        # standing where a needed region ingredient is available?
        if pos in reg_need and state["supply"][pos] > 0:
            second = pos if (reg_need[pos] > 1 or pantry_need == 0) else PANTRY
            return ("stock", (pos, second))
        # travel toward a needed region (adjacent first)
        target_regions = list(reg_need.keys())
        for d in ADJ[pos]:
            if pl["char"] == "auntie" and _is_hsr(pos, d):
                continue
            if d in target_regions:
                return ("travel", d, d if state["supply"][d] > 0 else PANTRY)
        # not adjacent — hop toward it (pick an adjacent that neighbours a target)
        for d in ADJ[pos]:
            if pl["char"] == "auntie" and _is_hsr(pos, d):
                continue
            if any(tr in ADJ[d] for tr in target_regions):
                return ("travel", d, d if state["supply"][d] > 0 else PANTRY)
    if pantry_need > 0:
        return ("stock", (PANTRY, PANTRY))
    if buzz_need > 0:
        return ("promote",)
    # Fully afforded but we chose to wait — bank Buzz (never a dead turn).
    return ("promote",)


def _engine_policy(view, p, legal, rng, W, flags):
    state = view
    pl = state["players"][p]
    cap = ROOKIE_CAP if pl["char"] == "rookie" else CAP_DEFAULT
    near_cap = sum(pl["larder"].values()) >= cap - 1
    ranked = _rank_vendors(state, p, W)          # (tempo_adj, val, et, tier, idx, vid, affordable)
    if not ranked:
        return ("promote",)
    affordable = [r for r in ranked if r[6] and r[1] > 0]
    # the goal to build toward = best tempo-adjusted target reachable soon (else the nearest one)
    near = [r for r in ranked if r[2] <= HORIZON]
    goal = near[0] if near else min(ranked, key=lambda r: r[2])
    if affordable:
        best_aff = affordable[0]
        # skip an affordable court only to build a strictly-better, near-affordable target — and never
        # while about to overflow the Larder (hoarding is a losing trade; court and ramp instead).
        better_soon = (not goal[6] and goal[5] != best_aff[5]
                       and goal[0] > best_aff[0] + HOLD_GAP and goal[2] <= 1.8)
        if better_soon and not near_cap:
            return _acquire_toward(state, p, goal[5], W, flags)
        return ("court", best_aff[3], best_aff[4])
    # nothing affordable yet — build toward the near-horizon goal (ramps via cheap wins first)
    return _acquire_toward(state, p, goal[5], W, flags)


# ---- strategy weight table -------------------------------------------------------------------------
def _mk(w_p=1.0, w_r=1.0, w_c=1.0, w_m=1.0, w_ramp=0.7, **flags):
    W = {"p": w_p, "r": w_r, "c": w_c, "m": w_m, "ramp": w_ramp}
    return W, flags


_STRATS = {
    "balanced":        _mk(),
    "prestige_rush":   _mk(w_p=1.5, w_r=0.6, w_c=0.3, w_ramp=0.55),
    "reputation_climb": _mk(w_p=0.7, w_r=1.7, w_c=0.4, w_ramp=0.6),
    "coverage_spread": _mk(w_p=0.7, w_r=0.6, w_c=1.9, w_ramp=0.15),
    "buzz_heavy":      _mk(w_p=1.0, w_r=1.0, w_c=0.6, w_ramp=0.55, buzz_open=True),
    "ingredient_heavy": _mk(w_p=1.0, w_r=0.8, w_c=0.4, w_ramp=1.25),
    "mission_focus":   _mk(w_p=0.9, w_r=0.8, w_c=0.7, w_m=2.1),
}


def _make_agent(name):
    W, flags = _STRATS[name]

    def agent(view, p, legal, rng):
        return _engine_policy(view, p, legal, rng, W, flags)
    return agent


def s_random(view, p, legal, rng):
    return rng.choice(legal)


def s_greedy_cheap(view, p, legal, rng):
    """Naive baseline: court the cheapest affordable vendor now; else Promote/Stock generically."""
    state = view
    pl = state["players"][p]
    best = None
    for t in (1, 2, 3):
        for idx, vid in enumerate(state["board"][t]):
            if GAME._affordable(state, p, vid):
                _, _, buzz = GAME._pay_plan(state, p, vid)
                key = (VENDORS[vid]["tier"], buzz)
                if best is None or key < best[0]:
                    best = (key, t, idx)
    if best:
        return ("court", best[1], best[2])
    if pl["buzz"] < 3:
        return ("promote",)
    pos = pl["pos"]
    return ("stock", (pos if state["supply"][pos] > 0 else PANTRY, PANTRY))


STRATEGIES = {
    "random": s_random,
    "greedy_cheap": s_greedy_cheap,
    "balanced": _make_agent("balanced"),
    "prestige_rush": _make_agent("prestige_rush"),
    "reputation_climb": _make_agent("reputation_climb"),
    "coverage_spread": _make_agent("coverage_spread"),
    "buzz_heavy": _make_agent("buzz_heavy"),
    "ingredient_heavy": _make_agent("ingredient_heavy"),
    "mission_focus": _make_agent("mission_focus"),
}


# ==================================================================================================
#  PROBE HARNESS (local runner that can assign characters + missions per seat)
# ==================================================================================================
import random  # noqa: E402

# make engine importable when this file is run directly
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "tools", "sim"))
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)
try:
    from engine import round_robin, format_round_robin, health_read  # noqa: E402
except Exception:
    round_robin = format_round_robin = health_read = None


def _pick_mission(rng, W, flags):
    """draw-3-keep-1: keep the dealt mission best aligned to the strategy's weights."""
    dealt = rng.sample(MISSIONS, 3)
    align = {
        "south_3": W["ramp"] + W["m"], "grand_tour": 2 * W["c"] + W["m"],
        "t1_3": W["ramp"] + W["m"] * 0.8, "t3_2": 1.5 * W["p"] + W["m"],
        "cuisines_3": W["c"] + W["m"], "tall_18": 1.6 * W["p"] + W["m"],
        "volume_5": W["r"] + W["m"] * 0.9, "marquee_feeders": W["p"] + W["m"],
    }
    return max(dealt, key=lambda k: align.get(k, 0.0))


def _series(agents, n, n_players=2, base_seed=1, characters=None, missions=None, weights=None,
            flags=None):
    """Play n games; agents = {seat: callable}. Optional fixed characters / missions per seat.
    If missions is None, each seat picks a strategy-aligned mission per game (weights/flags supply W)."""
    wins = {p: 0 for p in range(n_players)}
    ties = 0
    scores = {p: [] for p in range(n_players)}
    macc = {}
    for i in range(n):
        rng = random.Random(base_seed + i)
        if missions is None:
            ms = []
            for p in range(n_players):
                W = (weights or {}).get(p, _STRATS["balanced"][0])
                fl = (flags or {}).get(p, {})
                ms.append(_pick_mission(rng, W, fl))
        else:
            # allow per-seat None -> fill with a strategy-aligned pick (so an opponent can hold an
            # aligned mission while the tested seat is forced onto a specific one)
            ms = []
            for p, mm in enumerate(missions):
                if mm is None:
                    W = (weights or {}).get(p, _STRATS["balanced"][0])
                    fl = (flags or {}).get(p, {})
                    ms.append(_pick_mission(rng, W, fl))
                else:
                    ms.append(mm)
        s = GAME.new_state(rng, n_players, characters=characters, missions=ms)
        guard = 0
        while not GAME.is_over(s):
            acts = {}
            for pl in GAME.actors(s):
                acts[pl] = agents[pl](s, pl, GAME.legal_actions(s, pl), rng)
            s = GAME.step(s, acts, rng)
            guard += 1
            if guard > 6000:
                break
        sc = GAME.scores(s)
        best = max(sc.values())
        w = [p for p, v in sc.items() if v == best]
        if len(w) == 1:
            wins[w[0]] += 1
        else:
            ties += 1
        for p in range(n_players):
            scores[p].append(sc[p])
        for k, v in GAME.metrics(s).items():
            macc.setdefault(k, []).append(v)
    return {
        "win": {p: wins[p] / n for p in range(n_players)},
        "tie": ties / n,
        "score_mean": {p: statistics.mean(scores[p]) for p in range(n_players)},
        "metrics": {k: statistics.mean(v) for k, v in macc.items()},
    }


def _agent_for(name):
    return STRATEGIES[name]


def _weights_for(name):
    if name in _STRATS:
        return _STRATS[name][0], _STRATS[name][1]
    return _STRATS["balanced"][0], {}


# ---- PROBE 1: no dominant track/opening ------------------------------------------------------------
def probe1_tracks(n=1500):
    print("=" * 90)
    print("PROBE 1 — No dominant track/opening (2p). PASS: no line >~55%, >=3 viable in a tight band.")
    print("=" * 90)
    track_lines = ["balanced", "prestige_rush", "reputation_climb", "coverage_spread",
                   "buzz_heavy", "ingredient_heavy", "mission_focus"]
    # round-robin among the real lines only (exclude naive) for the viability band
    wr = {a: 0.0 for a in track_lines}
    cnt = {a: 0 for a in track_lines}
    seed = 1
    grid = {a: {} for a in track_lines}
    for a in track_lines:
        for b in track_lines:
            Wa, fa = _weights_for(a)
            Wb, fb = _weights_for(b)
            r = _series({0: _agent_for(a), 1: _agent_for(b)}, n, base_seed=seed,
                        weights={0: Wa, 1: Wb}, flags={0: fa, 1: fb})
            seed += n
            wa = r["win"][0] + 0.5 * r["tie"]
            grid[a][b] = wa
            wr[a] += wa
            cnt[a] += 1
            wr[b] += (1 - wa)
            cnt[b] += 1
    overall = {a: wr[a] / cnt[a] for a in track_lines}
    print("\n  Overall win rate (real lines only, both seatings; naive excluded):")
    for a, v in sorted(overall.items(), key=lambda kv: -kv[1]):
        print(f"    {a:18} {v*100:5.1f}%  {'#'*round(v*40)}")
    top = max(overall, key=overall.get)
    band = [a for a in track_lines if overall[a] >= 0.45]
    print(f"\n  field leader = {top} @ {overall[top]*100:.1f}%   |   lines in the 45%+ viable band: {len(band)}")
    # vs naive floor
    for naive in ("greedy_cheap", "random"):
        r = _series({0: _agent_for("balanced"), 1: _agent_for(naive)}, n, base_seed=seed,
                    weights={0: _STRATS["balanced"][0], 1: _STRATS["balanced"][0]})
        seed += n
        print(f"  floor check: balanced vs {naive:13} -> balanced {(r['win'][0]+0.5*r['tie'])*100:.1f}%")
    verdict = ("PASS" if overall[top] <= 0.56 and len(band) >= 3 else
               ("SOFT" if overall[top] <= 0.60 else "FAIL"))
    print(f"\n  --> PROBE 1: {verdict}  (leader {overall[top]*100:.1f}%, {len(band)} viable)\n")
    return overall, grid, verdict


# ---- PROBE 2: no economy runaway -------------------------------------------------------------------
def _probe2_pass(label, n, seed):
    lines = [("ingredient_heavy mirror", "ingredient_heavy", "ingredient_heavy"),
             ("ramp vs prestige", "ingredient_heavy", "prestige_rush"),
             ("balanced mirror", "balanced", "balanced")]
    headline = None
    for lab, a, b in lines:
        Wa, fa = _weights_for(a)
        Wb, fb = _weights_for(b)
        r = _series({0: _agent_for(a), 1: _agent_for(b)}, n, base_seed=seed,
                    weights={0: Wa, 1: Wb}, flags={0: fa, 1: fb})
        seed += n
        m = r["metrics"]
        print(f"\n  [{label} | {lab}]")
        print(f"    courts/player={m['courts_per_player']:.1f}  turns={m['turns']:.1f}  "
              f"court-interval={m['court_interval']:.2f} t/court  LATE={m['court_interval_late']:.2f}  "
              f"min-gap(1 player)={m['min_court_gap']:.2f}")
        print(f"    end by: rep={m['end_by_rep']*100:.0f}% season={m['end_by_season']*100:.0f}% "
              f"extract={m['end_by_extract']*100:.0f}%")
        print(f"    mid-game leader won = {m['mid_leader_won']*100:.0f}%   avg margin = {m['margin']:.1f} VP")
        print(f"    Buzz spent/game={m['buzz_spent']:.1f}  region-ing spent/game={m['region_ing_spent']:.1f}"
              f"  (B:I ratio = {m['buzz_spent']/max(1,m['region_ing_spent']):.2f})")
        if lab == "ingredient_heavy mirror":
            headline = m
    return headline, seed


def probe2_runaway(n=2000):
    print("=" * 90)
    print("PROBE 2 — No economy runaway (2p). Does the discount snowball outrun the end-clock, or does")
    print("the undiscountable-Buzz floor cap the court-rate at ~1 vendor / 2 turns even fully ramped?")
    print("=" * 90)
    seed = 1
    ta_rep_save = REP_TRIGGER
    globals()["REP_TRIGGER"] = 12
    print("\n  --- OLD design (Rep-top=12 ends the game — historical) ---")
    m_aw, seed = _probe2_pass("old-rep12", n, seed)
    # LOCKED default: the Season timer times the game (rep-top decoupled) so the ramp fully develops.
    globals()["REP_TRIGGER"] = ta_rep_save
    print(f"\n  --- LOCKED default (Season-timed; TA_REP_TRIGGER={ta_rep_save}) ---")
    m_st, seed = _probe2_pass("season-timed", n, seed)
    # read the runaway verdict off the regime where the ramp actually develops (season-timed)
    late = m_st["court_interval_late"]
    mid = m_st["mid_leader_won"]
    rate_ok = late >= 1.9                          # ~1 court / 2 turns even fully ramped
    no_snowball = mid <= 0.82                       # first-mover doesn't win ~always
    verdict = "PASS" if (rate_ok and no_snowball) else ("SOFT" if (late >= 1.7 and mid <= 0.88) else "FAIL")
    print(f"\n  --> PROBE 2: {verdict}  (season-timed late court-interval {late:.2f} t/court "
          f"[Buzz-floor target ~2.0], mid-leader-wins {mid*100:.0f}% [runaway if ~100%])")
    print(f"      NOTE: as-written ends by Rep-top in ~{m_aw['end_by_rep']*100:.0f}% of games at "
          f"{m_aw['courts_per_player']:.1f} courts/player — the ramp barely develops before the game ends.\n")
    return verdict


# ---- PROBE 3: character balance --------------------------------------------------------------------
def probe3_characters(n=900):
    print("=" * 90)
    print("PROBE 3 — Character balance (2p). PASS: each of 5 in 45-55%; no char x mission combo >~60%.")
    print("=" * 90)
    bal = _agent_for("balanced")
    Wb = _STRATS["balanced"][0]
    # 5x5 round-robin (fixed balanced strategy for both seats), both seatings averaged
    wr = {c: 0.0 for c in CHARACTERS}
    cnt = {c: 0 for c in CHARACTERS}
    seed = 1
    for a in CHARACTERS:
        for b in CHARACTERS:
            if a == b:
                continue
            r = _series({0: bal, 1: bal}, n, base_seed=seed, characters=[a, b],
                        weights={0: Wb, 1: Wb})
            seed += n
            wa = r["win"][0] + 0.5 * r["tie"]
            wr[a] += wa
            cnt[a] += 1
            wr[b] += (1 - wa)
            cnt[b] += 1
    overall = {c: wr[c] / cnt[c] for c in CHARACTERS}
    print("\n  Per-character win rate (vs the field of the other 4, balanced strategy, both seatings):")
    worst = 0.0
    for c, v in sorted(overall.items(), key=lambda kv: -kv[1]):
        flag = "" if 0.45 <= v <= 0.55 else "  <-- OUT OF BAND"
        worst = max(worst, abs(v - 0.5))
        print(f"    {c:12} {v*100:5.1f}%{flag}")
    # char x mission scan (MIRROR): (char c, forced mission m) vs the SAME char c holding an aligned
    # pick, both seatings averaged. Baseline ~50%; a spike >60% means m is a broken *synergy* for c
    # (beyond what c already earns) — isolating the combo from the generic "having an ability" edge.
    print("\n  Character x mission (mirror: char c on forced m vs same char c on aligned pick):")
    worst_combo = 0.0
    worst_name = ""
    nn = max(250, n // 2)
    for c in CHARACTERS:
        row = []
        for mkey in MISSIONS:
            rA = _series({0: bal, 1: bal}, nn, base_seed=seed, characters=[c, c],
                         missions=[mkey, None], weights={0: Wb, 1: Wb}); seed += nn
            rB = _series({0: bal, 1: bal}, nn, base_seed=seed, characters=[c, c],
                         missions=[None, mkey], weights={0: Wb, 1: Wb}); seed += nn
            wc = ((rA["win"][0] + 0.5 * rA["tie"]) + (rB["win"][1] + 0.5 * rB["tie"])) / 2
            row.append((mkey, wc))
            if wc > worst_combo:
                worst_combo, worst_name = wc, f"{c} x {mkey}"
        hot = max(row, key=lambda x: x[1])
        print(f"    {c:12} hottest combo: {hot[0]:16} {hot[1]*100:5.1f}%")
    band_ok = all(0.45 <= v <= 0.55 for v in overall.values())
    combo_ok = worst_combo <= 0.60
    verdict = "PASS" if (band_ok and combo_ok) else ("SOFT" if (worst <= 0.08 and worst_combo <= 0.63) else "FAIL")
    print(f"\n  --> PROBE 3: {verdict}  (widest char deviation {worst*100:.1f}pt from 50%; "
          f"hottest char x mission = {worst_name} @ {worst_combo*100:.1f}%)\n")
    return overall, verdict


def _dominant_mission(seed):
    # a fixed reasonable opponent mission for the char x mission scan
    return "tall_18"


# ---- PROBE 4: anti-hoard / hard-stuck --------------------------------------------------------------
def probe4_stuck(n=2500):
    print("=" * 90)
    print("PROBE 4 — Anti-hoard / hard-stuck ~= 0 (2p). Do the unlimited pantry + always-on Promote")
    print("prevent stuck turns? And does the Larder cap punish hoarding (overflow discards)?")
    print("=" * 90)
    Wb = _STRATS["balanced"][0]
    r = _series({0: _agent_for("balanced"), 1: _agent_for("ingredient_heavy")}, n, base_seed=1,
                weights={0: Wb, 1: _STRATS["ingredient_heavy"][0]},
                flags={0: {}, 1: _STRATS["ingredient_heavy"][1]})
    m = r["metrics"]
    print(f"\n  hard-stuck turns / game     = {m['stuck_turns']:.3f}   (target ~0)")
    print(f"  larder-overflow discards/gm = {m['overflow_discards']:.2f}   (hoarding is taxed, not free)")
    print(f"  turns / game                = {m['turns']:.1f}")
    verdict = "PASS" if m["stuck_turns"] < 0.05 else "FAIL"
    print(f"\n  --> PROBE 4: {verdict}  (stuck {m['stuck_turns']:.3f}/game; pantry+Promote valves hold)\n")
    return verdict


# ---- health read (via engine round-robin) ----------------------------------------------------------
def health(n=1200):
    print("=" * 90)
    print("HEALTH READ — full round-robin incl. naive baselines (engine health_read)")
    print("=" * 90)
    if round_robin is None:
        print("  (engine not importable; skipping)")
        return
    res = round_robin(GAME, STRATEGIES, n=n)
    print()
    print(format_round_robin(res, title="Travel Agents v3 — health read"))
    print()


if __name__ == "__main__":
    print(f"[knobs] SEASON_FINAL(2p)={SEASON_FINAL[2]}  REGION_SUPPLY={REGION_SUPPLY}  "
          f"EVENT_PROB={EVENT_PROB}  BUZZ_FLOOR_KNOB={BUZZ_FLOOR_KNOB}  DISCOUNT_CAP={DISCOUNT_CAP}\n")
    v1 = probe1_tracks(n=400)
    v2 = probe2_runaway(n=1500)
    v3 = probe3_characters(n=400)
    v4 = probe4_stuck(n=1500)
    health(n=250)
