

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
    :param reader:
    :param n_of_agents:
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
    (max_n_of_agents - min_n_of_agents). For each k will have a set of k agents.
    Example: min is 2 and max is 3 and n_of_buckets is 3.
    Return: [[[a0, a1], [a2, a3], [a4, a5]], [[a10, a11, a12], [a13, a14, a15], [a16, a17, a18]]]
    :param problem_map: map of the problem where generate the agents.
    :param is_edge_conflicts: if True also the edge conflicts are considered.
    :param min_n_of_agents: minimum value of number of agent for which we want a bucket.
    :param max_n_of_agents: maximum value of number of agent for which we want a bucket.
    :param n_of_buckets: number of buckets for each number of agents.
    :return: k list of buckets of agents.
    """
    from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
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
            problem_agents = generate_random_agents(problem_map, int(max_n_of_agents * 2))
            problem_instance = ProblemInstance(problem_map, problem_agents)

            solver_settings = SolverSettings(stay_in_goal=True, is_edge_conflict=is_edge_conflicts)
            a_star_solver = AStarSolver(solver_settings)
            id_framework = IDFramework(a_star_solver, solver_settings)
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

    """for i, k in enumerate(buckets_of_agents):
        print("Num of agents:", i + min_n_of_agents)
        for j, b in enumerate(k):
            print("Bucket:", j)
            for a in b:
                print(a, ' ', end='')
            print('')"""

    return buckets_of_agents


def generate_random_agent_buckets(problem_map, min_n_of_agents, max_n_of_agents, n_of_buckets):
    """
    It returns a bucket of agent for all the desired number of agent k. The length of the list will be
    (max_n_of_agents - min_n_of_agents). For each k will have a set of k agents.
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

    agents = []
    agents_starts = []
    agents_goals = []
    for i in range(n_of_agents):
        while True:
            random_start = random.sample(free_lst, 1)[0]
            if random_start not in agents_starts and random_start not in agents_goals:
                agents_starts.append(random_start)
                break
        while True:
            random_goal = random.sample(free_lst, 1)[0]
            if random_goal not in agents_starts and random_goal not in agents_goals:
                agents_goals.append(random_goal)
                break
        agents.append(Agent(i, random_start, random_goal))

    return agents


def load_map(reader):
    """
    Return the map object given the number of the chosen map.
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
