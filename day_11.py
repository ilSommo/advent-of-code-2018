"""Day 11: Chronal Charge"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools


def main():
    """Solve day 11 puzzles."""
    with open("data/day_11.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    table = generate_summed_area_table(int(puzzle_input))
    squares = {
        f"{i},{j}": compute_square_power(i + j * 1j, 3, table)
        for i, j in itertools.product(range(1, 299), repeat=2)
    }

    return max(squares, key=squares.get)


def star_2(puzzle_input):
    """Solve second puzzle."""
    table = generate_summed_area_table(int(puzzle_input))
    squares = {}

    for size in range(1, 301):
        size_squares = {
            f"{i},{j},{size}": compute_square_power(i + j * 1j, size, table)
            for i, j in itertools.product(range(1, 302 - size), repeat=2)
        }
        squares |= size_squares

        if max(size_squares.values()) < 0:
            break

    return max(squares, key=squares.get)


def compute_power_level(cell, serial_number):
    """Compute the power level of a cell."""
    return (
        int(((cell.real + 10) * cell.imag + serial_number) * (cell.real + 10))
        % 1000
        // 100
        - 5
    )


def compute_square_power(cell, size, table):
    """Compute the power of a square with given cell and size."""
    cell -= 1 + 1j

    return (
        table.get(cell, 0)
        + table[cell + size * (1 + 1j)]
        - table.get(cell + size, 0)
        - table.get(cell + size * 1j, 0)
    )


def compute_summed_area(cell, serial_number, table):
    """Compute the value of the summed-area table for a given cell."""
    return (
        compute_power_level(cell, serial_number)
        + table.get(cell - 1j, 0)
        + table.get(cell - 1, 0)
        - table.get(cell - 1 - 1j, 0)
    )


def generate_summed_area_table(serial_number):
    """Generate the summed-area table."""
    table = {}

    for size in range(1, 301):
        for k in range(1, size):
            table[size + k * 1j] = compute_summed_area(
                size + k * 1j, serial_number, table
            )
            table[k + size * 1j] = compute_summed_area(
                k + size * 1j, serial_number, table
            )

        table[size + size * 1j] = compute_summed_area(
            size + size * 1j, serial_number, table
        )

    return table


if __name__ == "__main__":
    main()
