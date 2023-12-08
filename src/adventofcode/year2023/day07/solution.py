import sys

from functools import cmp_to_key

from adventofcode.utils import utils

CARDS_1 = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

CARDS_2 = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 1,
    'Q': 12,
    'K': 13,
    'A': 14
}


HANDS = {
    'high_card': 1,
    'one_pair': 2,
    'two_pair': 3,
    'three_kind': 4,
    'full_house': 5,
    'four_kind': 6,
    'five_kind': 7
}


def get_hand_value_part1(hand: str) -> int:
    set_of_cards = set(hand)
    card_count = [(card, hand.count(card)) for card in set_of_cards]
    card_count.sort(key=lambda x: x[1], reverse=True)

    if card_count[0][1] == 5:
        return HANDS['five_kind']

    if card_count[0][1] == 4:
        return HANDS['four_kind']

    if card_count[0][1] == 3:
        if card_count[1][1] == 2:
            return HANDS['full_house']

        return HANDS['three_kind']

    if card_count[0][1] == 2:
        if card_count[1][1] == 2:
            return HANDS['two_pair']

        return HANDS['one_pair']

    return HANDS['high_card']


def get_hand_value_part2(hand: str) -> int:
    set_of_cards = set(hand)

    if len(set_of_cards) >= 2 and 'J' in set_of_cards:
        set_of_cards.remove('J')
        hand = hand.replace('J', max(set_of_cards,
                                     key=lambda x: hand.count(x)))

    card_count = [(card, hand.count(card)) for card in set_of_cards]
    card_count.sort(key=lambda x: x[1], reverse=True)

    if card_count[0][1] == 5:
        return HANDS['five_kind']

    if card_count[0][1] == 4:
        return HANDS['four_kind']

    if card_count[0][1] == 3:
        if card_count[1][1] == 2:
            return HANDS['full_house']

        return HANDS['three_kind']

    if card_count[0][1] == 2:
        if card_count[1][1] == 2:
            return HANDS['two_pair']

        return HANDS['one_pair']

    return HANDS['high_card']


def sort_hands_part1(x, y):
    if x[0] == y[0]:
        return 0

    for i in range(0, 5):
        if x[0][i] != y[0][i]:
            x_cmp = get_hand_value_part1(x[0]) * 15 + CARDS_1[x[0][i]]
            y_cmp = get_hand_value_part1(y[0]) * 15 + CARDS_1[y[0][i]]
            value = (x_cmp - y_cmp)

            return value


def sort_hands_part2(x, y):
    if x[0] == y[0]:
        return 0

    for i in range(0, 5):
        if x[0][i] != y[0][i]:
            x_cmp = get_hand_value_part2(x[0]) * 15 + CARDS_2[x[0][i]]
            y_cmp = get_hand_value_part2(y[0]) * 15 + CARDS_2[y[0][i]]
            value = (x_cmp - y_cmp)

            return value


def part1(puzzle_input: list[str]) -> None:
    hands = [(line.split()[0], int(line.split()[1])) for line in puzzle_input]

    hands.sort(key=cmp_to_key(sort_hands_part1), reverse=True)

    rank = len(hands)
    total = 0
    for hand in hands:
        total += hand[1]*rank
        rank -= 1

    print(total)


def part2(puzzle_input: list[str]) -> None:
    hands = [(line.split()[0], int(line.split()[1])) for line in puzzle_input]

    hands.sort(key=cmp_to_key(sort_hands_part2), reverse=True)

    rank = len(hands)
    total = 0
    for hand in hands:
        total += hand[1]*rank
        rank -= 1

    print(total)


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])

    part1(puzzle_input)
    part2(puzzle_input)


if __name__ == '__main__':
    main(sys.argv)
