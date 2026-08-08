"""
travel_agents.py — Travel Agents: Taiwan (v6.3.1 · four CD reworks on top of the tickets-only lock)
encoded for the simulation harness (see tools/sim/engine.py). Stdlib-only.

------------------------------------------------------------------------------------------------------
v6.3.1 — THE FOUR CD CHANGES (2026-08-08 re-sim; folds ON TOP of the tickets-only lock)
------------------------------------------------------------------------------------------------------
Canon: design/v6.3-content-draft.md "v6.3 → v6.3.1 — FOUR CD CHANGES". All four change the economy, so
they are validated TOGETHER in this gated re-sim. The tickets-only lock (SCORING=tickets_only, expanded
44-ticket deck, MS_MODE=perplayer) + the whole Reach economy are held FIXED (all prior-validated).

  CD-1  里長伯 (councillor) home-region rework (TA_COUNCILLOR_KIT=home, default). He picks ONE home
        region at setup; Old Favours −1 ingredient applies ONLY in his home region (floored at 0), and a
        +1 AWAY TAX (one chosen type — the vendor's local signature, cheapest-to-add since he must stand
        there) hits every Bribe OUTSIDE home. The old first-N-regions discount lives behind KIT=regions.
        The councillor NO-HSR restriction is REMOVED (re-homed as CD-2) — he uses HSR like everyone.
  CD-2  "Scheduled Maintenance" (排班保養) — a TABLE-WIDE, PERSISTENT event (NOT a ⦿/⬢/➤ scope). Seeded
        (TA_MAINT_COUNT copies, default 1) in a NIGHT ingredient deck of an HSR endpoint (TA_MAINT_REGION,
        default N). Fires on a Visit / Convenience-Store flip (whiffs on Travel, like any event). While
        active the HSR N↔S hop is CLOSED for ALL players until the start of the drawing player's next turn
        (one full go-around), then reopens. Tracked as s["hsr_closed_until_turn"].
  CD-3  Common Taipei start (TA_START_SPLIT=0, default). ALL players start in N (Taipei/North hub) at
        every count. The old split ({2:[N,S],...}) is behind TA_START_SPLIT=1 for the seat-balance A/B.
  CD-4  Night-cost escalation (TA_NIGHT_CURVE graded 0/1/2, default 1=SOFT). DAY vendors stay as-printed;
        the re-sim landed on the SOFT curve (a +1 escalation: NIGHT "both" foods → 3, apex ★ → 4, top apex
        5 — every night marquee CROSS-REGION biased). Soft keeps night sourcing alive (~113% of day) and
        cuts free night bribes 1.73→0.95 (each remaining free bribe now needs a genuine DUAL-region ramp =
        a legitimate deep-engine reward, not the single-region zero-out exploit) at a modest 2%→6% stall.
        The STEEP curve (2) meets the "≥2 residual" principle literally but pushes ~16% of games past the
        last-train into the stall backstop — REJECTED. Backstop TA_MIN1_FLOOR (default OFF) drives free
        bribes to 0 but adds a rule + stall for little gain — NOT needed (probe #1 verdict).

  ★ PROBE #1 (the load-bearing one): day/night SOURCING split (Visit+CStore+Travel per turn). Reported as
  the night-half rate as a FRACTION of the day-half rate. FAIL = night collapses ~0 (sourcing trivialised).
  GOAL = night stays ~60–100% of day. Over-correction watch = night marquees unaffordable (night claims
  thin / clock stalls / game drags) — probe night claims/player + turns-to-first-night-Bribe.

vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
(v6.3 lineage below — unchanged shape carried forward)

This reworks the v6.2 sim (region vendor markets + a vendor-claims clock + Prestige/Rep-VP scoring + perks)
to the v6.3 SHAPE-LOCK spec in design/v6.3-content-draft.md. v6.3 gives the Reputation track TEETH and
strips the perk/ticket-pool cruft. The board, dusk flip, 5-ingredient palette, the vendor-claims clock,
the push-your-luck market decks with scoped events, and the five characters all carry over from v6.2.

WHAT v6.3 MOVED — and what this rework implements (vs the v6.2 sim):

  (1) REPUTATION → "REACH": a LIVE CAP on committed Buzz. Your total Buzz committed across the board may
      never exceed your current Reach. Winning a vendor clears your Buzz off it → frees the cap.
      - START Reach = 2 (knob), track 0–12.
      - SOURCES: Travel = +1 Reach; ~3–4 event cards = +1 Reach; vendors grant NO Reach.
      - SINKS: a "Greedy Grab" (keep +1 on a Visit OR take a 2nd card on a Convenience Store) → −1 Reach;
        plus ~2–3 Reach-cost events (−1).
      - EDGE CASE: a voluntary Greedy Grab is legal only if it won't drop Reach below committed Buzz; a
        forced event loss that breaches the cap makes the player immediately return Buzz to supply until
        legal. Reach floors at 0.
      - Reach NO LONGER SCORES (the 3/6/9/top VP table is DELETED).

  (2) RAVE-REVIEW MILESTONES on the Bookings track: marks at Bookings 7 and 14, Set A "Tempo & Fuel"
      (Mark 7 → +1 Reach; Mark 14 → take 1 ingredient of choice + next Bribe costs 1 less). FIRST player
      to cross each gets the one-time boon.

  (3) PERKS ELIMINATED. A vendor = Bookings value + (region icon | no icon). No perk field, no Rep value.
      Vendor set = the reissued v6.3 table, PLUS the central-tea-export fix (see CENTRAL_TEA_FIX below):
      北 牛肉麵 (Beef Noodle) is re-pointed from →S to →C so Central tea has cross-region export demand and
      the cross-region cycle closes into a true four-region loop (N→C→S→E→N). This matches v6.2's validated
      movement fix; bg-design flagged it isn't in the v6.3 table text yet — surfaced for bg-developer.

  (4) TICKET POOLS 3→2 (DAY / NIGHT). General folded in per the spec (遍地開花 → both, 收藏家 & 揮金如土 →
      night). DAY tickets judged at DUSK into the win/lose piles; NIGHT tickets at the last train.

  (5) PER-PLAYER WIN/LOSE piles (成團 / 遺珠) — already how the v6.2 sim scored; made explicit here.

Scoring = TWO vectors: Bookings (live vendor-value track) + Tour Tickets (Σ win-pile − Σ floor(v/2)
lose-pile). Tiebreak (folded as a tiny fractional term so the harness picks the right winner): most
vendors → most regions → fewest lose-pile tickets.

------------------------------------------------------------------------------------------------------
DESIGN FIDELITY / SIMPLIFICATIONS (bots are a FLOOR on depth, not a ceiling)
------------------------------------------------------------------------------------------------------
Faithfully modelled: the 4-region ring + HSR(N↔S); the five actions; the 5-ingredient palette + common in
C&S; per-region day/night vendor decks with 2/1/1/1 face-up + refill + the dusk sweep; the conserved
per-region ingredient pool with renewable over-cap discard; Visit-3-keep-2 (+Greedy Grab) and Convenience-
Store single draw (+Greedy Grab) firing events by scope; Travel drawing the arriving region (whiffs) AND
granting +1 Reach; the Buzz-majority Bribe (≥margin lead, presence, pay ingredients − icon discounts)
clearing to supply; the discount ramp (food only); the ★ dynamic accolade; the Reach cap on Promote +
its forced-return edge case; the two milestone marks; Tour Tickets judged per-phase into win/lose piles;
the five v6.3-locked characters.

Simplifications (the sim's blind spots — hand these to the table):
  * SHARED "engine brain": every strategy scores legal actions with ONE greedy planner; strategies differ
    only in PREFS. Isolates the playstyle questions exactly as beacon.py isolates policy.
  * Event PAYLOADS abstracted: hazard = a bounded tempo tax OR a −1 Reach ding; boon = a free ingredient,
    a +1 Reach boon, or (a fraction) the dynamic ★. Warmth of rival-facing beats is the feel-test's job.
  * The Buzz war is resolved by a concession heuristic → bots rarely pile on the same vendor (contested
    rate is a FLOOR); the fight's fun/tension is a table question, not a sim one.
  * The Greedy Grab is taken only when the bot has comfortable Reach headroom (it never starves its own
    fight) — so the measured grab-rate is a conservative floor; a human grabs more aggressively.
  * 網紅's "Late to the Party" (miss the first NIGHT turn) is modelled exactly (a forced pass); "goes
    last" is only a seat tiebreak (mild for greedy bots). ASSUMPTIONS tagged `# ASSUMPTION:`.

(end v6.3 lineage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run:
    python tools/sim/simulate.py --module games/travel-agents/sim/travel_agents.py --n 3000 \
        --out games/travel-agents/playtests/sim-results.md
    python games/travel-agents/sim/travel_agents.py            # the full v6.3.1 probe suite
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
# >>> TICKETS-ONLY LOCK (CD-signed-off, 2026-08-07) — the defaults below now RUN the CD-locked shape:
#     SCORING=tickets_only · TICKETS=expanded · MS_MODE=perplayer
# (vendors stop scoring → they're pure engine + ticket-enablers = the "Draw" attribute; richer ticket
#  deck; the Rave-Review milestone boon spreads to EACH player so it can't pump the leader.) This was the
# v6.3-FIX recommendation (option A); it is now the run default. To recover the old v6.3 shape-lock for an
# A/B: TA_SCORING=both TA_TICKETS=base TA_MS_MODE=first.
#
# >>> v6.3 CHARACTER RE-PASS (2026-08-07) — the balance follow-on to the tickets-only lock. Under
# tickets-only, two kits drifted (playtests/sim-notes.md §v6.3 CHARACTER RE-PASS): 網紅 COLD (~39%) and
# 里長伯 HOT (~62%). Tuned ONE kit at a time, re-simmed to confirm. The re-pass defaults below:
#   * 網紅 influencer: "Late to the Party" flaw RETIRED (INFL_FLAW=none) → 49% (was 39%). The Reach cap
#     already throttles Promote-3 early, so the lost-turn flaw was redundant double-punishment.
#   * 里長伯 councillor: Old-Favours discount now covers your FIRST region only (COUNCILLOR_REGIONS=1,
#     was 2) → 56% (was 62%). Keeps the "regular's discount in your home patch" hook; drops the sprawl.
#     56% is ~top-of-band in-sim; the sim UNDER-counts his no-HSR flaw (a 4-region ring barely feels it),
#     so a real table sits lower. CD option B for a dead-centre in-sim landing (~51%): also start him at
#     Reach 1 (TA_COUNCILLOR_REACH=1) — "deep local favours, but his name doesn't carry across the island".
#   * 大哥 (49%) · 大胃王 (53%) · 媽寶 (42%) held ~in band as the other two were tuned (media/office kit
#     UNCHANGED). 媽寶's 42% is a tickets-only drift, not caused by this pass — its Travel-flexibility
#     ability is a documented greedy-bot blind spot, so 42% is a floor; carried to FTUE as a watch-flag.
#   * Draw bands (the vendor-value attribute) left AS-IS: the dead-vendor scan found no dead buys — every
#     Draw tier sees play (cheap Draw-1 stalls are heavily claimed as ramp/ticket-enablers) and the ★ apex
#     (Draw 8) stays the standout. The cold cards are the intentionally-cheap drinks + the known East/
#     Central under-pull (a bg-developer data question), not a Draw-value miscalibration.
BUZZ_SUPPLY  = int(os.environ.get("TA_BUZZ_SUPPLY", "24"))     # 2p Buzz supply (+~9/extra player)
BUZZ_MARGIN  = int(os.environ.get("TA_BUZZ_MARGIN", "2"))      # ≥N Buzz lead to Bribe (design 2)

# --- v6.3.1 CD-4 NIGHT-COST ESCALATION (the LOTR:Duel model) -------------------------------------
# NIGHT_CURVE is a GRADED level (the re-sim found the steep curve over-corrects → clock stalls):
#   0 = OFF (raw v6.3 night costs — "both" 2–3, apex 3, for the A/B floor);
#   1 = SOFT (default) — a +1 escalation, cross-region biased: "both" → 3, apex → 4 (top apex 5). Keeps
#       night sourcing alive (~60–100% of day) WITHOUT dragging the vendor-claims clock into the stall;
#   2 = STEEP — a +2 escalation: "both" → 4, apex → 5–6. Meets the design's "≥2 residual" principle to
#       the letter but pushes ~16% of games past the last-train into the stall backstop (rejected — see
#       playtests/sim-notes.md §v6.3.1). DAY costs held as printed unless DAY_CURVE (reserve knob).
NIGHT_CURVE = int(os.environ.get("TA_NIGHT_CURVE", "1"))      # 0 off | 1 soft (CD-4 default) | 2 steep
DAY_CURVE   = os.environ.get("TA_DAY_CURVE", "0") == "1"      # reserve: escalate DAY costs too (default OFF)
# CD-4 BACKSTOP: after ALL discounts, every Bribe still costs ≥1 ingredient of the vendor's cost. Default
# OFF — probe #1 decides whether the cost curve alone suffices or this floor is needed against free bribes.
MIN1_FLOOR  = os.environ.get("TA_MIN1_FLOOR", "0") == "1"    # (default OFF)

# --- v6.3.1 CD-3 COMMON TAIPEI START -------------------------------------------------------------
# 0 (default) = ALL players start in N (Taipei/North hub) at every count. 1 = the old per-count split
# ({2:[N,S], 3:[N,S,C], 4:[N,C,S,E]}) — kept behind the knob for the seat-balance A/B.
START_SPLIT = os.environ.get("TA_START_SPLIT", "0") == "1"   # (CD-3 default: common Taipei start)

# --- v6.3.1 CD-2 "Scheduled Maintenance" (排班保養) — table-wide HSR outage ------------------------
# A special TABLE-WIDE, PERSISTENT event (NOT a ⦿/⬢/➤ scope). Seeded as MAINT_COUNT marker(s) in the
# MAINT_REGION deck of phase MAINT_PHASE (1 day | 2 night). Surfacing on a Visit / Convenience-Store flip
# closes the HSR N↔S hop for ALL players until the start of the drawing player's next turn (one go-around).
# Count (1 vs 2) and day/night placement are the CD's knobs.
MAINT_COUNT  = int(os.environ.get("TA_MAINT_COUNT", "1"))     # copies seeded (CD default 1)
MAINT_REGION = os.environ.get("TA_MAINT_REGION", "N")         # HSR endpoint: "N" | "S" (CD default N)
MAINT_PHASE  = int(os.environ.get("TA_MAINT_PHASE", "2"))     # 1 day | 2 night (CD default night)
MAINT = "MAINT"                                               # the marker token mixed into that deck
LARDER_CAP   = int(os.environ.get("TA_LARDER_CAP", "7"))
STAR_BONUS_P = int(os.environ.get("TA_STAR_P", "2"))           # dynamic ★ token +Bookings (no more +Rep)
STALL_CAP    = int(os.environ.get("TA_STALL_CAP", "34"))       # hard per-player turn cap (drag backstop)

# --- REACH (v6.3 Change 1 — the live Buzz cap) ---------------------------------------------------
REACH_START  = int(os.environ.get("TA_REACH_START", "2"))      # starting Reach (sim knob — start generous)
REACH_TRAVEL = int(os.environ.get("TA_REACH_TRAVEL", "1"))     # +Reach per Travel (the engine's fuel line)
REACH_TOP    = int(os.environ.get("TA_REACH_TOP", "12"))       # track top
# event Reach economy: fraction of BOONS that are +1 Reach; fraction of HAZARDS that are −1 Reach
REACH_BOON_FRAC = float(os.environ.get("TA_REACH_BOON", "0.34"))  # ~3–4 reach-gain events salted in
REACH_HAZ_FRAC  = float(os.environ.get("TA_REACH_HAZ",  "0.30"))  # ~2–3 reach-loss events (負評/出包)

# --- GREEDY GRAB (v6.3 Change 1c — the voluntary Reach sink) -------------------------------------
# "off" | "visit" (Visit grab only) | "both" (Visit + Convenience Store) | "aggressive" (both, low headroom)
GRAB_MODE     = os.environ.get("TA_GRAB", "both")
GRAB_HEADROOM = int(os.environ.get("TA_GRAB_HEADROOM", "2"))   # only grab if Reach − committed ≥ this

# The per-region signature SUPPLY (the hoarder / anti-lockout knob) — conserved tokens per region PER
# PHASE. Larger = denial is weaker. Common (K) supply in C&S is K_SUPPLY.
SIG_SUPPLY = int(os.environ.get("TA_SIG_SUPPLY", "10"))
K_SUPPLY   = int(os.environ.get("TA_K_SUPPLY", "6"))

# Event density (the "hotter night" knob): fraction of market draws that are events, day vs night.
DAY_EVENT_FRAC   = float(os.environ.get("TA_DAY_EVENT", "0.25"))
NIGHT_EVENT_FRAC = float(os.environ.get("TA_NIGHT_EVENT", "0.42"))
EVENT_HAZARD_FRAC = float(os.environ.get("TA_HAZARD", "0.55"))  # of events, this frac are hazards
STAR_BOON_CHANCE  = float(os.environ.get("TA_STARBOON", "0.22"))# of (non-reach) boons, frac that drop a ★

# Scope ratio (⦿ self / ⬢ region / ➤ neighbour); hazards skew region/neigh, boons skew self.
SCOPE_SELF   = float(os.environ.get("TA_SCOPE_SELF", "0.40"))
SCOPE_REGION = float(os.environ.get("TA_SCOPE_REGION", "0.40"))
SCOPE_NEIGH  = float(os.environ.get("TA_SCOPE_NEIGH", "0.20"))

# --- THE CLOCK (v6.3: keep the v6.2 vendor-claims clock) -----------------------------------------
CLOCK_MODE = os.environ.get("TA_CLOCK", "vendor")             # "vendor" (v6.3 default) | "mission"
M_DUSK = int(os.environ.get("TA_M_DUSK", "3"))
M_END  = int(os.environ.get("TA_M_END",  "5"))
V_DUSK = int(os.environ.get("TA_V_DUSK", "5"))                # dusk @ 5th table-wide vendor claim @2p
V_END  = int(os.environ.get("TA_V_END",  "10"))               # last train @ 10th @2p
NIGHT_SPRINT = int(os.environ.get("TA_NIGHT_SPRINT", "0"))

MISSION_DRAW = int(os.environ.get("TA_MISSION_DRAW", "5"))     # tickets drawn per phase (2p)
MROW = int(os.environ.get("TA_MROW", "3"))                     # face-up ticket row width

# --- THE −½ PENALTY (carried question) -----------------------------------------------------------
PENALTY = os.environ.get("TA_PENALTY", "half")                 # "half" (−floor(v/2)) | "zero" (score 0)
# DAY-ticket judging timing (v6.3 Change 4 = "dusk"; "end" = the v6.2 behaviour, for the A/B diagnosis)
DAY_JUDGE = os.environ.get("TA_DAY_JUDGE", "dusk")             # "dusk" | "end"

# --- SCORING MODEL (v6.3-fix #1 — the CD's tickets-only hypothesis) -------------------------------
# "both"         = v6.3 shape-lock: final score = Bookings (vendor values) + Tour Tickets.
# "tickets_only" = vendors give NO direct points; a vendor is purely the ENGINE (discount ramp + the
#                  stop you assemble to COMPLETE tickets). Final score = Tour Tickets ONLY. Structurally
#                  kills "ignore the objectives" — objectives are the only points.
SCORING = os.environ.get("TA_SCORING", "tickets_only")         # "both" | "tickets_only" (CD-LOCKED default)
# how heavily the greedy planner still chases raw Bookings when it no longer scores. Under tickets_only a
# vendor's Bookings value is only an ENGINE-quality proxy (bigger dishes ramp/enable more), so down-weight
# it and let ticket-completion drive target choice. 1.0 = full weight (the "both" world).
BOOK_ENGINE_W = float(os.environ.get("TA_BOOK_W", "0.35"))

# --- MILESTONES ("Rave Reviews") — v6.3-fix #3 (runaway) + rehome under tickets-only --------------
# MS_MODE: "first"      = table-wide, first player to cross each mark (v6.3 lock; the runaway source).
#          "perplayer"  = EACH player earns the boon the first time THEY cross the mark (zero runaway).
#          "consolation"= first crosser gets the full boon; a later crosser gets a reduced boon.
MS_MODE = os.environ.get("TA_MS_MODE", "perplayer")           # (CD-LOCKED default; was "first")
# MS_ON: which track the marks sit on. "bookings" = Bookings 7/14 (works even under tickets-only, where
#        the Bookings track still accrues as an ENGINE meter). "tickets" = count of settled WIN-pile
#        tickets (a natural home once Bookings stops scoring) at MS_T1 / MS_T2.
MS_ON = os.environ.get("TA_MS_ON", "bookings")                 # "bookings" | "tickets"
MS_B1 = int(os.environ.get("TA_MS_B1", "7"))                   # bookings mark 1
MS_B2 = int(os.environ.get("TA_MS_B2", "14"))                  # bookings mark 2
MS_T1 = int(os.environ.get("TA_MS_T1", "2"))                   # tickets-completed mark 1
MS_T2 = int(os.environ.get("TA_MS_T2", "4"))                   # tickets-completed mark 2

# --- CONTESTED-FIGHT lever (v6.3-fix #2) ----------------------------------------------------------
# override the face-up vendor slot counts to test whether tighter scarcity lifts collisions. "" = default
# (N:2, others:1). e.g. TA_SLOTS="1,1,1,1" for a 4-slot board (max scarcity).
SLOTS_OVERRIDE = os.environ.get("TA_SLOTS", "")

# --- CHARACTER KNOBS (v6.3 kits — locked; do NOT pre-tweak, the re-sim reads them) ---------------
# H1 大胃王 flaw. "twice" (A, locked) | "keep2" (B) | "next" (C).
H1 = os.environ.get("TA_H1", "twice")
# H2 大哥. v6.3 lock = option D: THRESH 1 (must lead by ≥1), FLAW "none". Probe others if he drifts.
DAGE_THRESH = int(os.environ.get("TA_H2_THRESH", "1"))
DAGE_FLAW   = os.environ.get("TA_H2_FLAW", "none")            # "none"|"tab"|"promote1"|"nocontest"
# 媽寶 buff. v6.3 lock = "keep2". "none"|"keep2"|"travel2".
OFFICE_BUFF = os.environ.get("TA_OFFICE", "keep2")
# 網紅 flaw. CHARACTER RE-PASS default = "none" (Late-to-the-Party RETIRED — see the re-pass note in the
# header + playtests/sim-notes.md §v6.3 CHARACTER RE-PASS). Was "lateparty" (miss the first NIGHT turn),
# which double-taxed the kit once the Reach cap already throttles Promote-3. Probe "lateparty" to compare.
INFL_FLAW = os.environ.get("TA_INFL_FLAW", "none")            # "none" (RE-PASS default) | "lateparty"
# 里長伯 KIT (v6.3.1 CD-1) — "home" (default) is the reworked HOME-REGION kit:
#   * picks ONE home region at setup (bot heuristic: the region his face-up day ramp + dealt day-tickets
#     most reward — see _pick_home_region; ASSUMPTION-tagged, and since everyone now starts in N/Taipei
#     the home diagnostic reports whether he just camps North);
#   * Old Favours −1 ingredient applies ONLY in his home region (floored at 0, like any discount);
#   * an AWAY TAX +TAX of one chosen type (the vendor's local signature — cheapest-to-add, he must stand
#     there) on every Bribe OUTSIDE home; and he now USES HSR (the no-HSR flaw is re-homed as CD-2).
# "regions" recovers the retired first-N-regions discount kit (COUNCILLOR_REGIONS) for an A/B if useful.
COUNCILLOR_KIT       = os.environ.get("TA_COUNCILLOR_KIT", "home")   # "home" (CD-1 default) | "regions"
COUNCILLOR_HOME_DISC = int(os.environ.get("TA_COUNCILLOR_HOME_DISC", "1"))  # home Old-Favours magnitude
COUNCILLOR_AWAY_TAX  = int(os.environ.get("TA_COUNCILLOR_AWAY_TAX", "1"))   # away-tax magnitude
# (legacy "regions" kit knob — how many regions the old first-region discount covers; unused under KIT=home)
COUNCILLOR_REGIONS = int(os.environ.get("TA_COUNCILLOR_REGIONS", "1"))
# 里長伯 reserve BRAKE (CD-1 lever / the old option B): a thin island-wide name → less START Reach.
# Default -1 = OFF (start = REACH_START). Set 1 ("start Reach 1") if the home-region kit still runs hot.
COUNCILLOR_REACH = int(os.environ.get("TA_COUNCILLOR_REACH", "-1"))

# ==================================================================================================
#  MAP
# ==================================================================================================
REGIONS = ("N", "C", "S", "E")
RING = {"N": ["C", "E"], "C": ["N", "S"], "S": ["C", "E"], "E": ["S", "N"]}
HSR = ("N", "S")
COMMON = "K"
COMMON_REGIONS = {"C", "S"}                          # where the common 糖 lives (locally sourceable)


def neighbours(pos, char=None, hsr_open=True):
    """A pawn's LEGAL travel destinations. v6.3.1: the HSR N↔S hop is available to EVERYONE (the old
    里長伯 no-HSR guard is REMOVED — re-homed as the CD-2 table-wide Scheduled-Maintenance outage) UNLESS
    the HSR is currently closed by a Scheduled-Maintenance event (hsr_open=False → slow road for all)."""
    ns = list(RING[pos])
    if hsr_open and pos in HSR:
        other = HSR[1] if pos == HSR[0] else HSR[0]
        if other not in ns:
            ns.append(other)
    return ns


def _hsr_is_open(s):
    """CD-2: is the HSR N↔S hop currently open? Closed while a Scheduled-Maintenance card is active
    (until the start of the drawing player's next turn = s['turn'] reaches hsr_closed_until_turn)."""
    u = s.get("hsr_closed_until_turn")
    return u is None or s["turn"] >= u


def region_neighbours(r):
    """GEOGRAPHIC adjacency (ring + HSR) — resolves a ➤ neighbour-scoped event's spill."""
    ns = set(RING[r])
    if r in HSR:
        ns.add(HSR[1] if r == HSR[0] else HSR[0])
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
    return neighbours(pos, char, hsr_open)[0]


# ==================================================================================================
#  EVENT CARDS — ("ev", kind, scope, sub)
#    kind  : hazard | boon
#    scope : self | region | neigh
#    sub   : tempo | reach   (hazard);  ingredient | reach | star   (boon)
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
    if kind == "boon":
        if rng.random() < REACH_BOON_FRAC:
            return ("ev", "boon", "self", "reach")          # "word spreads" — +1 Reach to the flipper
        if rng.random() < STAR_BOON_CHANCE:
            return ("ev", "boon", "region", "star")
        return ("ev", "boon", _sample_scope("boon", rng), "ingredient")
    # hazard
    if rng.random() < REACH_HAZ_FRAC:
        return ("ev", "hazard", "self", "reach")            # 負評 / 出包 — −1 Reach to the flipper
    return ("ev", "hazard", _sample_scope("hazard", rng), "tempo")


# ==================================================================================================
#  VENDOR TABLE (v6.3 reissued — Bookings + (icon | none); NO perk, NO rep) + the central-tea fix
# ==================================================================================================
# A vendor: id, region, phase (1 day | 2 night), is_drink, cost (Counter over N/C/S/E/K),
# bookings (points), icon (bool — carries its own region discount icon), star (dynamic-★ eligible marker,
# unused for seeding — dynamic ★ is event-placed).
CENTRAL_TEA_FIX = os.environ.get("TA_TEA_FIX", "1") == "1"    # re-point 牛肉麵 →S to →C (tea gets export)


def _build_vendors():
    V = []

    def add(region, phase, is_drink, cost, bookings, icon, star=False):
        V.append({"id": len(V), "region": region, "phase": phase, "is_drink": is_drink,
                  "cost": Counter(cost), "bookings": bookings, "icon": icon,
                  "star": star, "total_cost": sum(cost.values())})

    # CD-4: NIGHT costs escalate (cross-region biased) so a night marquee EXCEEDS the max single-region
    # ramp; the region-discount defrays but never zeroes it. DAY costs held as printed (unless DAY_CURVE).
    # `nc(raw, soft, steep)` picks by NIGHT_CURVE level (0/1/2). The re-sim landed on SOFT (level 1):
    # a +1 escalation ("both"→3, apex→4, cross-region biased) — night sourcing stays live without the
    # STEEP curve's clock stall. `dc` is the reserve DAY escalation (default off).
    def nc(raw, soft, steep):
        return {0: raw, 1: soft, 2: steep}.get(NIGHT_CURVE, soft)

    def dc(base, escalated):
        return escalated if DAY_CURVE else base

    # --- North 北 (pork · 2 slots · no local K) ---
    add("N", 1, False, dc({"N": 1}, {"N": 1}), 2, True)   # 肉包 Pork Bao (discount-only)
    add("N", 1, False, dc({"N": 1}, {"N": 1}), 1, True)   # 蛋餅 Egg Crepe (discount-only)
    add("N", 1, True,  {"K": 1}, 2, False)                # 豆漿 Soy Milk (drink · none)
    add("N", 2, False, nc({"N": 2}, {"N": 2, "C": 1}, {"N": 3, "C": 1}), 5, True)  # 胡椒餅 (both, +C export)
    # 牛肉麵 Beef Noodle (both). v6.3 table = {N:2, S:1}→S. CENTRAL_TEA_FIX re-points it →C.
    if CENTRAL_TEA_FIX:
        add("N", 2, False, nc({"N": 2, "C": 1}, {"N": 2, "C": 1}, {"N": 3, "C": 1}), 6, True)  # 牛肉麵 →C
    else:
        add("N", 2, False, nc({"N": 2, "S": 1}, {"N": 2, "S": 1}, {"N": 3, "S": 1}), 6, True)  # 牛肉麵 →S
    add("N", 2, False, nc({"N": 3}, {"N": 3, "S": 1}, {"N": 4, "S": 1}), 7, False, True)  # ★ 大香腸 (apex, cross)
    add("N", 2, True,  {"K": 1}, 2, False)                # 珍奶 Bubble Tea (drink · none)
    # --- Central 中 (tea · 1 slot · local K) ---
    add("C", 1, False, dc({"C": 1}, {"C": 1}), 2, True)   # 肉圓 Ba-wan (discount-only)
    add("C", 1, False, dc({"C": 1}, {"C": 1}), 1, True)   # 麵線 Misua (discount-only)
    add("C", 1, True,  {"K": 1}, 2, False)                # 珍珠奶茶 Bubble Tea (drink · none)
    add("C", 2, False, nc({"C": 2}, {"C": 2, "S": 1}, {"C": 3, "S": 1}), 5, True)  # 大腸包小腸 (both, cross)
    add("C", 2, False, nc({"C": 2, "S": 1}, {"C": 3, "S": 1}, {"C": 4, "S": 1}), 6, False, True)  # ★ 逢甲名物 →S
    add("C", 2, True,  {"K": 1}, 2, False)                # 冬瓜茶 Wintermelon Tea (drink · none)
    # --- South 南 (seafood · 1 slot · local K) ---
    add("S", 1, False, dc({"S": 1}, {"S": 1}), 2, True)   # 虱目魚粥 Milkfish Congee (discount-only)
    add("S", 1, False, dc({"S": 1}, {"S": 1}), 1, True)   # 碗粿 Rice Bowl Cake (discount-only)
    add("S", 1, True,  {"K": 1}, 2, False)                # 木瓜牛奶 Papaya Milk (drink · none)
    add("S", 2, False, nc({"S": 2}, {"S": 2, "E": 1}, {"S": 3, "E": 1}), 5, True)  # 蚵仔煎 (both, cross)
    add("S", 2, False, nc({"S": 2, "E": 1}, {"S": 3, "E": 1}, {"S": 3, "E": 1}), 6, True)  # 棺材板 →E (both)
    add("S", 2, False, nc({"S": 3}, {"S": 3, "C": 1}, {"S": 4, "C": 1}), 7, False, True)  # ★ 擔仔麵 (apex, cross)
    # --- East 東 (rice · 1 slot · no local K · Indigenous-forward) ---
    add("E", 1, False, dc({"E": 2}, {"E": 2}), 2, True)   # 竹筒飯 Bamboo-Tube Rice (discount-only)
    add("E", 1, False, dc({"E": 1}, {"E": 1}), 2, True)   # 米糕 Rice Cake (discount-only)
    add("E", 1, True,  {"K": 1}, 2, False)                # 洛神花茶 Roselle Tea (drink · none)
    add("E", 2, False, nc({"E": 2}, {"E": 2, "N": 1}, {"E": 3, "N": 1}), 5, True)  # 麻糬 (both, cross)
    add("E", 2, False, nc({"E": 2, "N": 1}, {"E": 3, "N": 1}, {"E": 4, "N": 2}), 8, False, True)  # ★ 石板烤肉 →N (top apex)
    return V


VENDORS = _build_vendors()


def _rebuild_vendors():
    """Rebuild the module-level VENDORS table — needed when a cost knob (NIGHT_CURVE / DAY_CURVE) is
    toggled at RUNTIME for an A/B, since costs are baked in at build time."""
    global VENDORS
    VENDORS = _build_vendors()


def _is_cross(vid):
    """A cross-region (→X) dish: its cost spans >1 distinct signature region (K/common ignored)."""
    return len([r for r in VENDORS[vid]["cost"] if r != COMMON]) >= 2


def _region_deck(region, phase):
    return [v["id"] for v in VENDORS if v["region"] == region and v["phase"] == phase]


# ==================================================================================================
#  TOUR TICKETS (v6.3 — DAY / NIGHT pools; win/lose piles per phase)
# ==================================================================================================
# A ticket = (value, phase-tag "d"|"n"|"g", progress-fn(st)->(done, needed)). Progress is read from a
# won-vendor stat block (_wstat) so a ticket is a PATTERN over the vendors you have claimed. This is the
# machinery that makes "claim vendors to COMPLETE tours" the point of the game under tickets-only scoring.
#
# v6.3-fix knobs (this re-sim):
#   TA_TICKETS  = "base" (the v6.3 shape-lock set) | "expanded" (the CD's richer, more varied deck)
#   TA_TVAL     = ticket value multiplier (the lighter "just raise ticket VALUES" fix, e.g. 1.5)
TICKET_SET   = os.environ.get("TA_TICKETS", "expanded")       # "base" | "expanded" (CD-LOCKED default)
TICKET_VMULT = float(os.environ.get("TA_TVAL", "1.0"))        # scale all ticket values (lighter fix knob)


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
        "bookings": sum(v["bookings"] for v in won),
        "bookings_day": sum(v["bookings"] for v in won if v["act_won"] == 1),
        "contested": sum(1 for v in won if v["contested"]),
        "stars": sum(1 for v in won if v["starred"]),
        "cost_le2": sum(1 for v in won if v["total_cost"] <= 2),
        "cost_ge3": sum(1 for v in won if v["total_cost"] >= 3),
        "before_dusk": sum(1 for v in won if v["act_won"] == 1),
        "final_round": sum(1 for v in won if v["final_round"]),
        "cross": sum(1 for v in won if v.get("cross")),           # cross-region (→X) dishes claimed
        "max_region": max(by.values()) if by else 0,             # deepest single-region stack
    }


