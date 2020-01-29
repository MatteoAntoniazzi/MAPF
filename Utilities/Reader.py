import os
import pathlib

import numpy as np

from Utilities.macros import *


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


def get_scene_file_path(map_number, scene_type, scene_number):
    map_name = MAPS_NAMES_LIST.get(map_number)
    root_path = pathlib.Path(__file__).parent.parent
    scene_file_path = str(root_path / "Maps/scenes-") + scene_type + "/" + map_name + "-" + scene_type + "-" + str(scene_number) + ".scen"
    print(scene_file_path)
    return scene_file_path


class Reader:
    def __init__(self, map_number=0, scene_type="even", scene_file_number=1):
        self._map_number = map_number
        self._scene_type = scene_type
        self._scene_file_number = scene_file_number

        self._reload_instances = True  # If False it loads scene instances already loaded

        self._scene_instances = None
        self._change_scene_instances = False

    def load_map_file(self, occupied_char='@', valid_chars={'@', '.', 'T'}):
        assert(self._map_number is not None), "Map Number Not Set"

        root_path = pathlib.Path(__file__).parent.parent
        map_path = str(root_path / "Maps/maps/" / MAPS_NAMES_LIST.get(self._map_number)) + ".map"
        print(map_path)
        if not os.path.isfile(map_path):
            print("Map file not found!")
            exit(-1)
        map_ls = open(map_path, 'r').readlines()
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

    def load_scenario_file(self, occupancy_lst, map_width, map_height, n_of_agents=10):
        """
        Load a random scenario file. The random scenarios are used and since the agents are taken completely random the
        paths can be very long and the computation with some algorithm very long.
        :param occupancy_lst: list of the obstacles
        :param map_width: width of the map
        :param map_height: height of the map
        :param n_of_agents: number of agents to return
        :return: array of start and destination couples
        """
        scene_file_path = get_scene_file_path(self._map_number, self._scene_type, self._scene_file_number)

        if self._reload_instances:
            self.load_instances(scene_file_path, map_width, map_height)
            self._reload_instances = False

        if self._change_scene_instances:
            if self._scene_type == "even":
                values = [x[0] for x in self._scene_instances]
                next_bucket_number = self._scene_instances[len(self._scene_instances)-1][0]
                idx = values.index(next_bucket_number)
                self._scene_instances = self._scene_instances[idx:] + self._scene_instances[:idx-1]

                # from random import choice
                # values = [x[0] for x in self._scene_instances]
                # random_value = choice(tuple(set(values)))
                # idx = values.index(random_value)
                # self._scene_instances = self._scene_instances[idx:] + self._scene_instances[:idx - 1]

            elif self._scene_type == "random":
                np.random.shuffle(self._scene_instances)

            self._change_scene_instances = False

        instances = [((i[4], i[5]), (i[6], i[7])) for i in self._scene_instances]
        for start, goal in instances:
            assert(start not in occupancy_lst), "Overlapping error"
            assert(goal not in occupancy_lst), "Overlapping error"
        return instances[:n_of_agents]

    def change_scene_instances(self):
        self._change_scene_instances = True

    def load_instances(self, scene_file_path, map_width, map_height):
        if not os.path.isfile(scene_file_path):
            print("Scenario file not found!")
            exit(-1)
        ls = open(scene_file_path, 'r').readlines()
        if "version 1" not in ls[0]:
            print(".scen version type does not match!")
            exit(-1)
        self._scene_instances = [convert_nums(l.split('\t')) for l in ls[1:]]
        self._scene_instances.sort(key=lambda e: e[0])

        for i in self._scene_instances:
            assert (i[2] == map_width)
            assert (i[3] == map_height)

    def set_map(self, map_number):
        print("READER SET MAP ", map_number)
        self._map_number = map_number
        self._reload_instances = True

    def set_scene_type(self, scene_type):
        print("READER SCENE TYPE ", scene_type)
        self._scene_type = scene_type
        self._reload_instances = True

    def set_scene_file_number(self, scene_file_number):
        print("READER SET SCENE NUMBER ", scene_file_number)
        self._scene_file_number = scene_file_number
        self._reload_instances = True

    # TEST 1
    # return [instances[1], instances[7], instances[19], instances[22], instances[28], instances[42]]
    # TEST 2
    # return [instances[1], instances[7], instances[19]]
    # TEST 3
    # return [instances[28], instances[42]]
    # TEST 4
    # return [instances[1], instances[22], instances[28]]
    # TEST 5
    # return [instances[2], instances[24], instances[30]]
    # TEST 6
    # return [instances[26], instances[37]]
    # TEST 7
    # return [instances[21], instances[33]]
    # TEST 8
    # return [instances[21], instances[42]]

    # def setup_args(self):
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("map", type=str, help=".map Map file")
    #     parser.add_argument("scenario", type=str, help=".scen Scenario file")
    #     return parser.parse_args()
