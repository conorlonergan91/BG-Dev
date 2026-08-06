"""
travel_agents.py — Travel Agents: Taiwan (spine A "Rival Agents, Shared Beat") encoded for the
simulation harness (see tools/sim/engine.py). Stdlib-only.

Implements the first-pass rules in ../design/design-doc.md so we can attack the design's single
make-or-break assumption BEFORE any human playtest:

  Q1  Hoarder vs Generous-tipper (2p): is the Dead-drop individually rational, i.e. does cooperating
      (G) beat hoarding (H)?  PASS = G >= H.   (round-robin + --matchup H:G, and the __main__ report.)
  Q2  Kingmaker probe (3p): how much does ONE player's dead-drop *recipient* choice move the OTHER
      two's win rates?  PASS = small swing.    (kingmaker_probe(); printed in __main__.)
  Q3  Payout-C trigger-share (2p): does the winner sweep a disproportionate share of the 4 milestone
      picks, and does the +1-VP option ever solely decide a game?  PASS = spread & rarely decisive.
      (metrics: winner_pick_share, vp_pick_decisive.)
Plus the standard health read (dominant line? score spread? margin? draw rate?).

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (so we know what the sim does and doesn't cover)
------------------------------------------------------------------------------------------------------
Faithfully modelled: the 4-region ring + HSR (N-S) adjacency; Stock Up (+2 here) / Travel (+1 & move) /
Plate (spend recipe -> VP, Dossier +1, refill Menu) / Dead-drop (give 1 ingredient to a rival -> +1
Insider Tip, Dossier +1) / Extract; the region<->ingredient web (8 specialties + fungible pantry);
the shared face-up Menu race; the Larder cap of 7 (auto-discard down at end of turn); the Grand Dossier
+ payout-C milestones (flat base to all AND a triggerer pick of Insider Tip *or* +1 VP); scaled Dossier
thresholds [n*2,n*4,n*6,n*8]; the secret Assignment (+7, draw-2-keep-1); the end trigger (Extract OR
final milestone -> finish the round + one more full round); the 3-4p "receive <=1 Dead-drop per round".

Simplifications (noted in sim-notes):
  * SHARED "productive brain": sourcing/plating/routing is one greedy heuristic used by every strategy;
    strategies differ ONLY in Dead-drop policy (never / aggressive / rational) + recipient choice + the
    milestone-pick choice. This isolates the make-or-break variable exactly as beacon.py isolates the
    signal policy. Bots are a FLOOR on depth, not a ceiling — they rule out broken math and dominant/
    dead lines; they cannot judge whether the tip decision is *fun* (that's the human session).
  * Insider Tip is modelled through its two load-bearing uses: (a) +1 extra ingredient when you Stock Up,
    and (b) wild-substitute a recipe ingredient when you Plate. The "+1 travel hop" (c) is folded into
    routing (reachability). A tip's realised value is thus ~one sourcing step, matching the doc's
    "~+1 ingredient of flexibility". TIP_TEMPO exposes this as a knob.
  * Draw-2-keep-1 is approximated as one random Assignment per player (all types are ~equal difficulty by
    design, so the keep-1 choice mainly de-risks a bad draw; it barely moves balance).
  * Ingredient supply is unlimited/open (as specified). Dish deck ~24 built from the 14 exemplar recipes
    with duplicates of night-market staples (~46% cross-region), reshuffle-free (menu just stops
    refilling if the deck empties — rare).
"""
from __future__ import annotations

import copy
import os
import random
import statistics
from collections import Counter

# ---- sim-only knobs (env vars; do NOT change the printed game rules) ------------------------------
CAP = int(os.environ.get("TA_CAP", "7"))                 # Larder cap
TIP_TEMPO = float(os.environ.get("TA_TIP_TEMPO", "0.7")) # value of 1 Insider Tip in "ingredient" units
DEADDROP_VP = float(os.environ.get("TA_DEADDROP_VP", "0"))  # optional +VP per dead-drop (knob to test)

# ---- map -------------------------------------------------------------------------------------------
REGIONS = ("N", "C", "S", "E")
ADJ = {"N": ("C", "E", "S"), "C": ("N", "S"), "S": ("C", "E", "N"), "E": ("S", "N")}  # ring + HSR(N-S)
SPEC = {"N": ("Beef", "Pork"), "C": ("Tea", "Pearls"), "S": ("Oysters", "Milkfish"), "E": ("Rice", "Greens")}
ING_REGION = {i: r for r, pair in SPEC.items() for i in pair}   # Pantry has no region
PANTRY = "Pantry"


