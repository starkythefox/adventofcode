import sys
import math

from adventofcode.utils import utils


def parse_nodes(node_list: list[str]) -> dict[str, tuple]:
    nodes = dict()
    for line in node_list:
        node = line.split('=')[0].strip()
        dst = tuple(line.split('=')[1].strip().replace('(', '')
                    .replace(')', '').split(', '))

        nodes[node] = dst

    return nodes


def find_amount_of_steps(curr_node: str, last_node_ends_with: str,
                         left_right_moves: str,
                         nodes: dict[str, tuple]) -> int:
    steps = 0
    i = 0
    while not curr_node.endswith(last_node_ends_with):
        lr_move = left_right_moves[i]

#        print(curr_node, i, lr_move, nodes[curr_node])
        curr_node = (nodes[curr_node][0] if lr_move == 'L'
                     else nodes[curr_node][1])

        i = i + 1 if i + 1 < len(left_right_moves) else 0
        steps += 1

    return steps


def part1(puzzle_input: list[str]) -> None:
    left_right_moves = puzzle_input[0]
    nodes = parse_nodes(puzzle_input[2:])

    print(find_amount_of_steps('AAA', 'ZZZ', left_right_moves, nodes))


def part2(puzzle_input: list[str]) -> None:
    left_right_moves = puzzle_input[0]
    nodes = parse_nodes(puzzle_input[2:])

    curr_nodes = [node for node in nodes.keys() if node.endswith('A')]
    steps_per_starting_node: list[int] = []

    for curr_node in curr_nodes:
        steps_per_starting_node.append(
                find_amount_of_steps(curr_node, 'Z', left_right_moves, nodes))

    print(math.lcm(*steps_per_starting_node))


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])
    part1(puzzle_input)
    part2(puzzle_input)


if __name__ == '__main__':
    main(sys.argv)
