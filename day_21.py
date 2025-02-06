"""Day 21: Chronal Conversion"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 21 puzzles."""
    with open("data/day_21.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    instructions = load_program(puzzle_input)
    values = get_values(instructions)

    return values[0]


def star_2(puzzle_input):
    """Solve second puzzle."""
    instructions = load_program(puzzle_input)
    values = get_values(instructions)

    return values[-1]


def get_values(instructions):
    """Get halting values."""
    values = []
    a = instructions[5][1]

    while True:
        b = a | instructions[6][2]
        a = instructions[7][1]

        while b > 0:
            a = (
                ((a + (b & instructions[8][2])) & instructions[10][2])
                * instructions[11][2]
            ) & instructions[12][2]
            b //= instructions[8][2] + 1

        if a in values:
            return values

        values.append(a)


def load_program(puzzle_input):
    """Load program from input."""
    instructions = []

    for line in puzzle_input[1:]:
        opcode, a, b, c = line.split()
        a, b, c = map(int, (a, b, c))
        instructions.append((opcode, a, b, c))

    return tuple(instructions)


if __name__ == "__main__":
    main()
