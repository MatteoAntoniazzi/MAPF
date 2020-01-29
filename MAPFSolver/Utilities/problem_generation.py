from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.Agent import Agent
from MAPFSolver.Utilities.Map import Map
import random


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
    problem_map = get_map(reader)
    problem_agents = get_agents(reader, problem_map, n_of_agents)
    return ProblemInstance(problem_map, problem_agents)


def generate_random_map(map_width, map_height, obstacle_probability):
    """
    Generate a random map width x height, and for each cell the probability of being an obstacle is given by obstacle
    probability
    :param map_width: desired map width.
    :param map_height: desired map height.
    :param obstacle_probability: probability for a cell of being an obstacle.
    :return: an instance of Map
    """
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


def get_map(reader):
    """
    Return the map object given the number of the chosen map.
    """
    print("Loading map...")
    map_width, map_height, occupancy_list = reader.load_map_file()
    print("Map loaded.")

    return Map(map_height, map_width, occupancy_list)


def get_agents(reader, problem_map, n_of_agents):
    """
    Return the Agent list for the specified scene number of the given map and the selected number of agents.
    """
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
