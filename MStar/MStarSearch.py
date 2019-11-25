from Utilities.MAPFSolver import MAPFSolver
from MStar.MStarQueue import MStarQueue
from MStar.MStarState import MStarState
from AStarMultiAgent.SingleAgentState import SingleAgentState
from Heuristics.initialize_heuristics import initialize_heuristics


class MStarSearch(MAPFSolver):
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)
        self._frontier = None
        self._closed_list = None
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

    def solve(self, problem_instance, verbose=False, print_output=True):
        """
        Solve the MAPF problem using the A* algorithm returning the path as list of (x, y) positions.
        """
        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_f_value()
            cur_state = self._frontier.pop()

            if cur_state.is_completed():
                if print_output:
                    print("Total Expanded Nodes: ", self._n_of_expanded_nodes, " Number of loops: ", self._n_of_loops,
                          " Total time: ", cur_state.time_step(), " Total cost:", cur_state.g_value())
                return cur_state.get_paths_to_parent()

            # if not self._closed_list.contains_state(cur_state):
            #     self._closed_list.add(cur_state)
            expanded_nodes = cur_state.expand(verbose=verbose)
            for node in expanded_nodes:
                self.back_propagate(cur_state, node)
                if len(node.get_collisions_set()) == 0:
                    self._frontier.add(node)
                    self._n_of_expanded_nodes += 1
            self._n_of_loops += 1

        return []

    def back_propagate(self, vk, vl):   # vk is the previous state, vl is the expanded state
        cl = vl.get_collisions_set()
        ck = vk.get_collisions_set()

        if not cl.issubset(ck):
            vk.set_collisions_set(ck.union(cl))
            if not self._frontier.contains_state(vk):
                self._frontier.add(vk)

            for vm in vk.get_back_propagation_set():
                self.back_propagate(vm, vk)

    def initialize_problem(self, problem_instance):
        self._heuristics = initialize_heuristics(self._heuristics_str, problem_instance)
        self._frontier = MStarQueue()
        self._closed_list = MStarQueue()
        self._n_of_expanded_nodes = 0
        self._n_of_loops = 0

        single_agents_states = []
        for i, agent in enumerate(problem_instance.get_agents()):
            s = SingleAgentState(problem_instance.get_map(), agent.get_id(), agent.get_goal(), agent.get_start(), 0,
                                 self._heuristics)
            single_agents_states.append(s)

        starter_state = MStarState(problem_instance, single_agents_states, self._heuristics)
        self._frontier.add(starter_state)
