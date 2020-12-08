import sys


def part_one(instructions):
    acc = 0
    visited = set()
    i = 0
    instruction_sequence = []
    while True:
        if i in visited:
            return acc, instruction_sequence, True
        else:
            if i >= len(instructions):
                break
            prev = i
            visited.add(i)
            instruction_sequence.append((i, instructions[i]))

        instruction, count = instructions[i].split()
        count = int(count)

        if instruction == "acc":
            i += 1
            acc += count
        elif instruction == "nop":
            i += 1
        else:
            i += count

    return acc, instruction_sequence, False


def part_two(instructions, seq):
    for line_number, instruction in seq:
        if instruction.startswith("acc"):
            continue
        altered = [*instructions]
        if instruction.startswith("jmp"):
            altered[line_number] = altered[line_number].replace("jmp", "nop")
        elif instruction.startswith("nop"):
            altered[line_number] = altered[line_number].replace("nop", "jmp")
        acc, seq, early_terminated = part_one(altered)
        if not early_terminated:
            return acc, seq, line_number


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        instructions = [line.strip() for line in inf]

        acc, seq, early_terminated = part_one(instructions)
        print(f"Program terminated: {acc} acc")

        acc, seq, changed_line = part_two(instructions, seq)
        print(f"Program fixed: {acc} acc, changed {changed_line}")