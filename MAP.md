# The map

One page. Read it when you start, and again whenever you are not sure what to
do next. Everything else in this repository is reachable from here.

If you only read one section, read **§3 · The loop** below. That loop is the
training; everything else exists to make it fast.

---

## 1 · The whole road

```mermaid
flowchart TD
    START["<b>You are here</b><br/>arrays, loops, functions<br/>no C++, no Codeforces history"]

    subgraph P1["▪ PHASE 1 · weeks 1-3 · the entry cost"]
        direction LR
        L1["<b>Lessons 01-05</b><br/>the C++ subset, the template,<br/>complexity, the STL,<br/>stress testing"]
        Q1["<b>30 problems</b> @ 800<br/><i>syntax reps,<br/>not algorithms</i>"]
    end

    subgraph P2["▪ PHASE 2 · weeks 4-14 · core, first half"]
        direction LR
        L2["<b>Tier 02, lessons 01-06</b><br/>sorting, greedy, binary search,<br/>BFS/DFS, shortest paths,<br/>DSU, topological sort"]
        Q2["<b>12 problems a week</b><br/>rating 900-1300<br/><i>filtered by the lesson's tag</i>"]
    end

    subgraph P3["▪ PHASE 3 · weeks 15-26 · core, second half"]
        direction LR
        L3["<b>Tier 02, lessons 07-11</b><br/>DP, number theory,<br/>combinatorics, strings"]
        Q3["<b>12 a week</b> @ 1200-1600<br/>half of them tagged dp<br/>+ <b>1 virtual contest weekly</b>"]
    end

    subgraph P4["▪ PHASE 4 · weeks 27-34 · contest form"]
        direction LR
        L4["<b>Selected tier 03</b><br/>chosen by what past<br/>ECPC sets actually used"]
        Q4["<b>Find the team.</b><br/>5-hour team rounds<br/>on past ECPC sets<br/>+ the printed reference"]
    end

    subgraph P5["▪ PHASE 5 · weeks 35-38 · sharpening"]
        direction LR
        L5["<b>Nothing new.</b><br/>new topics this late cost<br/>confidence and buy nothing"]
        Q5["<b>2 timed rounds a week</b><br/>re-solve old failures<br/>classify your own errors"]
    end

    GOAL["<b>ECPC 2027</b><br/><i>date unconfirmed - verify it</i>"]

    START --> P1 --> P2 --> P3 --> P4 --> P5 --> GOAL

    CHK1["<b>gate</b><br/>a correct 800 in under 10 min,<br/>template from memory"]
    CHK2["<b>gate</b><br/>an unseen 1200 in under 40 min,<br/>4 times out of 5"]
    CHK3["<b>gate</b><br/>3 problems in a Div. 2 round"]
    CHK4["<b>gate</b><br/>a past ECPC set at a<br/>qualifying score"]

    P1 -.-> CHK1
    P2 -.-> CHK2
    P3 -.-> CHK3
    P4 -.-> CHK4
```

The gates matter more than the weeks. **A phase is finished when its gate
opens, not when its weeks run out.** If week 14 arrives and an unseen 1200
still takes you ninety minutes, you are in phase 2 — carry on, and move the
later dates. Marching forward on schedule with a gate unmet is how people
arrive at a contest having read about everything and being fast at nothing.

Full detail: [`TRAINING-PLAN.md`](TRAINING-PLAN.md). Topic order:
[`CURRICULUM.md`](CURRICULUM.md).

---

## 2 · The repo, by the question it answers

