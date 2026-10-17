# The template

Nine lines of boilerplate. You type them from memory before every problem, so
read this once and understand why each line is there — a template you cannot
explain is a template that will betray you in a contest.

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve() {
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t = 1;
    // cin >> t;
    while (t--) solve();
    return 0;
}
```

### `#include <bits/stdc++.h>`

Pulls in the entire standard library in one line. It is a GCC-specific header,
it does not exist on Apple's clang, and it would be unacceptable in production
code because it makes compilation slower. In a contest none of that matters:
Codeforces, ECPC and ICPC all judge on GCC, and you are not maintaining this
code — you are deleting it in two hours.

Apple's clang, which is what `g++` runs on this Mac, has no such header — a
solution copied from any editorial fails to compile with
`fatal error: 'bits/stdc++.h' file not found`. So this repo ships its own at
[`include/bits/stdc++.h`](../include/bits/stdc++.h), and `tools/judge.py`
compiles with `-I include`. Nothing to install, and the same source file
compiles here and on the judge.

One real gap remains: `__gcd(a, b)` is a GCC internal and does **not** work on
clang. Use `std::gcd(a, b)` from `<numeric>` instead — it is standard C++17, so
it works here *and* on Codeforces. Prefer the standard name over the GCC
internal everywhere; `__builtin_popcount`, `__builtin_clz` and `__int128` are
fine, both compilers have them.

### `using namespace std;`

Lets you write `sort` and `vector` instead of `std::sort` and `std::vector`. A
real codebase should never do this; in a 40-line file racing a clock, the saved
keystrokes are worth more than the namespace hygiene.

### `using ll = long long;`

**This line prevents more lost problems than any other.** A C++ `int` holds up
to about 2.1 billion. The moment a problem says "the answer can be up to 10^18",
or you multiply two numbers near 10^5, an `int` silently wraps around into a
wrong answer — no crash, no warning, just a wrong number. `ll` makes writing
the 64-bit type cheap enough that you actually use it.

### `ios_base::sync_with_stdio(false); cin.tie(nullptr);`

By default C++ keeps `cin`/`cout` synchronised with C's `scanf`/`printf`, and
flushes `cout` before every `cin`. Both guarantees cost time you do not need.
These two lines turn them off and make `cin` roughly as fast as `scanf`. On a
problem that reads 10^6 numbers this is the difference between passing and TLE.

The price: never use `printf` and `cout` in the same program after this, and
never rely on output appearing before you read input (so no interactive
problems without re-enabling the flush — use `endl` or `cout.flush()` there).

### `int t = 1; // cin >> t;`

Codeforces problems come in two shapes: one test case per run, or "the first
line contains t, the number of test cases". Writing it this way means switching
between them is uncommenting one line, not restructuring `main`.

### Why `solve()` and not everything in `main`

Multiple test cases need every variable to start fresh. A function gives you
that for free — locals are reborn on each call. The classic contest bug is a
global array that still holds the previous test case's data, and this shape of
template makes it hard to write.

## What is deliberately NOT here

You will see template files online with 200 lines of macros (`#define rep(i,a,b)`,
`#define pb push_back`, debug printers, random hash seeds). Do not copy them
yet. Every macro is a thing you have to remember under pressure, and a thing
that makes other people's editorials harder to read. Add a line only when you
have personally lost time for the want of it.
