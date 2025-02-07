"""Day 22: Mode Maze"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import bisect
import itertools
from functools import cache

MODULO = 20183
TOOLS = {
    0: {"climbing_gear", "torch"},
    1: {"climbing_gear", "neither"},
    2: {"torch", "neither"},
}


def main():
    """Solve day 22 puzzles."""
    with open("data/day_22.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    depth, target = load_depth_target(puzzle_input)

    return sum(
        compute_type(i + j * 1j, depth, target)
        for i, j in itertools.product(
            range(int(target.real) + 1), range(int(target.imag) + 1)
        )
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    depth, target = load_depth_target(puzzle_input)
    time_floor, time_ceiling = compute_times(0 + 0j, target)

    best_paths = {}
    paths = [(0 + 0j, "torch", 0, time_floor, time_ceiling)]

    while paths:
        location, tool, time, floor, ceiling = paths.pop(0)

        if location == target and tool == "torch":
            return time

        if floor >= time_ceiling or floor >= best_paths.get(
            (location, tool), time_ceiling
        ):
            continue

        time_ceiling = min(time_ceiling, ceiling)
        best_paths[(location, tool)] = time
        time += 1

        for neighbor in get_neighbors(location):
            if tool in TOOLS[compute_type(neighbor, depth, target)]:
                neighbor_floor, neighbor_ceiling = compute_times(
                    neighbor, target
                )
                bisect.insort(
                    paths,
                    (
                        neighbor,
                        tool,
                        time,
                        time + neighbor_floor,
                        time + neighbor_ceiling,
                    ),
                    key=lambda path: path[3],
                )

        tool = tuple(TOOLS[compute_type(location, depth, target)] - {tool})[0]
        time += 6

        bisect.insort(
            paths,
            (location, tool, time, floor + 7, ceiling - 7),
            key=lambda path: path[3],
        )

    return 0


@cache
def compute_distance(location, target):
    """Compute distance between a regions."""
    distance = location - target

    return int(abs(distance.real) + abs(distance.imag))


@cache
def compute_erosion(region, depth, target):
    """Compute the erosion of a region."""
    if region in (0 + 0j, target):
        geologic_index = 0

    elif region.imag == 0:
        geologic_index = int(region.real) * 16807

    elif region.real == 0:
        geologic_index = int(region.imag) * 48271

    else:
        geologic_index = compute_erosion(
            region - 1, depth, target
        ) * compute_erosion(region - 1j, depth, target)

    return (geologic_index + depth) % MODULO


@cache
def compute_times(location, target):
    """Compute floor and ceiling times."""
    distance = compute_distance(location, target)

    return distance, 8 * distance + 7


@cache
def compute_type(region, depth, target):
    """Compute the type of a region."""
    return compute_erosion(region, depth, target) % 3


@cache
def get_neighbors(location):
    """Get neighbors of a location."""
    return frozenset(
        location + direction
        for direction in (1, 1j, -1, -1j)
        if (location + direction).real >= 0
        and (location + direction).imag >= 0
    )


def load_depth_target(puzzle_input):
    """Load depth and target from input."""
    depth = int(puzzle_input[0].split()[-1])
    x, y = map(int, puzzle_input[1].split()[-1].split(","))

    return depth, x + y * 1j


if __name__ == "__main__":
    main()
