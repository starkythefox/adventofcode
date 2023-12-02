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
    X = 'ROCK'
    B = 'PAPER'
    Y = 'PAPER'
    C = 'SCISSORS'
    Z = 'SCISSORS'


def get_move(move_code: str) -> str:
    return Move[move_code].value


def check_round_result(theirs: str, mine: str) -> int:
    score = 0
    if (get_move(theirs) == 'ROCK' and get_move(mine) == 'PAPER' or
            get_move(theirs) == 'PAPER' and get_move(mine) == 'SCISSORS' or
            get_move(theirs) == 'SCISSORS' and get_move(mine) == 'ROCK'):
        score = RoundScore.WIN.value + MoveScore[get_move(mine)].value
    elif (get_move(theirs) == 'ROCK' and get_move(mine) == 'SCISSORS' or
            get_move(theirs) == 'PAPER' and get_move(mine) == 'ROCK' or
            get_move(theirs) == 'SCISSORS' and get_move(mine) == 'PAPER'):
        score = RoundScore.LOSS.value + MoveScore[get_move(mine)].value
    else:
        score = RoundScore.TIE.value + MoveScore[get_move(mine)].value

    return score


def main(args: list[str]) -> None:
    cheatcodes = utils.readlines(args[0])
    total = 0

    for cheatcode in cheatcodes:
        codes = cheatcode.split(' ')

        if (len(cheatcode) > 1):
            total += check_round_result(codes[0], codes[1])

    print(total)


if __name__ == '__main__':
    main(sys.argv[1:])
