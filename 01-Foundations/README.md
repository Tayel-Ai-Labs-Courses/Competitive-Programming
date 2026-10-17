# 01 · Foundations

The entry cost: the slice of C++ a contest needs, how to read a constraint, the
containers, and how to find a bug without guessing. Three weeks.

| # | Lesson |
|---|---|
| 01 | [C++ for a Python programmer](lessons/01-cpp-for-python-programmers.md) |
| 02 | [The template, and input/output](lessons/02-the-template-and-io.md) |
| 03 | [Complexity, and reading the constraints](lessons/03-complexity-and-constraints.md) |
| 04 | [The eight STL containers worth knowing](lessons/04-stl-containers.md) |
| 05 | [Stress testing: finding the hidden failing test](lessons/05-stress-testing.md) |
| 06 | Prefix sums and two pointers — *not yet written* |

Lessons 01–05 contain no claim that was not produced by running the code. Where
a claim could not be measured on this machine (the behaviour of GCC's
`sync_with_stdio`, in lesson 02), it says so and tells you how to measure it.

**Exit criteria before tier 02:**

- 30 problems at rating 800 committed to `problems/`, all passing `judge.py --all`
- the template typed from memory, with no copy-paste
- given `n ≤ 2·10⁵`, you say "O(n log n)" without thinking about it
- you have run `tools/stress.py` on a real bug and kept the failing test
