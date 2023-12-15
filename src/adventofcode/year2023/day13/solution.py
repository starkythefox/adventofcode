from src.adventofcode.utils import utils
import sys

Mirror = list[list[str]]


def find_mirrors_in_puzzle(puzzle_input: str) -> list[Mirror]:
    mirrors = []
    mirror: Mirror = list()

    for line in puzzle_input:
        if len(line) == 0:
            mirrors.append(mirror)
            mirror = list()
        else:
            mirror.append(list(line))

    mirrors.append(mirror)
    return mirrors


def compare(a: list[str], b: list[str], i: int, length: int,
            acc: int) -> tuple[int, bool, bool]:
    opposite = i + acc*2 + 1
    if ''.join(a) == ''.join(b):
        acc += 1
        if i == 0 or opposite + 1 >= length:
            return acc, True, True

        return acc, True, False

    return acc, False, False


def find_reflection_in_cols(mirror: Mirror, exclude: int) -> int:
    cols = 0
    for i in range(0, len(mirror[0]) - 1, 1):
        if i == exclude:
            continue

        for j in range(i, -1, -1):
            opposite = i + cols + 1

            cols, match, full_match = compare(
                    [row[j] for row in mirror],
                    [row[opposite] for row in mirror], j, len(mirror[0]), cols)
            if full_match:
                return i + 1

            if not match:
                cols = 0
                break

    return 0


def find_reflection_in_rows(mirror: Mirror, exclude: int) -> int:
    rows = 0
    for i in range(0, len(mirror) - 1, 1):
        if i == exclude:
            continue

        for j in range(i, -1, -1):
            opposite = i + rows + 1

            rows, match, full_match = compare(mirror[j], mirror[opposite], j,
                                              len(mirror), rows)
            if full_match:
                return i + 1

            if not match:
                rows = 0
                break

    return 0


def find_reflections(mirror: Mirror, exclude: int = -1) -> int:
    res = find_reflection_in_cols(mirror,
                                  (exclude - 1) if 0 <= exclude < 100 else -1)

    if res == 0:
        res = find_reflection_in_rows(
                mirror, (exclude // 100 - 1) if exclude >= 100 else -1)

        return res * 100 if res > 0 else 0

    return res


def smudge_then_find_reflections(mirror: Mirror) -> int:
    orig_refl = find_reflections(mirror)
    for i, row in enumerate(mirror):
        for j in range(len(row)):
            orig_char = row[j]
            row[j] = '#' if orig_char == '.' else '.'

            res = find_reflections(mirror, orig_refl)
            if res > 0:
                return res

            row[j] = orig_char

    return 0


def part1(puzzle_input: str) -> int:
    mirrors = find_mirrors_in_puzzle(puzzle_input)

    total = 0
    for mirror in mirrors:
        total += find_reflections(mirror)

    return total


def part2(puzzle_input: str) -> int:
    mirrors = find_mirrors_in_puzzle(puzzle_input)

    total = 0
    for mirror in mirrors:
        total += smudge_then_find_reflections(mirror)

    return total


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])
    print(part1(puzzle_input))
    print(part2(puzzle_input))


if __name__ == '__main__':
    main(sys.argv)
