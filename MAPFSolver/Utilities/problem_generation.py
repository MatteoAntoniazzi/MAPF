def generate_random_problem(map_width, map_height, obstacle_probability, n_of_agents):
    """
    Generate a random problem instance where map is width x height, and for each cell the probability of being an
    obstacle is given by obstacle probability. The agents are randomly generated and there's no agent that overlap his
    goal or start with another agent goal or start.
    :param map_width: desired map width.
    :param map_height: desired map height.
    :param obstacle_probability: probability for a cell of being an obstacle.
    :param n_of_agents: number of agents to generate.
    :return: an instance of ProblemInstance
    """
    from .ProblemInstance import ProblemInstance

    problem_map = generate_random_map(map_width, map_height, obstacle_probability)
    problem_agents = generate_random_agents(problem_map, n_of_agents)

    return ProblemInstance(problem_map, problem_agents)


def generate_problem_from_map_and_scene(reader, n_of_agents):
    """
    Generate a problem instance from map file and scene file inserted.
    :param reader: reader object.
    :param n_of_agents: number of agents to load.
    :return: an instance of ProblemInstance
    """
    from .ProblemInstance import ProblemInstance

    problem_map = load_map(reader)
    problem_agents = load_agents(reader, problem_map, n_of_agents)
    return ProblemInstance(problem_map, problem_agents)


def generate_agent_buckets_with_coupling_mechanism(problem_map, is_edge_conflicts, min_n_of_agents, max_n_of_agents,
                                                   n_of_buckets):
    """
    It returns a bucket of agent for all the desired number of agent k. The length of the list will be
    (max_n_of_agents - min_n_of_agents). For each k will have a set of n_of_buckets agents.
    Example: min is 2 and max is 3 and n_of_buckets is 3.
    Return: [[[a0, a1], [a2, a3], [a4, a5]], [[a10, a11, a12], [a13, a14, a15], [a16, a17, a18]]]
    :param problem_map: map of the problem where generate the agents.
    :param is_edge_conflicts: if True also the edge conflicts are considered.
    :param min_n_of_agents: minimum value of number of agent for which we want a bucket.
    :param max_n_of_agents: maximum value of number of agent for which we want a bucket.
    :param n_of_buckets: number of buckets for each number of agents.
    :return: k list of buckets of agents.
    """
    from MAPFSolver.SearchBasedAlgorithms.IDFramework import IDFramework
    from .SolverSettings import SolverSettings
    from .useful_functions import print_progress_bar
    from .ProblemInstance import ProblemInstance
    from .Agent import Agent

    print("Generate agent buckets with coupling mechanism...")

    n_of_free_cells = len(get_free_lst(problem_map))
    desired_range_length = max_n_of_agents + 1 - min_n_of_agents

    buckets_of_agents = []
    for i in range(desired_range_length):
        buckets_of_agents.append([])

    print_progress_bar(0, n_of_buckets, prefix='Progress:', suffix='Complete', length=50)
    for j in range(n_of_buckets):
        single_buckets_of_ids = []
        single_buckets_of_agents = []
        temp_min = min_n_of_agents

        while len(single_buckets_of_ids) < desired_range_length:

            problem_agents = generate_random_agents(problem_map, n_of_free_cells-1)
            problem_instance = ProblemInstance(problem_map, problem_agents)

            solver_settings = SolverSettings(heuristic="AbstractDistance", stay_at_goal=True,
                                             edge_conflict=is_edge_conflicts, time_out=300)
            id_framework = IDFramework("A*", solver_settings)
            returning_buckets_of_ids = id_framework.get_some_conflicting_ids_for_buckets(problem_instance, temp_min,
                                                                                         max_n_of_agents)

            if returning_buckets_of_ids:
                single_buckets_of_ids.extend(returning_buckets_of_ids)

                for bucket in returning_buckets_of_ids:
                    agent_list = []
                    for i, agent_id in enumerate(bucket):
                        agent_selected = problem_instance.get_original_agents()[agent_id]
                        agent_list.append(Agent(i, agent_selected.get_start(), agent_selected.get_goal()))
                    single_buckets_of_agents.append(agent_list)

                temp_min = min_n_of_agents if len(single_buckets_of_ids) == 0 else \
                    len(single_buckets_of_ids[len(single_buckets_of_ids) - 1]) + 1

        for c, bucket in enumerate(single_buckets_of_agents):
            buckets_of_agents[c].append(bucket)

        print_progress_bar(j+1, n_of_buckets, prefix='Progress:', suffix='Complete', length=50)

    print("Buckets generated.")

    return buckets_of_agents


def generate_random_agent_buckets(problem_map, min_n_of_agents, max_n_of_agents, n_of_buckets):
    """
    It returns a bucket of agent for all the desired number of agent k. The length of the list will be
    (max_n_of_agents - min_n_of_agents). For each k will have a set of n_of_buckets agents.
    Example: min is 2 and max is 3 and n_of_buckets is 3.
    Return: [[[a0, a1], [a2, a3], [a4, a5]], [[a10, a11, a12], [a13, a14, a15], [a16, a17, a18]]]
    :param problem_map: map of the problem where generate the agents.
    :param min_n_of_agents: minimum value of number of agent for which we want a bucket.
    :param max_n_of_agents: maximum value of number of agent for which we want a bucket.
    :param n_of_buckets: number of buckets for each number of agents.
    :return: k list of buckets of agents.
    """
    desired_range_length = max_n_of_agents + 1 - min_n_of_agents

    buckets_of_agents = []

    for i in range(desired_range_length):
        bucket = []
        for j in range(n_of_buckets):
            problem_agents = generate_random_agents(problem_map, i+min_n_of_agents)
            bucket.append(problem_agents)
        buckets_of_agents.append(bucket)

    return buckets_of_agents


