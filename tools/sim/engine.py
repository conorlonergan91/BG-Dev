"""
engine.py — a tiny, stdlib-only simulation harness for board game prototypes.

The point: let `bg-playtest` (or you) encode a game's rules once, then play it thousands of times with
different strategies to expose dominant lines, balance problems, score spreads, and how often a given
subsystem (a bonus, a catch-up rule) actually decides the game — *before* spending human playtests.

A **Game** is any object implementing (duck-typed):
    new_state(rng)                  -> state           # deal/shuffle using the given random.Random
    players(state)                  -> list[player]    # usually [0, 1]
    actors(state)                   -> list[player]    # who must act now; >1 == simultaneous
    legal_actions(state, player)    -> list[action]
    view(state, player)             -> state           # optional; hide hidden info (default: identity)
    step(state, actions, rng)       -> state           # actions: {player: action}; return NEW state
    is_over(state)                  -> bool
    scores(state)                   -> {player: float}
    metrics(state)                  -> {str: float}    # optional per-game diagnostics

An **agent** is a callable: agent(view, player, legal_actions, rng) -> action.

Determinism: everything flows from the seed, so results are reproducible and diffable.
"""
from __future__ import annotations

import random
import statistics


def random_agent(view, player, legal, rng):
    """Baseline: pick uniformly at random. Every game should beat this."""
    return rng.choice(legal)


def run_match(game, agents, seed):
    """Play one match. `agents` is {player: callable}. Returns (scores, metrics)."""
    rng = random.Random(seed)
    state = game.new_state(rng)
    guard = 0
    while not game.is_over(state):
        actions = {}
        for p in game.actors(state):
            v = game.view(state, p) if hasattr(game, "view") else state
            actions[p] = agents[p](v, p, game.legal_actions(state, p), rng)
        state = game.step(state, actions, rng)
        guard += 1
        if guard > 100_000:
            raise RuntimeError("match did not terminate (check is_over/step)")
    metrics = game.metrics(state) if hasattr(game, "metrics") else {}
    return game.scores(state), metrics


def play_series(game, agents, n=2000, base_seed=1):
    """Play n matches with a fixed {player: agent} assignment. Aggregate the outcome."""
    players = None
    wins = {}
    scores = {}
    ties = 0
    metric_acc = {}
    for i in range(n):
        sc, mt = run_match(game, agents, base_seed + i)
        if players is None:
            players = list(sc.keys())
            wins = {p: 0 for p in players}
            scores = {p: [] for p in players}
        best = max(sc.values())
        winners = [p for p, v in sc.items() if v == best]
        if len(winners) == 1:
            wins[winners[0]] += 1
        else:
            ties += 1
        for p in players:
            scores[p].append(sc[p])
        for k, v in mt.items():
            metric_acc.setdefault(k, []).append(v)
    return {
        "n": n,
        "players": players,
        "win_rate": {p: wins[p] / n for p in players},
        "tie_rate": ties / n,
        "score_mean": {p: statistics.mean(scores[p]) for p in players},
        "score_stdev": {p: (statistics.pstdev(scores[p]) if n > 1 else 0.0) for p in players},
        "score_min": {p: min(scores[p]) for p in players},
        "score_max": {p: max(scores[p]) for p in players},
        "metrics": {k: statistics.mean(v) for k, v in metric_acc.items()},
    }


class _AtCount:
    """Wrap a game so play_series runs it at a fixed player count. The game's new_state must accept an
    optional player count: new_state(rng, n_players). Games with a fixed count don't support this."""
    def __init__(self, game, n):
        self._g, self._n = game, n
    def new_state(self, rng):
        return self._g.new_state(rng, self._n)
    def __getattr__(self, k):
        return getattr(self._g, k)


def seat_balance(game, agent, n_players, n=1500, base_seed=1):
    """Self-play mirror at a given count: is any seat/turn-order winning more than its fair share?
    A fair game → each of the n_players seats wins ~1/n_players. Requires new_state(rng, n_players)."""
    res = play_series(_AtCount(game, n_players), {p: agent for p in range(n_players)},
                      n=n, base_seed=base_seed)
    wr = res["win_rate"]
    fair = 1.0 / n_players
    return {
        "n_players": n_players,
        "seat_win_rate": wr,
        "tie_rate": res["tie_rate"],
        "score_mean": res["score_mean"],
        "fair_share": fair,
        # heuristic: a seat winning ≥1.5× or ≤0.5× its fair share is a balance smell
        "suspect": max(wr.values()) > fair * 1.5 or min(wr.values()) < fair * 0.5,
    }


def per_count(game, agent, counts, n=1500, base_seed=1):
    """Run seat_balance at each player count. Games that don't parametrise count report that clearly."""
    out, seed = {}, base_seed
    for c in counts:
        try:
            out[c] = seat_balance(game, agent, c, n=n, base_seed=seed)
        except TypeError:
            out[c] = {"n_players": c, "error": "game.new_state(rng, n_players) not supported — "
                      "this game has a fixed player count and can't be tested at other counts."}
        seed += n
    return out


