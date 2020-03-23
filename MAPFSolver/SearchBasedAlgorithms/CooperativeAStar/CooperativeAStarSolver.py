from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.AStar import AStar
import time


class CooperativeAStarSolver(AbstractSolver):
    """
    Cooperative A* solver. If used with the AbstractDistance heuristics, it is the Hierarchical Cooperative A*.
    """

    def __init__(self, solver_settings):
        """
        Initialize the Cooperative A* solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._reservation_table = None
        self._completed_pos = None

    def solve(self, problem_instance, verbose=False, return_infos=False, time_out=None):
        """
        Solve the given MAPF problem using the Cooperative A* algorithm and, if exists, it returns a solution.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        :param time_out: max time for computing the solution. If the time is over it returns an empty solution.
        The time is expressed in milliseconds.
        :return the solution as list of paths, and, if return_infos is True, some output information.
        """
        start = time.time()

        self._reservation_table = dict()
        self._completed_pos = []

        paths = []
        for i, agent in enumerate(problem_instance.get_agents()):

            if time_out is not None:
                if time.time() - start > time_out:
                    return [] if not return_infos else ([], None)

            if verbose:
                print("Agent n:", i, "of", len(problem_instance.get_agents()))

            solver = AStar(self._solver_settings)
            path = solver.find_path_with_reservation_table(problem_instance.get_map(), agent.get_start(),
                                                           agent.get_goal(), self._reservation_table,
                                                           self._completed_pos)
            if not path:
                return [] if not return_infos else ([], None)

            paths.append(path)

            for j, pos in enumerate(path):
                if not self._reservation_table.get(pos):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(j)
            if self._solver_settings.stay_at_goal():
                self._completed_pos.append(path[-1])

        soc = calculate_soc(paths, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(paths, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())
        output_infos = self.generate_output_infos(soc, makespan, 0, 0, time.time() - start)

        if verbose:
            print("PROBLEM SOLVED: ", output_infos)

        return paths if not return_infos else (paths, output_infos)

    def __str__(self):
        return "Cooperative A* Solver using " + self._solver_settings.get_heuristic_str() + " heuristics"