```mermaid
flowchart TD
    Q["<b>What do I need right now?</b>"]

    Q -->|"what do I do today"| A1["<b>TRAINING-PLAN.md</b><br/>weeks, phases, volume"]
    Q -->|"what order do topics go in"| A2["<b>CURRICULUM.md</b><br/>the definitive sequence"]
    Q -->|"teach me the thing"| A3["<b>01-Foundations/lessons/</b><br/>then 02-, then 03-"]
    Q -->|"I don't understand, in Arabic"| A4["<b>NOTES.md</b><br/>from scratch, plus every<br/>bug hit building this"]
    Q -->|"what do I type at the top"| A5["<b>templates/README.md</b><br/>every line, explained"]
    Q -->|"is my solution right"| A6["<b>tools/judge.py</b>"]
    Q -->|"where is it wrong"| A7["<b>tools/stress.py</b>"]
    Q -->|"what have I actually done"| A8["<b>problems/</b><br/>and git log"]
    Q -->|"how does a contest work"| A9["<b>ECPC-Prep/README.md</b>"]

    A6 -.->|"--debug<br/>for crashes"| A6b["AddressSanitizer<br/>file + line number"]
```

`problems/` is the only directory that grows every day. The lessons are
scaffolding; **the problem log is the artifact.**

---

## 3 · The loop: one problem, start to finish

This is the repository. Everything else exists to make this loop fast.

```mermaid
flowchart TD
    READ["<b>1 · Read the constraints FIRST</b><br/>before the statement.<br/>write down n &lt;= ?"]
    DERIVE["<b>2 · Derive the allowed complexity</b><br/>from n alone<br/><i>lesson 03</i>"]
    IDEA["<b>3 · Have an idea.</b><br/>count ITS complexity,<br/>including the innermost loop body"]
    FITS{"does it fit<br/>the budget?"}
    SCAFFOLD["<b>4 · Scaffold</b><br/>new_problem.py, paste the sample"]
    WRITE["<b>5 · Write sol.cpp</b>"]
    JUDGE["<b>6 · python3 tools/judge.py</b>"]
    VERDICT{"verdict?"}
    SUBMIT["<b>7 · Submit to the judge</b>"]
    ONLINE{"online<br/>verdict?"}
    COMMENT["<b>8 · Write the insight</b><br/>at the top of sol.cpp:<br/>the idea, and the trap"]
    COMMIT["<b>9 · Commit</b><br/>it is now in the log"]

    STRESS["<b>tools/stress.py</b><br/>write gen.py + brute.py,<br/>let it find the case"]
    KEEP["<b>rename the failing test</b><br/>fail.in to NN-description.in<br/><i>permanent regression test</i>"]
    DEBUG["<b>judge.py --debug</b><br/>sanitizers: file + line"]
    RECOUNT["<b>recount the complexity</b><br/>the idea is wrong,<br/>not the code"]
    THIRTY{"stuck 30 min<br/>with no progress?"}
    EDITORIAL["<b>read the editorial fully,</b><br/>close it, implement from<br/>a BLANK file.<br/>mark solved_without_help: false"]
    RESOLVE["<b>re-solve it in 2 weeks</b><br/>from scratch"]

    READ --> DERIVE --> IDEA --> FITS
    FITS -->|"no"| IDEA
    FITS -->|"yes"| SCAFFOLD --> WRITE --> JUDGE --> VERDICT

    VERDICT -->|"AC"| SUBMIT
    VERDICT -->|"WA"| STRESS
    VERDICT -->|"RTE"| DEBUG
    VERDICT -->|"TLE"| RECOUNT

    STRESS --> KEEP --> WRITE
    DEBUG --> WRITE
    RECOUNT --> IDEA

    SUBMIT --> ONLINE
    ONLINE -->|"AC"| COMMENT --> COMMIT
    ONLINE -->|"WA on a hidden test"| STRESS
    ONLINE -->|"TLE"| RECOUNT

    IDEA -.-> THIRTY
    THIRTY -->|"yes"| EDITORIAL --> RESOLVE
```

Three things in that diagram are easy to skip and are the whole point:

**Steps 1–3 happen before you touch the keyboard.** They take a minute.
Typing the wrong idea takes twenty, and then you throw it away while the clock
runs.

**A WA never sends you back to reading your own code.** It sends you to
`stress.py`. Five minutes of mechanical work beats an hour of staring, every
time — see [lesson 05](01-Foundations/lessons/05-stress-testing.md), where the
tool found a one-element failing test on its second try.

**Step 8 is not paperwork.** One or two sentences at the top of `sol.cpp`
saying the idea and the trap. Re-reading your own summaries from three months
ago is the cheapest revision that exists.

