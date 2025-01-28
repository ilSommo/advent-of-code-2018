"""Day 4: Repose Record"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict
from datetime import datetime


def main():
    """Solve day 4 puzzles."""
    with open("data/day_4.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    guards = load_guards(puzzle_input)

    guards_sleep = {
        guard: sum(
            (interval[1] - interval[0]).seconds for interval in intervals
        )
        for guard, intervals in guards.items()
    }
    guard = max(guards_sleep, key=guards_sleep.get)

    return guard * get_minute(guards[guard])[0]


def star_2(puzzle_input):
    """Solve second puzzle."""
    guards = load_guards(puzzle_input)

    guards_minutes = {
        guard: get_minute(intervals) for guard, intervals in guards.items()
    }
    guard, minute = max(guards_minutes.items(), key=lambda item: item[1])

    return guard * minute[0]


def get_minute(intervals):
    """Get the minute in which a guard slept the most."""
    minutes = defaultdict(int)

    for i in range(60 * 60):
        for start, end in intervals:
            if (
                60 * start.hour + start.minute
                <= i
                < 60 * end.hour + end.minute
            ):
                minutes[i] += 1

    return max(minutes.items(), key=lambda item: item[1])


def load_guards(puzzle_input):
    """Load guards from input."""
    entries = sort_entries(puzzle_input)

    guards = defaultdict(list)
    guard = None
    start = None
    end = None

    for timestamp, action in entries.items():
        if "Guard" in action:
            guard = int(action.split()[1][1:])

        elif "asleep" in action:
            start = timestamp

        else:
            end = timestamp
            guards[guard].append((start, end))

    return guards


def parse_datetime(string):
    """Convert string into datetime."""
    date, time = string.split()
    year, month, day = map(int, date.split("-"))
    hour, minute = map(int, time.split(":"))

    return datetime(year, month, day, hour, minute)


def sort_entries(puzzle_input):
    """Sort input entries chronologically."""
    entries = {}

    for line in puzzle_input:
        timestamp = parse_datetime(line[1:].split("]")[0])
        entries[timestamp] = line.split("] ")[1]

    return dict(sorted(entries.items()))


if __name__ == "__main__":
    main()
