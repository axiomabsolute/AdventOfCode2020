from functools import reduce
import sys

CARDINAL_DIRECTIONS = ['N', 'E', 'S', 'W']

def rotate(direction, wise, value):
    index = CARDINAL_DIRECTIONS.index(direction)
    new_direction_index = (index + (wise * (value // 90))) % len(CARDINAL_DIRECTIONS)
    return CARDINAL_DIRECTIONS[new_direction_index]

CARDINAL_INSTRUCTIONS = {
    "N": lambda v, d, ew, ns: (d, ew, ns + v),
    "E": lambda v, d, ew, ns: (d, ew + v, ns),
    "S": lambda v, d, ew, ns: (d, ew, ns - v),
    "W": lambda v, d, ew, ns: (d, ew - v, ns),
}

RELATIVE_INSTRUCTIONS = {
    "L": lambda v, d, ew, ns: (rotate(d, -1, v), ew, ns),
    "R": lambda v, d, ew, ns: (rotate(d, 1, v), ew, ns),
    "F": lambda v, d, ew, ns: CARDINAL_INSTRUCTIONS[d](v, d, ew, ns),
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
    return result

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        instructions = [parse_instruction(line) for line in inf]

    heading, ew, ns = reduce(apply_instruction, instructions, ("E", 0, 0))
    print(abs(ew) + abs(ns))
