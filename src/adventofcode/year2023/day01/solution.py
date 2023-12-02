import sys
import functools

from adventofcode.utils import utils

NUMBERS_IN_TEXT = {'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                   'eight', 'nine'}

NUMBER_TRANSLATION = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def parse(input_str: str) -> int:
    if len(input_str) == 0:
        return 0

    parsed = list()

    i = 0
    while i < len(input_str):
        if input_str[i].isnumeric():
            parsed.append(input_str[i])
            i += 1
            continue

        j = i
        while j < len(input_str) and not input_str[j].isnumeric():
            if input_str[i:j+1] in NUMBERS_IN_TEXT:
                parsed.append(NUMBER_TRANSLATION[input_str[i:j+1]])

            j += 1

        i += 1

    print(input_str, parsed[0], parsed[-1], parsed)
    return int(parsed[0] + parsed[-1])


def main(args: list[str]) -> None:
    input_data = utils.readlines(args[0])
    numbers: list[int] = list()

    for line in input_data:
        numbers.append(parse(line))

    total = functools.reduce(lambda a, b: a + b, numbers)
    print(total)


if __name__ == '__main__':
    main(sys.argv[1:])
