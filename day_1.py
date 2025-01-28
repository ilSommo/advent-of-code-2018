"""Day 1: Chronal Calibration"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 1 puzzles."""
    with open("data/day_1.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return sum(int(line) for line in puzzle_input)


def star_2(puzzle_input):
    """Solve second puzzle."""
    base_frequencies = [0]

    for line in puzzle_input:
        base_frequencies.append(base_frequencies[-1] + int(line))

    offset = base_frequencies[-1]
    base_frequencies.pop(-1)
    frequencies = set(base_frequencies)
    i = 1

    while True:
        for frequency in base_frequencies:
            new_frequency = frequency + i * offset

            if new_frequency in frequencies:
                return new_frequency

            frequencies.add(new_frequency)

        i += 1


if __name__ == "__main__":
    main()
