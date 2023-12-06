import sys

from typing import cast

from adventofcode.utils import utils

Seed = int
Map = tuple[int, ...]


def parse(puzzle_input: list[str]) -> dict[str, list[Seed | Map]]:
    almanac: dict[str, list[Seed | Map]] = dict()
    current_map = ''
    for line in puzzle_input:
        if line == '':
            continue

        if line.startswith("seeds"):
            almanac['seeds'] = [int(seed) for seed in
                                line.split(':')[1].strip().split(' ')]
        elif line.endswith('map:'):
            current_map = line.split(' ')[0]
        else:
            if current_map not in almanac.keys():
                almanac[current_map] = list()

            almanac_map = tuple(int(num) for num in line.split(' '))
            almanac[current_map].append(almanac_map)

    return almanac


def get_destination(src_start: int, src_to_dst_maps: list[Map]):
    dst = src_start
    for map in src_to_dst_maps:
        m_dst_start, m_src_start, m_rng = map

        if m_src_start <= src_start and src_start < m_src_start + m_rng:
            dst = m_dst_start + src_start - m_src_start

    return dst


def get_destination_from_sources(sources: list[int],
                                 src_to_dst_maps: list[Map]) -> list[int]:
    destinations: list[int] = []
    for src in sources:
        dst = get_destination(src, src_to_dst_maps)

        destinations.append(dst)

    return destinations


def slice_source_ranges_for_maps(source_ranges: list[int],
                                 src_to_dst_maps: list[Map]) -> list[int]:
    for map in src_to_dst_maps:
        _, m_src_start, m_rng = map

        aux_src_rngs = []
        i = 0
        while i < len(source_ranges):
            s_start, s_rng = source_ranges[i], source_ranges[i+1]

            left_rng = max(min(m_src_start - s_start, s_rng), 0)

#            p13 = s_start
#            q13 = s_rng
#            r13 = p13 + r13
#            s13 = m_src_start
#            t13 = m_rng
#            u13 = s13 + t13
#            v13 = p13
#            w13 = left_rng
#            x13 = p13 + w13
#            y13 = max(min(s13, p13 + w13), r13)
#            z13 = min(u13, p13 + q13)
#            aa13 = min(y13, z13)
#            mid_rng = max(aa13 - x13, 0)
            mid_rng = max(min(max(min(m_src_start, s_start + left_rng),
                                  s_start + s_rng),
                              min((m_src_start + m_rng), s_start + s_rng))
                          - (s_start + left_rng), 0)

            right_rng = max(s_start + s_rng - max(m_src_start + m_rng,
                                                  s_start),
                            0)

            left_src = [s_start, left_rng] if left_rng > 0 else []
            mid_src = [s_start + left_rng, mid_rng] if mid_rng > 0 else []
            right_src = ([s_start + left_rng + mid_rng, right_rng]
                         if right_rng > 0 else [])

            aux_src_rngs += left_src + mid_src + right_src
            i += 2

        source_ranges = aux_src_rngs
    return source_ranges


def get_src_ranges_to_dst_ranges(source_ranges: list[int],
                                 src_to_dst_maps: list[Map]) -> list[int]:
    destinations: list[int] = []
    i = 0
    source_ranges = slice_source_ranges_for_maps(source_ranges,
                                                 src_to_dst_maps)

    while i < len(source_ranges):
        s_start, s_rng = source_ranges[i], source_ranges[i+1]
        dst_rng = [s_start, s_rng]

        for map in src_to_dst_maps:
            m_dst_start, m_src_start, m_rng = map
            dst = m_dst_start + s_start - m_src_start

            if (m_src_start <= s_start
                    and s_start < m_src_start + m_rng - 1):
                dst_rng = [dst, s_rng]

        destinations += dst_rng
        i += 2

    return destinations


def part1(puzzle_input: list[str]) -> None:
    almanac = parse(puzzle_input)
    sources = cast(list[Seed], almanac.pop('seeds'))
    for key in almanac.keys():
        sources = get_destination_from_sources(sources,
                                               cast(list[Map], almanac[key]))

    print(min(sources))


def part2(puzzle_input: list[str]) -> None:
    almanac = parse(puzzle_input)
    source_ranges = cast(list[Seed], almanac.pop('seeds'))
    for key in almanac.keys():
        source_ranges = get_src_ranges_to_dst_ranges(
                source_ranges, cast(list[Map], almanac[key]))

    print(min(n for i, n in enumerate(source_ranges) if i % 2 == 0))


def main(args: list[str]) -> None:
    puzzle_input = utils.readlines(args[1])

    try:
        part1(puzzle_input)
        part2(puzzle_input)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(sys.argv)
