"""Day 2: Inventory Management System"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from collections import Counter


def main():
    """Solve day 2 puzzles."""
    with open("data/day_2.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    twos = 0
    threes = 0

    for line in puzzle_input:
        counter = Counter(line)
        twos += 2 in counter.values()
        threes += 3 in counter.values()

    return twos * threes


def star_2(puzzle_input):
    """Solve second puzzle."""
    for id_0, id_1 in itertools.combinations(puzzle_input, 2):
        for i, _ in enumerate(id_0):
            if id_0[:i] + id_0[i + 1 :] == id_1[:i] + id_1[i + 1 :]:
                return id_0[:i] + id_0[i + 1 :]

    return None


if __name__ == "__main__":
    main()
