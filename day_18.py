"""Day 18: Settlers of The North Pole"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from functools import cache


def main():
    """Solve day 18 puzzles."""
    with open("data/day_18.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    grounds, trees, lumberyards = load_map(puzzle_input)

    for _ in range(10):
        grounds, trees, lumberyards = step(grounds, trees, lumberyards)

    return len(trees) * len(lumberyards)


def star_2(puzzle_input):
    """Solve second puzzle."""
    grounds, trees, lumberyards = load_map(puzzle_input)
    visited = [(grounds, trees, lumberyards)]
    minutes = 1000000000

    for _ in range(minutes):
        grounds, trees, lumberyards = step(grounds, trees, lumberyards)
        state = (grounds, trees, lumberyards)

        if state in visited:
            break

        visited.append(state)

    start = visited.index(state)
    visited = visited[start:]
    len_cycle = len(visited)

    grounds, trees, lumberyards = visited[(minutes - start) % len_cycle]

    return len(trees) * len(lumberyards)


@cache
def get_neighbors(location):
    """Get all neighbors to a location."""
    return frozenset(
        location + i + j * 1j
        for i, j in itertools.product(range(-1, 2), repeat=2)
        if i + j * 1j != 0
    )


def load_map(puzzle_input):
    """Load map from input."""
    grounds = set()
    trees = set()
    lumberyards = set()

    for i, line in enumerate(puzzle_input):
        for j, char in enumerate(line):
            match char:
                case ".":
                    grounds.add(i + j * 1j)
                case "|":
                    trees.add(i + j * 1j)
                case "#":
                    lumberyards.add(i + j * 1j)

    return tuple(map(frozenset, (grounds, trees, lumberyards)))


def step(grounds, trees, lumberyards):
    """Advance one step."""
    new_grounds = set()
    new_trees = set()
    new_lumberyards = set()

    for ground in grounds:
        if sum(neighbor in trees for neighbor in get_neighbors(ground)) >= 3:
            new_trees.add(ground)
        else:
            new_grounds.add(ground)

    for tree in trees:
        if (
            sum(neighbor in lumberyards for neighbor in get_neighbors(tree))
            >= 3
        ):
            new_lumberyards.add(tree)
        else:
            new_trees.add(tree)

    for lumberyard in lumberyards:
        if (
            sum(
                neighbor in lumberyards
                for neighbor in get_neighbors(lumberyard)
            )
            >= 1
            and sum(
                neighbor in trees for neighbor in get_neighbors(lumberyard)
            )
            >= 1
        ):
            new_lumberyards.add(lumberyard)
        else:
            new_grounds.add(lumberyard)

    return tuple(map(frozenset, (new_grounds, new_trees, new_lumberyards)))


if __name__ == "__main__":
    main()