def _avail(region):
    return set(SPEC[region]) | {PANTRY}


def _dish(name, vp, *recipe):
    rec = Counter(recipe)
    regions = frozenset(ING_REGION[i] for i in rec if i in ING_REGION)
    return {"name": name, "vp": vp, "recipe": rec, "regions": regions, "size": sum(rec.values())}


# 14 exemplar recipes (design-doc). VP: 2-ingredient=3, 3-ingredient=4, Signature(3 regions)=5.
_BASE_DISHES = [
    _dish("Beef noodle soup", 3, "Beef", PANTRY),
    _dish("Gua bao", 3, "Pork", PANTRY),
    _dish("Bubble tea", 3, "Tea", "Pearls"),
    _dish("Tea egg", 3, "Tea", PANTRY),
    _dish("Oyster omelette", 3, "Oysters", PANTRY),
    _dish("Oyster vermicelli", 3, "Oysters", PANTRY),
    _dish("Bamboo-tube rice", 3, "Rice", "Greens"),
    _dish("Milkfish porridge", 3, "Milkfish", "Rice"),
    _dish("Chishang bento", 4, "Rice", "Pork", PANTRY),
    _dish("East-coast platter", 4, "Greens", "Milkfish", PANTRY),
    _dish("Hakka stir-fry", 4, "Pork", "Tea", PANTRY),
    _dish("Braised-pork rice", 4, "Pork", "Rice", PANTRY),
    _dish("Banquet platter", 5, "Oysters", "Beef", "Greens"),      # Signature
    _dish("Round-island feast", 5, "Beef", "Tea", "Milkfish"),     # Signature
]
# ~24-card deck: 14 distinct + duplicates of staples (keeps ~46% cross-region, each specialty in 5-6).
_DUPES = ["Beef noodle soup", "Gua bao", "Bubble tea", "Tea egg", "Oyster omelette", "Bamboo-tube rice",
          "Chishang bento", "Hakka stir-fry", "Milkfish porridge", "Braised-pork rice"]
_BY_NAME = {d["name"]: d for d in _BASE_DISHES}


def _new_deck():
    deck = [dict(d) for d in _BASE_DISHES] + [dict(_BY_NAME[n]) for n in _DUPES]
    return deck


# ---- assignments (the one hidden hook; +7 VP, binary) ----------------------------------------------
SOUTHERN = {"Oysters", "Milkfish"}
_ASSIGN_TYPES = ["south_crawl", "variety", "signature_obsession", "big_eater", "night_market"]


def _make_assignment(rng):
    t = rng.choice(_ASSIGN_TYPES)
    a = {"type": t}
    if t == "signature_obsession":
        names = [d["name"] for d in _BASE_DISHES]
        a["targets"] = tuple(rng.sample(names, 2))
    return a


def _assign_state(a, log):
    """(done, needed) progress counters for an assignment given the player's plated log."""
    t = a["type"]
    if t == "south_crawl":
        return sum(1 for d in log if d["recipe"] & Counter(SOUTHERN)), 3
    if t == "variety":
        regions = set()
        for d in log:
            regions |= d["regions"]
        return len(regions & set(REGIONS)), 4
    if t == "signature_obsession":
        got = set(d["name"] for d in log)
        return sum(1 for n in a["targets"] if n in got), 2
    if t == "big_eater":
        return sum(1 for d in log if d["size"] >= 3), 2
    if t == "night_market":
        return len(log), 4
    return 0, 1


def _assign_complete(a, log):
    done, needed = _assign_state(a, log)
    return done >= needed


def _assign_marginal(a, log, dish):
    """Does plating `dish` advance the assignment counter? Returns (increment, completes)."""
    done, needed = _assign_state(a, log)
    if done >= needed:
        return 0, False
    t = a["type"]
    inc = 0
    if t == "south_crawl":
        inc = 1 if (dish["recipe"] & Counter(SOUTHERN)) else 0
    elif t == "variety":
        cur = set()
        for d in log:
            cur |= d["regions"]
        inc = 1 if (dish["regions"] - cur) else 0
    elif t == "signature_obsession":
        got = set(d["name"] for d in log)
        inc = 1 if (dish["name"] in a["targets"] and dish["name"] not in got) else 0
    elif t == "big_eater":
        inc = 1 if dish["size"] >= 3 else 0
    elif t == "night_market":
        inc = 1
    return inc, (done + inc >= needed and inc > 0)


# ---- heuristic weights -----------------------------------------------------------------------------
ASSIGN_STEP = 1.8      # value of one step of assignment progress (steers routing)
COMPLETE_BONUS = 7.0   # the Assignment payoff (+7 VP)


