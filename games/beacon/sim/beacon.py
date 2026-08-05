"""
beacon.py — Beacon encoded for the simulation harness (see tools/sim/engine.py).

Implements the first-pass rules in ../design/design-doc.md so we can pressure-test the open questions
before human playtesting:
  Q1  Is a fixed signal policy (e.g. always play your highest) dominant?
  Q2  How swingy is it — what's the score spread and win-margin?
  Q3  How often does the Tide bonus actually decide the game?

Ship-picking is handled by a shared greedy heuristic so the *only* thing that differs between
strategies is the signal policy — isolating Q1. Run it with:
    python tools/sim/simulate.py --module games/beacon/sim/beacon.py --n 3000
"""
from __future__ import annotations

import copy

SUITS = ("C", "P", "N")            # Cargo, Passenger, Naval
NIGHTS = 3
ROUNDS_PER_NIGHT = 4
CHANNEL = 2


def _new_deck():
    deck = []
    for s in SUITS:
        for v in (1, 1, 2, 2, 3, 3, 4, 4):
            deck.append((s, v))
    return deck


def _suit_counts(harbor):
    c = {s: 0 for s in SUITS}
    for s, _v in harbor:
        c[s] += 1
    return c


def _pick(harbor, options):
    """Greedy: take the most valuable ship; tie-break toward the suit you have fewest of (convoys)."""
    counts = _suit_counts(harbor)
    best = max(options, key=lambda sh: (sh[1] * 10) + (3 - counts[sh[0]]))
    other = [o for o in options if o is not best]
    return best, (other[0] if other else None)


def _score_ships(harbor):
    base = sum(v for _s, v in harbor)
    counts = _suit_counts(harbor)
    convoys = min(counts[s] for s in SUITS)          # complete {C,P,N} sets
    runs = 0
    for s in SUITS:
        vals = {v for (ss, v) in harbor if ss == s}
        for lo in (1, 2):                             # windows {1,2,3},{2,3,4}
            if {lo, lo + 1, lo + 2} <= vals:
                runs += 1
    return base + 2 * convoys + 2 * runs


class BeaconGame:
    def new_state(self, rng):
        deck = _new_deck()
        rng.shuffle(deck)
        night_decks = [deck[i * 8:(i + 1) * 8] for i in range(NIGHTS)]
        nd0 = night_decks[0]
        channel = [nd0.pop() for _ in range(CHANNEL)]
        return {
            "night_decks": night_decks,
            "night": 0,
            "channel": channel,
            "hands": {0: [0, 1, 2, 3, 4, 5], 1: [0, 1, 2, 3, 4, 5]},
            "played": {0: 0, 1: 0},
            "harbor": {0: [], 1: []},
            "tide": 0,                # + toward player 1, - toward player 0
            "first_keeper": rng.randint(0, 1),
            "tide_bonus": {0: 0, 1: 0},
            "round_in_night": 0,
            "done": False,
        }

    def players(self, state):
        return [0, 1]

    def actors(self, state):
        return [0, 1]                 # simultaneous signal selection

    def legal_actions(self, state, player):
        return sorted(set(state["hands"][player]))

    def step(self, state, actions, rng):
        s = copy.deepcopy(state)
        a0, a1 = actions[0], actions[1]
        s["hands"][0].remove(a0); s["hands"][1].remove(a1)
        s["played"][0] += 1; s["played"][1] += 1

        if a0 == a1:                                  # tie: no tide move, first keeper picks first
            fk = s["first_keeper"]
            pick, other = _pick(s["harbor"][fk], s["channel"])
            s["harbor"][fk].append(pick)
            s["harbor"][1 - fk].append(other)
        else:
            winner = 0 if a0 > a1 else 1
            s["tide"] = max(-3, min(3, s["tide"] + (1 if winner == 1 else -1)))
            pick, other = _pick(s["harbor"][winner], s["channel"])
            s["harbor"][winner].append(pick)
            s["harbor"][1 - winner].append(other)

        # refill channel from this night's deck
        s["channel"] = []
        nd = s["night_decks"][s["night"]]
        while len(s["channel"]) < CHANNEL and nd:
            s["channel"].append(nd.pop())

        s["round_in_night"] += 1
        if s["round_in_night"] >= ROUNDS_PER_NIGHT:
            # Tide bonus
            if s["tide"] > 0:
                s["tide_bonus"][1] += 3
            elif s["tide"] < 0:
                s["tide_bonus"][0] += 3
            # "The tide turns": the Tide loser becomes first keeper (fewer ships if centred)
            if s["tide"] > 0:
                s["first_keeper"] = 0
            elif s["tide"] < 0:
                s["first_keeper"] = 1
            else:
                n0, n1 = len(s["harbor"][0]), len(s["harbor"][1])
                if n0 != n1:
                    s["first_keeper"] = 0 if n0 < n1 else 1
            s["tide"] = 0
            s["hands"] = {0: [0, 1, 2, 3, 4, 5], 1: [0, 1, 2, 3, 4, 5]}
            s["played"] = {0: 0, 1: 0}
            s["round_in_night"] = 0
            s["night"] += 1
            if s["night"] >= NIGHTS:
                s["done"] = True
            else:
                nd = s["night_decks"][s["night"]]
                s["channel"] = [nd.pop() for _ in range(CHANNEL)]
        return s

    def is_over(self, state):
        return state["done"]

    def scores(self, state):
        return {p: _score_ships(state["harbor"][p]) + state["tide_bonus"][p] for p in (0, 1)}

    def metrics(self, state):
        base = {p: _score_ships(state["harbor"][p]) for p in (0, 1)}
        full = self.scores(state)
        winner_full = 0 if full[0] > full[1] else (1 if full[1] > full[0] else -1)
        winner_base = 0 if base[0] > base[1] else (1 if base[1] > base[0] else -1)
        return {
            "margin": abs(full[0] - full[1]),
            "tie": 1.0 if winner_full == -1 else 0.0,
            "tide_points_total": state["tide_bonus"][0] + state["tide_bonus"][1],
            "tide_decisive": 1.0 if winner_full != winner_base else 0.0,
        }


GAME = BeaconGame()
TITLE = "Beacon"

# --- strategies (signal policy only; ship-picking is the shared greedy heuristic) ---
def s_random(view, p, legal, rng):
    return rng.choice(legal)

def s_always_high(view, p, legal, rng):
    return max(legal)

def s_always_low(view, p, legal, rng):
    return min(legal)

def s_hoarder(view, p, legal, rng):
    # save big signals for later in the night
    return min(legal) if view["played"][p] < 2 else max(legal)

def s_reactive(view, p, legal, rng):
    # spend a big signal only when a valuable ship (>=3) is on offer
    top = max((v for _s, v in view["channel"]), default=0)
    return max(legal) if top >= 3 else min(legal)

STRATEGIES = {
    "random": s_random,
    "always_high": s_always_high,
    "always_low": s_always_low,
    "hoarder": s_hoarder,
    "reactive": s_reactive,
}
