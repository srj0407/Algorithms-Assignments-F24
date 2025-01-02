import math

def shift(counts, currents, sums, index):
    currents[index] -= 1

    curr = counts[currents[index]]
    sums[index] -= curr
    sums[index + 1] += curr


def poly(days, counts):
    if len(counts) == 0:
        return 0

    if days == 1:
        return sum(counts)

    if days >= len(counts):
        return max(counts)

    currents = [len(counts)] * (days - 1)
    sums = [0] * days
    sums[0] = sum(counts)

    while True:
        index, best = max(*enumerate(sums), key=lambda x: x[1])
        if index == days - 1:
            return best

        shift(counts, currents, sums, index)
        for i in range(index + 1, days):
            if sums[i] > best:
                if i == days - 1:
                    return best

                shift(counts, currents, sums, i)
                while sums[i] > best:
                    shift(counts, currents, sums, i)
            else:
                break


def get_days(size, counts):
    days = -1
    curr = size
    for count in counts:
        if count > size:
            return math.inf

        curr += count
        if curr > size:
            days += 1
            curr = count

    return days + 1


def log(days, counts):
    if len(counts) == 0:
        return 0

    low = max(counts)
    high = sum(counts)

    if low == high:
        return low

    while low + 1 != high:
        mid = (low + high) // 2
        curr_days = get_days(mid, counts)

        if days < curr_days:
            low = mid
        else:
            high = mid

    if get_days(low, counts) <= days:
        return low
    else:
        return high


poly(3, [1, 1, 2, 1, 1])
