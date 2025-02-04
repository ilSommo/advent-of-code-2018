"""Day 17: Reservoir Research"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import deque
from functools import cache


def main():
    """Solve day 17 puzzles."""
    with open("data/day_17.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    clay = load_clay(puzzle_input)
    spring = 500j
    water, _ = spread_water(spring, clay)

    return len(water)


def star_2(puzzle_input):
    """Solve second puzzle."""
    clay = load_clay(puzzle_input)
    spring = 500j
    _, wet = spread_water(spring, clay)

    return len(wet)


def fill(tail, clay):
    """Fill a row."""
    tails = []

    i, tails = fill_direction(tail, clay, tails, -1)
    j, tails = fill_direction(tail, clay, tails, 1)

    return set(tail + k * 1j for k in range(i, j + 1)), tails


def fill_direction(tail, clay, tails, direction):
    """Fill in the given direction."""
    i = 0

    while True:
        new = tail + direction * i * 1j

        if new + 1 not in clay:
            tails.append(new)
            break

        if new + direction * 1j in clay:
            break

        i += 1

    return i * direction, tails


def load_clay(puzzle_input):
    """Load clay coordinates from input."""
    clay = set()

    for line in puzzle_input:
        chunks = line.split(", ")
        a, b = map(int, chunks[1][2:].split(".."))
        c = int(chunks[0][2:])

        if chunks[0][0] == "x":
            clay.update({i + c * 1j for i in range(a, b + 1)})
        else:
            clay.update({c + j * 1j for j in range(a, b + 1)})

    return frozenset(clay)


@cache
def spread_water(spring, clay):
    """Spread water from spring."""
    clay = set(clay)
    streams = deque([[spring]])
    water = {spring}

    min_y = int(min(clay, key=lambda point: point.real).real)
    max_y = int(max(clay, key=lambda point: point.real).real)

    while streams:
        stream = streams.pop()
        tail = stream[-1]
        down = tail + 1

        if down.real > max_y or (down in water - clay):
            continue

        if down not in clay:
            water.add(down)
            streams.append(stream + [down])
            continue

        flow, tails = fill(tail, clay)
        water.update(flow)

        if tails:
            streams.extend([stream + [new_tail] for new_tail in tails])

        else:
            clay.update(flow)
            streams.append(stream[:-1])

    water = {elem for elem in water if min_y <= elem.real <= max_y}

    return water, water & clay


if __name__ == "__main__":
    main()