# --- the ticket registry: key -> (value, phase, ease, progress-fn) --------------------------------
# ease ≈ how claimable/finishable a bot rates it (row-pick heuristic only). progress-fn returns
# (done, needed) for monotonic partial credit.
def _T(st):  # tiny alias so the lambdas below read cleanly
    return st


_BASE = {
    # --- Daytime (the ramp / positioning phase) ---
    "d_breakfast3": (4, "d", 0.70, lambda s: (min(s["day_food"], 3), 3)),
    "d_travel3":    (5, "d", 0.50, lambda s: (min(len(s["regions"]), 3), 3)),
    "d_south2":     (4, "d", 0.70, lambda s: (min(s["by"]["S"], 2), 2)),
    "d_north2":     (4, "d", 0.80, lambda s: (min(s["by"]["N"], 2), 2)),
    "d_drinks2":    (3, "d", 0.60, lambda s: (min(s["drinks"], 2), 2)),
    "d_mix1":       (3, "d", 0.90, lambda s: (min(s["food"], 1) + min(s["drinks"], 1), 2)),
    "d_early3":     (5, "d", 0.50, lambda s: (min(s["before_dusk"], 3), 3)),
    "d_cheap3":     (4, "d", 0.70, lambda s: (min(s["cost_le2"], 3), 3)),
    "d_east1":      (3, "d", 0.70, lambda s: (min(s["by"]["E"], 1), 1)),
    "d_prestige8":  (4, "d", 0.60, lambda s: (min(s["bookings_day"], 8), 8)),
    "d_central2":   (4, "d", 0.70, lambda s: (min(s["by"]["C"], 2), 2)),
    "d_contest1":   (4, "d", 0.45, lambda s: (min(s["contested"], 1), 1)),
    # --- Nighttime (the apex / contest phase) ---
    "n_nmfood2":    (5, "n", 0.70, lambda s: (min(s["night_food"], 2), 2)),
    "n_star1":      (5, "n", 0.55, lambda s: (min(s["stars"], 1), 1)),
    "n_all4":       (7, "n", 0.30, lambda s: (min(len(s["regions"]), 4), 4)),
    "n_surfturf":   (4, "n", 0.70, lambda s: (min(s["by"]["S"], 1) + min(s["by"]["N"], 1), 2)),
    "n_prestige14": (6, "n", 0.50, lambda s: (min(s["bookings"], 14), 14)),
    "n_four":       (5, "n", 0.65, lambda s: (min(s["n"], 4), 4)),
    "n_expensive1": (4, "n", 0.70, lambda s: (min(s["cost_ge3"], 1), 1)),
    "n_east2":      (5, "n", 0.55, lambda s: (min(s["by"]["E"], 2), 2)),
    "n_contest2":   (5, "n", 0.40, lambda s: (min(s["contested"], 2), 2)),
    "n_final2":     (5, "n", 0.50, lambda s: (min(s["final_round"], 2), 2)),
    "n_drinks3":    (4, "n", 0.55, lambda s: (min(s["drinks"], 3), 3)),
    "n_allvenue":   (6, "n", 0.60, lambda s: (min(s["day_food"], 1) + min(s["night_food"], 1) + min(s["drinks"], 1), 3)),
    # --- General (folded: 遍地開花 → BOTH pools; 收藏家 / 揮金如土 → NIGHT) ---
    "g_travel3":    (5, "g", 0.55, lambda s: (min(len(s["regions"]), 3), 3)),
    "g_collect5":   (5, "g", 0.60, lambda s: (min(s["n"], 5), 5)),
    "g_prestige12": (6, "g", 0.55, lambda s: (min(s["bookings"], 12), 12)),
}

