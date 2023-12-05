import sys
from functools import reduce

from adventofcode.utils import utils


def part1(puzzle_input: list[str]) -> None:
    total = 0
    for line in puzzle_input:
        numbers = line.split(":")[1].strip()
        winning_numbers, player_numbers = tuple(n.strip().split() for n in
                                                numbers.split('|'))
        matched_numbers = [number for number in winning_numbers
                           if number in player_numbers]

        points = (2 ** (len(matched_numbers) - 1)
                  if len(matched_numbers) > 0 else 0)
        total += points
    print(total)


def part2(puzzle_input: list[str]) -> None:
    num_of_copies = [1] * len(puzzle_input)
    for idx, line in enumerate(puzzle_input):
        numbers = line.split(":")[1].strip()
        winning_numbers, player_numbers = tuple(n.strip().split() for n in
                                                numbers.split('|'))

        matched_numbers_count = len([number for number in winning_numbers
                                     if number in player_numbers])

        num_of_copies = [copies + 1 * num_of_copies[idx]
                         if i in range(idx + 1,
                                       idx + matched_numbers_count + 1)
                         else copies for i, copies in enumerate(num_of_copies)]

    print(reduce(lambda acc, x: acc + x, num_of_copies))


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])

    part1(puzzle_input)
    part2(puzzle_input)


if __name__ == '__main__':
    main(sys.argv)