def _want(dish, assignment, log):
    inc, completes = _assign_marginal(assignment, log, dish)
    return dish["vp"] + (ASSIGN_STEP if inc > 0 else 0.0) + (COMPLETE_BONUS if completes else 0.0)


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:
    def new_state(self, rng, n_players=2):
        deck = _new_deck()
        rng.shuffle(deck)
        menu_size = {2: 4, 3: 5, 4: 6}[n_players]
        menu = [deck.pop() for _ in range(menu_size)]
        starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "S", "C", "E"]}[n_players]
        thresholds = [n_players * 2, n_players * 4, n_players * 6, n_players * 8]
        return {
            "n": n_players,
            "menu_size": menu_size,
            "deck": deck,
            "menu": menu,
            "pos": {p: starts[p] for p in range(n_players)},
            "larder": {p: Counter() for p in range(n_players)},
            "tips": {p: 0 for p in range(n_players)},
            "log": {p: [] for p in range(n_players)},
            "assignment": {p: _make_assignment(rng) for p in range(n_players)},
            "dossier": 0,
            "thresholds": thresholds,
            "next_ms": 0,                         # index into thresholds
            "flat_base": [2, 3, 4, 5],            # payout-C flat base per milestone (equal to all)
            "flat_awarded": {p: 0 for p in range(n_players)},
            "bonus_vp": {p: 0 for p in range(n_players)},   # +1-VP milestone picks banked
            "picks": {p: [] for p in range(n_players)},     # list of "vp"/"tip" per triggered milestone
            "received": {p: 0 for p in range(n_players)},   # dead-drops received this round (3-4p cap)
            "turn": 0,                            # global turn counter (player-turns taken)
            "cur": 0,                             # whose turn
            "end_turn": None,                     # set when end-trigger fires
            "deaddrops": 0,                       # diagnostic
            "done": False,
        }

    def players(self, state):
        return list(range(state["n"]))

    def actors(self, state):
        return [state["cur"]]

    # ---- legal (fully-resolved) actions -----------------------------------------------------------
    def legal_actions(self, state, player):
        acts = []
        p = player
        pos = state["pos"][p]
        larder = state["larder"][p]
        tips = state["tips"][p]
        # Plate: any menu dish affordable with 0..k wilds (k = tips), minimal wilds
        for i, dish in enumerate(state["menu"]):
            missing = 0
            for ing, cnt in dish["recipe"].items():
                have = larder.get(ing, 0)
                if have < cnt:
                    missing += cnt - have
            if missing <= tips:
                acts.append(("plate", i, missing))
        # Stock Up: 2 ingredients available here (with repetition). Optionally a 3rd via a tip.
        avail = sorted(_avail(pos))
        pairs = set()
        for a in avail:
            for b in avail:
                pairs.add(tuple(sorted((a, b))))
        for pr in pairs:
            acts.append(("stock", pos, pr, 0))
            if tips >= 1:
                for c in avail:
                    acts.append(("stock", pos, tuple(sorted(pr + (c,))), 1))
        # Travel: to an adjacent region, arrive with 1 available ingredient
        for dest in ADJ[pos]:
            for ing in sorted(_avail(dest)):
                acts.append(("travel", dest, ing))
        # Dead-drop: give 1 larder ingredient to a rival (respect 3-4p receive cap)
        recips = [q for q in range(state["n"]) if q != p and
                  (state["n"] == 2 or state["received"][q] < 1)]
        for ing in sorted(larder):
            if larder[ing] > 0:
                for q in recips:
                    acts.append(("deaddrop", ing, q))
        # Extract
        acts.append(("extract",))
        return acts

    # ---- transition -------------------------------------------------------------------------------
    def step(self, state, actions, rng):
        s = copy.deepcopy(state)
        p = s["cur"]
        act = actions[p]
        kind = act[0]

        if kind == "plate":
            _, idx, n_wild = act
            dish = s["menu"][idx]
            # pay recipe from larder; wilds cover the shortfall
            need = dict(dish["recipe"])
            for ing, cnt in need.items():
                take = min(cnt, s["larder"][p].get(ing, 0))
                s["larder"][p][ing] -= take
                if s["larder"][p][ing] <= 0:
                    del s["larder"][p][ing]
            s["tips"][p] -= n_wild
            s["log"][p].append(dish)
            # refill menu
            if s["deck"]:
                s["menu"][idx] = s["deck"].pop()
            else:
                s["menu"].pop(idx)
            self._dossier_advance(s, p)

        elif kind == "stock":
            _, region, ings, n_tip = act
            for ing in ings:
                s["larder"][p][ing] += 1
            s["tips"][p] -= n_tip

        elif kind == "travel":
            _, dest, ing = act
            s["pos"][p] = dest
            s["larder"][p][ing] += 1

        elif kind == "deaddrop":
            _, ing, q = act
            s["larder"][p][ing] -= 1
            if s["larder"][p][ing] <= 0:
                del s["larder"][p][ing]
            s["larder"][q][ing] += 1
            s["tips"][p] += 1
            s["received"][q] += 1
            s["deaddrops"] += 1
            s["bonus_vp"][p] += 0  # placeholder for DEADDROP_VP knob applied below
            if DEADDROP_VP:
                s["bonus_vp"][p] += DEADDROP_VP
            self._dossier_advance(s, p)

        elif kind == "extract":
            self._trigger_end(s)

        # end-of-turn: discard down to CAP (auto, for free)
        self._discard_to_cap(s, p, rng)

        # advance turn / round bookkeeping
        s["turn"] += 1
        s["cur"] = s["turn"] % s["n"]
        if s["cur"] == 0:                       # a full round just completed
            s["received"] = {q: 0 for q in range(s["n"])}
        # end?
        if s["end_turn"] is not None and s["turn"] >= s["end_turn"]:
            s["done"] = True
        if s["turn"] > 600:                      # hard guard
            s["done"] = True
        return s

    def _dossier_advance(self, s, p):
        s["dossier"] += 1
        # cross milestones (can cross at most one per action given +1 steps)
        while s["next_ms"] < len(s["thresholds"]) and s["dossier"] >= s["thresholds"][s["next_ms"]]:
            ms = s["next_ms"]
            base = s["flat_base"][ms]
            for q in range(s["n"]):
                s["flat_awarded"][q] += base           # flat base to everyone (ranking-neutral)
            # triggerer pick: +1 VP or an Insider Tip
            pick = self._milestone_pick(s, p)
            s["picks"][p].append(pick)
            if pick == "vp":
                s["bonus_vp"][p] += 1
            else:
                s["tips"][p] += 1
            s["next_ms"] += 1
            if s["next_ms"] >= len(s["thresholds"]):   # final milestone -> end trigger
                self._trigger_end(s)

    def _milestone_pick(self, s, p):
        """Triggerer chooses +1 VP or a tip. Take a tip early when it has a use; else bank +1 VP."""
        near_end = s["end_turn"] is not None
        can_use_tip = any(True for _ in s["menu"])  # there are dishes to accelerate toward
        if (not near_end) and s["tips"][p] < 2 and can_use_tip:
            return "tip"
        return "vp"

    def _trigger_end(self, s):
        if s["end_turn"] is not None:
            return
        # finish the current round, then one more full round
        n = s["n"]
        turns_done = s["turn"] + 1   # this action's turn increments after; count it as done
        end = ((turns_done + n - 1) // n) * n + n
        s["end_turn"] = end

    def _discard_to_cap(self, s, p, rng):
        larder = s["larder"][p]
        total = sum(larder.values())
        if total <= CAP:
            return
        # discard the least-useful ingredients: prefer dumping what no menu dish needs; pantry last-ish
        menu_need = Counter()
        for d in s["menu"]:
            menu_need |= d["recipe"]
        excess = total - CAP
        # build a discard-priority list (most dumpable first)
        pool = []
        for ing, c in larder.items():
            # usefulness = appears in menu? pantry is generically useful (keep)
            use = menu_need.get(ing, 0) + (2 if ing == PANTRY else 0)
            pool.extend([(use, ing)] * c)
        pool.sort(key=lambda x: x[0])
        for _ in range(excess):
            _, ing = pool.pop(0)
            larder[ing] -= 1
            if larder[ing] <= 0:
                del larder[ing]

    def is_over(self, state):
        return state["done"]

    # ---- scoring ----------------------------------------------------------------------------------
    def scores(self, state):
        out = {}
        for p in range(state["n"]):
            dish_vp = sum(d["vp"] for d in state["log"][p])
            assign = 7 if _assign_complete(state["assignment"][p], state["log"][p]) else 0
            out[p] = dish_vp + assign + state["flat_awarded"][p] + state["bonus_vp"][p]
        return out

    def metrics(self, state):
        sc = self.scores(state)
        vals = sorted(sc.values(), reverse=True)
        margin = vals[0] - vals[1] if len(vals) > 1 else 0.0
        winners = [p for p, v in sc.items() if v == vals[0]]
        tie = 1.0 if len(winners) > 1 else 0.0
        winner = winners[0]
        # payout-C: pick-share of the winner + is a +1-VP pick solely decisive?
        total_picks = sum(len(state["picks"][p]) for p in range(state["n"]))
        win_picks = len(state["picks"][winner])
        win_vp_picks = state["picks"][winner].count("vp")
        pick_share = (win_picks / total_picks) if total_picks else 0.0
        # decisive if removing the winner's +1-VP picks would tie/flip the game
        vp_pick_decisive = 1.0 if (not tie and margin <= win_vp_picks and win_vp_picks > 0) else 0.0
        plates = statistics.mean(len(state["log"][p]) for p in range(state["n"]))
        return {
            "margin": float(margin),
            "tie": tie,
            "deaddrops_per_game": float(state["deaddrops"]),
            "plates_per_player": float(plates),
            "turns": float(state["turn"]),
            "dossier_end": float(state["dossier"]),
            "winner_pick_share": float(pick_share),
            "milestone_picks_total": float(total_picks),
            "vp_pick_decisive": vp_pick_decisive,
            "assign_done_rate": statistics.mean(
                1.0 if _assign_complete(state["assignment"][p], state["log"][p]) else 0.0
                for p in range(state["n"])),
        }


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan"


# ==================================================================================================
#  SHARED "productive brain" — sourcing / plating / routing (used by every strategy)
# ==================================================================================================
def _menu(view):
    return view["menu"]


def _best_target(view, p):
    """The menu dish the player most wants (affordable or not) — the aspiration to route toward.
    Returns ((idx, dish), want) or (None, -1) if the Menu is empty (deck exhausted)."""
    log = view["log"][p]
    a = view["assignment"][p]
    best, bw = None, -1
    for i, d in enumerate(view["menu"]):
        w = _want(d, a, log)
        if w > bw:
            best, bw = (i, d), w
    return best, bw


def _affordable(view, p):
    """List of (menu_index, dish, wilds_needed, want) the player can plate now (wilds<=tips)."""
    larder = view["larder"][p]
    tips = view["tips"][p]
    log = view["log"][p]
    a = view["assignment"][p]
    out = []
    for i, d in enumerate(view["menu"]):
        missing = sum(max(0, c - larder.get(ing, 0)) for ing, c in d["recipe"].items())
        if missing <= tips:
            out.append((i, d, missing, _want(d, a, log)))
    return out


def _productive_action(view, p, legal, rng):
    """Best Plate / Stock / Travel (never Dead-drop / Extract). Greedy, shared by all strategies."""
    larder = view["larder"][p]
    pos = view["pos"][p]
    if not view["menu"]:                 # deck exhausted, nothing left to plate — wind the trip down
        return ("extract",)
    aff = _affordable(view, p)
    (ti, target), tw = _best_target(view, p)

    # 1) Plate if we have a strong affordable dish.
    if aff:
        # prefer plating without wilds; among those, the highest want
        zero = [x for x in aff if x[2] == 0]
        pool = zero if zero else aff
        pool.sort(key=lambda x: (x[3], -x[2]), reverse=True)
        best_i, best_d, best_w, best_want = pool[0]
        # hold only if the aspiration is much better AND close (<=2 missing) — else bank VP now
        target_missing = sum(max(0, c - larder.get(ing, 0)) for ing, c in target["recipe"].items())
        hold = (tw - best_want >= 3.0) and (target_missing <= 2) and (target["name"] != best_d["name"])
        if not hold:
            return ("plate", best_i, best_w)

    # 2) Source toward the aspiration target. What's missing?
    missing = Counter()
    for ing, c in target["recipe"].items():
        short = c - larder.get(ing, 0)
        if short > 0:
            missing[ing] += short
    # generic usefulness: how many *wanted* menu dishes each ingredient could still serve for us
    a = view["assignment"][p]
    log = view["log"][p]
    useful = Counter()
    for d in view["menu"]:
        w = _want(d, a, log)
        for ing, c in d["recipe"].items():
            if larder.get(ing, 0) < c:          # only count toward dishes we don't yet have covered
                useful[ing] += 1

    here = _avail(pos)
    here_missing = [ing for ing in missing if ing in here]

    # Stock Up ONLY if standing where a *missing* target ingredient (or a broadly useful one) sits.
    if here_missing:
        picks = []
        # fill the missing target ingredients we can take here (respect their shortfall)
        for ing in sorted(here_missing, key=lambda i: -missing[i]):
            while len(picks) < 2 and picks.count(ing) < missing[ing]:
                picks.append(ing)
        # top up the 2nd slot with the most generally-useful thing here (a needed specialty > pantry)
        if len(picks) < 2:
            extras = sorted(here, key=lambda i: (-(useful.get(i, 0)), 0 if i != PANTRY else 1))
            for e in extras:
                if len(picks) < 2:
                    picks.append(e)
        return ("stock", pos, tuple(sorted(picks[:2])), 0)

    # 3) Otherwise Travel toward the region that supplies a missing target ingredient.
    if missing:
        best_dest, best_ing, best_score = None, None, -1e9
        for dest in ADJ[pos]:
            da = _avail(dest)
            for ing in da:
                sc = missing.get(ing, 0) * 5 + useful.get(ing, 0)
                if sc > best_score:
                    best_dest, best_ing, best_score = dest, ing, sc
        if best_dest is not None:
            return ("travel", best_dest, best_ing)

    # 4) Target fully covered but no affordable dish (needs a menu refresh / we're flush):
    #    take the most useful thing here, else travel to broaden options.
    if useful and any(i in here for i in useful):
        best = max((i for i in here), key=lambda i: useful.get(i, 0))
        return ("stock", pos, tuple(sorted([best, best if useful.get(best, 0) > 1 else PANTRY])), 0)
    # nothing useful here — hop to a fresh region
    dest = ADJ[pos][0]
    return ("travel", dest, sorted(_avail(dest))[0])


# ---- dead-drop helpers -----------------------------------------------------------------------------
def _surplus_ingredient(view, p):
    """A larder ingredient the player can most spare (not needed for the aspiration target; pantry last).
    Returns ing or None."""
    larder = view["larder"][p]
    if not larder:
        return None
    bt, _ = _best_target(view, p)
    need = bt[1]["recipe"] if bt is not None else Counter()   # empty Menu -> everything is surplus
    # score each held ingredient by how little we need it (higher = more sparable)
    def sparable(ing):
        needed_here = need.get(ing, 0)
        held = larder[ing]
        surplus = held - needed_here
        # pantry is flexible (useful for us) -> less sparable; specialties we overhold -> more sparable
        return surplus - (1 if ing == PANTRY else 0)
    best = max(larder, key=sparable)
    return best if larder[best] > 0 else None


def _recipient_least_useful(view, p, ing):
    """2p/default: the rival who can least use `ing` right now (fewest menu dishes it advances for them)."""
    opps = [q for q in view["log"].keys() if q != p]
    if len(opps) == 1:
        return opps[0]
    def usefulness_to(q):
        larder = view["larder"][q]
        score = 0
        for d in view["menu"]:
            if ing in d["recipe"] and larder.get(ing, 0) < d["recipe"][ing]:
                score += 1
        return score
    return min(opps, key=usefulness_to)


def _would_cross_milestone(view):
    """True if one more Dossier step crosses the next milestone (grab the pick)."""
    nm = view["next_ms"]
    if nm >= len(view["thresholds"]):
        return False
    return view["dossier"] + 1 >= view["thresholds"][nm]


def _jammed(view, p):
    """No zero-wild plate available AND larder near the cap — the classic dead-drop trigger."""
    aff = _affordable(view, p)
    zero = [x for x in aff if x[2] == 0]
    near_cap = sum(view["larder"][p].values()) >= CAP - 1
    return (not zero) and near_cap


# ==================================================================================================
#  STRATEGIES  (differ only in Dead-drop policy + recipient + extract)
# ==================================================================================================
def _maybe_extract(view, p):
    """Extract only when clearly ahead and the game is mature (rarely fires; Dossier usually ends it)."""
    if view["end_turn"] is not None:
        return False
    sc = {q: sum(d["vp"] for d in view["log"][q]) + view["bonus_vp"][q] for q in view["log"]}
    my = sc[p]
    lead = my - max(v for q, v in sc.items() if q != p)
    return view["dossier"] >= view["thresholds"][-1] - 2 and lead >= 4


def s_hoarder(view, p, legal, rng):
    """H: NEVER dead-drops. Hoards; the engine auto-discards surplus over the cap for nothing."""
    if _maybe_extract(view, p):
        return ("extract",)
    return _productive_action(view, p, legal, rng)


def _deaddrop_action(view, p, legal, recipient_policy="least_useful", rng=None):
    ing = _surplus_ingredient(view, p)
    if ing is None:
        return None
    if recipient_policy == "least_useful":
        q = _recipient_least_useful(view, p, ing)
    elif recipient_policy == "leader":
        q = max((x for x in view["log"] if x != p),
                key=lambda x: sum(d["vp"] for d in view["log"][x]) + view["bonus_vp"][x])
    elif recipient_policy == "trailer":
        q = min((x for x in view["log"] if x != p),
                key=lambda x: sum(d["vp"] for d in view["log"][x]) + view["bonus_vp"][x])
    elif recipient_policy == "random":
        opps = [x for x in view["log"] if x != p]
        q = rng.choice(opps)
    else:
        q = _recipient_least_useful(view, p, ing)
    act = ("deaddrop", ing, q)
    return act if act in legal else None


def s_generous(view, p, legal, rng):
    """G: dead-drops surplus aggressively — whenever near the cap with no free plate, OR to grab a
    milestone pick. (Blunt cooperation; the caricature the doc names.)"""
    if _maybe_extract(view, p):
        return ("extract",)
    trigger = _jammed(view, p) or (_would_cross_milestone(view) and
                                   sum(view["larder"][p].values()) >= 2)
    if trigger:
        dd = _deaddrop_action(view, p, legal, "least_useful", rng)
        if dd is not None:
            return dd
    return _productive_action(view, p, legal, rng)


def s_balanced(view, p, legal, rng):
    """Rational line: dead-drop ONLY when truly jammed (a wasted turn otherwise) or when a spare
    ingredient can grab a milestone pick. Otherwise pure productive play."""
    if _maybe_extract(view, p):
        return ("extract",)
    # only tip if productive play this turn would be wasted (jammed) or free milestone pick
    if _jammed(view, p):
        dd = _deaddrop_action(view, p, legal, "least_useful", rng)
        if dd is not None:
            return dd
    if _would_cross_milestone(view):
        # only if we have a genuinely surplus ingredient (larder above what target needs)
        ing = _surplus_ingredient(view, p)
        if ing is not None and sum(view["larder"][p].values()) >= 4:
            dd = _deaddrop_action(view, p, legal, "least_useful", rng)
            if dd is not None:
                return dd
    return _productive_action(view, p, legal, rng)


def s_assignment(view, p, legal, rng):
    """Assignment-focused: same brain (which already weights the Assignment heavily) but never wastes a
    turn tipping unless jammed — a variant baseline to check the +7 hook isn't dominating oddly."""
    if _maybe_extract(view, p):
        return ("extract",)
    if _jammed(view, p):
        dd = _deaddrop_action(view, p, legal, "least_useful", rng)
        if dd is not None:
            return dd
    return _productive_action(view, p, legal, rng)


def s_dossier_greedy(view, p, legal, rng):
    """Dossier-trigger-greedy: races to be the one who crosses milestones (dead-drops to grab picks
    even when not jammed, if it has any sparable ingredient)."""
    if _maybe_extract(view, p):
        return ("extract",)
    if _would_cross_milestone(view):
        dd = _deaddrop_action(view, p, legal, "least_useful", rng)
        if dd is not None:
            return dd
    if _jammed(view, p):
        dd = _deaddrop_action(view, p, legal, "least_useful", rng)
        if dd is not None:
            return dd
    return _productive_action(view, p, legal, rng)


def s_random(view, p, legal, rng):
    """Naive baseline: random legal action. Every real line should crush this."""
    return rng.choice(legal)


STRATEGIES = {
    "random": s_random,
    "hoarder": s_hoarder,           # H
    "generous": s_generous,         # G
    "balanced": s_balanced,         # rational tipper
    "assignment": s_assignment,
    "dossier_greedy": s_dossier_greedy,
}


# ==================================================================================================
#  Custom probes (run in __main__): Q1 head-to-head, Q2 kingmaker (3p), Q3 payout-C
# ==================================================================================================
def _run(agents, n, base_seed=1, n_players=2):
    from importlib import import_module  # noqa
    import statistics as st
    wins = {p: 0 for p in range(n_players)}
    ties = 0
    scores = {p: [] for p in range(n_players)}
    macc = {}
    for i in range(n):
        rng = random.Random(base_seed + i)
        s = GAME.new_state(rng, n_players)
        guard = 0
        while not GAME.is_over(s):
            acts = {}
            for pl in GAME.actors(s):
                acts[pl] = agents[pl](s, pl, GAME.legal_actions(s, pl), rng)
            s = GAME.step(s, acts, rng)
            guard += 1
            if guard > 5000:
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
        "score_mean": {p: st.mean(scores[p]) for p in range(n_players)},
        "metrics": {k: st.mean(v) for k, v in macc.items()},
    }