def generate_random_map(map_width, map_height, obstacle_probability):
    """
    Generate a random map width x height, and for each cell the probability of being an obstacle is given by obstacle
    probability
    :param map_width: desired map width.
    :param map_height: desired map height.
    :param obstacle_probability: probability for a cell of being an obstacle.
    :return: an instance of Map
    """
    from .Map import Map
    import random

    occupancy_lst = set()
    free_lst = set()

    for x in range(map_width):
        for y in range(map_height):
            if random.random() < obstacle_probability:
                occupancy_lst.add((x, y))
            else:
                free_lst.add((x, y))

    return Map(map_height, map_width, occupancy_lst)


def generate_random_agents(problem_map, n_of_agents):
    """
    Generate n_of_agents random agents for the given map.
    :param problem_map: map of the problem where generate the agents.
    :param n_of_agents: desired number of agents to generate.
    :return: a list of Agent instances.
    """
    from .Agent import Agent
    import random

    free_lst = get_free_lst(problem_map)

    free_start_lst = list(free_lst.copy())
    free_goal_lst = list(free_lst.copy())

    agents = []

    for i in range(n_of_agents):
        assert free_start_lst and free_goal_lst, "No more free spaces for placing the agents..."

        """random_start = random.sample(free_start_lst, 1)[0]
        free_start_lst.remove(random_start)

        random_goal = random.sample(free_goal_lst, 1)[0]
        free_goal_lst.remove(random_goal)"""

        r = random.randrange(len(free_start_lst))
        random_start = free_start_lst[r]
        free_start_lst.remove(random_start)

        r = random.randrange(len(free_goal_lst))
        random_goal = free_goal_lst[r]
        free_goal_lst.remove(random_goal)

        agents.append(Agent(i, random_start, random_goal))

    return agents


def load_map_from_file(file_path):
    """
    Load the map infos from a .map file.
    :param file_path: path of the file to load.
    :return: a Map object.
    """
    import os
    from .Map import Map

    occupied_char = '@'
    valid_chars = {'@', '.', 'T'}

    if not os.path.isfile(file_path):
        print("Map file not found!")
        exit(-1)
    map_ls = open(file_path, 'r').readlines()
    height = int(map_ls[1].replace("height ", ""))
    width = int(map_ls[2].replace("width ", ""))
    map_ls = map_ls[4:]
    map_ls = [l.replace('\n', '') for l in map_ls]
    occupancy_lst = set()
    assert (len(map_ls) == height)
    for y, l in enumerate(map_ls):
        assert (len(l) == width)
        for x, c in enumerate(l):
            assert (c in valid_chars)
            if c == occupied_char:
                occupancy_lst.add((x, y))

    return Map(height, width, occupancy_lst)


def load_scenario(scene_file_path, map_width, map_height, occupancy_lst, n_of_agents=10):
    """
    Load the instances from the scene file. It Returns a list of n agents.
    :param scene_file_path: path of the scene file to load.
    :param map_width: width of the map.
    :param map_height: height of the map.
    :param occupancy_lst: list of the obstacles in the map.
    :param n_of_agents: number of agents to return.
    """
    import os
    from .Agent import Agent

    if not os.path.isfile(scene_file_path):
        print("Scenario file not found!")
        exit(-1)
    ls = open(scene_file_path, 'r').readlines()
    if "version 1" not in ls[0]:
        print(".scen version type does not match!")
        exit(-1)
    scene_instances = [convert_nums(l.split('\t')) for l in ls[1:]]
    scene_instances.sort(key=lambda e: e[0])

    for i in scene_instances:
        assert (i[2] == map_width)
        assert (i[3] == map_height)

    instances = [((i[4], i[5]), (i[6], i[7])) for i in scene_instances]
    for start, goal in instances:
        assert(start not in occupancy_lst), "Overlapping error"
        assert(goal not in occupancy_lst), "Overlapping error"
    return [Agent(i, a[0], a[1]) for i, a in enumerate(instances[:n_of_agents])]


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


def load_map(reader):
    """
    Return the map object given the number of the chosen map.
    :param reader: Reader object.
    :return: a Map object.
    """
    from .Map import Map

    print("Loading map...")
    map_width, map_height, occupancy_list = reader.load_map_file()
    print("Map loaded.")

    return Map(map_height, map_width, occupancy_list)


def load_agents(reader, problem_map, n_of_agents):
    """
    Return the Agent list for the specified scene number of the given map and the selected number of agents.
    """
    from .Agent import Agent

    print("Loading scenario file...")
    agents = reader.load_scenario_file(problem_map.get_obstacles_xy(), problem_map.get_width(),
                                       problem_map.get_height(), n_of_agents=n_of_agents)
    print("Scenario loaded.")

    return [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]


def get_free_lst(problem_map):
    """
    Given a map it returns the list of free positions. (no obstacle cells)
    :param problem_map: map of the problem.
    :return: list of positions.
    """
    free_lst = set()

    for x in range(problem_map.get_width()):
        for y in range(problem_map.get_height()):
            if not (x, y) in problem_map.get_obstacles_xy():
                free_lst.add((x, y))

    return free_lst


"""def generate_problem_m_star_paper():
    from .Map import Map
    from .Agent import Agent
    from .ProblemInstance import ProblemInstance


    problem_map = Map(8, 8, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 7),
                             (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 7),
                             (1, 5), (2, 5), (4, 5), (5, 5), (6, 5), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)])

    problem_agents = [Agent(0, (1, 4), (6, 0)), Agent(1, (1, 6), (7, 6)), Agent(2, (6, 6), (0, 6))]

    return ProblemInstance(problem_map, problem_agents)"""
