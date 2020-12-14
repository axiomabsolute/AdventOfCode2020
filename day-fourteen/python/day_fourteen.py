from itertools import product
import sys

def to_binary(num, bits):
    return bin(num)[2:].zfill(bits)

def from_binary(bin_num):
    return int(bin_num, 2)

def mask_value(binary_num, mask):
    return [ mask[i] if mask[i] != "X" else binary_num[i] for i,m in enumerate(mask) ]

def mask_address(address, mask):
    iterables = [  ]
    for i, m in enumerate(mask):
        if m == "0":
            iterables.append([address[i]])
        elif m == "1": 
            iterables.append(["1"])
        else:
            iterables.append(["0", "1"])
    return [from_binary(''.join(p)) for p in product(*iterables)]

def update_registers_1(mask, registers, address, value):
    binary_value = to_binary(value, 36)
    registers = {**registers}
    registers[address] = mask_value(binary_value, mask)
    return registers

def update_registers_2(mask, registers, address, value):
    addresses_to_update = mask_address(to_binary(address, 36), mask)
    new_registers = {**registers}
    for masked_address in addresses_to_update:
        new_registers[masked_address] = value
    return new_registers

def interpret(memory, instructions, apply):
    if not len(instructions):
        return memory
    instruction = instructions[0]
    if instruction.startswith("mask"):
        new_memory = {
            **memory,
            "mask": instruction.split(" = ")[1].strip()
        }
        return interpret(new_memory, instructions[1:], apply)
    elif instruction.startswith("mem"):
        mask = memory["mask"]
        register, value = instruction.split(" = ")
        register = int(register[4:-1])
        value = int(value.strip())
        registers = apply(mask, memory["registers"], register, value)
        new_memory = {
            **memory,
            "registers": registers
        }
        return interpret(new_memory, instructions[1:], apply)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, "r") as inf:
        lines = list(inf)

    memory = interpret({"mask": "".zfill(36), "registers": {}}, lines, update_registers_1)
    result = sum(from_binary(''.join(b)) for b in memory["registers"].values())
    print(result)

    memory = interpret({"mask": "".zfill(36), "registers": {}}, lines, update_registers_2)
    result = sum(memory["registers"].values())
    print(result)
