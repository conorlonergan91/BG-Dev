#!/usr/bin/env python3
"""agent_watch.py — a one-call liveness / progress digest for background subagents.

WHY THIS EXISTS
---------------
The harness already fires a `<task-notification>` when a background agent
*completes*, so this tool is NOT for learning that an agent finished. It is for the
two things the harness does not give you for free while an agent is still running:

  1. HANG DETECTION  — is a running agent still making progress, or wedged?
  2. A PROGRESS PEEK — "where is it at right now?" WITHOUT reading the agent's
     `.output` file, which is the full JSONL transcript and overflows the
     orchestrator's context window.

It never reads transcript CONTENTS. It only *stats* the `.output` file (mtime +
size) and looks at what the agent is doing to the repository (recently-touched
files, git state). Signals, most trustworthy first:

    repo file mtimes  >  .output mtime  >  process list (advisory)

HONEST LIMIT: the filesystem alone cannot tell "finished cleanly" from "hung" —
both look like a `.output` that stopped growing. A QUIET verdict means exactly
that: no writes lately, so it either finished or wedged. Disambiguate with the
orchestrator's `ListAgents` (running vs done) — this tool says so in its output.

USAGE
-----
    python tools/agents/agent_watch.py --all
    python tools/agents/agent_watch.py --task af466da1df9f2a08e
    python tools/agents/agent_watch.py --all --stale-min 15 --repo /home/user/BG-Dev

Stdlib-only. Exit code 0 always (it is a reporting tool, not a gate).
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

# Directories that are noise for "what did the agent just touch" — build scratch,
# caches, vendored deps, and the git dir itself.
SKIP_DIRS = {".git", "build", "__pycache__", "node_modules", ".venv", ".mypy_cache"}


def _fmt_age(seconds: float) -> str:
    """Human age: '12s', '4m', '1h3m'."""
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m{s:02d}s" if s else f"{m}m"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m"


def _discover_tasks_dir() -> Path | None:
    """Find the newest harness `tasks/` dir under /tmp/claude-* by most-recent .output."""
    candidates: list[tuple[float, Path]] = []
    # The harness nests tasks dirs a variable depth under /tmp/claude-* (e.g.
    # /tmp/claude-0/-home-user-<repo>/<session-uuid>/tasks), so match recursively.
    seen: set[str] = set()
    for base in glob.glob("/tmp/claude-*"):
        for match in glob.glob(os.path.join(base, "**", "tasks"), recursive=True):
            tasks_dir = Path(match)
            if not tasks_dir.is_dir() or match in seen:
                continue
            seen.add(match)
            outs = list(tasks_dir.glob("*.output"))
            if outs:
                newest = max(o.stat().st_mtime for o in outs)
                candidates.append((newest, tasks_dir))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def _recently_touched(repo: Path, stale_min: float, limit: int = 12) -> list[tuple[float, str]]:
    """Files under `repo` modified within `stale_min` minutes, newest first.

    This is the truest 'is the agent actively working' signal — an agent writing
    files leaves fresh mtimes even when its .output flushes only on completion.
    """
    cutoff = time.time() - stale_min * 60
    hits: list[tuple[float, str]] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            p = Path(root) / name
            try:
                mt = p.stat().st_mtime
            except OSError:
                continue
            if mt >= cutoff:
                hits.append((mt, os.path.relpath(p, repo)))
    hits.sort(reverse=True)
    return hits[:limit]


def _git(repo: Path, *args: str) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=20,
        )
        return (out.stdout or out.stderr).strip()
    except Exception as e:  # pragma: no cover - defensive
        return f"(git error: {e})"


def _ps_claude() -> list[str]:
    """Best-effort process peek (advisory only — subagents may be in-process)."""
    try:
        out = subprocess.run(["ps", "-eo", "pid,etime,pcpu,comm"],
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    return [ln for ln in out.splitlines()
            if ("claude" in ln.lower() or "node" in ln.lower()) and "agent_watch" not in ln]


def _report_task(out_file: Path, stale_min: float) -> str:
    now = time.time()
    try:
        st = out_file.stat()
    except OSError:
        return f"  {out_file.name}: (no .output file)"
    age = now - st.st_mtime
    fresh = age < stale_min * 60
    verdict = "ALIVE (emitting)" if fresh else f"QUIET (>{int(stale_min)}m — finished or hung; check ListAgents)"
    return (f"  task {out_file.stem}\n"
            f"    .output: {st.st_size}B · last write {_fmt_age(age)} ago · {verdict}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="One-call liveness/progress digest for background subagents.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--task", help="A single task id (the .output basename) to report on.")
    g.add_argument("--all", action="store_true", help="Report on every task .output in the tasks dir.")
    ap.add_argument("--tasks-dir", help="Override the harness tasks/ dir (auto-discovered otherwise).")
    ap.add_argument("--repo", default=os.getcwd(), help="Repo root for git + touched-file signals (default: cwd).")
    ap.add_argument("--stale-min", type=float, default=10.0,
                    help="Minutes of no writes before an agent is flagged QUIET (default: 10).")
    ap.add_argument("--no-ps", action="store_true", help="Skip the advisory process peek.")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    now = time.time()

    print("=" * 68)
    print(f"agent_watch · {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(now))}Z · repo {repo.name}")
    print("=" * 68)

    # --- Agent .output liveness -------------------------------------------------
    tasks_dir = Path(args.tasks_dir) if args.tasks_dir else _discover_tasks_dir()
    print("\n[agents] (.output mtime — never reads transcript contents)")
    if not tasks_dir or not tasks_dir.exists():
        print("  (no tasks dir found)")
    else:
        print(f"  tasks dir: {tasks_dir}")
        if args.task:
            outs = [tasks_dir / f"{args.task}.output"]
        else:
            outs = sorted(tasks_dir.glob("*.output"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not outs:
            print("  (no .output files)")
        for o in outs:
            print(_report_task(o, args.stale_min))

    # --- Repo activity (the truest progress signal) -----------------------------
    print(f"\n[repo activity] files touched in the last {int(args.stale_min)}m:")
    touched = _recently_touched(repo, args.stale_min)
    if not touched:
        print("  (none — no agent is actively writing files right now)")
    else:
        for mt, rel in touched:
            print(f"  {_fmt_age(now - mt):>7} ago  {rel}")

    # --- Git state --------------------------------------------------------------
    print("\n[git status]")
    status = _git(repo, "status", "--porcelain")
    print("  clean working tree" if not status else "\n".join("  " + ln for ln in status.splitlines()))
    print("\n[git log -3]")
    print("\n".join("  " + ln for ln in _git(repo, "log", "--oneline", "-3").splitlines()))

    # --- Advisory process peek --------------------------------------------------
    if not args.no_ps:
        ps = _ps_claude()
        if ps:
            print("\n[ps] (advisory — subagents may be in-process, not separate PIDs)")
            for ln in ps[:6]:
                print("  " + ln.strip())

    print("\n" + "-" * 68)
    print("verdict key: ALIVE = writing recently · QUIET = idle >stale-min (finished")
    print("OR hung — ListAgents disambiguates). Repo-file mtimes are more trustworthy")
    print("than .output mtime, which flushes lazily for local subagents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