# --- CD's EXPANDED deck: more distinct patterns/paths so it isn't a narrow scramble --------------
# New PATTERN TYPES beyond the base: region PAIRS, cross-region (→X) dishes, single-region DEPTH,
# deeper collections, food-count ladders. Variety in difficulty + value so WHICH tours you chase is a
# real choice. (繁體 names are placeholders for bg-theme; the sim only reads the pattern + value.)
_EXPANDED_EXTRA = {
    # DAY — easier positioning variety
    "d_pairNC":     (3, "d", 0.75, lambda s: (min(s["by"]["N"], 1) + min(s["by"]["C"], 1), 2)),
    "d_pairSE":     (3, "d", 0.70, lambda s: (min(s["by"]["S"], 1) + min(s["by"]["E"], 1), 2)),
    "d_food3":      (4, "d", 0.65, lambda s: (min(s["food"], 3), 3)),
    "d_cheap2":     (3, "d", 0.80, lambda s: (min(s["cost_le2"], 2), 2)),
    "d_daymix":     (3, "d", 0.85, lambda s: (min(s["day_food"], 1) + min(s["drinks"], 1), 2)),
    "d_collect4":   (5, "d", 0.45, lambda s: (min(s["n"], 4), 4)),
    "d_deep2":      (3, "d", 0.75, lambda s: (min(s["max_region"], 2), 2)),
    # NIGHT — apex / high-value variety
    "n_cross1":     (4, "n", 0.55, lambda s: (min(s["cross"], 1), 1)),
    "n_cross2":     (6, "n", 0.35, lambda s: (min(s["cross"], 2), 2)),
    "n_expensive2": (6, "n", 0.45, lambda s: (min(s["cost_ge3"], 2), 2)),
    "n_collect6":   (7, "n", 0.35, lambda s: (min(s["n"], 6), 6)),
    "n_deep3":      (6, "n", 0.40, lambda s: (min(s["max_region"], 3), 3)),
    "n_nightfood3": (6, "n", 0.45, lambda s: (min(s["night_food"], 3), 3)),
    "n_eastnorth":  (4, "n", 0.65, lambda s: (min(s["by"]["E"], 1) + min(s["by"]["N"], 1), 2)),
    "n_censouth":   (4, "n", 0.70, lambda s: (min(s["by"]["C"], 1) + min(s["by"]["S"], 1), 2)),
    "n_allfood5":   (6, "n", 0.40, lambda s: (min(s["food"], 5), 5)),
    # GENERAL (both) — a cross-region flavour that reads either phase
    "g_cross1":     (4, "g", 0.55, lambda s: (min(s["cross"], 1), 1)),
}

