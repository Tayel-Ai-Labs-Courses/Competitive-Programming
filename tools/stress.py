#!/usr/bin/env python3
"""Stress tester: hunt for the test case that breaks your solution.

This is the single most useful debugging tool in competitive programming. When
the judge says "Wrong answer on test 7" and hides test 7, you do not guess. You
write a generator and a brute force, and let the machine find a small failing
case for you.

A problem directory needs three files for this to work:

    sol.cpp      the fast solution you suspect is wrong
    brute.py     a slow version that is obviously correct (O(n^3) is fine)
    gen.py       prints one random SMALL test to stdout

gen.py is called with a seed as argv[1], so the loop is reproducible:

    import random, sys
    random.seed(int(sys.argv[1]))
    n = random.randint(1, 8)
    print(n)
    print(*[random.randint(1, 10) for _ in range(n)])

Keep the generated tests tiny. A bug that shows up at n=1000 almost always
shows up at n=5 too, and you can read n=5 with your eyes.

Usage:
    python3 tools/stress.py problems/codeforces/4a-watermelon
    python3 tools/stress.py problems/codeforces/4a-watermelon -n 2000
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from judge import CXX_FLAGS, BUILD_DIR, compile_cpp, run_once, tokens  # noqa: E402

GREEN, RED, GREY, RESET = "\033[32m", "\033[31m", "\033[90m", "\033[0m"


def stress(problem_dir, iterations):
    name = os.path.relpath(problem_dir, ROOT)
    source = os.path.join(problem_dir, "sol.cpp")
    brute = os.path.join(problem_dir, "brute.py")
    gen = os.path.join(problem_dir, "gen.py")

    for path, what in ((source, "sol.cpp"), (brute, "brute.py"), (gen, "gen.py")):
        if not os.path.exists(path):
            print(f"{RED}missing {what}{RESET} in {name}")
            print(__doc__)
            return 1

    binary = os.path.join(BUILD_DIR, name.replace(os.sep, "_") + "_stress")
    ok, stderr = compile_cpp(source, binary)
    if not ok:
        print(f"{RED}compile error{RESET}")
        print(stderr.rstrip())
        return 1

    for seed in range(1, iterations + 1):
        made = subprocess.run(
            [sys.executable, gen, str(seed)], capture_output=True, text=True
        )
        if made.returncode != 0:
            print(f"{RED}gen.py crashed on seed {seed}{RESET}")
            print(made.stderr.rstrip())
            return 1
        test = made.stdout

        fast_status, fast_out, fast_err, _ = run_once([binary], test, 10.0)
        slow_status, slow_out, slow_err, _ = run_once(
            [sys.executable, brute], test, 10.0
        )

        if slow_status != "OK":
            print(f"{RED}brute.py {slow_status} on seed {seed}{RESET}")
            print(slow_err.rstrip())
            return 1

        broke = fast_status != "OK" or tokens(fast_out) != tokens(slow_out)
        if broke:
            fail_path = os.path.join(problem_dir, "tests", "fail.in")
            os.makedirs(os.path.dirname(fail_path), exist_ok=True)
            with open(fail_path, "w", encoding="utf-8") as handle:
                handle.write(test)
            with open(fail_path[:-3] + ".out", "w", encoding="utf-8") as handle:
                handle.write(slow_out)

            print(f"{RED}mismatch on seed {seed}{RESET} after {seed - 1} passing tests")
            print(f"{GREY}input{RESET}")
            print(test.rstrip())
            print(f"{GREY}brute.py says{RESET}  {slow_out.strip()}")
            if fast_status == "OK":
                print(f"{GREY}sol.cpp says {RESET}  {fast_out.strip()}")
            else:
                print(f"{GREY}sol.cpp     {RESET}  {fast_status}")
                if fast_err.strip():
                    print(fast_err.rstrip())
            print()
            print(f"saved as {os.path.relpath(fail_path, ROOT)} - now fix sol.cpp")
            print("and re-run; the test stays in tests/ as a regression check.")
            return 1

        if seed % 100 == 0:
            print(f"{GREY}{seed} tests, no mismatch{RESET}")

    print(f"{GREEN}{iterations} random tests, sol.cpp agrees with brute.py everywhere{RESET}")
    print("That is evidence, not proof - the bug may need a bigger or weirder test.")
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    target = os.path.abspath(argv[0])
    iterations = 500
    if "-n" in argv:
        iterations = int(argv[argv.index("-n") + 1])
    return stress(target, iterations)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
