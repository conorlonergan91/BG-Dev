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
    return "\n".join(lines)
