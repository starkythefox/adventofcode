# 19:04
import sys
from src.adventofcode.utils import utils
import itertools
from functools import reduce


def parse_records(puzzle_input: list[str]) -> list[tuple[str, str]]:
    return [(row.split(' ')) for row in puzzle_input]


def find_arrangements(springs_status: str, str_idx: int,
                      groups: list[int], grp_idx: int) -> set[str]:
    group = groups[grp_idx]

    arrangements = set()
    for i in range(str_idx,
                   len(springs_status) - reduce(lambda acc, x: acc + x,
                                                groups[grp_idx+1:], 0)):

        substr = springs_status[i:group+i]
        if '.' in substr:
            continue

        aux = (springs_status[:i].replace('?', '.')
               + substr.replace('?', '#')
               + springs_status[group+i:])

        aux2 = aux.replace('?', '.')

        if aux2 in arrangements:
            continue

        damaged = [len(list(repeats))
                   for status, repeats in itertools.groupby(aux2)
                   if status == '#']

        if groups == damaged:
            arrangements.add(aux2)
            continue

        if grp_idx >= len(damaged):
            continue

        if grp_idx + 1 < len(groups) and groups[grp_idx] == damaged[grp_idx]:
            arrangements.update(find_arrangements(aux, i + group, groups,
                                                  grp_idx + 1))

    return arrangements


def calculate_arragements(springs_status: str, spring_groups: str) -> int:
    groups = [int(num) for num in spring_groups.split(',')]

    arrangements = find_arrangements(springs_status, 0, groups, 0)

    return len(arrangements)


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
