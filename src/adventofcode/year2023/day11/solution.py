import sys

from typing import Optional

from adventofcode.utils import utils

ImageRow = list[Optional['Point']]
UniverseImage = list[ImageRow]


class Point:
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return '(%d, %d)' % (self.x, self.y)

    def __repr__(self) -> str:
        return self.__str__()


def parse_image(puzzle_input: list[str]) -> UniverseImage:
    image = list()
    for i, line in enumerate(puzzle_input):
        row: ImageRow = list()
        for j, char in enumerate(line):
            if char == '#':
                row.append(Point(j, i))
            else:
                row.append(None)

        image.append(row)

    return image


def find_expanded_zones(image: UniverseImage) -> tuple[list[int],
                                                       list[int]]:
    rows = [i for i, row in enumerate(image) if all(
        point is None for point in row)]
    columns = [j for j in range(len(image[0])) if all(
        image[i][j] is None for i in range(len(image)))]

    return rows, columns


def get_all_points(image: UniverseImage) -> list[Point]:
    return [point for row in image for point in row if point is not None]


def calc_shortest_distance(point_a: Point, point_b: Point,
                           expanded_rows: list[int],
                           expanded_columns: list[int],
                           expansion_factor: int = 2) -> int:
    distance = abs(point_b.x - point_a.x) + abs(point_b.y - point_a.y)

    min_x = min(point_a.x, point_b.x)
    max_x = max(point_a.x, point_b.x)
    min_y = min(point_a.y, point_b.y)
    max_y = max(point_a.y, point_b.y)
    for row in expanded_rows:
        distance += expansion_factor - 1 if min_y < row < max_y else 0

    for col in expanded_columns:
        distance += expansion_factor - 1 if min_x < col < max_x else 0

    return distance


def part1(puzzle_input: list[str]) -> int:
    image = parse_image(puzzle_input)
    expanded_rows, expanded_columns = find_expanded_zones(image)
    points = get_all_points(image)

    sum_distances = 0
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            sum_distances += calc_shortest_distance(points[i], points[j],
                                                    expanded_rows,
                                                    expanded_columns)

    return sum_distances


def part2(puzzle_input: list[str]) -> int:
    image = parse_image(puzzle_input)
    expanded_rows, expanded_columns = find_expanded_zones(image)
    points = get_all_points(image)

    sum_distances = 0
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            sum_distances += calc_shortest_distance(points[i], points[j],
                                                    expanded_rows,
                                                    expanded_columns,
                                                    1000000)

    return sum_distances


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])
    print(part1(puzzle_input))
    print(part2(puzzle_input))


if __name__ == '__main__':
    main(sys.argv)
