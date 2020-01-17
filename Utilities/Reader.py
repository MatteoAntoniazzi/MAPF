import os
import numpy as np


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


class Reader:
    def __init__(self):
        self._scene_file = None
        self._scene_instances = None
        self._shuffle = False

    def load_map_file(self, map_file, occupied_char='@', valid_chars={'@', '.', 'T'}):
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

    def load_random_scenario_file(self, scen_file, occupancy_lst, map_width, map_height, n_of_agents=10):
        """
        Load a random scenario file. The random scenarios are used and since the agents are taken completely random the
        paths can be very long and the computation with some algorithm very long.
        :param scen_file: scen file path
        :param occupancy_lst: list of the obstacles
        :param map_width: width of the map
        :param map_height: height of the map
        :param n_of_agents: number of agents to return
        :return:
        """
        if scen_file != self._scene_file:
            self._scene_file = scen_file
            self.load_instances(map_width, map_height)

        if self._shuffle:
            np.random.shuffle(self._scene_instances)
            self._shuffle = False

        instances = [((i[4], i[5]), (i[6], i[7])) for i in self._scene_instances]
        for start, goal in instances:
            assert(start not in occupancy_lst), "Overlapping error"
            assert(goal not in occupancy_lst), "Overlapping error"
        return instances[:n_of_agents]

    def load_even_scenario_file(self, scen_file, occupancy_list, map_width, map_height, n_of_agents=10):
        if scen_file != self._scene_file:
            self._scene_file = scen_file
            self.load_instances(map_width, map_height)

        if self._shuffle:
            from random import choice
            values = [x[0] for x in self._scene_instances]
            random_value = choice(tuple(set(values)))
            idx = values.index(random_value)
            self._scene_instances = self._scene_instances[idx:] + self._scene_instances[:idx-1]
            self._shuffle = False

        instances = [((i[4], i[5]), (i[6], i[7])) for i in self._scene_instances]
        for start, goal in instances:
            assert (start not in occupancy_list), "Overlapping error"
            assert (goal not in occupancy_list), "Overlapping error"
        return instances[:n_of_agents]

    def shuffle_instances(self):
        self._shuffle = True

    def load_instances(self, map_width, map_height):
        if not os.path.isfile(self._scene_file):
            print("Scenario file not found!")
            exit(-1)
        ls = open(self._scene_file, 'r').readlines()
        if "version 1" not in ls[0]:
            print(".scen version type does not match!")
            exit(-1)
        self._scene_instances = [convert_nums(l.split('\t')) for l in ls[1:]]
        self._scene_instances.sort(key=lambda e: e[0])

        for i in self._scene_instances:
            assert (i[2] == map_width)
            assert (i[3] == map_height)



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
