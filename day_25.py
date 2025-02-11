"""Day 25: Four-Dimensional Adventure"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """4-dimensional point."""

    x: int
    y: int
    z: int
    w: int


def main():
    """Solve day 25 puzzles."""
    with open("data/day_25.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    points = load_points(puzzle_input)
    constellations = []

    while points:
        point = points.pop()
        constellations = add_point(constellations, point)

    return len(constellations)


def add_point(constellations, point):
    """Add point to constellations."""
    to_merge = []

    for i, constellation in enumerate(constellations):
        for constellation_point in constellation:
            if compute_distance(point, constellation_point) <= 3:
                to_merge.append(i)
                break

    new_constellation = {point}

    for i in reversed(to_merge):
        new_constellation.update(constellations[i])
        del constellations[i]

    return constellations + [new_constellation]


def compute_distance(point_0, point_1):
    """Compute distance between points."""
    return (
        abs(point_0.x - point_1.x)
        + abs(point_0.y - point_1.y)
        + abs(point_0.z - point_1.z)
        + abs(point_0.w - point_1.w)
    )


def load_points(puzzle_input):
    """Load points from input."""
    points = set()

    for line in puzzle_input:
        x, y, z, w = map(int, line.split(","))
        points.add(Point(x, y, z, w))

    return points


if __name__ == "__main__":
    main()
