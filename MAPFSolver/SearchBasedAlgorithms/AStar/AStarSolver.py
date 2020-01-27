"""
Classical A* multi agent algorithm. It is complete and optimal.
"""
from MAPFSolver.Utilities.MAPFSolver import MAPFSolver
from Utilities.StatesQueue import StatesQueue
from MAPFSolver.Utilities.SingleAgentState import SingleAgentState
from MAPFSolver.SearchBasedAlgorithms.AStar.MultiAgentState import MultiAgentState
import time


class AStarSolver(MAPFSolver):
    def __init__(self, solver_settings):
        """
        Initialize the A* solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Solve the MAPF problem using the A* algorithm returning the paths as lists of list of (x, y) positions.
        """
        start = time.time()

        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                paths = cur_state.get_paths_to_parent()
                output_infos = self.generate_output_infos(cur_state.g_value(), cur_state.time_step() - 1,
                                                          self._n_of_expanded_nodes, time.time() - start)
                if verbose:
                    print("PROBLEM SOLVED: ", output_infos)

                if return_infos:
                    return paths, output_infos
                else:
                    return paths

            if not self._closed_list.contains_state(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand(verbose=verbose)
                self._n_of_expanded_nodes += len(expanded_nodes)
                self._n_of_loops += 1
                self._frontier.add_list_of_states(expanded_nodes)

        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the heuristic for the given problem.
        """
        self._solver_settings.initialize_heuristic(problem_instance)
        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        single_agents_states = []
        for i, agent in enumerate(problem_instance.get_agents()):
            s = SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(), agent.get_start(), 0,
                                 self._solver_settings)
            single_agents_states.append(s)

        starter_state = MultiAgentState(single_agents_states, self._solver_settings)
        self._frontier.add(starter_state)

    def __str__(self):
        return "A* Multi Agent Solver using " + self._solver_settings.get_heuristics_str() + \
               " heuristics minimizing " + self._solver_settings.get_objective_function()
