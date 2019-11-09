from Solvers.MAPFSolver import MAPFSolver
from States.ODState import ODState
from States.SingleAgentState import SingleAgentState
from QueueStructures.MultiAgentQueue import MultiAgentQueue
from Heuristics.initialize_heuristics import initialize_heuristics


class AStarOD(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False):
        """
        Solve the MAPF problem using the A* algorithm with Operator Decomposition returning the path as list of (x, y)
        positions.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                      " Total time: ", cur_state.time_step(), " Total cost:", cur_state.g_value())
                return cur_state.get_paths_to_parent()

            if not self._closed_list.contains_state(cur_state):
                if cur_state.is_a_standard_state():
                    self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand(verbose)
                self._n_of_expanded_nodes += len(expanded_nodes)
                self._n_of_loops += 1
                self._frontier.add_list_of_states(expanded_nodes)

        return []

    def initialize_problem(self, problem_instance):
        self._heuristics = initialize_heuristics(self._heuristics_str, problem_instance)
        self._frontier = MultiAgentQueue()
        self._closed_list = MultiAgentQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        single_agents_states = []
        for i, agent in enumerate(problem_instance.get_agents()):
            s = SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(), agent.get_start(), 0,
                                 heuristics=self._heuristics)
            single_agents_states.append(s)

        starter_state = ODState(problem_instance, single_agents_states, self._heuristics)
        self._frontier.add(starter_state)
