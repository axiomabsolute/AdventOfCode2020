from collections import defaultdict
from functools import reduce
import json
import sys

def bootstrap_game(seq):
    memory = defaultdict(lambda: [])
    last = None
    turn = 0
    for s in seq:
        s = int(s)
        turn += 1
        last = s
        memory[s].append(turn)
        # print(s)
    return turn, last, memory

def play_until_turn(turn, last, memory, target_turn):
    while turn < target_turn:
        turn += 1
        if len(memory[last]) == 1:
            current = 0
        else:
            current = memory[last][-1] - memory[last][-2]
        memory[current].append(turn)
        last = current
        memory[current] = memory[current][-2:]
        # print(current)
    return last, memory


if __name__ == "__main__":
    filename = sys.argv[1]
    nth_number = int(sys.argv[2])

    with open(filename, "r") as inf:
        seq = next(inf).split(",")

    turn, last, memory = bootstrap_game(seq)
    last, memory = play_until_turn(turn, last, memory, nth_number)
    print(last)
    # with open("output.json", "w") as outf:
    #     json.dump(memory, outf)