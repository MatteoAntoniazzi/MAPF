import os
import argparse


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=str, help=".map Map file")
    parser.add_argument("scenario", type=str, help=".scen Scenario file")
    return parser.parse_args()


def convert_nums(l):
    for i in range(len(l)):
        try:
            l[i] = int(l[i])
        except ValueError:
            try:
                l[i] = float(l[i])
            except ValueError:
                ""
    return l


def load_map_file(map_file, occupied_char='@', valid_chars={'@', '.', 'T'}):
    if not os.path.isfile(map_file):
        print("Map file not found!")
        exit(-1)
    map_ls = open(map_file, 'r').readlines()
    height = int(map_ls[1].replace("height ", ""))
    width = int(map_ls[2].replace("width ", ""))
    map_ls = map_ls[4:]
    map_ls = [l.replace('\n', '') for l in map_ls]
    occupancy_lst = set()
    assert(len(map_ls) == height)
    for y, l in enumerate(map_ls):
        assert(len(l) == width)
        for x, c in enumerate(l):
            assert(c in valid_chars)
            if c == occupied_char:
                occupancy_lst.add((x, y))
    return width, height, occupancy_lst


def load_scenario_file(scen_file, occupancy_list, map_width, map_height, number_of_agents=10):
    if not os.path.isfile(scen_file):
        print("Scenario file not found!")
        exit(-1)
    ls = open(scen_file, 'r').readlines()
    if "version 1" not in ls[0]:
        print(".scen version type does not match!")
        exit(-1)
    instances = [convert_nums(l.split('\t')) for l in ls[1:]]
    instances.sort(key=lambda e: e[0])
    for i in instances:
        assert(i[2] == map_width)
        assert(i[3] == map_height)
    # ((sx, sy), (gx, gy))
    instances = [((i[4], i[5]), (i[6], i[7])) for i in instances]
    for start, goal in instances:
        assert(start not in occupancy_list), "Overlapping error"
        assert(goal not in occupancy_list), "Overlapping error"
    # return instances[:number_of_agents]
    # return [instances[1], instances[7], instances[19], instances[22], instances[28], instances[42]]
    return [instances[28], instances[42]]
    # return [instances[1], instances[22], instances[28]]
    # return [instances[2], instances[24], instances[30]]
    # return [instances[26], instances[37]]
    # return [instances[21], instances[33]]
    # return [instances[21], instances[42]]
