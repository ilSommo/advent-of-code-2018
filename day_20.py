"""Day 20: A Regular Map"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict, deque

DIRECTIONS = {"N": 1j, "S": -1j, "E": 1, "W": -1}


def main():
    """Solve day 20 puzzles."""
    with open("data/day_20.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    paths = load_paths(puzzle_input)
    rooms = explore(paths, defaultdict(set), 0 + 0j)
    distances = compute_distances(rooms)

    return max(distances.values())


def star_2(puzzle_input):
    """Solve second puzzle."""
    paths = load_paths(puzzle_input)
    rooms = explore(paths, defaultdict(set), 0 + 0j)
    distances = compute_distances(rooms)

    return sum(distance >= 1000 for distance in distances.values())


def compute_distances(rooms):
    """Compute all distances from origin."""
    distances = {}
    open_rooms = deque([(0 + 0j, 0)])

    while open_rooms:
        room, steps = open_rooms.popleft()

        if steps < distances.get(room, float("inf")):
            distances[room] = steps
            open_rooms.extend(
                [(neighbor, steps + 1) for neighbor in rooms[room]]
            )

    return distances


def explore(paths, rooms, location):
    """Explore paths."""
    while paths:
        step = paths.pop(0)

        if isinstance(step, list):
            rooms = explore(step, rooms, location)

        else:
            rooms[location].add(location + step)
            rooms[location + step].add(location)
            location += step

    return rooms


def load_path(regex):
    """Load branch path."""
    path = []
    current_path = []

    while regex:
        char = regex.pop(0)

        match char:
            case "(":
                regex, new_paths = load_path(regex)
                current_path.append(new_paths)

            case "|":
                if current_path:
                    path.append(current_path)
                    current_path = []

            case ")":
                if current_path:
                    path.append(current_path)

                return regex, path

            case _:
                current_path.append(DIRECTIONS[char])

    if path:
        path.append(current_path)
    else:
        path = current_path

    return regex, path


def load_paths(puzzle_input):
    """Load paths from input."""
    regex = list(puzzle_input[1:-1])
    _, paths = load_path(regex)

    return paths


if __name__ == "__main__":
    main()
