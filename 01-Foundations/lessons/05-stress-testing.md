# 05 · Stress testing: finding the hidden failing test

The judge says:

```text
Wrong answer on test 7
```

and shows you nothing. You have a 60-line solution, a sample that passes, and
no idea which of your assumptions is wrong.

Almost everyone responds by rereading the code. That is the slowest available
option. The fast one is mechanical, takes about five minutes to set up, and
finds a *minimal* failing test for you — usually small enough to read with your
eyes and understand in seconds.

This lesson is the single highest-return technique in the repo.

---

## 1. The idea

You need three programs.

| File | What it is | How fast |
|---|---|---|
| `sol.cpp` | the solution you intend to submit, which you suspect | fast, maybe wrong |
| `brute.py` | the dumbest correct solution you can write | hopelessly slow, certainly right |
| `gen.py` | prints one random **small** test | — |

Then loop: generate a test, run both, compare. Repeat until they disagree. The
first disagreement is a failing case — and because the tests are tiny, it is a
*small* failing case.

`tools/stress.py` is that loop.

The insight worth internalising: you do not need to know what is wrong to find
the input that proves it. The brute force is correct precisely *because* it is
too slow to submit — no cleverness, no optimisation, nothing to get wrong.
O(n³) is fine. O(2ⁿ) is fine. It only ever runs on n = 5.

---

## 2. A real session

Here is the actual history of `problems/practice/max-subarray-sum/`, which is
in this repo as the worked example. The problem: given an array, find the
maximum sum of a non-empty contiguous subarray. Kadane's algorithm, O(n).

The first draft:

```cpp
ll best = 0, running = 0;
for (int i = 0; i < n; i++) {
    running = max(running + a[i], a[i]);
    best = max(best, running);
}
cout << best << "\n";
```

This passes the sample. It looks like every version of Kadane you have ever
seen. Now the generator — deliberately tiny, and seeded from `argv[1]` so the
run is reproducible:

```python
import random
import sys

random.seed(int(sys.argv[1]))

n = random.randint(1, 6)
print(n)
print(*[random.randint(-10, 10) for _ in range(n)])
```

And the oracle — every pair of endpoints, obviously correct:

```python
import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [int(x) for x in data[1 : 1 + n]]

best = None
for i in range(n):
    total = 0
    for j in range(i, n):
        total += a[j]
        if best is None or total > best:
            best = total

print(best)
```

Run it:

```bash
python3 tools/stress.py problems/practice/max-subarray-sum -n 500
```

```text
mismatch on seed 2 after 1 passing tests
input
1
-8
brute.py says  -8
sol.cpp says   0

saved as problems/practice/max-subarray-sum/tests/fail.in - now fix sol.cpp
and re-run; the test stays in tests/ as a regression check.
```

**The second random test.** A one-element array holding `-8`.

The bug is `ll best = 0`. Starting the answer at zero quietly asserts that the
empty subarray is allowed, so on an all-negative array the code returns 0
instead of the largest (least negative) element. The fix:

```cpp
ll best = a[0], running = a[0];
for (int i = 1; i < n; i++) { ... }
```

Now notice what the samples would never have told you. Sample tests for this
kind of problem are almost always mixed-sign, because that is what makes the
problem interesting to the setter. The all-negative case is the *boring* case,
which is exactly why it ends up in the hidden tests and not the sample.

After the fix:

```text
500 random tests, sol.cpp agrees with brute.py everywhere
That is evidence, not proof - the bug may need a bigger or weirder test.
```

---

## 3. The regression test

`tools/stress.py` writes the failing case to `tests/fail.in` and `tests/fail.out`.
Those two filenames are in `.gitignore` on purpose — they are scratch.

**When the case is a real bug, rename it and keep it forever:**

```bash
cd problems/practice/max-subarray-sum/tests
mv fail.in 01-all-negative.in
mv fail.out 01-all-negative.out
```

That file is now part of `python3 tools/judge.py --all`, and CI runs it on
every push. It is the one bug you are guaranteed never to make twice. The
repo's test suite grows out of your own mistakes, which is the only test suite
that is actually about you.

---

## 4. Writing a good generator

The generator is where this technique succeeds or fails.

**Keep it small.** `n` between 1 and 6. The instinct is to generate big tests
because the bug feels complicated; the opposite is true. A bug that appears at
n = 1000 appears at n = 5 in almost every case, and at n = 5 you can see it.

