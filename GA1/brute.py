import math
import random as rd

import algorithms as ag

def solve(days, counts):
    if len(counts) == 0:
        return 0

    if days == 1:
        return sum(counts)

    lowest = math.inf
    for i in range(len(counts)):
        curr = max(sum(counts[:i]), solve(days - 1, counts[i:]))

        if curr < lowest:
            lowest = curr

    return lowest


def generate():
    return rd.randint(1, 5), [rd.randint(0, 25) for i in range(rd.randint(0, 25))]


def test():
    days, counts = generate()

    l, p, t = ag.log(days, counts), ag.poly(days, counts), solve(days, counts)
    print('\033[92m' if l == t and p == t else f'\033[91m{days}, {counts} ', end='')
    print(l, p, t, end='')
    print('\033[0m')


if __name__ == "__main__":
    for i in range(256):
        test()
