# Prints one random test. Tiny on purpose: a bug that needs n=1000 to show up
# is rare, and a failing case you can read with your eyes is worth ten you
# cannot.
import random
import sys

random.seed(int(sys.argv[1]))

n = random.randint(1, 6)
print(n)
print(*[random.randint(-10, 10) for _ in range(n)])
