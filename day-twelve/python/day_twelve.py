from functools import partial, reduce
import sys

CARDINAL_DIRECTIONS = ['N', 'E', 'S', 'W']

# I'm mad I have to do this, but Python isn't clever enough
# for exact radian sin/cos functions
SINS = [0, 1, 0, -1]
COSS = [1, 0, -1, 0]

def rotate(direction, wise, value):
    index = CARDINAL_DIRECTIONS.index(direction)
    new_direction_index = (index + (wise * (value // 90))) % len(CARDINAL_DIRECTIONS)
    return CARDINAL_DIRECTIONS[new_direction_index]

def rotate_about_origin(direction, wise, value):
    x, y = direction
    shift = ( wise * (value // 90)) % 4
    return (
        x * COSS[shift] - (y * SINS[shift]),
        x * SINS[shift] + (y * COSS[shift])
    )

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

WAYPOINT_CARDINAL_INSTRUCTIONS = {
    "N": lambda v, d, ew, ns: ((d[0], d[1] + v), ew, ns),
    "E": lambda v, d, ew, ns: ((d[0] + v, d[1]), ew, ns),
    "S": lambda v, d, ew, ns: ((d[0], d[1] - v), ew, ns),
    "W": lambda v, d, ew, ns: ((d[0] - v, d[1]), ew, ns),
}

WAYPOINT_RELATIVE_INSTRUCTIONS = {
    "L": lambda v, d, ew, ns: (rotate_about_origin(d, 1, v), ew, ns),
    "R": lambda v, d, ew, ns: (rotate_about_origin(d, -1, v), ew, ns),
    "F": lambda v, d, ew, ns: (d, ew + (v * d[0]), ns + (v * d[1])),
}

WAYPOINT_INSTRUCTIONS = {
    **WAYPOINT_CARDINAL_INSTRUCTIONS,
    **WAYPOINT_RELATIVE_INSTRUCTIONS,
}


def parse_instruction(line):
    line = line.strip()
    instruction = line[0]
    value = int(line[1:])
    return (instruction, value)


def apply_instruction(instruction_set, state, next_instruction):
    instruction, value = next_instruction
    direction, ew, ns = state
    implementation = instruction_set[instruction]
    result = implementation(value, direction, ew, ns)
    return result

if __name__ == "__main__":
    filename = sys.argv[1]

    HEADING = (10, 1)

    with open(filename, "r") as inf:
        instructions = [parse_instruction(line) for line in inf]

    heading, ew, ns = reduce(partial(apply_instruction, INSTRUCTIONS), instructions, ("E", 0, 0))
    print(abs(ew) + abs(ns))
    
    heading, ew, ns = reduce(partial(apply_instruction, WAYPOINT_INSTRUCTIONS), instructions, (HEADING, 0, 0))
    print(abs(ew) + abs(ns))
