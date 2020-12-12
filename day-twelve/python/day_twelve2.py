from functools import reduce
from math import sin, cos, pi
import sys

SINS = [0, 1, 0, -1]
COSS = [1, 0, -1, 0]

def rotate(direction, wise, value):
    x, y = direction
    shift = ( wise * (value // 90)) % 4
    return (
        x * COSS[shift] - (y * SINS[shift]),
        x * SINS[shift] + (y * COSS[shift])
    )


CARDINAL_INSTRUCTIONS = {
    "N": lambda v, d, ew, ns: ((d[0], d[1] + v), ew, ns),
    "E": lambda v, d, ew, ns: ((d[0] + v, d[1]), ew, ns),
    "S": lambda v, d, ew, ns: ((d[0], d[1] - v), ew, ns),
    "W": lambda v, d, ew, ns: ((d[0] - v, d[1]), ew, ns),
}

RELATIVE_INSTRUCTIONS = {
    "L": lambda v, d, ew, ns: (rotate(d, 1, v), ew, ns),
    "R": lambda v, d, ew, ns: (rotate(d, -1, v), ew, ns),
    "F": lambda v, d, ew, ns: (d, ew + (v * d[0]), ns + (v * d[1])),
}

INSTRUCTIONS = {
    **CARDINAL_INSTRUCTIONS,
    **RELATIVE_INSTRUCTIONS,
}


def parse_instruction(line):
    line = line.strip()
    instruction = line[0]
    value = int(line[1:])
    return (instruction, value)


def apply_instruction(state, next_instruction):
    instruction, value = next_instruction
    direction, ew, ns = state
    implementation = INSTRUCTIONS[instruction]
    result = implementation(value, direction, ew, ns)
    print(result)
    return result

if __name__ == "__main__":
    filename = sys.argv[1]

    HEADING = (10, 1)

    with open(filename, "r") as inf:
        instructions = [parse_instruction(line) for line in inf]

    heading, ew, ns = reduce(apply_instruction, instructions, (HEADING, 0, 0))
    print(abs(ew) + abs(ns))
