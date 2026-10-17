# 03 · Complexity, and reading the constraints

The most valuable twenty seconds of any contest problem are spent at the
bottom of the statement, on the line that says how large `n` can be. That line
tells you which algorithm is allowed **before** you have had a single idea.
Experienced contestants read it first, and so should you.

---

## 1. What the constraint tells you

A contest problem has a time limit, usually 1 or 2 seconds. A judge machine
does on the order of **10⁸ simple operations per second** — the classic rule of
thumb, and a deliberately conservative one. Combine that with `n` and the
possible algorithms collapse to a short list:

| n up to | Budget allows | So the intended solution is |
|---|---|---|
| 10–12 | O(n!) | permutations, brute force over all orderings |
| 20–25 | O(2ⁿ · n) | subsets, bitmask DP |
| 100 | O(n³) | Floyd–Warshall, triple loop DP, matrix work |
| 1000–5000 | O(n²) | 2-D DP, all pairs, simple nested loops |
| 10⁵–10⁶ | O(n log n) | sort, binary search, set/map, heap, divide and conquer |
| 10⁶–10⁷ | O(n) | prefix sums, two pointers, single pass, sieve |
| 10⁹–10¹⁸ | O(log n) or O(1) | maths, fast exponentiation, binary search on the answer |

Read it in reverse and it becomes a hint generator:

- `n ≤ 20` is a *billboard* saying "iterate over subsets". Nothing else fits
  that tiny a bound, and no problem setter writes `n ≤ 20` by accident.
- `n ≤ 5000` with a two-sequence problem means an O(n²) DP table.
- `n ≤ 2·10⁵` — by far the most common bound on Codeforces — means O(n log n).
  If your idea is O(n²), it is the wrong idea; do not start typing.
- `n ≤ 10⁹` means you may not even *loop* over n. The answer is mathematical,
  or found by binary searching the answer.
- `sum of n over all test cases ≤ 2·10⁵` is an important variant: individual
  test cases may be large but the total is bounded, so an O(n log n) per case
  is fine. Read this line carefully; mistaking it for "n ≤ 2·10⁵ per case,
  t ≤ 10⁵" leads you to discard a correct solution.

---

## 2. What the rule of thumb actually looks like

Measured on the machine this repo was written on (Apple clang 17, `-O2`,
arm64), running real algorithms rather than synthetic loops:

| Work | Inner steps | Time |
|---|---|---|
| Floyd–Warshall, n = 500 | 1.25 · 10⁸ | 0.054 s |
| Edit-distance DP, 10⁴ × 10⁴ | 10⁸ | 0.140 s |
| `sort` on 10⁶ `int` | — | 0.047 s |
| `sort` on 10⁷ `int` | — | 0.537 s |
| 10⁷ dependent random array reads | 10⁷ | 0.037 s |
| 10⁶ inserts into `map<int,int>` | — | 0.447 s |
| 10⁶ inserts into `unordered_map<int,int>` | — | 0.141 s |
| 10⁸ additions in a plain loop | 10⁸ | 0.170 s |

Two conclusions, and they pull in opposite directions.

**This machine is faster than the rule of thumb.** 10⁸ steps of real DP took
0.14 s, not 1 s. Modern hardware with SIMD does better than the folklore
number, and the Floyd–Warshall row is faster still because that loop
vectorises.

**Use the rule of thumb anyway.** Judge machines are older x86 hardware and
slower than an Apple-silicon laptop; the limit has to hold for every language
and every constant factor; and the moment your inner loop contains a `map`
lookup instead of an array index, you lose an order of magnitude — look at the
`map` row, 0.447 s for a mere 10⁶ operations. **Never** conclude from a local
timing that an asymptotically-too-slow solution will pass.

### The constant factor is real, and it lives in your data structure

`map` against `unordered_map`, same million inserts: 0.447 s against 0.141 s.
Both are "fine" asymptotically — O(log n) and O(1) — and one is three times the
other. `map` is a balanced binary tree, which means pointer chasing and cache
misses; `unordered_map` is a hash table.

