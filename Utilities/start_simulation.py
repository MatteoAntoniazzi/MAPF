from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarMultiAgent import SolverAStarMultiAgent
from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarOD import SolverAStarOD
from SearchBasedAlgorithms.CooperativeAStar.SolverCooperativeAStar import SolverCooperativeAStar
from SearchBasedAlgorithms.ConflictBasedSearch.SolverConflictBasedSearch import SolverConflictBasedSearch
from SearchBasedAlgorithms.IndependenceDetection.SolverIndependenceDetection import SolverIndependenceDetection
from SearchBasedAlgorithms.IncreasingCostTreeSearch.SolverIncreasingCostTreeSearch import SolverIncreasingCostTreeSearch
from SearchBasedAlgorithms.MStar.SolverMStar import SolverMStar
from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.Map import *
import time


def start_simulation(algorithm, independence_detection, map_number, heuristic, objective_function):
    map = get_map(map_number)

    agents = get_agents(map_number, map)

    problem_instance = ProblemInstance(map, agents)

    start_time = time.time()

    solver = get_solver(algorithm, heuristic, independence_detection)
    paths = solver.solve(problem_instance, verbose=True)

    print("Precessed Time {:.2f} seconds.".format(time.time() - start_time))

    print(paths)

    # problem_instance.plot_on_terminal(paths)
    problem_instance.plot_on_gui(paths)


def get_solver(algorithm, heuristics, independence_detection):
    switcher = {
        "Cooperative A*": SolverCooperativeAStar(heuristics),
        "A*": SolverAStarMultiAgent(heuristics),
        "A* with Operator Decomposition": SolverAStarOD(heuristics),
        "Increasing Cost Tree Search": SolverIncreasingCostTreeSearch(heuristics),
        "Conflict Based Search": SolverConflictBasedSearch(heuristics),
        "M*": SolverMStar(heuristics)
    }
    if independence_detection:
        return SolverIndependenceDetection(switcher.get(algorithm))
    else:
        return switcher.get(algorithm)


def get_map(map_number):
    switcher = {
        0: "Maps/maps/room-32-32-4.map",
        1: "Maps/narrow_corridor.map"
    }
    print(map_number)
    print(switcher.get(map_number))

    print("Loading map")
    map_width, map_height, occupancy_list = load_map_file(switcher.get(map_number))
    print("Map loaded")

    return Map(map_height, map_width, occupancy_list)


def get_agents(scene_number, map):
    switcher = {
        0: "Maps/scenes-even/room-32-32-4-even-1.scen",
        1: "Maps/narrow_corridor.scen"
    }

    print("Loading scenario file")
    agents = load_scenario_file(switcher.get(scene_number), map.get_obstacles_xy(), map.get_width(), map.get_height(), 10)
    print("Scenario loaded")

    return [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

