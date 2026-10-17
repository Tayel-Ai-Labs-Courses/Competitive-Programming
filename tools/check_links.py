#!/usr/bin/env python3
"""Check that every relative link in every markdown file points at something.

A lesson that links to a file that does not exist is worse than one that does
not link at all, because the reader trusts it. CI runs this.

Fenced code blocks are skipped: C++ lambdas start with `[]`, which the link
regex would otherwise read as a markdown link with an empty label.

Usage:
    python3 tools/check_links.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".build", "node_modules"}
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")


def strip_code(text):
    """Blank out fenced code blocks, keeping line count so numbers stay right."""
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def main():
    broken = []
    checked = 0
    files = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            files += 1
            path = os.path.join(dirpath, filename)
            with open(path, encoding="utf-8") as handle:
                text = strip_code(handle.read())

            for lineno, line in enumerate(text.split("\n"), start=1):
                for match in LINK.finditer(line):
                    target = match.group(2)
                    if target.startswith(EXTERNAL):
                        continue
                    checked += 1
                    relative = target.split("#")[0]
                    if not relative:
                        continue
                    resolved = os.path.normpath(os.path.join(dirpath, relative))
                    if not os.path.exists(resolved):
                        broken.append(
                            (os.path.relpath(path, ROOT), lineno, target)
                        )

    print(f"{files} markdown files, {checked} relative links")
    if broken:
        for src, lineno, target in broken:
            print(f"  BROKEN  {src}:{lineno} -> {target}")
        print(f"{len(broken)} broken")
        return 1
    print("all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
