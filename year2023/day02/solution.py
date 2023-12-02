import sys


GameResultPart1 = tuple[int, bool]
GameResultPart2 = tuple[int, int, int, int]

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def get_input(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        data = f.read().splitlines()

    return data


def split_game_id_and_cube_sets(game: str) -> tuple[int, str]:
    aux, cube_sets = game.split(': ')
    game_id = int(aux.split(' ')[1])

    return game_id, cube_sets;


def find_possible_games(cube_sets: str) -> bool:
    cube_sets_arr = [cube_set.strip() for cube_set in cube_sets.split(';')]

    for cube_set in cube_sets_arr:
        cube_colors = [cubes.strip() for cubes in cube_set.split(',')]

        for cube_color in cube_colors:
            amount, color = cube_color.split(' ')

            if (
                color == 'red' and int(amount) > MAX_RED
                or color == 'green' and int(amount) > MAX_GREEN
                or color == 'blue' and int(amount) > MAX_BLUE
            ):
                return False

    return True


def get_total(games: list[GameResultPart1]) -> int:
    total = 0
    for game_id, possible_game in games:
        total += game_id if possible_game else 0

    return total


def get_mininum_number_of_cubes(cube_sets: str) -> tuple[int, int, int]:
    min_red_cubes = 0
    min_green_cubes = 0
    min_blue_cubes = 0

    cube_sets_arr = [cube_set.strip() for cube_set in cube_sets.split(';')]
    for cube_set in cube_sets_arr:
        cube_colors = [cubes.strip() for cubes in cube_set.split(',')]
        for cube_color in cube_colors:
            amount, color = cube_color.split(' ')

            if color == 'red':
                min_red_cubes = int(amount) if int(amount) > min_red_cubes else min_red_cubes
            elif color == 'green':
                min_green_cubes = int(amount) if int(amount) > min_green_cubes else min_green_cubes
            elif color == 'blue':
                min_blue_cubes = int(amount) if int(amount) > min_blue_cubes else min_blue_cubes
    
    return min_red_cubes, min_green_cubes, min_blue_cubes

def get_sum(games: list[GameResultPart2]) -> int:
    total = 0
    for game in games:
        total += game[1] * game[2] * game[3]

    return total


def part1(input_data: list[str]) -> None:
    games: list[GameResultPart1] = list()
    for line in input_data:
        game_id, cube_sets = split_game_id_and_cube_sets(line)
        possible_game = find_possible_games(cube_sets)

        games.append((game_id, possible_game))

    total = get_total(games)
    print(total)


def part2(input_data: list[str]) -> None:
    games: list[GameResultPart2] = list()
    for line in input_data:
        game_id, cube_sets = split_game_id_and_cube_sets(line)
        min_cube_set = get_mininum_number_of_cubes(cube_sets)
        games.append((game_id,)+min_cube_set)

    total = get_sum(games)
    print(total)


def main(args: list[str]) -> None:
    input_data = get_input(args[0])

    part1(input_data)
    part2(input_data)


if __name__ == '__main__':
    main(sys.argv[1:])
