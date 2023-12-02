import sys


def get_input(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        data = f.read().splitlines()

    return data


def store_calories_by_each_elf(calories_list: list[str]) -> dict:
    i = 1
    elfs: dict[str, int] = dict()

    for calories in calories_list:
        k = 'elf%d' % i
        if calories.isdigit():

            elfs[k] = elfs[k] + int(calories) if k in elfs else int(calories)
        else:
            i += 1

    return elfs


def generate_calories_top_list(elfs: dict[str, int]) -> list[str]:
    calories_leaderboard: list[str] = list()
    for elf, calories in elfs.items():
        if len(calories_leaderboard) == 0:
            calories_leaderboard.append(elf)
        else:
            for idx, cal_entry in enumerate(calories_leaderboard):
                if calories > elfs[cal_entry]:
                    calories_leaderboard.insert(idx, elf)
                    break

            if elf not in calories_leaderboard:
                calories_leaderboard.append(elf)

    return calories_leaderboard


def get_top_n_elves(calories_top_list: list[str], top_n: int, elfs: dict[str, int]) -> int:
    total = 0

    for i in range(0, top_n, 1):
        total += elfs[calories_top_list[i]]

    return total


def main(args: list[str]) -> None:
    calories_list = get_input(args[0])

    elfs = store_calories_by_each_elf(calories_list)
    calories_top_list = generate_calories_top_list(elfs)
    total = get_top_n_elves(calories_top_list, 3, elfs)

    print(total)


if __name__ == '__main__':
    main(sys.argv[1:])
