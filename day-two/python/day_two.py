import re
import sys

PATTERN = r"(?P<minimum>\d+)-(?P<maximum>\d+) (?P<pattern>.): (?P<candidate>.+)"

def parse_line(line):
    matches = re.match(PATTERN, line)
    return matches.groupdict()

def is_valid(minimum, maximum, pattern, candidate):
    minimum = int(minimum)
    maximum = int(maximum)
    return minimum <= candidate.count(pattern) <= maximum

def is_valid_part_two(minimum, maximum, pattern, candidate):
    p1 = int(minimum) - 1
    p2 = int(maximum) - 1
    return (candidate[p1] == pattern or candidate[p2] == pattern) and not (candidate[p1] == pattern and candidate[p2] == pattern)

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, 'r') as inf:
        valid = [line for line in inf if is_valid(**parse_line(line))]
        print(f"Valid 1: {len(valid)}")

    with open(filename, 'r') as inf:
        valid = [line for line in inf if is_valid_part_two(**parse_line(line))]
        print(f"Valid 2: {len(valid)}")