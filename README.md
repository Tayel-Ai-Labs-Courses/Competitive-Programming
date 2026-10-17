# Competitive Programming

Training repository aimed at the **Egyptian Collegiate Programming Contest
(ECPC)** and what comes after it — ACPC, and ICPC if it goes well.

Part of the [Tayel AI Labs course family](https://github.com/Tayel-Ai-Labs-Courses).
Unlike the other repos here, this one is not a course you read. It is a gym.
The lessons are short; the problem log is the real artifact.

---

## The language question, answered once

**C++ is the contest language. Every solution in `problems/` is C++.**

This is not a matter of taste. ICPC and ECPC time limits are calibrated against
C++ reference solutions, so a problem whose intended solution is O(n log n) at
n = 2·10⁵ passes in C++ and times out in Python. You lose problems you *solved
correctly*. Measured on the machine this repo was built on:

| 10⁸ additions in a loop | time |
|---|---|
| C++, `-O2` | **0.17 s** |
| Python 3.12 | 4.28 s |

Twenty-five times. A two-second limit does not forgive that.

The good news is that everything people hate about C++ is absent from
competitive programming. No classes, no header files, no CMake, no pointers, no
memory management, no template metaprogramming. The contest subset is about
forty lines of syntax plus the STL — see
[lesson 01](01-Foundations/lessons/01-cpp-for-python-programmers.md), written
specifically for someone who thinks in Python.

**Python appears in exactly two places**, and nowhere else:

1. `brute.py` — the slow, obviously-correct oracle that `tools/stress.py` uses
   to find the test case your C++ is wrong on. This is the single most
   effective debugging technique in contest programming, and Python's brevity
   is a genuine advantage for a throwaway O(n³) checker.
2. A short **"the same algorithm in Python"** section at the end of each
   lesson — because these algorithms are not only for contests. When a
   shortest path, a union-find or a segment tree turns up in a system you are
   building or in an AI project, you will want the Python version at hand.

The repo is C++ first. Python is a tool inside it, not a second track.

---

## Layout

| Path | What it is |
|---|---|
| `01-Foundations/` | C++ for a Python programmer, the template, complexity, the STL, stress testing |
| `02-Core-Algorithms/` | Binary search, greedy, graphs, DSU, DP, number theory, strings |
| `03-Advanced/` | Segment trees, trees and LCA, flows, geometry, bitmask DP |
| `ECPC-Prep/` | Past-contest mirrors, timed virtual rounds, team strategy |
| `problems/` | Every problem solved, as a directory with its tests. The log. |
| `templates/` | The contest template, and [why every line is in it](templates/README.md) |
| `tools/` | Local judge, stress tester, problem scaffolder. Standard library only. |
| `include/bits/stdc++.h` | Hand-written, because Apple clang does not ship it |

Start at [`CURRICULUM.md`](CURRICULUM.md) for the order, and
[`TRAINING-PLAN.md`](TRAINING-PLAN.md) for the week-by-week schedule.
[`NOTES.md`](NOTES.md) is the same material explained in Arabic, including
every bug hit while building this repo.

---

## The three commands

```bash
python3 tools/new_problem.py codeforces 4A "Watermelon"   # scaffold
python3 tools/judge.py problems/codeforces/4a-watermelon  # compile, run, diff
python3 tools/stress.py problems/practice/max-subarray-sum # hunt the bad case
```

Add `--debug` to `judge.py` to rebuild with AddressSanitizer and
UndefinedBehaviorSanitizer, which turn an out-of-bounds `vector` access from a
silent wrong answer into an error message with a line number.

```bash
python3 tools/judge.py --all
python3 tools/check_links.py
```

These two are what CI runs. `--all` re-judges every committed solution; a
problem that has been scaffolded but not solved yet is reported as `pending`
rather than counted as a pass, so an empty solution cannot show a green tick.

No pip install, no package manager, no virtualenv. Python 3 and `g++`, both of
which are already on the machine.

---

## The rule this repo is built on

**Nothing is committed to `problems/` until `tools/judge.py` says AC.**

Not "I think this is right", not "it passed the sample in my head". A solution
in this repository has been compiled and run against its tests by the machine.
The same standard as the sibling
[Advanced-AI](https://github.com/Tayel-Ai-Labs-Courses/Advanced-AI) and
[Cyber-Ai](https://github.com/Tayel-Ai-Labs-Courses/Cyber-Ai) repos, where every
printed number is a real run. CI enforces it on every push.

The second rule follows from the first: **when a stress test finds a failing
case, that case becomes a permanent test file.** It is the one bug you are
guaranteed never to make twice. `problems/practice/max-subarray-sum/tests/01-all-negative.in`
is such a file — the stress tester produced it, and it is now a regression test.

---

## Honest expectations

Contest results are not a linear function of effort, and no repository makes
anyone win. What this one does is remove every excuse: the setup works, the
feedback is instant, and the record of what you have actually solved is in git
rather than in memory. The hard part stays where it belongs — about 400–600
problems between here and being competitive, solved one at a time.
