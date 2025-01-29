"""Day 9: Marble Mania"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict, deque


def main():
    """Solve day 9 puzzles."""
    with open("data/day_9.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    players, n_marbles = load_players_marbles(puzzle_input)

    return compute_max_score(players, n_marbles)


def star_2(puzzle_input):
    """Solve second puzzle."""
    players, n_marbles = load_players_marbles(puzzle_input)

    return compute_max_score(players, 100 * n_marbles)


def compute_max_score(players, n_marbles):
    """Compute maximum score of given configuration."""
    marbles = deque([0])
    scores = defaultdict(int)

    for i in range(1, n_marbles + 1):
        if i % 23 == 0:
            marbles.rotate(7)
            scores[i % players] += i + marbles.popleft()

        else:
            marbles.rotate(-2)
            marbles.appendleft(i)

    return max(scores.values())


def load_players_marbles(puzzle_input):
    """Load players and marbles numbers from input."""
    chunks = puzzle_input.split()

    return int(chunks[0]), int(chunks[-2])


if __name__ == "__main__":
    main()
