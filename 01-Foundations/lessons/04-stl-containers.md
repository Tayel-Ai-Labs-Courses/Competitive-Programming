# 04 · The eight STL containers worth knowing

The standard library is why competitive programmers use C++. Not the language —
the library. Everything in this lesson is pre-written, debugged by thousands of
people, and fast. Writing your own balanced tree in a contest is a sign
something has gone wrong.

Eight containers cover virtually every ECPC problem. Every output below is a
real run.

---

## 1. `vector` — the default

Covered in [lesson 01](01-cpp-for-python-programmers.md). Reach for it first;
reach for something else only when `vector` cannot do the job.

An `int`-indexed `vector` is the fastest associative structure that exists.
When your keys are integers below, say, 10⁶, `vector<int> cnt(1000001, 0)` beats
every `map` and every hash table. Use it.

## 2. `set` — sorted, unique, O(log n)

```cpp
set<int> s = {5, 1, 5, 3};
```

```text
set: 1 3 5   size 3   count(5) 1
min 1   max 5
```

Duplicates vanish, iteration is in sorted order, and `*s.begin()` /
`*s.rbegin()` give you the minimum and maximum in O(1)-ish time. That last
property makes `set` the structure of choice whenever you need "the smallest
remaining element" *and* the ability to delete arbitrary elements — something a
`priority_queue` cannot do.

The operations that make it powerful are the searches:

```cpp
auto it = s.lower_bound(2);   // first element >= 2
it = s.upper_bound(3);        // first element >  3
```

```text
lower_bound(2) = 3
upper_bound(3) = 5
lower_bound(99) is end? 1
```

**Always check against `s.end()` before dereferencing.** `*s.lower_bound(99)`
on this set is undefined behaviour — not an exception, not a `None`. It is the
same class of bug as `v[10]` in lesson 01, and it is the most common crash in
set-based solutions.

Note: use `s.lower_bound(x)`, the member function, **not** `lower_bound(s.begin(), s.end(), x)`.
The free function assumes random-access iterators; on a `set` it degrades from
O(log n) to O(n) and silently makes your solution quadratic.

## 3. `multiset` — a `set` that keeps duplicates

```text
multiset: 1 3 5 5   count(5) 2
after erase(find(5)) count(5) = 1
```

The trap is in that second line. `ms.erase(5)` removes **every** copy of 5.
`ms.erase(ms.find(5))` removes **one**. Choosing the wrong one is a bug that
passes the samples and fails on a test with duplicates, which is most tests.

## 4. `map` — the dictionary, sorted by key, O(log n)

```cpp
map<string,int> freq;
for (string w : {"a","b","a","c","a"}) freq[w]++;
```

```text
map: a=3 b=1 c=1
```

`freq[w]++` on a key that does not exist creates it with value 0 and then
increments — which is exactly the frequency-counting idiom, and is why `map`
appears in so many solutions.

But that convenience has a sharp edge:

```text
freq["zzz"] before = 0  -> size now 4
count("qqq") = 0  -> size still 4
```

**Reading `freq["zzz"]` inserted it.** `operator[]` on a `map` is not a read —
it default-constructs a missing key. The map grew from 3 entries to 4 just by
being looked at. In a loop that checks `if (freq[x] > 0)` over 10⁶ distinct
values, you have built a 10⁶-entry map and possibly run out of memory and time.

To *ask without inserting*, use `count` (or `find`):

```cpp
if (freq.count(x)) { ... }
```

## 5. `unordered_map` / `unordered_set` — hash tables, O(1) average

Three times faster than `map` on a million inserts (0.141 s against 0.447 s,
measured in [lesson 03](03-complexity-and-constraints.md)). No sorted order,
and no `lower_bound`.

**And on Codeforces, do not use them with integer keys.** The default hash for
`int` is close to the identity function, so an adversary can submit a test
whose keys all collide into one bucket, turning every operation into O(n) and
your solution into a TLE. People do exactly this. Open hacking on Div. 2
rounds has killed many `unordered_map` solutions.

Your options, in order of preference:

