"""
Classical A* multi agent algorithm. It is complete and optimal.
"""
from MAPFSolver.Utilities.AbstractSolver import MAPFSolver
from MAPFSolver.Utilities.StatesQueue import StatesQueue
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.SearchBasedAlgorithms.AStar.MultiAgentState import MultiAgentState
import time

from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan


class AStarSolver(MAPFSolver):
    def __init__(self, solver_settings):
        """
        Initialize the A* solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the MAPF problem using the A* algorithm returning the paths as lists of list of (x, y) positions.
        :param problem_instance: problem instance to solve
        :param verbose: if True will be printed some computation infos on terminal.
        :param return_infos: if True returns in addition to the paths a struct with the output information.
        :return: list of paths, and if return_infos is True some output information.
        """
        start = time.time()

        self.initialize_problem(problem_instance)
        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                paths = cur_state.get_paths_to_parent()
                soc = calculate_soc(paths, self._solver_settings.stay_in_goal(),
                                    self._solver_settings.get_goal_occupation_time())
                makespan = calculate_makespan(paths, self._solver_settings.stay_in_goal(),
                                              self._solver_settings.get_goal_occupation_time())
                output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes,
                                                          self._n_of_expanded_nodes, time.time()-start)
                if verbose:
                    print("PROBLEM SOLVED: ", output_infos)

                if return_infos:
                    return paths, output_infos
                return paths

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand(verbose=verbose)
                self._n_of_generated_nodes += len(expanded_nodes)
                self._n_of_expanded_nodes += 1
                self._frontier.add_list_of_states(expanded_nodes)

        if return_infos:
            return [], None
        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the heuristic for the given problem.
        """
        self._solver_settings.initialize_heuristic(problem_instance)
        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        single_agents_states = []
        for agent in problem_instance.get_agents():
            s = SingleAgentState(problem_instance.get_map(), agent.get_goal(), agent.get_start(), self._solver_settings)
            single_agents_states.append(s)

        starter_state = MultiAgentState(single_agents_states, self._solver_settings)
        self._frontier.add(starter_state)