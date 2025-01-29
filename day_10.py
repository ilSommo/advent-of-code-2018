"""Day 10: The Stars Align"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import re
from dataclasses import dataclass


@dataclass
class Point:
    """Position and velocity of a point."""

    position: complex
    velocity: complex


def main():
    """Solve day 10 puzzles."""
    with open("data/day_10.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    star_1(puzzle_input)
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    points = load_points(puzzle_input)

    while is_message(points) is False:
        points = [
            Point(point.position + point.velocity, point.velocity)
            for point in points
        ]

    print_points(points)


def star_2(puzzle_input):
    """Solve second puzzle."""
    points = load_points(puzzle_input)
    i = 0

    while is_message(points) is False:
        i += 1
        points = [
            Point(point.position + point.velocity, point.velocity)
            for point in points
        ]

    return i


def compute_borders(positions):
    """Compute the borders of the points."""
    min_x = int(min(position.real for position in positions))
    max_x = int(max(position.real for position in positions))
    min_y = int(min(position.imag for position in positions))
    max_y = int(max(position.imag for position in positions))

    return min_x, max_x, min_y, max_y


def is_message(points):
    """Check if points compose a message."""
    positions = [point.position for point in points]
    _, _, min_y, max_y = compute_borders(positions)

    return max_y - min_y <= 10


def load_points(puzzle_input):
    """Load points from input."""
    points = []

    for line in puzzle_input:
        data = re.findall(r"(?<=<)[^>]*(?=>)", line)
        p = tuple(map(int, data[0].split(",")))
        v = tuple(map(int, data[1].split(",")))
        points.append(Point(p[0] + p[1] * 1j, v[0] + v[1] * 1j))

    return points


def print_points(points):
    """Print points."""
    positions = [point.position for point in points]
    min_x, max_x, min_y, max_y = compute_borders(positions)

    for j in range(min_y, max_y + 1):
        print(
            "".join(
                "#" if i + j * 1j in positions else "."
                for i in range(min_x, max_x + 1)
            )
        )


if __name__ == "__main__":
    main()
