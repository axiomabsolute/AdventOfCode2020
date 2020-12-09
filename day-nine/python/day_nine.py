from itertools import product
from math import floor
import sys

def sliding_window(entries, n):
    for i in range(len(entries) - n):
        yield entries[i:i+n]

def part_one(lines, preamble_length):
    for idx, window in enumerate(sliding_window(lines, preamble_length)):
        sums = {a + b for a,b in product(window, repeat=2) if a != b}
        next_val = lines[idx + preamble_length]
        if next_val not in sums:
            return next_val, idx + 1

def part_two(lines, preamble_length, invalid_value):
    for run_length in range(2, len(lines) - 1):
        for window in sliding_window(lines[:len(lines) - run_length], run_length):
            if sum(window) == invalid_value:
                return window


if __name__ == "__main__":
    filename = sys.argv[1]
    preamble_length = int(sys.argv[2])

    with open(filename, "r") as inf:
        lines = [int(line.strip()) for line in inf]

        bad_value, bad_position = part_one(lines, preamble_length)
        print(f"Invalid value {bad_value} at position {bad_position}")

        window = part_two(lines, preamble_length, bad_value)
        result = min(window) + max(window)
        print(f"Encryption weakness {result}")
        