1. Use a `vector` indexed by the key, if the keys are small integers.
2. Use `map`. The log factor is 20; it is not your problem.
3. If you really want the hash table, give it a randomised hash:

```cpp
struct Hash {
    size_t operator()(long long x) const {
        static const long long FIXED =
            chrono::steady_clock::now().time_since_epoch().count();
        x += FIXED;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9LL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebLL;
        return x ^ (x >> 31);
    }
};
unordered_map<long long, int, Hash> safe;
```

Keep that snippet; do not try to remember it.

## 6. `priority_queue` — the heap

```text
max-heap pops: 9 4 1
min-heap pops: 1 4 9
```

`priority_queue<int>` is a **max**-heap, which is the opposite of Python's
`heapq`. For a min-heap:

```cpp
priority_queue<int, vector<int>, greater<int>> minpq;
```

Memorise that line — you need a min-heap for Dijkstra, and Dijkstra appears in
almost every contest. The alternative trick is to push negated values into a
max-heap and negate on the way out; it works, and it reads badly at 3 a.m.

`top()`, `push()`, `pop()`. There is no way to look at anything but the top,
and no way to delete an arbitrary element — when you need that, use a `set`.

## 7. `deque` — push and pop at both ends, O(1)

```text
deque: 1 2 3   front 1 back 3
```

Needed for exactly two things, and both matter: BFS on a 0-1 weighted graph
(push cost-0 edges to the front, cost-1 to the back), and the sliding-window
maximum. Otherwise `vector` is better, because `deque` is slower per element
and scatters memory.

`queue` and `stack` also exist, and are `deque` with the other operations
hidden. `queue` for BFS is conventional and clear; use it.

## 8. `bitset` — booleans, 64 to a word

```cpp
bitset<1000000> seen;
seen[42] = 1;
if (seen[42]) { ... }
cout << seen.count();   // popcount of the whole thing
```

`bitset<N>` stores N bits packed into words, so it is 8× smaller than
`vector<bool>`-equivalent storage and its whole-set operations (`&`, `|`, `^`,
`count()`, `_Find_first()`) run 64 bits at a time. That constant factor of 64
is occasionally the difference between an O(n²/64) solution passing and an
O(n²) one failing — subset-sum and reachability problems are the classic uses.

The size must be a compile-time constant. If it is not, you need
`vector<bool>` or a hand-rolled `vector<uint64_t>`.

---

## 9. The algorithms, which matter as much as the containers

All of these take an iterator range. `v.begin(), v.end()` means "the whole
vector".

```cpp
vector<int> v = {4, 1, 4, 2, 9, 1};
sort(v.begin(), v.end());
```

```text
sorted: 1 1 2 4 4 9
lower_bound(4) index = 3
upper_bound(4) index = 5
count of 4 = 2
after unique: 1 2 4 9
sum = 16
max = 9
```

| Need | Call |
|---|---|
| sort | `sort(v.begin(), v.end())` |
| sort descending | `sort(v.rbegin(), v.rend())` |
| first index with value ≥ x | `lower_bound(v.begin(), v.end(), x) - v.begin()` |
| first index with value > x | `upper_bound(...) - v.begin()` |
| how many copies of x | `upper_bound(...) - lower_bound(...)` |
| is x present | `binary_search(v.begin(), v.end(), x)` |
| remove duplicates | `v.erase(unique(v.begin(), v.end()), v.end())` |
| sum | `accumulate(v.begin(), v.end(), 0LL)` |
| max value | `*max_element(v.begin(), v.end())` |
| index of max | `max_element(v.begin(), v.end()) - v.begin()` |
| reverse | `reverse(v.begin(), v.end())` |
| gcd | `gcd(a, b)` — **not** `__gcd`, which clang lacks |

**`lower_bound`, `upper_bound` and `binary_search` require a sorted range.**
On unsorted data they return something, that something is meaningless, and
nothing warns you. This is a top-three cause of "my binary search is wrong".

**`unique` does not remove anything.** It shuffles duplicates to the end and
returns where the unique part stops; the `v.erase(..., v.end())` is what
removes. And it only removes *adjacent* duplicates, so the range must be
sorted first. `unique` alone, without the erase, is a bug that reads as correct.

