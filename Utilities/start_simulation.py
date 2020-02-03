from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from MAPFSolver.SearchBasedAlgorithms.AStarOD.AStarODSolver import SolverAStarOD
from MAPFSolver.SearchBasedAlgorithms.CooperativeAStar.CoopAStarSolver import SolverCooperativeAStar
from MAPFSolver.SearchBasedAlgorithms.CBS.CBSSolver import CBSSolver
from MAPFSolver.SearchBasedAlgorithms.IDFramework import IDFramework
from SearchBasedAlgorithms.IncreasingCostTreeSearch.SolverIncreasingCostTreeSearch import SolverIncreasingCostTreeSearch
from SearchBasedAlgorithms.MStar.SolverMStar import SolverMStar
from MAPFSolver.Utilities.ProblemInstance import *
from MAPFSolver.Utilities.Agent import *
from MAPFSolver.Utilities.Map import *


def prepare_simulation(reader, frame, algorithm, independence_detection, solver_settings, n_of_agents):
    """
    Solve the MAPF problem and visualize the simulation on the frame.
    :param reader: Reader object for the loading of the map and the scen
    :param frame: Frame where the simulation will be displayed
    :param algorithm: String of the algorithm choose
    :param independence_detection: True if Independence Detection will be used with the algorithm
    :param solver_settings: Settings of the solver (heuristics, goal_occupation_time)
    :param n_of_agents: Number of Agents on the map
    """
    map = get_map(reader)
    agents = get_agents(reader, map, n_of_agents)
    problem_instance = ProblemInstance(map, agents)

    solver = get_solver(algorithm, solver_settings, independence_detection)
    print("Solver --> ", solver, "\nSolving...")
    paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)
    print("Solved.")

    problem_instance.plot_on_gui(frame, paths, output_infos)


def get_solver(algorithm, solver_settings, independence_detection):
    """
    Return the Solver object for the specified algorithm and relative settings.
    """
    switcher = {
        "Cooperative A*": SolverCooperativeAStar(solver_settings),
        "A*": AStarSolver(solver_settings),
        "A* with Operator Decomposition": SolverAStarOD(solver_settings),
        "Increasing Cost Tree Search": SolverIncreasingCostTreeSearch(solver_settings),
        "Conflict Based Search": CBSSolver(solver_settings),
        "M*": SolverMStar(solver_settings)
    }
    if independence_detection:
        return IDFramework(switcher.get(algorithm), solver_settings)
    else:
        return switcher.get(algorithm)


def get_map(reader):
    """
    Return the map object given the number of the choosen map.
    """
    print("Loading map...")
    map_width, map_height, occupancy_list = reader.load_map_file()
    print("Map loaded.")

    return Map(map_height, map_width, occupancy_list)


def get_agents(reader, map, n_of_agents):
    """
    Return the Agent list for the specified scene number of the given map and the selected number of agents.
    """
    print("Loading scenario file...")
    agents = reader.load_scenario_file(map.get_obstacles_xy(), map.get_width(), map.get_height(),
                                       n_of_agents=n_of_agents)
    print("Scenario loaded.")

    return [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

