from itertools import product
import sys

def parse_input(lines, dimensions):
    pad_by = dimensions - 2
    zeros = tuple(0 for n in range(pad_by))
    for y, row in enumerate(lines):
        for x, state in enumerate(row):
            if state == "#":
                result = (x, y, *zeros)
                yield result

def generate_neighbors(*coord):
    neighbors_by_coord = (tuple(t) for t in product(*(range(c-1, c+2) for c in coord)))
    for n in neighbors_by_coord:
        if n != coord:
            yield n

def cycle(initial_state):
    """initial_state is a set of active (x, y, z) coordinates"""
    # Set of all (x, y, z) coordinates next to at least one active coordinate
    candidates = {c for state in initial_state for c in generate_neighbors(*state)}
    # Dict mapping candidate coordinate to sequence of neighbors
    neighbors_by_candidates = {candidate: generate_neighbors(*candidate) for candidate in candidates}
    # Dict mapping candidate coordinate to count of active neighbors
    candidate_active_neighbor_counts = {candidate: sum(1 for n in neighbors if n in initial_state) for candidate, neighbors in neighbors_by_candidates.items()}
    result = set()
    for candidate, active_neighbor_count in candidate_active_neighbor_counts.items():
        if candidate in initial_state:
            if 1 < active_neighbor_count < 4:
                result.add(candidate)
        else:
            if active_neighbor_count == 3:
                result.add(candidate)
    return result


def game(initial_state, till_cycle_number):
    for i in range(till_cycle_number):
        initial_state = cycle(initial_state)
    return initial_state


def part_one(state):
    return len(state)


if __name__ == "__main__":
    filename = sys.argv[1]
    cycles = int(sys.argv[2])
    dimensions = int(sys.argv[3])

    with open(filename, "r") as inf:
        initial_state = set(parse_input(inf, dimensions))

    result = game(initial_state, cycles)

    print(part_one(result))