# 01 · C++ for a Python programmer

You are not learning C++. You are learning the slice of C++ that appears in
contests, which is smaller than it looks: types, `vector`, `string`, loops,
functions, references, and the STL. No classes, no headers, no pointers, no
build system.

Every output in this lesson was produced by compiling and running the code on
the machine this repo was written on. Where C++ and Python disagree, the
disagreement is shown rather than described.

---

## 1. The shape of a program

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << n * 2 << "\n";
    return 0;
}
```

Four structural differences from Python, and that is the entire list:

- **Every statement ends with `;`.** The compiler's error message when you
  forget is usually about the *next* line. Learn to look up one line.
- **Blocks are `{ }`, not indentation.** Indent anyway; you will read this
  code again in a contest when you are tired.
- **Variables are declared with a type.** `int n;` makes an integer named `n`.
  There is no `n = 5` without a type somewhere first.
- **Execution starts in `main`.** No top-level code.

Compile and run:

```bash
g++ -std=c++17 -O2 -I include sol.cpp -o sol && ./sol
```

In this repo you never type that — `python3 tools/judge.py <problem>` does it,
with the right flags and all the tests.

---

## 2. Types, and the bug that will cost you a problem

Python integers grow without limit. C++ integers do not, and when they
overflow there is **no error** — just a wrong number that keeps going.

```cpp
int a = 100000;
cout << "int  100000*100000 = " << a * a << "\n";
ll b = 100000;
cout << "ll   100000*100000 = " << b * b << "\n";
cout << "INT_MAX = " << INT_MAX << "\n";
cout << "LLONG_MAX = " << LLONG_MAX << "\n";
```

```text
int  100000*100000 = 1410065408
ll   100000*100000 = 10000000000
INT_MAX = 2147483647
LLONG_MAX = 9223372036854775807
```

`100000 * 100000` is 10¹⁰. It does not fit in an `int`, so it wrapped around to
`1410065408`. The program did not crash. It did not warn. It printed a
confident wrong answer, and a judge would have called it Wrong Answer with no
indication why.

In Python the same expression gives `10000000000`, which is why this bug is
invisible to you today and will not be next week.

| Type | Range | Use it when |
|---|---|---|
| `int` | ±2.1 · 10⁹ | the default, when you are sure the answer stays small |
| `long long` (`ll`) | ±9.2 · 10¹⁸ | any sum, any product, any "answer up to 10¹⁸" |
| `double` | ~15 significant digits | only when the problem genuinely wants real numbers |

**The rule:** if the problem says the answer can exceed about 2 · 10⁹, or you
multiply two numbers each over about 50000, use `ll`. When unsure, use `ll` —
it costs nothing you can measure.

### The half-fix that does not work

```cpp
cout << "ll = int*int (too late) : " << (ll)(a * a) << "\n";
cout << "ll = (ll)int*int (right): " << (ll)a * a << "\n";
```

```text
ll = int*int (too late) : 1410065408
ll = (ll)int*int (right): 10000000000
```

The overflow happens **during** `a * a`, because both operands are `int`.
Casting afterwards converts an already-wrong number. One operand must be `ll`
*before* the multiplication. This specific mistake is extremely common; the
cast looks right and does nothing.

### Division and modulo disagree with Python

```cpp
cout << "7/2 = " << 7 / 2 << "   -7/2 = " << -7 / 2 << "   -7%2 = " << -7 % 2 << "\n";
```

```text
7/2 = 3   -7/2 = -3   -7%2 = -1
```

Python, same expressions:

```text
7//2 = 3   -7//2 = -4   -7%2 = 1
```

On positives they agree. On negatives they do not: C++ truncates toward zero
and its `%` can return a negative value, while Python floors and its `%` is
always non-negative. This matters constantly in modular arithmetic — after any
subtraction mod `m`, write `((x % m) + m) % m`, not `x % m`.

Also note: C++ `/` on two ints is already integer division. There is no `//`.
To get a real quotient, make one side a `double`.

---

## 3. `vector` is the list

