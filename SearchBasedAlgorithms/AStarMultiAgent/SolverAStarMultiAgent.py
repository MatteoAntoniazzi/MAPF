"""
Classical A* multi agent algorithm. It is complete and optimal.
"""
from Utilities.MAPFSolver import MAPFSolver
from Utilities.StatesQueue import StatesQueue
from Utilities.SingleAgentState import SingleAgentState
from SearchBasedAlgorithms.AStarMultiAgent.MultiAgentState import MultiAgentState
from Heuristics.initialize_heuristics import *
import time


class SolverAStarMultiAgent(MAPFSolver):
    def __init__(self, solver_settings):
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the A* algorithm returning the paths as lists of list of (x, y) positions.
        """
        start = time.time()

        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.time_step()-1, " Total cost:", cur_state.g_value())

                if return_infos:
                    output_infos = {
                        "sum_of_costs": cur_state.g_value(),
                        "makespan": cur_state.time_step()-1,
                        "expanded_nodes": self._n_of_expanded_nodes,
                        "computation_time": time.time() - start
                    }
                    return cur_state.get_paths_to_parent(), output_infos

                return cur_state.get_paths_to_parent()

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
        self._heuristics = initialize_heuristics(self._solver_settings.get_heuristics_str(), problem_instance)
        self._frontier = StatesQueue()
        self._closed_list = StatesQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        single_agents_states = []
        for i, agent in enumerate(problem_instance.get_agents()):
            s = SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(), agent.get_start(), 0,
                                 self._heuristics, self._solver_settings.get_goal_occupation_time())
            single_agents_states.append(s)

        starter_state = MultiAgentState(problem_instance, single_agents_states, self._heuristics,
                                        self._solver_settings.get_objective_function(),
                                        is_edge_conflict=self._solver_settings.get_edge_conflicts())
        self._frontier.add(starter_state)

    def __str__(self):
        return "A* Multi Agent Solver using " + self._solver_settings.get_heuristics_str() + \
               " heuristics minimazing " + self._solver_settings.get_objective_function()
