"""Day 7: The Sum of Its Parts"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict


def main():
    """Solve day 7 puzzles."""
    with open("data/day_7.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file)

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    requirements = load_requirements(puzzle_input)
    available_steps = find_start(requirements)
    order = []

    while requirements:
        new_steps = [
            step
            for step, requirement in requirements.items()
            if requirement <= set(order)
        ]

        for step in new_steps:
            del requirements[step]

        available_steps = sorted(available_steps + new_steps)

        step = available_steps.pop(0)
        order.append(step)

    return "".join(order)


def star_2(puzzle_input):
    """Solve second puzzle."""
    requirements = load_requirements(puzzle_input)
    available_steps = find_start(requirements)
    order = []
    workers = 5 * [None]
    time = -1

    while requirements or workers != 5 * [None]:
        time += 1

        for i, worker in enumerate(workers):
            if worker:
                workers[i][1] -= 1

                if worker[1] == 0:
                    order.append(worker[0])
                    workers[i] = None

        new_steps = [
            step
            for step, requirement in requirements.items()
            if requirement <= set(order)
        ]

        for step in new_steps:
            del requirements[step]

        available_steps = sorted(available_steps + new_steps)

        for i, worker in enumerate(workers):
            if not worker and available_steps:
                step = available_steps.pop(0)
                workers[i] = [step, ord(step) - 4]

    return time


def find_start(requirements):
    """Find the starting steps."""
    start = set()

    for steps in requirements.values():
        for step in steps:
            if step not in requirements:
                start.add(step)

    return list(sorted(start))


def load_requirements(puzzle_input):
    """Load requirements from input."""
    requirements = defaultdict(set)

    for line in puzzle_input:
        chunks = line.split()
        requirements[chunks[-3]].add(chunks[1])

    return dict(sorted(requirements.items()))


if __name__ == "__main__":
    main()