```cpp
vector<int> v = {5, 3, 9, 1};
cout << "size " << v.size() << ", first " << v[0] << ", last " << v.back() << "\n";

sort(v.begin(), v.end());
cout << "sorted:";
for (int x : v) cout << " " << x;
cout << "\n";

sort(v.rbegin(), v.rend());
cout << "descending:";
for (int x : v) cout << " " << x;
cout << "\n";
```

```text
size 4, first 5, last 1
sorted: 1 3 5 9
descending: 9 5 3 1
```

| Python | C++ |
|---|---|
| `a = []` | `vector<int> a;` |
| `a = [0] * n` | `vector<int> a(n, 0);` |
| `a.append(x)` | `a.push_back(x);` |
| `len(a)` | `a.size()` |
| `a[-1]` | `a.back()` — **`a[-1]` is not an error, it is garbage memory** |
| `a.sort()` | `sort(a.begin(), a.end());` |
| `a.sort(reverse=True)` | `sort(a.rbegin(), a.rend());` |
| `for x in a:` | `for (int x : a)` |
| `a[2:5]` | no slicing; use indices, or iterators |

Reading n numbers into a vector — the single most common five lines in all of
competitive programming:

```cpp
int n;
cin >> n;
vector<ll> a(n);
for (ll &x : a) cin >> x;
```

That `&` is essential. Without it you read into a copy and `a` stays zero.

### Two dimensions

```cpp
int n = 3, m = 4;
vector<vector<int>> grid(n, vector<int>(m, 0));
grid[1][2] = 7;
```

```text
grid[1][2] = 7, rows 3, cols 4
```

Read it as "n copies of a row of m zeros".

### Out of bounds does not raise

This is the most dangerous difference in the whole lesson.

```cpp
vector<int> v = {1, 2, 3};
cout << "v[10] = " << v[10] << "\n";
cout << "still running\n";
```

Compiled the way the judge compiles it:

```text
v[10] = 903752
still running
```

Exit code 0. Python raises `IndexError: list index out of range`; C++ reads
whatever bytes happen to be there and carries on. Sometimes it crashes,
sometimes it prints a wrong answer, and which one you get can depend on the
input size — which is how "it works locally but fails on the judge" happens.

This repo has an answer. `tools/judge.py --debug` recompiles with
AddressSanitizer:

```bash
python3 tools/judge.py problems/practice/some-problem --debug
```

```text
==7397==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6020000000d8
READ of size 4 at 0x6020000000d8 thread T0
    #0 0x000102740b5c in main demo3.cpp:5
```

File and line number. **Any time a solution behaves strangely, run it with
`--debug` before you read a single line of your own code.**

---

## 4. Functions, and the `&` that changes everything

```cpp
void addOneCopy(vector<int> v) { v.push_back(1); }   // gets a copy
void addOneRef(vector<int> &v) { v.push_back(1); }   // works on the original
```

```text
after addOneCopy, size = 0
after addOneRef,  size = 1
```

Python passes a reference to the list, so a function that appends is visible to
the caller. C++ passes a **copy** by default. `addOneCopy` dutifully appended to
a vector that was destroyed when the function returned.

Two consequences:

- To modify the caller's data, take `vector<int> &v`.
- To *read* a large vector without modifying it, still take a reference —
  `const vector<int> &v` — because copying a vector of 10⁶ elements on every
  call is real time. Passing a big vector by value is a classic accidental
  TLE.

Return types come first: `int f(int x)`, and `void` means returns nothing.

---

## 5. `string`, `pair`, and `auto`

```cpp
string s = "funzo";
s += " coffee";
cout << s << " | length " << s.size() << " | s[0] " << s[0] << "\n";
cout << "substr(6,6) = " << s.substr(6, 6) << "\n";
```

```text
funzo coffee | length 12 | s[0] f
substr(6,6) = coffee
```

`substr(start, length)` — length, not end index. Unlike Python's `s[6:12]`.
Strings are mutable: `s[0] = 'F'` works.

`pair` is C++'s two-element tuple, and it is everywhere, because a vector of
pairs sorts by first element then second — for free:

```cpp
vector<pair<int, int>> pts = {{2, 9}, {1, 5}, {2, 1}};
sort(pts.begin(), pts.end());
for (auto [x, y] : pts) cout << " (" << x << "," << y << ")";
```

