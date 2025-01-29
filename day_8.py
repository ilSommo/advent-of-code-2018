"""Day 8: Memory Maneuver"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 8 puzzles."""
    with open("data/day_8.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return sum_metadata(load_tree(puzzle_input))


def star_2(puzzle_input):
    """Solve second puzzle."""
    return compute_value(load_tree(puzzle_input))


def compute_value(node):
    """Recursively compute the value of a node."""
    if not node[0]:
        return sum(node[1])

    return sum(
        compute_value(node[0][i - 1]) for i in node[1] if i - 1 < len(node[0])
    )


def load_node(chunks):
    """Load node from list of numbers."""
    n_metadata = chunks[1]
    index = 2
    children = []

    for _ in range(chunks[0]):
        child, offset = load_node(chunks[index:])
        children.append(child)
        index += offset

    metadata = tuple(chunks[index : index + n_metadata])

    return (tuple(children), metadata), index + n_metadata


def load_tree(puzzle_input):
    """Load tree from input."""
    return load_node(tuple(map(int, puzzle_input.split())))[0]


def sum_metadata(node):
    """Recursively sum metadata of node and children."""
    return sum(node[1]) + sum(sum_metadata(child) for child in node[0])


if __name__ == "__main__":
    main()
