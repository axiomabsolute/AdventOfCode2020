from itertools import combinations

import json
import sys

def expensify(values, n, target):
    candidate = next(tup for tup in combinations(values, n) if sum(tup) == target)
    print(candidate)
    product = 1
    for i in candidate:
        product = product * i
    return product


if __name__ == "__main__":
    file_name = sys.argv[1]
    count = int(sys.argv[2])
    target = int(sys.argv[3])
    with open(file_name, "r") as inf:
        data = [json.loads(r) for r in inf]
        print(expensify(data, count, target))