```text
sorted pairs: (1,5) (2,1) (2,9)
```

`auto [x, y]` is C++17 destructuring — the nearest thing to Python's
`for x, y in pts`. Without it you write `p.first` and `p.second`.

`auto` asks the compiler to infer the type. Use it for iterators and
structured bindings, where the real type is noise. Do **not** use it for
numbers: `auto x = 1e18;` gives you a `double`, silently, and your integer
answer loses precision.

---

## 6. The forty lines, as one table

| You want | Python | C++ |
|---|---|---|
| print | `print(x)` | `cout << x << "\n";` |
| read a number | `n = int(input())` | `int n; cin >> n;` |
| read a line of numbers | `a = list(map(int, input().split()))` | loop with `cin >> x` |
| big integers | automatic | `long long`, and watch for overflow |
| list | `[]` | `vector<int>` |
| dict | `{}` | `map<int,int>` or `unordered_map` |
| set | `set()` | `set<int>` or `unordered_set` |
| tuple of 2 | `(a, b)` | `pair<int,int>` |
| sort | `a.sort()` | `sort(a.begin(), a.end())` |
| min / max of a list | `min(a)` | `*min_element(a.begin(), a.end())` |
| sum of a list | `sum(a)` | `accumulate(a.begin(), a.end(), 0LL)` |
| string length | `len(s)` | `s.size()` |
| f-string | `f"{a} {b}"` | `cout << a << " " << b` |
| `**` | `2 ** 10` | `1 << 10` for powers of two, else a loop |
| `//` | `7 // 2` | `7 / 2` (already integer) |
| swap | `a, b = b, a` | `swap(a, b)` |

Note `accumulate(..., 0LL)`: the `0LL` sets the accumulator type to
`long long`. Passing `0` makes it an `int` and overflows — the same trap as
§2, wearing a different hat.

---

## 7. The same ideas in Python, for everything that is not a contest

Outside a contest these algorithms still matter — a graph traversal in a
system you are building, a DP in an AI project. The translation is mechanical,
and the one thing to carry across is the *reasoning*, not the syntax:

```python
# reading input the fast way, when input is large
import sys
data = sys.stdin.buffer.read().split()
n = int(data[0])
a = [int(x) for x in data[1:1 + n]]
```

Python has no overflow and no out-of-bounds garbage — the two bugs this lesson
spends the most time on simply do not exist there. That is exactly why it makes
a good `brute.py`: fewer ways for the oracle itself to be wrong. See
[lesson 05](05-stress-testing.md).

---

## Practice

Thirty problems at rating 800 on Codeforces. Not for the algorithms — these
are syntax reps, and the goal is a correct submission in under ten minutes with
nothing looked up.

Start here, scaffolding each one:

```bash
python3 tools/new_problem.py codeforces 4A "Watermelon"
```

| Problem | Why this one |
|---|---|
| [4A Watermelon](https://codeforces.com/problemset/problem/4/A) | already solved in this repo — read `problems/codeforces/4a-watermelon/sol.cpp` first |
| [71A Way Too Long Words](https://codeforces.com/problemset/problem/71/A) | strings, and multiple test cases in one run |
| [231A Team](https://codeforces.com/problemset/problem/231/A) | reading a fixed-size grid |
| [158A Next Round](https://codeforces.com/problemset/problem/158/A) | a vector, and an off-by-one that bites |
| [282A Bit++](https://codeforces.com/problemset/problem/282/A) | string comparison |
| [112A Petya and Strings](https://codeforces.com/problemset/problem/112/A) | case-insensitive compare, `tolower` |
| [339A Helpful Maths](https://codeforces.com/problemset/problem/339/A) | sorting characters |
| [50A Domino Piling](https://codeforces.com/problemset/problem/50/A) | one line, if you see it |
| [263A Beautiful Matrix](https://codeforces.com/problemset/problem/263/A) | 2-D indices, `abs` |
| [266B Queue at the School](https://codeforces.com/problemset/problem/266/B) | simulation, and the loop bound that traps everyone |

Then filter the Codeforces problemset by rating 800 and keep going to thirty.

**Next:** [02 · The template, and input/output](02-the-template-and-io.md)
