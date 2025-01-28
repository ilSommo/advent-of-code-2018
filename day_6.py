"""Day 6: Chronal Coordinates"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from collections import defaultdict


def main():
    """Solve day 6 puzzles."""
    with open("data/day_6.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file)

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    coordinates = load_coordinates(puzzle_input)
    min_x, max_x, min_y, max_y = get_borders(coordinates)
    areas = defaultdict(int)

    for x, y in itertools.product(
        range(min_x, max_x + 1),
        range(min_y, max_y + 1),
    ):
        index = get_index(x, y, coordinates)
        areas[index] += 1

    for i, coordinate in enumerate(coordinates):
        if coordinate[0] in (min_x, max_x) or coordinate[1] in (min_y, max_y):
            del areas[i]

    return max(areas.values())


def star_2(puzzle_input):
    """Solve second puzzle."""
    coordinates = load_coordinates(puzzle_input)
    min_x, max_x, min_y, max_y = get_borders(coordinates)

    return sum(
        get_total_distance(x, y, coordinates) < 10000
        for x, y, in itertools.product(
            range(min_x, max_x + 1), range(min_y, max_y + 1)
        )
    )


def get_borders(coordinates):
    """Get borders of the map."""
    min_x = min(coordinates, key=lambda coordinate: coordinate[0])[0]
    max_x = max(coordinates, key=lambda coordinate: coordinate[0])[0]
    min_y = min(coordinates, key=lambda coordinate: coordinate[1])[1]
    max_y = max(coordinates, key=lambda coordinate: coordinate[1])[1]

    return min_x, max_x, min_y, max_y


def get_index(x, y, coordinates):
    """Get index of closest coordinate."""
    closest = None
    min_distance = float("inf")

    for i, coordinate in enumerate(coordinates):
        distance = abs(coordinate[0] - x) + abs(coordinate[1] - y)

        if distance == min_distance:
            closest = None
        elif distance < min_distance:
            closest = i
            min_distance = distance

    return closest


def get_total_distance(x, y, coordinates):
    """Get total distance to all coordinates."""
    return sum(
        abs(coordinate[0] - x) + abs(coordinate[1] - y)
        for coordinate in coordinates
    )


def load_coordinates(puzzle_input):
    """Load coordinates from input."""
    coordinates = []

    for line in puzzle_input:
        x, y = map(int, line.split(","))
        coordinates.append((x, y))

    return tuple(coordinates)


if __name__ == "__main__":
    main()
