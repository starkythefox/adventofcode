import sys
from functools import reduce

from adventofcode.utils import utils


def difference_and_predict(differences: list[int]) -> int:
    if all(x == 0 for x in differences):
        return 0

    next_differences = ([differences[i + 1] - differences[i]
                         for i in range(0, len(differences) - 1)])

    predicted = difference_and_predict(next_differences)

    return differences[-1] + predicted


def difference_and_extrapolate(differences: list[int]) -> int:
    if all(x == 0 for x in differences):
        return 0

    next_differences = ([differences[i + 1] - differences[i]
                         for i in range(0, len(differences) - 1)])

    extrapolated = difference_and_extrapolate(next_differences)

    return differences[0] - extrapolated


def part1(puzzle_input: list[str]) -> int:
    prediced_history = []
    for line in puzzle_input:
        history = [int(value) for value in line.split()]

        prediced_history.append((difference_and_predict(history)))

    total = reduce(lambda acc, x: acc + x, prediced_history)
    return total


def part2(puzzle_input: list[str]) -> int:
    prediced_history = []
    for line in puzzle_input:
        history = [int(value) for value in line.split()]

        prediced_history.append((difference_and_extrapolate(history)))

    total = reduce(lambda acc, x: acc + x, prediced_history)
    return total


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])
    print(part1(puzzle_input))
    print(part2(puzzle_input))


if __name__ == '__main__':
    main(sys.argv)
