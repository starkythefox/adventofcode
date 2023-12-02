import sys
from enum import Enum

from adventofcode.utils import utils


class MoveScore(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RoundScore(Enum):
    LOSS = 0
    TIE = 3
    WIN = 6


class Move(Enum):
    A = 'ROCK'
    B = 'PAPER'
    C = 'SCISSORS'


class RoundOutcome(Enum):
    X = 'LOSS'
    Y = 'TIE'
    Z = 'WIN'


def get_input(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        data = f.read().splitlines()

    return data


def get_move(move_code: str) -> str:
    return Move[move_code].value


def check_round_result(theirs: str, mine: str) -> int:
    score = 0
    is_my_move_paper = (
        get_move(theirs) == 'ROCK' and RoundOutcome[mine].value == 'WIN'
        or get_move(theirs) == 'PAPER' and RoundOutcome[mine].value == 'TIE'
        or get_move(theirs) == 'SCISSORS'
        and RoundOutcome[mine].value == 'LOSS')

    is_my_move_scissors = (
        get_move(theirs) == 'ROCK' and RoundOutcome[mine].value == 'LOSS'
        or get_move(theirs) == 'PAPER' and RoundOutcome[mine].value == 'WIN'
        or get_move(theirs) == 'SCISSORS'
        and RoundOutcome[mine].value == 'TIE')

    if is_my_move_paper:
        score = (RoundScore[RoundOutcome[mine].value].value
                 + MoveScore.PAPER.value)
    elif is_my_move_scissors:
        score = (RoundScore[RoundOutcome[mine].value].value
                 + MoveScore.SCISSORS.value)
    else:
        score = (RoundScore[RoundOutcome[mine].value].value
                 + MoveScore.ROCK.value)

    return score


def main(args: list[str]):
    cheatcodes = utils.readlines(args[0])
    total = 0

    for cheatcode in cheatcodes:
        codes = cheatcode.split(' ')

        if (len(cheatcode) > 1):
            total += check_round_result(codes[0], codes[1])

    print(total)


if __name__ == '__main__':
    main(sys.argv[1:])