### `next_permutation`

```cpp
vector<int> p = {1, 2, 3};
do { cout << " " << p[0] << p[1] << p[2]; } while (next_permutation(p.begin(), p.end()));
```

```text
permutations: 123 132 213 231 312 321
```

All n! orderings, in lexicographic order, with no recursion to write. The
range must start sorted, or you get only the permutations after the current
one. This is the entire answer to every `n ≤ 10` brute-force problem.

### Custom comparators

```cpp
sort(people.begin(), people.end(), [](const auto &a, const auto &b){
    if (a.second != b.second) return a.second > b.second;  // age descending
    return a.first < b.first;                              // then name ascending
});
```

```text
by age desc then name: ali(20) sara(20) omar(17)
```

The lambda returns **true when `a` must come before `b`**. Two rules that are
not optional:

- It must be a *strict* ordering: `return a.second >= b.second` can crash
  `sort` (genuinely — the library may read out of bounds on inconsistent
  comparators), not merely sort wrongly.
- Take parameters by `const &`. By value, you copy every element on every one
  of the n log n comparisons.

---

## 10. Choosing, as one table

| You need | Use |
|---|---|
| a list | `vector` |
| counts keyed by a small integer | `vector<int>` sized to the max key |
| counts keyed by anything else | `map` |
| membership, sorted, with deletes | `set` |
| membership, duplicates allowed | `multiset` |
| the smallest remaining element, insert only | `priority_queue` with `greater` |
| the smallest remaining element, with arbitrary deletes | `set` |
| both ends | `deque` |
| millions of booleans, or set operations in bulk | `bitset` |

---

## 11. In Python

| C++ | Python |
|---|---|
| `vector` | `list` |
| `set` / `multiset` | `set` — but **unsorted**; use `sortedcontainers` or a heap for ordered work |
| `map` | `dict` — insertion-ordered, not key-sorted |
| `unordered_map` | `dict` (it already is a hash table) |
| `priority_queue` | `heapq` — a **min**-heap, the opposite default |
| `deque` | `collections.deque` |
| `lower_bound` | `bisect.bisect_left` |
| `upper_bound` | `bisect.bisect_right` |
| `next_permutation` | `itertools.permutations` |
| frequency count | `collections.Counter` |

The real gap: Python's standard library has **no sorted set or sorted map**.
`set.lower_bound` has no equivalent, and that is the one place where porting a
C++ solution to Python requires a different data structure rather than a
different name.

---

## Practice

Twelve problems, rating 900–1200, chosen so each forces one container:

| Problem | Container it forces |
|---|---|
| [4C Registration System](https://codeforces.com/problemset/problem/4/C) | `map<string,int>` |
| [230B T-primes](https://codeforces.com/problemset/problem/230/B) | sieve in a `vector`, and `ll` overflow |
| [474B Worms](https://codeforces.com/problemset/problem/474/B) | prefix sums + `lower_bound` |
| [705A Hulk](https://codeforces.com/problemset/problem/705/A) | none — a warm-up between the others |
| [702A Maximum Increase](https://codeforces.com/problemset/problem/702/A) | one pass over a `vector` |
| [500B New Year Permutation](https://codeforces.com/problemset/problem/500/B) | `vector` + sorting with indices |
| [550A Two Substrings](https://codeforces.com/problemset/problem/550/A) | `string::find` |
| [580C Kefa and Park](https://codeforces.com/problemset/problem/580/C) | DFS, and an adjacency `vector<vector<int>>` |
| [1092B Teams Forming](https://codeforces.com/problemset/problem/1092/B) | `sort`, pairing adjacent |
| [1061A Coins](https://codeforces.com/problemset/problem/1061/A) | greedy, one line |
| [1374C Move Brackets](https://codeforces.com/problemset/problem/1374/C) | `stack` reasoning without a `stack` |
| [1478B Nezzar and Lucky Number](https://codeforces.com/problemset/problem/1478/B) | thinking before coding |

**Next:** [05 · Stress testing: finding the hidden failing test](05-stress-testing.md)