TICKETS = dict(_BASE)
if TICKET_SET == "expanded":
    TICKETS.update(_EXPANDED_EXTRA)

# pools: DAY = day tickets + the DAY 遍地開花 copy; NIGHT = night tickets + the two night generals + the
# NIGHT 遍地開花 copy (+ any expanded generals ride NIGHT too). A ticket's pool IS its judging trigger.
DAY_TICKETS = [k for k, t in TICKETS.items() if t[1] == "d"]
NIGHT_TICKETS = [k for k, t in TICKETS.items() if t[1] == "n"]
GEN_TICKETS = [k for k, t in TICKETS.items() if t[1] == "g"]
DAY_POOL = DAY_TICKETS + ["g_travel3"]                        # base 13 / expanded ~20
NIGHT_POOL = NIGHT_TICKETS + GEN_TICKETS                       # base 15 / expanded ~25


def _mprog(key, st):
    """(done, needed) — monotonic partial credit for the planner."""
    t = TICKETS.get(key)
    if t is None:
        return 0, 1
    return t[3](st)


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
    v = TICKETS[key][0] * TICKET_VMULT
    return int(round(v))


def _judge_ticket(key, won):
    """Return the win/lose-pile score for one ticket judged against `won` (the vendors owned at the
    judging trigger — dusk for DAY tickets, last train for NIGHT tickets)."""
    v = _ticket_value(key)
    if _mdone(key, won):
        return v                       # 成團 (win pile) → +value
    if PENALTY == "half":
        return -(v // 2)               # 遺珠 (lose pile) → −floor(v/2)
    return 0                           # PENALTY == "zero"


def _ticket_ease(key):
    return TICKETS[key][2]


# --- which ticket a bot wants to CLAIM off the face-up row -----------------------------------------
_OPP_KEYS = ("n_star1", "n_prestige14", "g_prestige12", "d_prestige8", "n_expensive1",
             "n_expensive2", "n_cross2", "n_collect6")
_DISRUPT_KEYS = ("d_contest1", "n_contest2")
_SPEED_KEYS = ("d_early3", "n_final2", "d_breakfast3", "n_four", "d_cheap2", "d_pairNC")
_HARD_DRINK = ("d_drinks2", "n_drinks3")
_NEEDS_DRINK = ("d_drinks2", "n_drinks3", "d_mix1", "n_allvenue", "d_daymix")


def _ticket_fit(prefs, key):
    needs_drink = key in _NEEDS_DRINK
    hard_drink = key in _HARD_DRINK
    needs_food = key not in _HARD_DRINK
    if prefs.get("no_drinks") and hard_drink:
        return 0.05
    if prefs.get("pure_drinks") and needs_food and not needs_drink:
        return 0.1
    fit = 1.0
    if prefs.get("opportunistic") and key in _OPP_KEYS:
        fit *= 1.4
    if prefs.get("disrupt") and key in _DISRUPT_KEYS:
        fit *= 1.6
    if prefs.get("speed") and key in _SPEED_KEYS:
        fit *= 1.3
    return fit


def _ticket_keep_score(won, key, prefs):
    d, n = _mprog(key, _wstat(won))
    prog = (d / n) if n else 0.0
    return _ticket_value(key) * _ticket_ease(key) * _ticket_fit(prefs, key) + 2.0 * prog


# --- CD-1: 里長伯's home-region pick (bot heuristic) ----------------------------------------------
# ASSUMPTION: a real 里長伯 picks the region he intends to GRIND. The bot scores each region by (a) the
# face-up DAY ramp vendors sitting there (where he can build the icon ramp his home discount amplifies) +
# (b) how many of his dealt DAY tickets a single vendor of that region would advance (where the objectives
# pull him). argmax. Since CD-3 puts EVERYONE in N/Taipei at the start, North's 2 day slots give it a
# baseline edge — the home-region DIAGNOSTIC (probe below) reports the actual distribution so we can see
# whether he just camps North rather than making a real regional declaration.
def _pick_home_region(faceup, mrow):
    score = {r: 0.0 for r in REGIONS}
    for r in REGIONS:
        for vid in faceup[r]:
            v = VENDORS[vid]
            if not v["is_drink"] and v["icon"]:
                score[r] += 1.0
    for r in REGIONS:
        fake = {"id": -1, "region": r, "is_drink": False, "phase": 1, "bookings": 3,
                "total_cost": 1, "contested": False, "starred": False, "act_won": 1,
                "cross": False, "final_round": False}
        for key in mrow:
            if _mhelps(key, fake, []):
                score[r] += 1.5
    return max(REGIONS, key=lambda r: (score[r], -REGIONS.index(r)))


CHARACTERS = ("neutral", "councillor", "office", "influencer", "dagushi", "dage")


# ==================================================================================================
#  GAME
# ==================================================================================================
class TravelAgentsGame:
    # -------- setup --------
    def new_state(self, rng, n_players=2, characters=None, prefs=None):
        chars = list(characters) if characters else ["neutral"] * n_players
        prefs = list(prefs) if prefs else [dict(BAL) for _ in range(n_players)]
        slots = {"N": 2, "C": 1, "S": 1, "E": 1}
        if n_players >= 3: slots["C"] = 2
        if n_players >= 4: slots["S"] = 2
        if SLOTS_OVERRIDE:                                   # fix #2 lever — tighten face-up scarcity
            _sv = [int(x) for x in SLOTS_OVERRIDE.split(",")]
            slots = {"N": _sv[0], "C": _sv[1], "S": _sv[2], "E": _sv[3]}
        supply = int(round(BUZZ_SUPPLY * (1 + 0.375 * (n_players - 2))))
        mdraw = MISSION_DRAW + (1 if n_players == 3 else 2 if n_players >= 4 else 0)
        m_dusk = {2: M_DUSK, 3: M_DUSK + 1, 4: M_DUSK + 2}.get(n_players, M_DUSK)
        m_end  = {2: M_END,  3: M_END + 2,  4: M_END + 4}.get(n_players, M_END)
        v_dusk = {2: V_DUSK, 3: V_DUSK + 2, 4: V_DUSK + 4}.get(n_players, V_DUSK)
        v_end  = {2: V_END,  3: V_END + 4,  4: V_END + 8}.get(n_players, V_END)
        # CD-3: everyone starts in N (Taipei/North hub). The old per-count split is behind START_SPLIT.
        if START_SPLIT:
            starts = {2: ["N", "S"], 3: ["N", "S", "C"], 4: ["N", "C", "S", "E"]}.get(n_players, ["N", "S"])
        else:
            starts = ["N"] * n_players

        vdeck, faceup, buzz_ids = {}, {}, set()
        for r in REGIONS:
            d = _region_deck(r, 1); rng.shuffle(d)
            up = [d.pop() for _ in range(min(slots[r], len(d)))]
            vdeck[r] = d; faceup[r] = up
            buzz_ids |= set(up)

        ing_pool, ing_discard = {}, {}
        for r in REGIONS:
            pool = Counter({r: SIG_SUPPLY})
            if r in COMMON_REGIONS:
                pool[COMMON] += K_SUPPLY
            # CD-2: seed the Scheduled-Maintenance marker into the DAY deck only if MAINT_PHASE==1 (day).
            if MAINT_COUNT > 0 and r == MAINT_REGION and MAINT_PHASE == 1:
                pool[MAINT] += MAINT_COUNT
            ing_pool[r] = pool
            ing_discard[r] = Counter()

        drawn = rng.sample(DAY_POOL, min(mdraw, len(DAY_POOL)))
        mrow = drawn[:MROW]
        mreserve = drawn[MROW:]

        players = []
        for p in range(n_players):
            ch = chars[p]
            players.append({
                "char": ch, "prefs": prefs[p],
                "pos": starts[p % len(starts)],
                "larder": Counter(), "won": [], "icons": Counter(),
                "bookings": 0,                                   # the live Bookings (former Prestige)
                # v6.3: the live Buzz cap. 里長伯 option-B flaw = a thinner island-wide name → less start Reach.
                "reach": (COUNCILLOR_REACH if (ch == "councillor" and COUNCILLOR_REACH >= 0) else REACH_START),
                "promote_bonus": (1 if ch == "influencer" else 0),
                # CD-1: 里長伯 declares ONE home region at setup (bot heuristic). None for everyone else.
                "home_region": (_pick_home_region(faceup, mrow) if ch == "councillor" else None),
                "councillor_regions": set(),
                "tickets": [], "counted_done": set(),
                "day_ticket_score": 0, "day_win": 0, "day_lose": 0,   # DAY tickets frozen at dusk
                "next_visit_extra_hazard": 0, "tempo_tax": 0,
                "skip_next": False,                              # 網紅 "Late to the Party" pending pass
                "bribe_discount": 0,                             # milestone-14 one-shot −1 ingredient
                "ms7_done": False, "ms14_done": False,           # per-player milestone flags (fix #3)
            })

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
            # milestones (Rave Reviews). ms{7,14}_by = FIRST crosser (runaway diagnostic); ms{7,14}_earn
            # = how many players earned each boon (spreads under perplayer/consolation).
            "ms7_by": None, "ms14_by": None, "ms7_earn": 0, "ms14_earn": 0,
            # diagnostics
            "food_wins": 0, "drink_wins": 0, "contested_wins": 0,
            "star_placed": 0, "star_wins": {p: 0 for p in range(n_players)},
            "max_buzz_on_vendor": 0, "max_committed": 0,
            "claim_by_region": {r: 0 for r in REGIONS},
            "src_by_region": {r: 0 for r in REGIONS}, "src_common": 0,
            "travels": 0, "visits": 0, "cstores": 0, "promotes": 0, "inter_moves": 0,
            # --- v6.3.1 CD-4 probe #1: day/night SOURCING split (Visit+CStore+Travel per turn) ---
            "turns_day": 0, "turns_night": 0,
            "src_actions_day": 0, "src_actions_night": 0,
            "night_claims": 0, "night_food_wins": 0,       # night vendor claims (climax must still fire)
            "free_bribes": 0, "free_night_bribes": 0,       # fully-discounted bribes (the free-bribe exploit)
            # --- v6.3.1 CD-2 Scheduled Maintenance (table-wide HSR outage) ---
            "hsr_closed_until_turn": None, "maint_fired": 0, "maint_closed_turns": 0,
            "maint_seeded": (MAINT_COUNT if (MAINT_COUNT > 0 and MAINT_PHASE == 1) else 0),
            # --- v6.3.1 CD-1 councillor home/away diagnostics ---
            "councillor_home_bribes": 0, "councillor_away_bribes": 0,
            "home_pick": Counter(pl["home_region"] for pl in players if pl["home_region"]),
            "dusk_turn": None, "last_turn": None, "first_night_win_turn": None,
            "legal_counts": [], "forced_turns": 0,
            "events_fired": 0, "scope_fired": {"self": 0, "region": 0, "neigh": 0},
            "cs_rival_hits": 0, "takethat_hits": 0, "pokes": 0,
            "claims": 0, "empty_draws": 0, "passes": 0,
            # --- REACH economy diagnostics ---
            "reach_blocked": 0,                # times a bot wanted to Promote but the cap forbade it
            "reach_gain_travel": 0, "reach_gain_event": 0, "reach_gain_ms": 0,
            "reach_loss_grab": 0, "reach_loss_event": 0, "reach_forced_return": 0,
            "greedy_visit": 0, "greedy_cs": 0,
            "reach_zero_turns": 0, "reach_at_dusk": [], "reach_samples": [],
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

    def _committed(self, s, p):
        return sum(b[p] for b in s["buzz"].values())

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
        # 里長伯 CD-1 HOME-REGION kit (default): −HOME_DISC in his home region, +AWAY_TAX everywhere else.
        if pl["char"] == "councillor" and not v["is_drink"]:
            if COUNCILLOR_KIT == "home":
                if v["region"] == pl["home_region"]:
                    for _ in range(COUNCILLOR_HOME_DISC):    # Old Favours (home only), floored at 0
                        for r in sorted(pay, key=lambda k: -pay[k]):
                            if pay[r] > 0:
                                pay[r] -= 1; break
                else:
                    # AWAY TAX: +1 of a chosen type. He must STAND in the vendor's region to Bribe, so the
                    # vendor's local signature is the cheapest-to-add type (ASSUMPTION — a human might pay
                    # it in a surplus type; this keeps the tax reliably biting where he sources anyway).
                    tax_type = v["region"]
                    if tax_type == COMMON or tax_type not in pay:
                        # cross-region/common edge: fall back to the largest existing region cost entry
                        cands = [r for r in pay if r != COMMON] or list(pay)
                        tax_type = max(cands, key=lambda r: pay.get(r, 0)) if cands else v["region"]
                    pay[tax_type] = pay.get(tax_type, 0) + COUNCILLOR_AWAY_TAX
            else:  # legacy "regions" kit — first vendor courted in each of the first N regions costs 1 fewer
                if v["region"] not in pl["councillor_regions"] \
                        and len(pl["councillor_regions"]) < COUNCILLOR_REGIONS:
                    for r in sorted(pay, key=lambda k: -pay[k]):
                        if pay[r] > 0:
                            pay[r] -= 1; break
        # milestone-14 boon: your NEXT Bribe costs 1 less ingredient (one-shot)
        if pl["bribe_discount"] > 0:
            for r in sorted(pay, key=lambda k: -pay[k]):
                if pay[r] > 0:
                    pay[r] -= 1; break
        # 大哥 tab flaw (only if a "tab"/"nocontest" variant is being probed; v6.3 lock = no flaw)
        if pl["char"] == "dage" and DAGE_FLAW in ("tab", "nocontest"):
            tgt = COMMON if v["is_drink"] else v["region"]
            pay[tgt] = pay.get(tgt, 0) + 1
        # CD-4 BACKSTOP: after ALL discounts, every Bribe still costs ≥1 ingredient of the vendor's cost.
        if MIN1_FLOOR and v["total_cost"] > 0 and sum(pay.values()) <= 0:
            r0 = min(v["cost"], key=lambda k: (k == COMMON, v["cost"][k]))  # a type in the vendor's cost
            pay[r0] = 1
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

    def _promote_ok(self, s, p, vid):
        """Reach cap: committed Buzz + this Promote's Buzz must stay ≤ Reach."""
        if s["supply"] <= 0 or not self._present(s, p, vid):
            return False
        pl = s["players"][p]
        y = min(self._promote_yield(pl), s["supply"])
        return self._committed(s, p) + y <= pl["reach"]

    # -------- legal actions --------
    def legal_actions(self, s, p):
        pl = s["players"][p]
        if pl["skip_next"]:                                  # 網紅 misses this (its first NIGHT) turn
            return [("pass",)]
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
        for d in neighbours(pl["pos"], pl["char"], _hsr_is_open(s)):   # CD-2: HSR may be closed
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
        if pl["reach"] <= 0:
            s["reach_zero_turns"] += 1
        s["reach_samples"].append(pl["reach"])
        # CD-4 probe #1: which half is this turn, and CD-2: is the HSR currently closed this turn?
        if s["act"] == 1:
            s["turns_day"] += 1
        else:
            s["turns_night"] += 1
        if not _hsr_is_open(s):
            s["maint_closed_turns"] += 1
        kind = act[0]
        if kind == "pass":
            pl["skip_next"] = False
            s["passes"] += 1
        elif kind == "bribe":
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
            self._finalize(s)
            s["done"] = True
        if s["turn"] > 8000:
            self._finalize(s)
            s["done"] = True
        return s

    # -------- REACH helpers --------
    def _gain_reach(self, s, p, amt, kind):
        pl = s["players"][p]
        before = pl["reach"]
        pl["reach"] = min(REACH_TOP, pl["reach"] + amt)
        got = pl["reach"] - before
        s[f"reach_gain_{kind}"] += got

    def _lose_reach(self, s, p, amt, kind):
        """Forced/voluntary Reach loss. Floors at 0; if committed > Reach, return Buzz to supply."""
        pl = s["players"][p]
        before = pl["reach"]
        pl["reach"] = max(0, pl["reach"] - amt)
        lost = before - pl["reach"]
        s[f"reach_loss_{kind}"] += lost
        # enforce the cap invariant: pull Buzz back off the board (bot's choice) until committed ≤ Reach
        while self._committed(s, p) > pl["reach"]:
            cands = [vid for vid, b in s["buzz"].items() if b[p] > 0]
            if not cands:
                break
            # let a fizzle happen where you're LOSING the fight (least useful), tie-break least own buzz
            def _key(vid):
                lead, _ = self._buzz_lead(s, p, vid)
                return (lead, s["buzz"][vid][p])
            vid = min(cands, key=_key)
            s["buzz"][vid][p] -= 1
            s["supply"] += 1
            s["reach_forced_return"] += 1

    def _greedy_grab_ok(self, s, p):
        """The voluntary Greedy Grab is legal only if it wouldn't drop Reach below committed Buzz, and
        the bot only takes it with comfortable headroom (never starves its own fight)."""
        if GRAB_MODE == "off":
            return False
        pl = s["players"][p]
        headroom = pl["reach"] - self._committed(s, p)
        need = 1 if GRAB_MODE == "aggressive" else GRAB_HEADROOM
        if pl["reach"] - 1 < self._committed(s, p):          # would breach the cap → illegal
            return False
        if headroom < need:
            return False
        if sum(pl["larder"].values()) >= LARDER_CAP:         # nowhere to put the extra
            return False
        return self._hungry(s, p)

    def _hungry(self, s, p):
        """Is there a face-up food vendor this player is currently short of ingredients for?"""
        pl = s["players"][p]
        for vid in self._board(s):
            v = VENDORS[vid]
            if v["is_drink"]:
                continue
            pay = self._pay_plan(s, p, vid)
            if any(pl["larder"].get(r, 0) < c for r, c in pay.items()):
                return True
        return False

    def _do_promote(self, s, p, vid):
        pl = s["players"][p]
        y = min(self._promote_yield(pl), s["supply"])
        # clamp to the Reach cap (defensive; legal_actions already gates)
        y = min(y, pl["reach"] - self._committed(s, p))
        if y <= 0:
            return
        s["supply"] -= y
        s["buzz"][vid][p] += y
        s["promotes"] += 1
        s["max_buzz_on_vendor"] = max(s["max_buzz_on_vendor"], max(s["buzz"][vid]))
        s["max_committed"] = max(s["max_committed"], self._committed(s, p))

    def _do_claim(self, s, p):
        pl = s["players"][p]
        if not s["mrow"]:
            return
        # prefer a ticket we can actually finish in this phase's window (competence fix)
        reachable = [k for k in s["mrow"] if _reachable(s, p, k)]
        pool = reachable if reachable else s["mrow"]
        key = max(pool, key=lambda k: _ticket_keep_score(pl["won"], k, pl["prefs"]))
        s["mrow"].remove(key)
        pl["tickets"].append(key)
        s["claims"] += 1
        if s["mreserve"]:
            s["mrow"].append(s["mreserve"].pop(0))

    def _do_bribe(self, s, p, vid, rng):
        pl = s["players"][p]
        v = VENDORS[vid]
        _plan_pay = self._pay_plan(s, p, vid)
        # CD-4 diagnostic: a FULLY-FREE bribe (all ingredient cost discounted to 0) on a vendor that
        # printed a cost — the exploit the night curve / MIN1_FLOOR guard against.
        if v["total_cost"] > 0 and sum(_plan_pay.values()) <= 0:
            s["free_bribes"] += 1
            if v["phase"] == 2:
                s["free_night_bribes"] += 1
        for r, c in _plan_pay.items():
            pl["larder"][r] -= c
        pl["larder"] = +pl["larder"]
        if pl["bribe_discount"] > 0:
            pl["bribe_discount"] -= 1                        # consume the milestone-14 one-shot
        _, rival_buzz = self._buzz_lead(s, p, vid)
        contested = rival_buzz > 0
        starred = vid in s["star"]
        bookings = v["bookings"] + (STAR_BONUS_P if starred else 0)
        pl["bookings"] += bookings
        pl["won"].append({
            "id": vid, "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "bookings": bookings, "total_cost": v["total_cost"], "contested": contested,
            "starred": starred, "act_won": s["act"], "cross": _is_cross(vid),
            "final_round": s["end_turn"] is not None,
        })
        if not v["is_drink"]:                                # food → discount icon (drinks carry none)
            if v["icon"]:
                pl["icons"][v["region"]] += 1
            if pl["char"] == "councillor" and v["region"] not in pl["councillor_regions"] \
                    and len(pl["councillor_regions"]) < COUNCILLOR_REGIONS:
                pl["councillor_regions"].add(v["region"])
        if starred:
            s["star"].discard(vid); s["star_wins"][p] += 1
        # winning clears YOUR Buzz off it → frees your Reach cap. Rivals' Buzz on it also returns.
        s["supply"] += sum(s["buzz"][vid]); s["buzz"][vid] = [0] * s["n"]
        s["claim_by_region"][v["region"]] += 1
        if v["is_drink"]:
            s["drink_wins"] += 1
        else:
            s["food_wins"] += 1
        if contested:
            s["contested_wins"] += 1
        if v["phase"] == 2:                                  # CD-4: night claims — the climax must fire
            s["night_claims"] += 1
            if not v["is_drink"]:
                s["night_food_wins"] += 1
        if v["phase"] == 2 and s["first_night_win_turn"] is None:
            s["first_night_win_turn"] = s["turn"]
        if pl["char"] == "councillor" and COUNCILLOR_KIT == "home" and not v["is_drink"]:
            if v["region"] == pl["home_region"]:
                s["councillor_home_bribes"] += 1
            else:
                s["councillor_away_bribes"] += 1
        self._remove_and_refill(s, v["region"], vid)
        self._on_claim_clock(s, p)
        self._check_milestones(s, p)                         # after the clock so MS_ON=tickets sees fresh counted_done

    def _ms_meter(self, pl):
        """The track the Rave-Review marks sit on. Bookings (still accrues under tickets_only as an
        ENGINE meter) or the count of tickets this player has completed."""
        if MS_ON == "tickets":
            return len(pl["counted_done"])
        return pl["bookings"]

    def _ms_boon(self, s, p, which, reduced=False):
        pl = s["players"][p]
        if which == 1:
            self._gain_reach(s, p, 1, "ms")                  # Mark 1 → +1 Reach (small; full even reduced)
        else:
            tok = self._most_useful_token(s, p)
            pl["larder"][tok] += 1                           # Mark 2 → 1 ingredient of choice ...
            if not reduced:
                pl["bribe_discount"] += 1                    # ... + next Bribe 1 cheaper (dropped if reduced)
        s[f"ms{7 if which == 1 else 14}_earn"] += 1

    def _check_milestones(self, s, p):
        """Rave Reviews — the boon for crossing each mark. MS_MODE controls runaway: 'first' = table-wide
        first crosser only (v6.3 lock); 'perplayer' = each player the first time THEY cross (no runaway);
        'consolation' = full boon to the first crosser, a reduced boon to a later crosser."""
        pl = s["players"][p]
        m = self._ms_meter(pl)
        t1 = MS_T1 if MS_ON == "tickets" else MS_B1
        t2 = MS_T2 if MS_ON == "tickets" else MS_B2
        for which, thr, flag, sby in ((1, t1, "ms7_done", "ms7_by"), (2, t2, "ms14_done", "ms14_by")):
            if m < thr or pl[flag]:
                continue
            first = s[sby] is None
            if MS_MODE == "first":
                if first:
                    s[sby] = p
                    pl[flag] = True
                    self._ms_boon(s, p, which)
            elif MS_MODE == "perplayer":
                pl[flag] = True
                if first:
                    s[sby] = p
                self._ms_boon(s, p, which)
            else:  # consolation
                pl[flag] = True
                if first:
                    s[sby] = p
                    self._ms_boon(s, p, which)
                else:
                    self._ms_boon(s, p, which, reduced=True)

    def _most_useful_token(self, s, p):
        pl = s["players"][p]
        need = Counter()
        for vid in self._board(s):
            v = VENDORS[vid]
            if v["is_drink"]:
                continue
            for r, c in self._pay_plan(s, p, vid).items():
                short = c - pl["larder"].get(r, 0)
                if short > 0:
                    need[r] += short
        if need:
            return need.most_common(1)[0][0]
        return pl["pos"] if pl["pos"] in REGIONS else COMMON

    def _remove_and_refill(self, s, region, vid):
        up = s["faceup"][region]
        if vid in up:
            up.remove(vid)
        deck = s["vdeck"][region]
        if deck:
            nv = deck.pop()
            up.append(nv)
            s["buzz"].setdefault(nv, [0] * s["n"])

    # -------- the clock (vendor-claims default) --------
    def _on_claim_clock(self, s, p):
        s["vendor_claims"] += 1
        self._check_mission_completions(s, p)
        if s["clock_mode"] == "vendor":
            if s["act"] == 1 and s["vendor_claims"] >= s["v_dusk"]:
                self._dusk(s)
            if s["vendor_claims"] >= s["v_end"]:
                self._trigger_end(s, "lasttrain")
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
        # v6.3 Change 4: JUDGE all held DAY tickets into the win/lose piles NOW (frozen at dusk).
        # (TA_DAY_JUDGE="end" keeps them held to game end — the v6.2 behaviour — for the A/B diagnosis.)
        for p in range(s["n"]):
            pl = s["players"][p]
            keep = []
            for key in pl["tickets"]:
                ph = TICKETS[key][1]
                is_day = (ph == "d" or key == "g_travel3")
                if is_day and DAY_JUDGE == "dusk":           # DAY pool (incl. the DAY 遍地開花 copy)
                    sc = _judge_ticket(key, pl["won"])
                    pl["day_ticket_score"] += sc
                    if sc >= 0 and _mdone(key, pl["won"]):
                        pl["day_win"] += 1
                    else:
                        pl["day_lose"] += 1
                else:
                    keep.append(key)
            pl["tickets"] = keep
            s["reach_at_dusk"].append(pl["reach"])
            # 網紅 "Late to the Party": miss the FIRST turn of the NIGHT phase
            if pl["char"] == "influencer" and INFL_FLAW == "lateparty":
                pl["skip_next"] = True
        # sweep the day layer island-wide: swap in night vendor decks + fresh night ingredient pools
        for r in REGIONS:
            for vid in list(s["faceup"][r]):
                s["supply"] += sum(s["buzz"].get(vid, [0] * s["n"]))
                s["buzz"][vid] = [0] * s["n"]
                s["star"].discard(vid)
            nd = _region_deck(r, 2)
            self._rng_shuffle(s, nd)
            up = [nd.pop() for _ in range(min(s["slots"][r], len(nd)))]
            s["vdeck"][r] = nd; s["faceup"][r] = up
            for vid in up:
                s["buzz"].setdefault(vid, [0] * s["n"])
            pool = Counter({r: SIG_SUPPLY})
            if r in COMMON_REGIONS:
                pool[COMMON] += K_SUPPLY
            # CD-2: seed the Scheduled-Maintenance marker into the NIGHT deck (default MAINT_PHASE==2).
            if MAINT_COUNT > 0 and r == MAINT_REGION and MAINT_PHASE == 2:
                pool[MAINT] += MAINT_COUNT
                s["maint_seeded"] += MAINT_COUNT
            s["ing_pool"][r] = pool
            s["ing_discard"][r] = Counter()
        # the ticket row switches to the NIGHT pool
        rng = s.get("_rng")
        if rng is not None:
            drawn = rng.sample(NIGHT_POOL, min(s["mdraw"], len(NIGHT_POOL)))
        else:
            drawn = NIGHT_POOL[:s["mdraw"]]
        s["mrow"] = drawn[:MROW]
        s["mreserve"] = drawn[MROW:]
        if NIGHT_SPRINT > 0:
            if s["clock_mode"] == "mission":
                s["m_end"] = max(s["completions"] + 1, s["m_end"] - NIGHT_SPRINT)
            else:
                s["v_end"] = max(s["vendor_claims"] + 1, s["v_end"] - NIGHT_SPRINT)

    def _rng_shuffle(self, s, lst):
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
        s["end_turn"] = ((done + n - 1) // n) * n + n

    def _finalize(self, s):
        """At the last train: judge any still-held (NIGHT) tickets into the win/lose piles."""
        if s.get("_finalized"):
            return
        s["_finalized"] = True
        for p in range(s["n"]):
            pl = s["players"][p]
            night = 0
            for key in pl["tickets"]:
                night += _judge_ticket(key, pl["won"])
            pl["night_ticket_score"] = night

    # -------- events --------
    def _event_frac(self, s):
        return DAY_EVENT_FRAC if s["act"] == 1 else NIGHT_EVENT_FRAC

    def _draw_market(self, s, r, rng):
        if rng.random() < self._event_frac(s):
            kind = "hazard" if rng.random() < EVENT_HAZARD_FRAC else "boon"
            return _make_event(kind, rng)
        pool = s["ing_pool"][r]
        if sum(pool.values()) == 0:
            pool += s["ing_discard"][r]; s["ing_discard"][r] = Counter()
        if sum(pool.values()) == 0:
            s["empty_draws"] += 1
            return None
        toks = list(pool.elements())
        tok = rng.choice(toks)
        pool[tok] -= 1; pool = +pool; s["ing_pool"][r] = pool
        if tok == MAINT:
            # CD-2: the seeded Scheduled-Maintenance card surfaced — a table-wide event tuple. It FIRES
            # only on a Visit / Convenience-Store flip (Travel whiffs on any event); consumed either way.
            return ("ev", "maint", "table", "hsr")
        return tok

    def _return_token(self, s, tok):
        home = tok if tok != COMMON else "C"
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
        if kind == "maint":
            # CD-2: TABLE-WIDE HSR outage. Close the N↔S hop for ALL players until the start of the
            # drawing player's next turn (one full go-around). At fire time s["turn"] is still the drawing
            # player's turn, so their next turn is s["turn"] + n → reopen when s["turn"] reaches that.
            s["hsr_closed_until_turn"] = s["turn"] + s["n"]
            s["maint_fired"] += 1
            return 0
        s["scope_fired"][scope] += 1
        if kind == "boon" and sub == "star":
            self._place_star(s)
            return 0
        targets = self._event_targets(s, actor, drawn_region, scope)
        penalty = 0
        for t in targets:
            if kind == "hazard":
                if sub == "reach":
                    self._lose_reach(s, t, 1, "event")       # 負評 / 出包 — a −1 Reach ding
                    if t != actor:
                        s["takethat_hits"] += 1
                        if origin == "cstore":
                            s["cs_rival_hits"] += 1
                else:                                        # tempo tax
                    if during_visit and t == actor:
                        penalty += 1
                    else:
                        s["players"][t]["tempo_tax"] += 1
                    if t != actor:
                        s["takethat_hits"] += 1
                        if origin == "cstore":
                            s["cs_rival_hits"] += 1
            else:                                            # boon
                if sub == "reach":
                    self._gain_reach(s, t, 1, "event")       # "word spreads" — +1 Reach
                else:                                        # ingredient windfall (the region's signature)
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
        tgt = min(cand, key=lambda vid: VENDORS[vid]["bookings"])
        s["star"].add(tgt); s["star_placed"] += 1

    # -------- sourcing --------
    def _keep_cap(self, pl):
        if pl["char"] == "dagushi":
            return 3
        if pl["char"] == "office":
            return 2 if OFFICE_BUFF == "keep2" else 1
        return 2

    def _bump_src(self, s):
        """CD-4 probe #1: a sourcing action (Visit / Convenience Store / Travel), counted per game-half."""
        if s["act"] == 1:
            s["src_actions_day"] += 1
        else:
            s["src_actions_night"] += 1

    def _do_visit(self, s, p, rng):
        pl = s["players"][p]
        r = pl["pos"]
        s["visits"] += 1
        self._bump_src(s)
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
        # v6.3 Greedy Grab (Visit touchpoint): keep +1 more for −1 Reach, if affordable & useful
        if GRAB_MODE in ("visit", "both", "aggressive") and len(toks) > keep and self._greedy_grab_ok(s, p):
            keep += 1
            self._lose_reach(s, p, 1, "grab")
            s["greedy_visit"] += 1
        kept = toks[:keep]
        for c in kept:
            pl["larder"][c] += 1
            if c == COMMON:
                s["src_common"] += 1
            else:
                s["src_by_region"][c] += 1
        for c in toks[keep:]:
            self._return_token(s, c)

    def _do_cstore(self, s, p, r, rng):
        pl = s["players"][p]
        s["cstores"] += 1
        self._bump_src(s)
        c = self._draw_market(s, r, rng)
        grabbed = False
        if isinstance(c, str):
            got = self._apply_tempo_tax(pl, 1)
            if got > 0:
                pl["larder"][c] += 1
                if c == COMMON:
                    s["src_common"] += 1
                else:
                    s["src_by_region"][c] += 1
                grabbed = True
            else:
                self._return_token(s, c)
        elif isinstance(c, tuple):
            self._fire_event(s, p, r, c, rng, during_visit=False, origin="cstore")
        # v6.3 Greedy Grab (Convenience Store touchpoint): take the NEXT card too for −1 Reach
        if grabbed and GRAB_MODE in ("both", "aggressive") and self._greedy_grab_ok(s, p):
            c2 = self._draw_market(s, r, rng)
            if isinstance(c2, str):
                pl["larder"][c2] += 1
                if c2 == COMMON:
                    s["src_common"] += 1
                else:
                    s["src_by_region"][c2] += 1
                self._lose_reach(s, p, 1, "grab")
                s["greedy_cs"] += 1
            elif isinstance(c2, tuple):
                self._fire_event(s, p, r, c2, rng, during_visit=False, origin="cstore")

    def _do_travel(self, s, p, dest, rng):
        pl = s["players"][p]
        src = pl["pos"]
        pl["pos"] = dest
        s["travels"] += 1
        s["inter_moves"] += 1
        self._bump_src(s)
        self._gain_reach(s, p, REACH_TRAVEL, "travel")       # v6.3: Travel is the engine's fuel line
        draw_region = src if pl["char"] == "office" else dest
        n_draw = 2 if (pl["char"] == "office" and OFFICE_BUFF == "travel2") else 1
        for _ in range(n_draw):
            c = self._draw_market(s, draw_region, rng)
            if isinstance(c, str):                           # an event on a Travel fly-by whiffs (no fire)
                got = self._apply_tempo_tax(pl, 1)
                if got > 0:
                    pl["larder"][c] += 1
                    if c == COMMON:
                        s["src_common"] += 1
                    else:
                        s["src_by_region"][draw_region] += 1
                else:
                    self._return_token(s, c)
            elif isinstance(c, tuple) and c[1] == "maint":
                # CD-2: the Scheduled-Maintenance card only FIRES on a Visit/CStore flip. A Travel flyby
                # that surfaces it must NOT waste it — return the marker to the deck so it keeps waiting.
                s["ing_pool"][draw_region][MAINT] += 1

    def _discard_to_cap(self, s, pl):
        total = sum(pl["larder"].values())
        if total <= LARDER_CAP:
            return
        for _ in range(total - LARDER_CAP):
            tok = max((k for k in pl["larder"] if pl["larder"][k] > 0),
                      key=lambda k: pl["larder"][k])
            pl["larder"][tok] -= 1
            home = tok if tok != COMMON else "C"
            s["ing_discard"][home][tok] += 1
        pl["larder"] = +pl["larder"]

    # -------- scoring --------
    def _ticket_score(self, pl):
        return pl.get("day_ticket_score", 0) + pl.get("night_ticket_score", 0)

    def scores(self, s):
        if not s.get("_finalized"):
            self._finalize(s)
        out = {}
        for p in range(s["n"]):
            pl = s["players"][p]
            book = pl["bookings"] if SCORING == "both" else 0   # tickets_only: vendors don't score
            base = book + self._ticket_score(pl)
            # v6.3 tiebreak folded as a tiny fractional term: most vendors → most regions →
            # fewest lose-pile tickets (so the harness's max() picks the right winner).
            st = _wstat(pl["won"])
            lose = pl.get("day_lose", 0) + sum(1 for k in pl["tickets"] if not _mdone(k, pl["won"]))
            tie = 1e-3 * st["n"] + 1e-4 * len(st["regions"]) - 1e-5 * lose
            out[p] = base + tie
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
        end_reach = [s["players"][p]["reach"] for p in range(s["n"])]
        ms_both_same = 1.0 if (s["ms7_by"] is not None and s["ms7_by"] == s["ms14_by"]) else 0.0
        ms_both_fired = 1.0 if (s["ms7_by"] is not None and s["ms14_by"] is not None) else 0.0
        # CD-4 probe #1: day/night sourcing RATE (actions per turn in each half) + the night:day ratio.
        day_src_rate = (s["src_actions_day"] / s["turns_day"]) if s["turns_day"] else 0.0
        night_src_rate = (s["src_actions_night"] / s["turns_night"]) if s["turns_night"] else 0.0
        night_day_src_ratio = (night_src_rate / day_src_rate) if day_src_rate else 0.0
        c_home = s["councillor_home_bribes"]; c_away = s["councillor_away_bribes"]
        c_tot = c_home + c_away
        hp = s["home_pick"]; hp_tot = sum(hp.values()) or 1

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
            "max_committed": float(s["max_committed"]),
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
            "promotes_per_game": float(s["promotes"]),
            "passes_per_game": float(s["passes"]),
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
            "empty_draws_per_game": float(s["empty_draws"]),
            "claims_per_game": float(s["claims"]),
            # --- REACH economy ---
            "reach_start": float(REACH_START),
            "reach_blocked_per_game": float(s["reach_blocked"]),
            "reach_gain_travel": float(s["reach_gain_travel"]),
            "reach_gain_event": float(s["reach_gain_event"]),
            "reach_gain_ms": float(s["reach_gain_ms"]),
            "reach_loss_grab": float(s["reach_loss_grab"]),
            "reach_loss_event": float(s["reach_loss_event"]),
            "reach_forced_return": float(s["reach_forced_return"]),
            "greedy_visit_per_game": float(s["greedy_visit"]),
            "greedy_cs_per_game": float(s["greedy_cs"]),
            "greedy_grab_per_game": float(s["greedy_visit"] + s["greedy_cs"]),
            "reach_zero_turns": float(s["reach_zero_turns"]),
            "reach_mean_all": float(statistics.mean(s["reach_samples"])) if s["reach_samples"] else 0.0,
            "reach_at_dusk_mean": float(statistics.mean(s["reach_at_dusk"])) if s["reach_at_dusk"] else 0.0,
            "reach_end_mean": float(statistics.mean(end_reach)),
            # --- milestones (Rave Reviews) ---
            "ms7_fired": 1.0 if s["ms7_by"] is not None else 0.0,
            "ms14_fired": 1.0 if s["ms14_by"] is not None else 0.0,
            "ms_both_fired": ms_both_fired,
            "ms_both_same_player": ms_both_same,
            "ms_both_same_given_both": (ms_both_same if ms_both_fired else 0.0),
            "ms7_earn_players": float(s["ms7_earn"]),        # #players who got mark-1 boon (>1 spreads it)
            "ms14_earn_players": float(s["ms14_earn"]),
            # --- v6.3.1 CD-4 probe #1: day/night sourcing ---
            "src_day_per_turn": float(day_src_rate),
            "src_night_per_turn": float(night_src_rate),
            "night_day_src_ratio": float(night_day_src_ratio),
            "night_claims_per_player": float(s["night_claims"] / s["n"]),
            "night_food_wins_per_player": float(s["night_food_wins"] / s["n"]),
            "free_bribes_per_game": float(s["free_bribes"]),
            "free_night_bribes_per_game": float(s["free_night_bribes"]),
            "turns_night_frac": float(s["turns_night"] / s["turn"]) if s["turn"] else 0.0,
            # --- v6.3.1 CD-2 Scheduled Maintenance ---
            "maint_seeded_per_game": float(s["maint_seeded"]),
            "maint_fired_per_game": float(s["maint_fired"]),
            "maint_fired_rate": 1.0 if s["maint_fired"] > 0 else 0.0,
            "maint_closed_turns_per_game": float(s["maint_closed_turns"]),
            # --- v6.3.1 CD-1 councillor home/away ---
            "councillor_home_bribes": float(c_home),
            "councillor_away_bribes": float(c_away),
            "councillor_away_frac": float(c_away / c_tot) if c_tot else 0.0,
            "home_pick_N": float(hp.get("N", 0) / hp_tot), "home_pick_C": float(hp.get("C", 0) / hp_tot),
            "home_pick_S": float(hp.get("S", 0) / hp_tot), "home_pick_E": float(hp.get("E", 0) / hp_tot),
            # --- score breakdown (winner) ---
            "win_bookings": float(wp["bookings"]),
            "win_ticket_score": float(self._ticket_score(wp)),
            "win_total": float(int(round(best))),
            "tickets_held_winner": float(len(wp["tickets"])),
        }


GAME = TravelAgentsGame()
TITLE = "Travel Agents: Taiwan (v6.3.1 — four CD reworks: home-region 里長伯 · Maintenance · Taipei start · night curve)"


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
    if v["is_drink"] or not v["icon"]:
        return 0.0
    held = pl["icons"].get(v["region"], 0)
    return w * (0.5 + 0.4 * held)


def _tickets_marginal(s, p, vid):
    pl = s["players"][p]
    v = VENDORS[vid]
    cand = {"id": v["id"], "region": v["region"], "is_drink": v["is_drink"], "phase": v["phase"],
            "bookings": v["bookings"], "total_cost": v["total_cost"],
            "contested": False, "starred": vid in s["star"], "act_won": s["act"],
            "cross": _is_cross(vid), "final_round": s["end_turn"] is not None}
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
    bookings = v["bookings"] + (STAR_BONUS_P if vid in s["star"] else 0)
    # under tickets_only, Bookings no longer SCORE — a vendor's value is only an engine-quality proxy,
    # so down-weight the raw-Bookings term and let ticket-completion (below) drive target choice.
    bw = 1.0 if SCORING == "both" else BOOK_ENGINE_W
    core = bookings * bw
    if not v["is_drink"]:
        core += _ramp_value(pl, v, prefs.get("w_ramp", 1.0))
        core *= prefs.get("w_food", 1.0)
    else:
        core *= prefs.get("w_drink", 1.0)
    if prefs.get("opportunistic") and (vid in s["star"] or v["bookings"] >= 6):
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
        if s["buzz"][vid][p] > 0:
            score += 0.4
        if score > bscore:
            bscore, best = score, vid
    return best


def _token_source(s, p, tok, legal, prefs):
    pl = s["players"][p]
    ho = _hsr_is_open(s)
    if tok == COMMON:
        targets = list(COMMON_REGIONS)
    else:
        targets = [tok]
    if pl["pos"] in targets and ("visit",) in legal:
        return ("visit",)
    dest = min(targets, key=lambda r: _dist(pl["pos"], r, pl["char"], ho))
    if pl["pos"] == dest and ("visit",) in legal:
        return ("visit",)
    hop = _next_hop(pl["pos"], dest, pl["char"], ho)
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


def _claim_window(s, p):
    """A player's remaining vendor-claim budget before the CURRENT phase's ticket-judging trigger
    (DAY tickets judged at dusk, NIGHT at the last train — v6.3 Change 4). Used so the bot doesn't
    speculatively claim a ticket it can't finish inside its phase window (a competence fix — a human
    wouldn't claim an un-finishable day ticket at dusk-minus-one)."""
    if s["clock_mode"] == "vendor":
        if s["act"] == 1:
            remaining = max(0, s["v_dusk"] - s["vendor_claims"])
        else:
            remaining = max(0, s["v_end"] - s["vendor_claims"])
    else:
        remaining = 6
    return max(1, (remaining + s["n"] - 1) // s["n"])       # my ~fair share of the remaining claims


def _reachable(s, p, key):
    """Can this player plausibly COMPLETE ticket `key` within its phase window (in vendor claims)?"""
    pl = s["players"][p]
    d, n = _mprog(key, _wstat(pl["won"]))
    if d >= n:
        return True
    gap = n - d
    # bookings-count tickets gain ~4 per claim; everything else ~1 progress per claim
    per_claim = 4.0 if key in ("d_prestige8", "n_prestige14", "g_prestige12") else 1.0
    needed_claims = (gap + per_claim - 1) // per_claim if per_claim == 1.0 else (gap / per_claim)
    return needed_claims <= _claim_window(s, p)


def _should_claim(s, p, legal, prefs):
    if ("claim",) not in legal or prefs.get("no_tickets"):
        return False
    pl = s["players"][p]
    incomplete = [k for k in pl["tickets"] if not _mdone(k, pl["won"])]
    limit = 3 if prefs.get("speed") else 2
    if s["clock_mode"] == "mission":
        room = s["completions"] < s["m_end"] - 1
    else:
        room = s["vendor_claims"] < s["v_end"] - 1
    if not (len(incomplete) < limit and room):
        return False
    # only claim if the row holds a ticket we can realistically FINISH in this phase's window
    return any(_reachable(s, p, k) for k in s["mrow"])


def _any_travel(s, p, legal, toward=None):
    """A Travel action — toward a region if given, else any legal hop (used to farm Reach when the cap
    blocks a Promote the bot wants to make)."""
    pl = s["players"][p]
    if toward is not None:
        hop = _next_hop(pl["pos"], toward, pl["char"], _hsr_is_open(s))
        if ("travel", hop) in legal:
            return ("travel", hop)
    for a in legal:
        if a[0] == "travel":
            return a
    return None


def _plan(s, p, legal, rng, prefs):
    pl = s["players"][p]
    if legal == [("pass",)]:
        return ("pass",)

    # 1) a bribe that fits the road always progresses
    bribes = [a for a in legal if a[0] == "bribe"
              and not (prefs.get("pure_drinks") and not VENDORS[a[1]]["is_drink"])
              and not (prefs.get("no_drinks") and VENDORS[a[1]]["is_drink"])]
    if bribes:
        return max(bribes, key=lambda a: _road_value(s, p, a[1], prefs))

    # 2) hoarder overlay
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

    # 4) get on-site if short the local ingredient, else route toward the target
    if not present:
        pos = pl["pos"]
        if need.get(pos, 0) > 0 and ("visit",) in legal:
            return ("visit",)
        if need.get(COMMON, 0) > 0 and pos in COMMON_REGIONS and ("cstore", pos) in legal:
            return ("cstore", pos)
        hop = _next_hop(pos, eff, pl["char"], _hsr_is_open(s))
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

    # 6) win the Buzz fight — Reach-cap-aware
    if lead < margin and present:
        if ("promote", tgt) in legal:
            return ("promote", tgt)
        # the ingredients are ready and we're present, but the Reach cap forbids the Promote →
        # Travel to build Reach (the intended play: travel is the fight's fuel). Record the block.
        if s["supply"] > 0 and GAME._committed(s, p) + GAME._promote_yield(pl) > pl["reach"]:
            s["reach_blocked"] += 1
            mv = _any_travel(s, p, legal)
            if mv is not None:
                return mv
    if lead < margin and not present:
        hop = _next_hop(pl["pos"], eff, pl["char"], _hsr_is_open(s))
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
MIXPREFS = {**BAL, "w_drink": 1.1, "w_ticket": 1.15}
IGNORE_OBJ = {**BAL, "no_tickets": True, "no_drinks": True}
PURE_DRINKS = {"w_val": 1.0, "w_food": 0.0, "w_drink": 1.0, "w_ramp": 0.0, "pure_drinks": True, "w_ticket": 1.0}
NO_DRINKS = {**BAL, "no_drinks": True}


def s_random(s, p, legal, rng):
    return rng.choice(legal)


def s_greedy_bookings(s, p, legal, rng):
    if legal == [("pass",)]:
        return ("pass",)
    bribes = [a for a in legal if a[0] == "bribe"]
    if bribes:
        return max(bribes, key=lambda a: VENDORS[a[1]]["bookings"])
    return _plan(s, p, legal, rng, BAL)


STRATEGIES = {
    "random":        s_random,
    "greedy_book":   s_greedy_bookings,
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
    "random": BAL, "greedy_book": BAL, "balanced": BAL, "opportunistic": OPPORTUNISTIC,
    "disruptive": DISRUPTIVE, "endgame": ENDGAME, "mix": MIXPREFS, "ignore_obj": IGNORE_OBJ,
    "pure_drinks": PURE_DRINKS, "no_drinks": NO_DRINKS,
}


# ==================================================================================================
#  A rng-threaded wrapper so dusk() can shuffle the night decks deterministically.
# ==================================================================================================
class _Seeded:
    def __init__(self, n=2, characters=None, prefs=None):
        self.n, self.characters, self.prefs = n, characters, prefs

    def new_state(self, rng, n=None):
        st = GAME.new_state(rng, n or self.n, characters=self.characters, prefs=self.prefs)
        st["_rng"] = rng
        return st

    def __getattr__(self, k):
        return getattr(GAME, k)


# ==================================================================================================
#  __main__ — the v6.3 probe suite
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


def _char_metrics(ch, n=1200, seed=1, prefs=None):
    """Run char (seat 0) vs neutral and return the averaged metrics — for the character-specific
    diagnostics (里長伯 home-pick distribution + away-tax incidence) that the neutral field can't show."""
    pr = prefs or BAL
    _, _, _, mt = _run({0: STRATEGIES["balanced"], 1: STRATEGIES["balanced"]},
                       n=n, seed=seed, characters=[ch, "neutral"], prefs=[pr, BAL])
    return mt


def _field_metrics(n=1500, seed=1):
    _, _, _, mt = _run({0: STRATEGIES["balanced"], 1: STRATEGIES["balanced"]},
                       n=n, seed=seed, prefs=[BAL, BAL])
    return mt


if __name__ == "__main__":
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _SIM = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "tools", "sim"))
    if _SIM not in sys.path:
        sys.path.insert(0, _SIM)

    if "--counts" in sys.argv:
        counts = [2, 3, 4]
        print(f"# {TITLE} — seat balance by player count (self-play: balanced)\n")
        from engine import seat_balance
        for c in counts:
            g = _Seeded(c)
            r = seat_balance(g, STRATEGIES["balanced"], c, n=800)
            flag = "SUSPECT" if r["suspect"] else "ok"
            wr = "  ".join(f"seat{p}={v*100:.0f}%" for p, v in r["seat_win_rate"].items())
            print(f"  {c}p  {flag}  (fair {r['fair_share']*100:.0f}%)  {wr}  ties={r['tie_rate']*100:.0f}%")
        sys.exit(0)

    N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1200
    print(f"# {TITLE} — v6.3.1 probe suite ({N} games/cell)\n")
    print(f"  KNOBS: NIGHT_CURVE={int(NIGHT_CURVE)} MIN1_FLOOR={int(MIN1_FLOOR)} "
          f"START_SPLIT={int(START_SPLIT)} COUNCILLOR_KIT={COUNCILLOR_KIT} "
          f"MAINT={MAINT_COUNT}@{MAINT_REGION}/ph{MAINT_PHASE}  "
          f"(SCORING={SCORING} TICKETS={TICKET_SET} MS_MODE={MS_MODE})\n")

    print("## Game arc (balanced mirror)")
    mt = _field_metrics(n=N)
    print(f"  turns/player {mt['turns_per_player']:.1f}  vendors/player {mt['wins_per_player']:.1f}  "
          f"winner {mt['win_total']:.1f} (Bookings {mt['win_bookings']:.1f} / Tickets {mt['win_ticket_score']:.1f})")
    print(f"  dusk turn {mt['dusk_turn']:.1f}  last-train {mt['last_turn']:.1f}  "
          f"end: LT {mt['end_by_lasttrain']*100:.0f}% deck {mt['end_by_deck']*100:.0f}% stall {mt['end_by_stall']*100:.0f}%")
    print(f"  contested-win frac {mt['contested_frac']*100:.1f}%  max_buzz {mt['max_buzz_on_vendor']:.1f}  "
          f"max_committed {mt['max_committed']:.1f}  drink-win share {mt['drink_win_share']*100:.0f}%  "
          f"claims/gm {mt['claims_per_game']:.1f}")
    print(f"  CLAIM share  N {mt['claim_share_N']*100:.0f}% C {mt['claim_share_C']*100:.0f}% "
          f"S {mt['claim_share_S']*100:.0f}% E {mt['claim_share_E']*100:.0f}%")
    print(f"  SRC   share  N {mt['src_share_N']*100:.0f}% C {mt['src_share_C']*100:.0f}% "
          f"S {mt['src_share_S']*100:.0f}% E {mt['src_share_E']*100:.0f}% K {mt['src_share_common']*100:.0f}%")
    print(f"  moves/gm {mt['inter_moves']:.1f}  promotes/gm {mt['promotes_per_game']:.1f}  "
          f"forced_turn_frac {mt['forced_turn_frac']:.3f}  avg_legal {mt['avg_legal_actions']:.1f}")

    print("\n## ★ PROBE #1 — day/night SOURCING split (CD-4 night curve: does sourcing stay live at night?)")
    print(f"  sourcing/turn: DAY {mt['src_day_per_turn']:.2f}  NIGHT {mt['src_night_per_turn']:.2f}  "
          f"→ night is {mt['night_day_src_ratio']*100:.0f}% of day  (GOAL ~60-100%; FAIL = collapse→0)")
    print(f"  night claims/player {mt['night_claims_per_player']:.2f}  night-food/player {mt['night_food_wins_per_player']:.2f}  "
          f"first-night-Bribe turn {mt['first_night_win_turn']:.1f}  (over-correction watch: claims must not thin out)")
    print(f"  FREE (zero-ingredient) bribes/gm: all {mt['free_bribes_per_game']:.2f}  night {mt['free_night_bribes_per_game']:.2f}  "
          f"(the exploit CD-4 guards — MIN1_FLOOR only earns its keep if this is non-trivial)")
    print(f"  end: LT {mt['end_by_lasttrain']*100:.0f}% deck {mt['end_by_deck']*100:.0f}% "
          f"stall {mt['end_by_stall']*100:.0f}%  (drag/stall watch — night must stay reachable-with-a-good-engine)")

    print("\n## PROBE #1 curve level A/B — 0 off / 1 soft (default) / 2 steep / 1+MIN1_FLOOR")
    for lbl, lvl, flr in (("0 off (raw v6.3)", 0, False), ("1 soft (DEFAULT)", 1, False),
                          ("1 soft +MIN1_FLOOR", 1, True), ("2 steep", 2, False)):
        globals()["NIGHT_CURVE"] = lvl; globals()["MIN1_FLOOR"] = flr
        _rebuild_vendors()
        m = _field_metrics(n=max(400, N // 2))
        print(f"  {lbl:22} night/day-src {m['night_day_src_ratio']*100:3.0f}%  "
              f"night-claims/plyr {m['night_claims_per_player']:.2f}  "
              f"1st-night turn {m['first_night_win_turn']:.1f}  LT {m['end_by_lasttrain']*100:.0f}%  "
              f"stall {m['end_by_stall']*100:.0f}%  turns/plyr {m['turns_per_player']:.1f}")
    globals()["NIGHT_CURVE"] = 1; globals()["MIN1_FLOOR"] = False; _rebuild_vendors()

    print("\n## CD-2 — Scheduled Maintenance (table-wide HSR outage) — fires? symmetric? no dead stretch")
    print(f"  seeded/gm {mt['maint_seeded_per_game']:.2f}  fired/gm {mt['maint_fired_per_game']:.2f}  "
          f"fired-at-least-once {mt['maint_fired_rate']*100:.0f}%  HSR-closed turns/gm {mt['maint_closed_turns_per_game']:.2f}")

    print("\n## CD-1 — 里長伯 home-region: pick distribution + away-tax incidence (watch: does he camp North?)")
    cm = _char_metrics("councillor", n=N)
    print(f"  home pick:  N {cm['home_pick_N']*100:.0f}%  C {cm['home_pick_C']*100:.0f}%  "
          f"S {cm['home_pick_S']*100:.0f}%  E {cm['home_pick_E']*100:.0f}%")
    print(f"  councillor bribes: home {cm['councillor_home_bribes']:.2f}  away {cm['councillor_away_bribes']:.2f}  "
          f"→ away-tax paid on {cm['councillor_away_frac']*100:.0f}% of his food bribes")

    print("\n## REACH economy (probe 1 — does the Buzz fight BREATHE or CHOKE?)")
    print(f"  reach: start {mt['reach_start']:.0f}  mean(all turns) {mt['reach_mean_all']:.1f}  "
          f"at dusk {mt['reach_at_dusk_mean']:.1f}  at end {mt['reach_end_mean']:.1f}  "
          f"turns@0 {mt['reach_zero_turns']:.2f}")
    print(f"  reach GAIN: travel {mt['reach_gain_travel']:.1f}  event {mt['reach_gain_event']:.1f}  "
          f"milestone {mt['reach_gain_ms']:.2f}   LOSS: grab {mt['reach_loss_grab']:.1f}  "
          f"event {mt['reach_loss_event']:.1f}  forced-return {mt['reach_forced_return']:.2f}")
    print(f"  REACH-BLOCKED promotes/gm {mt['reach_blocked_per_game']:.2f}  "
          f"(a Promote the bot wanted but the cap forbade → it Travelled to build Reach instead)")
    print(f"  GREEDY GRABS/gm: visit {mt['greedy_visit_per_game']:.2f}  cstore {mt['greedy_cs_per_game']:.2f}  "
          f"total {mt['greedy_grab_per_game']:.2f}")

    print("\n## MILESTONES (Rave Reviews — race vs runaway)")
    print(f"  mark-7 fired {mt['ms7_fired']*100:.0f}%  mark-14 fired {mt['ms14_fired']*100:.0f}%  "
          f"both fired {mt['ms_both_fired']*100:.0f}%  "
          f"SAME player took both (given both fired) {mt['ms_both_same_given_both']*100:.0f}%")

    print("\n## PROBE 3 — the five playstyles vs each other + naive (win% vs the field)")
    field = ["balanced", "opportunistic", "disruptive", "endgame", "mix"]
    for a in field:
        wr = statistics.mean([_versus(a, b, n=N // 2) for b in field if b != a])
        crush = _versus(a, "random", n=N // 3)
        print(f"  {a:14} avg vs field {wr*100:5.1f}%   vs random {crush*100:4.0f}%")
    nd = statistics.mean([_versus("no_drinks", b, n=N // 2) for b in field])
    print(f"  {'no_drinks':14} avg vs field {nd*100:5.1f}%   (ignore-drinks control — should trail)")

    print("\n## PROBE 3b — a MIX beats the ignore-both control; pure-drinks must lose")
    print(f"  mix         vs ignore_obj  {_versus('mix', 'ignore_obj', n=N)*100:5.1f}%  (want >50)")
    print(f"  balanced    vs ignore_obj  {_versus('balanced', 'ignore_obj', n=N)*100:5.1f}%")
    print(f"  pure_drinks vs balanced    {_versus('pure_drinks', 'balanced', n=N)*100:5.1f}%  (want clearly <50)")

    print("\n## PROBE 4/5 — character balance (char vs neutral, both seatings) — target 45-55%")
    for ch in ("councillor", "office", "influencer", "dagushi", "dage"):
        wr = _char_winrate(ch, n=N)
        flag = "ok" if 0.45 <= wr <= 0.55 else "<-- OUT"
        print(f"  {ch:12} {wr*100:5.1f}%  {flag}")

    print("\n## 網紅 — Late-to-the-Party flaw ON vs OFF (RE-PASS: retired it — 'none' is now the default)")
    for lbl, mode in (("none (RE-PASS default)", "none"), ("lateparty (old lock)", "lateparty")):
        globals()["INFL_FLAW"] = mode
        print(f"  {lbl:22} influencer {_char_winrate('influencer', n=N)*100:5.1f}%")
    globals()["INFL_FLAW"] = "none"

    print("\n## 里長伯 — CD-1 HOME-REGION kit levers (home-disc / away-tax / start-Reach) + legacy A/B")
    _save = (COUNCILLOR_KIT, COUNCILLOR_HOME_DISC, COUNCILLOR_AWAY_TAX, COUNCILLOR_REACH, COUNCILLOR_REGIONS)
    for lbl, kit, disc, tax, cr, rg in (
            ("home d1/t1 (CD-1 default)", "home", 1, 1, -1, 1),
            ("home d1/t1 + start-Reach1", "home", 1, 1, 1, 1),
            ("home d1/t2 (harsher tax)", "home", 1, 2, -1, 1),
            ("home d1/t0 (no away tax)", "home", 1, 0, -1, 1),
            ("legacy REGIONS=1 (old A/B)", "regions", 1, 1, -1, 1)):
        globals()["COUNCILLOR_KIT"] = kit; globals()["COUNCILLOR_HOME_DISC"] = disc
        globals()["COUNCILLOR_AWAY_TAX"] = tax; globals()["COUNCILLOR_REACH"] = cr
        globals()["COUNCILLOR_REGIONS"] = rg
        print(f"  {lbl:28} councillor {_char_winrate('councillor', n=N)*100:5.1f}%")
    (globals()["COUNCILLOR_KIT"], globals()["COUNCILLOR_HOME_DISC"], globals()["COUNCILLOR_AWAY_TAX"],
     globals()["COUNCILLOR_REACH"], globals()["COUNCILLOR_REGIONS"]) = _save

    print("\n## 大哥 — does he drift? (v6.3 lock = D: lead-by-1, no flaw)")
    for lbl, thr, flaw in (("D lead1+none (lock)", 1, "none"), ("A tie+tab", 0, "tab"),
                           ("C lead1+tab", 1, "tab"), ("E tie+nocontest", 0, "nocontest")):
        globals()["DAGE_THRESH"] = thr; globals()["DAGE_FLAW"] = flaw
        print(f"  {lbl:20} dage {_char_winrate('dage', n=N)*100:5.1f}%")
    globals()["DAGE_THRESH"] = 1; globals()["DAGE_FLAW"] = "none"

    print("\n## PROBE 6 — Greedy Grab modes (usage + net Reach drain)")
    for mode in ("off", "visit", "both", "aggressive"):
        globals()["GRAB_MODE"] = mode
        m = _field_metrics(n=N // 2)
        print(f"  grab={mode:10} grabs/gm {m['greedy_grab_per_game']:.2f} "
              f"(V {m['greedy_visit_per_game']:.2f}/CS {m['greedy_cs_per_game']:.2f})  "
              f"reach end {m['reach_end_mean']:.1f}  blocked/gm {m['reach_blocked_per_game']:.2f}  "
              f"contested {m['contested_frac']*100:.1f}%")
    globals()["GRAB_MODE"] = "both"

    print("\n## PROBE 8 — hoarder (over-source a scarce signature to deny) — should LOSE")
    for hr in ("E", "S"):
        hoard = {**BAL, "hoard_region": hr}
        STRATEGIES["_hoard"] = _make(hoard); STRAT_PREFS["_hoard"] = hoard
        wr = _versus("_hoard", "balanced", n=N // 2)
        print(f"  hoard {hr}  vs balanced  {wr*100:5.1f}%  (want <50 = a trap)")
    del STRATEGIES["_hoard"]; del STRAT_PREFS["_hoard"]

    print("\n## PROBE 11 — MP light seat-balance smoke (per count)")
    from engine import seat_balance
    for c in (2, 3, 4):
        g = _Seeded(c)
        r = seat_balance(g, STRATEGIES["balanced"], c, n=600)
        flag = "SUSPECT" if r["suspect"] else "ok"
        wr = "  ".join(f"seat{p}={v*100:.0f}%" for p, v in r["seat_win_rate"].items())
        print(f"  {c}p  {flag}  (fair {r['fair_share']*100:.0f}%)  {wr}  ties={r['tie_rate']*100:.0f}%")
