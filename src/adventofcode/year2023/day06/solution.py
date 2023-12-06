import sys
import math

from functools import reduce

from adventofcode.utils import utils


def part1(puzzle_input: list[str]) -> None:
    time = puzzle_input[0].split(':')[1].strip().split()
    distance = puzzle_input[1].split(':')[1].strip().split()

    time_distances = ([(int(time[i]), int(distance[i]))
                       for i in range(0, len(time))])

    c_t = []
    for time_distance in time_distances:
        c = 0
        for i in range(1, time_distance[0] + 1):
            if time_distance[0] * i - i * i > time_distance[1]:
                c += 1

        c_t.append(c)

    print(reduce(lambda acc, x: acc * x, c_t, 1))


def part2(puzzle_input: list[str]) -> None:
    time = int(''.join(puzzle_input[0].split(':')[1].strip().split()))
    distance = int(''.join(puzzle_input[1].split(':')[1].strip().split()))

    end1 = math.ceil((time - math.sqrt(time**2 - 4 * distance))/2)
    end2 = math.ceil((time + math.sqrt(time**2 - 4 * distance))/2)

    print(abs(end1-end2))


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])

    part1(puzzle_input)
    part2(puzzle_input)


if __name__ == '__main__':
    main(sys.argv)
