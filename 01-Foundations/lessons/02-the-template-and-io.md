# 02 · The template, and input/output

Two subjects that look like trivia and are not. Input handling is a real source
of lost problems, and the numbers below are surprising enough that they change
how you should read your own local timings.

The template itself, line by line, lives in
[`templates/README.md`](../../templates/README.md). Read that first; this
lesson is the measurement behind it.

---

## 1. The measurement

One million integers on standard input, summed. Five runs each, minimum and
median reported, on the machine this repo was written on (Apple clang 17,
libc++, `-O2`, arm64):

| How the integers were read | min | median |
|---|---|---|
| `cin >>`, no `sync_with_stdio` call | 1056.9 ms | 1080.8 ms |
| `cin >>` with `sync_with_stdio(false); cin.tie(nullptr);` | 1038.7 ms | 1080.2 ms |
| `scanf("%lld")` | **61.1 ms** | 62.2 ms |
| hand-rolled `getchar_unlocked` reader | **8.7 ms** | 9.9 ms |
| Python `sys.stdin.buffer.read().split()` | 117.9 ms | 144.1 ms |

Three things in that table are worth more than the rest of this lesson.

### `sync_with_stdio(false)` did essentially nothing here

1056.9 ms against 1038.7 ms is noise. Every tutorial on earth presents these
two lines as the fix for slow input, and on this machine they are not.

The reason is which standard library is underneath. On **GCC with libstdc++**,
which is what Codeforces, ECPC and ICPC judge on, `cin` is synchronised with C
stdio by default and unsynchronising it is a large, well-documented win. On
**Apple clang with libc++**, which is what `g++` on this Mac actually is,
`cin` is slow for a different reason that the flag does not address.

Keep the two lines. They cost nothing, and they matter on the machine that
decides your score. Just do not expect to see them work locally.

> **Unverified here.** The GCC side of that claim is not measured in this repo
> — there is no libstdc++ on this machine. Verify it yourself the first time
> you have an input-heavy problem: submit it twice to Codeforces, once with the
> lines and once without, and read the reported times. Write the result in this
> file.

### Python's I/O beat C++'s `cin` by nine times

117.9 ms against 1056.9 ms. Reading input is the one place Python can be
*faster* than naive C++, because `sys.stdin.buffer.read()` is one system call
into a C-speed split, while `cin >>` parses one number at a time through a
locale-aware stream.

This does not change the conclusion of the
[README](../../README.md) — Python still loses the *computation* by twenty-five
times, and computation is what time limits are about. But it kills a popular
piece of folklore, and it is a good reminder that "C++ is faster" is a
statement about what you measured, not a law.

### Your local timings lie to you about I/O

Because `cin` is ~17× slower here than `scanf`, an input-heavy solution can
look alarmingly slow on this Mac and be comfortably fast on Codeforces. Do not
rewrite a correct solution because of a local timing on an input-heavy problem.
Trust the judge's number; use the local one for correctness and for
*computation*-heavy timing only.

`tools/judge.py` prints a time for each test for exactly one purpose — noticing
an accidental O(n²) — not for predicting the judge.

---

## 2. So what should you actually write?

```cpp
ios_base::sync_with_stdio(false);
cin.tie(nullptr);
```

These two lines, in `main`, always. Then `cin >>` and `cout <<` for everything.

**Do not** start writing `getchar_unlocked` readers. Yes, the table says 8.7 ms
against 1056.9 ms, and no, that does not matter: problems where input parsing
is the bottleneck are rare, the reader is one more thing to get wrong under
pressure, and `getchar_unlocked` is not even portable (it is absent on
Windows judges). Learn that it exists; reach for it on the one problem in a
hundred that reads 10⁷ numbers.

Two rules that come with the two lines:

- **Never mix `cout` with `printf`** in the same program afterwards. Their
  buffers are no longer coordinated, and your output can come out in the wrong
  order — a Wrong Answer with correct logic, which is a miserable way to spend
  an hour.
- **Never use `endl`.** `endl` writes a newline *and flushes the stream*. The
  flush is the expensive part, and in a loop it undoes everything the two lines
  bought you. Write `"\n"`. The only exception is an interactive problem, where
  the judge is waiting for your output and the flush is the point.

---

## 3. Output formatting

Integers need nothing. Floating point needs this:

```cpp
cout << fixed << setprecision(6) << ans << "\n";
```

`fixed` means "not scientific notation", and `setprecision(6)` means six digits
after the decimal point. Both are sticky — set them once in `main`. Problems
that want real numbers always state the required precision; match it exactly,
and never print a `double` without this line, or `1000000.0` can appear as
`1e+06` and score zero.

For problems whose answer is a very long line of numbers, build a `string` and
print it once rather than streaming millions of small writes.

---

## 4. The multiple-test-cases shape

Most modern Codeforces problems look like:

```text
3
5
1 2 3 4 5
1
7
4
-1 -2 -3 -4
```

"First line: t, the number of test cases." The template handles it by
uncommenting one line:

```cpp
int t = 1;
cin >> t;          // <- uncommented
while (t--) solve();
```

The reason `solve()` is a separate function is that every local variable inside
it is created fresh on each call. The classic contest bug is a global array
still holding the previous test case's data — most often a `visited[]` array
that was never reset, so test 2 believes everything is already visited. If
state lives inside `solve()`, that bug is hard to write.

If you *must* use a global array for speed, reset only the part you touched —
clearing a 10⁶-element array for every one of 10⁵ test cases is itself a TLE.

---

## 5. Reading until end of input

Some older problems do not tell you how many test cases there are: read until
input runs out.

```cpp
int a, b;
while (cin >> a >> b) {
    cout << a + b << "\n";
}
```

`cin >> a >> b` evaluates to false when the read fails, which includes end of
file. This is the C++ equivalent of iterating over `sys.stdin`.

---

## 6. The same thing in Python

For when the algorithm, not the contest, is what you need:

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [int(x) for x in data[pos:pos + n]]; pos += n
        out.append(str(sum(a)))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

Two habits worth keeping from this even outside contests: read all of stdin in
one call, and accumulate output in a list and join it once. `print()` per line
in a loop is slow for the same reason `endl` is.

---

## Practice

No new problem list for this lesson. Instead, go back through the thirty
rating-800 problems from lesson 01 and make all of them use the template from
memory — no copy-paste from a previous file.

Then one concrete experiment, which also fills in the gap left above:

1. Pick any Codeforces problem whose input is at least 10⁵ numbers.
2. Submit it with `sync_with_stdio(false)` and note the reported time.
3. Submit the identical code with those two lines deleted and note it again.
4. Write both numbers into §1 of this file, with the submission ids.

That turns the one unmeasured claim in this lesson into a measured one.

**Next:** [03 · Complexity, and reading the constraints](03-complexity-and-constraints.md)
