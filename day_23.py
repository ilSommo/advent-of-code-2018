"""Day 23: Experimental Emergency Teleportation"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from dataclasses import dataclass

from z3 import If, Int, Optimize, Sum


@dataclass
class Nanobot:
    """Nanobot with coordinates and range."""

    x: int
    y: int
    z: int
    r: int


def main():
    """Solve day 23 puzzles."""
    with open("data/day_23.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    nanobots = load_nanobots(puzzle_input)
    strongest = max(nanobots, key=lambda nanobot: nanobot.r)

    return sum(
        compute_distance(strongest, nanobot) <= strongest.r
        for nanobot in nanobots
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    nanobots = load_nanobots(puzzle_input)

    opt = Optimize()
    x, y, z = Int("x"), Int("y"), Int("z")
    in_range = []

    for i, nanobot in enumerate(nanobots):
        d = Int(f"d_{i}")
        opt.add(
            d
            == z3_abs(x - nanobot.x)
            + z3_abs(y - nanobot.y)
            + z3_abs(z - nanobot.z),
        )
        in_range.append(If(d <= nanobot.r, 1, 0))

    count = Int("count")
    opt.add(count == Sum(in_range))
    opt.maximize(count)

    dist = Int("dist")
    opt.add(dist == z3_abs(x) + z3_abs(y) + z3_abs(z))
    opt.minimize(dist)

    opt.check()

    return opt.model()[dist].as_long()


def compute_distance(nanobot_0, nanobot_1):
    """Compute distance between two nanobots."""
    return (
        abs(nanobot_1.x - nanobot_0.x)
        + abs(nanobot_1.y - nanobot_0.y)
        + abs(nanobot_1.z - nanobot_0.z)
    )


def load_nanobots(puzzle_input):
    """Load nanobots from puzzle_input."""
    nanobots = []

    for line in puzzle_input:
        chunks = line.split()
        x, y, z = map(int, chunks[0][5:-2].split(","))
        r = int(chunks[1][2:])
        nanobots.append(Nanobot(x, y, z, r))

    return tuple(nanobots)


def z3_abs(value):
    """Calculate the z3 absolute value."""
    return If(value >= 0, value, -value)


if __name__ == "__main__":
    main()
