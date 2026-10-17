# problems/

The actual record. Lessons are scaffolding; this directory is the training.

## Layout

```
problems/<judge>/<id>-<slug>/
    sol.cpp       the submitted solution
    brute.py      optional: the slow oracle for tools/stress.py
    gen.py        optional: the random test generator
    meta.json     url, rating, tags, and whether you needed help
    tests/        NN.in and NN.out, including cases found by stress testing
```

Scaffold one with:

```bash
python3 tools/new_problem.py codeforces 158A "Next Round"
```

## The two rules

**Nothing lands here until `tools/judge.py` prints AC.** CI re-runs every
solution on every push, so a solution that stops compiling cannot hide.

**Write a comment at the top of `sol.cpp` saying what the problem actually
was.** One or two sentences: the idea, and the trap. Not a restatement of the
statement — the *insight*. Reading your own one-line summaries from three
months ago is the cheapest revision that exists, and a solution with no comment
is a solution you will not recognise.

See `codeforces/4a-watermelon/sol.cpp` and
`practice/max-subarray-sum/sol.cpp` for the intended tone. The second one
documents the bug the stress tester found, and keeps the failing test as
`tests/01-all-negative.in`.

## `meta.json`

```json
{
  "title": "Next Round",
  "url": "https://codeforces.com/problemset/problem/158/A",
  "time_limit": 2.0,
  "rating": 800,
  "tags": ["implementation"],
  "solved_without_help": true
}
```

`solved_without_help` is the field that matters. Set it to `false` whenever you
read an editorial, and re-solve that problem from a blank file two weeks later.
A directory full of `true` is progress; a directory full of `false` is a
reading list.
