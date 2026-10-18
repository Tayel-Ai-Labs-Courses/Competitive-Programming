# Curriculum

> Lost? [`MAP.md`](MAP.md) draws all of this, plus the dependency graph showing
> which topic needs which.

The definitive order. Topics are listed in the sequence they should be learned,
because most of them depend on the ones above. A lesson marked ✅ is written;
the rest are planned and will be written as the training reaches them.

Each lesson is short on purpose — perhaps fifteen minutes of reading — followed
by a problem list. **The reading is not the work. The problems are the work.**
A ratio of one hour reading to ten hours solving is about right.

---

## 01 · Foundations

The entry cost. Three weeks, and you will never revisit most of it.

| # | Lesson | Status |
|---|---|---|
| 01 | [C++ for a Python programmer](01-Foundations/lessons/01-cpp-for-python-programmers.md) — the whole contest subset of the language | ✅ |
| 02 | [The template, and input/output](01-Foundations/lessons/02-the-template-and-io.md) — with measured numbers for why `cin` is dangerous | ✅ |
| 03 | [Complexity, and reading the constraints](01-Foundations/lessons/03-complexity-and-constraints.md) — how n tells you the algorithm before you think | ✅ |
| 04 | [The eight STL containers worth knowing](01-Foundations/lessons/04-stl-containers.md) | ✅ |
| 05 | [Stress testing: finding the hidden failing test](01-Foundations/lessons/05-stress-testing.md) | ✅ |
| 06 | Prefix sums and two pointers | planned |

## 02 · Core Algorithms

This tier is the bulk of ECPC. A team that is solid on everything here and fast
on implementation qualifies.

| # | Lesson | Status |
|---|---|---|
| 01 | Sorting, and greedy with an exchange argument | planned |
| 02 | Binary search — on an array, and on the answer | planned |
| 03 | Graph representation, BFS, DFS, connected components | planned |
| 04 | Shortest paths: BFS on unweighted, Dijkstra, 0-1 BFS | planned |
| 05 | Disjoint Set Union, and minimum spanning trees | planned |
| 06 | Topological sort and DAG dynamic programming | planned |
| 07 | Dynamic programming I: 1-D, knapsack, coin change | planned |
| 08 | Dynamic programming II: on grids, LIS, LCS, edit distance | planned |
| 09 | Number theory: sieve, factorisation, modular arithmetic, fast power | planned |
| 10 | Combinatorics: nCr mod p, inclusion–exclusion | planned |
| 11 | Strings: hashing, prefix function (KMP), Z-function | planned |

## 03 · Advanced

Only after tier 02 is genuinely fluent. These decide the top of the scoreboard,
not whether you qualify.

| # | Lesson | Status |
|---|---|---|
| 01 | Segment tree, and Fenwick (BIT) | planned |
| 02 | Trees: rooting, subtree DP, binary lifting and LCA | planned |
| 03 | Dynamic programming III: bitmask, digit, DP on trees | planned |
| 04 | Max flow / min cut, and bipartite matching | planned |
| 05 | Computational geometry: orientation, convex hull | planned |
| 06 | Game theory basics: Nim, Grundy numbers | planned |

## ECPC-Prep

Not topics — habits. Run in parallel with tier 02 onward, not after it.

- Virtual contests under real time pressure, 5 hours, no editorials
- Reading a problem set as a team: who reads what, when to switch problems
- Writing by hand on paper first when the implementation is long
- The printed team reference document, and what belongs on it
- Penalty-time discipline: when a wrong submission is worth the risk

---

## What is deliberately left out

**Templates and library code copied in bulk.** A 2000-line personal library you
did not write and cannot debug is worse than an empty file. Each data structure
enters this repo only after being implemented from scratch once and passing a
stress test.

**Language trivia.** Move semantics, `constexpr`, smart pointers, the rule of
five. All of it real C++ engineering, none of it worth a single minute before
ECPC.

**Competitive programming "tricks" without the underlying idea.** Fast
input-output tricks and bit hacks are mentioned where they matter and ignored
where they do not. A trick saves milliseconds; an algorithm saves orders of
magnitude.
