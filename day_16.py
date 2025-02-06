"""Day 16: Chronal Classification"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from dataclasses import dataclass

OPCODES = [
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
]


@dataclass
class Sample:
    """Sample of opcode application."""

    before: tuple[int]
    opcode: int
    a: int
    b: int
    c: int
    after: tuple[int]


def main():
    """Solve day 16 puzzles."""
    with open("data/day_16.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    samples, _ = load_samples_test(puzzle_input)

    return sum(
        sum(
            sample.after
            == execute(opcode, sample.a, sample.b, sample.c, sample.before)
            for opcode in OPCODES
        )
        >= 3
        for sample in samples
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    samples, test = load_samples_test(puzzle_input)

    candidates = {i: set(OPCODES) for i in range(len(OPCODES))}
    opcodes = {}

    while candidates:
        sample = samples.pop()

        if sample.opcode in opcodes:
            continue

        incompatible = {
            opcode
            for opcode in candidates[sample.opcode]
            if sample.after
            != execute(opcode, sample.a, sample.b, sample.c, sample.before)
        }

        candidates[sample.opcode] -= incompatible

        while any(len(candidate) == 1 for candidate in candidates.values()):
            opcodes, candidates = simplify(opcodes, candidates)

    registers = 4 * [0]

    for opcode, a, b, c in test:
        registers = execute(opcodes[opcode], a, b, c, registers)

    return registers[0]


def execute(opcode, a, b, c, registers):
    """Execute an instruction."""
    registers = list(registers)

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

    return tuple(registers)


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


def load_samples_test(puzzle_input):
    """Load samples and test from input."""
    samples = []
    i = 0

    while "Before" in puzzle_input[i]:
        before = tuple(map(int, puzzle_input[i][9:-1].split(",")))
        opcode, a, b, c = map(int, puzzle_input[i + 1].split())
        after = tuple(map(int, puzzle_input[i + 2][9:-1].split(",")))
        samples.append(Sample(before, opcode, a, b, c, after))
        i += 4

    test = [tuple(map(int, line.split())) for line in puzzle_input[i + 2 :]]

    return samples, test


def simplify(opcodes, candidates):
    """Simplify candidates."""
    for k, v in candidates.items():
        if len(v) == 1:
            value = tuple(v)[0]
            opcodes[k] = value
            del candidates[k]

            for kk in candidates:
                candidates[kk] -= v

            break

    return opcodes, candidates


if __name__ == "__main__":
    main()