---

## 4 · When it goes wrong: symptom to tool

```mermaid
flowchart TD
    S["<b>something is wrong</b>"]

    S --> W{"what does<br/>the judge say?"}

    W -->|"Wrong Answer"| WA["<b>tools/stress.py</b><br/>gen.py + brute.py<br/><i>do NOT reread your code</i>"]
    W -->|"Runtime Error"| RE["<b>judge.py --debug</b><br/>out of bounds, division by zero,<br/>stack overflow from recursion"]
    W -->|"Time Limit"| TLE["<b>recount the complexity</b><br/>including map/set/substr<br/>inside the loop"]
    W -->|"Memory Limit"| ML["<b>a 2-D table you don't need</b><br/>most DP only reads<br/>the previous row"]
    W -->|"Compilation Error"| CE["<b>read the FIRST error only</b><br/>and look one line UP"]
    W -->|"works locally,<br/>fails on the judge"| LJ["<b>judge.py --debug</b><br/>undefined behaviour reads<br/>different garbage elsewhere"]

    WA --> WA2{"no brute force<br/>possible?"}
    WA2 -->|"many valid answers"| CHECKER["write <b>check.py</b> that<br/>verifies the OUTPUT is valid,<br/>not that it equals an answer"]
    WA2 -->|"no idea what's correct"| TWO["stress your O(n log n)<br/>against your own O(n^2)"]

    TLE --> T2{"is the<br/>complexity fine?"}
    T2 -->|"yes"| CONST["<b>the constant factor</b><br/>map 0.447s vs vector index.<br/>pass vectors by const ref.<br/>never endl"]
    T2 -->|"no"| IDEA2["the idea is wrong.<br/>go back to the constraints"]

    SUSPECT["<b>and before any of this:</b><br/>is a value overflowing int?<br/>100000*100000 = 1410065408"]
    S -.-> SUSPECT
```

The overflow box is dotted because it is not a verdict — it is the thing to
suspect regardless of which verdict you got. It produces wrong answers,
impossible timings and bizarre crashes, and it is invisible if you came from
Python. [Lesson 01 §2](01-Foundations/lessons/01-cpp-for-python-programmers.md).

---

## 5 · The constraint tells you the algorithm

Read this before the statement. It is the most valuable twenty seconds in any
contest problem.

```mermaid
flowchart LR
    N["<b>n &lt;= ?</b><br/>the line at the<br/>bottom of the statement"]

    N --> A["<b>10-12</b><br/>O(n!)<br/><i>next_permutation</i>"]
    N --> B["<b>20-25</b><br/>O(2^n · n)<br/><i>subsets, bitmask DP</i>"]
    N --> C["<b>100</b><br/>O(n^3)<br/><i>Floyd-Warshall, triple DP</i>"]
    N --> D["<b>1000-5000</b><br/>O(n^2)<br/><i>2-D DP, all pairs</i>"]
    N --> E["<b>1e5-1e6</b><br/>O(n log n)<br/><i>sort, binary search,<br/>set/map, heap</i>"]
    N --> F["<b>1e6-1e7</b><br/>O(n)<br/><i>prefix sums, two pointers,<br/>one pass, sieve</i>"]
    N --> G["<b>1e9-1e18</b><br/>O(log n) or O(1)<br/><i>maths, fast power,<br/>binary search the ANSWER</i>"]
```

`n <= 20` is a billboard reading "iterate over subsets". Nobody writes
`n <= 20` by accident. And `n <= 2e5` — the most common bound on Codeforces —
means O(n log n): if your idea is O(n²), it is the wrong idea, and you should
not start typing.

Watch for **"the sum of n over all test cases"**. That is a different, looser
promise than a per-case bound, and mistaking it makes you discard a correct
solution.

---

## 6 · What depends on what

Nothing here is optional, but the arrows are real: a topic with an unmet
prerequisite will not stick.

