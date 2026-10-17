# Training plan

Starting point: **17 October 2026.** Comfortable with arrays, loops and
functions; no C++; no Codeforces history.

Target: **ECPC 2027.**

> ⚠️ **Verify the date.** ECPC qualification rounds have historically run in
> the summer, with the finals a few weeks later, but the schedule moves every
> year and is announced by the ECPC organisers. The plan below is laid out in
> *weeks from the start*, not in calendar dates, so a date change shifts the
> finish line without invalidating the phases. Check the official announcement
> and write the real date here.

Assuming the quals land in summer 2027, that is roughly **36 to 40 weeks**.

---

## The honest arithmetic

Qualifying for the ECPC finals from a university team usually means being able
to solve, under time pressure, problems in the Codeforces 1200–1600 band, with
one person on the team who can take a 1700+. Converting that into a schedule:

| | |
|---|---|
| Problems needed to get there | **400–600** |
| Weeks available | ~38 |
| Problems per week | **12–15** |
| Hours per week | **10–12** |

Twelve problems a week is about two a day with one day off. That is the whole
plan. Everything below is organisation around that number.

The number that matters is not hours spent, it is **problems finished** — read,
solved, submitted, accepted, and committed to `problems/`. An hour spent
staring at a problem you then abandon counts for very little; an hour spent on
a problem you then solve counts for a great deal. `git log` is the only
progress report that cannot be fooled.

---

## Phase 1 — Entry cost · weeks 1–3

Goal: C++ stops being an obstacle.

- Lessons 01–05 of `01-Foundations/`.
- 30 problems at Codeforces rating 800. Not for the algorithms — these are
  pure syntax reps. The target is writing a correct 800 in under 10 minutes
  without looking anything up.
- Set up your Codeforces handle and solve in the problemset, not in contests,
  for now.

Checkpoint: `python3 tools/judge.py --all` shows 30 passing problems, and the
template is typed from memory.

## Phase 2 — Core, first half · weeks 4–14

Goal: the algorithms that appear in every contest.

- Lessons 02/01 through 02/06 — sorting and greedy, binary search, graph
  traversal, shortest paths, DSU, topological sort.
- 12 problems a week, rating 900–1300, **chosen by tag to match the lesson**.
  Codeforces problemset filters by tag; use it.
- Start the habit now: every solved problem gets its directory and tests.

Checkpoint (week 14): a 1200-rated problem you have never seen, solved in
under 40 minutes, four times out of five.

## Phase 3 — Core, second half · weeks 15–26

Goal: dynamic programming, which is where most people stall and most problems
are decided.

- Lessons 02/07 through 02/11 — DP, number theory, combinatorics, strings.
- 12 problems a week, rating 1200–1600. At least half tagged `dp`.
- **Begin virtual contests: one every week, 2 hours, Div. 2 rounds, no
  editorials until the clock stops.** Solving is a skill; solving *under a
  clock with four unread problems* is a different skill, and it only trains
  under a clock.

Checkpoint (week 26): consistently 3 problems in a Div. 2 virtual round.

## Phase 4 — Team and contest form · weeks 27–34

Goal: stop training as an individual.

- ECPC is three people, one machine. Find the team now, not in month nine.
- Weekly 5-hour team virtual contest on past ECPC / ACPC problem sets, mirrored
  in `ECPC-Prep/`.
- Divide the reading: who opens the problem set from the front, who from the
  back, who writes the implementation while the others read.
- Build the printed team reference document from code **you** wrote in this
  repo. That constraint is the point.
- Selected tier 03 topics, chosen by what the past sets actually use —
  segment trees and LCA usually earn their place, flows usually do not.

Checkpoint: a past ECPC set with a score that would have qualified.

## Phase 5 — Sharpening · weeks 35–38

Goal: do not learn anything new. Get fast and stop making errors.

- No new topics. New topics this late cost confidence and buy nothing.
- Two timed team contests a week, with a real penalty-time count.
- Re-solve problems you failed earlier, from scratch, without your old code.
- Review your own wrong submissions and classify them: wrong algorithm,
  wrong implementation, or wrong reading of the statement. The third category
  is usually the largest, and it is the cheapest to fix.

---

## Rules that make the difference

**The 30-minute rule.** Stuck on a problem for 30 minutes with no progress:
read the editorial, understand it completely, then close it and implement from
scratch with nothing on screen. Three hours of unproductive staring teaches
less than one editorial read properly. Mark it in `meta.json`
(`"solved_without_help": false`) and re-solve it two weeks later from a blank
file.

**Never copy an accepted solution.** Not from an editorial, not from a
friend, not from a model. The typing is where the learning happens. A solution
you pasted will not be there in the contest hall.

**Stress test before you suspect.** The moment a submission comes back WA on a
hidden test, do not reread the code. Write `gen.py` and `brute.py` and let
`tools/stress.py` find the case. Five minutes of mechanical work beats an hour
of staring, every time. See
[lesson 05](01-Foundations/lessons/05-stress-testing.md).

**Volume over perfection.** Twelve problems solved adequately beats three
solved beautifully. Contest programming rewards pattern recognition, and
patterns come from count.

**One day off a week, taken deliberately.** Thirty-eight weeks is long enough
that burnout is the most likely way this plan fails — more likely than any
topic being too hard.
