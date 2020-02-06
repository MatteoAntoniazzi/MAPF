import os
import pathlib
import numpy as np


# Dictionary Map Number and corresponding String
MAPS_NAMES_LIST = {
    0: "Berlin_1_256",
    1: "Boston_0_256",
    2: "brc202d",
    3: "den312d",
    4: "den520d",
    5: "empty-8-8",
    6: "empty-16-16",
    7: "empty-32-32",
    8: "empty-48-48",
    9: "ht_chantry",
    10: "ht_mansion_n",
    11: "lak303d",
    12: "lt_gallowstemplar_n",
    13: "maze-32-32-2",
    14: "maze-32-32-4",
    15: "maze-128-128-2",
    16: "maze-128-128-10",
    17: "orz900d",
    18: "ost003d",
    19: "Paris_1_256",
    20: "random-32-32-10",
    21: "random-32-32-20",
    22: "random-64-64-10",
    23: "random-64-64-20",
    24: "room-32-32-4",
    25: "room-64-64-8",
    26: "room-64-64-16",
    27: "w_woundedcoast",
    28: "narrow_corridor"
}


class Reader:
    """
    This class takes care of the loading of map and agents from the corresponding map files and scene files.
    In order to load a certain file the methods set_map(), set_scene_type() and set_scene_file_number() must be called
    before calling the corresponding load_map_file() or load_scenario_file().
    """

    def __init__(self, map_number=0, scene_type="even", scene_file_number=1):
        """
        Initialize a reader object.
        :param map_number: map number to load.
        :param scene_type: scene type to load.
        :param scene_file_number: scene file number to load.
        """
        self._map_number = map_number
        self._scene_type = scene_type
        self._scene_file_number = scene_file_number

        self._reload_instances = True  # If False it loads scene instances already loaded
        self._change_scene_instances = False

        self._scene_instances = None

    def load_map_file(self, occupied_char='@', valid_chars={'@', '.', 'T'}):
        """
        Load the map infos from a .map file.
        :param occupied_char: Char representing an occupied cell.
        :param valid_chars: chars valid in the map file.
        :return: width of the map, height of the map and the list of the obstacles in the map.
        """
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
        Load a set of agents from scenario file. This method keep into account those class variables:
        - self._map_number: in order to find the corresponding scene file.
        - self._scene_type: the scene files can be Even or Random.
        - self._scene_file_number: number of the scene file to pick.
        - self._reload_instances: this is False if I want to use the already loaded instances. If I've changed map or
                                  scene this will be True since the instances need to be reloaded. This variable is
                                  useful in order to keep into memory the last instances that could have been loaded
                                  randomly.
        - self._change_scene_instances: is True if I want to select another bucket of agents from the scene file (if
                                        Even) or another random bucket from the scene file(if Random).
        :param occupancy_lst: list of the obstacles.
        :param map_width: width of the map.
        :param map_height: height of the map.
        :param n_of_agents: number of agents to return.
        :return: array of start and destination couples. (Agents starts and goals)
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

            elif self._scene_type == "random":
                np.random.shuffle(self._scene_instances)

            self._change_scene_instances = False

        instances = [((i[4], i[5]), (i[6], i[7])) for i in self._scene_instances]
        for start, goal in instances:
            assert(start not in occupancy_lst), "Overlapping error"
            assert(goal not in occupancy_lst), "Overlapping error"
        return instances[:n_of_agents]

    def change_scene_instances(self):
        """
        Call this method every time I want to change the agent selected in the scene file. It will set the corresponding
        variable to True in order to load a different bucket when the scenario file is loaded.
        """
        self._change_scene_instances = True

    def load_instances(self, scene_file_path, map_width, map_height):
        """
        Load the instances from the scene file.
        :param scene_file_path: path of the scene file to load.
        :param map_width: width of the map.
        :param map_height: height of the map.
        """
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
        """
        Set the map number to load.
        :param map_number: map number to set.
        """
        self._map_number = map_number
        self._reload_instances = True

    def set_scene_type(self, scene_type):
        """
        Set the scene type to load.
        :param scene_type:
        """
        self._scene_type = scene_type
        self._reload_instances = True

    def set_scene_file_number(self, scene_file_number):
        """
        Set the scene file number to load.
        :param scene_file_number: scene file number to set.
        """
        self._scene_file_number = scene_file_number
        self._reload_instances = True


def convert_nums(lst):
    """
    Convert list of strings into nums.
    :param lst: string to convert.
    :return: list of int or float.
    """
    for i in range(len(lst)):
        try:
            lst[i] = int(lst[i])
        except ValueError:
            try:
                lst[i] = float(lst[i])
            except ValueError:
                ""
    return lst


def get_scene_file_path(map_number, scene_type, scene_number):
    map_name = MAPS_NAMES_LIST.get(map_number)
    root_path = pathlib.Path(__file__).parent.parent
    scene_file_path = str(root_path / "Maps/scenes-") + scene_type + "/" + map_name + "-" + scene_type + "-" + str(
        scene_number) + ".scen"
    print(scene_file_path)
    return scene_file_path

    # def setup_args(self):
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("map", type=str, help=".map Map file")
    #     parser.add_argument("scenario", type=str, help=".scen Scenario file")
    #     return parser.parse_args()