So prefer `unordered_map` when you only need lookups? Usually, **but not on
Codeforces**, where `unordered_map<int,int>` is deliberately attacked:
competitors submit anti-hash tests that collide its hash function and turn it
into O(n) per operation. Use `map`, or `unordered_map` with a randomised hash,
or best of all an ordinary `vector` indexed by the key when the keys are small
integers. An array index beats every hash table ever written.

---

## 3. How to count complexity

Count the loops, and what the body of the innermost one costs.

```cpp
for (int i = 0; i < n; i++)          // n times
    for (int j = 0; j < n; j++)      // times n
        ans += a[i] * a[j];          // O(1) body
```

O(n²).

```cpp
for (int i = 0; i < n; i++)          // n times
    if (s.count(a[i])) ans++;        // set lookup: O(log n)
```

O(n log n) — the loop is n, but the body is not O(1). This is the most common
counting mistake: a `set`, `map`, `string` comparison or `substr` inside a loop
quietly multiplies your complexity.

Three specific traps:

- **`s.substr(i, k)` inside a loop is O(k)**, because it copies. A loop over
  all positions taking a substring each time is O(n·k), not O(n).
- **`v.erase(v.begin() + i)` is O(n)**, because the rest of the vector shifts.
  Erasing in a loop is O(n²). Build a new vector instead.
- **Passing a vector by value to a function in a loop copies it every call.**
  See lesson 01 §4. Take `const vector<int> &`.

And the logarithm: `log₂(10⁶) ≈ 20`, `log₂(10⁹) ≈ 30`. A log factor is
essentially free — n log n at n = 10⁶ is about 2·10⁷ steps. Never contort an
algorithm to remove a log.

---

## 4. Memory is also a constraint

Limits are typically 256 MB. An `int` is 4 bytes, a `long long` 8.

| Allocation | Memory |
|---|---|
| `vector<int>` of 10⁶ | 4 MB |
| `vector<int>` of 10⁷ | 40 MB |
| `vector<ll>` of 10⁷ | 80 MB |
| `vector<vector<int>>`, 10⁴ × 10⁴ | **400 MB — exceeds the limit** |

That last row kills real submissions. A 10⁴ × 10⁴ DP table does not fit, and
the fix is almost always that you do not need the whole table: most 2-D DPs
only read the previous row, so two rows of size n suffice. The edit-distance
benchmark above does exactly that — `prev` and `cur`, swapped each iteration —
which is why 10⁴ × 10⁴ ran in 80 KB instead of 400 MB.

Also: `vector<vector<int>>` is a vector of separately allocated vectors, so a
tall thin one costs extra and scatters cache lines. When you need a fixed
rectangle and speed matters, one flat `vector<int>` of size `n*m` indexed
`i*m + j` is measurably faster.

---

## 5. The discipline

Before writing any code:

1. Read the constraints. Write `n ≤ ?` on your paper.
2. Derive the complexity you are allowed from the table in §1.
3. Have an idea. Count its complexity honestly, including the body of the
   innermost loop.
4. Only if step 3 fits step 2, start typing.

Steps 1–3 take a minute. Typing the wrong idea takes twenty, and then you must
throw it away while the clock runs and the scoreboard moves. This single habit
separates people who solve four problems from people who solve two.

---

## 6. In Python

The same analysis, with the constant shifted. Python does roughly 10⁷ simple
operations per second against C++'s 10⁸–10⁹ — the 25× gap measured in the
[README](../../README.md). So when you are using these algorithms outside a
contest, the asymptotic reasoning is identical and the practical ceiling on n
is about one order of magnitude lower. An O(n²) Python solution is comfortable
at n = 2000 and hopeless at n = 20000.

Where Python does win: `sorted()`, `sum()`, `min()` and `set`/`dict`
operations are implemented in C, so a solution whose work happens *inside*
those calls rather than in your loop can be surprisingly fast. The rule is
"push the loop into the library".

---

## Practice

Not problems this time — a reading exercise, and it is the one that pays.

Open the Codeforces problemset, filter to rating 1000–1300, and open ten
problems. For each, **read only the constraints and the statement, do not
solve**, and write down:

- the bound on n
- the complexity that bound allows
- your guess at the technique

Then look at the problem's tags to check your guess. Ten problems, twenty
minutes, and the constraint-to-technique reflex starts forming.

**Next:** [04 · The eight STL containers worth knowing](04-stl-containers.md)
