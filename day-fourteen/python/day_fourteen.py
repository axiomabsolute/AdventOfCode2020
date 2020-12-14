import sys

def to_binary(num, bits):
    return bin(num)[2:].zfill(bits)

def from_binary(bin_num):
    return int(bin_num, 2)

def mask_value(binary_num, mask):
    return [ mask[i] if mask[i] != "X" else binary_num[i] for i,m in enumerate(mask) ]

def interpret(memory, instructions):
    if not len(instructions):
        return memory
    instruction = instructions[0]
    if instruction.startswith("mask"):
        new_memory = {
            **memory,
            "mask": instruction.split(" = ")[1].strip()
        }
        return interpret(new_memory, instructions[1:])
    elif instruction.startswith("mem"):
        mask = memory["mask"]
        register, value = instruction.split(" = ")
        register = int(register[4:-1])
        value = int(value.strip())
        binary_value = to_binary(value, 36)
        registers = {**memory["registers"]}
        registers[register] = mask_value(binary_value, mask)
        new_memory = {
            **memory,
            "registers": registers
        }
        return interpret(new_memory, instructions[1:])


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        lines = list(inf)

    memory = interpret({"mask": "".zfill(36), "registers": {}}, lines)
    result = sum(from_binary(''.join(b)) for b in memory["registers"].values())
    print(result)
