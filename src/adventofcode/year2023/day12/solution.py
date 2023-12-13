# 19:04
import sys

from src.adventofcode.utils import utils
from itertools import groupby


cache: dict[tuple, int] = dict()


def parse_records(puzzle_input: list[str]) -> list[tuple[str, str]]:
    return [(row.split(' ')) for row in puzzle_input]


def create_next_string(s: str, i: int) -> str:
    first_char = (s[i] if len(s) > i else '')

    return (('.' if first_char == '?' else first_char)
            + s[i+1:])


def is_damaged_group(springs: str, group: int) -> bool:
    if (len(springs) >= group
            and '.' not in springs[:group]):

        k, g = next(groupby('#' * group + create_next_string(springs, group)))
        count = sum(1 for _ in g) if k == '#' else 0

        return count == group

    return False


def find_arrangements(springs: str, groups: list[int]) -> int:
    if ((len(springs) == 0 or all(c in ('?', '.') for c in springs))
            and len(groups) == 0):
        return 1

    if (len(springs) == 0 and len(groups) > 0 or
            len(springs) > 0 and '#' in springs and len(groups) == 0):
        return 0

    if springs[0] == '.':
        return find_arrangements(springs[1:], groups)

    if springs[0] == '?':
        return (find_arrangements(springs.replace('?', '#', 1), groups)
                + find_arrangements(springs.replace('?', '.', 1),
                                    groups))

    if (springs, tuple(groups)) in cache:
        return cache[(springs, tuple(groups))]

    if is_damaged_group(springs, groups[0]):
        res = find_arrangements(create_next_string(springs, groups[0]),
                                groups[1:])
        cache[(springs, tuple(groups))] = res
        return res

    return 0


def calculate_arragements(springs_status: str, spring_groups: str) -> int:
    groups = [int(num) for num in spring_groups.split(',')]

    arrangements = find_arrangements(springs_status, groups)

    return arrangements


def part1(puzzle_input: list[str]) -> int:
    condition_records = parse_records(puzzle_input)

    total_arragements = 0
    for record in condition_records:
        total_arragements += calculate_arragements(record[0], record[1])

    return total_arragements


def part2(puzzle_input: list[str]) -> int:
    return 0


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])

    print(part1(puzzle_input))
    print(part2(puzzle_input))


if __name__ == '__main__':
    main(sys.argv)
