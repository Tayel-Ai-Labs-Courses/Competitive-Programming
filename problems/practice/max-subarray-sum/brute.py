# O(n^2): try every (start, end) pair. Obviously correct, far too slow to
# submit, which is exactly what makes it a good oracle.
import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [int(x) for x in data[1 : 1 + n]]

best = None
for i in range(n):
    total = 0
    for j in range(i, n):
        total += a[j]
        if best is None or total > best:
            best = total

print(best)
