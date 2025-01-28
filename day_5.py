"""Day 5: Alchemical Reduction"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import string


def main():
    """Solve day 5 puzzles."""
    with open("data/day_5.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return len(react(puzzle_input))


def star_2(puzzle_input):
    """Solve second puzzle."""
    return min(
        len(react(puzzle_input.replace(unit, "").replace(unit.upper(), "")))
        for unit in string.ascii_lowercase
    )


def are_reactive(unit_0, unit_1):
    """Check if two units are reactive."""
    return unit_0.lower() == unit_1.lower() and (
        (unit_0.isupper() and unit_1.islower())
        or (unit_0.islower() and unit_1.isupper())
    )


def react(polymer):
    """Make polymer react."""
    reacted = []

    for unit in polymer:
        if reacted and are_reactive(unit, reacted[-1]):
            reacted.pop()
        else:
            reacted.append(unit)

    return reacted


if __name__ == "__main__":
    main()
