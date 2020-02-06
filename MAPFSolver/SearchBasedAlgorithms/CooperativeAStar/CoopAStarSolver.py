from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.AStar import AStar
import time


class CoopAStarSolver(AbstractSolver):
    """
    Cooperative A* (CA*) is a an (not optimal!) algorithm for solving the Co-operative Path-finding problem.
    The task is decoupled into a series of single agent searches. The individual searches
    are performed in three dimensional space-time, and take account of the planned routes of other agents.
    A wait move is included in the agent’s action set, to enable it to remain stationary.
    After each agent’s route is calculated, the states along the route are marked into a reservation table.
    Entries in the reservation table are considered impassable and are avoided during searches by subsequent agents.
    The reservation table represents the agents’ shared knowledge about each other’s planned routes.
    It is a sparse data structure marking off regions of space-time.
    A simple implementation, used here, is to treat the reservation table as a 3-dimensional grid (two spatial dimensions
    and one time dimension). Each cell of the grid that is intersected by the agent’s planned route is marked as impassable
    for precisely the duration of the intersection, thus preventing any other agent from planning a colliding route. Only a
    small proportion of grid locations will be touched, and so the grid can be efficiently implemented as a hash table,
    hashing on a randomly distributed function of the (x, y, t) key.
    """
    def __init__(self, solver_settings):
        """
        Initialize the Cooperative A* solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._reservation_table = None
        self._completed_pos = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the MAPF problem using the Cooperative A* algorithm returning the paths as lists of list of (x, y)
        positions.
        """
        start = time.time()

        self._reservation_table = dict()
        self._completed_pos = []
        paths = []

        for i, agent in enumerate(problem_instance.get_agents()):
            if verbose:
                print("Agent n:", i+1, "of", len(problem_instance.get_agents()))

            solver = AStar(self._solver_settings)
            path = solver.find_path_with_reservation_table(problem_instance.get_map(), agent.get_start(),
                                                           agent.get_goal(), self._reservation_table,
                                                           self._completed_pos)
            paths.append(path)

            print("PATH", path)

            for j, pos in enumerate(path):
                if not self._reservation_table.get(pos):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(j)

            if self._solver_settings.stay_in_goal():
                self._completed_pos.append(path[len(path)-1])

        soc = calculate_soc(paths, self._solver_settings.stay_in_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(paths, self._solver_settings.stay_in_goal(),
                                      self._solver_settings.get_goal_occupation_time())
        output_infos = self.generate_output_infos(soc, makespan, 0, 0, time.time() - start)

        if verbose:
            print("PROBLEM SOLVED: ", output_infos)

        if return_infos:
            return paths, output_infos
        return paths

    def __str__(self):
        return "Cooperative A* Solver using " + self._solver_settings.get_heuristic_str()\
               + " heuristics"