def round_robin(game, strategies, n=1000, base_seed=1):
    """
    Two-player strategy tournament. `strategies` = {name: agent}. Plays every ordered pair
    (including a strategy against itself and both seatings) so first-player advantage is averaged out.
    Returns per-strategy win rate + a matchup grid + averaged game metrics.
    """
    names = list(strategies)
    played = {a: 0 for a in names}
    won = {a: 0.0 for a in names}          # ties count as 0.5 to each
    grid = {a: {b: None for b in names} for a in names}  # grid[a][b] = a's win rate as P0 vs b as P1
    metric_acc = {}
    seed = base_seed
    for a in names:
        for b in names:
            res = play_series(game, {0: strategies[a], 1: strategies[b]}, n=n, base_seed=seed)
            seed += n
            wa = res["win_rate"][0] + 0.5 * res["tie_rate"]
            grid[a][b] = wa
            played[a] += 1; won[a] += wa
            played[b] += 1; won[b] += (1 - wa)  # b's share as P1
            for k, v in res["metrics"].items():
                metric_acc.setdefault(k, []).append(v)
    overall = {a: won[a] / played[a] for a in names}
    return {
        "n_per_matchup": n,
        "strategies": names,
        "overall_win_rate": dict(sorted(overall.items(), key=lambda kv: -kv[1])),
        "matchup_grid": grid,   # grid[row as P0][col as P1] = row's win rate
        "metrics": {k: statistics.mean(v) for k, v in metric_acc.items()},
    }


def _is_naive(name):
    n = name.lower()
    return n.startswith("random") or n.startswith("always") or n in ("min", "max", "first")


def health_read(res):
    """Turn a round-robin into balance signals (the reusable lessons from playtesting).
    See knowledge/simulation-and-balance.md for how to read these."""
    names = res["strategies"]
    grid = res["matchup_grid"]
    if len(names) < 2:
        return ["(need ≥2 strategies for a health read)"]
    # head-to-head win rate, averaged over both seatings
    def h2h(a, b):
        return (grid[a][b] + (1 - grid[b][a])) / 2
    # Condorcet winner = a strategy that beats every other head-to-head
    condorcet = [a for a in names if all(h2h(a, b) > 0.5 for b in names if b != a)]
    # intransitive triple (rock-paper-scissors)?
    intransitive = any(h2h(a, b) > 0.5 and h2h(b, c) > 0.5 and h2h(c, a) > 0.5
                       for a in names for b in names for c in names
                       if len({a, b, c}) == 3)
    top = max(res["overall_win_rate"], key=res["overall_win_rate"].get)
    top_wr = res["overall_win_rate"][top]
    out = []
    if condorcet:
        c = condorcet[0]
        worst = min(h2h(c, b) for b in names if b != c)
        if _is_naive(c):
            out.append(f"⚠ a **naive** line (`{c}`) beats the whole field (worst h2h {worst*100:.0f}%) "
                       f"— the interesting decisions may not matter yet. Tune, then re-sim.")
        elif worst > 0.60:
            out.append(f"⚠ **possible dominant strategy**: `{c}` beats every other line "
                       f"(worst h2h {worst*100:.0f}%). Check it isn't a memorizable one-liner before shipping.")
        else:
            out.append(f"~ mild edge to `{c}` (beats all, but by ≤{ (worst-0.5)*100:.0f}pt margins) — "
                       f"no crushing dominance.")
    if intransitive and not condorcet:
        out.append("✓ **no single dominant line** — strategies are intransitive "
                   "(rock-paper-scissors). A good depth signal.")
    elif intransitive:
        out.append("• intransitivity present among some lines (a depth signal), alongside the note above.")
    if not _is_naive(top) and top_wr < 0.60:
        out.append(f"✓ the field leader `{top}` ({top_wr*100:.0f}%) is a rule-aware line, not a naive "
                   "baseline — skill is being rewarded.")
    out.append("Reminder: identical **deterministic** strategies always mirror-tie in a simultaneous "
               "game — that's an artifact, not shallowness. Read depth from *cross-strategy* results and "
               "whether the optimal line actually uses the signature mechanic (probe with --matchup).")
    return out


def format_round_robin(res, title="Simulation report"):
    lines = [f"# {title}", "",
             f"{res['n_per_matchup']} games per matchup; win rate averages both seatings "
             f"(ties = 0.5).", "", "## Overall win rate by strategy"]
    for name, wr in res["overall_win_rate"].items():
        bar = "█" * round(wr * 30)
        lines.append(f"- **{name:16}** {wr*100:5.1f}%  {bar}")
    names = res["strategies"]
    lines += ["", "## Matchup grid (row as P0 vs column as P1 — row's win rate)", "",
              "| P0 \\ P1 | " + " | ".join(f"{n[:10]}" for n in names) + " |",
              "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = " | ".join(f"{res['matchup_grid'][a][b]*100:4.0f}%" for b in names)
        lines.append(f"| {a[:10]} | {row} |")
    if res["metrics"]:
        lines += ["", "## Averaged game metrics"]
        for k, v in res["metrics"].items():
            lines.append(f"- {k}: {v:.3f}")
    lines += ["", "## Health read"] + [f"- {s}" for s in health_read(res)]
    return "\n".join(lines)
