import sys
from functools import reduce

from adventofcode.utils import utils

NOT_SYMBOLS = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def parse_lines_into_a_2d_list(puzzle_input: list[str]) -> list[list[str]]:
    engine_schematic = []
    for line in puzzle_input:
        engine_schematic.append(list(line))

    return engine_schematic


def lookup_left(engine_schematic: list[list[str]], seen: list[list[bool]],
                col: int, row: int) -> str:
    number = ''

    while col >= 0:
        curr = engine_schematic[row][col]
        if seen[row][col]:
            return number

        if not curr.isdecimal():
            seen[row][col] = True
            return number

        number = curr + number
        seen[row][col] = True
        col -= 1

    return number


def lookup_right(engine_schematic: list[list[str]], seen: list[list[bool]],
                 col: int, row: int) -> str:
    number = ''
    while col < len(engine_schematic[row]):
        curr = engine_schematic[row][col]
        if seen[row][col]:
            return number

        if not curr.isdecimal():
            seen[row][col] = True
            return number

        number += curr
        seen[row][col] = True
        col += 1

    return number


def construct_number(engine_schematic: list[list[str]], seen: list[list[bool]],
                     col: int, row: int) -> int | bool:
    if seen[row][col]:
        return False

    curr_char = engine_schematic[row][col]
    if not curr_char.isdecimal():
        seen[row][col] = True
        return False

    left_part = lookup_left(engine_schematic, seen, col-1, row)
    right_part = lookup_right(engine_schematic, seen, col+1, row)

    return int(left_part + curr_char
               + right_part)


def find_numbers_around_symbol(engine_schematic: list[list[str]],
                               seen: list[list[bool]],
                               symbol_pos: tuple[int, int]) -> list[int]:
    row = symbol_pos[1] - 1 if (symbol_pos[1] - 1 >= 0) else 0
    numbers = list()
    while row <= symbol_pos[1] + 1 and row < len(engine_schematic):
        col = symbol_pos[0] - 1 if (symbol_pos[0] - 1 >= 0) else 0
        while (col <= symbol_pos[0] + 1 and
               col < len(engine_schematic[row])):
            if (col, row) == symbol_pos:
                seen[row][col] = True
                col += 1
                continue

            number = construct_number(engine_schematic, seen, col, row)
            if not number:
                col += 1
                continue

            numbers.append(number)
            col += 1

        row += 1

    return numbers


def find_symbol_positions(engine_schematic: list[list[str]],
                          seen: list[list[bool]]) -> list[tuple[int, int]]:
    symbol_positions = list()
    for row_idx, row in enumerate(engine_schematic):
        for col_idx, col in enumerate(row):
            if seen[row_idx][col_idx]:
                continue

            if col not in NOT_SYMBOLS:
                symbol_positions.append((col_idx, row_idx))
            elif col == '.':
                seen[row_idx][col_idx] = True

    return symbol_positions


def find_gear_positions(engine_schematic: list[list[str]],
                        seen: list[list[bool]]) -> list[tuple[int, int]]:
    gear_positions = list()
    for row_idx, row in enumerate(engine_schematic):
        for col_idx, col in enumerate(row):
            if seen[row_idx][col_idx]:
                continue

            if col == '*':
                gear_positions.append((col_idx, row_idx))
            elif col == '.':
                seen[row_idx][col_idx] = True

    return gear_positions


def part1(puzzle_input: list[str]) -> None:
    engine_schematic = parse_lines_into_a_2d_list(puzzle_input)

    seen = [[False] * len(inner) for inner in engine_schematic]
    symbol_positions = find_symbol_positions(engine_schematic, seen)
    total = 0

    for symbol_pos in symbol_positions:
        numbers = find_numbers_around_symbol(engine_schematic, seen,
                                             symbol_pos)
        total = reduce(lambda acc, x: acc + x, numbers, total)

    print(total)


def part2(puzzle_input: list[str]) -> None:
    engine_schematic = parse_lines_into_a_2d_list(puzzle_input)

    seen = [[False] * len(inner) for inner in engine_schematic]
    gear_positions = find_gear_positions(engine_schematic, seen)

    total = 0
    for gear_pos in gear_positions:
        numbers = find_numbers_around_symbol(engine_schematic, seen,
                                             gear_pos)
        if len(numbers) == 2:
            total = total + reduce(lambda acc, x: acc * x, numbers, 1)

    print(total)


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[0])
    part1(puzzle_input)
    part2(puzzle_input)


if __name__ == '__main__':
    main(sys.argv[1:])
