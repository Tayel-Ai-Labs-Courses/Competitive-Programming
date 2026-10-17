#!/usr/bin/env python3
"""Local judge: compile a solution, run it against every test, compare output.

A problem directory looks like this:

    problems/<judge>/<slug>/
        sol.cpp          the solution that gets submitted
        brute.py         optional, a slow-but-obviously-correct version
        gen.py           optional, prints one random test (used by stress.py)
        meta.json        optional, {"time_limit": 2.0, "url": "...", "tags": [...]}
        tests/01.in      input
        tests/01.out     expected output

Comparison is token-based, like a real judge: runs of whitespace are equal, and
trailing newlines do not matter. Exit code is non-zero if any test fails, so CI
can call this.

Usage:
    python3 tools/judge.py problems/codeforces/4a-watermelon
    python3 tools/judge.py problems/codeforces/4a-watermelon --debug
    python3 tools/judge.py --all
"""

import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(ROOT, ".build")
DEFAULT_TIME_LIMIT = 2.0

# -O2 matches what Codeforces does; the warnings catch the mistakes that cost
# an hour in a contest (uninitialised reads, signed overflow, bad formats).
# -I include/ supplies our hand-written bits/stdc++.h, which Apple clang lacks.
CXX_FLAGS = [
    "-std=c++17",
    "-O2",
    "-Wall",
    "-Wextra",
    "-Wshadow",
    "-I",
    os.path.join(ROOT, "include"),
]

# --debug swaps -O2 for the sanitizers. They make the program several times
# slower, and in exchange an out-of-bounds vector access or a signed overflow
# becomes a loud error message with a line number instead of a silent wrong
# answer. Run a failing problem this way before you start reading the code.
DEBUG_FLAGS = [
    "-std=c++17",
    "-g",
    "-O1",
    "-fsanitize=address,undefined",
    "-fno-omit-frame-pointer",
    "-Wall",
    "-Wextra",
    "-Wshadow",
    "-I",
    os.path.join(ROOT, "include"),
]

GREEN, RED, YELLOW, GREY, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"


def tokens(text):
    return text.split()


def compile_cpp(source, binary, debug=False):
    """Compile source to binary. Returns (ok, stderr)."""
    os.makedirs(os.path.dirname(binary), exist_ok=True)
    flags = DEBUG_FLAGS if debug else CXX_FLAGS
    proc = subprocess.run(
        ["g++", *flags, source, "-o", binary],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0, proc.stderr


def run_once(command, stdin_text, time_limit):
    """Run command feeding it stdin_text. Returns (status, stdout, stderr, seconds)."""
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            command,
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=time_limit,
        )
    except subprocess.TimeoutExpired:
        return "TLE", "", "", time.perf_counter() - start
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        return "RTE", proc.stdout, proc.stderr, elapsed
    return "OK", proc.stdout, proc.stderr, elapsed


def load_meta(problem_dir):
    path = os.path.join(problem_dir, "meta.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def judge(problem_dir, verbose=True, debug=False):
    """Judge one problem directory.

    Returns True if every test passed, False if any failed, and None if the
    problem has been scaffolded but not solved yet (all tests still empty).
    """
    name = os.path.relpath(problem_dir, ROOT)
    source = os.path.join(problem_dir, "sol.cpp")
    if not os.path.exists(source):
        print(f"{RED}no sol.cpp{RESET}  {name}")
        return False

    meta = load_meta(problem_dir)
    time_limit = float(meta.get("time_limit", DEFAULT_TIME_LIMIT))

    binary = os.path.join(BUILD_DIR, name.replace(os.sep, "_"))
    ok, stderr = compile_cpp(source, binary, debug=debug)
    if not ok:
        print(f"{RED}CE{RESET}        {name}")
        if verbose:
            print(stderr.rstrip())
        return False
    if stderr.strip() and verbose:
        print(f"{YELLOW}warnings{RESET}  {name}")
        print(stderr.rstrip())

    tests_dir = os.path.join(problem_dir, "tests")
    inputs = sorted(
        f for f in os.listdir(tests_dir) if f.endswith(".in")
    ) if os.path.isdir(tests_dir) else []
    if not inputs:
        print(f"{YELLOW}no tests{RESET}  {name}")
        return False

    # A scaffolded-but-unsolved problem has empty .in/.out files. An empty
    # program prints nothing, nothing "equals" nothing, and the judge would
    # report AC - a green tick for an unwritten solution. Catch that here.
    def is_blank(path):
        try:
            with open(path, encoding="utf-8") as handle:
                return not handle.read().strip()
        except OSError:
            return True

    if all(
        is_blank(os.path.join(tests_dir, f)) for f in inputs
    ) and all(
        is_blank(os.path.join(tests_dir, f[:-3] + ".out")) for f in inputs
    ):
        print(f"{YELLOW}pending{RESET}   {name} - tests are still empty")
        return None

    all_passed = True
    for input_name in inputs:
        stem = input_name[:-3]
        with open(os.path.join(tests_dir, input_name), encoding="utf-8") as handle:
            stdin_text = handle.read()
        expected_path = os.path.join(tests_dir, stem + ".out")
        if not os.path.exists(expected_path):
            print(f"{YELLOW}no .out{RESET}   {name} [{stem}]")
            all_passed = False
            continue
        with open(expected_path, encoding="utf-8") as handle:
            expected = handle.read()

        status, stdout, stderr, elapsed = run_once([binary], stdin_text, time_limit)
        if status == "TLE":
            print(f"{RED}TLE{RESET}       {name} [{stem}] > {time_limit:.1f}s")
            all_passed = False
            continue
        if status == "RTE":
            print(f"{RED}RTE{RESET}       {name} [{stem}]")
            if verbose and stderr.strip():
                print(stderr.rstrip())
            all_passed = False
            continue
        if tokens(stdout) != tokens(expected):
            print(f"{RED}WA{RESET}        {name} [{stem}]")
            if verbose:
                print(f"  {GREY}input   {RESET}{stdin_text.strip()[:200]}")
                print(f"  {GREY}expected{RESET}{expected.strip()[:200]}")
                print(f"  {GREY}got     {RESET}{stdout.strip()[:200]}")
            all_passed = False
            continue
        if verbose:
            print(f"{GREEN}AC{RESET}        {name} [{stem}] {elapsed * 1000:.0f}ms")

    return all_passed


def find_problems():
    base = os.path.join(ROOT, "problems")
    found = []
    for dirpath, _dirnames, filenames in os.walk(base):
        if "sol.cpp" in filenames:
            found.append(dirpath)
    return sorted(found)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    debug = "--debug" in argv
    argv = [a for a in argv if a != "--debug"]

    if argv[0] == "--all":
        problems = find_problems()
        if not problems:
            print("no problems with a sol.cpp yet")
            return 0
        results = {p: judge(p) for p in problems}
        failed = [p for p, r in results.items() if r is False]
        pending = [p for p, r in results.items() if r is None]
        passed = [p for p, r in results.items() if r is True]
        print()
        summary = f"{len(passed)}/{len(passed) + len(failed)} solved problems pass"
        if pending:
            summary += f", {len(pending)} pending (scaffolded, not solved yet)"
        print(summary)
        return 1 if failed else 0

    target = os.path.abspath(argv[0])
    return 0 if judge(target, debug=debug) is not False else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
