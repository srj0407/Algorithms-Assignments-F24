from tokenize import group

import algorithms
import os
import brute

def main():
    files = os.listdir("./test_cases")
    for file in files:
        with open("./test_cases/" + file, "r") as test_case:
            days = int(test_case.readline())
            groups = [int(value) for value in test_case.readline().split(",")]
            print(algorithms.log(days, groups), algorithms.poly(days, groups), brute.solve(days, groups))


if __name__ == "__main__":
    main()