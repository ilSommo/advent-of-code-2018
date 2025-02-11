"""Day 24: Immune System Simulator 20XX"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import re
from dataclasses import dataclass

ENEMIES = {"immune_system": "infection", "infection": "immune_system"}


@dataclass
class Attack:
    """Attack damage and type."""

    damage: int
    type_: str


@dataclass
class Group:
    """Group of units."""

    army: str
    units: int
    hit_points: int
    attack: Attack
    initiative: int
    weaknesses: set[str]
    immunities: set[str]

    @property
    def effective_power(self):
        """Effective power getter."""
        return self.units * self.attack.damage


def main():
    """Solve day 24 puzzles."""
    with open("data/day_24.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    groups = fight(load_groups(puzzle_input))

    return sum(group.units for group in groups.values())


def star_2(puzzle_input):
    """Solve second puzzle."""
    groups = {}
    boost = 0

    while {group.army for group in groups.values()} != {"immune_system"}:
        boost += 1
        groups = fight(load_groups(puzzle_input), boost)

    return sum(group.units for group in groups.values())


def attack_round(groups, targets):
    """Perform an attack round."""
    killed = set()

    for i, j in sorted(
        targets.items(), key=lambda i: groups[i[0]].initiative, reverse=True
    ):
        if i not in killed:
            groups[j].units -= (
                compute_damage(groups[i], groups[j]) // groups[j].hit_points
            )

            if groups[j].units <= 0:
                killed.add(j)

    for i in killed:
        del groups[i]

    return groups


def compute_damage(group, target):
    """Compute potential damage of a group to a target."""
    if group.attack.type_ in target.immunities:
        return 0

    if group.attack.type_ in target.weaknesses:
        return 2 * group.effective_power

    return group.effective_power


def fight(groups, boost=0):
    """Perform a whole fight."""
    for group in groups.values():
        if group.army == "immune_system":
            group.attack.damage += boost

    total = sum(group.units for group in groups.values())

    while len({group.army for group in groups.values()}) == 2:
        groups = attack_round(groups, select_targets(groups))

        if total == sum(group.units for group in groups.values()):
            break

        total = sum(group.units for group in groups.values())

    return groups


def load_group(army, line):
    """Load a group."""
    if "(" not in line:
        line = line.replace("points", "points ()")

    parts = re.split(r" \(|\) ", line)

    units = int(parts[0].split()[0])
    hit_points = int(parts[0].split()[4])

    weaknesses = set()
    immunities = set()

    for section in parts[1].split("; "):
        chunks = section.replace(",", "").split()

        if chunks and chunks[0] == "weak":
            weaknesses = set(chunks[2:])
        elif chunks:
            immunities = set(chunks[2:])

    attack_damage = int(parts[2].split()[5])
    attack_type = parts[2].split()[6]
    initiative = int(parts[2].split()[-1])

    return Group(
        army,
        units,
        hit_points,
        Attack(attack_damage, attack_type),
        initiative,
        weaknesses,
        immunities,
    )


def load_groups(puzzle_input):
    """Load groups from input."""
    i = 1
    groups = []

    while puzzle_input[i]:
        groups.append(load_group("immune_system", puzzle_input[i]))
        i += 1

    groups.extend(
        [load_group("infection", line) for line in puzzle_input[i + 2 :]]
    )

    return dict(enumerate(groups))


def select_target(group, targets):
    """Select target for group."""
    if not targets:
        return None

    damages = {
        i: compute_damage(group, target) for i, target in targets.items()
    }

    target, max_damage = max(
        damages.items(),
        key=lambda damage: (
            damage[1],
            targets[damage[0]].effective_power,
            targets[damage[0]].initiative,
        ),
    )

    return target if max_damage else None


def select_targets(groups):
    """Select all targets for all groups."""
    targets = {}
    available = {"immune_system": {}, "infection": {}}

    for i, group in groups.items():
        available[group.army][i] = group

    for i, group in sorted(
        groups.items(),
        key=lambda group: (group[1].effective_power, group[1].initiative),
        reverse=True,
    ):
        j = select_target(group, available[ENEMIES[group.army]])

        if j is not None:
            targets[i] = j
            del available[ENEMIES[group.army]][j]

    return targets


if __name__ == "__main__":
    main()