```mermaid
flowchart TD
    subgraph F["▪ FOUNDATIONS"]
        direction LR
        CPP["<b>C++ subset</b><br/>+ overflow"]
        CX["<b>complexity</b><br/>from constraints"]
        STL["<b>the STL</b>"]
        ST["<b>stress testing</b>"]
    end

    CPP --> SORT["<b>sorting &amp; greedy</b><br/>exchange argument"]
    STL --> SORT
    CX --> SORT

    SORT --> BS["<b>binary search</b><br/>on an array,<br/>and on the ANSWER"]
    SORT --> PS["<b>prefix sums</b><br/>&amp; two pointers"]

    STL --> GR["<b>graphs</b><br/>adjacency list,<br/>BFS, DFS"]
    GR --> SP["<b>shortest paths</b><br/>Dijkstra needs a<br/>min-heap"]
    GR --> TOPO["<b>topological sort</b>"]
    GR --> DSU["<b>DSU</b><br/>+ minimum<br/>spanning tree"]

    TOPO --> DP["<b>DP</b><br/>1-D, knapsack,<br/>grids, LIS, LCS"]
    PS --> DP
    BS --> DP

    DP --> DPA["<b>advanced DP</b><br/>bitmask, digit,<br/>DP on trees"]
    GR --> TREE["<b>trees</b><br/>subtree DP,<br/>binary lifting, LCA"]
    TREE --> DPA

    PS --> SEG["<b>segment tree</b><br/>&amp; Fenwick"]
    SEG --> TREE

    CPP --> NT["<b>number theory</b><br/>sieve, modular,<br/>fast power"]
    NT --> COMB["<b>combinatorics</b><br/>nCr mod p"]
    NT --> STR["<b>strings</b><br/>hashing, KMP,<br/>Z-function"]

    DSU --> FLOW["<b>flows &amp; matching</b>"]
    SEG --> FLOW
    GOAL2["<b>ECPC</b>"]
    DP --> GOAL2
    SP --> GOAL2
    DSU --> GOAL2
    STR --> GOAL2
    SEG --> GOAL2

    ST -.->|"used on every<br/>topic above"| GOAL2
```

Two readings of that graph are worth making explicit.

**DP has three arrows into it.** Prefix sums, binary search and topological
sort all feed it, which is why DP is where people stall: arriving there with a
shaky grasp of any of the three makes DP feel like magic rather than like
bookkeeping. If phase 3 is going badly, the fix is usually in phase 2.

**`stress testing` has a dotted arrow to the end.** It is not a topic you
finish. It is the tool you use on every topic, for thirty-eight weeks.

---

## 7 · Today

When you do not know what to do, do this:

```mermaid
flowchart TD
    T["<b>open the repo</b>"]
    T --> Q1{"have you read<br/>lessons 01-05?"}
    Q1 -->|"no"| R["read the next one.<br/>15 minutes.<br/><i>then come back</i>"]
    Q1 -->|"yes"| Q2{"did you solve<br/>12 problems<br/>this week?"}
    Q2 -->|"no"| S["<b>solve the next problem.</b><br/>the list is at the end<br/>of the current lesson"]
    Q2 -->|"yes"| Q3{"is this week's<br/>virtual contest<br/>done? (phase 3+)"}
    Q3 -->|"no"| V["<b>run it.</b> 2 hours,<br/>no editorials until<br/>the clock stops"]
    Q3 -->|"yes"| Q4{"any problem marked<br/>solved_without_help: false<br/>older than 2 weeks?"}
    Q4 -->|"yes"| RS["<b>re-solve it</b><br/>from a blank file"]
    Q4 -->|"no"| REST["<b>take the day off.</b><br/>deliberately.<br/><i>burnout is the most likely<br/>way 38 weeks fails</i>"]
    R --> S
```

That last box is not filler. Over thirty-eight weeks, burnout is a more likely
cause of failure than any topic being too hard.

---

## The two rules, once more

**Nothing enters `problems/` until `tools/judge.py` prints AC.** Not "I think
this is right". The machine compiled it and ran it. CI re-checks every solution
on every push.

**Every failing case the stress tester finds becomes a permanent test file.**
It is the one bug you are guaranteed never to make twice, and it makes the test
suite a record of your own mistakes — the only test suite that is actually
about you.
