"""Day 15: Beverage Bandits"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import copy
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cache


@dataclass
class Unit:
    """Unit."""

    race: str
    attack: int = 3
    points: int = 200


def main():
    """Solve day 15 puzzles."""
    with open("data/day_15.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    units, caverns = load_map(puzzle_input)
    over = False
    turn = -1

    while not over:
        turn += 1
        units, over = play_turn(units, caverns)

    return turn * sum(unit.points for unit in units.values())


def star_2(puzzle_input):
    """Solve second puzzle."""
    units, caverns = load_map(puzzle_input)
    new_units = {}

    while len(new_units) == 0:
        for unit in units.values():
            if unit.race == "E":
                unit.attack += 1

        new_units, turn = fight_battle(units, caverns)

    return turn * sum(unit.points for unit in new_units.values())


def attack(location, units):
    """Make unit attack."""
    enemies = get_enemies(location, units)

    if enemies:
        target = min(enemies, key=lambda enemy: units[enemy].points)
        units[target].points -= units[location].attack

        if units[target].points <= 0:
            del units[target]

    return units


def count_elves(units):
    """Count the number of elves."""
    return sum(1 for unit in units.values() if unit.race == "E")


def fight_battle(units, caverns):
    """Fight a whole battle."""
    elves = count_elves(units)
    units = copy.deepcopy(units)
    over = False
    turn = -1

    while not over:
        turn += 1
        units, over = play_turn(units, caverns)

        if count_elves(units) < elves:
            return {}, 0

    return units, turn


def get_enemies(location, units):
    """Get neighboring enemies."""
    return tuple(
        neighbor
        for neighbor in get_neighbors(location)
        if neighbor in units and units[neighbor].race != units[location].race
    )


@cache
def get_neighbors(location):
    """Get all neighbors to a location."""
    return tuple(location + direction for direction in (-1, -1j, 1j, 1))


@cache
def get_path(start, end, free):
    """Get shortest path from start to end."""
    paths = deque([[start]])
    visited = {start}

    while paths:
        path = paths.popleft()

        for neighbor in get_neighbors(path[-1]):
            if neighbor == end:
                return tuple(path[1:] + [neighbor])

            if neighbor in free and neighbor not in visited:
                visited.add(neighbor)
                paths.append(path + [neighbor])

    return tuple()


def load_map(puzzle_input):
    """Load map from input."""
    units = {}
    caverns = set()

    for i, line in enumerate(puzzle_input):
        for j, char in enumerate(line):
            if char in ("G", "E"):
                units[i + j * 1j] = Unit(char)

            if char != "#":
                caverns.add(i + j * 1j)

    return units, frozenset(caverns)


def move_unit(location, units, caverns):
    """Move a unit."""
    unit = units[location]

    in_range = set.union(
        *(
            set(get_neighbors(k)) & caverns
            for k, v in units.items()
            if v.race != unit.race
        )
    )

    paths = defaultdict(list)
    free = frozenset(caverns - set(units.keys()))

    for end in in_range & free:
        path = get_path(location, end, free)

        if path:
            paths[len(path)].append(path)

    if paths:
        del units[location]
        location = min(
            sorted(paths.items())[0][1],
            key=lambda path: (path[0].real, path[0].imag),
        )[0]
        units[location] = unit

    return location, units


def play_turn(units, caverns):
    """Play battle turn."""
    for location in sorted(
        units, key=lambda location: (location.real, location.imag)
    ):

        if len(set(unit.race for unit in units.values())) < 2:
            return units, True

        if location in units:
            units = play_unit_turn(location, units, caverns)

    return units, False


def play_unit_turn(location, units, caverns):
    """Play a single unit turn."""
    if not get_enemies(location, units):
        location, units = move_unit(location, units, caverns)

    units = attack(location, units)

    return units


if __name__ == "__main__":
    main()
