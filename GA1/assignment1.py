import math

#helper function for log()
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


#takes days and array of clubs and returns min number attendees
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


def min_num_attendees(input_file, output_file):
    with open(input_file, "r") as test_case:
        days = int(test_case.readline())
        groups = [int(value) for value in test_case.readline().split(",")]
        # print(algorithms.log(days, groups), algorithms.poly(days, groups), brute.solve(days, groups))
        with open(output_file, "w+") as output_file:
            output_file.write(str(log(days, groups)))


def main():
    min_num_attendees("./test_cases/1", "output_test.txt")


if __name__ == '__main__':
    main()