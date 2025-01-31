"""Day 13: Mine Cart Madness"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from dataclasses import dataclass

TURN_ORDER = {1j: 1, 1: -1j, -1j: 1j}


@dataclass
class Cart:
    """Cart."""

    position: complex
    direction: complex
    turn: complex = 1j


def main():
    """Solve day 13 puzzles."""
    with open("data/day_13.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    carts, tracks = load_map(puzzle_input)
    crashed = []

    while not crashed:
        carts, crashed = move_carts(carts, tracks, crashed)

    y, x = map(int, (crashed[0].position.real, crashed[0].position.imag))

    return f"{x},{y}"


def star_2(puzzle_input):
    """Solve second puzzle."""
    carts, tracks = load_map(puzzle_input)
    crashed = []

    while len(carts) > 1:
        carts, crashed = move_carts(carts, tracks, crashed)

    y, x = map(int, (carts[0].position.real, carts[0].position.imag))

    return f"{x},{y}"


def load_map(puzzle_input):
    """Load map from input."""
    carts = []
    tracks = {}

    for i, line in enumerate(puzzle_input):
        for j, char in enumerate(line):
            coordinates = i + j * 1j

            if char == "^":
                carts.append(Cart(coordinates, -1))
                tracks[coordinates] = "|"
            elif char == "v":
                carts.append(Cart(coordinates, 1))
                tracks[coordinates] = "|"
            elif char == "<":
                carts.append(Cart(coordinates, -1j))
                tracks[coordinates] = "-"
            elif char == ">":
                carts.append(Cart(coordinates, 1j))
                tracks[coordinates] = "-"
            elif char:
                tracks[coordinates] = char

    return carts, tracks


def move_cart(cart, tracks):
    """Move a single cart on tracks."""
    cart.position += cart.direction

    match tracks[cart.position]:
        case "/":
            cart.direction = -(cart.direction.imag + cart.direction.real * 1j)
        case "\\":
            cart.direction = cart.direction.imag + cart.direction.real * 1j
        case "+":
            cart.direction *= cart.turn
            cart.turn = TURN_ORDER[cart.turn]

    return cart


def move_carts(carts, tracks, crashed):
    """Move carts on tracks."""
    crash_indices = []

    for i, cart in enumerate(carts):
        carts[i] = move_cart(cart, tracks)

        for j, _ in enumerate(carts):
            if i != j and carts[i].position == carts[j].position:
                crash_indices.extend([i, j])

    crashed.extend([carts[i] for i in crash_indices])
    carts = [cart for i, cart in enumerate(carts) if i not in crash_indices]

    return carts, crashed


if __name__ == "__main__":
    main()
