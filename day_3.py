"""Day 3: No Matter How You Slice It"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from functools import cache


def main():
    """Solve day 3 puzzles."""
    with open("data/day_3.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    common = compute_common(puzzle_input)

    return len(common)


def star_2(puzzle_input):
    """Solve second puzzle."""
    common = compute_common(puzzle_input)

    for claim, squares in load_claims(puzzle_input).items():
        if not squares & common:
            return claim

    return 0


@cache
def compute_common(puzzle_input):
    """Compute common squares."""
    squares = load_claims(puzzle_input).values()

    return set.union(
        *(
            squares_0 & squares_1
            for squares_0, squares_1 in itertools.combinations(squares, 2)
        )
    )


def load_claims(puzzle_input):
    """Load claims from input."""
    claims = {}

    for line in puzzle_input:
        chunks = line.split()
        x, y = map(int, chunks[2][:-1].split(","))
        w, h = map(int, chunks[-1].split("x"))
        claims[int(chunks[0][1:])] = {
            i + j * 1j
            for i, j in itertools.product(range(x, x + w), range(y, y + h))
        }

    return claims


if __name__ == "__main__":
    main()
