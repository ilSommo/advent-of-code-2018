"""Day 14: Chocolate Charts"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from functools import cache


def main():
    """Solve day 14 puzzles."""
    with open("data/day_14.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    number = int(puzzle_input)
    recipes = "37"
    elf_0 = 0
    elf_1 = 1

    while len(recipes) < number + 10:
        recipes += create_recipe(recipes[elf_0], recipes[elf_1])
        elf_0 = (elf_0 + 1 + int(recipes[elf_0])) % len(recipes)
        elf_1 = (elf_1 + 1 + int(recipes[elf_1])) % len(recipes)

    return recipes[number : number + 10]


def star_2(puzzle_input):
    """Solve second puzzle."""
    recipes = "37"
    elf_0 = 0
    elf_1 = 1

    while puzzle_input not in recipes[-len(puzzle_input) - 1 :]:
        recipes += create_recipe(recipes[elf_0], recipes[elf_1])
        elf_0 = (elf_0 + 1 + int(recipes[elf_0])) % len(recipes)
        elf_1 = (elf_1 + 1 + int(recipes[elf_1])) % len(recipes)

    return recipes.index(puzzle_input)


@cache
def create_recipe(recipe_0, recipe_1):
    return str(int(recipe_0) + int(recipe_1))


if __name__ == "__main__":
    main()
