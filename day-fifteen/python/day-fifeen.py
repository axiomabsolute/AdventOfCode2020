from collections import defaultdict
from functools import reduce
import json
import sys

def bootstrap_game(seq):
    memory = defaultdict(lambda: [None, None])
    last = None
    turn = 0
    for s in seq:
        s = int(s)
        turn += 1
        last = s
        _, later = memory[s]
        memory[s][0] = later
        memory[s][1] = turn
    return turn, last, memory

def play_until_turn(turn, last, memory, target_turn):
    while turn < target_turn:
        turn += 1
        if memory[last][0] is None:
            current = 0
        else:
            current = memory[last][1] - memory[last][0]
        memory[current][0] = memory[current][1]
        memory[current][1] = turn
        last = current
    return last, memory


if __name__ == "__main__":
    filename = sys.argv[1]
    nth_number = int(sys.argv[2])

    with open(filename, "r") as inf:
        seq = next(inf).split(",")

    turn, last, memory = bootstrap_game(seq)
    last, memory = play_until_turn(turn, last, memory, nth_number)
    print(last)
