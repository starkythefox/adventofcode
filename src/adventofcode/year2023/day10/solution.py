import sys

from typing import Optional

from adventofcode.utils import utils

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

Connection = tuple[int, int]
Maze = list[list['Node']]
Seen = list[list[bool]]

NW_SE_TURN = 'NW-SE'
NE_SW_TURN = 'NE-SW'


class Node:
    value: str
    x: int
    y: int
    prev: Optional['Node']
    next: Optional['Node']
    possible_connections: set[Connection]

    def __init__(self, value: str, x: int, y: int,
                 prev: Optional['Node'] = None,
                 next: Optional['Node'] = None) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.prev = prev
        self.next = next
        self.possible_connections = self.generate_possible_connections(value)

    def __str__(self):
        node_str = "%s(%d, %d)"
        prev_node = ((node_str + " <- ") % (self.prev.value, self.prev.x,
                                            self.prev.y)
                     if self.prev else '')
        next_node = ((" -> " + node_str) % (self.next.value, self.next.x,
                                            self.next.y)
                     if self.next else '')

        return (prev_node + node_str + next_node) % (self.value, self.x,
                                                     self.y)

    def __repr__(self):
        return self.__str__()

    def generate_possible_connections(self, value: str) -> set[Connection]:
        if value == '|':
            return {UP, DOWN}

        if value == '-':
            return {RIGHT, LEFT}

        if value == 'L':
            return {UP, RIGHT}

        if value == 'J':
            return {UP, LEFT}

        if value == '7':
            return {DOWN, LEFT}

        if value == 'F':
            return {RIGHT, DOWN}

        if value == 'S':
            return {UP, RIGHT, DOWN, LEFT}

        return set()

    def can_connect_to(self, node: 'Node') -> bool:
        return self.possible_connections.__contains__((node.x - self.x,
                                                      node.y - self.y))


def join_nodes(node, adjacent_node, reverse, stack) -> None:
    if not reverse:
        if node.next is None:
            adjacent_node.prev = node
            node.next = adjacent_node
            stack.append((node.next, False))
        elif not reverse and node.prev is None:
            adjacent_node.next = node
            node.prev = adjacent_node
            stack.append((node.prev, True))
    else:
        if node.prev is None:
            adjacent_node.next = node
            node.prev = adjacent_node
            stack.append((node.prev, True))
        elif reverse and node.next is None:
            adjacent_node.prev = node
            node.next = adjacent_node
            stack.append((node.next, False))


def find_node_connections(node, reverse, maze, seen, stack) -> None:
    for connection in node.possible_connections:
        x = node.x + connection[0]
        y = node.y + connection[1]
        if (x < 0 or x >= len(maze[node.y]) or y < 0 or y >= len(maze)):
            continue

        if seen[y][x]:
            continue

        adjacent_node = maze[y][x]

        if (adjacent_node.can_connect_to(node)):
            join_nodes(node, adjacent_node, reverse, stack)


def find_all_connections(node: Node, maze: Maze, seen: Seen) -> None:
    stack = [(node, False)]
    while True:
        if len(stack) == 0:
            break

        curr, reverse = stack.pop()
        if seen[curr.y][curr.x]:
            continue

        find_node_connections(curr, reverse, maze, seen, stack)
        seen[curr.y][curr.x] = True


def parse_maze(puzzle_input: list[str]) -> tuple[Maze, tuple[int, int]]:
    maze = []
    for y, line in enumerate(puzzle_input):
        row = []
        for x, value in enumerate(line):
            if value == 'S':
                starting_node_pos = (x, y)

            row.append(Node(value=value, x=x, y=y))

        maze.append(row)

    return maze, starting_node_pos


def fix_starting_point_value(node: Node):
    assert node.prev is not None and node.next is not None

    directions = {(node.x - node.prev.x, node.y - node.prev.y),
                  (node.x - node.next.x, node.y - node.next.y)}

    if directions == {UP, DOWN}:
        node.value = '|'
    elif directions == {RIGHT, LEFT}:
        node.value = '-'
    elif directions == {UP, RIGHT}:
        node.value = '7'
    elif directions == {UP, LEFT}:
        node.value = 'F'
    elif directions == {DOWN, LEFT}:
        node.value = 'L'
    elif directions == {RIGHT, DOWN}:
        node.value = 'J'


def calculate_max_distance(maze: Maze,
                           starting_node_pos: tuple[int, int]) -> int:
    distances = [0]
    starting_node = maze[starting_node_pos[1]][starting_node_pos[0]]
    n = starting_node.next
    p = starting_node.prev
    i = 1
    while True:
        distances.append(i)
        i += 1
        if n == p:
            break

        n = n.next if n else None
        p = p.prev if p else None

    return max(distances)


def part1(puzzle_input: list[str]) -> int:
    maze, starting_node_pos = parse_maze(puzzle_input)

    seen = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    for row in maze:
        for node in row:
            find_all_connections(node, maze, seen)

    fix_starting_point_value(maze[starting_node_pos[1]][starting_node_pos[0]])
    return calculate_max_distance(maze, starting_node_pos)


def part2(puzzle_input: list[str]) -> int:
    maze, starting_node_pos = parse_maze(puzzle_input)

    seen = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    for row in maze:
        for node in row:
            find_all_connections(node, maze, seen)

    fix_starting_point_value(maze[starting_node_pos[1]][starting_node_pos[0]])
    connected_loop = []
    starting_node = maze[starting_node_pos[1]][starting_node_pos[0]]
    curr: Node | None = starting_node
    while True:
        if curr is None:
            break

        connected_loop.append(curr)
        curr = curr.next

        if (starting_node == curr):
            break

    count = 0
    for y, row in enumerate(maze):
        is_inside = False
        on_pipe = ''
        for x, node in enumerate(row):
            if connected_loop.__contains__(node):
                if node.value in ('F', 'J'):
                    if on_pipe == NW_SE_TURN:
                        is_inside = not is_inside
                        on_pipe = ''
                    elif on_pipe == NE_SW_TURN:
                        on_pipe = ''
                    else:
                        on_pipe = NW_SE_TURN
                elif node.value in ('7', 'L'):
                    if on_pipe == NE_SW_TURN:
                        is_inside = not is_inside
                        on_pipe = ''
                    elif on_pipe == NW_SE_TURN:
                        on_pipe = ''
                    else:
                        on_pipe = NE_SW_TURN
                elif on_pipe == '':
                    is_inside = not is_inside
            else:
                count += 1 if is_inside else 0

    return count


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])
    print(part1(puzzle_input))
    print(part2(puzzle_input))


if __name__ == '__main__':
    main(sys.argv)