def q1_head_to_head(n=4000):
    print("== Q1: Hoarder (H) vs Generous-tipper (G), 2p ==")
    r = _run({0: s_hoarder, 1: s_generous}, n)
    r2 = _run({0: s_generous, 1: s_hoarder}, n)   # swap seats
    h = (r["win"][0] + r2["win"][1]) / 2
    g = (r["win"][1] + r2["win"][0]) / 2
    tie = (r["tie"] + r2["tie"]) / 2
    print(f"  H win={h*100:.1f}%   G win={g*100:.1f}%   tie={tie*100:.1f}%   (n={n} each seating)")
    print(f"  score mean  H={ (r['score_mean'][0]+r2['score_mean'][1])/2:.1f}"
          f"   G={ (r['score_mean'][1]+r2['score_mean'][0])/2:.1f}")
    print(f"  deaddrops/game (H-vs-G runs)={r['metrics']['deaddrops_per_game']:.2f}"
          f"   plates/player={r['metrics']['plates_per_player']:.2f}"
          f"   turns={r['metrics']['turns']:.1f}")
    verdict = "PASS (G >= H)" if g >= h - 0.005 else "FAIL (H dominates -> co-op is a trap)"
    print(f"  --> {verdict}\n")
    return g, h, tie


def q2_kingmaker(n=3000):
    print("== Q2: Kingmaker probe, 3p (player 0 varies ONLY its dead-drop recipient) ==")
    # players 1 & 2 always balanced; player 0 = generous tipper with a fixed recipient policy
    def make_p0(policy):
        def agent(view, p, legal, rng):
            if _maybe_extract(view, p):
                return ("extract",)
            if _jammed(view, p) or (_would_cross_milestone(view) and sum(view["larder"][p].values()) >= 2):
                dd = _deaddrop_action(view, p, legal, policy, rng)
                if dd is not None:
                    return dd
            return _productive_action(view, p, legal, rng)
        return agent
    results = {}
    for policy in ("leader", "trailer", "random", "least_useful"):
        r = _run({0: make_p0(policy), 1: s_balanced, 2: s_balanced}, n, n_players=3)
        results[policy] = r
        print(f"  p0 feeds {policy:12} ->  win p1={r['win'][1]*100:4.1f}%  p2={r['win'][2]*100:4.1f}%"
              f"  (p0={r['win'][0]*100:4.1f}%, tie={r['tie']*100:.1f}%)")
    swing1 = abs(results["leader"]["win"][1] - results["trailer"]["win"][1])
    swing2 = abs(results["leader"]["win"][2] - results["trailer"]["win"][2])
    swing = max(swing1, swing2)
    print(f"  max swing in a rival's win-rate between feed-leader vs feed-trailer = {swing*100:.1f}pt")
    verdict = "PASS (targeting barely moves who wins)" if swing < 0.10 else \
              ("SOFT (swing 10-18pt)" if swing < 0.18 else "FAIL (kingmaking: tighten receive cap / tip value)")
    print(f"  --> {verdict}\n")
    return swing


