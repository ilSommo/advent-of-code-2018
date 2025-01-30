"""Day 12: Subterranean Sustainability"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

GENERATIONS = 50000000000


def main():
    """Solve day 12 puzzles."""
    with open("data/day_12.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    pots, rules = load_pots_rules(puzzle_input)

    for _ in range(20):
        pots = spread(pots, rules)

    return sum(pots)


def star_2(puzzle_input):
    """Solve second puzzle."""
    pots, rules = load_pots_rules(puzzle_input)

    offset = min(pots)
    pots = {pot - offset for pot in pots}
    states = [(pots, offset)]

    for _ in range(GENERATIONS):
        pots = spread(states[-1][0], rules)
        offset = min(pots)
        pots = {pot - offset for pot in pots}

        if (pots, offset) in states:
            break

        states.append((pots, offset))

    i = states.index((pots, offset))
    base_offset = sum(state[1] for state in states[:i])
    states = states[i:]
    generations = GENERATIONS - i
    len_cycle = len(states)

    pots = states[generations % len_cycle][0]
    offset = (
        base_offset
        + sum(state[1] for state in states) * generations // len_cycle
        + states[generations % len_cycle][1]
    )

    return sum(pots) + offset * len(pots)


def apply(condition, pots, i):
    """Check if condition applies to pot."""
    for j in range(-2, 3):
        if (j in condition) != (i + j in pots):
            return False

    return True


def load_pots_rules(puzzle_input):
    """Load initial pots and rules from input."""
    pots = {
        i for i, pot in enumerate(puzzle_input[0].split()[-1]) if pot == "#"
    }

    rules = {}

    for line in puzzle_input[2:]:
        condition, result = line.split(" => ")
        rules[
            tuple(i - 2 for i, pot in enumerate(condition) if pot == "#")
        ] = (1 if result == "#" else 0)

    return pots, rules


def spread(pots, rules):
    """Perform a spread round on pots."""
    new_pots = pots.copy()

    for i in range(min(pots) - 2, max(pots) + 3):
        for condition, result in rules.items():
            if apply(condition, pots, i):
                if result == 1:
                    new_pots.add(i)
                elif result == 0:
                    new_pots.discard(i)
                break

    return new_pots


if __name__ == "__main__":
    main()
