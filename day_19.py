"""Day 19: Go With The Flow"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 19 puzzles."""
    with open("data/day_19.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    ip, instructions = load_program(puzzle_input)
    registers = execute_instructions(instructions, 6 * [0], ip)

    return registers[0]


def star_2(puzzle_input):
    """Solve second puzzle."""
    ip, instructions = load_program(puzzle_input)
    registers = execute_instructions(instructions, [1] + 5 * [0], ip)

    return registers[0]


def execute(instruction, registers):
    """Execute an instruction."""
    opcode, a, b, c = instruction

    match opcode[:2]:
        case "ad":
            registers = execute_add(opcode, a, b, c, registers)
        case "mu":
            registers = execute_mul(opcode, a, b, c, registers)
        case "ba":
            registers = execute_ban(opcode, a, b, c, registers)
        case "bo":
            registers = execute_bor(opcode, a, b, c, registers)
        case "se":
            registers = execute_set(opcode, a, c, registers)
        case "gt":
            registers = execute_gt(opcode, a, b, c, registers)
        case "eq":
            registers = execute_eq(opcode, a, b, c, registers)

    return registers


def execute_add(opcode, a, b, c, registers):
    """Execute an addition."""
    match opcode:
        case "addr":
            registers[c] = registers[a] + registers[b]
        case "addi":
            registers[c] = registers[a] + b

    return registers


def execute_ban(opcode, a, b, c, registers):
    """Execute a bitwise AND."""
    match opcode:
        case "banr":
            registers[c] = registers[a] & registers[b]
        case "bani":
            registers[c] = registers[a] & b

    return registers


def execute_bor(opcode, a, b, c, registers):
    """Execute a bitwise OR."""
    match opcode:
        case "borr":
            registers[c] = registers[a] | registers[b]
        case "bori":
            registers[c] = registers[a] | b

    return registers


def execute_eq(opcode, a, b, c, registers):
    """Execute an equality testing."""
    match opcode:
        case "eqir":
            registers[c] = int(a == registers[b])
        case "eqri":
            registers[c] = int(registers[a] == b)
        case "eqrr":
            registers[c] = int(registers[a] == registers[b])

    return registers


def execute_gt(opcode, a, b, c, registers):
    """Execute a greater-than testing."""
    match opcode:
        case "gtir":
            registers[c] = int(a > registers[b])
        case "gtri":
            registers[c] = int(registers[a] > b)
        case "gtrr":
            registers[c] = int(registers[a] > registers[b])

    return registers


def execute_instructions(instructions, registers, ip):
    """Execute list of instructions."""
    while 0 <= registers[ip] < len(instructions):
        if registers[ip] == 2:
            registers = execute_loop(instructions[2:12], registers)
        else:
            registers = execute(instructions[registers[ip]], registers)

        registers[ip] += 1

    return registers


def execute_loop(instructions, registers):
    """Execute special loop."""
    while registers[instructions[1][1]] <= registers[instructions[2][2]]:
        if registers[instructions[2][2]] % registers[instructions[1][1]] == 0:
            registers[instructions[5][2]] += registers[instructions[1][1]]

        registers[instructions[1][1]] += 1

    registers[instructions[4][1]] = 11

    return registers


def execute_mul(opcode, a, b, c, registers):
    """Execute a multiplication."""
    match opcode:
        case "mulr":
            registers[c] = registers[a] * registers[b]
        case "muli":
            registers[c] = registers[a] * b

    return registers


def execute_set(opcode, a, c, registers):
    """Execute an assignment."""
    match opcode:
        case "setr":
            registers[c] = registers[a]
        case "seti":
            registers[c] = a

    return registers


def load_program(puzzle_input):
    """Load program from input."""
    ip = int(puzzle_input[0][-1])
    instructions = []

    for line in puzzle_input[1:]:
        opcode, a, b, c = line.split()
        a, b, c = map(int, (a, b, c))
        instructions.append((opcode, a, b, c))

    return ip, tuple(instructions)


if __name__ == "__main__":
    main()
