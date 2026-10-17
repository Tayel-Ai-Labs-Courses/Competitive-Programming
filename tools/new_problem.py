#!/usr/bin/env python3
"""Scaffold a problem directory so starting a problem costs no typing.

Usage:
    python3 tools/new_problem.py codeforces 4A "Watermelon"
    python3 tools/new_problem.py --url https://codeforces.com/problemset/problem/4/A

Creates problems/<judge>/<id>-<slug>/ with sol.cpp (from templates/template.cpp),
meta.json, and an empty tests/01.in + 01.out for you to paste the sample into.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    url = ""
    if argv[0] == "--url":
        url = argv[1]
        match = re.search(r"problem/(\d+)/([A-Za-z]\d?)", url)
        if not match:
            print("could not read a problem id out of that url; pass it by hand")
            return 1
        judge = "codeforces"
        problem_id = (match.group(1) + match.group(2)).lower()
        title = ""
    else:
        judge = slugify(argv[0])
        problem_id = argv[1].lower()
        title = argv[2] if len(argv) > 2 else ""

    folder = problem_id if not title else f"{problem_id}-{slugify(title)}"
    target = os.path.join(ROOT, "problems", judge, folder)
    if os.path.exists(target):
        print(f"{os.path.relpath(target, ROOT)} already exists")
        return 1

    os.makedirs(os.path.join(target, "tests"))

    with open(os.path.join(ROOT, "templates", "template.cpp"), encoding="utf-8") as handle:
        template = handle.read()
    with open(os.path.join(target, "sol.cpp"), "w", encoding="utf-8") as handle:
        handle.write(template)

    meta = {
        "title": title,
        "url": url,
        "time_limit": 2.0,
        "tags": [],
        "solved_without_help": None,
    }
    with open(os.path.join(target, "meta.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)
        handle.write("\n")

    for suffix in ("in", "out"):
        open(os.path.join(target, "tests", f"01.{suffix}"), "w").close()

    rel = os.path.relpath(target, ROOT)
    print(f"created {rel}")
    print(f"  1. paste the sample into {rel}/tests/01.in and 01.out")
    print(f"  2. solve in {rel}/sol.cpp")
    print(f"  3. python3 tools/judge.py {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