**Hit the edges of every range.** If values can be negative, generate
negatives. If they can be zero, generate zeros. If `n` can be 1, generate
n = 1 — that is the case that caught Kadane above, and `random.randint(1, 6)`
produced it on the second try precisely because the range starts at 1. A
generator over `randint(2, 6)` would have found nothing in a thousand runs.

**Keep the value range narrow.** `randint(-10, 10)` rather than
`randint(-10**9, 10**9)`. Small values collide, and collisions are where
duplicate-handling bugs live. A generator that never produces two equal numbers
will never find your `<` that should be `<=`.

**Respect the problem's validity rules.** If the input must be a tree, generate
a tree (`parent[i] = randint(0, i-1)`) and not a random edge list. A
"disagreement" on an invalid input teaches nothing and wastes your time.

Generating structured inputs:

```python
# a random tree on n nodes, as n-1 edges
import random, sys
random.seed(int(sys.argv[1]))
n = random.randint(1, 7)
print(n)
for v in range(2, n + 1):
    print(random.randint(1, v - 1), v)
```

```python
# a random permutation
print(*random.sample(range(1, n + 1), n))
```

```python
# a random string over a tiny alphabet - small alphabets find bugs
print("".join(random.choice("ab") for _ in range(n)))
```

That last one matters more than it looks. Over `"abcdefghij"`, repeats are rare;
over `"ab"`, every string is full of repeats and periodicity, which is where
string algorithms break.

---

## 5. When there is no brute force

Sometimes the slow-but-correct version is itself the hard part. Three
alternatives, in order of usefulness:

**Check a property instead of an answer.** Many problems ask you to *construct*
something — a valid arrangement, a path, a partition. There may be many correct
answers, so comparing output to a brute force is meaningless. Instead write a
`check.py` that verifies your output satisfies the conditions: is it a
permutation, do all the edges exist, does the sum match. Then stress against
the checker rather than against an answer.

**Compare two of your own solutions.** If you have a clever O(n log n) and a
plain O(n²), and they disagree, one of them is wrong and you have a case to
look at. Neither has to be a "brute force" in the textbook sense.

**Test the invariant, not the output.** A data structure can be stressed by
performing random operations against a `vector` that does the same thing
naively.

---

## 6. The other tool: sanitizers

Stress testing finds *logic* errors. For *memory* errors there is a faster
route:

```bash
python3 tools/judge.py problems/codeforces/some-problem --debug
```

This rebuilds with AddressSanitizer and UndefinedBehaviorSanitizer, which turn
the silent out-of-bounds read from [lesson 01](01-cpp-for-python-programmers.md)
into:

```text
==7397==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6020000000d8
READ of size 4 at 0x6020000000d8 thread T0
    #0 0x000102740b5c in main demo3.cpp:5
```

A file and a line number, instead of a wrong number.

The decision rule is simple:

| Symptom | Reach for |
|---|---|
| Wrong answer on a hidden test | `tools/stress.py` |
| Runtime error, or works locally and crashes on the judge | `--debug` |
| Works on small input, wrong on large | `--debug` first, then stress with a bigger generator |
| Time limit exceeded | neither — recount the complexity ([lesson 03](03-complexity-and-constraints.md)) |

---

## 7. Why Python for `brute.py`

This is the one place in this repo where Python is the right tool, and the
reasons are worth stating:

- The oracle must be **obviously** correct. Fewer lines means fewer places for
  the oracle itself to be wrong, and an incorrect oracle is worse than none —
  it sends you hunting a bug that is not there.
- Python has no integer overflow, so the oracle cannot share the `int`-versus-
  `long long` bug you may be hunting. If both programs were C++ and both used
  `int`, they would agree on the wrong answer.
- Python raises `IndexError` instead of reading garbage, so an out-of-bounds in
  the oracle is loud.
- Speed is irrelevant. It runs on n = 5.

That is also why `brute.py` and the lesson-end Python sections are the *only*
Python in this repository. Everywhere else, C++.

---

## Practice

1. Take any three problems you have already solved and accepted. For each,
   write `gen.py` and `brute.py`, and run 1000 iterations. You are looking for
   nothing — this is practice at the mechanics, so that in a contest the setup
   costs you three minutes and no thought.

2. Then do it properly: take a problem you got Wrong Answer on and could not
   fix, and stress it. Keep the failing test.

3. Deliberately break a working solution — change a `<=` to a `<`, remove an
   edge case — and see how many random tests it takes to catch it. Then make
   the generator smaller and narrower and see the count drop. That is the
   lesson about generator design, learned by measurement rather than by being
   told.

**Next:** 06 · Prefix sums and two pointers *(not yet written)*