def q3_payout_c(n=4000):
    print("== Q3: Payout-C trigger-share & decisiveness, 2p (balanced mirror + cross) ==")
    for label, agents in (("balanced vs balanced", {0: s_balanced, 1: s_balanced}),
                          ("balanced vs dossier_greedy", {0: s_balanced, 1: s_dossier_greedy})):
        r = _run(agents, n)
        m = r["metrics"]
        print(f"  [{label}]  winner_pick_share={m['winner_pick_share']*100:.1f}%"
              f"  picks/game={m['milestone_picks_total']:.2f}"
              f"  vp_pick_decisive={m['vp_pick_decisive']*100:.1f}%"
              f"  margin={m['margin']:.1f}")
    # fair share of picks for the winner at 2p with 4 milestones is ~50%
    r = _run({0: s_balanced, 1: s_balanced}, n)
    share = r["metrics"]["winner_pick_share"]
    dec = r["metrics"]["vp_pick_decisive"]
    verdict = ("PASS (picks spread ~fair, rarely solely decisive)"
               if share < 0.70 and dec < 0.15 else
               "WATCH (winner sweeps picks or +1VP often decisive -> cap picks / drop +1VP option)")
    print(f"  --> {verdict}\n")
    return share, dec


if __name__ == "__main__":
    print(f"[knobs] CAP={CAP}  TIP_TEMPO={TIP_TEMPO}  DEADDROP_VP={DEADDROP_VP}\n")
    q1_head_to_head(n=3000)
    q2_kingmaker(n=2000)
    q3_payout_c(n=3000)
