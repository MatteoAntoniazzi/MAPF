from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.AStar import AStar
from threading import Thread, Event
import time


class CooperativeAStarSolver(AbstractSolver):
    """
    Cooperative A* solver. If used with the AbstractDistance heuristics, it is the Hierarchical Cooperative A*.
    """

    def __init__(self, solver_settings):
        """
        Initialize the Cooperative A* solver.
        :param solver_settings: settings used by the Cooperative A* solver.
        """
        super().__init__(solver_settings)
        self._reservation_table = None
        self._completed_pos = None
        self._solution = []

        self._stop_event = None

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the given MAPF problem with the Cooperative A* algorithm and it returns, if exists, a solution.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        :return the solution as list of paths, and, if return_infos is True, a tuple composed by the solution and a
        struct with output information.
        """
        self._stop_event = Event()
        start = time.time()

        thread = Thread(target=self.solve_problem, args=(problem_instance, verbose,))
        thread.start()
        thread.join(timeout=self._solver_settings.get_time_out())
        self._stop_event.set()

        soc = calculate_soc(self._solution, self._solver_settings.stay_at_goal(),
                            self._solver_settings.get_goal_occupation_time())
        makespan = calculate_makespan(self._solution, self._solver_settings.stay_at_goal(),
                                      self._solver_settings.get_goal_occupation_time())

        output_infos = self.generate_output_infos(soc, makespan, 0, 0,
                                                  time.time() - start)
        if verbose:
            print("Problem ended: ", output_infos)

        return self._solution if not return_infos else (self._solution, output_infos)

    def solve_problem(self, problem_instance, verbose=False):
        """
        Solve the given MAPF problem using the Cooperative A* algorithm.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        """
        self._reservation_table = dict()
        self._completed_pos = []

        paths = []
        for i, agent in enumerate(problem_instance.get_agents()):

            if self._stop_event.is_set():
                break

            if verbose:
                print("Agent n:", i, "of", len(problem_instance.get_agents()))

            solver = AStar(self._solver_settings)
            path = solver.find_path_with_reservation_table(problem_instance.get_map(), agent.get_start(),
                                                           agent.get_goal(), self._reservation_table,
                                                           self._completed_pos)
            if not path:
                paths.append([])
                path = [agent.get_start()]
            else:
                paths.append(path)

            for j, pos in enumerate(path):
                if not self._reservation_table.get(pos):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(j)
                self._reservation_table[pos].sort()
            if self._solver_settings.stay_at_goal():
                self._completed_pos.append(path[-1])

            """print("Path:", path)
            print("Reservation table:", self._reservation_table)
            print("Completed pos:", self._completed_pos)"""

        self._solution = paths

    def __str__(self):
        return "Cooperative A* Solver using " + self._solver_settings.get_heuristic_str() + " heuristics"
