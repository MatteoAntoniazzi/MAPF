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


def prepare_simulation(start_menu, frame, algorithm, independence_detection, map_number, solver_settings, objective_function, n_of_agents):

    print(solver_settings)

    map = get_map(map_number)
    agents = get_agents(map_number, map, n_of_agents)
    problem_instance = ProblemInstance(map, agents)

    start_time = time.time()

    solver = get_solver(algorithm, solver_settings, objective_function, independence_detection)
    print("Solver --> ", solver)
    paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)

    print("Precessed Time {:.2f} seconds.".format(time.time() - start_time))

    problem_instance.plot_on_gui(start_menu, frame, paths, output_infos)


def get_solver(algorithm, solver_settings, objective_function, independence_detection):
    switcher = {
        "Cooperative A*": SolverCooperativeAStar(solver_settings, objective_function),
        "A*": SolverAStarMultiAgent(solver_settings, objective_function),
        "A* with Operator Decomposition": SolverAStarOD(solver_settings, objective_function),
        "Increasing Cost Tree Search": SolverIncreasingCostTreeSearch(solver_settings, objective_function),
        "Conflict Based Search": SolverConflictBasedSearch(solver_settings, objective_function),
        "M*": SolverMStar(solver_settings, objective_function)
    }
    if independence_detection:
        return SolverIndependenceDetection(switcher.get(algorithm), solver_settings, objective_function)
    else:
        return switcher.get(algorithm)


def get_map(map_number):
    switcher = {
        0: "Maps/maps/Berlin_1_256.map",
        1: "Maps/maps/Boston_0_256.map",
        2: "Maps/maps/brc202d.map",
        3: "Maps/maps/den312d.map",
        4: "Maps/maps/den520d.map",
        5: "Maps/maps/empty-8-8.map",
        6: "Maps/maps/empty-16-16.map",
        7: "Maps/maps/empty-32-32.map",
        8: "Maps/maps/empty-48-48.map",
        9: "Maps/maps/ht_chantry.map",
        10: "Maps/maps/ht_mansion_n.map",
        11: "Maps/maps/lak303d.map",
        12: "Maps/maps/lt_gallowstemplar_n.map",
        13: "Maps/maps/maze-32-32-2.map",
        14: "Maps/maps/maze-32-32-4.map",
        15: "Maps/maps/maze-128-128-2.map",
        16: "Maps/maps/maze-128-128-10.map",
        17: "Maps/maps/orz900d.map",
        18: "Maps/maps/ost003d.map",
        19: "Maps/maps/Paris_1_256.map",
        20: "Maps/maps/random-32-32-10.map",
        21: "Maps/maps/random-32-32-20.map",
        22: "Maps/maps/random-64-64-10.map",
        23: "Maps/maps/random-64-64-20.map",
        24: "Maps/maps/room-32-32-4.map",
        25: "Maps/maps/room-64-64-8.map",
        26: "Maps/maps/room-64-64-16.map",
        27: "Maps/maps/w_woundedcoast.map",
        28: "Maps/maps/narrow_corridor.map"
    }
    print(map_number)
    print(switcher.get(map_number))

    print("Loading map")
    map_width, map_height, occupancy_list = load_map_file(switcher.get(map_number))
    print("Map loaded")

    return Map(map_height, map_width, occupancy_list)


def get_agents(scene_number, map, n_of_agents):
    switcher = {
        0: "Maps/scenes/Berlin_1_256-even-1.scen",
        1: "Maps/scenes/Boston_0_256-even-1.scen",
        2: "Maps/scenes/brc202d-even-1.scen",
        3: "Maps/scenes/den312d-even-1.scen",
        4: "Maps/scenes/den520d-even-1.scen",
        5: "Maps/scenes/empty-8-8-even-1.scen",
        6: "Maps/scenes/empty-16-16-even-1.scen",
        7: "Maps/scenes/empty-32-32-even-1.scen",
        8: "Maps/scenes/empty-48-48-even-1.scen",
        9: "Maps/scenes/ht_chantry-even-1.scen",
        10: "Maps/scenes/ht_mansion_n-even-1.scen",
        11: "Maps/scenes/lak303d-even-1.scen",
        12: "Maps/scenes/lt_gallowstemplar_n-even-1.scen",
        13: "Maps/scenes/maze-32-32-2-even-1.scen",
        14: "Maps/scenes/maze-32-32-4-even-1.scen",
        15: "Maps/scenes/maze-128-128-2-even-1.scen",
        16: "Maps/scenes/maze-128-128-10-even-1.scen",
        17: "Maps/scenes/orz900d-even-1.scen",
        18: "Maps/scenes/ost003d-even-1.scen",
        19: "Maps/scenes/Paris_1_256-even-1.scen",
        20: "Maps/scenes/random-32-32-10-even-1.scen",
        21: "Maps/scenes/random-32-32-20-even-1.scen",
        22: "Maps/scenes/random-64-64-10-even-1.scen",
        23: "Maps/scenes/random-64-64-20-even-1.scen",
        24: "Maps/scenes/room-32-32-4-even-1.scen",
        25: "Maps/scenes/room-64-64-8-even-1.scen",
        26: "Maps/scenes/room-64-64-16-even-1.scen",
        27: "Maps/scenes/w_woundedcoast-even-1.scen",
        28: "Maps/scenes/narrow_corridor.scen"
    }

    print("Loading scenario file")
    agents = load_scenario_file(switcher.get(scene_number), map.get_obstacles_xy(), map.get_width(), map.get_height(),
                                number_of_agents=n_of_agents)
    print("Scenario loaded")

    return [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

